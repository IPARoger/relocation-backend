# PHASE 3.15b - REAL SINGLE POLYGON BORDER REMOVAL

## Result

PASS.

This pass only changed the visual style of the existing Phase 3.15 sandbox polygon:

- Fill changed to translucent yellow/gold.
- Visible polygon outline stroke removed.
- Geometry unchanged.
- Backend request unchanged.
- Generation mode unchanged.
- Polygon source unchanged.
- Map setup unchanged.
- No animation, particles, dots, edge segments, or debug HUD added.

## Same backend polygon source confirmed

The sandbox still generates the polygon live from the existing backend:

- App: `main_centerline_FIXER.py`
- Endpoint: `POST /search-regions`
- Mode: `generation_mode: "contour"`
- Condition: Sun in house 1
- Chart: Jan 13 1976, 7:47 AM New York City
- Backend time: `1976-01-13 12.78333 UTC`

The request body remains:

```json
{
  "birth_year": 1976,
  "birth_month": 1,
  "birth_day": 13,
  "birth_hour_utc": 12.78333,
  "house_conditions": [{ "planet": "sun", "house": 1 }],
  "angle_sign_conditions": [],
  "generation_mode": "contour",
  "resolution": 1.5
}
```

The returned/rendered feature remains:

```json
{
  "canonicalFeatureId": "house-0-sun-1-0",
  "planet": "sun",
  "house": 1,
  "condition_index": 0,
  "overlap_count": 1,
  "generation_mode": "contour"
}
```

## What changed

Only the Leaflet style block in:

`validation/sandboxes/phase3_15_real_single_polygon.html`

Changed from a blue translucent fill with a dark outline to:

```js
style: {
  stroke: false,
  fillColor: "#d8a11d",
  fillOpacity: 0.22,
}
```

## Border removed

Confirmed: the polygon is now rendered with `stroke: false`, so there is no visible hard/dark outline stroke.

## No geometry changes

Confirmed: no changes were made to:

- `REQUEST_BODY`
- `fetchRealPolygon`
- backend endpoint
- generation mode
- feature filtering
- map initialization
- tile layer setup
- polygon source

The exact same live backend-generated Sun-in-1 polygon is rendered; only its fill/stroke styling changed.

## Follow-up deliberately deferred

Edge waviness, subpixel behavior, and any brute-force/subdivision refinement should be reviewed later.

This pass does not attempt to fix waviness, alter sampling, change geometry, change generation mode, or introduce refinement.

## Deliverables

1. `validation/sandboxes/phase3_15_real_single_polygon.html`
2. `CURSOR_EXPORT_PHASE_3_15_REAL_SINGLE_POLYGON.md`

No commit was made.
