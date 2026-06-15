# Phase 2.20 — Ambiguity CandidateGroup Sandbox

## Purpose

Phase 2.20 creates a controlled, reversible, dev-only sandbox for ambiguity candidate_groups.

It proves adaptive refinement overlays can represent unresolved and overlapping candidate candidate_groups while preserving truth continuity, uncertainty integrity, deterministic supersession, viewport/namespace isolation, adaptive continuity, and renderer isolation.

The production renderer remains sovereign.

## Sandbox Shape

`sampling_cache_ambiguity_domain_sandbox.js` exposes `window.RelocationSamplingCacheAmbiguityCandidateGroupSandbox` with:

- `createAmbiguityCandidateGroupSandbox`
- `hydrateAmbiguity`
- `invalidateAmbiguity`
- `setViewportScope`
- `removeAll`
- `inspect`

The sandbox maintains an internal active viewport scope, isolated namespace/candidate_group records, and sanitized ambiguity lineage. It writes only disposable dev DOM nodes under a caller-provided root.

## Behavior

The sandbox preserves `rendererSubstrate = legacy_search_regions` and always reports that renderer ownership was not claimed. Ambiguity metadata is sanitized into candidate_group id, confidence, overlap, candidate ids, uncertainty generation, and status. Multiple ambiguity candidate_groups may coexist, including overlapping candidate candidate_groups. Newer uncertainty generations supersede older records deterministically while preserving lineage.

Unresolved ambiguity may remain visible safely. Ambiguity is not treated as error. Overlapping candidates are not treated as simultaneously confirmed truth. Unresolved structure is not treated as fake or invalid.

It rejects mismatched viewport scopes, stale hydration, cancelled hydration, non-visible observer states, non-ready metadata, older uncertainty generations, and envelopes containing raw or renderer-owned fields such as GeoJSON features, geometry, coordinates, renderer output, canvas pixels, Leaflet layers, debug/aura/virga fields, workers, fetch URLs, or generation-mode hints.

It does not call fetch, create map layers, use Leaflet, wire into `map_CURRENT.html`, mutate production overlay lifecycle, persist ambiguity state, start workers, schedule background rendering, synthesize truth, run real ambiguity visualization, interpret astrology, or change backend runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_20_ambiguity_domain_sandbox.py
```

The smoke verifies:

- ambiguity candidate_groups coexist deterministically,
- overlapping candidate candidate_groups preserve continuity,
- ambiguity supersession resolves correctly,
- unresolved ambiguity may remain visible safely,
- ambiguity invalidation cleans up correctly,
- stale and cancelled ambiguity refinements do not display,
- viewport isolation survives ambiguity candidate_groups,
- namespace isolation survives ambiguity candidate_groups,
- adaptive density continuity survives ambiguity transitions,
- production renderer remains untouched,
- no overlay registry contamination occurs,
- no DOM writes escape the sandbox root,
- `rendererSubstrate` remains `legacy_search_regions`,
- raw payload fields are rejected,
- ambiguity truth semantics remain honest,
- no fetch occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_ambiguity_domain_sandbox.js`
- `scripts/smoke_phase2_20_ambiguity_domain_sandbox.py`
- this narrative
- the tiny Phase 2.20 roadmap note

No production renderer logic, production overlay registry, production viewport synchronization path, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga system, AI/intake path, interpretation system, persistence layer, real ambiguity visualization engine, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** ambiguity can stay visible and structured without collapsing uncertainty into error or confirmed truth.
- **Deferred excellence:** aura/virga rendering, animation, speculative truth synthesis, AI interpretation, adaptive worker swarms, scheduler takeover, production overlay ownership, persistence, and real ambiguity visualization remain future work.
- **Rejected scope:** renderer takeover, real scheduler integration, production registry mutation, raw GeoJSON hydration, Leaflet lifecycle integration, backend changes, and AI/intake behavior.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.20 checkpoint only if no unrelated files are staged.
