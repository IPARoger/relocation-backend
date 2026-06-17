# Phase 2.39d - Near-Ridge Compressed Pressure Topology

This validation-only refinement continues the hidden-mechanism direction from Phase 2.39c but corrects pressure distribution. Phase 2.39c hid visible scaffolding, but the field risked collapsing back into a full-width atmospheric wash. Phase 2.39d compresses most visible pressure into the first 10-18% of normalized side-width and lets the remaining width decay into a quiet resonance tail.

## Method

Phase 2.36f geometry remains locked. The renderer uses paired boundary correspondence from the existing centerline, left boundary, and right boundary polylines. Each side is normalized from carrier `u=0` to boundary `u=1`; the solved side width is the visual transfer domain. No degree subdivisions, half-degree rings, fake shells, production geometry changes, cap changes, or mask changes are introduced.

The field uses high-density boundary-parametric surface cells with a steep near-ridge pressure transfer. Visible contour strokes, lamination strokes, blur filters, gaussian feathering, white carrier strokes, and `ImageData` nearest-pixel pressure sampling are not used. The carrier is drawn last from the same station geometry.

## Modes Rendered

- Carrier only
- Compressed 12% field
- Compressed 18% field
- Quiet-tail candidate

## Visual Assessment

The pressure distribution is corrected relative to Phase 2.39c: most visible information is near the carrier, with a faster outward decay and a quieter outer field. The rendering mechanism remains hidden, and the carrier remains saturated and continuous. MC and ASC both improve as near-ridge pressure studies.

The strongest candidate is quiet-tail candidate. The first-run issue is that the field is now extremely restrained in screenshots. The full-width atmospheric wash is reduced, but the wider solved domain may become visually under-explained if pressure is compressed too aggressively. This is ready for visual QA as a pressure-distribution diagnostic, not final visual success.

The next correction should tune that single candidate only: slightly stronger carrier-adjacent body versus slightly quieter outer residual tail, without adding contours, laminations, or visible topology marks.

## Governance

No production code, `map_CURRENT.html`, Phase 2.36f geometry, dynamic side-cap math, masks, house-width sampling, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_39d_compressed_pressure_topology.html`
- `validation/visual_targets/phase2_39d_compressed_pressure_topology_mc.png`
- `validation/visual_targets/phase2_39d_compressed_pressure_topology_asc.png`
- `validation/reports/phase2_39d_compressed_pressure_topology.json`
