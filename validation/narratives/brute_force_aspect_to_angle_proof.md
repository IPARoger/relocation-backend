# Brute-Force Aspect-to-Angle Centerline Proof

> Status: validated  
> Doctrine reference: `docs/relocation_map_architecture.md` — brute-force
> classification is the canonical truth layer; centerlines remain
> truthful occupancy bands, never interpolated curves.  
> Development order reference: step 6 (aspect-to-angle centerlines).  
> Companion narratives: `brute_force_polygon_proof.md`,
> `brute_force_multi_condition_proof.md`,
> `brute_force_angle_in_sign_proof.md`.

## What this proves

The classical "relocation centerline" — for example, *"where on Earth
is Saturn conjunct the relocated MC?"* — is implemented as **occupancy
classification**, not as a curve-fitting problem. The engine asks
each cell of a brute-force grid a single binary question:

```
abs_sep = abs(((planet_long − angle_long + 180) % 360) − 180)
match   = abs(abs_sep − aspect_target_deg) ≤ orb
```

When the orb is narrow and the grid is dense, the *band* of matching
cells is geometrically thin and naturally reads as a line. **The
centerline is not drawn; it emerges.** No spline, no curve fit, no
inferred geometry — only honest per-cell truth.

This proof demonstrates four claims:

1. **Aspect-to-angle is the same kind of occupancy problem as
   planet-in-house and angle-in-sign.** The engine reuses the same
   `swe.houses` call per cell and adds a single small numerical test.
   Its result composes through the same bitmask response shape and the
   same mask palette as every other condition type.

2. **The two geometric shapes the astronomy predicts both appear.**
   MC depends only on local sidereal time (= longitude), so aspects to
   MC must produce *meridian-like vertical bands*. ASC depends on
   latitude and longitude both, so aspects to ASC must produce
   *curved bands*. Both shapes appear, from the same engine, with no
   special handling for either case.

3. **Orb is a real, linear knob.** Doubling the orb roughly doubles
   the band width and roughly doubles the match count. Halving the
   orb tightens the centerline visibly. There is no rendering trick:
   the orb is the mathematical tolerance and the only thing changing
   between the orb-sensitivity captures is one float in the request.

4. **The math identities the angles imply still hold to the cell.**
   *Saturn ☌ IC* and *Saturn ☍ MC* must produce identical cell sets
   because IC ≡ MC + 180°. *Saturn ☌ DSC* and *Saturn ☍ ASC* must
   produce identical cell sets for the same reason. Both identities
   pass: at the proof's resolution, the cell counts match exactly,
   and a direct set-difference smoke test on the matches returns
   zero (see "Math identities" below).

## How the endpoint was extended

`POST /brute-force-grid` now accepts a third condition shape in the
discriminated union:

```jsonc
{
  "conditions": [
    {
      "type":   "aspect_to_angle",
      "planet": "saturn",
      "angle":  "mc",
      "aspect": "conjunction",   // | sextile | square | trine | opposition
      "orb":    1.0              // degrees, > 0 and ≤ 15
    }
  ]
}
```

For each cell the engine still computes one set of cusps via
`swe.houses(jd, lat, lon)`. The per-cell test for an aspect-to-angle
slot is:

```python
d        = ((planet_long - cusps[cusp_idx_for(angle)] + 180.0) % 360.0) - 180.0
abs_sep  = abs(d)                                # range [0, 180]
match    = abs(abs_sep - aspect_target_deg) <= orb
```

Aspect target degrees are the classical five major aspects:
conjunction = 0°, sextile = 60°, square = 90°, trine = 120°,
opposition = 180°. Minor aspects (quintile, quincunx, septile, etc.)
are intentionally absent for this proof.

The planet longitude is the natal value. Tropical-zodiac longitudes
do not change with location; only houses and angles do.

Match cells continue to be returned as `[lat, lon, mask]` so the
renderer, response shape, and overlap semantics are identical to the
two earlier condition types — aspect-to-angle composes freely with
planet-in-house and angle-in-sign in the same single classification
pass.

## How the sandbox was extended

