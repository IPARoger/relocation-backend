# PHASE 3.17 - REAL PIXEL-BASED POLYGON EMERGENCE STORYBOARD

## Result

PASS.

Created a sandbox-only computational storyboard:

`validation/sandboxes/phase3_17_polygon_emergence_storyboard.html`

The page renders:

- 8 storyboard slides
- dark mode and light mode variants
- 16 total static canvas panels
- deterministic raster/pixel occupancy particles
- final vector-clean polygon state

Static proof screenshot:

`validation/screenshots/phase3_17_polygon_emergence_storyboard/01_dark_light_storyboard.png`

Screenshot metadata:

```text
PNG image data, 1600 x 1800, 8-bit/color RGB, non-interlaced
```

## Real Polygon Source

The storyboard uses the same real Sun-in-1 polygon substrate from Phase 3.15 / Phase 3.16:

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

No synthetic polygon, hand-authored shape, placeholder rectangle, production polygon edit, backend/math change, or map_CURRENT integration was added.

## Computational Basis

The storyboard is generated from real polygon geometry and deterministic occupancy logic:

- real GeoJSON polygon projection into canvas space
- point-in-polygon occupancy classification
- screen-space distance to the actual polygon boundary
- deterministic seeded particle field
- delayed color identity
- wide peak froth before edge lock
- center-out interior settlement
- boundary-weighted particle visibility
- static frame states that can later become timing doctrine

The particle field is not painterly. Particles are drawn as snapped raster-native square occupancy marks. Organic behavior comes from distribution, density, boundary distance, convergence weighting, and delayed identity assignment.

## Storyboard Doctrine Implemented

Slides:

1. `Uncertain Field` - sparse neutral silver occupancy particles; no color identity and no visible winner.
2. `Directional Sensing` - weak alignment pressure appears, still neutral and unresolved.
3. `Local Clustering` - micro-clusters and local occupancy neighborhoods form; color remains nearly absent.
4. `Border Hunting` - both sides begin clustering toward the boundary; early identity appears but the edge remains unstable.
5. `Peak Froth` - widest and densest uncertainty band; both sides temporarily overpopulate around the border.
6. `Border Lock` - the edge becomes inevitable while froth remains active around it.
7. `Virga + Rebirth` - rejected fields rise and dissolve; selected interior settlement begins from confidence zones.
8. `Silent Vector Resolution` - clean final vector polygon only, with no particles, texture, outline, or process traces.

## Addendum Correction Applied

The storyboard was revised after QA identified that the previous version revealed color identity too early and underplayed peak froth.

Corrections made:

- Act 1 and Act 2 now render neutral silver occupancy only.
- Act 3 remains mostly ambiguous, using micro-clustering rather than full border revelation.
- Color identity is gated by convergence confidence and appears late with geometry.
- Peak froth uses a much wider boundary band and stronger density before edge lock.
- Border lock happens before final cleanup, making frame 8 feel more earned.
- Frame 7 now preserves ghost/virga particles while center-out interior settlement begins.
- The slide titles now match the 8-act doctrine: uncertain field, directional sensing, local clustering, border hunting, peak froth, border lock, virga + rebirth, silent vector resolution.

Dark mode:

- near-black/navy computational field
- restrained grid
- cool scientific atmosphere
- disciplined yellow/red/blue particle families

Light mode:

- pale cartographic substrate
- restrained grid
- map-discovery feeling
- same occupancy logic and frame progression

## Rejected Aesthetics Avoided

Verified no use of:

- `requestAnimationFrame`
- `setTimeout`
- `setInterval`
- CSS transitions
- CSS animations
- gradients
- blur/filter effects
- painterly brush/watercolor/smudge logic

The artifact is a static storyboard and animation foundation, not a running animation or VFX sequence.

## Browser Verification

Automated browser verification confirmed:

```text
ok: True
source: POST /search-regions generation_mode=contour
slideCount: 8
modeCount: 2
canvasCount: 16
particleCount: 1800
```

Verified computational basis exposed by `window.__phase317State`:

```text
real GeoJSON polygon projection
point-in-polygon occupancy
screen-space boundary distance
deterministic seeded particle field
delayed color identity
wide peak froth before edge lock
center-out interior settlement
static storyboard frames
```

## Files Changed

```text
?? CURSOR_EXPORT_PHASE_3_17_POLYGON_EMERGENCE_STORYBOARD.md
?? validation/sandboxes/phase3_17_polygon_emergence_storyboard.html
?? validation/screenshots/phase3_17_polygon_emergence_storyboard/
```

No commit was made.

## Architectural Answer

This phase matters because it reframes future motion as the rendering of an already-defined computational convergence process. The storyboard proves that the desired visual language can come from occupancy, containment, boundary distance, and deterministic raster sampling before any dynamic animation is introduced.

The intended reading is now: pixels discovering a polygon, then resolving into vector form.
