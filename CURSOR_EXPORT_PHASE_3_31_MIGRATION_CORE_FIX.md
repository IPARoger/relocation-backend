# Phase 3.31 Migration Core Fix

**Emergence claimed: false**

**Visuals proven: UNPROVEN**

Edited file only: `validation/scripts/phase3_30_minimal_migration_core.py`

Regenerated: `validation/reports/phase3_30_minimal_migration_core.json` (seed 3030)

---

## What changed (mechanics)

| Audit issue | Fix |
|---|---|
| Grep evasion via runtime string composition | Removed. `AUDIT_FORBIDDEN_PARTICLE_STATE_KEYS` is a literal allowlisted tuple; `grepEvasionPresent: false`; `grepStructuralProofClaimed: false` in report. |
| Target-cell collapse (~68% top-3) | Per-step occupancy caps, weighted top-K stochastic target pick, particle-specific bias, dwell-based retarget exclusion. |
| Loop trapping (~88%) | Removed tangential “transit” orbit mode; repeat-bin steering turn; distance-scaled pull. |
| Early move-then-trap (~98% first-half displacement) | `COLD_START_STEPS` local resample phase; post-cold speed damp through step 31; stronger pull after progress 0.58; late frontier-close steering. |

---

## Acceptance gates (fixed thresholds, not tuned post-run)

| Gate | Threshold |
|---|---|
| `centralizationTop1Fraction` | ≤ 0.12 |
| `centralizationTop3Fraction` | ≤ 0.30 |
| `uniqueFinalTargetCellIds` | ≥ 40 |
| `percentParticlesTrappedInSmallLoops` | ≤ 0.25 |
| `oscillationScoreMean` | ≤ 6 |
| `repeatedPositionRatio` | ≤ 0.25 |
| `meanFirstHalfDisplacementFraction` | ≤ 0.70 |
| `initialMacroCellCoverage` | ≥ 0.70 |
| `percentParticlesMovedSignificantDistance` | ≥ 0.35 |
| Frontier distance early → late | must decrease |
| `frontierAttractionAlignmentScore` | > 0 |
| `grepEvasionPresent` | false |

---

## Multi-seed results (3030–3034)

All seeds **PASS** all gates.

| Seed | Verdict | top1 | top3 | unique targets | loop % | osc mean | repeat ratio | half disp frac | moved % |
|---|---|---|---|---|---|---|---|---|---|
| 3030 | PASS | 0.013 | 0.037 | 125 | 0.003 | 2.82 | 0.240 | 0.694 | 0.509 |
| 3031 | PASS | 0.013 | 0.037 | 125 | 0.003 | 2.78 | 0.240 | 0.692 | 0.480 |
| 3032 | PASS | 0.013 | 0.037 | 124 | 0.006 | 2.80 | 0.239 | 0.665 | 0.547 |
| 3033 | PASS | 0.013 | 0.037 | 125 | 0.002 | 2.62 | 0.243 | 0.621 | 0.502 |
| 3034 | PASS | 0.013 | 0.037 | 124 | 0.006 | 2.92 | 0.243 | 0.680 | 0.492 |

---

## Seed 3030 report snapshot

- `overallVerdict`: PASS
- `grepEvasionPresent`: false
- `frontierAttractionAlignmentScore`: positive (see JSON)
- `boundaryTargetAlignmentScore`: audit metric only (projected ring; not a move target)

---

## Honest limits

- This is still a **metrics-only** core. No renderer; migration **appearance** is UNPROVEN.
- Passing self-gates does **not** overturn Phase 3.30 self-audit rejection of “emergence” or Phase 3.29 hostile findings on Phase 3.28.
- `frontierAttractionAlignmentScore` still measures alignment toward **chosen solver target cells**, not raw nearest-frontier geometry.
- Anti-cheat metrics are **reported by the same script** that implements the gates; external hostile re-audit is still warranted.
- Grep on forbidden tokens may now match `AUDIT_FORBIDDEN_PARTICLE_STATE_KEYS`; that is **documented as non-authoritative** structural proof.

---

## Status

Phase 3.31 mechanics address the **specific Phase 3.30 self-audit failures** under the stated fixed gates on seeds 3030–3034. **Not accepted as emergent discovery.** No commit.
