# Project State and Next Phase

**Date:** 2026-06-13
**Sources:** `PHASE_5_CLOSEOUT.md`, `OWNERSHIP_IMPLEMENTATION_SEQUENCE_v1.md`, `ACCOUNT_WORKSPACE_RLS_PLAN_v1_2026-06-12.md`

---

## 1. Product Status

The product has no working frontend connected to a live backend. No user has ever signed up. No real data exists in either the production or staging database. The backend schema and security model are fully designed and validated on staging; the product is not usable end-to-end yet.

---

## 2. Frontend Status

**Unknown from the three source files.** The source documents contain no frontend inventory. What is confirmed: no frontend wiring was performed in Phases 1–5. The app is not yet connected to the publishable key with a real auth session. Phase 7 is defined as the app cutover point.

---

## 3. Backend Status

The backend schema exists in two states:

**Production (`dpmtmmryvlftfahipowa`):** Original schema only (`2026_06_08_schema_v1.sql`). No `accounts` table, no `account_memberships`, no `account_id` columns on child tables, no RLS policies. Contains smoke-test profile rows that must be deleted before any migration is applied. The Option A cleanup script exists and is ready.

**Staging (`rnwlrdtqhfjhpllryxiz`):** Fully migrated through Phase 5. All tables structured, constrained, and secured. Zero real data rows. Ready for Phase 6.

---

## 4. Supabase Status

| Item | Production | Staging |
|---|---|---|
| Project ref | `dpmtmmryvlftfahipowa` | `rnwlrdtqhfjhpllryxiz` |
| Region | Northeast Asia (Tokyo) | East US (North Virginia) |
| Base schema | Applied | Applied |
| `accounts` + `account_memberships` | **Not applied** | Applied (Phase 1) |
| `account_id` columns on 13 tables | **Not applied** | Applied (Phase 2) |
| Integrity lock (FKs, NOT NULL, triggers) | **Not applied** | Applied (Phase 4) |
| RLS policies | **None** | Applied (Phase 5) — 57 policies |
| `get_shared_chart` RPC | **Not present** | Present, tested |
| Auth providers | Email only (never tested with real user) | Email only (test users created via admin API) |
| Real auth users | 0 | 3 (test fixtures only) |
| Reference data (`places`) | 21 rows | 0 rows (no import run) |

---

## 5. Ownership Model Status

**Locked and implemented on staging. Not applied to production.**

The ownership chain is `auth.users → account_memberships → accounts → profiles → child tables`. Every child table carries a denormalized `account_id NOT NULL` column enforced by a composite FK to its parent. Ownership drift is structurally impossible: the database engine rejects any `(profile_id, account_id)` pair with no matching parent row.

Roles defined in the check constraint: `owner`, `admin`, `member`, `assistant`, `viewer`. Only `owner` is exercised in v1. The `accepted_at IS NOT NULL` requirement on memberships is the access gate — pending invitations grant no access.

The legacy `account_user_id` column remains on `profiles` and `user_settings`. It is not removed until Phase 7 (post-cutover).

---

## 6. RLS Status

**Implemented and validated on staging. Not applied to production.**

- RLS enabled on all 17 `public` tables.
- 57 policies active. All 14 owned tables have 4 policies each (SELECT/INSERT/UPDATE/DELETE).
- `places`: authenticated SELECT only; no write policies.
- `profile_relationships`: RLS enabled, zero policies (default-deny). Unusable until `account_id` is added to it.
- `share_links` public reads: only via `get_shared_chart` RPC — no direct table access for anon.
- All isolation tests passed (13/13) under publishable key + real JWT sessions. Service-role was not used for any authorization assertion.

---

## 7. Auth Status

**Not implemented.** No OAuth providers (Google, Apple) are configured on either project. No signup flow exists. No SECURITY DEFINER signup function has been written. The first membership bootstrap — creating an `accounts` row and `owner` membership atomically for a new user — is Phase 6 work and is not yet done.

The `memberships_insert` RLS policy correctly blocks membership creation under a normal session, which means no user can self-onboard without the Phase 6 signup function.

