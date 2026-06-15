# AUDIT: 27_PROFILE_ARCHIVE_PHASE_B_PLAN

Task: `27_PROFILE_ARCHIVE_PHASE_B_PLAN`
Mode: planning only; documentation output. No implementation.
Result: **VERIFIED**

## Source evidence

- `audits/26_profile_archive_backend_readiness_audit.md`
- `results/26_profile_archive_backend_readiness_audit.md`
- `results/23_profile_rename_copy_and_live_smoke.md`
- `docs/architecture/ENV_STAGING_CANON.md`

## Design constraints carried forward

- Frontend-only MVP. Soft archive via Supabase client write. No backend route (`POST /profiles/{id}/archive` not ownership-hardened).
- Profile Management cards only. Account Drawer untouched. No change to `first_profile_intake.js`, backend, schema, map, renderer.
- Soft archive parent only; never delete or re-parent child rows.
- All QA against `.env.staging` project `rnwlrdtqhfjhpllryxiz` (per ENV canon).
- Pattern mirror: the Task 22 rename handler (`pm-rename-profile`, `app_shell.html:2165-2194`) is the structural template.

## Exact implementation plan

### 1. Exact UI placement for Archive button

In `screenProfileList()` card actions (`app_shell.html`), the `.pm-actions` row currently ends with the Rename button at line 1770. Add Archive as the last button in that row, only on Profile Management cards:

```
<button type="button" data-action="pm-archive-profile"
        data-chart-record="${r.chartRecordId}"
        data-current-name="${escapeHtml(r.displayName)}">Archive</button>
```

Placement rule:
- After `pm-rename-profile`, inside the same `<div class="pm-actions">`.
- Not on the dashboard library list, not in Account Drawer, not on the Chart Record page.

Copy-board note: `screenProfileList()` currently has `<p class="must-not">Must not appear: archive, delete, ...</p>` at line 1786. Enabling archive REQUIRES first removing `archive` from that must-not line (keep `delete`). That copy edit is part of Phase B, not a separate task.

### 2. Exact confirmation copy

Use a single `window.confirm` (mirrors `archive-favorite`/`archive-exploration` style). Two variants depending on whether the target is the current default:

Standard:
```
Archive "<name>"? It will be hidden from your profiles. Its favorites, saved searches, and comparisons are kept but hidden. You can restore it later from the database.
```

When archiving the current default profile, append:
```
This is your default profile. Archiving it will switch your default to "<replacementName>".
```

If the guard (section 4) trips, do NOT show confirm; show:
```
You cannot archive your only profile. Add another profile first.
```

### 3. Exact Supabase query to load active profiles

Before writing, load the account's active profiles fresh (do not trust only the in-memory view model), mirroring the bridge query at `supabase_store_bridge.js:64-69`:

```
const { data: activeProfiles, error } = await client
  .from("profiles")
  .select("id, display_name")
  .eq("account_id", accountId)
  .is("archived_at", null)
  .order("created_at", { ascending: true });
```

Use `activeProfiles` for the guard and replacement selection.

### 4. Exact guard for blocking last active profile

```
if (error) throw error;
const active = activeProfiles || [];
if (active.length <= 1) {
  window.alert('You cannot archive your only profile. Add another profile first.');
  return;
}
if (!active.some(p => p.id === profileId)) {
  window.alert('That profile is no longer active.');
  return;
}
```

Rule: never allow active count to drop below 1. The check uses the freshly loaded active list, not the cached view model.

### 5. Exact replacement profile selection rule

Replacement is only needed when the archived profile is the current default and/or the active/persisted profile. Selection order:

1. Current default `viewModel.defaultChartRecordId`, if it is active and not the profile being archived.
2. Otherwise the first profile in `active` (created_at ascending) whose `id !== profileId`.

```
const currentDefault = (window.__rmAppShell && window.__rmAppShell.viewModel()
  && window.__rmAppShell.viewModel().defaultChartRecordId) || null;
const remaining = active.filter(p => p.id !== profileId);
const replacementId =
  (currentDefault && currentDefault !== profileId
    && remaining.some(p => p.id === currentDefault))
    ? currentDefault
    : remaining[0].id;
```

`remaining[0]` is guaranteed to exist because of the section 4 guard (active.length >= 2).

### 6. Exact Supabase update for `profiles.archived_at`

Soft archive, parent only, scoped by `id` + `account_id`, idempotent via `.is("archived_at", null)`:

```
const nowIso = new Date().toISOString();
let upd = client
  .from("profiles")
  .update({ archived_at: nowIso, updated_at: nowIso })
  .eq("id", profileId)
  .is("archived_at", null);
if (accountId) upd = upd.eq("account_id", accountId);
const { error: archiveErr } = await upd;
if (archiveErr) throw archiveErr;
```

