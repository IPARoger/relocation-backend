#!/usr/bin/env python3
"""Browser smoke for the Phase 2.20 ambiguity candidate_group sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_ambiguity_domain_sandbox.js",
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
                    throw new Error("fetch not allowed in Phase 2.20 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                const root = document.createElement("div");
                root.id = "phase2-20-isolated-root";
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
                const sandbox = window.RelocationSamplingCacheAmbiguityCandidateGroupSandbox
                    .createAmbiguityCandidateGroupSandbox({ root, viewport_scope: viewportA });

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
                            discovery_state: blocked ? "none" : "unresolved_ambiguity",
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
                        refinement_load: 0.5,
                        boundary_priority: 0.5,
                        interior_stability: 0.4,
                        refinement_budget: 1,
                        adaptive_generation: generation
                    };
                }

                function ambiguity(candidate_group, generation, status = "unresolved", candidates = []) {
                    return {
                        ambiguity_continuity_group_id: candidate_group,
                        ambiguity_confidence: 0.55,
                        ambiguity_overlap: candidates.length > 1 ? 0.72 : 0.2,
                        candidate_refinement_ids: candidates,
                        uncertainty_generation: generation,
                        ambiguity_status: status
                    };
                }

                const candidate_groupA = sandbox.hydrateAmbiguity(envelope("rm:v1:amb-a", 3), {
                    namespace: "alpha",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-a", 1, "unresolved", ["cand-a1", "cand-a2"])
                });
                const candidate_groupB = sandbox.hydrateAmbiguity(envelope("rm:v1:amb-b", 5), {
                    namespace: "beta",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-b", 1, "unresolved", ["cand-b1"])
                });
                const overlap = sandbox.hydrateAmbiguity(envelope("rm:v1:amb-overlap", 7), {
                    namespace: "overlap",
                    viewport_scope: viewportA,
                    adaptive: adaptive(2),
                    ambiguity: ambiguity("candidate_group-overlap", 1, "overlapping_candidates", ["cand-a2", "cand-b1"])
                });
                const resolvedA = sandbox.hydrateAmbiguity(envelope("rm:v1:amb-a-resolved", 9), {
                    namespace: "alpha",
                    viewport_scope: viewportA,
                    adaptive: adaptive(2),
                    ambiguity: ambiguity("candidate_group-a", 2, "resolved_candidate", ["cand-a2"])
                });
                const olderA = sandbox.hydrateAmbiguity(envelope("rm:v1:amb-a-old", 11), {
                    namespace: "alpha",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-a", 1, "unresolved", ["cand-a1"])
                });
                const stale = sandbox.hydrateAmbiguity(envelope("rm:v1:stale", 13, "stale"), {
                    namespace: "stale",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-stale", 1, "unresolved", ["stale-candidate"])
                });
                const cancelled = sandbox.hydrateAmbiguity(envelope("rm:v1:cancelled", 15, "cancelled"), {
                    namespace: "cancelled",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-cancelled", 1, "unresolved", ["cancelled-candidate"])
                });
                const afterAmbiguity = sandbox.inspect();
                const rawPayload = sandbox.hydrateAmbiguity({
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
                    ambiguity: ambiguity("candidate_group-raw", 1, "unresolved", ["raw-candidate"])
                });
                const invalidateB = sandbox.invalidateAmbiguity("candidate_group-b", "candidate_group_superseded");
                const afterInvalidate = sandbox.inspect();
                const shiftToB = sandbox.setViewportScope(viewportB);
                const gammaB = sandbox.hydrateAmbiguity(envelope("rm:v1:amb-gamma-b", 19), {
                    namespace: "gamma",
                    viewport_scope: viewportB,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("candidate_group-gamma", 1, "unresolved", ["cand-g1", "cand-g2"])
                });
                const afterViewportB = sandbox.inspect();
                const removeAll = sandbox.removeAll();
                const finalInspect = sandbox.inspect();
                const domNodes = Array.from(root.querySelectorAll(
                    "." + window.RelocationSamplingCacheAmbiguityCandidateGroupSandbox.OVERLAY_CLASS
                ));
                const serialized = JSON.stringify({
                    candidate_groupA,
                    candidate_groupB,
                    overlap,
                    resolvedA,
                    olderA,
                    stale,
                    cancelled,
                    afterAmbiguity,
                    rawPayload,
                    invalidateB,
                    afterInvalidate,
                    shiftToB,
                    gammaB,
                    afterViewportB,
                    removeAll,
                    finalInspect
                });
                window.fetch = originalFetch;
                return {
                    ambiguity_candidate_groups_coexist_deterministically:
                        candidate_groupA.accepted === true &&
                        candidate_groupB.accepted === true &&
                        overlap.accepted === true &&
                        afterAmbiguity.overlays.map(item => item.namespace).join(",") === "alpha,beta,overlap",
                    overlapping_candidates_preserve_continuity:
                        overlap.ambiguity.ambiguity_status === "overlapping_candidates" &&
                        overlap.ambiguity.candidate_refinement_ids.length === 2 &&
                        overlap.overlapping_candidates_confirmed_truth === false,
                    ambiguity_supersession_resolves_correctly:
                        resolvedA.action === "ambiguity_superseded" &&
                        resolvedA.superseded_overlay_id === candidate_groupA.overlay_id &&
                        resolvedA.ambiguity.uncertainty_generation === 2 &&
                        olderA.accepted === false &&
                        olderA.reason === "older_uncertainty_generation",
                    unresolved_ambiguity_visible_safely:
                        candidate_groupB.visible === true &&
                        candidate_groupB.ambiguity.ambiguity_status === "unresolved" &&
                        candidate_groupB.ambiguity_is_error === false &&
                        candidate_groupB.unresolved_structure_invalid === false,
                    ambiguity_invalidation_cleans_up:
                        invalidateB.invalidated === true &&
                        !afterInvalidate.overlays.some(item => item.ambiguity_continuity_group_id === "candidate_group-b"),
                    stale_cancelled_ambiguity_do_not_display:
                        stale.accepted === false &&
                        stale.visible === false &&
                        cancelled.accepted === false &&
                        cancelled.visible === false,
                    viewport_isolation_survives_ambiguity:
                        shiftToB.accepted === true &&
                        JSON.stringify([...shiftToB.invalidated].sort()) === JSON.stringify(["alpha", "overlap"]) &&
                        gammaB.accepted === true &&
                        gammaB.viewport_id === "viewport-b" &&
                        afterViewportB.overlays.every(item => item.viewport_id === "viewport-b"),
                    namespace_isolation_survives_ambiguity:
                        afterAmbiguity.overlays.some(item => item.namespace === "alpha") &&
                        afterAmbiguity.overlays.some(item => item.namespace === "beta") &&
                        afterAmbiguity.overlays.some(item => item.namespace === "overlap"),
                    adaptive_density_continuity_survives_ambiguity:
                        candidate_groupA.density_affects_activity_not_truth === true &&
                        resolvedA.adaptive.adaptive_generation === 2 &&
                        afterAmbiguity.overlays.every(item => item.density_affects_activity_not_truth === true),
                    production_renderer_untouched:
                        window.__productionRendererOwner === "legacy_search_regions" &&
                        window.__productionOverlayLifecycleTouched === false &&
                        candidate_groupA.renderer_ownership_claimed === false &&
                        resolvedA.renderer_ownership_claimed === false,
                    no_overlay_registry_contamination:
                        window.__productionOverlayRegistry.length === 0 &&
                        candidate_groupA.production_registry_mutated === false &&
                        resolvedA.production_registry_mutated === false &&
                        removeAll.production_registry_mutated === false,
                    no_dom_writes_escape_sandbox_root:
                        document.querySelectorAll(".production-overlay").length === 0 &&
                        removeAll.removed === true &&
                        domNodes.length === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    renderer_substrate_legacy:
                        candidate_groupA.rendererSubstrate === "legacy_search_regions" &&
                        resolvedA.rendererSubstrate === "legacy_search_regions" &&
                        window.RelocationSamplingCacheAmbiguityCandidateGroupSandbox.RENDERER_SUBSTRATE ===
                            "legacy_search_regions",
                    raw_payload_rejected:
                        rawPayload.accepted === false &&
                        rawPayload.reason === "raw_or_forbidden_field_present",
                    ambiguity_truth_semantics_honest:
                        afterAmbiguity.overlays.every(item =>
                            item.ambiguity_is_error === false &&
                            item.overlapping_candidates_confirmed_truth === false &&
                            item.unresolved_structure_invalid === false &&
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
        "ambiguity_candidate_groups_coexist_deterministically",
        "overlapping_candidates_preserve_continuity",
        "ambiguity_supersession_resolves_correctly",
        "unresolved_ambiguity_visible_safely",
        "ambiguity_invalidation_cleans_up",
        "stale_cancelled_ambiguity_do_not_display",
        "viewport_isolation_survives_ambiguity",
        "namespace_isolation_survives_ambiguity",
        "adaptive_density_continuity_survives_ambiguity",
        "production_renderer_untouched",
        "no_overlay_registry_contamination",
        "no_dom_writes_escape_sandbox_root",
        "renderer_substrate_legacy",
        "raw_payload_rejected",
        "ambiguity_truth_semantics_honest",
        "no_fetch_occurs",
        "raw_payload_not_exposed",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_20_ambiguity_candidate_group_sandbox",
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
