# Sun Conjunct ASC Truth-Field Spine — Phase A Validation

**Date:** 2026-05-20  
**Scope:** Phase A only — trustworthy scalar spine, convergence metrics, no product reveal UX  
**Doctrine:** `docs/technical_philosophy/truth_field_rendering_path.md`, `progressive_field_reveal.md`

## What changed

| Layer | Change |
|-------|--------|
| `aura_field_engine.py` | Reference truth role (`uniform_one_sample_per_paint_pixel`); `compute_convergence_vs_reference()`; adaptive API properties: `stop_reason`, `cell_count`, `convergence_vs_reference`, `depth_regression_diagnostics`; `leaf_budget` leaf stop reason; default doctrine max depth **6** |
| `main_centerline_FIXER.py` | Default `max_depth=6`; `include_convergence_metrics` on adaptive request |
| `scripts/benchmark_adaptive_aura.py` | Full convergence metrics per viewport; depth sweep; minimum convergent depth; depth-8 regression analysis; `greenland_iceland` viewport |
| `map_CURRENT.html` | Debug panel only: stop reason + convergence vs reference (no reveal animation) |
| `scripts/smoke_map_current.py` | Asserts convergence + stop_reason on adaptive API |

## What remained unchanged

- Uniform raster path (`?rasterAura=1`) semantics — still one truth sample per pixel, no blur/gamma
- Leaf paint policy — deepest containing leaf, center strength, `imageSmoothingEnabled = false`
- No cosmetic smoothing, feather, stroke widening, or interpolation between truths
- House/aspect/centerline engines — mismatch probe still exposed, not hidden
- Progressive reveal UX — **not** productized (compatibility preserved via stage metadata only)

## Reference truth definition

For Sun conjunct ASC at paint grid **W×H**:

> **Reference** = `generate_aura_raster()` at identical bounds and dimensions: exactly **W×H** `swe.houses` evaluations, strength = `max(0, 1 − orb/maxOrb)`.

Adaptive output is judged against this reference, not against a blurred or upscaled target.

## Convergence metrics (reported)

| Metric | Location |
|--------|----------|
| `sample_count` / `truth_sample_count` | adaptive properties |
| `cell_count` (= leaf count) | adaptive properties |
| `max_depth_reached` | adaptive properties |
| `mean_delta_vs_reference` | `convergence_vs_reference` |
| `max_delta_vs_reference` | `convergence_vs_reference` |
| `pixels_above_threshold_pct` (Δ > 0.05) | `convergence_vs_reference` |
| `stop_reason` | adaptive properties (pass-level) |

## Depth 8 regression — identified cause

On **`asc_band`** viewport (96×72), depth sweep shows:

| max_depth | samples | % pixels Δ>0.05 | maxΔ | leaf_budget |
|-----------|---------|-----------------|------|-------------|
| 4 | 17360 | **0%** | 0.030 | no |
| 6 | 49260 | **0%** | 0.030 | no |
| 8 | 80040 | **7.49%** | 0.344 | **yes** |

**Mechanism:** At depth 8 the quadtree hits `max_leaves` (12000) mid-band. Subdivision stops unevenly: sibling leaves sit at different depths. Each paint pixel inherits the **center** strength of its smallest containing leaf, while the reference samples **pixel center** directly. Truncated trees increase maxΔ without any cosmetic fix.

**Governance response:** Default `max_depth` lowered to **6**; overshoot guard = do not promote depth when `leaf_budget_hit` and convergence worsens.

## Lowest acceptable depth (automated, asc_band)

- **Numerically:** `max_depth=4` — 0% pixels above 0.05 threshold vs reference (same as depth 6 on this viewport).
- **Recommended default:** **6** — matches prior validated band behavior with headroom before leaf budget on wider active-band views.
- **Do not use depth 8** without raising `max_leaves` proportionally or convergence-governed stop.

## Viewport summary (default max_depth=6)

| Viewport | Converged | Notes |
|----------|-----------|-------|
| mid_lat_wide | yes | No field signal — coarse depth 0, 0Δ |
| high_north | yes | Cap-adjacent weak field |
| greenland_iceland | yes* | Aura scalar only; line/house clip mismatch remains elsewhere |
| southern | yes | Weak/no signal |
| asc_band | yes | Active band; ~49k truth samples |

\*Greenland/Iceland **overlay gap** (centerline tail, house vs line cap) is a **clip-policy** issue per doctrine — not fixed by aura density and **not** cosmetically hidden.

## Where mismatch still exists

1. **Centerline vs aura** — separate geometry engines; debug mismatch probe unchanged  
2. **High-latitude cap** — ±65° product cap; aura/house/line may disagree until unified clip policy  
3. **Leaf-constant fill** — stair-steps at leaf borders until depth sufficient (density, not blur)  
4. **Depth 8 + leaf budget** — regression if forced deeper without budget governance  

## Visual smoothness source

**Only** truthful sample density:

- More/adaptive `swe.houses` evaluations and smaller leaves along the band  
- Nearest-neighbor canvas upscale (`imageSmoothingEnabled = false`) — **not** cosmetic blur  

No new blur, glow, feather, widened strokes, or interpolation between cell truths in this phase.

## Tests run

```bash
./venv/bin/python3 scripts/benchmark_adaptive_aura.py
./venv/bin/python3 scripts/validate_sprint_dc_ic.py
./venv/bin/python3 scripts/smoke_map_current.py
```

| Script | Result |
|--------|--------|
| `benchmark_adaptive_aura.py` | pass — 5 viewports; asc_band converged at depth 6; depth-8 regression confirmed on sweep |
| `validate_sprint_dc_ic.py` | pass |
| `smoke_map_current.py` | pass (server restarted for adaptive convergence fields) |

Report: `validation/reports/adaptive_aura_benchmark.json`
