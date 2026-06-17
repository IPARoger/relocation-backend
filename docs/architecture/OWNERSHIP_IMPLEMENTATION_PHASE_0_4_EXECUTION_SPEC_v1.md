# Ownership Implementation — Phase 0–4 Execution Spec (for human review)

**Status:** Review artifact — updated 2026-06-13 (3 review corrections applied; migration blocker documented).
**Date:** 2026-06-13
**Sources (only):** `OWNERSHIP_IMPLEMENTATION_SEQUENCE_v1.md`, `OWNERSHIP_IMPLEMENTATION_PHASE_0_4_CHECKLISTS_v1.md`. Model A locked.
**Scope:** Phases 0–4 only. No RLS, auth, or frontend.

## Table classification (drives everything below)

| Class | Tables | account_id source |
|------|--------|-------------------|
| **Root** | `profiles` | `account_id → accounts(id)` |
| **Composite-FK targets** (need `UNIQUE(id, account_id)`) | `profiles`, `comparison_sets` | — |
| **profile_id-owned children** (10) | `birth_records`, `intention_profiles`, `current_location_history`, `location_events`, `favorite_places`, `visited_places`, `saved_searches`, `comparison_sets`, `notes`, `share_links` | from their `profiles` row |
| **set-owned child** (1) | `comparison_set_places` | from its `comparison_sets` row |
| **account-direct + optional profile** (1) | `user_settings` | `accounts` directly; `profiles` when `profile_id` set |
| **Global, NO account_id** | `places` | — (untouched) |
| **Deliberately excluded (out of scope)** | `profile_relationships` | keeps `account_user_id` only; future-room table, per source docs — not modified in 0–4 |

13 tables carry `account_id`. `comparison_sets` is both a child (of `profiles`) and a target (of `comparison_set_places`), creating a **two-level cascade** that must be tested.

---

## 1. Required SQL objects by phase (specification, not code)

### Phase 0 — Staging setup
- No DB objects. Artifacts only: staging branch/project; baseline record (per-table row counts; distinct `account_user_id`; snapshot of the ~5 `account_user_id`-bearing rows).

### Phase 1 — Structural tables
- **Table** `accounts` (id, name, account_type+check, created_by→auth.users, timestamps, archived_at).
- **Table** `account_memberships` (id, account_id→accounts, user_id→auth.users, role+check, invited_by, accepted_at, timestamps, archived_at; `UNIQUE(account_id,user_id)`).
- **Indexes** `idx_memberships_user`, `idx_memberships_account`.
- **Functions** `app_account_ids()`, `app_has_account_role()` — SECURITY DEFINER, pinned `search_path`. *(Defined now; only consumed by Phase 5 — created here so the security review covers them once.)*

### Phase 2 — account_id rollout (nullable)
- **Column** `account_id uuid NULL REFERENCES accounts(id)` added to all 13 carrying tables.
- **Index** on `account_id` for each of the 13.
- No NOT NULL, no composite FK, no triggers yet.

### Phase 3 — Backfill *(Option A — clean start; no sentinel migration)*
- **On staging (fresh project):** no existing rows require backfill. Insert one test account + one test membership + one test profile as validation fixtures only. These are test data, not migration artefacts.
- **On production (before Phase 1–4 apply):** run `2026_06_13_phase0_option_a_cleanup.sql` first (deletes all smoke-test profile-owned rows and both user_settings rows; preserves all 21 `places` rows). After cleanup, production also has no rows requiring backfill.
- **No sentinel UUIDs are migrated.** The first real `accounts` row is created by the signup flow (Phase 6).
- Data updates only (no new objects).

### Phase 4 — Integrity lock
- **Unique constraints**: `profiles UNIQUE(id, account_id)`, `comparison_sets UNIQUE(id, account_id)`.
- **NOT NULL**: `account_id` on all 13 carrying tables.
- **Composite FKs** (details §5): 10 profile_id children → `profiles(id,account_id)`; `comparison_set_places` → `comparison_sets(id,account_id)`; `user_settings` → `profiles(id,account_id)` (MATCH SIMPLE) + plain `account_id→accounts`.
- **Trigger function** `app_set_account_from_parent()` + **BEFORE INSERT OR UPDATE OF profile_id/comparison_set_id triggers** on each child (details §6).
- **Partial unique indexes** on `user_settings`: account-default (`profile_id IS NULL`), per-profile (`profile_id IS NOT NULL`).
- **`share_links`**: default `visibility` → `private`; value check `in ('private','unlisted','public')`.

---

## 2. Migration ordering (phase-level)

