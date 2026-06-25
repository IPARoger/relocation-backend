"""City Intelligence Service — cache-first reads and background hydration."""

from __future__ import annotations

import logging
import threading
from typing import Callable

from city_intelligence.hydration import HydrationError, hydrate_city
from repositories import city_intelligence_repository as repo

logger = logging.getLogger(__name__)

_inflight: set[str] = set()
_inflight_lock = threading.Lock()


class CityIntelligenceError(Exception):
    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


def get_cached(city_id: str) -> dict | None:
    row = repo.get_by_city_id(city_id)
    if row and row.get("status") in ("ready", "custom"):
        return row
    return None


def get_or_hydrate(city_id: str) -> dict:
    """Cache-first GET path: return cached row or hydrate synchronously."""
    cached = get_cached(city_id)
    if cached:
        return cached
    try:
        return hydrate_city(city_id)
    except HydrationError as exc:
        raise CityIntelligenceError(str(exc), exc.reason) from exc


def force_hydrate(city_id: str) -> dict:
    try:
        return hydrate_city(city_id, force=True)
    except HydrationError as exc:
        raise CityIntelligenceError(str(exc), exc.reason) from exc


def _background_worker(city_id: str) -> None:
    try:
        hydrate_city(city_id)
    except HydrationError as exc:
        logger.warning("background hydration skipped city_id=%s reason=%s", city_id, exc.reason)
    except Exception:
        logger.exception("background hydration failed city_id=%s", city_id)
    finally:
        with _inflight_lock:
            _inflight.discard(city_id)


def enqueue_background_hydration(city_id: str) -> None:
    """Non-blocking hydration for favorites/comparison/relocated flows."""
    if not city_id:
        return
    cached = get_cached(city_id)
    if cached:
        return
    with _inflight_lock:
        if city_id in _inflight:
            return
        _inflight.add(city_id)
    thread = threading.Thread(
        target=_background_worker,
        args=(city_id,),
        name=f"ci-hydrate-{city_id[:8]}",
        daemon=True,
    )
    thread.start()


def enqueue_background_hydration_many(city_ids: list[str]) -> None:
    for city_id in city_ids:
        enqueue_background_hydration(city_id)


def wire_hydration_hook(save_fn: Callable[..., dict]) -> Callable[..., dict]:
    """Decorator: after successful save, enqueue background hydration for place_id."""

    def wrapper(*args, **kwargs):
        result = save_fn(*args, **kwargs)
        place_id = kwargs.get("place_id")
        if place_id is None and args:
            # save_favorite(jwt, profile_id, place_id, ...)
            if len(args) >= 3:
                place_id = args[2]
        if isinstance(result, dict):
            place_id = place_id or result.get("place_id")
        if place_id:
            enqueue_background_hydration(str(place_id))
        return result

    return wrapper
