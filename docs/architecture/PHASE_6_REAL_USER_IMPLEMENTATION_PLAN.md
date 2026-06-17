# Phase 6 — Real User Implementation Plan

**Date:** 2026-06-13
**Scope:** Staging only (`rnwlrdtqhfjhpllryxiz`). Production untouched until staging passes.
**Goal:** Prove one real user can sign up, create a profile, favorite a city, save a comparison set, log out, log back in, and recover all data — using only the publishable key.

---

## Preconditions (already true on staging)

- Phases 1–5 applied and validated.
- 57 RLS policies active. All isolation tests passed.
- `app_account_ids()` and `app_has_account_role()` deployed.
- `favorite_places`, `comparison_sets`, `comparison_set_places` tables exist with `account_id NOT NULL` and composite FKs.
- `places` table has no reference data on staging — one city row must be seeded before favorites and comparison tests can run.
- No OAuth providers configured. No signup function exists. Email auth is available but untested with a real user.

---

## 1. Required Supabase Auth Configuration

**Staging dashboard — two changes required before any other Phase 6 work:**

**1a. Email signup confirmation.**
By default, Supabase requires email confirmation before a session is issued. For staging, disable the "Enable email confirmations" setting under Authentication → Email. This allows immediate session issuance on signup without a working email server. Re-enable for production.

**1b. Auth provider decision.**
Choose exactly one for Phase 6:
- **Email/password** — no dashboard configuration beyond 1a. Sufficient to prove the full workflow. Requires no OAuth app registration.
- **Google OAuth** — requires a Google Cloud OAuth 2.0 client ID and secret registered under Authentication → Providers → Google. Requires a redirect URL allow-list entry for the staging frontend origin.

Either is sufficient. Email/password is the minimum path. Google OAuth can be added in parallel or after.

No Apple configuration is required for Phase 6.

---

## 2. Required Signup Bootstrap Function

**The problem:** The `memberships_insert` RLS policy requires the caller to already hold `owner` or `admin` role in the target account before inserting a membership. A brand-new user has no memberships, so no normal session can bootstrap itself. This must be solved with a SECURITY DEFINER function that runs with elevated privileges.

**One new database function required:**

`handle_new_user()` — SECURITY DEFINER, `search_path` pinned to `public`.

**Logic (in order, atomic):**
1. Insert one row into `accounts` with `name = 'Personal'` (or derived from user email), `account_type = 'personal'`, `created_by = NEW.id` (the new `auth.users.id`).
2. Insert one row into `account_memberships` with `account_id` = the id from step 1, `user_id = NEW.id`, `role = 'owner'`, `accepted_at = now()`.
3. Return `NEW`.

**Hook:** A Postgres trigger on `auth.users` AFTER INSERT, calling `handle_new_user()` FOR EACH ROW.

**Result after signup:** every new `auth.uid()` automatically has one account and one accepted owner membership, so `app_account_ids()` immediately returns a non-empty set and all write policies resolve.

**No other bootstrap logic is needed for Phase 6.** Profile creation, favorites, and comparison sets are all performed by the user through normal RLS-authorized writes after the account exists.

---

## 3. Required Frontend Changes

Phase 6 requires the minimum frontend surface to drive the nine-step workflow. No new pages beyond what is needed to prove the workflow.

**3a. Auth screens — two views:**
- Sign-up form: email + password fields, submit calls Supabase `signUp()` with the publishable key.
- Sign-in form: email + password fields, submit calls `signInWithPassword()`.
- Sign-out button: calls `signOut()`, clears local session, returns user to sign-in view.
- Session persistence: the Supabase client handles token storage and refresh. No custom logic required.

**3b. Profile creation — one form:**
- Input: display name (text field).
- On submit: POST to `profiles` via the Supabase client with `account_id` sourced from `app_account_ids()` (call the RPC once after sign-in and store the result for the session).
- On success: store the returned `profile.id` in local state for use by child writes.

**3c. City search — one dependency:**
The `places` table must have at least one row before favorites or comparison sets can be tested. A GeoNames import is the production path, but for staging a single seed row inserted via service-role is sufficient. The frontend only needs to present the `place.id` of that row for selection — a hardcoded dropdown or a simple search input querying `places?display_name=ilike.*term*` under the authenticated session is enough.

**3d. Favorite a city — one write:**
- On city selection: POST to `favorite_places` with `profile_id`, `place_id`, `account_id` (from session context). The trigger `trg_favorite_places_set_account` will fill `account_id` from the profile if not supplied, but the app should supply it explicitly.

**3e. Comparison set — two writes:**
- Create a comparison set: POST to `comparison_sets` with `profile_id`, `account_id`, `title`, `settings_snapshot_json` (can be `{}`).
- Add a city to it: POST to `comparison_set_places` with `comparison_set_id`, `place_id`, `account_id`, `sort_order = 1`.

