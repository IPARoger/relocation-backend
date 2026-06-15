#!/usr/bin/env python3
"""
Smoke validation for DC/IC parity (relocated chart + angle-in-sign regions).
Requires a running main_centerline_FIXER server (default http://127.0.0.1:8000).

  python scripts/validate_sprint_dc_ic.py
  BASE_URL=http://127.0.0.1:8000 python scripts/validate_sprint_dc_ic.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def get_json(url: str) -> tuple[int, dict]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} for {url}: {body[:500]}") from e


def post_json(url: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.status, json.loads(resp.read().decode())


def angle_sign_from_longitude(deg: float) -> str:
    signs = [
        "aries",
        "taurus",
        "gemini",
        "cancer",
        "leo",
        "virgo",
        "libra",
        "scorpio",
        "sagittarius",
        "capricorn",
        "aquarius",
        "pisces",
    ]
    return signs[int((deg % 360) // 30)]


def main() -> int:
    results: dict = {
        "description": "DC/IC sprint validation — relocated chart parity + angle-in-sign spot checks.",
        "base_url": BASE,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": [],
    }
    ok_all = True

    # --- relocated chart: algebraic parity ---
    lat, lon = -33.9249, 18.4241  # Cape Town lat; within cap
    q = (
        f"{BASE}/relocated-chart?"
        f"lat={lat}&lon={lon}&birth_year=2000&birth_month=6&birth_day=21&birth_hour_utc=12"
    )
    status, chart = get_json(q)
    dc_deg = chart.get("dc_deg")
    desc_deg = chart.get("desc_deg")
    ic_deg = chart.get("ic_deg")
    mc_deg = chart.get("mc_deg")
    checks = []

    def near(a, b, eps=1e-3):
        return abs(((float(a) - float(b) + 180) % 360) - 180) < eps

    if dc_deg is None or desc_deg is None:
        checks.append({"name": "dc_desc_deg_present", "pass": False})
        ok_all = False
    else:
        same = near(dc_deg, desc_deg)
        checks.append({"name": "dc_deg_matches_desc_deg", "pass": same, "dc": dc_deg, "desc": desc_deg})
        ok_all &= same

    if ic_deg is not None and mc_deg is not None:
        ic_expected = (float(mc_deg) + 180.0) % 360
        ic_ok = near(ic_deg, ic_expected)
        checks.append({"name": "ic_deg_opposes_mc_deg", "pass": ic_ok, "ic": ic_deg, "mc": mc_deg})
        ok_all &= ic_ok

    if chart.get("dc_sign") and chart.get("desc_sign"):
        s_ok = chart["dc_sign"] == chart["desc_sign"]
        checks.append({"name": "dc_sign_matches_desc_sign", "pass": s_ok})
        ok_all &= s_ok

    # cusp fields on planets
    ph = chart.get("planet_houses") or {}
    sun = ph.get("Sun") or {}
    cusp_ok = "cusp_separation_deg" in sun and "near_cusp" in sun
    checks.append({"name": "planet_cusp_fields_present", "pass": bool(cusp_ok)})
    ok_all &= cusp_ok

    results["checks"].append({"endpoint": "relocated-chart", "status": status, "checks": checks})

    # --- search-regions angle-in-sign DC / IC ---
    body = {
        "birth_year": 2000,
        "birth_month": 6,
        "birth_day": 21,
        "birth_hour_utc": 12,
        "house_conditions": [],
        "angle_sign_conditions": [
            {"angle": "DC", "sign": angle_sign_from_longitude(float(chart["desc_deg"]))},
        ],
        "generation_mode": "truth_grid",
        "truth_grid_resolution": 3.0,
        "aspect_overlay": None,
    }
    st, fc = post_json(f"{BASE}/search-regions", body)
    polys = [f for f in fc.get("features", []) if f.get("geometry", {}).get("type") == "Polygon"]
    contra = sum((f.get("properties") or {}).get("validation_contradictions", 0) for f in polys)
    inside = False
    for f in polys:
        coords = f.get("geometry", {}).get("coordinates", [[]])[0]
        if not coords:
            continue
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        if min(lons) <= lon <= max(lons) and min(lats) <= lat <= max(lats):
            inside = True
            break
    dc_region_ok = st == 200 and contra == 0 and inside
    results["checks"].append(
        {
            "endpoint": "search-regions (DC angle sign)",
            "status": st,
            "validation_contradictions": contra,
            "point_inside_some_dc_polygon": inside,
            "pass": dc_region_ok,
        }
    )
    ok_all &= dc_region_ok

    body_ic = {
        "birth_year": 2000,
        "birth_month": 6,
        "birth_day": 21,
        "birth_hour_utc": 12,
        "house_conditions": [],
        "angle_sign_conditions": [{"angle": "IC", "sign": angle_sign_from_longitude(float(chart["ic_deg"]))}],
        "generation_mode": "truth_grid",
        "truth_grid_resolution": 3.0,
        "aspect_overlay": None,
    }
    st_ic, fc_ic = post_json(f"{BASE}/search-regions", body_ic)
    polys_ic = [f for f in fc_ic.get("features", []) if f.get("geometry", {}).get("type") == "Polygon"]
    contra_ic = sum((f.get("properties") or {}).get("validation_contradictions", 0) for f in polys_ic)
    inside_ic = False
    for f in polys_ic:
        coords = f.get("geometry", {}).get("coordinates", [[]])[0]
        if not coords:
            continue
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        if min(lons) <= lon <= max(lons) and min(lats) <= lat <= max(lats):
            inside_ic = True
            break
    ic_region_ok = st_ic == 200 and contra_ic == 0 and inside_ic
    results["checks"].append(
        {
            "endpoint": "search-regions (IC angle sign)",
            "status": st_ic,
            "validation_contradictions": contra_ic,
            "point_inside_some_ic_polygon": inside_ic,
            "pass": ic_region_ok,
        }
    )
    ok_all &= ic_region_ok

    # --- aspect-to-angle: DC contour (line features only sanity) ---
    body_aspect_dc = {
        "birth_year": 2000,
        "birth_month": 6,
        "birth_day": 21,
        "birth_hour_utc": 12,
        "house_conditions": [],
        "angle_sign_conditions": [],
        "generation_mode": "truth_grid",
        "truth_grid_resolution": 0.75,
        "aspect_overlay": {"planet": "sun", "aspect": "conjunction", "angle": "DC"},
        "aspect_resolution": 1.0,
    }
    st_ad, fc_ad = post_json(f"{BASE}/search-regions", body_aspect_dc)
    lines = [
        f
        for f in fc_ad.get("features", [])
        if f.get("geometry", {}).get("type") == "LineString"
        and (f.get("properties") or {}).get("angle") == "DC"
    ]
    aspect_dc_ok = st_ad == 200 and len(lines) >= 1
    results["checks"].append(
        {
            "endpoint": "search-regions (aspect to DC)",
            "status": st_ad,
            "dc_linestring_count": len(lines),
            "pass": aspect_dc_ok,
        }
    )
    ok_all &= aspect_dc_ok

    results["overall_pass"] = ok_all

    out_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "validation",
        "reports",
        "sprint_dc_ic_validation.json",
    )
    out_path = os.path.normpath(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")

    print(json.dumps({"overall_pass": ok_all, "report": out_path}, indent=2))
    return 0 if ok_all else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except urllib.error.URLError as e:
        print("Server not reachable:", e, file=sys.stderr)
        print("Start: uvicorn main_centerline_FIXER:app --reload", file=sys.stderr)
        raise SystemExit(2)
