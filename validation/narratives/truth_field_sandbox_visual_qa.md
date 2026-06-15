# Truth Field Reveal — Sandbox Visual QA Evidence Bundle

**Date:** 2026-05-20
**Sandbox URL:** `http://127.0.0.1:8000/map_SANDBOX_truth_reveal.html`
**Output dir:** `validation/screenshots/truth_field_sandbox/`
**Manifest (machine-readable):** `validation/screenshots/truth_field_sandbox/manifest.json`
**Capture script:** `scripts/capture_truth_reveal_sandbox.py`
**Sandbox HTML:** `map_SANDBOX_truth_reveal.html`

This document is **evidence**, not assessment. Every metric below is read
directly from `properties.*` on the `/aura-raster-convergence` response and
serialized into the manifest. The screenshots are the literal map pane at
the moment the engine reported `__sandboxStatus === "complete"`.

Human QA should compare images side by side and decide whether what is
visible matches what the metrics claim.

## How the captures were produced (no rendering-logic changes)

The sandbox HTML was extended with four URL-param hooks. None of them
change how Mode A / B / C / Off render — they only control initial state
and an optional early termination of the run loop:

| Param | Effect |
|---|---|
| `?mode=silent\|pointillist\|frontier\|off` | preselect a reveal mode |
| `?viewport=asc\|greenland` | preselect viewport bounds |
| `?stopAtStage=N` | stop after stage N (0..3); does **not** alter what each stage renders |
| `?latCap=0\|1` | passes `apply_lat_cap` to the engine (default 1) |
| `?profile=<id>` | preselect a chart profile |
| `?auto=1` | auto-run the reveal once profile + viewport are ready |

The sandbox also exposes `window.__sandboxStatus` and
`window.__sandboxStageResults` for Playwright synchronization and to
extract per-stage engine state without scraping the panel.

## File list

| Image | Case | Engine state (final stage of run) |
|---|---|---|
| `mode_a_silent_stage0_asc_band.png` | Mode A, seed only | 240 samples, 184 leaves, frontier 166, residual 0, maxΔ=0.2841, meanΔ=0.0257, stop=`sample_budget`, converged=false |
| `mode_a_silent_final_asc_band.png` | Mode A, full run | 3,452 samples, 3,544 leaves, frontier 2,099, residual 2,023, maxΔ=0.0341, meanΔ=0.0067, stop=`converged`, converged=true |
| `mode_b_pointillist_early_asc_band.png` | Mode B, seed only | 240 samples, 184 leaves, frontier 166, residual 0, maxΔ=0.2841, stop=`sample_budget` |
| `mode_b_pointillist_mid_asc_band.png` | Mode B, stages 0+1 | 900 samples, 679 leaves, frontier 631, residual 0, maxΔ=0.1029, meanΔ=0.0144, stop=`sample_budget` |
| `mode_b_pointillist_final_asc_band.png` | Mode B, full run | 3,452 samples, 3,544 leaves, frontier 2,099, residual 2,023, maxΔ=0.0341, stop=`converged` |
| `mode_c_frontier_final_asc_band.png` | Mode C at Sun–ASC band | 3,452 samples, 3,544 leaves, frontier 2,099, residual 2,023, maxΔ=0.0341, stop=`converged` |
| `mode_c_frontier_final_greenland.png` | Mode C at Greenland (cap on) | 206 samples, 208 leaves, frontier 99, residual 98, maxΔ=0.1757, meanΔ=0.0166, stop=`no_actionable_leaves` |
| `mode_off_final_asc_band.png` | Off at Sun–ASC band | 3,452 samples, 3,544 leaves, frontier 2,099, residual 2,023, maxΔ=0.0341, stop=`converged` |
| `latcap_capped_greenland.png` | Lat-cap A/B: cap **on** | 206 samples, 208 leaves, frontier 99, residual 98, **maxΔ=0.1757**, stop=`no_actionable_leaves` |
| `latcap_uncapped_greenland.png` | Lat-cap A/B: cap **off** | 336 samples, 325 leaves, frontier 142, residual 141, **maxΔ=0.6941**, stop=`no_actionable_leaves` |

Profile used in all captures: `baseline_validated`. Viewport bounds for `asc_band`: ~(-17.3°S … 17.3°N, -110.7°W … -69.3°W). Viewport bounds for `greenland`: ~(57.5°N … 71.7°N, -50.4°W … -4.6°W).

## Exact URL/query used for each screenshot

