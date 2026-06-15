# Phase 2.13 — Dev Execution Runtime

## Purpose

Phase 2.13 creates the first minimal reversible execution runtime for one controlled semantic request lifecycle.

It remains dev/smoke-only and metadata-only. It does not call production fetch endpoints, render overlays, generate GeoJSON, hydrate renderer output, mutate map state, create workers, persist data, or execute speculative/background work.

## Runtime Shape

`sampling_cache_execution_runtime_dev.js` exposes `window.RelocationSamplingCacheExecutionRuntimeDev` with:

- `createExecutionRuntimeDev`
- `executeOnce`
- `inspect`

The runtime composes existing committed contracts:

- Phase 2.4 semantic cache key,
- Phase 2.6 in-memory cache store,
- Phase 2.7 orchestration envelope,
- Phase 2.9 lifecycle semantics,
- Phase 2.10 observer semantics,
- Phase 2.11 execution policy semantics.

## Behavior

The runtime accepts saved-investigation-like input, creates a semantic cache key, applies execution policy, creates lifecycle envelopes, simulates one queued-to-running-to-completed pass, writes sanitized metadata into the in-memory cache store, creates a sanitized hydration envelope, and exposes observer-safe metadata.

Only one request lifecycle is allowed at a time. The bridge remains reversible because it uses only local in-memory state and returns metadata envelopes.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_13_execution_runtime_dev.py
```

The smoke verifies:

- one semantic request executes successfully,
- lifecycle transitions are queued -> running -> completed,
- the cache store receives sanitized metadata only,
- the hydration envelope is sanitized,
- stale/cancelled requests cannot hydrate visibly,
- policy gates are respected,
- observer metadata remains read-only,
- no production fetch occurs,
- no renderer/map takeover occurs,
- `rendererSubstrate` remains `legacy_search_regions`,
- execution remains single-request and reversible.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_execution_runtime_dev.js`
- `scripts/smoke_phase2_13_execution_runtime_dev.py`
- this narrative
- the tiny Phase 2.13 roadmap note

No renderer runtime, backend, UI, account/auth, cache persistence, scheduler runtime, `phase2_cache_scheduler.js`, aura engine, truth-grid engine, worker, fetch, production feature flag, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** one controlled metadata-only lifecycle now proves the chain can execute without touching production renderer behavior.
- **Deferred excellence:** real fetches, workers, persistence, map integration, telemetry, UI, and visual observers remain future work.
- **Rejected scope:** renderer takeover, production fetch paths, background/speculative execution, renderer output hydration, GeoJSON/pixel/layer output, backend storage, and account/auth work.
- **Next recommendation:** commit as a narrow Phase 2.13 dev runtime checkpoint if the smoke passes and no unrelated files are staged.
