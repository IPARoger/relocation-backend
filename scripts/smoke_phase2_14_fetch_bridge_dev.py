#!/usr/bin/env python3
"""Browser smoke for the Phase 2.14 isolated fetch bridge."""

from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.request

from playwright.sync_api import sync_playwright


BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_contract.js",
    ROOT / "sampling_cache_store_contract.js",
    ROOT / "sampling_cache_orchestration_contract.js",
    ROOT / "sampling_cache_execution_bridge_contract.js",
    ROOT / "sampling_cache_observer_contract.js",
    ROOT / "sampling_cache_execution_policy_contract.js",
    ROOT / "sampling_cache_fetch_bridge_dev.js",
]


def backend_available() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE}/", timeout=5) as resp:
            return resp.status < 500
    except Exception:
        try:
            with urllib.request.urlopen(f"{BASE}/docs", timeout=5) as resp:
                return resp.status < 500
        except Exception:
            return False


def run_browser_probe() -> dict:
    sources = [path.read_text(encoding="utf-8") for path in SOURCES]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        result = page.evaluate(
            """async ({ sources, endpoint }) => {
                const fetchCalls = [];
                const originalFetch = window.fetch.bind(window);
                window.fetch = (...args) => {
                    fetchCalls.push(String(args[0] || ""));
                    return originalFetch(...args);
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
                const bridge = window.RelocationSamplingCacheFetchBridgeDev.createFetchBridgeDev({
                    endpoint,
                    store_options: { ttl_ms: 1000, now: () => 1000 }
                });
                const savedInvestigation = {
                    chart_key: "chart-a",
                    birth_year: 1990,
                    birth_month: 1,
                    birth_day: 1,
                    birth_hour_utc: 12,
                    house_conditions: [{ planet: "sun", house: 1, slot: "A" }],
                    viewport: { north: 60, south: -60, east: 180, west: -180, zoom: 1 },
                    sampling: { width: 360, height: 180, block_px: 30, lat_cap: true },
                    intent_group: "chart-a:sun-house-1",
                    generation: 1,
                    renderer_substrate: "canonical_screen_space",
                    debug: true,
                    aura_mode: "raster"
                };
                const result = await bridge.executeOnce(savedInvestigation);
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
                    inspect: bridge.inspect()
                });
                mutationObserver.disconnect();
                window.fetch = originalFetch;
                return {
                    one_real_fetch_executes:
                        fetchCalls.length === 1 &&
                        fetchCalls[0].includes("/search-regions") &&
                        result.backend.status === 200,
                    semantic_request_survives_chain:
                        result.semantic_key.startsWith("rm:v1:") &&
                        result.execution.job.cache_key === result.semantic_key &&
                        result.policy.decisions[0].cache_key === result.semantic_key,
                    lifecycle_transitions_correct:
                        JSON.stringify(result.lifecycle) === JSON.stringify(["queued", "running", "completed"]) &&
                        result.execution.state === "completed",
                    backend_response_sanitized:
                        result.backend.metadata.summary.feature_count >= 0 &&
                        result.backend.metadata.metrics.backend_status === 200,
                    metadata_only_hydration:
                        result.hydration.hydrated === true &&
                        result.hydration.execution_required === false &&
                        result.hydration.hydration.summary.feature_count >= 0,
                    cache_store_sanitized_metadata_only:
                        result.store.count === 1 &&
                        result.store.entries[0].payload_fields.includes("chart_key") &&
                        result.store.entries[0].value_fields.includes("summary"),
                    stale_cancelled_cannot_hydrate:
                        staleObserver.hydration_visible === false &&
                        cancelledObserver.hydration_visible === false,
                    observer_read_only:
                        result.observer.read_only === true &&
                        result.observer.can_control_scheduler === false &&
                        result.observer.can_control_execution === false,
                    no_map_dom_writes: mutationRecords.length === 0,
                    renderer_substrate_legacy:
                        result.rendererSubstrate === "legacy_search_regions" &&
                        bridge.inspect().rendererSubstrate === "legacy_search_regions",
                    single_request_reversible:
                        bridge.inspect().active === false &&
                        result.store.count === 1,
                    raw_payload_not_exposed:
                        !serialized.includes('"features"') &&
                        !serialized.includes('"coordinates"') &&
                        !serialized.includes('"geometry"') &&
                        !serialized.includes("canonical_screen_space") &&
                        !serialized.includes("debug") &&
                        !serialized.includes("aura_mode")
                };
            }""",
            {"sources": sources, "endpoint": f"{BASE}/search-regions"},
        )
        browser.close()
        return result


def main() -> int:
    if not backend_available():
        payload = {
            "results": [
                {
                    "test": "backend_available",
                    "pass": False,
                    "detail": {"base_url": BASE, "reason": "backend not reachable"},
                }
            ],
            "all_pass": False,
        }
        print(json.dumps(payload, indent=2))
        return 1

    result = run_browser_probe()
    checks = [
        "one_real_fetch_executes",
        "semantic_request_survives_chain",
        "lifecycle_transitions_correct",
        "backend_response_sanitized",
        "metadata_only_hydration",
        "cache_store_sanitized_metadata_only",
        "stale_cancelled_cannot_hydrate",
        "observer_read_only",
        "no_map_dom_writes",
        "renderer_substrate_legacy",
        "single_request_reversible",
        "raw_payload_not_exposed",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_14_fetch_bridge_dev",
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
