# Phase 3.14 — Stop / Select One Real Polygon Only

## Outcome

Selected exactly **one real existing polygon overlay** and exactly **one border segment** for the next tiny discovery step.

- **Selected polygon source file**: `validation/geojson/integration/truth_grid-high_northern-sun-house-7.geojson`
- **Selected polygon feature**: `canonicalFeatureId = truth-grid-house-0-sun-7-0`
- **Selected single edge segment** (for first discovery work): first outer-ring edge from:
  - `[148.5, -65.0]` to `[156.0, -65.0]` (lon, lat)

## Why this polygon was chosen

1. It is **real project-derived geometry** already used in truth-grid integration validation, not synthetic corridor geometry.
2. It is tied to validated chart workflow context documented in `validation/reports/truth_grid_integration_summary.json` and `validation/narratives/truth_grid_integration.md`.
3. It belongs to the high-northern validated set from prior browser validation history.
4. It allows strict single-variable discipline: one polygon, one edge, no animation, no multi-region dynamics.

## Sun in 1st-house preference check

- Searched current geojson validation sources for Sun house 1 geometry.
- No `sun-house-1` / `house-1` integration files were found in `validation/geojson`.
- Therefore selected one real existing chart-derived region from available validated integration data (Sun house 7 high-northern).

## Real vs synthetic classification

- **Classification**: **Real project-derived geometry**
- **Reason**: Directly loaded from existing truth-grid integration GeoJSON produced by project pipeline (`generation_mode: truth_grid`, metadata present in feature properties).
- **Not used**: synthetic diagonal corridors, aspect-to-angle bands, three-region sandbox constructs.

## Static proof artifact (no animation)

Created static proof page (single polygon + single edge only):
- `validation/sandboxes/phase3_14_polygon_selection_static.html`

Captured screenshot:
- `validation/screenshots/phase3_14_polygon_selection/01_selected_polygon_single_edge.png`

Page label includes:
- source file path
- selected canonical feature id
- explicit declaration of single chosen edge segment

## Exact files changed

- `validation/sandboxes/phase3_14_polygon_selection_static.html` (new)
- `validation/screenshots/phase3_14_polygon_selection/01_selected_polygon_single_edge.png` (new)
- `CURSOR_EXPORT_PHASE_3_14_POLYGON_SELECTION.md` (new)

## Git status summary (focused)

```text
 M validation/sandboxes/phase3_01_rain_reveal_sandbox.html
?? validation/sandboxes/phase3_14_polygon_selection_static.html
?? validation/screenshots/phase3_14_polygon_selection/01_selected_polygon_single_edge.png
?? CURSOR_EXPORT_PHASE_3_14_POLYGON_SELECTION.md
```

Note: `validation/sandboxes/phase3_01_rain_reveal_sandbox.html` was already modified from prior phases; no new Phase 3.14 animation behavior was added.

## Recommendation for next tiny step

Use this exact selected edge segment only, and run a **static edge-neighborhood occupancy probe** (no motion, no fill) that marks which side of this edge contains confirmed truth cells, to validate edge-side discovery logic before any dynamic behavior resumes.

