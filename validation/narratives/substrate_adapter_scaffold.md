# Substrate Adapter Scaffold Validation

Date: 2026-05-24

## Status

`substrate_adapter.js` is a production-loaded inert scaffold.

It is:

- not renderer integration,
- not a substrate flip,
- not cache/scheduler execution,
- not product UI,
- and not a user-facing readiness or interpretation surface.

The adapter exists as a contract-builder and ownership-boundary scaffold for future renderer-adjacent work. It does not promote that future work into production behavior.

## Production Contact

The backend serves the adapter at:

```text
/substrate_adapter.js
```

`map_CURRENT.html` loads that script and stores the global API from:

```text
window.RelocationSubstrateAdapter
```

The active production renderer substrate remains:

```text
legacy_search_regions
```

The adapter is therefore production-loaded, but the production rendering path still enters the legacy map flow and posts to `/search-regions`.

## What The Adapter Defines

- Viewport request shape: bounds, zoom, paint size, block size, and lat-cap policy.
- Classification request shape: birth payload, viewport, conditions, and optional request id.
- Cancellation scope: an `AbortController`-backed signal and explicit abort hook.
- Cache boundary shape: chart key, substrate id, viewport-derived keys, lat-cap flag, and condition set.
- Semantic cache-key payload construction and stable hashing.
- Refinement status shape: stage, sample count, cell count, stop reason, and convergence flag.
- Renderer-host ownership boundary: production host owns Leaflet state, visible layers, sidebar inputs, popup truth, render status, and debug panels; substrate/cache layers own classification, masks, refinement metrics, cancellation, priority, and budget accounting.

## Boundaries

The substrate adapter scaffold does not:

- fetch,
- call `/search-regions`,
- call `/screen-pixel-truth`,
- render,
- mutate DOM, map, or layers,
- hydrate production layers,
- change renderer substrate,
- warm cache entries,
- schedule background work,
- execute scheduler/cache logic,
- expose raw backend payloads,
- create recommendation/scoring/final-truth surfaces,
- introduce aura rendering,
- create product UI,
- or alter account/auth/persistence behavior.

## Why It Is Inert

`map_CURRENT.html` loads `/substrate_adapter.js` and stores `window.RelocationSubstrateAdapter` in `substrateAdapter`, but the production-host exposure is limited to contract builders and smoke-state metadata.

The default render path still uses:

```text
legacy_search_regions
```

The adapter can be called by tests or debug-only future scaffolds to construct metadata objects, but it does not perform side effects by itself.

## Smoke Validation

Run:

```bash
./venv/bin/python scripts/smoke_map_current.py
./venv/bin/python scripts/smoke_substrate_adapter.py
```

Pass criteria:

- production map smoke passes,
- substrate adapter smoke passes,
- `legacy_search_regions` remains active,
- adapter route serves,
- adapter loads in `map_CURRENT.html`,
- adapter contract builders work,
- semantic cache-key construction excludes transient/debug/rendered payload fields,
- adapter remains inert unless called,
- normal production render still calls `/search-regions`,
- normal production render does not call `/screen-pixel-truth`,
- no substrate flip occurs,
- no visible behavior changes,
- no production layer hydration occurs,
- no console errors occur.

## Rollback Scope

Rollback is limited to removing:

- `<script src="/substrate_adapter.js"></script>` and smoke-state exposure in `map_CURRENT.html`,
- the `/substrate_adapter.js` route in `main_centerline_FIXER.py`,
- `substrate_adapter.js`,
- `scripts/smoke_substrate_adapter.py`,
- and this narrative.

The default `legacy_search_regions` path remains recoverable because no persisted data, astrology math, renderer semantics, cache state, account/auth behavior, or production layer ownership depends on this scaffold.

## Governance Closeout

- **Accepted scope:** production-loaded inert contract scaffold.
- **Rejected scope:** renderer integration, substrate flip, cache/scheduler execution, product UI, aura rendering, recommendation/scoring/final-truth surfaces.
- **Next allowed step:** commit only after production smoke and substrate adapter smoke pass, with a narrow commit scope that excludes unrelated workspace files.
