#!/usr/bin/env python3
"""Smoke test for the Phase 2.6 in-memory cache store contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CACHE_CONTRACT_PATH = ROOT / "sampling_cache_contract.js"
STORE_CONTRACT_PATH = ROOT / "sampling_cache_store_contract.js"


def run_contract_probe() -> dict:
    cache_source = CACHE_CONTRACT_PATH.read_text(encoding="utf-8")
    store_source = STORE_CONTRACT_PATH.read_text(encoding="utf-8")
    probe = r"""
const window = {};
eval(cacheSource);
eval(storeSource);
const cache = window.RelocationSamplingCacheContract;
const storeContract = window.RelocationSamplingCacheStoreContract;
let currentTime = 1000;
const store = storeContract.createMemoryCacheStore({
  ttl_ms: 100,
  now: () => currentTime
});

const semanticA = cache.createSemanticCacheKey({
  chart_key: "chart-a",
  investigation: {
    house_conditions: [{ planet: "sun", house: 1 }]
  },
  viewport: { north: 10, south: -10, east: 20, west: -20, zoom: 4 },
  sampling: { width: 1000, height: 700, block_px: 12, lat_cap: true },
  generation_mode: "truth_grid",
  debug: true,
  aura_mode: "raster"
});
const semanticB = cache.createSemanticCacheKey({
  chart_key: "chart-a",
  investigation: {
    house_conditions: [{ planet: "moon", house: 4 }]
  },
  viewport: { north: 10, south: -10, east: 20, west: -20, zoom: 4 },
  sampling: { width: 1000, height: 700, block_px: 12, lat_cap: true }
});

store.set({
  key: semanticA.key,
  payload: {
    ...semanticA.payload,
    generation_mode: "truth_grid",
    renderer_substrate: "legacy_search_regions",
    debug: true,
    aura_mode: "raster",
    rendered_geojson: { type: "FeatureCollection" },
    canvas_pixels: "pixels",
    leaflet_layers: ["layer"],
    fetch_url: "/screen-pixel-truth",
    worker_id: "worker-1",
    backend_id: "db-1",
    user_id: "user-1"
  },
  value: {
    status: "ready",
    summary: { matched: 12 },
    metrics: { sample_count: 144 },
    error: { bad: "not string" },
    geojson: { type: "FeatureCollection" },
    canvas_pixels: "pixels",
    renderer_output: true,
    cache_hit_count: 10
  }
});
const beforeExpire = store.get(semanticA.key);
const publicJson = JSON.stringify(beforeExpire);
const hasBeforeExpire = store.has(semanticA.key);

store.set({
  key: semanticB.key,
  payload: semanticB.payload,
  value: { status: "pending", summary: { matched: 0 }, metrics: { sample_count: 0 } }
});
const distinctKeys = store.inspect().count === 2 && semanticA.key !== semanticB.key;
const invalidatedOne = store.invalidate(semanticB.key) === 1 && !store.has(semanticB.key);

const descriptorLike = { cache_key: "rm:v1:descriptor-key" };
store.set({
  cache_key: descriptorLike.cache_key,
  payload: semanticA.payload,
  value: { status: "queued" }
});
const descriptorAccepted = store.has(descriptorLike.cache_key);

currentTime = 1200;
const expiredGet = store.get(semanticA.key);
const expiredHas = store.has(semanticA.key);

const clearCount = store.clear();
const inspectAfterClear = store.inspect();

const result = {
  set_get_returns_sanitized_entry:
    beforeExpire &&
    beforeExpire.key === semanticA.key &&
    beforeExpire.schema_version === 1 &&
    beforeExpire.value.status === "ready" &&
    beforeExpire.value.error === undefined,
  has_true_before_expiration: hasBeforeExpire === true,
  expired_entries_not_returned: expiredGet === null && expiredHas === false,
  invalidate_removes_one_entry: invalidatedOne,
  clear_removes_all_entries: clearCount >= 1 && inspectAfterClear.count === 0,
  pollution_stripped:
    !publicJson.includes("generation_mode") &&
    !publicJson.includes("renderer_substrate") &&
    !publicJson.includes("debug") &&
    !publicJson.includes("aura_mode") &&
    !publicJson.includes("rendered_geojson") &&
    !publicJson.includes("canvas_pixels") &&
    !publicJson.includes("leaflet_layers") &&
    !publicJson.includes("fetch_url") &&
    !publicJson.includes("worker_id") &&
    !publicJson.includes("backend_id") &&
    !publicJson.includes("user_id") &&
    !publicJson.includes("renderer_output") &&
    !publicJson.includes("cache_hit_count"),
  different_semantic_keys_distinct: distinctKeys,
  works_with_sampling_cache_contract_output:
    beforeExpire.payload.chart_key === "chart-a" &&
    beforeExpire.payload.investigation.house_conditions[0].planet === "sun",
  accepts_scheduler_descriptor_cache_key: descriptorAccepted,
  inspect_sanitized:
    storeContract.PAYLOAD_FIELDS.includes("chart_key") &&
    !storeContract.PAYLOAD_FIELDS.includes("generation_mode") &&
    !storeContract.VALUE_FIELDS.includes("geojson")
};
console.log(JSON.stringify(result));
"""
    completed = subprocess.run(
        [
            "node",
            "-e",
            "const cacheSource = process.argv[1]; const storeSource = process.argv[2];" + probe,
            cache_source,
            store_source,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    result = run_contract_probe()
    checks = [
        "set_get_returns_sanitized_entry",
        "has_true_before_expiration",
        "expired_entries_not_returned",
        "invalidate_removes_one_entry",
        "clear_removes_all_entries",
        "pollution_stripped",
        "different_semantic_keys_distinct",
        "works_with_sampling_cache_contract_output",
        "accepts_scheduler_descriptor_cache_key",
        "inspect_sanitized",
    ]
    payload = {
        "results": [
            {
                "test": "phase2_6_in_memory_cache_store_contract",
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
