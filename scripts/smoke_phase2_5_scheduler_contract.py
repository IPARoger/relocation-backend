#!/usr/bin/env python3
"""Smoke test for the Phase 2.5 sampling/cache scheduler contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "sampling_cache_scheduler_contract.js"


def run_contract_probe() -> dict:
    source = CONTRACT_PATH.read_text(encoding="utf-8")
    probe = r"""
const window = {};
eval(source);
const s = window.RelocationSamplingCacheSchedulerContract;

const foreground = s.createWorkDescriptor({
  tier: s.TIERS.FOREGROUND_USER_REQUEST,
  cache_key: "rm:v1:foreground",
  cache_payload: {
    chart_key: "chart-a",
    investigation: { house_conditions: [{ planet: "sun", house: 1 }] },
    viewport: { north: 10, south: -10, east: 20, west: -20, zoom: 4 },
    sampling: { width: 1000, height: 700, block_px: 12, lat_cap: true },
    generation_mode: "truth_grid",
    renderer_substrate: "legacy_search_regions",
    debug: true,
    aura_mode: "raster"
  },
  scope_role: "current_viewport",
  preempt_group: "chart-a:sun-house-1"
});
const sameRequest = s.createWorkDescriptor({
  tier: s.TIERS.SAME_REQUEST_NEXT_SCOPE,
  cache_key: "rm:v1:same-request-next-zoom",
  scope_role: "next_zoom",
  preempt_group: "chart-a:sun-house-1"
});
const boundary = s.createWorkDescriptor({
  tier: s.TIERS.BOUNDARY_REFINEMENT,
  cache_key: "rm:v1:boundary",
  scope_role: "boundary_refinement",
  preempt_group: "chart-a:sun-house-1"
});
const alternate = s.createWorkDescriptor({
  tier: s.TIERS.ALTERNATE_INVESTIGATION,
  cache_key: "rm:v1:alternate",
  scope_role: "alternate_variable",
  preempt_group: "chart-a:moon-house-4"
});

const sorted = s.sortWorkDescriptors([alternate, boundary, sameRequest, foreground]);
const preempted = s.applyUserPreemption([sameRequest, boundary, alternate], {
  cache_key: "rm:v1:new-user-request",
  scope_role: "current_viewport",
  preempt_group: "chart-a:venus-house-7"
});
const publicShape = s.descriptorPublicShape(foreground);
const publicJson = JSON.stringify(publicShape);

const result = {
  tier_ordering: sorted.map(item => item.tier).join(",") === "0,1,2,3",
  descriptor_generation:
    foreground.id.startsWith("scw:v1:") &&
    foreground.tier_name === "foreground_user_request" &&
    sameRequest.tier_name === "same_request_next_scope" &&
    boundary.tier_name === "boundary_refinement" &&
    alternate.tier_name === "alternate_investigation",
  preemption_semantics:
    preempted.foreground.tier === 0 &&
    preempted.queue[0].cache_key === "rm:v1:new-user-request" &&
    preempted.queue.filter(item => item.cancelled).length === 3 &&
    preempted.queue.filter(item => item.deprioritized).length === 3,
  semantic_scope_oriented:
    foreground.cache_key === "rm:v1:foreground" &&
    foreground.scope_role === "current_viewport" &&
    foreground.preempt_group === "chart-a:sun-house-1",
  no_renderer_debug_aura_pollution:
    !publicJson.includes("generation_mode") &&
    !publicJson.includes("renderer_substrate") &&
    !publicJson.includes("debug") &&
    !publicJson.includes("aura_mode") &&
    !publicJson.includes("worker") &&
    !publicJson.includes("fetch"),
  public_fields: Object.keys(publicShape).sort(),
  queue: preempted.queue.map(item => ({
    tier: item.tier,
    cache_key: item.cache_key,
    cancelled: item.cancelled,
    deprioritized: item.deprioritized
  }))
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
        "tier_ordering",
        "descriptor_generation",
        "preemption_semantics",
        "semantic_scope_oriented",
        "no_renderer_debug_aura_pollution",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_5_sampling_cache_scheduler_contract",
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
