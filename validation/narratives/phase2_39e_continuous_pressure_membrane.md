# Phase 2.39e - Continuous Pressure Membrane

This validation-only refinement responds to the Phase 2.39d edge diagnosis. The remaining problem is not blur but material breakup: low-opacity areas can read as powder, dust, mist, or sprayed transparency when the renderer reduces visible field integrity along with opacity.

## Method

Phase 2.36f geometry remains locked. The renderer uses paired boundary correspondence from the existing centerline, left boundary, and right boundary polylines. Each side is normalized from carrier `u=0` to boundary `u=1`; the solved side width is the visual transfer domain. No degree subdivisions, half-degree rings, fake shells, production geometry changes, cap changes, or mask changes are introduced.

The field is rendered as a continuous translucent pressure membrane. Every normalized side slice is filled, including the outer tail. Edge opacity is low but nonzero, so reduced intensity does not become field fragmentation. No cell skipping, particulate density, noise, visible contour strokes, lamination strokes, blur filters, gaussian feathering, white carrier strokes, or `ImageData` nearest-pixel pressure sampling are used. The carrier is drawn last from the same station geometry.

## Modes Rendered

- Carrier only
- Translucent glass membrane
- Lacquered pressure membrane
- Coherent plasma candidate

## Visual Assessment

This pass prioritizes material continuity over disappearance. The edge should read as low-transmission pressure material rather than dust or mist. The strongest first candidate is coherent plasma candidate. The tradeoff is that restoring continuous edge integrity can reintroduce more full-width field presence than Phase 2.39d. Visual QA should balance membrane continuity against near-ridge compression.

This is a controlled tradeoff, not final visual success. The next correction should tune `plasma_candidate` only: preserve nonzero edge alpha and continuous material integrity, but slightly steepen near-ridge decay and reduce baseline edge alpha if the field feels too broad.

## Governance

No production code, `map_CURRENT.html`, Phase 2.36f geometry, dynamic side-cap math, masks, house-width sampling, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_39e_continuous_pressure_membrane.html`
- `validation/visual_targets/phase2_39e_continuous_pressure_membrane_mc.png`
- `validation/visual_targets/phase2_39e_continuous_pressure_membrane_asc.png`
- `validation/reports/phase2_39e_continuous_pressure_membrane.json`
