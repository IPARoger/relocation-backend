# Manual Truth-grid QA Checklist

## URL

Open:

`http://127.0.0.1:8000/map_CURRENT.html?generation_mode=truth_grid&debugGeometry=1`

Use the served HTTP URL above. Manual QA should not use `file://`.

## Confirm Truth-grid Mode

After clicking `Find Regions`, confirm the debug badge is visible on the map and shows:

- `Generation mode: truth_grid`
- `Resolution: 0.75`
- `Debug geometry: on`
- `Feature count: <non-zero polygon count>`
- `Validation contradictions: 0`
- `Aspect overlay status: not requested`, `pending`, or `ready`

If the badge says `contour`, the URL is missing `generation_mode=truth_grid`.

## Chart Profiles To Test

- `baseline_validated` / Baseline Validated Chart
- `edge_high_north` / Edge Case - High Northern Birth
- `edge_southern` / Edge Case - Southern Hemisphere Birth

## Houses To Test

Prioritize Sun houses:

- House 7
- House 8
- House 9

Secondary regression sweep:

- House 1
- House 4
- House 10
- Two-condition tests with Planet B enabled, especially House 7 plus House 8 or 9.

## Seam Behavior

Inspect both left and right map edges around the antimeridian:

- Pacific / Fiji / New Zealand side
- Alaska / Bering Strait side
- Eastern Russia / western Aleutians
- Southern Pacific near New Zealand and Antarctica-adjacent latitudes within the displayed cap

Expected behavior:

- Rectangular truth-grid cells may meet or stop at the seam.
- No false sliver regions should appear.
- No orphan fragments should appear with popup truth contradicting the region.
- No house should visually borrow another house's feature identity.
- Minor blockiness is acceptable in truth-grid mode.

## Popup Truth Vs Overlay Truth

1. Select one chart profile and Sun House 7, 8, or 9.
2. Click `Find Regions`.
3. Click cities or arbitrary map points inside and near the edge of a colored region.
4. In the regular popup, compare the Sun house value to the selected overlay house.
5. In debug mode, click a polygon fragment and record:
   - `canonicalFeatureId`
   - `displayFeatureId`
   - `planet`
   - `house`
   - `bbox`
   - `touches +/-180`
   - `crosses +/-180`
   - `validation_contradictions`
6. For ASC/MC overlays, select `All Major Aspects`, then verify house polygons appear before the angular overlay finishes.

Expected behavior:

- Points clearly inside a region should report the same planet/house in popup truth.
- Points outside the region should not report that selected house.
- Boundary clicks can be ambiguous at grid-cell edges; record them separately from clear interior failures.
- `validation_contradictions` should remain `0`.

## How To Report Failures

For each failure, capture:

- Exact URL.
- Chart profile ID and name.
- Planet and house selection.
- Angular overlay selection, if any.
- Screenshot of the map and debug badge.
- Approximate clicked lat/lon or nearby city.
- Popup truth result.
- Debug polygon fields listed above.
- Whether the failure is:
  - false filled region,
  - missing region,
  - seam artifact,
  - wrong popup truth,
  - delayed rendering,
  - browser/rendering-only artifact.

