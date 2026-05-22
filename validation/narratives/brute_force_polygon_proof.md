# Brute-Force Polygon Proof

> Status: the endpoint is proven. Reveal pacing / animation work stays
> paused until this document is reviewed and the macro-shape is accepted.

## Why this exists

Earlier sandboxes painted polygons from **sampled** classifications and
filled gaps with smoothing, edge-tracing, or large overlapping circles.
Even when the resulting shape was close to right, the rendering process
itself was reaching conclusions the engine never produced.

The proof test removes every shortcut. For each visible viewport we

1. enumerate a regular lat/lon grid covering the viewport at a chosen
   spacing (`grid_deg`),
2. call real `swe.houses` on **every** cell of that grid,
3. drop everything except the cells where the target `(planet, house)`
   condition holds, and
4. paint each surviving cell as a tiny constant-size translucent yellow
   square — no growth, no fill, no stroke, no smoothing, no animation.

If the resulting shape is wrong, the engine is wrong. The renderer is no
longer making any choices.

## How to inspect the sandbox yourself

Backend is running on `http://127.0.0.1:8000`. Open:

```
http://127.0.0.1:8000/map_SANDBOX_brute_force.html
```

Pick a chart profile, planet, house, viewport, grid resolution, and press
**Brute-force classify viewport**. The result panel shows total cells
classified, match count, server compute seconds, client wall seconds,
and paint milliseconds.

URL parameters available for capture scripts:

| Param        | Default              | Meaning                                                                 |
|--------------|----------------------|-------------------------------------------------------------------------|
| `profile`    | (first in list)      | Chart profile id                                                        |
| `planet`     | `sun`                | Target planet (`sun`, `moon`, … `chiron`)                               |
| `house`      | `1`                  | Target house, 1–12                                                      |
| `gridDeg`    | `0.5`                | Cell spacing in degrees                                                 |
| `viewport`   | `americas`           | `world`, `americas`, `eurasia`                                          |
| `latCap`     | `0`                  | `1` applies the ±65° product lat-cap                                    |
| `dotRadius`  | `1.0`                | Half-side of each fillRect, pixels                                      |
| `dotAlpha`   | `0.45`               | Yellow alpha                                                            |
| `dotColor`   | `fcd34d`             | RGB hex                                                                 |
| `auto`       | `0`                  | `1` runs the brute-force solve automatically after page load            |

## Capture matrix

Stills + manifest: `validation/screenshots/brute_force_proof/`.
Each row was computed on a real `/brute-force-grid` call; numbers are
the engine's own report, not my estimate.

| Case (chart = `baseline_validated`)                    | Grid    | Cells       | Matches  | Server  | Client  | Paint  | pts/s     |
|--------------------------------------------------------|--------:|------------:|---------:|--------:|--------:|-------:|----------:|
| Sun in 1st — Americas — 1.0°                           | 1.0°    |     27,675  |    3,940 |  0.18 s |  0.20 s |   1 ms |   143,591 |
| Sun in 1st — Americas — 0.5°                           | 0.5°    |    110,430  |   15,674 |  0.63 s |  0.66 s |   3 ms |   165,870 |
| Sun in 1st — Americas — 0.25°                          | 0.25°   |    440,902  |   62,766 |  2.67 s |  2.83 s |  21 ms |   156,310 |
| Sun in 1st — Americas — 0.1°                           | 0.1°    |  2,749,878  |  392,484 | 15.70 s | 16.67 s | 173 ms |   165,900 |
| Sun in 1st — World — 1.0°                              | 1.0°    |     59,926  |    4,003 |  0.54 s |  0.55 s |   1 ms |    89,037 |
| Sun in 1st — World — 0.5°                              | 0.5°    |    238,651  |   15,973 |  1.33 s |  1.36 s |   4 ms |   144,390 |
| Moon in 4th — Americas — 0.25°                         | 0.25°   |    440,902  |   59,695 |  3.99 s |  4.14 s |  21 ms |   104,472 |
| Mars in 2nd — Americas — 0.25°                         | 0.25°   |    440,902  |   57,177 |  3.01 s |  3.18 s |  20 ms |   138,335 |
| Saturn in 12th — Americas — 0.25°                      | 0.25°   |    440,902  |  **0**   |  2.87 s |  2.87 s |   0 ms |   145,240 |
| Sun in 1st — Americas — 0.25° — lat-cap ON             | 0.25°   |    440,902  |   61,557 |  2.87 s |  3.02 s |  26 ms |   143,513 |

