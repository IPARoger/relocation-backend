# Phase 2.27 — Real Map Shadow Self-Check Hook

## Purpose

Phase 2.27 introduces the first debug-gated production-page self-check hook for production shadow readiness metadata.

This is not visible integration.

## Boundary

The hook is available only when the real map page is loaded with:

```text
?productionShadowSelfCheck=1
```

Without that flag, `window.__rmProductionShadowState` is absent.

The hook exposes sanitized metadata only. It does not fetch, render, create map layers, hydrate production layers, mutate visible DOM, change renderer substrate, alter scheduler/cache behavior, expose raw backend payloads, control observers, or create recommendation/scoring/interpretive surfaces.

## Production Behavior

Default production behavior is unchanged.

The active renderer substrate remains `legacy_search_regions`.

No aura rendering is implemented. No aura/debug visual mode is activated by the self-check flag.

No production readiness UI or adapter UI is created.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_map_current.py
./venv/bin/python scripts/smoke_phase2_26_real_map_shadow_adapter.py
./venv/bin/python scripts/smoke_phase2_27_real_map_shadow_self_check.py
```

The Phase 2.27 smoke proves:

- default page load works without the debug flag,
- the self-check hook is absent by default,
- debug-flagged page load exposes `window.__rmProductionShadowState`,
- returned metadata is neutral and sanitized,
- active substrate remains `legacy_search_regions`,
- no visible UI appears,
- no map layer is added,
- no raw payload, recommendation, scoring, or final-truth surface appears,
- no aura/debug visual mode is invoked,
- calling the hook causes no unexpected fetch, DOM/map mutation, registry mutation, or layer hydration.

## Rollback Scope

Rollback is limited to:

- removing the debug-gated hook from `map_CURRENT.html`,
- deleting `scripts/smoke_phase2_27_real_map_shadow_self_check.py`,
- deleting this narrative.

No backend runtime, renderer implementation, scheduler/cache execution, `truth_grid_engine.py`, aura implementation, account/auth/persistence, or production output is changed.

## Governance Closeout

- **Trust risk addressed:** the real page can expose a debug-only sanitized readiness self-check without adopting production integration.
- **Deferred excellence:** visible readiness UI, production telemetry, renderer promotion, CI enforcement, and adapter-driven production behavior remain future work.
- **Rejected scope:** substrate flip, aura rendering, raw payload exposure, layer hydration, visible UI, backend changes, cache/scheduler changes, and recommendation/scoring/interpretive surfaces.