| Image | URL |
|---|---|
| `mode_a_silent_stage0_asc_band.png` | `?mode=silent&viewport=asc&stopAtStage=0&profile=baseline_validated&auto=1` |
| `mode_a_silent_final_asc_band.png` | `?mode=silent&viewport=asc&profile=baseline_validated&auto=1` |
| `mode_b_pointillist_early_asc_band.png` | `?mode=pointillist&viewport=asc&stopAtStage=0&profile=baseline_validated&auto=1` |
| `mode_b_pointillist_mid_asc_band.png` | `?mode=pointillist&viewport=asc&stopAtStage=1&profile=baseline_validated&auto=1` |
| `mode_b_pointillist_final_asc_band.png` | `?mode=pointillist&viewport=asc&profile=baseline_validated&auto=1` |
| `mode_c_frontier_final_asc_band.png` | `?mode=frontier&viewport=asc&profile=baseline_validated&auto=1` |
| `mode_c_frontier_final_greenland.png` | `?mode=frontier&viewport=greenland&profile=baseline_validated&auto=1` |
| `mode_off_final_asc_band.png` | `?mode=off&viewport=asc&profile=baseline_validated&auto=1` |
| `latcap_capped_greenland.png` | `?mode=silent&viewport=greenland&latCap=1&profile=baseline_validated&auto=1` |
| `latcap_uncapped_greenland.png` | `?mode=silent&viewport=greenland&latCap=0&profile=baseline_validated&auto=1` |

All prefixed with `http://127.0.0.1:8000/map_SANDBOX_truth_reveal.html`.

## What human QA should inspect

### Mode A — stage 0 vs final (same viewport)
- **Stage 0 image** should show a visibly *blocky* aura — the 4×4 initial quadtree partition with shallow recursion (max depth ≈ 1–2). Individual leaf rectangles should be discernible. The band's outline should be present but stair-stepped.
- **Final image** should show a continuous band with no visible quadtree grid.
- QA question: is the stage-0 frame *acceptable* as the opening of a reveal, or does it look like a debug overlay that shouldn't be shown to a user? The doctrine permits showing this honestly; the product question is whether it's perceptually right.
- maxΔ falls from 0.28 → 0.034 between these two frames. That's an order-of-magnitude truth improvement. Verify the visual improvement matches.

### Mode B — early / mid / final
- **Early (240 samples)** should be visibly sparse: ~184 dots aligned to the 4×4 initial-division grid, with depth-1/2 leaves doubling the local density in band cells. Dots should clearly read as individual points.
- **Mid (900 samples)** should be a transitional density: 679 dots, ~2× denser in the band than off-band. Individual dots still discernible.
- **Final (3,452 samples)** dots blend into a near-continuous band along the spine. QA question: at this density, is "pointillist" still legible, or does it just look like a stippled raster?
- meanΔ falls 0.0257 → 0.0144 → 0.0067 across the three. Verify the visible densification corresponds.

### Mode C — frontier at two viewports
- **asc_band frontier**: dashed pink outlines should densely cover the band region and extend slightly past it. Two dash styles: lighter dash = frontier leaves still owed work; tighter dash = pixel-atomic / min-cell leaves with non-zero debt (cannot refine further). The engine reports `converged=true` but 2,023 of 3,544 leaves are residual — i.e., the convergence threshold is met *globally* while individual leaves still disagree with the per-pixel reference.
- QA question: does seeing the dense pink mesh on a "converged" map *help* the user, or does it look like the engine is broken?
- **Greenland frontier**: pink mesh should appear only inside the southern tip of Greenland (below ~65°N). The rest of Greenland and all of Iceland should be empty (no aura, no outlines).

### Mode Off — sanity check
- Visually identical to Mode A final (same converged raster). Confirms that staging does not change the truth — only its presentation.

### Lat-cap A/B — Greenland
- **Capped**: amber aura exists only in the SW corner of the viewport (south of ~65°N). Greenland mainland and Iceland are clean. maxΔ = 0.176.
- **Uncapped**: amber aura extends visibly further north along the western coast of Greenland into the polar region. maxΔ = **0.694** (≈ 4× worse).
- QA question: the uncapped image is more visually "complete" — does it look more correct, or does the 4× worse max disagreement against the reference change the interpretation? The doctrine claim is that swe.houses is unstable near the poles and the cap is honest refusal, not arbitrary clipping. The maxΔ supports that.

## Known artifacts visible in the bundle

