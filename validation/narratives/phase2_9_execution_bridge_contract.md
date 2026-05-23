# Phase 2.9 — Mock Execution Bridge Contract

## Purpose

Phase 2.9 defines deterministic execution lifecycle semantics for orchestration jobs without performing real execution.

It accepts Phase 2.7/2.8-shaped orchestration job envelopes and simulates state transitions only.

## Contract Shape

`sampling_cache_execution_bridge_contract.js` exposes `window.RelocationSamplingCacheExecutionBridgeContract` with:

- `createExecutionEnvelope`
- `transitionExecution`
- `canTransition`
- `applyLogicalPreemption`
- `propagateStale`
- `canHydrate`

Supported states:

- `queued`
- `running`
- `completed`
- `cancelled`
- `stale`
- `error`

## Scope

The bridge preserves Tier 0 foreground ownership, supports logical preemption, propagates stale state, produces sanitized execution-state envelopes, exposes observer-safe read-only progress metadata, and answers conceptual hydration eligibility.

It does not execute jobs. It does not fetch, render, spawn workers, use promises/timing loops, persist, touch DOM/Leaflet/map state, hydrate renderer output, or integrate with `map_CURRENT.html`.

## Hydration Eligibility

Only completed, compatible, non-stale, non-cancelled execution envelopes may hydrate conceptually. Stale, cancelled, running, queued, and error states cannot hydrate.

This is a lifecycle semantics check only. It does not store or hydrate renderer results.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_9_execution_bridge_contract.py
```

The smoke verifies:

- valid lifecycle transitions,
- invalid transition rejection,
- Tier 0 ownership preservation,
- preemption marks lower-priority incompatible jobs stale/cancelled,
- stale jobs cannot hydrate,
- completed compatible jobs may hydrate conceptually,
- observer metadata is sanitized and read-only,
- renderer/debug/aura/fetch/worker fields are stripped,
- no runtime/map/persistence coupling exists.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_execution_bridge_contract.js`
- `scripts/smoke_phase2_9_execution_bridge_contract.py`
- this narrative
- the tiny Phase 2.9 roadmap note

No renderer runtime, backend, UI, account/auth, cache persistence, scheduler runtime, `phase2_cache_scheduler.js`, aura engine, truth-grid engine, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** execution lifecycle semantics are defined before real runtime wiring.
- **Deferred excellence:** real execution, real cancellation, fetches, workers, telemetry, persistence, map integration, and visual observers remain future work.
- **Rejected scope:** renderer output hydration, runtime rendering, worker orchestration, backend storage, UI integration, aura/virga/raindrop implementation, and account/auth work.
- **Next recommendation:** commit as a narrow Phase 2.9 execution bridge checkpoint if the smoke passes and no unrelated files are staged.