---

## 8. Notes Status

The `notes` table exists in the schema with columns `profile_id`, `account_id`, `target_type`, `target_id`, `section_key`, `title`, `body`, `archived_at`. RLS is applied: authenticated users in an account can CRUD their notes; viewers cannot write. No frontend, no API endpoint, no UI wired. The table is structurally ready but not usable end-to-end.

---

## 9. Settings Status

The `user_settings` table exists with RLS applied. It supports two row shapes: account-level (`profile_id IS NULL`) and per-profile (`profile_id IS NOT NULL`). Partial unique indexes prevent duplicate rows per shape. No frontend or API endpoint is wired. The `account_user_id` column remains as a legacy field. The table is structurally ready but not usable end-to-end.

---

## 10. Comparison Status

The `comparison_sets` and `comparison_set_places` tables exist with full integrity enforcement: `comparison_sets` has a composite FK to `profiles(id, account_id)` and `comparison_set_places` has a composite FK to `comparison_sets(id, account_id)`, creating a two-level ownership cascade. Both tables have RLS applied. No frontend or API endpoint wired.

---

## 11. Favorites Status

The `favorite_places` and `visited_places` tables exist with `account_id NOT NULL`, composite FK to `profiles(id, account_id)`, and RLS applied (4 policies each). The `places` table is globally readable to authenticated users but has no reference data on staging. No frontend or API endpoint wired.

---

## 12. Frozen Features

The following are **not started** and have no blocking issues from the current schema, but are explicitly outside current phase scope:

- Any frontend page or screen
- Google OAuth / Apple OAuth configuration
- The signup function (SECURITY DEFINER, atomic account + membership creation)
- GeoNames / city search data import into staging
- Notes UI
- Settings UI
- Share page rendering (the RPC exists; the page reading it does not)
- Profile creation flow
- `profile_relationships` (no `account_id`, RLS-locked, unusable)
- `account_user_id` column drop (Phase 7, post-cutover)
- Production migration apply

---

## 13. Known Risks

**Production has not been migrated.** Applying Phases 1–5 to production requires running the Option A cleanup script first (deletes all smoke-test profile rows, keeps `places`). This is destructive and irreversible. It must be executed manually and verified before proceeding.

**No signup flow exists.** Until Phase 6 is complete, no user can authenticate and receive a usable session. The RLS policies are correct but the account bootstrap step is missing, making the app non-functional for real users even after any frontend work.

**`profile_relationships` is blocked.** Any feature depending on profile relationship data cannot be built until `account_id` is added to that table and a policy is applied. This requires another Phase-4-style migration.

**`places` has no data on staging.** Any test involving city search, map display, or comparison picking against staging will return empty results until a GeoNames import is run.

**`account_user_id` creates a dual-column ambiguity.** Both `account_user_id` (legacy) and `account_id` (new) exist on `profiles` and `user_settings`. Any app code that reads `account_user_id` for authorization is bypassing RLS entirely. All app authorization must route through `account_id` and the membership layer.

---

## 14. Recommended Next Phase

**Phase 6: Auth + first real user on staging.**

Three sequential steps, each must pass before the next:

1. **Write the signup function.** A SECURITY DEFINER Postgres function that, given `auth.uid()`, atomically inserts one `accounts` row (`created_by = auth.uid()`) and one `account_memberships` row (`role = 'owner'`, `accepted_at = now()`). Hook as a trigger on `auth.users` INSERT.

2. **Enable at least one OAuth provider** (Google) in the staging Supabase Auth dashboard. Test the signup trigger: sign in, confirm `app_account_ids()` returns one account, confirm the user can INSERT a profile and read it back under the publishable key with no service-role involvement.

3. **After staging passes:** apply the Option A cleanup to production, then apply Phases 1–5 migrations to production in order, then apply Phase 6. Only then is the production database usable by a real user.

Phase 7 (app cutover: wire the frontend to the publishable key; drop `account_user_id`) follows once Phase 6 is confirmed stable on production.
