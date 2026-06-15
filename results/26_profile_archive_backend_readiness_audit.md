# RESULT: 26_PROFILE_ARCHIVE_BACKEND_READINESS_AUDIT

Task: `26_PROFILE_ARCHIVE_BACKEND_READINESS_AUDIT`
Mode: read-only audit; documentation output only
Result: **VERIFIED**

## Scope

Inspected only the requested production paths and source evidence:

- `repositories/profiles_repository.py`
- `main_centerline_FIXER.py`
- `supabase_store_bridge.js`
- `app_shell.html`
- `results/21_profile_rename_archive_scope_plan.md`
- `results/23_profile_rename_copy_and_live_smoke.md`
- `results/24_env_staging_canon_audit.md`
- `docs/architecture/ENV_STAGING_CANON.md`

No production files were modified.

## Executive finding

Profile archive can be implemented safely **only** as a guarded soft archive that also handles active/default profile replacement. The storage model already supports non-destructive archive through `profiles.archived_at`, and the Supabase bridge already hides archived profiles. Child objects are profile-scoped and do not need to be renamed, deleted, or re-parented.

The unsafe path would be a naive backend call to `POST /profiles/{profile_id}/archive`: the route exists, but it uses repository functions that fetch/update by profile id only and do not show caller ownership checks in the inspected code. The safer MVP remains a direct Supabase client write from the Profile Management card, filtered by both `id` and `account_id`, matching the Task 22 rename pattern.

## Answers

### 1. Does `profiles` already support soft archive via `archived_at`?

Yes.

Evidence:

- `repositories/profiles_repository.py` has `archive_profile(profile_id)` that updates:
  - `archived_at` to the current UTC timestamp
  - `updated_at` to the current UTC timestamp
- `main_centerline_FIXER.py` exposes `POST /profiles/{profile_id}/archive`, which calls `archive_profile(profile_id)` after checking that `get_profile(profile_id)` returns a row.
- Task 23 source evidence confirmed the active staging schema includes `profiles.archived_at`.

This is a soft archive; no delete/cascade behavior is present in the inspected archive function.

### 2. Does the bridge already exclude archived profiles?

Yes.

`supabase_store_bridge.js` queries profiles with:

- `.eq("account_id", accountId)`
- `.is("archived_at", null)`

So archived profiles are excluded from the active `profiles` list before the app shell view model is assembled.

The bridge also excludes archived child list rows where those child tables support it:

- `favorite_places`: `.is("archived_at", null)`
- `comparison_sets`: `.is("archived_at", null)`
- `saved_searches`: `.is("archived_at", null)`

Archive of a profile does not currently cascade to children; children remain in the DB and simply become unreachable through active profile lists because their parent profile is hidden.

### 3. What happens if the active profile disappears?

Partially safe, but not fully normalized.

Existing fallback:

- `getChartRecord(id)` returns `vm.chartRecords.find(...) || vm.chartRecords[0]`.
- If the URL/local active profile id points at an archived profile that is no longer in `vm.chartRecords`, display code that calls `activeRecord()` will often render the first available active profile.
- `loadViewModelFromStore()` only applies the locally persisted chart id if it still exists in `viewModel.chartRecords`, so stale persisted ids are ignored after reload.

Remaining risk:

- `normalizeNavContext()` fills a missing required `chartRecordId`, but it does not replace an invalid/stale `chartRecordId` that is still present in the URL hash.
- Some action handlers use `navContext.chartRecordId` directly rather than the fallback record id, including:
  - `open-map-record`
  - `open-map-favorite`
  - `set-current-location`
  - `save-chart-note`

Therefore a stale URL hash for an archived profile can visually render the first active profile while still keeping the archived id in `navContext`. That can orphan actions or send map/current-location/note operations with a stale archived profile id.

Archive implementation must explicitly replace/clear stale active profile context before reload or navigation.

### 4. What happens if the default profile disappears?

The bridge has data-level fallback.

`supabase_store_bridge.js` reads `rawSettings.default_chart_record_id`, then checks whether it is still present in assembled `storeClients`. If valid, it uses it. If invalid/missing, it falls back to `storeClients[0].id`.

So if the stored default profile is archived, the next bridge load will choose the first remaining active profile as `default_chart_record_id` in the in-memory store.

However, this fallback is not persisted automatically. `app_shell.html` can persist default settings through `saveAccountSettingsPatch({ default_chart_record_id })`, but archive does not yet update `user_settings.settings_json.default_chart_record_id`. Without an explicit settings patch, the stale default can remain stored and the bridge will keep applying a runtime fallback on each load.

### 5. Is there already fallback logic?

Yes, but it is incomplete for archive.

Existing fallback logic:

- Bridge: invalid stored default falls back to first remaining active client.
- Shell: stale persisted chart id is ignored if it no longer appears in the loaded chart records.
- Shell: `getChartRecord(id)` falls back to first record for display.

Missing fallback/guardrails for archive:

- No explicit block for archiving the last active profile.
- No explicit default replacement persistence when archiving the default profile.
- No URL/navContext normalization when the current route points to the archived profile.
- No clearing/updating of the locally persisted chart id when archiving the persisted active profile.
- No archive button/flow in Profile Management yet, by product choice.

### 6. Is there any path that could orphan the UI?

Yes, if archive is implemented naively.

Orphan risks:

1. Last active profile archived
   - Bridge will load zero active profiles and throw `[supabase_store_bridge] No profiles found. Intake overlay required.`
   - App shell treats that as `INTAKE_REQUIRED`, which could incorrectly show intake for an account that has archived profiles rather than no profiles.
   - This must be blocked.

