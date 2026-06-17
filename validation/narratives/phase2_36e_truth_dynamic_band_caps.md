# Phase 2.36e - Truth-Derived Dynamic Band Caps Blocker Report

## Status

Phase 2.36e is blocked as a complete visual artifact pass.

The MC side-cap cases are available from real chart truth, but the required ASC Case A and ASC Case B were not found in a bounded search of the currently available validated/stress profiles and selected major planet/aspect combinations.

Per instruction, no schematic ASC examples and no fabricated dynamic bands were generated.

## Core Rule

For each side of an exact aspect-to-angle centerline:

`effective_side_width = min(default_or_user_orb_for_aspect, cap_percentage * adjacent_house_width)`

For this validation pass:

- default orb cap: `10 degrees`,
- cap percentage: `0.30`,
- sides computed independently.

This replaces constant asymmetry such as `3/10` or `10/3` all along a line. The width should begin at the requested orb where the adjacent house/space is large enough and shrink only where real adjacent space forces it to shrink.

## MC Evidence Available

The MC method uses house 9 and house 10 spaces around the MC/10th-house cusp.

### MC Case A

- Profile: `baseline_validated`
- Condition: Moon square MC
- Result: house 9 / left side narrows while house 10 / right side remains full.

| Latitude | Longitude | House 9 width | Effective left width | House 10 width | Effective right width |
|---:|---:|---:|---:|---:|---:|
| 0.0 | 34.8965 | 30.667 | 10.0 | 32.494 | 10.0 |
| 19.697 | 34.8965 | 28.467 | 8.54 | 33.012 | 10.0 |
| 39.394 | 34.8965 | 25.772 | 7.732 | 33.771 | 10.0 |
| 65.0 | 34.8965 | 18.716 | 5.615 | 36.76 | 10.0 |

### MC Case B

- Profile: `baseline_validated`
- Condition: Sun square MC
- Result: house 10 / right side narrows while house 9 / left side remains full.

| Latitude | Longitude | House 9 width | Effective left width | House 10 width | Effective right width |
|---:|---:|---:|---:|---:|---:|
| 0.0 | -103.1134 | 32.503 | 10.0 | 30.704 | 10.0 |
| 19.697 | -103.1134 | 33.046 | 10.0 | 28.516 | 8.555 |
| 39.394 | -103.1134 | 33.842 | 10.0 | 25.837 | 7.751 |
| 65.0 | -103.1134 | 36.978 | 10.0 | 18.84 | 5.652 |

## ASC Blocker

The required ASC cases were not found quickly enough to support honest artifact generation.

Required but not found:

- ASC Case A: 12th-house side narrows while 1st-house side remains wider/full.
- ASC Case B: 1st-house side narrows while 12th-house side remains wider/full.

Search scope:

- profiles: `baseline_validated`, `edge_high_north`, `edge_southern`, and selected high-latitude/stress fixtures,
- planets: Sun, Moon, Jupiter, Saturn, Uranus,
- aspects: conjunction, sextile, square, trine, opposition,
- method: sampled ASC root tracing by latitude with house 12 / house 1 widths computed from `swe.houses`.

Result: no qualifying ASC branch was found where one side dropped to capped width while the opposite side remained full and the branch started from a normal region.

## Generalization Notes

The same modular rule should eventually generalize as follows:

- MC: adjacent spaces are 9th / 10th.
- ASC: adjacent spaces are 12th / 1st.
- IC: adjacent spaces are 3rd / 4th.
- DSC: adjacent spaces are 6th / 7th.

IC and DSC were not implemented in this blocked pass.

## Governance Closeout

Gradient/color/aura styling remains blocked until dynamic cap geometry is approved across the required cases.

No production code, `map_CURRENT.html`, backend behavior, fetch behavior, scheduler/cache execution, aura implementation, product UI, roadmap file, or unrelated file was edited.

## High-Latitude Continuation

A follow-up targeted search generated temporary validation-only high-latitude chart assumptions for:

- Reykjavik, Iceland,
- Anchorage, Alaska,
- Stockholm, Sweden,
- Tromso, Norway,
- Fairbanks, Alaska,
- Ushuaia, Argentina,
- Punta Arenas, Chile.

The search used solstice/equinox-style dates and multiple UTC birth times. These generated charts were not added to production profile files.

### What Was Found

Strong ASC-adjacent house compression exists at high latitudes when scanning fixed longitudes.

Examples from the high-latitude scan:

- `1988-06-21 00:00 UTC`, longitude `-20`: 12th-side effective width moves from `10` at latitude `0` to `8.717` at latitude `50`, `5.718` at latitude `60`, and `1.856` at latitude `65`, while the 1st side remains `10`.
- `1988-06-21 00:00 UTC`, longitude `10`: 1st-side effective width moves from `10` at latitude `0` to `3.802` at latitude `65`, while the 12th side remains `10`.

### Why This Is Still Blocked

Those fixed-longitude compression examples are not enough for Phase 2.36e approval.

When the promising candidates were validated as exact ASC aspect centerlines, the real centerline shifted longitude by latitude. Along that solved real ASC centerline, the same side compression disappeared in the tested candidates.

Therefore the blocker is not mathematical proof that ASC cases cannot exist. It is an implementation-method/search-breadth blocker:

- high-latitude adjacent house compression exists,
- but no qualifying exact aspect-to-ASC branch was found with the bounded search and branch-tracing method used here.

No ASC visual artifacts were created because doing so would risk presenting fixed-longitude compression as if it were aspect-to-ASC centerline compression.

## Fairbanks Focused ASC Validation

A narrowed follow-up tested the existing `baseline_validated` Jan 13 1976 chart relocated to Fairbanks, Alaska (`64.8378`, `-147.7164`).

Relocated Fairbanks house spans:

- House 12: `12.699` degrees
- House 1: `25.672` degrees

The nearest ASC aspect is Uranus conjunct ASC. Uranus longitude is `216.771741` and relocated Fairbanks ASC is `216.920478`, with an orb delta of `0.148736` degrees.

A real Uranus conjunct ASC branch was traced through the Fairbanks high-latitude region. Along that branch, both adjacent sides are capped because both 12th and 1st house spans are below 30 degrees, but the 12th side narrows more strongly:

| Latitude | Longitude | House 12 span | Effective 12th width | House 1 span | Effective 1st width |
|---:|---:|---:|---:|---:|---:|
| 35 | -169.5672 | 23.809 | 7.143 | 28.917 | 8.675 |
| 40 | -167.5802 | 22.491 | 6.747 | 28.768 | 8.63 |
| 45 | -165.2599 | 21.051 | 6.315 | 28.571 | 8.571 |
| 50 | -162.4629 | 19.442 | 5.833 | 28.295 | 8.489 |
| 55 | -158.9555 | 17.592 | 5.278 | 27.872 | 8.361 |
| 60 | -154.3226 | 15.388 | 4.616 | 27.135 | 8.14 |
| 65 | -147.7304 | 12.63 | 3.789 | 25.571 | 7.671 |

Artifact:

- `validation/visual_targets/phase2_36e_truth_dynamic_band_caps_asc_fairbanks.png`

This is real Swiss Ephemeris geometry and not schematic drawing. It does not prove a perfect one-side-full ASC case, because the 1st side is also capped. It does validate that the modular side-cap renderer follows real adjacent house widths along a real ASC aspect branch.
