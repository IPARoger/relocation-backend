# Phase 2.43 - Orthogonal Transport Renderer

This validation-only phase keeps the Phase 2.41d transfer locked and addresses only geometric transport. The approved rectangular gradient should be transported through curvature like a high-quality curved gradient stroke, not warped as one giant polygon fill.

## Source Of Truth

The transfer source is `validation/visual_targets/phase2_41d_locked_transfer_reference.png`. The transfer remains frozen. No new transfer curves, visual language, pressure philosophy, topology theory, contour logic, or membrane theory is introduced.

## Geometry

The geometry source is the Phase 2.36f validation artifact. Centerline, left boundary, right boundary, and polygon inputs remain unchanged.

## Method

The offline renderer samples the locked 2.41d transfer into a LUT. It resamples the centerline and boundaries densely. At each station it computes local tangent and local orthogonal direction, then transports the locked transfer across local cross-sections from centerline `u=0` to boundary `u=1`. Neighboring cross-sections overlap smoothly to avoid station seams. The projected polygon mask is applied so the field remains inside the locked geometry.

The transfer is not globally warped across a polygon and is not redesigned. The renderer only changes transport.

## QA Questions

1. Does the curved version still feel like the approved rectangle?
2. Does the field maintain coherent directional pressure?
3. Does the curve preserve dense mids?
4. Does the tail release intentionally instead of spraying outward?
5. Does the renderer now feel vector-clean instead of foggy?

## Governance

No production code, `map_CURRENT.html`, Phase 2.36f geometry, dynamic side-cap math, masks, house-width sampling, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_43_orthogonal_transport_mc.png`
- `validation/visual_targets/phase2_43_orthogonal_transport_asc.png`
- `validation/reports/phase2_43_orthogonal_transport.json`