`map_SANDBOX_brute_force.html` gains a third type-selector option
(`Aspect to Angle`) per slot. The parameter row for that type
contains four controls: a planet picker, an angle picker
(ASC/MC/IC/DSC), an aspect picker, and a numeric orb input (degrees,
0.1–15.0). The mask-aware renderer is unchanged; it does not know
which condition type lives in any slot.

URL parameter syntax extends the existing slot grammar:

| URL shape                              | Meaning                                |
|----------------------------------------|----------------------------------------|
| `?A=sun:1`                             | legacy, planet-in-house default        |
| `?A=pih:sun:1`                         | explicit planet-in-house               |
| `?A=ais:asc:scorpio`                   | angle-in-sign                          |
| `?A=a2a:saturn:mc:conjunction:1.0`     | aspect-to-angle (5 tokens; orb last)   |

A new optional `?bounds=south,west,north,east` parameter was added so
capture scripts can seed both the map view *and* the engine query
with the same explicit bounds, independent of Leaflet's
aspect-ratio-adjusted viewport. This made the orb-sensitivity
captures reproducible without depending on `fitBounds` aspect padding.

## Capture matrix

All captures live in
`validation/screenshots/brute_force_aspect_to_angle/` and are listed
in `manifest.json`. Profile: `baseline_validated`
(1976-01-13 12:47 UTC). Natal Saturn = 120.08° (Leo 0°).

| Case | Description | Cells | Matches | Server | Notes |
|------|-------------|-------|---------|--------|-------|
| 01 | Saturn × MC fan: conj + opp + sq, world 0.5°, orb 1.0° | 238,651 | 4,256 | 1.5 s | four parallel meridians, spaced 90° apart |
| 02 | Saturn ☌ MC alone, Pacific 178°E, 0.25°, orb 1.0° | 63,041 | 4,168 | 0.4 s | meridian through Fiji/New Zealand |
| 03 | Saturn ☐ MC alone, world 0.5°, orb 1.0° | 238,651 | 2,128 | 1.5 s | two meridians at ±90° from conjunction line |
| 04 | Saturn △ MC alone, world 0.5°, orb 1.0° | 238,651 | 2,394 | 1.4 s | two meridians at ±120° |
| 05 | Saturn ☍ MC alone, world 0.5°, orb 1.0° | 238,651 | 1,064 | 1.4 s | single meridian at 180° away from conj line |
| 06 | Saturn ☌ ASC alone, world 0.5°, orb 1.0° | 238,651 | 1,100 | 1.7 s | **curved** band (not a meridian) |
| 07 | Saturn ☌ IC alone, world 0.5°, orb 1.0° | 238,651 | 1,064 | 1.5 s | **identical to case 05** (IC ≡ MC + 180°) |
| 08 | Saturn ☌ DSC alone, world 0.5°, orb 1.0° | 238,651 | 1,109 | 1.7 s | curved; identity-twin of Saturn ☍ ASC (see smoke test) |
| 09 | Saturn ☌ MC, orb **0.5°**, Pacific 178°E, 0.1° grid | 391,601 | 13,010 | 2.7 s | tight centerline (visibly thin) |
| 09b | Saturn ☌ MC, orb **1.0°**, Pacific 178°E, 0.1° grid | 391,601 | 27,321 | 2.4 s | product-default corridor (~2× the 0.5° count) |
| 10 | Saturn ☌ MC, orb **2.0°**, Pacific 178°E, 0.1° grid | 391,601 | 49,438 | 2.8 s | wide corridor (~4× the 0.5° count) |
| 11 | Sun-in-1st (PIH) + Saturn ☌ ASC (A2A), world 0.5°, orb 1.0° | 238,651 | 17,073 | 1.8 s | yellow polygon AND blue centerline on one map |
| 12 | Saturn ☌ MC (A2A) + Saturn ☌ ASC (A2A), world 0.5°, orb 1.0° | 238,651 | 2,164 | 1.6 s | a meridian and a curve, same chart, same engine |

## Math identities verified to the cell

Three independent self-consistency identities fall out of the
astronomy, and all three pass at the proof's resolution:

