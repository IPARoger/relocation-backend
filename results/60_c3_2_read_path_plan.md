# RESULT: 60_c3_2_read_path_plan

**Roadmap ID:** C3-2
**Author:** Cursor (manual copy-paste track)
**Date:** 2026-06-17 UTC

---

## Canonical Read Path (keep)

| Component | Role | Reason to keep |
|-----------|------|----------------|
| `supabase_client.js` | Fetch `/config/supabase`, bootstrap Supabase JS client, expose `window.SupabaseReady` | Single entry point for the authenticated client; all downstream reads depend on it |
| `auth_guard.js` | Gate: confirms session exists before any read | Prevents reads on unauthenticated session; no duplication |
| `user_profile.js` | Loads `CurrentUser` via RPC + `accounts`/`account_memberships` SELECT | Canonical account-identity source; no other file should replicate this |
| `supabase_store_bridge.js` | Assembles product store from Supabase tables → `window.SupabaseStore` / `SupabaseStoreReady` | Only file whose output is typed and tested against `adaptStoreToView()`; READ-ONLY, zero writes |
| `app_shell.html` → `adaptStoreToView()` / `loadViewModelFromStore()` | Consumes bridge output, drives UI | Downstream consumer; not a read source |
| `app_shell.html` → `GET /chart-records` | Engine summaries supplement | JWT-authenticated HTTP GET; does not duplicate bridge data |
| `app_shell.html` → `GET /supabase/chart-records/{id}/engine-birth` | Birth → UTC resolution | Dedicated backend RPC; no bridge equivalent |

---

## Legacy Reads to Consolidate (Chat 4 work)

**Total legacy Supabase reads:** 12 (7 in `app_shell.html` + 5 in `map_CURRENT.html`)
(Exceeds 20-flag threshold: **No** — 12 total. No flag required.)

### app_shell.html

| # | Lines | Table(s) | When | Recommended replacement | Risk |
|---|-------|----------|------|------------------------|------|
| A1 | ~1299–1325 | `comparison_sets`, `comparison_set_places` | Chart-record panel hydration (`hydrateChartRecordComparisonSets`) | Add `comparison_sets` + join to `supabase_store_bridge.js` incremental fetch, or new `GET /comparison-sets?profile_id=` JWT route | MEDIUM — UI-visible; bridge must expose per-chart-record slice |
| A2 | ~2344–2368 | `profiles`, `birth_records`, `places` | Post-create profile patch (`appendCreatedProfileToStore`) | Bridge already owns these tables; extend `SupabaseStore` with a re-fetch-after-create pattern or expose `store.refreshProfile(id)` | LOW — incremental patch; bridge already has all tables |
| A3 | ~3405–3420 | `profiles` | Archive planning (`planProfileArchive`) | Read active profiles from `window.SupabaseStore.profiles` (already in bridge store) | LOW — bridge already caches `profiles`; no new read needed |

### map_CURRENT.html

| # | Lines | Table(s) | When | Recommended replacement | Risk |
|---|-------|----------|------|------------------------|------|
| M1 | ~1859–1875 | `saved_searches` | Reopen saved investigation (`reopenSavedExploration`) | New `GET /saved-investigations/{id}` JWT route (matches write-path pattern) | MEDIUM — map feature; needs new JWT GET route |
| M2 | ~2394–2420 | `places` | Favorite button state check (by geonames_id) | `GET /places/search?q=` already exists at 8004; or add `GET /places?geonames_id=` | LOW — fallback read; already guarded try/catch |
| M3 | ~2419 | `favorite_places` | Favorite button state | New `GET /favorites?profile_id=` JWT GET route (mirrors `/favorites/save` write) | MEDIUM — map-visible; needs new route |
| M4 | ~6180–6195 | `favorite_places`, `places` | Saved-places sidebar (`loadSavedPlacesForActiveProfile`) | New `GET /favorites?profile_id=` JWT GET route (same as M3 above) | MEDIUM — same route satisfies M3+M4 |
| M5 | ~6254 | `places` | Place handoff centering (`centerOnHandoffPlaceId`) | `GET /place/{id}` already exists at 8004 | LOW — read by ID; backend route already live |

