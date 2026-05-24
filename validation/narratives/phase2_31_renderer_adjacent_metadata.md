# Phase 2.31 — Renderer-Adjacent Metadata Placeholder

## Purpose

Phase 2.31 adds a renderer-adjacent readiness metadata placeholder inside the existing Phase 2.30 debug dev overlay container.

This is metadata only. It is not renderer integration and does not create real rendering.

## Boundary

The placeholder appears only when the real map page is loaded with:

```text
?productionShadowSelfCheck=1
```

It is absent by default.

The metadata is visibly labeled as DEV / DEBUG and is hosted inside the existing debug dev overlay container. It reports only sanitized negative assertions and the active substrate.

## Non-Goals

Phase 2.31 does not:

- change default behavior,
- change renderer substrate,
- create real rendering,
- implement aura rendering,
- invoke aura output,
- alter backend behavior,
- alter fetch behavior,
- touch `truth_grid_engine.py`,
- execute scheduler/cache work,
- hydrate production layers,
- expose raw payloads,
- create product UI,
- create recommendation/scoring surfaces,
- or claim final truth.

## Placeholder Fields

The debug-only placeholder may expose:

- `renderer_adjacent_placeholder: true`
- `debug_only: true`
- `active_substrate: legacy_search_regions`
- `substrate_flip_requested: false`
- `real_rendering_created: false`
- `production_layers_hydrated: false`
- `raw_payload_exposed: false`
- `scheduler_cache_execution: false`
- `aura_output_created: false`
- `product_ui_created: false`
- `recommendation_surface_created: false`
- `scoring_surface_created: false`
- `final_truth_claimed: false`

These fields are not user-facing product status. They are development diagnostics only.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_map_current.py
./venv/bin/python scripts/smoke_phase2_26_real_map_shadow_adapter.py
./venv/bin/python scripts/smoke_phase2_27_real_map_shadow_self_check.py
./venv/bin/python scripts/smoke_phase2_28_in_page_readiness_evaluation.py
./venv/bin/python scripts/smoke_phase2_29_visible_readiness_indicator.py
./venv/bin/python scripts/smoke_phase2_30_dev_overlay_container.py
./venv/bin/python scripts/smoke_phase2_31_renderer_adjacent_metadata.py
```

The Phase 2.31 smoke verifies:

- default page load has no renderer-adjacent metadata panel,
- default page load has no dev overlay container,
- debug-flagged page load shows the existing dev overlay container,
- renderer-adjacent placeholder metadata exists only under the debug flag,
- active substrate remains `legacy_search_regions`,
- no map layer is added,
- no raw payload is exposed,
- no scheduler/cache execution occurs,
- no aura output is created,
- no production layer hydration occurs,
- no recommendation/scoring/final-truth surface appears,
- creating/displaying the placeholder does not fetch,
- calling the debug hook does not mutate DOM,
- renderer substrate, production registry, and layer hydration state remain unchanged.

## Rollback Scope

Rollback is limited to:

- removing the renderer-adjacent placeholder from the debug-only metadata object in `map_CURRENT.html`,
- removing the renderer-adjacent panel from the debug-only dev overlay container,
- deleting `scripts/smoke_phase2_31_renderer_adjacent_metadata.py`,
- deleting this narrative.

No backend runtime, fetch path, scheduler/cache execution, `truth_grid_engine.py`, aura implementation, account/auth/persistence, renderer substrate, production layers, or default production behavior is changed.

## Governance Closeout

- **Trust risk addressed:** renderer-adjacent readiness has an explicit debug-only metadata placeholder before any rendering integration.
- **Deferred excellence:** real renderer integration, substrate switching, production telemetry, CI enforcement, product UI, and aura rendering remain future work.
- **Rejected scope:** default visibility, substrate flip, real rendering, aura output, raw payload exposure, scheduler/cache execution, product UI, recommendation/scoring/final-truth surfaces, backend changes, and production layer hydration.
