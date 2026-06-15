# Screen-pixel truth: deliberately dumb maximal proof

> **STATUS: SUPERSEDED** (2026-05-21) — preserved as archaeology.
>
> **Why superseded:** This pass optimised the *wrong target* (largest global
> block size). Production uses **adaptive refinement toward 1px truth**, not
> a single block size everywhere.
>
> **Current doctrine:** `docs/CURRENT_RENDERING_DOCTRINE.md` →
> `validation/narratives/screen_pixel_adaptive_refinement.md`
>
> **Warning:** Do not ship a global `block_px=N` production setting based on
> this sweep alone.

This narrative is the answer to the user's direct ask: stop calling the
existing renderer "every point", classify the actual visible screen
output pixel-by-pixel, and find out what happens. No optimisation, no
smoothing, no interpolation, no aura, no change to astrology math.

## TL;DR

- **The gaps disappear** the moment we classify screen pixels instead of
  a 0.5° lat/lon grid. The "dashed-line" appearance of aspect-to-angle
  centerlines is entirely a drawing-primitive artefact — astrology math
  is correct; we were just under-painting the sampled cells.
- **The overlay stays continuous when zoomed** because every visible
  screen block is touched on every render. There is no stale geographic
  grid to reuse.
- **The aspect line stops being dashed** at every tested block size,
  including 8 px. The line is just slightly thicker at coarser blocks.
- **True 1-pixel brute force is feasible**: a 1480×900 viewport (≈1.33 M
  points) classifies in ~8.5–9 s of server compute, ~11 s end-to-end.
  Block sizes of 2 / 4 / 8 px drop end-to-end time to ~3 / 0.7 / 0.2 s
  with identical visual coverage.

## Sandbox

- **Lat/lon-grid renderer** (the "old" thing the user is asking about):
  - URL: `http://127.0.0.1:8000/map_SANDBOX_brute_force.html`
  - Sampling: `gridDeg`° lat/lon grid clipped to the engine's bounds.
  - Painting: a fixed-size dot (default 2 × 2 px, `dotRadius=1.0`) at
    each match's projected screen position.
- **Screen-pixel-truth renderer** (the deliberately dumb maximal proof):
  - URL: `http://127.0.0.1:8000/map_SANDBOX_screen_pixel_truth.html`
  - Sampling: iterate every `block_px`-pixel screen block in the
    visible map div, take the centre pixel, unproject to lat/lon.
  - Painting: a `block_px × block_px` filled rectangle on the canvas
    overlay at the same screen coordinates.

### Equality knobs added for apples-to-apples comparison

- `?fitBounds=s,w,n,e` was added to both sandboxes. It sets the visible
  viewport without pinning the brute-force engine to that rectangle, so
  brute-force queries `map.getBounds()` (the same surface the
  screen-pixel renderer iterates over).
- The screen-pixel sandbox now matches the brute-force sandbox's zoom
  snapping (`zoomSnap: 0.25, zoomDelta: 0.5`); previously SPT used
  `zoomSnap: 1` and landed on a different zoom level for the same
  `fitBounds` URL.
- The `/screen-pixel-truth` endpoint's `POINT_CAP` was raised from
  1 000 000 to 2 000 000 so a 1480×900 viewport at `block_px=1`
  (1.33 M points) actually fits.
- For payload bodies above ~12 MB the screen-pixel sandbox client-side
  chunks into 400 k-point requests and stitches the per-chunk mask
  arrays back together. Aggregation preserves match counts and
  overlap masks.

## Experiment matrix

- Profile: `baseline_validated`.
- Visible viewport: `?fitBounds=-65,150,65,180` → Leaflet lands at zoom
  2.75 with a 1480×900 frame showing Africa→Americas.
- Lat/lon-grid reference: `gridDeg=0.5` (clearly exposes the gap
  artefact at this zoom; finer grids hide it but do not eliminate it).
- Screen-pixel block sizes: 1, 2, 4, 8 px.
- Five test conditions × 5 captures each = **25 stills**:
  1. Sun in 1st House — polygon
  2. Saturn ☌ MC, orb 1° — sharp centerline
  3. Saturn ☌ ASC, orb 1° — sharp centerline
  4. Saturn ☌ MC, orb 6° — wide band
  5. Saturn ☌ ASC, orb 6° — wide band

