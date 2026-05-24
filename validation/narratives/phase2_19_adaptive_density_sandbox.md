# Phase 2.19 — Adaptive Refinement Density Sandbox

## Purpose

Phase 2.19 creates a controlled, reversible, dev-only sandbox for adaptive refinement density.

It proves progressive refinement can prioritize density according to sanitized semantic importance, boundary pressure, interior stability, and budget metadata while preserving truth continuity, deterministic supersession, viewport/namespace isolation, and renderer isolation.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_adaptive_density_sandbox.js` exposes `window.RelocationSamplingCacheAdaptiveDensitySandbox` with:

- `createAdaptiveDensitySandbox`
- `hydrateAdaptive`
- `planAdaptiveBatch`
- `setViewportScope`
- `removeAll`
- `inspect`

The sandbox maintains an internal active viewport scope, isolated namespace records, and a transient in-memory pending list for budget-deferred candidates. It writes only disposable dev DOM nodes under a caller-provided root.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and always reports that renderer ownership was not claimed. Adaptive metadata is sanitized into refinement density, pressure, boundary priority, interior stability, budget, generation, and a deterministic priority score. Batch planning selects candidates by score within a refinement budget and defers lower-priority candidates.

Edge-priority and high-pressure regions can supersede prior overlays deterministically. Sparse stable interiors may be deferred without implying they are incomplete truth. High-density regions are more actively refined, not more true. Every returned envelope keeps `density_affects_activity_not_truth = true` and `truth_final = false`.

It rejects mismatched viewport scopes, stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, older adaptive generations, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist adaptive state, start workers, schedule background rendering, run real adaptive sampling, interpret astrology, or change backend runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_19_adaptive_density_sandbox.py
```

The smoke verifies:

- adaptive density overlays refine deterministically,
- edge-priority regions supersede correctly,
- sparse interiors remain stable,
- refinement continuity survives density changes,
- refinement budgets constrain adaptive growth,
- stale and cancelled adaptive refinements do not display,
- viewport isolation survives adaptive refinement,
- namespace isolation survives adaptive refinement,
- production renderer remains untouched,
- no overlay registry contamination occurs,
- no DOM writes escape the sandbox root,
- `rendererSubstrate` remains `legacy_search_regions`,
- raw payload fields are rejected,
- density semantics remain truth-honest,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_adaptive_density_sandbox.js`
- `scripts/smoke_phase2_19_adaptive_density_sandbox.py`
- this narrative
- the tiny Phase 2.19 roadmap note

No production renderer logic, production overlay registry, production viewport synchronization path, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga system, AI/intake path, interpretation system, persistence layer, real adaptive sampling engine, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** adaptive refinement can prioritize effort without implying density equals truth.
- **Deferred excellence:** aura/virga rendering, animation, real adaptive sampling, worker execution, scheduler takeover, speculative refinement, production overlay ownership, persistence, and AI interpretation remain future work.
- **Rejected scope:** renderer takeover, real scheduler integration, production registry mutation, raw GeoJSON hydration, Leaflet lifecycle integration, adaptive worker swarms, backend changes, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.19 checkpoint only if no unrelated files are staged.
