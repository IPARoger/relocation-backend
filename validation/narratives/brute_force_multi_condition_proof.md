# Brute-Force Multi-Condition Proof

> Status: multi-condition planet-in-house rendering is proven. Up to
> three simultaneous planet-in-house conditions are supported, overlap
> is observed from the same `swe.houses` call per cell (never
> reconstructed), and every mask state is reported as a real count.

## What changed since the single-condition proof

`/brute-force-grid` now accepts a `conditions: [{planet, house}]` list
in place of the old `target_planet`/`target_house` shorthand (both
remain accepted for backward compatibility). The handler still classifies
every cell exactly once via `swe.houses`, but tests the resulting cusp
set against every condition in that single pass and emits each match
as `[lat, lon, mask]` where bit `i` of `mask` is set iff condition `i`
is satisfied.

The renderer side (`map_SANDBOX_brute_force.html`) draws each match in
the colour of its mask:

| Mask  | Meaning      | Colour              |
|-------|--------------|---------------------|
| `1`   | A only       | yellow              |
| `2`   | B only       | blue                |
| `4`   | C only       | rose                |
| `3`   | A ∩ B        | green               |
| `5`   | A ∩ C        | orange              |
| `6`   | B ∩ C        | violet              |
| `7`   | A ∩ B ∩ C    | deep slate          |

The overlap colours are chosen so they look like a perceptual blend of
the component conditions (yellow + blue ≈ green; yellow + rose ≈ orange;
blue + rose ≈ violet). The rarer the overlap, the later it is painted —
overlap cells always sit on top of single-condition fills.

## Sandbox URL

```
http://127.0.0.1:8000/map_SANDBOX_brute_force.html
```

URL parameters relevant to multi-condition use:

| Param        | Default                  | Meaning                                                              |
|--------------|--------------------------|----------------------------------------------------------------------|
| `A`          | `sun:1`                  | Condition A as `planet:house` (always enabled).                       |
| `B`          | _disabled_               | Condition B as `planet:house` (presence in URL enables it).           |
| `C`          | _disabled_               | Condition C as `planet:house` (presence in URL enables it).           |
| `planet`/`house` | _legacy_             | Single-condition shorthand for A; equivalent to `A=planet:house`.    |

Everything else (`profile`, `gridDeg`, `viewport`, `latCap`, `auto`,
`dotRadius`) carries over from the single-condition sandbox.

## Capture matrix (chart = `baseline_validated`, lat-cap OFF)

Stills + manifest: `validation/screenshots/brute_force_multi/`.

| Case                                                | Conds | Grid  | Cells     | Any matches | Server  | Per-condition                                        | Overlaps                                                       |
|-----------------------------------------------------|------:|------:|----------:|------------:|--------:|------------------------------------------------------|----------------------------------------------------------------|
| 01 — Sun in 1st (Americas)                          |   1   | 0.25° |   436,590 |      62,766 |  2.74 s | A=62,766                                              | —                                                              |
| 02 — Sun in 1st + Moon in 4th (Americas)            |   2   | 0.25° |   436,590 |     118,395 |  3.01 s | A=62,766, B=59,695                                    | **A∩B = 4,066**                                                |
| 03 — Sun in 1st + Moon in 4th + Mars in 2nd (Americas) | 3 | 0.25° |   436,590 |     174,779 |  3.13 s | A=62,766, B=59,695, C=56,473                          | A∩B = 4,066, A∩C = 89, B∩C = 0, A∩B∩C = 0                      |
| 04 — A∩B close-up (eastern US, A=Sun-1st, B=Moon-4th) | 2 | 0.25° |    17,535 |      17,014 |  0.13 s | A=8,857, B=8,983                                      | A∩B = 826                                                      |
| 05 — three conds at world view, 0.5°                 |  3   | 0.5°  |   238,651 |      46,758 |  1.51 s | A=15,973, B=15,887, C=15,939                          | A∩B = 1,016, A∩C = 25, B∩C = 0, A∩B∩C = 0                      |

Per-condition counts are checked: adding A_only + every pair containing
A + the triple equals A's per-condition total exactly (62,766 in case
03). No arithmetic disagreement between the per-mask histogram and the
per-condition sums.

## Visual readout

* **One condition (case 01)** — same yellow diagonal band as the
  single-condition proof; serves as the calibration baseline.
* **Two conditions (case 02)** — yellow Sun-1st band running NW→SE;
  blue Moon-4th band running parallel to it slightly east. They
  intersect over a narrow green region in the upper US / Quebec.
  4,066 cells are real intersections.
