# RESULT: 31_PRE_COMMIT_COPY_FIX_ARCHIVE_RESTORE

Task: `31_PRE_COMMIT_COPY_FIX_ARCHIVE_RESTORE`
Mode: implementation (tiny copy fix)
Allowed file: `app_shell.html` (only file changed)
Source: `results/30_account_management_checkpoint_audit.md`
Result: **VERIFIED**

## Change

In the `pm-archive-profile` confirmation message, replaced the clause that implied a
self-serve unarchive UI:

- Before: `You can restore it later from the database.`
- After:  `Archived profiles are hidden, not deleted.`

Only the confirmation copy string changed. No logic touched.

## Validation

1. Old phrase gone — confirmed (grep count = 0 for "You can restore it later from the database").
2. New phrase exists — confirmed at line 2234 ("Archived profiles are hidden, not deleted.").
3. `pm-archive-profile` handler still exists — confirmed at line 2196.
4. Only `app_shell.html` changed by this task — confirmed. (`first_profile_intake.js`,
   `main_centerline_FIXER.py`, and untracked `supabase_store_bridge.js` predate this task and
   were not modified here.)
5. Live archive smoke NOT run (per task rule).

## Rules compliance

- Archive logic unchanged.
- Supabase writes unchanged.
- Rename logic unchanged.
- `first_profile_intake.js` untouched.
- Backend/repositories/schema/map/renderer untouched.
- Only `app_shell.html` modified.

VERIFIED
