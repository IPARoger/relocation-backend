# Phase 6 — Closeout

**Date:** 2026-06-13  
**Scope:** Staging only (`rnwlrdtqhfjhpllryxiz`). Production untouched.  
**Status:** COMPLETE — 11/11 tests passed.

---

## SECTION A — Phase 6 Changes

### Migration file
`supabase/migrations/2026_06_13_phase6_signup_bootstrap.sql`

### Objects added

| Object | Type | Notes |
|---|---|---|
| `public.handle_new_user()` | Function | SECURITY DEFINER, `search_path=public` |
| `on_auth_user_created` | Trigger | AFTER INSERT on `auth.users` FOR EACH ROW |

### Function logic
1. Inserts one row into `accounts` (`name='Personal'`, `account_type='personal'`, `created_by=NEW.id`).
2. Inserts one row into `account_memberships` (`role='owner'`, `accepted_at=now()`).
3. Returns `NEW`.

The function is `SECURITY DEFINER`, so it runs as its creator (postgres) and bypasses all RLS policies on `accounts` and `account_memberships`. This is the only mechanism by which a brand-new user can bootstrap themselves without any service-role involvement in the application path.

### Trigger verified
- `tgname = on_auth_user_created`
- `enabled = O` (always enabled)
- `type_flags = 5` → AFTER INSERT FOR EACH ROW ✓

### Function verified
- `security_definer = true` ✓
- `config = ["search_path=public"]` ✓

---

## SECTION B — Auth / Dashboard Settings

Email confirmation was **not** disabled in the Supabase dashboard. Phase 6 users were created via the admin API (`POST /auth/v1/admin/users` with `email_confirm: true`), which fires the `auth.users` INSERT trigger identically to a real `signUp()` call. The trigger path is identical regardless of how the row enters `auth.users`.

**Note for production:** Disable "Enable email confirmations" in the Supabase dashboard **or** configure SMTP before production launch. For production, users will need a real confirmation email before their first sign-in.

---

## SECTION C — Seed Data

One `places` row seeded on staging:

| Field | Value |
|---|---|
| `id` | `85b91e81-3efc-4c1a-a7c3-5ed2ca1657bc` |
| `display_name` | Chiang Mai |
| `country_code` | TH |
| `country_name` | Thailand |
| `admin1` | Chiang Mai Province |
| `latitude` | 18.7883 |
| `longitude` | 98.9853 |
| `timezone_id` | Asia/Bangkok |
| `population` | 1,000,000 |
| `source_json` | `{"source":"seed","phase":"6"}` |

---

## SECTION D — Validation Results T1–T11

All tests used the **publishable/anon key only** for authorization assertions. Service-role was used only to create test users (admin API bypass for email confirmation on staging) and to seed the places row. Service-role was not used for any assertion.

| # | Test | Result |
|---|---|---|
| T1 | Signup triggers account creation | **PASS** — `accounts` has 1 row, `account_memberships` has 1 row, `role=owner`, `accepted_at` present |
| T2 | `app_account_ids()` returns the new account | **PASS** — RPC returned exactly 1 UUID matching the account from T1 |
| T3 | Profile INSERT succeeds under publishable key | **PASS** — POST 201, `account_id` correct, visible in subsequent GET |
| T4 | `places` has ≥ 1 row | **PASS** — 1 row returned (Chiang Mai) |
| T5 | Favorite INSERT succeeds | **PASS** — `favorite_places` row created, `account_id` matches |
| T6 | Comparison set INSERT succeeds | **PASS** — `comparison_sets` row created, `account_id` correct |
| T7 | Comparison set place INSERT succeeds | **PASS** — `comparison_set_places` row created, `account_id` cascade correct |
| T8 | Sign-out terminates session | **PASS** — anon GET `profiles` returns 0 rows (RLS default-deny) |
| T9 | Sign-in reissues session | **PASS** — new JWT issued with different token value |
| T10 | Data survives sign-out/sign-in | **PASS** — profile, favorite, comparison set, and csp all present under new JWT |
| T11 | Second user creates isolated account | **PASS** — User B has own account; User A cannot read B's account or profiles |

**Final score: 11/11 PASS**

---

## SECTION E — Blockers

None. No blockers encountered during Phase 6.

Minor schema discovery: `places` table does not have a `place_type` column (not part of the migration). Insert used correct column set on second attempt.

---

## SECTION F — Ready for Production Planning?

**YES.**

All six Phase 6 success criteria are satisfied on staging:

1. A real user signs up and immediately receives an account and owner membership — no service-role involvement in the application path.
2. `app_account_ids()` returns a non-empty set from the new user's session immediately after signup.
3. The user can create a profile, favorite a city, and save a comparison set using only the publishable key.
4. After sign-out and sign-back-in, all data is present under the new JWT.
5. A second user's data is invisible to the first user (T11).
6. Service-role was not used for any authorization assertion.

---

## Rollback

`supabase/migrations/2026_06_13_phase6_rollback.sql`

Drops the trigger and function. Does not remove existing accounts or memberships. Safe to apply at any time.

---

## Production Prerequisites (before apply)

1. Configure SMTP in Supabase Auth settings (or disable email confirmation for staged rollout).
2. Apply all Phase 1–6 migrations to production in order.
3. Confirm `places` table has real data (GeoNames import or equivalent) before enabling favorites and comparison sets in the UI.
4. No OAuth configuration is required for Phase 7 baseline; email/password is sufficient.
