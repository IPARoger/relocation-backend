# Phase 2.41d - Locked Approved Transfer Reference

This validation-only artifact locks the approved transfer function from the uploaded earlier #8 Alpha-Only Control reference. It does not invent a new transfer philosophy, visual language, curve family, topology model, or pressure theory.

## Source Of Truth

The uploaded cropped approved #8 reference image is sampled directly. The generated reference preserves the same release timing, midpoint behavior, body proportion, and translucency arrival.

## Method

The renderer samples the horizontal RGB profile of the approved reference gradient, upsamples it to a high-resolution profile, applies only light smoothing to reduce screenshot quantization, and renders the same sampled transfer at narrow, medium, and wide widths. Each width uses the same transfer function scaled proportionally.

No new curve logic is introduced. No delayed body, speed-bump, late collapse, flat translucent plateau, contour logic, topology, map, geometry, mask, or production renderer work is introduced.

## Intended Renderer Macro

1. Determine centerline.
2. Determine left boundary.
3. Determine right boundary.
4. Normalize local width from centerline to boundary.
5. Apply this locked transfer proportionally across width.
6. Render continuously.

## Governance

No production code, `map_CURRENT.html`, geometry, masks, house math, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_41d_locked_transfer_reference.png`
- `validation/reports/phase2_41d_locked_transfer_reference.json`