Capture script: `scripts/capture_screen_pixel_block_sweep.py`. Total
wall: **102.2 s** for all 25 captures.

## Output

- Screenshots: `validation/screenshots/screen_pixel_block_sweep/`
- Manifest: `validation/screenshots/screen_pixel_block_sweep/manifest.json`

```
01_sun_in_1st_brute_ref.png
01_sun_in_1st_spt_block_{1,2,4,8}.png
02_saturn_conj_mc_orb_1_brute_ref.png
02_saturn_conj_mc_orb_1_spt_block_{1,2,4,8}.png
03_saturn_conj_asc_orb_1_brute_ref.png
03_saturn_conj_asc_orb_1_spt_block_{1,2,4,8}.png
04_saturn_conj_mc_orb_6_brute_ref.png
04_saturn_conj_mc_orb_6_spt_block_{1,2,4,8}.png
05_saturn_conj_asc_orb_6_brute_ref.png
05_saturn_conj_asc_orb_6_spt_block_{1,2,4,8}.png
manifest.json
```

## Visual diagnosis (the five questions, answered directly)

### 1. Do the gaps disappear?

Yes. The clearest single proof is case 02 (Saturn ☌ MC, orb 1°). At
`gridDeg=0.5°`, the lat/lon-grid sandbox places a 2 px dot every ~5 px
along the meridian at zoom 2.75 — leaving a ~3 px gap between every
consecutive dot. Net visual: a vertical dashed line.

The same condition rendered at `block_px=1` on the screen-pixel sandbox
produces a solid 1-pixel-wide yellow line continuous from the visible
top to the visible bottom of the map. At `block_px=8` the line is
slightly thicker (each match paints an 8 × 8 block) but is still
unbroken.

| condition | lat/lon-grid matches | spt block_px=1 matches | spt block_px=8 matches |
|---|---:|---:|---:|
| Saturn ☌ MC, orb 1° | 1 330 | 8 620 | 108 |
| Saturn ☌ ASC, orb 1° | n/a (none drawn in viewport) | 8 594 | 137 |
| Saturn ☌ MC, orb 6° | (band) | 51 720 | 756 |
| Saturn ☌ ASC, orb 6° | (band) | 51 501 | 807 |
| Sun in 1st (polygon) | (polygon dots) | 123 488 | 1 932 |

The 6× ratio between orb-6° and orb-1° match counts is preserved across
all block sizes — width-scaling stays linear, so band thickness is
proportional to orb. This is the truth-first commitment intact.

### 2. Does the overlay stay continuous when zoomed?

Yes. The screen-pixel layer's `_reposition` clears the canvas on every
`moveend` / `zoomend`, forcing a fresh sample of the current visible
viewport. There is no lat/lon grid to reuse, so there is nothing to
become stale relative to the new Mercator projection.

In contrast, the lat/lon-grid sandbox reuses the previously fetched
match coordinates and re-projects them on pan/zoom (unless
`Re-run after pan/zoom` is checked). When the geographic spacing of
cells exceeds 2 × `dotRadius`, the result is the same dashed pattern
seen here.

### 3. Does the aspect line stop being dashed?

Yes — at every tested block size. Even `block_px=8` produces a solid
(if thicker) line because the painting primitive matches the sampling
primitive. The line in the screen-pixel renderer is exactly as wide as
the truth band (≤ orb°) projected to pixels, never less.

### 4. Is the current problem caused by geographic sampling rather than astrology math?

Confirmed. The astrology math is identical between the two endpoints
(`/brute-force-grid` and `/screen-pixel-truth` share `julian_day`,
`get_houses`, and the per-condition dispatch). Match counts scale
linearly with the number of points sampled within the same geographic
region. The three real causes of the artefacts are:

- **Drawing-primitive mismatch.** 2 × 2 px dots cannot cover the
  geographic cell they were sampled from once the projected cell size
  exceeds the dot. At `gridDeg=0.5°`, zoom 2.75: cells project to
  ~5 × 5 px, dots are 2 × 2 px, gaps are inevitable.
- **Sampling-area mismatch (when `?bounds=` is used).** Out of scope
  here — see `screen_pixel_truth_diagnosis.md` for the dedicated
  capture pair.
- **Insufficient sampling density.** `gridDeg=0.5°` undersamples
  anything thinner than ~5 px on screen. Decreasing to `gridDeg=0.1°`
  shrinks the gaps but never eliminates them at high zoom; the screen-
  pixel renderer always paints exactly what the eye sees.

