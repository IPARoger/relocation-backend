# Production Cutover Plan

**Date:** 2026-06-13  
**Status:** Planning only. No execution. No SQL. Production untouched.  
**Author source:** PHASE_6_CLOSEOUT.md + PROJECT_STATE_AND_NEXT_PHASE.md  

---

## Overview

The staging project (`rnwlrdtqhfjhpllryxiz`) has passed all Phase 1–6 validation gates including 11/11 real-user tests. The production project (`dpmtmmryvlftfahipowa`, Tokyo) remains on the original schema with zero RLS, zero ownership layer, and zero auth wiring. This document defines the minimum required sequence to bring production to parity with staging.

**Production ref:** `dpmtmmryvlftfahipowa`  
**Staging ref:** `rnwlrdtqhfjhpllryxiz`  
**Migrations to apply:** Phases 1, 2, 3 (audit), 4, 5, 6 — in order.  
**Irreversible steps:** Option A cleanup (deletes smoke-test rows), NOT NULL constraints, composite FK locks.

---

## 1. Preconditions

All of the following must be true before any production command is issued.

### 1a. Staging has passed Phase 6

- Staging Phase 6 closeout confirmed: 11/11 tests PASS.
- `handle_new_user()` and `on_auth_user_created` verified SECURITY DEFINER with pinned `search_path`.
- All 57 RLS policies validated. No regressions.
- Status: **MET** as of 2026-06-13.

### 1b. Full database backup exists

- A point-in-time backup of the production database must be confirmed available in the Supabase dashboard under **Project Settings → Database → Backups** before any destructive step is taken.
- Supabase Pro/Team plans retain daily backups; confirm the most recent backup timestamp is within 24 hours of cutover start.
- If manual backup is required: export via Supabase dashboard (SQL dump) and store off-platform before proceeding.

### 1c. Production row audit is current

The known production state (from prior audit):
- `places`: 21 rows — **must be preserved through all steps.**
- `profiles`: has smoke-test rows tied to orphaned `account_user_id` values — **must be deleted before Phase 1.**
- `accounts`: table does not yet exist.
- All other carrying tables (birth_records, favorite_places, etc.): assumed empty. **Verify before executing Option A.**
- `auth.users`: 0 confirmed real users.

Before executing Option A, re-run the audit queries (not listed here; documented in the original Option A script) and confirm:
- `profiles` row count, and that all profile rows are smoke-test only (no real user data).
- All other 12 carrying tables have 0 rows.
- `places` has 21 rows.

If any carrying table other than `places` contains unexpected rows, stop. Do not proceed. Investigate before Option A.

### 1d. CLI is authenticated and linked to production

- Confirm `supabase projects list` shows `dpmtmmryvlftfahipowa`.
- Confirm the CLI is **linked to production**, not staging.
- Double-check with `supabase db query` targeting the production ref: `select current_database()` returns `postgres`, and a count of `places` returns 21.
- Do not proceed if there is any ambiguity about which project is linked.

### 1e. A maintenance window is scheduled

Production has 0 real users today, so there is no downtime risk to actual users. However:
- Choose a low-activity period as a precaution.
- Do not execute the cutover while actively testing other features or running other Supabase CLI operations.
- Estimated wall-clock time: 45–90 minutes including verification pauses.

### 1f. The Option A cleanup script is ready

The Option A cleanup script was prepared during Phase 0 planning. Confirm it:
- Deletes all rows from `profiles` (and cascading child tables, if any).
- Does **not** touch `places`.
- Does **not** drop any tables or columns.
- Is idempotent (safe to run twice if interrupted).

If the script has not been written yet, it must be written and reviewed before cutover begins. It is a prerequisite, not part of the migration sequence.

---

## 2. Option A Cleanup Sequence

This is the only irreversible destructive step. Execute it before any migration is applied.

**Purpose:** Remove all smoke-test data from production so that Phase 4's NOT NULL and composite FK constraints can be applied to a clean slate. The production `places` table is explicitly excluded.

**Order of operations:**

1. Run the pre-cleanup row audit. Capture exact row counts for every carrying table. Record them.
2. Confirm: `places` count = 21. If not 21, stop.
3. Confirm: all profile-linked tables (birth_records, intention_profiles, current_location_history, location_events, favorite_places, visited_places, saved_searches, comparison_sets, notes, share_links, user_settings) count = 0. If any are non-zero, stop and investigate.
4. Execute the Option A cleanup: delete all rows from `profiles`. (Child tables should already be empty per step 3.)
5. Re-run the audit. Confirm:
   - `profiles` count = 0.
   - `places` count = 21.
   - All other carrying tables count = 0.
