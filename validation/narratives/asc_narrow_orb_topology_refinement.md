# ASC Narrow-Orb Topology Refinement

Date: 2026-05-22

## Scope

Phase 1.15 adds a targeted debug-only refinement rule for narrow-orb ASC/DSC aspect-to-angle cases. It is active only inside the canonical visible diagnostic path:

```text
?canonicalVisible=1
```

Default production remains `legacy_search_regions`. No aura, gradients, animation, cache integration, production scheduler wiring, smoothing, interpolation, contour fallback, or astrology math change was made.

## Targeted Rule

The rule applies only when the canonical debug payload contains:

- `aspect_to_angle`,
- angle `asc` or `dsc`,
- orb `<= 0.5`.

For those cases, the existing transition-cell refinement remains the first pass. Sparse transition cells then receive a second-level subdivision. To avoid globally widening the line, the second-level pass retains at most one positive sub-sample per sparse transition cell, selecting the positive closest to that cell's center.

This is not a global slowdown:

- MC cases stay at depth 1,
- regular ASC cases with wider orbs stay at depth 1,
- house and angle-sign combinations stay at depth 1,
- high-latitude ASC remains measured but not automatically broadened.

## Wall Metrics

The full-pixel wall case for narrow-orb Sun conjunct ASC changed as follows:

| Metric | One-level baseline | Targeted rule |
| --- | ---: | ---: |
| refined sample count | 20 | 21 |
| second-level candidates | 0 | 16 |
| retained second-level positives | 0 | 1 |
| canonical false negatives vs wall | 1 | 1 |
| canonical false positives vs wall | 0 | 1 |
| canonical disagreement vs wall | 5.000% | 9.524% |
| legacy disagreement at same samples | 0.000% | 4.762% |

The broader ASC + Sun house case remained unchanged:

- targeted: false,
- max depth: 1,
- canonical false negatives: 0,
- canonical disagreement: 3.571%,
- canonical remains closer to wall than legacy.

The high-latitude ASC case remained unchanged:

- targeted: false,
- max depth: 1,
- canonical false negatives: 3,
- canonical disagreement: 6.897%,
- canonical remains closer to wall than legacy.

MC/seam behavior remained clean:

- targeted: false,
- no second-level refinement,
- seam-centered MC canonical remains wall-correct in the previous wall classification.

## Interpretation

The targeted second-level pass found additional narrow-orb positive evidence, but it did not reduce false negatives against the 1px wall in the compact diagnostic viewport. Retaining more positives widened the debug topology and increased false positives; retaining only one positive per sparse cell bounded the widening but still did not improve wall parity.

This means the remaining narrow-orb ASC issue is not solved by simply adding more sub-cell samples around the same transition cells. The likely issue is representation/alignment between sparse sample centers and the 1px wall line, not astrology math.

## Acceptability

The targeted rule is safe enough as diagnostic instrumentation because it is narrow, debug-only, and does not affect MC or production behavior. It is not enough to declare ASC/narrow-orb ready for perceptual/aura work.

Remaining imperfections are still structural, not overlay grace. Phase 1.16 should probably focus on contour/topology extraction from the 1px wall or a wall-guided edge metric, not additional local thickening.
