"""Phase 3.0b — local product store (file-only scaffold).

TEMPORARY_LOCAL_SCAFFOLD — not product storage, not connected to map or library.json.

Product language: Chart Record. Storage language: clients[] row (1:1 birth_profiles[]).
"""

from __future__ import annotations

import json
import os
import tempfile
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

APP_DIR = Path(__file__).resolve().parent
DEFAULT_STORE_PATH = APP_DIR / "scaffold" / "local_product" / "TEMPORARY_product_store.json"

STORAGE_SCHEMA_VERSION = 3
SUPABASE_MIRROR_VERSION = 1
STORAGE_MARKER = "TEMPORARY_LOCAL_SCAFFOLD"

RECORD_TYPES = frozenset({"self", "client", "research"})
HISTORY_EVENT_TYPES = frozenset({"map_search", "map_view", "place_inspect"})

FORBIDDEN_KEY_SUBSTRINGS = (
    "geojson",
    "renderer_substrate",
    "canvas",
    "aura",
    "virga",
    "cache",
    "debug",
)

DEFAULT_USER_SETTINGS: dict[str, Any] = {
    "settings_version": 1,
    "house_system": "placidus",
    "zodiac_mode": "tropical",
    "orb_defaults": {
        "conjunction": 10,
        "opposition": 10,
        "square": 8,
        "trine": 8,
        "sextile": 6,
    },
    "visible_minor_aspects": False,
    "helper_layers": {},
    "ontology_pack_id": None,
    "default_chart_record_id": None,
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


# --- Chart Record adapter (product language ↔ storage) ---


def list_chart_records(state: dict[str, Any]) -> list[dict[str, Any]]:
    """Chart Records are stored as clients[] rows."""
    return list(state.get("clients") or [])


def get_chart_record(state: dict[str, Any], chart_record_id: str) -> dict[str, Any] | None:
    for client in state.get("clients") or []:
        if isinstance(client, dict) and str(client.get("id")) == str(chart_record_id):
            return client
    return None


def chart_record_id(client: dict[str, Any]) -> str:
    return str(client["id"])


def get_default_chart_record_id(state: dict[str, Any]) -> str | None:
    settings = state.get("user_settings") or {}
    value = settings.get("default_chart_record_id")
    return str(value) if value else None


class ChartRecordBirthResolutionError(Exception):
    """Failed to resolve Store v3 Chart Record natal inputs to engine birth params."""

    def __init__(self, reason: str, message: str | None = None) -> None:
        self.reason = reason
        self.message = message or reason
        super().__init__(self.message)


def get_birth_profile_for_chart_record(
    state: dict[str, Any], chart_record_id: str
) -> dict[str, Any] | None:
    client = get_chart_record(state, chart_record_id)
    if client is None:
        return None
    birth_profiles = _index_by_id(state.get("birth_profiles") or [])
    bp_id = client.get("birth_profile_id")
    if not bp_id:
        return None
    return birth_profiles.get(str(bp_id))


def birth_profile_to_engine_params(
    birth_profile: dict[str, Any], *, chart_record_id: str | None = None
) -> dict[str, Any]:
    birth_date = birth_profile.get("birth_date")
    birth_time = birth_profile.get("birth_time")
    timezone_id = birth_profile.get("timezone_id")

    if birth_time is None or str(birth_time).strip() == "":
        raise ChartRecordBirthResolutionError(
            "birth_time_required",
            "Chart Record birth profile has no exact birth_time",
        )
    if not birth_date or not timezone_id:
        raise ChartRecordBirthResolutionError(
            "invalid_birth_data",
            "birth_date and timezone_id are required",
        )

    try:
        year_s, month_s, day_s = str(birth_date).split("-", 2)
        year, month, day = int(year_s), int(month_s), int(day_s)
        time_parts = str(birth_time).split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1]) if len(time_parts) > 1 else 0
        second = int(time_parts[2]) if len(time_parts) > 2 else 0
    except (TypeError, ValueError, IndexError) as exc:
        raise ChartRecordBirthResolutionError(
            "invalid_birth_data",
            f"invalid birth_date or birth_time: {birth_date!r} {birth_time!r}",
        ) from exc

    try:
        local_dt = datetime(
            year, month, day, hour, minute, second, tzinfo=ZoneInfo(str(timezone_id))
        )
    except Exception as exc:
        raise ChartRecordBirthResolutionError(
            "invalid_birth_data",
            f"invalid timezone_id: {timezone_id!r}",
        ) from exc

    utc_dt = local_dt.astimezone(timezone.utc)
    params: dict[str, Any] = {
        "birth_year": utc_dt.year,
        "birth_month": utc_dt.month,
        "birth_day": utc_dt.day,
        "birth_hour_utc": utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600,
    }
    if chart_record_id is not None:
        params["chart_record_id"] = chart_record_id
    return params


