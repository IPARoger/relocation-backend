# Dense Multi-Condition Residue: Human Review Index

Policy: `edge2_thin2_highlat2_probes` (targeted refinement, no global slowdown).
Endpoint condition cap: `6` (5-condition and 6-condition stacks tested; 7-8 requires a backend cap change).

## `human_review_dense_5_world.png`

- Case: 5 conditions, world (`5` conditions)
- Reduction vs 1px: `54.2%`
- Adaptive samples: `148,481`
- 1px server seconds: `2.40` · adaptive server seconds: `1.08`
- XOR vs 1px: `0.280%`
- Changed pixels: `0.091%`
- Verdict: **acceptable with visible edge residue**
- Review PNG: `validation/screenshots/screen_pixel_dense_residue/human_review_dense_5_world.png`

## `human_review_dense_5_americas.png`

- Case: 5 conditions, Americas (`5` conditions)
- Reduction vs 1px: `42.3%`
- Adaptive samples: `186,853`
- 1px server seconds: `2.17` · adaptive server seconds: `1.33`
- XOR vs 1px: `0.386%`
- Changed pixels: `0.134%`
- Verdict: **acceptable with visible edge residue**
- Review PNG: `validation/screenshots/screen_pixel_dense_residue/human_review_dense_5_americas.png`

## `human_review_dense_5_pacific_seam.png`

- Case: 5 conditions, Pacific seam (`5` conditions)
- Reduction vs 1px: `70.6%`
- Adaptive samples: `95,122`
- 1px server seconds: `2.14` · adaptive server seconds: `0.64`
- XOR vs 1px: `0.073%`
- Changed pixels: `0.009%`
- Verdict: **acceptable / effectively identical**
- Review PNG: `validation/screenshots/screen_pixel_dense_residue/human_review_dense_5_pacific_seam.png`

## `human_review_dense_6_world.png`

- Case: 6 conditions, world (`6` conditions)
- Reduction vs 1px: `51.4%`
- Adaptive samples: `157,517`
- 1px server seconds: `2.25` · adaptive server seconds: `1.17`
- XOR vs 1px: `0.180%`
- Changed pixels: `0.065%`
- Verdict: **acceptable / effectively identical**
- Review PNG: `validation/screenshots/screen_pixel_dense_residue/human_review_dense_6_world.png`

## `human_review_dense_6_americas.png`

- Case: 6 conditions, Americas (`6` conditions)
- Reduction vs 1px: `40.0%`
- Adaptive samples: `194,265`
- 1px server seconds: `2.50` · adaptive server seconds: `1.44`
- XOR vs 1px: `0.334%`
- Changed pixels: `0.128%`
- Verdict: **acceptable with visible edge residue**
- Review PNG: `validation/screenshots/screen_pixel_dense_residue/human_review_dense_6_americas.png`

## `human_review_dense_6_pacific_seam.png`

- Case: 6 conditions, Pacific seam (`6` conditions)
- Reduction vs 1px: `70.6%`
- Adaptive samples: `95,122`
- 1px server seconds: `2.25` · adaptive server seconds: `0.69`
- XOR vs 1px: `0.073%`
- Changed pixels: `0.009%`
- Verdict: **acceptable / effectively identical**
- Review PNG: `validation/screenshots/screen_pixel_dense_residue/human_review_dense_6_pacific_seam.png`

## `human_review_dense_6_polar_north.png`

- Case: 6 conditions, polar north (`6` conditions)
- Reduction vs 1px: `73.8%`
- Adaptive samples: `84,986`
- 1px server seconds: `1.40` · adaptive server seconds: `0.57`
- XOR vs 1px: `0.117%`
- Changed pixels: `0.011%`
- Verdict: **acceptable / effectively identical**
- Review PNG: `validation/screenshots/screen_pixel_dense_residue/human_review_dense_6_polar_north.png`

## `human_review_dense_6_thin_world.png`

- Case: 6 conditions including 0.25° thin line, world (`6` conditions)
- Reduction vs 1px: `48.2%`
- Adaptive samples: `167,673`
- 1px server seconds: `2.30` · adaptive server seconds: `1.42`
- XOR vs 1px: `0.188%`
- Changed pixels: `0.070%`
- Verdict: **acceptable / effectively identical**
- Review PNG: `validation/screenshots/screen_pixel_dense_residue/human_review_dense_6_thin_world.png`
