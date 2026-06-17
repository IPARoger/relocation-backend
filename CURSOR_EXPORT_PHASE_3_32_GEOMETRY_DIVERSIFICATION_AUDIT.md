# Phase 3.32 Geometry Diversification Hostile Audit

**Overall verdict: FAIL**

**Emergence claimed: false**

**Visuals: UNPROVEN**

Artifacts:

- `validation/scripts/phase3_32_geometry_diversification_audit.py`
- `validation/reports/phase3_32_geometry_diversification_audit.json`

Mechanics: Phase 3.31 (`phase3_30_minimal_migration_core.py`) run unchanged via injected `truth(point)` only. No target geometry coordinates passed to particles.

Seeds: **3030–3039** (10 seeds per geometry)

Geometries: **10** (Sun-in-1, circle, thin diagonal ribbon, two islands, concave crescent, narrow fjord, noisy blob, hollow donut, long coastline strip, small compact island)

---

## Executive conclusions

| Question | Answer |
|---|---|
| Does geometry materially change behavior? | **Yes** — frontier cell counts, pass rates, unique targets, and spatial variance differ strongly by shape. |
| Is the solver overfit only to Sun-in-1? | **No** — Sun pass rate is 80%, but thin diagonal ribbon also 80%; circle/small island/crescent/fjord/blob are 0%. Failure is not Sun-exclusive. |
| Are any metrics suspiciously stable? | **Yes** — `frontierAttractionAlignmentScore` ~0.76±0.01 across all geometries (relative spread **3.5%**). Several other metrics barely move. |
| Evidence for frontier-responsive migration? | **Partial** — frontier tracking ratio ~0.54 and occupancy variance change, but alignment score stability undermines confidence. |
| Passing self-gates sufficient? | **No** — most non-ribbon geometries fail gates on most seeds. |

---

## Test verdicts

| Test | Verdict |
|---|---|
| Multi-geometry robustness | **PASS** (behavior differs materially) |
| Geometry fingerprint audit | **SUSPICIOUS** |
| Motion authenticity audit | **PASS** |
| Frontier dependence audit | **PASS** |
| Seed robustness (cross-geometry gates) | **FAIL** |

---

## Geometry pass rates (seeds 3030–3039)

| Geometry | Pass rate |
|---|---|
| sun_in_1_polygon | 0.80 |
| thin_diagonal_ribbon | 0.80 |
| two_disconnected_islands | 0.20 |
| hollow_ring_donut | 0.30 |
| long_coastline_strip | 0.10 |
| circle | **0.00** |
| concave_crescent | **0.00** |
| narrow_fjord | **0.00** |
| randomized_noisy_blob | **0.00** |
| small_compact_island | **0.00** |

Phase 3.31 self-gates are **not** robust across geometry diversity. Only Sun and thin ribbon pass reliably.

---

## Mean metrics by geometry (seeds averaged)

| Geometry | Frontier align | Frontier cells (mean) | Unique targets | Moved % | Loop % | Repeat ratio | Half-disp frac |
|---|---|---|---|---|---|---|---|
| sun_in_1 | 0.765 | 128 | 124 | 0.477 | 0.0005 | 0.242 | 0.672 |
| circle | 0.766 | 113 | 107 | 0.322 | 0.0006 | 0.258 | 0.750 |
| thin_ribbon | 0.763 | 122 | 118 | 0.448 | 0.0008 | 0.244 | 0.701 |
| two_islands | 0.763 | 119 | 115 | 0.392 | 0.0002 | 0.251 | 0.709 |
| crescent | 0.764 | 126 | 122 | 0.366 | 0.0003 | 0.253 | 0.718 |
| narrow_fjord | 0.748 | 142 | 136 | 0.299 | 0.0006 | 0.261 | 0.743 |
| noisy_blob | 0.766 | 114 | 109 | 0.376 | 0.0006 | 0.254 | 0.740 |
| hollow_donut | 0.758 | 138 | 137 | 0.414 | 0.0009 | 0.250 | 0.693 |
| coastline_strip | 0.760 | 126 | 122 | 0.399 | 0.0006 | 0.252 | 0.703 |
| small_island | 0.775 | 89 | 83 | 0.359 | 0.0005 | 0.258 | 0.728 |

**Suspicious stability:** `frontierAttractionAlignmentScore` stays ~0.75–0.77 regardless of radically different truth shapes. Relative spread **0.035** — far below hostile threshold **0.10**.

Also flagged stable: `repeatedPositionRatio`, `targetSelectionEntropy`, `frontierTrackingRatio`.

**Material variation (good):** `frontierCellCountMean` (89–142), `percentParticlesMovedSignificantDistance` (0.30–0.48), `uniqueFinalTargetCellIds` (83–137).

---

## Strongest evidence FOR geometry dependence

- Frontier cell population shifts by shape (e.g. small island **~89** vs narrow fjord **~142** mean cells).
- Gate pass rates collapse on circle, crescent, fjord, blob, and small island.
- Spatial distribution variance and occupancy variance differ by geometry.

## Strongest evidence AGAINST honest geometry-driven migration

- **Alignment metric is nearly geometry-invariant** — suggests steering statistic may be measuring generic target-cell pull, not shape-specific frontier discovery.
- Five of ten geometries **never pass** self-gates across ten seeds.
- High moved fraction on Sun does not transfer to circle (0% pass) despite similar alignment scores (~0.766).

---

## Interpretation (hostile)

1. The solver is **not merely overfit to Sun-in-1** (ribbon matches Sun pass rate; other shapes fail differently).
2. The solver is **not geometry-agnostic either** — frontier counts and pass rates change with shape.
3. Several headline metrics look **metric-theater stable** while underlying gate success varies wildly. That is suspicious.
4. **Frontier-responsive migration is UNPROVEN as honest discovery** — tracking ratios pass, but near-constant alignment across shapes undermines the claim that particles meaningfully adapt discovery to each geometry.

---

## Status

Phase 3.32 **FAIL** overall. Geometry diversification **breaks** gate compliance on most shapes (expected hostile outcome). Geometry **does** change some behavior, but **stable alignment scores** across diverse truths warrant continued distrust.

No visuals. No emergence claim. No commit.