`Phase 0 → 1 → 2 → 3 → 4`, each in its own transaction, each fully validated before the next. **Hard gate:** Phase 4 may not begin until Phase 3 drift-audit = 0 **and** null-audit = 0.

Within the build, the dependency spine is: create `accounts` (P1) → add nullable `account_id` (P2) → populate it (P3) → only then add constraints that assume it is present and correct (P4).

---

## 3. Constraint ordering (within Phase 4 — strict)

1. `UNIQUE(id, account_id)` on **`profiles`** (target for child FKs).
2. `UNIQUE(id, account_id)` on **`comparison_sets`** (target for `comparison_set_places`).
3. `NOT NULL` on `profiles.account_id`, then on `comparison_sets.account_id`, then on the remaining 11 carrying tables. *(Targets must be non-null before they back FKs.)*
4. **Composite FKs** added as **`NOT VALID`** (cheap, no full scan) — order: the 10 profile_id children, then `comparison_set_places`, then `user_settings`.
5. **`VALIDATE CONSTRAINT`** each composite FK (separate step; surfaces any bad row without a long exclusive lock).
6. **Trigger function + triggers** attached to all children.
7. **`user_settings`** partial unique indexes.
8. **`share_links`** default change + check constraint.

Rationale: unique targets exist before FKs reference them; columns are non-null before FKs assume presence; `NOT VALID`→`VALIDATE` splits the lock; triggers only affect future writes so they can follow validation.

---

## 4. Backfill ordering (within Phase 3 — strict, parent-before-child)

1. Insert **Legacy Dev Account** (sentinel id).
2. **`profiles.account_id`** = legacy, where `account_user_id` = sentinel.
3. **10 profile_id children** ← their `profiles.account_id` (includes `comparison_sets`).
4. **`comparison_set_places`** ← its `comparison_sets.account_id` (must follow step 3).
5. **`user_settings`**: per-profile rows ← their `profiles.account_id`; account-level rows (`profile_id IS NULL`) = legacy directly.
6. Run **drift-audit** and **null-audit** (§7). Both must be 0 before Phase 4.

Rationale: an account must exist before profiles point at it; a profile's `account_id` must be set before its children copy it; a comparison set must be set before its places copy it.

---

## 5. Composite FK implementation details

**Principle:** the FK — not the trigger — is the guarantee. A child's `(profile_id, account_id)` must reference an existing `(id, account_id)` pair in the parent, so a mismatched `account_id` has no referent and is rejected by the engine.

| Child | FK columns | References | On update | On delete | Notes |
|------|-----------|-----------|-----------|-----------|-------|
| 10 profile_id children | `(profile_id, account_id)` | `profiles(id, account_id)` | **CASCADE** | CASCADE | **The existing single-column `profile_id → profiles(id)` FK is dropped when the composite FK is added.** The composite FK subsumes it entirely (a valid `(profile_id, account_id)` pair implies `profile_id` references a real profile). Retaining both creates duplicate enforcement on every write with no additional guarantee. |
| `comparison_set_places` | `(comparison_set_id, account_id)` | `comparison_sets(id, account_id)` | **CASCADE** | CASCADE | second cascade level |
| `user_settings` (per-profile) | `(profile_id, account_id)` | `profiles(id, account_id)` | **CASCADE** | CASCADE | **MATCH SIMPLE** → when `profile_id IS NULL`, not enforced |
| `user_settings` (account-level) | `(account_id)` | `accounts(id)` | — | CASCADE | always enforced |

**Transfer mechanics:** updating `profiles.account_id` cascades to the 10 children automatically; for any transferred `comparison_sets` row, the change cascades again to its `comparison_set_places`. This two-level cascade is the explicit transfer test in §7.

**Lock strategy:** add every composite FK `NOT VALID` first, then `VALIDATE` separately.

---

## 6. Trigger implementation details

- **One trigger function** `app_set_account_from_parent()` (PLPGSQL), reused by all children.
- **Behavior (fill-only):** on the affected row, if `account_id IS NULL`, derive it from the parent —
  - profile_id-owned children + per-profile `user_settings`: `account_id := profiles.account_id` for `NEW.profile_id`.
  - `comparison_set_places`: `account_id := comparison_sets.account_id` for `NEW.comparison_set_id`.
