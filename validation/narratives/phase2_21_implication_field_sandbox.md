# Phase 2.21 — Implication Field Sandbox

## Purpose

Phase 2.21 creates a controlled, reversible, dev-only sandbox for implication fields.

It proves ambiguity and adaptive refinement domains can imply nearby unresolved symbolic structure while preserving truth integrity, implication honesty, deterministic supersession, viewport/namespace isolation, adaptive continuity, and renderer isolation.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_implication_field_sandbox.js` exposes `window.RelocationSamplingCacheImplicationFieldSandbox` with:

- `createImplicationFieldSandbox`
- `hydrateImplication`
- `invalidateImplication`
- `setViewportScope`
- `removeAll`
- `inspect`

The sandbox maintains an internal active viewport scope, isolated namespace/implication records, and sanitized implication lineage. It writes only disposable dev DOM nodes under a caller-provided root.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and always reports that renderer ownership was not claimed. Implication metadata is sanitized into field id, direction, strength, source ambiguity domain, generation, and status. Multiple implication fields may coexist. Newer implication generations supersede older records deterministically while preserving lineage.

Unresolved implication may remain visible safely. Implication is not confirmed truth. Directional attraction does not guarantee symbolic outcome. The sandbox does not synthesize speculative astrology meaning.

It rejects mismatched viewport scopes, stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, older implication generations, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist implication state, start workers, schedule background rendering, synthesize truth, run real implication visualization, interpret astrology, or change backend runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_21_implication_field_sandbox.py
```

The smoke verifies:

- implication fields coexist deterministically,
- ambiguity domains can imply nearby structure safely,
- implication supersession resolves correctly,
- implication invalidation cleans up correctly,
- unresolved implications may remain visible safely,
- stale and cancelled implications do not display,
- viewport isolation survives implication fields,
- namespace isolation survives implication fields,
- adaptive density continuity survives implication transitions,
- production renderer remains untouched,
- no overlay registry contamination occurs,
- no DOM writes escape the sandbox root,
- `rendererSubstrate` remains `legacy_search_regions`,
- raw payload fields are rejected,
- implication truth semantics remain honest,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_implication_field_sandbox.js`
- `scripts/smoke_phase2_21_implication_field_sandbox.py`
- this narrative
- the tiny Phase 2.21 roadmap note

No production renderer logic, production overlay registry, production viewport synchronization path, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga system, AI/intake path, interpretation system, persistence layer, real implication visualization engine, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** implication can stay visible and directional without becoming confirmed truth or interpretation.
- **Deferred excellence:** aura/virga rendering, animation, speculative truth synthesis, AI interpretation, adaptive worker swarms, scheduler takeover, production overlay ownership, persistence, and real implication visualization remain future work.
- **Rejected scope:** renderer takeover, real scheduler integration, production registry mutation, raw GeoJSON hydration, Leaflet lifecycle integration, backend changes, astrology interpretation, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.21 checkpoint only if no unrelated files are staged.
