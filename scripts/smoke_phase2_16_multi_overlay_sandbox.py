#!/usr/bin/env python3
"""Browser smoke for the Phase 2.16 multi-overlay coexistence sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_multi_overlay_sandbox.js",
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
                    throw new Error("fetch not allowed in Phase 2.16 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                const root = document.createElement("div");
                root.id = "phase2-16-isolated-root";
                document.body.appendChild(root);
                sources.forEach(source => eval(source));
                const sandbox = window.RelocationSamplingCacheMultiOverlaySandbox
                    .createMultiOverlaySandbox({ root });

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

                const createA = sandbox.hydrateOverlay(envelope("rm:v1:a", 3), { namespace: "alpha" });
                const createB = sandbox.hydrateOverlay(envelope("rm:v1:b", 5), { namespace: "beta" });
                const afterCreate = sandbox.inspect();
                const alphaCountAfterCreate = root.querySelectorAll('[data-overlay-namespace="alpha"]').length;
                const betaCountAfterCreate = root.querySelectorAll('[data-overlay-namespace="beta"]').length;
                const updateA = sandbox.hydrateOverlay(envelope("rm:v1:a2", 7), { namespace: "alpha" });
                const afterUpdate = sandbox.inspect();
                const replaceB = sandbox.replaceOverlay("beta", envelope("rm:v1:b2", 11));
                const afterReplace = sandbox.inspect();
                const cancelled = sandbox.hydrateOverlay(envelope("rm:v1:cancelled", 13, "cancelled"), {
                    namespace: "cancelled"
                });
                const stale = sandbox.hydrateOverlay(envelope("rm:v1:stale", 17, "stale"), {
                    namespace: "stale"
                });
                const invalidateA = sandbox.invalidateOverlay("alpha", "stale");
                const afterInvalidate = sandbox.inspect();
                const createC = sandbox.hydrateOverlay(envelope("rm:v1:c", 19), { namespace: "gamma" });
                const afterCreateC = sandbox.inspect();
                const rawPayload = sandbox.hydrateOverlay({
                    ...envelope("rm:v1:raw", 23),
                    hydration: {
                        ...envelope("rm:v1:raw", 23).hydration,
                        hydration: {
                            ...envelope("rm:v1:raw", 23).hydration.hydration,
                            geometry: { coordinates: [0, 0] }
                        }
                    }
                }, { namespace: "raw" });
                const removeB = sandbox.removeOverlay("beta");
                const afterRemoveB = sandbox.inspect();
                const removeAll = sandbox.removeAll();
                const finalInspect = sandbox.inspect();
                const domNodes = Array.from(root.querySelectorAll(
                    "." + window.RelocationSamplingCacheMultiOverlaySandbox.OVERLAY_CLASS
                ));
                const serialized = JSON.stringify({
                    createA,
                    createB,
                    afterCreate,
                    updateA,
                    afterUpdate,
                    replaceB,
                    afterReplace,
                    cancelled,
                    stale,
                    invalidateA,
                    afterInvalidate,
                    createC,
                    afterCreateC,
                    rawPayload,
                    removeB,
                    afterRemoveB,
                    removeAll,
                    finalInspect
                });
                window.fetch = originalFetch;
                return {
                    multiple_overlays_coexist_safely:
                        createA.accepted === true &&
                        createB.accepted === true &&
                        afterCreate.overlay_count === 2 &&
                        afterCreate.dom_overlay_count === 2,
                    overlay_namespaces_isolated:
                        JSON.stringify(afterCreate.overlays.map(item => item.namespace)) ===
                            JSON.stringify(["alpha", "beta"]) &&
                        alphaCountAfterCreate === 1 &&
                        betaCountAfterCreate === 1,
                    stale_overlays_invalidate_correctly:
                        stale.accepted === false &&
                        invalidateA.invalidated === true &&
                        afterInvalidate.overlays.every(item => item.namespace !== "alpha"),
                    replacement_overlays_supersede_correctly:
                        updateA.action === "updated" &&
                        updateA.overlay_count === 2 &&
                        afterUpdate.overlays.find(item => item.namespace === "alpha").feature_count === 7 &&
                        replaceB.action === "created" &&
                        afterReplace.overlays.find(item => item.namespace === "beta").cache_key === "rm:v1:b2",
                    cleanup_removal_works_fully:
                        removeB.removed === true &&
                        afterRemoveB.overlays.every(item => item.namespace !== "beta") &&
                        removeAll.removed === true &&
                        finalInspect.overlay_count === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    hydration_ordering_deterministic:
                        JSON.stringify(afterCreate.overlays.map(item => item.namespace)) ===
                            JSON.stringify(["alpha", "beta"]) &&
                        afterUpdate.overlays.find(item => item.namespace === "alpha").order === 1 &&
                        afterUpdate.overlays.find(item => item.namespace === "beta").order === 2 &&
                        afterCreateC.overlays.map(item => item.namespace).join(",") === "beta,gamma",
                    cancelled_overlays_do_not_display:
                        cancelled.accepted === false &&
                        cancelled.visible === false &&
                        !afterCreateC.overlays.some(item => item.namespace === "cancelled"),
                    production_renderer_untouched:
                        window.__productionRendererOwner === "legacy_search_regions" &&
                        window.__productionOverlayLifecycleTouched === false &&
                        createA.renderer_ownership_claimed === false &&
                        createC.renderer_ownership_claimed === false,
                    no_overlay_registry_contamination:
                        window.__productionOverlayRegistry.length === 0 &&
                        createA.production_registry_mutated === false &&
                        replaceB.production_registry_mutated === false &&
                        removeAll.production_registry_mutated === false,
                    no_dom_writes_escape_sandbox_root:
                        document.querySelectorAll(".production-overlay").length === 0 &&
                        domNodes.length === 0 &&
                        finalInspect.dom_overlay_count === 0,
                    renderer_substrate_legacy:
                        createA.rendererSubstrate === "legacy_search_regions" &&
                        afterReplace.rendererSubstrate === "legacy_search_regions" &&
                        window.RelocationSamplingCacheMultiOverlaySandbox.RENDERER_SUBSTRATE ===
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
        "multiple_overlays_coexist_safely",
        "overlay_namespaces_isolated",
        "stale_overlays_invalidate_correctly",
        "replacement_overlays_supersede_correctly",
        "cleanup_removal_works_fully",
        "hydration_ordering_deterministic",
        "cancelled_overlays_do_not_display",
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
                "test": "phase2_16_multi_overlay_sandbox",
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
