# W2-WIRE-3 — QA cleanup closeout

**Date:** 2026-06-19  
**Scope:** Small fixes from QA screenshots/notes (post :8000 restart). No genie/ghost, settings, notes, exports, dignity, or renderer changes.

---

## Delivered

### 1. Map popup — single favorite control (Web2)

- **One** favorite control in compact map popup (not two buttons; no star/rating in popup).
- Not saved: **Favorite** button.
- Saved: **Favorited ✓** span (replaces button).
- `dedupePopupFavoriteButtons()` + `markPopupFavoriteSaved()` guard against legacy duplicate markup.
- Star/rating behavior deferred to Profile / Comparison / detail pages.

### 2. View relocated chart — place context

- Map popup **View relocated chart** passes `chartRecordId` + `placeId` (+ lat/lon/name backup) in hash.
- `sessionStorage` handoff (`rm_shell_chart_handoff`) + `repairChartHashFromHandoff()` on app shell bootstrap.
- `registerHandoffPlaceInMemory()` so Screen 4 can resolve coordinates.

### 3. Saved-place dropdown

- Selecting a saved place **recenters only** (`recenterMapOnPlace`); does not open chart popup.

### 4. Family B search messaging

- Distinct empty states in `saved_location_search_ui.js`:
  - typing → “Type at least 2 characters…”
  - starter → “No saved favorites yet. Type to search locations.”
  - results → “No matching locations or favorites.”
- “Searching locations…” status while querying.

### 5. Chart Record compare from favorites

- Checkboxes on favorites + **Compare selected** (2–5 picks).
- Uses `createComparisonSetFromPlaceIds` → navigate to compare screen.

### 6. Paris ranking sanity

- `localityBoost()` + population/importance in `saved_location_search_service.js`.
- Paris, France ranks above Paris, IL for query `paris`.

### 7. Custom location labels / UUID leakage

- Favorites use `fav.notes` (label) instead of raw `place_id` in UI.
- `humanPlaceLabel()` — comparison chips/workspace never show bare UUIDs.

---

## Files touched

| File | Change |
|------|--------|
| `map_CURRENT.html` | Single favorite control, chart handoff, saved-place recenter |
| `app_shell.html` | Chart handoff consume, compare checkboxes, human labels |
| `saved_location_search_ui.js` | Search messaging states |
| `saved_location_search_service.js` | Paris/locality ranking |
| `scripts/smoke_favorites.py` | Profile wait + favorited span assertion |

---

## Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_map_current.py      # PASS
venv/bin/python scripts/smoke_favorites.py        # PASS
venv/bin/python scripts/smoke_comparison_sets.py  # PASS
```

---

## Manual QA checklist

1. Map right-click popup → **one** Favorite OR Favorited ✓ (never both).
2. **View relocated chart** → Screen 4 with chart + place (hash includes `placeId`).
3. Saved-places dropdown → map recenters, no popup.
4. Search “paris” → France above IL; empty states correct when no hits.
5. Chart Record → select 2–5 favorites → **Compare selected**.
6. Comparison chips show place names, not UUIDs.
