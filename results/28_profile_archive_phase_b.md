# RESULT: 28_PROFILE_ARCHIVE_PHASE_B

Task: `28_PROFILE_ARCHIVE_PHASE_B`
Mode: implementation
Allowed file: `app_shell.html` (only file changed)
Source plan: `audits/27_profile_archive_phase_b_plan.md`, `results/27_profile_archive_phase_b_plan.md`
Result: **VERIFIED**

## What was implemented (app_shell.html only)

### 1. Archive button (Profile Management cards only)
Added as the last button in the `.pm-actions` row of `screenProfileList()`, after Rename:

```
<button type="button" data-action="pm-archive-profile"
        data-chart-record="${r.chartRecordId}"
        data-current-name="${escapeHtml(r.displayName)}">Archive</button>
```

Appears only on Profile Management cards (not dashboard library, Account Drawer, or Chart Record page).

### 2. Must-not copy updated
`Must not appear: archive, delete, ...` -> `Must not appear: delete, notes count, saved searches count.`
`archive` removed; `delete` retained.

### 3-11. `pm-archive-profile` handler
Added next to the other `pm-*` handlers. Behavior, exactly per the approved plan:

- Active-profile query: `profiles.select("id, display_name").is("archived_at", null).order(created_at asc)`, scoped by `account_id` when present.
- Last-profile guard: if active count <= 1, alert and abort. Also aborts if the target is no longer in the active list.
- Replacement selection: keep `viewModel.defaultChartRecordId` if it is active and not the target; else first remaining active (created_at asc).
- Confirmation copy: standard message; default-profile variant appended when archiving the default.
- Soft archive: `profiles.update({ archived_at: now, updated_at: now }).eq("id", profileId).is("archived_at", null)`, scoped by `account_id` when present. If the write errors referencing `updated_at`, it retries once with `{ archived_at: now }` only.
- Default patch: `saveAccountSettingsPatch({ default_chart_record_id: replacementId })` only when the archived profile was the default.
- Persisted active repair: if `_loadPersistedChartRecord() === profileId`, set persisted chart to `replacementId`.
- Navigation/reload: set hash to `#/profiles` when the archived profile was default or the active route target, then `window.location.reload()`. Otherwise just reload.
- Error path: `window.alert("Archive failed: ...")` (mirrors rename/archive-favorite).

## Requirement checklist

1. Archive button on Profile Management cards only — yes.
2. Removed `archive` from must-not line — yes (`delete` kept).
3. Active-profile query implemented — yes.
4. Last-profile guard — yes (`active.length <= 1`).
5. Replacement-profile selection exactly as planned — yes.
6. Soft archive sets `archived_at = now`, `updated_at = now` (with fallback) — yes.
7. Supabase client write — yes (`window.SupabaseReady`).
8. Write scoped by `id` + `account_id` + `archived_at IS NULL` — yes.
9. `default_chart_record_id` patched only when archived profile is default — yes.
10. Persisted active profile repaired only when it points at archived profile — yes.
11. Reload/navigate exactly as specified — yes.
12. No changes to Account Drawer, `first_profile_intake.js`, backend, repositories, schema, `map_CURRENT.html`, renderer — yes.

## Validation performed

1. Only `app_shell.html` changed for this task. (`first_profile_intake.js` and `supabase_store_bridge.js` appear in git status from earlier sessions; this task did not modify them.)
2. `pm-archive-profile` button rendered only inside `screenProfileList()` card actions — confirmed (grep: 1 button markup + 1 handler).
3. Last-profile guard present — confirmed.
4. Default replacement path present (gated by `wasDefault` + `saveAccountSettingsPatch`) — confirmed.
5. Persisted-profile repair present (gated by `_loadPersistedChartRecord() === profileId`) — confirmed.
6. No child-table writes: handler `.from(...)` targets are `profiles` only (load + archive + fallback). No writes to `birth_records`, `favorite_places`, `saved_searches`, `comparison_sets`, `comparison_set_places`, `current_location_history` — confirmed by static scan of the handler block.
7. Code-path validation: extracted the main inline script and ran `node --check` -> NODE_SYNTAX_OK. Logic-branch presence check -> ALL_PRESENT: true.
8. Destructive live archive smoke NOT run (not explicitly approved). The handler is RLS-scoped (`id` + `account_id`) and guarded; a reversible staging smoke can be run later per the Task 27 plan if approved.

## Scope verification

- Only `app_shell.html` modified by this task.
- No backend, repository, schema, Account Drawer, intake, map, or renderer changes.

VERIFIED
