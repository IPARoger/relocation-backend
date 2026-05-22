# Wall-Guided Topology Extraction

Date: 2026-05-22

## Scope

Phase 1.16 adds continuous topology diagnostics for thin ASC/DSC and MC loci. The work is diagnostic-only and runs from the smoke harness against `?canonicalVisible=1`.

Default production remains `legacy_search_regions`. No aura, animation, cache integration, smoothing, interpolation, thickening, contour fallback, or astrology math change was made.

## Why Pixel-Center Wall Is Insufficient

The 1px wall classifies pixel centers. Thin loci can pass through a pixel cell without crossing that exact center. Phase 1.15 showed this directly: second-level subpixel samples found true positives, but raw wall-center comparison could still count them as false positives.

For thin curves, the useful question is not only "does this point equal the wall pixel center?" but also:

- are positives close to wall-positive pixels,
- are positives close to expected legacy/canonical line trajectory,
- do positives form a coherent trajectory,
- do they introduce seam/cap discontinuities.

## Diagnostics Added

For each wall case, the smoke harness now records:

- subpixel positive count,
- 1px wall-positive pixel count,
- mean/max distance from canonical positives to wall-positive pixels,
- mean/max distance from canonical positives to legacy line geometry when line geometry exists,
- centerline step continuity,
- discontinuity count,
- seam discontinuity count,
- cap-adjacent discontinuity count,
- coherent trajectory verdict.

## Topology Evidence

### Narrow-Orb Sun Conjunct ASC

- subpixel positives: 2,
- wall-positive pixels: 118,
- mean distance to wall-positive pixels: 0.5 px,
- max distance to wall-positive pixels: 1 px,
- mean/max distance to legacy line: 0 px,
- discontinuity count: 0,
- coherent trajectory: true.

Interpretation: the narrow-orb ASC positives are not random noise. They lie on the legacy line and within 1 px of wall-positive pixels. Pixel-center overlap alone undercounts the thin locus.

### ASC + Sun House

- subpixel positives: 34,
- wall-positive pixels: 3520,
- mean distance to wall-positive pixels: 0.118 px,
- max distance to wall-positive pixels: 1 px,
- discontinuity count: 0,
- coherent trajectory: true.

Interpretation: the overlap-heavy ASC/house case has coherent topology despite earlier pixel-overlap disagreement.

### High-Latitude ASC

- subpixel positives: 27,
- wall-positive pixels: 1185,
- mean distance to wall-positive pixels: 0.185 px,
- max distance to wall-positive pixels: 1 px,
- mean distance to legacy line: 1.753 px,
- max distance to legacy line: 2.828 px,
- discontinuity count: 1,
- seam discontinuity count: 0,
- cap-adjacent discontinuity count: 0,
- coherent trajectory: true.

Interpretation: high-latitude ASC remains coherent and near the wall trajectory, with one continuity break that should remain on the diagnostic backlog.

### Seam-Centered MC

- subpixel positives: 160,
- wall-positive pixels: 5760,
- mean/max distance to wall-positive pixels: 0 px,
- mean distance to legacy line: 3 px,
- max distance to legacy line: 6 px,
- discontinuity count: 0,
- seam discontinuity count: 0,
- cap-adjacent discontinuity count: 0,
- coherent trajectory: true.

Interpretation: MC remains clean. The seam anomaly is not canonical topology instability.

### Clean MC Control

- subpixel positives: 0,
- wall-positive pixels: 0,
- discontinuity count: 0.

Interpretation: the negative control remains clean.

## Root-Cause Classification

The remaining ASC issue is topology extraction/representation, not astrology math. ASC subpixel positives are coherent and close to the wall-positive trajectory. Raw pixel-center overlap is too brittle for narrow loci because a valid curve can pass through a pixel cell without occupying the center sample.

Legacy line geometry remains useful as a trajectory reference, but not as the final truth source. The canonical wall and subpixel diagnostics are more precise.

## Recommendation

Future canonical rendering for narrow lines should use a continuous topology/edge extraction abstraction instead of raw occupied blocks alone. A future renderer should derive a centerline or edge trajectory from classified samples, then use that topology as the truth substrate for any later perceptual/aura work.

Do not begin aura yet. The next safe step is a debug-only centerline/edge extraction prototype validated against the wall metrics above.
