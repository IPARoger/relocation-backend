# Phase 2.21 — Adjacent candidate Field Sandbox

## Purpose

Phase 2.21 creates a controlled, reversible, dev-only sandbox for adjacent_candidate fields.

It proves ambiguity and adaptive refinement candidate_groups can imply nearby unresolved analysis structure while preserving truth integrity, adjacent_candidate honesty, deterministic supersession, viewport/namespace isolation, adaptive continuity, and renderer isolation.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_implication_field_sandbox.js` exposes `window.RelocationSamplingCacheAdjacentCandidateFieldSandbox` with:

- `createAdjacentCandidateFieldSandbox`
- `hydrateAdjacentCandidate`
- `invalidateAdjacentCandidate`
- `setViewportScope`
- `removeAll`
- `inspect`

The sandbox maintains an internal active viewport scope, isolated namespace/adjacent_candidate records, and sanitized adjacent_candidate lineage. It writes only disposable dev DOM nodes under a caller-provided root.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and always reports that renderer ownership was not claimed. Adjacent candidate metadata is sanitized into field id, direction, weight, source ambiguity candidate_group, generation, and status. Multiple adjacent_candidate fields may coexist. Newer adjacent_candidate generations supersede older records deterministically while preserving lineage.

Unresolved adjacent_candidate may remain visible safely. Adjacent candidate is not confirmed truth. Directional continuity does not claim an analysis outcome. The sandbox preserves ontology boundaries and does not synthesize speculative astrology meaning.

It rejects mismatched viewport scopes, stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, older adjacent_candidate generations, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist adjacent_candidate state, start workers, schedule background rendering, synthesize truth, run real adjacent_candidate visualization, interpret astrology, or change backend runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_21_implication_field_sandbox.py
```

The smoke verifies:

- adjacent_candidate fields coexist deterministically,
- ambiguity candidate_groups can imply nearby structure safely,
- adjacent_candidate supersession resolves correctly,
- adjacent_candidate invalidation cleans up correctly,
- unresolved adjacent_candidates may remain visible safely,
- stale and cancelled adjacent_candidates do not display,
- viewport isolation survives adjacent_candidate fields,
- namespace isolation survives adjacent_candidate fields,
- adaptive density continuity survives adjacent_candidate transitions,
- production renderer remains untouched,
- no overlay registry contamination occurs,
- no DOM writes escape the sandbox root,
- `rendererSubstrate` remains `legacy_search_regions`,
- raw payload fields are rejected,
- adjacent_candidate truth semantics remain honest,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_implication_field_sandbox.js`
- `scripts/smoke_phase2_21_implication_field_sandbox.py`
- this narrative
- the tiny Phase 2.21 roadmap note

No production renderer logic, production overlay registry, production viewport synchronization path, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga system, AI/intake path, interpretation system, persistence layer, real adjacent_candidate visualization engine, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** adjacent_candidate can stay visible and directional without becoming confirmed truth or interpretation.
- **Deferred excellence:** aura/virga rendering, animation, speculative truth synthesis, AI interpretation, adaptive worker swarms, scheduler takeover, production overlay ownership, persistence, and real adjacent_candidate visualization remain future work.
- **Rejected scope:** renderer takeover, real scheduler integration, production registry mutation, raw GeoJSON hydration, Leaflet lifecycle integration, backend changes, astrology interpretation, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.21 checkpoint only if no unrelated files are staged.
