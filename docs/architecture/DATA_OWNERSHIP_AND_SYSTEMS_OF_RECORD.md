# DATA OWNERSHIP AND SYSTEMS OF RECORD

**Status:** Production reference  
**Last updated:** 2026-06-14  
**Purpose:** Define what owns each kind of data, where it lives, how it is read and written, and what its production-readiness status is. Use this to prevent wiring drift, ghost writes, and incorrect data sources being treated as canonical.

---

## READING THIS DOCUMENT

Status labels used throughout:
- **REAL** — wired, tested, canonical
- **PARTIAL** — wired but incomplete; known gaps
- **MOCKED** — placeholder or static data, not real values
- **DEFERRED** — intentionally not implemented yet
- **LEGACY** — lives in old system; not migrated; may be absent
- **NOT CANONICAL** — do not treat as source of truth

---

## 1. AUTH USERS

**Canonical source of truth:** Supabase Auth (`auth.users`) — hosted Postgres, Supabase-managed

**Status:** REAL

**Read paths:**
- `auth_guard.js`: `supabase.auth.getSession()` — browser session check
- `user_profile.js`: `supabase.auth.getUser()` — fetches authenticated user object, extracts `user.id`
- `supabase.auth.onAuthStateChange()` — event listener for login/logout/confirmation

**Write paths:**
- `auth.html`: `supabase.auth.signUp()` — creates `auth.users` row
- `auth.html`: `supabase.auth.signInWithPassword()` — creates session
- `auth.html`: `supabase.auth.resetPasswordForEmail()` — sends reset email
- `auth_guard.js` (via `window.logout()`): `supabase.auth.signOut()` — destroys session

**Local/session cache:**
- Supabase SDK manages session persistence in browser localStorage automatically
- No manual caching in application code

**What must never be treated as canonical:**
- `window.CurrentUser.userId` is derived from `auth.users.id` — it is a copy, not the source. Read it for convenience; never write to `auth.users` through it.

---

## 2. ACCOUNTS

**Canonical source of truth:** Supabase `accounts` table

**Status:** REAL

**Read paths:**
- `user_profile.js`: calls `app_account_ids()` RPC → returns array of account IDs for current user
- `account_drawer.js`: reads `window.CurrentUser.accountId`, `window.CurrentUser.accountName`, `window.CurrentUser.accountType`

**Write paths:**
- `handle_new_user()` SECURITY DEFINER trigger — the ONLY write path. Fires on `auth.users` INSERT.
- No browser code writes directly to `accounts`.
- RLS prohibits all browser-originating writes.

**Local/session cache:**
- `window.CurrentUser` (set by `user_profile.js`) — runtime copy of account data. Not persisted across page loads; re-derived on every load.

**What must never be treated as canonical:**
- `window.CurrentUser` is a derived runtime object. The database row is canonical.
- Do not attempt to CREATE or UPDATE `accounts` from browser code — RLS blocks it and `handle_new_user()` is the sole bootstrap path.

---

## 3. ACCOUNT MEMBERSHIPS

**Canonical source of truth:** Supabase `account_memberships` table

**Status:** REAL

**Read paths:**
- `user_profile.js` via `app_account_ids()` RPC — indirectly; the RPC queries `account_memberships` internally

**Write paths:**
- `handle_new_user()` trigger only — creates a single membership row (role='owner') at signup

**What must never be treated as canonical:**
- No UI surface exists yet for managing memberships (adding team members, changing roles). The only membership that exists per account is the owner's membership created at signup.

---

## 4. PROFILES

**Canonical source of truth:** Supabase `profiles` table

**Status:** REAL

**Read paths:**
- `supabase_store_bridge.js`: authenticated Supabase JS client, `SELECT profiles WHERE account_id IN (app_account_ids())` — user sees only their own account's profiles
- `GET http://127.0.0.1:8004/profiles`: service-role key, **returns ALL profiles across all users** — used by `map_CURRENT.html loadChartProfiles()`. **RISK: Multi-tenant data leak if multiple users on same server. Do not deploy to shared production without adding account_id filter.**
- `GET http://127.0.0.1:8004/profiles/{id}`: single profile by UUID

**Write paths:**
- `first_profile_intake.js` → `POST http://127.0.0.1:8004/profiles` — service-role key; creates new profile row
- `POST /profiles/{id}/archive` — soft-delete (not yet surfaced in UI)

**Local/session cache:**
- `window.__rmAppShell.viewModel().chartRecords` — runtime copy populated by `supabase_store_bridge.js`. Refreshed on page load.
- `sessionStorage: rm_active_profile_id` — persists active profile UUID across same-tab reloads

**What must never be treated as canonical:**
- The `#chartProfile` dropdown in `map_CURRENT.html` reflects the profiles loaded at page init. If a profile is created after page load, the dropdown is stale until reload.
- Legacy `chart-profiles` endpoint (port 8000) is NOT canonical. It may return mock data.

