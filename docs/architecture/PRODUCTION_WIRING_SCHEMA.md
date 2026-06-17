# PRODUCTION WIRING SCHEMA

**Status:** Production reference  
**Last updated:** 2026-06-14  
**Purpose:** Factual wiring map of the current system. Not a roadmap. Not philosophy.  
**Scope:** All files as deployed. Use this document to eliminate archaeology sessions.

---

## 1. SYSTEM OVERVIEW

### Topology

```
Browser
  └── auth.html              (login / signup gate)
  └── app_shell.html         (account / profile / settings shell — placeholder map UI)
  └── map_CURRENT.html       (production map instrument — Leaflet + overlays + Genie)

Backend (FastAPI, Python)
  └── main_centerline_FIXER.py   port 8004
      ├── static file serving (all .html, .js assets)
      ├── /search-regions          (computation engine — calls internal Python math)
      ├── /supabase/* endpoints    (server-side Supabase reads with service-role key)
      └── /repositories/*          (CRUD over Supabase via service-role key)

Supabase (hosted Postgres + Auth + RLS)
  └── staging project: rnwlrdtqhfjhpllryxiz.supabase.co
  └── anon key used in browser (supabase_client.js)
  └── service-role key used in backend (services/supabase_client.py)

Legacy backend (port 8000) — NOT RUNNING in Web2
  └── /search-regions (migrated to 8004)
  └── /aura-*, /screen-pixel-truth, /aspect-orb-at-point (still called from map_CURRENT.html — hardcoded 8000)
  └── /chart-profiles (still attempted by map_CURRENT.html — optional/guarded)
  └── /library/*, /chart-records/*, /relocated-chart, /profile-library/* (legacy)
```

### Production vs Sandbox Assets

| Asset | Status |
|---|---|
| `map_CURRENT.html` | Production |
| `app_shell.html` | Production (stub map, real profile/account/settings shell) |
| `auth.html` | Production |
| `map_SANDBOX_*.html` | Sandboxes — not user-facing |
| `prototype_*.html` | Prototypes — not user-facing |
| `genie_SANDBOX_variable_builder.html` | Sandbox |

---

## 2. PAGE REGISTRY

### auth.html

**Purpose:** Email/password signup and login. Gate before all application pages.

**Entry points:**
- Direct URL: `/auth.html`
- Auth guard redirect: any unauthenticated hit to a guarded page
- Email confirmation deep-link (Supabase `redirectTo` callback)

**Dependencies (scripts loaded):**
- `supabase_client.js` (browser Supabase client)

**APIs called:**
- `supabase.auth.signUp()` — creates auth.users row, triggers `handle_new_user()`
- `supabase.auth.signInWithPassword()`
- `supabase.auth.resetPasswordForEmail()`
- `supabase.auth.onAuthStateChange()` — detects confirmed session, redirects

**Storage touched:**
- Supabase Auth session (cookie/localStorage managed by Supabase JS SDK)

**On success:** `window.location.href = '/map_CURRENT.html'`

**Related tables:** `auth.users` (Supabase Auth — not directly accessible), `accounts`, `account_memberships` (created via `handle_new_user()` trigger)

---

### app_shell.html

**Purpose:** Account/profile shell. Displays profile selector, settings, account drawer, help, guided onboarding, notes, favorites list, comparison list. Contains a placeholder map screen with a link to `map_CURRENT.html`.

**Entry points:**
- Direct URL: `/app_shell.html`
- Navigated from within itself (hash routing)

**Dependencies (scripts loaded in order):**
1. `supabase_client.js` — exposes `window.SupabaseClient`, `window.SupabaseReady`
2. `auth_guard.js` — redirects unauthenticated users to `/auth.html`, exposes `window.logout()`
3. `user_profile.js` — exposes `window.CurrentUser`, `window.CurrentUserReady`
4. `supabase_store_bridge.js` — exposes `window.SupabaseStore`, `window.SupabaseStoreReady`
5. `first_profile_intake.js` — exposes `window.__showFirstProfileIntake()`
6. `current_location_editor.js` — exposes `window.__showCurrentLocationEditor()`
7. `account_drawer.js` — exposes `window.__showAccountDrawer()`
8. `genie_variable_builder.js` — exposes `window.__rmAvailableObjectsRegistry`

