"""Provider protocols for City Intelligence hydration."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class AirportProviderProtocol(Protocol):
    def fetch_airports(self, *, place: dict, location_context: dict | None) -> dict:
        ...


@runtime_checkable
class PhotoProviderProtocol(Protocol):
    def fetch_photos(self, *, place: dict, location_context: dict | None) -> dict:
        ...


@runtime_checkable
class LocationProviderProtocol(Protocol):
    def resolve(self, *, latitude: float, longitude: float, place: dict | None = None) -> dict:
        ...


@runtime_checkable
class AiSummaryProviderProtocol(Protocol):
    def generate_summaries(
        self,
        *,
        place: dict,
        location_context: dict | None,
        airports: dict,
        photos: dict,
    ) -> dict[str, str]:
        ...


ProviderBundle = dict[str, Any]
