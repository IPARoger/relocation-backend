# Phase 2.42 - Locked Transfer Geometry Reintegration

This validation-only phase reintroduces real geometry using the locked Phase 2.41d transfer reference. The transfer function is no longer exploratory. The renderer is subordinate to the approved transfer.

## Source Of Truth

The transfer source is `validation/visual_targets/phase2_41d_locked_transfer_reference.png`. Its sampled profile is treated as frozen for beta purposes. No new curve logic, delayed body, speed-bump, topology theory, contour logic, membrane language, or visual reinterpretation is introduced.

## Geometry

The geometry source is the Phase 2.36f validation artifact. Centerline, left boundary, right boundary, and polygon inputs remain unchanged. MC and ASC both use the same locked transfer behavior; only their geometry differs.

## Method

The renderer samples the locked 2.41d RGB transfer into a LUT. It then densely samples the centerline-to-left/right boundary domains and applies the LUT proportionally from centerline `u=0` to boundary `u=1`. The render is offline and supersampled. An exact projected polygon-domain mask is applied before and after smoothing/downsampling so sampling coverage cannot create rectangular footprints.

## QA Rule

If the result appears to drift from the locked Phase 2.41d transfer, the transfer must not be changed. Only sampling, interpolation, masking, or compositing may be adjusted.

## First-Run Audit

The locked transfer is preserved, and MC/ASC use the same transfer behavior with geometry as the only intended difference. No white centerline is visible. The previous rectangular sampling footprint issue is improved by exact polygon-domain masking.

Faint horizontal endpoint edges may still be visible in the offline pseudo-basemap context. These are coverage/masking artifacts, not transfer drift. Human visual QA should check for residual endpoint-edge artifacts, but any further changes must preserve the locked transfer and adjust only sampling, coverage, or edge antialiasing.

## Governance

No production code, `map_CURRENT.html`, Phase 2.36f geometry, dynamic side-cap math, masks, house-width sampling, rain, virga, animation, caching, scheduler work, production UI, staging, or commit work was performed.

## Artifacts

- `validation/visual_targets/phase2_42_locked_transfer_geometry_mc.png`
- `validation/visual_targets/phase2_42_locked_transfer_geometry_asc.png`
- `validation/reports/phase2_42_locked_transfer_geometry.json`
