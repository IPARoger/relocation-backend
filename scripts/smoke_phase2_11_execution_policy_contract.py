#!/usr/bin/env python3
"""Smoke test for the Phase 2.11 execution policy contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "sampling_cache_execution_policy_contract.js"


def run_policy_probe() -> dict:
    source = CONTRACT_PATH.read_text(encoding="utf-8")
    probe = r"""
const window = {};
eval(source);
const policy = window.RelocationSamplingCacheExecutionPolicyContract;

const context = {
  budgets: { foreground: 1, same_request: 1, boundary: 1, alternate: 0, total: 3 },
  observer_cadence_ms: 500,
  speculative_limit: 1,
  priority_hint: {
    source: "future_ai_intake",
    mode: "current_location_review",
    priority: "high",
    confidence: 0.7,
    reason: "opaque user intent hint",
    astrology_meaning: "do not encode"
  }
};
const work = [
  {
    tier: 0,
    cache_key: "rm:v1:foreground",
    intent_group: "chart-a:sun-house-1",
    state: "queued",
    generation_mode: "truth_grid",
    renderer_substrate: "legacy_search_regions",
    debug: true,
    aura_mode: "raster",
    fetch_url: "/screen-pixel-truth",
    worker_id: "worker-1"
  },
  { tier: 1, cache_key: "rm:v1:same", intent_group: "chart-a:sun-house-1", state: "queued" },
  { tier: 2, cache_key: "rm:v1:boundary", intent_group: "chart-a:sun-house-1", state: "queued" },
  { tier: 3, cache_key: "rm:v1:alternate", intent_group: "chart-a:moon-house-4", state: "queued" },
  { tier: 3, cache_key: "rm:v1:alternate-2", intent_group: "chart-a:venus-house-7", state: "queued" },
  { tier: 1, cache_key: "rm:v1:stale", intent_group: "chart-a:sun-house-1", state: "stale", stale: true },
  { tier: 1, cache_key: "rm:v1:cancelled", intent_group: "chart-a:sun-house-1", state: "cancelled", cancelled: true },
  { tier: 1, cache_key: "rm:v1:truth-ready", intent_group: "chart-a:sun-house-1", state: "completed" },
  { tier: 1, cache_key: "rm:v1:hydration-ready", intent_group: "chart-a:sun-house-1", state: "completed", hydration_eligible: true }
];
const resultEnvelope = policy.applyExecutionPolicy({ context, work });
const decisions = Object.fromEntries(resultEnvelope.decisions.map(d => [d.cache_key, d]));
const serialized = JSON.stringify(resultEnvelope);

const result = {
  tier0_foreground_never_blocked:
    resultEnvelope.foreground_blocked === false &&
    decisions["rm:v1:foreground"].decision === "run",
  background_budget_capped:
    decisions["rm:v1:same"].decision === "run" &&
    decisions["rm:v1:boundary"].decision === "run" &&
    decisions["rm:v1:alternate"].decision === "throttle",
  same_request_outranks_alternate:
    resultEnvelope.decisions.findIndex(d => d.cache_key === "rm:v1:same") <
    resultEnvelope.decisions.findIndex(d => d.cache_key === "rm:v1:alternate"),
  speculative_work_throttled_or_dropped:
    decisions["rm:v1:alternate"].decision === "throttle" &&
    decisions["rm:v1:alternate-2"].decision === "throttle",
  stale_cancelled_cannot_hydrate:
    decisions["rm:v1:stale"].hydration_allowed === false &&
    decisions["rm:v1:cancelled"].hydration_allowed === false,
  completed_compatible_truth_ready:
    policy.readinessFor({ state: "completed", hydration_eligible: false }) === "truth_ready",
  readiness_distinctions_preserved:
    policy.readinessFor({ state: "completed", hydration_eligible: false }) === "truth_ready" &&
    policy.readinessFor({ state: "completed", hydration_eligible: true }) === "hydration_ready" &&
    policy.READINESS.DISPLAY_READY === "display_ready",
  observer_cadence_limited_read_only:
    decisions["rm:v1:foreground"].observer_update_allowed === true &&
    decisions["rm:v1:foreground"].observer_cadence_ms === 500,
  pollution_stripped:
    !serialized.includes("generation_mode") &&
    !serialized.includes("renderer_substrate") &&
    !serialized.includes("debug") &&
    !serialized.includes("aura_mode") &&
    !serialized.includes("fetch_url") &&
    !serialized.includes("worker_id"),
  priority_hints_opaque_no_astrology:
    resultEnvelope.context.priority_hint.source === "future_ai_intake" &&
    resultEnvelope.context.priority_hint.mode === "current_location_review" &&
    resultEnvelope.context.priority_hint.astrology_meaning_encoded === false &&
    !serialized.includes("do not encode"),
  no_runtime_coupling:
    !serialized.includes("map_CURRENT") &&
    !serialized.includes("localStorage") &&
    !serialized.includes("indexedDB") &&
    !serialized.includes("fetch") &&
    !serialized.includes("worker")
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
    result = run_policy_probe()
    checks = [
        "tier0_foreground_never_blocked",
        "background_budget_capped",
        "same_request_outranks_alternate",
        "speculative_work_throttled_or_dropped",
        "stale_cancelled_cannot_hydrate",
        "completed_compatible_truth_ready",
        "readiness_distinctions_preserved",
        "observer_cadence_limited_read_only",
        "pollution_stripped",
        "priority_hints_opaque_no_astrology",
        "no_runtime_coupling",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_11_execution_policy_contract",
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
