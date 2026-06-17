# Phase 5 — RLS Rollout Execution Spec (architecture review)

**Status:** ARCHITECTURE REVIEW ONLY. No SQL, no migration, no apply.
**Date:** 2026-06-13
**Author role:** Principal Database Architect
**Scope:** Staging only. Production untouched.
**Sources (only):** `ACCOUNT_WORKSPACE_RLS_PLAN_v1_2026-06-12.md`, `OWNERSHIP_IMPLEMENTATION_SEQUENCE_v1.md`, `OWNERSHIP_IMPLEMENTATION_PHASE_0_4_EXECUTION_SPEC_v1.md`, `supabase/migrations/2026_06_13_phase4_integrity_lock.sql`.

**Preconditions (must be true before Phase 5 begins):**
- All 8 Phase 4.5 gates green on staging.
- `app_account_ids()` and `app_has_account_role()` exist, are `SECURITY DEFINER`, `search_path` pinned (created Phase 1).
- Every carrying table has `account_id NOT NULL` + validated composite FK (Phase 4).
- Under the publishable key, every table currently returns 0 rows (default-deny; no policies yet).

---

## 0. The boundary primitive

Every authorization predicate in Phase 5 reduces to one of two forms, both built on the Phase 1 helpers (which are `SECURITY DEFINER` and therefore **do not recurse** through RLS on `account_memberships`):

- **Read/membership test:** `account_id IN (SELECT app_account_ids())`
- **Role-gated write test:** `app_has_account_role(account_id, <role array>)`

`app_account_ids()` resolves `auth.uid()` → `account_memberships` → set of `account_id`. For an anonymous caller, `auth.uid()` is NULL → the set is empty → every account-scoped predicate denies. This is the structural reason anon sees nothing without an explicit anon policy.

The composite-FK guarantee from Phase 4 is what makes a **single** denormalized predicate safe: because `child.account_id` can never disagree with its parent's `account_id`, a per-table `account_id` check is sufficient and cannot be bypassed by re-parenting.

---

## 1. Exact rollout order by table

Order is chosen so that (a) the policy backbone is correct before anything depends on it, (b) each table is validated in isolation before the next is opened, and (c) the highest-risk public surface (`share_links`) is last among writes. Each table default-denies until its own policy lands, so ordering governs **correctness of dependencies**, not exposure windows.

| Step | Table | Class | Why here |
|---|---|---|---|
| 0 | *(verify helpers + RLS-enabled status on all 16 tables)* | — | Confirm `SECURITY DEFINER` helpers resolve; confirm RLS is ON (deny-all) everywhere before adding any permissive policy |
| 1 | `accounts` | structural | The object every membership and profile points at; must be readable before profiles make sense |
| 2 | `account_memberships` | structural | Backs `app_account_ids()`. Helper is `SECURITY DEFINER` so its own RLS cannot break the helper; add policies here before relying on member visibility |
| 3 | `profiles` | root | Single source of truth for `account_id`; all child reads are meaningless until profiles is scoped |
| 4 | `birth_records` | profile-owned | First child — full pattern proven on the most sensitive owned table |
| 5 | `intention_profiles` | profile-owned | |
| 6 | `current_location_history` | profile-owned | |
| 7 | `location_events` | profile-owned | |
| 8 | `favorite_places` | profile-owned | |
| 9 | `visited_places` | profile-owned | |
| 10 | `saved_searches` | profile-owned | |
| 11 | `comparison_sets` | profile-owned **and** FK target | Must be scoped before its set-owned child |
| 12 | `comparison_set_places` | set-owned | Depends on `comparison_sets` being scoped (step 11) |
| 13 | `notes` | profile-owned | |
| 14 | `user_settings` | account-direct + optional profile | Dual shape (account-level + per-profile) handled after simple children |
| 15 | `share_links` | profile-owned **+ public surface** | Last owned table; pairs with the public-read RPC (§4) |
| 16 | `places` | global | Read-only reference; opened last, independent of account scope |
| 17 | `profile_relationships` | **excluded from 0–4 (no `account_id`)** | Decision required (§8.J). Default action: leave default-deny |

The public-read RPC for share links (§4) is created **immediately after step 15** and validated as part of the same step.

---

## 2. Exact policies required

