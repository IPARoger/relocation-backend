# Chat 5 Closure Audit

**Roadmap ID:** Chat 5 Closure Audit  
**Checkpoint:** `3bb5905` — `C5-6: remove unused back-compat state proxy`  
**Date:** 2026-06-18  
**Mode:** Read-only — no source modifications, no commits

---

## Per-Slice Status

| Slice | Status | Evidence | Verification |
| ----- | ------ | -------- | ------------ |
| C5-1 | **COMPLETE** | `results/68_c5_1_dead_code_audit.md` — read-only dead-code inventory; priority queue for C5-2..C5-6 | **VERIFIED** — grep-only audit; no product edits |
| C5-2 | **BLOCKED** | `results/69_c5_2_dead_helper_removal.md` — NOT VERIFIED; hard stop on `_deprecated_legacy_write` | **NOT VERIFIED** (intentional pause). At `3bb5905`: **26** refs in `main_centerline_FIXER.py` (25 shim call sites + definition). Deletion would break 25 legacy-write 410 routes |
| C5-2a | **COMPLETE** | `e56a40f` — removed 6 confirmed-dead functions; `results/69b_c5_2a_narrow_removal.md` | **VERIFIED** — 6× `# removed: … C5-2a` tombstones; `smoke_legacy_writes_deprecated.py` 25/25 PASS at closeout |
| C5-3 | **BLOCKED** | `results/70_c5_3_bridge_helpers.md` — NOT VERIFIED; `toConfidenceTier`, `toRecordType`, `trimTime` live inside `buildSupabaseStore` / `refreshProfile` | **NOT VERIFIED** (intentional pause). At `3bb5905`: each helper has **2** internal call sites in `supabase_store_bridge.js` (lines 395–633) |
| C5-4 | **COMPLETE** | `f84072a` — `results/71_c5_4_legacy_map_audit.md` — read-only legacy map block inventory | **VERIFIED** — `LEGACY_SEARCH_REGIONS`, `buildPlanFromLegacyDom()`, shadow suite reclassified **LIVE**; only marginal dead items flagged |
| C5-4a | **COMPLETE** (scoped partial) | `2363b32` / `49abf86` — `results/72_c5_4a_quarantine_dead_renderer.md` | **VERIFIED** — empty quarantined `renderBellAuraBandsAroundLine` stub retained at `map_CURRENT.html:4676` (0 callers); `CANONICAL_RENDERER_BRANCH_ACTIVE` correctly kept **LIVE**; `smoke_map_current.py` PASS at closeout |
| C5-5 | **COMPLETE** | `75a3443` — `results/79_c5_5_orb_defaults_write.md` | **VERIFIED** — `settingsPatch.orb_defaults` write removed; read fallback `eff.major_aspect_orbs \|\| eff.orb_defaults` retained at `app_shell.html:1738`. **Re-run 2026-06-18:** `smoke_settings_account.py` PASS (17/17) |
| C5-6 | **COMPLETE** | `3bb5905` — `results/80_c5_6_back_compat_state_removal.md` | **VERIFIED** — back-compat `const state` proxy and `__rmAppShell.state` export removed; `navContext` / `uiState` canonical. **Re-run 2026-06-18:** `smoke_app_shell_context_transport.py` PASS; `smoke_app_shell_map_handoff.py` PASS |

**Note:** C5-7 (`results/81_c5_7_candidate_audit.md`) was a read-only candidate audit only — not an approved implementation slice. Per closure charter, no C5-7/C5-8 work is created here.

---

## Specific Verification Checks

### 1. C5-2 remains legitimately blocked

**Yes.** `_deprecated_legacy_write` is the shared 410 gate for 25 JWT-era legacy write routes exercised by `smoke_legacy_writes_deprecated.py`. Caller grep at checkpoint: **26** matches (definition + 25 shims). C5-2 closeout correctly triggered hard stop; C5-2a safely removed only the 6 zero-caller stubs without touching the shim infrastructure.

### 2. C5-3 remains legitimately blocked

**Yes.** All three helpers are called from live exported bridge paths (`buildSupabaseStore`, profile refresh). Removing them requires inlining across live data-mapping code — a refactor, not dead-code deletion. C5-3 closeout correctly marked NOT VERIFIED.

### 3. No unresolved regressions from C5-5 or C5-6

**None observed.**

| Change | Targeted smoke | Re-run result |
|--------|----------------|---------------|
| C5-5 orb_defaults write removal | `smoke_settings_account.py` | PASS |
| C5-6 state proxy removal | `smoke_app_shell_context_transport.py`, `smoke_app_shell_map_handoff.py` | PASS |

Grep confirms intended post-state: no `settingsPatch.orb_defaults` write; no `__rmAppShell.state` or back-compat `const state` block in `app_shell.html`.

### 4. All recovery smokes are green

**Yes** at audit time (2026-06-18, `.env.staging`, port 8004):

| Smoke | Result |
|-------|--------|
| `smoke_settings_account.py` | PASS |
| `smoke_app_shell_context_transport.py` | PASS |
| `smoke_app_shell_map_handoff.py` | PASS |
| `smoke_legacy_writes_deprecated.py` | 25/25 PASS |
| `smoke_map_current.py` | PASS (`overall_pass: true`) |
| `smoke_favorites.py` | PASS (17/17; one retry after transient archive-detach flake) |
| `smoke_comparison_sets.py` | PASS (13/13) |