**APIs called:**
- Supabase JS (via `SupabaseReady`) — all reads done through `supabase_store_bridge.js`
- `GET /local-product-store.json` — fallback if `SupabaseStoreReady` is absent

**Storage touched:**
- `localStorage: rm_selected_chart_<accountId>` — persists active chart record selection
- `localStorage: rm_guided_onboarding_dismissed` — onboarding dismissal flag
- `localStorage: rm_note_<chartRecordId>` — per-chart note text

**Window globals exposed:**
```
window.__rmAppShell
window.__rmAppShellGenie
window.__showAccountDrawer
window.__showCurrentLocationEditor
window.__showFirstProfileIntake
```

**Map handoff:** `buildMapHandoffUrl()` produces URLs of the form:
```
/map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<iso>&chartRecordId=<uuid>[&placeId=<uuid>][&explorationId=<uuid>][&comparisonSetId=<uuid>][&returnTo=<encoded>][&genieRenderRef=<ref>]
```

**Store schema version:** `STORE_SCHEMA_VERSION = 3`

**Related tables (via bridge):** `profiles`, `birth_records`, `places`, `user_settings`, `favorite_places`, `comparison_sets`, `comparison_set_places`, `current_location_history`

---

### map_CURRENT.html

**Purpose:** Primary map instrument. Leaflet-based map with planet/house condition selectors, overlay rendering, popup relocated charts, Genie variable builder integration, city search, favorites.

**Entry points:**
- Redirect from `auth.html` after login/signup: bare `/map_CURRENT.html`
- Redirect from `first_profile_intake.js` after intake: `/map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<iso>&chartRecordId=<uuid>`
- Link from `app_shell.html` screenMap(): `buildMapHandoffUrl()` result (same shape)

**Dependencies (scripts loaded):**
1. `supabase_client.js` — browser Supabase client
2. `auth_guard.js` — session guard, logout
3. `user_profile.js` — `window.CurrentUser`, `window.CurrentUserReady`
4. `supabase_store_bridge.js` — `window.SupabaseStoreReady`
5. `first_profile_intake.js` — self-triggers on `SupabaseStoreReady` rejection
6. `place_resolution.js` — `window.RMPlaceResolution`
7. `genie_variable_builder.js` — `window.__rmAvailableObjectsRegistry`
8. `genie_map_engine_adapter.js` — `window.RelocationGenieMapEngineAdapter`
9. `substrate_adapter.js` — `window.RelocationSubstrateAdapter`
10. `cities.js` — `citiesData` for city typeahead (GeoNames, ~68k cities)

**URL params read at load:**
| Param | Purpose |
|---|---|
| `handoff` | Must equal `"app_shell"` to activate `lastAppShellHandoff` |
| `chartRecordId` | Profile UUID passed to birth resolution |
| `placeId` | Pre-selected map center place |
| `explorationId` | Saved exploration to resume |
| `comparisonSetId` | Active comparison set |
| `returnTo` | Encoded back-navigation context |
| `handoffCreatedAt` | ISO timestamp of handoff creation |
| `genieRenderRef` | Key into sessionStorage for Genie payload |
| `skipOnboarding` | Skips map onboarding if `"1"` |
| `generation_mode` | Override polygon generation mode |
| `canonicalBlock` | Debug canonical screen-space block size |

**APIs called — port 8004 (active):**
| Endpoint | Caller function | Purpose |
|---|---|---|
| `GET http://127.0.0.1:8004/profiles` | `loadChartProfiles()` | Populate profile selector dropdown |
| `GET http://127.0.0.1:8004/places/search?q=` | `applyMapFavoriteButtonState()` | Look up place before favorite check |
| `POST http://127.0.0.1:8004/places` | `resolvePlaceFromMapSelection()` via `RMPlaceResolution` | Create new place record |
| `GET http://127.0.0.1:8004/places/search` | `resolvePlaceFromMapSelection()` via `RMPlaceResolution` | Resolve existing place |
| `POST http://127.0.0.1:8004/search-regions` | `postSearchRegions()` | Find regions for planet/house conditions |
| `GET /supabase/chart-records/{id}/engine-birth` | `fetchEngineBirthForChartRecord()` | Resolve Supabase profile birth → UTC params |

