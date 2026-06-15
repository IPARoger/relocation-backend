# Full-Pixel Wall Anomaly Check

Date: 2026-05-22

## Scope

Phase 1.14 uses full 1px screen-space truth as the control specimen for the remaining ASC and seam anomalies. The wall comparison is diagnostic-only and runs from the smoke harness against `?canonicalVisible=1`.

Default production remains `legacy_search_regions`. No aura, animation, cache integration, smoothing, interpolation, contour fallback, or astrology math change was made.

## Method

Each case uses a compact 420 x 480 map viewport so the wall is still true 1px screen-space classification while staying practical in smoke:

- full 1px canonical wall: every screen pixel center is classified through `/screen-pixel-truth`,
- topology-refined canonical: current `canonicalBlock=12` plus one-level boundary subdivision,
- legacy geometry: `/search-regions` GeoJSON sampled at the same comparison points.

The comparison asks whether topology-refined canonical or legacy is closer to the 1px wall at the same sample points. It also records duplicate refined pixels, longitude out-of-range samples, seam disagreements, and cap-adjacent disagreements.

## Wall Metrics

| Case | 1px wall | Refined | Legacy | Closer to wall | Root classification |
| --- | ---: | ---: | ---: | --- | --- |
| Narrow-orb Sun conjunct ASC | 1485 ms | 14 ms | 1146 ms | legacy at refined samples | refinement undersamples one wall-positive point |
| ASC angle + Sun 1st | 1450 ms | 18 ms | 3327 ms | canonical | legacy is much farther from wall; refinement adds small false-positive edge overshoot |
| High-latitude Sun conjunct ASC | 1186 ms | 17 ms | 1742 ms | canonical | canonical closer; cap-adjacent wall differences appear in coarse comparison |
| Seam-centered Saturn conjunct MC | 1607 ms | 34 ms | 5 ms | canonical | legacy misses wall-positive refined samples; no canonical wrap/duplicate error found |
| Clean MC control | 1420 ms | 13 ms | 2 ms | tie | no wall occupancy in this viewport; no boundary refinement needed |

## Detailed Findings

### Narrow-Orb Sun Conjunct ASC

Coarse canonical is closer to the wall than legacy:

- canonical disagreement: 0.143%,
- legacy disagreement: 0.571%.

At refined samples, legacy happens to match the wall better:

- canonical false negatives: 1,
- legacy false negatives: 0,
- canonical disagreement: 5%.

Classification: this does not prove ASC geometry instability. It points to insufficient boundary density / edge-neighbor sampling for very narrow-orb ASC. The refined sample set is too small to reliably capture the 1px wall line.

### ASC Angle + Sun 1st

Canonical is closer to the wall in both coarse and refined comparisons:

- coarse canonical disagreement: 0.071%,
- coarse legacy disagreement: 50.143%,
- refined canonical disagreement: 3.571%,
- refined legacy disagreement: 4.464%.

Classification: legacy is much farther from the wall in the coarse comparison. Remaining refined disagreement is mostly canonical false-positive edge overshoot, likely from one-level topology refinement around a complex overlap boundary.

### High-Latitude Sun Conjunct ASC

Canonical is closer to the wall:

- coarse canonical disagreement: 0.214%,
- coarse legacy disagreement: 1.071%,
- refined canonical disagreement: 6.897%,
- refined legacy disagreement: 8.621%.

Classification: canonical remains closer, but refined comparison worsens relative to coarse. Coarse cap-adjacent disagreement count was 4; refined cap disagreement was 0. This suggests cap-adjacent sampling and one-level edge refinement need targeted follow-up, not smoothing.

### Seam-Centered Saturn Conjunct MC

The seam anomaly is not a canonical wrap bug in this wall check:

- coarse canonical disagreement: 0%,
- coarse legacy disagreement: 0%,
- refined canonical disagreement: 0%,
- refined legacy disagreement: 25%,
- duplicate refined pixels: 0,
- longitude out-of-range refined samples: 0,
- seam disagreement count: 0.

Classification: refined canonical matches the 1px wall. Legacy is farther from the wall at refined samples. The prior seam-centered parity anomaly was likely legacy representation / line-width semantics or comparison-method mismatch, not canonical longitude normalization or duplicate wrapped samples.

### Clean MC Control

The control viewport produced no wall occupancy and no refined boundary samples. This is a valid negative control: no seam/cap/wrap issue appeared, and both canonical and legacy tied the wall.

## Answer To The Critical Question

When refined parity gets worse against legacy, the wall shows different causes by case:

- Narrow-orb ASC: current refinement can miss very thin wall-positive loci; increase topology refinement depth or target boundary density.
- ASC + house: legacy is farther from the wall overall; refined canonical has small edge overshoot.
- High-latitude ASC: canonical remains closer, but cap-adjacent and one-level refinement behavior need targeted validation.
- Seam MC: canonical is correct against the wall; legacy/comparison semantics caused the apparent parity regression.
- Clean MC: no issue reproduced.

## Phase 1.15 Recommendation

Phase 1.15 should refine topology, not switch production and not start aura. The next step should be targeted second-level boundary refinement for ASC/narrow-orb cases, plus a seam-specific comparison rule that distinguishes line-width representation from truth occupancy.

No astrology math change is justified by this wall check.
