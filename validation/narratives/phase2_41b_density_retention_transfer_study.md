# Phase 2.41b - Density-Retention Transfer Study

This validation-only study continues the geometry-free transfer-function work from Phase 2.41. The correction is perceptual: the prior board still read mostly as blue fading into transparency. Phase 2.41b explores stronger center density, delayed release, and tonal/luminance shaping beyond alpha interpolation.

## Method

No maps, curves, astrology, masks, polygons, ASC, or MC geometry are used. Each panel is a simple rectangle. The left edge is the carrier ridge. The right edge is the outer field boundary. The horizontal coordinate is normalized transfer distance `u=0..1`.

The board is rendered offline with Python, PIL, and numpy at 4x supersampling. Candidate functions combine alpha, tonal density, and luminance retention. There is no noise, particulate dropout, contour marking, strip construction, or geometry-derived artifact.

## Candidates

- Delayed Logistic Body
- Hybrid Density Hold
- Harmonic Body Retention
- Enamel Density
- Plasma Hold
- Gamma-Shaped Body
- Luminance Retention
- Alpha-Only Control
- Composite Candidate

The Alpha-Only Control is intentionally included to expose the old failure mode. The strongest candidates for human visual QA are expected to be Composite Candidate, Delayed Logistic Body, Hybrid Density Hold, Harmonic Body Retention, and Luminance Retention.

## Visual Doctrine

The target is compressed pressure body releasing outward, not a uniform smooth fade. The ridge should hold density before releasing. Lower opacity should preserve coherent material and chromatic solidity.

## First-Run Audit

Center density is substantially stronger than Phase 2.41, delayed release is explored, and the board now uses tonal/luminance shaping beyond alpha interpolation. No visible terracing or banding is obvious in the generated board, but human visual QA still needs to decide whether the strongest candidates escape the refined-gradient read. The leading candidates are Composite Candidate, Delayed Logistic Body, Hybrid Density Hold, and Harmonic Body Retention.

## Governance

No production code, `map_CURRENT.html`, geometry, masks, house math, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_41b_density_retention_transfer_study.png`
- `validation/reports/phase2_41b_density_retention_transfer_study.json`
