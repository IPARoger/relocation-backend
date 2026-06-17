# Phase 2.36c - Truth-Derived Aspect-Band Boundary Proof Extension

## Purpose

Phase 2.36c creates validation/design artifacts for truth-derived on-map aspect-to-angle band boundaries before any gradient or aura color study.

This revision fixes the symmetric proof images so diagnostic annotation does not obscure the band geometry, and adds truth-derived asymmetric side-width artifacts generated from the same sampled Saturn conjunct ASC truth field.

## Chart / Profile Used

- Profile: `baseline_validated` / Baseline Validated Chart
- Birth date: `1976-01-13`
- Birth time: `12:47 UTC`
- Place label: `Test`

## Aspect-To-Angle Condition

- Condition type: `aspect_to_angle`
- Planet: `saturn`
- Angle: `asc`
- Aspect: `conjunction`

## Math / Source

The geometry is derived from the same source formula used by the existing backend diagnostic aspect-to-angle classifier:

1. Compute natal Saturn longitude with Swiss Ephemeris: `swe.calc_ut(jd, swe.SATURN)`.
2. For each sampled map point, compute relocated Placidus angles with `swe.houses(jd, lat, lon, b"P")`.
3. Use relocated ASC from `ascmc[0]`.
4. Compute signed separation: `((planet_long - asc + 180) % 360) - 180`.
5. Derive the centerline from the `0 degree` contour.
6. Derive left-side boundary from the negative signed threshold and right-side boundary from the positive signed threshold.

The source classification is truth-derived. Boundary vectors are sampled contours over that truth field, not analytic exact vector solutions.

## Symmetric Artifacts

The symmetric 3, 6, 8, and 10 degree artifacts are truth-derived sampled orb-band geometry.

The in-map diagnostic inset and line labels were removed. Explanatory labels now live outside the map frame in the legend/explanation text, so they do not obscure the proof branch.

Width ordering remains correct: `10 > 8 > 6 > 3` by sampled match count.

## Asymmetric Artifacts

The asymmetric artifacts are truth-derived sampled independent-side-width geometry:

- `left 3 / right 10`: `-3 <= signed_sep <= +10`
- `left 10 / right 3`: `-10 <= signed_sep <= +3`
- optional `left 6 / right 10`: `-6 <= signed_sep <= +10`
- optional `left 10 / right 6`: `-10 <= signed_sep <= +6`

These are not schematic. They are generated from the same sampled truth-derived Saturn-ASC field and the same real 0 degree centerline as the symmetric artifacts.

They prove the diagnostic artifact generator can render unequal left/right signed side widths from the real centerline. They do not prove adjacent-house/space cap behavior.

## Line Provenance

- Neutral mask: sampled occupancy polygon for the requested signed range; neutral presentation only, no stroke.
- Dashed centerline: truth-derived 0 degree Saturn-ASC contour.
- Solid left boundary: truth-derived negative-side contour at `-left_degrees`.
- Solid right boundary: truth-derived positive-side contour at `+right_degrees`.
- Western same-condition component: truth-derived but suppressed from proof view pending separate component/seam validation.

No unexplained duplicate curves remain in the proof view.

## Rendering Scope

The visual output remains boundary/mask only:

- flat neutral fill,
- visible outer bounds,
- visible dashed centerline,
- no gradient fill,
- no aura color,
- no blur,
- no feathering,
- no opacity falloff,
- no rain,
- no virga,
- no dots,
- no particles,
- no animation.

The HTML uses a diagnostic Leaflet map surface only. It does not edit `map_CURRENT.html`, alter production behavior, or change the default renderer.

## Sampling / Diagnostic Status

- Sampled lon/lat grid: `0.5 degree`
- Latitude range: `-65.0` to `65.0`
- Longitude range: `-180.0` to `180.0`
- Valid points: `188181`
- Failed points: `0`

This artifact is truth-derived sampled diagnostic evidence for the eastern/Australia proof branch only. It is not final renderer output.

## What Remains Unproven

- Exact analytic vector boundaries rather than sampled contours.
- Complete multi-component aspect-band proof, including the western same-condition component.
- Antimeridian/component handling.
- Adjacent-house/space capping for aspect-band side widths.
- Asymmetric side-cap behavior caused by adjacent-house/space caps.
- Production renderer integration.
- Gradient, color, opacity, and aura visual treatment.

## Suitability

This artifact is suitable as truth-derived sampled evidence for symmetric orb-band width ordering and independent signed-side-width rendering before gradient studies.

It is not suitable as final renderer output and not sufficient to approve adjacent-house/space capping.
