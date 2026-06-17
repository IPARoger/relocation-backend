# Phase 2.39f - Unified Pressure Body

This validation-only refinement responds to the Phase 2.39d/2.39e diagnosis: the problem is no longer blur alone, but visible primitive decomposition. Prior passes could expose strips, seams, membranes, or field construction artifacts. Phase 2.39f tests whether the field reads more coherently when each side is rendered as one continuous pressure body.

## First-Run Issues

The initial iterative bilinear per-cell renderer timed out in-browser. A second paired-boundary scalar pass also timed out. The final artifact therefore uses a lightweight single-membrane side-gradient prototype so screenshots could be produced without changing Phase 2.36f geometry. This is a visual-methodology prototype, not the final local normalized shader.

## Method

Phase 2.36f geometry remains locked. The renderer uses the existing centerline, left boundary, and right boundary polylines. Each side is treated as one continuous membrane from carrier to solved side boundary. No degree subdivisions, half-degree rings, fake shells, production geometry changes, cap changes, or mask changes are introduced.

The renderer draws one filled side membrane per side, then draws the carrier last. No visible strips, quad boundaries, contours, laminations, cell skipping, noise, blur filters, white carrier strokes, or degree rings are used.

## Modes Rendered

- Carrier only
- Unified pressure body
- Coherent plasma body
- Translucent enamel body

## Visual Assessment

This pass is meant to test visual unity: whether removing primitive decomposition and giving the near-ridge region more body makes the field feel like one coherent pressure structure. The strongest first candidate is coherent plasma body. If this direction is visually approved, the next step should be a performant local normalized shader or equivalent renderer that preserves this unified-body language without returning to visible strip primitives.

The first-run limitation is visible in ASC: the lightweight side-membrane prototype can read as a broad polygonal side wedge rather than a final local pressure topology. This artifact should therefore be used to judge unified-body language and seam reduction, not as proof of the final renderer method.

## Governance

No production code, `map_CURRENT.html`, Phase 2.36f geometry, dynamic side-cap math, masks, house-width sampling, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_39f_unified_pressure_body.html`
- `validation/visual_targets/phase2_39f_unified_pressure_body_mc.png`
- `validation/visual_targets/phase2_39f_unified_pressure_body_asc.png`
- `validation/reports/phase2_39f_unified_pressure_body.json`