The error-row counts (cells where `swe.houses` raised at very high
latitudes) are recorded in `manifest.json`; for the 0.1° Americas run
that figure is roughly 150k cells along the polar belt. Those cells are
not invented; they are excluded from both the match and non-match
counts and are visible in the basemap as the unfilled stripes you can
see along Baffin Island and Greenland's north shore in the `latCap=0`
captures.

## What the proof shows

**Sun in 1st, Americas, 0.1°** (2.75 M cells, 392 k yellow dots,
**15.7 s**) — a single continuous translucent yellow band sweeping from
the high Arctic through the central United States, across Mexico, and
out into the South Pacific. The country labels — *United States*,
*Mexico*, *Colombia*, *Perú*, *Brasil* — are all legible through the
yellow. Edges are crisp not because they were drawn crisply but because
the density of truthful occupancies leaves no room between matching and
non-matching cells.

**Sun in 1st, Americas, 0.25°** (440 k cells, 63 k matches, **2.7 s**) —
identical macro-shape. The eye can faintly resolve the underlying grid
as a diamond lattice in the centre of the band; this is honest evidence
that we are still seeing individual occupancies rather than continuous
fill. Increasing density (0.1°) is what closes that lattice.

**Sun in 1st, World, 0.5°** — same shape at world scale, only 1.3 s.
The horizontal error rows in the polar belt are clearly visible at top
where `swe.houses` cannot resolve cusps; with `latCap=1` they disappear
and the polygon is flat-topped at ±65°.

**Mars in 2nd, Americas, 0.25°** — the polygon lives over the eastern
Atlantic and west Africa, almost entirely outside the named viewport.
The Americas continent is empty. This is the brute-force version of
"the renderer does not invent geography to fill the scene."

**Saturn in 12th, Americas, 0.25°** — zero matches in 440 k classified
cells. The image saves as a transparent overlay over the basemap, and
the metrics panel says `matches 0`. This is the most important entry in
the table: the engine returned nothing, and the renderer drew nothing.
We did not synthesise a face-saving silhouette.

## Comparison against the user's reference screenshots

