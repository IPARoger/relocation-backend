# Phase 3.33 Alignment Metric Deconstruction

**frontierAttractionAlignmentScore verdict: FAIL**

**Recommendation: RETIRE or RENAME** (do not use as frontier-geometry evidence)

**evidenceSupportsFrontierResponsiveMigration: false** (corrected in Phase 3.34)

**Emergence claimed: false**

Artifacts:

- `validation/scripts/phase3_33_alignment_metric_deconstruction.py`
- `validation/reports/phase3_33_alignment_metric_deconstruction.json`
- Reference: `validation/reports/phase3_32_geometry_diversification_audit.json`

Mechanics: Phase 3.31 unchanged. Samples collected at the **same instant** as production `frontierAttractionAlignmentScore` (after target-pull velocity, before late steering corrections).

Seeds: **3030–3039** | Geometries: **10**

---

## What the metric actually measures

Implementation (from `phase3_30_minimal_migration_core.py`):

```python
dx, dy = tx - p.x, ty - p.y   # direction to chosen solver TARGET CELL
frontier_alignment_samples.append((p.vx, p.vy, dx, dy))
```

`frontierAttractionAlignmentScore` is **cosine alignment between particle velocity and direction to the assigned target grid cell**. It is **not** alignment to nearest frontier geometry.

Deconstruction confirms **exact tautology**:

| Metric | Correlation with reported |
|---|---|
| `chosen_target_pull` | **1.000** (identical) |
| `nearest_frontier_direction` | 0.264 |
| `boundary_normal_audit` | -0.237 |
| `center_pull_baseline` | -0.007 |
| `random_steering_baseline` | -0.112 |

---

## Mean alignment by geometry (seeds averaged)

| Geometry | Reported (misnamed) | Nearest frontier | Random | Center pull | Boundary audit | Displacement from init |
|---|---|---|---|---|---|---|
| sun_in_1 | **0.765** | 0.037 | 0.001 | 0.026 | 0.177 | 0.292 |
| circle | **0.766** | -0.004 | 0.000 | 0.155 | 0.130 | 0.216 |
| thin_ribbon | **0.763** | 0.029 | 0.000 | 0.068 | 0.177 | 0.273 |
| two_islands | **0.763** | 0.010 | -0.001 | 0.078 | 0.087 | 0.248 |
| crescent | **0.764** | -0.001 | -0.001 | 0.160 | 0.096 | 0.243 |
| narrow_fjord | **0.748** | 0.004 | -0.001 | 0.082 | 0.131 | 0.214 |
| noisy_blob | **0.766** | -0.000 | -0.001 | 0.193 | 0.128 | 0.237 |
| hollow_donut | **0.758** | -0.003 | 0.000 | 0.248 | 0.110 | 0.255 |
| coastline_strip | **0.760** | 0.009 | 0.000 | 0.121 | 0.169 | 0.245 |
| small_island | **0.775** | 0.019 | -0.002 | 0.104 | 0.084 | 0.206 |

**Reported score range:** 0.748–0.775 (relative spread **3.5%**).

**Nearest-frontier score range:** roughly -0.004–0.037 (spread **412%** of mean magnitude, but absolute values near **zero**).

---

## Test verdicts

| Test | Verdict | Evidence |
|---|---|---|
| Tautology (reported = chosen target pull) | **FAIL** | r = 1.0 |
| Geometry sensitivity (reported) | **FAIL** | spread 3.5% < 10% threshold |
| vs random baseline | **PASS** | reported − random ≈ **0.763** |
| vs center-pull redundancy | **PASS** | r ≈ −0.007 (not center-redundant) |

Passing the random baseline does **not** rescue the metric: any coherent steering beats random noise. That is not evidence of frontier discovery.

---

## Relative spread across geometries

| Metric | Relative spread |
|---|---|
| **frontierAttractionAlignmentScore (reported)** | **0.035** |
| chosen_target_pull | 0.035 |
| nearest_frontier_direction | **4.120** |
| displacement_from_initial | 0.354 |
| boundary_normal_audit | 0.725 |
| center_pull_baseline | 1.793 |
| random_steering_baseline | 9.166 |
| final_target_cell_direction | 0.070 |

`nearest_frontier_direction` varies more across geometries but stays **near zero alignment** — particles are **not** velocity-aligned with nearest frontier points. The solver steers toward **chosen cells**, which are only loosely related to nearest frontier geometry (r = 0.26).

---

## Answers to required questions

### Is the metric geometry-sensitive?

**No.** Reported score is stable (~0.76±0.01) across all ten truth shapes. Phase 3.32 fingerprint finding is **confirmed**.

### Is it redundant with generic target pull?

**Yes.** It is **definitionally identical** to chosen-target-pull alignment (correlation 1.0). It is a **control-loop artifact**, not an independent observation.

### Does it distinguish geometry better than random/center baselines?

- **vs random:** yes (gap ~0.76), but trivially so.
- **vs center pull:** yes (decorrelated), but that does not make it frontier-sensitive.
- **vs nearest frontier:** reported is **much higher** (~0.76 vs ~0.03) but measures a **different direction** entirely.

### Should the metric be retired, renamed, or retained?

| Action | Guidance |
|---|---|
| **RETIRE** as `frontierAttractionAlignmentScore` | **Recommended** for any emergence claim |
| **RENAME** to `chosenTargetPullAlignmentScore` | If a steering-coherence diagnostic is still wanted |
| **ADD** separate `nearestFrontierAlignmentScore` | Only if near-zero values are acceptable; currently ~0.03 means particles do not track nearest frontier vector |
| **RETAIN** under current name | **Not justified** — name is misleading |

---

## Contradiction audit (Phase 3.34 correction)

The prior JSON incorrectly set `evidenceSupportsFrontierResponsiveMigration: true`.

| Item | Detail |
|---|---|
| Prior value | `true` (wrong) |
| Corrected value | `false` |
| Why it was wrong | The field used `nearestFrontierRelativeSpread >= 0.10` only. Nearest-frontier alignment has high relative spread (~412%) around a **near-zero mean (~0.03)**, which is not material frontier-directional evidence. |
| Controlling rule (now) | True **only if all** hold: (1) reported metric not tautological with chosen target pull, (2) reported metric geometry-sensitive (spread ≥ 10%), (3) nearest-frontier **mean** alignment ≥ 0.15. |

All three fail on measured data: tautology (r=1.0), reported spread 3.5%, nearest mean ~0.012.

Report-generation logic patched in `phase3_33_alignment_metric_deconstruction.py`; JSON regenerated via `--recompute-integrity-only` (no solver re-run).

---

## Evidence for/against frontier-responsive migration

**Against (via this metric):**

- Name implies frontier geometry; implementation uses target cell vector.
- Score invariant across radically different truths.
- Nearest-frontier alignment is ~0.03, so velocity is **not** frontier-directional in the sense the name suggests.

**Not supported by this metric:**

- `evidenceSupportsFrontierResponsiveMigration` is **false** under the Phase 3.34 rule.

**Other observations (Phase 3.32, separate from this metric):**

- Frontier cell counts and gate pass rates change by geometry, but this alignment score does not demonstrate frontier-directional velocity.

---

## Overall conclusion

`frontierAttractionAlignmentScore` is **metric theater** for frontier emergence claims: a **stable, high, positively biased** number that tracks **generic target-cell steering**, not geometry-sensitive frontier attraction.

**PASS is not warranted.** **FAIL** is warranted. **UNPROVEN** does not apply — evidence is sufficient to reject the metric's naming and interpretive use.

No solver changes. No emergence claim. No commit.
