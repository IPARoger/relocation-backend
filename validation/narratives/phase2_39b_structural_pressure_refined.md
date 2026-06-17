# Phase 2.39b - Refined Structural Pressure Field

This validation-only refinement keeps the structural/topographic direction from Phase 2.39 but reduces visible contour-line behavior. The goal is a unified topographic pressure field: carrier sovereignty, compressed near-ridge pressure, continuous transition, and structural organization without alpha fog or diagrammatic contour art.

## Method

Phase 2.36f geometry remains locked. The renderer uses paired boundary correspondence from the existing centerline, left boundary, and right boundary polylines. Each side is normalized from carrier `u=0` to boundary `u=1`; the solved side width is the visual transfer domain. No degree subdivisions, half-degree rings, fake shells, production geometry changes, or mask changes are introduced.

The visual transfer uses SVG vector surfaces: low-opacity normalized-domain ribbons establish continuity, while very low-contrast compressed micro-laminations add structural pressure intelligence. The saturated carrier is drawn last from the same station geometry. There is no raster `ImageData` pressure field, blur filter, gaussian feather, or white carrier stroke.

## Modes Rendered

- Carrier only
- Unified pressure surface
- Ridge compression
- Merged laminations
- Premium hybrid candidate

## Visual Assessment

Visible striation is reduced compared with Phase 2.39, especially in unified pressure and premium hybrid modes. The carrier remains continuous and saturated, with no white centerline artifact observed in the generated screenshots. The field reads more structurally than the earlier blur/alpha-fog studies, though the ridge-compression mode still risks exposing individual structural marks as stripes.

MC and ASC both improve as design studies. ASC benefits from the paired boundary-correspondence domain and from reducing hard contour-line dominance. The strongest candidates are unified pressure surface and premium hybrid candidate. Human visual QA should choose between them before another tuning pass.

## Strict Visual-Methodology Audit

1. Carrier line continuous and saturated everywhere: **pass**. The carrier is drawn last from the same station geometry and appears continuous in MC and ASC.
2. White or washed-out centerline artifacts: **pass**. No white carrier stroke is used, and no white centerline artifact is visible in the first-run screenshots.
3. Structural bands merged rather than stripes: **partial**. Unified pressure and premium hybrid reduce visible striation, but ridge compression and some micro-laminations can still read as structural marks if pushed further.
4. Field reads as topographic pressure rather than blur/glow: **partial**. The vector surface reduces alpha-fog behavior and is more structural than Phases 2.37/2.38, but unified pressure still uses translucent ribbons and may be judged too soft by visual QA.
5. Pressure consistent without random stronger/weaker pockets: **partial**. The field is more consistent than Phase 2.39, but subtle local density variation remains where micro-laminations and ribbons overlap.
6. Field remains inside locked Phase 2.36f mask: **pass**. The renderer uses paired correspondence between the locked centerline, leftBoundary, and rightBoundary polylines and does not extend beyond those side domains.
7. MC and ASC both improved: **pass**. Both improve over Phase 2.39 in carrier continuity and reduced line-art dominance.

Overall result: **diagnostic success, not final visual success**.

Smallest next correction: choose one candidate, likely unified pressure or premium hybrid, then tune density and contrast in a single-mode artifact. Reduce ridge-compression-style marks, slightly strengthen carrier/near-ridge pressure, and keep outer ribbons subtle without adding blur.

## Governance

No production code, `map_CURRENT.html`, Phase 2.36f geometry, dynamic side-cap math, masks, house-width sampling, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_39b_structural_pressure_refined.html`
- `validation/visual_targets/phase2_39b_structural_pressure_refined_mc.png`
- `validation/visual_targets/phase2_39b_structural_pressure_refined_asc.png`
- `validation/reports/phase2_39b_structural_pressure_refined.json`
