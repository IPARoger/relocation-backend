# PRODUCTION DEPENDENCY MATRIX

**Status:** Production reference  
**Last updated:** 2026-06-14  
**Purpose:** Feature-by-feature dependency table. Use this to determine what must be running, wired, and verified before any given feature can work.

---

## STATUS LABELS

| Label | Meaning |
|---|---|
| REAL | Fully wired, tested, confirmed working |
| PARTIAL | Wired but incomplete; known limitations |
| MOCKED | Placeholder / static data; not real values |
| BLOCKED | Cannot function until a prerequisite is resolved |
| DEFERRED | Intentionally not implemented; no target date |
| LEGACY | Wired to old port 8000 system; may be absent |
| OUT OF SCOPE | Not planned for current phase |

---

## FEATURE DEPENDENCY TABLE

### 1. AUTH — Email/Password

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `auth.html`, `supabase_client.js`, `auth_guard.js` |
| **Backend endpoint(s)** | None (Supabase Auth hosted) |
| **Supabase table(s)** | `auth.users`, `accounts`, `account_memberships` |
| **Required global objects** | `window.SupabaseClient` (from `supabase_client.js`) |
| **Required env vars** | `SUPABASE_URL`, `SUPABASE_ANON_KEY` (served via `GET /config/supabase`) |
| **Required port** | 8004 (to serve auth.html and supabase config) |
| **Current status** | **REAL** |
| **Blockers** | `handle_new_user()` trigger must exist in Supabase project |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §1 |

---

### 2. GOOGLE AUTH

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `auth.html` |
| **Backend endpoint(s)** | None (Supabase OAuth) |
| **Supabase table(s)** | `auth.users` |
| **Required global objects** | `window.SupabaseClient` |
| **Required env vars** | Google OAuth Client ID configured in Supabase Auth Providers |
| **Required port** | 8004 |
| **Current status** | **DEFERRED** |
| **Blockers** | Not implemented. No `signInWithOAuth({provider:'google'})` call in `auth.html`. Requires Google Cloud Console OAuth app. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §2 |

---

### 3. APPLE AUTH

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `auth.html` |
| **Backend endpoint(s)** | None (Supabase OAuth) |
| **Supabase table(s)** | `auth.users` |
| **Required global objects** | `window.SupabaseClient` |
| **Required env vars** | Apple Developer credentials configured in Supabase Auth Providers |
| **Required port** | 8004 |
| **Current status** | **DEFERRED** |
| **Blockers** | Not implemented. Requires Apple Developer account. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §3 |

---

### 4. ACCOUNT BOOTSTRAP

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `user_profile.js`, `supabase_client.js` |
| **Backend endpoint(s)** | None (runs via Supabase trigger) |
| **Supabase table(s)** | `accounts`, `account_memberships`, `auth.users` |
| **Required global objects** | `window.SupabaseClient`, `window.CurrentUser` (set by `user_profile.js`) |
| **Required env vars** | `SUPABASE_URL`, `SUPABASE_ANON_KEY` |
| **Required port** | 8004 |
| **Current status** | **REAL** |
| **Blockers** | `handle_new_user()` trigger must exist. If absent: `app_account_ids()` returns empty, `window.CurrentUser` is null, all downstream features fail. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §1 (verify `accounts` + `account_memberships` rows) |

---

### 5. FIRST PROFILE INTAKE

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `first_profile_intake.js`, `supabase_client.js`, `user_profile.js`, `supabase_store_bridge.js` |
| **Backend endpoint(s)** | `POST http://127.0.0.1:8004/profiles`, `POST http://127.0.0.1:8004/birth-records` |
| **Supabase table(s)** | `profiles`, `birth_records`, `places` |
| **Required global objects** | `window.SupabaseClient`, `window.CurrentUser` (with `accountId`), `window.SupabaseReady` |
| **Required env vars** | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` (backend) |
| **Required port** | 8004 |
| **Current status** | **REAL** |
| **Blockers** | `places` table must have GeoNames data loaded (~68,032 rows). City search quality is functional but not production-ready (see city search row). |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §4, §5 |

---

### 6. PROFILE SELECTOR

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `map_CURRENT.html` (`loadChartProfiles()`, `applyActiveProfileSelection()`) |
| **Backend endpoint(s)** | `GET http://127.0.0.1:8004/profiles` |
| **Supabase table(s)** | `profiles` |
| **Required global objects** | None (direct fetch; profile UUIDs populated into `#chartProfile` dropdown) |
| **Required env vars** | `SUPABASE_SERVICE_ROLE_KEY` (backend — query is service-role) |
| **Required port** | 8004 |
| **Current status** | **PARTIAL** |
| **Blockers** | `/profiles` endpoint returns all profiles across all accounts (no user scoping). Multi-tenant data leak risk in production with multiple users on the same server. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §6 |

