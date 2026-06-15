# Phase 2.48 - Extreme Asymmetry Stress Test

This is a validation-only structural truth test. It does not improve aesthetics, redesign texture, redesign transport, or integrate with the map.

## Frozen Invariants

- Transport
- Geometry
- Local `(s,u)` architecture
- Asymmetry handling
- Hierarchy logic
- Surface coherence logic

## Stress Cases

1. Fixed: left `10`, right `1`
2. Fixed: left `10`, right `0.5`
3. Dynamic: left `10`, right `10 -> 0.5`
4. Dynamic: left `10`, right `3 -> 0.25`

The board renders diagnostic graphite and teal versions so collapse behavior is readable without changing the material logic.

## QA Result

The side-local profile scaling holds structurally. The compressed side samples the full profile over local `side_u = 0..1`, so it is the same material at smaller scale rather than a cropped 10-unit side.

At `0.5` and especially `0.25` units, the compressed side can read nearly line-like because the physical/display width approaches pixel collapse. This is an expected stress result, not evidence of a separate ridge stroke or transport redesign.

Continuity survives in the generated board. Tonal hierarchy survives clearly at `1` unit and becomes marginal but structurally truthful at `0.5` and `0.25` units.

No production integration, map change, staging, or commit work was performed.
