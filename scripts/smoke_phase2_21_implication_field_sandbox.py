#!/usr/bin/env python3
"""Browser smoke for the Phase 2.21 adjacent_candidate field sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_implication_field_sandbox.js",
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
                    throw new Error("fetch not allowed in Phase 2.21 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                const root = document.createElement("div");
                root.id = "phase2-21-isolated-root";
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
                const sandbox = window.RelocationSamplingCacheAdjacentCandidateFieldSandbox
                    .createAdjacentCandidateFieldSandbox({ root, viewport_scope: viewportA });

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

                function adjacent_candidate(field, generation, direction, source, status = "unresolved") {
                    return {
                        adjacent_candidate_field_id: field,
                        adjacent_candidate_direction: direction,
                        adjacency_weight: 0.62,
                        adjacent_candidate_source_candidate_group: source,
                        adjacent_candidate_generation: generation,
                        adjacent_candidate_status: status
                    };
                }

                const east = sandbox.hydrateAdjacentCandidate(envelope("rm:v1:imp-east", 3), {
                    namespace: "east",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-a", 1),
                    adjacent_candidate: adjacent_candidate("imp-east", 1, "east", "candidate_group-a")
                });
                const north = sandbox.hydrateAdjacentCandidate(envelope("rm:v1:imp-north", 5), {
                    namespace: "north",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-a", 1),
                    adjacent_candidate: adjacent_candidate("imp-north", 1, "north", "candidate_group-a")
                });
                const eastRefined = sandbox.hydrateAdjacentCandidate(envelope("rm:v1:imp-east-refined", 7), {
                    namespace: "east",
                    viewport_scope: viewportA,
                    adaptive: adaptive(2),
                    ambiguity: ambiguity("candidate_group-a", 2),
                    adjacent_candidate: adjacent_candidate("imp-east", 2, "east-northeast", "candidate_group-a", "strengthened")
                });
                const olderEast = sandbox.hydrateAdjacentCandidate(envelope("rm:v1:imp-east-old", 9), {
                    namespace: "east",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-a", 1),
                    adjacent_candidate: adjacent_candidate("imp-east", 1, "east", "candidate_group-a")
                });
                const stale = sandbox.hydrateAdjacentCandidate(envelope("rm:v1:stale", 11, "stale"), {
                    namespace: "stale",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-stale", 1),
                    adjacent_candidate: adjacent_candidate("imp-stale", 1, "west", "candidate_group-stale")
                });
                const cancelled = sandbox.hydrateAdjacentCandidate(envelope("rm:v1:cancelled", 13, "cancelled"), {
                    namespace: "cancelled",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-cancelled", 1),
                    adjacent_candidate: adjacent_candidate("imp-cancelled", 1, "south", "candidate_group-cancelled")
                });
                const afterAdjacentCandidates = sandbox.inspect();
                const rawPayload = sandbox.hydrateAdjacentCandidate({
                    ...envelope("rm:v1:raw", 15),
                    hydration: {
                        ...envelope("rm:v1:raw", 15).hydration,
                        hydration: {
                            ...envelope("rm:v1:raw", 15).hydration.hydration,
                            features: [{ geometry: { coordinates: [0, 0] } }]
                        }
                    }
                }, {
                    namespace: "raw",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-raw", 1),
                    adjacent_candidate: adjacent_candidate("imp-raw", 1, "nearby", "candidate_group-raw")
                });
                const invalidateNorth = sandbox.invalidateAdjacentCandidate("imp-north", "adjacent_candidate_superseded");
                const afterInvalidate = sandbox.inspect();
                const shiftToB = sandbox.setViewportScope(viewportB);
                const gammaB = sandbox.hydrateAdjacentCandidate(envelope("rm:v1:imp-gamma-b", 17), {
                    namespace: "gamma",
                    viewport_scope: viewportB,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-gamma", 1),
                    adjacent_candidate: adjacent_candidate("imp-gamma", 1, "northwest", "candidate_group-gamma")
                });
                const afterViewportB = sandbox.inspect();
                const removeAll = sandbox.removeAll();
                const finalInspect = sandbox.inspect();
                const domNodes = Array.from(root.querySelectorAll(
                    "." + window.RelocationSamplingCacheAdjacentCandidateFieldSandbox.OVERLAY_CLASS
                ));
                const serialized = JSON.stringify({
                    east,
                    north,
                    eastRefined,
                    olderEast,
                    stale,
                    cancelled,
                    afterAdjacentCandidates,
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
                    adjacent_candidate_fields_coexist_deterministically:
                        east.accepted === true &&
                        north.accepted === true &&
                        afterAdjacentCandidates.overlays.map(item => item.namespace).join(",") === "east,north",
                    ambiguity_candidate_groups_imply_nearby_structure_safely:
                        east.ambiguity.ambiguity_continuity_group_id === "candidate_group-a" &&
                        east.adjacent_candidate.adjacent_candidate_source_candidate_group === "candidate_group-a" &&
                        east.adjacent_candidate.adjacent_candidate_confirmed_truth_claimed === false,
                    adjacent_candidate_supersession_resolves_correctly:
                        eastRefined.action === "adjacent_candidate_superseded" &&
                        eastRefined.superseded_overlay_id === east.overlay_id &&
                        eastRefined.adjacent_candidate.adjacent_candidate_generation === 2 &&
                        olderEast.accepted === false &&
                        olderEast.reason === "older_adjacent_candidate_generation",
                    adjacent_candidate_invalidation_cleans_up:
                        invalidateNorth.invalidated === true &&
                        !afterInvalidate.overlays.some(item => item.adjacent_candidate_field_id === "imp-north"),
                    unresolved_adjacent_candidates_visible_safely:
                        north.visible === true &&
                        north.adjacent_candidate.adjacent_candidate_status === "unresolved" &&
                        north.adjacent_candidate_confirmed_truth_claimed === false &&
                        north.directional_continuity_claimed === false,
                    stale_cancelled_adjacent_candidates_do_not_display:
                        stale.accepted === false &&
                        stale.visible === false &&
                        cancelled.accepted === false &&
                        cancelled.visible === false,
                    viewport_isolation_survives_adjacent_candidates:
                        shiftToB.accepted === true &&
                        JSON.stringify([...shiftToB.invalidated].sort()) === JSON.stringify(["east"]) &&
                        gammaB.accepted === true &&
                        gammaB.viewport_id === "viewport-b" &&
                        afterViewportB.overlays.every(item => item.viewport_id === "viewport-b"),
                    namespace_isolation_survives_adjacent_candidates:
                        afterAdjacentCandidates.overlays.some(item => item.namespace === "east") &&
                        afterAdjacentCandidates.overlays.some(item => item.namespace === "north") &&
                        afterAdjacentCandidates.overlays.every(item => item.adjacent_candidate_source_candidate_group === "candidate_group-a"),
                    adaptive_density_continuity_survives_adjacent_candidates:
                        east.density_affects_activity_not_truth === true &&
                        eastRefined.adaptive.adaptive_generation === 2 &&
                        afterAdjacentCandidates.overlays.every(item => item.density_affects_activity_not_truth === true),
                    production_renderer_untouched:
                        window.__productionRendererOwner === "legacy_search_regions" &&
                        window.__productionOverlayLifecycleTouched === false &&
                        east.renderer_ownership_claimed === false &&
                        eastRefined.renderer_ownership_claimed === false,
                    no_overlay_registry_contamination:
                        window.__productionOverlayRegistry.length === 0 &&
                        east.production_registry_mutated === false &&
                        eastRefined.production_registry_mutated === false &&
                        removeAll.production_registry_mutated === false,
                    no_dom_writes_escape_sandbox_root:
                        document.querySelectorAll(".production-overlay").length === 0 &&
                        removeAll.removed === true &&
                        domNodes.length === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    renderer_substrate_legacy:
                        east.rendererSubstrate === "legacy_search_regions" &&
                        eastRefined.rendererSubstrate === "legacy_search_regions" &&
                        window.RelocationSamplingCacheAdjacentCandidateFieldSandbox.RENDERER_SUBSTRATE ===
                            "legacy_search_regions",
                    raw_payload_rejected:
                        rawPayload.accepted === false &&
                        rawPayload.reason === "raw_or_forbidden_field_present",
                    adjacent_candidate_truth_semantics_honest:
                        afterAdjacentCandidates.overlays.every(item =>
                            item.adjacent_candidate_confirmed_truth_claimed === false &&
                            item.directional_continuity_claimed === false &&
                            item.ontology_boundary_preserved === true &&
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
        "adjacent_candidate_fields_coexist_deterministically",
        "ambiguity_candidate_groups_imply_nearby_structure_safely",
        "adjacent_candidate_supersession_resolves_correctly",
        "adjacent_candidate_invalidation_cleans_up",
        "unresolved_adjacent_candidates_visible_safely",
        "stale_cancelled_adjacent_candidates_do_not_display",
        "viewport_isolation_survives_adjacent_candidates",
        "namespace_isolation_survives_adjacent_candidates",
        "adaptive_density_continuity_survives_adjacent_candidates",
        "production_renderer_untouched",
        "no_overlay_registry_contamination",
        "no_dom_writes_escape_sandbox_root",
        "renderer_substrate_legacy",
        "raw_payload_rejected",
        "adjacent_candidate_truth_semantics_honest",
        "no_fetch_occurs",
        "raw_payload_not_exposed",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_21_adjacent_candidate_field_sandbox",
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
