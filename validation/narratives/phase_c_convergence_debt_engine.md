# Phase C — Convergence-debt-driven adaptive aura (C1–C4)

**Date:** 2026-05-20  
**Scope:** Sun conjunct ASC raster aura only.  
**Doctrine:** `docs/technical_philosophy/truth_field_rendering_path.md` §4 Phase C; `rendering_truth_over_cosmetics.md`.  
**Status:** Engine + API + benchmark complete; smoke + sprint validation passing. No commit.

## What changed (working tree)

| File | C-step | Role |
|------|--------|------|
| `aura_field_engine.py` | C1–C4 | `generate_aura_convergence_raster()` — pixel attribution map, per-leaf debt, priority-queue refinement, per-pass budgets + overshoot guard |
| `main_centerline_FIXER.py` | API | `POST /aura-raster-convergence` + `AuraConvergenceRasterRequest` schema |
| `scripts/benchmark_adaptive_aura.py` | Eval | Runs depth-driven and convergence-driven side-by-side on 5 viewports; per-pass budget sweep; depth-8 regression analysis |
| `validation/reports/adaptive_aura_benchmark.json` | Output | Per-viewport metrics, per-pass history, depth-8 prevention summary |
| `scripts/smoke_map_current.py` | UI smoke | Unchanged for Phase C (uniform raster + adaptive routes still exercised) |
| `map_CURRENT.html` | UI | Phase C raster path not yet surfaced (Phase B reveal scope) — intentional |

Engine file is currently untracked in git; that is the prior state from earlier phases. No commit performed.

## Doctrine compliance — no cosmetic smoothing

| Channel | Status |
|---------|--------|
| Engine code | Searched for `smooth`, `blur`, `gauss`, `chaikin`, `spline`, `feather`, `interpolat`, `imageSmoothing` — all hits are **rejection comments** or `interpolation_policy: "none_across_cells; partition of viewport"`. |
| Strength rule | `strength = max(0, 1 − orb_deg / max_orb)` from `swe.houses`. Per-leaf strength = center truth sample of that leaf. Pixels inherit owning leaf via attribution map (C1). |
| Reference | Uniform raster with **one** `swe.houses` evaluation per paint pixel — same bounds, same `apply_lat_cap`. |
| Convergence delta | Pixel-level absolute Δ against reference; threshold 0.05. Mismatch is **counted and reported**, never suppressed. |
| Overshoot | If a pass increases `pixels_above_threshold`, engine halts with `stop_reason: overshoot_guard_triggered`. No silent “smooth over” fallback. |
| Frontend | No blur/glow added; nearest-neighbor canvas upscale unchanged. |

## C1 — Pixel attribution map

- `pixel_strength: list[float]` per paint pixel — current strength assigned by owning leaf.
- `pixel_leaf_id: list[int]` per paint pixel — id of leaf currently owning it.
- On split, parent pixels are partitioned to four children by mid-lon / mid-lat (`_partition_pixels_to_children`); each child inherits the subset of parent pixels geometrically inside it. No pixel is shared, double-counted, or orphaned.
- `pixel_attribution_complete` is reported in response properties; benchmark confirms `true` for all five viewports.

## C2 — Per-leaf convergence debt

For each non-leaf-split leaf:

```
debt = Σ_pixel_in_leaf | leaf_strength − reference_strength[pixel] |
```

`pixels_above` is maintained incrementally as pixels move into/out of the threshold band. When a leaf reaches `debt = 0` it is marked `settled` with `stop_reason: zero_debt` and removed from the active queue.

## C3 — Priority-queue refinement loop

- `heapq` min-heap keyed on `−debt`, tie-broken by insertion sequence (`heap_seq`).
- Loop pops highest-debt leaf, attempts split into four cells, samples each child center, recomputes debt for the four children, pushes back non-settled children.
- Stale heap entries (leaf already split or settled) are skipped on pop; defensive re-push if the leaf’s debt mutated between push and pop.
- Settled / non-splittable leaves carry explicit `stop_reason` (`zero_debt`, `pixel_atomic`, `min_cell`, `leaf_budget`, `sample_budget`, `outside_lat_cap`, `no_pixels`). No hidden stops.

## C4 — Per-pass budgets + overshoot guard

Each pass:

1. Spends up to `per_pass_sample_budget` truth samples (default 2000).
2. Records `pixels_above_threshold` before and after.
3. If `pixels_above_after > pixels_above_before` and `overshoot_guard=True` → halt with `stop_reason: overshoot_guard_triggered`. No subsequent pass.
4. If pass split no leaves → halt with `no_actionable_leaves`.
5. If two consecutive passes show no progress → halt with `convergence_stalled`.
6. If `pixels_above ≤ target` (default 0) → halt with `converged`.

`pass_history[]` carries per-pass: samples used, leaves split, before/after pct, overshoot flag, skipped-leaf counters. This is **on-the-record** evidence of where samples were spent.

## Convergence metrics — depth-driven vs convergence-driven

Viewport-by-viewport (paint grid 96×72, reference samples = 6912):

