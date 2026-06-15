#!/usr/bin/env python3
"""Browser smoke for the Phase 2.18 progressive refinement sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_progressive_refinement_sandbox.js",
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
                    throw new Error("fetch not allowed in Phase 2.18 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                const root = document.createElement("div");
                root.id = "phase2-18-isolated-root";
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
                const sandbox = window.RelocationSamplingCacheProgressiveRefinementSandbox
                    .createProgressiveRefinementSandbox({ root, viewport_scope: viewportA });

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
                            discovery_state: blocked ? "none" : "confirmed_discovered_structure",
                            color_state: blocked ? "muted" : "colored",
                            hydration_visible: !blocked,
                            read_only: true,
                            can_control_scheduler: false,
                            can_control_execution: false
                        }
                    };
                }

                function refinement(level, generation, parent = null, status = "provisional") {
                    return {
                        refinement_level: level,
                        parent_overlay_id: parent,
                        refinement_generation: generation,
                        refinement_scope: "current_viewport",
                        refinement_status: status
                    };
                }

                const coarse = sandbox.hydrateRefinement(envelope("rm:v1:coarse", 3), {
                    namespace: "alpha",
                    viewport_scope: viewportA,
                    refinement: refinement("coarse", 1)
                });
                const refined = sandbox.hydrateRefinement(envelope("rm:v1:refined", 9), {
                    namespace: "alpha",
                    viewport_scope: viewportA,
                    refinement: refinement("refined", 2, coarse.overlay_id)
                });
                const stale = sandbox.hydrateRefinement(envelope("rm:v1:stale", 11, "stale"), {
                    namespace: "alpha",
                    viewport_scope: viewportA,
                    refinement: refinement("refined", 3, refined.overlay_id)
                });
                const cancelled = sandbox.hydrateRefinement(envelope("rm:v1:cancelled", 13, "cancelled"), {
                    namespace: "alpha",
                    viewport_scope: viewportA,
                    refinement: refinement("refined", 4, refined.overlay_id)
                });
                const beta = sandbox.hydrateRefinement(envelope("rm:v1:beta-coarse", 5), {
                    namespace: "beta",
                    viewport_scope: viewportA,
                    refinement: refinement("coarse", 1)
                });
                const olderAttempt = sandbox.hydrateRefinement(envelope("rm:v1:older", 7), {
                    namespace: "alpha",
                    viewport_scope: viewportA,
                    refinement: refinement("coarse", 1, coarse.overlay_id)
                });
                const afterRefinement = sandbox.inspect();
                const rawPayload = sandbox.hydrateRefinement({
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
                    refinement: refinement("refined", 1)
                });
                const shiftToB = sandbox.setViewportScope(viewportB);
                const gammaB = sandbox.hydrateRefinement(envelope("rm:v1:gamma-b", 17), {
                    namespace: "gamma",
                    viewport_scope: viewportB,
                    refinement: refinement("coarse", 1)
                });
                const afterViewportB = sandbox.inspect();
                const invalidateGamma = sandbox.invalidateRefinement("gamma", "stale_refinement");
                const removeAll = sandbox.removeAll();
                const finalInspect = sandbox.inspect();
                const domNodes = Array.from(root.querySelectorAll(
                    "." + window.RelocationSamplingCacheProgressiveRefinementSandbox.OVERLAY_CLASS
                ));
                const serialized = JSON.stringify({
                    coarse,
                    refined,
                    stale,
                    cancelled,
                    beta,
                    olderAttempt,
                    afterRefinement,
                    rawPayload,
                    shiftToB,
                    gammaB,
                    afterViewportB,
                    invalidateGamma,
                    removeAll,
                    finalInspect
                });
                window.fetch = originalFetch;
                return {
                    coarse_refines_into_newer_overlay:
                        coarse.accepted === true &&
                        refined.accepted === true &&
                        refined.action === "refined" &&
                        refined.superseded_overlay_id === coarse.overlay_id &&
                        refined.overlay_count === 1,
                    refinement_supersession_deterministic:
                        afterRefinement.overlays.find(item => item.namespace === "alpha").cache_key === "rm:v1:refined" &&
                        afterRefinement.overlays.find(item => item.namespace === "alpha").refinement_generation === 2 &&
                        olderAttempt.accepted === false &&
                        olderAttempt.reason === "older_refinement_generation",
                    superseded_overlays_cleanup_correct:
                        root.querySelectorAll('[data-cache-key="rm:v1:coarse"]').length === 0 &&
                        root.querySelectorAll('[data-cache-key="rm:v1:refined"]').length === 0 &&
                        afterRefinement.dom_overlay_count === 2,
                    refinement_lineage_coherent:
                        refined.lineage.length === 2 &&
                        refined.lineage[0].overlay_id === coarse.overlay_id &&
                        refined.lineage[1].parent_overlay_id === coarse.overlay_id &&
                        refined.lineage[1].superseded_overlay_id === coarse.overlay_id,
                    stale_cancelled_refinements_do_not_display:
                        stale.accepted === false &&
                        stale.visible === false &&
                        cancelled.accepted === false &&
                        cancelled.visible === false,
                    viewport_isolation_survives_refinement:
                        shiftToB.accepted === true &&
                        JSON.stringify([...shiftToB.invalidated].sort()) === JSON.stringify(["alpha", "beta"]) &&
                        gammaB.accepted === true &&
                        gammaB.viewport_id === "viewport-b" &&
                        afterViewportB.overlays.every(item => item.viewport_id === "viewport-b"),
                    namespace_isolation_survives_refinement:
                        beta.accepted === true &&
                        afterRefinement.overlays.some(item => item.namespace === "alpha") &&
                        afterRefinement.overlays.some(item => item.namespace === "beta") &&
                        afterRefinement.overlays.length === 2,
                    truth_continuity_preserved:
                        coarse.truth_final === false &&
                        refined.truth_final === false &&
                        afterRefinement.overlays.every(item => item.truth_final === false) &&
                        refined.refinement.refinement_status === "provisional",
                    production_renderer_untouched:
                        window.__productionRendererOwner === "legacy_search_regions" &&
                        window.__productionOverlayLifecycleTouched === false &&
                        coarse.renderer_ownership_claimed === false &&
                        refined.renderer_ownership_claimed === false,
                    no_overlay_registry_contamination:
                        window.__productionOverlayRegistry.length === 0 &&
                        coarse.production_registry_mutated === false &&
                        refined.production_registry_mutated === false &&
                        removeAll.production_registry_mutated === false,
                    no_dom_writes_escape_sandbox_root:
                        document.querySelectorAll(".production-overlay").length === 0 &&
                        invalidateGamma.invalidated === true &&
                        removeAll.removed === true &&
                        domNodes.length === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    renderer_substrate_legacy:
                        coarse.rendererSubstrate === "legacy_search_regions" &&
                        refined.rendererSubstrate === "legacy_search_regions" &&
                        window.RelocationSamplingCacheProgressiveRefinementSandbox.RENDERER_SUBSTRATE ===
                            "legacy_search_regions",
                    raw_payload_rejected:
                        rawPayload.accepted === false &&
                        rawPayload.reason === "raw_or_forbidden_field_present",
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
        "coarse_refines_into_newer_overlay",
        "refinement_supersession_deterministic",
        "superseded_overlays_cleanup_correct",
        "refinement_lineage_coherent",
        "stale_cancelled_refinements_do_not_display",
        "viewport_isolation_survives_refinement",
        "namespace_isolation_survives_refinement",
        "truth_continuity_preserved",
        "production_renderer_untouched",
        "no_overlay_registry_contamination",
        "no_dom_writes_escape_sandbox_root",
        "renderer_substrate_legacy",
        "raw_payload_rejected",
        "no_fetch_occurs",
        "raw_payload_not_exposed",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_18_progressive_refinement_sandbox",
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
