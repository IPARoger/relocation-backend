# RESULT: 19_FIRST_PROFILE_INTAKE_AUDIT

Task: `19_FIRST_PROFILE_INTAKE_AUDIT`
Mode: read-only audit; documentation output only
Result: **VERIFIED**

## Files inspected

- `first_profile_intake.js`
- `app_shell.html`
- `account_drawer.js`
- `supabase_store_bridge.js`
- `results/18_profile_add_rename_archive_audit.md`

## Answers

1. **What renders:** overlay/card titled `Set up your first chart`, exposed as `window.__showFirstProfileIntake()`.
2. **Fields collected:** display name, birth date, birth time mode (Exact/Unknown), exact birth time when needed, and birth city selected from existing `places` search results.
3. **Writes to Supabase:** yes.
4. **Tables:** inserts `profiles`, inserts `birth_records`, best-effort deletes `profiles` if birth-record insert fails. No updates/upserts found.
5. **Rows created:** creates profile + birth record. Does not create place rows; selects existing place. Does not create current-location rows.
6. **`account_id`:** uses `window.CurrentUser.accountId` for both `profiles.account_id` and `birth_records.account_id`; uses `CurrentUser.userId` for legacy `profiles.account_user_id`.
7. **Refresh after save:** does not refresh app shell in place; redirects to `/map_CURRENT.html?...&chartRecordId=<profileId>`.
8. **Add Profile label honest:** mostly yes; it creates the profile/birth-record pair the shell uses as Profile / Chart Record. Minor copy risk: overlay says `first chart` even when used to add later profiles.
9. **Missing/risky:** no current location setup, no new place creation, two-step non-transactional write with compensating delete, possible orphan profile if cleanup fails, first-only wording, no in-shell refresh.
10. **Smallest safe fix:** copy-only: retitle overlay to `Create profile and chart record` / similar, clarify current location is set separately, and mention birth city must be selected from available places. Implementation hardening can be separate.

## Scope verification

- No production files modified.
- No backend, schema, database, renderer, or map logic changed.
- Full detail written to `audits/19_first_profile_intake_audit.md`.

VERIFIED