**3f. Data recovery view — one read per table:**
After sign-out and sign-in, the frontend must perform:
- GET `profiles` — confirm the user's profile is returned.
- GET `favorite_places?profile_id=eq.<id>` — confirm the favorited city is returned.
- GET `comparison_sets?profile_id=eq.<id>` — confirm the set is returned.
- GET `comparison_set_places?comparison_set_id=eq.<id>` — confirm the city inside the set is returned.

All reads use only the publishable key with the re-authenticated session JWT.

**What is explicitly not required for Phase 6:**
- Map rendering
- Notes UI
- Settings UI
- Share links
- Birth records
- Any chart or astrological calculation

---

## 4. Required Validation Sequence

Each step must pass before the next is attempted. All validation uses the publishable key only.

**Step 1 — Bootstrap function deployed**
Confirm: `handle_new_user()` exists in `public` schema, is SECURITY DEFINER, `search_path` pinned. Confirm: trigger `on_auth_user_created` (or equivalent name) exists on `auth.users` AFTER INSERT.

**Step 2 — Signup creates account and membership**
Action: sign up a new user via email/password.
Confirm (via the user's own session, not service-role):
- `SELECT * FROM accounts` returns exactly 1 row.
- `SELECT * FROM account_memberships` returns exactly 1 row with `role = 'owner'` and `accepted_at IS NOT NULL`.
- `SELECT app_account_ids()` returns the id of that account.

**Step 3 — Profile creation**
Action: POST to `profiles`.
Confirm: the returned row has `account_id` matching the user's account.

**Step 4 — City seed present**
Confirm: `SELECT count(*) FROM places` returns at least 1.
If 0: seed one row via service-role before proceeding.

**Step 5 — Favorite a city**
Action: POST to `favorite_places` using the user's session.
Confirm: the returned row exists with the correct `profile_id`, `place_id`, and `account_id`.

**Step 6 — Comparison set and member city**
Action: POST to `comparison_sets`, then POST to `comparison_set_places`.
Confirm:
- `comparison_sets` row has `account_id` matching the user's account.
- `comparison_set_places` row has `account_id` matching the user's account (two-level cascade verified).

**Step 7 — Sign out**
Action: call `signOut()`.
Confirm: a subsequent GET to `profiles` with no session returns 0 rows.

**Step 8 — Sign back in**
Action: call `signInWithPassword()` with the same credentials.
Confirm: a new JWT is issued.

**Step 9 — Data recovery**
Confirm using the new JWT (publishable key only, no service-role):
- `profiles` returns the original profile row.
- `favorite_places` returns the favorited city row.
- `comparison_sets` returns the comparison set row.
- `comparison_set_places` returns the city inside the set.

---

## 5. Required Staging Tests

Each test uses the publishable key and a real user session. Service-role is not used for any assertion below.

| # | Test | Pass condition |
|---|---|---|
| T1 | Signup triggers account creation | `accounts` has 1 row for the new user's `created_by`; `account_memberships` has 1 row; `role = owner`; `accepted_at IS NOT NULL` |
| T2 | `app_account_ids()` returns the new account | RPC returns exactly 1 UUID matching the account created in T1 |
| T3 | Profile INSERT succeeds under publishable key | POST to `profiles` returns 201; row visible in subsequent GET |
| T4 | `places` has at least 1 row | GET `places` returns ≥ 1 row |
| T5 | Favorite INSERT succeeds | POST to `favorite_places` returns 201; row visible; `account_id` = user's account |
| T6 | Comparison set INSERT succeeds | POST to `comparison_sets` returns 201; `account_id` correct |
| T7 | Comparison set place INSERT succeeds | POST to `comparison_set_places` returns 201; `account_id` matches comparison set's account (cascade) |
| T8 | Sign-out terminates session | GET `profiles` after `signOut()` returns 0 rows |
| T9 | Sign-in reissues session | `signInWithPassword()` returns a valid `access_token` |
| T10 | Data survives sign-out/sign-in | Profile, favorite, comparison set, and comparison_set_places rows all present in GET after re-auth |
| T11 | Second signup creates isolated account | Sign up a second user; confirm each user's `app_account_ids()` returns only their own account; User A cannot read User B's profile |

T11 is a regression check against the Phase 5 isolation guarantee for a real signup-triggered account, not just a seeded test fixture.

---

## 6. Success Criteria

Phase 6 is complete when all of the following are true on staging:

1. **A real user can sign up using only email/password and the publishable key**, and immediately receives an account and owner membership with no service-role involvement.

2. **`app_account_ids()` returns a non-empty set** from the new user's session at the moment sign-up completes.

3. **The user can create a profile, favorite a city, and save a comparison set** using only the publishable key and their own JWT. No service-role call is required for any of these writes.

4. **After sign-out and sign-back-in, all data is present.** The profile, favorited city, and comparison set with its member city are all returned in GET requests using the new JWT.

5. **A second user's data is invisible to the first user.** T11 passes.

6. **Service-role was not used for any assertion in the test run.** Setup-only seeding (the one `places` row) may use service-role; all authorization assertions must use publishable-key sessions.

When all six criteria are met on staging, production apply may be planned.
