# ACCOUNT / SHELL STATE OWNERSHIP — ARCHITECTURE NOTE

Status: Read-only architecture note. No code changes. Derived from the Application Shell & Drawer Architecture Audit.

Scope: app_shell.html, account_drawer.js, Profile Management UI, first_profile_intake.js, current_location_editor.js, and the account bootstrap globals they depend on. Out of scope: renderer, Rain/Virga, map math, overlays, GeoJSON, AI, export, sharing.

## 1. Current runtime chain

```
SupabaseReady (supabase_client.js)
  -> CurrentUserReady (user_profile.js)
    -> SupabaseStoreReady (supabase_store_bridge.js)
      -> app_shell.html viewModel (adaptStoreToView)
        -> account_drawer.js + Profile Management UI
```

- `supabase_client.js` fetches `/config/supabase`, loads the supabase-js UMD build, and resolves `window.SupabaseReady` with the client.
- `user_profile.js` waits on `SupabaseReady`, resolves the auth session, calls `app_account_ids()`, loads the `accounts` row and `account_memberships` role, and resolves `window.CurrentUserReady` / sets `window.CurrentUser`.
- `supabase_store_bridge.js` waits on `CurrentUserReady` + `SupabaseReady`, queries the account's profiles / birth records / favorites / comparison sets / saved searches / current locations / places / user_settings, and resolves `window.SupabaseStoreReady` with an assembled store. It rejects with an intake signal when no profiles/birth records exist.
- `app_shell.html` awaits `SupabaseStoreReady`, runs `adaptStoreToView()` to build `viewModel`, and renders screens. On the intake rejection it shows the first-profile overlay; on other failures it falls back to `/local-product-store.json`.
- `account_drawer.js` and Profile Management read from the resulting `viewModel` and `window.CurrentUser`.

## 2. Component responsibility map

### app_shell.html
- Owns shell page, route table, hash/query parsing, screen rendering, and map handoff URL construction.
- Owns runtime state: `navContext`, `uiState`, `viewModel`, `storeRaw`.
- Owns `adaptStoreToView()` (raw store -> UI view model).
- Owns Profile Management screen rendering and its actions (open, set location, rename, archive, add).
- Owns `saveAccountSettingsPatch()` (account-level user_settings write).
- Exposes the shell API as `window.__rmAppShell`.

### account_drawer.js
- Owns Account drawer DOM, styles, open/close, and click handling.
- Reads identity from `window.CurrentUser`.
- Reads profiles/default/active from `window.__rmAppShell.viewModel()` and `.navContext`.
- Delegates: navigation -> `__rmAppShell.navigate()`; add profile -> `__showFirstProfileIntake()`; set location -> `__showCurrentLocationEditor()`; logout -> `window.logout()`.
- Persists default-profile changes via `__rmAppShell.saveAccountSettingsPatch()` and mirrors via `savePersistedChartRecord()`.

### Profile Management UI
- Lives inside app_shell.html (not a separate module).
- Renders cards from `viewModel.chartRecords`; marks default from `viewModel.defaultChartRecordId`.
- Performs direct Supabase writes for rename and archive (not via a shared repository helper).
- Runs a direct `profiles` query as an archive safety guard (last-profile guard, replacement default selection).
- Delegates add profile and set current location to the shared overlays; refreshes via full page reload after writes.

### first_profile_intake.js
- Owns the first-profile / birth-record intake overlay.
- Activates on the `SupabaseStoreReady` intake rejection, or when called via `window.__showFirstProfileIntake()`.
- Writes: INSERT `profiles`, then INSERT `birth_records`, with best-effort compensating profile delete on failure.
- On success, redirects to the map with handoff params.

### current_location_editor.js
- Owns the "Set Current Location" overlay, exposed as `window.__showCurrentLocationEditor(profileId)`.
- Writes: retire existing `is_current` rows, then INSERT a new current `current_location_history` row (RLS-compliant, no service role).
- Refreshes via page reload after save.

## 3. Global state map

| Global | Owner | Purpose |
| --- | --- | --- |
| `window.__rmAppShell` | app_shell.html | Shell API + access to navContext, uiState, viewModel(), storeRaw(), helpers |
| `window.CurrentUser` | user_profile.js | Resolved account/user identity (userId, accountId, accountName, accountType, role) |
| `window.CurrentUserReady` | user_profile.js | Promise<CurrentUser> |
| `window.SupabaseClient` | supabase_client.js | Initialized Supabase client instance |
| `window.SupabaseReady` | supabase_client.js | Promise<SupabaseClient> |
| `window.SupabaseStore` | supabase_store_bridge.js | Assembled live account/profile store object |
| `window.SupabaseStoreReady` | supabase_store_bridge.js | Promise<store>; rejects when intake required |
| `window.__showAccountDrawer` | account_drawer.js | Open the Account drawer |
| `window.__showFirstProfileIntake` | first_profile_intake.js | Show first-profile/birth-record intake overlay |
| `window.__showCurrentLocationEditor` | current_location_editor.js | Show set-current-location overlay |
| `window.logout` | auth_guard.js | Sign out and redirect to auth |

Additional related globals observed (for completeness, not in the requested list): `window.initializeCurrentUser` (user_profile.js), `window.__rmAppShellGenie` (in-shell Genie mount).

## 4. Source-of-truth decisions

- Current account = `window.CurrentUser` (from user_profile.js).
- Raw account/profile store = `window.SupabaseStore` (from supabase_store_bridge.js).
- UI view model = app_shell.html adapted `viewModel` (from adaptStoreToView).
- Current active profile = `navContext.chartRecordId` (app_shell.html).
- Account default profile = `user_settings.settings_json.default_chart_record_id` (persisted in Supabase).
- Last selected profile = `localStorage` key `rm_selected_chart_<userId>` (app_shell.html).
- Account drawer open state = DOM-owned in account_drawer.js (drawer/scrim `.open` class).
- Genie drawer state = `uiState.drawerOpen` in app_shell.html (in-shell map drawer, NOT the Account drawer).

## 5. Main architecture problem

`viewModel.defaultChartRecordId` currently blurs two distinct concepts:

- the **account default profile** (`user_settings.settings_json.default_chart_record_id`), and
- the **last selected / current profile** (`localStorage rm_selected_chart_<userId>`).

After `adaptStoreToView()`, app_shell.html overrides `viewModel.defaultChartRecordId` with the localStorage last-selected chart when that value is valid. As a result, a single field is read in places that mean "account default" (Dashboard, Settings default selector, default star) and in places effectively driven by "last selected." Default writes are also spread across multiple paths (account drawer star, Settings save, archive replacement selection), each touching both the Supabase setting and the localStorage mirror.

## 6. Required future correction

Separate the two concepts into clearly named state:

- `accountDefaultChartRecordId` — sourced only from `user_settings.settings_json.default_chart_record_id`; never overwritten by localStorage.
- `selectedChartRecordId` / `lastSelectedChartRecordId` — sourced from `localStorage rm_selected_chart_<userId>` (and/or `navContext.chartRecordId` for the active session).

Consumers should then read the field that matches intent: Dashboard / default star / Settings default selector read `accountDefaultChartRecordId`; map entry and resume read the selected/last-selected value. Default writes should flow through a single helper rather than being duplicated across drawer, settings, and archive.

## 7. Recommendation

Do not add new profile/account features until this distinction is named and tightened. The current architecture is acceptable but fragile; introducing more behavior on top of the overloaded `defaultChartRecordId` will compound the ambiguity. The smallest safe next step after this note is to split account-default from last-selected state, leaving raw loading (supabase_store_bridge.js) and identity (user_profile.js) unchanged.
