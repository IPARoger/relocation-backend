#!/usr/bin/env python3
"""Browser smoke for the Phase 2.19 adaptive density sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_adaptive_density_sandbox.js",
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
                    throw new Error("fetch not allowed in Phase 2.19 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                const root = document.createElement("div");
                root.id = "phase2-19-isolated-root";
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
                const sandbox = window.RelocationSamplingCacheAdaptiveDensitySandbox
                    .createAdaptiveDensitySandbox({ root, viewport_scope: viewportA });

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
                            discovery_state: blocked ? "none" : "runtime_structure_available",
                            display_state: blocked ? "muted" : "active",
                            hydration_visible: !blocked,
                            read_only: true,
                            can_control_scheduler: false,
                            can_control_execution: false
                        }
                    };
                }

                function adaptive(density, pressure, boundary, stability, budget, generation) {
                    return {
                        refinement_density: density,
                        refinement_load: pressure,
                        boundary_priority: boundary,
                        interior_stability: stability,
                        refinement_budget: budget,
                        adaptive_generation: generation
                    };
                }

                const batch = sandbox.planAdaptiveBatch([
                    {
                        envelope: envelope("rm:v1:edge", 9),
                        options: {
                            namespace: "edge",
                            viewport_scope: viewportA,
                            adaptive: adaptive("high", 0.95, 1, 0.2, 2, 1)
                        }
                    },
                    {
                        envelope: envelope("rm:v1:interior", 5),
                        options: {
                            namespace: "interior",
                            viewport_scope: viewportA,
                            adaptive: adaptive("sparse", 0.05, 0, 0.95, 2, 1)
                        }
                    },
                    {
                        envelope: envelope("rm:v1:mid", 7),
                        options: {
                            namespace: "mid",
                            viewport_scope: viewportA,
                            adaptive: adaptive("medium", 0.5, 0.4, 0.5, 2, 1)
                        }
                    }
                ], { refinement_budget: 2 });
                const afterBatch = sandbox.inspect();
                const edgeRefined = sandbox.hydrateAdaptive(envelope("rm:v1:edge-refined", 13), {
                    namespace: "edge",
                    viewport_scope: viewportA,
                    adaptive: adaptive("high", 0.98, 1, 0.15, 2, 2)
                });
                const olderEdge = sandbox.hydrateAdaptive(envelope("rm:v1:edge-old", 11), {
                    namespace: "edge",
                    viewport_scope: viewportA,
                    adaptive: adaptive("high", 0.9, 1, 0.2, 2, 1)
                });
                const stale = sandbox.hydrateAdaptive(envelope("rm:v1:stale", 15, "stale"), {
                    namespace: "stale",
                    viewport_scope: viewportA,
                    adaptive: adaptive("high", 1, 1, 0, 1, 1)
                });
                const cancelled = sandbox.hydrateAdaptive(envelope("rm:v1:cancelled", 17, "cancelled"), {
                    namespace: "cancelled",
                    viewport_scope: viewportA,
                    adaptive: adaptive("high", 1, 1, 0, 1, 1)
                });
                const afterSupersession = sandbox.inspect();
                const rawPayload = sandbox.hydrateAdaptive({
                    ...envelope("rm:v1:raw", 19),
                    hydration: {
                        ...envelope("rm:v1:raw", 19).hydration,
                        hydration: {
                            ...envelope("rm:v1:raw", 19).hydration.hydration,
                            features: [{ geometry: { coordinates: [0, 0] } }]
                        }
                    }
                }, {
                    namespace: "raw",
                    viewport_scope: viewportA,
                    adaptive: adaptive("high", 1, 1, 0, 1, 1)
                });
                const shiftToB = sandbox.setViewportScope(viewportB);
                const gammaB = sandbox.hydrateAdaptive(envelope("rm:v1:gamma-b", 21), {
                    namespace: "gamma",
                    viewport_scope: viewportB,
                    adaptive: adaptive("medium", 0.4, 0.3, 0.6, 1, 1)
                });
                const afterViewportB = sandbox.inspect();
                const removeAll = sandbox.removeAll();
                const finalInspect = sandbox.inspect();
                const domNodes = Array.from(root.querySelectorAll(
                    "." + window.RelocationSamplingCacheAdaptiveDensitySandbox.OVERLAY_CLASS
                ));
                const serialized = JSON.stringify({
                    batch,
                    afterBatch,
                    edgeRefined,
                    olderEdge,
                    stale,
                    cancelled,
                    afterSupersession,
                    rawPayload,
                    shiftToB,
                    gammaB,
                    afterViewportB,
                    removeAll,
                    finalInspect
                });
                window.fetch = originalFetch;
                return {
                    adaptive_density_refines_deterministically:
                        batch.accepted === true &&
                        batch.applied.length === 2 &&
                        batch.applied[0].namespace === "edge" &&
                        batch.applied[1].namespace === "mid",
                    edge_priority_supersedes_correctly:
                        edgeRefined.accepted === true &&
                        edgeRefined.action === "adaptively_refined" &&
                        edgeRefined.superseded_overlay_id !== null &&
                        afterSupersession.overlays.find(item => item.namespace === "edge").adaptive_generation === 2,
                    sparse_interiors_remain_stable:
                        batch.deferred.length === 1 &&
                        batch.deferred[0].namespace === "interior" &&
                        batch.deferred[0].stable_sparse_interior === true &&
                        batch.deferred[0].interior_stability === 0.95,
                    refinement_continuity_survives_density_changes:
                        edgeRefined.density_affects_activity_not_truth === true &&
                        edgeRefined.final_truth_claimed === false &&
                        afterSupersession.overlays.every(item => item.final_truth_claimed === false),
                    refinement_budgets_constrain_growth:
                        batch.budget === 2 &&
                        afterBatch.overlay_count === 2 &&
                        afterBatch.pending_count === 1,
                    stale_cancelled_adaptive_do_not_display:
                        stale.accepted === false &&
                        stale.visible === false &&
                        cancelled.accepted === false &&
                        cancelled.visible === false,
                    viewport_isolation_survives_adaptive_refinement:
                        shiftToB.accepted === true &&
                        JSON.stringify([...shiftToB.invalidated].sort()) === JSON.stringify(["edge", "mid"]) &&
                        gammaB.accepted === true &&
                        gammaB.viewport_id === "viewport-b" &&
                        afterViewportB.overlays.every(item => item.viewport_id === "viewport-b"),
                    namespace_isolation_survives_adaptive_refinement:
                        afterSupersession.overlays.some(item => item.namespace === "edge") &&
                        afterSupersession.overlays.some(item => item.namespace === "mid") &&
                        !afterSupersession.overlays.some(item => item.namespace === "interior") &&
                        olderEdge.accepted === false &&
                        olderEdge.reason === "older_adaptive_generation",
                    production_renderer_untouched:
                        window.__productionRendererOwner === "legacy_search_regions" &&
                        window.__productionOverlayLifecycleTouched === false &&
                        batch.renderer_ownership_claimed === false &&
                        edgeRefined.renderer_ownership_claimed === false,
                    no_overlay_registry_contamination:
                        window.__productionOverlayRegistry.length === 0 &&
                        batch.production_registry_mutated === false &&
                        edgeRefined.production_registry_mutated === false &&
                        removeAll.production_registry_mutated === false,
                    no_dom_writes_escape_sandbox_root:
                        document.querySelectorAll(".production-overlay").length === 0 &&
                        removeAll.removed === true &&
                        domNodes.length === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    renderer_substrate_legacy:
                        batch.rendererSubstrate === "legacy_search_regions" &&
                        edgeRefined.rendererSubstrate === "legacy_search_regions" &&
                        window.RelocationSamplingCacheAdaptiveDensitySandbox.RENDERER_SUBSTRATE ===
                            "legacy_search_regions",
                    raw_payload_rejected:
                        rawPayload.accepted === false &&
                        rawPayload.reason === "raw_or_forbidden_field_present",
                    density_truth_semantics_honest:
                        batch.density_affects_activity_not_truth === true &&
                        edgeRefined.density_affects_activity_not_truth === true &&
                        afterSupersession.overlays.every(item => item.density_affects_activity_not_truth === true),
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
        "adaptive_density_refines_deterministically",
        "edge_priority_supersedes_correctly",
        "sparse_interiors_remain_stable",
        "refinement_continuity_survives_density_changes",
        "refinement_budgets_constrain_growth",
        "stale_cancelled_adaptive_do_not_display",
        "viewport_isolation_survives_adaptive_refinement",
        "namespace_isolation_survives_adaptive_refinement",
        "production_renderer_untouched",
        "no_overlay_registry_contamination",
        "no_dom_writes_escape_sandbox_root",
        "renderer_substrate_legacy",
        "raw_payload_rejected",
        "density_truth_semantics_honest",
        "no_fetch_occurs",
        "raw_payload_not_exposed",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_19_adaptive_density_sandbox",
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