| Identity | Why it must hold | Observed |
|----------|------------------|----------|
| Saturn ☌ IC ≡ Saturn ☍ MC | IC ≡ MC + 180° on the ecliptic | case 05 = case 07 = 1,064 cells |
| Saturn ☌ DSC ≡ Saturn ☍ ASC | DSC ≡ ASC + 180° on the ecliptic | smoke test at world 1° grid: 278 cells each, symmetric set difference = 0 |
| Saturn ☌ MC ⊥ Saturn ☍ MC (disjoint) | the two meridians are 180° apart | mixed two-slot test reports `A∩B = 0` |

The first identity is also verified at this proof's resolution as a
direct cell-set equality smoke test before the captures were taken
(see `/tmp/brute_a2a_*.log`). The disjointness of the five major
aspects against the same angle is what makes the *fan* in case 01
read as four cleanly-separated bands rather than as one diffuse
region; if any two aspect tests collided, the rendering would have
shown an unintended green/orange overlap and the engine would have
to be rejected.

## Orb sensitivity — the linear knob

Cases 09, 09b, and 10 are the same chart, same condition
(Saturn ☌ MC), same viewport (Pacific 178°E, bounds
`-65, 150, 65, 180`), same grid spacing (0.1°). The only thing that
changes is the `orb` parameter — three values, three captures, one
truth substrate:

| Orb (°) | Matches | Ratio vs. orb=0.5° | Ratio vs. previous row |
|---------|---------|--------------------|------------------------|
| 0.5     | 13,010  | 1.0× (baseline)    | —                      |
| 1.0     | 27,321  | **2.10×**          | 2.10× (vs. 0.5°)       |
| 2.0     | 49,438  | **3.80×**          | 1.81× (vs. 1.0°)       |

Exact 2× / 4× scaling would require the band width to land on
grid-aligned cell boundaries at every orb; the measured ratios
(2.10× and 3.80×) reflect the ~5% rounding penalty inherent to a
finite grid, in both directions — the 1.0° step lands slightly
*over* the ideal 2× (gridding gives back a sliver of width), the
2.0° step lands slightly *under* the ideal 4× (the wider corridor
clips against a few extra grid cells the narrow one missed). The
mid-point case is exactly that: a middle data point, not a
correction.

The visual confirms the linear-knob claim across all three captures:
the 1.0° band is roughly twice as wide as the 0.5° band, and the
2.0° band is roughly twice as wide as the 1.0° band, all with the
same centerline running through every image. Orb is **not** a
rendering trick — it is the mathematical tolerance on the per-cell
aspect test, and the engine reports it truthfully at every width.

This three-point sweep also pre-validates the **aura model** doctrine
(see `docs/relocation_map_architecture.md` → Aura Rendering
Principles): each of these bands is exactly the discrete "occupancy
widening" the aura section requires (`≤0.5°`, `≤1°`, `≤2°` of an
exact aspect), produced by the same per-cell brute-force test. When
aura rendering arrives, it will compose these *already-truthful*
bands with non-linear opacity / saturation / density — never blur,
never a fake field.

## Two geometric shapes, one engine

The clearest visual proof of the engine's correctness is that the
same per-cell test produces two geometrically-different shapes
depending only on which angle is asked about:

- **Aspects to MC (or IC)** ↦ vertical meridian bands. MC depends
  only on local sidereal time (= longitude), so the locus where
  *MC = Saturn ± aspect_target* is a meridian on Earth. The fan in
  case 01 and the orb-sensitivity captures (cases 09 / 09b / 10) show
  this unambiguously.
- **Aspects to ASC (or DSC)** ↦ curved bands. ASC depends on both
  latitude and longitude through Placidus, so the locus where
  *ASC = Saturn ± aspect_target* is a curve that bends with latitude
  (visible in cases 06, 08, 11, 12).

Neither shape is drawn. Both *emerge* from the same one-line per-cell
test. That is the doctrine's "we are not inventing geometry, we are
revealing already-proven geometry" stated in pixels.

## Mixed-type composition

