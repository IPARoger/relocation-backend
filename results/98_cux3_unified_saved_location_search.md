# C-UX-3 — Unified Saved Location Search (Family B)

**Date:** 2026-06-18  
**Roadmap ID:** C-UX-3  
**Checkpoint:** C-UX-2 → this slice

# Audit (pre-implementation)

| Surface | Before | Gap |
|---------|--------|-----|
| Compare picker (`app_shell.html`) | Checkbox list of `r.favorites` only | No GeoNames search; no custom saved places section; no ranking |
| Map location search (`map_CURRENT.html`) | `#citySearch` exact-match against `cities.js` placeholder | No favorites/custom merge; no `/places/search` |
| Family A editors | `current_location_editor.js` via `place_search_client.js` | **Out of scope** — placeholder stays "Search locations" / city typing copy |

Doctrine from `results/95_comparison_workflow_truth_audit.md`: Family B placeholder **"Search locations or favorites"**; starter on focus with **Favorites** + **Locations** sections; typed search only after **2+ chars**; ranked merge with `place_id` dedupe.

# Files Changed

| File | Change |
|------|--------|
| `saved_location_search_service.js` | **New** — `RMSavedLocationSearch`: favorites + `map_custom` enrichment, GeoNames via `RMPlaceSearch`, ranking, dedupe, starter sections |
| `saved_location_search_ui.js` | **New** — `RMSavedLocationSearchUI.mount()`: input, debounced panel, keyboard nav, source badges |
| `main_centerline_FIXER.py` | Serve `place_search_client.js`, `saved_location_search_service.js`, `saved_location_search_ui.js` |
| `repositories/account_favorites_repository.py` | Favorites list includes `provider`, `geonames_id`, `country_code`, `admin1` for search enrichment |
| `app_shell.html` | Compare picker → unified search mount; chip + hidden `.rm-cmp-pick` for build handler; `addComparisonPick` / `mountComparisonLocationSearch` |
| `map_CURRENT.html` | Replace exact-name `#citySearch` with `#rm-map-loc-search-mount`; `openSavedLocationSearchResult` recenters + popup |
| `scripts/smoke_comparison_sets.py` | Family B placeholder, starter, merge-search; build via `addComparisonPick` |
| `scripts/smoke_map_current.py` | Family B placeholder, starter panel, London merge (supabase profile select) |

# Family B Contract

| Rule | Implementation |
|------|----------------|
| Placeholder | `"Search locations or favorites"` (`RMSavedLocationSearch.PLACEHOLDER`) |
| Sources | `GET /favorites` + `/place/{id}` meta (`map_custom` → Locations); `GET /places/search` |
| Empty focused | Sections: **Favorites**, **Locations**; no typed results until `query.length >= 2` |
| Ranking | exact fav → exact custom → exact GeoNames → prefix fav/custom → prefix GeoNames → contains fav/custom → contains GeoNames |
| Dedupe | By `place_id` (`dedupeResults`) |
| Family A untouched | Birth/current/relocated editors keep existing placeholders |

# Compare Integration

- Picker panel: `#rm-cmp-loc-search-mount` + `#rm-cmp-selected` chips
- Select → `addComparisonPick(place_id, name)` appends chip with hidden checked `.rm-cmp-pick`
- **Build comparison** still reads `document.querySelectorAll(".rm-cmp-pick:checked")` — unchanged
- Restored set chips pre-render from `comparisonPickChipHtml` with checked picks

# Map Integration

- `#rm-map-loc-search-mount` replaces legacy exact-name input
- On select: `map.setView(lat, lon, 6)` then `openDatasetCityPopup(...)` (coordinate fallback via `/place/{id}`)
- Profile change: `invalidateProfile` + remount search
- Script chain: `place_search_client.js` → `saved_location_search_service.js` → `saved_location_search_ui.js`

# Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_map_current.py       # PASS 22/22
venv/bin/python scripts/smoke_comparison_sets.py   # PASS 22/22
```

New smoke IDs: `family_b_placeholder`, `family_b_starter_panel`, `family_b_geonames_merge` (map); `fe_family_b_placeholder`, `fe_family_b_starter`, `fe_family_b_merge_search` (compare).

# C-UX-3 Verdict

**PASS** — Family B unified saved-location search ships on compare picker and map location panel. Family A location editors unchanged. Ready for C-UX-4 comparison overlay.