1. **Mode A stage 0 quadtree grid is visible.** This is not a rendering bug — the 184 leaves at depth 0–2 are 96×72 pixels divided coarsely. With nearest-neighbor rendering enforced (`imageSmoothingEnabled=false`), each leaf paints as a rectangle of constant color. A naive viewer may read this as broken graphics.
2. **Mode B dots have grid bias.** Dots sit at leaf centers, which inherit the quadtree's regular subdivision pattern. Especially visible in the early frame: rows and columns are clearly aligned. This is real — leaf centers are not jittered — but it weakens the "organic discovery" feel.
3. **Mode C residual count is large at convergence (2,023 of 3,544).** The engine reports `converged=true` against the global `pixels_above_threshold` target (0.05) while ~57 % of leaves are pixel-atomic with debt > 0. The dashed mesh is therefore very dense at "convergence." This is a sandbox-revealed limit of the current convergence definition, not a rendering choice.
4. **Mode C at Greenland — no visible cap line.** The transition between "below cap, aura + frontier" and "above cap, nothing" is implicit. A user not told about the ±65° policy may not realize *why* the field stops. The sandbox does not draw a cap boundary; the metrics report it but the map does not annotate it.
5. **Lat-cap uncapped — visible block artifacts at higher latitudes.** Above ~65°N the uncapped raster shows larger, blockier amber leaves than south of the cap. This is the adaptive engine spending fewer samples there (depth bound + no_actionable_leaves stop), which honestly reflects degraded engine confidence. A viewer may misread the blockiness as a rendering bug.
6. **Sandbox banner ("stage X · N samples") overlaps the map in screenshots.** This is part of the sandbox UX, not a capture artifact. It does not obstruct any aura region for the cases captured here, but it does sit at the top-center of every image.
7. **OSM basemap shows full color at high zoom while the sandbox CSS dims tile-pane brightness.** Both states are present in different images (e.g. Greenland appears warmer because Iceland's tile coverage is denser). This is a basemap rendering quirk, not a truth-field artifact.
8. **The map pixel scale is non-uniform across captures.** The Greenland viewport zoom level resolves to a smaller map area in screen pixels than the asc_band zoom; comparing dot sizes across viewports is misleading. Within a viewport, comparisons are valid.

## Whether Cursor's assessment may be overly generous

**Yes, in specific places.** I am the model that wrote both the sandbox and this evidence bundle. Some risks of self-graded generosity:

- **The previous narrative report (delivered before the screenshots existed)** called Mode A's stage-0 result "already looks mostly correct." The actual stage-0 image refutes that — it is visibly blocky. The screenshots are more critical of the seed pass than the prose was. **Trust the images, not the earlier prose.**
- **Mode A is the easiest mode to over-praise** because the final image looks clean. The progression *is* real (maxΔ 0.28 → 0.034, four stages of refinement), but whether the in-between frames are aesthetically acceptable is a human-only judgment. I am inclined to call it "premium" or "calm." Do not trust me on that. Inspect the images.
- **Mode B "discovery" framing risks being aspirational.** The early image is genuinely sparse and reads as discovery; the final image reads as a stippled raster. The mid frame is the strongest argument for the mode, and it's the one I had to re-capture (the initial stop-at-stage-2 was visually identical to final). I have an incentive to present Mode B as more effective than it is.
- **Mode C self-assessment is more reliable.** The dense pink mesh on a "converged" map is uncomfortable to look at; I have already flagged this and the visual unambiguously supports the critique. Low risk of over-generosity here.
- **Lat-cap A/B is the strongest doctrine demonstration in the bundle** and I do believe the metrics (maxΔ 0.18 vs 0.69) are decisive. But "decisive" is a quantitative claim; the perceptual reading ("looks honest") is still a human-only judgment. Inspect both images.
- **Doctrine compliance can be claimed mechanically:** the capture script reads `properties.*` directly from the engine response and writes them to the manifest; the sandbox HTML only renders attributes that exist on the engine response (strengths, leaf bounds, leaf debt, leaf stop_reason). There is no path in the captured code where a visual element comes from a non-engine source.

## Suggested human QA workflow

1. Open the two Mode A images side by side. Ask: *does the visible refinement justify keeping a staged reveal in the product, or is "Off mode" sufficient?*
2. Open the three Mode B images. Ask: *does the early-stage image look like a debug overlay or like discovery?* If the answer is "debug overlay," the mode does not survive — the doctrine forbids smoothing the dots, so the only fix is restricting Mode B to viewports/zooms where dot count stays below some threshold.
3. Open the Mode C asc_band image. Ask: *would a user trust this map?* If no, the convergence threshold and/or residual handling needs to be tightened (Phase D work, not a rendering tweak).
4. Open the two lat-cap Greenland images side by side. Ask: *does the cap policy feel like the right default?* The maxΔ numbers argue strongly yes, but the uncapped image is the one that will resurface if anyone proposes "let's just show everything."
5. Open the Mode C Greenland image. Ask: *is it obvious why the field stops where it stops?* If no, Phase D should add a visible cap-line annotation.

## Reproduction

```
# server (must be running for the sandbox to fetch endpoints)
./venv/bin/uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000

# captures (10 cases, ~16s end-to-end against the live server)
./venv/bin/python3 scripts/capture_truth_reveal_sandbox.py
```

Re-running overwrites all PNGs and the manifest in place.
