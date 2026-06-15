# Phase 2.32 — Dev-Only Renderer Integration Proof

## Purpose

Phase 2.32 is the first controlled renderer integration proof in the real map page.

It is dev-only and metadata-only. It proves that a renderer-adjacent branch can be explicitly detected in the real page without changing default behavior, flipping the production substrate, hydrating production layers, invoking aura output, fetching from the backend, or creating product UI.

## Boundary

The proof activates only when both explicit debug flags are present:

```text
?productionShadowSelfCheck=1&devRendererProof=1
```

The proof is absent by default.

`?productionShadowSelfCheck=1` alone keeps the Phase 2.31 renderer-adjacent metadata placeholder active but does not activate the Phase 2.32 dev renderer proof.

## Non-Goals

Phase 2.32 does not:

- change default behavior,
- flip the production renderer substrate,
- create product UI,
- create real user rendering,
- create production map layers,
- hydrate production layers,
- invoke aura output,
- alter backend behavior,
- alter fetch behavior,
- touch `truth_grid_engine.py`,
- execute scheduler/cache work,
- expose raw payloads,
- create recommendation/scoring/interpretive surfaces,
- or claim final truth.

## Proof Metadata

The proof may expose only sanitized debug metadata:

- `dev_renderer_proof: true`
- `debug_only: true`
- `active_substrate: legacy_search_regions`
- `production_substrate_flipped: false`
- `production_layers_hydrated: false`
- `real_user_rendering_created: false`
- `product_ui_created: false`
- `aura_output_created: false`
- `backend_fetch_created: false`
- `scheduler_cache_execution: false`
- `raw_payload_exposed: false`
- `recommendation_surface_created: false`
- `scoring_surface_created: false`
- `final_truth_claimed: false`

These fields are development diagnostics only. They are not product status, user-facing readiness, recommendation logic, scoring, or interpretation.

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
```

The Phase 2.32 smoke verifies:

- default page load has no dev renderer proof,
- default page load has no dev renderer UI/marker/container,
- default production substrate remains `legacy_search_regions`,
- `?productionShadowSelfCheck=1` alone does not activate the proof,
- `?productionShadowSelfCheck=1&devRendererProof=1` activates only sanitized metadata,
- no production map layer is added,
- no production registry is mutated,
- no production layer hydration occurs,
- no fetch is caused by the proof,
- no renderer substrate change occurs,
- no aura output is invoked,
- no raw payload is exposed,
- no product UI is created,
- no recommendation/scoring/final-truth surface appears,
- existing Phase 2.26-2.31 smokes remain compatible.

## Rollback Scope

Rollback is limited to:

- removing the `devRendererProof` flag parsing in `map_CURRENT.html`,
- removing the debug-only dev renderer proof metadata object,
- removing the debug-only dev renderer proof overlay section,
- deleting `scripts/smoke_phase2_32_dev_renderer_integration.py`,
- deleting this narrative.

No backend runtime, fetch path, scheduler/cache execution, `truth_grid_engine.py`, aura implementation, account/auth/persistence, production renderer substrate, production layers, or default production behavior is changed.

## Governance Closeout

- **Trust risk addressed:** the first renderer integration proof is explicitly gated, metadata-only, and validated before any real rendering.
- **Deferred excellence:** actual renderer integration, production layer ownership, substrate switching, scheduler/cache execution, aura rendering, product UI, and CI enforcement remain future work.
- **Rejected scope:** default visibility, production substrate flip, production layer hydration, real user rendering, aura output, raw payload exposure, backend/fetch changes, product UI, recommendation/scoring/final-truth surfaces.
