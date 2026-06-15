#!/usr/bin/env python3
"""Smoke test for the Phase 2.8 mock runtime harness."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_contract.js",
    ROOT / "sampling_cache_store_contract.js",
    ROOT / "sampling_cache_orchestration_contract.js",
    ROOT / "sampling_cache_mock_runtime_harness.js",
]


def run_harness_probe() -> dict:
    sources = [path.read_text(encoding="utf-8") for path in SOURCES]
    probe = r"""
const window = {};
sources.forEach(source => eval(source));
const harnessContract = window.RelocationSamplingCacheMockRuntimeHarness;
const harness = harnessContract.createMockRuntimeHarness({
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
  generation_mode: "truth_grid",
  renderer_substrate: "legacy_search_regions",
  debug: true,
  aura_mode: "raster",
  fetch_url: "/screen-pixel-truth",
  worker_id: "worker-1",
  map_id: "map"
};

const semantic = harness.createSemanticRequest(savedInvestigation);
const miss = harness.handleRequest(savedInvestigation);
const seeded = harness.seedCache(savedInvestigation, {
  status: "ready",
  summary: { matched: 12 },
  metrics: { sample_count: 144 },
  renderer_output: true,
  geojson: { type: "FeatureCollection" },
  canvas_pixels: "pixels",
  leaflet_layers: ["layer"],
  fetch_response: { ok: true },
  worker_id: "worker-1",
  aura_mode: "raster"
});
const hit = harness.handleRequest(savedInvestigation);
const sameZoom = harness.simulateSameRequestScope(savedInvestigation, {
  scope_role: "next_zoom"
});
const changedSampling = harness.simulateSameRequestScope(savedInvestigation, {
  sampling: { width: 1200 },
  scope_role: "changed_sampling"
});
const incompatibleJob = harness.handleRequest({
  ...savedInvestigation,
  chart_key: "chart-b",
  intent_group: "chart-b:sun-house-1"
}).job;
const preempted = harness.simulatePreemption(
  [sameZoom.job, incompatibleJob],
  {
    ...savedInvestigation,
    house_conditions: [{ planet: "Venus", house: 7, slot: "A" }],
    intent_group: "chart-a:venus-house-7",
    generation: 2
  }
);
const conditionChanged = harness.createSemanticRequest({
  ...savedInvestigation,
  house_conditions: [{ planet: "Moon", house: 4, slot: "A" }],
  intent_group: "chart-a:moon-house-4"
});
const chartChanged = harness.createSemanticRequest({
  ...savedInvestigation,
  chart_key: "chart-b",
  intent_group: "chart-b:sun-house-1"
});
const runtimeJson = JSON.stringify({ semantic, miss, hit, preempted, inspect: harness.inspect() });
const hitJson = JSON.stringify(hit);

const result = {
  saved_investigation_to_cache_key_to_orchestration_chain:
    semantic.semantic.key.startsWith("rm:v1:") &&
    semantic.orchestration_request.cache_key === semantic.semantic.key &&
    semantic.orchestration_request.intent_group === "chart-a:sun-house-1",
  cache_miss_creates_tier0_work_envelope:
    miss.outcome === "cache_miss" &&
    miss.job.tier === 0 &&
    miss.job.cache_key === semantic.semantic.key &&
    miss.hydration === null,
  cache_hit_returns_sanitized_hydration_envelope:
    hit.outcome === "cache_hit" &&
    hit.hydration.hydrated === true &&
    hit.hydration.execution_required === false &&
    hit.job === null &&
    hit.hydration.hydration.status === "ready",
  preemption_stales_incompatible_work:
    preempted.foreground.cache_key.startsWith("rm:v1:") &&
    preempted.jobs.filter(job => job.stale).length === 2 &&
    preempted.jobs.filter(job => job.cancelled).length === 1,
  same_semantic_request_compatible_zoom:
    sameZoom.compatibility.compatible === true &&
    sameZoom.job.scope_role === "next_zoom",
  chart_condition_sampling_changes_invalidate:
    conditionChanged.semantic.key !== semantic.semantic.key &&
    chartChanged.semantic.key !== semantic.semantic.key &&
    changedSampling.compatibility.compatible === false,
  runtime_pollution_stripped:
    !runtimeJson.includes("generation_mode") &&
    !runtimeJson.includes("renderer_substrate") &&
    !runtimeJson.includes("debug") &&
    !runtimeJson.includes("aura_mode") &&
    !runtimeJson.includes("fetch_url") &&
    !runtimeJson.includes("worker_id") &&
    !runtimeJson.includes("map_id"),
  no_renderer_output_hydration:
    !hitJson.includes("renderer_output") &&
    !hitJson.includes("geojson") &&
    !hitJson.includes("canvas_pixels") &&
    !hitJson.includes("leaflet_layers") &&
    !hitJson.includes("fetch_response"),
  no_fetch_worker_renderer_map_persistence_fields:
    !runtimeJson.includes("fetch") &&
    !runtimeJson.includes("worker") &&
    !runtimeJson.includes("renderer") &&
    !runtimeJson.includes("Leaflet") &&
    !runtimeJson.includes("localStorage") &&
    !runtimeJson.includes("indexedDB")
};
console.log(JSON.stringify(result));
"""
    completed = subprocess.run(
        [
            "node",
            "-e",
            "const sources = JSON.parse(process.argv[1]);" + probe,
            json.dumps(sources),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    result = run_harness_probe()
    checks = [
        "saved_investigation_to_cache_key_to_orchestration_chain",
        "cache_miss_creates_tier0_work_envelope",
        "cache_hit_returns_sanitized_hydration_envelope",
        "preemption_stales_incompatible_work",
        "same_semantic_request_compatible_zoom",
        "chart_condition_sampling_changes_invalidate",
        "runtime_pollution_stripped",
        "no_renderer_output_hydration",
        "no_fetch_worker_renderer_map_persistence_fields",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_8_mock_runtime_harness",
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
