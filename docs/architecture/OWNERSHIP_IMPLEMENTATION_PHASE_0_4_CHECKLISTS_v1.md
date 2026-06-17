# Ownership Implementation — Phase 0–4 Checklists & Validation Procedures

**Status:** Execution checklist. **Staging only — no production apply, no RLS, no frontend wiring.**
**Date:** 2026-06-13
**Basis:** `OWNERSHIP_IMPLEMENTATION_SEQUENCE_v1.md` (Model A locked).
**Scope:** Phases 0–4 (staging setup → structural tables → account_id rollout → backfill → integrity lock). Phases 5–7 excluded.

Conventions:
- **Integrity test** = tests the database engine (drift, transfer, constraints). May run under service-role.
- **Authorization test** = tests who-can-read-what. **Must** run under a publishable-key session. **Deferred to Phase 5.**
- "Drift-audit" = count of child rows whose `account_id` ≠ their parent's `account_id`; **pass = 0**.
- "Null-audit" = count of owned rows with `account_id IS NULL`; **pass = 0** (after Phase 3).
- Every phase runs in its own transaction on the **staging branch**, reversible before moving on.

---

## PHASE 0 — Staging setup

### Build checklist
- [ ] Confirm Supabase **branching** is available on the current plan tier. If not, provision a **separate staging project** as fallback.
- [ ] Create the staging branch/project from the **current production schema**.
- [ ] Ensure staging contains the live **15 tables** and a representative data snapshot: the `00000000…` placeholder profiles, the 21 `places`, and the existing favorites/notes/etc.
- [ ] Record a **baseline**: row count per table; distinct `account_user_id` values; a snapshot of the ~5 rows that carry `account_user_id` (`profiles`, `user_settings`, `profile_relationships`).
- [ ] Confirm staging **publishable** and **service-role** keys are distinct from production and stored separately.
- [ ] Write-protect production: confirm no tooling in this work points at the prod URL.

### Validation procedure
- [ ] Schema diff **staging == production** (no drift introduced by branching).
- [ ] Row counts **match baseline** exactly.
- [ ] Baseline snapshot file saved and readable.

**Exit criteria:** staging mirrors prod; baseline captured. **Rollback:** discard branch (zero impact).

---

## PHASE 1 — Structural tables

### Build checklist
- [ ] Create `accounts` (additive).
- [ ] Create `account_memberships` with `unique(account_id, user_id)` and FKs to `auth.users`.
- [ ] Create helper functions `app_account_ids()` and `app_has_account_role()` as **SECURITY DEFINER with a pinned `search_path`** (anti-escalation requirement).
- [ ] Confirm **no existing table is altered** (purely additive).

### Validation procedure
- [ ] `accounts` and `account_memberships` exist; the 15 existing tables are **unchanged** (schema diff shows only additions).
- [ ] Helper functions exist; **verify `search_path` is pinned** and ownership is a trusted role (security review of the definer functions).
- [ ] FKs to `auth.users` resolve (auth schema reachable).
- [ ] Existing-table **row counts unchanged** (no data touched).

**Risk:** Low. **Rollback:** drop the two tables + two functions.

---

## PHASE 2 — account_id rollout (nullable)

### Build checklist
- [ ] Add `account_id` (**nullable**, FK → `accounts`) to: `profiles`, `birth_records`, `intention_profiles`, `current_location_history`, `location_events`, `favorite_places`, `visited_places`, `saved_searches`, `comparison_sets`, `comparison_set_places`, `notes`, `share_links`, `user_settings`.
- [ ] Add a per-table index on `account_id`.
- [ ] Confirm **no NOT NULL, no composite FK, no triggers yet** (those are Phase 4).

### Validation procedure
- [ ] **Schema-lint:** enumerate "owned tables" and confirm **each** now has an `account_id` column + index — **zero gaps**.
- [ ] All `account_id` values are currently **NULL** (expected pre-backfill).
- [ ] Additive-only: existing data untouched; row counts unchanged.

**Risk:** Low. **Rollback:** drop the columns/indexes.

---

## PHASE 3 — Backfill

### Build checklist
- [ ] Insert the **Legacy Dev Account** row reusing the sentinel id `00000000-0000-0000-0000-000000000000` (greppable, reversible).
- [ ] Set `profiles.account_id = legacy` where `account_user_id = sentinel`.
- [ ] **Cascade-copy** `account_id` to each child **from its profile**.
- [ ] `comparison_set_places.account_id` from its parent `comparison_sets`.
- [ ] `user_settings`: per-profile rows from their profile; **account-level rows (`profile_id` null)** set `account_id = legacy` directly.
- [ ] Identify any **orphans** (child whose profile is missing or whose profile has null `account_id`) → quarantine list; resolve before Phase 4 (should be none, since `profile_id` FK already exists).

### Validation procedure (gates Phase 4)
- [ ] **Drift-audit = 0** across every child table.
- [ ] **Null-audit = 0** across every owned table (every row backfilled).
- [ ] Row counts unchanged except **+1** in `accounts` (the legacy row); backfill is update-only otherwise.
- [ ] **Spot-check:** pick one known profile; confirm its `birth_records`, `favorite_places`, `notes` all carry the **same** `account_id`.
- [ ] Orphan list is **empty**.