No writes to `birth_records`, `favorite_places`, `saved_searches`, `comparison_sets`, `comparison_set_places`, `current_location_history`, or notes.

Note: `updated_at` is included to match `repositories/profiles_repository.archive_profile`. If a PostgREST error indicates the column is not writable under the anon/RLS path, fall back to `{ archived_at: nowIso }` only.

### 7. Exact `default_chart_record_id` patch rule

Only patch settings when the archived profile WAS the stored/effective default. Reuse existing `saveAccountSettingsPatch` (`app_shell.html:2393-2427`), which merges into the account-level `user_settings` row (`profile_id IS NULL`):

```
const wasDefault = currentDefault && currentDefault === profileId;
if (wasDefault) {
  await saveAccountSettingsPatch({ default_chart_record_id: replacementId });
}
```

If not default, do not touch `user_settings`. (Bridge already falls back at load, but persisting avoids a stale stored default.)

### 8. Exact persisted active-profile repair rule

The persisted key is `rm_selected_chart_<uid>` via `_savePersistedChartRecord` / `_loadPersistedChartRecord` (`app_shell.html:245-259`). Repair only if it points at the archived profile:

```
const persisted = (window.__rmAppShell && window.__rmAppShell.loadPersistedChartRecord
  ? window.__rmAppShell.loadPersistedChartRecord()
  : null);
if (persisted === profileId) {
  window.__rmAppShell.savePersistedChartRecord(replacementId);
}
```

(Exposed as `window.__rmAppShell.savePersistedChartRecord` at line 2451; a `loadPersistedChartRecord` getter should be added to the same export object if not already present, or read the key directly. This is an internal wiring detail, not a product decision.)

Do not clear the key to empty; always set to a valid replacement to avoid an undefined active profile.

### 9. Exact post-archive navigation/reload behavior

After a successful archive + (optional) default patch + persisted repair:

- If the archived profile was the active route target (`navContext.chartRecordId === profileId`) OR was default:
  - Navigate to a safe neutral route and reload, so the bridge re-derives active profiles and default:
    ```
    window.location.hash = '#/profiles';
    window.location.reload();
    ```
- Otherwise (archived a non-active, non-default profile from the list):
  - `window.location.reload();` (stay on Profile Management; card disappears).

Rationale: a full reload re-runs `supabase_store_bridge.js`, which excludes the archived profile and re-selects a valid default, matching how Task 22/23 rename concluded with `window.location.reload()`.

Error path mirrors rename:
```
} catch (err) {
  window.alert("Archive failed: " + (err.message || String(err)));
}
```

### 10. Exact live smoke sequence (reversible)

Run on `.env.staging` (`rnwlrdtqhfjhpllryxiz`), authenticated as the owning QA user via magiclink session (same harness as Task 23). Choose a safe disposable test profile that has children; do NOT archive `DG1`/`lisa` if they are the only two (guard would also block leaving one). Preferred: create a temporary throwaway profile for the destructive path, or pick an account with >=3 active profiles.

Sequence:
1. Snapshot: list active profiles for the account; record `default_chart_record_id`; record child counts (favorites, comparison_sets, saved_searches, birth_records) for the target profile id.
2. Guard check: confirm active count >= 2.
3. Compute expected replacement per section 5.
4. Archive via the exact section 6 update (client authenticated as owner).
5. Verify:
   - target `archived_at` is now set (single read by id).
   - target no longer appears in `profiles ... is archived_at null`.
   - child rows for target id still exist with identical counts (preserved, just hidden).
   - if target was default: `user_settings.settings_json.default_chart_record_id == replacementId`.
6. Reversible restore (only if a reversible smoke is explicitly approved):
   - `profiles.update({ archived_at: null }).eq("id", targetId).eq("account_id", accountId)`
   - if default was changed, restore `default_chart_record_id` to the original via `saveAccountSettingsPatch`/settings update.
   - re-verify target reappears in active list and child counts unchanged.
7. If reversible restore is NOT approved, do not mutate live data; mark live smoke NOT RUN and rely on code review.

Restore must run in a `finally` block so a mid-smoke failure still reverts, exactly as Task 23 did for rename.

## Out of scope for Phase B (do later)

- Unarchive UI, bulk archive, delete/hard delete, cascade.
- Archive from Account Drawer or Chart Record page.
- Backend route hardening (Phase C).

## Scope verification

- No production files modified (planning only).
- Plan references exact anchors in `app_shell.html` and `supabase_store_bridge.js`.
- Written to `audits/27_profile_archive_phase_b_plan.md` and `results/27_profile_archive_phase_b_plan.md`.

VERIFIED