- **Fires:** `BEFORE INSERT OR UPDATE OF profile_id` (children) / `OF comparison_set_id` (`comparison_set_places`). This keeps `account_id` correct when a row is **re-parented**, not just on insert.
- **Does NOT reject** mismatches — that is the composite FK's job. Trigger = ergonomics; FK = correctness. (A row that is re-parented to a profile in a different account gets its `account_id` recomputed by the trigger; if a caller explicitly forces a conflicting `account_id`, the FK rejects it.)
- **Account-level `user_settings`** (`profile_id IS NULL`): trigger does nothing; the caller/app supplies `account_id` (no parent profile to derive from).

---

## 7. Validation queries (specifications — predicate + expected result)

> Expressed as logical checks for human review, not as runnable migration code.

**A. Drift audit (pass = 0 for every line):**
- For each of the 10 profile_id children + per-profile `user_settings`: rows where `child.account_id ≠ profiles.account_id` (joined on `child.profile_id = profiles.id`). Expected **0**.
- `comparison_set_places`: rows where `account_id ≠ comparison_sets.account_id` (joined on `comparison_set_id`). Expected **0**.

**B. Null audit (pass = 0 for every table):**
- For each of the 13 carrying tables: rows where `account_id IS NULL`. Expected **0** (post Phase 3).

**C. Negative insert test (expected = FAILURE):**
- Attempt to insert into a child (e.g., `favorite_places`) with `profile_id` = a profile in **Account A** but `account_id` = **Account B**.
- Expected: **foreign-key violation (SQLSTATE 23503)**. A success here is a critical failure of the design.

