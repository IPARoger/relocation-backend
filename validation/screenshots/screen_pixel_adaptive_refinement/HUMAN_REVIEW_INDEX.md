# Human Review Index: Adaptive Screen-Space Refinement

These PNGs are review sheets only. They composite the already-generated adaptive overlays over a matching Leaflet basemap; no rendering logic, astrology math, colors, aura, or styling were changed.

Folder: `/Users/davegoodman/Desktop/relocation-backend/validation/screenshots/screen_pixel_adaptive_refinement`

## `human_review_saturn_mc_0p5_pacific.png`

- Path: `/Users/davegoodman/Desktop/relocation-backend/validation/screenshots/screen_pixel_adaptive_refinement/human_review_saturn_mc_0p5_pacific.png`
- What it proves: `Saturn conjunct MC, orb 0.5, Pacific` adaptive refinement over real map context, compared against full 1px screen-space truth.
- 1px sample count: `576,000`
- Adaptive sample count: `50,580`
- Reduction: `91.22%`
- Timing: full 1px `5.41s`; adaptive classify `0.47s`; speedup `11.5x`
- Overlay XOR: `0.000%`
- Visual verdict: Visually identical; final adaptive overlay matches the 1px reference in this proof.

## `human_review_saturn_mc_1_pacific.png`

- Path: `/Users/davegoodman/Desktop/relocation-backend/validation/screenshots/screen_pixel_adaptive_refinement/human_review_saturn_mc_1_pacific.png`
- What it proves: `Saturn conjunct MC, orb 1, Pacific` adaptive refinement over real map context, compared against full 1px screen-space truth.
- 1px sample count: `576,000`
- Adaptive sample count: `53,130`
- Reduction: `90.78%`
- Timing: full 1px `5.38s`; adaptive classify `0.49s`; speedup `11.1x`
- Overlay XOR: `0.000%`
- Visual verdict: Visually identical; final adaptive overlay matches the 1px reference in this proof.

## `human_review_saturn_asc_1_world.png`

- Path: `/Users/davegoodman/Desktop/relocation-backend/validation/screenshots/screen_pixel_adaptive_refinement/human_review_saturn_asc_1_world.png`
- What it proves: `Saturn conjunct ASC, orb 1, world` adaptive refinement over real map context, compared against full 1px screen-space truth.
- 1px sample count: `576,000`
- Adaptive sample count: `56,168`
- Reduction: `90.25%`
- Timing: full 1px `4.98s`; adaptive classify `0.48s`; speedup `10.4x`
- Overlay XOR: `0.000%`
- Visual verdict: Visually identical; final adaptive overlay matches the 1px reference in this proof.

## `human_review_sun_1st_world.png`

- Path: `/Users/davegoodman/Desktop/relocation-backend/validation/screenshots/screen_pixel_adaptive_refinement/human_review_sun_1st_world.png`
- What it proves: `Sun in 1st, world` adaptive refinement over real map context, compared against full 1px screen-space truth.
- 1px sample count: `576,000`
- Adaptive sample count: `70,329`
- Reduction: `87.79%`
- Timing: full 1px `4.89s`; adaptive classify `0.58s`; speedup `8.5x`
- Overlay XOR: `0.140%`
- Visual verdict: Effectively identical; inspect diff panel for tiny boundary residue.

## `human_review_triple_overlap_americas.png`

- Path: `/Users/davegoodman/Desktop/relocation-backend/validation/screenshots/screen_pixel_adaptive_refinement/human_review_triple_overlap_americas.png`
- What it proves: `Sun 1st + ASC Capricorn + MC Libra, Americas` adaptive refinement over real map context, compared against full 1px screen-space truth.
- 1px sample count: `576,000`
- Adaptive sample count: `109,423`
- Reduction: `81.00%`
- Timing: full 1px `5.03s`; adaptive classify `1.00s`; speedup `5.0x`
- Overlay XOR: `0.018%`
- Visual verdict: Visually identical for review purposes; only tiny edge-pixel residue remains.
