# Staged ASC Overlay Validation

Date: 2026-05-17

Manual QA URL:
`http://127.0.0.1:8000/map_CURRENT.html?generation_mode=truth_grid&debugGeometry=1`

## Changes Validated

- ASC overlay requests now accept `aspect_resolution` and `overlay_stage`.
- ASC overlays compute the ASC grid once per request and reuse it for all requested aspect offsets.
- ASC all-major frontend rendering now requests three stages:
  - coarse: `2.0` degrees
  - medium: `1.0` degrees
  - final: `0.5` degrees
- House polygons still render before angular overlays.
- MC overlays remain on the existing fast path.

## Browser Timing Results

High Northern chart, Sun houses 7/8/9, ASC all-major:

| House | Polygons visible | First ASC overlay | Final ASC overlay | Polygon features | ASC features |
|---|---:|---:|---:|---:|---:|
| 7 | 1.49s | 1.64s | 2.10s | 157 | 10 |
| 8 | 0.82s | 0.92s | 1.43s | 126 | 10 |
| 9 | 1.02s | 1.33s | 2.00s | 56 | 10 |

High Northern chart, Sun House 7, MC all-major:

- Polygons and MC overlay ready at ~1.07s.
- MC feature count: 8.

Previous observed ASC all-major behavior:

- Async split before staged ASC: final ASC overlay ready around ~12-19s in browser validation.
- Old combined API timing before async split: ~17.2s before polygons could appear.

## API Timing Snapshot

High Northern Sun ASC all-major overlay-only request:

- coarse `2.0`: ~0.15s over HTTP, 10 features.
- medium `1.0`: ~0.52s over HTTP, 10 features.
- final `0.5`: ~2.04s over HTTP, 10 features.

## Final Output Equivalence

The final `0.5` shared-grid ASC output was compared against the previous per-offset ASC grid loop:

- Old line count: 10.
- New line count: 10.
- Offset/point-count/bbox/first-point/last-point summaries matched.

The shared-grid optimization preserves final output semantics for this fixture while removing repeated ASC grid recomputation.

## Regression Checks

- Debug badge showed `generation_mode=truth_grid`, `resolution=0.75`, `validation_contradictions=0`.
- Debug badge updated overlay stage and aspect resolution.
- Known false probes remained excluded.
- Relocated-chart popup endpoint smoke test returned `200`.
- Popup truth logic was not changed.

## Validation Artifacts

- `validation/reports/staged_asc_overlay_browser_check.json`
- `validation/reports/staged_asc_shared_grid_equivalence.json`

## Visual Caveats

- Coarse and medium ASC overlays are preview geometry and can shift when replaced by the final `0.5` overlay.
- Brief layer replacement is expected between stages; no heavy frontend smoothing was added in this prototype.
