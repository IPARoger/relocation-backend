# APPLICATION SHELL ARCHITECTURE SPECIFICATION

Status: Read-only specification. No implementation, staging, or commits.

Sources:
- results/33_account_infrastructure_hygiene_closeout.md
- results/34_account_shell_state_ownership_audit.md

Scope: app_shell.html, account_drawer.js, Profile Management UI, first_profile_intake.js, current_location_editor.js, and the account bootstrap globals they depend on. Out of scope: renderer, Rain/Virga, map math, overlays, GeoJSON, AI, export, sharing.

This document defines the *intended* architecture (the target). It is not a description of current behavior except where noted. Current behavior is in note 34.

---

## 1. Intended ownership model

Each state object has exactly one owning module. "Owner" means the single module responsible for the canonical value; all other modules read through the owner's published surface.

| State object | Intended owner | Canonical source |
| --- | --- | --- |
| Account | user_profile.js | Supabase auth session + accounts/account_memberships -> `window.CurrentUser` |
| Profile (set of profiles) | supabase_store_bridge.js | Supabase `profiles` (+ related) -> `window.SupabaseStore` |
| Default profile | supabase_store_bridge.js (read) / app_shell.html `saveAccountSettingsPatch()` (write) | `user_settings.settings_json.default_chart_record_id` |
| Selected profile (current active) | app_shell.html | `navContext.chartRecordId` |
| Last selected profile | app_shell.html | `localStorage rm_selected_chart_<userId>` |
| Account drawer state | account_drawer.js | DOM (`#rm-account-drawer` / scrim `.open`) |
| Navigation state | app_shell.html | `navContext` + `uiState` (incl. `uiState.drawerOpen` = Genie drawer, not Account drawer) |

Key rule: **account default profile and selected/last-selected profile are distinct objects with distinct owners and must not be collapsed into one field.** This is the core correction carried from note 34.

Target naming (replacing the overloaded `viewModel.defaultChartRecordId`):
- `accountDefaultChartRecordId` — account default, Supabase-sourced only.
- `selectedChartRecordId` — current active profile for this session (mirror of `navContext.chartRecordId`).
- `lastSelectedChartRecordId` — persisted last selection (localStorage).

---

## 2. Allowed write paths for each state object

- **Account (`window.CurrentUser`)**: written only by user_profile.js after auth/session resolution. Re-runnable via `initializeCurrentUser()`.
- **Profile store (`window.SupabaseStore`)**: assembled only by supabase_store_bridge.js (read-only assembler; zero DB writes in the bridge itself).
- **Profile records (DB rows)**:
  - Create profile + birth record: first_profile_intake.js only.
  - Rename profile / archive profile: Profile Management actions (app_shell.html), ideally via a single shared profile-write helper.
  - Current location rows: current_location_editor.js only.
- **Default profile (`user_settings...default_chart_record_id`)**: written only through `app_shell.html` `saveAccountSettingsPatch()`. Callers: Settings save, Account drawer star, archive replacement logic.
- **Selected profile (`navContext.chartRecordId`)**: written only by app_shell.html navigation functions (`navigate()`, `switchChartRecord()`).
- **Last selected profile (localStorage)**: written only by app_shell.html `savePersistedChartRecord()` (exposed as `__rmAppShell.savePersistedChartRecord`).
- **Account drawer state**: written only by account_drawer.js `open()` / `close()`.
- **Navigation/UI state**: written only by app_shell.html (`navigate`, `render`, `uiState` mutations).

---

## 3. Forbidden write paths

- No module other than user_profile.js may set `window.CurrentUser`.
- No module may mutate `window.SupabaseStore` after assembly; consumers treat it as immutable.
- account_drawer.js must NOT directly mutate `viewModel.defaultChartRecordId` (current code does this optimistically — disallowed in target). It must go through `saveAccountSettingsPatch()` and let the shell own the resulting value.
- Profile Management and account_drawer.js must NOT write localStorage selection directly; they use `savePersistedChartRecord()`.
- localStorage last-selected must NOT overwrite `accountDefaultChartRecordId` (the current override in `loadViewModelFromStore()` is the specific anti-pattern to remove).
- Overlays (first_profile_intake.js, current_location_editor.js) must NOT read or write shell `navContext`/`viewModel` directly; they communicate by their entry-point arguments and by triggering reload.
- No module outside app_shell.html may construct map handoff URLs or mutate route hash directly.

---

## 4. Component read / write / persistence / rendering ownership

