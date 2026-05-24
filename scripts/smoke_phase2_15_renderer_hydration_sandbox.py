#!/usr/bin/env python3
"""Browser smoke for the Phase 2.15 renderer hydration sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_renderer_hydration_sandbox.js",
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
                    throw new Error("fetch not allowed in Phase 2.15 smoke");
                };
                window.__productionOverlayRegistry = [];
                window.__productionRendererOwner = "legacy_search_regions";
                window.__productionOverlayLifecycleTouched = false;
                const root = document.createElement("div");
                root.id = "phase2-15-isolated-root";
                document.body.appendChild(root);
                const mutationRecords = [];
                const mutationObserver = new MutationObserver(records => mutationRecords.push(...records));
                mutationObserver.observe(document.body, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    characterData: true
                });
                sources.forEach(source => eval(source));
                const sandbox = window.RelocationSamplingCacheRendererHydrationSandbox
                    .createRendererHydrationSandbox({ root });
                const sanitizedEnvelope = {
                    hydration: {
                        schema_version: 1,
                        cache_key: "rm:v1:phase2-15",
                        compatible: true,
                        hydrated: true,
                        execution_required: false,
                        hydration: {
                            schema_version: 1,
                            key: "rm:v1:phase2-15",
                            status: "ready",
                            summary: { feature_count: 3, response_type: "FeatureCollection" },
                            metrics: { backend_status: 200 },
                            created_at_ms: 1000,
                            updated_at_ms: 1000,
                            expires_at_ms: 2000
                        }
                    },
                    execution: {
                        state: "completed",
                        job: {
                            cache_key: "rm:v1:phase2-15",
                            intent_group: "chart-a:sun-house-1",
                            generation: 1,
                            stale: false,
                            cancelled: false
                        }
                    },
                    observer: {
                        cache_key: "rm:v1:phase2-15",
                        observer_state: "hydration_eligible",
                        discovery_state: "confirmed_discovered_structure",
                        color_state: "colored",
                        hydration_visible: true,
                        read_only: true,
                        can_control_scheduler: false,
                        can_control_execution: false
                    }
                };
                const visibleResult = sandbox.hydrateOnce(sanitizedEnvelope);
                const visibleInspect = sandbox.inspect();
                const overlayNode = root.querySelector(
                    "." + window.RelocationSamplingCacheRendererHydrationSandbox.OVERLAY_CLASS
                );
                const staleResult = sandbox.hydrateOnce({
                    ...sanitizedEnvelope,
                    execution: {
                        state: "stale",
                        job: { ...sanitizedEnvelope.execution.job, state: "stale", stale: true }
                    },
                    observer: {
                        ...sanitizedEnvelope.observer,
                        observer_state: "stale",
                        hydration_visible: false
                    }
                });
                const cancelledResult = sandbox.hydrateOnce({
                    ...sanitizedEnvelope,
                    execution: {
                        state: "cancelled",
                        job: { ...sanitizedEnvelope.execution.job, state: "cancelled", cancelled: true }
                    },
                    observer: {
                        ...sanitizedEnvelope.observer,
                        observer_state: "cancelled",
                        hydration_visible: false
                    }
                });
                const rawPayloadResult = sandbox.hydrateOnce({
                    ...sanitizedEnvelope,
                    hydration: {
                        ...sanitizedEnvelope.hydration,
                        hydration: {
                            ...sanitizedEnvelope.hydration.hydration,
                            features: [{ geometry: { coordinates: [0, 0] } }]
                        }
                    }
                });
                const secondVisibleResult = sandbox.hydrateOnce(sanitizedEnvelope);
                const removed = sandbox.removeOverlay();
                const finalInspect = sandbox.inspect();
                const serialized = JSON.stringify({
                    visibleResult,
                    visibleInspect,
                    staleResult,
                    cancelledResult,
                    rawPayloadResult,
                    secondVisibleResult,
                    removed,
                    finalInspect
                });
                mutationObserver.disconnect();
                window.fetch = originalFetch;
                return {
                    sanitized_hydration_visible:
                        visibleResult.accepted === true &&
                        visibleResult.visible === true &&
                        overlayNode !== null &&
                        overlayNode.dataset.rendererSubstrate === "legacy_search_regions" &&
                        overlayNode.dataset.devOnly === "true",
                    production_renderer_untouched:
                        window.__productionRendererOwner === "legacy_search_regions" &&
                        window.__productionOverlayLifecycleTouched === false &&
                        visibleResult.renderer_ownership_claimed === false,
                    sandbox_overlay_isolated:
                        visibleResult.overlay_kind === "isolated_dev_dom_overlay" &&
                        visibleInspect.overlay_count === 1 &&
                        document.querySelectorAll(".production-overlay").length === 0,
                    no_renderer_ownership_transfer:
                        visibleResult.rendererSubstrate === "legacy_search_regions" &&
                        visibleInspect.rendererSubstrate === "legacy_search_regions" &&
                        secondVisibleResult.renderer_ownership_claimed === false,
                    metadata_governed:
                        visibleResult.metadata.status === "ready" &&
                        visibleResult.metadata.summary.feature_count === 3 &&
                        visibleResult.observer.read_only === true,
                    stale_cancelled_do_not_display:
                        staleResult.accepted === false &&
                        staleResult.visible === false &&
                        cancelledResult.accepted === false &&
                        cancelledResult.visible === false,
                    raw_payload_rejected:
                        rawPayloadResult.accepted === false &&
                        rawPayloadResult.reason === "raw_or_forbidden_field_present",
                    no_persistent_overlay_state:
                        visibleResult.persisted === false &&
                        removed.persisted === false &&
                        finalInspect.persisted === false,
                    no_overlay_registry_contamination:
                        window.__productionOverlayRegistry.length === 0 &&
                        visibleResult.production_registry_mutated === false &&
                        secondVisibleResult.production_registry_mutated === false,
                    overlay_removal_clean:
                        removed.removed === true &&
                        removed.overlay_count === 0 &&
                        finalInspect.visible === false &&
                        finalInspect.overlay_count === 0,
                    renderer_substrate_legacy:
                        visibleResult.rendererSubstrate === "legacy_search_regions" &&
                        removed.rendererSubstrate === "legacy_search_regions" &&
                        window.RelocationSamplingCacheRendererHydrationSandbox.RENDERER_SUBSTRATE ===
                            "legacy_search_regions",
                    only_sandbox_dom_mutates:
                        root.querySelectorAll(
                            "." + window.RelocationSamplingCacheRendererHydrationSandbox.OVERLAY_CLASS
                        ).length === 0 &&
                        document.querySelectorAll(".production-overlay").length === 0 &&
                        window.__productionOverlayLifecycleTouched === false,
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
        "sanitized_hydration_visible",
        "production_renderer_untouched",
        "sandbox_overlay_isolated",
        "no_renderer_ownership_transfer",
        "metadata_governed",
        "stale_cancelled_do_not_display",
        "raw_payload_rejected",
        "no_persistent_overlay_state",
        "no_overlay_registry_contamination",
        "overlay_removal_clean",
        "renderer_substrate_legacy",
        "only_sandbox_dom_mutates",
        "no_fetch_occurs",
        "raw_payload_not_exposed",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_15_renderer_hydration_sandbox",
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
