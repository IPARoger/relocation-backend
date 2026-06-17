# Phase 2.36d - Truth-Derived Dynamic Side-Cap Validation

## Purpose

Phase 2.36d validates dynamic adjacent-house side capping along real truth-derived aspect-to-angle centerlines.

This is validation/design artifact work only. It does not edit production code, `map_CURRENT.html`, backend runtime behavior, renderer integration, scheduler/cache, aura rendering, product UI, or doctrine docs.

## Method

The validation uses MC aspect centerlines because the requested side language is house-9 / house-10 adjacent geometry around the MC/10th-house cusp.

For each sampled point on a real MC aspect centerline:

1. Compute Placidus cusps with `swe.houses(jd, lat, lon, b"P")`.
2. Compute house 9 span as forward zodiac distance from cusp 9 to cusp 10.
3. Compute house 10 span as forward zodiac distance from cusp 10 to cusp 11.
4. Compute side caps independently:
   - if adjacent space is below `30 deg`, side width is `min(10 deg, 30% of adjacent width)`;
   - otherwise side width remains the requested `10 deg`.

The visual boundary offsets are diagnostic presentation of the truth-derived side-width values around an MC meridian centerline. They are not production geodesic rendering.

## Chart / Profile

- Profile: `baseline_validated` / Baseline Validated Chart
- Birth date: `1976-01-13`
- Birth time: `12:47 UTC`
- Requested orb: `10 deg`

## Case A

- Condition: Moon square MC
- Centerline longitude: `34.8965`
- Result: left/9th-side cap narrows while right/10th-side remains full width.

Sample callouts:

| Latitude | House 9 span | House 10 span | Left width | Right width |
|---:|---:|---:|---:|---:|
| 0.0 | 30.667 | 32.494 | 10.0 | 10.0 |
| 19.697 | 28.467 | 33.012 | 8.54 | 10.0 |
| 39.394 | 25.772 | 33.771 | 7.732 | 10.0 |
| 65.0 | 18.716 | 36.76 | 5.615 | 10.0 |

## Case B

- Condition: Sun square MC
- Centerline longitude: `-103.1134`
- Result: right/10th-side cap narrows while left/9th-side remains full width.

Sample callouts:

| Latitude | House 9 span | House 10 span | Left width | Right width |
|---:|---:|---:|---:|---:|
| 0.0 | 32.503 | 30.704 | 10.0 | 10.0 |
| 19.697 | 33.046 | 28.516 | 10.0 | 8.555 |
| 39.394 | 33.842 | 25.837 | 10.0 | 7.751 |
| 65.0 | 36.978 | 18.84 | 10.0 | 5.652 |

## Findings

- Case A found: `True`
- Case B found: `True`
- Dynamic capping observed: `True`
- Constant asymmetry failure: `False`

These cases are not constant `3/10` or `10/3` bands. The side widths evolve along the same real centerline according to adjacent house-space widths.

## Scope Limits

- No gradient/color/aura styling was created.
- No rain, virga, particles, dots, animation, or discovery effects were created.
- No production files were touched.
- This does not validate final production geodesic rendering.
- This covers MC-adjacent house 9 / house 10 dynamic caps only; ASC-side cap behavior remains separate.
