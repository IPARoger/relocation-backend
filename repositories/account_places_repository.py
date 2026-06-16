"""JWT-gated place resolution (resolve-or-create).

Places is a global reference table: authenticated users may read via RLS;
inserts are performed with the service-role client after the caller JWT is
validated. Mirrors the browser place_resolution.js matching rules so the map
favorite workflow behaves identically.
"""

from __future__ import annotations

from repositories.places_repository import create_place, search_places
from services.supabase_user_client import get_supabase_for_user


class PlacesError(Exception):
    """Raised when place resolution cannot proceed."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


def _norm(value) -> str:
    return str(value if value is not None else "").strip().lower()


def _resolve_account_id(client, jwt_token: str) -> str:
    user_resp = client.auth.get_user(jwt_token)
    if getattr(user_resp, "user", None) is None:
        raise PlacesError("Authenticated user could not be resolved", "auth_user_missing")
    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise PlacesError("No account membership for authenticated user", "account_missing")
    return account_ids[0]


def _find_existing_match(
    matches: list[dict],
    display_name: str,
    latitude: float | None,
    longitude: float | None,
    coord_tolerance: float,
) -> dict | None:
    has_coords = latitude is not None and longitude is not None
    for place in matches:
        if _norm(place.get("display_name")) != _norm(display_name):
            continue
        if has_coords:
            try:
                plat = float(place.get("latitude"))
                plon = float(place.get("longitude"))
            except (TypeError, ValueError):
                continue
            if (
                abs(plat - latitude) <= coord_tolerance
                and abs(plon - longitude) <= coord_tolerance
            ):
                return place
        else:
            return place
    return None


def _lookup_by_geonames(client, geonames_id: str) -> dict | None:
    if not geonames_id:
        return None
    try:
        result = (
            client.table("places")
            .select("*")
            .eq("geonames_id", geonames_id)
            .limit(1)
            .execute()
        )
    except Exception:  # noqa: BLE001
        return None
    if result.data:
        return result.data[0]
    return None


def resolve_or_create_place(
    jwt_token: str,
    display_name: str,
    latitude: float | None = None,
    longitude: float | None = None,
    country: str | None = None,
    admin: str | None = None,
    origin: str | None = None,
    geonames_id: str | None = None,
    coord_tolerance: float = 0.02,
) -> dict:
    """Return an existing place row or create one when coordinates are present."""
    name = str(display_name or "").strip()
    if not name:
        raise PlacesError("display_name is required", "validation_failed")

    client = get_supabase_for_user(jwt_token)
    _resolve_account_id(client, jwt_token)

    gid = str(geonames_id).strip() if geonames_id is not None else ""
    if gid:
        existing = _lookup_by_geonames(client, gid)
        if existing and existing.get("id"):
            existing["_status"] = "existing"
            return existing

    matches = search_places(name)
    if not isinstance(matches, list):
        matches = []

    has_coords = latitude is not None and longitude is not None
    existing = _find_existing_match(matches, name, latitude, longitude, coord_tolerance)
    if existing:
        existing["_status"] = "existing"
        return existing

    if not has_coords:
        raise PlacesError(
            f'no coordinates and no exact match for "{name}"',
            "place_unresolved",
        )

    created = create_place(
        display_name=name,
        latitude=float(latitude),
        longitude=float(longitude),
        provider=origin or "manual",
        admin1=admin,
        country_name=country,
    )
    if not created:
        raise PlacesError("place create returned no row", "create_failed")
    created["_status"] = "created"
    return created
