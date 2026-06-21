#!/usr/bin/env python3
"""A2A-MOTION-1 — applying/separating/exact on canonical aspect rows."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MOTION_FIELDS = frozenset({"exact", "applying", "separating", "motion"})
MOTION_ENUM = frozenset({"applying", "separating", "exact", "unknown"})


def static_checks() -> list[tuple[str, bool, str]]:
    main = (ROOT / "main_centerline_FIXER.py").read_text(encoding="utf-8")
    defaults = json.loads((ROOT / "settings" / "astrology_settings_defaults.json").read_text())
    out: list[tuple[str, bool, str]] = []
    out.append(("static_motion_helper", "_aspect_motion_fields" in main, "motion helper"))
    out.append(("static_angle_speeds", "_angle_speeds_deg_per_day" in main, "angle speed sample"))
    out.append(("static_exact_default", defaults.get("exact_aspect_threshold_deg") == 0.5, "exact threshold default"))
    out.append(("static_a2a_motion_merge", "motion_fields" in main, "A2A merge"))
    out.append(("static_p2p_motion_merge", "_compute_aspects_planet_to_planet" in main, "P2P merge"))
    return out


def unit_checks() -> list[tuple[str, bool, str]]:
    from main_centerline_FIXER import (
        _P2P_ASPECT_TARGET_DEG,
        _aspect_motion_fields,
        _separation_from_exact,
    )

    out: list[tuple[str, bool, str]] = []
    lon_a, lon_b = 88.0, 0.0
    delta = _separation_from_exact(lon_a, lon_b, "square", _P2P_ASPECT_TARGET_DEG)
    applying = _aspect_motion_fields(
        delta, lon_a, 1.0, lon_b, 0.0, "square", _P2P_ASPECT_TARGET_DEG,
        station_a=False, station_b=False, exact_threshold=0.5,
    )
    out.append(("unit_applying", applying.get("motion") == "applying", str(applying)))

    exact = _aspect_motion_fields(
        0.2, 89.8, 1.0, 0.0, 0.0, "square", _P2P_ASPECT_TARGET_DEG,
        station_a=False, station_b=False, exact_threshold=0.5,
    )
    out.append(("unit_exact", exact.get("motion") == "exact", str(exact)))

    lon_a, lon_b = 91.0, 0.0
    delta = _separation_from_exact(lon_a, lon_b, "square", _P2P_ASPECT_TARGET_DEG)
    separating = _aspect_motion_fields(
        delta, lon_a, 1.0, lon_b, 0.0, "square", _P2P_ASPECT_TARGET_DEG,
        station_a=False, station_b=False, exact_threshold=0.5,
    )
    out.append(("unit_separating", separating.get("motion") == "separating", str(separating)))

    station = _aspect_motion_fields(
        2.0, 88.0, 0.01, 0.0, 0.0, "square", _P2P_ASPECT_TARGET_DEG,
        station_a=True, station_b=False, exact_threshold=0.5,
    )
    out.append(("unit_station_unknown", station.get("motion") == "unknown", str(station)))
    return out


def api_checks() -> list[tuple[str, bool, str]]:
    from fastapi.testclient import TestClient
    from main_centerline_FIXER import app

    client = TestClient(app)
    url = (
        "/relocated-chart?lat=40.7128&lon=-74.0060"
        "&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0"
    )
    resp = client.get(url)
    out: list[tuple[str, bool, str]] = []
    if resp.status_code != 200:
        out.append(("be_relocated_chart", False, f"status={resp.status_code}"))
        return out

    cc = resp.json().get("canonical_chart") or {}
    a2a = cc.get("aspects_to_angles") or []
    p2p = cc.get("aspects_planet_to_planet") or []
    a2a_ok = bool(a2a) and all(MOTION_FIELDS.issubset(r.keys()) for r in a2a)
    p2p_ok = bool(p2p) and all(MOTION_FIELDS.issubset(r.keys()) for r in p2p)
    enum_ok = all(r.get("motion") in MOTION_ENUM for rows in (a2a, p2p) for r in rows)
    bool_ok = all(
        isinstance(r.get("exact"), bool)
        and isinstance(r.get("applying"), bool)
        and isinstance(r.get("separating"), bool)
        for rows in (a2a, p2p) for r in rows
    )
    pluto_rows = [r for r in p2p if "Pluto" in (r.get("body_a"), r.get("body_b"))]
    pluto_unknown = bool(pluto_rows) and all(r.get("motion") == "unknown" for r in pluto_rows)
    out.append(("be_a2a_motion_fields", a2a_ok, f"rows={len(a2a)}"))
    out.append(("be_p2p_motion_fields", p2p_ok, f"rows={len(p2p)}"))
    out.append(("be_motion_enum", enum_ok, "motion in enum"))
    out.append(("be_motion_bools", bool_ok, "exact/applying/separating bool"))
    out.append(("be_pluto_station_unknown", pluto_unknown, f"pluto_rows={len(pluto_rows)}"))
    return out


def main() -> int:
    results = static_checks() + unit_checks() + api_checks()
    passed = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
