# A2 — Signup Bootstrap Verification

**Roadmap:** WEB2_COMPLETION (Phase A — A2)  
**Date:** 2026-06-18  
**Prior audit:** `results/86_web2_launch_blockers_audit.md`  
**Migration:** `supabase/migrations/2026_06_13_phase6_signup_bootstrap.sql`

---

## Step 1 — Trigger State

### Migration present in repo

**Yes** — `supabase/migrations/2026_06_13_phase6_signup_bootstrap.sql`

| Object | Status |
|--------|--------|
| `public.handle_new_user()` | Defined — SECURITY DEFINER, `search_path = public` |
| `on_auth_user_created` trigger | Defined — AFTER INSERT ON `auth.users` FOR EACH ROW |
| Dependent tables | `accounts`, `account_memberships` |

### Migration applied?

**Yes (staging)** — inferred from live bootstrap test (2026-06-18). Creating a new `auth.users` row via `admin.create_user(email_confirm=True)` immediately produced `accounts` + `account_memberships` rows matching migration logic.

Direct `information_schema.triggers` query was not run (no `DATABASE_URL` in `.env.staging`). Phase 6 closeout (`docs/architecture/PHASE_6_CLOSEOUT.md`) previously verified trigger metadata on staging (2026-06-13).

### Trigger active?

**Yes (staging)** — bootstrap chain completes on every disposable user test. If trigger were missing or disabled, `accounts` count would be 0 and `app_account_ids()` would return empty.

---

## Step 2 — Live Bootstrap Test

**Method:** `admin.auth.admin.create_user({ email_confirm: True })` — same `auth.users` INSERT path as `signUp()` per Phase 6 closeout.

**Disposable account (manual probe, 2026-06-18):**

| Step | Result |
|------|--------|
| `auth.users` row created | `user_id=61bf07cb-4958-4628-a763-0840d2ea29c6` |
| `accounts` row | 1 row — `name=Personal`, `account_type=personal`, `created_by=user_id` |
| `account_memberships` row | 1 row — `role=owner`, `accepted_at` set |
| Sign-in | Session issued |
| `app_account_ids()` | Returns account UUID |
| `GET /profiles` | 200, count=0 (expected for new user) |
| Cleanup | User + account rows deleted |

**Note:** Direct `signUp()` with `@relocation-smoke.test` domain rejected by Supabase as invalid email. Admin create path is the validated production-equivalent INSERT path.

---

## Step 3 — Failure Analysis

**Bootstrap did not fail.** No fix required.

If bootstrap had failed, break points would be:
1. Missing migration / trigger not applied
2. `handle_new_user()` function error on INSERT
3. RLS blocking function (unlikely — SECURITY DEFINER)
4. `app_account_ids()` requiring `accepted_at` on membership (trigger sets this)

---

## Step 4 — Regression Coverage

**Created:** `scripts/smoke_signup_bootstrap.py`

Checks:
- Migration artifact present in repo
- Disposable user creation
- Exactly 1 `accounts` row (Personal/personal)
- Exactly 1 `account_memberships` row (owner, accepted_at)
- `app_account_ids()` returns account for new JWT
- `GET /profiles` returns 200
- Cleanup of user + account rows

---

## Step 5 — Validation

### smoke_signup_bootstrap.py — PASS (12/12)

```
PASS: migration_file_present
PASS: migration_contains_handle_new_user
PASS: migration_contains_on_auth_user_created
PASS: migration_contains_account_memberships
PASS: auth_user_created
PASS: accounts_row_created
PASS: accounts_personal
PASS: membership_row_created
PASS: membership_owner_accepted
PASS: sign_in_succeeds
PASS: app_account_ids_returns_account
PASS: get_profiles_200
PASS: smoke_signup_bootstrap
```

### Impacted auth smoke

| Smoke | Result |
|-------|--------|
| `smoke_profile_create.py` | PASS (14/14) |

---

## Final Verdict

**VERIFIED** — Signup bootstrap is functioning on staging. `handle_new_user()` trigger chain produces required account records; new users can authenticate and access scoped APIs. Permanent regression smoke added.

**A2 blocker status:** Resolved for staging. Re-run `smoke_signup_bootstrap.py` when deploying to a new Supabase environment.
