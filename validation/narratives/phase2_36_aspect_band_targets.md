# Phase 2.36 — Static Aspect-to-Angle Band Targets

## Purpose

Phase 2.36 creates static visual targets for aspect-to-angle bands before any further aura, renderer, or animation implementation.

These artifacts are design/validation evidence only. They are not production code, renderer integration, `map_CURRENT.html` changes, rain, virga, dots, discovery particles, or animation.

## Artifacts

- `validation/visual_targets/phase2_36_aspect_band_targets.html`
- `validation/visual_targets/phase2_36_aspect_band_10deg.png`
- `validation/visual_targets/phase2_36_aspect_band_8deg.png`
- `validation/visual_targets/phase2_36_aspect_band_6deg.png`
- `validation/visual_targets/phase2_36_aspect_band_3deg.png`
- `validation/reports/phase2_36_aspect_band_targets.json`

## Visual Approach

The targets use:

- one consistent map-like background,
- small city/map labels under the band,
- one diagonal exactness path shared by all four variants,
- a gold/yellow selected color,
- a narrow dark selected-color centerline,
- a smooth continuous selected-color gradient,
- proportional band widths for `±10°`, `±8°`, `±6°`, and `±3°` per side.

The targets intentionally avoid:

- white centerlines,
- white edges,
- frayed/noisy edges,
- stripe artifacts,
- dots or particles,
- rain,
- virga,
- production map layers,
- renderer implementation.

## Acceptance Criteria

The mockups are intended to satisfy:

- smooth continuous gradient,
- no frayed/noisy edge,
- no white centerline,
- no white edge,
- centerline is darkest/most opaque selected color,
- opacity concentrated tightly at centerline,
- rapid falloff after immediate center/core,
- most of band outside core is translucent/near-transparent,
- no visible stripe artifacts,
- no pixelated/probe-field artifacts,
- label/map readability preserved outside tight core,
- band feels like exactness crest, not fat cloudy speedbump,
- outer boundary is continuous and uniform, but extremely faint,
- centerline/core is narrow, not broad.

## Result

The generated JSON report records all mechanical checks as passing.

Human visual review is still required before implementation. These targets are candidates, not final production renderer rules.

## Rollback Scope

Rollback is limited to deleting:

- the standalone HTML target sheet,
- the four generated PNG targets,
- the JSON report,
- this narrative.

No production code, backend behavior, renderer behavior, `truth_grid_engine.py`, scheduler/cache execution, aura implementation, smoke file, roadmap file, sandbox/prototype file, or `map_CURRENT.html` behavior was changed.

## Governance Closeout

- **Accepted scope:** static aspect-to-angle band target artifacts only.
- **Rejected scope:** animation, rain, virga, dots, discovery particles, production renderer integration, `map_CURRENT.html` changes.
- **Next gate:** human review of the static PNG targets before any algorithmic or renderer implementation.
