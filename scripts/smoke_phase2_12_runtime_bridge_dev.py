#!/usr/bin/env python3
"""Browser smoke for the Phase 2.12 dev runtime bridge."""

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
    ROOT / "sampling_cache_runtime_bridge_dev.js",
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
                    throw new Error("fetch not allowed in Phase 2.12 smoke");
                };
                const mutationRecords = [];
                const observer = new MutationObserver(records => mutationRecords.push(...records));
                observer.observe(document.documentElement, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    characterData: true
                });
                sources.forEach(source => eval(source));
                const bridge = window.RelocationSamplingCacheRuntimeBridgeDev.createDevRuntimeBridge({
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
                const miss = bridge.evaluate(savedInvestigation);
                bridge.seedCache(savedInvestigation, {
                    status: "ready",
                    summary: { matched: 12 },
                    metrics: { sample_count: 144 },
                    renderer_output: true,
                    geojson: { type: "FeatureCollection" },
                    canvas_pixels: "pixels",
                    leaflet_layers: ["layer"],
                    fetch_response: { ok: true },
                    worker_id: "worker-1"
                });
                const hit = bridge.evaluate(savedInvestigation);
                const staleCandidate = {
                    ...hit.execution.job,
                    state: "stale",
                    stale: true,
                    hydration_eligible: false
                };
                const staleObserver = window.RelocationSamplingCacheObserverContract.createObserverEnvelope(staleCandidate);
                const serialized = JSON.stringify({ miss, hit, inspect: bridge.inspect(), staleObserver });
                observer.disconnect();
                window.fetch = originalFetch;
                return {
                    bridge_loads_in_browser: Boolean(window.RelocationSamplingCacheRuntimeBridgeDev),
                    semantic_request_flows_through_chain:
                        miss.semantic_key &&
                        miss.semantic_key.startsWith("rm:v1:") &&
                        miss.execution.job.cache_key === miss.semantic_key &&
                        miss.policy.decisions[0].cache_key === miss.semantic_key,
                    cache_miss_metadata_would_run:
                        miss.outcome === "cache_miss" &&
                        miss.execution_required === false &&
                        miss.execution.state === "queued" &&
                        miss.policy.decisions[0].decision === "run",
                    cache_hit_sanitized_hydration:
                        hit.outcome === "cache_hit" &&
                        hit.hydration.hydrated === true &&
                        hit.hydration.execution_required === false &&
                        hit.execution.hydration_eligible === true,
                    stale_cancelled_cannot_hydrate:
                        staleObserver.observer_state === "stale" &&
                        staleObserver.hydration_visible === false,
                    observer_read_only:
                        hit.observer.read_only === true &&
                        hit.observer.can_control_scheduler === false &&
                        hit.observer.can_control_execution === false,
                    no_fetch_occurs: fetchCalls.length === 0,
                    no_dom_map_writes: mutationRecords.length === 0,
                    renderer_substrate_legacy:
                        miss.rendererSubstrate === "legacy_search_regions" &&
                        hit.rendererSubstrate === "legacy_search_regions" &&
                        bridge.inspect().rendererSubstrate === "legacy_search_regions",
                    pollution_stripped:
                        !serialized.includes("canonical_screen_space") &&
                        !serialized.includes("debug") &&
                        !serialized.includes("aura_mode") &&
                        !serialized.includes("fetch_url") &&
                        !serialized.includes("worker_id") &&
                        !serialized.includes("renderer_output") &&
                        !serialized.includes("geojson") &&
                        !serialized.includes("canvas_pixels") &&
                        !serialized.includes("leaflet_layers") &&
                        !serialized.includes("fetch_response")
                };
            }""",
            sources,
        )
        browser.close()
        return result


def main() -> int:
    result = run_browser_probe()
    checks = [
        "bridge_loads_in_browser",
        "semantic_request_flows_through_chain",
        "cache_miss_metadata_would_run",
        "cache_hit_sanitized_hydration",
        "stale_cancelled_cannot_hydrate",
        "observer_read_only",
        "no_fetch_occurs",
        "no_dom_map_writes",
        "renderer_substrate_legacy",
        "pollution_stripped",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_12_runtime_bridge_dev",
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
