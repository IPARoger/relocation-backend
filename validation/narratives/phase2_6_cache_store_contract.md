# Phase 2.6 — In-Memory Cache Store Contract

## Purpose

Phase 2.6 adds a narrow local/in-memory cache store contract scaffold between the Phase 2.4 semantic cache key and Phase 2.5 scheduler descriptors.

It does not render, fetch, persist, spawn workers, wire into `map_CURRENT.html`, or introduce backend/database/account storage.

## Contract Shape

`sampling_cache_store_contract.js` exposes `window.RelocationSamplingCacheStoreContract` with:

- `createMemoryCacheStore(options)`
- `store.get(key)`
- `store.set(entry)`
- `store.has(key)`
- `store.invalidate(keyOrPredicate)`
- `store.inspect()`
- `store.clear()`

The default TTL is explicit: 5 minutes.

## Stored Fields

Entries retain only:

- `schema_version`
- `key`
- sanitized `payload`
- sanitized `value`
- `created_at_ms`
- `updated_at_ms`
- `expires_at_ms`

Payloads retain only:

- `schema_version`
- `chart_key`
- `investigation`
- `viewport`
- `sampling`

Values retain only:

- `status`
- `summary`
- `metrics`
- `error` when it is a string

## Explicitly Rejected Fields

The store strips renderer output, GeoJSON, canvas pixels, Leaflet layers, `generation_mode`, renderer substrate, debug flags, aura/raster/adaptive flags, fetch URLs/responses, worker IDs, backend/database IDs, account/user IDs, request IDs, and cache hit/miss counters.

## Scaffold Behavior

Expired `get` returns `null`, expired `has` returns `false`, and expired entries are removed lazily. `invalidate(key)` removes one entry. `invalidate(predicate)` is supported for semantic cleanup but does not imply runtime scheduler execution. `inspect()` returns sanitized summaries only.

There is no persistence across page/process lifetime. There is no `localStorage`, IndexedDB, filesystem, backend, database, worker, fetch, UI, or map integration.

## Conceptual Boundary

`sampling_cache_contract.js` creates canonical semantic keys and payloads. `sampling_cache_scheduler_contract.js` creates descriptors that may reference cache keys. This Phase 2.6 store accepts those keys and sanitized semantic payloads without executing scheduler work.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_6_cache_store_contract.py
```

The smoke verifies:

- set/get returns sanitized entries,
- `has` is true before expiration,
- expired entries are not returned,
- `invalidate` removes one entry,
- `clear` removes all entries,
- renderer/debug/aura/transient pollution is stripped,
- different semantic keys remain distinct,
- store entries work with `sampling_cache_contract.js` output,
- descriptor-shaped `cache_key` input is accepted without scheduler execution.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_store_contract.js`
- `scripts/smoke_phase2_6_cache_store_contract.py`
- this narrative
- the tiny Phase 2.6 roadmap note

No renderer runtime, backend, UI, account/auth, cache persistence, scheduler runtime, `phase2_cache_scheduler.js`, `substrate_adapter.js`, aura engine, truth-grid engine, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** cache storage now has a sanitation boundary before any future runtime wiring.
- **Deferred excellence:** persistent cache storage, account-scoped cache ownership, scheduler execution, telemetry tuning, and invalidation policy remain future work.
- **Rejected scope:** renderer output storage, fetch/worker execution, backend persistence, UI integration, aura/raindrop/virga behavior, and account/user data.
- **Next recommendation:** commit as a narrow Phase 2.6 scaffold only if the smoke passes and no unrelated files are staged.