**APIs called — port 8000 (legacy, may be absent):**
| Endpoint | Caller function | Status |
|---|---|---|
| `GET ${LIBRARY_API_BASE}/chart-profiles` | `loadChartProfiles()` | Optional, guarded try/catch |
| `GET ${LIBRARY_API_BASE}/library/state` | `fetchLibraryStateSafe()` | Optional |
| `POST ${LIBRARY_API_BASE}/library/views` | `saveCurrentViewToLibrary()` | Optional |
| `GET ${LIBRARY_API_BASE}/library/views` | `applyLibrarySavedViewReplay()` | Optional |
| `GET http://127.0.0.1:8000/aura-field` | `renderAuraField()` | Required for aura overlays — **NOT migrated** |
| `GET http://127.0.0.1:8000/aura-raster` | `renderRasterAura()` | Required for raster aura — **NOT migrated** |
| `GET http://127.0.0.1:8000/aura-raster-adaptive` | `renderAdaptiveAura()` | Required for adaptive aura — **NOT migrated** |
| `GET http://127.0.0.1:8000/screen-pixel-truth` | `runScreenPixelTruth()` | Debug mode only — **NOT migrated** |
| `GET http://127.0.0.1:8000/aspect-orb-at-point` | `getAspectOrbAtPoint()` | Popup aspect calculation — **NOT migrated** |
| `GET /chart-records/{id}/engine-birth` | `fetchEngineBirthForChartRecord()` | Legacy fallback for non-UUID IDs |
| `GET /relocated-chart` | `fetchRelocatedChart()` | Popup relocated chart |

**Supabase JS direct calls (via `SupabaseClient`):**
| Table | Operation | Caller |
|---|---|---|
| `favorite_places` | SELECT id (duplicate check) | `favoriteMapSelectionFromButton()` |
| `favorite_places` | INSERT | `favoriteMapSelectionFromButton()` |
| `favorite_places` | SELECT id (button state) | `applyMapFavoriteButtonState()` |

**sessionStorage keys:**
| Key | Written by | Read by | Purpose |
|---|---|---|---|
| `rm_active_profile_id` | `applyActiveProfileSelection()` | `readActiveProfileIdFromUrlOrSession()` | Persist active Supabase profile |
| `rm_library_active` | legacy library | `readActiveLibraryChartIdFromUrlOrSession()` | Persist active legacy chart |
| `rm_map_onboarding_dismissed` | onboarding handler | onboarding check | Skip map onboarding |
| `rm_recent_favorite_place_id` | `favoriteMapSelectionFromButton()` | profile page (external) | Highlight recently favorited place |
| `rm_genie_render:<ref>` | `app_shell.html` `storeGenieRenderPayload()` | `loadGenieRenderPayloadFromHandoff()` | Genie render payload side-channel |

**Window globals exposed:**
```
window.__rmAppShellHandoff         — read-only copy of lastAppShellHandoff
window.__rmChartProfilesReady      — Promise resolving after profile dropdown loads
window.__rmLoadChartProfiles       — function to reload profile dropdown
window.__rmExecuteGenieRender      — execute Genie render payload
window.__rmGenieMapAdapter         — alias for RelocationGenieMapEngineAdapter
window.__rmGenieRenderHandoff      — last Genie render execution state
window.__rmGenieRenderExecutionSummary
window.__rmLibraryHandoff          — legacy library handoff state
window.__rmMap                     — the Leaflet map instance
window.__rmResolvePlaceFromMapSelection
window.__rmApplyMapFavoriteButtonState
window.__rmGetActiveFavoriteProfileId
window.__rmSmokeState              — smoke test state object
window.__rmProductionShadowState
window.__rmRasterAuraState
window.__rmSaveCurrentViewToLibrary
window.__rmApplyLibrarySavedViewReplay
```

---

## 3. USER FLOW WIRING

