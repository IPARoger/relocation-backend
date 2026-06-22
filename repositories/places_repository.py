from services.supabase_client import get_supabase
from utils.place_alias_normalize import normalize_place_alias

import logging
import time
from threading import Lock

logger = logging.getLogger(__name__)

_SEARCH_CACHE_TTL_SEC = 180
_SEARCH_CACHE: dict[tuple[str, int], tuple[float, list]] = {}
_SEARCH_CACHE_LOCK = Lock()


def _search_cache_get(key: tuple[str, int]):
    with _SEARCH_CACHE_LOCK:
        entry = _SEARCH_CACHE.get(key)
        if not entry:
            return None
        ts, data = entry
        if time.monotonic() - ts > _SEARCH_CACHE_TTL_SEC:
            del _SEARCH_CACHE[key]
            return None
        return data


def _search_cache_set(key: tuple[str, int], data: list):
    with _SEARCH_CACHE_LOCK:
        _SEARCH_CACHE[key] = (time.monotonic(), data)


def _rpc_search_rows(client, fn: str, params: dict):
    result = client.rpc(fn, params).execute()
    return result.data or []



_PLACE_FIELDS = (
    "id",
    "provider",
    "provider_place_id",
    "geonames_id",
    "display_name",
    "canonical_name",
    "admin1",
    "admin2",
    "country_code",
    "country_name",
    "latitude",
    "longitude",
    "timezone_id",
    "population",
    "importance_rank",
    "language_code",
    "alternate_names_json",
    "source_json",
    "created_at",
    "updated_at",
)


def _strip_search_meta(row: dict) -> dict:
  out = {k: row[k] for k in _PLACE_FIELDS if k in row}
  matched = row.get("matched_alias")
  if matched:
      out["matched_alias"] = matched
  return out


def list_places(limit: int = 50):
    client = get_supabase()
    result = (
        client.table("places")
        .select("*")
        .order("display_name", desc=False)
        .limit(limit)
        .execute()
    )
    return result.data


def get_place(place_id: str):
    client = get_supabase()
    result = (
        client.table("places")
        .select("*")
        .eq("id", place_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def create_place(
    display_name: str,
    latitude: float,
    longitude: float,
    provider: str = None,
    provider_place_id: str = None,
    geonames_id: str = None,
    canonical_name: str = None,
    admin1: str = None,
    admin2: str = None,
    country_code: str = None,
    country_name: str = None,
    timezone_id: str = None,
    population: int = None,
    importance_rank: float = None,
    language_code: str = None,
    alternate_names_json: dict = None,
    source_json: dict = None,
):
    client = get_supabase()

    payload = {
        "display_name": display_name,
        "latitude": latitude,
        "longitude": longitude,
    }

    optional = {
        "provider": provider,
        "provider_place_id": provider_place_id,
        "geonames_id": geonames_id,
        "canonical_name": canonical_name,
        "admin1": admin1,
        "admin2": admin2,
        "country_code": country_code,
        "country_name": country_name,
        "timezone_id": timezone_id,
        "population": population,
        "importance_rank": importance_rank,
        "language_code": language_code,
        "alternate_names_json": alternate_names_json,
        "source_json": source_json,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = client.table("places").insert(payload).execute()
    return result.data[0] if result.data else None


def _search_places_fallback(query: str, limit: int):
    """Legacy display_name ILIKE when ranked RPC is unavailable."""
    client = get_supabase()
    pattern = f"%{query}%"
    result = (
        client.table("places")
        .select("*")
        .ilike("display_name", pattern)
        .order("importance_rank", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []


def search_places(query: str, limit: int = 20):
    q = str(query or "").strip()
    if not q:
        return []
    q_norm = normalize_place_alias(q)
    lim = max(1, min(int(limit or 20), 50))
    cache_key = (q_norm, lim)
    cached = _search_cache_get(cache_key)
    if cached is not None:
        logger.info(
            "places.search cache_hit query=%r norm=%r limit=%d n=%d",
            q,
            q_norm,
            lim,
            len(cached),
        )
        return cached

    t0 = time.perf_counter()
    client = get_supabase()
    rows = []
    stage = "fallback_table"
    fast_n = 0
    fallback_n = 0

    try:
        fast_rows = _rpc_search_rows(
            client,
            "search_places_ranked_fast",
            {"p_query": q, "p_norm": q_norm, "p_limit": lim},
        )
        fast_n = len(fast_rows)
        rows = list(fast_rows)
        if fast_n < lim:
            exclude = [row["id"] for row in fast_rows if row.get("id")]
            fallback_rows = _rpc_search_rows(
                client,
                "search_places_ranked_fallback",
                {
                    "p_query": q,
                    "p_norm": q_norm,
                    "p_limit": lim - fast_n,
                    "p_exclude": exclude,
                },
            )
            fallback_n = len(fallback_rows)
            rows.extend(fallback_rows)
        stage = "staged" if fallback_n else "staged_fast_only"
    except Exception:
        try:
            rows = _rpc_search_rows(
                client,
                "search_places_ranked",
                {"p_query": q, "p_norm": q_norm, "p_limit": lim},
            )
            stage = "legacy_ranked"
        except Exception:
            rows = []

    if not rows:
        rows = _search_places_fallback(q, lim)
        stage = "fallback_table"

    out = [_strip_search_meta(row) for row in rows]
    _search_cache_set(cache_key, out)
    total_ms = int((time.perf_counter() - t0) * 1000)
    logger.info(
        "places.search query=%r norm=%r limit=%d stage=%s fast=%d fallback=%d n=%d ms=%d",
        q,
        q_norm,
        lim,
        stage,
        fast_n,
        fallback_n,
        len(out),
        total_ms,
    )
    return out


def search_places_by_geonames(geonames_id: str):
    client = get_supabase()
    gid = str(geonames_id or "").strip()
    if not gid:
        return []
    try:
        result = (
            client.table("places")
            .select("*")
            .eq("geonames_id", gid)
            .limit(1)
            .execute()
        )
    except Exception:  # noqa: BLE001
        return []
    return result.data or []