6. If any count is unexpected, stop before proceeding to Phase 1.

**What is not deleted:**
- `places` — preserved throughout.
- Any tables that do not exist yet (`accounts`, `account_memberships`) — they do not exist in production at this point.

---

## 3. Migration Order

Apply migrations in the exact order listed. Do not skip phases. Do not combine phases into a single operation.

Each phase must be applied individually and validated before the next phase begins. The migration files are in `supabase/migrations/`.

| Step | File | Phase | What it does |
|---|---|---|---|
| M1 | `2026_06_13_phase1_accounts_memberships.sql` | Phase 1 | Creates `accounts`, `account_memberships` tables and `app_account_ids()`, `app_has_account_role()` SECURITY DEFINER functions |
| M2 | `2026_06_13_phase2_account_id_columns.sql` | Phase 2 | Adds nullable `account_id uuid` columns and indexes to all 13 carrying tables |
| M3 | `2026_06_13_phase3_backfill_audit.sql` | Phase 3 | Read-only audit: confirms zero rows need backfill (production should be clean after Option A) |
| M4 | `2026_06_13_phase4_integrity_lock.sql` | Phase 4 | NOT NULL on all 13 `account_id` columns; UNIQUE constraints; composite FKs with ON UPDATE CASCADE; `app_set_account_from_parent()` trigger function and 13 triggers; `user_settings` partial unique indexes; `share_links` visibility default and check |
| M5 | `2026_06_13_phase5_rls_policies.sql` | Phase 5 | Enables RLS on all 17 tables; creates 57 RLS policies; creates `get_shared_chart()` SECURITY DEFINER RPC |
| M6 | `2026_06_13_phase6_signup_bootstrap.sql` | Phase 6 | Creates `handle_new_user()` SECURITY DEFINER function and `on_auth_user_created` trigger on `auth.users` |

**Do not apply Phase 4 before verifying Phase 3 audit results.** Phase 3 is a no-op if the database is clean, but it is the gate that confirms you are not locking non-null constraints onto rows that have null `account_id` values. If Phase 3 returns any non-zero backfill count, stop before Phase 4 and investigate.

---

## 4. Validation Checkpoints

A checkpoint must pass before the next migration is applied. None of these require executing application code — they are database-level probes only.

### Checkpoint 1 — After Option A (before any migration)

- `places` count = 21.
- `profiles` count = 0.
- All other 12 carrying tables count = 0.
- No `accounts` table exists yet.

### Checkpoint 2 — After M1 (Phase 1)

- `accounts` table exists with columns: `id`, `name`, `account_type`, `created_by`, `created_at`.
- `account_memberships` table exists with columns: `account_id`, `user_id`, `role`, `accepted_at`, etc.
- `app_account_ids()` function exists in `public` schema, is SECURITY DEFINER.
- `app_has_account_role()` function exists in `public` schema, is SECURITY DEFINER.
- Both tables have 0 rows.

### Checkpoint 3 — After M2 (Phase 2)

- All 13 carrying tables have an `account_id uuid` column with `is_nullable = YES`.
- All 13 tables have an index on `account_id`.
- All `account_id` values across all 13 tables are NULL (since all rows were deleted in Option A).

### Checkpoint 4 — After M3 (Phase 3)

- Phase 3 audit output: `total_rows = 0` for every carrying table.
- `assigned = 0` for every carrying table.
- No rows require backfill. If any non-zero count appears, stop.

### Checkpoint 5 — After M4 (Phase 4)

- All 13 `account_id` columns report `is_nullable = NO`.
- UNIQUE constraints exist on `profiles(id, account_id)` and `comparison_sets(id, account_id)`.
- Composite FKs exist: at minimum confirm `birth_records`, `favorite_places`, `comparison_set_places` each have a composite FK referencing their parent with ON UPDATE CASCADE.
- `app_set_account_from_parent()` trigger function exists.
- 13 triggers named `trg_*_set_account` exist (one per carrying child table).
- Partial unique indexes exist on `user_settings`.
- `share_links.visibility` default is `'private'` and has a check constraint.

### Checkpoint 6 — After M5 (Phase 5)

- `pg_policies` has exactly 57 rows for the `public` schema.
- RLS is enabled (`relrowsecurity = true`) on all 17 tables.
- `get_shared_chart()` function exists in `public` schema, is SECURITY DEFINER.
- Spot-check: `places` has an authenticated SELECT policy but no INSERT/UPDATE/DELETE policies.
- Spot-check: `accounts` has all 4 CRUD policies.

### Checkpoint 7 — After M6 (Phase 6) — the production smoke test