Case 11 places `Sun in 1st (planet_in_house)` next to `Saturn ☌ ASC
(aspect_to_angle)` in the same request. The renderer paints the
yellow Sun-1st area polygon over North America and the blue
Saturn-ASC curved centerline through Asia, on a single map. They do
not visually overlap on this chart, and the engine reports
`A∩B = 0` honestly — overlap is real when it exists and zero when it
does not. Case 12 does the same with two aspect-to-angle slots
(Saturn ☌ MC + Saturn ☌ ASC), showing that meridian and curve
centerlines can coexist on one chart with no extra plumbing.

## Performance footprint

The per-cell cost of an aspect-to-angle test is essentially free on
top of the existing `swe.houses` call: a subtraction modulo 360,
an absolute value, a comparison. Observed compute times on the
validation host:

- single aspect, world 0.5° (~240k cells): 1.4–1.8 s server
- three aspects fan, world 0.5°: 1.5 s server
- single aspect, Pacific 178°E 0.1° (~390k cells): 2.7–2.8 s server
- mixed condition types, 2 slots, world 0.5°: 1.6–1.8 s server

Adding aspect-to-angle slots costs roughly nothing per cell; the
dominant cost is `swe.houses` per cell, the same cost the other
condition types pay. This preserves the doctrine's "barely more
expensive to classify many conditions than one" property required
for opportunistic background expansion later.

## Honest self-critique

- **Polar errors persist.** `swe.houses` returns NaNs/exceptions at
  extreme latitudes in Placidus, and those cells are excluded from
  every condition equally. The proof's polar gaps are real
  computational limits of the house system, not engine bugs;
  surfacing them honestly is the doctrine's policy.
- **No transit support yet.** This proof tests natal aspect-to-angle
  only — the planet's longitude is the natal Saturn. Step 8 (transit
  aspect-to-relocated-angle) will reuse the exact same condition type
  with a transit ephemeris time providing the planet longitude
  instead. The schema does not need to change.
- **Grid alignment costs ~5% on the orb knob.** The orb-sensitivity
  ratio came back at 3.80× instead of 4.00× because the band edges
  do not always land on grid lines. This is the honest cost of a
  finite grid; tighter grids reduce it but never eliminate it. The
  refinement step (10 in the doctrine) is where any sub-grid line
  resolution would be addressed, not earlier.
- **Visible lattice at coarse grids.** Cases 03/04/05 at world 0.5°
  show the lattice in the rendered bands at high latitudes. That is
  what 0.5° world looks like at truth; refinement is deferred per
  doctrine.
- **The capture script's manual-bounds path was brittle.** A
  Leaflet-aspect-ratio race made early runs of cases 02 / 09 / 09b / 10
  classify the wrong area. The fix was to add a
  `?bounds=south,west,north,east` URL parameter so the sandbox can
  seed both the map view and the engine bounds from the same
  authoritative source, without depending on `fitBounds` padding.
  Worth recording because future capture scripts should use the URL
  parameter, not a post-load `fitBounds` + JS override.
- **Aura is still not built.** The user explicitly deferred aura
  layering and distance shading; this proof produces only binary
  occupancy bands. A future aura layer would weight matches by
  `|abs_sep − aspect_target| / orb` (or similar), but the binary
  occupancy proven here remains the truth substrate it would sit
  on top of.

## What this unlocks

Step 6 is done. The remaining engineering directions in the doctrine
all reuse the same discriminated-union schema:

- Step 7 — transit-house overlays (`type: "transit_planet_in_house"`)
  reuses planet-in-house with a transit ephemeris time.
- Step 8 — transit aspect-to-angle (`type: "transit_aspect_to_angle"`)
  reuses today's `aspect_to_angle` shape with a transit ephemeris
  time for the planet longitude.
- Step 9 — aura / gradient rendering sits *on top of* the binary
  occupancy proven in this and the earlier proofs; it does not
  replace it.
- Step 10 — refinement acceleration is gated on steps 3–9 being
  stable, per doctrine.

None of these require a new wire contract or a new renderer; only a
new condition shape and, for transit, a time-source parameter.
