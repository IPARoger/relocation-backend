# Screen-pixel-truth diagnosis: why the brute-force renderer has gaps

**Status:** Diagnostic pass. No astrology math changed. No optimisation
attempted. No smoothing introduced. The goal is to identify, with
visual and numerical evidence, **why** the current renderer produces
gaps, dashed centerlines, and disappearing overlays — and to
recommend the correct production rendering architecture for the
brute-force truth substrate going forward.

**Evidence bundle:**
`validation/screenshots/screen_pixel_truth_diagnosis/`
(12 PNGs + `manifest.json`).

**See also:** `validation/narratives/screen_pixel_block_sweep.md` —
follow-up "deliberately dumb maximal proof" that re-runs the same
conditions across `block_px ∈ {1, 2, 4, 8}` and includes a true 1-pixel
classification of the entire 1480×900 viewport (1.33 M points,
end-to-end in ~11 s). That bundle is the direct answer to the
question "what happens when we classify the actual output surface
itself?"

**New code added for this proof (not in production yet):**

- `POST /screen-pixel-truth` — sibling endpoint to `/brute-force-grid`
  that classifies an explicit list of `(lat, lon)` points (no grid
  contract). Same Swiss Ephemeris call, same condition compilation,
  same dispatch.
- `map_SANDBOX_screen_pixel_truth.html` — sibling sandbox that
  iterates the visible map div in screen-pixel **blocks** (default
  4 px), projects each block's center to `(lat, lon)` via
  `map.containerPointToLatLng`, posts the list to
  `/screen-pixel-truth`, and paints each matching block as a real
  filled rectangle on the canvas.

## TL;DR

The brute-force sandbox does **not** render every visible pixel
truthfully. Three distinct bugs combine to produce the symptoms the
user described as "gaps, dashed lines, disappearing overlays":

