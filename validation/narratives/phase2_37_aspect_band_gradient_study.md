# Phase 2.37 - Topographic Pressure-Field Transfer Study

This validation-only refinement adopts a topographic pressure-field model. Phase 2.36f geometry remains locked. The centerline is treated as the mathematically exact carrier wave, and the surrounding field is a continuous pressure falloff inside the already-derived mask.

## Rendering Model

The renderer computes the real truth-derived boundary first, then evaluates opacity from normalized distance to the carrier wave. For each pixel, the nearest centerline projection is found, the pixel side is identified, and the distance from that centerline point to the unchanged polygon boundary on that side becomes normalized distance 1.0. This means a 10-degree side, 8-degree side, 6-degree side, 3-degree side, or dynamically capped side all receive the same continuous 0-to-1 transfer model after the boundary exists.

No opacity is derived from degree subdivisions, half-degree steps, artificial rings, or nested band fills.

## Modes Rendered

- Centerline only
- Topographic steep falloff
- Fibonacci falloff
- Harmonic/overtone falloff
- Soft bell curve / Gaussian
- Convex speed-bump/heavy mode

## Validation Findings

The generated artifacts indicate that the centerline-only mode is a single unfilled carrier line, the falloff modes are continuous rather than striated, the centerline is not visually too thick, the outer tail remains subtle, and map readability is preserved. Topographic steep falloff, harmonic/overtone falloff, and Fibonacci falloff are the strongest candidates for continued doctrine work. Gaussian remains a soft comparison mode, and convex speed-bump remains intentionally heavy.

## Governance

No centerline geometry, dynamic side-cap math, polygon mask generation, house-width sampling, or Phase 2.36f source geometry was changed. No rain, virga, animation, production integration, cache work, or scheduler work was introduced.

## Artifacts

- `validation/visual_targets/phase2_37_aspect_band_gradient_study.html`
- `validation/visual_targets/phase2_37_aspect_band_gradient_mc.png`
- `validation/visual_targets/phase2_37_aspect_band_gradient_asc.png`
- `validation/reports/phase2_37_aspect_band_gradient_study.json`
