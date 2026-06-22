#!/usr/bin/env python3
"""WHEEL-ORIENT-1: static + geometry checks for ecliptic CCW wheel orientation."""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def static_checks(shell: str) -> list[tuple[str, bool, str]]:
    out: list[tuple[str, bool, str]] = []
    m = re.search(
        r"function wheelEclipticToCanvasDeg\(lonDeg, ascLonDeg\)\s*\{[^}]+return\s+([^;]+);",
        shell,
        re.S,
    )
    formula = m.group(1).replace(" ", "") if m else ""
    out.append(("static_lon_minus_asc", "(norm-asc)" in formula, "canvas uses lon - asc"))
    out.append(("static_wedge_even", "wheelSvgWedgeEven" in shell, "zodiac wedgeEven helper"))
    out.append(("static_zodiac_uses_even", "wheelSvgWedgeEven(cx, cy, a1, a2, Rout, Rzod" in shell, "zodiac band uses wedgeEven"))
    out.append(("static_house_wedge_cusp", "wheelSvgWedgeCanvas(cx, cy, a1, a2, Rzod, Raring" in shell, "house band keeps wedgeCusp"))
    out.append(("static_asc_rotation_180", "WHEEL_ASC_ROTATION_DEG = 180" in shell, "ASC rotation preserved"))
    return out


def geometry_checks() -> list[tuple[str, bool, str]]:
    out: list[tuple[str, bool, str]] = []
    asc = 98.029
    cx = cy = 180.0
    rad = 150.0
    rot = 180.0

    def canvas(lon: float) -> float:
        return (lon - asc) % 360

    def polar(cdeg: float) -> tuple[float, float]:
        a = math.radians(cdeg + rot)
        return cx + rad * math.cos(a), cy - rad * math.sin(a)

    def ccw_delta(lon1: float, lon2: float) -> float:
        x1, y1 = polar(canvas(lon1))
        x2, y2 = polar(canvas(lon2))
        a1 = math.atan2(-(y1 - cy), x1 - cx)
        a2 = math.atan2(-(y2 - cy), x2 - cx)
        return (a2 - a1) % (2 * math.pi)

    x_asc, _ = polar(canvas(asc))
    out.append(("geom_asc_left", x_asc < cx, f"ASC x={x_asc:.1f}"))
    d_near = ccw_delta(asc + 5, asc + 15)
    out.append(("geom_ccw_near_asc", 0 < d_near < math.pi / 3, f"delta={d_near:.3f} rad"))
    d_sign = ccw_delta(15, 45)
    expected = math.radians(30)
    out.append(("geom_ccw_sign_step", abs(d_sign - expected) < 0.02, f"delta={d_sign:.3f} ~ pi/6"))
    return out


def main() -> int:
    shell = (ROOT / "app_shell.html").read_text(encoding="utf-8")
    results = static_checks(shell) + geometry_checks()
    passed = 0
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
        if ok:
            passed += 1
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