---

## 5. BIRTH RECORDS

**Canonical source of truth:** Supabase `birth_records` table

**Status:** REAL

**Read paths:**
- `supabase_store_bridge.js`: authenticated Supabase JS, scoped to current account's profiles
- `GET http://127.0.0.1:8004/supabase/chart-records/{profile_id}/engine-birth`: service-role, resolves birth record + place → UTC engine params. This is the critical read path for all chart calculations.
- `GET http://127.0.0.1:8004/birth-records/{profile_id}`: raw birth records list

**Write paths:**
- `first_profile_intake.js` → `POST http://127.0.0.1:8004/birth-records` — service-role; creates birth record row

**Local/session cache:**
- Birth params (year, month, day, hour_utc) are fetched fresh on each Find Regions call. Not cached.

**What must never be treated as canonical:**
- Legacy `/chart-records/{id}/engine-birth` on port 8000 is a fallback for non-UUID IDs. It is NOT canonical for Supabase profiles and should not be used.

---

## 6. PLACES

**Canonical source of truth:** Supabase `places` table

**Status:** REAL (functional, not production-quality for search)

**Read paths:**
- `first_profile_intake.js`: Supabase JS direct, authenticated — `SELECT places WHERE display_name ILIKE 'query%' LIMIT 8`
- `current_location_editor.js`: Supabase JS direct, authenticated — same query pattern
- `GET http://127.0.0.1:8004/places/search?q=<query>`: service-role proxy used by `place_resolution.js` and `applyMapFavoriteButtonState()`
- `GET http://127.0.0.1:8004/place/{id}`: single place by UUID

**Write paths:**
- `scripts/ingest_cities_to_places.py`: bulk ingest of ~68,032 GeoNames cities (service-role, one-time / re-runnable)
- `place_resolution.js` → `POST http://127.0.0.1:8004/places`: creates a new place row when a map selection resolves to an unknown location

**RLS:**
- `for select to authenticated using (true)` — all authenticated users can read all places. No anonymous read. No user writes (service-role only for writes).

**Local/session cache:**
- None. Places are fetched on demand.

**Production-readiness gap:**
- City search uses `ILIKE display_name%` only — no alternate names, no transliteration, no fuzzy matching, no abbreviation normalization. Estimated Recall@1 ~60%. See `CITY_SEARCH_PRODUCTION_REQUIREMENTS.md` for acceptance criteria.
- `alternate_names_json` column exists in schema but is not populated.
- `admin1` field contains numeric codes (e.g., "16") not human-readable region names — `admin1CodesASCII.txt` not loaded during ingest.

**What must never be treated as canonical:**
- City search results from the current implementation. They are functional but not production-quality. Do not launch to users who expect to find cities by nickname, historical name, transliteration, or typo.

---

## 7. CURRENT LOCATION

**Canonical source of truth:** Supabase `current_location_history` table (the row where `is_current = true`)

**Status:** REAL

**Read paths:**
- `supabase_store_bridge.js`: authenticated Supabase JS — reads most recent `is_current=true` row per profile
- Account Drawer: renders current location city name from bridge viewModel

**Write paths:**
- `current_location_editor.js`: Supabase JS direct —
  1. UPDATE `current_location_history` SET `is_current=false` WHERE `profile_id=<id>` AND `account_id=<id>`
  2. INSERT new row with `is_current=true`, `source='manual'`, `selected_at=now()`

**Local/session cache:**
- None. Re-read from Supabase on every page load.

**What must never be treated as canonical:**
- GPS / browser geolocation is NOT implemented. All current location data is manually set.
- `is_current=false` rows are retained as history — do not read them as the current location.

---

## 8. USER SETTINGS

**Canonical source of truth:** Supabase `user_settings` table, `settings_json` JSONB column

**Status:** PARTIAL (settings screen implemented; not all settings affect behavior)

**Read paths:**
- `supabase_store_bridge.js`: authenticated Supabase JS — reads settings row per account

**Write paths:**
- `app_shell.html save-settings` action:
  - SELECT check → if no row: `POST http://127.0.0.1:8004/user-settings`
  - If row exists: `PATCH http://127.0.0.1:8004/user-settings/{id}`

**Fields currently in `settings_json`:**
- `default_chart_record_id` — profile UUID for default chart
- `house_system` — astrological house system (e.g., "Whole Sign", "Placidus")

**Local/session cache:**
- `SupabaseStore.user_settings` — in-memory copy refreshed on page load. Not persisted across reloads.

**What must never be treated as canonical:**
- Settings form display state (prior to Save). The form may differ from the saved value until Save is clicked.
- Settings are account-level (`profile_id = null`). There is no per-profile settings differentiation.

---