**D. Negative update test (expected = FAILURE):**
- Take an existing child row correctly in **Account A**; attempt `UPDATE … SET account_id = B` (B ≠ its profile's account).
- Expected: **foreign-key violation (23503)**.

**E. Transfer cascade test (expected = PASS):**
- Preconditions: a 2nd test account **A2** — **A2 must be inserted as a real `accounts` row in the staging database before this test runs; this insert is test setup, not a migration step, and its absence produces a FK-violation failure indistinguishable from a genuine cascade bug**; a test profile **P** in **A1** that has children including a `comparison_sets` row with `comparison_set_places`.
- Action: `UPDATE profiles SET account_id = A2 WHERE id = P`.
- Expected:
  1. All 10-children rows for P now show `account_id = A2`.
  2. P's `comparison_set_places` rows (via its sets) now show `account_id = A2` (**two-level cascade**).
  3. Count of P's child rows still showing `account_id = A1` is **0**.
  4. Drift-audit remains **0**.

**F. Schema lint (pass = no gaps):**
- Every owned table (the 13) has: `account_id` column; an index on it; (post-Phase-4) a composite FK present and **validated**; `NOT NULL`. Any missing element = fail.

**G. Composite FK validation (pass = all validated):**
- Every composite FK reports `convalidated = true`.

**H. Regression guard (Phase 0–4 close):**
- Under the **publishable key**, every table still returns **0 rows** (no read path opened; RLS remains default-deny until Phase 5).

---

## 8. Rollback procedure per phase (reverse-order)

| Phase | Rollback |
|------|----------|
| **0** | Discard staging branch/project. Zero impact. |
| **1** | Drop `app_has_account_role`, `app_account_ids`; drop `account_memberships`; drop `accounts` (memberships before accounts due to FK). |
| **2** | Drop `account_id` indexes; drop `account_id` columns on all 13 tables. |
| **3** | Set `account_id = NULL` on all 13 tables where it equals legacy; delete the Legacy Dev Account row. (No FKs yet, so null-order is unconstrained.) |
| **4** | **Exact reverse order (FK targets cannot be dropped while FKs reference them):** (1) drop `share_links` check + restore `visibility` default; (2) drop `user_settings` partial unique indexes; (3) drop triggers + trigger function; (4) drop `comparison_set_places` composite FK **first** (it references `comparison_sets UNIQUE`); (5) drop all remaining child composite FKs (they reference `profiles UNIQUE`); (6) drop `user_settings` composite FK; (7) set `account_id` columns nullable (drop NOT NULL) on all 13 tables; (8) drop `UNIQUE(id, account_id)` on `comparison_sets`; (9) drop `UNIQUE(id, account_id)` on `profiles`. Skipping step 4 before step 8 causes a Postgres dependency error and stalls the rollback. |

Every phase is additive/reversible; nothing in 0–4 is destructive to existing rows except the Phase 3 `account_id` writes, which are reversible to NULL.

---

## Phase 4.5 — Human Review Gate (must all be green before Phase 5)

| # | Gate | Source check |
|---|------|--------------|
| 1 | Drift audit = 0 | §7A |
| 2 | Null audit = 0 | §7B |
| 3 | Negative insert fails | §7C |
| 4 | Negative update fails | §7D |
| 5 | Profile transfer cascade passes | §7E |
| 6 | Composite FK validation passes | §7G |
| 7 | account_id present on every owned table | §7F |
| 8 | Schema lint passes | §7F |

Only when all eight are green on staging may RLS (Phase 5) be planned for execution. **No production changes, no RLS, no auth, no frontend in this scope.**

---

## ⛔ MIGRATION BLOCKER — Phase 0 finding (2026-06-13)

**Discovered during:** Phase 0 baseline capture (live DB introspection).
**Baseline file:** `docs/architecture/staging/PHASE_0_BASELINE_2026-06-12.json`
**Status:** Human decision required before Phase 3 backfill can be specified.

### What the spec assumed

Phase 3 backfill was specified as:
> Insert the Legacy Dev Account using sentinel `00000000-0000-0000-0000-000000000000`.
> Set `profiles.account_id = legacy` where `account_user_id = sentinel`.

This assumed **one** `account_user_id` value in the data.

### What the live database actually contains

**`profiles` table — 3 rows, 3 distinct `account_user_id` values:**

| profile | display_name | account_user_id | archived? |
|---------|-------------|-----------------|-----------|
| 4173c016 | Smoke Test Profile | `00000000-…-0001` | no |
| 757980ff | SMOKE TEST renamed | `00000000-…-0000` | yes |
| fc10ef29 | API SMOKE patched | `00000000-…-0002` | yes (type: pet) |

**`user_settings` table — 2 rows, 2 distinct `account_user_id` values:**

| settings row | account_user_id | profile_id | notes |
|-------------|-----------------|------------|-------|
| 930ba94f | `00000000-…-0999` | null | smoke test theme |
| 5dce5b17 | `bffe7a2a-d183-4a96-abbf-c205fcb0d762` | null | `theme: cloud-grey, zodiac: tropical` — **looks like a real user** |

**The `bffe7a2a` UUID does not follow the all-zeros sentinel pattern.** It appears to be a real UUID inserted at some point. Auth `list_users()` returns 0 — this user does not exist in Supabase Auth. The row is currently orphaned with no corresponding auth user.

### Why this blocks Phase 3

The backfill join `WHERE account_user_id = '00000000-…-0000'` only captures one of the three profile sentinel values, leaving two profiles (and their children) with `account_id` remaining NULL — causing the Phase 3 null-audit to fail and the Phase 4 NOT NULL constraint to be unappliable.

Additionally: the `bffe7a2a` user_settings row cannot be attributed to any account until a human decides what it represents.

### The three options — human must choose one

**Option A — Discard all smoke-test data, start clean (recommended)**
Delete all 3 profiles and their cascaded children; delete both user_settings rows. Keep all 21 `places` rows (real reference data). Phase 3 backfill then only needs to insert the legacy account and wire the first real user at signup (Phase 6). The `bffe7a2a` settings row is discarded.

- Simplest backfill.
- No ambiguity about sentinel ownership.
- Loses nothing of product value (all rows are named "Smoke Test").

**Option B — One legacy account per distinct sentinel group**
Map all sentinel-pattern UUIDs (`…0000`, `…0001`, `…0002`, `…0999`) to a single "Legacy Dev Account." Treat `bffe7a2a` as the owner of that account (insert it as an `account_memberships` row linking that UUID to the legacy account). If `bffe7a2a` is Dave Goodman's real auth user, this connects correctly when he signs up.

- Preserves all existing rows.
- The `bffe7a2a` settings row resolves naturally if that is the real owner.
- Backfill WHERE clause must cover all four sentinel patterns.

**Option C — Targeted: keep `bffe7a2a` row, discard sentinels**
Delete the 3 smoke-test profiles and their children; delete the `…0999` user_settings row. Keep the `bffe7a2a` settings row. Create a real account for `bffe7a2a` as the owner. Wire that account at first real-user signup (if `bffe7a2a` is the real user ID) or treat as orphaned cleanup.

- Preserves the one settings row that may carry real preferences.
- Still requires a human to confirm whether `bffe7a2a` is a real intended user.

### What is needed from a human

1. **Is `bffe7a2a-d183-4a96-abbf-c205fcb0d762` your real Supabase auth user ID, or a test value?**
2. **Do you want to keep any of the smoke-test profile/settings rows, or start clean?**
3. **Choose Option A, B, or C above** (or state a different preference).

Phase 3 backfill cannot be finalized until this is answered. Phase 0 baseline capture and Phase 1 structural-table SQL can still be authored in parallel.
