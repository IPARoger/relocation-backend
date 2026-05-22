# Dense Multi-Condition Residue — Focused Stress

No rendering logic, astrology math, colors, aura, raindrop visuals, or new refinement rules added. This pass re-runs the doctrine-selected targeted policy against a focused dense-overlay matrix to determine whether the previously-observed `~0.334%` XOR residue on `mixed_dense_six_conditions` is acceptable, reducible, or a sign of another refinement rule.

Doctrine cross-reference: `docs/relocation_map_architecture.md` § "Refinement Hardening — Targeted Policy, Not Global Slowdown". Original adaptive policy report: `validation/narratives/screen_pixel_adaptive_targeted.md`.

## Outputs

- Manifest: `validation/screenshots/screen_pixel_dense_residue/manifest.json`
- Human review index: `validation/screenshots/screen_pixel_dense_residue/HUMAN_REVIEW_INDEX.md`
- Screenshots root: `validation/screenshots/screen_pixel_dense_residue`

## Policy under test

- `edge2_thin2_highlat2_probes` — edge halo +`2`, thin-line halo +`2`, high-latitude halo +`2`, lat-cap boundary force-refine within `4.0°` of ±`65.0°`.
- Tested against the doctrine-frozen `screen_pixel_adaptive_targeted` policy; no extra refinement was added for this pass.
- Endpoint condition cap is `6` (`_MAX_CONDITIONS` in `main_centerline_FIXER.py`). 7–8-condition stacks would require a backend cap change and are explicitly out of scope for this pass.

## Results

| case | n | viewport | samples | reduction | xor% | changed% | verdict |
|---|---:|---|---:|---:|---:|---:|---|
| `dense_5_world` | 5 | world | 148,481 | 54.2% | 0.280 | 0.091 | acceptable with visible edge residue |
| `dense_5_americas` | 5 | -55,-160,70,-30 | 186,853 | 42.3% | 0.386 | 0.134 | acceptable with visible edge residue |
| `dense_5_pacific_seam` | 5 | -50,160,5,200 | 95,122 | 70.6% | 0.073 | 0.009 | acceptable / effectively identical |
| `dense_6_world` | 6 | world | 157,517 | 51.4% | 0.180 | 0.065 | acceptable / effectively identical |
| `dense_6_americas` | 6 | -55,-160,70,-30 | 194,265 | 40.0% | 0.334 | 0.128 | acceptable with visible edge residue |
| `dense_6_pacific_seam` | 6 | -50,160,5,200 | 95,122 | 70.6% | 0.073 | 0.009 | acceptable / effectively identical |
| `dense_6_polar_north` | 6 | 55,-60,82,40 | 84,986 | 73.8% | 0.117 | 0.011 | acceptable / effectively identical |
| `dense_6_thin_world` | 6 | world | 167,673 | 48.2% | 0.188 | 0.070 | acceptable / effectively identical |

Worst XOR observed: **0.386%** on `dense_5_americas` (5 conditions, Americas).

## Verdict

All cases pass the previous `failed or needs tighter refinement` threshold; the worst case is **`0.386%`** XOR which falls in the `acceptable with visible edge residue` band. Residue is structurally edge-only and concentrated at multi-condition transition seams where 4-5 polygons stack. Recommendation: **accept** this residue and proceed to aesthetics. Targeted refinement is already pulling at the structural limit of bitmask-mode rendering on 720×450, and further reduction would require either (a) higher per-pixel sample density along multi-overlap seams or (b) the negative-space optimisation noted as future work.

## Where the residue concentrates

Diff bounding boxes for every case lie at multi-overlap **transition seams** between two or more occupied conditions. No residue was observed inside stable single-condition regions, on empty regions, or on the centerline of the thin-line aspect itself.

## Endpoint cap note (not blocking)

The `/screen-pixel-truth` endpoint currently caps requests at `6` simultaneous conditions (`_MAX_CONDITIONS`). 7–8-condition stacks would require:

1. Raising `_MAX_CONDITIONS` and `_CONDITION_LABELS` in `main_centerline_FIXER.py`.
2. Raising the bitmask width in the renderer's `deterministic_color()` fallback (currently >7 → debug-only deterministic palette).
3. Re-checking the rendering palette for legible overlap colors at higher condition counts.

Items (1) and (2) are mechanical; (3) is a colour-system question and belongs in the aesthetics pass. No 5-condition or 6-condition case in this matrix is constrained by the cap.
