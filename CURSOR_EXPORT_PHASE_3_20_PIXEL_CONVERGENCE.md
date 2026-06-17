# PHASE 3.20 - PIXEL CONVERGENCE / ANTI-IMPRESSIONISM CORRECTION

## Result

PASS.

Updated the existing Phase 3.17 storyboard sandbox:

`validation/sandboxes/phase3_17_polygon_emergence_storyboard.html`

Refreshed the proof screenshot:

`validation/screenshots/phase3_17_polygon_emergence_storyboard/01_dark_light_storyboard.png`

This remains a static storyboard. No animation loop, production integration, backend math change, cache change, or Phase 3.15 / Phase 3.16 change was made.

## Behavioral Corrections

- Reduced color identity to binary computational roles: selected occupancy uses the yellow family, rejected occupancy uses the blue family.
- Removed red from active occupancy rendering to avoid multicolor/impressionistic mixing.
- Delayed interior fill further: Acts 5-6 are now dominated by border pressure and compression, not center fill.
- Replaced Act 6 with `Occupancy Compression`, separating broad froth from final lock.
- Generated paired boundary samples on both sides of real edges so peak froth is more bilateral.
- Changed particle rendering to two-pixel snapped square marks for a more raster-native computational field.
- Kept virga visible through Act 7 while selected occupancy settles toward the center-out fill.
- Preserved Act 8 as clean vector certainty with no particles, outline, residue, texture, or process trace.

## Verified Browser State

```text
source: POST /search-regions generation_mode=contour
canonicalFeatureId: house-0-sun-1-0
planet: sun
house: 1
generation_mode: contour
slideCount: 8
modeCount: 2
canvasCount: 16
particleCount: 2300
```

Verified computational basis:

```text
real GeoJSON polygon projection
point-in-polygon occupancy
screen-space boundary distance
deterministic seeded particle field
delayed color identity
binary yellow/blue occupancy identity
wide peak froth before edge lock
bilateral froth overpopulation
occupancy compression before vector resolution
staggered upward virga release
center-out interior settlement
two-pixel snapped square raster marks
static storyboard frames
```

## Static / Anti-Painterly Verification

Keyword scan found no use of:

- `requestAnimationFrame`
- `setTimeout`
- `setInterval`
- CSS transitions
- CSS animations
- gradients
- blur/filter effects
- glow
- painterly brush/watercolor/smudge logic

Linter diagnostics reported no errors for the storyboard file.

Screenshot metadata:

```text
PNG image data, 1600 x 1800, 8-bit/color RGB, non-interlaced
```

## Files Changed

```text
?? CURSOR_EXPORT_PHASE_3_20_PIXEL_CONVERGENCE.md
?? validation/sandboxes/phase3_17_polygon_emergence_storyboard.html
?? validation/screenshots/phase3_17_polygon_emergence_storyboard/
```

No commit was made.

## Honest Remaining Notes

- This is still a storyboard-state artifact, not a live 3-5 second runtime animation.
- Pixel marks are more computational now, but actual production density and zoom behavior remain untested.
- The blue rejected side is still a visual scaffold, not final overlay semantics.
- Act 7 is closer to Act 8, but live temporal easing will need a separate pass to make the transition feel fully earned.
