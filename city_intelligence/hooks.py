"""Integration hooks for background City Intelligence hydration."""

from __future__ import annotations

from city_intelligence.service import enqueue_background_hydration, enqueue_background_hydration_many


def on_place_saved(place_id: str | None) -> None:
    if place_id:
        enqueue_background_hydration(str(place_id))


def on_places_saved(place_ids: list[str] | None) -> None:
    if place_ids:
        enqueue_background_hydration_many([str(pid) for pid in place_ids if pid])
