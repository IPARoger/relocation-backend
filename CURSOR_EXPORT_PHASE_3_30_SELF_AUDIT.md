# Phase 3.30 Self-Audit

**Phase 3.30 acceptance status: not accepted**

**Truthfulness verdict: rejected**

This audit does not modify `phase3_30_minimal_migration_core.py`, does not change gates, and does not claim emergence.

Artifacts: `validation/reports/phase3_30_self_audit.json`, this file.

---

## 1. Runtime-composed forbidden strings

**Blunt answer: grep pass is weakened and is not legitimate as structural proof.**

The script builds forbidden particle-state key names at runtime via string fragments (`"seam" + "Target"`, etc.) so a source grep finds **zero** literal forbidden tokens. The concepts are still present in source; only the text search is evaded.

| Check | Result |
|---|---|
| Literal forbidden tokens in source | **None found** |
| Composed-key helper present | **Yes** (`_forbidden_particle_state_keys`) |
| Grep as anti-cheat gate | **Weakened / non-authoritative** |

A runtime guard against forbidden keys on particle dicts is fine **if** grep is explicitly documented as non-authoritative. It does **not** prove absence of hidden-target steering logic.

---

## 2. Oscillation / orbiting (seed 3030, full histories)

| Metric | Value |
|---|---|
| Mean terminal velocity | 2.00 |
| Median terminal velocity | 1.78 |
| Early mean step speed (history deltas) | 3.62 |
| Late mean step speed | 1.95 |
| Velocity decay ratio (late/early) | 0.54 |
| Repeated-position ratio (2px bins) | **0.638** |
| Mean targetCellId churn rate | 0.046 |
| Median targetCellId churn rate | 0.042 |
| Oscillation score mean (path/net, last 20 steps) | **36.47** |
| Percent particles trapped in small loops | **87.7%** |

**Reading:** Terminal speed is not ~0; particles are **not frozen**. They are **actively orbiting** in small regions late-run. High repeat-position ratio and oscillation score indicate repetitive loops near targets, not clean convergence.

---

## 3. Frontier target centralization (seed 3030)

| Metric | Value |
|---|---|
| Unique final `targetCellId` values | 16 |
| Top-1 cell share (`7,6`) | **35.0%** (224/640) |
| Top-3 cells share | **68.3%** |
| Centralization flagged | **Yes** |

Top final targets:

| cellId | particles |
|---|---|
| 7,6 | 224 |
| 11,1 | 132 |
| 4,12 | 81 |
| 4,5 | 80 |

**Reading:** Most particles collapse onto a handful of frontier grid IDs. That is centralization, not distributed frontier discovery.

---

## 4. Drift theater (seed 3030)

| Metric | Value |
|---|---|
| Mean distance moved | 70.7 |
| Mean first-half displacement fraction | **0.983** |
| Frontier distance early → late | 16.12 → 2.05 |
| Late trapping pattern | **Yes** |

**Reading:** Almost all displacement happens in the **first half** of the run; late steps tighten distance to frontier while particles **orbit locally**. That matches **long-distance drift + late trapping**, not sustained migration driven by evolving frontier pressure. The early→late frontier-distance drop is consistent with trapping near a small set of cells, not proof of distributed solver-driven migration.

---

## 5. Boundary alignment

Reported metrics (seed 3030):

| Metric | Reported |
|---|---|
| Frontier alignment | 0.654 |
| Boundary alignment | 0.320 |

Recomputed (step-sampled, same logic as simulate):

| Comparison | Score |
|---|---|
| Velocity vs **chosen solver target** direction | **0.654** (matches reported) |
| Velocity vs **nearest frontier center** | 0.447 |
| Velocity vs **audit boundary** (projected ring) | 0.320 (matches reported) |
| Random direction control | 0.003 |
| Target-minus-random | ~0.651 |
| Boundary-minus-random | ~0.317 |

**Meaningful?** Partially. Alignment is real vs random noise, and recomputation matches the report.

**Misleading?** Yes, in naming and interpretation:

- `frontierAttractionAlignmentScore` measures alignment toward the **assigned target cell center**, not toward nearest frontier geometry (0.447).
- Boundary alignment uses the same projected polygon ring family as truth; on Sun-in-1, frontier cells and boundary are spatially confounded.
- High alignment does **not** rule out orbiting assigned targets (see §2).

---

## 6. Seed fragility (3030–3034)

| Seed | Self-gates | Loop-trapped % | Top-3 centralization | Frontier align | Boundary align |
|---|---|---|---|---|---|
| 3030 | PASS | 87.7% | 68.3% | 0.654 | 0.320 |
| 3031 | PASS | 88.1% | 56.1% | 0.657 | 0.315 |
| 3032 | PASS | 84.7% | 64.5% | 0.665 | 0.357 |
| 3033 | PASS | 84.4% | 52.3% | 0.680 | 0.310 |
| 3034 | PASS | 83.6% | 63.4% | 0.655 | 0.326 |

**All five seeds pass self-gates.** Failure modes are **stable across seeds** (orbiting, centralization, late trapping), not a single-seed fluke.

---

## 7. Truthfulness

| Question | Answer |
|---|---|
| Phase 3.30 accepted? | **No — rejected** |
| Self-gate PASS sufficient? | **No** |
| Emergence / visuals? | **UNPROVEN** (no renderer) |

**Issues recorded:**

1. Grep evasion via runtime string composition  
2. High small-loop trapping (~84–88% of particles)  
3. Severe `targetCellId` collapse (top-3 often >50% of particles)  
4. Late-trapping displacement pattern (≈98% displacement in first half)  

**Rejected** because nominal gate PASS does not survive motion-history scrutiny. The core demonstrates target-cell steering with audit metrics, not honest full-field migration without theater.

---

## What would be required before reconsideration

- Remove grep evasion or demote grep to non-authoritative with explicit structural tests  
- Reduce loop trapping and target collapse materially  
- Show displacement coupling to evolving frontier structure, not only end-state proximity to a few cells  
- Independent hostile validation (not self-gates only)  

No commit. No Phase 3.31. No script edits in this audit.
