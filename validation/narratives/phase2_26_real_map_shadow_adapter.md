# Phase 2.26 — Real Map Shadow Adapter Smoke

## Purpose

Phase 2.26 proves that the real production map page can be evaluated by the Phase 2.25 production shadow adapter and Phase 2.24 readiness contract from the test context only.

This is smoke-only. It is not visible integration.

## Boundary

The smoke loads the default `map_CURRENT.html` page and does not modify the page source.

The Phase 2.24 contract and Phase 2.25 adapter are injected by Playwright evaluation only. `map_CURRENT.html` is not required to include those scripts, and the smoke removes the injected globals after evaluation.

The active production substrate remains `legacy_search_regions`.

No aura rendering, debug aura mode, canonical renderer flip, production readiness UI, adapter UI, production registry mutation, or map layer hydration occurs.

## Validation Shape

The smoke:

- loads `map_CURRENT.html` with only `skipOnboarding=1` and a cache buster,
- reads `window.__rmSmokeState()` for production-adjacent metadata,
- builds a sanitized neutral readiness profile,
- evaluates it through `RelocationSamplingCacheProductionShadowAdapterDev`,
- verifies no additional fetch occurs during adapter evaluation,
- verifies no DOM or map layer count changes,
- verifies no adapter/readiness UI appears,
- verifies no aura/debug path initializes,
- verifies the renderer substrate remains `legacy_search_regions`,
- verifies no raw backend payload is exposed.

## Rollback Scope

Rollback is deleting:

- `scripts/smoke_phase2_26_real_map_shadow_adapter.py`
- this narrative

No production UI, backend runtime, renderer implementation, scheduler/cache execution, `truth_grid_engine.py`, aura implementation, account/auth/persistence, or production behavior is changed.

## Validation Command

```bash
./venv/bin/python scripts/smoke_phase2_26_real_map_shadow_adapter.py
```

Expected result:

- `all_pass: true`

## Governance Closeout

- **Trust risk addressed:** the real map can be shadow-evaluated by the readiness adapter without wiring the adapter into production.
- **Deferred excellence:** real production integration, visible UI, CI enforcement, telemetry, and renderer promotion remain future work.
- **Rejected scope:** editing `map_CURRENT.html`, flipping substrates, implementing aura visuals, hydrating production layers, exposing raw payloads, or creating recommendation/scoring/interpretive surfaces.
