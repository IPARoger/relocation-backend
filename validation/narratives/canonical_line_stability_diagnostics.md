# Canonical Line Stability Diagnostics

Date: 2026-05-22

## Scope

This diagnostic pass adds objective continuity metrics for the debug-only canonical visible layer. It does not advance to Phase 1.11, does not make canonical rendering default, and does not change astrology math.

## Metrics Added

For matched canonical screen samples, the debug state now records:

- matched point count,
- neighbor step count,
- mean step distance,
- maximum single-step deviation,
- maximum neighbor angular delta,
- neighbor angular delta variance,
- curvature variance,
- local heading-change variance,
- discontinuity count,
- seam crossing count,
- cap-adjacent count,
- block size and zoom,
- sampling status.

## Objective Findings

MC at `canonicalBlock=12` produced no matched samples in the default world viewport. This is a sampling aliasing result: the line is narrower than the coarse grid alignment for that view.

MC at `canonicalBlock=8` produced a stable vertical sample set:

- matched points: 61,
- mean step distance: 8,
- max single-step deviation: 8,
- neighbor angular delta max: 0,
- heading/curvature variance: 0,
- discontinuity count: 0,
- seam crossing count: 0.

After one zoom step, MC at `canonicalBlock=8` remained stable:

- matched points: 73,
- max single-step deviation: 8,
- heading/curvature variance: 0,
- discontinuity count: 0.

ASC at `canonicalBlock=12` produced matched samples with measurable curvature:

- matched points: 21,
- max single-step deviation: 43.267,
- max neighbor angular delta: 26.565,
- local heading-change variance: 98.03,
- discontinuity count: 2,
- seam crossing count: 0.

## Interpretation

The observed MC wobble is not mathematically real in the current diagnostic sample. It is induced by coarse screen-grid sampling and display interpretation. When the sampling block decreases from 12 to 8, MC resolves into a straight, stable vertical sample set with zero heading variance.

The ASC curve is not proven unstable, but the current metric is limited: it screen-sorts matched samples and does not reconstruct a true contour topology. Its measured heading variation is expected for a curved ASC locus plus coarse sampling. The discontinuity count should be revisited with a topology-aware contour extraction step before production migration.

## Aura / Refinement Implication

Aura, blur, or aesthetic refinement would only hide coarse sampling artifacts if applied now. It would not prove geometry. The true remedy for visible wobble is denser and/or adaptive canonical sampling plus topology-aware continuity validation, not cosmetic smoothing.

## Production Readiness

The current canonical substrate geometry is trustworthy enough for continued production refinement work behind debug gates. It is not yet ready to replace legacy visible rendering by default. The next phase should add topology-aware comparison/parity diagnostics before any default migration.

## Remaining Unproven

- Topological contour reconstruction from canonical masks.
- Pixel-level parity against legacy linework.
- ASC continuity across pan/zoom and higher latitudes.
- Seam behavior at world wrap.
- Full-density or adaptive refinement behavior.
- Popup truth integration on canonical pixels.
