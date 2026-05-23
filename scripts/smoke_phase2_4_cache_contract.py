#!/usr/bin/env python3
"""Smoke test for the narrow Phase 2.4 sampling/cache contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "sampling_cache_contract.js"


def run_contract_probe() -> dict:
    source = CONTRACT_PATH.read_text(encoding="utf-8")
    probe = r"""
const window = {};
const globalThisShim = { window };
eval(source);
const c = window.RelocationSamplingCacheContract;

const base = {
  chart_key: "lib_chart_1",
  investigation: {
    house_conditions: [
      { house: "7", planet: "Venus", type: "planet_in_house", slot: "B" },
      { planet: "Moon", house: 4, slot: "A", type: "planet_in_house" }
    ],
    angle_sign_conditions: [
      { sign: "Capricorn", angle: "MC", type: "angle_in_sign" }
    ],
    aspect_overlay: {
      planet: "Saturn",
      angle: "DSC",
      aspect: "Square",
      type: "aspect_to_angle"
    }
  },
  viewport: {
    north: 81.201419542,
    south: -72.181803556,
    east: 127.265625,
    west: -127.265625,
    zoom: 2
  },
  sampling: {
    width: 1024,
    height: 720,
    block_px: 12,
    lat_cap: true
  }
};

const equivalent = {
  debugAura: true,
  rendererSubstrate: "canonical_screen_space",
  generation_mode: "truth_grid",
  requestId: "transient",
  cacheHits: 99,
  auraMode: "raster",
  adaptiveAura: true,
  renderedGeoJson: { type: "FeatureCollection" },
  canvasPixels: "ignored",
  savedViewId: "saved-view-1",
  sampling: {
    latCap: true,
    blockPx: 12,
    height: 720,
    width: 1024
  },
  viewport: {
    west: -127.2656250001,
    east: 127.2656250001,
    south: -72.1818035564,
    north: 81.2014195421,
    zoom: 2.0004
  },
  chartKey: "lib_chart_1",
  intent: {
    aspectOverlay: { angle: "DC", aspect: "square", planet: "saturn" },
    angleSignConditions: [{ angle: "mc", sign: "capricorn" }],
    houseConditions: [
      { type: "planet_in_house", slot: "A", planet: "moon", house: 4 },
      { type: "planet_in_house", slot: "B", planet: "venus", house: 7 }
    ]
  }
};

const changedChart = { ...base, chart_key: "lib_chart_2" };
const changedCondition = {
  ...base,
  investigation: {
    ...base.investigation,
    house_conditions: [
      { planet: "moon", house: 5, slot: "A", type: "planet_in_house" },
      { planet: "venus", house: 7, slot: "B", type: "planet_in_house" }
    ]
  }
};
const changedViewport = {
  ...base,
  viewport: { ...base.viewport, zoom: 3 }
};
const changedSampling = {
  ...base,
  sampling: { ...base.sampling, width: 1200 }
};
const changedLatCap = {
  ...base,
  sampling: { ...base.sampling, lat_cap: false }
};

const keys = {
  base: c.createSemanticCacheKey(base),
  equivalent: c.createSemanticCacheKey(equivalent),
  changedChart: c.createSemanticCacheKey(changedChart),
  changedCondition: c.createSemanticCacheKey(changedCondition),
  changedViewport: c.createSemanticCacheKey(changedViewport),
  changedSampling: c.createSemanticCacheKey(changedSampling),
  changedLatCap: c.createSemanticCacheKey(changedLatCap)
};
const stable = keys.equivalent.stable_json;
const result = {
  equivalent_semantics_same_key: keys.base.key === keys.equivalent.key,
  different_chart_changes_key: keys.base.key !== keys.changedChart.key,
  different_condition_changes_key: keys.base.key !== keys.changedCondition.key,
  different_viewport_changes_key: keys.base.key !== keys.changedViewport.key,
  different_sampling_changes_key: keys.base.key !== keys.changedSampling.key,
  different_lat_cap_changes_key: keys.base.key !== keys.changedLatCap.key,
  renderer_debug_aura_transients_excluded:
    !stable.includes("generation_mode") &&
    !stable.includes("rendererSubstrate") &&
    !stable.includes("debugAura") &&
    !stable.includes("auraMode") &&
    !stable.includes("adaptiveAura") &&
    !stable.includes("renderedGeoJson") &&
    !stable.includes("canvasPixels") &&
    !stable.includes("cacheHits") &&
    !stable.includes("requestId") &&
    !stable.includes("savedViewId"),
  normalized_angle: keys.base.payload.investigation.aspect_overlay.angle,
  normalized_planet: keys.base.payload.investigation.house_conditions[0].planet,
  normalized_sampling: keys.base.payload.sampling,
  base_key: keys.base.key
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
        "equivalent_semantics_same_key",
        "different_chart_changes_key",
        "different_condition_changes_key",
        "different_viewport_changes_key",
        "different_sampling_changes_key",
        "different_lat_cap_changes_key",
        "renderer_debug_aura_transients_excluded",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_4_sampling_cache_contract",
                "pass": all(result[name] for name in checks)
                and result["normalized_angle"] == "DC"
                and result["normalized_planet"] == "moon"
                and result["normalized_sampling"]["block_px"] == 12
                and result["normalized_sampling"]["lat_cap"] is True,
                "detail": result,
            }
        ]
    }
    payload["all_pass"] = all(item["pass"] for item in payload["results"])
    print(json.dumps(payload, indent=2))
    return 0 if payload["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
