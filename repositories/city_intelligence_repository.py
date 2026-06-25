"""Supabase persistence for city_intelligence cache."""

from __future__ import annotations

import math
from datetime import datetime, timezone

from services.supabase_client import get_supabase

_TEXT_FIELDS = (
    "overview",
    "population",
    "climate",
    "cost",
    "safety",
    "language",
    "healthcare",
    "transport",
    "visa",
    "culture",
    "expat",
)

_SELECT = (
    "city_id, status, overview, population, climate, cost, safety, language, "
    "healthcare, transport, visa, culture, expat, photos_json, airport_json, "
    "ai_version, generated_at, created_at, updated_at"
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_by_city_id(city_id: str) -> dict | None:
    client = get_supabase()
    result = (
        client.table("city_intelligence")
        .select(_SELECT)
        .eq("city_id", city_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def upsert_intelligence(city_id: str, payload: dict) -> dict:
    client = get_supabase()
    row = {"city_id": city_id, "updated_at": _utc_now_iso()}
    for key in ("status", "photos_json", "airport_json", "ai_version", "generated_at"):
        if key in payload:
            row[key] = payload[key]
    for key in _TEXT_FIELDS:
        if key in payload:
            row[key] = payload[key]

    result = client.table("city_intelligence").upsert(row, on_conflict="city_id").execute()
    return result.data[0] if result.data else row


def mark_status(city_id: str, status: str) -> dict | None:
    return upsert_intelligence(city_id, {"status": status})


def list_ready_city_ids(limit: int = 1000) -> list[str]:
    client = get_supabase()
    result = (
        client.table("city_intelligence")
        .select("city_id")
        .eq("status", "ready")
        .limit(limit)
        .execute()
    )
    return [row["city_id"] for row in (result.data or [])]


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def nearest_places(latitude: float, longitude: float, limit: int = 8) -> list[dict]:
    """Return places ordered by approximate distance (client-side sort over candidate set)."""
    client = get_supabase()
    lat_pad = 2.0
    lon_pad = 2.0
    result = (
        client.table("places")
        .select(
            "id, display_name, canonical_name, country_code, country_name, "
            "latitude, longitude, population, importance_rank, geonames_id"
        )
        .gte("latitude", latitude - lat_pad)
        .lte("latitude", latitude + lat_pad)
        .gte("longitude", longitude - lon_pad)
        .lte("longitude", longitude + lon_pad)
        .limit(200)
        .execute()
    )
    rows = result.data or []
    for row in rows:
        row["_distance_km"] = _haversine_km(
            latitude,
            longitude,
            float(row["latitude"]),
            float(row["longitude"]),
        )
    rows.sort(key=lambda r: (r["_distance_km"], -(int(r.get("population") or 0))))
    return rows[:limit]


def find_place_by_geonames_id(geonames_id: str) -> dict | None:
    client = get_supabase()
    result = (
        client.table("places")
        .select("id, display_name, geonames_id, latitude, longitude, population, country_code, country_name")
        .eq("geonames_id", str(geonames_id))
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None
