# Phase 2.14 — Isolated Fetch Bridge

## Purpose

Phase 2.14 creates the smallest reversible bridge between the semantic runtime spine and one real backend fetch path.

It remains dev/smoke-only and single-request. It calls the existing `/search-regions` endpoint, sanitizes the backend response into metadata-only cache/hydration envelopes, and never exposes raw backend payloads to observers.

## Bridge Shape

`sampling_cache_fetch_bridge_dev.js` exposes `window.RelocationSamplingCacheFetchBridgeDev` with:

- `createFetchBridgeDev`
- `executeOnce`
- `inspect`

The bridge composes existing committed contracts:

- Phase 2.4 semantic cache key,
- Phase 2.6 in-memory cache store,
- Phase 2.7 orchestration envelope,
- Phase 2.9 lifecycle semantics,
- Phase 2.10 observer semantics,
- Phase 2.11 execution policy semantics.

## Behavior

The bridge accepts saved-investigation-like input, creates a semantic cache key, applies execution policy, creates lifecycle envelopes, performs one POST to `/search-regions`, sanitizes the response to metadata, writes sanitized metadata into the in-memory cache store, creates a sanitized hydration envelope, and exposes observer-safe metadata.

It does not hydrate renderer overlays, create Leaflet layers, mutate map state, persist responses, execute speculative work, run concurrent requests, create workers, expose raw GeoJSON/features/coordinates to observers, or change production runtime behavior.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_14_fetch_bridge_dev.py
```

The smoke verifies:

- one real backend fetch executes successfully,
- semantic request survives the full runtime chain,
- lifecycle transitions occur correctly,
- backend response is sanitized,
- metadata-only hydration occurs,
- cache store contains sanitized metadata only,
- stale/cancelled requests cannot hydrate visibly,
- observer metadata remains read-only,
- no map/DOM writes occur,
- `rendererSubstrate` remains `legacy_search_regions`,
- execution remains single-request and reversible.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_fetch_bridge_dev.js`
- `scripts/smoke_phase2_14_fetch_bridge_dev.py`
- this narrative
- the tiny Phase 2.14 roadmap note

No renderer runtime, backend, UI, account/auth, cache persistence, scheduler runtime, `phase2_cache_scheduler.js`, aura engine, truth-grid engine, worker system, production fetch path, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** one backend fetch can enter the semantic spine without exposing raw renderer payloads or taking over production behavior.
- **Deferred excellence:** production runtime integration, workers, cancellation of real requests, persistence, map integration, UI, telemetry, and visual observers remain future work.
- **Rejected scope:** renderer takeover, raw GeoJSON hydration, Leaflet layer creation, map mutation, speculative/background execution, backend changes, and account/auth work.
- **Next recommendation:** commit as a narrow Phase 2.14 fetch bridge checkpoint if the smoke passes and no unrelated files are staged.
