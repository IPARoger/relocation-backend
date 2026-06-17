# Account / Workspace + RLS Plan (v1)

**Status:** DESIGN ARTIFACT — nothing applied, no data changed, no users created.
**Date:** 2026-06-12
**Pairs with:** `supabase/migrations/2026_06_12_account_workspace_rls_draft.sql` (draft, self-aborting)
**Inputs read:** `SUPABASE_ASSET_INVENTORY_v1_2026-06-12.md`, `2026_06_08_schema_v1.sql`, `repositories/*`, live schema metadata.

---

## 1. Why this exists

Today "account" = a single `auth.users` row, stored as a bare `account_user_id uuid` (no FK) on three tables. That model cannot survive professional+client, assistants, family/multi-login, or client portals without a re-policy. We are inserting an **accounts + memberships** layer **now**, while there are **0 users and 0 RLS policies**, so RLS is wired to a workspace boundary instead of one human forever.

### Target ownership chain

```
auth.users
   └─ account_memberships (user_id, account_id, role)
        └─ accounts
             └─ profiles (account_id)
                  └─ child tables (denormalized account_id)
```

The same schema must serve, with **no structural change**, all of:

| Scenario | How it maps |
|----------|-------------|
| Solo user | 1 account, 1 membership (owner), N profiles |
| Professional w/ clients | 1 account, 1 owner; each client = a profile (later: a viewer membership) |
| Assistant login | 2nd membership (role `assistant`) on the same account |
| Family / multi-user | N memberships on 1 account |
| Client portal (future) | client gets a `viewer` membership scoped to their profile(s) |

---

## 2. Decisions taken in this draft

1. **Insert `accounts` + `account_memberships`** (many-to-many auth.users↔accounts). This is the load-bearing change.
2. **Role model = `CHECK` constraint, not a PG `enum`.** Enums are painful to alter (`ALTER TYPE … ADD VALUE` can't run in a transaction, can't remove values). A text + check is trivially evolvable. Roles: `owner, admin, member, assistant, viewer` (§4).
3. **Denormalize `account_id` onto every child table** (recommended) rather than join through `profiles` in every policy. Rationale:
   - **Safety:** a single backstop column; one forgotten policy can't silently cross tenants because the predicate is uniform (`account_id in (app_account_ids())`).
   - **Performance:** one indexed equality vs a `profiles` subquery on every row check.
   - **Cost:** must keep `account_id` consistent with `profile_id` (backfill once + a sync trigger or app-set on insert). Acceptable.
   - *Alternative considered (join-through-profiles)* is documented as Open Q2 in case reviewers prefer fewer columns.
4. **Access via `SECURITY DEFINER` helper** `app_account_ids()` returning the caller's account ids — avoids RLS recursion on `account_memberships` and keeps policies one-liners.
5. **`share_links.visibility` default → `private`** + a value check. Public was a dangerous default for the app's most sensitive data.
6. **`user_settings` uniqueness fixed**: one account-level default (`profile_id null`) per account; one per `(account, profile)` otherwise.
7. **`places` stays global**: RLS-enabled with an authenticated-read policy; writes restricted to service role. Without this the map/search silently breaks under the publishable key.
8. **`account_user_id` retained during transition** on `profiles`/`user_settings` (Open Q1); dropped only after cutover.

---

## 3. Backfill strategy (the `00000000…` dev owner)

All existing rows are owned by the sentinel `00000000-0000-0000-0000-000000000000` and are mostly smoke-test junk ("Smoke Test Profile", "API SMOKE patched").

**Recommended:** create a single **Legacy Dev Account** reusing that same all-zero uuid as the `accounts.id` (greppable + reversible), point existing `profiles.account_id` at it, denormalize `account_id` down to children from each row's profile, then — **only when the first real user signs up** — insert one `owner` membership linking that user to the legacy account. Alternatively, discard the smoke-test profiles entirely and start clean (keep `places`, which is real reference data).

Backfill DML lives in the draft migration as a **commented** block (§8 of the SQL) so it is reviewed line-by-line and never auto-runs.

---

## 4. Membership role list (justification)

