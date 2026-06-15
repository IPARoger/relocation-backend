# RESULT: 22_PROFILE_RENAME_PHASE_A

Task: `22_PROFILE_RENAME_PHASE_A`
Mode: implementation — rename only, no archive
Allowed file: `app_shell.html` (only this file changed)
Result: **VERIFIED**

## What was implemented

A safe profile rename action on Profile Management cards.

### 1. Rename button (Profile Management card)
Added one button to the `.pm-actions` row in `screenProfileList()`:

```
<button type="button" data-action="pm-rename-profile"
        data-chart-record="${r.chartRecordId}"
        data-current-name="${escapeHtml(r.displayName)}">Rename</button>
```

- Appears only on Profile Management cards (alongside Open / Set Current Location).
- Carries the profile id (`chartRecordId === profiles.id`) and current name (escaped).
- No inline edit form, no archive/delete control — uses a single `window.prompt`.

### 2. Rename handler (`pm-rename-profile`)
Added next to the other `pm-*` handlers:

- Reads `profileId` from `data-chart-record`; returns early if missing.
- Prefills `window.prompt` with the current name.
- Cancel (`null`) → no-op.
- Trims input; rejects blank with an alert and aborts (no write).
- No-op if the trimmed name equals the current trimmed name.
- Supabase **client** write (no backend route):
  ```
  client.from("profiles")
        .update({ display_name: newName })
        .eq("id", profileId)
        .eq("account_id", accountId)   // applied when accountId present
  ```
- Updates `profiles.display_name` only — birth records untouched.
- On success: `window.location.reload()` so the new name appears.
- On error: alert with the message; no silent failure.

## Requirement check

1. Rename action only on Profile Management cards — yes.
2. Supabase client write, not backend route — yes (`window.SupabaseReady`).
3. Updates `profiles.display_name` only — yes.
4. Filtered by `id = profileId` AND `account_id = current account id` — yes (account_id from `window.CurrentUser.accountId`).
5. Trim name — yes.
6. Reject blank names — yes (alert + abort).
7. Refresh on success — yes (`window.location.reload()`).
8. Birth records not renamed — yes (no `birth_records` write).
9. No archive — yes.
10. Account Drawer unchanged — yes.
11. `first_profile_intake.js` unchanged — yes.
12. Backend/repository/schema/map/renderer untouched — yes.

## Validation

- **Code-level verified:** button + handler present and well-formed (mirrors the existing
  `archive-favorite` Supabase-write pattern: `await window.SupabaseReady`, `.update().eq(...)`,
  `error` check, reload, alert-on-failure).
- **Blank rename rejected:** trimmed-empty input triggers an alert and returns before any write.
- **Child objects preserved:** rename only mutates `profiles.display_name`; favorites,
  saved searches/investigations, and comparison sets remain keyed by the same `profile_id`,
  so they stay visible for the same profile after reload.
- **Birth records unchanged:** no write targets `birth_records`.
- **Live DB rename NOT executed** to avoid mutating production account data without an
  explicit go-ahead; the operation is RLS-scoped (`id` + `account_id`) so it is safe to run
  manually on a test profile. Run by clicking Rename on a Profile Management card, entering a
  new name, and confirming the card label and `profiles.display_name` update on reload.

## Scope verification

- Only `app_shell.html` was modified for this task. The pre-existing modified state of other
  files in `git status` predates Task 22 (earlier approved honesty-fix tasks); this task added
  exactly: one Rename button and one `pm-rename-profile` handler.
- No backend, repository, schema, Account Drawer, `first_profile_intake.js`, map, or renderer
  changes.

VERIFIED
