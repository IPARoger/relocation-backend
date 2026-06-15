# Phase 2.24 — Production Readiness Boundary Contract

## Purpose

Phase 2.24 creates a controlled, reversible, dev-only boundary contract between experimental/transitional sandboxes and any future production integration.

It does not promote any sandbox into production.

The production renderer remains sovereign.

## Contract Shape

`sampling_cache_production_readiness_contract.js` exposes `window.RelocationSamplingCacheProductionReadinessContract` with:

- `classifyReadiness`
- `inspectContract`

The contract accepts a caller-supplied readiness profile and classifies it into one of:

- `not_ready`
- `sandbox_only`
- `transitional_candidate`
- `production_candidate`

`production_candidate` is only allowed when every hard gate passes.

## Hard Gates

The contract evaluates:

- layer sovereignty,
- runtime sovereignty,
- truth integrity,
- observer safety,
- cache/scheduler safety,
- terminology safety,
- validation requirements,
- and production path preservation.

These gates are classification boundaries only. They do not mutate runtime state, create UI, connect to a renderer, start workers, call fetch, persist data, or hydrate production overlays.

## Behavior

The contract rejects or marks not ready any profile that contains:

- Layer 2/3/4 interpretation inside Layer 1/runtime metadata,
- symbolic scoring,
- recommendation authority,
- best-location logic,
- hidden ontology,
- renderer ownership seizure,
- production registry mutation,
- raw backend payload exposure,
- unsafe hydration,
- final truth claims,
- observer lifecycle/scheduler/hydration/cache control,
- stale or cancelled work that can hydrate visibly,
- forbidden production-shaped vocabulary,
- missing smoke coverage,
- missing validation narrative,
- unclear rollback scope,
- or production path coupling.

Layer 4-style candidate language is only allowed when explicitly quarantined as non-runtime candidate vocabulary.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_24_production_readiness_contract.py
```

The smoke verifies:

- a clean profile can become `production_candidate` only when all hard gates pass,
- a clean profile can become `transitional_candidate` when all hard gates pass,
- symbolic scoring fails,
- recommendation logic fails,
- raw payload exposure fails,
- observer control fails,
- renderer ownership mutation fails,
- stale hydration fails,
- neutral runtime terminology passes,
- Layer 4 language is allowed only when quarantined,
- forbidden runtime vocabulary fails,
- the production path remains `legacy_search_regions`,
- no fetch, worker, DOM/map, renderer, persistence, or backend coupling occurs,
- accepted profiles do not echo raw payload fields,
- and the contract remains classification-only.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_production_readiness_contract.js`
- `scripts/smoke_phase2_24_production_readiness_contract.py`
- this narrative
- the tiny Phase 2.24 roadmap note

No production renderer logic, production overlay registry, production viewport synchronization path, `truth_grid_engine.py`, `phase2_cache_scheduler.js`, backend runtime, worker system, account/auth layer, aura/virga production system, AI/intake path, interpretation system, persistence layer, recommendation engine, scoring engine, unified astrology doctrine, or `map_CURRENT.html` hook is involved.

## Governance Closeout

- **Trust risk addressed:** production promotion now has an explicit boundary contract instead of relying on informal memory of sandbox constraints.
- **Deferred excellence:** actual production integration, promotion automation, CI enforcement, UI exposure, scheduler integration, renderer ownership decisions, and production telemetry remain future work.
- **Rejected scope:** renderer takeover, production registry mutation, map hooks, backend changes, scheduler changes, persistence, visible UI, and sandbox promotion.
- **Next recommendation:** run the smoke, inspect scoped status, then commit as a narrow Phase 2.24 checkpoint only if no unrelated files are staged.
