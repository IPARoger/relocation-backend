# Phase 2.33 — Isolated Debug Renderer Test Layer

## Purpose

Phase 2.33 is the first isolated debug renderer test layer proof in the real map page.

It is dev/debug-only. It proves that a tiny non-production test marker can be explicitly activated, labeled, counted, and removed from the default experience without changing production behavior, flipping the production substrate, hydrating production layers, invoking aura output, fetching from the backend, or becoming product UI.

## Boundary

The proof activates only when all explicit debug flags are present:

```text
?productionShadowSelfCheck=1&devRendererProof=1&devRendererTestLayer=1
```

The test layer is absent by default.

`?productionShadowSelfCheck=1` alone keeps the existing debug overlay active but does not activate the dev renderer proof or the isolated test layer.

`?productionShadowSelfCheck=1&devRendererProof=1` keeps the Phase 2.32 metadata-only proof active but does not activate the isolated test layer.

## Non-Goals

Phase 2.33 does not:

- change default behavior,
- flip the production renderer substrate,
- create product UI,
- create real user rendering,
- create production map layers,
- mutate production layer registries,
- hydrate production layers,
- invoke aura output,
- alter backend behavior,
- alter fetch behavior,
- touch `truth_grid_engine.py`,
- execute scheduler/cache work,
- expose raw payloads,
- create recommendation/scoring/interpretive surfaces,
- or claim final truth.

## Debug Test Layer Metadata

The proof may expose only sanitized debug metadata:

- `dev_renderer_test_layer: true`
- `debug_only: true`
- `active_substrate: legacy_search_regions`
- `production_substrate_flipped: false`
- `production_layers_hydrated: false`
- `production_layer_registry_mutated: false`
- `isolated_debug_layer_created: true`
- `isolated_debug_layer_count: 1`
- `real_user_rendering_created: false`
- `product_ui_created: false`
- `aura_output_created: false`
- `backend_fetch_created: false`
- `scheduler_cache_execution: false`
- `raw_payload_exposed: false`
- `recommendation_surface_created: false`
- `scoring_surface_created: false`
- `final_truth_claimed: false`

These fields are development diagnostics only. They are not product status, product UI, recommendation logic, scoring, interpretation, or production readiness claims.

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
./venv/bin/python scripts/smoke_phase2_32_dev_renderer_integration.py
./venv/bin/python scripts/smoke_phase2_33_isolated_debug_test_layer.py
```

The Phase 2.33 smoke verifies:

- default page load has no dev renderer proof,
- default page load has no dev renderer test layer,
- default page load has no dev overlay,
- default production substrate remains `legacy_search_regions`,
- `?productionShadowSelfCheck=1` alone does not activate the proof or test layer,
- `?productionShadowSelfCheck=1&devRendererProof=1` remains metadata-only and does not activate the test layer,
- `?productionShadowSelfCheck=1&devRendererProof=1&devRendererTestLayer=1` activates only the isolated debug marker inside the dev overlay,
- the isolated debug marker is labeled `DEV DEBUG`,
- the isolated debug marker is separately counted,
- no production map layer is added,
- no production registry is mutated,
- no production layer hydration occurs,
- no fetch is caused by the proof,
- no renderer substrate change occurs,
- no aura output is invoked,
- no raw payload is exposed,
- no product UI is created,
- no recommendation/scoring/final-truth surface appears,
- existing Phase 2.26-2.32 smokes remain compatible.

## Rollback Scope

Rollback is limited to:

- removing the `devRendererTestLayer` flag parsing in `map_CURRENT.html`,
- removing the debug-only dev renderer test layer metadata object,
- removing the debug-only test layer overlay section,
- deleting `scripts/smoke_phase2_33_isolated_debug_test_layer.py`,
- deleting this narrative.

No backend runtime, fetch path, scheduler/cache execution, `truth_grid_engine.py`, aura implementation, account/auth/persistence, production renderer substrate, production layers, or default production behavior is changed.

## Governance Closeout

- **Trust risk addressed:** the first isolated renderer test marker is explicitly gated, overlay-contained, separately counted, and validated before any real rendering.
- **Deferred excellence:** actual renderer integration, production layer ownership, substrate switching, scheduler/cache execution, aura rendering, product UI, and CI enforcement remain future work.
- **Rejected scope:** default visibility, production substrate flip, production layer hydration, production registry mutation, real user rendering, aura output, raw payload exposure, backend/fetch changes, product UI, recommendation/scoring/final-truth surfaces.