Notation: each policy is `(command, role-target, USING predicate, WITH CHECK predicate)`. `authenticated` and `anon` are the Postgres/Supabase grant roles; membership roles (`owner/admin/member/assistant/viewer`) are tested via `app_has_account_role`. No SQL — predicates stated logically.

**Write-role set (reused below):**
- `WRITE_ROLES = {owner, admin, member, assistant}` — can CRUD account data.
- `SHARE_ROLES = {owner, admin, member}` — can create/manage external shares (assistant excluded per role matrix).
- `MANAGE_ROLES = {owner, admin}` — can manage members.
- `OWNER_ONLY = {owner}` — destructive account-level ops.

### 2.1 Structural tables

**`accounts`**
- SELECT · authenticated · USING `id IN (SELECT app_account_ids())`
- INSERT · authenticated · WITH CHECK `created_by = auth.uid()` *(self-authored; the matching `owner` membership is created by the Phase 6 signup function, not here)*
- UPDATE · authenticated · USING + CHECK `app_has_account_role(id, MANAGE_ROLES)`
- DELETE · authenticated · USING `app_has_account_role(id, OWNER_ONLY)`

**`account_memberships`**
- SELECT · authenticated · USING `account_id IN (SELECT app_account_ids())` *(a user always sees their own membership because that account is in their set)*
- INSERT · authenticated · WITH CHECK `app_has_account_role(account_id, MANAGE_ROLES)`
- UPDATE · authenticated · USING + CHECK `app_has_account_role(account_id, MANAGE_ROLES)`
- DELETE · authenticated · USING `app_has_account_role(account_id, MANAGE_ROLES)`
- *Recursion note:* these policies query `app_account_ids()`/`app_has_account_role`, which read `account_memberships` **as definer** (RLS bypassed inside the function). No policy recursion occurs.

### 2.2 Root + profile-owned children (steps 3–13, 15)

Uniform 4-policy pattern, applied identically to `profiles`, `birth_records`, `intention_profiles`, `current_location_history`, `location_events`, `favorite_places`, `visited_places`, `saved_searches`, `comparison_sets`, `notes`:

- SELECT · authenticated · USING `account_id IN (SELECT app_account_ids())`
- INSERT · authenticated · WITH CHECK `app_has_account_role(account_id, WRITE_ROLES)`
- UPDATE · authenticated · USING `app_has_account_role(account_id, WRITE_ROLES)` · CHECK `app_has_account_role(account_id, WRITE_ROLES)`
- DELETE · authenticated · USING `app_has_account_role(account_id, WRITE_ROLES)`

`UPDATE` carries **both** USING (old row must be writable) and WITH CHECK (new row must remain in a writable account) — this blocks moving a row into an account the caller cannot write, independent of the FK.

### 2.3 Set-owned child (step 12)

**`comparison_set_places`** — same 4-policy pattern keyed on its own `account_id` (kept correct by the Phase 4 composite FK to `comparison_sets(id, account_id)`). No join needed.

### 2.4 Account-direct + optional profile (step 14)

**`user_settings`** — same 4-policy pattern keyed on `account_id`. The dual shape (account-level `profile_id IS NULL` vs per-profile) needs **no policy branching**: both rows carry `account_id`, so `account_id IN (SELECT app_account_ids())` covers both. The per-row uniqueness is already enforced by the Phase 4 partial unique indexes, not by RLS.

### 2.5 Public surface (step 15)

**`share_links`** (owner-management policies — public reads do NOT use these; see §4):
- SELECT · authenticated · USING `account_id IN (SELECT app_account_ids())` *(owner sees their own links to manage)*
- INSERT · authenticated · WITH CHECK `app_has_account_role(account_id, SHARE_ROLES)`
- UPDATE · authenticated · USING + CHECK `app_has_account_role(account_id, SHARE_ROLES)`
- DELETE · authenticated · USING `app_has_account_role(account_id, SHARE_ROLES)`
- **No `anon` policy on this table.** Anonymous visitors never select `share_links` directly.

### 2.6 Global reference (step 16)

**`places`**:
- SELECT · authenticated · USING `true` *(all reference rows readable to any logged-in user)*
- No INSERT/UPDATE/DELETE policies → writes impossible via publishable key; ingestion runs as service-role (RLS bypassed).
- `anon` SELECT: **deferred** (see §5 and §8.I).

### 2.7 Excluded table (step 17)

