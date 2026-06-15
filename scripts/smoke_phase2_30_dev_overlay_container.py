#!/usr/bin/env python3
"""Smoke Phase 2.30: debug-only dev overlay container."""

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
            const container = document.getElementById("productionShadowDevOverlay");
            const indicator = document.getElementById("productionShadowDebugIndicator");
            const containerStyle = container ? window.getComputedStyle(container) : null;
            const state = typeof window.__rmProductionShadowState === "function" && callHook
                ? window.__rmProductionShadowState()
                : null;
            const smokeAfter = window.__rmSmokeState();
            const bodyAfter = document.body.innerHTML;
            const mapLayerCountAfter = window.__rmMap ? Object.keys(window.__rmMap._layers || {}).length : null;
            return {
                selfCheckHookExists: typeof window.__rmProductionShadowState === "function",
                state,
                serializedState: JSON.stringify(state || {}),
                containerExists: Boolean(container),
                containerVisible: Boolean(container && containerStyle && containerStyle.display !== "none"),
                containerText: container ? container.textContent : "",
                indicatorExists: Boolean(indicator),
                indicatorText: indicator ? indicator.textContent : "",
                bodyUnchangedByHookCall: bodyBefore === bodyAfter,
                mapLayerCountBefore,
                mapLayerCountAfter,
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
    readiness = debug_state.get("readiness") or {}
    container_text = debug_probe.get("containerText") or ""
    forbidden_terms = [
        '"features"',
        '"geometry"',
        '"coordinates"',
        "best",
        "recommended",
        "truth confirmed",
        "recommendation_logic",
        "symbolic_score",
    ]

    checks = {
        "default_page_loads": default_probe["http_status"] == 200,
        "default_dev_overlay_container_absent": default_probe["containerExists"] is False,
        "default_readiness_indicator_absent": default_probe["indicatorExists"] is False,
        "default_substrate_remains_legacy_search_regions": (
            default_probe["smokeAfter"].get("rendererSubstrate") == "legacy_search_regions"
            and not default_probe["smokeAfter"].get("canonicalRendererBranchActive")
        ),
        "default_no_extra_ui_or_map_layer_or_aura": (
            default_probe["mapLayerCountBefore"] == default_probe["mapLayerCountAfter"]
            and default_probe["smokeAfter"].get("rasterAura", {}).get("initialized") is False
            and (default_probe["smokeAfter"].get("rasterAura", {}).get("sampleCount") or 0) == 0
            and default_probe["smokeAfter"].get("auraLayers") == 0
        ),
        "debug_page_loads": debug_probe["http_status"] == 200,
        "debug_dev_overlay_container_exists_and_is_visible": (
            debug_probe["containerExists"] is True
            and debug_probe["containerVisible"] is True
        ),
        "debug_container_marked_dev_debug": (
            "DEV DEBUG overlay container" in container_text
            and "DEV DEBUG readiness metadata" in container_text
        ),
        "readiness_metadata_surface_exists_in_container": (
            debug_probe["indicatorExists"] is True
            and "status:" in container_text
            and "substrate: legacy_search_regions" in container_text
        ),
        "displayed_metadata_is_sanitized_only": (
            "debug_only: true" in container_text
            and "default_behavior_changed: false" in container_text
            and "renderer_substrate_changed: false" in container_text
            and "aura_rendering_invoked: false" in container_text
            and "raw_payload_exposed: false" in container_text
            and "recommendation_surface_created: false" in container_text
            and "scoring_surface_created: false" in container_text
            and "final_truth_claimed: false" in container_text
            and not any(term in container_text.lower() for term in forbidden_terms)
        ),
        "debug_substrate_remains_legacy_search_regions": (
            readiness.get("substrate") == "legacy_search_regions"
            and debug_state.get("activeRendererSubstrate") == "legacy_search_regions"
            and debug_probe["smokeAfter"].get("rendererSubstrate") == "legacy_search_regions"
            and not debug_probe["smokeAfter"].get("canonicalRendererBranchActive")
        ),
        "debug_no_map_layer_added": debug_probe["mapLayerCountBefore"] == debug_probe["mapLayerCountAfter"],
        "debug_no_raw_payload_recommendation_scoring_or_final_truth_surface": (
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
        "container_causes_no_fetch_map_layer_or_registry_mutation": (
            debug_probe["request_count_after_hook"] == debug_probe["request_count_before_hook"]
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
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