---

### 7. CURRENT LOCATION

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `current_location_editor.js`, `account_drawer.js`, `app_shell.html` |
| **Backend endpoint(s)** | None (Supabase JS direct) |
| **Supabase table(s)** | `current_location_history`, `places` |
| **Required global objects** | `window.SupabaseClient`, `window.CurrentUser` (with `accountId`) |
| **Required env vars** | `SUPABASE_URL`, `SUPABASE_ANON_KEY` |
| **Required port** | 8004 (to serve JS assets) |
| **Current status** | **REAL** |
| **Blockers** | None |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §7 |

---

### 8. SETTINGS

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `app_shell.html` (`screenSettings()`, `save-settings` action) |
| **Backend endpoint(s)** | `POST http://127.0.0.1:8004/user-settings`, `PATCH http://127.0.0.1:8004/user-settings/{id}` |
| **Supabase table(s)** | `user_settings` |
| **Required global objects** | `window.SupabaseClient`, `window.CurrentUser` (with `accountId`), `window.SupabaseStoreReady` |
| **Required env vars** | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` (backend) |
| **Required port** | 8004 |
| **Current status** | **PARTIAL** |
| **Blockers** | Settings fields (`default_chart_record_id`, `house_system`) are stored but `house_system` does not currently drive the chart engine in `map_CURRENT.html`. Settings save is functional; effect is incomplete. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §15 |

---

### 9. MAP LAUNCH

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `map_CURRENT.html`, `supabase_store_bridge.js`, `auth_guard.js`, `user_profile.js`, `supabase_client.js`, `first_profile_intake.js`, `place_resolution.js` |
| **Backend endpoint(s)** | `GET http://127.0.0.1:8004/profiles`, `GET http://127.0.0.1:8004/supabase/chart-records/{id}/engine-birth` |
| **Supabase table(s)** | `profiles`, `birth_records`, `places` |
| **Required global objects** | `window.SupabaseClient`, `window.CurrentUser`, `window.SupabaseStoreReady` |
| **Required env vars** | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` (backend) |
| **Required port** | 8004 |
| **Current status** | **REAL** |
| **Blockers** | None for basic map load. Aura overlays and popup charts blocked (see below). |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §8 |

---

### 10. FIND REGIONS (house/planet polygon overlays)

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `map_CURRENT.html` (`findRegions()`, `postSearchRegions()`, `fetchEngineBirthForChartRecord()`) |
| **Backend endpoint(s)** | `GET http://127.0.0.1:8004/supabase/chart-records/{id}/engine-birth`, `POST http://127.0.0.1:8004/search-regions` |
| **Supabase table(s)** | `birth_records`, `places` |
| **Required global objects** | None beyond what map launch requires |
| **Required env vars** | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` (backend), Python math engine loaded in FastAPI |
| **Required port** | 8004 |
| **Current status** | **REAL** |
| **Blockers** | Profile with `birth_time_mode='exact'` required. "Unknown" birth time returns 422 from engine-birth. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §9 |

---

### 11. ANGULAR OVERLAYS (aura/aspect lines)

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `map_CURRENT.html` (`renderRasterAura()`, `renderAdaptiveAuraProgressive()`, `renderAuraField()`) |
| **Backend endpoint(s)** | `POST http://127.0.0.1:8000/aura-raster`, `POST http://127.0.0.1:8000/aura-raster-adaptive`, `POST http://127.0.0.1:8000/aura-field` |
| **Supabase table(s)** | None |
| **Required global objects** | None |
| **Required env vars** | None (port 8000 server) |
| **Required port** | **8000 (legacy — not migrated)** |
| **Current status** | **LEGACY / BLOCKED** |
| **Blockers** | Port 8000 legacy server must be running. Endpoints not migrated to 8004. No migration scheduled. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §10 |

---