## 9. FAVORITES

**Canonical source of truth:** Supabase `favorite_places` table

**Status:** REAL (write path confirmed; full list display in app_shell not fully smoke-tested)

**Read paths:**
- `supabase_store_bridge.js`: authenticated Supabase JS — reads `favorite_places` WHERE `account_id IN (app_account_ids())`
- `map_CURRENT.html applyMapFavoriteButtonState()`: Supabase JS direct, checks for existing favorite for current place+profile

**Write paths:**
- `map_CURRENT.html favoriteMapSelectionFromButton()`: Supabase JS direct INSERT — adds favorite
- Soft-delete: UPDATE `archived_at` — not yet surfaced in UI

**Fields written:**
- `account_id`, `profile_id`, `place_id`, `label` (display_name), `rank` (null — ordering not yet implemented), `archived_at` (null = active)

**Local/session cache:**
- `sessionStorage: rm_recent_favorite_place_id` — written after successful favorite; used externally to highlight the recently favorited place
- `SupabaseStore.favorite_places` — in-memory copy from bridge, refreshed on page load

**What must never be treated as canonical:**
- The favorite button state on the map. It reflects the state at page load + any actions taken since. It does not auto-refresh if another device/tab adds a favorite.

---

## 10. SAVED INVESTIGATIONS

**Canonical source of truth (intended):** Supabase `saved_searches` table

**Status:** DEFERRED — backend CRUD exists; frontend not wired

**Read paths:** `GET http://127.0.0.1:8004/saved-searches/{profile_id}` — exists but not called by any UI
**Write paths:** `POST http://127.0.0.1:8004/saved-searches` — exists but not called by any UI

**What must never be treated as canonical:**
- Nothing. No data is being written to this table from any UI flow.

---

## 11. SAVED COMPARISONS

**Canonical source of truth (intended):** Supabase `comparison_sets` + `comparison_set_places` tables

**Status:** PARTIAL — list rendering works; comparison facts are MOCKED

**Read paths:**
- `supabase_store_bridge.js`: reads `comparison_sets` and `comparison_set_places` from Supabase
- `app_shell.html screenCompare()`: renders comparison list from bridge viewModel

**Write paths:**
- `POST http://127.0.0.1:8004/comparison-sets` — exists; not surfaced in production UI as a user-accessible action
- `POST http://127.0.0.1:8004/comparison-sets/{id}/places` — exists; not surfaced

**Comparison facts (planet positions, house placements for comparison cities):**
- **MOCKED / PLACEHOLDER.** The UI renders static text ("Sun in 10th", "ASC in Gemini") as example content. Real comparison facts require calling the chart engine with each comparison city's coordinates. This is NOT wired.

**What must never be treated as canonical:**
- Any comparison fact displayed in the current UI. All visible fact data is placeholder text.
- Do not mark comparisons "done" until real relocated chart data drives the comparison display.

---

## 12. NOTES

**Canonical source of truth:** `localStorage` key `rm_note_<chartRecordId>` (browser-local only)

**Status:** PARTIAL — functional but not canonical storage; Supabase `notes` table exists but is NOT wired

**Read paths:**
- `app_shell.html screenChartRecord()`: `localStorage.getItem('rm_note_<chartRecordId>')`

**Write paths:**
- `app_shell.html save-chart-note` action: `localStorage.setItem('rm_note_<chartRecordId>', value)`

**Supabase `notes` table:**
- Schema exists. Backend CRUD endpoints exist (`GET /notes/{profile_id}`, `POST /notes`).
- No UI path writes to or reads from this table.

**What must never be treated as canonical:**
- localStorage notes are temporary and non-canonical. They will be lost on device switch, browser clear, or private mode.
- Do not advertise note-taking as a persistent feature until the Supabase `notes` table is wired.

---

## 13. HELP CONTENT

**Canonical source of truth:** Static HTML in `app_shell.html screenHelp()` function

**Status:** MOCKED / STATIC — content is hand-authored placeholder text, not fetched from any CMS or database

**Read paths:** None (inline in `screenHelp()`)
**Write paths:** None (requires code change to update)

**What must never be treated as canonical:**
- The current help content does not represent final copy. It is a structural placeholder.

---

## 14. ONBOARDING STATE

**Canonical source of truth:** `localStorage` key `rm_guided_onboarding_dismissed`

**Status:** REAL (functional for per-browser dismissal)

**Read paths:** `app_shell.html maybeShowGuidedOnboarding()`: checks `localStorage.getItem('rm_guided_onboarding_dismissed') === '1'`
**Write paths:** Onboarding "Skip" or "Start here" handlers: `localStorage.setItem('rm_guided_onboarding_dismissed', '1')`

**What must never be treated as canonical:**
- This state is browser-local only. If user clears storage or uses a different browser, onboarding reappears. This is acceptable for a dismissal flag.
- No Supabase table tracks onboarding completion. There is no server-side record of whether a user has completed onboarding.

