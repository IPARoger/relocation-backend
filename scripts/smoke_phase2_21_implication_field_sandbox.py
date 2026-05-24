#!/usr/bin/env python3
"""Browser smoke for the Phase 2.21 implication field sandbox."""

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
                const sandbox = window.RelocationSamplingCacheImplicationFieldSandbox
                    .createImplicationFieldSandbox({ root, viewport_scope: viewportA });

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
                            discovery_state: blocked ? "none" : "implied_nearby_structure",
                            color_state: blocked ? "muted" : "transitioning",
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
                        refinement_pressure: 0.45,
                        boundary_priority: 0.5,
                        interior_stability: 0.4,
                        refinement_budget: 1,
                        adaptive_generation: generation
                    };
                }

                function ambiguity(domain, generation = 1) {
                    return {
                        ambiguity_domain_id: domain,
                        ambiguity_confidence: 0.55,
                        ambiguity_overlap: 0.4,
                        candidate_refinement_ids: ["candidate-a", "candidate-b"],
                        uncertainty_generation: generation,
                        ambiguity_status: "unresolved"
                    };
                }

                function implication(field, generation, direction, source, status = "unresolved") {
                    return {
                        implication_field_id: field,
                        implication_direction: direction,
                        implication_strength: 0.62,
                        implication_source_domain: source,
                        implication_generation: generation,
                        implication_status: status
                    };
                }

                const east = sandbox.hydrateImplication(envelope("rm:v1:imp-east", 3), {
                    namespace: "east",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("domain-a", 1),
                    implication: implication("imp-east", 1, "east", "domain-a")
                });
                const north = sandbox.hydrateImplication(envelope("rm:v1:imp-north", 5), {
                    namespace: "north",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("domain-a", 1),
                    implication: implication("imp-north", 1, "north", "domain-a")
                });
                const eastRefined = sandbox.hydrateImplication(envelope("rm:v1:imp-east-refined", 7), {
                    namespace: "east",
                    viewport_scope: viewportA,
                    adaptive: adaptive(2),
                    ambiguity: ambiguity("domain-a", 2),
                    implication: implication("imp-east", 2, "east-northeast", "domain-a", "strengthened")
                });
                const olderEast = sandbox.hydrateImplication(envelope("rm:v1:imp-east-old", 9), {
                    namespace: "east",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("domain-a", 1),
                    implication: implication("imp-east", 1, "east", "domain-a")
                });
                const stale = sandbox.hydrateImplication(envelope("rm:v1:stale", 11, "stale"), {
                    namespace: "stale",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("domain-stale", 1),
                    implication: implication("imp-stale", 1, "west", "domain-stale")
                });
                const cancelled = sandbox.hydrateImplication(envelope("rm:v1:cancelled", 13, "cancelled"), {
                    namespace: "cancelled",
                    viewport_scope: viewportA,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("domain-cancelled", 1),
                    implication: implication("imp-cancelled", 1, "south", "domain-cancelled")
                });
                const afterImplications = sandbox.inspect();
                const rawPayload = sandbox.hydrateImplication({
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
                    ambiguity: ambiguity("domain-raw", 1),
                    implication: implication("imp-raw", 1, "nearby", "domain-raw")
                });
                const invalidateNorth = sandbox.invalidateImplication("imp-north", "implication_superseded");
                const afterInvalidate = sandbox.inspect();
                const shiftToB = sandbox.setViewportScope(viewportB);
                const gammaB = sandbox.hydrateImplication(envelope("rm:v1:imp-gamma-b", 17), {
                    namespace: "gamma",
                    viewport_scope: viewportB,
                    adaptive: adaptive(1),
                    ambiguity: ambiguity("domain-gamma", 1),
                    implication: implication("imp-gamma", 1, "northwest", "domain-gamma")
                });
                const afterViewportB = sandbox.inspect();
                const removeAll = sandbox.removeAll();
                const finalInspect = sandbox.inspect();
                const domNodes = Array.from(root.querySelectorAll(
                    "." + window.RelocationSamplingCacheImplicationFieldSandbox.OVERLAY_CLASS
                ));
                const serialized = JSON.stringify({
                    east,
                    north,
                    eastRefined,
                    olderEast,
                    stale,
                    cancelled,
                    afterImplications,
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
                    implication_fields_coexist_deterministically:
                        east.accepted === true &&
                        north.accepted === true &&
                        afterImplications.overlays.map(item => item.namespace).join(",") === "east,north",
                    ambiguity_domains_imply_nearby_structure_safely:
                        east.ambiguity.ambiguity_domain_id === "domain-a" &&
                        east.implication.implication_source_domain === "domain-a" &&
                        east.implication.implication_is_confirmed_truth === false,
                    implication_supersession_resolves_correctly:
                        eastRefined.action === "implication_superseded" &&
                        eastRefined.superseded_overlay_id === east.overlay_id &&
                        eastRefined.implication.implication_generation === 2 &&
                        olderEast.accepted === false &&
                        olderEast.reason === "older_implication_generation",
                    implication_invalidation_cleans_up:
                        invalidateNorth.invalidated === true &&
                        !afterInvalidate.overlays.some(item => item.implication_field_id === "imp-north"),
                    unresolved_implications_visible_safely:
                        north.visible === true &&
                        north.implication.implication_status === "unresolved" &&
                        north.implication_is_confirmed_truth === false &&
                        north.directional_attraction_guarantees_outcome === false,
                    stale_cancelled_implications_do_not_display:
                        stale.accepted === false &&
                        stale.visible === false &&
                        cancelled.accepted === false &&
                        cancelled.visible === false,
                    viewport_isolation_survives_implications:
                        shiftToB.accepted === true &&
                        JSON.stringify([...shiftToB.invalidated].sort()) === JSON.stringify(["east"]) &&
                        gammaB.accepted === true &&
                        gammaB.viewport_id === "viewport-b" &&
                        afterViewportB.overlays.every(item => item.viewport_id === "viewport-b"),
                    namespace_isolation_survives_implications:
                        afterImplications.overlays.some(item => item.namespace === "east") &&
                        afterImplications.overlays.some(item => item.namespace === "north") &&
                        afterImplications.overlays.every(item => item.implication_source_domain === "domain-a"),
                    adaptive_density_continuity_survives_implications:
                        east.density_affects_activity_not_truth === true &&
                        eastRefined.adaptive.adaptive_generation === 2 &&
                        afterImplications.overlays.every(item => item.density_affects_activity_not_truth === true),
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
                        window.RelocationSamplingCacheImplicationFieldSandbox.RENDERER_SUBSTRATE ===
                            "legacy_search_regions",
                    raw_payload_rejected:
                        rawPayload.accepted === false &&
                        rawPayload.reason === "raw_or_forbidden_field_present",
                    implication_truth_semantics_honest:
                        afterImplications.overlays.every(item =>
                            item.implication_is_confirmed_truth === false &&
                            item.directional_attraction_guarantees_outcome === false &&
                            item.speculative_astrology_meaning_synthesized === false &&
                            item.truth_final === false
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
        "implication_fields_coexist_deterministically",
        "ambiguity_domains_imply_nearby_structure_safely",
        "implication_supersession_resolves_correctly",
        "implication_invalidation_cleans_up",
        "unresolved_implications_visible_safely",
        "stale_cancelled_implications_do_not_display",
        "viewport_isolation_survives_implications",
        "namespace_isolation_survives_implications",
        "adaptive_density_continuity_survives_implications",
        "production_renderer_untouched",
        "no_overlay_registry_contamination",
        "no_dom_writes_escape_sandbox_root",
        "renderer_substrate_legacy",
        "raw_payload_rejected",
        "implication_truth_semantics_honest",
        "no_fetch_occurs",
        "raw_payload_not_exposed",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_21_implication_field_sandbox",
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
