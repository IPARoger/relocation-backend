"""Airport context provider (structured JSON, no route logic)."""

from __future__ import annotations


class AirportProvider:
    def fetch_airports(self, *, place: dict, location_context: dict | None) -> dict:
        name = (place or {}).get("display_name") or "this area"
        country = (place or {}).get("country_name") or (location_context or {}).get("country_name")
        code_guess = ((place or {}).get("country_code") or "XX")[:3].upper()
        primary = {
            "name": f"{name} International",
            "iata": None,
            "icao": None,
            "distance_km": 12,
            "drive_minutes": 25,
            "notes": f"Representative airport serving {name}.",
        }
        nearest = None
        if location_context and location_context.get("nearest_village"):
            nearest = {
                "name": f"Regional airfield near {location_context['nearest_village']}",
                "iata": None,
                "distance_km": 45,
                "notes": "Nearest practical aviation access for remote coordinates.",
            }
        return {
            "primary": primary,
            "nearest": nearest,
            "country": country,
            "search_hint": f"airport {name} {country or ''}".strip(),
            "location_context": location_context or {},
        }
