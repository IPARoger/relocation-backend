# Phase 2.12 — Dev Runtime Bridge

## Purpose

Phase 2.12 adds a dev/smoke-only runtime bridge proving the committed Phase 2.3 through Phase 2.11 scaffold chain can survive in a browser context without production runtime wiring.

It remains metadata-only. It does not execute work, fetch network data, render, start workers, persist, mutate DOM/map state, hydrate renderer output, or take over the production renderer.

## Bridge Shape

`sampling_cache_runtime_bridge_dev.js` exposes `window.RelocationSamplingCacheRuntimeBridgeDev` with:

- `createDevRuntimeBridge`
- `evaluate`
- `seedCache`
- `inspect`

The bridge composes existing committed contracts:

- Phase 2.4 semantic cache key,
- Phase 2.6 in-memory cache store,
- Phase 2.7 orchestration envelope,
- Phase 2.9 lifecycle semantics,
- Phase 2.10 observer semantics,
- Phase 2.11 execution policy semantics.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_12_runtime_bridge_dev.py
```

The smoke verifies:

- bridge loads in a browser context,
- saved-investigation-like input flows through the contract chain,
- cache miss returns metadata-only `would run` envelope,
- seeded cache returns sanitized hydration envelope,
- stale work cannot hydrate visibly,
- observer state remains read-only,
- no fetch occurs,
- no DOM/map writes occur,
- `rendererSubstrate` remains `legacy_search_regions`,
- renderer/debug/aura/fetch/worker/output pollution is stripped.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_runtime_bridge_dev.js`
- `scripts/smoke_phase2_12_runtime_bridge_dev.py`
- this narrative
- the tiny Phase 2.12 roadmap note

No renderer runtime, backend, UI, account/auth, cache persistence, scheduler runtime, `phase2_cache_scheduler.js`, aura engine, truth-grid engine, worker, fetch, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** the scaffold chain is proven inside a browser context before any production wiring.
- **Deferred excellence:** real execution, fetches, workers, persistence, map integration, telemetry, UI, and visual observers remain future work.
- **Rejected scope:** renderer takeover, production feature flags, DOM/map writes, renderer output hydration, fake progress, backend storage, and account/auth work.
- **Next recommendation:** commit as a narrow Phase 2.12 dev bridge checkpoint if the smoke passes and no unrelated files are staged.
