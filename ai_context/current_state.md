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

- The map is usable; the sidebar was tightened (sections, paired planet/house rows, calmer chrome) but remains a single-column prototype—no drawer overhaul yet.
- Debug status should remain debug-only.
- User-facing status clutter should stay hidden unless deliberately redesigned.
- Dropdown behavior has been a recurring bug; recent work added a targeted click-through guard while keeping native selects.
- Popup behavior is generally good, with further aesthetic refinement still needed.

- See also: `docs/current_sidebar_ux_audit.md` for latest sidebar audit and pass notes.

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

## Rendering Substrate (2026-05-21)

- **Canonical visible overlays:** screen-space classification via `/screen-pixel-truth`, adaptive refinement (`edge2_thin2_highlat2_probes` + lat-cap boundary rules). See `docs/CURRENT_RENDERING_DOCTRINE.md`.
- **Authoritative Phase-C doctrine:** `docs/PHASE_C_RENDERING_ARCHITECTURE.md`, `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`, `docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md`, and `docs/PHASE_C_IMPLEMENTATION_PROTOCOL.md`.
- **Brute-force geographic grid:** validation wall only (`map_SANDBOX_brute_force.html`); not production.
- **Phase-2 cache:** prototype in `map_SANDBOX_phase2_cache.html`; smoke `scripts/smoke_phase2_cache.py`. Not wired to `map_CURRENT.html` yet.
- **Ready for aesthetics** per dense-residue pass (`validation/narratives/screen_pixel_dense_residue.md`).

## Renderer Beta Stabilization (2026-05-26)

- The transported-material aspect-band renderer is **beta-stabilized in validation artifacts**, not production-integrated and not final aesthetic approval.
- Frozen validation architecture: texture-coordinate transport, local `(s,u)` sampling, independent side normalization, proportional ridge/material scaling under asymmetry, and ridge embedded inside the material rather than drawn as a separate stroke.
- Validated in static/sandbox artifacts through asymmetry, extreme asymmetry, multicolor, and map-like overlap boards.
- Current next renderer-adjacent work should remain validation-only: review Phase 2.52 map/overlap sandbox evidence, run map-context validation only if needed, then resume rain/virga exploration.
- Do not edit `map_CURRENT.html` or reopen renderer architecture unless map-context validation proves structural failure.
