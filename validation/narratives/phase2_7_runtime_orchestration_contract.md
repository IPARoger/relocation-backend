# Phase 2.7 — Runtime Orchestration Contract

## Purpose

Phase 2.7 defines contract-only runtime orchestration semantics for how saved investigations, semantic cache keys, scheduler descriptors, and in-memory cache entries will eventually interact.

It does not execute runtime work. It does not fetch, render, spawn workers, persist, touch DOM/Leaflet/map state, or wire into `map_CURRENT.html`.

## Contract Shape

`sampling_cache_orchestration_contract.js` exposes `window.RelocationSamplingCacheOrchestrationContract` with:

- `createOrchestrationRequest`
- `createJobEnvelope`
- `classifyJobCompatibility`
- `applyRuntimePreemption`
- `markStaleJobs`
- `createHydrationEnvelope`

## Foreground / Background Rules

Foreground belongs to the active user request. Tier 0 always wins. Lower-tier jobs are speculative and may be cancelled or marked stale when the user changes chart, conditions, viewport/sampling scope, or ambiguity domain.

Same-request zoom and pan-adjacent scopes may remain compatible only when their semantic cache key, intent group, and generation still match the active request.

## Hydration Envelope Meaning

A hydration envelope means sanitized scaffold metadata says a compatible cache/store entry is available. It does not include renderer output, truth results, GeoJSON, pixels, layers, fetch responses, worker state, or visual artifacts.

Hydration metadata may indicate `hydrated: true` and `execution_required: false`, but it does not execute cache hydration or render anything.

## Future Visual Observers

Future raindrop, virga, and aura layers may observe read-only progress metadata such as queued/running/completed status. They must not control scheduler priority, fabricate progress, alter truth, force hydration, or make background work block foreground.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_7_orchestration_contract.py
```

The smoke verifies:

- foreground requests create Tier 0 envelopes,
- cache hits create sanitized metadata hydration envelopes without execution work,
- cache misses create job envelopes,
- new user requests preempt and stale lower-tier jobs,
- same-request zoom/pan scopes remain compatible only when semantic key assumptions match,
- condition/chart/sampling changes mark old jobs stale,
- hydration strips renderer/debug/aura/fetch/worker fields,
- observer progress metadata is read-only and cannot control scheduler priority,
- no fetch/worker/DOM/map/renderer/persistence fields appear.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_orchestration_contract.js`
- `scripts/smoke_phase2_7_orchestration_contract.py`
- this narrative
- the tiny Phase 2.7 roadmap note

No renderer runtime, backend, UI, account/auth, cache persistence, scheduler runtime, `phase2_cache_scheduler.js`, aura engine, truth-grid engine, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** orchestration semantics are defined before runtime wiring, reducing stale job, cache pollution, and foreground/background ownership risk.
- **Deferred excellence:** real execution, cancellation of actual work, telemetry, workers, persistent cache, visual progress observers, and map integration remain future work.
- **Rejected scope:** runtime rendering, fetch execution, worker orchestration, DOM/map coupling, renderer/debug/aura fields, and hydration of renderer results.
- **Next recommendation:** commit this as a narrow Phase 2.7 contract checkpoint if the smoke passes and no unrelated files are staged.
