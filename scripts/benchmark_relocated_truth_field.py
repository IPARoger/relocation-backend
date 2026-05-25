"""Benchmark Layer 1 relocated truth-field throughput.

Validation-only evidence gathering. This does not implement caching,
production rendering, scheduler behavior, or aura styling.

Run:
    ./venv/bin/python scripts/benchmark_relocated_truth_field.py
"""

from __future__ import annotations

import json
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import swisseph as swe

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "validation" / "reports" / "relocated_truth_field_benchmark.json"
NARRATIVE_PATH = ROOT / "validation" / "narratives" / "relocated_truth_field_benchmark.md"
PROFILE_PATH = ROOT / "charts" / "chart_profiles.json"

LAT_MIN = -65.0
LAT_MAX = 65.0
LON_MIN = -180.0
LON_MAX = 180.0
SAMPLE_SIZES = [1, 1_000, 10_000, 83_040]
CAP_PERCENT = 0.30
DEFAULT_ORB = 10.0
ASPECT_TARGETS = {
    "conjunction": 0.0,
    "sextile": 60.0,
    "square": 90.0,
    "trine": 120.0,
    "opposition": 180.0,
}
PLANETS = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO,
}
ANGLES = ("asc", "mc", "dsc", "ic")


def load_profile() -> dict[str, Any]:
    profiles = json.loads(PROFILE_PATH.read_text())
    return next(p for p in profiles if p["id"] == "baseline_validated")


def profile_jd(profile: dict[str, Any]) -> float:
    year, month, day = [int(x) for x in profile["date"].split("-")]
    hour, minute = [int(x) for x in profile["time"].split(":")]
    return swe.julday(year, month, day, hour + minute / 60.0)


def build_points(n: int) -> list[tuple[float, float]]:
    if n == 1:
        return [(0.0, 0.0)]
    points: list[tuple[float, float]] = []
    lat_span = LAT_MAX - LAT_MIN
    lon_span = LON_MAX - LON_MIN
    # Deterministic low-discrepancy-ish grid sweep without random overhead.
    for i in range(n):
        lat = LAT_MIN + ((i * 37) % 10_000) / 10_000 * lat_span
        lon = LON_MIN + ((i * 91) % 10_000) / 10_000 * lon_span
        points.append((lat, lon))
    return points


def forward_distance(a: float, b: float) -> float:
    return (b - a) % 360.0


def signed_delta(a: float, b: float) -> float:
    return ((a - b + 180.0) % 360.0) - 180.0


def compute_planets(jd: float) -> dict[str, float]:
    return {name: swe.calc_ut(jd, pid)[0][0] % 360.0 for name, pid in PLANETS.items()}


def houses_only(jd: float, points: list[tuple[float, float]]) -> int:
    count = 0
    for lat, lon in points:
        try:
            cusps, ascmc = swe.houses(jd, lat, lon, b"P")
            _ = ascmc[0] % 360.0
            _ = ascmc[1] % 360.0
            _ = [c % 360.0 for c in cusps[:12]]
            count += 1
        except Exception:
            pass
    return count


