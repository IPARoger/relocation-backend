#!/usr/bin/env python3
"""Smoke Phase 2.27: debug-gated real-map production shadow self-check."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BROWSER_PATH = ROOT / ".playwright-browsers"

if DEFAULT_BROWSER_PATH.exists():
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(DEFAULT_BROWSER_PATH)


def server_ok() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE}/health", timeout=5) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def page_probe(page, url: str, call_hook: bool) -> dict:
    requested_urls: list[str] = []
    console_errors: list[str] = []
    page.on("request", lambda request: requested_urls.append(request.url))
    page.on("pageerror", lambda exc: console_errors.append(f"pageerror: {exc}"))
    page.on(
        "console",
        lambda msg: console_errors.append(f"console.{msg.type}: {msg.text}")
        if msg.type == "error"
        else None,
    )
    resp = page.goto(url, wait_until="networkidle", timeout=30000)
    page.wait_for_function(
        "() => window.__rmMap && window.__rmSmokeState && document.getElementById('chartProfile')?.options?.length >= 3",
        timeout=30000,
    )
    before_count = len(requested_urls)
    result = page.evaluate(
        """callHook => {
            const smokeBefore = window.__rmSmokeState();
            const bodyBefore = document.body.innerHTML;
            const mapLayerCountBefore = window.__rmMap ? Object.keys(window.__rmMap._layers || {}).length : null;
            const hookExistsBefore = typeof window.__rmProductionShadowState === "function";
            const readinessUiCountBefore = document.querySelectorAll('[data-production-readiness], #productionReadiness, .production-readiness').length;
            const adapterUiCountBefore = document.querySelectorAll('[data-production-shadow-adapter], #productionShadowAdapter, .production-shadow-adapter').length;
            const state = hookExistsBefore && callHook ? window.__rmProductionShadowState() : null;
            const smokeAfter = window.__rmSmokeState();
            const bodyAfter = document.body.innerHTML;
            const mapLayerCountAfter = window.__rmMap ? Object.keys(window.__rmMap._layers || {}).length : null;
            return {
                hookExists: hookExistsBefore,
                state,
                serializedState: JSON.stringify(state || {}),
                bodyUnchanged: bodyBefore === bodyAfter,
                mapLayerCountBefore,
                mapLayerCountAfter,
                readinessUiCountBefore,
                readinessUiCountAfter: document.querySelectorAll('[data-production-readiness], #productionReadiness, .production-readiness').length,
                adapterUiCountBefore,
                adapterUiCountAfter: document.querySelectorAll('[data-production-shadow-adapter], #productionShadowAdapter, .production-shadow-adapter').length,
                smokeBefore,
                smokeAfter
            };
        }""",
        call_hook,
    )
    after_count = len(requested_urls)
    return {
        "http_status": resp.status if resp else None,
        "request_count_before_hook": before_count,
        "request_count_after_hook": after_count,
        "console_errors": console_errors,
        **result,
    }


def main() -> int:
    if not server_ok():
        print(json.dumps({"all_pass": False, "error": f"Server not reachable at {BASE}/health"}))
        return 1

    bust = int(time.time())
    default_url = f"{BASE}/map_CURRENT.html?bust={bust}&skipOnboarding=1"
    debug_url = f"{BASE}/map_CURRENT.html?bust={bust + 1}&skipOnboarding=1&productionShadowSelfCheck=1"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        default_page = browser.new_page(viewport={"width": 1400, "height": 900})
        default_probe = page_probe(default_page, default_url, call_hook=False)
        debug_page = browser.new_page(viewport={"width": 1400, "height": 900})
        debug_probe = page_probe(debug_page, debug_url, call_hook=True)
        browser.close()

    debug_state = debug_probe.get("state") or {}
    checks = {
        "default_page_loads_without_debug_flag": default_probe["http_status"] == 200,
        "default_hook_absent_or_inert": default_probe["hookExists"] is False,
        "default_substrate_remains_legacy_search_regions": (
            default_probe["smokeAfter"].get("rendererSubstrate") == "legacy_search_regions"
            and not default_probe["smokeAfter"].get("canonicalRendererBranchActive")
        ),
        "default_no_readiness_or_adapter_ui": (
            default_probe["readinessUiCountAfter"] == 0
            and default_probe["adapterUiCountAfter"] == 0
        ),
        "default_no_new_map_layer": default_probe["mapLayerCountBefore"] == default_probe["mapLayerCountAfter"],
        "default_no_aura_or_debug_mode_invoked": (
            default_probe["smokeAfter"].get("rasterAura", {}).get("initialized") is False
            and (default_probe["smokeAfter"].get("rasterAura", {}).get("sampleCount") or 0) == 0
            and default_probe["smokeAfter"].get("auraLayers") == 0
            and default_probe["smokeAfter"].get("canonicalVisibleDebugEnabled") is False
            and default_probe["smokeAfter"].get("canonicalDryRunEnabled") is False
        ),
        "debug_page_loads_with_flag": debug_probe["http_status"] == 200,
        "debug_hook_exists": debug_probe["hookExists"] is True,
        "debug_metadata_is_sanitized_and_neutral": (
            debug_state.get("mode") == "debug_production_shadow_self_check_only"
            and debug_state.get("productionShadowSelfCheckEnabled") is True
            and debug_state.get("rendererMutationClaimed") is False
            and debug_state.get("rawPayloadExposureClaimed") is False
            and debug_state.get("observerControlClaimed") is False
            and debug_state.get("staleHydrationClaimed") is False
            and debug_state.get("symbolicScoringClaimed") is False
            and debug_state.get("recommendationSurfaceClaimed") is False
            and debug_state.get("finalTruthClaimed") is False
            and '"features"' not in debug_probe["serializedState"]
            and '"geometry"' not in debug_probe["serializedState"]
            and '"coordinates"' not in debug_probe["serializedState"]
        ),
        "debug_substrate_remains_legacy_search_regions": (
            debug_state.get("activeRendererSubstrate") == "legacy_search_regions"
            and debug_probe["smokeAfter"].get("rendererSubstrate") == "legacy_search_regions"
            and not debug_probe["smokeAfter"].get("canonicalRendererBranchActive")
        ),
        "debug_no_visible_ui": (
            debug_probe["readinessUiCountBefore"] == 0
            and debug_probe["readinessUiCountAfter"] == 0
            and debug_probe["adapterUiCountBefore"] == 0
            and debug_probe["adapterUiCountAfter"] == 0
        ),
        "debug_no_map_layer_added": debug_probe["mapLayerCountBefore"] == debug_probe["mapLayerCountAfter"],
        "debug_no_raw_payload_or_recommendation_scoring_truth_surface": (
            debug_state.get("rawBackendPayloadExposed") is False
            and debug_state.get("recommendationSurfaceClaimed") is False
            and debug_state.get("symbolicScoringClaimed") is False
            and debug_state.get("finalTruthClaimed") is False
        ),
        "debug_no_aura_or_debug_mode_invoked": (
            debug_state.get("auraDebugVisualModeActive") is False
            and debug_state.get("auraInitialized") is False
            and debug_state.get("auraSampleCount") == 0
            and debug_state.get("auraLayerCount") == 0
            and debug_state.get("canonicalVisibleDebugEnabled") is False
            and debug_state.get("canonicalDryRunEnabled") is False
        ),
        "self_check_hook_causes_no_unexpected_fetch": (
            debug_probe["request_count_after_hook"] == debug_probe["request_count_before_hook"]
        ),
        "self_check_hook_causes_no_dom_or_map_mutation": (
            debug_probe["bodyUnchanged"] is True
            and debug_probe["mapLayerCountBefore"] == debug_probe["mapLayerCountAfter"]
        ),
        "self_check_hook_causes_no_registry_mutation_or_hydration": (
            debug_state.get("productionRegistryMutated") is False
            and debug_state.get("productionLayersHydrated") is False
            and debug_state.get("domOrMapMutated") is False
        ),
        "no_console_errors": (
            len(default_probe["console_errors"]) == 0
            and len(debug_probe["console_errors"]) == 0
        ),
    }
    all_pass = all(checks.values())
    print(
        json.dumps(
            {
                "all_pass": all_pass,
                "default_url": default_url,
                "debug_url": debug_url,
                "checks": checks,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
