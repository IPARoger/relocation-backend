# Multi-Condition Parity Stress Diagnostics

Date: 2026-05-22

## Scope

Phase 1.13 stress-tests topology-refined canonical parity under multi-condition and difficult geometry scenarios. The work remains diagnostic-only and active only through:

```text
?canonicalVisible=1
```

Default production remains `legacy_search_regions`. No aura, gradients, animation, cache integration, production scheduler wiring, hidden interpolation, contour fallback, astrology math changes, or production substrate switching were added.

## Stress Cases

The smoke harness now probes six debug-only parity scenarios:

- ASC angle-in-sign plus Sun-in-1st house,
- MC angle-in-sign plus Saturn-in-10th house,
- triple house overlap: Sun 1st, Moon 7th, Saturn 10th,
- narrow-orb Sun conjunct ASC,
- high-latitude Sun conjunct ASC,
- seam-centered Saturn conjunct MC.

These probes call the existing dispatch layer under `?canonicalVisible=1`, with production still locked to legacy. The canonical path remains shadow/debug output only.

## Observed Metrics

| Case | Coarse overlap | Boundary overlap | Refined overlap | Refined disagreement | Improvement |
| --- | ---: | ---: | ---: | ---: | ---: |
| ASC + Sun house | 21.739% | 66.667% | 68.336% | 23.031% | -0.196 |
| MC + Saturn house | 90.376% | 68.939% | 99.129% | 0.370% | 14.815 |
| Triple house overlap | 35.632% | 75.909% | 77.278% | 15.143% | 0 |
| Narrow-orb ASC | 9.259% | 55.556% | 23.810% | 16.667% | 0 |
| High-latitude ASC | 50.980% | 66.667% | 68.519% | 9.341% | 4.945 |
| Seam-centered MC | 100% | 100% | 50% | 25% | -25 |

Timing remained diagnostic-safe:

- canonical debug elapsed time ranged from about 33 ms to 82 ms,
- comparison time ranged from about 3 ms to 140 ms,
- every stress case remained under the smoke threshold.

## Convergence Behavior

Refinement improved or held parity in four of six cases. It was strongest for MC + Saturn house, where refined overlap reached 99.129% with only 0.370% refined disagreement.

Triple house overlap remained stable and overlap-heavy. This suggests multi-condition house topology is tractable with the current one-level refinement, though still not production-final.

ASC-heavy cases remain the dominant difficult geometry. Narrow-orb ASC and ASC + house overlap show lower refined parity and higher false-negative counts, indicating a plateau where one subdivision level and current line/point comparison tolerance are not enough to explain all disagreement.

The seam-centered MC case is intentionally suspicious: coarse and boundary agreement were perfect, but refined samples produced false positives and dropped refined overlap. That points toward representation or seam-local comparison artifacts rather than a proven MC geometry failure, especially because previous MC continuity diagnostics remain clean.

## Disagreement Clustering

Observed disagreement clusters around:

- ASC curve regions,
- narrow-orb aspect boundaries,
- cap-adjacent samples in overlap-heavy cases,
- seam-centered refined samples.

False negatives dominate ASC and multi-house overlap cases. False positives dominate seam-centered MC. This split suggests that remaining issues are not one uniform geometry failure.

Likely sources:

- topology reconstruction limits from one-level refinement,
- block quantization in curved ASC regions,
- legacy line-width/centerline representation mismatch,
- cap/seam comparison artifacts,
- possible localized geometry mismatch still requiring targeted proof.

## Production Trust Assessment

The canonical substrate is becoming more trustworthy as a diagnostic substrate. It is not yet ready to become the default production renderer.

Confidence is high for:

- MC stability away from seam stress,
- multi-house overlap tractability,
- debug-only parity measurement reproducibility.

Confidence is still incomplete for:

- ASC overlap-heavy boundaries,
- narrow-orb aspect parity,
- seam-centered refined comparison,
- cap-adjacent disagreement classification.

## Readiness For Perceptual/Aura Work

Future perceptual/aura work should wait until the remaining disagreement is classified more sharply. The substrate is close enough to continue diagnostic convergence work, but not yet ready for styling that could hide unresolved ASC, seam, or cap disagreement.
