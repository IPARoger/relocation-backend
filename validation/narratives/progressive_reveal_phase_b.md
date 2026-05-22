# Progressive Reveal — Phase B Validation

> **STATUS: SUPERSEDED** (2026-05-21) — preserved as archaeology.
>
> **Why superseded:** Progressive reveal debug path (`debugProgressiveReveal`)
> is not the production architecture. Screen-space adaptive refinement +
> targeted escalation replaced it.
>
> **Current doctrine:** `docs/CURRENT_RENDERING_DOCTRINE.md` →
> `validation/narratives/screen_pixel_adaptive_refinement.md`

**Date:** 2026-05-20  
**Scope:** Minimal truthful progressive reveal architecture (debug-only)  
**Flag:** `?debugProgressiveReveal=1` (Sun conjunct ASC requested overlay only)  
**Doctrine:** `progressive_field_reveal.md`, `truth_field_rendering_path.md`, Phase A spine narrative

## Architecture decisions

### 1. Refinement stage model (engine-owned)

Canonical stages in `aura_field_engine.REFINEMENT_REVEAL_STAGES`:

| stage_id | Engine knobs | Role |
|----------|--------------|------|
| `coarse_world` | divisions 4, max_depth 2 | Initial partition; weak interior stable |
| `regional_refine` | divisions 5, max_depth 4 | Band-scale subdivision |
| `boundary_refine` | divisions 6, max_depth 5 | Gradient/orb/threshold frontiers |
| `contour_stabilization` | divisions 6, max_depth 6 | Target convergence pass |

Stages are **not** timer phases. Each maps to real `max_depth`, `initial_divisions`, and `max_samples` budgets.

**Observed stage** (`classify_observed_refinement_stage`) is derived post-pass from:

- `max_depth_reached`
- `active_frontier_leaf_count` (leaves still wanting refinement)
- `convergence_vs_reference.converged`

### 2. Reveal transport structure

Per adaptive API response when `include_reveal_transport=true`:

```json
{
  "transport_version": 1,
  "replace_prior_snapshot": true,
  "overlay_scope": "sun_conjunct_asc_poc_only",
  "requested_stage": { "stage_id", "max_depth_limit", ... },
  "observed_stage": { "stage_id", "derivation", "active_frontier_leaf_count", ... },
  "engine_state": { "truth_sample_count", "convergence_vs_reference", ... },
  "truth_samples": [{ "lon", "lat", "strength", "role", "leaf_depth" }],
  "frontier_cells": { "type": "FeatureCollection", ... }
}
```

**Design choice:** stage snapshots via repeated inspectable POSTs (same as existing adaptive staging), not WebSocket streaming. Truth-first inspectability over clever transport.

Manifest endpoint: `GET /aura-refinement-reveal-stages`.

### 3. Truthful vs fake reveal

| Truthful (implemented) | Fake (rejected) |
|------------------------|-----------------|
| Points at actual corner/center sample coordinates | Random lat/lon sprinkles |
| Cells from real quadtree leaves | Decorative particles |
| Raster replaced each stage (`replace_prior_snapshot`) | Stacked ghost semi-transparent layers |
| 220ms canvas opacity fade on replace only | Cinematic motion / sonar sweeps |
| Frontier cells where `stop_reason` ∈ pending refine set | Timer-based progress bars |
| Stage labels from API `reveal_transport` | Client-invented stage graph |

### 4. Frontend PoC (`?debugProgressiveReveal=1`)

- Enables adaptive raster path without requiring `?debugAdaptive=1`
- Runs `PROGRESSIVE_REVEAL_STAGES` sequence on **Find regions** for Sun conjunct ASC only
- Clears sample/frontier/cell layers between stages (replace, not stack)
- Draws `truth_samples` as small circle markers (strength → opacity)
- Draws `frontier_cells` as dashed red outlines
- Separate `progressiveRevealStatus` panel with observed stage + convergence
- Mismatch probe still logged at end — **not hidden**

## What changed

| File | Change |
|------|--------|
| `aura_field_engine.py` | Stage manifest, `build_reveal_transport`, per-leaf `truth_samples`, `include_reveal_transport` |
| `main_centerline_FIXER.py` | Request fields + `GET /aura-refinement-reveal-stages` |
| `map_CURRENT.html` | `debugProgressiveReveal` mode, layers, `renderProgressiveRevealAdaptive` |
| `validation/narratives/progressive_reveal_phase_b.md` | This document |

## What remained unchanged

- Phase A reference truth and convergence metrics
- No blur, interpolation between truths, or cosmetic band widening
- No product default-on reveal; debug flag only
- House/aspect overlays not revealed unless user requests them
- Centerline mismatch still visible

## Failure modes

| Risk | Mitigation |
|------|------------|
| Leaf budget truncates late stage | Observed stage reports frontier count; convergence may fail — visible, not smoothed |
| Payload size (truth_samples) | Capped at 4000 points per response; `truth_sample_truncated` flag |
| Client layer churn | Layers cleared each stage; only one snapshot visible |
| Misread “smooth” fade | Fade is canvas replace only, not cross-blend between unlike rasters |
| Adjacent overlay sampling | `overlay_scope` documented; reveal only for requested PoC overlay |

## Performance implications

- Progressive reveal = **4× adaptive API calls** per Find (one per stage) + optional uniform reference per pass for convergence
- Acceptable for debug/architectural proof; not optimized for production
- Benchmark script unchanged (single-pass); no premature optimization added

## UX observations (architectural proof)

**Increases trust when:**

- User sees cells subdivide along the band while interior stays dashed/stable
- Sample dots appear only at evaluated coordinates
- Status panel shows sample count and convergence tightening stage-to-stage

**Risk of distraction:**

- Four passes on world view with active band can take several seconds — acceptable in debug, would need suppression on pan/cache for product
- Frontier red outlines add visual noise — intentional for QA, would tone down in consumer mode

**Honesty of stages:**

- Stages feel honest because each is a complete engine snapshot with matching depth histogram and sample count monotonicity along active band
- Observed stage may differ slightly from requested (e.g. empty viewport stays `coarse_world`) — derivation string documents why

**Truthful reveal ugliness:**

- Leaf-constant fill stair-steps remain visible early — **good** for doctrine test
- Beauty, if any, emerges from densifying real samples, not from animation

## Verdict (Phase B)

| Question | Answer |
|----------|--------|
| Can truthful visible computation ship as identity? | **Promising** for debug/education; needs user study before default-on |
| Does reveal increase trust? | **Likely yes** when gated — shows measuring, not decorating |
| Does reveal become distracting? | **Possible** on world+band view; debounce/cache required for product |
| Are stages honest? | **Yes** — tied to depth, frontier, convergence, real samples |
| Reject concept? | **No** — reject only fake variants; keep truth-first reveal as optional microscope |

## How to run

```bash
./venv/bin/uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000
# Debug progressive reveal:
/map_CURRENT.html?debugProgressiveReveal=1&debugAura=1
# Overlay: Sun · Conjunction · ASC → Find regions (zoom band for visible refinement)
```

## Tests

```bash
./venv/bin/python3 scripts/benchmark_adaptive_aura.py
./venv/bin/python3 scripts/validate_sprint_dc_ic.py
./venv/bin/python3 scripts/smoke_map_current.py
```

| Script | Result |
|--------|--------|
| `benchmark_adaptive_aura.py` | pass |
| `validate_sprint_dc_ic.py` | pass |
| `smoke_map_current.py` | pass (reveal_transport on adaptive API) |
