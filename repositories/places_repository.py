from services.supabase_client import get_supabase
from utils.place_alias_normalize import normalize_place_alias

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
    client = get_supabase()
    try:
        result = client.rpc(
            "search_places_ranked",
            {"p_query": q, "p_norm": q_norm, "p_limit": lim},
        ).execute()
        rows = result.data or []
        if rows:
            return [_strip_search_meta(row) for row in rows]
    except Exception:
        pass
    return _search_places_fallback(q, lim)


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
