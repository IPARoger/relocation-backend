# Async Overlay Decoupling Validation

Date: 2026-05-17

Served URL:
`http://127.0.0.1:8000/map_CURRENT.html?generation_mode=truth_grid&debugGeometry=1`

## Summary

House region rendering is now decoupled from angular overlay rendering in the frontend. The first request fetches and renders house polygons without `aspect_overlay`; when an angular overlay is selected, a second request fetches overlay features with `house_conditions: []` and renders them when ready.

No truth-grid math, ASC/MC aspect calculations, generation defaults, or contour fallback behavior were changed.

## Validation Results

- ASC all-major House 7: polygons rendered at ~1.1s; overlay ready at ~12.8s.
- ASC all-major House 8: polygons rendered at ~1.1s; overlay ready at ~13.6s.
- ASC all-major House 9: polygons rendered at ~0.8s; overlay ready at ~11.9s.
- MC all-major House 7: polygons and overlay were ready at ~1.2s.
- Debug badge showed `generation_mode=truth_grid`, `resolution=0.75`, and `validation_contradictions=0`.
- Known false probes remained excluded.
- Relocated-chart popup endpoint smoke test returned 200.

## Validation Artifacts

- `validation/reports/async_overlay_decoupling_check.json`
- `validation/reports/house_789_async_overlay_check.json`
