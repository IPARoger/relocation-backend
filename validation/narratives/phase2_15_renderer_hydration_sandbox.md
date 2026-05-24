# Phase 2.15 — Renderer Hydration Sandbox

## Purpose

Phase 2.15 creates one isolated, reversible, dev-only visual hydration sandbox.

It proves sanitized runtime hydration metadata can become visible without transferring renderer ownership, replacing production overlays, mutating production overlay registries, persisting state, or exposing raw backend payloads.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_renderer_hydration_sandbox.js` exposes `window.RelocationSamplingCacheRendererHydrationSandbox` with:

- `createRendererHydrationSandbox`
- `hydrateOnce`
- `removeOverlay`
- `inspect`

The sandbox accepts a sanitized hydration envelope plus observer/execution metadata. When the envelope is compatible, ready, observer-visible, read-only, and not stale or cancelled, it creates one isolated dev-only DOM overlay representation inside a caller-provided root.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and reports that renderer ownership was not claimed. It removes any previous sandbox overlay before hydrating a new one, and `removeOverlay` clears the sandbox node without touching production overlay state.

It rejects stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist hydrated state, start workers, schedule background rendering, interpret astrology, or change backend runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_15_renderer_hydration_sandbox.py
```

The smoke verifies:

- sanitized hydration can become visible,
- production renderer ownership remains untouched,
- the sandbox overlay is isolated,
- no renderer ownership transfer occurs,
- hydration remains metadata-governed,
- stale and cancelled hydration do not display,
- raw payload fields are rejected,
- no persistent overlay state remains,
- no production overlay registry contamination occurs,
- overlay removal works cleanly,
- `rendererSubstrate` remains `legacy_search_regions`,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_renderer_hydration_sandbox.js`
- `scripts/smoke_phase2_15_renderer_hydration_sandbox.py`
- this narrative
- the tiny Phase 2.15 roadmap note

No production renderer logic, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga system, AI/intake path, interpretation system, persistence layer, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** sanitized metadata can produce one visible proof without becoming the renderer.
- **Deferred excellence:** real overlay orchestration, scheduler takeover, animation, production map hydration, workers, persistence, background rendering, UI redesign, and richer visual semantics remain future work.
- **Rejected scope:** production overlay ownership, raw GeoJSON hydration, Leaflet lifecycle integration, backend changes, aura/virga rendering, speculative hydration, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.15 checkpoint only if no unrelated files are staged.
