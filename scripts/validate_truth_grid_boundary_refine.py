#!/usr/bin/env python3
"""Validate /search-regions truth_grid boundary refinement behavior."""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "validation" / "reports" / "truth_grid_boundary_refine_validation.json"

BASELINE_BIRTH = {
    "birth_year": 1990,
    "birth_month": 6,
    "birth_day": 15,
    "birth_hour_utc": 12.5,
}

HIGH_NORTH_BIRTH = {
    "birth_year": 1988,
    "birth_month": 6,
    "birth_day": 21,
    "birth_hour_utc": 3.2,
}

HOUSE_CASES = [
    {
        "case_id": "baseline_sun_1st_world",
        "birth": BASELINE_BIRTH,
        "house_conditions": [{"planet": "sun", "house": 1}],
        "angle_sign_conditions": [],
        "planet": "sun",
        "house": 1,
        "probes": [
            {"name": "americas_control", "lat": 20.0, "lon": -90.0},
            {"name": "atlantic_control", "lat": 0.0, "lon": -30.0},
            {"name": "dateline_control", "lat": 5.0, "lon": 179.0},
        ],
    },
    {
        "case_id": "high_north_sun_1st_greenland",
        "birth": HIGH_NORTH_BIRTH,
        "house_conditions": [{"planet": "sun", "house": 1}],
        "angle_sign_conditions": [],
        "planet": "sun",
        "house": 1,
        "probes": [
            {"name": "gap_ocean_1", "lat": 64.0263, "lon": -30.2749},
            {"name": "inside_yellow_1", "lat": 59.9330, "lon": -16.8750},
            {"name": "greenland_east", "lat": 64.5478, "lon": -47.7559},
            {"name": "seam_control", "lat": 62.0, "lon": 179.0},
        ],
    },
]

ANGLE_CASES = [
    {
        "case_id": "baseline_dc_cancer",
        "birth": BASELINE_BIRTH,
        "house_conditions": [],
        "angle_sign_conditions": [{"angle": "DC", "sign": "cancer"}],
        "angle": "DC",
        "sign": "cancer",
        "probes": [
            {"name": "dc_cancer_control", "lat": 20.0, "lon": -90.0},
            {"name": "dc_cancer_edge_candidate", "lat": 0.0, "lon": -30.0},
            {"name": "dateline_control", "lat": 5.0, "lon": 179.0},
        ],
    },
    {
        "case_id": "high_north_ic_cancer",
        "birth": HIGH_NORTH_BIRTH,
        "house_conditions": [],
        "angle_sign_conditions": [{"angle": "IC", "sign": "cancer"}],
        "angle": "IC",
        "sign": "cancer",
        "probes": [
            {"name": "greenland_gap", "lat": 64.0263, "lon": -30.2749},
            {"name": "ic_high_lat_control", "lat": 59.9330, "lon": -16.8750},
            {"name": "seam_control", "lat": 62.0, "lon": 179.0},
        ],
    },
]


def request_json(path: str, method: str = "GET", body: dict[str, Any] | None = None, timeout: int = 180) -> tuple[dict[str, Any], float]:
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=headers, method=method)
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload, time.perf_counter() - started


def point_in_ring(lon: float, lat: float, ring: list[list[float]]) -> bool:
    inside = False
    for i in range(len(ring)):
        j = (i - 1) % len(ring)
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > lat) != (yj > lat):
            if lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-15) + xi:
                inside = not inside
    return inside


def feature_contains(feature: dict[str, Any], lon: float, lat: float) -> bool:
    geom = feature.get("geometry") or {}
    if geom.get("type") != "Polygon":
        return False
    ring = (geom.get("coordinates") or [[]])[0]
    return point_in_ring(lon, lat, ring)


def relocated_chart(birth: dict[str, Any], lat: float, lon: float) -> dict[str, Any]:
    q = urllib.parse.urlencode({**birth, "lat": lat, "lon": lon})
    payload, _elapsed = request_json(f"/relocated-chart?{q}", timeout=60)
    return payload


def zodiac_name(index_or_name: Any) -> str:
    names = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
    ]
    if isinstance(index_or_name, int):
        if 0 <= index_or_name <= 11:
            return names[index_or_name]
        if 1 <= index_or_name <= 12:
            return names[index_or_name - 1]
    return str(index_or_name).strip().lower()


