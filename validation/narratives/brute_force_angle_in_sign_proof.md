# Brute-Force Angle-in-Sign + Mixed-Condition-Type Proof

> Status: validated  
> Doctrine reference: `docs/relocation_map_architecture.md` — brute-force
> classification is the canonical truth layer; mixed condition types
> share that substrate.  
> Development order reference: step 4 (angle-in-sign) and step 5 (mixed
> condition types) — kept as separate items in the doctrine, but step 4
> requires the schema work that also covers step 5's first half, so the
> proof is exercised together.  
> Companion narratives: `brute_force_polygon_proof.md`,
> `brute_force_multi_condition_proof.md`.

## What this proves

The brute-force classifier now accepts a **discriminated** condition
union — `planet_in_house` or `angle_in_sign` per slot — and classifies
every cell once against all conditions in a single `swe.houses` pass.
The same response shape and the same bitmask palette extend to the new
condition type without any client-side reconstruction of overlap.

This proves four claims:

1. **Angle-in-sign is the same kind of occupancy problem as
   planet-in-house.** A cell is "ASC in Scorpio" or it is not, the
   same way it is "Sun in 1st" or it is not. Same engine, same
   `cusps`, same brute-force pass, only a different per-cell test.

2. **Mixed condition types compose truthfully.** A single request can
   freely combine `planet_in_house` and `angle_in_sign` slots; every
   cell is tested against all of them in the same classification pass,
   so overlap is real ("this cell satisfies all three simultaneously")
   and is never composed by the client.

3. **The mask palette and renderer are condition-type-agnostic.** The
   sandbox draws yellow / blue / rose for slot A / B / C and the
   blended green / orange / violet / deep-slate for overlaps,
   independent of whether the slot is a planet-in-house or an
   angle-in-sign condition.

4. **The math identities the angles imply still hold to the cell.**
   IC ≡ MC + 180°, so "IC in Cancer" cell counts must match "MC in
   Capricorn" cell counts exactly. They do. DSC ≡ ASC + 180°, so
   "DSC in Taurus" must match "ASC in Scorpio". It does. A two-slot
   composition of `ASC=Capricorn` and `DSC=Cancer` must produce a
   polygon entirely painted as A∩B with `A_only = B_only = 0`. It
   does.

## How the endpoint was extended

`POST /brute-force-grid` now accepts a discriminated union per
condition slot:

```jsonc
{
  "conditions": [
    { "type": "planet_in_house", "planet": "sun", "house": 1 },
    { "type": "angle_in_sign",   "angle":  "asc", "sign":  "capricorn" },
    { "type": "angle_in_sign",   "angle":  "mc",  "sign":  "libra" }
  ]
}
```

`type` defaults to `"planet_in_house"` for back-compat with the older
condition shape, so existing clients keep working unchanged.

For each cell the engine computes one set of cusps via
`swe.houses(jd, lat, lon)` and then evaluates every condition against
those cusps:

- `planet_in_house` — unchanged: `planet_in_house(planet_long, house, cusps)`
- `angle_in_sign`   — `int(cusps[cusp_idx] // 30) == requested_sign_idx`,
  where `cusp_idx` is `0` for ASC (cusp of the 1st house), `3` for IC,
  `6` for DSC, `9` for MC.

A match is returned as `[lat, lon, mask]` where `mask` has one bit set
per slot the cell satisfies. The response carries the same statistics
shape as before: `per_mask_counts`, `overlap_counts`, and a `conditions`
array where each entry now also declares its own `type`. No new wire
contract was needed; only a new condition type slot.

## How the sandbox was extended

`map_SANDBOX_brute_force.html` was reshaped to a stacked-per-slot
layout. Each condition row is now:

```
[on/off]  [swatch]  [A]  [ type: Planet in House | Angle in Sign ]
                          [ first param ]   [ second param ]
```

Selecting `Angle in Sign` swaps the parameter row from planet/house
pickers to angle/sign pickers, and the URL parameter syntax
correspondingly extends:

| URL shape                    | Meaning                              |
|------------------------------|--------------------------------------|
| `?A=sun:1`                   | legacy: planet-in-house (default)    |
| `?A=pih:sun:1`               | explicit planet-in-house             |
| `?A=ais:asc:scorpio`         | angle-in-sign                        |
| `?B=ais:mc:libra`            | second slot — angle-in-sign          |

The mask-aware renderer is unchanged; it does not know or care which
condition type populated which slot. That asymmetry is the desired
one: the renderer paints occupancy, the engine decides what occupancy
means.

## Capture matrix

All captures live in `validation/screenshots/brute_force_angle_in_sign/`
and are listed in `manifest.json`. Profile: `baseline_validated`
(1976-01-13 12:47 UTC, Sun at 22° Capricorn).

| Case | Description | Cells | Matches | Server | Notable |
|------|-------------|-------|---------|--------|---------|
| 01 | ASC-Scorpio (Americas 0.25°) | 436,590 | 49,843 | 6.1 s | tilted ASC band |
| 02 | MC-Capricorn (Americas 0.25°) | 436,590 | 65,790 | 5.7 s | MC depends only on lon → near-vertical band |
| 03 | IC-Cancer (Americas 0.25°) | 436,590 | 65,790 | 5.6 s | **identical count to MC-Capricorn** ← see identity check below |
| 04 | DSC-Taurus (Americas 0.25°) | 436,590 | 49,843 | 6.3 s | **identical count to ASC-Scorpio** |
| 05 | ASC-Aries (world 0.5°) | 238,651 | 14,752 | 3.0 s | sign sweep frame 1/4 |
| 06 | ASC-Cancer (world 0.5°) | 238,651 | 17,135 | 3.0 s | sign sweep frame 2/4 |
| 07 | ASC-Libra (world 0.5°) | 238,651 | 14,868 | 3.0 s | sign sweep frame 3/4 |
| 08 | ASC-Capricorn (world 0.5°) | 238,651 | 17,103 | 2.8 s | sign sweep frame 4/4 |
| 09 | Sun-1st + ASC-Capricorn (Americas 0.25°) | 436,590 | 81,199 | 6.4 s | A∩B = 45,952 (real cross-type overlap) |
| 10 | Sun-1st + ASC-Capricorn + MC-Libra (Americas 0.25°) | 436,590 | 99,701 | 6.3 s | A∩B=45,952, A∩C=31,523, B∩C=29,204, **A∩B∩C=22,109** |
| 11 | ASC-Capricorn + DSC-Cancer (Americas 0.25°) | 436,590 | 64,385 | 6.1 s | **identity check**: A=B=A∩B=64,385, A_only=B_only=0 |
| 12 | Sun-1st + ASC-Capricorn + MC-Libra (world 0.5°) | 238,651 | 26,577 | 3.2 s | A∩B=11,745, A∩C=7,872, B∩C=7,299, A∩B∩C=5,521 |

## Math identities verified to the cell

Three independent self-consistency checks fall out of the data, and
all three pass exactly:

| Identity | Why it must hold | Observed |
|----------|------------------|----------|
| IC-Cancer cell count ≡ MC-Capricorn cell count | IC ≡ MC + 180°; Cancer is the sign 180° from Capricorn | both = 65,790 |
| DSC-Taurus cell count ≡ ASC-Scorpio cell count | DSC ≡ ASC + 180°; Taurus is the sign 180° from Scorpio | both = 49,843 |
| Two-slot {ASC=Capricorn, DSC=Cancer} → polygon entirely A∩B | the two conditions are the *same locus* | A=B=A∩B=64,385, A_only=B_only=0 |

These are not test fixtures we set up. They are *consequences of the
astronomy* that the brute-force engine is now exposing. If a future
optimisation path returns a different answer to any of these
identities for any cell, that optimisation is wrong by the canonical-
truth definition in the architecture doctrine.

## Three-slot mixed overlap — visual reading

