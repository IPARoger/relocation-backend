# Phase 2.39 - Structural Pressure Topology Study

This validation-only study responds to the Phase 2.38 diagnosis: mathematically cleaner pressure rendering still read as transparent blur paint. The failure was no longer banding; it was lack of structural organization.

## Why Phase 2.38 Was Insufficient

Phase 2.38 moved from pixel-space raster sampling to boundary-parametric quads, but the visual transfer still behaved like a transparent blue wash around a line. It reduced raster fog but retained the perceptual language of glow, watercolor, and gaussian transparency.

The target is different: a mathematically exact carrier ridge surrounded by organized pressure topology. The field should read through compression, expansion, contour density, terrace rhythm, and directional coherence, not through soft opacity alone.

## Domain Model

Phase 2.36f geometry remains locked. The study uses the existing matched centerline, left boundary, and right boundary polylines as a correspondence domain. Each side is normalized from carrier `u=0` to solved boundary `u=1`. Structural topology samples are placed across that normalized domain. They are not degree subdivisions, half-degree rings, or new truth geometry.

## Rendering Language Explored

- Carrier only
- Compressed pressure contours
- Pressure terraces
- Directional laminations
- Hybrid structural field

The prototype uses an SVG vector overlay rather than an `ImageData` raster pressure field. There is no blur pass, gaussian feather, or continuous alpha-fog wash. Semi-transparent strokes and small terrace regions are used as structural marks, not as Photoshop glow.

## Visual Assessment

The structural modes give the carrier more authority than the continuous alpha studies. Compressed contours and hybrid topology are the strongest first candidates because they show organized pressure expansion without becoming pure fog. Terrace mode is useful diagnostically but risks becoming too diagrammatic. Directional laminations improve coherence, especially in the ASC curve, but need restraint.

This is ready for visual QA as a language study. It is not production-ready and should not be integrated. The next pass should tune density, reduce visual clutter, and decide whether the final doctrine wants mostly compressed contours, mostly laminations, or a restrained hybrid.

## Governance

No production code, `map_CURRENT.html`, Phase 2.36f geometry, dynamic side-cap math, house-width sampling, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_39_structural_pressure_topology.html`
- `validation/visual_targets/phase2_39_structural_pressure_topology_mc.png`
- `validation/visual_targets/phase2_39_structural_pressure_topology_asc.png`
- `validation/reports/phase2_39_structural_pressure_topology.json`