---

## Dead Routes to Quarantine (Chat 4 or Chat 5)

All confirmed DEAD in C3-1 / task 42 with 0 production frontend callers.

| Route | Risk | Action |
|-------|------|--------|
| `GET /account-store` | LOW | 410-quarantine via `_quarantine_legacy_read()` |
| `GET /profile-library/{id}` | LOW | 410-quarantine via `_quarantine_legacy_read()` |
| `GET /saved-searches/{profile_id}` | LOW | 410-quarantine via `_quarantine_legacy_read()` |
| `GET /saved-search/{saved_search_id}` | LOW | 410-quarantine via `_quarantine_legacy_read()` |

---

## Recommended canonical read path going forward

`supabase_store_bridge.js` should remain the **single read adapter** for store-level data (`profiles`, `birth_records`, `places`, `saved_searches`, `favorite_places`, `comparison_sets`, `user_settings`, `current_location_history`, `notes`). Its contract — zero writes, typed output, tested against `adaptStoreToView()` — is exactly what is needed. Extending it is lower risk than duplicating the pattern.

`map_CURRENT.html` direct reads should migrate behind **new JWT GET routes** on 8004 (`GET /saved-investigations/{id}`, `GET /favorites?profile_id=`), matching the established write-path pattern. This keeps the map client consistent and makes the routes testable with the existing smoke framework. The two medium-risk reads (M1, M3/M4) are self-contained features and can each be one Chat 4 task.

`app_shell.html` inline reads (A1–A3) should consolidate into the bridge. A2 and A3 are low-risk: A3 can eliminate its read entirely by using already-cached `SupabaseStore.profiles`; A2 needs a `refreshProfile()` extension to the bridge. A1 (`comparison_sets` per chart-record) is the most complex; add as a late Chat 4 slice after JWT route work is stable.

---

## Chat 4 implementation sequence

Ordered by risk ascending, smallest/lowest risk first. One task per slice.

1. **C4-1 (S):** `app_shell.html` A3 — eliminate `planProfileArchive` inline read; use `window.SupabaseStore.profiles` cache. No new route. Smoke: `smoke_map_current.py`.
2. **C4-2 (M):** `map_CURRENT.html` M2 + M5 — replace `places` geonames lookup (M2) and handoff place-center (M5) with existing `GET /places/search?q=` and `GET /place/{id}` backend routes. No new route needed. Smoke: ownership + `smoke_map_current.py`.
3. **C4-3 (M):** New `GET /favorites?profile_id=` JWT route on 8004. Migrate `map_CURRENT.html` M3 + M4 to use it. Smoke: new route smoke + `smoke_map_current.py`.
4. **C4-4 (M):** New `GET /saved-investigations/{id}` JWT route on 8004. Migrate `map_CURRENT.html` M1 to use it. Smoke: new route smoke + `smoke_saved_investigations.py`.
5. **C4-5 (M):** `app_shell.html` A2 — add `store.refreshProfile(id)` to `supabase_store_bridge.js`; migrate `appendCreatedProfileToStore` to use it. Smoke: `smoke_map_current.py`.
6. **C4-6 (L):** `app_shell.html` A1 — add `comparison_sets`+`comparison_set_places` per-chart-record slice to bridge or JWT route. Migrate `hydrateChartRecordComparisonSets`. Smoke: smoke_map_current.
7. **C4-7 (S):** 410-quarantine 4 dead GET routes (`/account-store`, `/profile-library/{id}`, `/saved-searches/{profile_id}`, `/saved-search/{saved_search_id}`). Smoke: `smoke_legacy_writes_deprecated.py` extended or new dead-reads smoke.

---

**VERIFIED**

All 4 plan sections complete. Chat 4 sequence has 7 ordered slices (≥ 3). No source files modified.