**`profile_relationships`** — has no `account_id` (excluded from Phase 0–4). **Default action: add no policy** → remains default-deny → invisible/unusable under the publishable key (safe). Promoting it to account scope requires first adding `account_id` (a Phase 4-style change) and is **out of scope** for Phase 5. Flagged for decision in §8.J.

---

## 3. Public vs authenticated vs owner access matrix

"Owner" below means *any writing member of the owning account* unless a stricter membership role is named.

| Table | anon (no session) | authenticated, non-member | authenticated, member (read) | authenticated, write-role | Notes |
|---|---|---|---|---|---|
| `accounts` | — | — | own accounts (SELECT) | UPDATE: admin+; DELETE: owner | INSERT: self (`created_by`) |
| `account_memberships` | — | — | own-account rows | manage: admin+ | |
| `profiles` | — | — | account rows | CRUD: write-roles | |
| 10 profile-owned children | — | — | account rows | CRUD: write-roles | viewer = read-only |
| `comparison_set_places` | — | — | account rows | CRUD: write-roles | |
| `user_settings` | — | — | account rows | CRUD: write-roles | account-level + per-profile both covered |
| `share_links` (direct) | — | — | own-account rows | manage: share-roles | assistant cannot share |
| `share_links` (via RPC) | sanitized payload by slug | same | same | same | §4 — not table RLS |
| `places` | deferred (default —) | all rows | all rows | — (no write) | service-role ingests |
| `profile_relationships` | — | — | — (default-deny) | — | §8.J decision |

`—` = no access. Anonymous access exists **only** through the share RPC (§4); everything else requires an authenticated session whose membership places the row's `account_id` in `app_account_ids()`.

---

## 4. Share-link architecture

**Problem:** RLS is row-grained, not field-grained. `share_links` carries `hide_birth_data`, `include_notes`, `include_tables`, `include_chart_wheel`. A raw anon SELECT on `share_links` (and a join to `birth_records`) cannot enforce those flags — it would expose the full row. Therefore **public reads must not touch the tables directly.**

**Design — single `SECURITY DEFINER` RPC as the only anonymous read path:**

1. **Function** `get_shared_chart(slug text)` — `SECURITY DEFINER`, pinned `search_path`, granted to `anon` + `authenticated`.
2. **Gate checks inside the function (all must pass, else return empty/not-found):**
   - `share_links.slug = input`
   - `visibility <> 'private'` (i.e. `unlisted` or `public`)
   - `revoked_at IS NULL`
   - `expires_at IS NULL OR expires_at > now()`
3. **Field assembly (whitelist, never `SELECT *`):** the function returns only the fields permitted by the link's flags:
   - `hide_birth_data = true` → omit exact birth time/coordinates; return only what the share contract allows.
   - `include_notes`, `include_tables`, `include_chart_wheel` → include those sections only when true.
4. **No direct grants** to anon on `share_links`, `birth_records`, `profiles`, or any owned table. The RPC is the sole anonymous surface.

**Visibility semantics (enforced in RPC/app, not RLS):**
- `private` — never returned by the RPC; owner-only via authenticated table policy.
- `unlisted` — returned by the RPC for anyone holding the exact slug; not enumerable.
- `public` — same as unlisted for the RPC; may additionally be surfaced in listing features later. The distinction is **discoverability**, not access mechanism.

**Why definer, not a permissive anon RLS policy:** a definer function bounds the exposed columns in code and can branch on the flags; an RLS policy can only filter rows. Sanitization is a code concern, so it lives in the function.

**Owner side stays on RLS:** creating, editing, revoking links is the authenticated `share_links` policy set (SHARE_ROLES). Assistant role is intentionally excluded from sharing.

---

## 5. Places-table access model

