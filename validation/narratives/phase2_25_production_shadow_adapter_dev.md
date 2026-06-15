# Phase 2.25 — Production Shadow Adapter Dev

## Purpose

Phase 2.25 creates a debug-only production shadow adapter that evaluates production-adjacent candidate metadata through the Phase 2.24 production-readiness contract.

It does not create visible UI, alter default production behavior, flip renderer substrate, touch aura rendering, modify backend endpoint behavior, modify `truth_grid_engine.py`, change scheduler/cache execution, or connect to account/auth/persistence.

## Adapter Shape

`sampling_cache_production_shadow_adapter_dev.js` exposes:

- `createShadowProfile`
- `evaluateShadowCandidate`
- `inspectAdapter`

The adapter is standalone and classification-only. It creates sanitized readiness envelopes and passes them to `RelocationSamplingCacheProductionReadinessContract.classifyReadiness`.

## Production Boundary

The adapter must not:

- fetch,
- render,
- mutate DOM or map state,
- register production ownership,
- hydrate production layers,
- alter `legacy_search_regions`,
- expose raw backend payloads,
- make final truth claims,
- create recommendation, scoring, or interpretive surfaces.

The active production substrate remains `legacy_search_regions`.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_25_production_shadow_adapter_dev.py
```

The smoke verifies:

- adapter loads in isolation,
- a clean production-adjacent profile evaluates through the Phase 2.24 contract,
- a clean transitional candidate remains transitional,
- symbolic scoring fails,
- recommendation logic fails,
- raw payload exposure fails,
- observer control fails,
- renderer ownership mutation fails,
- stale hydration fails,
- adapter does not fetch,
- adapter does not mutate DOM/map,
- adapter does not change renderer substrate,
- adapter does not touch the production registry,
- output remains metadata-only and sanitized,
- `legacy_search_regions` remains the active production substrate,
- and no worker, renderer, persistence, or backend coupling occurs.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_production_shadow_adapter_dev.js`
- `scripts/smoke_phase2_25_production_shadow_adapter_dev.py`
- this narrative
- the tiny Phase 2.25 roadmap note

No production renderer logic, production overlay registry, map UI, `truth_grid_engine.py`, scheduler/cache execution, backend runtime, worker system, account/auth layer, aura rendering, persistence, recommendation engine, scoring engine, or Phase 2.25 visible product behavior is involved.

## Governance Closeout

- **Trust risk addressed:** production-adjacent metadata can now be dry-evaluated through the Phase 2.24 contract without touching production behavior.
- **Deferred excellence:** production integration, CI enforcement, telemetry, and any visible adapter UI remain future work.
- **Rejected scope:** renderer takeover, production registry mutation, DOM/map hooks, backend changes, scheduler changes, aura rendering, persistence, visible UI, and sandbox promotion.