This is the only checkpoint that involves creating a real auth user. Execute once, then clean up.

1. Create one production smoke-test user via the admin API (service-role) with `email_confirm: true`.
2. Sign in as that user to obtain a JWT (using the production publishable key).
3. Confirm via the user's own session (not service-role):
   - `SELECT * FROM accounts` returns exactly 1 row with `created_by` = the new user's `auth.uid()`.
   - `SELECT * FROM account_memberships` returns exactly 1 row with `role = 'owner'` and `accepted_at IS NOT NULL`.
   - `SELECT app_account_ids()` returns the account id.
4. Delete the smoke-test user via the admin API (service-role cleanup).
5. Confirm `accounts` and `account_memberships` counts return to 0 — or, if the membership/account was not cascade-deleted, delete them explicitly via service-role.

If any of steps 1–3 fail, roll back Phase 6 immediately using the rollback file before investigating.

---

## 5. Rollback Points

Each phase has an independent rollback file. Rollbacks must be applied in reverse order if multiple phases need to be unwound.

| After applying | Rollback file | What it does | Reversible? |
|---|---|---|---|
| M6 | `2026_06_13_phase6_rollback.sql` | Drops trigger + function. Leaves accounts/memberships intact. | Yes |
| M5 | `2026_06_13_phase5_rollback.sql` | Drops all 57 RLS policies and `get_shared_chart()`. Keeps RLS enabled. | Yes |
| M4 | No automated rollback written yet. | Would require dropping triggers, composite FKs, UNIQUE constraints, and reverting NOT NULL — all in the correct order. | Complex; prepare before cutover. |
| M3 | N/A (read-only audit; no objects created) | No action needed. | N/A |
| M2 | Drop all `account_id` columns and indexes added in Phase 2. | Straightforward but requires a separate script. | Yes |
| M1 | Drop `accounts`, `account_memberships`, `app_account_ids()`, `app_has_account_role()`. | Must be done after M2 rollback if M2 was applied. | Yes |

**Phase 4 rollback note:** A Phase 4 rollback script was not generated during staging implementation. Before production cutover, this script must be written and reviewed. It is a blocking prerequisite. Without it, applying Phase 4 to production means any failure after that point cannot be mechanically reversed without manual intervention.

**Golden rule:** If any checkpoint fails, do not proceed to the next phase. Roll back the current phase, investigate the failure, fix it on staging first, then re-validate before re-applying to production.

---

## 6. Production Auth Configuration

These are manual steps in the Supabase dashboard for the production project (`dpmtmmryvlftfahipowa`). They cannot be done via SQL migration.

### 6a. SMTP configuration (required before launch)

Email/password signup is the minimum for launch. Supabase's built-in email sender is rate-limited and not suitable for production volume.

Required: configure an external SMTP provider under **Authentication → Email → SMTP Settings**.

Recommended providers: Resend, Postmark, SendGrid. Any transactional email provider with SPF/DKIM configured for the sending domain works.

Configuration fields required:
- SMTP Host
- SMTP Port (587 or 465)
- SMTP User
- SMTP Password
- Sender email address (must be verified on the provider)
- Sender name

**Do not disable email confirmation in production.** Email confirmation is a security control. Users must confirm their email before their first session is issued. This is the correct production behavior.

### 6b. Auth email templates (optional but recommended)

Supabase provides default confirmation and password-reset email templates. Customize them under **Authentication → Email Templates** to match the product's brand before launch. This is cosmetic, not a security requirement.

### 6c. JWT expiry

Default Supabase JWT expiry is 1 hour with a 1-week refresh window. These defaults are acceptable for v1. Review after the first real user cohort if session management issues arise.

### 6d. OAuth providers

No OAuth provider (Google, Apple) is required for Phase 6 or the production cutover. Email/password is sufficient. OAuth can be added post-launch without any database migration.

### 6e. Rate limiting

Supabase's built-in auth rate limits (signup attempts per IP, OTP requests, etc.) are enabled by default. Do not disable them in production.

---

## 7. Places Data Requirements

The production database currently has 21 `places` rows. This data must be preserved through all migration steps.

**Phase 3 is the risk point.** Phase 3's audit script checks `places` row counts as part of the audit. It does not delete anything, but the Phase 4 migration does nothing to `places` (the `places` table does not carry `account_id` — it is a global reference table). Confirm this before Phase 4 by re-reading the Phase 4 migration file.

**21 rows is not enough for a real launch.** The application's city search and comparison features require meaningful reference data. For an initial launch, the minimum acceptable corpus depends on the initial user geography. The recommended approach:

