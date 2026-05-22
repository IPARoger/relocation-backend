# Canonical vs Legacy Parity Diagnostics

Date: 2026-05-22

## Scope

Phase 1.12 adds quantitative parity diagnostics between topology-refined canonical samples and legacy visible geometry. The diagnostics run only when canonical visible debug mode is explicitly enabled:

```text
?canonicalVisible=1
```

Default production remains `legacy_search_regions`. No aura, animation, gradient styling, cache integration, scheduler production wiring, astrology math changes, or production substrate switching were added.

## What Is Compared

The diagnostic compares three canonical populations against legacy geometry:

- coarse canonical viewport samples,
- coarse samples adjacent to occupied/non-occupied topology boundaries,
- topology-refined edge samples from Phase 1.11.

Legacy geometry is evaluated as point-in-polygon for polygon features and screen-distance-to-line for line features. This matters because the current legacy aspect overlay can be visible linework rather than filled polygon area.

## Why Exact Visual Identity Is Not The Goal

Legacy output is a visible geometry approximation. Canonical output is sampled truth from `/screen-pixel-truth`. Exact visual identity would reward compatibility with legacy artifacts rather than convergence toward truth.

The goal is measurable agreement where both systems describe the same occupied region, plus clear diagnosis when they disagree.

## Metrics Observed

For the debug ASC viewport at `canonicalBlock=12`:

- coarse canonical samples: 5025,
- refined edge samples: 360,
- refinement depth: 1,
- coarse occupied overlap: 38.889%,
- boundary occupied overlap: 53.846%,
- refined-edge occupied overlap: 76.667%,
- coarse occupied disagreement: 0.657% of all coarse samples,
- boundary occupied disagreement: 20% of boundary samples,
- refined-edge occupied disagreement: 5.833% of refined samples,
- refined-edge agreement improvement: 14.167 percentage points,
- refined false positives: 1,
- refined false negatives: 20,
- cap-adjacent refined disagreements: 2,
- seam disagreements: 0,
- refinement pass: about 4-5 ms,
- parity comparison pass: about 53-54 ms after geometry indexing,
- total canonical debug elapsed: about 33-34 ms in the smoke comparison path.

## Where Canonical Appears Superior

Topology refinement improves agreement specifically at boundaries, where coarse sampling was weakest. It does this by adding truth samples near detected occupancy frontiers, not by hiding disagreement.

MC stability remains clean in the existing continuity diagnostic path: at `canonicalBlock=8`, MC retains zero heading/curvature variance and zero discontinuities.

## Where Canonical Still Underperforms

Refined-edge disagreement remains. Most observed refined disagreement is false negative against the legacy line-distance envelope, meaning legacy linework marks nearby occupied pixels that the sampled canonical truth did not mark at those exact points.

This can come from block-size sampling, the chosen legacy line tolerance, actual canonical/legacy geometry mismatch, or legacy geometry being visually wider than its mathematical centerline.

## Disagreement Sources

The current viewport does not prove a fundamental geometry mismatch. It shows:

- topology refinement improves boundary agreement,
- cap-adjacent disagreements still exist,
- seam disagreement was not observed,
- remaining edge disagreement needs targeted tests with multiple block sizes and legacy tolerance windows.

Some disagreement is likely legacy artifact or representation mismatch: visible legacy linework has width on screen, while canonical truth samples are point classifications.

## Production Migration Viability

Production migration is approaching viability for diagnostic comparison, not for default rendering. Canonical parity is converging, but the remaining disagreement needs classification before perceptual/aura work:

- topology vs geometry,
- legacy line-width artifact vs true mismatch,
- cap-edge behavior,
- zoom/tolerance invariance.

The next perceptual/aura phase should wait until these parity metrics are tracked across several representative conditions.