**Risk:** Medium (data correctness). **Rollback:** set `account_id = NULL` on all tables where it equals legacy; delete the legacy `accounts` row. **Do not proceed to Phase 4 until drift-audit and null-audit both return 0.**

---

## PHASE 4 — Integrity lock (drift becomes impossible here)

### Build checklist
- [ ] Add `UNIQUE(id, account_id)` to `profiles` (makes it a composite FK target).
- [ ] Set `account_id` **NOT NULL** on `profiles` and all children (safe now — Phase 3 null-audit was 0).
- [ ] Add composite FK `(profile_id, account_id) → profiles(id, account_id)` **`ON UPDATE CASCADE` / `ON DELETE CASCADE`** to each child — add as **`NOT VALID` first, then `VALIDATE`** separately (avoids long locks; surfaces bad rows without blocking).
- [ ] `comparison_set_places`: composite FK → `comparison_sets(id, account_id)`.
- [ ] `user_settings`: composite FK → `profiles(id, account_id)` (MATCH SIMPLE, so account-level rows with null `profile_id` are skipped) + plain `account_id → accounts`.
- [ ] Add `BEFORE INSERT` **auto-fill triggers** per child (populate `account_id` from the profile when null).
- [ ] Add `user_settings` partial-unique indexes: one account-level default per account; one per `(account, profile)`.
- [ ] Set `share_links.visibility` **default → `private`** + value check (existing rows reviewed, not force-rewritten).

### Validation procedure — **THE DRIFT PROOF** (integrity tests; service-role acceptable)
- [ ] **Negative insert:** attempt to insert a child with an `account_id` that differs from its profile's → **MUST fail** (FK violation). *Proves drift cannot be created.*
- [ ] **Negative update:** attempt to change a child's `account_id` to a different account → **MUST fail**.
- [ ] **Auto-fill:** insert a child **without** `account_id` → trigger fills from profile; row matches; drift-audit still 0.
- [ ] **Transfer (check #3):** move a test profile to a 2nd test account by updating `profiles.account_id` → **all children's `account_id` cascade-follow**; drift-audit = 0. *Proves transfer works and stays consistent.*
- [ ] **NOT NULL:** attempt a null-`account_id` insert → **MUST fail**.
- [ ] **user_settings uniqueness:** 2nd account-level row for same account → **fails**; 2nd row for same `(account, profile)` → **fails**.
- [ ] **share_links default:** new row without `visibility` → defaults `private`; out-of-set value → **rejected**.
- [ ] Re-run **drift-audit = 0** and **null-audit = 0**.

**Risk:** Medium (constraints will reject any imperfect backfill — that is the intended behavior). **Rollback:** drop composite FKs, triggers, unique indexes, NOT NULL, and the `profiles` unique constraint; restore `share_links` default if reverting.

---

## Consolidated validation checklist (the 7 required checks)

| # | Check | Status at end of Phase 4 | How |
|---|-------|--------------------------|-----|
| 1 | **Ownership drift impossible** | ✅ **PROVEN** | Phase 4 negative insert/update + cascade |
| 3 | **Profile transfer works** | ✅ **PROVEN** | Phase 4 transfer/cascade test |
| 5 | **Places still readable** | ✅ **NOT REGRESSED** | `places` RLS untouched in 0–4 (unchanged from baseline) |
| 6 | **Publishable-key tests pass** | ◻ **PRECONDITION ONLY** | Regression guard: publishable key still returns 0 everywhere (no hole opened); authorization proof is Phase 5 |
| 2 | **User A cannot read User B** | ◻ **DEFERRED → Phase 5** | Precondition met: every row carries correct `account_id` for policies to key on |
| 4 | **Share links cannot expose private data** | ◻ **DEFERRED → Phase 5 + RPC** | Precondition met: `visibility` default flipped to `private` |
| 7 | **Service-role ignored for authz** | ✅ **ENFORCED AS POLICY** | Integrity tests used service-role intentionally; authorization tests reserved for publishable-key sessions in Phase 5 |

**Phase 0–4 completion definition:** checks 1, 3, 5, 7 satisfied; checks 2, 4, 6 have their preconditions established and are explicitly carried into Phase 5. Nothing applied to production.

---

## Regression guard before declaring Phase 0–4 done
- [ ] On staging, with the **publishable key**, select each table → still **0 rows** (confirms the new columns/constraints did **not** accidentally open a read path; RLS remains default-deny until Phase 5).
- [ ] Schema diff prod vs staging documented (the exact delta to be applied later, after human review).
- [ ] Baseline vs post-Phase-4 row counts reconciled (only `accounts` +1).

---

## What is NOT done here (carried to later phases — do not start)
- RLS policies / table enablement (Phase 5).
- Auth providers, first real user, membership wiring (Phase 6).
- Frontend/repository cutover to publishable key; dropping `account_user_id` (Phase 7).
- Any browser read/write of user data; city search; map/translation; share pages.
