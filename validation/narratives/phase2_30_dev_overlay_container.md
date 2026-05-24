# Phase 2.30 — Dev Overlay Container

## Purpose

Phase 2.30 introduces a small debug-only dev overlay container in the real production map page.

The container gives readiness/debug metadata surfaces a bounded place to live without turning them into product UI or changing production behavior.

## Boundary

The container appears only when the real map page is loaded with:

```text
?productionShadowSelfCheck=1
```

It is absent by default.

The container is explicitly labeled DEV / DEBUG and currently hosts the debug readiness metadata indicator created in Phase 2.29.

## Non-Goals

Phase 2.30 does not:

- change default behavior,
- change renderer substrate,
- implement aura rendering,
- alter backend behavior,
- fetch,
- hydrate production layers,
- mutate scheduler/cache execution,
- touch `truth_grid_engine.py`,
- expose raw payloads,
- create recommendation/scoring/interpretive surfaces,
- or claim final truth.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_map_current.py
./venv/bin/python scripts/smoke_phase2_26_real_map_shadow_adapter.py
./venv/bin/python scripts/smoke_phase2_27_real_map_shadow_self_check.py
./venv/bin/python scripts/smoke_phase2_28_in_page_readiness_evaluation.py
./venv/bin/python scripts/smoke_phase2_29_visible_readiness_indicator.py
./venv/bin/python scripts/smoke_phase2_30_dev_overlay_container.py
```

The Phase 2.30 smoke verifies:

- default page load has no dev overlay container,
- default page load has no readiness indicator,
- debug-flagged page load shows the dev overlay container,
- container is visibly marked DEV / DEBUG,
- readiness metadata surface exists inside the container,
- displayed fields are sanitized metadata only,
- substrate remains `legacy_search_regions`,
- no map layer is added,
- no raw payload is exposed,
- no recommendation/scoring/final-truth surface appears,
- no aura rendering is invoked,
- no production layer hydration occurs,
- creating the container does not fetch,
- creating the container does not mutate map layers, renderer substrate, production registry, or layer hydration state.

## Rollback Scope

Rollback is limited to:

- removing the debug-only container CSS and render path from `map_CURRENT.html`,
- deleting `scripts/smoke_phase2_30_dev_overlay_container.py`,
- deleting this narrative.

No backend runtime, renderer implementation outside the debug hook, scheduler/cache execution, `truth_grid_engine.py`, aura implementation, account/auth/persistence, or default production behavior is changed.

## Governance Closeout

- **Trust risk addressed:** debug metadata now has a bounded dev-only overlay surface rather than ad hoc visual placement.
- **Deferred excellence:** product UI, production telemetry, CI enforcement, renderer integration, and user-facing readiness affordances remain future work.
- **Rejected scope:** default visibility, substrate flip, aura rendering, raw payload exposure, recommendation/scoring/final-truth surfaces, backend changes, and production layer hydration.