| Role | Can | Cannot | Use |
|------|-----|--------|-----|
| `owner` | everything incl. billing, delete account, manage members | — | account creator; ≥1 required |
| `admin` | manage members + all data | billing, delete account | trusted partner |
| `member` | full CRUD on account data | manage members/billing | default for solo & family adults |
| `assistant` | CRUD data, **no** member mgmt, **no** sharing/billing | invite, share externally | professional's helper (future) |
| `viewer` | read-only (optionally scoped to specific profiles) | any write | client portal, family read-only (future) |

v1 only needs `owner`; the rest are reserved so the check constraint doesn't need widening later.

---

## 5. Child-table `account_id` strategy

**Chosen: denormalized `account_id` on all profile-owned children** (`birth_records`, `intention_profiles`, `current_location_history`, `location_events`, `favorite_places`, `visited_places`, `saved_searches`, `comparison_sets`, `notes`, `share_links`), plus `comparison_set_places` (from its set) and `user_settings` (from `account_user_id`). Consistency maintained by: backfill once → set on insert in the repo/app → optional trigger guard. Policies then reduce to `account_id in (select app_account_ids())`.

---

## 6. Rollback plan

Because nothing is applied yet, "rollback" = either don't apply, or reverse the additive changes:

1. All new objects are additive (`create table … if not exists`, `add column if not exists`, new indexes, new policies). Reverse order:
   - `drop policy …` (if any were enabled), `alter table … disable row level security` for the tables we toggled.
   - `drop index` the new unique/idx.
   - `alter table … drop column account_id` on each child + `profiles` + `user_settings`.
   - `alter table share_links alter column visibility set default 'public'` + drop the check (to restore prior state) — *only if reverting intentionally*.
   - `drop function app_account_ids, app_has_account_role`.
   - `drop table account_memberships, accounts`.
2. Backfill is reversible: the legacy account id is the known all-zero constant; `update … set account_id = null where account_id = '00000000-…'`.
3. Keep a row snapshot of the ~5 rows carrying `account_user_id` before any DML.

---

## 7. Test plan (validate with the **publishable** key, not service role)

| # | Assertion | Method |
|---|-----------|--------|
| 1 | **User A cannot read User B** | Sign in as A (publishable key), select each table → only A's account rows; B's invisible |
| 2 | **Account member can read account profiles** | A invites C (membership `member`); C selects profiles → sees account profiles |
| 3 | **Non-member cannot read account profiles** | D (no membership) selects → 0 rows |
| 4 | **`places` readable as intended** | Authenticated select on `places` → rows returned; anon per policy decision |
| 5 | **Share link exposes only sanitized path** | Anon select `share_links` by slug → row visible; the **target** (`birth_records`) NOT directly selectable; only the SECURITY DEFINER RPC returns data, honoring `hide_birth_data`/`include_*` |
| 6 | **Service-role bypass acknowledged** | Note that service-role ignores RLS; it must **not** be used for tenant-boundary tests — all isolation tests use the publishable key under a real session |

Each test run against a **staging branch/project**, inside a transaction that is rolled back, before any production apply.

---

## 8. Open questions (resolve before apply)

1. **Dual columns during transition?** Keep both `account_id` *and* `account_user_id` on `profiles`/`user_settings` until app cutover, then drop `account_user_id`? (Draft assumes **yes — keep both, drop later**.)
2. **Denormalize `account_id` on children, or join through `profiles`?** (Draft recommends **denormalize**; reviewer may prefer fewer columns + a `profiles` subquery.)
3. **Exact role list?** Confirm `owner/admin/member/assistant/viewer` — or trim to `owner/member/viewer` for v1.
4. **Public share reading: raw RLS or RPC/Edge Function?** (Draft strongly recommends **RPC/Edge Function** because `hide_birth_data` and `include_*` sanitization cannot be enforced by RLS alone.)
5. **`places` read: `authenticated` only, or `anon` too?** (Affects whether logged-out share pages can render a map.)
6. **Keep or discard smoke-test data** during backfill?

---

## SAFEST NEXT HUMAN REVIEW DECISION

**Decide Open Q2 first: denormalized `account_id` on children vs join-through-`profiles`.** It is the one choice that changes the column set, every RLS policy, the backfill, and the repository insert paths — so it must be locked *before* any migration is finalized or applied. Everything else (role names, dual-column transition, share-read mechanism) can be adjusted later without reshaping the schema; this one cannot. Review the draft migration against that decision, then validate on a staging branch with the publishable key before considering a production apply.