Case 10 (`10_mixed_three_slot_overlap.png`) is the proof that the mask
palette renders mixed-type overlap correctly. Every region of the
palette is honestly visible:

| Region                 | Mask | Color (in sandbox)            | Cells |
|------------------------|------|-------------------------------|-------|
| Sun-1st only           | 1    | translucent yellow            | varies |
| ASC-Capricorn only     | 2    | translucent blue              | varies |
| MC-Libra only          | 4    | translucent rose              | varies |
| Sun-1st ∩ ASC-Cap      | 3    | green                         | 45,952 |
| Sun-1st ∩ MC-Lib       | 5    | orange                        | 31,523 |
| ASC-Cap ∩ MC-Lib       | 6    | violet                        | 29,204 |
| **all three**          | 7    | **deep slate**                | **22,109** |

The deep-slate core where all three conditions are simultaneously
true is the first visual confirmation that A∩B∩C is a non-empty real
region — earlier multi-condition runs (planet-in-house only) had
A∩B∩C = 0 because the three planet-in-house bands didn't cross. With
angle-in-sign included, the geometry of the three condition families
forces a meaningful triple-overlap region into view.

## Performance footprint

Angle-in-sign costs essentially nothing per cell on top of the
existing `swe.houses` call: each `angle_in_sign` slot is a
floor-divide, an int compare, and a bit-or. The dominant cost stays
where it always was — one `swe.houses` per cell.

Observed server-compute times on the validation host, baseline chart:

- single-condition, 0.25° Americas (~440k cells): ~6.1 s server
- two-slot mixed (planet + angle), 0.25° Americas: ~6.4 s server
- three-slot mixed (planet + 2 × angle), 0.25° Americas: ~6.3 s server
- three-slot mixed, 0.5° world (~240k cells): ~3.2 s server

The per-cell cost is dominated by `swe.houses`, so adding condition
slots costs only the additional per-cell tests, not additional
classification work. This is the property the doctrine relies on for
opportunistic background expansion: classifying for many conditions
at once is barely more expensive than classifying for one.

## Honest self-critique

- **No transit support yet.** This proof is natal-relocation only.
  Transit-house overlays (step 6 in the doctrine) reuse the same
  endpoint with a different time-source per cell or per request;
  step 4 deliberately does not pre-build that scaffolding.
- **Sign boundaries are exact.** A cusp at exactly 30.000 falls in
  Taurus, not Aries (we use `int(c // 30)`). For brute-force at
  0.05°–0.25° resolution this lands on negligibly few cells, but it
  is a real choice — adjacent-sign-aware boundary smoothing would
  conceptually be a "refinement" pass, not a brute-force truth fix.
- **Aspect-to-angle is still pending.** Step 6's aspect-to-angle
  centerline classifier ("Saturn conjunct relocated MC") will need a
  new condition type with its own orb. The discriminated union here
  is the schema that step 6 will extend.
- **Visible lattice at coarser grids.** Cases 05–08 at 0.5° world
  visibly show the lattice, especially in the polar belt where each
  cell is geographically large. That is what 0.5° world looks like at
  truth, not what we will ship to a polished product surface; a
  refinement layer will revisit this without changing the
  classification answers.
- **The capture script is flaky around headless Chromium tile loads.**
  Two of the runs that produced this proof saw transient "Failed to
  fetch" / `wait_for_function` timeouts on case 9 or 10. The script
  now retries once per case and falls back to any previously-good
  capture before erroring; the manifest under
  `validation/screenshots/brute_force_angle_in_sign/` reflects a
  clean 12/12 run.

## What this unlocks

Step 4 is done. The schema and renderer now compose freely across
condition types, so step 5 ("mixed condition types") is also done in
practice — every mixed example in cases 09–12 exercises it. The
remaining doctrine steps (transit-house overlays, aspect-to-angle
centerlines) reuse the same discriminated-union pattern with
additional condition types added alongside `planet_in_house` and
`angle_in_sign`. None of them require any change to the renderer or
the response contract.
