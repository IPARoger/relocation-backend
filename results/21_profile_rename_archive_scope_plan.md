# RESULT: 21_PROFILE_RENAME_ARCHIVE_SCOPE_PLAN

Task: `21_PROFILE_RENAME_ARCHIVE_SCOPE_PLAN`
Mode: read-only planning; documentation output only
Result: **VERIFIED**

## Answers

1. **Backend/repository rename support:** exists. `PATCH /profiles/{profile_id}` calls `update_profile(...)`, which updates `profiles.display_name`, `profile_type`, and `updated_at`.
2. **Backend/repository archive support:** exists. `POST /profiles/{profile_id}/archive` calls `archive_profile(...)`, which sets `profiles.archived_at` and `updated_at`.
3. **Frontend surfaces:** first expose Rename/Archive only on Profile Management cards. Account Drawer and Chart Record page can come later; avoid archive in drawer for MVP.
4. **If default profile is archived:** choose a remaining active profile as replacement, patch account-level `default_chart_record_id`, update persisted local active profile if needed, and navigate/reload onto the replacement. Block archiving the last active profile.
5. **Child objects preserved:** birth records, favorites, saved searches/investigations, comparison sets/places, current location history, visited places, notes, share links, and profile-scoped settings. Archive should soft-hide parent only; no cascade delete.
6. **Rejected for MVP:** hard delete, cascade delete, unarchive UI, bulk archive, archive last profile, archive from account drawer, edit birth facts, profile merge/split, backend route use without ownership hardening.
7. **Smallest sequence:** Phase A rename only via RLS-scoped Supabase update from Profile Management; Phase B archive with guardrails/default replacement/child preservation; Phase C backend auth hardening if backend routes are used.

## Key caution

The backend routes exist but currently use service-role-style repository functions and do not show caller ownership checks in the inspected code. For the first frontend MVP, direct Supabase client writes with `id` + `account_id` filters are safer unless backend ownership checks are added first.

## Scope verification

- No production files modified.
- No backend, schema, database, renderer, or map logic changed.
- Full detail written to `audits/21_profile_rename_archive_scope_plan.md`.

VERIFIED