---

## 15. CITY SEARCH DATA

**Canonical source of truth:** Supabase `places` table (GeoNames dataset)

**Status:** PARTIAL / NOT PRODUCTION-READY

**Dataset:** ~68,032 cities (population ≥ 5,000) loaded from GeoNames `cities5000_enriched.json`

**What is present:**
- `display_name`, `canonical_name`, `latitude`, `longitude`, `country_code`, `country_name`, `timezone_id`, `population`, `importance_rank`, `geonames_id`, `provider='geonames'`

**What is absent (required for production):**
- `alternate_names_json` — not populated; no alternate names, historical names, or transliterations searchable
- Full-text search index — not created; queries use `ILIKE display_name%` only
- `admin1` full name — currently stores numeric admin1 code, not human-readable region name

**Acceptance criteria:** See `CITY_SEARCH_PRODUCTION_REQUIREMENTS.md` §9 and §11. City search must not be treated as production-ready until Recall@1 ≥ 85% on the required test set.

---

## 16. MAP OVERLAYS (rendered output)

**Canonical source of truth:** DERIVED — not stored. Computed fresh on every "Find Regions" click.

**Status:** REAL (for house/planet polygon overlays); BLOCKED for angular/aura overlays (port 8000)

**Derivation path:**
```
birth_records (Supabase) + places (Supabase)
  → /supabase/chart-records/{id}/engine-birth (8004)
  → birth params (UTC float)
  → /search-regions (8004)
  → Python math engine
  → GeoJSON FeatureCollection
  → Leaflet polygon layers
```

**Angular/aura overlays:** BLOCKED — `/aura-raster`, `/aura-raster-adaptive`, `/aura-field` on port 8000 not migrated.

**What must never be treated as canonical:**
- Map overlay polygons are derived output. They are never persisted to the database. Reloading the page discards them. Re-running "Find Regions" may produce slightly different output if birth data or the math engine changes.

---

## 17. RELOCATED CHART CALCULATIONS

**Canonical source of truth:** DERIVED — computed by Python chart engine on demand. Not stored.

**Status:** BLOCKED — popup relocated chart calls `GET http://127.0.0.1:8000/relocated-chart` (port 8000, not migrated). If port 8000 is down, popup relocated charts are unavailable.

**What must never be treated as canonical:**
- Popup chart data is ephemeral. It is computed at click time and displayed in a popup. It is not saved anywhere.

---

## 18. COMPARISON FACTS

**Canonical source of truth (intended):** Computed via chart engine for each comparison city. Not yet implemented.

**Status:** MOCKED

**Current state:** The comparison screen displays static placeholder text for fact values. No computation occurs. No real astrological data is shown.

**What must never be treated as canonical:**
- Any fact value in the current comparison screen UI. All values are fictional placeholders.
- Do not run Diffs against comparison facts — Diffs are BLOCKED until real comparison facts exist.

---

## 19. DIFFS

**Status:** BLOCKED — depends on real comparison facts, which are MOCKED.

Diffs (showing how a person's chart variables change between two locations) require:
1. Real relocated chart computation for each comparison city
2. A diff engine that compares the two result sets

Neither exists in production-wired form. Do not implement or claim Diffs until comparison facts are REAL.

---

## 20. EXPORTS

**Status:** DEFERRED — `screenExport()` is a placeholder. No export functionality is implemented.

**What must never be treated as canonical:**
- The Export screen. It renders but contains no functional controls.

---

## 21. LAYER 2 INTERPRETATION

**Canonical source of truth:** Genie variable builder (`genie_variable_builder.js`) + `genie_map_engine_adapter.js`

**Status:** PARTIAL — Genie variable builder is wired in `app_shell.html` and `map_CURRENT.html`. The adapter exposes `window.RelocationGenieMapEngineAdapter`. However, Genie is NOT integrated into the production map render flow. The production map (`map_CURRENT.html`) renders house/planet polygons via the Python engine, not through Genie. Genie render payloads are handled via sessionStorage side-channel (H-3) which breaks on new-tab navigation.

**What must never be treated as canonical:**
- Genie output in the current map. Genie is present as infrastructure but is not the driver of the production polygon rendering. Treat Genie integration as PARTIAL until it is the primary render path.

---

## 22. AI OUTPUTS

**Status:** OUT OF SCOPE / QUARANTINED

AI-generated interpretation (Layer 2) is defined as a separate system that produces human-readable summaries of astrological chart variables. It is:
- Not wired to any production data
- Not stored in any Supabase table
- Not a source of truth for chart calculations
- Quarantined from the calculation engine

AI outputs must never influence, override, or be treated as equivalent to chart engine computations. Layer 2 is additive interpretation only.
