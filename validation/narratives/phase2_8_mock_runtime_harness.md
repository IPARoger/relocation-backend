# Phase 2.8 — Mock Runtime Harness

## Purpose

Phase 2.8 proves the Phase 2.3 through Phase 2.7 contract chain coheres without production runtime wiring.

The harness composes saved-investigation-like input, Phase 2.4 semantic cache keys, the Phase 2.6 in-memory cache store, and Phase 2.7 orchestration envelopes. It is a semantic-flow proof only.

## What It Does

`sampling_cache_mock_runtime_harness.js` exposes `window.RelocationSamplingCacheMockRuntimeHarness` with:

- `createMockRuntimeHarness`
- `createSemanticRequest`
- `handleRequest`
- `seedCache`
- `simulateSameRequestScope`
- `simulatePreemption`
- `inspect`

The harness can:

- accept a saved-investigation-like request,
- generate a semantic cache key,
- check the in-memory store,
- return a sanitized hydration envelope on cache hit,
- return a Tier 0 job envelope on cache miss,
- simulate same-request zoom compatibility,
- simulate stale-job transitions and request preemption,
- expose sanitized inspection metadata.

## Explicit Non-Scope

The harness does not fetch, render, spawn workers, persist, call backend APIs, touch DOM/Leaflet/map state, hydrate renderer output, produce GeoJSON, produce pixels, create layers, implement aura/virga/raindrop behavior, or integrate with `map_CURRENT.html`.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_8_mock_runtime_harness.py
```

The smoke verifies:

- saved-investigation-like input becomes semantic cache key and orchestration request,
- cache miss creates Tier 0 work envelope,
- cache hit returns sanitized metadata hydration envelope,
- preemption stales incompatible work,
- same semantic request with compatible zoom remains compatible,
- chart, condition, and sampling changes invalidate compatibility,
- runtime pollution fields are stripped,
- no renderer output is hydrated,
- no fetch/worker/renderer/map/persistence fields appear.

The first smoke run caught two boundary issues: hydration needed to expose sanitized store metadata only, and the preemption assertion needed to match existing Tier 0/Tier >0 cancellation semantics.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_mock_runtime_harness.js`
- `scripts/smoke_phase2_8_mock_runtime_harness.py`
- this narrative
- the tiny Phase 2.8 roadmap note

No renderer runtime, backend, UI, account/auth, cache persistence, scheduler runtime, `phase2_cache_scheduler.js`, aura engine, truth-grid engine, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** the scaffold chain is proven coherently before runtime wiring.
- **Deferred excellence:** production wiring, real execution, fetches, workers, telemetry, persistence, map integration, and visual observers remain future work.
- **Rejected scope:** renderer output hydration, fake progress, UI/runtime coupling, aura/virga/raindrop implementation, backend storage, and account/auth work.
- **Next recommendation:** commit as a narrow Phase 2.8 mock harness checkpoint if the smoke passes and no unrelated files are staged.
