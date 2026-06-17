# Angle-in-Sign MVP Validation

Date: 2026-05-17

Manual QA URL:
`http://127.0.0.1:8000/map_CURRENT.html?generation_mode=truth_grid&debugGeometry=1`

## Implementation Summary

- Added `angle_sign_conditions` to `/search-regions`.
- Supported angles: `ASC`, `MC`.
- Supported signs: Aries through Pisces.
- Angle-in-sign regions use truth-grid style classification and merged rectangles.
- Regions render as polygons alongside house regions.
- Popup truth now includes `asc_sign`, `mc_sign`, `desc_sign`, and `ic_sign`.
- Existing house truth-grid generation, contour fallback, ASC/MC aspect calculations, and popup house logic were preserved.

## API Validation

Validated against:

- Baseline Validated Chart
- Edge Case - High Northern Birth
- Edge Case - Southern Hemisphere Birth

Conditions tested:

- ASC in Aries
- ASC in Taurus
- MC in Gemini

Results:

- All API requests returned `200`.
- All region requests returned nonzero polygon features.
- All validation contradictions were `0`.
- Representative polygon-center popup truth samples matched the requested sign.
- Typical request time was about `0.48s` per angle-sign condition at `0.75` degree resolution.

Detailed artifact:
`validation/reports/angle_sign_api_validation.json`

## Frontend Validation

Served-page checks:

| Profile | Condition | House | Overlay | Polygons | Angle-sign polygons | Aspect features | Contradictions |
|---|---|---:|---|---:|---:|---:|---:|
| Baseline Validated | ASC in Aries | 7 | MC all-major | 201 | 67 | 8 | 0 |
| High Northern | ASC in Taurus | 7 | ASC all-major staged | 279 | 122 | 10 | 0 |
| Southern | MC in Gemini | 9 | MC all-major | 57 | 1 | 8 | 0 |

Popup smoke:

- `/relocated-chart` returned `200`.
- Response included `asc_sign` and `mc_sign`.

Detailed artifact:
`validation/reports/angle_sign_frontend_validation.json`

## UX Notes

- Angle-sign regions use purple fill to distinguish them from house conditions.
- Normal status text remains visible without debug mode.
- Debug geometry popups now include `condition_type`, `angle`, and `sign`.
- Dropdown cleanup added event isolation for panel interactions and disabled Leaflet keyboard handling.
- Popup typography was lightly cleaned up: location headers remain bold, while planet/angle labels are plain text.

## MVP Readiness

Angle-in-Sign appears MVP-ready for `ASC` and `MC` sign regions, subject to broader manual QA. The implementation follows the same truth-field approach as house overlays and keeps region semantics deterministic.

## Caveats

- Angle-sign boundaries are rectangular truth-grid cells and can look blocky.
- Boundary clicks can still be ambiguous near grid-cell edges.
- `IC` and `DSC` are exposed in popup truth but not yet searchable.
- The interface is functional but not yet professionally organized.