def resolve_engine_birth_params(
    state: dict[str, Any], chart_record_id: str
) -> dict[str, Any]:
    birth_profile = get_birth_profile_for_chart_record(state, chart_record_id)
    if birth_profile is None:
        raise ChartRecordBirthResolutionError(
            "chart_record_not_found",
            f"unknown chart_record_id: {chart_record_id}",
        )
    return birth_profile_to_engine_params(
        birth_profile, chart_record_id=str(chart_record_id)
    )


def _birth_time_display(birth_profile: dict[str, Any]) -> str:
    meta = birth_profile.get("confidence_metadata") or {}
    if meta.get("time_range_display") and birth_profile.get("birth_time") is None:
        return f"Time uncertain: {meta['time_range_display']}"
    if birth_profile.get("birth_time"):
        return str(birth_profile["birth_time"])
    return "Time unknown"


def _has_birth_time_uncertainty(birth_profile: dict[str, Any]) -> bool:
    tier = birth_profile.get("confidence_tier")
    if tier in ("T2", "T3", "T4"):
        return True
    return birth_profile.get("birth_time") is None and tier != "T0"


def summarize_chart_record(
    state: dict[str, Any], chart_record_id: str
) -> dict[str, Any] | None:
    """Read-only Chart Record summary for library UI (product language)."""
    client = get_chart_record(state, chart_record_id)
    if client is None:
        return None

    birth_profile = get_birth_profile_for_chart_record(state, chart_record_id)
    if birth_profile is None:
        return None

    places = _index_by_id(state.get("places") or [])
    birth_place = places.get(str(birth_profile.get("birth_place_id")))
    current_place_id = client.get("current_location_place_id")
    current_place = (
        places.get(str(current_place_id)) if current_place_id is not None else None
    )

    try:
        params = resolve_engine_birth_params(state, chart_record_id)
        engine_birth: dict[str, Any] = {"ok": True, **params}
    except ChartRecordBirthResolutionError as err:
        engine_birth = {
            "ok": False,
            "reason": err.reason,
            "message": err.message,
        }

    birth_city = birth_place.get("display_name") if birth_place else "—"
    birth_summary = (
        f"{birth_profile.get('birth_date')} · "
        f"{_birth_time_display(birth_profile)} · {birth_city}"
    )

    return {
        "chartRecordId": str(chart_record_id),
        "displayName": client.get("display_name"),
        "recordType": client.get("record_type", "client"),
        "birthSummary": birth_summary,
        "confidenceTier": birth_profile.get("confidence_tier"),
        "hasTimeUncertainty": _has_birth_time_uncertainty(birth_profile),
        "birthCity": birth_city,
        "currentCity": current_place.get("display_name") if current_place else None,
        "engineBirth": engine_birth,
    }