- **`places` is global reference data**, not account-scoped (no `account_id`; explicitly untouched in Phase 0–4).
- **Read:** `authenticated · SELECT · USING true`. Every logged-in user can read all places (city search, map labels, comparison picking).
- **Write:** **no policies** → no publishable-key writes. The geocoding/ingestion pipeline runs as **service-role**, which bypasses RLS. This matches "writes restricted to service role" from the plan.
- **Anonymous read — deferred decision (§8.I):** logged-out share pages get their place data **through the share RPC** (which is definer and can read `places` server-side), so anon does **not** need a direct `places` read policy for v1. Recommendation: **do not** grant anon SELECT on `places` in Phase 5; revisit only if a public, non-share map page is built.
- **Regression obligation (from Sequence charter #5):** Phase 5 must leave `places` *readable*, not broken. The authenticated read policy satisfies this; the existing 21 reference rows must remain selectable under a real session.

---

## 6. Publishable-key validation plan

All authorization tests use the **publishable (anon) key under a real user session** — never the service-role key (service-role bypasses RLS and would give false passes). This is the non-negotiable distinction from the Sequence charter (#7).

**Test harness setup (staging only):**
- Create **two real auth users** via Supabase Auth: **User A**, **User B**. (Phase 6 owns the signup flow; for Phase 5 testing, users may be seeded directly in `auth` + a definer helper that creates an account + owner membership, used as **test fixture only**.)
- Account A owned by User A; Account B owned by User B.
- Seed each account with one profile + a representative child row in each of the 13 tables (via service-role for setup speed — setup is not an authz test).

**Validation classes:**

| Class | Key used | Asserts |
|---|---|---|
| **Default-deny baseline** | anon (no session) | every account-scoped table returns 0 rows |
| **Owner read** | A's session (publishable) | A sees exactly A's rows in all 13 tables |
| **Owner write** | A's session | A can INSERT/UPDATE/DELETE in A's account; trigger fills `account_id`; FK + policy both hold |
| **Cross-tenant read** | A's session | A sees **0** of B's rows (§7) |
| **Cross-tenant write** | A's session | A cannot INSERT/UPDATE a row into B's `account_id` (policy WITH CHECK denies; FK also denies) |
| **Role gating** | a `viewer` membership session | SELECT works; INSERT/UPDATE/DELETE denied |
| **Share private** | anon via RPC | `private`/revoked/expired slug → empty; `birth_records` never directly selectable |
| **Share public/unlisted** | anon via RPC | valid slug → sanitized payload honoring `hide_birth_data`/`include_*` |
| **Places read** | A's session | all reference rows returned; no write permitted |
| **Service-role caveat** | service-role | documented as bypass; **excluded** from all authz assertions |

Each test runs against staging; data-mutating tests wrap in a transaction rolled back where practical, or clean up by id (as in Phase 4 testing).

---

## 7. User A vs User B isolation tests

The single most important Phase 5 proof (charter #2). Concrete matrix, all executed under **publishable-key sessions**:

| # | Actor (session) | Action | Expected |
|---|---|---|---|
| 1 | A | SELECT each of 13 tables | only A's rows; count matches A's seed |
| 2 | A | SELECT each table filtered to B's known ids | **0 rows** |
| 3 | B | SELECT each of 13 tables | only B's rows |
| 4 | B | SELECT A's known ids | **0 rows** |
| 5 | A | UPDATE a B-owned row by id (set any field) | **0 rows affected** (invisible → not matched) |
| 6 | A | DELETE a B-owned row by id | **0 rows affected** |
| 7 | A | INSERT a child with `account_id = B` | **denied** (policy WITH CHECK + composite FK) |
| 8 | A | UPDATE an A-owned row, set `account_id = B` | **denied** (WITH CHECK + FK) |
| 9 | A | call `app_account_ids()` | returns only A's account id(s); never B's |
| 10 | Non-member C (3rd session) | SELECT A's account profiles | **0 rows** |
| 11 | A invites C as `member`; C | SELECT A's profiles | rows visible (account membership works) |
| 12 | A invites D as `viewer`; D | SELECT then UPDATE A's profile | SELECT ok; UPDATE **denied** |

Pass condition: tests 2, 4, 5, 6, 7, 8, 10 return zero rows / denials; tests 1, 3, 9, 11 succeed with exact-match counts; test 12 reads but cannot write.

---

## 8. Failure modes

| # | Failure | Direction | Mitigation |
|---|---|---|---|
| A | **Forgotten policy** on a new/owned table | Table default-denies → app breaks (loud, safe) | Schema-lint: every owned table must have all 4 policies before sign-off; CI check on policy count per table |
| B | **Over-permissive policy** (e.g. `USING true` on an owned table) | Cross-tenant leak (silent, dangerous) | Review every predicate against the boundary primitive (§0); the A-vs-B suite (§7) catches it |
| C | **`account_memberships` policy recursion** | Helper fails / infinite recursion | Helpers are `SECURITY DEFINER` and bypass RLS internally — confirmed by design; never call non-definer membership lookups inside a policy |
| D | **`search_path` hijack** of a definer helper | Privilege confusion | `search_path` pinned on all definer functions (Phase 1 + RPC); re-verify in step 0 |
| E | **Service-role key shipped to browser** | Total RLS bypass | Never expose service key client-side; only publishable key in app; out-of-band ops use server context |
| F | **RPC returns `SELECT *`** / ignores flags | Field-level leak on public shares | RPC whitelists columns and branches on `hide_birth_data`/`include_*`; tested in §6 share tests |
| G | **RPC skips revoked/expired/private checks** | Stale or private link readable | All four gate checks mandatory inside the function; explicit tests for revoked + expired + private |
| H | **Viewer can write** (missing role gate) | Unauthorized mutation | Write policies use `app_has_account_role(..., WRITE_ROLES)`, not bare membership; test 12 proves it |
| I | **Anon SELECT granted on `places`** unnecessarily | Broader-than-needed exposure of reference data | Default: no anon `places` policy; share data flows through the definer RPC instead |
| J | **`profile_relationships` left ambiguous** | Either silently unusable, or (if hastily policy'd by a `profiles` join) a mis-scoped leak | Default-deny in Phase 5; promoting it requires adding `account_id` first — explicitly deferred, not improvised |
| K | **`anon`/NULL `auth.uid()`** in a predicate | Unintended match if predicate mishandles NULL | `account_id IN (SELECT app_account_ids())` yields empty set for anon → denies; no special-casing needed, but confirm no policy uses `OR auth.uid() IS NULL` |
| L | **New table added later** without RLS | Default-deny if RLS on; **full-open if RLS forgotten** | Standing rule: enabling RLS is step 0 for any new owned table; lint for `relrowsecurity = true` on all `public` tables |

---

## 9. Rollback strategy

**Principle:** policies and the RPC are additive and non-destructive to data. The **only** dangerous rollback action is `DISABLE ROW LEVEL SECURITY`, which removes row filtering and **opens** a table — so rollback **drops policies but keeps RLS enabled** (reverting each table to default-deny), never disables RLS.

**Per-table rollback (reverse of §1 rollout order):**
1. `profile_relationships` — nothing to undo (no policy added).
2. `places` — drop the authenticated SELECT policy (table returns to default-deny; reference reads stop, app degrades safely).
3. `share_links` — drop the 4 management policies; **drop the `get_shared_chart` RPC** (public read path closes).
4. `user_settings` → `comparison_set_places` → `comparison_sets` → ... → `profiles` — drop their 4 policies each, in reverse dependency order.
5. `account_memberships`, then `accounts` — drop their policies last (the backbone), so nothing relies on member visibility mid-rollback.
6. **Leave RLS ENABLED on every table** throughout. End state = the Phase 4 close state (RLS on, zero policies, publishable key returns 0 rows).

**Helpers:** `app_account_ids()` / `app_has_account_role()` are **not** dropped on Phase 5 rollback — they are Phase 1 objects and other phases depend on them.

**Data:** no data is altered by Phase 5; rollback touches policy/function objects only. Test fixtures (Users A/B, seeded rows) are cleaned by id, as in Phase 4.

**Scope:** staging only. No production policy is created or dropped in this phase.

---

## Phase 5.5 — Human Review Gate (must all be green before Phase 6)

| # | Gate | Source |
|---|---|---|
| 1 | A-vs-B isolation: all 12 checks pass | §7 |
| 2 | Role gating: viewer read-only proven | §7 test 12 |
| 3 | Non-member sees 0; invited member sees rows | §7 tests 10–11 |
| 4 | Share RPC: private/revoked/expired → empty | §4, §6 |
| 5 | Share RPC: public/unlisted → sanitized payload honoring flags | §4, §6 |
| 6 | `places` readable (authenticated), not writable | §5 |
| 7 | Every owned table has all 4 policies; RLS enabled on all `public` tables | §8.A, §8.L |
| 8 | All authz tests used publishable key; service-role used only for setup/integrity | §6 |

Only when all eight are green on staging may Phase 6 (auth + first real user) proceed. **No production changes, no auth wiring, no frontend in this phase.**
