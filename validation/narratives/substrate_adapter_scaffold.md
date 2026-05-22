# Substrate Adapter Scaffold Validation

Date: 2026-05-22

## Scope

Phase 1.4 validates the inert substrate adapter scaffold created for the future production migration path. The adapter is an interface boundary only; it does not migrate rendering, change astrology math, change overlay visuals, or connect `map_CURRENT.html` to `/screen-pixel-truth`.

## What The Adapter Defines

- Viewport request shape: bounds, zoom, paint size, block size, and lat-cap policy.
- Classification request shape: birth payload, viewport, conditions, and optional request id.
- Cancellation scope: an `AbortController`-backed signal and explicit abort hook.
- Cache boundary shape: chart key, substrate id, viewport-derived keys, lat-cap flag, and condition set.
- Refinement status shape: stage, sample count, cell count, stop reason, and convergence flag.
- Renderer-host ownership boundary: production host owns Leaflet state, visible layers, sidebar inputs, popup truth, render status, and debug panels; substrate/cache layers own classification, masks, refinement metrics, cancellation, priority, and budget accounting.

## What It Does Not Do

- It does not call `/search-regions`.
- It does not call `/screen-pixel-truth`.
- It does not render layers, alter colors, or compose overlays.
- It does not warm cache entries or schedule background work.
- It does not replace `currentRenderToken`, `postSearchRegions`, or any legacy production renderer path.
- It does not introduce aura, reveal, animation, or aesthetics.

## Why It Is Inert

`map_CURRENT.html` loads `/substrate_adapter.js` and stores `window.RelocationSubstrateAdapter` in `substrateAdapter`, but the only production-host exposure is through `window.__rmSmokeState()`. The rendering path still enters `findRegions()`, builds the legacy payload, and posts through `postSearchRegions()` to `/search-regions`.

The hardened smoke asserts that a normal production render triggers `/search-regions`, does not trigger `/screen-pixel-truth`, and leaves the adapter as observational contract state only.

## Rollback Scope

Rollback is limited to removing:

- `/substrate_adapter.js` serving route in `main_centerline_FIXER.py`.
- `<script src="/substrate_adapter.js"></script>` and smoke-state exposure in `map_CURRENT.html`.
- `substrate_adapter.js`.
- `scripts/smoke_substrate_adapter.py`.
- This narrative.

No persisted data, astrology math, rendering semantics, or cache state depend on the scaffold.

## Readiness

The scaffold is ready for the next migration step as an interface boundary. Phase 1.5 may begin only if it preserves one instability source and keeps production rendering on `/search-regions` until a separately validated adapter dispatch step is introduced.
