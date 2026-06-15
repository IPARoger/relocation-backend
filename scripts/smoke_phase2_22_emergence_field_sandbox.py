#!/usr/bin/env python3
"""Browser smoke for the Phase 2.22 aggregate_candidate field sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_emergence_field_sandbox.js",
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
                    throw new Error("fetch not allowed in Phase 2.22 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                const root = document.createElement("div");
                root.id = "phase2-22-isolated-root";
                document.body.appendChild(root);
                sources.forEach(source => eval(source));

                const viewportA = {
                    id: "viewport-a",
                    zoom: 4,
                    north: 30,
                    south: -10,
                    east: 40,
                    west: -20,
                    semantic_id: "atlantic-window"
                };
                const viewportB = {
                    id: "viewport-b",
                    zoom: 6,
                    north: 55,
                    south: 35,
                    east: 15,
                    west: -15,
                    semantic_id: "europe-window"
                };
                const sandbox = window.RelocationSamplingCacheAggregateCandidateFieldSandbox
                    .createAggregateCandidateFieldSandbox({ root, viewport_scope: viewportA });

                function envelope(cacheKey, featureCount, state = "completed") {
                    const blocked = state === "stale" || state === "cancelled";
                    return {
                        hydration: {
                            schema_version: 1,
                            cache_key: cacheKey,
                            compatible: true,
                            hydrated: true,
                            execution_required: false,
                            hydration: {
                                schema_version: 1,
                                key: cacheKey,
                                status: "ready",
                                summary: { feature_count: featureCount, response_type: "FeatureCollection" },
                                metrics: { backend_status: 200 },
                                created_at_ms: 1000 + featureCount,
                                updated_at_ms: 1000 + featureCount,
                                expires_at_ms: 2000 + featureCount
                            }
                        },
                        execution: {
                            state,
                            job: {
                                cache_key: cacheKey,
                                intent_group: "chart-a:sun-house-1",
                                generation: 1,
                                stale: state === "stale",
                                cancelled: state === "cancelled"
                            }
                        },
                        observer: {
                            cache_key: cacheKey,
                            observer_state: blocked ? state : "hydration_eligible",
                            discovery_state: blocked ? "none" : "nearby_structure_available",
                            display_state: blocked ? "muted" : "transitioning",
                            hydration_visible: !blocked,
                            read_only: true,
                            can_control_scheduler: false,
                            can_control_execution: false
                        }
                    };
                }

                function adaptive(generation = 1) {
                    return {
                        refinement_density: "medium",
                        refinement_load: 0.45,
                        boundary_priority: 0.5,
                        interior_stability: 0.4,
                        refinement_budget: 1,
                        adaptive_generation: generation
                    };
                }

                function ambiguity(candidate_group, generation = 1) {
                    return {
                        ambiguity_continuity_group_id: candidate_group,
                        ambiguity_confidence: 0.55,
                        ambiguity_overlap: 0.4,
                        candidate_refinement_ids: ["candidate-a", "candidate-b"],
                        uncertainty_generation: generation,
                        ambiguity_status: "unresolved"
                    };
                }

                function adjacent_candidate(field, generation, direction, source) {
                    return {
                        adjacent_candidate_field_id: field,
                        adjacent_candidate_direction: direction,
                        adjacency_weight: 0.62,
                        adjacent_candidate_source_candidate_group: source,
                        adjacent_candidate_generation: generation,
                        adjacent_candidate_status: "unresolved"
                    };
                }

                function aggregate_candidate(field, generation, contributors, status = "exploratory") {
                    return {
                        aggregate_candidate_field_id: field,
                        aggregate_candidate_generation: generation,
                        aggregate_weight: contributors.length / 3,
                        aggregate_candidate_contributors: contributors,
                        aggregate_candidate_status: status,
                        aggregate_candidate_lineage: contributors,
                        aggregate_candidate_scope: "current_viewport"
                    };
                }

                const east = sandbox.hydrateAggregateCandidate(envelope("rm:v1:em-east", 3), {
                    namespace: "east",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-a", 1),
                    adjacent_candidate: adjacent_candidate("imp-east", 1, "east", "candidate_group-a"),
                    aggregate_candidate: aggregate_candidate("aggregate_candidate-a", 1, ["imp-east", "candidate_group-a"])
                });
                const north = sandbox.hydrateAggregateCandidate(envelope("rm:v1:em-north", 5), {
                    namespace: "north",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-a", 1),
                    adjacent_candidate: adjacent_candidate("imp-north", 1, "north", "candidate_group-a"),
                    aggregate_candidate: aggregate_candidate("aggregate_candidate-b", 1, ["imp-north", "candidate_group-a"])
                });
                const convergence = sandbox.hydrateAggregateCandidate(envelope("rm:v1:em-converged", 7), {
                    namespace: "converged",
                    viewport_scope: viewportA,
                    adaptive: adaptive(2),
                    ambiguity: ambiguity("candidate_group-a", 2),
                    adjacent_candidate: adjacent_candidate("imp-converged", 2, "northeast", "candidate_group-a"),
                    aggregate_candidate: aggregate_candidate("aggregate_candidate-converged", 1, ["imp-east", "imp-north", "candidate_group-a"])
                });
                const convergenceRefined = sandbox.hydrateAggregateCandidate(envelope("rm:v1:em-converged-refined", 9), {
                    namespace: "converged",
                    viewport_scope: viewportA,
                    adaptive: adaptive(3),
                    ambiguity: ambiguity("candidate_group-a", 3),
                    adjacent_candidate: adjacent_candidate("imp-converged", 3, "east-northeast", "candidate_group-a"),
                    aggregate_candidate: aggregate_candidate("aggregate_candidate-converged", 2, ["imp-east", "imp-north", "candidate_group-a"], "strengthened")
                });
                const olderConvergence = sandbox.hydrateAggregateCandidate(envelope("rm:v1:em-old", 11), {
                    namespace: "converged",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-a", 1),
                    adjacent_candidate: adjacent_candidate("imp-converged", 1, "northeast", "candidate_group-a"),
                    aggregate_candidate: aggregate_candidate("aggregate_candidate-converged", 1, ["imp-east"], "exploratory")
                });
                const stale = sandbox.hydrateAggregateCandidate(envelope("rm:v1:stale", 13, "stale"), {
                    namespace: "stale",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-stale", 1),
                    adjacent_candidate: adjacent_candidate("imp-stale", 1, "west", "candidate_group-stale"),
                    aggregate_candidate: aggregate_candidate("aggregate_candidate-stale", 1, ["imp-stale"])
                });
                const cancelled = sandbox.hydrateAggregateCandidate(envelope("rm:v1:cancelled", 15, "cancelled"), {
                    namespace: "cancelled",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-cancelled", 1),
                    adjacent_candidate: adjacent_candidate("imp-cancelled", 1, "south", "candidate_group-cancelled"),
                    aggregate_candidate: aggregate_candidate("aggregate_candidate-cancelled", 1, ["imp-cancelled"])
                });
                const afterAggregateCandidate = sandbox.inspect();
                const rawPayload = sandbox.hydrateAggregateCandidate({
                    ...envelope("rm:v1:raw", 17),
                    hydration: {
                        ...envelope("rm:v1:raw", 17).hydration,
                        hydration: {
                            ...envelope("rm:v1:raw", 17).hydration.hydration,
                            features: [{ geometry: { coordinates: [0, 0] } }]
                        }
                    }
                }, {
                    namespace: "raw",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-raw", 1),
                    adjacent_candidate: adjacent_candidate("imp-raw", 1, "nearby", "candidate_group-raw"),
                    aggregate_candidate: aggregate_candidate("aggregate_candidate-raw", 1, ["imp-raw"])
                });
                const invalidateNorth = sandbox.invalidateAggregateCandidate("aggregate_candidate-b", "aggregate_candidate_superseded");
                const afterInvalidate = sandbox.inspect();
                const shiftToB = sandbox.setViewportScope(viewportB);
                const gammaB = sandbox.hydrateAggregateCandidate(envelope("rm:v1:em-gamma-b", 19), {
                    namespace: "gamma",
                    viewport_scope: viewportB,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-gamma", 1),
                    adjacent_candidate: adjacent_candidate("imp-gamma", 1, "northwest", "candidate_group-gamma"),
                    aggregate_candidate: aggregate_candidate("aggregate_candidate-gamma", 1, ["imp-gamma", "candidate_group-gamma"])
                });
                const afterViewportB = sandbox.inspect();
                const removeAll = sandbox.removeAll();
                const finalInspect = sandbox.inspect();
                const domNodes = Array.from(root.querySelectorAll(
                    "." + window.RelocationSamplingCacheAggregateCandidateFieldSandbox.OVERLAY_CLASS
                ));
                const serialized = JSON.stringify({
                    east,
                    north,
                    convergence,
                    convergenceRefined,
                    olderConvergence,
                    stale,
                    cancelled,
                    afterAggregateCandidate,
                    rawPayload,
                    invalidateNorth,
                    afterInvalidate,
                    shiftToB,
                    gammaB,
                    afterViewportB,
                    removeAll,
                    finalInspect
                });
                window.fetch = originalFetch;
                return {
                    multiple_adjacent_candidate_fields_converge_deterministically:
                        east.accepted === true &&
                        north.accepted === true &&
                        convergence.accepted === true &&
                        convergence.aggregate_candidate.aggregate_candidate_contributors.length === 3 &&
                        afterAggregateCandidate.overlays.map(item => item.namespace).join(",") === "east,north,converged",
                    aggregate_candidate_supersession_resolves_correctly:
                        convergenceRefined.action === "aggregate_candidate_superseded" &&
                        convergenceRefined.superseded_overlay_id === convergence.overlay_id &&
                        convergenceRefined.aggregate_candidate.aggregate_candidate_generation === 2 &&
                        olderConvergence.accepted === false &&
                        olderConvergence.reason === "older_aggregate_candidate_generation",
                    aggregate_candidate_invalidation_cleans_up:
                        invalidateNorth.invalidated === true &&
                        !afterInvalidate.overlays.some(item => item.aggregate_candidate_field_id === "aggregate_candidate-b"),
                    unresolved_aggregate_candidate_visible_safely:
                        east.visible === true &&
                        east.aggregate_candidate.aggregate_candidate_status === "exploratory" &&
                        east.aggregate_candidate_confirmed_truth_claimed === false &&
                        east.interpretation_boundary_preserved === true,
                    stale_cancelled_aggregate_candidate_do_not_display:
                        stale.accepted === false &&
                        stale.visible === false &&
                        cancelled.accepted === false &&
                        cancelled.visible === false,
                    viewport_isolation_survives_aggregate_candidate:
                        shiftToB.accepted === true &&
                        JSON.stringify([...shiftToB.invalidated].sort()) === JSON.stringify(["converged", "east"]) &&
                        gammaB.accepted === true &&
                        gammaB.viewport_id === "viewport-b" &&
                        afterViewportB.overlays.every(item => item.viewport_id === "viewport-b"),
                    namespace_isolation_survives_aggregate_candidate:
                        afterAggregateCandidate.overlays.some(item => item.namespace === "east") &&
                        afterAggregateCandidate.overlays.some(item => item.namespace === "north") &&
                        afterAggregateCandidate.overlays.some(item => item.namespace === "converged"),
                    adaptive_density_continuity_survives_aggregate_candidate:
                        east.density_affects_activity_not_truth === true &&
                        convergenceRefined.adaptive.adaptive_generation === 3 &&
                        afterAggregateCandidate.overlays.every(item => item.density_affects_activity_not_truth === true),
                    adjacent_candidate_continuity_survives_aggregate_candidate:
                        convergence.adjacent_candidate.adjacent_candidate_field_id === "imp-converged" &&
                        convergence.aggregate_candidate.aggregate_candidate_contributors.includes("imp-east") &&
                        convergence.aggregate_candidate.aggregate_candidate_contributors.includes("imp-north"),
                    production_renderer_untouched:
                        window.__productionRendererOwner === "legacy_search_regions" &&
                        window.__productionOverlayLifecycleTouched === false &&
                        east.renderer_ownership_claimed === false &&
                        convergenceRefined.renderer_ownership_claimed === false,
                    no_overlay_registry_contamination:
                        window.__productionOverlayRegistry.length === 0 &&
                        east.production_registry_mutated === false &&
                        convergenceRefined.production_registry_mutated === false &&
                        removeAll.production_registry_mutated === false,
                    no_dom_writes_escape_sandbox_root:
                        document.querySelectorAll(".production-overlay").length === 0 &&
                        removeAll.removed === true &&
                        domNodes.length === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    renderer_substrate_legacy:
                        east.rendererSubstrate === "legacy_search_regions" &&
                        convergenceRefined.rendererSubstrate === "legacy_search_regions" &&
                        window.RelocationSamplingCacheAggregateCandidateFieldSandbox.RENDERER_SUBSTRATE ===
                            "legacy_search_regions",
                    raw_payload_rejected:
                        rawPayload.accepted === false &&
                        rawPayload.reason === "raw_or_forbidden_field_present",
                    aggregate_candidate_truth_semantics_honest:
                        afterAggregateCandidate.overlays.every(item =>
                            item.aggregate_candidate_confirmed_truth_claimed === false &&
                            item.interpretation_boundary_preserved === true &&
                            item.recommendation_boundary_preserved === true &&
                            item.predictive_authority_boundary_preserved === true &&
                            item.aggregate_continuity_claimed === false &&
                            item.no_visual_theater_surface === true &&
                            item.final_truth_claimed === false
                        ),
                    no_fetch_occurs: fetchCalls.length === 0,
                    raw_payload_not_exposed:
                        !serialized.includes('"features"') &&
                        !serialized.includes('"coordinates"') &&
                        !serialized.includes('"geometry"') &&
                        !serialized.includes("raw_payload") &&
                        !serialized.includes("renderer_output") &&
                        !serialized.includes("leaflet_layers") &&
                        !serialized.includes("aura_mode") &&
                        !serialized.includes("virga_mode")
                };
            }""",
            sources,
        )
        browser.close()
        return result


def main() -> int:
    result = run_browser_probe()
    checks = [
        "multiple_adjacent_candidate_fields_converge_deterministically",
        "aggregate_candidate_supersession_resolves_correctly",
        "aggregate_candidate_invalidation_cleans_up",
        "unresolved_aggregate_candidate_visible_safely",
        "stale_cancelled_aggregate_candidate_do_not_display",
        "viewport_isolation_survives_aggregate_candidate",
        "namespace_isolation_survives_aggregate_candidate",
        "adaptive_density_continuity_survives_aggregate_candidate",
        "adjacent_candidate_continuity_survives_aggregate_candidate",
        "production_renderer_untouched",
        "no_overlay_registry_contamination",
        "no_dom_writes_escape_sandbox_root",
        "renderer_substrate_legacy",
        "raw_payload_rejected",
        "aggregate_candidate_truth_semantics_honest",
        "no_fetch_occurs",
        "raw_payload_not_exposed",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_22_aggregate_candidate_field_sandbox",
                "pass": all(result[name] for name in checks),
                "detail": result,
            }
        ]
    }
    payload["all_pass"] = all(item["pass"] for item in payload["results"])
    print(json.dumps(payload, indent=2))
    return 0 if payload["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
