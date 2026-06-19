# W2-LABEL-1: Human place label normalization

**Date:** 2026-06-16  
**Scope:** `human_place_label.js`, `place_resolution.js`, `supabase_store_bridge.js`, `saved_location_search_service.js`, `map_CURRENT.html`, `app_shell.html`

## Summary

User-visible place labels now use one shared formatter so known cities include country (and admin when useful), while custom map points keep user names or coordinate fallbacks.

## Shared helper

**`human_place_label.js`** → `window.RMHumanPlaceLabel.humanPlaceLabel(placeOrFavorite)`  
Re-exported on `window.RMPlaceResolution.humanPlaceLabel`.

### Rules

| Case | Label |
|------|-------|
| Known city with admin + country | `City, Admin, Country` |
| Known city without useful admin | `City, Country` |
| Already disambiguated `display_name` | Use as-is (no duplicate country) |
| Custom (`map_custom` / `source: custom`) | User label first; else `Saved location near {lat}, {lon}` |
| UUID-only string | `Saved place` (no UUID leakage) |

### Examples

- Paris, TX, United States
- Paris, Île-de-France, France
- Moscow, Russia
- Lahore, Punjab, Pakistan

## Surfaces updated

1. **Map popup** (`map_CURRENT.html`) — `mapHumanPlaceLabel()` in title; admin/country no longer duplicated on coords line
2. **Favorites cards** (`app_shell.html` `adaptStoreToView`) — `formatPlaceLabel()` with full place row
3. **Comparison chips / overlay** — search picks, favorite picks, compare screen chips
4. **Relocated chart header** — `screenChart()` uses `shellHumanPlaceLabel(placeId)`
5. **Family B search** — `formatPlaceDisplayName()` delegates to shared helper

## Data loading

`supabase_store_bridge.js` now selects `admin1`, `country_code`, `country_name`, `canonical_name`, `provider` for store places (frontend-only; no API changes).

## Validation (2026-06-16, port 8004)

```
PASS: smoke_map_current.py
PASS: smoke_favorites.py
PASS: smoke_comparison_sets.py
```

## Out of scope

Search performance, settings, notes, exports, help/onboarding, astrology math, renderer, genie/ghost UI.
