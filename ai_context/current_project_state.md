# Current Project State

## Branch

Current branch at bootstrap creation:

- `checkpoint/pre-phase-2-3`

---

# Current Production Path

The active production-facing map path remains:

- `map_CURRENT.html`
- legacy `/search-regions` rendering behavior, now with accepted truth-grid boundary refinement
- renderer substrate: `legacy_search_regions`

The production renderer remains sovereign. Phase 2 sandbox work has not replaced production overlay ownership.

Accepted production truth work:

- `21b85bd` — accepted truth-grid boundary refinement for `/search-regions`.
- Boundary-refined truth-grid output is accepted production behavior after dedicated validation.
- `map_CURRENT.html` default behavior remains unchanged apart from continuing to use the legacy production substrate.

Production readiness visibility:

- A debug-only readiness indicator exists only under `?productionShadowSelfCheck=1`.
- `8d93fc7` added the Phase 2.30 debug dev overlay container.
- `3f8ced0` added Phase 2.31 renderer-adjacent debug metadata.
- The debug dev overlay container is absent by default and appears only under `?productionShadowSelfCheck=1`.
- The readiness indicator and renderer-adjacent metadata are hosted inside the debug dev overlay container.
- It is absent by default and must not be treated as product UI.
- It reports sanitized readiness metadata only and does not change production behavior.
- Phase 2.31 is renderer-adjacent metadata only, not renderer integration.
- No real rendering has been created.

Aura status:

- Aura remains prototype/debug/design-only, not production rendering.
- No aura output has been promoted.
- The aura visual concept is not approved yet.
- Static visual mockups and readability/overlap tests are still needed before production aura rendering.

---

# Phase 2 State

## Phase 2.4-2.14 Transitional Runtime / Cache / Fetch Chain

The transitional chain proves cache/runtime concepts without production takeover:

- Phase 2.4 semantic cache-key contract
- Phase 2.5 scheduler population semantics
- Phase 2.6 in-memory cache store scaffold
- Phase 2.7 orchestration contract
- Phase 2.8 mock runtime harness
- Phase 2.9 mock execution bridge
- Phase 2.10 observer/progress semantics
- Phase 2.11 execution policy semantics
- Phase 2.12 dev runtime bridge
- Phase 2.13 dev execution runtime
- Phase 2.14 isolated fetch bridge

Governance posture:

- transitional path,
- metadata-first,
- mostly contract-only,
- no production renderer ownership,
- no persistence,
- and no symbolic interpretation.

## Phase 2.15-2.23 Experimental Sandbox Chain

The experimental chain proves isolated hydration and symbolic-exploration structures without production promotion:

- Phase 2.15 renderer hydration sandbox
- Phase 2.16 multi-overlay coexistence sandbox
- Phase 2.17 viewport-scoped hydration sandbox
- Phase 2.18 progressive refinement hydration sandbox
- Phase 2.19 adaptive refinement density sandbox
- Phase 2.20 ambiguity-domain sandbox
- Phase 2.21 implication-field sandbox
- Phase 2.22 emergence-field sandbox
- Phase 2.23 cross-domain continuity sandbox

Governance posture:

- experimental path,
- dev-only,
- smoke-tested,
- isolated DOM roots,
- no production overlay registry mutation,
- no renderer ownership transfer,
- no persistence,
- and `rendererSubstrate = legacy_search_regions`.

## Phase 2.24-2.31 Production Shadow Governance Chain

The production-shadow chain proves readiness evaluation and visibility boundaries without changing default production behavior:

- `35acb7a` — Phase 2.24 production-readiness boundary contract.
- `3184fa0` — Phase 2.25 production shadow adapter scaffold.
- `3072ffd` — Phase 2.26 real-map shadow adapter smoke.
- `a184f76` — Phase 2.27 debug production shadow self-check.
- `95d4afc` — Phase 2.28 in-page readiness evaluation.
- `ea65d35` — Phase 2.29 debug readiness indicator.
- `8d93fc7` — Phase 2.30 debug dev overlay container.
- `3f8ced0` — Phase 2.31 renderer-adjacent debug metadata.

Governance posture:

- debug-only,
- metadata-only,
- no default behavior change,
- no renderer substrate flip,
- no backend changes,
- no production fetch changes,
- no production layer hydration,
- no raw payload exposure,
- no recommendation/scoring/final-truth surface,
- no product UI,
- no visible renderer integration,
- no real rendering,
- and no aura production integration.

