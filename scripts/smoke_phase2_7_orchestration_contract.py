#!/usr/bin/env python3
"""Smoke test for the Phase 2.7 orchestration contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "sampling_cache_orchestration_contract.js"


def run_contract_probe() -> dict:
    source = CONTRACT_PATH.read_text(encoding="utf-8")
    probe = r"""
const window = {};
eval(source);
const o = window.RelocationSamplingCacheOrchestrationContract;

const active = o.createOrchestrationRequest({
  schema_version: 1,
  chart_key: "chart-a",
  investigation: { house_conditions: [{ planet: "sun", house: 1 }] },
  viewport: { north: 10, south: -10, east: 20, west: -20, zoom: 4 },
  sampling: { width: 1000, height: 700, block_px: 12, lat_cap: true },
  cache_key: "rm:v1:active",
  intent_group: "chart-a:sun-house-1",
  scope_role: "current_viewport",
  generation: 1,
  generation_mode: "truth_grid",
  renderer_substrate: "legacy_search_regions",
  debug: true,
  aura_mode: "raster",
  fetch_url: "/screen-pixel-truth",
  worker_id: "worker-1",
  dom_node: "#map"
});
const foreground = o.createJobEnvelope({ request: active, tier: o.TIERS.FOREGROUND_USER_REQUEST });
const cacheEntry = {
  key: active.cache_key,
  status: "ready",
  summary: { matched: 12 },
  metrics: { sample_count: 144 },
  created_at_ms: 1000,
  updated_at_ms: 1100,
  expires_at_ms: 2000,
  rendered_geojson: { type: "FeatureCollection" },
  canvas_pixels: "pixels",
  leaflet_layers: ["layer"],
  renderer_output: true,
  generation_mode: "truth_grid",
  debug: true,
  aura_mode: "raster",
  fetch_response: { ok: true },
  worker_id: "worker-1"
};
const hydrationHit = o.createHydrationEnvelope(cacheEntry, active);
const missRequest = o.createOrchestrationRequest({ ...active, cache_key: "rm:v1:miss" });
const hydrationMiss = o.createHydrationEnvelope(cacheEntry, missRequest);
const missJob = o.createJobEnvelope({ request: missRequest, tier: o.TIERS.FOREGROUND_USER_REQUEST });
const zoomSame = o.createJobEnvelope({
  request: { ...active, scope_role: "next_zoom" },
  tier: o.TIERS.SAME_REQUEST_NEXT_SCOPE
});
const panSame = o.createJobEnvelope({
  request: { ...active, scope_role: "pan_adjacent" },
  tier: o.TIERS.SAME_REQUEST_NEXT_SCOPE
});
const conditionChanged = o.createJobEnvelope({
  request: {
    ...active,
    cache_key: "rm:v1:condition-change",
    intent_group: "chart-a:moon-house-4"
  },
  tier: o.TIERS.ALTERNATE_INVESTIGATION
});
const chartChanged = o.createJobEnvelope({
  request: {
    ...active,
    chart_key: "chart-b",
    cache_key: "rm:v1:chart-change",
    intent_group: "chart-b:sun-house-1"
  },
  tier: o.TIERS.ALTERNATE_INVESTIGATION
});
const samplingChanged = o.createJobEnvelope({
  request: {
    ...active,
    cache_key: "rm:v1:sampling-change",
    sampling: { width: 1200, height: 700, block_px: 12, lat_cap: true }
  },
  tier: o.TIERS.SAME_REQUEST_NEXT_SCOPE
});
const marked = o.markStaleJobs(
  [zoomSame, panSame, conditionChanged, chartChanged, samplingChanged],
  active
);
const preempted = o.applyRuntimePreemption(
  [zoomSame, conditionChanged, chartChanged, samplingChanged],
  {
    ...active,
    cache_key: "rm:v1:new-user-request",
    intent_group: "chart-a:venus-house-7",
    generation: 2
  }
);
const hydratedJson = JSON.stringify(hydrationHit);
const requestJson = JSON.stringify(active);
const observerProgress = foreground.observer_progress;

const result = {
  foreground_request_creates_tier0:
    foreground.tier === 0 &&
    foreground.cache_key === active.cache_key &&
    foreground.state === "queued",
  cache_hit_creates_sanitized_metadata_hydration_without_execution:
    hydrationHit.compatible === true &&
    hydrationHit.hydrated === true &&
    hydrationHit.execution_required === false &&
    hydrationHit.hydration.status === "ready",
  cache_miss_creates_job_envelope:
    hydrationMiss.compatible === false &&
    hydrationMiss.hydrated === false &&
    missJob.tier === 0 &&
    missJob.cache_key === "rm:v1:miss",
  preemption_stales_lower_tier_jobs:
    preempted.foreground.tier === 0 &&
    preempted.foreground.cache_key === "rm:v1:new-user-request" &&
    preempted.jobs.filter(job => job.stale).length === 4 &&
    preempted.jobs.filter(job => job.cancelled).length === 4,
  same_request_zoom_pan_compatible_only_when_key_matches:
    marked.find(job => job.scope_role === "next_zoom").stale === false &&
    marked.find(job => job.scope_role === "pan_adjacent").stale === false &&
    o.classifyJobCompatibility(samplingChanged, active).compatible === false,
  condition_chart_sampling_changes_stale:
    marked.filter(job => job.stale).length === 3 &&
    marked.find(job => job.cache_key === "rm:v1:condition-change").state === "stale" &&
    marked.find(job => job.cache_key === "rm:v1:chart-change").state === "stale" &&
    marked.find(job => job.cache_key === "rm:v1:sampling-change").state === "stale",
  hydration_strips_runtime_pollution:
    !hydratedJson.includes("rendered_geojson") &&
    !hydratedJson.includes("canvas_pixels") &&
    !hydratedJson.includes("leaflet_layers") &&
    !hydratedJson.includes("renderer_output") &&
    !hydratedJson.includes("generation_mode") &&
    !hydratedJson.includes("debug") &&
    !hydratedJson.includes("aura_mode") &&
    !hydratedJson.includes("fetch_response") &&
    !hydratedJson.includes("worker_id"),
  observer_progress_read_only_and_non_controlling:
    observerProgress.read_only === true &&
    observerProgress.status === "queued" &&
    foreground.tier === 0,
  no_fetch_worker_dom_map_renderer_persistence_fields:
    !requestJson.includes("fetch_url") &&
    !requestJson.includes("worker_id") &&
    !requestJson.includes("dom_node") &&
    !requestJson.includes("renderer_substrate") &&
    !requestJson.includes("debug") &&
    !requestJson.includes("aura_mode") &&
    !requestJson.includes("localStorage") &&
    !requestJson.includes("indexedDB")
};
console.log(JSON.stringify(result));
"""
    completed = subprocess.run(
        ["node", "-e", "const source = process.argv[1];" + probe, source],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    result = run_contract_probe()
    checks = [
        "foreground_request_creates_tier0",
        "cache_hit_creates_sanitized_metadata_hydration_without_execution",
        "cache_miss_creates_job_envelope",
        "preemption_stales_lower_tier_jobs",
        "same_request_zoom_pan_compatible_only_when_key_matches",
        "condition_chart_sampling_changes_stale",
        "hydration_strips_runtime_pollution",
        "observer_progress_read_only_and_non_controlling",
        "no_fetch_worker_dom_map_renderer_persistence_fields",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_7_runtime_orchestration_contract",
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
