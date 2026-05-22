# Topology-Aware Canonical Refinement

Date: 2026-05-22

## Scope

Phase 1.11 adds topology-aware edge subdivision to the debug-only canonical visible path. It is active only under:

```text
?canonicalVisible=1
```

Default production remains legacy `/search-regions`. No cache, scheduler production integration, aura, animation, aesthetics, or astrology math changed.

## Refinement Strategy

The canonical viewport grid is first classified at the debug block size. The client then detects occupied/non-occupied neighbor transitions in the screen-space mask grid. Cells adjacent to a transition are treated as boundary cells.

Each boundary cell is subdivided once into four quarter-cell samples. Only these boundary-derived points are sent through a second `/screen-pixel-truth` request. Stable interiors are not resampled.

This is topology-aware refinement because extra work is driven by observed occupancy transitions, not by visual smoothing or cosmetic interpolation.

## Why This Is Not Aesthetic Smoothing

Blur, gradients, contour smoothing, or aura effects would hide block edges without adding truth samples. This pass adds more classified points exactly where topology is uncertain: along occupied/non-occupied frontiers.

The visible debug layer still paints simple blocks. It does not invent continuity between samples.

## Metrics Observed

For the ASC debug viewport at `canonicalBlock=12`:

- coarse canonical points: 5025,
- coarse matched points: 21,
- occupied boundary cells: 90,
- subdivision count: 90,
- refined points: 360,
- refined matched points: 70,
- total matched points after refinement: 91,
- refinement elapsed time: about 5-7 ms,
- total canonical elapsed time: about 40-43 ms,
- discontinuity count: reduced from 2 in the pre-refinement diagnostic to 1.

MC stability remains clean at `canonicalBlock=8`:

- matched points: 61,
- max single-step deviation: 8,
- heading/curvature variance: 0,
- discontinuity count: 0.

## Artifacts Reduced

The refinement increases boundary evidence around curved ASC regions and reduces false discontinuity in the current smoke viewport. It also keeps MC behavior stable because MC does not need extra smoothing to remain straight when sampled densely enough.

## Remaining Unresolved

- True contour topology is still not reconstructed from masks.
- Parity against legacy line/polygon geometry is not yet quantified.
- Boundary refinement currently has one subdivision level only.
- Seam and high-latitude stress cases still need targeted validation.
- Popup truth integration is still not attached to canonical pixels.

## Parity Direction

Canonical parity is improving: matched samples are now denser only near detected edges, and continuity diagnostics improve without hiding defects through blur or cosmetic smoothing.

This is still debug-only. It is not a production renderer replacement.