def angle_degree(chart: dict[str, Any], angle: str) -> float | None:
    angle = angle.upper()
    direct_keys = {
        "ASC": ("asc_deg",),
        "MC": ("mc_deg",),
        "DC": ("dc_deg", "desc_deg"),
        "DSC": ("dc_deg", "desc_deg"),
        "IC": ("ic_deg",),
    }
    for key in direct_keys.get(angle, (f"{angle.lower()}_deg",)):
        value = chart.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    for key in (angle, angle.lower()):
        value = chart.get(key)
        if isinstance(value, dict):
            for degree_key in ("degree", "deg", "longitude"):
                if degree_key in value:
                    return float(value[degree_key])
        if isinstance(value, (int, float)):
            return float(value)
    angles = chart.get("angles") or {}
    value = angles.get(angle) or angles.get(angle.lower())
    if isinstance(value, dict):
        for degree_key in ("degree", "deg", "longitude"):
            if degree_key in value:
                return float(value[degree_key])
    if isinstance(value, (int, float)):
        return float(value)
    return None


def search_regions(case: dict[str, Any], boundary_refine: bool) -> tuple[dict[str, Any], float]:
    payload = {
        **case["birth"],
        "house_conditions": case.get("house_conditions", []),
        "angle_sign_conditions": case.get("angle_sign_conditions", []),
        "generation_mode": "truth_grid",
        "truth_grid_resolution": 0.75,
        "truth_grid_boundary_refine": boundary_refine,
    }
    return request_json("/search-regions", method="POST", body=payload, timeout=240)


def house_features(features: list[dict[str, Any]], planet: str, house: int) -> list[dict[str, Any]]:
    return [
        feature for feature in features
        if (feature.get("properties") or {}).get("planet") == planet
        and (feature.get("properties") or {}).get("house") == house
    ]


def angle_features(features: list[dict[str, Any]], angle: str, sign: str) -> list[dict[str, Any]]:
    return [
        feature for feature in features
        if (feature.get("properties") or {}).get("condition_type") == "angle_sign"
        and str((feature.get("properties") or {}).get("angle", "")).upper() == angle.upper()
        and str((feature.get("properties") or {}).get("sign", "")).lower() == sign.lower()
    ]


def summarize_geo(geo: dict[str, Any], elapsed_seconds: float) -> dict[str, Any]:
    features = geo.get("features") or []
    props = geo.get("properties") or {}
    truth_grid = props.get("truth_grid") or {}
    angle_sign = props.get("angle_sign") or {}
    feature_props = [
        feature.get("properties") or {}
        for feature in features
        if feature.get("geometry", {}).get("type") == "Polygon"
    ]
    return {
        "elapsed_seconds": round(elapsed_seconds, 4),
        "feature_count": len(features),
        "polygon_feature_count": len(feature_props),
        "generation_mode": props.get("generation_mode"),
        "truth_grid_metadata": truth_grid,
        "angle_sign_metadata": angle_sign,
        "boundary_refined_property_count": sum(1 for props in feature_props if props.get("boundary_refined") is True),
        "coarse_resolution_property_count": sum(1 for props in feature_props if "coarse_resolution" in props),
        "validation_contradiction_sum": sum(int(props.get("validation_contradictions") or 0) for props in feature_props),
    }


def compare_summaries(unrefined: dict[str, Any], refined: dict[str, Any]) -> dict[str, Any]:
    ratio = refined["elapsed_seconds"] / unrefined["elapsed_seconds"] if unrefined["elapsed_seconds"] else None
    return {
        "feature_count_delta": refined["feature_count"] - unrefined["feature_count"],
        "polygon_feature_count_delta": refined["polygon_feature_count"] - unrefined["polygon_feature_count"],
        "elapsed_seconds_delta": round(refined["elapsed_seconds"] - unrefined["elapsed_seconds"], 4),
        "elapsed_seconds_ratio": round(ratio, 3) if ratio is not None else None,
        "refined_has_boundary_properties": refined["boundary_refined_property_count"] > 0,
        "refined_has_coarse_resolution_properties": refined["coarse_resolution_property_count"] > 0,
        "refined_validation_contradictions": refined["validation_contradiction_sum"],
    }


def classify_report(cases: list[dict[str, Any]], obvious_performance_risk: bool) -> str:
    if not all(case["overall_pass"] for case in cases):
        return "promising_but_needs_more_validation"
    if obvious_performance_risk:
        return "valid_but_needs_performance_guard"
    return "accepted_production_truth_grid_improvement"


