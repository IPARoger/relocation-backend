"""Resolve coordinates to known cities or custom/remote location context."""

from __future__ import annotations

import math
from typing import Callable

_KNOWN_CITY_MAX_KM = 25.0
_MIN_KNOWN_POPULATION = 5_000


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


class LocationProvider:
    """Reverse-geocode workflow using nearest known place from the database."""

    def __init__(self, nearest_place_lookup: Callable[[float, float, int], list[dict]] | None = None):
        self._nearest_place_lookup = nearest_place_lookup

    def resolve(self, *, latitude: float, longitude: float, place: dict | None = None) -> dict:
        if place and place.get("id"):
            return {
                "is_known_city": True,
                "city_id": place["id"],
                "display_name": place.get("display_name") or place.get("canonical_name"),
                "country_code": place.get("country_code"),
                "country_name": place.get("country_name"),
                "latitude": float(place.get("latitude", latitude)),
                "longitude": float(place.get("longitude", longitude)),
                "nearest_village": None,
                "nearest_airport": None,
                "nearest_city_id": place["id"],
                "regional_context": place.get("display_name"),
                "is_custom": False,
                "is_remote": False,
                "suggested_name": None,
            }

        candidates: list[dict] = []
        if self._nearest_place_lookup is not None:
            candidates = self._nearest_place_lookup(latitude, longitude, 8)

        nearest = candidates[0] if candidates else None
        dist = 9999.0
        if nearest:
            dist = _haversine_km(
                latitude,
                longitude,
                float(nearest["latitude"]),
                float(nearest["longitude"]),
            )
            pop = int(nearest.get("population") or 0)
            if dist <= _KNOWN_CITY_MAX_KM and pop >= _MIN_KNOWN_POPULATION:
                return {
                    "is_known_city": True,
                    "city_id": nearest["id"],
                    "display_name": nearest.get("display_name"),
                    "country_code": nearest.get("country_code"),
                    "country_name": nearest.get("country_name"),
                    "latitude": latitude,
                    "longitude": longitude,
                    "nearest_village": None,
                    "nearest_airport": None,
                    "nearest_city_id": nearest["id"],
                    "regional_context": nearest.get("display_name"),
                    "is_custom": False,
                    "is_remote": False,
                    "suggested_name": None,
                }

        village = nearest.get("display_name") if nearest else None
        village_id = nearest.get("id") if nearest else None
        country_code = (nearest or {}).get("country_code")
        country_name = (nearest or {}).get("country_name")
        is_remote = bool(nearest and dist > _KNOWN_CITY_MAX_KM)

        suggested = self._suggest_custom_name(latitude, longitude, village, country_name)
        return {
            "is_known_city": False,
            "city_id": None,
            "display_name": suggested,
            "country_code": country_code,
            "country_name": country_name,
            "latitude": latitude,
            "longitude": longitude,
            "nearest_village": village,
            "nearest_airport": None,
            "nearest_city_id": village_id,
            "regional_context": village or country_name,
            "is_custom": not is_remote,
            "is_remote": is_remote,
            "suggested_name": suggested,
        }

    @staticmethod
    def _suggest_custom_name(lat: float, lon: float, village: str | None, country: str | None) -> str:
        base = village or "Custom Location"
        if country:
            return f"{base} area, {country}"
        return f"{base} ({lat:.2f}, {lon:.2f})"
