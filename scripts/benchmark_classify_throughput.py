"""Measure ``/classify-points`` throughput so the feasibility estimate
("could we classify every visible pixel at once?") is grounded in real
timing, not hand-waving.

For each batch size, the script:
  * generates a fresh batch of random (lat, lon) points inside the visible
    band (-65° .. 65° latitude, full longitude),
  * posts to /classify-points,
  * records both client-observed wall time and server-reported
    compute_seconds.

Then prints a feasibility table for several relocation viewports and
target sampling resolutions. The math is straightforward; the numbers are
empirical for the current Python+swisseph stack.

Usage:
    ./venv/bin/python3 scripts/benchmark_classify_throughput.py
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path
from typing import Any

import urllib.request

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "validation" / "reports" / "classify_points_throughput.json"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
API = "http://127.0.0.1:8000"
BIRTH = {
    "birth_year": 1990, "birth_month": 6, "birth_day": 15,
    "birth_hour_utc": 12.5,
}
BATCH_SIZES = [100, 500, 1000, 5000, 20_000, 50_000]
TRIALS_PER_SIZE = 3
SEED = 12345


def random_points(n: int, rng: random.Random) -> list[dict[str, float]]:
    return [
        {"lat": rng.uniform(-65, 65), "lon": rng.uniform(-180, 180)}
        for _ in range(n)
    ]


def post_classify(points: list[dict[str, float]]) -> tuple[dict[str, Any], float]:
    body = json.dumps({**BIRTH, "points": points, "apply_lat_cap": True})
    req = urllib.request.Request(
        f"{API}/classify-points",
        data=body.encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=300) as resp:
        raw = resp.read()
    dt = time.perf_counter() - t0
    data = json.loads(raw)
    return data, dt


def main() -> int:
    rng = random.Random(SEED)
    samples: list[dict[str, Any]] = []
    for n in BATCH_SIZES:
        trials_n: list[dict[str, Any]] = []
        for t in range(TRIALS_PER_SIZE):
            pts = random_points(n, rng)
            data, dt = post_classify(pts)
            props = data["properties"]
            trial = {
                "trial": t,
                "client_seconds": round(dt, 4),
                "server_compute_seconds": props["compute_seconds"],
                "point_count": props["point_count"],
                "classified_count": props["classified_count"],
                "outside_lat_cap_count": props["outside_lat_cap_count"],
                "error_count": props["error_count"],
            }
            trials_n.append(trial)
            print(f"  n={n:>6}  trial={t}  "
                  f"client={trial['client_seconds']:.3f}s  "
                  f"server={trial['server_compute_seconds']:.3f}s  "
                  f"-> {n/trial['client_seconds']:.0f} pts/s (client) "
                  f"/ {n/trial['server_compute_seconds']:.0f} pts/s (server)")
        # aggregate
        med_client = sorted(t["client_seconds"] for t in trials_n)[len(trials_n) // 2]
        med_server = sorted(t["server_compute_seconds"] for t in trials_n)[len(trials_n) // 2]
        samples.append({
            "batch_size": n,
            "trials": trials_n,
            "median_client_seconds": med_client,
            "median_server_seconds": med_server,
            "median_client_pts_per_s": n / med_client,
            "median_server_pts_per_s": n / med_server,
        })

    # Feasibility analysis using the largest measured batch's median server rate
    # (server rate excludes HTTP overhead, which is the relevant rate for a
    # production pipeline that bypasses the wire).
    largest = samples[-1]
    pts_per_s_server = largest["median_server_pts_per_s"]
    pts_per_s_client = largest["median_client_pts_per_s"]

    # Common viewports x sampling resolutions
    SCENARIOS = [
        # (label, span_lat_deg, span_lon_deg, sample_step_deg, display_w, display_h)
        ("world @ 2.0° grid (90×180 cells)",     130, 360, 2.0,   None, None),
        ("world @ 1.0° grid",                    130, 360, 1.0,   None, None),
        ("world @ 0.5° grid",                    130, 360, 0.5,   None, None),
        ("continent @ 1.0° grid (~115×60 cells)", 60, 120, 1.0,   None, None),
        ("continent @ 0.5° grid",                 60, 120, 0.5,   None, None),
        ("continent @ 0.25° grid",                60, 120, 0.25,  None, None),
        ("continent @ 0.1° grid",                 60, 120, 0.1,   None, None),
        ("1480×900 viewport @ 1 pixel",          0, 0, 0,         1480, 900),
        ("1480×900 viewport @ 1 sample/4px",     0, 0, 0,         370, 225),
    ]
    feasibility: list[dict[str, Any]] = []
    for label, dlat, dlon, step, dw, dh in SCENARIOS:
        if dw is not None:
            n_pts = dw * dh
        else:
            n_pts = int((dlat / step) * (dlon / step))
        seconds_server = n_pts / pts_per_s_server
        seconds_client = n_pts / pts_per_s_client
        feasibility.append({
            "scenario": label,
            "point_count": n_pts,
            "seconds_single_core_server_rate": round(seconds_server, 2),
            "seconds_single_core_client_rate": round(seconds_client, 2),
            "seconds_at_8_cores_optimistic": round(seconds_server / 6.0, 2),
        })

    report = {
        "schema": "classify_points_throughput@1",
        "api": API,
        "trials_per_size": TRIALS_PER_SIZE,
        "samples": samples,
        "feasibility": feasibility,
        "notes": [
            "Server rate excludes JSON/HTTP wire overhead; production code "
            "that calls the engine in-process would see ≈ server-rate, not "
            "client-rate.",
            "Per-point cost is dominated by swe.houses (Placidus). swisseph "
            "is single-threaded per process; an 8-core machine could "
            "approach 6× throughput via multiprocessing with shared input "
            "list and per-worker swe init.",
            "These numbers are for ALL 11 planets per point. Restricting to "
            "one planet would not measurably speed things up — swe.houses "
            "is the cost, not the planet-in-house comparisons.",
        ],
    }
    OUT_PATH.write_text(json.dumps(report, indent=2))
    print("\n--- feasibility ---")
    for row in feasibility:
        print(f"  {row['scenario']:42s}  "
              f"n={row['point_count']:>10,}  "
              f"server={row['seconds_single_core_server_rate']:>7.2f}s  "
              f"8-core={row['seconds_at_8_cores_optimistic']:>6.2f}s")
    print(f"\nreport: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
