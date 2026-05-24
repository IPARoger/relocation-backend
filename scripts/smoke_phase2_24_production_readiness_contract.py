#!/usr/bin/env python3
"""Browser smoke for the Phase 2.24 production-readiness boundary contract."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_production_readiness_contract.js",
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
                    throw new Error("fetch not allowed in Phase 2.24 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                window.__backendRuntimeTouched = false;
                window.__workerStarted = false;
                window.__persistenceTouched = false;
                sources.forEach(source => eval(source));

                const contract = window.RelocationSamplingCacheProductionReadinessContract;

                function cleanProfile(status = "production_candidate") {
                    return {
                        requested_readiness_status: status,
                        layer_sovereignty: {
                            no_interpretation_in_runtime_metadata: true,
                            no_symbolic_scoring: true,
                            no_recommendation_authority: true,
                            no_best_location_logic: true,
                            no_hidden_ontology: true
                        },
                        runtime_sovereignty: {
                            renderer_ownership_claimed: false,
                            production_registry_mutated: false,
                            dom_mutation_outside_approved_root: false,
                            raw_backend_payload_exposed: false,
                            unsafe_hydration: false
                        },
                        truth_integrity: {
                            final_truth_claimed: false,
                            candidates_confirmed_as_truth: false,
                            runtime_priority_implies_symbolic_importance: false
                        },
                        observer_safety: {
                            read_only: true,
                            can_control_lifecycle: false,
                            can_control_scheduler: false,
                            can_control_hydration: false,
                            can_control_cache: false,
                            metadata_sanitized: true
                        },
                        cache_scheduler_safety: {
                            semantic_cache_keys_renderer_independent: true,
                            semantic_cache_keys_debug_independent: true,
                            semantic_cache_keys_aura_independent: true,
                            foreground_user_request_protected: true,
                            background_work_cannot_block_current_intent: true,
                            stale_or_cancelled_work_cannot_hydrate_visibly: true
                        },
                        terminology_safety: {
                            neutral_runtime_metadata: true,
                            candidate_vocabulary_quarantined: true,
                            runtime_envelope: {
                                refinement_load: 0.4,
                                refinement_order_score: 0.7,
                                display_state: "active",
                                runtime_structure_available: true,
                                final_truth_claimed: false
                            },
                            quarantined_candidate_vocabulary: {
                                context: "non_runtime_candidate_vocabulary",
                                layer4_terms: ["recommendation", "best_location"]
                            }
                        },
                        validation_requirements: {
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

                function classify(profile) {
                    return contract.classifyReadiness(profile);
                }

                const cleanProduction = classify(cleanProfile("production_candidate"));
                const cleanTransitional = classify(cleanProfile("transitional_candidate"));

                const symbolicScoring = cleanProfile("production_candidate");
                symbolicScoring.layer_sovereignty.no_symbolic_scoring = false;
                const symbolicScoringResult = classify(symbolicScoring);

                const recommendation = cleanProfile("production_candidate");
                recommendation.layer_sovereignty.no_recommendation_authority = false;
                const recommendationResult = classify(recommendation);

                const rawPayload = cleanProfile("production_candidate");
                rawPayload.runtime_sovereignty.raw_backend_payload_exposed = true;
                rawPayload.terminology_safety.runtime_envelope.raw_payload = { geometry: { coordinates: [0, 0] } };
                const rawPayloadResult = classify(rawPayload);

                const observerControl = cleanProfile("production_candidate");
                observerControl.observer_safety.can_control_scheduler = true;
                const observerControlResult = classify(observerControl);

                const rendererMutation = cleanProfile("production_candidate");
                rendererMutation.runtime_sovereignty.renderer_ownership_claimed = true;
                rendererMutation.runtime_sovereignty.production_registry_mutated = true;
                const rendererMutationResult = classify(rendererMutation);

                const staleHydration = cleanProfile("production_candidate");
                staleHydration.cache_scheduler_safety.stale_or_cancelled_work_cannot_hydrate_visibly = false;
                const staleHydrationResult = classify(staleHydration);

                const forbiddenRuntimeVocabulary = cleanProfile("production_candidate");
                forbiddenRuntimeVocabulary.terminology_safety.runtime_envelope.best_location_logic = true;
                const forbiddenRuntimeVocabularyResult = classify(forbiddenRuntimeVocabulary);

                const unquarantinedLayer4 = cleanProfile("production_candidate");
                unquarantinedLayer4.terminology_safety.candidate_vocabulary_quarantined = false;
                unquarantinedLayer4.terminology_safety.quarantined_candidate_vocabulary = {
                    layer4_terms: ["recommendation", "best_location"]
                };
                const unquarantinedLayer4Result = classify(unquarantinedLayer4);

                const inspect = contract.inspectContract();
                const serialized = JSON.stringify({
                    cleanProduction,
                    cleanTransitional,
                    symbolicScoringResult,
                    recommendationResult,
                    rawPayloadResult,
                    observerControlResult,
                    rendererMutationResult,
                    staleHydrationResult,
                    forbiddenRuntimeVocabularyResult,
                    unquarantinedLayer4Result,
                    inspect
                });
                window.fetch = originalFetch;

                return {
                    clean_profile_can_be_production_candidate_only_when_all_hard_gates_pass:
                        cleanProduction.accepted === true &&
                        cleanProduction.hard_gates_passed === true &&
                        cleanProduction.readiness_status === "production_candidate" &&
                        cleanProduction.production_candidate_allowed === true,
                    clean_profile_can_be_transitional_candidate_when_all_hard_gates_pass:
                        cleanTransitional.accepted === true &&
                        cleanTransitional.hard_gates_passed === true &&
                        cleanTransitional.readiness_status === "transitional_candidate" &&
                        cleanTransitional.transitional_candidate_allowed === true,
                    symbolic_scoring_fails:
                        symbolicScoringResult.accepted === false &&
                        symbolicScoringResult.failed_gates.includes("layer_sovereignty"),
                    recommendation_logic_fails:
                        recommendationResult.accepted === false &&
                        recommendationResult.failed_gates.includes("layer_sovereignty"),
                    raw_payload_exposure_fails:
                        rawPayloadResult.accepted === false &&
                        rawPayloadResult.readiness_status === "not_ready",
                    observer_control_fails:
                        observerControlResult.accepted === false &&
                        observerControlResult.failed_gates.includes("observer_safety"),
                    renderer_ownership_mutation_fails:
                        rendererMutationResult.accepted === false &&
                        rendererMutationResult.failed_gates.includes("runtime_sovereignty"),
                    stale_hydration_fails:
                        staleHydrationResult.accepted === false &&
                        staleHydrationResult.failed_gates.includes("cache_scheduler_safety"),
                    neutral_runtime_terminology_passes:
                        cleanProduction.gate_results.find(item => item.gate === "terminology_safety").passed === true,
                    layer4_language_allowed_only_when_quarantined:
                        cleanProduction.accepted === true &&
                        unquarantinedLayer4Result.accepted === false &&
                        unquarantinedLayer4Result.failed_gates.includes("terminology_safety"),
                    forbidden_runtime_vocabulary_fails:
                        forbiddenRuntimeVocabularyResult.accepted === false &&
                        forbiddenRuntimeVocabularyResult.failed_gates.includes("terminology_safety"),
                    production_path_remains_legacy_search_regions:
                        inspect.rendererSubstrate === "legacy_search_regions" &&
                        cleanProduction.rendererSubstrate === "legacy_search_regions" &&
                        window.__productionRendererOwner === "legacy_search_regions",
                    no_fetch_worker_dom_map_renderer_persistence_or_backend_coupling:
                        fetchCalls.length === 0 &&
                        window.__productionOverlayRegistry.length === 0 &&
                        window.__productionOverlayLifecycleTouched === false &&
                        window.__backendRuntimeTouched === false &&
                        window.__workerStarted === false &&
                        window.__persistenceTouched === false &&
                        cleanProduction.fetch_used === false &&
                        cleanProduction.worker_started === false &&
                        cleanProduction.dom_or_map_mutated === false &&
                        cleanProduction.backend_coupled === false &&
                        cleanProduction.production_registry_mutated === false &&
                        cleanProduction.persisted === false,
                    no_raw_payload_echoed_from_accepted_profile:
                        !JSON.stringify(cleanProduction).includes('"features"') &&
                        !JSON.stringify(cleanProduction).includes('"coordinates"') &&
                        !JSON.stringify(cleanProduction).includes('"geometry"'),
                    contract_is_classification_only:
                        inspect.contract_only === true &&
                        cleanProduction.contract_only === true &&
                        serialized.includes("production_candidate")
                };
            }""",
            sources,
        )
        browser.close()
        return result


def main() -> int:
    result = run_browser_probe()
    checks = [
        "clean_profile_can_be_production_candidate_only_when_all_hard_gates_pass",
        "clean_profile_can_be_transitional_candidate_when_all_hard_gates_pass",
        "symbolic_scoring_fails",
        "recommendation_logic_fails",
        "raw_payload_exposure_fails",
        "observer_control_fails",
        "renderer_ownership_mutation_fails",
        "stale_hydration_fails",
        "neutral_runtime_terminology_passes",
        "layer4_language_allowed_only_when_quarantined",
        "forbidden_runtime_vocabulary_fails",
        "production_path_remains_legacy_search_regions",
        "no_fetch_worker_dom_map_renderer_persistence_or_backend_coupling",
        "no_raw_payload_echoed_from_accepted_profile",
        "contract_is_classification_only",
    ]
    passed = {name: bool(result.get(name)) for name in checks}
    all_pass = all(passed.values())
    print(json.dumps({
        "results": [{
            "test": "phase2_24_production_readiness_contract",
            "pass": all_pass,
            "detail": passed,
        }],
        "all_pass": all_pass,
    }, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