- **GeoNames cities15000.txt** — covers all cities with population > 15,000 worldwide (~24,000 rows). This is the production-quality minimum.
- The import must be run against production as a **separate step after all Phase 1–6 migrations have been applied and validated.** It is not part of the migration sequence.
- The import uses the service-role key and a batch insert script. It has no dependency on auth or RLS (the places table has no RLS write policies; service-role bypasses RLS entirely).
- After import, verify with an authenticated GET via the publishable key that `places?display_name=ilike.*Tokyo*` returns at least one result.

**The 21 existing production rows are valid.** Option A cleanup does not touch `places`. All Phase 1–6 migrations do not alter the `places` table schema or delete any `places` rows.

---

## 8. Go / No-Go Checklist

Complete this checklist immediately before issuing any production command. Every item must be YES.

### Database readiness

- [ ] Point-in-time backup confirmed available within 24 hours of cutover start.
- [ ] Pre-Option-A audit run and results recorded (row counts for all 13 carrying tables).
- [ ] `profiles` count confirmed as smoke-test only (no real user data).
- [ ] `places` count confirmed = 21.
- [ ] Option A cleanup script reviewed, approved, and ready.
- [ ] Phase 4 rollback script written and reviewed (this was not generated during staging — must be done before cutover).
- [ ] CLI authenticated and linked to production (`dpmtmmryvlftfahipowa`), not staging.

### Staging sign-off

- [ ] All 6 Phase 1–6 migrations were applied to staging in order with no modifications.
- [ ] Phase 6 closeout confirmed: 11/11 tests PASS.
- [ ] Staging has been running stable for at least 24 hours after Phase 6 was applied (no unexpected errors observed).

### Auth readiness

- [ ] SMTP provider selected, credentials obtained, and ready to configure.
- [ ] Sending domain has SPF and DKIM records configured (or in progress).
- [ ] Production publishable key confirmed for use in application.
- [ ] Production service-role key stored securely (not in any code repository or frontend).

### Places data readiness

- [ ] Decision made: use the 21 existing rows for soft launch, or run GeoNames import before launch.
- [ ] If GeoNames import: import script is ready and tested against staging before production import.

### Application readiness

- [ ] Frontend is not yet connected to the production publishable key (no real users are making requests to production during the cutover window).
- [ ] The application-level `account_user_id` field usage has been audited. Any code path that reads `account_user_id` for authorization instead of routing through `account_id` and the membership layer must be identified before cutover. (Phase 7 drops the column; Phase 6 cutover does not require the drop, but the code must not rely on it for auth logic.)

### Rollback readiness

- [ ] Phase 5 rollback file confirmed present: `supabase/migrations/2026_06_13_phase5_rollback.sql`.
- [ ] Phase 6 rollback file confirmed present: `supabase/migrations/2026_06_13_phase6_rollback.sql`.
- [ ] Phase 4 rollback script written and present.
- [ ] Responsible engineer is available and not multitasking during the cutover window.

---

## Execution Order (summary)

```
[STOP] Confirm all Go / No-Go items are YES
  ↓
[STEP 1] Run pre-Option-A row audit. Record results.
  ↓
[STEP 2] Execute Option A cleanup (delete smoke-test profiles). Verify Checkpoint 1.
  ↓
[STEP 3] Apply M1 (Phase 1). Verify Checkpoint 2.
  ↓
[STEP 4] Apply M2 (Phase 2). Verify Checkpoint 3.
  ↓
[STEP 5] Apply M3 (Phase 3 audit). Verify Checkpoint 4. If any non-zero backfill count → STOP.
  ↓
[STEP 6] Apply M4 (Phase 4). Verify Checkpoint 5.
  ↓
[STEP 7] Apply M5 (Phase 5). Verify Checkpoint 6.
  ↓
[STEP 8] Apply M6 (Phase 6). Verify Checkpoint 7 (production smoke test). Clean up smoke-test user.
  ↓
[STEP 9] Configure SMTP in Supabase Auth dashboard.
  ↓
[STEP 10] (Optional) Run GeoNames places import if decided in Go/No-Go.
  ↓
[COMPLETE] Production is on parity with staging. Phase 7 (app cutover) may begin.
```

---

## What Is Not In Scope for This Cutover

The following are explicitly deferred to Phase 7 or later:

- Dropping the `account_user_id` column from `profiles` and `user_settings`.
- Wiring the frontend application to the production publishable key.
- Configuring Google or Apple OAuth providers.
- Adding `account_id` to `profile_relationships` and writing its RLS policies.
- Notes UI.
- Settings UI.
- Share page rendering.
- Any chart, map, or astrological calculation feature.