No smoke failure attributable to C5-5 or C5-6 product diffs.

### 5. Governance files accurately reflect current reality

**No — stale.** At `3bb5905`:

| File | Drift |
|------|-------|
| `relay/ROADMAP_QUEUE.md` | Header still emphasizes Chat 4 closure; Chat 5 marked **READY (CURRENT)**; C5-7+ listed **NEXT** despite C5-5/C5-6 complete |
| `relay/CHAT_INSTRUCTIONS.md` | Chat 5 marked **ACTIVE** — "resume C5-5+"; does not record Chat 5 completion |

C5-2 caller count in governance says "24 shim callers"; current grep is 25 shims + definition (26 refs) — minor numeric drift, same hard stop.

### 6. No previously approved Chat 5 slice remains partially implemented

**None.**

- C5-2 / C5-3: blocked before product edit — no partial deletion.
- C5-4a: intentionally scoped to quarantine (empty stub retained as rollback surface) — closeout VERIFIED as partial scope, not incomplete work.
- C5-5 / C5-6: fully committed and smoke-verified.

---

## Remaining Cleanup Inventory

| Item | Classification | Rationale |
|------|----------------|-----------|
| `_deprecated_legacy_write` + 25 legacy-write 410 shims | **BLOCKED** | Live gate; C5-2 hard stop; needs migration spec |
| `toConfidenceTier`, `toRecordType`, `trimTime` | **BLOCKED** | Live bridge internals; C5-3 hard stop |
| `LEGACY_SEARCH_REGIONS`, `buildPlanFromLegacyDom()`, shadow comparison suite | **LIVE** | Production renderer / search substrate |
| `CANONICAL_RENDERER_BRANCH_ACTIVE` | **LIVE** | Smoke telemetry field |
| Bridge/resolver `orb_defaults` read mirrors | **LIVE** | Legacy row compatibility (C5-5 removed app_shell write only) |
| `__rmAppShell.getProfiles`, `activeRecord`, drawer hooks | **LIVE** | `account_drawer.js` production callers |
| `renderBellAuraBandsAroundLine` empty stub | **ARCHAEOLOGY** | 0 callers; C5-4a rollback surface; marginal delete only |
| `# removed: … C5-2a` tombstone comments (6×) | **ARCHAEOLOGY** | Comment-only; zero runtime effect |
| `getSelectedChartRecordId`, `uiState`, other zero-caller `__rmAppShell` exports | **ARCHAEOLOGY** | Test-hook surface; marginal micro-cleanup |
| `smoke_account_store_read.py` expects 410 on deleted `/account-store` | **OUT OF SCOPE** | Smoke hygiene (route returns 404 post-C5-2a); not Chat 5 product debt |
| Megacommit hygiene (`816ecfe`, `ccb0287`) | **OUT OF SCOPE** | Process debt; not incremental dead-code retirement |
| Product features (settings UX, city search, port 8000, etc.) | **OUT OF SCOPE** | Product track per roadmap |

No new roadmap slices created from this inventory.

---

## Closure Decision

### A. CHAT 5 COMPLETE

**Why remaining items do not justify continued cleanup work:**

1. **C5-1 priority queue exhausted.** Every confirmed-dead item the audit rated as safe incremental work has been executed (C5-2a, C5-4a quarantine, C5-5, C5-6) or correctly classified LIVE/BLOCKED.
2. **Blocked slices are hard stops, not backlog.** C5-2 and C5-3 require new task specs and multi-route or multi-function migrations — outside the "one small dead-code slice" charter.
3. **Archaeology is marginal.** The empty `renderBellAuraBandsAroundLine` stub and tombstone comments carry near-zero value vs. renderer hard-stop risk.
4. **Live substrate is production code.** `LEGACY_SEARCH_REGIONS`, bridge helpers, and shim infrastructure are intentionally retained.
5. **C5-7 candidate audit** (`results/81_c5_7_candidate_audit.md`) independently reached the same conclusion: end cleanup track; move to product.

No exact remaining **required** slice exists. C5-7 was audit-only and explicitly not approved for implementation.

---

## Governance Recommendation

Apply these edits when governance sync is authorized (not part of this read-only audit):

### `relay/ROADMAP_QUEUE.md`

1. **Status line** — replace Chat 5 READY (CURRENT) with Chat 5 COMPLETE (`3bb5905`); mark **Product track CURRENT**; cite `results/82_chat5_closure_audit.md`.
2. **Chat 5 section header** — `## Chat 5 — Dead Code Retirement & Cleanup ✅ COMPLETE`
3. **Remove C5-7+ NEXT row**; add closure note: C5-2/C5-3 BLOCKED; no further Chat 5 slices planned.
4. **Add closure commits:** `75a3443` (C5-5), `3bb5905` (C5-6).
5. **Product track section** — `## Product track ▶ CURRENT`
6. **Planner rule 1** — Product track CURRENT; Chat 5 COMPLETE; do not retry C5-2/C5-3 without new spec.

### `relay/CHAT_INSTRUCTIONS.md`

Replace **Current roadmap state** with Chat 5 COMPLETE, C5-2/C5-3 BLOCKED notes, **Product track: CURRENT**.

---

## Audit Method

- Read all listed C5 closeouts (`results/68`–`81`)
- Grep verification at checkpoint `3bb5905`
- Re-ran recovery smokes with `.env.staging` (see §4)
- No source files modified except this closeout

---

# VERDICT

CHAT 5 COMPLETE
