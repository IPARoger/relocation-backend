#!/usr/bin/env python3
"""Browser smoke for the Phase 2.23 cross-candidate_group continuity sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_cross_domain_continuity_sandbox.js",
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
                    throw new Error("fetch not allowed in Phase 2.23 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                const root = document.createElement("div");
                root.id = "phase2-23-isolated-root";
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
                const sandbox = window.RelocationSamplingCacheCrossCandidateGroupContinuitySandbox
                    .createCrossCandidateGroupContinuitySandbox({ root, viewport_scope: viewportA });

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

                function adjacent_candidate(field, source) {
                    return {
                        adjacent_candidate_field_id: field,
                        adjacent_candidate_direction: "nearby",
                        adjacency_weight: 0.62,
                        adjacent_candidate_source_candidate_group: source,
                        adjacent_candidate_generation: 1,
                        adjacent_candidate_status: "unresolved"
                    };
                }

                function aggregate_candidate(field, contributors) {
                    return {
                        aggregate_candidate_field_id: field,
                        aggregate_candidate_generation: 1,
                        aggregate_weight: contributors.length / 4,
                        aggregate_candidate_contributors: contributors,
                        aggregate_candidate_status: "exploratory",
                        aggregate_candidate_lineage: contributors,
                        aggregate_candidate_scope: "current_viewport"
                    };
                }

                function candidate_group(id, generation, contributors, status = "coexisting") {
                    return {
                        continuity_group_id: id,
                        continuity_group_generation: generation,
                        continuity_group_lineage: contributors,
                        contributing_groups: contributors,
                        continuity_status: status,
                        coexistence_scope: "current_viewport"
                    };
                }

                const house = sandbox.hydrateCandidateGroup(envelope("rm:v1:house", 3), {
                    namespace: "house",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    adjacent_candidate: adjacent_candidate("imp-house", "house-placement"),
                    aggregate_candidate: aggregate_candidate("em-house", ["house-placement"]),
                    candidate_group: candidate_group("house-placement", 1, ["house-placement"])
                });
                const angle = sandbox.hydrateCandidateGroup(envelope("rm:v1:angle", 5), {
                    namespace: "angle",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    adjacent_candidate: adjacent_candidate("imp-angle", "angularity"),
                    aggregate_candidate: aggregate_candidate("em-angle", ["angularity"]),
                    candidate_group: candidate_group("angularity", 1, ["angularity"])
                });
                const cross = sandbox.hydrateCandidateGroup(envelope("rm:v1:cross", 7), {
                    namespace: "cross",
                    viewport_scope: viewportA,
                    adaptive: adaptive(2),
                    adjacent_candidate: adjacent_candidate("imp-cross", "house-placement"),
                    aggregate_candidate: aggregate_candidate("em-cross", ["house-placement", "angularity"]),
                    candidate_group: candidate_group("cross-candidate_group-bridge", 1, ["house-placement", "angularity"], "structural_continuity")
                });
                const crossRefined = sandbox.hydrateCandidateGroup(envelope("rm:v1:cross-refined", 9), {
                    namespace: "cross",
                    viewport_scope: viewportA,
                    adaptive: adaptive(3),
                    adjacent_candidate: adjacent_candidate("imp-cross-refined", "angularity"),
                    aggregate_candidate: aggregate_candidate("em-cross", ["house-placement", "angularity", "aspect"]),
                    candidate_group: candidate_group("cross-candidate_group-bridge", 2, ["house-placement", "angularity", "aspect"], "structural_continuity")
                });
                const olderCross = sandbox.hydrateCandidateGroup(envelope("rm:v1:cross-old", 11), {
                    namespace: "cross",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    adjacent_candidate: adjacent_candidate("imp-cross-old", "house-placement"),
                    aggregate_candidate: aggregate_candidate("em-cross", ["house-placement"]),
                    candidate_group: candidate_group("cross-candidate_group-bridge", 1, ["house-placement"], "coexisting")
                });
                const stale = sandbox.hydrateCandidateGroup(envelope("rm:v1:stale", 13, "stale"), {
                    namespace: "stale",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    adjacent_candidate: adjacent_candidate("imp-stale", "aspect"),
                    aggregate_candidate: aggregate_candidate("em-stale", ["aspect"]),
                    candidate_group: candidate_group("aspect", 1, ["aspect"])
                });
                const cancelled = sandbox.hydrateCandidateGroup(envelope("rm:v1:cancelled", 15, "cancelled"), {
                    namespace: "cancelled",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    adjacent_candidate: adjacent_candidate("imp-cancelled", "sign-angle"),
                    aggregate_candidate: aggregate_candidate("em-cancelled", ["sign-angle"]),
                    candidate_group: candidate_group("sign-angle", 1, ["sign-angle"])
                });
                const afterCandidateGroups = sandbox.inspect();
                const rawPayload = sandbox.hydrateCandidateGroup({
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
                    adjacent_candidate: adjacent_candidate("imp-raw", "raw-candidate_group"),
                    aggregate_candidate: aggregate_candidate("em-raw", ["raw-candidate_group"]),
                    candidate_group: candidate_group("raw-candidate_group", 1, ["raw-candidate_group"])
                });
                const invalidateAngle = sandbox.invalidateCandidateGroup("angularity", "candidate_group_superseded");
                const afterInvalidate = sandbox.inspect();
                const shiftToB = sandbox.setViewportScope(viewportB);
                const gammaB = sandbox.hydrateCandidateGroup(envelope("rm:v1:gamma-b", 19), {
                    namespace: "gamma",
                    viewport_scope: viewportB,
                    adaptive: adaptive(1),
                    adjacent_candidate: adjacent_candidate("imp-gamma", "future-analysis"),
                    aggregate_candidate: aggregate_candidate("em-gamma", ["future-analysis"]),
                    candidate_group: candidate_group("future-analysis", 1, ["future-analysis"])
                });
                const afterViewportB = sandbox.inspect();
                const removeAll = sandbox.removeAll();
                const finalInspect = sandbox.inspect();
                const domNodes = Array.from(root.querySelectorAll(
                    "." + window.RelocationSamplingCacheCrossCandidateGroupContinuitySandbox.OVERLAY_CLASS
                ));
                const serialized = JSON.stringify({
                    house,
                    angle,
                    cross,
                    crossRefined,
                    olderCross,
                    stale,
                    cancelled,
                    afterCandidateGroups,
                    rawPayload,
                    invalidateAngle,
                    afterInvalidate,
                    shiftToB,
                    gammaB,
                    afterViewportB,
                    removeAll,
                    finalInspect
                });
                window.fetch = originalFetch;
                return {
                    multiple_candidate_groups_coexist_deterministically:
                        house.accepted === true &&
                        angle.accepted === true &&
                        cross.accepted === true &&
                        afterCandidateGroups.overlays.map(item => item.namespace).join(",") === "house,angle,cross",
                    cross_candidate_group_continuity_persists_safely:
                        cross.candidate_group.continuity_status === "structural_continuity" &&
                        cross.candidate_group.contributing_groups.includes("house-placement") &&
                        cross.candidate_group.contributing_groups.includes("angularity") &&
                        cross.interpretation_boundary_preserved === true,
                    cross_candidate_group_adjacent_candidate_continuity_survives:
                        cross.adjacent_candidate.adjacent_candidate_source_candidate_group === "house-placement" &&
                        crossRefined.adjacent_candidate.adjacent_candidate_source_candidate_group === "angularity",
                    cross_candidate_group_aggregate_candidate_continuity_survives:
                        cross.aggregate_candidate.aggregate_candidate_contributors.length === 2 &&
                        crossRefined.aggregate_candidate.aggregate_candidate_contributors.includes("aspect"),
                    invalidation_cleans_up_correctly:
                        invalidateAngle.invalidated === true &&
                        !afterInvalidate.overlays.some(item => item.continuity_group_id === "angularity"),
                    stale_cancelled_candidate_groups_do_not_display:
                        stale.accepted === false &&
                        stale.visible === false &&
                        cancelled.accepted === false &&
                        cancelled.visible === false,
                    viewport_isolation_survives_cross_candidate_group:
                        shiftToB.accepted === true &&
                        JSON.stringify([...shiftToB.invalidated].sort()) === JSON.stringify(["cross", "house"]) &&
                        gammaB.accepted === true &&
                        gammaB.viewport_id === "viewport-b" &&
                        afterViewportB.overlays.every(item => item.viewport_id === "viewport-b"),
                    namespace_isolation_survives_cross_candidate_group:
                        afterCandidateGroups.overlays.some(item => item.namespace === "house") &&
                        afterCandidateGroups.overlays.some(item => item.namespace === "angle") &&
                        afterCandidateGroups.overlays.some(item => item.namespace === "cross"),
                    adaptive_continuity_survives_cross_candidate_group:
                        house.density_affects_activity_not_truth === true &&
                        crossRefined.adaptive.adaptive_generation === 3 &&
                        afterCandidateGroups.overlays.every(item => item.density_affects_activity_not_truth === true),
                    candidate_group_supersession_deterministic:
                        crossRefined.action === "candidate_group_continuity_superseded" &&
                        crossRefined.superseded_overlay_id === cross.overlay_id &&
                        olderCross.accepted === false &&
                        olderCross.reason === "older_continuity_group_generation",
                    production_renderer_untouched:
                        window.__productionRendererOwner === "legacy_search_regions" &&
                        window.__productionOverlayLifecycleTouched === false &&
                        house.renderer_ownership_claimed === false &&
                        crossRefined.renderer_ownership_claimed === false,
                    no_overlay_registry_contamination:
                        window.__productionOverlayRegistry.length === 0 &&
                        house.production_registry_mutated === false &&
                        crossRefined.production_registry_mutated === false &&
                        removeAll.production_registry_mutated === false,
                    no_dom_writes_escape_sandbox_root:
                        document.querySelectorAll(".production-overlay").length === 0 &&
                        removeAll.removed === true &&
                        domNodes.length === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    renderer_substrate_legacy:
                        house.rendererSubstrate === "legacy_search_regions" &&
                        crossRefined.rendererSubstrate === "legacy_search_regions" &&
                        window.RelocationSamplingCacheCrossCandidateGroupContinuitySandbox.RENDERER_SUBSTRATE ===
                            "legacy_search_regions",
                    raw_payload_rejected:
                        rawPayload.accepted === false &&
                        rawPayload.reason === "raw_or_forbidden_field_present",
                    cross_candidate_group_truth_semantics_honest:
                        afterCandidateGroups.overlays.every(item =>
                            item.interpretation_boundary_preserved === true &&
                            item.no_unified_meaning_surface === true &&
                            item.recommendation_boundary_preserved === true &&
                            item.convergence_validates_truth_claimed === false &&
                            item.scoring_boundary_preserved === true &&
                            item.forbidden_recommendation_surface_absent === true &&
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
        "multiple_candidate_groups_coexist_deterministically",
        "cross_candidate_group_continuity_persists_safely",
        "cross_candidate_group_adjacent_candidate_continuity_survives",
        "cross_candidate_group_aggregate_candidate_continuity_survives",
        "invalidation_cleans_up_correctly",
        "stale_cancelled_candidate_groups_do_not_display",
        "viewport_isolation_survives_cross_candidate_group",
        "namespace_isolation_survives_cross_candidate_group",
        "adaptive_continuity_survives_cross_candidate_group",
        "candidate_group_supersession_deterministic",
        "production_renderer_untouched",
        "no_overlay_registry_contamination",
        "no_dom_writes_escape_sandbox_root",
        "renderer_substrate_legacy",
        "raw_payload_rejected",
        "cross_candidate_group_truth_semantics_honest",
        "no_fetch_occurs",
        "raw_payload_not_exposed",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_23_cross_candidate_group_continuity_sandbox",
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