1. **Sampling-area mismatch (Bug #1).** When the URL specifies
   `?bounds=…`, the engine is asked to classify exactly that lat/lon
   rectangle — but Leaflet's `fitBounds()` expands the visible map
   well beyond that rectangle to match the viewport aspect ratio.
   Matches that exist inside the visible map but outside the queried
   rectangle are simply **never asked for**. They are not rendered.
2. **Drawing-primitive mismatch (Bug #2).** Matching cells are
   returned as `(lat, lon, mask)` vertices, and painted as
   **fixed-size 2-px squares** at the projected center. The
   geographic area each cell represents (≈ `grid_deg × grid_deg`) is
   never covered. At any zoom where `grid_deg` in screen pixels
   exceeds the dot size, the rendered pattern is a lattice of dots
   with un-painted basemap between them.
3. **World-copy mismatch (Bug #3).** The canvas overlay paints once
   per `(lat, lon)` match in the primary world copy. The Leaflet
   basemap tiles, however, repeat across world copies whenever the
   visible map spans more than 360°. At low zoom, the user sees the
   basemap twice but the overlay once.

The screen-pixel-truth experiment confirms all three: it inverts the
sampling axis (iterate screen pixels, classify each point on the
client's behalf), and it paints the block that was sampled. **All
three bugs disappear in the experiment**, at every zoom and viewport
we tested.

## Q1–Q5 diagnosis (the user's questions)

### Q1. What are we sampling today?

**Geographic lat/lon grid vertices.** The brute-force endpoint
iterates a regular grid:

```python
lats = [south + i * req.grid_deg for i in range(lat_count)]
lons = [west  + j * req.grid_deg for j in range(lon_count)]
for lat in lats:
    for lon in lons:
        cusps = get_houses(jd, lat, lon)
        ...
```

Each `(lat, lon)` is a **point** (vertex of an imaginary grid). The
response is a flat list of `[lat, lon, mask]` tuples for every cell
that matched at least one condition. The "cell" has no width or
height in the response; it is a single point.

Neither screen pixels nor Leaflet projected pixels are involved on
the server. The server has no concept of a viewport, of zoom, or of
a screen.

### Q2. What is the drawing primitive?

**Fixed-size canvas squares.** In
`map_SANDBOX_brute_force.html` the `BrutePoints._redraw` loop
projects every match and paints a tiny rectangle:

```js
const r = this._opts.radius || 1.0;   // default URL_DOT_RAD = 1.0
const r2 = r * 2;
…
const p = map.latLngToContainerPoint(bucket[i]);
ctx.fillRect(p.x - r, p.y - r, r2, r2);
```

That is a **2×2 pixel square** at the projected cell center.

Not SVG. Not circles. Not geographic rectangles. Not polygons. Not
canvas pixels in the screen-space sense. The dot size is *in screen
pixels and constant*; it does not scale with zoom, with latitude, or
with `grid_deg`.

### Q3. Are we painting the full area each sample represents?

**No.** The sample is the cell *vertex* (a single point). It is
painted as a 2×2 px square in screen space, regardless of how many
pixels the corresponding `grid_deg × grid_deg` geographic patch
actually covers on screen at the current zoom and latitude.

A 0.1° cell at world zoom (Mercator, equator) is roughly **0.4 px**
wide — so 2-px dots overlap and the polygon looks solid. At zoom 6
the same 0.1° cell is roughly **11 px** wide, but the dot is still
2 px — so the rendered "polygon" becomes a lattice of dots with ~9
px of un-painted basemap between rows and columns. That is the
"dashed line" the user reports.

### Q4. What happens on zoom?

The `BrutePoints` layer attaches handlers for
`viewreset zoomend moveend resize` and on each one **re-projects the
same `[lat, lon]` list** to new container pixel coordinates and
paints the same 2-px squares again:

```js
map.on("viewreset zoomend moveend resize", this._redraw, this);
```

The lat/lon grid is fixed at request time. It does *not* get re-
sampled when the user pans or zooms. So:

- Zoom in → the same `N` points spread across more screen pixels →
  inter-sample pixel distance grows → dots that were dense at the
  original zoom become a sparse lattice.
- Pan outside the originally-queried rectangle → no points exist
  there → the basemap shows through bare.
- Resize browser → no resample → same N points, same gap behaviour.

There is **no re-query on the new viewport/resolution** at all in
the current sandbox. (The "Re-run after pan/zoom" checkbox in the
sandbox UI does exist, but it re-runs the original lat/lon grid for
the new visible bounds — at the same `grid_deg`, so the lattice gets
the same dot-size-vs-cell-width mismatch at the new zoom.)

### Q5. Why do white blank stripes / sparse overlays appear?

Three causes, all of which we now have evidence for:

| Cause | Visible symptom | Captures that prove it |
|-------|-----------------|------------------------|
| Lat/lon `grid_deg` becomes coarser than the dot size in screen pixels at zoom | dashed lines, lattice/stipple instead of bands | every brute-force capture at zoom > 4 |
| `?bounds=…` rectangle is smaller than the actual visible map (Leaflet fitBounds-aspect-padding) | overlay confined to a narrow band; rest of the visible viewport painted bare | **cases 02_…_A_brute_force.png** and **03_…_A_brute_force.png** (0 matches in bounded mode) vs the SPT result (244 / 3,637 matches) |
| Canvas overlay paints in one world copy; basemap tiles repeat in multiple | bare basemap on one half of the screen at low zoom | **01_saturn_mc_A_brute_force_apples.png** (one yellow meridian) vs **01_saturn_mc_B_screen_pixel_apples.png** (yellow meridians in both world copies) |

Leaflet tile loading is NOT at fault; canvas layer bounds are
correct; z-index/layer clipping is correct; tile seams render fine;
stale overlay dimensions are not a factor here.

## The screen-pixel-truth experiment

For each of three conditions we captured two screenshots in two
modes:

- **Bounded mode** — `?bounds=-65,150,65,180` (Pacific 178°E,
  matching orb-sensitivity cases 09 / 09b / 10).
- **Apples-to-apples mode** — `?viewport=world` (no `?bounds`), so
  the brute-force sandbox uses `map.getBounds()` (the actual visible
  viewport). Same visible map in both renderers.

### Per-case results

| Case | Mode | Renderer A (brute-force) matches | Renderer B (screen-pixel) matches | Notes |
|------|------|--:|--:|------|
| Saturn ☌ MC  | bounded (0.1° grid, 4 px block)  | 27,321 | 129    | Meridian *is* inside the bounded rect → A finds it. B sees fewer because viewport is wider than rect and only one slice of the meridian lands in the block centers; coverage of those blocks is solid. |
| Saturn ☌ ASC | bounded                            | **0**  | **244** | ASC band does NOT pass through `lon ∈ [150,180]` → A misses entirely. B classifies the whole visible viewport → finds 244 matching blocks. |
| Sun in 1st   | bounded                            | **0**  | **3,637** | Polygon does NOT pass through `lon ∈ [150,180]` → A misses entirely. B classifies the whole visible viewport → finds 3,637 matching blocks. |
| Saturn ☌ MC  | apples (world, 0.25° grid, 6 px block) | 4,256  | 172  | A renders ONE yellow meridian; B renders TWO (one in each visible world copy). |
| Saturn ☌ ASC | apples                              | 4,419  | 100  | A renders curved band in one world copy only; B renders it in both. |
| Sun in 1st   | apples                              | 63,835 | 1,988 | A renders the polygon densely (over-sampled at world zoom; dots paint atop dots, so alpha stacks and looks more opaque than `rgba(…, 0.55)`); B renders the same polygon in both world copies at the correct translucency. |

Match counts differ between A and B in apples mode because they are
sampling at different densities (0.25° lat/lon = 952,501 cells vs
6 × 6 screen blocks = 37,050 sampled points). **Count is not the
diagnostic; coverage is.** Both renderers find the band in the right
geographic place. The question is whether the painted result covers
every visible pixel of that band, and whether it covers every world
copy that is visible.

### Visual evidence (4 panels, both modes)

The clearest single comparison is the bounded Sun-in-1st pair:

```390:480:validation/screenshots/screen_pixel_truth_diagnosis/manifest.json
        "B": {
          "renderer": "screen_pixel_blocks",
          "url":      "…?A=pih:sun:1&block=4&profile=baseline_validated&auto=1&bounds=-65,150,65,180",
          "image":    "03_sun_1st_B_screen_pixel.png",
          "block_px": 4,
          "timings":  { "match_count": 3637, "server_compute_seconds": 0.41 }
        }
```

- `03_sun_1st_A_brute_force.png` — completely blank map. 0 matches.
  Same URL, same visible viewport.
- `03_sun_1st_B_screen_pixel.png` — solid translucent yellow
  crescent painted across the visible map, with a small slice of the
  same crescent on the left edge (the wrapped world copy). 3,637
  matches.

The apples-to-apples Saturn ☌ MC pair makes Bug #3 visible:

- `01_saturn_mc_A_brute_force_apples.png` — one solid yellow
  meridian at lon ≈ 178°E.
- `01_saturn_mc_B_screen_pixel_apples.png` — the **same** yellow
  meridian at lon ≈ 178°E, **plus** the same meridian in the wrapped
  second world copy on the left side. Both are correct — the basemap
  shows the world twice, so the overlay should show the condition
  twice.

The apples-to-apples Sun-in-1st pair makes Bug #2 visible at low
zoom indirectly via alpha-stacking:

- `03_sun_1st_A_brute_force_apples.png` — polygon looks **more
  opaque** than `rgba(252, 211, 77, 0.55)` would suggest, because at
  world zoom each 0.25° cell is sub-pixel wide and multiple dots
  paint atop the same pixel, stacking alpha. Edges look unnaturally
  crisp.
- `03_sun_1st_B_screen_pixel_apples.png` — same polygon at the
  intended translucency, painted once per 6 × 6 screen block. Edges
  are honest at the block resolution. The basemap below remains
  readable.

The doctrine wants the **honest translucency** behaviour
(`docs/relocation_map_architecture.md` → Aura Rendering Principles
§3: Map readability is sacred; §5: current palette is proof-of-
concept). Today's renderer happens to violate it via accidental
over-paint.

## Timings

| Mode | Renderer | Sample count | Server compute | Client total | Paint | Notes |
|------|----------|---:|---:|---:|---:|------|
| bounded (0.1° / 4 px) | A brute-force | 391,601 cells | 2.4–2.5 s | 2.5 s | ~10 ms | server-side cost dominates |
| bounded (0.1° / 4 px) | B screen-pixel | 83,250 points | 0.40–0.55 s | 0.55 s | ~1 ms | ~5× faster server because ~5× fewer points |
| apples (0.25° / 6 px) | A brute-force | 952,501 cells | 5.3–6.2 s | ~5.7 s | ~10–20 ms | brute-force at world is expensive |
| apples (0.25° / 6 px) | B screen-pixel | 37,050 points | 0.18–0.20 s | ~0.3 s | ~1–2 ms | ~30× faster server because ~25× fewer points |

The screen-pixel approach **classifies fewer points** than the
lat/lon-grid approach at the same visible map, and yet covers every
visible block — because the points it classifies are exactly the
ones it will paint. There is zero waste. Latency drops by an order
of magnitude in apples-to-apples mode.

Per-point cost is identical (same `swe.houses` call, same condition
dispatch). The win is purely structural.

## Conclusion: where the gaps come from

| User's hypothesis | Confirmed? | Evidence |
|-------------------|----|----------|
| Insufficient sampling | partially | yes, at zooms where `grid_deg` > 2 px per cell — that explains dashed centerlines and lattice stipple |
| Wrong drawing primitive | **yes** | fixed-pixel dot at the projected center, instead of a primitive that covers the area each sample represents |
| Projection mismatch | partially | Leaflet's `fitBounds()` aspect-padding makes the visible map larger than the URL bounds rectangle; the renderer doesn't reconcile this |
| Zoom-layer reuse | **yes** | the layer reprojects the same lat/lon list on every zoom/pan, never resamples geography for the new viewport, and never covers area per cell |
| Tile / canvas rendering bugs | no | tiles render fine; canvas dimensions and offsets are correct; the missing pixels are not painted by the *overlay*, not lost by the *basemap* |

The visible "white stripes" are the basemap showing through
un-painted gaps in the overlay. They are an overlay-render artifact,
not a tile or canvas defect.

## Recommendation: production rendering architecture

The brute-force engine is correct — every captures shows the
classification is truthful where it is asked. The bug is that the
**renderer asks the wrong thing**, and **paints the wrong primitive**.

Three options for the production renderer, evaluated against
doctrine (`docs/relocation_map_architecture.md`):

### Option A — keep lat/lon grid, paint geographic rectangles

**Idea:** Continue classifying a lat/lon grid; on paint, compute the
on-screen rectangle of each cell at the current zoom
(`latLngToContainerPoint(lat, lon)` and `latLngToContainerPoint(lat+grid_deg, lon+grid_deg)`),
and `fillRect` the whole rectangle.

**Strengths:** Minimal change. Single server call. Reuses the
existing `/brute-force-grid` response. Cell area is correctly
covered.

**Weaknesses:**
- Bug #1 unresolved unless we also reconcile the bounds-rect with
  `map.getBounds()` for the request. (Easy fix — always send
  `map.getBounds()` not the URL bounds.)
- Bug #3 unresolved unless we also paint the cell in every visible
  world copy. (Moderate fix — query `getBounds()` after wrap-
  normalisation and stretch the wrapped longitudes.)
- Geographic cells become very large on screen at high zoom; the
  cell can span dozens of pixels. The classification was done at the
  cell *vertex*, so the painted rectangle may be wrong at the
  vertex's far side if the underlying field changes within the cell.
  At 0.5° grid this is fine for house polygons (slowly varying); at
  0.1° it is fine for aspect-to-angle bands. At higher zoom, the
  cell can become tens of pixels across; per-vertex classification
  becomes a noticeable approximation near boundaries.

**Verdict:** correct for region polygons (slowly varying fields);
risky for aspect-to-angle bands at high zoom; *still does not adapt
to zoom* without explicit re-query logic.

### Option B — screen-pixel-truth as production

**Idea:** Iterate screen pixels (or small screen blocks) of the
visible map. Convert each block to `(lat, lon)`. Classify. Paint the
block. Re-query on every meaningful zoom/pan.

**Strengths:**
- Bug #1 cannot occur: the geography classified IS what is visible.
- Bug #2 cannot occur: the primitive painted IS the primitive sampled.
- Bug #3 cannot occur: each visible world copy generates its own
  screen pixels and is classified independently.
- Adaptive in the right direction: zoom in → fewer points per
  square degree → faster requests. Zoom out → more points per square
  degree → more compute, but the user is intentionally asking for a
  global view.
- Latency on world view is already **<0.3 s client total** at
  `block_px=6` for a single condition (this experiment).
- Geographic accuracy is governed by `block_px` (small block →
  per-pixel-correct).

**Weaknesses:**
- Cache-unfriendly across zoom levels: re-zooming means re-
  classifying. Mitigation: cache by (chart_id, condition_id,
  zoom_bucket, tile_id) — natural tile-style cache key.
- Each pan in the same zoom must re-request the new on-screen pixels.
  Mitigation: ask for a slightly larger ring around the visible
  viewport so small pans are free.
- Block-center sampling is wrong at the block scale; at `block_px=1`
  this is exact, at larger blocks it is a sub-block approximation.
  Mitigation: use the smallest block we can afford; production target
  is probably `block_px=2` or `block_px=3` (most "every pixel"
  language stays honest).

**Verdict:** structurally correct for both region polygons AND
aspect-to-angle bands. Adaptive to zoom. Compose-able with the
brute-force substrate (same astrology, same dispatch). Aligns with
the doctrine's "brute force as control specimen" (Option B *is* the
control specimen, just driven by screen pixels instead of
geographic vertices).

### Option C — tile-space (precomputed map tiles)

**Idea:** Pre-classify the full world at one fixed lat/lon
resolution per zoom level. Serve as raster tiles. Composite under
overlays.

**Strengths:**
- Cache-perfect across users with the same chart and condition.
- Predictable latency (just tile fetches).

**Weaknesses:**
- Requires a precomputation pass per (chart, condition, zoom). The
  app currently has one chart at a time; precomputing the world for
  every condition for every chart is plausible but heavy.
- Per-chart conditions are many (planet × house = 120; angle ×
  sign = 48; planet × angle × aspect × orb = thousands).
- Storage and invalidation get complex.

**Verdict:** Premature for the current phase. May become relevant
after the substrate is stable and we want sub-100 ms global zooms;
deferred per doctrine's "no premature optimisation" rule.

### Recommended path

**Adopt Option B (screen-pixel-truth) as the production renderer.**

1. Move the canonical "classify what is on screen" sandbox from
   `map_SANDBOX_screen_pixel_truth.html` into the production map.
2. Default `block_px = 2`. Profile-driven adjustment is fine; below
   that we should be using Option C tiles instead.
3. Re-query on `zoomend` and on debounced `moveend`. Cache by
   tile-style key so small pans are free.
4. Keep `/brute-force-grid` for back-end validation, regression
   tests, and the "control specimen" proof bundle. The lat/lon grid
   path is the right shape for off-screen *verification* (does the
   field exist where we think it does); the screen-pixel path is the
   right shape for on-screen *rendering*.
5. Aura, when it lands (step 9 in the doctrine), composes the
   discrete occupancy bands over the screen-pixel substrate — same
   rule as Option B, just with mask-aware opacity / saturation /
   density (as `docs/relocation_map_architecture.md` →
   Aura Rendering Principles requires).

Bug #1 (sampling-area mismatch) and Bug #3 (world-copy mismatch) are
solved automatically by this architecture. Bug #2 (drawing
primitive) is solved by construction.

### What this does NOT change

- **Astrology math is untouched.** Same Swiss Ephemeris call, same
  condition dispatch, same per-cell test. Both endpoints share that
  code path.
- **No smoothing was added.** Both A and B paint binary occupancy
  only.
- **No aura was added.** Banding, intensity curves, and per-orb
  weighting remain deferred to the aura phase.
- **No fake interpolation was added.** Block edges are honest at the
  block resolution; smaller blocks → finer edges, no spline-fitting.

The doctrine's "no inventing geometry" rule is intact in both
renderers; the screen-pixel renderer just samples the geometry where
the eye will actually look at it.

## Reproduce

```bash
# Server must be running:
./venv/bin/uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000

# Capture the 12-screenshot comparison matrix:
PLAYWRIGHT_BROWSERS_PATH=./venv/lib/python3.11/site-packages/playwright/driver/package/.local-browsers \
  ./venv/bin/python scripts/capture_screen_pixel_truth_diagnosis.py
```

Manual inspection of either sandbox (replace bounds / block / grid
to taste):

- Brute-force (lat/lon grid):
  `http://127.0.0.1:8000/map_SANDBOX_brute_force.html?A=a2a:saturn:mc:conjunction:1.0&gridDeg=0.1&bounds=-65,150,65,180&profile=baseline_validated&auto=1`
- Screen-pixel truth (sibling sandbox):
  `http://127.0.0.1:8000/map_SANDBOX_screen_pixel_truth.html?A=a2a:saturn:mc:conjunction:1.0&block=4&bounds=-65,150,65,180&profile=baseline_validated&auto=1`

URL slot syntax is identical between the two sandboxes (`pih:planet:house`,
`ais:angle:sign`, `a2a:planet:angle:aspect:orb`).
