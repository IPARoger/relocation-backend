# Phase 3.35 — Black-Box Acceptance Harness (External)

**Date:** 2026-05-28  
**Verdict:** **FAIL**  
**Accepted for visual prototyping:** **No**  
**Emergence claimed:** No

---

## Purpose

End the cat-and-mouse pattern where the solver self-certifies PASS. Phase 3.35 runs the current Phase 3.31 mechanics (`validation/scripts/phase3_30_minimal_migration_core.py`) **as-is** but computes acceptance only from **raw particle histories** and **raw `truth(point)`** checks. All solver self-reported PASS booleans, report claims, and retired metrics are ignored.

**No solver changes in this phase.** No visuals. No commit.

---

## Artifacts

| Artifact | Path |
|----------|------|
| Harness | `validation/scripts/phase3_35_black_box_acceptance.py` |
| Report | `validation/reports/phase3_35_black_box_acceptance_against_current.json` |
| Export | `CURSOR_EXPORT_PHASE_3_35_BLACK_BOX_ACCEPTANCE.md` |

---

## Method

1. Import Phase 3.31 solver module via `importlib` (mechanics loop replicated with injected `truth(point)` oracle only).
2. **20 unknown geometries** (synthetic canvas polygons; solver never defines them).
3. **Seeds 4000–4029** (30 seeds × 20 geometries = **600 runs**).
4. Black-box metrics computed independently from histories + frontier cell centers.
5. **`nearestFrontierVelocityAlignment`**: velocity vs vector to **nearest frontier cell center** at the post-pull sample point (before late frontier steering). **Not** chosen-target alignment. **`frontierAttractionAlignmentScore` is retired and unused.**

---

## Unknown geometry set (20)

| Geometry | Family |
|----------|--------|
| circle | round |
| ellipse | round |
| rectangle | rectilinear |
| thin_ribbon | ribbon |
| diagonal_ribbon | ribbon |
| crescent | concave |
| fjord | concave |
| donut | ring |
| single_island | island |
| two_islands | island |
| three_islands | island |
| noisy_blob | organic |
| small_compact | round |
| wide_band | ribbon |
| s_curve | organic |
| split_corridor | corridor |
| off_center_shape | placement |
| shape_near_edge | placement |
| fragmented_field | fragmented |
| negative_space_frame | ring |

---

## Fixed black-box gates (not tuned after results)

| Gate | Threshold |
|------|-----------|
| initialCoverage | ≥ 0.70 |
| particleMigrationFraction | ≥ 0.35 |
| frontierDistanceDelta | > 0 |
| nearestFrontierVelocityAlignment | ≥ 0.15 |
| targetCentralizationTop1 | ≤ 0.12 |
| targetCentralizationTop3 | ≤ 0.30 |
| uniqueTargetCells | ≥ 40 |
| loopTrapFraction | ≤ 0.25 |
| oscillationScore | ≤ 6 |
| repeatedPositionRatio | ≤ 0.25 |
| firstHalfDisplacementFraction | ≤ 0.70 |

**Global gates:**

- ≥ 70% of geometries must pass (≥ 70% of seeds per geometry pass all per-run gates)
- No geometry family may have 0% pass rate
- Metrics must vary materially by geometry (relative spread ≥ 0.10 on key metrics)

---

## Overall result

| Field | Value |
|-------|-------|
| **overallVerdict** | **FAIL** |
| **acceptedForVisualPrototyping** | **false** |
| Runs passing all per-run gates | **0 / 600** |
| Geometries passing (≥ 70% seeds) | **0 / 20** |
| Seed pass rates | **0.0** for all seeds 4000–4029 |

### Global failure reasons

1. `geometry_pass_fraction 0.000 < 0.7`
2. `geometry_families_with_zero_pass_rate`: round, rectilinear, ribbon, concave, ring, island, organic, corridor, placement, fragmented

### Geometry sensitivity (material variation — met)

| Metric | Relative spread across geometry means |
|--------|--------------------------------------|
| nearestFrontierVelocityAlignment | **8.03** |
| frontierDistanceDelta | **0.56** |
| particleMigrationFraction | **0.54** |

Metrics **do** vary by geometry, but **no geometry or seed achieves black-box PASS** under the fixed gates.

---

## Dominant per-run failure reasons (600 runs)

| Failure | Count |
|---------|-------|
| `nearestFrontierVelocityAlignment >= 0.15` | **600** (every run) |
| `repeatedPositionRatio <= 0.25` | 470 |
| `firstHalfDisplacementFraction <= 0.70` | 365 |
| `particleMigrationFraction >= 0.35` | 299 |
| `frontierDistanceDelta > 0` | 7 |
| `oscillationScore <= 6` | 2 |

---

## Mean black-box metrics by geometry (selected)

| Geometry | Pass rate | nearestFrontierVelocityAlignment | particleMigrationFraction | frontierDistanceDelta |
|----------|-----------|----------------------------------|---------------------------|------------------------|
| diagonal_ribbon | 0.00 | 0.0288 | 0.451 | 3.94 |
| donut | 0.00 | -0.0054 | 0.409 | 4.05 |
| thin_ribbon | 0.00 | 0.0151 | 0.356 | 4.16 |
| circle | 0.00 | -0.0062 | 0.316 | 4.11 |
| rectangle | 0.00 | 0.0123 | 0.319 | 4.01 |
| fjord | 0.00 | 0.0029 | 0.297 | 3.82 |

**All geometry means:** `nearestFrontierVelocityAlignment` ∈ roughly **[-0.015, 0.036]** — far below the **0.15** gate. This is the intended hostile outcome: velocity is **not** aligned with motion toward the nearest discovered frontier cell.

`frontierDistanceDelta` is positive on most runs (mean distance to nearest frontier decreases early→late), but that alone does not satisfy acceptance.

---

## Conclusions

1. **External black-box harness is in place** and cannot be self-certified by the solver.
2. **Current Phase 3.31 solver FAILS** all 600 black-box runs under fixed gates.
3. **`nearestFrontierVelocityAlignment` remains near zero** across every geometry and seed — consistent with Phase 3.33 deconstruction (chosen-target pull ≠ frontier-responsive migration).
4. **Do not proceed to visual prototyping** on this solver until a future mechanics phase addresses black-box failures (not in Phase 3.35).
5. **No emergence claim.** Expected failure is acceptable; no solver patch in this phase.

---

## Reproduce

```bash
./venv/bin/python validation/scripts/phase3_35_black_box_acceptance.py
```

Report written to `validation/reports/phase3_35_black_box_acceptance_against_current.json`.
