# Phase 2.23 — Cross-CandidateGroup Continuity Sandbox

## Purpose

Phase 2.23 creates a controlled, reversible, dev-only sandbox for cross-candidate_group analysis continuity.

It proves multiple analysis exploration candidate_groups can coexist, reference one another, and preserve structural continuity across adjacent_candidate and aggregate_candidate records without collapsing into unified interpretation, recommendation, scoring, or truth inflation.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_cross_domain_continuity_sandbox.js` exposes `window.RelocationSamplingCacheCrossCandidateGroupContinuitySandbox` with:

- `createCrossCandidateGroupContinuitySandbox`
- `hydrateCandidateGroup`
- `invalidateCandidateGroup`
- `setViewportScope`
- `removeAll`
- `inspect`

The sandbox maintains an internal active viewport scope, isolated namespace/candidate_group records, and sanitized candidate_group lineage. It writes only disposable dev DOM nodes under a caller-provided root.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and always reports that renderer ownership was not claimed. Cross-candidate_group metadata is sanitized into candidate_group id, generation, lineage, contributing candidate_groups, continuity status, and coexistence scope. Multiple analysis candidate_groups may coexist, and cross-candidate_group records may reference adjacent_candidate and aggregate_candidate continuity.

Cross-candidate_group continuity is structural coexistence only. It is not interpretation, recommendation, analysis scoring, best-location logic, validation, or unified astrology doctrine.

It rejects mismatched viewport scopes, stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, older candidate_group generations, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist candidate_group state, start workers, schedule background rendering, synthesize unified astrology meaning, score analysis candidate_groups, create recommendation logic, or change backend runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_23_cross_domain_continuity_sandbox.py
```

The smoke verifies:

- multiple candidate_groups coexist deterministically,
- cross-candidate_group continuity persists safely,
- cross-candidate_group adjacent_candidate continuity survives,
- cross-candidate_group aggregate_candidate continuity survives,
- invalidation cleans up correctly,
- stale and cancelled candidate_groups do not display,
- viewport isolation survives cross-candidate_group coexistence,
- namespace isolation survives cross-candidate_group coexistence,
- adaptive continuity survives cross-candidate_group interaction,
- production renderer remains untouched,
- no overlay registry contamination occurs,
- no DOM writes escape the sandbox root,
- `rendererSubstrate` remains `legacy_search_regions`,
- raw payload fields are rejected,
- cross-candidate_group truth semantics remain honest,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_cross_domain_continuity_sandbox.js`
- `scripts/smoke_phase2_23_cross_domain_continuity_sandbox.py`
- this narrative
- the tiny Phase 2.23 roadmap note

No production renderer logic, production overlay registry, production viewport synchronization path, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga production system, AI/intake path, interpretation system, persistence layer, recommendation engine, analysis scoring engine, unified astrology doctrine, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** analysis candidate_groups can coexist structurally without merging into interpretation, recommendation, validation, scoring, or truth.
- **Deferred excellence:** AI interpretation, recommendation systems, analysis scoring, aura/virga rendering, animation, scheduler takeover, production overlay ownership, persistence, and unified doctrine remain future work.
- **Rejected scope:** renderer takeover, real scheduler integration, production registry mutation, raw GeoJSON hydration, Leaflet lifecycle integration, backend changes, astrology interpretation, recommendation logic, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.23 checkpoint only if no unrelated files are staged.
