#!/usr/bin/env python3
"""Browser smoke for the Phase 2.17 viewport hydration sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_viewport_hydration_sandbox.js",
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
                    throw new Error("fetch not allowed in Phase 2.17 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                window.__productionViewportOwner = "production-map";
                const root = document.createElement("div");
                root.id = "phase2-17-isolated-root";
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
                const sandbox = window.RelocationSamplingCacheViewportHydrationSandbox
                    .createViewportHydrationSandbox({ root, viewport_scope: viewportA });

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

                const createA = sandbox.hydrateOverlay(envelope("rm:v1:a", 3), {
                    namespace: "alpha",
                    viewport_scope: viewportA
                });
                const createB = sandbox.hydrateOverlay(envelope("rm:v1:b", 5), {
                    namespace: "beta",
                    viewport_scope: viewportA
                });
                const afterViewportA = sandbox.inspect();
                const alphaViewportAttr = root
                    .querySelector('[data-overlay-namespace="alpha"]')
                    ?.getAttribute("data-viewport-id");
                const betaViewportAttr = root
                    .querySelector('[data-overlay-namespace="beta"]')
                    ?.getAttribute("data-viewport-id");
                const wrongViewportAttempt = sandbox.hydrateOverlay(envelope("rm:v1:wrong", 7), {
                    namespace: "wrong",
                    viewport_scope: viewportB
                });
                const shiftToB = sandbox.setViewportScope(viewportB);
                const afterShift = sandbox.inspect();
                const replaceAlphaB = sandbox.replaceOverlay("alpha", envelope("rm:v1:a-b", 11), {
                    viewport_scope: viewportB
                });
                const createGammaB = sandbox.hydrateOverlay(envelope("rm:v1:g-b", 13), {
                    namespace: "gamma",
                    viewport_scope: viewportB
                });
                const afterViewportB = sandbox.inspect();
                const stale = sandbox.hydrateOverlay(envelope("rm:v1:stale", 17, "stale"), {
                    namespace: "stale",
                    viewport_scope: viewportB
                });
                const cancelled = sandbox.hydrateOverlay(envelope("rm:v1:cancelled", 19, "cancelled"), {
                    namespace: "cancelled",
                    viewport_scope: viewportB
                });
                const rawPayload = sandbox.hydrateOverlay({
                    ...envelope("rm:v1:raw", 23),
                    hydration: {
                        ...envelope("rm:v1:raw", 23).hydration,
                        hydration: {
                            ...envelope("rm:v1:raw", 23).hydration.hydration,
                            features: [{ geometry: { coordinates: [0, 0] } }]
                        }
                    }
                }, { namespace: "raw", viewport_scope: viewportB });
                const removeGamma = sandbox.removeOverlay("gamma");
                const afterRemoveGamma = sandbox.inspect();
                const removeAll = sandbox.removeAll();
                const finalInspect = sandbox.inspect();
                const domNodes = Array.from(root.querySelectorAll(
                    "." + window.RelocationSamplingCacheViewportHydrationSandbox.OVERLAY_CLASS
                ));
                const serialized = JSON.stringify({
                    createA,
                    createB,
                    afterViewportA,
                    wrongViewportAttempt,
                    shiftToB,
                    afterShift,
                    replaceAlphaB,
                    createGammaB,
                    afterViewportB,
                    stale,
                    cancelled,
                    rawPayload,
                    removeGamma,
                    afterRemoveGamma,
                    removeAll,
                    finalInspect
                });
                window.fetch = originalFetch;
                return {
                    overlays_bound_to_viewport_scope:
                        createA.accepted === true &&
                        createB.accepted === true &&
                        alphaViewportAttr === "viewport-a" &&
                        betaViewportAttr === "viewport-a" &&
                        afterViewportA.overlays.every(item => item.viewport_id === "viewport-a"),
                    viewport_shift_invalidates_stale_overlays:
                        shiftToB.accepted === true &&
                        JSON.stringify([...shiftToB.invalidated].sort()) === JSON.stringify(["alpha", "beta"]) &&
                        afterShift.overlay_count === 0 &&
                        afterShift.viewport_id === "viewport-b",
                    replacement_supersedes_after_viewport_change:
                        wrongViewportAttempt.accepted === false &&
                        wrongViewportAttempt.reason === "viewport_scope_mismatch" &&
                        replaceAlphaB.accepted === true &&
                        replaceAlphaB.viewport_id === "viewport-b" &&
                        replaceAlphaB.cache_key === "rm:v1:a-b",
                    deterministic_ordering_survives_viewport_transitions:
                        JSON.stringify(afterViewportA.overlays.map(item => item.namespace)) ===
                            JSON.stringify(["alpha", "beta"]) &&
                        JSON.stringify(afterViewportB.overlays.map(item => item.namespace)) ===
                            JSON.stringify(["alpha", "gamma"]) &&
                        afterViewportB.overlays[0].viewport_id === "viewport-b" &&
                        afterViewportB.overlays[1].viewport_id === "viewport-b",
                    out_of_scope_cleanup_correct:
                        afterShift.dom_overlay_count === 0 &&
                        afterRemoveGamma.overlays.every(item => item.namespace !== "gamma") &&
                        removeAll.removed === true &&
                        finalInspect.overlay_count === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    namespace_isolation_survives_viewport_changes:
                        afterViewportB.overlays.some(item =>
                            item.namespace === "alpha" && item.cache_key === "rm:v1:a-b"
                        ) &&
                        afterViewportB.overlays.some(item =>
                            item.namespace === "gamma" && item.cache_key === "rm:v1:g-b"
                        ) &&
                        !afterViewportB.overlays.some(item => item.viewport_id === "viewport-a"),
                    cancelled_stale_do_not_display:
                        stale.accepted === false &&
                        stale.visible === false &&
                        cancelled.accepted === false &&
                        cancelled.visible === false,
                    production_renderer_untouched:
                        window.__productionRendererOwner === "legacy_search_regions" &&
                        window.__productionViewportOwner === "production-map" &&
                        window.__productionOverlayLifecycleTouched === false &&
                        createA.renderer_ownership_claimed === false &&
                        createA.viewport_ownership_claimed === false,
                    no_overlay_registry_contamination:
                        window.__productionOverlayRegistry.length === 0 &&
                        createA.production_registry_mutated === false &&
                        replaceAlphaB.production_registry_mutated === false &&
                        removeAll.production_registry_mutated === false,
                    no_dom_writes_escape_sandbox_root:
                        document.querySelectorAll(".production-overlay").length === 0 &&
                        domNodes.length === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    renderer_substrate_legacy:
                        createA.rendererSubstrate === "legacy_search_regions" &&
                        shiftToB.rendererSubstrate === "legacy_search_regions" &&
                        window.RelocationSamplingCacheViewportHydrationSandbox.RENDERER_SUBSTRATE ===
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
        "overlays_bound_to_viewport_scope",
        "viewport_shift_invalidates_stale_overlays",
        "replacement_supersedes_after_viewport_change",
        "deterministic_ordering_survives_viewport_transitions",
        "out_of_scope_cleanup_correct",
        "namespace_isolation_survives_viewport_changes",
        "cancelled_stale_do_not_display",
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
                "test": "phase2_17_viewport_hydration_sandbox",
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
