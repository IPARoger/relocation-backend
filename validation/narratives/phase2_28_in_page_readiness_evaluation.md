# Phase 2.28 — In-Page Readiness Evaluation

## Purpose

Phase 2.28 extends the debug-gated production shadow self-check so the real map page can return sanitized production-readiness metadata under an explicit debug flag.

This is debug-only. It is not visible integration.

## Boundary

The readiness metadata is available only through the existing debug hook when the page is loaded with:

```text
?productionShadowSelfCheck=1
```

Default page behavior is unchanged. Without the flag, the hook remains absent.

The result is metadata-only and does not include raw backend payloads, geometry, coordinates, symbolic scoring, recommendation logic, interpretation, best-location language, or aura output.

## Non-Goals

Phase 2.28 does not:

- create visible UI,
- change renderer substrate,
- implement aura rendering,
- fetch,
- hydrate production layers,
- alter scheduler/cache execution,
- change backend behavior,
- touch `truth_grid_engine.py`,
- create recommendation/scoring/interpretive surfaces,
- or expose raw payloads.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_map_current.py
./venv/bin/python scripts/smoke_phase2_26_real_map_shadow_adapter.py
./venv/bin/python scripts/smoke_phase2_27_real_map_shadow_self_check.py
./venv/bin/python scripts/smoke_phase2_28_in_page_readiness_evaluation.py
```

The Phase 2.28 smoke verifies:

- default page load leaves readiness/self-check hooks absent or inert,
- debug-flagged page load exposes sanitized readiness metadata,
- substrate remains `legacy_search_regions`,
- no visible UI is created,
- no map layer is added,
- no raw payload is exposed,
- no recommendation/scoring/final-truth surface appears,
- no aura rendering is invoked,
- no production layer hydration occurs,
- calling the hook causes no fetch, DOM/map mutation, renderer-substrate change, registry mutation, or layer creation.

## Rollback Scope

Rollback is limited to:

- removing the readiness metadata extension from the debug-gated hook in `map_CURRENT.html`,
- deleting `scripts/smoke_phase2_28_in_page_readiness_evaluation.py`,
- deleting this narrative.

No backend runtime, renderer implementation outside the debug hook, scheduler/cache execution, `truth_grid_engine.py`, aura implementation, account/auth/persistence, or default production behavior is changed.

## Governance Closeout

- **Trust risk addressed:** debug-only readiness metadata can be inspected inside the production page without operationalizing it.
- **Deferred excellence:** visible readiness indicators, CI enforcement, telemetry, renderer promotion, and production adapter behavior remain future work.
- **Rejected scope:** visible UI, substrate flip, aura rendering, backend changes, raw payload exposure, layer hydration, scheduler/cache mutation, recommendation/scoring/interpretive surfaces.
