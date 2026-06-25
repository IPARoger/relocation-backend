"""Photo URL provider — category URLs only (hero, street, residential, nature, landmark)."""

from __future__ import annotations

_CATEGORIES = ("hero", "street", "residential", "nature", "landmark")


class PhotoProvider:
  def fetch_photos(self, *, place: dict, location_context: dict | None) -> dict:
      slug = (
          (place or {}).get("canonical_name")
          or (place or {}).get("display_name")
          or (location_context or {}).get("suggested_name")
          or "city"
      )
      slug = "".join(ch if ch.isalnum() else "-" for ch in slug.lower()).strip("-") or "city"
      base = f"https://images.example.com/ci/{slug}"
      return {
          category: f"{base}/{category}.jpg"
          for category in _CATEGORIES
      }
