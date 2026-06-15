#!/usr/bin/env python3
"""Smoke test for the Phase 2.9 execution bridge contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "sampling_cache_orchestration_contract.js",
    ROOT / "sampling_cache_execution_bridge_contract.js",
]


def run_bridge_probe() -> dict:
    sources = [path.read_text(encoding="utf-8") for path in SOURCES]
    probe = r"""
const window = {};
sources.forEach(source => eval(source));
const orchestration = window.RelocationSamplingCacheOrchestrationContract;
const bridge = window.RelocationSamplingCacheExecutionBridgeContract;

const activeRequest = orchestration.createOrchestrationRequest({
  chart_key: "chart-a",
  investigation: { house_conditions: [{ planet: "sun", house: 1 }] },
  viewport: { north: 10, south: -10, east: 20, west: -20, zoom: 4 },
  sampling: { width: 1000, height: 700, block_px: 12, lat_cap: true },
  cache_key: "rm:v1:active",
  intent_group: "chart-a:sun-house-1",
  scope_role: "current_viewport",
  generation: 1
});
const tier0Job = orchestration.createJobEnvelope({
  request: {
    ...activeRequest,
    generation_mode: "truth_grid",
    renderer_substrate: "legacy_search_regions",
    debug: true,
    aura_mode: "raster",
    fetch_url: "/screen-pixel-truth",
    worker_id: "worker-1",
    map_id: "map"
  },
  tier: orchestration.TIERS.FOREGROUND_USER_REQUEST
});
const lowerJob = orchestration.createJobEnvelope({
  request: { ...activeRequest, cache_key: "rm:v1:lower", intent_group: "chart-a:moon-house-4" },
  tier: orchestration.TIERS.ALTERNATE_INVESTIGATION
});
const queued = bridge.createExecutionEnvelope({ job: tier0Job });
const running = bridge.transitionExecution(queued, bridge.STATES.RUNNING);
const completed = bridge.transitionExecution(running, bridge.STATES.COMPLETED);
const invalid = bridge.transitionExecution(completed, bridge.STATES.RUNNING);
const cancelled = bridge.transitionExecution(queued, bridge.STATES.CANCELLED);
const errored = bridge.transitionExecution(
  bridge.transitionExecution(bridge.createExecutionEnvelope({ job: lowerJob }), bridge.STATES.RUNNING),
  bridge.STATES.ERROR,
  {
    message: "mock error",
    renderer_output: true,
    fetch_response: { ok: false }
  }
);
const preempted = bridge.applyLogicalPreemption([tier0Job, lowerJob], {
  ...tier0Job,
  cache_key: "rm:v1:new",
  intent_group: "chart-a:venus-house-7",
  generation: 2
});
const stalePropagation = bridge.propagateStale([tier0Job, lowerJob], tier0Job);
const jsonEnvelope = JSON.stringify({ queued, running, completed, invalid, cancelled, errored, preempted, stalePropagation });

const result = {
  valid_lifecycle_transitions:
    queued.state === "queued" &&
    running.state === "running" &&
    completed.state === "completed" &&
    cancelled.state === "cancelled" &&
    errored.state === "error",
  invalid_transition_rejected:
    invalid.rejected === true &&
    invalid.rejection_reason === "invalid_transition:completed->running",
  tier0_ownership_preserved:
    queued.foreground_owned === true &&
    running.foreground_owned === true &&
    completed.foreground_owned === true,
  preemption_marks_lower_priority_incompatible:
    preempted.foreground.foreground_owned === true &&
    preempted.jobs.filter(item => item.state === "stale").length === 2 &&
    preempted.jobs.filter(item => item.job.cancelled).length === 1,
  stale_jobs_cannot_hydrate:
    bridge.canHydrate(stalePropagation.find(item => item.job.cache_key === "rm:v1:lower")) === false &&
    bridge.canHydrate(cancelled) === false &&
    bridge.canHydrate(errored) === false,
  completed_compatible_jobs_may_hydrate:
    bridge.canHydrate(completed) === true,
  observer_metadata_sanitized_read_only:
    completed.observer_progress.read_only === true &&
    completed.observer_progress.status === "completed" &&
    completed.observer_progress.completed === 1,
  runtime_pollution_stripped:
    !jsonEnvelope.includes("generation_mode") &&
    !jsonEnvelope.includes("renderer_substrate") &&
    !jsonEnvelope.includes("debug") &&
    !jsonEnvelope.includes("aura_mode") &&
    !jsonEnvelope.includes("fetch_url") &&
    !jsonEnvelope.includes("worker_id") &&
    !jsonEnvelope.includes("map_id") &&
    !jsonEnvelope.includes("renderer_output") &&
    !jsonEnvelope.includes("fetch_response"),
  no_runtime_map_persistence_coupling:
    !jsonEnvelope.includes("localStorage") &&
    !jsonEnvelope.includes("indexedDB") &&
    !jsonEnvelope.includes("Leaflet") &&
    !jsonEnvelope.includes("document") &&
    !jsonEnvelope.includes("window.fetch")
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
    result = run_bridge_probe()
    checks = [
        "valid_lifecycle_transitions",
        "invalid_transition_rejected",
        "tier0_ownership_preserved",
        "preemption_marks_lower_priority_incompatible",
        "stale_jobs_cannot_hydrate",
        "completed_compatible_jobs_may_hydrate",
        "observer_metadata_sanitized_read_only",
        "runtime_pollution_stripped",
        "no_runtime_map_persistence_coupling",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_9_execution_bridge_contract",
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
