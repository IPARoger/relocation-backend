# W2-WIRE-4: Family B search quality + map search cleanup

**Date:** 2026-06-19  
**Scope:** `map_CURRENT.html`, `saved_location_search_service.js`, `saved_location_search_ui.js`, `scripts/smoke_favorites.py`

## Summary

Family B search is now the **only** map location entry point. The legacy “Recenter a saved favorite” dropdown was removed. Search ranking, state-aware matching, stale-result handling, custom-location labeling, and a small client query cache were improved.

## Changes

### 1. Map search cleanup (`map_CURRENT.html`)
- Removed `#savedPlacesSection` dropdown (“Recenter a saved favorite”).
- Kept `recenterMapOnPlace` / `openSavedPlace` for shell handoff centering.
- Profile switch now only invalidates Family B cache and remounts search.
- Favorite save invalidates profile cache and refreshes Family B search (no dropdown refresh).

### 2. State-name matching (`saved_location_search_service.js`)
- Added `parseCityStateQuery()` for patterns like `Paris Texas`, `Paris, Texas`, `London Ohio`, `Springfield Missouri`.
- US state names and 2-letter abbreviations resolve to `admin1` (TX, OH, MO, …).
- When a state is present in the query, results must match `admin1`; wrong-state homonyms are excluded.
- City+state exact matches receive a large locality boost.

### 3. Stale results (`saved_location_search_ui.js`)
- On `input`, panel clears immediately when query length ≥ 2; shows “Searching…” for the active query only.
- Removed logic that kept prior results when a same-query empty response arrived.
- Empty “No matching locations” only renders for the latest in-flight response (`searchSeq` guard retained).

### 4. Ranking improvements (`saved_location_search_service.js`)
- Tier order unchanged: exact → prefix → contains; favorites/custom only when `rankTier` matches query.
- `importanceScore()` uses population / importance_rank for famous cities (e.g. Paris, France over Paris, TX when no state in query).
- Favorites/custom no longer appear in typed results unless they match the query.

### 5. Custom location labels (`saved_location_search_service.js`)
- Generic names (`Custom location`, `Saved place`, etc.) replaced with coordinate label: `Saved location near {lat}, {lon}` when no user label exists.
- User-provided `favorite.label` preferred when non-generic.

### 6. Performance
**`/places/search` latency (port 8004, cold curl, 2026-06-19):**

| Query | Latency |
|-------|---------|
| Paris | 8.76s |
| Paris Texas | 5.07s |
| Paris, Texas | 3.80s |
| London Ohio | 4.13s |
| Springfield Missouri | 3.97s |

**Client cache:** 45s TTL, max 48 entries, keyed by `profileId + normalized query`. Cleared on `invalidateProfile()`.

**Backend recommendation:** Latency is high enough that backend caching or index tuning on `search_places_ranked` is warranted next (especially for short city queries). Client cache helps repeat typing/backspace within a session only.

### 7. Security
**Verified (read-only):**
- `GET /favorites?profile_id=` uses JWT + `list_favorites()` which filters `.eq("account_id", account_id).eq("profile_id", profile_id)` and requires owned active profile.
- Family B `fetchFavorites()` sends Bearer token; no cross-account data without auth.
- GeoNames results are global `places` table (expected); saved rows are profile-scoped only.

## Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_map_current.py      # PASS
venv/bin/python scripts/smoke_favorites.py        # PASS (fe_map_search_refresh)
venv/bin/python scripts/smoke_comparison_sets.py  # PASS
```

## Files changed

| File | Change |
|------|--------|
| `map_CURRENT.html` | Remove saved-places dropdown; Family B refresh on favorite save |
| `saved_location_search_service.js` | State parsing, ranking, labels, query cache |
| `saved_location_search_ui.js` | Stale-result / searching UX |
| `scripts/smoke_favorites.py` | Assert favorite in Family B search vs dropdown |

## Rollback

```bash
git checkout -- map_CURRENT.html saved_location_search_service.js saved_location_search_ui.js scripts/smoke_favorites.py
```

## Remaining unverified (manual)

- Browser QA: `Paris Texas` vs `Paris, Texas` ranking against live GeoNames data on :8000/:8004.
- Hover/pointer persistence on search panel after this stale-result change (regression check).
- Whether 8s+ Paris latency is environmental vs RPC cold-start; consider timed p95 sampling in CI.
