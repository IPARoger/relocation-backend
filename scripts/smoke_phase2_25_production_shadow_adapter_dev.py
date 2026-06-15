#!/usr/bin/env python3
"""Browser smoke for Phase 2.25 dev-only production shadow adapter."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_production_readiness_contract.js",
    ROOT / "sampling_cache_production_shadow_adapter_dev.js",
]


def run_browser_probe() -> dict:
    sources = [path.read_text(encoding="utf-8") for path in SOURCES]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        result = page.evaluate(
            """sources => {
                const fetchCalls = [];
                const originalFetch = window.fetch;
                window.fetch = (...args) => {
                    fetchCalls.push(String(args[0] || ""));
                    throw new Error("fetch not allowed in Phase 2.25 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                window.__backendRuntimeTouched = false;
                window.__workerStarted = false;
                window.__persistenceTouched = false;
                window.__domMutationTouched = false;
                window.__mapMutationTouched = false;
                const beforeBody = document.body.innerHTML;

                sources.forEach(source => eval(source));

                const contract = window.RelocationSamplingCacheProductionReadinessContract;
                const adapter = window.RelocationSamplingCacheProductionShadowAdapterDev;

                function cleanCandidate(status = "production_candidate") {
                    return {
                        requested_readiness_status: status,
                        runtime_metadata: {
                            refinement_load: 0.25,
                            refinement_order_score: 0.75,
                            display_state: "active",
                            runtime_structure_available: true,
                            final_truth_claimed: false
                        },
                        boundary_flags: {
                            no_interpretation_in_runtime_metadata: true,
                            no_symbolic_scoring: true,
                            no_recommendation_authority: true,
                            no_best_location_logic: true,
                            no_hidden_ontology: true,
                            renderer_ownership_claimed: false,
                            production_registry_mutated: false,
                            dom_mutation_outside_approved_root: false,
                            raw_backend_payload_exposed: false,
                            unsafe_hydration: false,
                            final_truth_claimed: false,
                            candidates_confirmed_as_truth: false,
                            runtime_priority_implies_symbolic_importance: false,
                            neutral_runtime_metadata: true,
                            candidate_vocabulary_quarantined: true
                        },
                        observer: {
                            read_only: true,
                            can_control_lifecycle: false,
                            can_control_scheduler: false,
                            can_control_hydration: false,
                            can_control_cache: false
                        },
                        cache: {
                            semantic_cache_keys_renderer_independent: true,
                            semantic_cache_keys_debug_independent: true,
                            semantic_cache_keys_aura_independent: true,
                            foreground_user_request_protected: true,
                            background_work_cannot_block_current_intent: true,
                            stale_or_cancelled_work_cannot_hydrate_visibly: true
                        },
                        validation: {
                            dedicated_smoke_exists: true,
                            narrative_exists: true,
                            rollback_scope_clear: true
                        },
                        production_path: {
                            renderer_substrate: "legacy_search_regions",
                            fetch_coupled: false,
                            worker_coupled: false,
                            dom_or_map_coupled: false,
                            renderer_coupled: false,
                            persistence_coupled: false,
                            backend_coupled: false
                        }
                    };
                }

                function evaluate(candidate) {
                    return adapter.evaluateShadowCandidate(candidate);
                }

                const cleanProduction = evaluate(cleanCandidate("production_candidate"));
                const cleanTransitional = evaluate(cleanCandidate("transitional_candidate"));

                const symbolicScoring = cleanCandidate("production_candidate");
                symbolicScoring.runtime_metadata.symbolic_score = 0.91;
                const symbolicScoringResult = evaluate(symbolicScoring);

                const recommendation = cleanCandidate("production_candidate");
                recommendation.runtime_metadata.recommendation_logic = true;
                const recommendationResult = evaluate(recommendation);

                const rawPayload = cleanCandidate("production_candidate");
                rawPayload.runtime_metadata.raw_payload = {
                    features: [{ geometry: { coordinates: [0, 0] } }]
                };
                const rawPayloadResult = evaluate(rawPayload);

                const observerControl = cleanCandidate("production_candidate");
                observerControl.observer.can_control_scheduler = true;
                const observerControlResult = evaluate(observerControl);

                const rendererMutation = cleanCandidate("production_candidate");
                rendererMutation.boundary_flags.renderer_ownership_claimed = true;
                rendererMutation.boundary_flags.production_registry_mutated = true;
                const rendererMutationResult = evaluate(rendererMutation);

                const staleHydration = cleanCandidate("production_candidate");
                staleHydration.cache.stale_or_cancelled_work_cannot_hydrate_visibly = false;
                const staleHydrationResult = evaluate(staleHydration);

                const inspect = adapter.inspectAdapter();
                const contractInspect = contract.inspectContract();
                const cleanSerialized = JSON.stringify(cleanProduction);
                const rawSerialized = JSON.stringify(rawPayloadResult);

                window.fetch = originalFetch;

                return {
                    adapter_loads_in_isolation:
                        Boolean(adapter) &&
                        typeof adapter.evaluateShadowCandidate === "function" &&
                        typeof adapter.inspectAdapter === "function" &&
                        inspect.standalone === true &&
                        inspect.debug_only === true,
                    clean_production_adjacent_profile_evaluates_through_contract:
                        cleanProduction.accepted === true &&
                        cleanProduction.readiness_status === "production_candidate" &&
                        cleanProduction.classification.mode === contract.CONTRACT_MODE &&
                        cleanProduction.classification.production_candidate_allowed === true,
                    clean_transitional_profile_remains_transitional_candidate:
                        cleanTransitional.accepted === true &&
                        cleanTransitional.readiness_status === "transitional_candidate" &&
                        cleanTransitional.classification.transitional_candidate_allowed === true,
                    symbolic_scoring_fails:
                        symbolicScoringResult.accepted === false &&
                        symbolicScoringResult.failed_gates.includes("layer_sovereignty"),
                    recommendation_logic_fails:
                        recommendationResult.accepted === false &&
                        recommendationResult.failed_gates.includes("layer_sovereignty"),
                    raw_payload_exposure_fails:
                        rawPayloadResult.accepted === false &&
                        rawPayloadResult.failed_gates.includes("runtime_sovereignty"),
                    observer_control_fails:
                        observerControlResult.accepted === false &&
                        observerControlResult.failed_gates.includes("observer_safety"),
                    renderer_ownership_mutation_fails:
                        rendererMutationResult.accepted === false &&
                        rendererMutationResult.failed_gates.includes("runtime_sovereignty"),
                    stale_hydration_fails:
                        staleHydrationResult.accepted === false &&
                        staleHydrationResult.failed_gates.includes("cache_scheduler_safety"),
                    adapter_does_not_fetch:
                        fetchCalls.length === 0 &&
                        cleanProduction.fetch_used === false &&
                        inspect.fetch_used === false,
                    adapter_does_not_mutate_dom_or_map:
                        document.body.innerHTML === beforeBody &&
                        window.__domMutationTouched === false &&
                        window.__mapMutationTouched === false &&
                        cleanProduction.dom_or_map_mutated === false &&
                        inspect.dom_or_map_mutated === false,
                    adapter_does_not_change_renderer_substrate:
                        inspect.active_production_substrate === "legacy_search_regions" &&
                        cleanProduction.active_production_substrate === "legacy_search_regions" &&
                        contractInspect.rendererSubstrate === "legacy_search_regions" &&
                        window.__productionRendererOwner === "legacy_search_regions",
                    adapter_does_not_touch_production_registry:
                        window.__productionOverlayRegistry.length === 0 &&
                        window.__productionOverlayLifecycleTouched === false &&
                        cleanProduction.production_registry_mutated === false &&
                        inspect.production_registry_mutated === false,
                    output_metadata_only_and_sanitized:
                        cleanProduction.metadata_only === true &&
                        cleanProduction.raw_backend_payload_exposed === false &&
                        cleanProduction.final_truth_claimed === false &&
                        cleanProduction.recommendation_surface_created === false &&
                        cleanProduction.scoring_surface_created === false &&
                        cleanProduction.interpretation_surface_created === false &&
                        !cleanSerialized.includes('"features"') &&
                        !cleanSerialized.includes('"geometry"') &&
                        !cleanSerialized.includes('"coordinates"') &&
                        !rawSerialized.includes('"features"') &&
                        !rawSerialized.includes('"geometry"') &&
                        !rawSerialized.includes('"coordinates"'),
                    legacy_search_regions_remains_active_production_substrate:
                        inspect.legacy_search_regions_active === true &&
                        cleanProduction.legacy_search_regions_active === true &&
                        inspect.rendererSubstrate === "legacy_search_regions" &&
                        cleanProduction.rendererSubstrate === "legacy_search_regions",
                    no_worker_renderer_persistence_or_backend_coupling:
                        window.__workerStarted === false &&
                        window.__persistenceTouched === false &&
                        window.__backendRuntimeTouched === false &&
                        inspect.worker_started === false &&
                        inspect.persisted === false &&
                        inspect.backend_coupled === false &&
                        inspect.render_started === false &&
                        cleanProduction.render_started === false
                };
            }""",
            sources,
        )
        browser.close()
        return result


def main() -> int:
    result = run_browser_probe()
    checks = [
        "adapter_loads_in_isolation",
        "clean_production_adjacent_profile_evaluates_through_contract",
        "clean_transitional_profile_remains_transitional_candidate",
        "symbolic_scoring_fails",
        "recommendation_logic_fails",
        "raw_payload_exposure_fails",
        "observer_control_fails",
        "renderer_ownership_mutation_fails",
        "stale_hydration_fails",
        "adapter_does_not_fetch",
        "adapter_does_not_mutate_dom_or_map",
        "adapter_does_not_change_renderer_substrate",
        "adapter_does_not_touch_production_registry",
        "output_metadata_only_and_sanitized",
        "legacy_search_regions_remains_active_production_substrate",
        "no_worker_renderer_persistence_or_backend_coupling",
    ]
    all_pass = all(bool(result.get(check)) for check in checks)
    print(json.dumps({"all_pass": all_pass, "checks": result}, indent=2, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
