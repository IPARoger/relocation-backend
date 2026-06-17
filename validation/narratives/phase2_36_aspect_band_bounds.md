# Phase 2.36 — Aspect Band Boundary Mask Correction

## Purpose

Human QA rejected the first colored Phase 2.36 aspect-band mockups.

Rejected findings:

- width ordering was not visually trustworthy,
- centerline/core was too thick,
- opacity fell off too abruptly,
- middle gradient was missing,
- outer translucency stayed too transparent for too long,
- the result did not read as a controlled exactness crest.

This correction breaks the visual target into a simpler boundary/mask-only pass before any color-gradient work continues.

## Artifacts

- `validation/visual_targets/phase2_36_aspect_band_bounds.html`
- `validation/visual_targets/phase2_36_aspect_band_bounds_3deg.png`
- `validation/visual_targets/phase2_36_aspect_band_bounds_6deg.png`
- `validation/visual_targets/phase2_36_aspect_band_bounds_10deg.png`
- `validation/visual_targets/phase2_36_aspect_band_bounds_mixed_3_10deg.png`
- `validation/reports/phase2_36_aspect_band_bounds.json`

## Scope

This pass is boundary/mask-only.

It uses:

- flat neutral fill,
- smooth continuous outer boundaries,
- the same diagonal path in every mockup,
- map-like labels/background for scale.

It does not use:

- gold gradient,
- centerline opacity styling,
- blur,
- feathering,
- dots,
- rain,
- virga,
- animation,
- particles,
- stripe artifacts,
- pixel/probe artifacts,
- production code,
- renderer integration,
- `map_CURRENT.html` changes.

## Boundary Targets

The correction includes:

- `±3°` per side,
- `±6°` per side,
- `±10°` per side,
- asymmetric mixed example with `3°` on one side and `10°` on the other.

The JSON report records:

- `10°` wider than `6°`,
- `6°` wider than `3°`,
- `3°` as a narrow exactness corridor,
- mixed `3°/10°` as visibly asymmetric.

## Governance Rule

Boundary/mask approval must precede gradient approval.

Future gradient work should fill the approved mask rather than trying to create geometry by blurring a centerline.

After the mask is approved, a separate gradient pass should test:

- centerline width,
- centerline opacity,
- falloff curve,
- middle-gradient behavior,
- outer-edge translucency.

## Result

The boundary-mask report records mechanical acceptance checks as passing.

Human review is still required before this mask becomes the approved geometry target for later gradient work.

## Rollback Scope

Rollback is limited to deleting:

- the boundary-mask HTML,
- the four boundary-mask PNGs,
- the boundary-mask JSON report,
- this narrative.

No production code, backend behavior, renderer behavior, `truth_grid_engine.py`, scheduler/cache execution, aura implementation, smoke file, roadmap file, sandbox/prototype file, validation report outside the allowed output, or `map_CURRENT.html` behavior was changed.
