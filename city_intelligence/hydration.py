"""Hydration pipeline: providers → structured payload → repository store."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from city_intelligence.providers.airport import AirportProvider
from city_intelligence.providers.ai_summary import AiSummaryProvider
from city_intelligence.providers.location import LocationProvider
from city_intelligence.providers.photo import PhotoProvider
from repositories import city_intelligence_repository as repo
from repositories.places_repository import get_place

logger = logging.getLogger(__name__)


class HydrationError(Exception):
    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_providers():
    location = LocationProvider(nearest_place_lookup=repo.nearest_places)
    return {
        "location": location,
        "airport": AirportProvider(),
        "photo": PhotoProvider(),
        "ai": AiSummaryProvider(),
    }


def hydrate_city(
    city_id: str,
    *,
    force: bool = False,
    providers: dict | None = None,
) -> dict:
    """Run full hydration for a known city_id (places.id)."""
    place = get_place(city_id)
    if not place:
        raise HydrationError("city not found", "city_not_found")

    existing = None if force else repo.get_by_city_id(city_id)
    if existing and existing.get("status") == "ready":
        return existing

    bundle = providers or _default_providers()
    repo.mark_status(city_id, "hydrating")

    try:
        location_context = bundle["location"].resolve(
            latitude=float(place["latitude"]),
            longitude=float(place["longitude"]),
            place=place,
        )
        airports = bundle["airport"].fetch_airports(place=place, location_context=location_context)
        photos = bundle["photo"].fetch_photos(place=place, location_context=location_context)
        summaries = bundle["ai"].generate_summaries(
            place=place,
            location_context=location_context,
            airports=airports,
            photos=photos,
        )

        status = "custom" if location_context.get("is_custom") else "ready"
        payload = {
            **summaries,
            "photos_json": photos,
            "airport_json": airports,
            "ai_version": getattr(bundle["ai"], "version", "ci-stub-v1"),
            "generated_at": _utc_now_iso(),
            "status": status,
        }
        stored = repo.upsert_intelligence(city_id, payload)
        logger.info("city_intelligence hydrated city_id=%s status=%s", city_id, status)
        return stored
    except Exception as exc:
        logger.exception("city_intelligence hydration failed city_id=%s", city_id)
        repo.mark_status(city_id, "error")
        raise HydrationError(str(exc), "hydration_failed") from exc


def hydrate_custom_coordinates(
    latitude: float,
    longitude: float,
    *,
    city_id: str,
    providers: dict | None = None,
) -> dict:
    """Hydrate intelligence for a custom place row using coordinate workflow."""
    place = get_place(city_id)
    if not place:
        raise HydrationError("city not found", "city_not_found")

    bundle = providers or _default_providers()
    repo.mark_status(city_id, "hydrating")
    location_context = bundle["location"].resolve(
        latitude=latitude,
        longitude=longitude,
        place=None,
    )

    if location_context.get("suggested_name") and not place.get("display_name", "").strip():
        place = {**place, "display_name": location_context["suggested_name"]}

    airports = bundle["airport"].fetch_airports(place=place, location_context=location_context)
    photos = bundle["photo"].fetch_photos(place=place, location_context=location_context)
    summaries = bundle["ai"].generate_summaries(
        place=place,
        location_context=location_context,
        airports=airports,
        photos=photos,
    )
    payload = {
        **summaries,
        "photos_json": photos,
        "airport_json": airports,
        "ai_version": getattr(bundle["ai"], "version", "ci-stub-v1"),
        "generated_at": _utc_now_iso(),
        "status": "custom",
    }
    return repo.upsert_intelligence(city_id, payload)
