#!/usr/bin/env python3
"""Smoke Phase 2.32: dev-only renderer integration proof metadata."""

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
            const rendererPanel = document.getElementById("productionShadowRendererAdjacentMetadata");
            const proofPanel = document.getElementById("productionShadowDevRendererProof");
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
                rendererPanelExists: Boolean(rendererPanel),
                rendererPanelText: rendererPanel ? rendererPanel.textContent : "",
                proofPanelExists: Boolean(proofPanel),
                proofPanelText: proofPanel ? proofPanel.textContent : "",
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


def no_aura(smoke: dict) -> bool:
    return (
        smoke.get("rasterAura", {}).get("initialized") is False
        and (smoke.get("rasterAura", {}).get("sampleCount") or 0) == 0
        and smoke.get("auraLayers") == 0
    )


def main() -> int:
    if not server_ok():
        print(json.dumps({"all_pass": False, "error": f"Server not reachable at {BASE}/health"}))
        return 1

    bust = int(time.time())
    default_url = f"{BASE}/map_CURRENT.html?bust={bust}&skipOnboarding=1"
    self_check_url = f"{BASE}/map_CURRENT.html?bust={bust + 1}&skipOnboarding=1&productionShadowSelfCheck=1"
    proof_url = (
        f"{BASE}/map_CURRENT.html?bust={bust + 2}&skipOnboarding=1"
        "&productionShadowSelfCheck=1&devRendererProof=1"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        default_page = browser.new_page(viewport={"width": 1400, "height": 900})
        default_probe = page_probe(default_page, default_url, call_hook=False)
        self_check_page = browser.new_page(viewport={"width": 1400, "height": 900})
        self_check_probe = page_probe(self_check_page, self_check_url, call_hook=True)
        proof_page = browser.new_page(viewport={"width": 1400, "height": 900})
        proof_probe = page_probe(proof_page, proof_url, call_hook=True)
        browser.close()

    self_check_state = self_check_probe.get("state") or {}
    self_check_renderer_adjacent = self_check_state.get("rendererAdjacent") or {}
    self_check_proof = self_check_state.get("devRendererProof") or {}
    proof_state = proof_probe.get("state") or {}
    proof = proof_state.get("devRendererProof") or {}
    proof_text = proof_probe.get("proofPanelText") or ""
    forbidden_terms = [
        '"features"',
        '"geometry"',
        '"coordinates"',
        "best",
        "recommended",
        "truth confirmed",
        "recommendation_logic",
        "symbolic_score",
        "production ready",
    ]

    checks = {
        "default_page_loads": default_probe["http_status"] == 200,
        "default_no_dev_renderer_proof": (
            default_probe["selfCheckHookExists"] is False
            and default_probe["proofPanelExists"] is False
        ),
        "default_no_dev_renderer_ui_or_marker": (
            default_probe["containerExists"] is False
            and default_probe["proofPanelExists"] is False
        ),
        "default_substrate_remains_legacy_search_regions": (
            default_probe["smokeAfter"].get("rendererSubstrate") == "legacy_search_regions"
            and not default_probe["smokeAfter"].get("canonicalRendererBranchActive")
        ),
        "default_no_extra_ui_map_layer_or_aura": (
            default_probe["mapLayerCountBefore"] == default_probe["mapLayerCountAfter"]
            and no_aura(default_probe["smokeAfter"])
        ),
        "self_check_page_loads": self_check_probe["http_status"] == 200,
        "self_check_does_not_activate_dev_renderer_proof": (
            self_check_state.get("devRendererProofEnabled") is False
            and self_check_proof.get("dev_renderer_proof") is False
            and self_check_probe["proofPanelExists"] is False
        ),
        "self_check_overlay_and_placeholder_still_work": (
            self_check_probe["containerExists"] is True
            and self_check_probe["rendererPanelExists"] is True
            and self_check_renderer_adjacent.get("renderer_adjacent_placeholder") is True
            and self_check_renderer_adjacent.get("active_substrate") == "legacy_search_regions"
        ),
        "self_check_no_layers_or_aura_or_hydration": (
            self_check_probe["mapLayerCountBefore"] == self_check_probe["mapLayerCountAfter"]
            and self_check_state.get("productionLayersHydrated") is False
            and no_aura(self_check_probe["smokeAfter"])
            and self_check_state.get("auraInitialized") is False
        ),
        "proof_page_loads": proof_probe["http_status"] == 200,
        "proof_flag_activates_only_dev_renderer_metadata": (
            proof_state.get("devRendererProofEnabled") is True
            and proof.get("dev_renderer_proof") is True
            and proof_probe["proofPanelExists"] is True
            and "DEV DEBUG dev renderer proof" in proof_text
        ),
        "proof_metadata_negative_assertions": (
            proof.get("debug_only") is True
            and proof.get("active_substrate") == "legacy_search_regions"
            and proof.get("production_substrate_flipped") is False
            and proof.get("production_layers_hydrated") is False
            and proof.get("real_user_rendering_created") is False
            and proof.get("product_ui_created") is False
            and proof.get("aura_output_created") is False
            and proof.get("backend_fetch_created") is False
            and proof.get("scheduler_cache_execution") is False
            and proof.get("raw_payload_exposed") is False
            and proof.get("recommendation_surface_created") is False
            and proof.get("scoring_surface_created") is False
            and proof.get("final_truth_claimed") is False
        ),
        "proof_display_sanitized_only": (
            "dev_renderer_proof: true" in proof_text
            and "active_substrate: legacy_search_regions" in proof_text
            and "production_substrate_flipped: false" in proof_text
            and "production_layers_hydrated: false" in proof_text
            and "real_user_rendering_created: false" in proof_text
            and "product_ui_created: false" in proof_text
            and "aura_output_created: false" in proof_text
            and "backend_fetch_created: false" in proof_text
            and "scheduler_cache_execution: false" in proof_text
            and "raw_payload_exposed: false" in proof_text
            and "recommendation_surface_created: false" in proof_text
            and "scoring_surface_created: false" in proof_text
            and "final_truth_claimed: false" in proof_text
            and not any(term in proof_text.lower() for term in forbidden_terms)
        ),
        "proof_substrate_remains_legacy_search_regions": (
            proof_state.get("activeRendererSubstrate") == "legacy_search_regions"
            and proof_state.get("rendererSubstrate") == "legacy_search_regions"
            and proof_probe["smokeAfter"].get("rendererSubstrate") == "legacy_search_regions"
            and not proof_probe["smokeAfter"].get("canonicalRendererBranchActive")
        ),
        "proof_no_map_layer_registry_or_hydration_mutation": (
            proof_probe["mapLayerCountBefore"] == proof_probe["mapLayerCountAfter"]
            and proof_state.get("productionRegistryMutated") is False
            and proof_state.get("domOrMapMutated") is False
            and proof_state.get("productionLayersHydrated") is False
        ),
        "proof_no_aura_output_or_debug_mode_invoked": (
            proof_state.get("auraDebugVisualModeActive") is False
            and proof_state.get("auraInitialized") is False
            and proof_state.get("auraSampleCount") == 0
            and proof_state.get("auraLayerCount") == 0
            and proof.get("aura_output_created") is False
        ),
        "proof_causes_no_fetch": (
            proof_probe["request_count_after_hook"] == proof_probe["request_count_before_hook"]
            and proof.get("backend_fetch_created") is False
        ),
        "proof_hook_call_only_mutates_no_dom": proof_probe["bodyUnchangedByHookCall"] is True,
        "no_console_errors": (
            len(default_probe["console_errors"]) == 0
            and len(self_check_probe["console_errors"]) == 0
            and len(proof_probe["console_errors"]) == 0
        ),
    }
    all_pass = all(checks.values())
    print(
        json.dumps(
            {
                "all_pass": all_pass,
                "default_url": default_url,
                "self_check_url": self_check_url,
                "proof_url": proof_url,
                "checks": checks,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