def point_payload(jd: float, points: list[tuple[float, float]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lat, lon in points:
        try:
            cusps, ascmc = swe.houses(jd, lat, lon, b"P")
            cusps = [c % 360.0 for c in cusps[:12]]
            spans = [forward_distance(cusps[i], cusps[(i + 1) % 12]) for i in range(12)]
            asc = ascmc[0] % 360.0
            mc = ascmc[1] % 360.0
            rows.append({
                "lat": lat,
                "lon": lon,
                "asc": asc,
                "mc": mc,
                "dsc": (asc + 180.0) % 360.0,
                "ic": (mc + 180.0) % 360.0,
                "cusps": cusps,
                "spans": spans,
            })
        except Exception:
            pass
    return rows


def planet_house(planet_long: float, cusps: list[float]) -> int:
    for idx in range(12):
        start = cusps[idx]
        end = cusps[(idx + 1) % 12]
        if start <= end:
            if start <= planet_long < end:
                return idx + 1
        elif planet_long >= start or planet_long < end:
            return idx + 1
    return -1


def derive_from_payload(rows: list[dict[str, Any]], planets: dict[str, float]) -> dict[str, int]:
    pih_count = 0
    angle_sign_count = 0
    aspect_count = 0
    cap_count = 0
    for row in rows:
        cusps = row["cusps"]
        spans = row["spans"]
        for planet_long in planets.values():
            _ = planet_house(planet_long, cusps)
            pih_count += 1
        for angle in ANGLES:
            _ = int(row[angle] // 30)
            angle_sign_count += 1
        for planet_long in planets.values():
            for angle in ANGLES:
                sep = abs(signed_delta(planet_long, row[angle]))
                for target in ASPECT_TARGETS.values():
                    _ = sep - target
                    aspect_count += 1
        # Dynamic cap primitives for ASC/MC/DSC/IC adjacent pairs.
        adjacent_pairs = [(11, 0), (8, 9), (5, 6), (2, 3)]
        for left_idx, right_idx in adjacent_pairs:
            left_span = spans[left_idx]
            right_span = spans[right_idx]
            _ = min(DEFAULT_ORB, left_span * CAP_PERCENT if left_span < 30.0 else DEFAULT_ORB)
            _ = min(DEFAULT_ORB, right_span * CAP_PERCENT if right_span < 30.0 else DEFAULT_ORB)
            cap_count += 2
    return {
        "planet_in_house_evaluations": pih_count,
        "angle_sign_evaluations": angle_sign_count,
        "aspect_to_angle_evaluations": aspect_count,
        "dynamic_side_cap_evaluations": cap_count,
    }


def time_call(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


def row(label: str, point_count: int, elapsed: float, classified: int | None = None) -> dict[str, Any]:
    classified = point_count if classified is None else classified
    return {
        "workload": label,
        "point_count": point_count,
        "classified_count": classified,
        "total_seconds": round(elapsed, 6),
        "seconds_per_point": round(elapsed / max(classified, 1), 9),
        "points_per_second": round(classified / elapsed, 2) if elapsed > 0 else None,
    }


def projected_seconds(seconds_per_point: float, points: int) -> float:
    return round(seconds_per_point * points, 3)


def main() -> int:
    swe.set_ephe_path(str(ROOT / "ephe"))
    profile = load_profile()
    jd = profile_jd(profile)
    planets = compute_planets(jd)
    results: list[dict[str, Any]] = []
    derived_results: list[dict[str, Any]] = []
    first_run_issues: list[str] = []

    for n in SAMPLE_SIZES:
        points = build_points(n)
        classified, elapsed = time_call(houses_only, jd, points)
        results.append(row("A_swe_houses_only", n, elapsed, classified))

        rows, elapsed_payload = time_call(point_payload, jd, points)
        results.append(row("B_full_relocated_point_payload", n, elapsed_payload, len(rows)))

        counts, elapsed_derived = time_call(derive_from_payload, rows, planets)
        derived = row("C_derived_classifiers_from_cached_payload", n, elapsed_derived, len(rows))
        derived["evaluation_counts"] = counts
        derived_results.append(derived)
        results.append(derived)

    # Use the largest full-payload row as primary projection basis.
    payload_rows = [r for r in results if r["workload"] == "B_full_relocated_point_payload"]
    largest_payload = payload_rows[-1]
    spp = largest_payload["seconds_per_point"]
    grid_05 = int((130 / 0.5) * (360 / 0.5))
    grid_025 = int((130 / 0.25) * (360 / 0.25))
    projections = {
        "basis_workload": largest_payload,
        "83040_samples_seconds": projected_seconds(spp, 83_040),
        "world_0p5deg_points": grid_05,
        "world_0p5deg_projected_seconds": projected_seconds(spp, grid_05),
        "world_0p25deg_points": grid_025,
        "world_0p25deg_projected_seconds": projected_seconds(spp, grid_025),
    }

    cache_window = {
        "three_second_plausible_for_83040_payload": projections["83040_samples_seconds"] <= 3.0,
        "ten_second_plausible_for_83040_payload": projections["83040_samples_seconds"] <= 10.0,
        "three_second_plausible_for_0p5deg_world_payload": projections["world_0p5deg_projected_seconds"] <= 3.0,
        "ten_second_plausible_for_0p5deg_world_payload": projections["world_0p5deg_projected_seconds"] <= 10.0,
        "note": "Projection uses measured in-process full-payload timing, not HTTP overhead and not multiprocessing.",
    }

    report = {
        "schema": "relocated_truth_field_benchmark@1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "profile": profile,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor(),
        },
        "sample_sizes": SAMPLE_SIZES,
        "results": results,
        "projections": projections,
        "cache_window_assessment": cache_window,
        "recommendations": {
            "cache_immediately": [
                "natal planet/point longitudes",
                "initial relocated cusp/angle payload for current/first viewport or coarse world grid",
                "house spans needed for dynamic side caps",
                "currently selected user variable",
            ],
            "cache_on_demand": [
                "minor/custom aspects",
                "alternate house systems",
                "alternate zodiac/ayanamsa modes",
                "fine-grained 0.25 degree world fields",
                "user-overridden orb/cap-percent variants",
            ],
        },
        "limitations": [
            "In-process benchmark only; no HTTP serialization overhead measured.",
            "No multiprocessing or worker-pool optimization measured.",
            "Point generation is deterministic synthetic coverage, not exact production viewport sampling.",
            "0.5 degree and 0.25 degree world grids are projected from measured per-point timing unless later explicitly benchmarked.",
            "No production caching behavior was implemented.",
        ],
        "first_run_issues": first_run_issues,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True))

    narrative = f"""# Relocated Truth Field Benchmark

## Purpose

This validation-only benchmark measures Layer 1 relocated truth-field throughput for the existing `baseline_validated` chart. It does not implement production caching, renderer integration, aura styling, rain, virga, scheduler/cache execution, or production behavior.

## Workloads

- A: `swe.houses` only, extracting ASC, MC, cusps, and house spans.
- B: full relocated point payload: ASC, MC, DSC, IC, all cusps, all spans.
- C: derived classifiers from cached point payload: planet-in-house, angle-in-sign, aspect-to-angle signed separation, and dynamic side-cap widths.

## Key Result

Largest measured full-payload sample: `{largest_payload['point_count']}` points in `{largest_payload['total_seconds']}` seconds.

Projected `83,040` sample full-payload time: `{projections['83040_samples_seconds']}` seconds.

Projected 0.5 degree world-grid full-payload time (`{grid_05}` points): `{projections['world_0p5deg_projected_seconds']}` seconds.

Projected 0.25 degree world-grid full-payload time (`{grid_025}` points): `{projections['world_0p25deg_projected_seconds']}` seconds.

## Cache Window Assessment

- 3 second window plausible for 83,040 samples: `{cache_window['three_second_plausible_for_83040_payload']}`
- 10 second window plausible for 83,040 samples: `{cache_window['ten_second_plausible_for_83040_payload']}`
- 3 second window plausible for 0.5 degree world grid: `{cache_window['three_second_plausible_for_0p5deg_world_payload']}`
- 10 second window plausible for 0.5 degree world grid: `{cache_window['ten_second_plausible_for_0p5deg_world_payload']}`

These are in-process timings only and do not include HTTP overhead.

## Governance

No production code or renderer behavior was changed. This is evidence-gathering only.
"""
    NARRATIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    NARRATIVE_PATH.write_text(narrative)

    print(json.dumps({
        "report": str(REPORT_PATH.relative_to(ROOT)),
        "narrative": str(NARRATIVE_PATH.relative_to(ROOT)),
        "largest_payload": largest_payload,
        "projections": projections,
        "cache_window_assessment": cache_window,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
