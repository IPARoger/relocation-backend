# ADD PROFILE OVERLAY BEHAVIOR SPEC

Status: read-only spec. No implementation in this note.
Scope of behavior: `app_shell.html`, `account_drawer.js`, `first_profile_intake.js`.
Related: `results/34_account_shell_state_ownership_audit.md`, `results/35_application_shell_architecture_spec.md`.

## Product decision

- Add Profile is always an overlay launched on top of whatever page the user is already using. It must not switch screens or navigate to a new page just to render the form.
- There are two cases:
  1. First profile (created immediately after account creation): the overlay is shown over the map page, and after save the user continues into the map/product flow for the new profile.
  2. Future Add Profile (account already has a profile): the overlay is launched in place over the current page, and after save the user returns to the same page/screen.
- The future Add Profile overlay includes a "Switch to new profile" toggle, checked by default. The user may uncheck it to remain on the previous profile.
- Adding a profile never changes the account default profile.
- A full app reload should be avoided unless unavoidable in the current implementation.

## Current mismatch

Launch points today all call `window.__showFirstProfileIntake()`:

- Profile / Chart Record page (`add-chart-record`)
- Profile Management (`pm-add-profile`)
- Account Drawer (`ad-add-profile`)
- First-run auto path (`INTAKE_REQUIRED`)

On success, `first_profile_intake.js` always does a hard navigation:

```
INSERT profiles
INSERT birth_records
window.location.href = /map_CURRENT.html?...&chartRecordId=<newProfileId>
```

Mismatches against the product decision:

1. The same overlay and the same "redirect to map" success behavior is used for both first-profile creation and future Add Profile.
2. Future Add Profile exits the current page to the map, which is a screen switch the user did not ask for.
3. The new profile does not become selected/last-selected in shell state; only the map handoff URL carries it. Returning to the page can still show the previous profile.
4. There is no "Switch to new profile" toggle; the flow always switches and always goes to the map.
5. Behavior is correct only for the first-profile case.

## Desired behavior

### First profile (immediately after account creation)
1. Overlay is shown over the map page.
2. User completes the simple profile form (display name, birth date, birth time mode/time, birth place).
3. Save creates the new profile and its birth record via the existing RLS-compliant write path.
4. After save, the user continues into the map/product flow for the new profile (current redirect behavior is acceptable here).
5. No "Switch to new profile" toggle is needed; it is the only profile.

### Future Add Profile (account already has a profile)
1. User clicks Add Profile from the Profile/Chart Record page, Profile Management, Account Drawer, or any future shell screen.
2. Add Profile opens as a lightweight overlay/modal in place. No screen switch, no new page load to show the form.
3. The overlay includes a "Switch to new profile" toggle, checked by default.
4. User completes the simple profile form.
5. Save creates the new profile (and its birth record).
6. Account default profile remains unchanged. No write to `user_settings.settings_json.default_chart_record_id`.
7. After a successful save, the overlay closes in place.
8. If "Switch to new profile" is checked (default):
   - selected profile becomes the new profile (`navContext.chartRecordId` / `viewModel.selectedChartRecordId`)
   - last-selected profile becomes the new profile (`rm_selected_chart_<userId>` via `savePersistedChartRecord`)
   - the user returns to the same page/screen they launched from, now scoped to the new profile where applicable
9. If "Switch to new profile" is unchecked:
   - selected profile remains the previous profile
   - last-selected profile remains the previous profile
   - the user returns to the same page/screen unchanged
10. In both checked and unchecked cases, the profile list and Account Drawer reflect the new profile after the relevant view refreshes/updates.

## Selected / default / last-selected semantics

Using the ownership model from spec 35:

| State | Source of truth | Switch checked (default) | Switch unchecked | First profile |
| --- | --- | --- | --- | --- |
| Account default profile | `user_settings.settings_json.default_chart_record_id` (written only via `saveAccountSettingsPatch()`) | unchanged | unchanged | unchanged (may be set later, not by Add Profile) |
| Selected profile (current active) | `navContext.chartRecordId` / `viewModel.selectedChartRecordId` (shell nav only) | becomes new profile | unchanged (previous profile) | the new profile via map flow |
| Last-selected profile | `localStorage rm_selected_chart_<userId>` (via `savePersistedChartRecord`) | becomes new profile | unchanged (previous profile) | n/a until shell next loads |

Rules:

- Add Profile never writes the account default. "Set as default" stays a separate, explicit action (Account Drawer star / Settings).
- The "Switch to new profile" checked path is the only one that writes selected and last-selected, and it does both together to stay consistent.
- The unchecked path writes nothing to selection state.
- Either way, the user returns to the same page/screen they launched from (only re-scoped to the new profile when Switch is checked).

## First-profile case

- Detected today by `SupabaseStoreReady` rejecting with `INTAKE_REQUIRED` (no profiles/birth records yet), which corresponds to first profile creation right after account creation.
- In this case the new profile is the only profile, so the overlay shows over the map page and continuing into the map/product flow for it is correct.
- The "Switch to new profile" toggle applies only when at least one profile already exists.

## Smallest safe implementation plan

Goal: separate "first profile" from "future Add Profile" without rewriting the intake form, and without touching default-profile logic.

Phase 1 - introduce a launch context (no behavior change for first profile):
- Give `window.__showFirstProfileIntake(options)` an optional `options` argument carrying a `mode` (e.g. "first" vs "add") and/or `onCreated` callback.
- Backwards-compatible: called with no args behaves exactly as today (first-profile overlay over map, redirect to map flow).
- Shell launch points (`add-chart-record`, `pm-add-profile`, Account Drawer `ad-add-profile`) pass an "add" context.

Phase 2 - branch success behavior on context:
- First-profile / no-context: keep current `window.location.href` map flow.
- Add context: on success, do NOT redirect; close the overlay and hand the new `profileId` (and the "Switch to new profile" toggle value) back to the shell.

Phase 3 - add the "Switch to new profile" toggle (add context only):
- Render the toggle in the overlay, checked by default, only when launched in add context.

Phase 4 - shell-owned post-save handling:
- Add a shell helper (e.g. `handleProfileCreated(newProfileId, { switchToNew })`) that:
  - refreshes the profile list/view model so the new profile appears,
  - if `switchToNew`: re-scopes the current page to the new profile and writes selected + last-selected (reuse `switchChartRecord` / `savePersistedChartRecord`),
  - if not `switchToNew`: leaves selection untouched and returns to the same page unchanged.
- Account default writes are explicitly excluded from this helper.

Phase 5 - reduce reloads opportunistically:
- Prefer view-model refresh + `render()` over `window.location.reload()` where feasible.
- If a full reload is currently the only safe refresh mechanism, it is acceptable as an interim step, but the chosen selected/last-selected state must survive it.

Validation expectations for the eventual implementation (not part of this note):
- Future Add Profile from each shell entry point opens an in-place overlay, never a page switch to show the form.
- Toggle defaults to checked.
- After save with Switch checked: selected + last-selected become the new profile; default unchanged; user is back on the same page scoped to the new profile.
- After save with Switch unchecked: selected + last-selected unchanged; default unchanged; user is back on the same page unchanged.
- New profile appears in lists/drawer after refresh in both cases.
- First profile (no profiles yet) still shows over the map and continues into the map/product flow.

## Explicit non-goals

- Do not introduce dashboard or SaaS-style home screen language.
- Do not automatically make the new profile the account default.
- Do not always redirect to the map after future Add Profile (only the first-profile case continues into the map flow).
- Do not reload the whole app unless unavoidable in the current implementation.
