# Adaptive Screen-Space Stress Test + Cache Feasibility

No rendering logic, astrology math, aura logic, raindrop visuals, or color polish changed. This is a benchmark artifact pass only.

## Outputs

- Screenshot folder: `validation/screenshots/screen_pixel_adaptive_stress`
- Manifest: `validation/screenshots/screen_pixel_adaptive_stress/manifest.json`
- Human review index: `validation/screenshots/screen_pixel_adaptive_stress/HUMAN_REVIEW_INDEX.md`

## Stress Summary

- Stress cases run: `18`
- Median reduction vs full 1px: `90.5%`
- Worst overlay XOR case: `high_svalbard_latcap_off` at `5.615%`
- Worst-case adaptive samples: `106,893`

## Cache Protocol Recommendation

1. Before first paint: compute only the requested field for the visible screen.
2. Immediately after first paint: if the render finished comfortably, compute zoom +1 for the same center only.
3. When user pauses: compute the 25% pan buffer and optionally zoom +2.
4. Only when the user opens relevant controls: compute angle/sign and aspect families.
5. Do not eagerly cache all planet/house/aspect combinations yet; the benchmark shows this is possible but not necessary before user intent is known.

Use the worst observed adaptive sample count plus 20% as the conservative production budget for first-pass scheduling.

## Cache Benchmark

### Priority 1: current requested field/current viewport/full visible screen

- Samples: `324,000`
- Server time: `1.94s`
- Memory estimate: `2.78 MiB`
- Background feasible: `True`
- Policy: `eager`
- Trigger: before first paint only for requested field

### Priority 2: same center zoom +1

- Samples: `324,000`
- Server time: `1.87s`
- Memory estimate: `2.78 MiB`
- Background feasible: `True`
- Policy: `delayed`
- Trigger: after first paint if user pauses

### Priority 2: same center zoom +2

- Samples: `324,000`
- Server time: `1.87s`
- Memory estimate: `2.78 MiB`
- Background feasible: `True`
- Policy: `delayed`
- Trigger: after first paint if user pauses

### Priority 3: 25% pan buffer around current viewport

- Samples: `729,000`
- Server time: `4.36s`
- Memory estimate: `6.26 MiB`
- Background feasible: `True`
- Policy: `delayed`
- Trigger: after first paint when user pauses

### Priority 4: all planet-in-house fields visible screen (10 planets * 1 selected house each)

- Samples: `324,000`
- Server time: `2.22s`
- Memory estimate: `2.78 MiB`
- Background feasible: `True`
- Policy: `delayed`
- Trigger: after first paint only if house overlay UI likely

### Priority 5: angle-in-sign fields visible screen

- Samples: `324,000`
- Server time: `2.09s`
- Memory estimate: `2.78 MiB`
- Background feasible: `True`
- Policy: `user-triggered`
- Trigger: when user opens angle/sign controls

### Priority 6: aspect-to-angle narrow envelope sample

- Samples: `324,000`
- Server time: `2.15s`
- Memory estimate: `2.78 MiB`
- Background feasible: `True`
- Policy: `user-triggered`
- Trigger: when user opens aspect controls

### Priority 6: aspect-to-angle wider envelope sample

- Samples: `324,000`
- Server time: `2.15s`
- Memory estimate: `2.78 MiB`
- Background feasible: `True`
- Policy: `user-triggered`
- Trigger: after user selects an aspect family