2. Active route points to archived profile
   - Display may fall back to first active profile, but `navContext.chartRecordId` can remain stale.
   - Actions may operate on the archived id.

3. Default profile archived without persisted replacement
   - Runtime bridge fallback works, but stored settings remain stale.
   - Settings/default UI may keep requiring fallback every load instead of reflecting the new default.

4. Backend route used as-is
   - `POST /profiles/{profile_id}/archive` is id-only in the inspected route/repository path.
   - It does not show caller auth/ownership checks and should not be exposed to frontend archive until hardened.

### 7. What exact updates would be required during archive?

Minimum safe archive transaction/sequence from Profile Management:

1. Resolve current account/user context.
2. Load active profiles for the account, excluding archived profiles.
3. Block archive if there is only one active profile.
4. Choose replacement profile if the archived profile is currently default or active:
   - Prefer existing default if it is not the archived profile.
   - Otherwise choose the first remaining active profile.
5. Soft archive only the parent profile:
   - update `profiles`
   - set `archived_at = now`
   - set `updated_at = now` if available/desired
   - filter by `id = profileId`
   - filter by `account_id = current account id`
   - ideally also `.is("archived_at", null)` for idempotency
6. If archived profile was the stored default, patch account-level `user_settings.settings_json.default_chart_record_id` to the replacement profile id.
7. If archived profile was the active URL/persisted profile, update local persisted chart id to replacement or clear it.
8. Navigate to a safe route/profile and reload/refetch app shell state.
9. Do not mutate or delete child rows:
   - `birth_records`
   - `favorite_places`
   - `saved_searches`
   - `comparison_sets`
   - `comparison_set_places`
   - `current_location_history`
   - notes/local note keys

### 8. What validations must run before archive is enabled?

Required validations:

1. Environment canon
   - Confirm backend/frontend QA is using `.env.staging` project `rnwlrdtqhfjhpllryxiz`, not stale `.env` project `dpmtmmryvlftfahipowa`.

2. Pre-archive data check
   - At least two active profiles exist for the account.
   - Candidate profile belongs to current account.
   - Candidate profile is not already archived.
   - Replacement active profile exists and has a birth record.

3. Default behavior
   - If non-default profile archived: stored default remains unchanged.
   - If default profile archived: stored `default_chart_record_id` changes to replacement.
   - Dashboard opens map for the replacement default.

4. Active context behavior
   - If current route/hash points at archived profile, shell lands on replacement profile or dashboard with replacement default.
   - `navContext.chartRecordId` is not left stale.
   - persisted chart id is not left stale.

5. Child preservation
   - Child row counts for archived profile are unchanged after archive:
     - birth records
     - favorite places
     - saved searches/investigations
     - comparison sets/places
     - current location history
   - Children are not visible under unrelated active profiles.

6. Visibility
   - Archived profile disappears from Profile Management cards, dashboard library, settings default selector, and map selector.
   - Remaining profiles and their children still render.

7. Guardrails
   - Blank/missing profile id rejected.
   - Last active profile archive blocked.
   - Archive action not exposed in Account Drawer for MVP.
   - Backend route not used unless ownership checks are added first.

### 9. What is the smallest safe implementation sequence?

Smallest safe sequence:

1. Frontend-only MVP in `app_shell.html`, Profile Management cards only.
   - Add an Archive button only after the copy/product decision explicitly allows it.
   - Keep Account Drawer untouched.

2. Implement preflight guard in the handler.
   - Use `window.SupabaseReady` and `window.CurrentUser.accountId`.
   - Query active profiles for the current account with `archived_at IS NULL`.
   - Block archiving if active profile count is 1.
   - Compute replacement profile id before writing.

3. Soft archive via Supabase client write.
   - `profiles.update({ archived_at: now, updated_at: now }).eq("id", profileId).eq("account_id", accountId).is("archived_at", null)`
   - Do not call `POST /profiles/{profile_id}/archive` for MVP, because backend ownership hardening is not visible in the inspected code.

4. Patch default settings only when necessary.
   - If archived profile was `viewModel.defaultChartRecordId`, use the existing `saveAccountSettingsPatch` pattern to set `default_chart_record_id` to replacement.

5. Repair active context.
   - If archived profile equals `navContext.chartRecordId` or locally persisted chart id, set persisted chart id to replacement and navigate/reload to a safe route using replacement.

6. Run focused live smoke on staging.
   - Archive a safe test profile with children if available.
   - Verify profile disappears from active UI.
   - Verify child rows remain in DB.
   - Verify default/active replacement.
   - Restore by clearing `archived_at` only if a reversible smoke is explicitly approved; otherwise do not mutate live data.

7. Later harden backend.
   - If backend route is ever used by the frontend, add authenticated request handling and account ownership filtering before `get_profile`/`archive_profile`.

## Readiness conclusion

The database and bridge are ready for soft archive semantics. The app is not ready for a one-line archive button yet because active/default context must be repaired explicitly, and the existing backend route should not be used by the frontend until ownership checks are hardened.

Safe implementation is feasible as a small Phase B, but only with these guardrails:

- block last active profile
- choose replacement first
- soft archive parent only
- persist default replacement when needed
- clear/update active persisted profile and route
- validate child preservation
- use `.env.staging` for QA

## Scope verification

- No production files modified.
- Audit written to `audits/26_profile_archive_backend_readiness_audit.md` and `results/26_profile_archive_backend_readiness_audit.md`.

VERIFIED