```
auth.html
  ├── signUp → handle_new_user() trigger → accounts + account_memberships created
  │   └── redirect → /map_CURRENT.html (bare)
  │       └── SupabaseStoreReady rejects (no profiles) → first_profile_intake.js fires
  │           └── intake: profiles INSERT + birth_records INSERT
  │               └── success: redirect → /map_CURRENT.html?handoff=app_shell&chartRecordId=<uuid>
  │                   └── loadChartProfiles() → GET /profiles → populate selector
  │                       └── applyActiveProfileSelection() → select profile from URL
  │                           └── Find Regions → GET /engine-birth → POST /search-regions → overlay renders
  │
  └── signIn → existing session → redirect → /map_CURRENT.html (or app_shell.html)

Current Location (from app_shell.html Account Drawer):
  → Set Current Location → current_location_editor.js
    → places search (Supabase direct) → SELECT places
    → save: UPDATE current_location_history SET is_current=false
           INSERT current_location_history (is_current=true, source="manual")
    → reload page

Map Favorites (from map_CURRENT.html popup):
  → click Favorite button
  → resolvePlaceFromMapSelection() → RMPlaceResolution → GET/POST /places (8004)
  → Supabase JS: SELECT favorite_places (duplicate check)
  → Supabase JS: INSERT favorite_places {account_id, profile_id, place_id, label, rank:null}
  → sessionStorage.setItem("rm_recent_favorite_place_id", place.id)

Settings (from app_shell.html):
  → screenSettings() → read SupabaseStore.user_settings
  → save-settings action → SELECT user_settings (check exists) → UPDATE or INSERT
  → fields: default_chart_record_id, house_system stored in settings_json

Notes (from app_shell.html screenChartRecord()):
  → textarea autofills from localStorage: rm_note_<chartRecordId>
  → save-chart-note action → localStorage.setItem(rm_note_<chartRecordId>, value)
  (Notes are localStorage-only; not written to Supabase)

Account Drawer:
  → opens via window.__showAccountDrawer()
  → reads window.CurrentUser for accountName, accountType, role
  → reads window.__rmAppShell.viewModel().chartRecords for profile list
```

---

## 4. API WIRING

### Port 8004 Endpoints (active Web2 server)

| Endpoint | Purpose | Primary Caller | Data Source | Output Consumer |
|---|---|---|---|---|
| `GET /auth.html` | Serve auth page | Browser direct | Filesystem | Browser |
| `GET /app_shell.html` | Serve shell page | Browser direct | Filesystem | Browser |
| `GET /map_CURRENT.html` | Serve map page | Browser direct | Filesystem | Browser |
| `GET /health` | Liveness check | Monitoring / curl | Inline | Monitoring |
| `GET /config/supabase` | Supabase public config | `supabase_client.js` | `.env` | Browser Supabase client init |
| `GET /supabase_client.js` | Browser Supabase init | `<script>` tags | Filesystem | All pages |
| `GET /auth_guard.js` | Session guard | `<script>` tags | Filesystem | All pages |
| `GET /user_profile.js` | CurrentUser init | `<script>` tags | Filesystem | All pages |
| `GET /supabase_store_bridge.js` | Store bridge | `<script>` tags | Filesystem | app_shell, map_CURRENT |
| `GET /first_profile_intake.js` | Intake overlay | `<script>` tags | Filesystem | app_shell, map_CURRENT |
| `GET /current_location_editor.js` | Location editor overlay | `<script>` tags | Filesystem | app_shell |
| `GET /account_drawer.js` | Account drawer | `<script>` tags | Filesystem | app_shell |
| `GET /place_resolution.js` | Shared place resolver | `<script>` tags | Filesystem | map_CURRENT |
| `GET /genie_variable_builder.js` | Genie UI | `<script>` tags | Filesystem | app_shell, map_CURRENT |
| `GET /genie_map_engine_adapter.js` | Genie→engine adapter | `<script>` tags | Filesystem | map_CURRENT |
| `GET /cities.js` | GeoNames city dataset | `<script>` tags | Filesystem | map_CURRENT typeahead |
| `GET /profiles` | List all profiles (service-role) | `loadChartProfiles()` in map_CURRENT | Supabase `profiles` | `#chartProfile` dropdown |
| `GET /profiles/{id}` | Get single profile | Various | Supabase `profiles` | - |
| `POST /profiles` | Create profile | `first_profile_intake.js` | - | Supabase `profiles` |
| `GET /places` | List places | Various | Supabase `places` | - |
| `GET /places/search?q=` | Search places by display_name | `place_resolution.js`, `applyMapFavoriteButtonState()` | Supabase `places` | Place selection UI |
| `POST /places` | Create place | `place_resolution.js` | - | Supabase `places` |
| `GET /place/{id}` | Get single place | Various | Supabase `places` | - |
| `POST /search-regions` | Compute planet-in-house regions | `postSearchRegions()` | Python math engine | GeoJSON polygon overlay |
| `GET /supabase/chart-records/{profile_id}/engine-birth` | Resolve profile birth → UTC | `fetchEngineBirthForChartRecord()` | Supabase `birth_records` + `places` | Chart engine birth params |
| `GET /birth-records/{profile_id}` | List birth records | Various | Supabase `birth_records` | - |
| `POST /birth-records` | Create birth record | `first_profile_intake.js` | - | Supabase `birth_records` |
| `GET /favorite-places/{profile_id}` | List favorites | Legacy map button state check | Supabase `favorite_places` | **LEGACY — no longer called by map_CURRENT (migrated to Supabase JS direct)** |
| `POST /favorite-places` | Create favorite | **LEGACY — no longer called by map_CURRENT (migrated to Supabase JS direct)** | - | - |
| `GET /user-settings/{account_user_id}` | Get settings | `supabase_store_bridge.js` fallback | Supabase `user_settings` | Settings screen |
| `POST /user-settings` | Create settings | `app_shell.html` save-settings | - | Supabase `user_settings` |
| `PATCH /user-settings/{id}` | Update settings | `app_shell.html` save-settings | - | Supabase `user_settings` |

