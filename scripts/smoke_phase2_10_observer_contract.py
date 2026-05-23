#!/usr/bin/env python3
"""Smoke test for the Phase 2.10 observer/progress contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "sampling_cache_observer_contract.js"


def run_observer_probe() -> dict:
    source = CONTRACT_PATH.read_text(encoding="utf-8")
    probe = r"""
const window = {};
eval(source);
const observer = window.RelocationSamplingCacheObserverContract;

const runningPartial = observer.createObserverEnvelope({
  cache_key: "rm:v1:partial",
  intent_group: "chart-a:sun-house-1",
  state: "running",
  observer_progress: { completed: 3, total: 10 },
  discovery_state: "implied_nearby_structure",
  generation_mode: "truth_grid",
  renderer_substrate: "legacy_search_regions",
  debug: true,
  aura_mode: "raster",
  fetch_url: "/screen-pixel-truth",
  worker_id: "worker-1",
  map_id: "map"
});
const completed = observer.createObserverEnvelope({
  cache_key: "rm:v1:complete",
  intent_group: "chart-a:sun-house-1",
  state: "completed",
  discovery_state: "confirmed_discovered_structure",
  observer_progress: { completed: 10, total: 10 }
});
const hydration = observer.createObserverEnvelope({
  cache_key: "rm:v1:hydrated",
  intent_group: "chart-a:sun-house-1",
  state: "completed",
  hydrated: true,
  discovery_state: "confirmed_discovered_structure"
});
const stale = observer.createObserverEnvelope({
  cache_key: "rm:v1:stale",
  state: "stale",
  discovery_state: "confirmed_discovered_structure"
});
const cancelled = observer.createObserverEnvelope({
  cache_key: "rm:v1:cancelled",
  state: "cancelled",
  discovery_state: "implied_nearby_structure"
});
const errored = observer.createObserverEnvelope({
  cache_key: "rm:v1:error",
  state: "error",
  discovery_state: "confirmed_discovered_structure"
});
const ambiguity = observer.createObserverEnvelope({
  cache_key: "rm:v1:ambiguous",
  state: "running",
  ambiguity: true,
  observer_progress: { completed: 1, total: 4 }
});
const batch = observer.createObserverBatch([runningPartial, completed, stale]);
const serialized = JSON.stringify({
  runningPartial,
  completed,
  hydration,
  stale,
  cancelled,
  errored,
  ambiguity,
  batch
});

const result = {
  observer_envelopes_sanitized:
    !serialized.includes("generation_mode") &&
    !serialized.includes("renderer_substrate") &&
    !serialized.includes("debug") &&
    !serialized.includes("aura_mode") &&
    !serialized.includes("fetch_url") &&
    !serialized.includes("worker_id") &&
    !serialized.includes("map_id"),
  stale_cancelled_error_degrade:
    stale.observer_state === "stale" &&
    stale.color_state === "muted" &&
    stale.truth_complete === false &&
    cancelled.observer_state === "cancelled" &&
    cancelled.discovery_state === "implied_nearby_structure" &&
    errored.observer_state === "error" &&
    errored.color_state === "muted",
  partial_discovery_not_completed_truth:
    runningPartial.observer_state === "partially_discovered" &&
    runningPartial.progress_ratio === 0.3 &&
    runningPartial.truth_complete === false,
  implied_nearby_not_confirmed:
    runningPartial.discovery_state === "implied_nearby_structure" &&
    runningPartial.discovery_state !== completed.discovery_state,
  confirmed_structure_can_color:
    completed.discovery_state === "confirmed_discovered_structure" &&
    completed.color_state === "colored" &&
    completed.truth_complete === true,
  unresolved_ambiguity_distinct:
    ambiguity.discovery_state === "unresolved_ambiguity" &&
    ambiguity.truth_complete === false &&
    ambiguity.color_state === "transitioning",
  neutral_to_colored_semantics:
    runningPartial.color_state === "transitioning" &&
    completed.color_state === "colored",
  hydration_visibility:
    hydration.hydration_visible === true &&
    hydration.observer_state === "hydration_eligible",
  read_only_no_control:
    runningPartial.read_only === true &&
    runningPartial.can_control_scheduler === false &&
    runningPartial.can_control_execution === false,
  no_renderer_map_persistence_coupling:
    !serialized.includes("renderer") &&
    !serialized.includes("Leaflet") &&
    !serialized.includes("localStorage") &&
    !serialized.includes("indexedDB") &&
    !serialized.includes("document")
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
    result = run_observer_probe()
    checks = [
        "observer_envelopes_sanitized",
        "stale_cancelled_error_degrade",
        "partial_discovery_not_completed_truth",
        "implied_nearby_not_confirmed",
        "confirmed_structure_can_color",
        "unresolved_ambiguity_distinct",
        "neutral_to_colored_semantics",
        "hydration_visibility",
        "read_only_no_control",
        "no_renderer_map_persistence_coupling",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_10_observer_contract",
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
