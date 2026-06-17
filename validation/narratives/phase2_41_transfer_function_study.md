# Phase 2.41 - Geometry-Free Transfer-Function Study

This validation-only study stops all topology, map, orb, curve, and geometry work. It isolates the remaining problem: the pressure transfer function itself.

## Method

No maps, curves, astrology, masks, polygons, ASC, or MC geometry are used. Each panel is a simple rectangle. The left edge is the carrier ridge. The right edge is the outer field boundary. The horizontal coordinate is normalized transfer distance `u=0..1`.

The board is rendered offline with Python, PIL, and numpy at 4x supersampling. Every candidate is a continuous scalar function. There is no noise, particulate dropout, contour marking, strip construction, or geometry-derived artifact.

## Candidates

- Exponential Pressure
- Harmonic Pressure
- Logistic Release
- Fibonacci Power
- Enamel Membrane
- Plasma Density
- Gaussian Comparison
- Linear Fade Comparison
- Hybrid Candidate

The Gaussian and Linear examples are intentional controls: they should reveal what still reads as blur, fog, or blue fading to transparent. The stronger candidates are expected to be Hybrid Candidate, Plasma Density, Exponential Pressure, and Harmonic Pressure, pending visual QA.

## Visual Doctrine

The target is not blue fading to transparent. The target is pressure releasing continuously: one coherent material body, compressed near-ridge density, continuous release, non-powder edge, and solid chroma even at low opacity.

## First-Run Audit

The board is now strictly geometry-free and label overlap was fixed after the first render. However, the perceptual result is still only partial: several candidates read as refined gradients rather than a fully solved pressure-release phenomenon. Plasma Density, Hybrid Candidate, Exponential Pressure, and Harmonic Pressure remain the strongest candidates for human visual QA, but none should be treated as final doctrine yet.

## Governance

No production code, `map_CURRENT.html`, geometry, masks, house math, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_41_transfer_function_study.png`
- `validation/reports/phase2_41_transfer_function_study.json`