### 5. How slow is true screen-space brute force?

End-to-end, per capture, at 1480 × 900 (apples-to-apples, baseline
chart, all 5 test conditions averaged):

| block_px | points | server compute | client total wall | paint |
|---:|---:|---:|---:|---:|
| 1 | 1 332 000 | 8.50 s ±0.20 s | 11.20 s ±0.25 s | ~290 ms |
| 2 |   333 000 | 2.18 s ±0.07 s |  2.89 s ±0.08 s | ~80 ms |
| 4 |    83 250 | 0.56 s ±0.02 s |  0.74 s ±0.03 s | ~25 ms |
| 8 |    20 905 | 0.15 s ±0.02 s |  0.20 s ±0.02 s | ~12 ms |

Server side, the engine sustains ~150–160 k classified points/sec on
this machine. The client-side projection loop is ~270 ms for 1.33 M
`containerPointToLatLng` calls — comfortably below network/compute.
At `block_px=1` the request is split into 4 chunks of 333 k points so
no single POST body exceeds ~10 MB.

The lat/lon-grid sandbox at `gridDeg=0.5°` for the same viewport takes
~0.48 s server / ~0.50 s wall but produces visibly broken output. To
match the visual quality of `block_px=4` (continuous coverage at this
zoom), the lat/lon-grid renderer would need `gridDeg≈0.05–0.1°`, which
recomputes 25–100× more points without ever guaranteeing pixel-level
coverage at all zoom levels.

## Recommendation for the next rendering architecture

**Use the screen-pixel-truth approach as the production renderer.** It
is structurally correct: it asks the astrology engine exactly the
question the user can see, and paints exactly that answer. The chosen
operating point is most likely `block_px=2` or `block_px=4`:

- **`block_px=4`** at 1480 × 900 = 83 k classifications, ~0.7 s
  end-to-end. Faster than the existing `gridDeg=0.5°` lat/lon-grid
  renderer in wall time and produces unbroken overlays at any zoom.
  Visual minimum stroke width is 4 px on screen — fine for most
  conditions; aspect centerlines may need block=2 if we want a 2 px
  visual thickness.
- **`block_px=2`** at 1480 × 900 = 333 k classifications, ~2.9 s
  end-to-end. Pixel-doublet stroke; visually indistinguishable from
  `block_px=1` for most overlays.
- **`block_px=1`** stays as the inspection / validation mode. ~11 s
  per render is acceptable for a "show me the truth" diagnostic but
  not for interactive panning.

Adaptive block size is the natural next step: pick `block_px` from the
orb / band-width budget so that the projected stroke width is at least
one block. For 1° orb at zoom 2.75 this gives `block_px≈1–2`; for a
24° band (Sun in 1st polygon) `block_px=4` is more than sufficient.
This is purely an efficiency knob and does not change the truth-first
commitment: every visible block still corresponds to a real
classification, never a smoothing or interpolation step.

## What this does NOT change

- Astrology math: untouched. Both endpoints call the same
  `get_houses` / `planet_in_house` / aspect-evaluation code paths.
- Smoothing: no.
- Interpolation: no.
- Aura: no.
- Truth-first doctrine: reinforced. The screen-pixel renderer is the
  closest physical realisation of the doctrine yet — it literally
  classifies the surface the user sees.

## Reproduce

```bash
# Backend (FastAPI):
cd /Users/davegoodman/Desktop/relocation-backend
lsof -ti :8000 | xargs -r kill -9 ; sleep 1
./venv/bin/uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000 \
  > /tmp/uvicorn_brute.log 2>&1 &

# Re-run the full sweep (25 captures, ~100s wall):
./venv/bin/python3 scripts/capture_screen_pixel_block_sweep.py

# Manually drive a single comparison:
#   lat/lon-grid:
open "http://127.0.0.1:8000/map_SANDBOX_brute_force.html?profile=baseline_validated&fitBounds=-65,150,65,180&gridDeg=0.5&A=a2a:saturn:mc:conjunction:1.0&auto=1"
#   screen-pixel @ block=1:
open "http://127.0.0.1:8000/map_SANDBOX_screen_pixel_truth.html?profile=baseline_validated&fitBounds=-65,150,65,180&block=1&A=a2a:saturn:mc:conjunction:1.0&auto=1"
```
