# A3 GeoNames Alternate-Name Search — Implementation Closeout

**Date:** 2026-06-18  
**Roadmap:** `docs/roadmaps/active/WEB2_COMPLETION__ACTIVE__2026-06-18.md`  
**Strategy:** `results/88_a3_geonames_alternate_names_strategy.md`

## Verdict: **PASS**

Launch-critical alias search is implemented, imported, deployed to staging, and validated end-to-end.

---

## 1. Import Completion

| Metric | Value |
|--------|------:|
| `places` rows | 68,038 |
| `place_aliases` total | 433,369 |
| `geonames_main` | 433,353 |
| `override` (launch pairs) | 16 |
| Importer processes running | **0** (none at verification time) |

**Target:** ~433,353 `geonames_main` rows — **met** (433,353).

### Sample aliases (staging)

| City | geonames_id | Query aliases present |
|------|-------------|------------------------|
| Mumbai | 1275339 | Bombay (override + geonames_main) |
| Kochi | 1273874 | Cochin (override + geonames_main) |
| Prague | 3067696 | Praha (override + geonames_main) |
| Köln | 2886242 | Cologne, Koeln (override + geonames_main) |
| Beijing | 1816670 | Peking (override + geonames_main) |

Canonical names (Mumbai, Kochi, Prague, Köln, Beijing) resolve via exact canonical/display match; historic exonyms via alias + override rows.

### Constraint health

- PK `place_aliases_pkey` — OK
- FK `place_aliases_place_id_fkey` → `places(id)` ON DELETE CASCADE — OK
- CHECK `place_aliases_source_check` (`geonames_main`, `geonames_v2`, `override`) — OK
- UNIQUE `place_aliases_place_norm_source_uidx` on `(place_id, normalized_alias, source)` — OK

---

## 2. Backend Search Integration

**Route:** `GET /places/search` in `main_centerline_FIXER.py`  
**Repository:** `repositories/places_repository.py` → `search_places()` / `search_places_by_geonames()`

**Ranking** via `search_places_ranked` RPC (`supabase/migrations/2026_06_18_place_aliases.sql`):

1. Exact canonical / display primary segment
2. Exact normalized alias
3. Prefix canonical / display
4. Prefix normalized alias
5. ILIKE fallback on `display_name` / `canonical_name`

**Preserved behavior:**
- `q=` text search and `geonames_id=` lookup
- Frontend response shape (`_PLACE_FIELDS`); `matched_alias` included when present
- Dedupe by `place_id`; sort by `match_rank`, then `importance_rank`, population, name

**RPC on staging:** deployed and callable (`supabase db query --linked` verified).

**Fallback:** `_search_places_fallback()` — legacy `display_name ILIKE` if RPC unavailable.

---

## 3. Frontend Caller Audit

| Caller | Path | Status |
|--------|------|--------|
| `map_CURRENT.html` | `GET /places/search` | OK (direct API) |
| `first_profile_intake.js` | `RMPlaceSearch.searchPlaces` → `/places/search` | **Fixed** (was direct Supabase) |
| `current_location_editor.js` | `RMPlaceSearch.searchPlaces` → `/places/search` | OK |
| `place_search_client.js` | Shared client | **New** |
| `app_shell.html`, `map_CURRENT.html` | Load `place_search_client.js` | OK |
| Comparison / favorites | `map_CURRENT.html` resolution paths | OK (backend API) |

**No remaining direct Supabase `places` ILIKE search in scoped intake/editor paths.**

---

## 4. Smoke / QA Results

All run with `.env.staging`, API on `:8004`.

| Script | Result |
|--------|--------|
| `scripts/smoke_place_alias_search.py` | **31/31 PASS** (29 alias cases + geonames_id + 422) |
| `scripts/smoke_place_resolution.py` | **9/9 PASS** |
| `scripts/smoke_map_current.py` | **PASS** |
| `scripts/smoke_favorites.py` | **17/17 PASS** |

### 29-case alias matrix (all PASS)

NYC, New York, Bombay, Mumbai, Madras, Chennai, Calcutta, Kolkata, Cochin, Kochi, Praha, Prague, Köln, Cologne, Koeln, Kiev, Kyiv, Peking, Beijing, Firenze, Florence, Roma, Rome, Moskva, Moscow, Lisboa, Lisbon, Wien, Vienna.

---

## 5. About / Data Sources

Added in `prototype_settings_v2.html` → **Data Sources** section:

- Swiss Ephemeris — astronomical calculations
- GeoNames — city and place names, alternate/historic forms (CC BY 4.0)
- IANA Time Zone Database — time zone identifiers
- Leaflet — interactive map display
- OpenStreetMap — map tiles

Attribution is discreet (settings), not on map/chart surfaces. GeoNames is **not** labeled "Place database".

---

## 6. Remaining Gaps (post-launch)

| Gap | Notes |
|-----|-------|
| `alternateNamesV2.zip` | Not imported; Tier-1 `cities500` alternatenames only |
| Diacritic-native canonical match | `Köln` relies on ILIKE/display when norm `koln` ≠ DB `köln`; works in QA but could add `koln` override for hardening |
| Homonym edge cases | Rare substring false positives outside the 29-case set |
| `geonames_v2` source | Schema ready; import script stub only |
| Periodic refresh | No automated monthly GeoNames re-import job |

**Madras → Chennai:** **PASS** (override + alias rank correctly over Madras, OR).

---

## Files Touched (A3 scope)

- `supabase/migrations/2026_06_18_place_aliases.sql`
- `utils/place_alias_normalize.py`, `utils/__init__.py`
- `repositories/places_repository.py`
- `scripts/import_place_aliases_cities500.py`, `scripts/import_place_aliases_v2.py`
- `scripts/smoke_place_alias_search.py`
- `place_search_client.js`
- `first_profile_intake.js`, `current_location_editor.js`, `map_CURRENT.html`, `app_shell.html`
- `prototype_settings_v2.html`