| Concern | Owner |
| --- | --- |
| Reading account identity | user_profile.js (others read `window.CurrentUser`) |
| Reading profile data | supabase_store_bridge.js (others read via `viewModel`) |
| Writing profile DB rows | first_profile_intake.js (create), Profile Management (rename/archive), current_location_editor.js (location) |
| Writing account settings (default) | app_shell.html `saveAccountSettingsPatch()` |
| Persistence of selection | app_shell.html (`savePersistedChartRecord` -> localStorage) |
| Persistence of default | Supabase user_settings (via shell helper) |
| Rendering shell + screens + Profile Management | app_shell.html |
| Rendering Account drawer | account_drawer.js |
| Rendering intake overlay | first_profile_intake.js |
| Rendering location overlay | current_location_editor.js |
| View model derivation (raw store -> UI) | app_shell.html `adaptStoreToView()` |

Principle: identity and raw data are read-owned by their loaders; the shell owns derivation, navigation, selection persistence, and default writes; drawers/overlays are render + delegate only.

---

## 5. Globals that should remain public

These are legitimate cross-module contracts and should stay public:

- `window.SupabaseReady` / `window.SupabaseClient` — shared client contract.
- `window.CurrentUser` / `window.CurrentUserReady` — identity contract.
- `window.SupabaseStore` / `window.SupabaseStoreReady` — store contract.
- `window.logout` — invoked from drawer and any page UI.
- `window.__showAccountDrawer`, `window.__showFirstProfileIntake`, `window.__showCurrentLocationEditor` — overlay/drawer entry points used across modules.

---

## 6. Globals that should eventually become internal

- `window.__rmAppShell` — currently a broad surface (navContext, uiState, viewModel(), storeRaw(), many helpers). It should be narrowed to a small, intentional API. Internal-only items to hide or wrap behind methods: raw `state`, `storeRaw()`, internal contracts, and direct `viewModel` mutation access.
- `window.__rmAppShellGenie` — in-shell map drawer mount; should be internal to the shell/Genie integration, not a global.
- `window.initializeCurrentUser` — can remain but is effectively internal re-init; keep only if a real re-auth caller exists.
- Direct writable access to `viewModel.defaultChartRecordId` via `__rmAppShell.viewModel()` should be removed once accountDefault/selected are split; the drawer should consume read-only values + a write method.

---

## 7. Future shell boundary recommendations

- Define a thin `__rmAppShell` public API: `navigate()`, `openMap()`, `getAccountDefaultChartRecordId()`, `getSelectedChartRecordId()`, `setAccountDefaultChartRecord()`, `setSelectedChartRecord()`, read-only `getProfiles()`. Hide everything else.
- Introduce one profile-write module (rename/archive/create/location) so Profile Management and intake/location overlays share consistent write + RLS handling instead of inline direct queries.
- Rename `uiState.drawerOpen` to something Genie-specific (e.g. `genieDrawerOpen`) to end the "drawer" naming collision with the Account drawer.
- Replace post-write full page reloads with a single explicit "refresh store + re-render" path owned by the shell, so write modules do not each depend on reload semantics.
- Keep identity (user_profile.js) and raw assembly (supabase_store_bridge.js) as pure read layers; never let UI modules write through them.

---

## 8. Refactor priority ranking

### Must do before new profile features
1. Split `accountDefaultChartRecordId` from `selectedChartRecordId` / `lastSelectedChartRecordId`; remove the localStorage override of the account default in `loadViewModelFromStore()`.
2. Route ALL default-profile writes through `saveAccountSettingsPatch()`; stop account_drawer.js from directly mutating `viewModel.defaultChartRecordId`.
3. Make `window.SupabaseStore` / `viewModel` consumption read-only for the drawer (no in-place mutation).

### Should do later
4. Narrow the `__rmAppShell` public API; hide internal state/helpers.
5. Extract a single shared profile-write helper for rename/archive/create/location.
6. Rename `uiState.drawerOpen` -> Genie-specific name to remove the drawer ambiguity.
7. Replace per-action page reloads with a shell-owned refresh + re-render.

### Leave alone
8. user_profile.js identity loading and the `app_account_ids()` RPC path.
9. supabase_client.js bootstrap and `/config/supabase` contract.
10. supabase_store_bridge.js as a read-only assembler (its query shape is fine; only consumers need tightening).
11. The overlay entry-point pattern (`__show*`) — keep as the cross-module contract.

---

## Closing note

The account infrastructure is committed and reproducible (note 33). The remaining work is boundary clarity, not new data plumbing. The single highest-leverage correction is item 1: stop one field from meaning both "account default" and "last selected." No new profile/account feature should be added until items 1-3 are done.
