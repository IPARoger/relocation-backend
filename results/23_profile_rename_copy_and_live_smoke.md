# RESULT: 23_PROFILE_RENAME_COPY_AND_LIVE_SMOKE

Task: `23_PROFILE_RENAME_COPY_AND_LIVE_SMOKE`
Mode: implementation (copy) + live validation
Allowed file: `app_shell.html` (only this file changed)
Result: **VERIFIED**

## 1. Copy cleanup (app_shell.html)

Profile Management "Must not appear" note updated so it no longer forbids rename/edit,
while archive/delete remain forbidden:

- Before: `Must not appear: edit form, archive, delete, notes count, saved searches count.`
- After:  `Must not appear: archive, delete, notes count, saved searches count.`

Archive and delete are still listed as forbidden. No archive control was added. Rename handler
logic was left unchanged (see finding below).

## 2. Handler review — no logic change

Task 22's handler filters `profiles` by `id` + `account_id`. During validation I initially
queried the WRONG database (`.env` -> `dpmtmmryvlftfahipowa`), which is a stale schema where
`profiles` has only the legacy `account_user_id` and no `account_id`. That triggered a false
"bug" alarm.

The ACTIVE database is `.env.staging` -> `rnwlrdtqhfjhpllryxiz` (the backend uvicorn process and
every Playwright QA smoke source `.env.staging`; the frontend pulls Supabase config from the
backend `/config/supabase`). On the active DB, `profiles` DOES have `account_id`
(columns: account_id, account_user_id, archived_at, created_at, display_name, id, profile_type,
updated_at). The Task 22 handler is therefore correct against the real schema, consistent with
`supabase_store_bridge.js` and `first_profile_intake.js`. **No handler change made.**

### Side note for the planner (out of scope, not actioned)
The stale `.env` DB (`dpmtmmryvlftfahipowa`) has an older schema (`account_user_id`, no
`account_id`). It is not the active DB, but if anything still points at it, it would break the
frontend's `account_id`-based queries. Flagging only; no action taken.

## 3. Live rename smoke — RUN, PASSED

Performed against the ACTIVE staging DB using the existing QA harness pattern: authenticated as
the owning user via magiclink -> session (RLS enforced), then exercised the EXACT app query
(`profiles.update({display_name}).eq("id", id).eq("account_id", accountId)`).

- Test profile: `DG1` (id `0a409b44-c522-4430-bb5e-0ff80402caee`, account
  `46b0e3f1-f1ae-4550-b9a6-2b2d9c1589b7`) — a test fixture with children, ideal for verifying
  child preservation. Authenticated as `davidleongoodman@gmail.com`.
- Rename applied: `DG1` -> `DG1 (rename smoke)` (`rename_applied: true`).
- `profiles.display_name` changed: confirmed via RLS read.
- Children intact across rename: favorites=2, comparison_sets=1, saved_searches=3,
  birth_records=1 (birth_date `1976-01-13`) — identical before and during rename.
- `birth_records` unchanged: same count and birth_date (no birth write).
- Reverted to original: `DG1` restored (`reverted_ok: true`); revert runs in a `finally` block.
- Children intact after revert: favorites=2, comparison_sets=1, saved_searches=3,
  birth_records=1 — `children_preserved: true`.

Blank-rename rejection is enforced client-side in the handler (trim + reject empty before any DB
call), verified by code inspection; it cannot reach the DB layer, so it was not exercised against
the live DB.

## Validation summary

- Only `app_shell.html` changed for this task (copy line; Task 22's button/handler also present in
  the same uncommitted working tree). No backend, schema, repository, Account Drawer,
  `first_profile_intake.js`, map, or renderer changes.
- Archive/delete copy remains forbidden; edit/rename prohibition removed.
- Live smoke RUN and PASSED: display_name changed, children preserved, birth record unchanged,
  original name restored.

VERIFIED
