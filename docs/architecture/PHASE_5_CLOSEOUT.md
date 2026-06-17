# Phase 5 Closeout

**Date:** 2026-06-13
**Scope:** Staging only (`rnwlrdtqhfjhpllryxiz`). Production untouched.
**Sources:** Phases 1–5 migration files only.

---

## 1. Scope

Phases 1–5 applied sequentially to a clean staging Supabase project. Production database has not been modified. No auth configuration, no frontend work, no settings wiring performed.

---

## 2. Objects Added

| Phase | File | Objects |
|---|---|---|
| 1 | `2026_06_13_phase1_accounts_memberships.sql` | Tables: `accounts`, `account_memberships`. Indexes: `idx_memberships_user`, `idx_memberships_account`. Functions: `app_account_ids()`, `app_has_account_role()` (both SECURITY DEFINER, `search_path` pinned). |
| 2 | `2026_06_13_phase2_account_id_columns.sql` | Column `account_id uuid NULL REFERENCES accounts(id)` added to 13 tables. 13 indexes on `account_id`. |
| 4 | `2026_06_13_phase4_integrity_lock.sql` | UNIQUE constraints on `profiles(id,account_id)` and `comparison_sets(id,account_id)`. NOT NULL on all 13 `account_id` columns. 13 composite FKs (all validated). Trigger function `app_set_account_from_parent()` + 12 BEFORE INSERT/UPDATE triggers. Partial unique indexes on `user_settings`. `share_links.visibility` default changed to `private`; check constraint added. |
| 5 | `2026_06_13_phase5_rls_policies.sql` | RLS enabled on 17 tables. 57 policies (4 per 14 owned tables + account/membership backbone + 1 on `places`). Function `get_shared_chart(text)` SECURITY DEFINER, granted to `anon` + `authenticated`. |

**Phase 3** was a no-op on staging (clean start, zero rows to backfill).

---

## 3. Ownership Architecture

```
auth.users
  └─ account_memberships (user_id, account_id, role, accepted_at)
       └─ accounts (id, account_type)
            └─ profiles (id, account_id NOT NULL)
                 └─ 10 profile-owned child tables (account_id NOT NULL, composite FK)
                      └─ comparison_set_places (account_id NOT NULL, composite FK → comparison_sets)
            └─ user_settings (account_id NOT NULL; profile_id nullable — MATCH SIMPLE)
```

`app_account_ids()` resolves `auth.uid()` → accepted, non-archived memberships → set of `account_id`. All RLS predicates reduce to `account_id IN (SELECT app_account_ids())` for reads and `app_has_account_role(account_id, roles[])` for writes.

---

## 4. Integrity Lock Summary

Enforced by Phase 4:

- **Drift impossible:** composite FK `(profile_id, account_id) → profiles(id, account_id) ON UPDATE CASCADE` on all 10 profile-owned children. A mismatched pair has no referent and is rejected by the engine.
- **Two-level cascade:** `profiles.account_id` update cascades to its 10 children; `comparison_sets.account_id` update cascades to `comparison_set_places`.
- **Trigger ergonomics:** `app_set_account_from_parent()` fills `account_id` on INSERT/UPDATE from parent when null. The FK is the correctness guarantee; the trigger is convenience.
- **`user_settings`:** per-profile rows use composite FK with MATCH SIMPLE (null `profile_id` not enforced). Account-level rows use plain `account_id → accounts(id) ON DELETE CASCADE`.
- **Validated:** all 13 composite FKs carry `convalidated = true`.

---

## 5. RLS Summary

- RLS enabled on all 17 `public` tables.
- `profile_relationships`: RLS enabled, zero policies (default-deny; no `account_id` column — deferred).
- `places`: one SELECT policy, `authenticated` only, `USING true`. No write policies; ingestion requires service-role.
- All 14 owned tables: 4 policies each (SELECT/INSERT/UPDATE/DELETE). UPDATE carries both USING and WITH CHECK to block row moves between accounts.
- Role hierarchy enforced by policy: viewer = SELECT only; assistant = CRUD but not share; owner/admin = manage memberships.
- `share_links` public reads: no anon table policy. Only path is `get_shared_chart(slug)` SECURITY DEFINER RPC, which enforces `visibility ≠ private`, `revoked_at IS NULL`, and `expires_at` before returning a whitelisted JSON payload.