### Relative URL Endpoints (served by FastAPI, no hardcoded port)

| Endpoint | Purpose | Caller |
|---|---|---|
| `GET /chart-profiles` | Legacy mock chart profiles | `loadChartProfiles()` — guarded optional |
| `GET /chart-records/{id}/engine-birth` | Legacy birth resolution | `fetchEngineBirthForChartRecord()` — fallback |
| `GET /relocated-chart` | Popup relocated chart | `fetchRelocatedChart()` |
| `GET /local-product-store.json` | Fallback store | `app_shell.html` loadViewModelFromStore() |

---

## 5. DATABASE WIRING

### Supabase Tables

#### `accounts`
- **Owner:** created by `handle_new_user()` trigger on `auth.users` INSERT
- **Read paths:** `user_profile.js` via `app_account_ids()` RPC; `account_drawer.js` via `window.CurrentUser`
- **Write paths:** `handle_new_user()` only (browser writes are prohibited by RLS)
- **RLS:** CRUD policies using `app_account_ids()` + `app_has_account_role()`

#### `account_memberships`
- **Owner:** created by `handle_new_user()` trigger
- **Read paths:** `user_profile.js` via `app_account_ids()` RPC
- **Write paths:** `handle_new_user()` only
- **RLS:** CRUD policies

#### `profiles`
- **Read paths:** `supabase_store_bridge.js` (anon key, authenticated user, RLS filter); `GET /profiles` (service-role, all profiles)
- **Write paths:** `first_profile_intake.js` → `POST /profiles` (8004 backend, service-role); `archive_profile()` via `POST /profiles/{id}/archive`
- **RLS:** `for select to authenticated using (account_id in (select app_account_ids()))` — authenticated user sees only own account's profiles

#### `birth_records`
- **Read paths:** `supabase_store_bridge.js`; `GET /supabase/chart-records/{profile_id}/engine-birth` (service-role)
- **Write paths:** `first_profile_intake.js` → `POST /birth-records` (8004)
- **RLS:** CRUD policies scoped to `account_id`

#### `places`
- **Read paths:** `first_profile_intake.js` direct Supabase JS (authenticated); `current_location_editor.js` direct Supabase JS; `supabase_store_bridge.js`; `GET /places/search` (8004 service-role)
- **Write paths:** `place_resolution.js` → `POST /places` (8004 service-role)
- **RLS:** `for select to authenticated using (true)` — all authenticated users can read all places. No anon read. No user writes (service-role only).
- **Dataset:** 68,032 GeoNames cities loaded via `scripts/ingest_cities_to_places.py`

#### `favorite_places`
- **Read paths:** `supabase_store_bridge.js` (authenticated, scoped by `account_id`); `map_CURRENT.html` direct Supabase JS via `window.SupabaseClient`
- **Write paths:** `map_CURRENT.html` direct Supabase JS INSERT (authenticated) via `favoriteMapSelectionFromButton()`; soft-delete via `archived_at` update
- **RLS:** CRUD policies scoped to `account_id`
- **Fields used:** `id`, `account_id`, `profile_id`, `place_id`, `label`, `rank`, `archived_at`