### 12. POPUP RELOCATED CHART

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `map_CURRENT.html` (`fetchRelocatedChart()`, `getAspectOrbAtPoint()`) |
| **Backend endpoint(s)** | `GET http://127.0.0.1:8000/relocated-chart`, `GET http://127.0.0.1:8000/aspect-orb-at-point` |
| **Supabase table(s)** | None |
| **Required global objects** | Active profile + birth params |
| **Required env vars** | None (port 8000 server) |
| **Required port** | **8000 (legacy — not migrated)** |
| **Current status** | **LEGACY / BLOCKED** |
| **Blockers** | Port 8000 required. Endpoints not migrated. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §10 (combined with angular overlays) |

---

### 13. FAVORITES

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `map_CURRENT.html` (`favoriteMapSelectionFromButton()`, `applyMapFavoriteButtonState()`), `place_resolution.js` |
| **Backend endpoint(s)** | `GET http://127.0.0.1:8004/places/search`, `POST http://127.0.0.1:8004/places` (for place resolution) |
| **Supabase table(s)** | `favorite_places`, `places` |
| **Required global objects** | `window.SupabaseClient`, `window.CurrentUser` (with `accountId`), `window.RMPlaceResolution` |
| **Required env vars** | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` (backend) |
| **Required port** | 8004 |
| **Current status** | **REAL** |
| **Blockers** | `window.CurrentUser.accountId` must be populated (account bootstrap complete). Active profile must be a Supabase UUID (not a legacy chart ID). |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §11 |

---

### 14. NOTES

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `app_shell.html` (`screenChartRecord()`, `save-chart-note` action) |
| **Backend endpoint(s)** | None (localStorage only) |
| **Supabase table(s)** | `notes` (exists; NOT wired to UI) |
| **Required global objects** | None |
| **Required env vars** | None |
| **Required port** | 8004 (asset serving only) |
| **Current status** | **PARTIAL** |
| **Blockers** | Supabase `notes` table exists but is not wired. Current implementation is localStorage-only — not persistent across devices or browsers. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §14 |

---

### 15. HELP

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `app_shell.html` (`screenHelp()`), `account_drawer.js` (navigation link) |
| **Backend endpoint(s)** | None |
| **Supabase table(s)** | None |
| **Required global objects** | None |
| **Required env vars** | None |
| **Required port** | 8004 (asset serving only) |
| **Current status** | **PARTIAL** |
| **Blockers** | Content is static placeholder text. Not a live CMS. Requires code change to update content. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §17 |

---

### 16. GUIDED ONBOARDING

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `app_shell.html` (`maybeShowGuidedOnboarding()`, onboarding modal) |
| **Backend endpoint(s)** | None |
| **Supabase table(s)** | None |
| **Required global objects** | None |
| **Required env vars** | None |
| **Required port** | 8004 (asset serving only) |
| **Current status** | **PARTIAL** |
| **Blockers** | Modal content is minimal/static. No multi-step walkthrough. Dismissal state is localStorage-only (not per-account). Onboarding styling absent. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §18 |

---

### 17. SAVED INVESTIGATIONS

| Dimension | Value |
|---|---|
| **Frontend file(s)** | None wired |
| **Backend endpoint(s)** | `POST http://127.0.0.1:8004/saved-searches`, `GET http://127.0.0.1:8004/saved-searches/{profile_id}` |
| **Supabase table(s)** | `saved_searches` |
| **Required global objects** | N/A |
| **Required env vars** | N/A |
| **Required port** | 8004 |
| **Current status** | **DEFERRED** |
| **Blockers** | No frontend UI wired. Backend exists and is ready. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §12 |

---

### 18. SAVED COMPARISONS

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `app_shell.html` (`screenCompare()`) |
| **Backend endpoint(s)** | `POST http://127.0.0.1:8004/comparison-sets`, `POST http://127.0.0.1:8004/comparison-sets/{id}/places` |
| **Supabase table(s)** | `comparison_sets`, `comparison_set_places` |
| **Required global objects** | `window.SupabaseStoreReady` |
| **Required env vars** | `SUPABASE_SERVICE_ROLE_KEY` (backend) |
| **Required port** | 8004 |
| **Current status** | **PARTIAL** |
| **Blockers** | Comparison creation UI not user-accessible. Comparison facts are mocked/placeholder (not computed from chart engine). |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §13 |

---

