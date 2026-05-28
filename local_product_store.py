"""Phase 3.0a — local product store (file-only scaffold).

TEMPORARY_LOCAL_SCAFFOLD — not product storage, not connected to map or library.json.
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

APP_DIR = Path(__file__).resolve().parent
DEFAULT_STORE_PATH = APP_DIR / "scaffold" / "local_product" / "TEMPORARY_product_store.json"

STORAGE_SCHEMA_VERSION = 2
SUPABASE_MIRROR_VERSION = 1
STORAGE_MARKER = "TEMPORARY_LOCAL_SCAFFOLD"

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
        "conjunction": 8,
        "square": 6,
        "opposition": 8,
        "trine": 8,
        "sextile": 4,
    },
    "visible_minor_aspects": False,
    "helper_layers": {},
    "ontology_pack_id": None,
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


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
        if k not in ("updated_at",)
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
        "tags",
        "notes",
    ):
        if key not in state:
            errors.append(f"missing top-level key: {key}")

    places = _index_by_id(state.get("places") or [])
    birth_profiles = _index_by_id(state.get("birth_profiles") or [])
    clients = state.get("clients") or []

    seen_birth_profiles: set[str] = set()
    for client in clients:
        if not isinstance(client, dict):
            errors.append("each client must be an object")
            continue
        bp_id = client.get("birth_profile_id")
        if not bp_id:
            errors.append(f"client {client.get('id')} missing birth_profile_id")
            continue
        if bp_id in seen_birth_profiles:
            errors.append(f"birth_profile_id reused across clients: {bp_id}")
        seen_birth_profiles.add(str(bp_id))
        if str(bp_id) not in birth_profiles:
            errors.append(f"client {client.get('id')} references unknown birth_profile {bp_id}")

    for bp_id, bp in birth_profiles.items():
        place_id = bp.get("birth_place_id")
        if place_id and str(place_id) not in places:
            errors.append(f"birth_profile {bp_id} references unknown place {place_id}")

    for inv in state.get("saved_investigations") or []:
        if not isinstance(inv, dict):
            errors.append("each saved_investigation must be an object")
            continue
        if "settings_snapshot" not in inv:
            errors.append(f"investigation {inv.get('id')} missing settings_snapshot")
        elif not isinstance(inv.get("settings_snapshot"), dict):
            errors.append(f"investigation {inv.get('id')} settings_snapshot must be object")
        if "conditions" not in inv:
            errors.append(f"investigation {inv.get('id')} missing conditions")
        forbidden = _collect_forbidden_keys(
            {
                "conditions": inv.get("conditions"),
                "settings_snapshot": inv.get("settings_snapshot"),
                "layer_display_state": inv.get("layer_display_state"),
            }
        )
        for hit in forbidden:
            errors.append(f"forbidden key in investigation {inv.get('id')}: {hit}")

    forbidden_settings = _collect_forbidden_keys(state.get("user_settings"))
    for hit in forbidden_settings:
        errors.append(f"forbidden key in user_settings: {hit}")

    for fav in state.get("favorite_cities") or []:
        if str(fav.get("place_id")) not in places:
            errors.append(f"favorite {fav.get('id')} references unknown place")
        client_ids = {str(c.get("id")) for c in clients if isinstance(c, dict)}
        if str(fav.get("client_id")) not in client_ids:
            errors.append(f"favorite {fav.get('id')} references unknown client")

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
) -> dict[str, Any]:
    if external_source not in ("geoname", "wof", "manual", "map_pick"):
        raise ValueError(f"invalid external_source: {external_source}")

    place = {
        "id": _new_id("place"),
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
) -> dict[str, Any]:
    if confidence_tier not in ("T0", "T1", "T2", "T3", "T4"):
        raise ValueError(f"invalid confidence_tier: {confidence_tier}")

    ts = _now_iso()
    place = create_place(state, **birth_place)

    birth_profile = {
        "id": _new_id("bp"),
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
        "id": _new_id("client"),
        "display_name": display_name,
        "birth_profile_id": birth_profile["id"],
        "notes": notes,
        "tags": list(tags or []),
        "schema_version": 1,
        "updated_at": ts,
    }
    state.setdefault("clients", []).append(client)
    return client


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
) -> dict[str, Any]:
    if default_reopen_mode not in ("keep_snapshot", "use_current"):
        raise ValueError("default_reopen_mode must be keep_snapshot or use_current")

    clients = _index_by_id(state.get("clients") or [])
    if client_id not in clients:
        raise ValueError(f"unknown client_id: {client_id}")

    client = clients[client_id]
    snapshot = deepcopy(settings_snapshot) if settings_snapshot is not None else _layer2_settings_snapshot(state)
    if not isinstance(snapshot, dict):
        raise ValueError("settings_snapshot must be an object")

    ts = _now_iso()
    investigation = {
        "id": _new_id("inv"),
        "client_id": client_id,
        "birth_profile_id": client["birth_profile_id"],
        "title": title,
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
        "id": _new_id("fav"),
        "client_id": client_id,
        "place_id": place_id,
        "saved_investigation_id": saved_investigation_id,
        "notes": notes,
        "sort_order": sort_order if sort_order is not None else len(favorites),
        "schema_version": 1,
    }
    favorites.append(favorite)
    return favorite
