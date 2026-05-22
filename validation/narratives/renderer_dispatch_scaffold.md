# Renderer Dispatch Scaffold Validation

Date: 2026-05-22

## Scope

Phase 1.5 introduces an explicit renderer dispatch boundary in `map_CURRENT.html` without changing production rendering behavior. The active substrate is locked to:

```text
legacy_search_regions
```

## Dispatch Boundary

`map_CURRENT.html` now declares `ACTIVE_RENDERER_SUBSTRATE` and routes overlay requests through `dispatchOverlayRequest()`. That dispatcher currently accepts only `legacy_search_regions`; every valid production overlay request still delegates to the existing `postSearchRegions()` helper and therefore to `/search-regions`.

This makes future substrate switching explicit. A future phase can add a named canonical screen-space branch, but there is no automatic substrate detection, hidden fallback, or opportunistic route selection.

## Why Active Substrate Remains Legacy

Production rendering is still the legacy GeoJSON overlay path. It preserves the current visual behavior, request shape, layer composition, debug status flow, and rollback expectations while the canonical screen-space path remains unwired.

The hardened smoke confirms a normal production render calls `/search-regions`, does not call `/screen-pixel-truth`, and reports `rendererSubstrate = legacy_search_regions`.

## Reversibility

Rollback is limited to removing `ACTIVE_RENDERER_SUBSTRATE`, replacing `dispatchOverlayRequest(...)` calls with the previous `postSearchRegions(...)` calls, and removing the smoke assertion/narrative. No backend route, astrology math, visual styling, cache behavior, or substrate adapter contract depends on this dispatch boundary.

## Future Switch Step

The future canonical screen-space migration should add a separate, explicitly named substrate branch after validation proves parity. That step should be its own instability source and should still avoid cache integration, aura styling, animation, and unrelated renderer cleanup.

## Intentionally Not Changed

- `/search-regions` remains the active production route.
- `/screen-pixel-truth` is not called from production.
- No cache or scheduler is wired into `map_CURRENT.html`.
- No visible overlay colors, geometry semantics, layer ordering, or popup truth behavior changed.
- No astrology math changed.
- No aura, reveal, animation, or aesthetic work was introduced.