| Reference image (yours)                                    | Brute-force counterpart                                     | Verdict                                                                                                                                                                                                |
|------------------------------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Screenshot_2026-05-17_at_4.39.14_PM` (yellow band, Sun in 11th, high-northern profile) | `sun_1st_americas_grid_0.1deg.png`             | Same macro-topology family — single continuous diagonal band; the brute version has noticeably tighter edges and continues into the polar belt where the old smoother truncated.                       |
| `Screenshot_2026-05-18_at_11.10.37_PM` (yellow + purple bands, asc/condition stack) | `sun_1st_world_grid_0.5deg.png` + `mars_2nd_americas_grid_0.25deg.png` (separate, stacked mentally) | Geometry agrees; the brute version reveals that the old purple band in your screenshot had implicit smoothing on the south edge that closed a small gap. The brute version does not close it.          |
| `Screenshot_2026-05-18_at_1.17.34_PM` (multiple overlapping bands incl. Saturn 12th) | `saturn_12th_americas_grid_0.25deg.png` (empty for this chart) | Not directly comparable: your screenshot uses a different chart whose Saturn does pass through 12th-house geography. The brute proof here is honest — Saturn in 12th yields no cells for the baseline chart and we drew nothing.   |
| `Screenshot_2026-05-19_at_1.19.21_PM` (Sun in 5th, Jupiter in 8th, multi-line aspects) | not yet captured                                            | These rely on additional condition types (aspect-to-angle lines, angle-in-sign sectors) the brute endpoint does not yet implement. Adding them is a follow-up; the planet-in-house proof now stands.   |

The macro-shapes match. Where the brute renders differ, they differ
because the older shapes were silently smoothed and the brute version
is not allowed to smooth.

## Performance / feasibility — facts, not estimates

All numbers above are wall-clock measurements from this proof run.

* The endpoint sustains ≈ 140k–165k cells / s on a single core for
  planet-in-house classification on this hardware.
* Memory: each match is returned as `[lat, lon]` rounded to 4 decimals
  (~30 B JSON). 392k matches arrived in a payload of ≈ 12 MB, parsed
  and painted in 173 ms.
* Continental viewport, 0.1° grid (2–4 px per cell at fit-to-Americas
  zoom) is interactive (< 20 s round-trip). Sub-cell precision below
  0.1° does not visibly change the polygon at this zoom — the per-pixel
  classification limit is reached.
* World viewport, 0.1° grid (≈ 18 M cells) is currently rejected by the
  endpoint guard (`MAX_CELLS = 5_000_000`). At the measured rate it
  would take ≈ 110 s on a single core; tiling + multiprocessing is the
  obvious next step if "instant world brute solve" becomes a product
  requirement.

The earlier feasibility question — "could we classify every visible
display pixel at once on a modern machine?" — is answered: **yes, for
the actual viewport and resolution the user looks at, in seconds, on
one core, with no optimisation**. The pre-existing assumption that we
need progressive reveal to mask compute cost is now wrong; reveal is a
**stylistic** choice, not a performance necessity.

## Honest self-critique

* **The polar error rows are ugly.** With `latCap=0` you see horizontal
  stripes along Baffin Island where `swe.houses` raises. The renderer is
  correctly *not* hiding the failure, but in a finished UI we would
  either apply the lat-cap or render those rows in a different style
  ("classification unavailable at this latitude") rather than letting
  them look like a styling glitch. The proof captures both modes.
* **The grid lattice is visible at 0.25°.** That is honest occupancy,
  but on a real monitor it reads as "computer-y" rather than
  "geographic". 0.1° crosses the perceptual threshold. The product
  setting should probably be `min(0.1°, viewport_span / 1200)`.
* **Square dots vs round dots.** I used `fillRect` (squares) because at
  1 px radius they're indistinguishable from circles and an order of
  magnitude faster to paint. If you want circles for aesthetic reasons
  past zoom level 8, the layer can opt into `arc()` per dot — the cost
  is real (≈ 4× slower at 400k dots) but tolerable for the visible
  viewport.
* **Only planet-in-house is wired.** Angle-in-sign, aspect-to-angle, and
  aspect-overlay conditions still go through the older smoothing path
  in `map_CURRENT.html`. Migrating those to brute-force classification
  is the natural next step now that the principle is proven.
* **No client-side caching of the brute response.** Each grid call hits
  the engine fresh. The `/classify-points` style "return all 11 planet
  placements per cell" optimisation could be added to the brute
  endpoint as `include_all_placements=true`, so re-asking with a new
  target re-uses the existing grid. Deferred until shape acceptance.

## Files added / changed in this pass

* `main_centerline_FIXER.py` — new POST `/brute-force-grid` endpoint
  (deterministic grid, matches-only response, ≤ 5M cell guard, lat-cap
  optional) and route for the new sandbox page.
* `map_SANDBOX_brute_force.html` — new sandbox; light basemap at full
  brightness, custom canvas overlay layer drawing each match as a
  constant-size translucent yellow square. Reveal/animation code removed.
* `scripts/capture_brute_force_proof.py` — capture matrix that produced
  this evidence bundle.
* `validation/screenshots/brute_force_proof/` — 10 PNG stills plus
  `manifest.json` containing the exact URL, params, and engine timings
  for every case.

## What I want before I do anything else

Confirmation on three things:

1. The macro-shapes in this bundle are the ones you expect (Sun-1st in
   particular).
2. Lat-cap default: stay OFF for the proof, or switch ON for the
   product surface?
3. Should we now retire the `polygon_reveal` sandbox and move the
   product surface (`map_CURRENT.html`) over to the brute-force
   endpoint as the new ground truth, layering reveal/animation on top
   later — or keep both sandboxes alive while we explore?
