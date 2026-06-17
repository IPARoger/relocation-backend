#!/usr/bin/env python3
"""
Probe Greenland/Iceland overlay boundary: popup truth vs polygon containment.

Compares /relocated-chart house assignments with point-in-rectangle checks on
/search-regions truth_grid features (with boundary refinement).

Usage:
  ./venv/bin/python3 scripts/diagnose_greenland_overlay.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
REPORT_DIR = Path(__file__).resolve().parent.parent / "validation" / "reports"

# Probe points from human QA screenshots (Greenland / Iceland gap region).
PROBE_POINTS = [
    {"name": "gap_ocean_1", "lat": 64.0263, "lon": -30.2749},
    {"name": "gap_ocean_2", "lat": 62.9535, "lon": -32.8356},
    {"name": "gap_ocean_3", "lat": 64.1861, "lon": -32.1562},
    {"name": "inside_yellow_1", "lat": 59.9330, "lon": -16.8750},
    {"name": "inside_yellow_2", "lat": 60.1306, "lon": -18.2813},
    {"name": "greenland_east", "lat": 64.5478, "lon": -47.7559},
    {"name": "greenland_east_2", "lat": 64.6487, "lon": -43.1831},
]

HIGH_NORTH_BIRTH = {
    "birth_year": 1988,
    "birth_month": 6,
    "birth_day": 21,
    "birth_hour_utc": 3.2,
}


def get_json(url: str, method: str = "GET", body: dict | None = None) -> dict:
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


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


def feature_contains(feature: dict, lon: float, lat: float) -> bool:
    geom = feature.get("geometry") or {}
    if geom.get("type") != "Polygon":
        return False
    ring = geom.get("coordinates", [[]])[0]
    return point_in_ring(lon, lat, ring)


def relocated_houses(lat: float, lon: float) -> dict[str, int]:
    q = urllib.parse.urlencode({**HIGH_NORTH_BIRTH, "lat": lat, "lon": lon})
    data = get_json(f"{BASE}/relocated-chart?{q}")
    out: dict[str, int] = {}
    for planet, info in (data.get("planet_houses") or {}).items():
        out[planet.lower()] = info["house"]
    return out


def search_regions() -> dict:
    payload = {
        **HIGH_NORTH_BIRTH,
        "house_conditions": [
            {"planet": "sun", "house": 1},
            {"planet": "venus", "house": 1},
        ],
        "angle_sign_conditions": [{"angle": "DC", "sign": "cancer"}],
        "generation_mode": "truth_grid",
        "truth_grid_resolution": 0.75,
        "truth_grid_boundary_refine": True,
    }
    return get_json(f"{BASE}/search-regions", method="POST", body=payload)


def main() -> int:
    geo = search_regions()
    features = geo.get("features") or []
    house_features = [
        f
        for f in features
        if f.get("geometry", {}).get("type") == "Polygon"
        and (f.get("properties") or {}).get("condition_type") != "angle_sign"
    ]
    sun_h1 = [f for f in house_features if (f.get("properties") or {}).get("planet") == "sun" and (f.get("properties") or {}).get("house") == 1]
    venus_h1 = [
        f
        for f in house_features
        if (f.get("properties") or {}).get("planet") == "venus" and (f.get("properties") or {}).get("house") == 1
    ]

    probes = []
    for pt in PROBE_POINTS:
        lat, lon = pt["lat"], pt["lon"]
        houses = relocated_houses(lat, lon)
        sun_inside = any(feature_contains(f, lon, lat) for f in sun_h1)
        venus_inside = any(feature_contains(f, lon, lat) for f in venus_h1)
        probes.append(
            {
                **pt,
                "popup_sun_house": houses.get("sun"),
                "popup_venus_house": houses.get("venus"),
                "sun_h1_polygon_inside": sun_inside,
                "venus_h1_polygon_inside": venus_inside,
                "sun_match": (houses.get("sun") == 1) == sun_inside,
                "venus_match": (houses.get("venus") == 1) == venus_inside,
            }
        )

    mismatches = [p for p in probes if not p["sun_match"] or not p["venus_match"]]
    report = {
        "description": "Greenland/Iceland overlay boundary probe",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "generation_mode": geo.get("properties", {}).get("generation_mode"),
        "truth_grid": geo.get("properties", {}).get("truth_grid"),
        "sun_h1_feature_count": len(sun_h1),
        "venus_h1_feature_count": len(venus_h1),
        "probe_count": len(probes),
        "mismatch_count": len(mismatches),
        "overall_pass": len(mismatches) == 0,
        "probes": probes,
        "mismatches": mismatches,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / "greenland_overlay_diagnosis.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall_pass": report["overall_pass"], "mismatch_count": len(mismatches), "report": str(path)}, indent=2))
    return 0 if report["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