### 19. COMPARISON FACTS

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `app_shell.html` `screenCompare()` |
| **Backend endpoint(s)** | `POST http://127.0.0.1:8000/relocated-chart` (legacy) — not yet wired for comparison |
| **Supabase table(s)** | None (computed on demand, not stored) |
| **Required global objects** | Active profile + birth params, comparison city coordinates |
| **Required env vars** | N/A |
| **Required port** | 8000 (legacy) |
| **Current status** | **MOCKED** |
| **Blockers** | Requires: (1) relocated chart endpoint migrated to 8004, (2) comparison cities wired to chart engine, (3) diff engine implemented. None of these are done. |
| **Smoke test reference** | None — not testable in current state |

---

### 20. DIFFS

| Dimension | Value |
|---|---|
| **Frontend file(s)** | None wired |
| **Backend endpoint(s)** | None |
| **Supabase table(s)** | None |
| **Required global objects** | Requires real comparison facts |
| **Required env vars** | N/A |
| **Required port** | N/A |
| **Current status** | **BLOCKED** |
| **Blockers** | Comparison facts must be REAL before diffs can be computed. Comparison facts are currently MOCKED. |
| **Smoke test reference** | None |

---

### 21. EXPORTS

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `app_shell.html` (`screenExport()` placeholder) |
| **Backend endpoint(s)** | None |
| **Supabase table(s)** | None |
| **Required global objects** | N/A |
| **Required env vars** | N/A |
| **Required port** | 8004 (asset serving only) |
| **Current status** | **DEFERRED** |
| **Blockers** | Not implemented. Screen renders but has no functional controls. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §16 |

---

### 22. CITY SEARCH

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `first_profile_intake.js` (intake overlay), `current_location_editor.js` (location editor), `cities.js` (GeoNames dataset, ~12MB, map typeahead) |
| **Backend endpoint(s)** | `GET http://127.0.0.1:8004/places/search?q=` (server-side search proxy) |
| **Supabase table(s)** | `places` |
| **Required global objects** | `window.SupabaseClient` (for intake/location editor direct queries), `window.RMPlaceResolution` (for place resolution) |
| **Required env vars** | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` (backend) |
| **Required port** | 8004 |
| **Current status** | **PARTIAL** |
| **Blockers** | Functional for prefix search on canonical names. NOT production-ready: no alternate names, no historical names, no transliterations, no abbreviations, no typo tolerance. "NYC" → no results. "Bombay" → no results. Must meet CITY_SEARCH_PRODUCTION_REQUIREMENTS.md §11 before production launch. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §5 |

---

### 23. GENIE PRODUCTION INTEGRATION

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `genie_variable_builder.js`, `genie_map_engine_adapter.js`, `substrate_adapter.js` |
| **Backend endpoint(s)** | None (Genie is browser-side) |
| **Supabase table(s)** | None |
| **Required global objects** | `window.__rmAvailableObjectsRegistry`, `window.RelocationGenieMapEngineAdapter`, `window.RelocationSubstrateAdapter` |
| **Required env vars** | None |
| **Required port** | 8004 (asset serving) |
| **Current status** | **PARTIAL** |
| **Blockers** | Genie is present as infrastructure. The production map uses the Python engine for polygon rendering, not Genie. Genie render payload handoff (via sessionStorage) breaks on new-tab navigation. Genie is NOT the production render driver. |
| **Smoke test reference** | None — integration not smoke-tested |

---

### 24. EMAIL STYLING

| Dimension | Value |
|---|---|
| **Frontend file(s)** | Supabase Auth email templates (configured in Supabase dashboard) |
| **Backend endpoint(s)** | None |
| **Supabase table(s)** | None |
| **Required global objects** | N/A |
| **Required env vars** | N/A |
| **Required port** | N/A |
| **Current status** | **DEFERRED** |
| **Blockers** | Supabase default email templates are in use. No branded/styled email templates have been configured. Confirmation emails, password reset emails use Supabase defaults. |
| **Smoke test reference** | None |

---

### 25. ONBOARDING STYLING

| Dimension | Value |
|---|---|
| **Frontend file(s)** | `app_shell.html` (onboarding modal inline styles/content) |
| **Backend endpoint(s)** | None |
| **Supabase table(s)** | None |
| **Required global objects** | None |
| **Required env vars** | None |
| **Required port** | 8004 (asset serving) |
| **Current status** | **DEFERRED** |
| **Blockers** | Onboarding modal content is minimal placeholder text with no visual design applied. Not production-ready as a first-time user experience. |
| **Smoke test reference** | OPERATIONAL_SMOKE_TESTS.md §18 |
