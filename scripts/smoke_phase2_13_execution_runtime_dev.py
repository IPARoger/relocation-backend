#!/usr/bin/env python3
"""Browser smoke for the Phase 2.13 dev execution runtime."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_contract.js",
    ROOT / "sampling_cache_store_contract.js",
    ROOT / "sampling_cache_orchestration_contract.js",
    ROOT / "sampling_cache_execution_bridge_contract.js",
    ROOT / "sampling_cache_observer_contract.js",
    ROOT / "sampling_cache_execution_policy_contract.js",
    ROOT / "sampling_cache_execution_runtime_dev.js",
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
                    throw new Error("fetch not allowed in Phase 2.13 smoke");
                };
                const mutationRecords = [];
                const mutationObserver = new MutationObserver(records => mutationRecords.push(...records));
                mutationObserver.observe(document.documentElement, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    characterData: true
                });
                sources.forEach(source => eval(source));
                const runtime = window.RelocationSamplingCacheExecutionRuntimeDev.createExecutionRuntimeDev({
                    store_options: { ttl_ms: 1000, now: () => 1000 }
                });
                const savedInvestigation = {
                    chart_key: "chart-a",
                    house_conditions: [{ planet: "Sun", house: 1, slot: "A" }],
                    angle_sign_conditions: [{ angle: "MC", sign: "Capricorn" }],
                    aspect_overlay: { planet: "Saturn", aspect: "Square", angle: "DSC" },
                    viewport: { north: 10, south: -10, east: 20, west: -20, zoom: 4 },
                    sampling: { width: 1000, height: 700, block_px: 12, lat_cap: true },
                    intent_group: "chart-a:sun-house-1",
                    generation: 1,
                    renderer_substrate: "canonical_screen_space",
                    debug: true,
                    aura_mode: "raster",
                    fetch_url: "/screen-pixel-truth",
                    worker_id: "worker-1"
                };
                const result = runtime.executeOnce(savedInvestigation);
                const staleObserver = window.RelocationSamplingCacheObserverContract.createObserverEnvelope({
                    ...result.execution.job,
                    state: "stale",
                    stale: true,
                    hydration_eligible: false
                });
                const cancelledObserver = window.RelocationSamplingCacheObserverContract.createObserverEnvelope({
                    ...result.execution.job,
                    state: "cancelled",
                    cancelled: true,
                    hydration_eligible: false
                });
                const serialized = JSON.stringify({
                    result,
                    staleObserver,
                    cancelledObserver,
                    inspect: runtime.inspect()
                });
                mutationObserver.disconnect();
                window.fetch = originalFetch;
                return {
                    one_request_executes_successfully:
                        result.accepted === true &&
                        result.mode === "dev_single_request_only" &&
                        result.semantic_key.startsWith("rm:v1:"),
                    lifecycle_transitions_correct:
                        JSON.stringify(result.lifecycle) === JSON.stringify(["queued", "running", "completed"]) &&
                        result.execution.state === "completed",
                    cache_store_sanitized_metadata_only:
                        result.store.count === 1 &&
                        result.store.entries[0].payload_fields.includes("chart_key") &&
                        result.store.entries[0].value_fields.includes("status"),
                    hydration_sanitized:
                        result.hydration.hydrated === true &&
                        result.hydration.execution_required === false &&
                        result.hydration.hydration.status === "ready",
                    stale_cancelled_cannot_hydrate:
                        staleObserver.hydration_visible === false &&
                        cancelledObserver.hydration_visible === false,
                    policy_gates_respected:
                        result.policy.foreground_blocked === false &&
                        result.policy.decisions[0].decision === "run",
                    observer_read_only:
                        result.observer.read_only === true &&
                        result.observer.can_control_scheduler === false &&
                        result.observer.can_control_execution === false,
                    no_fetch_occurs: fetchCalls.length === 0,
                    no_renderer_map_takeover:
                        result.rendererSubstrate === "legacy_search_regions" &&
                        runtime.inspect().rendererSubstrate === "legacy_search_regions",
                    no_dom_map_writes: mutationRecords.length === 0,
                    single_request_reversible:
                        runtime.inspect().active === false &&
                        result.store.count === 1,
                    pollution_stripped:
                        !serialized.includes("canonical_screen_space") &&
                        !serialized.includes("debug") &&
                        !serialized.includes("aura_mode") &&
                        !serialized.includes("fetch_url") &&
                        !serialized.includes("worker_id") &&
                        !serialized.includes("renderer_output") &&
                        !serialized.includes("geojson") &&
                        !serialized.includes("canvas_pixels") &&
                        !serialized.includes("leaflet_layers")
                };
            }""",
            sources,
        )
        browser.close()
        return result


def main() -> int:
    result = run_browser_probe()
    checks = [
        "one_request_executes_successfully",
        "lifecycle_transitions_correct",
        "cache_store_sanitized_metadata_only",
        "hydration_sanitized",
        "stale_cancelled_cannot_hydrate",
        "policy_gates_respected",
        "observer_read_only",
        "no_fetch_occurs",
        "no_renderer_map_takeover",
        "no_dom_map_writes",
        "single_request_reversible",
        "pollution_stripped",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_13_execution_runtime_dev",
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
