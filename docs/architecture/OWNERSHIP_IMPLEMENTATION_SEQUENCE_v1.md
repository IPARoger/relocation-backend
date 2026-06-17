# Ownership Implementation Sequence (v1) — APPROVED

**Status:** Approved basis for implementation. Ownership **Model A is locked** (accounts → memberships → profiles → children, with **denormalized `account_id` on every child table**). Not to be reopened.
**Date:** 2026-06-13
**Pairs with:** `OWNERSHIP_IMPLEMENTATION_PHASE_0_4_CHECKLISTS_v1.md` (detailed Phase 0–4 checklists), `ACCOUNT_WORKSPACE_RLS_PLAN_v1`, `SUPABASE_ASSET_INVENTORY_v1`.
**Inputs:** inventory + plan docs, `2026_06_08_schema_v1.sql`, `2026_06_12_account_workspace_rls_draft.sql`.

---

## Locked decisions (do not revisit)

- Chain: `auth.users → account_memberships → accounts → profiles → child tables`.
- **Every child table carries `account_id`** (denormalized).
- **Drift is made structurally impossible by a composite foreign key**, not by trigger alone:
  - `profiles` gets `UNIQUE(id, account_id)`.
  - each child gets `FK (profile_id, account_id) → profiles(id, account_id) ON UPDATE CASCADE` (and `ON DELETE CASCADE`).
  - `account_id` is `NOT NULL` after backfill.
  - a `BEFORE INSERT` trigger auto-fills `account_id` from the profile (ergonomics); the FK is the guarantee.
  - `comparison_set_places` chains via `comparison_sets(id, account_id)`; `user_settings` uses the composite FK for per-profile rows and a plain `account_id → accounts` FK for account-level rows.

`profiles.account_id` is the single source of truth; child `account_id` is a cascaded copy, never independently authored.

---

## Phase map

| Phase | Purpose | Risk | Rollback | Depends on |
|------|---------|------|----------|-----------|
| 0 | Staging mirror of prod schema + data | None | Discard branch | — |
| 1 | Structural tables (`accounts`, `account_memberships`) + helpers | Low | Drop | 0 |
| 2 | Add nullable `account_id` columns + indexes | Low | Drop columns | 1 |
| 3 | Backfill account_id (legacy account → profiles → children) | Med (data) | Set null | 2 |
| 4 | Integrity lock (NOT NULL, UNIQUE, composite FKs, triggers, uniqueness, share default) | Med | Drop constraints | 3 clean |
| 5 | RLS + policies (table-by-table) | **High** | Disable/drop policy | 4 |
| 6 | Auth (Google/Apple) + first real user + membership | Med | Moderate | 5 |
| 7 | App cutover to publishable key; later drop `account_user_id` | Med | Hard | 6 |

**This work order covers Phases 0–4 only.** Phases 5–7 are out of scope here.

---

## Validation charter (the 7 required checks, honestly scoped)

| # | Required check | Where proven | Phase 0–4 obligation |
|---|----------------|--------------|----------------------|
| 1 | Ownership drift impossible | **Phase 4** ✅ | Prove via negative insert/update + cascade |
| 2 | User A cannot read User B | **Phase 5** (needs RLS) | Establish precondition: every row carries correct `account_id` |
| 3 | Profile transfer works | **Phase 4** ✅ | Prove via cascade test |
| 4 | Share links cannot expose private data | **Phase 5 + RPC** | Establish precondition: `visibility` default → private |
| 5 | Places still readable | **Phase 5** (read policy) | Obligation: do **not** alter `places` RLS in 0–4 (don't make it worse) |
| 6 | Publishable-key tests pass | **Phase 5** | Phase 0–4 regression guard: publishable key still returns 0 (no hole opened) |
| 7 | Service-role ignored for authz validation | **Principle (always)** | Integrity tests may use service-role; **authorization** tests never may |

Key honesty point: **service-role is acceptable for integrity tests** (drift/transfer — they test the database engine), but is **forbidden for authorization tests** (A-vs-B — those must use a real publishable-key session). The two test classes must not be conflated.
