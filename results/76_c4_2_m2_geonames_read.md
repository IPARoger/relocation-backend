# RESULT: 76_c4_2_m2_geonames_read

**Roadmap ID:** C4-2 M2
**Date:** 2026-06-18

## Files Changed

| File | Change |
|------|--------|
| `repositories/places_repository.py` | Added `search_places_by_geonames(geonames_id)` — returns 0–1 row as list |
| `main_centerline_FIXER.py` | `GET /places/search` accepts optional `geonames_id` or `q`; 422 if neither |
| `map_CURRENT.html` | `applyMapFavoriteButtonState` geonames lookup → `fetch(/places/search?geonames_id=...)` |

## Backend Search Behavior

| Request | Response |
|---------|----------|
| `GET /places/search?q=<name>&limit=N` | Unchanged — ILIKE display_name, ordered by importance |
| `GET /places/search?geonames_id=<id>` | List with matching place or `[]` (200) |
| `GET /places/search` (no params) | 422 `missing_query` |

`POST /places/resolve-or-create` and `POST /places` (410) untouched.

## Frontend Read Path

**Before:** `sbClient.from("places").select("id").eq("geonames_id", geonamesId)`

**After:** `fetch(\`${API_BASE}/places/search?geonames_id=${encodeURIComponent(geonamesId)}\`)` — uses first match `row.id`; display-name + coordinate fallback unchanged.

## Validation

| Script | Exit | Result |
|--------|------|--------|
| `smoke_map_current.py` | 0 | `overall_pass: true` |
| `smoke_favorites.py` | 0 | 17/17 PASS |
| `smoke_place_resolution.py` | 0 | 8/8 PASS |

| Grep | Result |
|------|--------|
| `from("places")` in `map_CURRENT.html` | **0 matches** |

Manual route check (restarted server): `?geonames_id=99999999` → `200 []`; bare `/places/search` → `422`.

## Remaining Places Reads

| File | Direct Supabase `places` reads |
|------|-------------------------------|
| `map_CURRENT.html` | **None** |

Bridge and backend repositories still read `places` table (expected).

## C4-2 M2 Verdict

**VERIFIED**
