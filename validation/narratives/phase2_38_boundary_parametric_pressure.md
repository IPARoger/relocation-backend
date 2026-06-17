# Phase 2.38 - Boundary-Parametric Pressure-Field Renderer Prototype

This validation/design prototype replaces the Phase 2.37 raster pressure-field method with a boundary-parametric renderer. Phase 2.36f geometry remains immutable: centerline, left boundary, right boundary, polygon masks, dynamic side caps, and house-width sampling are not changed.

## Why Phase 2.37 Was Insufficient

Phase 2.37 evaluated opacity per pixel in projected screen space. For each pixel, it found the nearest centerline segment and measured a ray distance to the polygon boundary. That removed explicit degree rings, but the pixel grid became the implicit subdivision. The visible carrier was also drawn separately from the pressure field, so ASC curves could expose wobble, raster softness, and a glow-like or airbrushed feel.

## Boundary-Parametric Method

Phase 2.38 resamples the locked centerline into stations. At each station, the local centerline segment defines a tangent, and the 90-degree normal defines the transverse pressure direction. The normal is oriented by the corresponding locked left/right boundary side.

The renderer then intersects the oriented normal with the locked left boundary polyline and the opposite normal with the locked right boundary polyline. Those intersections define the solved side-width domains. Each side is normalized from centerline `u=0` to boundary `u=1`, and the transfer function is evaluated across that normalized width. The field is rendered as stitched quadrilateral cells between adjacent stations.

This is not degree subdivision, half-degree rings, blur, or image-space glow. The strips are rendering tessellation for a solved geometric domain.

## Modes Rendered

- Centerline only
- Topographic steep falloff
- Fibonacci falloff
- Harmonic/overtone falloff
- Convex speed-bump/heavy middle

## First-Run Issues

Normal intersection diagnostics are recorded in the JSON report. MC solved cleanly with zero normal-intersection failures. ASC exposed 14 unique station failures, repeated across the five rendered modes for 70 diagnostic records total. The misses occur near open curve ends where the strict projected normal ray does not intersect the locked boundary segment on one side.

This should not be patched by inventing geometry. The smallest correction is to keep Phase 2.36f geometry unchanged but add a boundary correspondence pass for curved cases: interpolate matched left/right boundary stations by centerline parameter first, then use those corresponded endpoints as the transverse domain when the strict normal ray misses near open ends.

## Visual Assessment

The prototype appears more structurally tied to the carrier line than Phase 2.37 because the carrier and pressure strips now share station geometry. The ASC curve improves relative to the raster pressure version: less nearest-segment wobble, less airbrushed fog, and a clearer relationship between side width and pressure domain.

However, Phase 2.38 v1 is not yet a complete renderer candidate. It is ready for visual QA as a diagnostic prototype, but ASC endpoint correspondence needs another rendering pass before this method can be treated as solved. Minor tessellation/compositing artifacts also remain possible and require visual review.

## Governance

No production code, `map_CURRENT.html`, Phase 2.36f geometry, dynamic side-cap math, house-width sampling, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_38_boundary_parametric_pressure.html`
- `validation/visual_targets/phase2_38_boundary_parametric_pressure_mc.png`
- `validation/visual_targets/phase2_38_boundary_parametric_pressure_asc.png`
- `validation/reports/phase2_38_boundary_parametric_pressure.json`
