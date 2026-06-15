#!/usr/bin/env python3
"""Smoke Phase 2.28: debug-only in-page readiness evaluation metadata."""

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
            const bodyBefore = document.body.innerHTML;
            const smokeBefore = window.__rmSmokeState();
            const mapLayerCountBefore = window.__rmMap ? Object.keys(window.__rmMap._layers || {}).length : null;
            const selfCheckHookExists = typeof window.__rmProductionShadowState === "function";
            const readinessHookExists = typeof window.__rmProductionReadinessEvaluation === "function";
            const readinessUiCountBefore = document.querySelectorAll('[data-production-readiness], #productionReadiness, .production-readiness').length;
            const adapterUiCountBefore = document.querySelectorAll('[data-production-shadow-adapter], #productionShadowAdapter, .production-shadow-adapter').length;
            const state = selfCheckHookExists && callHook ? window.__rmProductionShadowState() : null;
            const readiness = state?.readiness || (readinessHookExists && callHook ? window.__rmProductionReadinessEvaluation() : null);
            const smokeAfter = window.__rmSmokeState();
            const bodyAfter = document.body.innerHTML;
            const mapLayerCountAfter = window.__rmMap ? Object.keys(window.__rmMap._layers || {}).length : null;
            return {
                selfCheckHookExists,
                readinessHookExists,
                state,
                readiness,
                serializedState: JSON.stringify(state || {}),
                serializedReadiness: JSON.stringify(readiness || {}),
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
    readiness = debug_probe.get("readiness") or {}
    forbidden_payload_terms = ('"features"', '"geometry"', '"coordinates"', "best_location", "recommendation_logic", "symbolic_score")
    serialized_all = f"{debug_probe.get('serializedState', '')}\n{debug_probe.get('serializedReadiness', '')}"

    checks = {
        "default_page_loads": default_probe["http_status"] == 200,
        "default_readiness_and_self_check_hooks_absent_or_inert": (
            default_probe["selfCheckHookExists"] is False
            and default_probe["readinessHookExists"] is False
        ),
        "default_substrate_remains_legacy_search_regions": (
            default_probe["smokeAfter"].get("rendererSubstrate") == "legacy_search_regions"
            and not default_probe["smokeAfter"].get("canonicalRendererBranchActive")
        ),
        "default_no_visible_ui_or_layers_or_aura": (
            default_probe["readinessUiCountAfter"] == 0
            and default_probe["adapterUiCountAfter"] == 0
            and default_probe["mapLayerCountBefore"] == default_probe["mapLayerCountAfter"]
            and default_probe["smokeAfter"].get("rasterAura", {}).get("initialized") is False
            and (default_probe["smokeAfter"].get("rasterAura", {}).get("sampleCount") or 0) == 0
            and default_probe["smokeAfter"].get("auraLayers") == 0
        ),
        "debug_page_loads": debug_probe["http_status"] == 200,
        "debug_self_check_hook_exists": debug_probe["selfCheckHookExists"] is True,
        "debug_readiness_evaluation_exists": isinstance(readiness, dict) and readiness.get("debug_only") is True,
        "readiness_result_is_sanitized_metadata_only": (
            readiness.get("status") in ["not_ready", "sandbox_only", "transitional_candidate", "production_candidate"]
            and isinstance(readiness.get("passed"), bool)
            and isinstance(readiness.get("failed_gates"), list)
            and isinstance(readiness.get("warnings"), list)
            and readiness.get("substrate") == "legacy_search_regions"
            and readiness.get("default_behavior_changed") is False
            and readiness.get("visible_ui_created") is False
            and readiness.get("renderer_substrate_changed") is False
            and readiness.get("raw_payload_exposed") is False
            and readiness.get("recommendation_surface_created") is False
            and readiness.get("scoring_surface_created") is False
            and readiness.get("final_truth_claimed") is False
            and not any(term in serialized_all for term in forbidden_payload_terms)
        ),
        "debug_substrate_remains_legacy_search_regions": (
            debug_state.get("activeRendererSubstrate") == "legacy_search_regions"
            and debug_probe["smokeAfter"].get("rendererSubstrate") == "legacy_search_regions"
            and not debug_probe["smokeAfter"].get("canonicalRendererBranchActive")
        ),
        "debug_no_visible_ui_or_map_layer_added": (
            debug_probe["readinessUiCountBefore"] == 0
            and debug_probe["readinessUiCountAfter"] == 0
            and debug_probe["adapterUiCountBefore"] == 0
            and debug_probe["adapterUiCountAfter"] == 0
            and debug_probe["mapLayerCountBefore"] == debug_probe["mapLayerCountAfter"]
        ),
        "debug_no_raw_payload_recommendation_scoring_or_final_truth": (
            debug_state.get("rawBackendPayloadExposed") is False
            and debug_state.get("recommendationSurfaceClaimed") is False
            and debug_state.get("symbolicScoringClaimed") is False
            and debug_state.get("finalTruthClaimed") is False
            and readiness.get("raw_payload_exposed") is False
            and readiness.get("recommendation_surface_created") is False
            and readiness.get("scoring_surface_created") is False
            and readiness.get("final_truth_claimed") is False
        ),
        "debug_no_aura_rendering_or_layer_hydration": (
            debug_state.get("auraDebugVisualModeActive") is False
            and debug_state.get("auraInitialized") is False
            and debug_state.get("auraSampleCount") == 0
            and debug_state.get("auraLayerCount") == 0
            and readiness.get("aura_rendering_invoked") is False
            and debug_state.get("productionLayersHydrated") is False
        ),
        "readiness_hook_causes_no_fetch_dom_map_or_registry_mutation": (
            debug_probe["request_count_after_hook"] == debug_probe["request_count_before_hook"]
            and debug_probe["bodyUnchanged"] is True
            and debug_probe["mapLayerCountBefore"] == debug_probe["mapLayerCountAfter"]
            and debug_state.get("productionRegistryMutated") is False
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
                "readiness": readiness,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
