# Current State

## Stable Milestone

The app has reached an early professional-tool milestone:

- `truth_grid` house overlays are working and remain opt-in.
- Staged/shared-grid ASC overlays are working.
- Angle-in-Sign MVP for `ASC` and `MC` is working.
- Seam behavior is visually coherent in current manual QA.
- Popup truth generally matches overlays in current validation.
- Validation contradictions are `0` in current truth-grid and angle-sign tests.
- Difficult High Northern and Southern edge cases have passed manual QA.
- The app is viable as an early professional astrology exploration tool, pending UX cleanup and broader QA.

## Current UX State

- The map is usable, but the sidebar is still prototype-like and too tall.
- Debug status should remain debug-only.
- User-facing status clutter should stay hidden unless deliberately redesigned.
- Dropdown behavior has been a recurring bug; recent work added a targeted click-through guard while keeping native selects.
- Popup behavior is generally good, with further aesthetic refinement still needed.

## Current Engineering State

- `main_centerline_FIXER.py` is the active backend entry point.
- `map_CURRENT.html` is the active frontend prototype.
- `truth_grid_engine.py` contains production-path truth-grid helpers.
- `truth_field_regions.py` remains an experimental/prototype utility.
- Existing validation reports live under `validation/`.

## Caveats

- `truth_grid` is not yet the default generation mode.
- The `+/-65` latitude cap remains in place.
- Stress-test coverage needs to expand before broader release.
- Leaflet remains acceptable for MVP, but should be reassessed after display and UX stabilization.
- Local Chrome temp folders and other scratch artifacts should not be committed.
