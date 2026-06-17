# Phase 2.40 - Reference Pressure Render

This validation-only artifact is an expensive offline visual target, not an implementation. It exists to show the ideal pressure-field result once so efficient production rendering can be worked backward from the target.

## Method

Phase 2.36f geometry remains locked. The renderer loads the existing centerline, left boundary, right boundary, and polygon data from the Phase 2.36f validation artifact. Each side is treated as a normalized domain from carrier `u=0` to boundary `u=1`.

The PNG is rendered offline with Python, PIL, and numpy at 4x supersampling. Dense centerline stations and dense cross-domain samples create a continuous scalar pressure field. The field has strong near-ridge body mass, fast topographic decay, and a low-opacity but materially continuous tail. The carrier is drawn last as a saturated uninterrupted ridge. Final downsampling happens once at the end.

## Visual Doctrine

The target is coherent translucent pressure material: no visible primitives, no strip seams, no powder edges, no white centerline, no contour marks, no ribbons, and no wedge/membrane read. Low opacity should not mean lower field integrity.

## Known Limitations

This is not an efficient renderer and should not be treated as production strategy. It uses a deterministic pseudo-basemap instead of Leaflet tiles so the reference image is self-contained. A light smoothing step is applied to the completed scalar material field to remove sample grain; this is a reference-render finishing step, not a blur/glow rendering doctrine.

The first-run image is not yet the final ideal target. It still shows a faint rectangular/sampling footprint near the lower band ends. The smallest next correction is to apply an exact polygon-domain alpha mask before smoothing and final downsampling, so supersampled sample coverage cannot reveal rectangular station footprints.

## Governance

No production code, `map_CURRENT.html`, Phase 2.36f geometry, dynamic side-cap math, masks, house-width sampling, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_40_reference_pressure_render.png`
- `validation/reports/phase2_40_reference_pressure_render.json`