def list_chart_record_summaries(state: dict[str, Any]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for client in state.get("clients") or []:
        if not isinstance(client, dict) or not client.get("id"):
            continue
        summary = summarize_chart_record(state, str(client["id"]))
        if summary is not None:
            summaries.append(summary)
    return summaries


def empty_store() -> dict[str, Any]:
    ts = _now_iso()
    return {
        "_storage": STORAGE_MARKER,
        "_warning": (
            "NOT PRODUCT STORAGE. NOT AUTHORITATIVE. "
            "Parallel to library/library.json until explicit migration."
        ),
        "storage_schema_version": STORAGE_SCHEMA_VERSION,
        "supabase_mirror_version": SUPABASE_MIRROR_VERSION,
        "professional_account": {
            "id": "acct_local_1",
            "display_name": "Local Professional",
            "schema_version": 1,
            "created_at": ts,
            "updated_at": ts,
        },
        "user_settings": {**deepcopy(DEFAULT_USER_SETTINGS), "updated_at": ts},
        "places": [],
        "birth_profiles": [],
        "clients": [],
        "saved_investigations": [],
        "favorite_cities": [],
        "comparison_sets": [],
        "chart_record_history": [],
        "tags": [],
        "notes": [],
    }


def load(path: Path | str | None = None) -> dict[str, Any]:
    store_path = Path(path) if path is not None else DEFAULT_STORE_PATH
    if not store_path.exists():
        return empty_store()
    with open(store_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("store root must be a JSON object")
    return data


def save(state: dict[str, Any], path: Path | str | None = None) -> None:
    store_path = Path(path) if path is not None else DEFAULT_STORE_PATH
    errors = validate_store(state)
    if errors:
        raise ValueError("store validation failed: " + "; ".join(errors))

    payload = deepcopy(state)
    payload["storage_schema_version"] = STORAGE_SCHEMA_VERSION

    store_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=".product_store_",
        suffix=".json",
        dir=str(store_path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=False)
            fh.write("\n")
        os.replace(tmp_name, store_path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _collect_forbidden_keys(obj: Any, path: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_path = f"{path}.{key}" if path else key
            lower = key.lower()
            if any(sub in lower for sub in FORBIDDEN_KEY_SUBSTRINGS):
                hits.append(key_path)
            hits.extend(_collect_forbidden_keys(value, key_path))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            hits.extend(_collect_forbidden_keys(item, f"{path}[{idx}]"))
    return hits


def _layer2_settings_snapshot(state: dict[str, Any]) -> dict[str, Any]:
    settings = state.get("user_settings") or {}
    snapshot = {
        k: deepcopy(v)
        for k, v in settings.items()
        if k not in ("updated_at", "default_chart_record_id")
    }
    snapshot["settings_snapshot_version"] = settings.get("settings_version", 1)
    return snapshot


def _index_by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        row_id = row.get("id")
        if row_id:
            out[str(row_id)] = row
    return out


def validate_store(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if state.get("_storage") != STORAGE_MARKER:
        errors.append("_storage must be TEMPORARY_LOCAL_SCAFFOLD")

    if state.get("storage_schema_version") != STORAGE_SCHEMA_VERSION:
        errors.append(f"storage_schema_version must be {STORAGE_SCHEMA_VERSION}")

    for key in (
        "professional_account",
        "user_settings",
        "places",
        "birth_profiles",
        "clients",
        "saved_investigations",
        "favorite_cities",
        "comparison_sets",
        "chart_record_history",
        "tags",
        "notes",
    ):
        if key not in state:
            errors.append(f"missing top-level key: {key}")

    places = _index_by_id(state.get("places") or [])
    birth_profiles = _index_by_id(state.get("birth_profiles") or [])
    clients_list = state.get("clients") or []
    client_ids = {str(c.get("id")) for c in clients_list if isinstance(c, dict) and c.get("id")}

    settings = state.get("user_settings") or {}
    default_cr = settings.get("default_chart_record_id")
    if default_cr is not None and str(default_cr) not in client_ids:
        errors.append(f"default_chart_record_id references unknown client: {default_cr}")

    seen_birth_profiles: set[str] = set()
    for client in clients_list:
        if not isinstance(client, dict):
            errors.append("each client must be an object")
            continue
        cid = client.get("id")
        bp_id = client.get("birth_profile_id")
        if not bp_id:
            errors.append(f"client {cid} missing birth_profile_id")
            continue
        if bp_id in seen_birth_profiles:
            errors.append(f"birth_profile_id reused across clients: {bp_id}")
        seen_birth_profiles.add(str(bp_id))
        if str(bp_id) not in birth_profiles:
            errors.append(f"client {cid} references unknown birth_profile {bp_id}")

        record_type = client.get("record_type", "client")
        if record_type not in RECORD_TYPES:
            errors.append(f"client {cid} invalid record_type: {record_type}")

        current_loc = client.get("current_location_place_id")
        if current_loc is not None and str(current_loc) not in places:
            errors.append(f"client {cid} references unknown current_location_place_id {current_loc}")

    for bp_id, bp in birth_profiles.items():
        place_id = bp.get("birth_place_id")
        if place_id and str(place_id) not in places:
            errors.append(f"birth_profile {bp_id} references unknown place {place_id}")
        meta = bp.get("confidence_metadata")
        if meta is not None and not isinstance(meta, dict):
            errors.append(f"birth_profile {bp_id} confidence_metadata must be object")

    investigation_ids = {
        str(inv.get("id"))
        for inv in (state.get("saved_investigations") or [])
        if isinstance(inv, dict) and inv.get("id")
    }

    for inv in state.get("saved_investigations") or []:
        if not isinstance(inv, dict):
            errors.append("each saved_investigation must be an object")
            continue
        inv_id = inv.get("id")
        if str(inv.get("client_id")) not in client_ids:
            errors.append(f"investigation {inv_id} references unknown client_id")
        origin = inv.get("originating_chart_record_id")
        if origin is not None and str(origin) not in client_ids:
            errors.append(f"investigation {inv_id} references unknown originating_chart_record_id")
        if origin is not None and str(origin) != str(inv.get("client_id")):
            errors.append(
                f"investigation {inv_id} originating_chart_record_id must match client_id in v3"
            )
        if "settings_snapshot" not in inv:
            errors.append(f"investigation {inv_id} missing settings_snapshot")
        elif not isinstance(inv.get("settings_snapshot"), dict):
            errors.append(f"investigation {inv_id} settings_snapshot must be object")
        if "conditions" not in inv:
            errors.append(f"investigation {inv_id} missing conditions")
        forbidden = _collect_forbidden_keys(
            {
                "conditions": inv.get("conditions"),
                "settings_snapshot": inv.get("settings_snapshot"),
                "layer_display_state": inv.get("layer_display_state"),
            }
        )
        for hit in forbidden:
            errors.append(f"forbidden key in investigation {inv_id}: {hit}")

    forbidden_settings = _collect_forbidden_keys(state.get("user_settings"))
    for hit in forbidden_settings:
        errors.append(f"forbidden key in user_settings: {hit}")

    for fav in state.get("favorite_cities") or []:
        if not isinstance(fav, dict):
            errors.append("each favorite_city must be an object")
            continue
        if str(fav.get("place_id")) not in places:
            errors.append(f"favorite {fav.get('id')} references unknown place")
        if str(fav.get("client_id")) not in client_ids:
            errors.append(f"favorite {fav.get('id')} references unknown client")

    for cs in state.get("comparison_sets") or []:
        if not isinstance(cs, dict):
            errors.append("each comparison_set must be an object")
            continue
        cs_id = cs.get("id")
        if str(cs.get("client_id")) not in client_ids:
            errors.append(f"comparison_set {cs_id} references unknown client_id")
        place_ids = cs.get("place_ids")
        if not isinstance(place_ids, list):
            errors.append(f"comparison_set {cs_id} place_ids must be array")
            continue
        if not (2 <= len(place_ids) <= 5):
            errors.append(f"comparison_set {cs_id} must have 2–5 place_ids")
        if len(set(place_ids)) != len(place_ids):
            errors.append(f"comparison_set {cs_id} place_ids must not contain duplicates")
        for pid in place_ids:
            if str(pid) not in places:
                errors.append(f"comparison_set {cs_id} references unknown place {pid}")
        parent_inv = cs.get("saved_investigation_id")
        if parent_inv is not None and str(parent_inv) not in investigation_ids:
            errors.append(f"comparison_set {cs_id} references unknown saved_investigation_id")

    for row in state.get("chart_record_history") or []:
        if not isinstance(row, dict):
            errors.append("each chart_record_history row must be an object")
            continue
        hid = row.get("id")
        if str(row.get("client_id")) not in client_ids:
            errors.append(f"history {hid} references unknown client_id")
        event_type = row.get("event_type")
        if event_type not in HISTORY_EVENT_TYPES:
            errors.append(f"history {hid} invalid event_type: {event_type}")
        if not row.get("occurred_at"):
            errors.append(f"history {hid} missing occurred_at")
        payload = row.get("payload")
        if payload is not None and not isinstance(payload, dict):
            errors.append(f"history {hid} payload must be object")
        hist_inv = row.get("saved_investigation_id")
        if hist_inv is not None and str(hist_inv) not in investigation_ids:
            errors.append(f"history {hid} references unknown saved_investigation_id")

    return errors


def create_place(
    state: dict[str, Any],
    *,
    display_name: str,
    lat: float,
    lon: float,
    external_source: str = "manual",
    external_id: str | None = None,
    admin1: str | None = None,
    country_code: str | None = None,
    country_name: str | None = None,
    place_id: str | None = None,
) -> dict[str, Any]:
    if external_source not in ("geoname", "wof", "manual", "map_pick"):
        raise ValueError(f"invalid external_source: {external_source}")

    place = {
        "id": place_id or _new_id("place"),
        "external_source": external_source,
        "external_id": external_id,
        "display_name": display_name,
        "admin1": admin1,
        "country_code": country_code,
        "country_name": country_name,
        "lat": lat,
        "lon": lon,
        "schema_version": 1,
    }
    state.setdefault("places", []).append(place)
    return place


def create_client(
    state: dict[str, Any],
    *,
    display_name: str,
    birth_date: str,
    birth_time: str | None,
    timezone_id: str,
    birth_place: dict[str, Any],
    confidence_tier: str = "T0",
    confidence_metadata: dict[str, Any] | None = None,
    notes: str = "",
    tags: list[str] | None = None,
    record_type: str = "client",
    current_location_place_id: str | None = None,
    client_id: str | None = None,
    birth_profile_id: str | None = None,
) -> dict[str, Any]:
    if confidence_tier not in ("T0", "T1", "T2", "T3", "T4"):
        raise ValueError(f"invalid confidence_tier: {confidence_tier}")
    if record_type not in RECORD_TYPES:
        raise ValueError(f"invalid record_type: {record_type}")

    ts = _now_iso()
    place = create_place(state, **birth_place)

    birth_profile = {
        "id": birth_profile_id or _new_id("bp"),
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_place_id": place["id"],
        "timezone_id": timezone_id,
        "confidence_tier": confidence_tier,
        "confidence_metadata": confidence_metadata or {},
        "representative_time": None,
        "schema_version": 1,
        "updated_at": ts,
    }
    state.setdefault("birth_profiles", []).append(birth_profile)

    client = {
        "id": client_id or _new_id("client"),
        "display_name": display_name,
        "birth_profile_id": birth_profile["id"],
        "record_type": record_type,
        "current_location_place_id": current_location_place_id,
        "notes": notes,
        "tags": list(tags or []),
        "schema_version": 1,
        "updated_at": ts,
    }
    state.setdefault("clients", []).append(client)
    return client


def set_default_chart_record_id(state: dict[str, Any], chart_record_id: str) -> None:
    if get_chart_record(state, chart_record_id) is None:
        raise ValueError(f"unknown chart_record_id: {chart_record_id}")
    settings = state.setdefault("user_settings", {})
    settings["default_chart_record_id"] = chart_record_id
    settings["updated_at"] = _now_iso()


def save_investigation(
    state: dict[str, Any],
    *,
    client_id: str,
    title: str,
    conditions: dict[str, Any],
    viewport: dict[str, Any],
    settings_snapshot: dict[str, Any] | None = None,
    layer_display_state: dict[str, Any] | None = None,
    default_reopen_mode: str = "keep_snapshot",
    name: str | None = None,
    notes: str = "",
    originating_chart_record_id: str | None = None,
    investigation_id: str | None = None,
) -> dict[str, Any]:
    if default_reopen_mode not in ("keep_snapshot", "use_current"):
        raise ValueError("default_reopen_mode must be keep_snapshot or use_current")

    clients = _index_by_id(state.get("clients") or [])
    if client_id not in clients:
        raise ValueError(f"unknown client_id: {client_id}")

    origin = originating_chart_record_id or client_id
    if origin != client_id:
        raise ValueError("originating_chart_record_id must match client_id in v3")

    client = clients[client_id]
    snapshot = deepcopy(settings_snapshot) if settings_snapshot is not None else _layer2_settings_snapshot(state)
    if not isinstance(snapshot, dict):
        raise ValueError("settings_snapshot must be an object")

    ts = _now_iso()
    investigation = {
        "id": investigation_id or _new_id("inv"),
        "client_id": client_id,
        "birth_profile_id": client["birth_profile_id"],
        "originating_chart_record_id": origin,
        "title": title,
        "name": name if name is not None else title,
        "notes": notes,
        "conditions": conditions,
        "viewport": viewport,
        "settings_snapshot": snapshot,
        "settings_snapshot_version": snapshot.get("settings_snapshot_version", 1),
        "layer_display_state": layer_display_state or {},
        "default_reopen_mode": default_reopen_mode,
        "schema_version": 1,
        "updated_at": ts,
    }
    state.setdefault("saved_investigations", []).append(investigation)
    return investigation


def add_favorite_city(
    state: dict[str, Any],
    *,
    client_id: str,
    place_id: str,
    notes: str = "",
    saved_investigation_id: str | None = None,
    sort_order: int | None = None,
    favorite_id: str | None = None,
) -> dict[str, Any]:
    clients = _index_by_id(state.get("clients") or [])
    places = _index_by_id(state.get("places") or [])
    if client_id not in clients:
        raise ValueError(f"unknown client_id: {client_id}")
    if place_id not in places:
        raise ValueError(f"unknown place_id: {place_id}")

    favorites = state.setdefault("favorite_cities", [])
    for fav in favorites:
        if fav.get("client_id") == client_id and fav.get("place_id") == place_id:
            raise ValueError("favorite city already exists for client+place")

    favorite = {
        "id": favorite_id or _new_id("fav"),
        "client_id": client_id,
        "place_id": place_id,
        "saved_investigation_id": saved_investigation_id,
        "notes": notes,
        "sort_order": sort_order if sort_order is not None else len(favorites),
        "schema_version": 1,
    }
    favorites.append(favorite)
    return favorite


def create_comparison_set(
    state: dict[str, Any],
    *,
    client_id: str,
    place_ids: list[str],
    notes: str = "",
    saved_investigation_id: str | None = None,
    comparison_set_id: str | None = None,
) -> dict[str, Any]:
    if not (2 <= len(place_ids) <= 5):
        raise ValueError("comparison set requires 2–5 place_ids")
    if len(set(place_ids)) != len(place_ids):
        raise ValueError("comparison set place_ids must be unique")

    clients = _index_by_id(state.get("clients") or [])
    places = _index_by_id(state.get("places") or [])
    if client_id not in clients:
        raise ValueError(f"unknown client_id: {client_id}")
    for pid in place_ids:
        if pid not in places:
            raise ValueError(f"unknown place_id: {pid}")

    if saved_investigation_id is not None:
        inv_ids = {str(i.get("id")) for i in state.get("saved_investigations") or []}
        if saved_investigation_id not in inv_ids:
            raise ValueError(f"unknown saved_investigation_id: {saved_investigation_id}")

    ts = _now_iso()
    comparison_set = {
        "id": comparison_set_id or _new_id("cmp"),
        "client_id": client_id,
        "place_ids": list(place_ids),
        "saved_investigation_id": saved_investigation_id,
        "notes": notes,
        "schema_version": 1,
        "updated_at": ts,
    }
    state.setdefault("comparison_sets", []).append(comparison_set)
    return comparison_set


def append_chart_record_history(
    state: dict[str, Any],
    *,
    client_id: str,
    event_type: str,
    payload: dict[str, Any] | None = None,
    saved_investigation_id: str | None = None,
    occurred_at: str | None = None,
    history_id: str | None = None,
) -> dict[str, Any]:
    if event_type not in HISTORY_EVENT_TYPES:
        raise ValueError(f"invalid event_type: {event_type}")
    if get_chart_record(state, client_id) is None:
        raise ValueError(f"unknown client_id: {client_id}")

    if saved_investigation_id is not None:
        inv_ids = {str(i.get("id")) for i in state.get("saved_investigations") or []}
        if saved_investigation_id not in inv_ids:
            raise ValueError(f"unknown saved_investigation_id: {saved_investigation_id}")

    row = {
        "id": history_id or _new_id("hist"),
        "client_id": client_id,
        "event_type": event_type,
        "occurred_at": occurred_at or _now_iso(),
        "saved_investigation_id": saved_investigation_id,
        "payload": payload or {},
        "schema_version": 1,
    }
    state.setdefault("chart_record_history", []).append(row)
    return row
