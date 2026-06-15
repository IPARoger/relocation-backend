# Connected-Component Topology Solver

Date: 2026-05-22

## Scope

Phase 1.18 replaces the crude screen-sort topology ordering from Phase 1.17 with a debug-only connected-component / nearest-neighbor path solver. The work remains inside the `?canonicalVisible=1` diagnostics and smoke harness.

Default production remains `legacy_search_regions`. No visible production renderer changed. No aura, animation, cache integration, smoothing, blur, line thickening, contour fallback, or astrology math change was made.

## Why Path Ordering Matters

Phase 1.17 proved that canonical ASC/MC positives are coherent, but the extractor sorted samples by screen `y/x`. That was deterministic and inspectable, but it could connect points in an order that is not the actual path. This made heading and curvature metrics noisier than the topology itself.

Path ordering matters because future line/aura rendering should consume topology, not arbitrary sample order.

## Solver Method

The new solver keeps the same canonical positive samples and does not invent new points. It:

1. projects matched/subpixel-positive samples into screen space,
2. builds connected components using the existing discontinuity threshold,
3. refuses longitude seam jumps while forming components,
4. orders each component with a nearest-neighbor walk,
5. preserves seam-safe and cap-safe discontinuity accounting,
6. reports the same segment, spacing, heading, curvature, wall-distance, and legacy-distance metrics,
7. keeps the old crude ordering as `crudeOrdering` for before/after comparison.

The output now exposes `pathSolver` and aliases it as `continuousTopology`.

## Before / After Metrics

### Narrow-Orb Sun Conjunct ASC

- crude: 1 segment, 6.403 px total length, 6.403 px mean spacing, curvature variance 0, discontinuities 0.
- solver: 1 component, 1 segment, 6.403 px total length, 6.403 px mean spacing, curvature variance 0, discontinuities 0.
- distance to wall positives: 0.5 px mean.
- distance to legacy line: 0 px mean.

The case is unchanged because there are only two positive samples. It remains coherent but sparse.

### ASC + Sun House

- crude: 1 segment, 265.453 px total length, 8.044 px mean spacing, 18.974 px max spacing, curvature variance 4920.445, discontinuities 0.
- solver: 1 component, 1 segment, 220.328 px total length, 6.677 px mean spacing, 13.416 px max spacing, curvature variance 1831.553, discontinuities 0.
- distance to wall positives: 0.118 px mean.

The solver produces a shorter, more local path and reduces curvature variance materially without smoothing or adding samples.

### High-Latitude ASC

- crude: 2 segments, 241.253 px total length, 9.65 px mean spacing, curvature variance 4018.272, discontinuities 1.
- solver: 2 components, 2 segments, 184.328 px total length, 7.373 px mean spacing, curvature variance 713.342, discontinuities 1.
- seam discontinuities: 0.
- cap-adjacent discontinuities: 0.
- distance to wall positives: 0.185 px mean.
- distance to legacy line: 1.753 px mean.

The high-latitude split remains, but it is now explainable as two connected components rather than an artifact of screen-sort ordering.

### Seam-Centered Saturn Conjunct MC

- crude: 1 segment, 1150.337 px total length, 7.235 px mean spacing, curvature variance 0, discontinuities 0.
- solver: 1 component, 1 segment, 960 px total length, 6.038 px mean spacing, curvature variance 50.941, discontinuities 0.
- seam discontinuities: 0.
- cap-adjacent discontinuities: 0.
- distance to wall positives: 0 px mean.
- distance to legacy line: 3 px mean.

MC remains clean. The solver does not introduce false seam/cap continuity. The small curvature signal is a diagnostic result of nearest-neighbor local ordering, not a geometry defect.

### Clean MC Control

- crude: 0 segments.
- solver: 0 components, 0 segments.
- wall positives: 0.

The negative control remains clean.

## Interpretation

The connected-component solver improves the meaning of topology metrics. ASC discontinuities remain bounded, high-latitude ASC segmentation is more explainable, and MC remains seam-safe.

This is not smoothing. The solver only changes the order and grouping of already-classified positive samples. It does not create intermediate samples, widen the line, blur the field, or change formulas.

## Remaining Gaps

The solver is still greedy nearest-neighbor. It is enough for diagnostic confidence but not a final production path system. Future work should consider:

- endpoint-aware path starts,
- branch handling for overlapping conditions,
- stable component IDs across zoom/pan,
- explicit graph path scoring instead of greedy local choice.

## Readiness

Topology extraction is now strong enough to support a future debug-only visible line experiment. It is not yet a source for production aura rendering. A future perceptual/aura phase should consume connected topology only after another debug pass validates component stability across zoom and pan.