#### `current_location_history`
- **Read paths:** `supabase_store_bridge.js` — reads `is_current=true` row per profile
- **Write paths:** `current_location_editor.js` — UPDATE `is_current=false` on existing rows, then INSERT new row with `is_current=true, source="manual"`
- **RLS:** CRUD policies scoped to `account_id`

#### `user_settings`
- **Read paths:** `supabase_store_bridge.js`
- **Write paths:** `app_shell.html` save-settings action → `POST /user-settings` or `PATCH /user-settings/{id}` (8004)
- **RLS:** CRUD policies scoped to `account_id`
- **Note:** Settings are account-level (`profile_id = null`). Written as `settings_json` JSONB column.

#### `comparison_sets`, `comparison_set_places`
- **Read paths:** `supabase_store_bridge.js`
- **Write paths:** Backend CRUD endpoints on 8004 (`POST /comparison-sets`, etc.)
- **RLS:** CRUD policies scoped to `account_id`

#### `notes`
- **Read paths:** Backend `GET /notes/{profile_id}`
- **Write paths:** Backend `POST /notes`
- **RLS:** CRUD policies scoped to `account_id`
- **Note:** App-shell Notes v1 uses `localStorage` only, not this table.

#### `saved_searches`
- **Read/write paths:** Backend CRUD endpoints on 8004
- **RLS:** CRUD policies scoped to `account_id`

#### `share_links`
- **Read/write paths:** Backend CRUD endpoints on 8004
- **RLS:** CRUD policies scoped to `account_id`

#### `visited_places`
- **Read/write paths:** Backend CRUD endpoints on 8004
- **RLS:** CRUD policies scoped to `account_id`

### Supabase RLS Helper Functions

| Function | Purpose |
|---|---|
| `app_account_ids()` | Returns array of `account_id` values for the current authenticated user's memberships |
| `app_has_account_role(account_id, roles[])` | Returns true if current user has one of the named roles on the given account |
| `handle_new_user()` | `SECURITY DEFINER` trigger on `auth.users` INSERT — creates `accounts` + `account_memberships` row |

---

## 6. HANDOFF REGISTRY

### app_shell → map_CURRENT handoff

**Creator:** `app_shell.html` `buildMapHandoffUrl()` (called from `screenMap()` link, `openMap()` action buttons, `prepareGenieRenderHandoff()`)

**Consumer:** `map_CURRENT.html` `readAppShellHandoff()` — only active when `?handoff=app_shell` is present

**Contract fields:**

| URL Param | Type | Required | Purpose |
|---|---|---|---|
| `handoff` | string | Yes — must equal `"app_shell"` | Activates `lastAppShellHandoff` object |
| `skipOnboarding` | `"1"` | Yes | Skips map onboarding overlay |
| `handoffCreatedAt` | ISO 8601 | Yes | Timestamp of handoff creation |
| `chartRecordId` | UUID | Conditional | Profile UUID; drives birth data resolution |
| `placeId` | UUID | Optional | Pre-selected place to center map |
| `explorationId` | UUID | Optional | Resume saved exploration |
| `comparisonSetId` | UUID | Optional | Active comparison set |
| `returnTo` | encoded string | Optional | Back-navigation context (`route|chartRecordId|placeId|explorationId|comparisonSetId`) |
| `genieRenderRef` | string | Optional | Key to Genie payload in sessionStorage |

**Without `handoff=app_shell`:**  `lastAppShellHandoff` is null. Map still loads but profile must be selected manually from dropdown. Birth resolution falls back to URL `chartRecordId` bare param (Path C) or dropdown selection.

### first_profile_intake → map_CURRENT handoff

**Creator:** `first_profile_intake.js` success handler

**Form:**
```
/map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<iso>&chartRecordId=<profileId>
```

**Note:** `chartRecordId` here is the `profiles.id` UUID (the newly created profile). This matches what `app_shell.html` passes via the same param.

### Genie render handoff (side-channel)

**Creator:** `app_shell.html` `prepareGenieRenderHandoff(ctx, payload)` — stores payload in `sessionStorage[rm_genie_render:<ref>]`, passes `ref` as `genieRenderRef` URL param