| Viewport | Depth-driven samples → max Δ / converged | Convergence-driven samples → max Δ / converged | Samples saved | Stop reason |
|----------|------------------------------------------|------------------------------------------------|---------------|-------------|
| `mid_lat_wide` | 180 → 0.0 / **yes** | 16 → 0.0 / **yes** | −91.1% | `converged_at_initial_partition` |
| `high_north` | 150 → 0.0 / **yes** | 16 → 0.0 / **yes** | −89.3% | `converged_at_initial_partition` |
| `greenland_iceland` | 120 → 0.0 / **yes** | 12 → 0.0 / **yes** | −90.0% | `converged_at_initial_partition` |
| `southern` | 180 → 0.0 / **yes** | 16 → 0.0 / **yes** | −91.1% | `converged_at_initial_partition` |
| `asc_band` | 49 260 → 0.0302 / **yes** | **4 016** → 0.0391 / **yes** | **−91.8%** | `converged` after 2 passes |

“Empty-field” viewports — no aspect signal in frame — converge at the initial coarse partition with **only the initial coarse-cell samples**. The engine refuses to spend samples on a flat reference.

The active band (`asc_band`) — the only place where work is actually required — converges with **92% fewer truth samples** than the depth-driven engine.

## Depth-8 regression — prevented

Depth-driven sweep on `asc_band`:

| `max_depth` | Samples | max Δ | pixels Δ > 0.05 | Stop reason | Leaf budget hit |
|-------------|---------|-------|------------------|-------------|------------------|
| 2 | 2 880 | 0.067 | 10.37% | `max_depth_with_pending_refinement` | no |
| 4 | 17 360 | 0.030 | 0.00% | `max_depth_with_pending_refinement` | no |
| 6 | 49 260 | 0.030 | 0.00% | `max_depth_with_pending_refinement` | no |
| **8** | 80 040 | **0.344** | **7.49%** | **`leaf_budget`** | **yes** |

Mechanism (already diagnosed in `_depth_regression_diagnostics`): mid-band leaf budget truncation creates heterogeneous leaf depths — pixels at one depth inherit a flat strength while reference samples each pixel center, increasing max Δ without any blur involved.

Convergence-driven `phase_c_summary.depth_8_regression_prevented_by_convergence_engine: true`:

- Zero overshoot passes detected across all five viewports.
- `max_depth` is no longer the budget; the engine spends until `converged` or `overshoot_guard`/`convergence_stalled` fires. No path through the new engine can sample heavily into a truncated heterogeneous quadtree because the guard halts at the first regressive pass.

## Per-pass budget sweep (asc_band)

| `per_pass_sample_budget` | Samples | Passes | max Δ | Converged | Stop reason |
|--------------------------|---------|--------|-------|-----------|-------------|
| 500 | 3 016 | 6 | 0.054 | **no** | `convergence_stalled` |
| 1000 | 4 016 | 4 | 0.039 | yes | `converged` |
| 2000 | 4 016 | 2 | 0.039 | yes | `converged` |
| 4000 | 4 016 | 1 | 0.039 | yes | `converged` |

At 500 samples/pass on this band, the engine **stalls just above the threshold** and reports it honestly (`convergence_stalled`, max Δ 0.054 > 0.05). It does **not** declare convergence or smooth over the mismatch. From 1000 samples/pass upward the active band converges within four passes.

## Remaining mismatches (visible, not hidden)

- `asc_band` final max Δ vs reference = **0.0391** (mean 0.0085). Below the 0.05 convergence threshold but non-zero — this is the residual from leaf-flat strength assignment vs per-pixel reference sampling. Tightening the threshold would force more samples; doctrine accepts the visible non-zero rather than pretending it’s zero.
- `asc_band` with `per_pass_sample_budget=500` reports `convergence_stalled` at max Δ 0.054. The engine refuses to advance, surfaces the gap, and stops — this is the doctrine working.
- The four “empty-field” viewports report **zero** mismatch by point evaluation; they are honestly converged at the coarse partition.
- High-latitude lat-cap behavior remains a Phase D concern (clip policy unification across line / polygon / aura); Phase C does not touch it.

## Cosmetic smoothing audit

- `grep -i` for `smooth|blur|gauss|chaikin|spline|feather|interpolat|imageSmoothing` in `aura_field_engine.py` → all hits are **explicit rejection language** or `interpolation_policy: "none_across_cells"`.
- No CSS filter / blur / opacity ramp in the Phase C code path.
- Frontend canvas: `imageSmoothingEnabled = false` (nearest-neighbor only). Unchanged by Phase C.
- Convergence engine produces the same flat-strength leaf rendering as the depth-driven engine — beauty must come from **smaller leaves**, not from smoothing.

## Validation

```bash
./venv/bin/python3 scripts/validate_sprint_dc_ic.py    # overall_pass: true
./venv/bin/python3 scripts/benchmark_adaptive_aura.py  # 5 viewports; depth-8 prevention: true
./venv/bin/python3 scripts/smoke_map_current.py        # overall_pass: true
```

Reports:

- `validation/reports/sprint_dc_ic_validation.json`
- `validation/reports/adaptive_aura_benchmark.json`
- `validation/reports/map_current_smoke.json`

## What Phase C does **not** do

- No animation / reveal polish (Phase B scope).
- No house / aspect / angle-sign engine changes (Phase E scope; doctrine blocks until A–D done).
- No high-lat clip policy unification (Phase D scope; mismatch remains visible).
- No reduction of `max_samples` or `per_pass_sample_budget` defaults for FPS — convergence governs spend, FPS is downstream.
- No interpolation, no smoothing, no widened strokes, no glow. The doctrine reset is honored.
