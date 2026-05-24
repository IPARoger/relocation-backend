# Phase 2.17 — Viewport-Scoped Hydration Sandbox

## Purpose

Phase 2.17 creates a controlled, reversible, dev-only sandbox for viewport-scoped hydration overlays.

It proves isolated overlays can remain bound to sanitized viewport metadata, invalidate during viewport shifts, and rehydrate replacements without transferring renderer ownership, claiming viewport ownership, synchronizing production map state, mutating production overlay registries, persisting state, or exposing raw backend payloads.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_viewport_hydration_sandbox.js` exposes `window.RelocationSamplingCacheViewportHydrationSandbox` with:

- `createViewportHydrationSandbox`
- `hydrateOverlay`
- `setViewportScope`
- `replaceOverlay`
- `invalidateOutOfScope`
- `removeOverlay`
- `removeAll`
- `inspect`

The sandbox maintains an internal active viewport scope and an isolated namespace map. It writes only disposable dev DOM nodes under a caller-provided root. Overlay validity is scoped to sanitized viewport metadata such as viewport id, zoom, bounds, and semantic viewport id.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and always reports that renderer and viewport ownership were not claimed. Overlay hydration is accepted only when the requested viewport scope matches the active sandbox viewport. Changing the sandbox viewport invalidates out-of-scope overlays and clears their sandbox DOM nodes. Replacement after a viewport shift must rehydrate against the new active viewport.

It rejects mismatched viewport scopes, stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist hydrated state, start workers, schedule background rendering, synchronize production viewport state, interpret astrology, or change backend runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_17_viewport_hydration_sandbox.py
```

The smoke verifies:

- overlays remain bound to viewport scope,
- viewport shifts invalidate stale overlays correctly,
- replacement overlays supersede correctly after viewport changes,
- deterministic hydration ordering survives viewport transitions,
- out-of-scope overlays clean up correctly,
- namespace isolation survives viewport changes,
- cancelled and stale overlays do not display,
- production renderer remains untouched,
- no overlay registry contamination occurs,
- no DOM writes escape the sandbox root,
- `rendererSubstrate` remains `legacy_search_regions`,
- raw payload fields are rejected,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_viewport_hydration_sandbox.js`
- `scripts/smoke_phase2_17_viewport_hydration_sandbox.py`
- this narrative
- the tiny Phase 2.17 roadmap note

No production renderer logic, production overlay registry, production viewport synchronization path, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga system, AI/intake path, interpretation system, persistence layer, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** viewport-scoped hydrated proofs can invalidate and rehydrate without becoming viewport or renderer orchestration.
- **Deferred excellence:** live map binding, production viewport synchronization, production overlay ownership, animation, scheduler takeover, workers, background rendering, persistence, and richer map integration remain future work.
- **Rejected scope:** viewport synchronization takeover, real scheduler integration, production registry mutation, raw GeoJSON hydration, Leaflet lifecycle integration, aura/virga rendering, speculative rendering, backend changes, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.17 checkpoint only if no unrelated files are staged.