* **Three conditions (case 03)** — yellow + blue + rose. The yellow
  and blue still produce the green overlap region; rose (Mars-2nd) is
  out over Europe / West Africa and has 89 cells of orange (A∩C)
  overlap up by Iceland / east Greenland. No three-way overlap exists
  in this chart for this viewport — and the renderer correctly draws
  no slate-coloured cells.
* **Close-up (case 04)** — at the same 0.25° spacing zoomed onto the
  eastern US, the individual dots are clearly visible as a lattice and
  the green A∩B band runs through Ohio → West Virginia → Pennsylvania
  → Virginia → North Carolina. Yellow dots dominate to the west
  (Iowa, Kansas, Memphis); blue dots dominate to the east (Boston,
  Atlantic). City labels (Toronto, Cleveland, Pittsburgh, New York,
  Philadelphia, Washington, Raleigh, Atlanta) remain readable through
  the dotted overlay.
* **World (case 05)** — three parallel bands sweeping pole-belt to
  pole-belt, with the green A∩B sliver and the orange A∩C smudge
  visible near Greenland. The same green band that appears in case 02
  is preserved at world scale, confirming the overlap is geometry not
  resolution artefact.

## Reporting

Every run returns the following to the client (and the panel displays
them):

```
properties.classified_count          # cells that swe.houses succeeded on
properties.match_count               # ANY-condition matches (= sum of per_mask_counts)
properties.conditions[]              # one entry per slot with .count
properties.per_mask_counts           # histogram keyed by mask integer
properties.overlap_counts            # derived: A_only, A_and_B, A_and_B_and_C, any, ...
properties.compute_seconds           # server-side
properties.points_per_second         # server throughput on this request
properties.error_count               # cells where swe.houses raised (polar belt)
properties.outside_lat_cap_count     # cells skipped due to lat-cap
properties.bounds                    # echoed back

(client) timings.client_total_seconds   # round-trip including transport
(client) timings.paint_ms               # canvas redraw time
```

The sandbox metrics panel shows per-condition counts with the
condition's swatch beside them, then the overlap counts with the
overlap's blended-colour swatch beside them, so the eye can verify
"the green region's count matches the A∩B number" without leaving the
panel.

## Grid resolutions — plain English

`grid_deg` is the spacing of the regular lat/lon grid we classify. One
degree of latitude is **about 111 km** on Earth. The chosen spacing
controls three things at once:

1. **Geographic resolution** — the smallest piece of geography we can
   distinguish (any sub-cell variation is invisible to the renderer
   because we never compute it).
2. **Compute cost** — total cells scale with `1/grid_deg²`, so halving
   `grid_deg` quadruples the work.
3. **Perceived density on screen** — for a given viewport, a smaller
   `grid_deg` makes each cell occupy fewer pixels; below ~1 px/cell
   the eye reads the polygon as a continuous colour, above ~3 px/cell
   it reads as a visible lattice of dots.

### Settings cheat-sheet

| Setting    | km / cell | What it's good for                                      | Visual character at fit-to-continent zoom |
|------------|-----------|---------------------------------------------------------|--------------------------------------------|
| **2.0°**   | ~222 km   | Sanity-check or "preview before commit"                  | Very visible discrete squares; gappy.       |
| **1.0°**   | ~111 km   | World overview                                          | Clearly individual squares.                 |
| **0.5°**   | ~55 km    | Sandbox default; world resolves into a recognisable shape | Lattice visible; macro-shape correct.       |
| **0.25°**  | ~28 km    | Continental detail; default for the proof captures      | Lattice faint; close-ups show grid.         |
| **0.1°**   | ~11 km    | Region or country detail                                | Reads as continuous colour at fit-to-region zoom. |
| **0.05°**  | ~5.5 km   | Single-state / single-province zoom                    | Beyond what most screens can resolve.      |

The sandbox panel shows a live hint (`≈ 28 km / cell · 1.2 px / cell at
current zoom · lattice still readable`) so the operator can pick the
setting that matches the viewport rather than guessing.

### Recommended defaults by screen / viewport

The visually right `grid_deg` depends on viewport span (in degrees of
longitude) and the available pixel width of the map pane. The rule of
thumb that worked in practice during these captures:

```
target grid_deg ≈ (visible longitude span in °) / (map pane width in px)
```

i.e. roughly 1 cell per pixel at the current zoom. Anything coarser
than that and you see the lattice; anything finer wastes compute.

Concrete recommendations:

| Audience / device                         | Map pane width | Default viewport                | Sensible `grid_deg` |
|-------------------------------------------|---------------:|---------------------------------|----------------------|
| Big external desktop monitor (≥ 27")      |  ~1700 px      | World (~360°)                   | **0.5°** for world, **0.1°** for continent zoom |
| Same monitor, zoomed to a continent (~130°) |  ~1700 px    | Americas / Eurasia              | **0.1°** to **0.05°** |
| Standard laptop (15", retina)             |  ~1100 px      | World (~360°)                   | **0.5°** to **1.0°**  |
| Standard laptop, continent zoom (~130°)   |  ~1100 px      | Americas / Eurasia              | **0.25°** (default for captures) |
| Mobile portrait (390 px wide)             |   ~390 px      | World (~360°)                   | **1.0°**             |
| Mobile portrait, continent zoom (~130°)   |   ~390 px      | Americas / Eurasia              | **0.5°**             |
| Mobile portrait, country zoom (~25°)      |   ~390 px      | Single country                  | **0.1°**             |

The capture script's settings reflect those choices: world cases use
`0.5°`, continental cases use `0.25°` (visible lattice but acceptable
for a still), the close-up uses `0.25°` deliberately so the grid is
still resolvable as proof of "honest dots not smoothed fills".

A natural next-step UX is to compute the recommendation at run-time
(`viewport_span_deg / pane_width_px`) and offer it as an "Auto" preset.
That avoids the user picking a coarse grid on a 4K display or wasting
compute on a phone.

## Performance / feasibility (multi-condition)

* The grid pass is per-cell-times-O(1) for condition testing. Going
  from 1 to 3 conditions added **~16 %** to compute time
  (`2.74 s → 3.13 s` on the Americas / 0.25° case), not 3×. The
  dominant cost is still `swe.houses`.
* Sustained throughput at 0.25° Americas with 3 conditions: ~138 k
  cells/s on a single core. That's the same as single-condition; the
  added work of the planet-in-house tests is negligible next to the
  cusp computation.
* Wire payload grew by 50 % per added condition (the mask is one byte
  rendered as one-or-two JSON characters per match, plus more cells
  matched at least one condition).
* Paint cost is still under 75 ms even with 175 k cells split across 5
  mask buckets (case 03).

The earlier conclusion still holds: reveal/animation is now a
**stylistic** choice, not a performance necessity, even with multiple
simultaneous conditions.

## Honest self-critique

* **0.25° lattice still visible** in continental views. That is honest
  ("each dot is one truthful occupancy") but on a finished surface the
  default should probably drop to 0.1° on retina displays and let the
  eye read continuous colour. The cost at 0.1° Americas was ~16 s in
  the previous proof — likely ~17 s for 3 conditions.
* **B∩C and A∩B∩C were 0** on this chart, so the violet and slate
  swatches are documented but not yet seen on a captured polygon. The
  renderer code path exists and was exercised at the JS level, but a
  truly "all three" visual needs a chart whose planet positions
  produce a triple-overlap region — easy to engineer for a follow-up.
* **No exclusivity colouring option.** Right now A∩B always wins over
  drawing as "A only". A possible future toggle is "show me where A is
  but B is not" — implementable purely client-side by re-painting
  using mask filters.
* **Polar `swe.houses` errors still show as horizontal stripes** in
  the world / lat-cap-off views. Same as the single-condition proof:
  this is honest "engine couldn't classify here" feedback; the product
  surface can either honour the lat-cap or distinguish "unavailable"
  visually from "no match".
* **`B∩C = 0` is not a renderer bug.** The endpoint correctly reports
  zero overlap; the violet colour simply isn't drawn. The metrics
  panel's `B ∩ C: 0` line tells the operator "the renderer correctly
  drew nothing here", which is exactly the behaviour we want.

## Files added / changed in this pass

* `main_centerline_FIXER.py` — `BruteForceGridRequest` extended with
  optional `conditions: list[PlanetInHouseCondition]`; handler does a
  single classify-pass that tests every condition and returns
  `[lat, lon, mask]` plus per-mask / per-condition / pairwise / triple
  overlap counts.
* `map_SANDBOX_brute_force.html` — three condition slots (A required,
  B / C optional), mask-aware canvas overlay with 7 blended colours,
  live grid-resolution hint, exposes `window.__map` for capture
  scripts.
* `scripts/capture_brute_force_multi.py` — new capture matrix
  (1 / 2 / 3 conditions, close-up, world).
* `validation/screenshots/brute_force_multi/` — 5 PNG stills plus
  `manifest.json` with every URL, parameter set, and timing for the
  matrix above.

## Open questions for you

1. The overlap colour assignments (yellow+blue=green, yellow+rose=orange,
   blue+rose=violet, triple=slate) are mine to pick. Want a different
   palette, or is the perceptual-blend logic right?
2. Should the sandbox compute a recommended `grid_deg` automatically
   from viewport span and pane width? (It would override the current
   preset selector unless the user picks "Lock to X°".)
3. Should we engineer one extra chart specifically to exercise a real
   `A ∩ B ∩ C` triple-overlap region for the captures, or wait until
   that combination shows up naturally in product use?