**Consumer:** `map_CURRENT.html` `loadGenieRenderPayloadFromHandoff(ref)` — reads from sessionStorage

**Constraint:** Same-tab navigation only. Does not survive `target="_blank"` (sessionStorage is tab-scoped).

---

## 7. FEATURE WIRING MATRIX

| Feature | Frontend | Backend | Tables | Notes |
|---|---|---|---|---|
| Signup | `auth.html` `supabase.auth.signUp()` | Supabase trigger `handle_new_user()` | `auth.users`, `accounts`, `account_memberships` | Browser-only |
| Login | `auth.html` `supabase.auth.signInWithPassword()` | Supabase Auth | `auth.users` | Browser-only |
| First profile intake | `map_CURRENT.html` → `first_profile_intake.js` | `POST /profiles`, `POST /birth-records` (8004) | `profiles`, `birth_records`, `places` | Triggers on `SupabaseStoreReady` rejection |
| Profile selection | `map_CURRENT.html` `#chartProfile` dropdown | `GET /profiles` (8004) | `profiles` | Uses Supabase UUID; legacy chart-profiles optional |
| Birth data → engine | `map_CURRENT.html` `fetchEngineBirthForChartRecord()` | `GET /supabase/chart-records/{id}/engine-birth` (8004) | `birth_records`, `places` | Converts birth date+time+tz to UTC float |
| Find Regions | `map_CURRENT.html` `findRegions()` | `POST /search-regions` (8004) | None (compute only) | Requires resolved birth params |
| Popup relocated chart | `map_CURRENT.html` `fetchRelocatedChart()` | `GET /relocated-chart` (8000 legacy) | None | **Port 8000 — not migrated** |
| Aura overlays | `map_CURRENT.html` aura functions | `POST /aura-raster`, `/aura-raster-adaptive`, `/aura-field` (8000 legacy) | None | **Port 8000 — not migrated** |
| Place resolution | `map_CURRENT.html` `resolvePlaceFromMapSelection()` via `place_resolution.js` | `GET /places/search`, `POST /places` (8004) | `places` | PL-2: confirmed 8004 |
| Map favorites — write | `map_CURRENT.html` `favoriteMapSelectionFromButton()` | Supabase JS direct | `favorite_places` | FAV-4: direct Supabase, account_id required |
| Map favorites — read state | `map_CURRENT.html` `applyMapFavoriteButtonState()` | `GET /places/search` (8004) + Supabase JS | `places`, `favorite_places` | Checks if place already favorited |
| Current location | `app_shell.html` → `current_location_editor.js` | Supabase JS direct | `current_location_history`, `places` | Manual set only; no GPS |
| Settings | `app_shell.html` screenSettings() | `POST /user-settings`, `PATCH /user-settings/{id}` (8004) | `user_settings` | Account-level settings_json |
| Account drawer | `app_shell.html` → `account_drawer.js` | None (reads window.CurrentUser + viewModel) | None (read-only from already-loaded data) | |
| Help/Learn | `app_shell.html` screenHelp() | None | None | Static content |
| Guided onboarding | `app_shell.html` modal | None | None | localStorage dismissal |
| Notes | `app_shell.html` screenChartRecord() | None | None | **localStorage only — Supabase `notes` table is not wired** |
| Comparison | `app_shell.html` screenCompare() | `GET/POST /comparison-sets`, `/comparison-set/{id}/places` (8004) | `comparison_sets`, `comparison_set_places` | Compare facts are placeholder/static |
| Saved searches | Not wired in UI | Backend CRUD exists (8004) | `saved_searches` | Backend ready; frontend not wired |
| Share links | Not wired in UI | Backend CRUD exists (8004) | `share_links` | Backend ready; frontend not wired |
| Export | `app_shell.html` screenExport() placeholder | None | None | Not implemented |

---

## 8. LEGACY DEPENDENCIES

`LIBRARY_API_BASE = "http://127.0.0.1:8000"` is defined in `map_CURRENT.html`.