Related smoke/governance commits:

- `eeb7657` — kept `scripts/smoke_map_current.py` focused on production/default map behavior.
- `a73a548` — split aura debug checks from the production map smoke.
- `7e87b08` — committed `substrate_adapter.js` as an inert production-loaded scaffold.
- `8328c0f` — committed `aura_field_engine.py` as debug/prototype backend support.

Related visual-design doctrine:

- `df473af` — added `docs/visual_design/aura_visual_design_brief.md`.

---

# Path Separation

## Active Production Path

- `map_CURRENT.html`
- backend modules
- existing `/search-regions` behavior with accepted truth-grid boundary refinement
- current visible renderer behavior

This is the live behavior path and should not be casually modified during governance or purification passes.

## Transitional Path

- `phase2_cache_scheduler.js`
- `sampling_cache_contract.js`
- `sampling_cache_store_contract.js`
- `sampling_cache_orchestration_contract.js`
- `sampling_cache_execution_bridge_contract.js`
- `sampling_cache_observer_contract.js`
- `sampling_cache_execution_policy_contract.js`
- `sampling_cache_runtime_bridge_dev.js`
- `sampling_cache_execution_runtime_dev.js`
- `sampling_cache_fetch_bridge_dev.js`

This path proves runtime/cache/fetch mechanics and should be purified before promotion.

## Experimental Path

- `sampling_cache_renderer_hydration_sandbox.js`
- `sampling_cache_multi_overlay_sandbox.js`
- `sampling_cache_viewport_hydration_sandbox.js`
- `sampling_cache_progressive_refinement_sandbox.js`
- `sampling_cache_adaptive_density_sandbox.js`
- `sampling_cache_ambiguity_domain_sandbox.js`
- `sampling_cache_implication_field_sandbox.js`
- `sampling_cache_emergence_field_sandbox.js`
- `sampling_cache_cross_domain_continuity_sandbox.js`

These files are proof scaffolds, not production architecture.

## Archaeology / Reference Path

- `memory_archaeology_raw/`
- `docs/review_bundle/`
- older `docs/technical_philosophy/` documents
- validation narratives and reports
- older doctrine documents referenced by `docs/DOCTRINE_INDEX.md`

These are evidence and deeper context. Do not treat superseded archaeology as implementation law unless explicitly revived.

---

# Current Governance Findings

The Phase 2 chain is mostly aligned with constitutional doctrine:

- renderer ownership remains isolated,
- raw backend payloads are rejected or sanitized,
- production overlay registries are not mutated,
- persistence is avoided,
- and smoke tests explicitly check rollback and isolation boundaries.

Resolved governance progress:

- Phase 2.19-2.21 terminology purification was committed.
- Phase 2.22 and Phase 2.23 were committed as isolated sandbox scaffolds.
- Phase 2.24-2.31 established debug-only production readiness checks, visible dev-only readiness metadata, a bounded dev overlay container, and renderer-adjacent placeholder metadata without production behavior change.
- `substrate_adapter.js` was production-loaded but untracked; it is now committed as an inert scaffold.
- `aura_field_engine.py` was backend-imported but untracked; it is now committed as debug/prototype backend support.

Current cautions:

- Keep `phase2_cache_scheduler.js` out of renderer work unless scheduler/cache execution is explicitly in scope.
- `phase2_cache_scheduler.js` remains sandbox/prototype for the current path.
- Do not mix aura visual work with the production readiness bridge.
- Do not treat the debug readiness indicator, Phase 2.30 debug dev overlay container, or Phase 2.31 renderer-adjacent metadata as product UI.
- Do not implement aura rendering until the visual concept is approved.
- Do not proceed to first renderer integration without a Phase 2.32 decision review.

---

# Recommended Next Sequence

Next recommended action:

1. Perform a read-only Phase 2.32 decision review.
2. Likely Phase 2.32 options:
   - A. final debug-only renderer readiness contract check,
   - B. first controlled dev-only renderer integration,
   - C. workspace hygiene/quarantine,
   - D. aura visual mockup work separately.

Do not proceed to first renderer integration until the Phase 2.32 decision review confirms scope and required validation.
