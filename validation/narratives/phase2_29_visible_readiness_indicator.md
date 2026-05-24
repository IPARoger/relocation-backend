# Phase 2.29 — Visible Readiness Indicator

## Purpose

Phase 2.29 introduces the first visible indicator for the production readiness metadata path.

This is debug-only. It is not product UI and not visible renderer integration.

## Boundary

The indicator appears only when the real map page is loaded with:

```text
?productionShadowSelfCheck=1
```

It is absent by default.

The indicator is intentionally labeled as DEV / DEBUG and displays only sanitized readiness metadata from the existing in-page self-check hook.

## Non-Goals

Phase 2.29 does not:

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
```

The Phase 2.29 smoke verifies:

- default page load has no indicator,
- debug-flagged page load shows the indicator,
- indicator is visibly marked DEV / DEBUG,
- displayed fields are sanitized readiness metadata only,
- substrate remains `legacy_search_regions`,
- no map layer is added,
- no raw payload is exposed,
- no recommendation/scoring/final-truth surface appears,
- no aura rendering is invoked,
- no production layer hydration occurs,
- rendering the indicator does not fetch,
- rendering the indicator does not mutate map layers, renderer substrate, production registry, or layer hydration state.

## Rollback Scope

Rollback is limited to:

- removing the debug-only indicator CSS and render function from `map_CURRENT.html`,
- deleting `scripts/smoke_phase2_29_visible_readiness_indicator.py`,
- deleting this narrative.

No backend runtime, renderer implementation outside the debug hook, scheduler/cache execution, `truth_grid_engine.py`, aura implementation, account/auth/persistence, or default production behavior is changed.

## Governance Closeout

- **Trust risk addressed:** readiness metadata can be made visible for developers without becoming product UI.
- **Deferred excellence:** real product readiness UI, production telemetry, CI enforcement, renderer integration, and user-facing guidance remain future work.
- **Rejected scope:** default visibility, substrate flip, aura rendering, raw payload exposure, recommendation/scoring/final-truth surfaces, backend changes, and production layer hydration.
