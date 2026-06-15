# Phase 2.16 — Multi-Overlay Coexistence Sandbox

## Purpose

Phase 2.16 creates a controlled, reversible, dev-only sandbox for multiple isolated hydration overlays.

It proves sanitized runtime metadata can create, update, replace, invalidate, and remove multiple sandbox overlays without transferring renderer ownership, mutating production overlay registries, persisting state, or exposing raw backend payloads.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_multi_overlay_sandbox.js` exposes `window.RelocationSamplingCacheMultiOverlaySandbox` with:

- `createMultiOverlaySandbox`
- `hydrateOverlay`
- `replaceOverlay`
- `invalidateOverlay`
- `removeOverlay`
- `removeAll`
- `inspect`

The sandbox maintains its own isolated namespace map and writes only disposable dev DOM nodes under a caller-provided root. It preserves deterministic hydration order by first accepted namespace creation and keeps replacements scoped to that namespace.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and always reports that renderer ownership was not claimed. Multiple overlays may coexist if they are sanitized, ready, observer-visible, read-only, compatible hydration envelopes. Updating the same namespace replaces metadata in place. Replacement removes prior namespace state before rehydrating. Invalidation and removal delete only sandbox-owned nodes.

It rejects stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist hydrated state, start workers, schedule background rendering, synchronize viewports, interpret astrology, or change backend runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_16_multi_overlay_sandbox.py
```

The smoke verifies:

- multiple overlays can coexist safely,
- overlay namespaces remain isolated,
- stale overlays invalidate correctly,
- replacement overlays supersede correctly,
- cleanup/removal works fully,
- hydration ordering remains deterministic,
- cancelled overlays do not display,
- production renderer remains untouched,
- no overlay registry contamination occurs,
- no DOM writes escape the sandbox root,
- `rendererSubstrate` remains `legacy_search_regions`,
- raw payload fields are rejected,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_multi_overlay_sandbox.js`
- `scripts/smoke_phase2_16_multi_overlay_sandbox.py`
- this narrative
- the tiny Phase 2.16 roadmap note

No production renderer logic, production overlay registry, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga system, AI/intake path, interpretation system, persistence layer, viewport synchronization path, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** multiple hydrated visual proofs can coexist without becoming production overlay orchestration.
- **Deferred excellence:** production overlay ownership, animation, scheduler takeover, workers, background rendering, persistence, viewport sync, and richer map integration remain future work.
- **Rejected scope:** renderer takeover, real scheduler integration, production registry mutation, raw GeoJSON hydration, Leaflet lifecycle integration, aura/virga rendering, speculative rendering, backend changes, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.16 checkpoint only if no unrelated files are staged.
