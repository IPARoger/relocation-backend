# Adaptive Aura Refinement PoC — Research Report

**Date:** 2026-05-20  
**Scope:** Sun conjunct ASC scalar field only  
**Flags:** `?debugAdaptive=1` (+ `?debugAura=1` for metrics panel)

## What changed

| Layer | Change |
|-------|--------|
| `aura_field_engine.py` | `generate_aura_adaptive_raster()` — quadtree subdivision with truth samples at corners + center |
| `main_centerline_FIXER.py` | `POST /aura-raster-adaptive` |
| `map_CURRENT.html` | Adaptive progressive stages, debug cell overlay, metrics panel; gated behind `?debugAdaptive=1` |
| `scripts/benchmark_adaptive_aura.py` | Uniform vs adaptive comparison + depth convergence sweep |
| `scripts/smoke_map_current.py` | Adaptive API + UI checks |

Uniform raster (`?rasterAura=1`) is unchanged. No blur, splines, Chaikin, or CSS smoothing added.

## Adaptive strategy

1. **Coarse grid** — `initial_divisions` (4→6) over viewport bounds.
2. **Truth sample** each cell: 4 corners + center via `swe.houses` → `strength = max(0, 1 − orb/maxOrb)`.
3. **Refine when** (any):
   - `gradient` — corner/center strength spread > tolerance (depth-scaled)
   - `center_corner` — center disagrees with a corner (thin-band detection)
   - `orb_boundary` — zero ↔ nonzero crossing
   - `threshold_0.04` / `threshold_0.4` — strength band crossings
4. **Stop when** — stable interior, `max_depth`, `min_cell_deg`, or sample/leaf budget.
5. **Paint** — each pixel inherits **deepest leaf** containing its center; `imageSmoothingEnabled = false` (nearest-neighbor upscale only).

## Where refinement concentrates

Benchmark viewport **`asc_band`** (near Sun–ASC line, lon −100…−80):

- **Refine triggers:** gradient 589, center_corner 508, orb_boundary 197, threshold crossings 1000+
- **Depth histogram:** mass at depths 4–6 (fine cells on band + falloff)
- **Stable leaves:** 5270 / 7398 — interior weak/zero regions stay coarse

Global viewports with **no aura signal** in frame: **depth 0 only**, ~97% fewer truth samples than uniform grid (correct “don’t subdivide empty field”).

## Sample reduction vs uniform raster

| Viewport | Uniform samples | Adaptive truth samples | Reduction | maxΔ strength |
|----------|-----------------|------------------------|-----------|---------------|
| mid_lat_wide | 6912 | 180 | 97.4% | 0 |
| asc_band | 6912 | 49260 (depth 6) | −612%* | 0.030 |

\*Negative reduction = **more** `swe.houses` calls than one sample/pixel when the band is active and refinement is deep. Trade-off: spend samples on boundaries, not on uniform weak areas.

## Convergence threshold (automated sweep)

On `asc_band` 96×72 paint grid vs uniform reference:

| max_depth | truth_samples | pixels with Δ>0.05 |
|-----------|---------------|-------------------|
| 2 | 2880 | 10.37% |
| 4 | 17360 | **0%** |
| 6 | 49260 | 0% (mean Δ 0.0086) |
| 8 | 80040 | 7.49% (overshoot — budget/depth interaction) |

**Finding:** depth **4–6** reaches perceptual parity with uniform grid on this band (automated metric). Depth 8 can regress (more samples, larger maxΔ) — needs budget tuning, not more depth blindly.

**Human QA still required** for “does aura feel continuous?” and polygon saw-teeth on house overlays (separate engine).

## Visual quality / artifacts

**Improved (expected):** continuous alpha where leaves are fine along band; debug overlay shows refinement hugging centerline/falloff.

**Remaining artifact classes:**

1. **Leaf constant fill** — each leaf is flat strength (center sample); pixel stair-steps at leaf boundaries until depth sufficient.
2. **World view + active band** — refinement can exhaust budget or run long; use zoomed view or staged `maxSamples`.
3. **Regions still needing brute force** — cusp-heavy house boundaries, dateline seams, polar cap edges (house/aspect engines, not aura adaptive).
4. **Server restart** — old uvicorn without `/aura-raster-adaptive` causes hung fetches; restart after pulling this PoC.

## Cosmetic smoothing?

**None** in adaptive path. Interpolation policy: `none_across_cells; partition of viewport`. Allowed: extra truthful samples + documented leaf inheritance.

## Future unified scalar-field engine

This PoC treats aura as a **sampled truth field** with render mode `adaptive_raster`. House polygons and aspect lines can converge to the same pattern: coarse truth → refine on gradient/cusp/band crossing → render as line/polygon/alpha field without changing the underlying samples.

## How to run

```bash
./venv/bin/uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000
# Adaptive PoC (debug cells on final stage only):
/map_CURRENT.html?debugAdaptive=1&debugAura=1
# Compare uniform:
/map_CURRENT.html?rasterAura=1&debugAura=1
# Benchmark:
./venv/bin/python3 scripts/benchmark_adaptive_aura.py
```

Overlay: Sun · Conjunction · ASC → Find regions. Zoom into band for meaningful refinement visualization.

## Tests

- `./venv/bin/python3 scripts/validate_sprint_dc_ic.py` — pass
- `./venv/bin/python3 scripts/smoke_map_current.py` — pass (requires server with adaptive route)