| Endpoint | Caller | Status | Classification |
|---|---|---|---|
| `GET ${LIBRARY_API_BASE}/chart-profiles` | `loadChartProfiles()` | Guarded try/catch; falls back to `profiles=[]` when absent | Optional — safe to leave; no migration needed |
| `GET ${LIBRARY_API_BASE}/library/state` | `fetchLibraryStateSafe()` | try/catch; optional | Optional — library feature is not Web2 |
| `POST ${LIBRARY_API_BASE}/library/views` | `saveCurrentViewToLibrary()` | Called only if library available | Optional |
| `GET ${LIBRARY_API_BASE}/library/views` | `applyLibrarySavedViewReplay()` | try/catch | Optional |
| `GET http://127.0.0.1:8000/aura-raster` | `renderRasterAura()` | Called for aura overlays — no guard | **Required for aura — must migrate** |
| `GET http://127.0.0.1:8000/aura-raster-adaptive` | `renderAdaptiveAuraProgressive()` | Called for adaptive aura | **Required for aura — must migrate** |
| `POST http://127.0.0.1:8000/aura-field` | `renderAuraField()` | Called for aura overlays | **Required for aura — must migrate** |
| `GET http://127.0.0.1:8000/screen-pixel-truth` | `runScreenPixelTruth()` | Debug mode only (`?screenPixelTruth=1`) | Candidate for migration (debug) |
| `GET http://127.0.0.1:8000/aspect-orb-at-point` | `getAspectOrbAtPoint()` | Popup aspect display | **Required for popup aspect orb — must migrate** |
| `GET /chart-records/{id}/engine-birth` | `fetchEngineBirthForChartRecord()` | Fallback for non-UUID IDs | Optional — legacy chart IDs only |
| `GET /relocated-chart` | `fetchRelocatedChart()` | Popup relocated chart calculation | **Required for popup charts — must migrate** |

---

## 9. KNOWN WIRING RISKS

**R1: Port 8000 aura/popup endpoints not migrated**  
`/aura-raster`, `/aura-raster-adaptive`, `/aura-field`, `/aspect-orb-at-point`, `/relocated-chart` all hardcode `http://127.0.0.1:8000`. If port 8000 is down, aura overlays silently fail and popup relocated charts throw. No user-visible error is shown for aura failures.

**R2: `GET /profiles` returns all profiles (service-role, no user scoping)**  
`repositories/profiles_repository.py` `list_profiles()` uses service-role key with no account filter. If multiple users exist on the same server instance, all users' profiles appear in the dropdown for all users. This is safe in single-user development but is a multi-tenant data leak risk in production.

**R3: `setRenderStatus()` is hidden unless `debugGeometry=true`**  
All status messages from `findRegions()` (including "Birth data required", "No profile selected", "Rendering…") are written to `#renderStatus` but the element is hidden by `status.style.display = debugGeometry ? "block" : "none"`. Errors silently produce no visible feedback to the user.

**R4: Notes are localStorage-only**  
`app_shell.html` Notes v1 writes to `localStorage: rm_note_<chartRecordId>`. The Supabase `notes` table is not wired. Notes are not persisted across devices, browsers, or cleared storage.

**R5: `first_profile_intake.js` allows one profile per intake session**  
After the first profile creation, `location.reload()` or redirect fires immediately. If the user's account already has profiles but `SupabaseStoreReady` rejects for a different reason (network error, RLS misconfiguration), the intake overlay fires on top of an account that may already have data.

**R6: `handle_new_user()` is the only allowed account bootstrap path**  
`user_profile.js` performs no writes. If `handle_new_user()` trigger fails silently (e.g., migration not applied, Supabase trigger disabled), the user authenticates successfully but `app_account_ids()` returns empty, `CurrentUser` is null, and no diagnostic reaches the user beyond a logged console error.

**R7: `services/supabase_client.py` calls `load_dotenv()` without explicit path**  
Loads `.env` from current working directory. If server is started outside the repo root, or if `.env` is absent and only `.env.staging` exists, the backend connects to no Supabase project and all repository calls fail silently or raise `RuntimeError`.

**R8: `cities.js` (GeoNames city typeahead) is ~12MB**  
Loaded synchronously via `<script>` tag in `map_CURRENT.html`. On slow connections this delays map initialization. No async loading or lazy-loading is in place.

**R9: Genie render sessionStorage handoff is same-tab only**  
`rm_genie_render:<ref>` is written to sessionStorage before navigation. `target="_blank"` map links (used in `screenMap()`) do not carry sessionStorage. Genie render payload is silently absent for new-tab map opens from app_shell.

