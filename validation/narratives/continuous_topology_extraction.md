# Continuous Topology Extraction

Date: 2026-05-22

## Scope

Phase 1.17 prototypes a debug-only continuous topology extractor for thin canonical aspect-to-angle loci. It runs inside the smoke harness against `?canonicalVisible=1`.

Default production remains `legacy_search_regions`. No aura, animation, cache integration, smoothing, interpolation, line thickening, contour fallback, or astrology math change was made.

## Extraction Method

The prototype starts from canonical positive samples already produced by the debug topology path. It does not invent values between samples. It:

1. projects positive canonical samples into screen space,
2. orders them deterministically by screen position,
3. splits them into path segments when spacing exceeds the debug block discontinuity threshold,
4. records segment count, segment lengths, total length, mean/max point spacing,
5. computes heading variance and curvature variance from neighbor steps,
6. records seam and cap-adjacent discontinuities,
7. compares extracted samples to wall-positive pixels and legacy line geometry where available.

This is not aesthetic smoothing. It is a diagnostic topology extraction from classified truth samples.

## Observed Metrics

### Narrow-Orb Sun Conjunct ASC

- extracted segments: 1,
- segment length: 6.403 px,
- mean/max point spacing: 6.403 px,
- heading variance: 0,
- curvature variance: 0,
- discontinuities: 0,
- seam discontinuities: 0,
- cap-adjacent discontinuities: 0,
- mean distance to wall positives: 0.5 px,
- mean distance to legacy line: 0 px,
- coherent topology: true.

The line is too sparse to be production-ready, but the positives form a coherent local segment rather than random noise.

### ASC + Sun House

- extracted segments: 1,
- total segment length: 265.453 px,
- mean spacing: 8.044 px,
- max spacing: 18.974 px,
- heading variance: 4999.962,
- curvature variance: 4920.445,
- discontinuities: 0,
- mean distance to wall positives: 0.118 px,
- coherent topology: true.

The high heading/curvature variance is expected for screen-sorted ASC/overlap geometry and should be replaced by a stronger path-ordering algorithm before production use.

### High-Latitude ASC

- extracted segments: 2,
- segment lengths: 21.902 px and 219.351 px,
- total length: 241.253 px,
- mean spacing: 9.65 px,
- max spacing: 25.456 px,
- heading variance: 4769.279,
- curvature variance: 4018.272,
- discontinuities: 1,
- seam discontinuities: 0,
- cap-adjacent discontinuities: 0,
- mean distance to wall positives: 0.185 px,
- mean distance to legacy line: 1.753 px,
- coherent topology: true.

High-latitude ASC remains coherent but shows a real split that should stay on the backlog.

### Seam-Centered Saturn Conjunct MC

- extracted segments: 1,
- total segment length: 1150.337 px,
- mean spacing: 7.235 px,
- max spacing: 8.485 px,
- heading variance: 4556.07,
- curvature variance: 0,
- discontinuities: 0,
- seam discontinuities: 0,
- cap-adjacent discontinuities: 0,
- mean distance to wall positives: 0 px,
- mean distance to legacy line: 3 px,
- coherent topology: true.

MC remains clean. The seam case continues to support canonical topology rather than legacy representation as the better source.

### Clean MC Control

- extracted segments: 0,
- wall positives: 0,
- discontinuities: 0.

The negative control remains clean.

## Interpretation

ASC subpixel positives form coherent trajectories near the wall-positive locus. Pixel-center overlap is inadequate for narrow ASC because it ignores valid subpixel crossings. The remaining problem is topology extraction and path ordering, not astrology math.

The current prototype is sufficient as evidence for the next abstraction, but not enough for final rendering. Screen-sorted ordering is deterministic and inspectable, but it is not a real graph/path solver. The next step should extract connected components or nearest-neighbor paths from classified samples.

## Readiness

This prototype is not an aura source yet. It is the right diagnostic direction for a future aura/perceptual renderer: continuous topology should become the source truth for thin line phenomena, and aura should only come after this topology is stable.
