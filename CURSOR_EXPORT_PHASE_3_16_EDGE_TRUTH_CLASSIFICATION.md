# PHASE 3.16 - STATIC EDGE TRUTH CLASSIFICATION

## Result

PASS.

Created a static edge-side truth proof at:

`validation/sandboxes/phase3_16_edge_truth_classification.html`

The page renders the same single real Sun-in-1 polygon from Phase 3.15, hides the full polygon border, highlights one chosen border segment, and shows a small cluster of mathematically classified sample dots near that segment.

No animation, particles, probes, reproduction, rain/reveal systems, pressure systems, wake propagation, timers, fades, transitions, multiple polygons, or synthetic polygon geometry were added.

## Exact Polygon Source

The polygon source is unchanged from Phase 3.15:

- Backend file: `main_centerline_FIXER.py`
- Endpoint: `POST /search-regions`
- Mode: `generation_mode: "contour"`
- Condition: Sun in house 1
- Chart: Jan 13 1976, 7:47 AM New York City
- Backend time: `1976-01-13 12.78333 UTC`

Request:

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

Verified returned feature:

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

## Exact Chosen Edge

Chosen polygon exterior-ring edge index:

`22`

Edge endpoints:

```text
A: lon -85.80149558666838, lat 31.5
B: lon -79.80507534609015, lat 40.5
```

Only this edge is highlighted, using a restrained red/orange line. The full polygon border is hidden.

## Exact Containment Method

Containment uses the returned GeoJSON polygon geometry in the browser:

- The polygon exterior ring is tested with ray-casting point-in-ring.
- Interior rings, if present, are treated as holes and exclude points from containment.
- Each sample dot is classified by `pointInPolygon(point, rings)` against the actual returned polygon coordinates.

No truth labels are manually assigned. The only manual choice is which real returned polygon edge to inspect.

## Sample Points

Sample points are generated from the chosen edge by taking three positions along the segment and four local normal offsets, for 12 total points. Each point is then classified mathematically by containment.

```text
s1-1  lon -83.303747, lat 33.084635  OUTSIDE
s1-2  lon -83.761459, lat 33.389594  OUTSIDE
s1-3  lon -84.843323, lat 34.110406  INSIDE
s1-4  lon -85.301034, lat 34.415365  INSIDE
s2-1  lon -81.804642, lat 35.334635  OUTSIDE
s2-2  lon -82.262353, lat 35.639594  OUTSIDE
s2-3  lon -83.344217, lat 36.360406  INSIDE
s2-4  lon -83.801929, lat 36.665365  INSIDE
s3-1  lon -80.305537, lat 37.584635  OUTSIDE
s3-2  lon -80.763248, lat 37.889594  OUTSIDE
s3-3  lon -81.845112, lat 38.610406  INSIDE
s3-4  lon -82.302824, lat 38.915365  INSIDE
```

Verified count:

- Total samples: `12`
- Inside: `6`
- Outside: `6`

## Static Verification

Automated browser verification loaded the sandbox and confirmed:

- `window.__phase316State.ok === true`
- Polygon source: `POST /search-regions generation_mode=contour`
- One returned Sun-in-1 feature: `house-0-sun-1-0`
- Chosen edge index: `22`
- Sample count: `12`
- Inside/outside results are present and printed on-page.

Keyword scan confirmed no use of:

- `requestAnimationFrame`
- `setTimeout`
- `setInterval`
- `transition`
- `animation`
- `particle`
- `probe`
- `reproduction`
- `pressure`
- `wake`

## Why This Phase Matters

This phase establishes edge-side truth before any dynamic discovery behavior resumes. If the renderer cannot clearly demonstrate that one real polygon border separates true points from false points, then later discovery, condensation, or frontier behavior has no trustworthy target. Phase 3.16 proves the smallest inspectable unit: one real boundary segment, nearby generated samples, and mathematical inside/outside classification against actual project geometry.

## Files Changed

- `validation/sandboxes/phase3_16_edge_truth_classification.html`
- `CURSOR_EXPORT_PHASE_3_16_EDGE_TRUTH_CLASSIFICATION.md`

No commit was made.
