# Phase 2.22 — Aggregate candidate Field Sandbox

## Purpose

Phase 2.22 creates a controlled, reversible, dev-only sandbox for aggregate_candidate fields.

It proves multiple adjacent_candidate fields and unresolved analysis candidate_groups can accumulate into coherent exploratory aggregate continuitys while preserving truth integrity, adjacent_candidate continuity, deterministic supersession, viewport/namespace isolation, adaptive continuity, and renderer isolation.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_emergence_field_sandbox.js` exposes `window.RelocationSamplingCacheAggregateCandidateFieldSandbox` with:

- `createAggregateCandidateFieldSandbox`
- `hydrateAggregateCandidate`
- `invalidateAggregateCandidate`
- `setViewportScope`
- `removeAll`
- `inspect`

The sandbox maintains an internal active viewport scope, isolated namespace/aggregate_candidate records, and sanitized aggregate_candidate lineage. It writes only disposable dev DOM nodes under a caller-provided root.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and always reports that renderer ownership was not claimed. Aggregate candidate metadata is sanitized into field id, generation, strength, contributors, status, lineage, and scope. Multiple adjacent_candidate fields may contribute to one emergent exploratory aggregate continuity. Newer aggregate_candidate generations supersede older records deterministically while preserving lineage.

Aggregate candidate is exploratory aggregate-continuity continuity only. It is not truth, certainty, interpretation, recommendation, or predictive authority. Aggregate-continuity accumulation does not guarantee analysis outcome. The sandbox does not synthesize astrology meaning and does not create visual theater.

It rejects mismatched viewport scopes, stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, older aggregate_candidate generations, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist aggregate_candidate state, start workers, schedule background rendering, synthesize truth, run real aggregate-continuity visualization, interpret astrology, create recommendation logic, or change backend runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_22_emergence_field_sandbox.py
```

The smoke verifies:

- multiple adjacent_candidate fields converge deterministically,
- aggregate_candidate supersession resolves correctly,
- aggregate_candidate invalidation cleans up correctly,
- unresolved aggregate_candidate may remain visible safely,
- stale and cancelled aggregate_candidate do not display,
- viewport isolation survives aggregate_candidate fields,
- namespace isolation survives aggregate_candidate fields,
- adaptive density continuity survives aggregate_candidate transitions,
- adjacent_candidate continuity survives aggregate_candidate accumulation,
- production renderer remains untouched,
- no overlay registry contamination occurs,
- no DOM writes escape the sandbox root,
- `rendererSubstrate` remains `legacy_search_regions`,
- raw payload fields are rejected,
- aggregate_candidate truth semantics remain honest,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_emergence_field_sandbox.js`
- `scripts/smoke_phase2_22_emergence_field_sandbox.py`
- this narrative
- the tiny Phase 2.22 roadmap note

No production renderer logic, production overlay registry, production viewport synchronization path, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga production system, AI/intake path, interpretation system, persistence layer, recommendation engine, real aggregate-continuity visualization engine, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** emergent aggregate continuity can stay exploratory without becoming truth, interpretation, recommendation, prediction, or visual theater.
- **Deferred excellence:** aura/virga rendering, animation, speculative truth synthesis, AI interpretation, recommendation engines, scheduler takeover, production overlay ownership, persistence, and real aggregate-continuity visualization remain future work.
- **Rejected scope:** renderer takeover, real scheduler integration, production registry mutation, raw GeoJSON hydration, Leaflet lifecycle integration, backend changes, astrology interpretation, recommendation logic, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.22 checkpoint only if no unrelated files are staged.