def validate_house_case(case: dict[str, Any]) -> dict[str, Any]:
    geo_false, elapsed_false = search_regions(case, False)
    geo_true, elapsed_true = search_regions(case, True)
    false_summary = summarize_geo(geo_false, elapsed_false)
    true_summary = summarize_geo(geo_true, elapsed_true)
    false_features = house_features(geo_false.get("features") or [], case["planet"], case["house"])
    true_features = house_features(geo_true.get("features") or [], case["planet"], case["house"])
    probes = []
    for probe in case["probes"]:
        lat = float(probe["lat"])
        lon = float(probe["lon"])
        chart = relocated_chart(case["birth"], lat, lon)
        houses = chart.get("planet_houses") or {}
        planet_house = (houses.get(case["planet"]) or houses.get(case["planet"].title()) or {}).get("house")
        point_truth = planet_house == case["house"]
        false_inside = any(feature_contains(feature, lon, lat) for feature in false_features)
        true_inside = any(feature_contains(feature, lon, lat) for feature in true_features)
        probes.append({
            **probe,
            "point_truth": point_truth,
            "point_house": planet_house,
            "unrefined_inside": false_inside,
            "refined_inside": true_inside,
            "unrefined_matches_point_truth": false_inside == point_truth,
            "refined_matches_point_truth": true_inside == point_truth,
        })
    return {
        "case_id": case["case_id"],
        "case_type": "house",
        "unrefined": false_summary,
        "refined": true_summary,
        "comparison": compare_summaries(false_summary, true_summary),
        "probe_results": probes,
        "overall_pass": all(probe["refined_matches_point_truth"] for probe in probes)
        and true_summary["validation_contradiction_sum"] == 0,
    }


def validate_angle_case(case: dict[str, Any]) -> dict[str, Any]:
    geo_false, elapsed_false = search_regions(case, False)
    geo_true, elapsed_true = search_regions(case, True)
    false_summary = summarize_geo(geo_false, elapsed_false)
    true_summary = summarize_geo(geo_true, elapsed_true)
    false_features = angle_features(geo_false.get("features") or [], case["angle"], case["sign"])
    true_features = angle_features(geo_true.get("features") or [], case["angle"], case["sign"])
    probes = []
    for probe in case["probes"]:
        lat = float(probe["lat"])
        lon = float(probe["lon"])
        chart = relocated_chart(case["birth"], lat, lon)
        degree = angle_degree(chart, case["angle"])
        sign = zodiac_name(int(degree // 30)) if degree is not None else None
        point_truth = sign == case["sign"]
        false_inside = any(feature_contains(feature, lon, lat) for feature in false_features)
        true_inside = any(feature_contains(feature, lon, lat) for feature in true_features)
        probes.append({
            **probe,
            "point_truth": point_truth,
            "point_sign": sign,
            "angle_degree": degree,
            "unrefined_inside": false_inside,
            "refined_inside": true_inside,
            "unrefined_matches_point_truth": false_inside == point_truth,
            "refined_matches_point_truth": true_inside == point_truth,
        })
    return {
        "case_id": case["case_id"],
        "case_type": "angle_sign",
        "unrefined": false_summary,
        "refined": true_summary,
        "comparison": compare_summaries(false_summary, true_summary),
        "probe_results": probes,
        "overall_pass": all(probe["refined_matches_point_truth"] for probe in probes)
        and true_summary["validation_contradiction_sum"] == 0,
    }


def main() -> int:
    cases = [validate_house_case(case) for case in HOUSE_CASES]
    cases.extend(validate_angle_case(case) for case in ANGLE_CASES)
    obvious_performance_risk = any(
        case["refined"]["elapsed_seconds"] > max(3.0, case["unrefined"]["elapsed_seconds"] * 4)
        for case in cases
    )
    report = {
        "description": "Truth-grid boundary refinement validation for /search-regions",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "base_url": BASE,
        "case_count": len(cases),
        "overall_pass": all(case["overall_pass"] for case in cases) and not obvious_performance_risk,
        "obvious_performance_risk": obvious_performance_risk,
        "cases": cases,
        "classification": classify_report(cases, obvious_performance_risk),
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "overall_pass": report["overall_pass"],
        "classification": report["classification"],
        "obvious_performance_risk": obvious_performance_risk,
        "report": str(REPORT_PATH),
    }, indent=2))
    return 0 if report["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
