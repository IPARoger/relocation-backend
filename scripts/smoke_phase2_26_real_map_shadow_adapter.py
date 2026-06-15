#!/usr/bin/env python3
"""Smoke Phase 2.26: evaluate real map state with the shadow adapter."""

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
SOURCES = [
    ROOT / "sampling_cache_production_readiness_contract.js",
    ROOT / "sampling_cache_production_shadow_adapter_dev.js",
]

if DEFAULT_BROWSER_PATH.exists():
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(DEFAULT_BROWSER_PATH)


def server_ok() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE}/health", timeout=5) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def main() -> int:
    if not server_ok():
        print(json.dumps({"all_pass": False, "error": f"Server not reachable at {BASE}/health"}))
        return 1

    sources = [path.read_text(encoding="utf-8") for path in SOURCES]
    url = f"{BASE}/map_CURRENT.html?bust={int(time.time())}&skipOnboarding=1"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
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

        before = page.evaluate(
            """() => {
                const smoke = window.__rmSmokeState();
                return {
                    bodyHtml: document.body.innerHTML,
                    mapLayerCount: window.__rmMap ? Object.keys(window.__rmMap._layers || {}).length : null,
                    smoke,
                    adapterGlobalExists: Boolean(window.RelocationSamplingCacheProductionShadowAdapterDev),
                    contractGlobalExists: Boolean(window.RelocationSamplingCacheProductionReadinessContract),
                    readinessUiCount: document.querySelectorAll('[data-production-readiness], #productionReadiness, .production-readiness').length,
                    adapterUiCount: document.querySelectorAll('[data-production-shadow-adapter], #productionShadowAdapter, .production-shadow-adapter').length,
                    auraCanvasVisible: (() => {
                        const c = document.getElementById('auraRasterCanvas');
                        return Boolean(c && c.style.display !== 'none' && c.width > 0);
                    })()
                };
            }"""
        )
        request_count_before = len(requested_urls)
        initial_console_count = len(console_errors)

        result = page.evaluate(
            """sources => {
                const originalFetch = window.fetch;
                const adapterFetchCalls = [];
                window.fetch = (...args) => {
                    adapterFetchCalls.push(String(args[0] || ""));
                    throw new Error("Phase 2.26 adapter evaluation must not fetch");
                };

                const smoke = window.__rmSmokeState();
                const bodyBefore = document.body.innerHTML;
                const mapLayerCountBefore = window.__rmMap ? Object.keys(window.__rmMap._layers || {}).length : null;
                const registryBefore = window.__productionOverlayRegistry;
                window.__phase226TestRegistry = [];

                sources.forEach(source => eval(source));

                const adapter = window.RelocationSamplingCacheProductionShadowAdapterDev;
                const contract = window.RelocationSamplingCacheProductionReadinessContract;
                const substrate = smoke.rendererSubstrate || "legacy_search_regions";
                const profile = {
                    requested_readiness_status: "production_candidate",
                    runtime_metadata: {
                        renderer_substrate_observed: substrate,
                        polygon_layer_count: smoke.polygonLayers || 0,
                        aspect_layer_count: smoke.aspectLayers || 0,
                        non_finite_coordinate_count: smoke.nonFiniteCoords || 0,
                        canonical_renderer_branch_active: Boolean(smoke.canonicalRendererBranchActive),
                        canonical_visible_debug_enabled: Boolean(smoke.canonicalVisibleDebugEnabled),
                        canonical_dry_run_enabled: Boolean(smoke.canonicalDryRunEnabled),
                        final_truth_claimed: false,
                        display_state: "active"
                    },
                    boundary_flags: {
                        no_interpretation_in_runtime_metadata: true,
                        no_symbolic_scoring: true,
                        no_recommendation_authority: true,
                        no_best_location_logic: true,
                        no_hidden_ontology: true,
                        renderer_ownership_claimed: false,
                        production_registry_mutated: false,
                        dom_mutation_outside_approved_root: false,
                        raw_backend_payload_exposed: false,
                        unsafe_hydration: false,
                        final_truth_claimed: false,
                        candidates_confirmed_as_truth: false,
                        runtime_priority_implies_symbolic_importance: false,
                        neutral_runtime_metadata: true,
                        candidate_vocabulary_quarantined: true
                    },
                    observer: {
                        read_only: true,
                        can_control_lifecycle: false,
                        can_control_scheduler: false,
                        can_control_hydration: false,
                        can_control_cache: false
                    },
                    cache: {
                        semantic_cache_keys_renderer_independent: true,
                        semantic_cache_keys_debug_independent: true,
                        semantic_cache_keys_aura_independent: true,
                        foreground_user_request_protected: true,
                        background_work_cannot_block_current_intent: true,
                        stale_or_cancelled_work_cannot_hydrate_visibly: true
                    },
                    validation: {
                        dedicated_smoke_exists: true,
                        narrative_exists: true,
                        rollback_scope_clear: true
                    },
                    production_path: {
                        renderer_substrate: substrate,
                        fetch_coupled: false,
                        worker_coupled: false,
                        dom_or_map_coupled: false,
                        renderer_coupled: false,
                        persistence_coupled: false,
                        backend_coupled: false
                    }
                };
                const evaluation = adapter.evaluateShadowCandidate(profile);
                const inspect = adapter.inspectAdapter();
                const contractInspect = contract.inspectContract();
                const mapLayerCountAfter = window.__rmMap ? Object.keys(window.__rmMap._layers || {}).length : null;
                const bodyAfter = document.body.innerHTML;
                const smokeAfter = window.__rmSmokeState();

                window.fetch = originalFetch;
                delete window.RelocationSamplingCacheProductionShadowAdapterDev;
                delete window.RelocationSamplingCacheProductionReadinessContract;
                delete window.__phase226TestRegistry;

                return {
                    page_substrate_before: substrate,
                    page_substrate_after: smokeAfter.rendererSubstrate,
                    adapter_fetch_calls: adapterFetchCalls,
                    body_unchanged: bodyBefore === bodyAfter,
                    map_layer_count_before: mapLayerCountBefore,
                    map_layer_count_after: mapLayerCountAfter,
                    registry_before_was_undefined: typeof registryBefore === "undefined",
                    readiness_ui_count_after: document.querySelectorAll('[data-production-readiness], #productionReadiness, .production-readiness').length,
                    adapter_ui_count_after: document.querySelectorAll('[data-production-shadow-adapter], #productionShadowAdapter, .production-shadow-adapter').length,
                    adapter_global_removed: !window.RelocationSamplingCacheProductionShadowAdapterDev,
                    contract_global_removed: !window.RelocationSamplingCacheProductionReadinessContract,
                    evaluation,
                    inspect,
                    contractInspect,
                    smoke_after: smokeAfter,
                    sanitized_serialized: JSON.stringify(evaluation)
                };
            }""",
            sources,
        )

        request_count_after = len(requested_urls)
        after = page.evaluate(
            """() => {
                const smoke = window.__rmSmokeState();
                return {
                    bodyHtml: document.body.innerHTML,
                    mapLayerCount: window.__rmMap ? Object.keys(window.__rmMap._layers || {}).length : null,
                    smoke,
                    adapterGlobalExists: Boolean(window.RelocationSamplingCacheProductionShadowAdapterDev),
                    contractGlobalExists: Boolean(window.RelocationSamplingCacheProductionReadinessContract),
                    readinessUiCount: document.querySelectorAll('[data-production-readiness], #productionReadiness, .production-readiness').length,
                    adapterUiCount: document.querySelectorAll('[data-production-shadow-adapter], #productionShadowAdapter, .production-shadow-adapter').length,
                    auraCanvasVisible: (() => {
                        const c = document.getElementById('auraRasterCanvas');
                        return Boolean(c && c.style.display !== 'none' && c.width > 0);
                    })()
                };
            }"""
        )
        browser.close()

    checks = {
        "real_map_default_page_loads": resp is not None and resp.status == 200,
        "production_substrate_remains_legacy_search_regions": (
            before["smoke"].get("rendererSubstrate") == "legacy_search_regions"
            and result["page_substrate_before"] == "legacy_search_regions"
            and result["page_substrate_after"] == "legacy_search_regions"
            and after["smoke"].get("rendererSubstrate") == "legacy_search_regions"
            and not after["smoke"].get("canonicalRendererBranchActive")
        ),
        "no_visible_adapter_or_readiness_ui_exists": (
            before["adapterUiCount"] == 0
            and before["readinessUiCount"] == 0
            and result["adapter_ui_count_after"] == 0
            and result["readiness_ui_count_after"] == 0
            and after["adapterUiCount"] == 0
            and after["readinessUiCount"] == 0
        ),
        "adapter_scripts_not_required_by_page": (
            before["adapterGlobalExists"] is False
            and before["contractGlobalExists"] is False
        ),
        "adapter_globals_removed_after_test_context": (
            result["adapter_global_removed"] is True
            and result["contract_global_removed"] is True
            and after["adapterGlobalExists"] is False
            and after["contractGlobalExists"] is False
        ),
        "profile_evaluates_through_shadow_adapter": (
            result["evaluation"].get("accepted") is True
            and result["evaluation"].get("readiness_status") == "production_candidate"
            and result["evaluation"].get("classification", {}).get("hard_gates_passed") is True
        ),
        "no_additional_fetch_caused_by_adapter": (
            result["adapter_fetch_calls"] == []
            and request_count_after == request_count_before
        ),
        "no_dom_or_map_mutation_caused_by_adapter": (
            result["body_unchanged"] is True
            and before["bodyHtml"] == after["bodyHtml"]
            and result["map_layer_count_before"] == result["map_layer_count_after"]
            and before["mapLayerCount"] == after["mapLayerCount"]
        ),
        "no_map_layer_added_by_adapter": result["map_layer_count_before"] == result["map_layer_count_after"],
        "no_renderer_substrate_changed": (
            result["inspect"].get("active_production_substrate") == "legacy_search_regions"
            and result["contractInspect"].get("rendererSubstrate") == "legacy_search_regions"
            and result["evaluation"].get("active_production_substrate") == "legacy_search_regions"
        ),
        "no_production_registry_mutation": (
            result["registry_before_was_undefined"] is True
            and result["evaluation"].get("production_registry_mutated") is False
            and result["inspect"].get("production_registry_mutated") is False
        ),
        "no_aura_or_debug_path_invoked": (
            before["smoke"].get("rasterAura", {}).get("initialized") is False
            and after["smoke"].get("rasterAura", {}).get("initialized") is False
            and (before["smoke"].get("rasterAura", {}).get("sampleCount") or 0) == 0
            and (after["smoke"].get("rasterAura", {}).get("sampleCount") or 0) == 0
            and after["smoke"].get("auraLayers") == 0
            and after["smoke"].get("canonicalVisibleDebugEnabled") is False
            and after["smoke"].get("canonicalDryRunEnabled") is False
        ),
        "no_raw_backend_payload_exposed": (
            result["evaluation"].get("raw_backend_payload_exposed") is False
            and '"features"' not in result["sanitized_serialized"]
            and '"geometry"' not in result["sanitized_serialized"]
            and '"coordinates"' not in result["sanitized_serialized"]
        ),
        "no_console_errors_during_adapter_evaluation": len(console_errors) == initial_console_count,
    }
    diagnostics = {
        "before_aura": before["smoke"].get("rasterAura"),
        "after_aura": after["smoke"].get("rasterAura"),
        "before_aura_layers": before["smoke"].get("auraLayers"),
        "after_aura_layers": after["smoke"].get("auraLayers"),
        "before_aura_canvas_visible": before["auraCanvasVisible"],
        "after_aura_canvas_visible": after["auraCanvasVisible"],
        "after_canonical_visible_debug": after["smoke"].get("canonicalVisibleDebugEnabled"),
        "after_canonical_dry_run": after["smoke"].get("canonicalDryRunEnabled"),
    }
    all_pass = all(checks.values())
    print(json.dumps({"all_pass": all_pass, "url": url, "checks": checks, "diagnostics": diagnostics}, indent=2, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
