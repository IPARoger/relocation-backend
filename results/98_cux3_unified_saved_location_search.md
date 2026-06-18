# C-UX-3 — Unified Saved Location Search (Family B)

**Status:** Verified  
**Date:** 2026-06-18

## Goal

Replace favorites-only pickers with unified **Family B** search: profile favorites + custom saved places + `GET /places/search`, placeholder `"Search locations or favorites"`. Family A (birth/current/relocated intake) unchanged.

## Audit (before)

| Surface | Prior behavior |
|---------|----------------|
| Comparison add-location | Checkbox list of favorites only |
| Map city search | Placeholder dataset, exact-name Enter only |
| Shared client | `place_search_client.js` → GeoNames only |

## Implementation

- `saved_location_search_service.js` — `RMSavedLocationSearch` (ranking, dedupe, starter sections)
- `saved_location_search_ui.js` — reusable mount + panel
- `app_shell.html` — comparison `#rm-cmp-loc-search-mount`, chip picker + build flow
- `map_CURRENT.html` — `#rm-map-loc-search-mount`, select → recenter + popup
- `main_centerline_FIXER.py` — static routes for new JS

Family A placeholders remain `"Search locations"`.

## Smokes

- `smoke_map_current.py` — overall_pass: true
- `smoke_comparison_sets.py` — PASS (23/23), includes Family B placeholder/starter/merge checks