---

## 6. Validation Results

All tests run under publishable key + JWT session. Service-role used for fixture setup only, never for authorization assertions.

**Isolation (13/13 PASS):**
- A sees only A's rows; B sees only B's rows.
- A querying B's ids by primary key returns 0 rows.
- A UPDATE/DELETE on B's rows: 0 rows affected.
- A INSERT with `account_id = B`: HTTP 403, SQLSTATE 42501.
- A UPDATE own row to `account_id = B`: HTTP 403, SQLSTATE 42501.
- `app_account_ids()` returns only the caller's account ids.
- Unauthenticated session returns 0 rows from all tables.

**Role gating (3/3 PASS):**
- Viewer C (accepted membership in Account A) can SELECT A's profiles.
- Viewer C INSERT into Account A: HTTP 403.
- Viewer C UPDATE A's profile: 0 rows affected.
- Owner A INSERT/UPDATE/DELETE own data: all succeed.

**Share RPC (9/9 PASS):**
- Private slug → null. Revoked → null. Expired → null. Unknown → null.
- Valid unlisted slug → payload with correct fields.
- `hide_birth_data = true` → `birth_data_visible: false` in payload.
- `hide_birth_data = false` → `birth_data_visible: true`.
- Anon direct SELECT on `share_links` → 0 rows.

**Schema lint (17/17 PASS):** RLS enabled, correct policy count on every table.

---

## 7. Known Limitations

- **`profile_relationships` is unusable** under the publishable key (RLS on, no policies, no `account_id`). Not a regression; it was unusable before. Requires a Phase-4-style `account_id` add before it can be policy'd.
- **`places` has no reference data** on staging. The SELECT policy is correct; 0 rows returned because no GeoNames import has run against the staging project.
- **`places` is not readable anonymously.** Share pages that need to render a map for a logged-out visitor must go through the `get_shared_chart` RPC (which can read `places` as definer) or require a future anon policy decision.
- **First membership bootstrap** is not wired. Creating an account and owner membership atomically requires a SECURITY DEFINER signup function (Phase 6 scope). The `memberships_insert` policy correctly blocks this under a normal session.
- **`account_user_id`** column remains on `profiles` and `user_settings`. It is a pre-existing column from the original schema, not removed in this phase. Drop is a Phase 7 task post-cutover.

---

## 8. Rollback References

| Phase | Rollback file / action |
|---|---|
| 5 | `supabase/migrations/2026_06_13_phase5_rollback.sql` — drops all policies + RPC in dependency order; RLS stays enabled (tables return to default-deny). |
| 4 | Drop triggers → composite FKs → NOT NULL → UNIQUE constraints (exact 9-step order in spec §8). |
| 2 | Drop 13 `account_id` indexes; drop 13 `account_id` columns. |
| 1 | Drop `app_has_account_role`, `app_account_ids`; drop `account_memberships`; drop `accounts`. |

No rollback touches data (phases 1, 2, 5). Phase 4 rollback is constraint-only. Phase 3 rollback is NULL-setting; not applicable on staging (no rows existed).

---

## 9. Production Status

**Production database (`dpmtmmryvlftfahipowa`) is unmodified.** No migration has been applied to it. It retains its original schema from `2026_06_08_schema_v1.sql` with no `accounts`, `account_memberships`, `account_id` columns, or RLS policies. Before production apply, the Option A cleanup script (`2026_06_13_phase0_option_a_cleanup.sql`) must be run first to clear smoke-test profile rows.

---

## 10. Recommended Next Phase

**Phase 6: Auth + first real user.**

Minimum work required:
1. Enable Google OAuth (and/or Apple) in the Supabase Auth dashboard for the staging project.
2. Write a SECURITY DEFINER signup function that atomically creates an `accounts` row and an `owner` membership with `accepted_at = now()` for the new `auth.uid()`.
3. Hook that function as a trigger on `auth.users` INSERT or call it from the app's post-signup handler.
4. Sign up a real user, confirm `app_account_ids()` returns their account, confirm they can INSERT a profile and read it back under the publishable key.
5. Only after that test passes on staging: apply Phases 1–5 to production (after running the Option A cleanup), then apply Phase 6.
