# Phase 2.18 — Progressive Refinement Hydration Sandbox

## Purpose

Phase 2.18 creates a controlled, reversible, dev-only sandbox for progressive hydration refinement.

It proves coarse overlays can refine into newer overlays while preserving semantic continuity, deterministic supersession, lineage tracking, cleanup guarantees, viewport/namespace isolation, and truth-boundary honesty without transferring renderer ownership, mutating production overlay registries, persisting state, or exposing raw backend payloads.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_progressive_refinement_sandbox.js` exposes `window.RelocationSamplingCacheProgressiveRefinementSandbox` with:

- `createProgressiveRefinementSandbox`
- `hydrateRefinement`
- `invalidateRefinement`
- `setViewportScope`
- `removeAll`
- `inspect`

The sandbox maintains an internal active viewport scope, isolated namespace records, and sanitized lineage metadata. It writes only disposable dev DOM nodes under a caller-provided root. Each namespace/viewport pair has one visible current overlay; newer accepted refinements supersede older overlays and remove superseded DOM immediately.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and always reports that renderer ownership was not claimed. A coarse overlay can be followed by a refined overlay in the same namespace and viewport. The refined overlay records lineage, parent linkage, generation, superseded overlay id, and provisional truth status. Older generations are rejected after newer refinements are visible.

It rejects mismatched viewport scopes, stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, older refinement generations, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist refinement state, start workers, schedule background rendering, run adaptive sampling, synchronize production viewport state, interpret astrology, or change backend runtime behavior.

Incomplete refinement is never marked as final truth.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_18_progressive_refinement_sandbox.py
```

The smoke verifies:

- coarse overlays can refine into newer overlays,
- refinement supersession is deterministic,
- superseded overlays clean up correctly,
- refinement lineage remains coherent,
- stale and cancelled refinements do not display,
- viewport isolation survives refinement,
- namespace isolation survives refinement,
- progressive hydration preserves truth continuity,
- production renderer remains untouched,
- no overlay registry contamination occurs,
- no DOM writes escape the sandbox root,
- `rendererSubstrate` remains `legacy_search_regions`,
- raw payload fields are rejected,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_progressive_refinement_sandbox.js`
- `scripts/smoke_phase2_18_progressive_refinement_sandbox.py`
- this narrative
- the tiny Phase 2.18 roadmap note

No production renderer logic, production overlay registry, production viewport synchronization path, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga system, AI/intake path, interpretation system, persistence layer, adaptive sampling engine, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** progressive refinement can supersede coarse hydrated proofs without pretending provisional refinement is final truth.
- **Deferred excellence:** animation, aura/virga rendering, adaptive sampling, live scheduler integration, workers, background rendering, production overlay ownership, persistence, and live viewport orchestration remain future work.
- **Rejected scope:** renderer takeover, real scheduler integration, production registry mutation, raw GeoJSON hydration, Leaflet lifecycle integration, speculative refinement, backend changes, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.18 checkpoint only if no unrelated files are staged.
