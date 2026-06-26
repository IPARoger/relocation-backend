#!/usr/bin/env python3
"""Static smoke for M1-C popup overlay discovery + city readability."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    if not MAP.is_file():
        print(f"FAIL map file missing: {MAP}")
        return 1

    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    # Part 1 — popup reverse discovery
    check("View overlays here" in text, "popup: View overlays here button label")
    check("popup-action-view-overlays" in text, "popup: view overlays button class")
    check("extractPlanetHouseConditionsFromChartData" in text, "popup: derives from canonical chart")
    check("CANONICAL_PLANET_ORDER" in text, "popup: canonical planet order")
    check("cc.planets[planet]" in text, "popup: reads canonical_chart.planets house")
    check("buildPlanForPopupOverlayDiscovery" in text, "popup: plan builder for overlay run")
    check('source: "popup_overlay_discovery"' in text, "popup: uses popup_overlay_discovery source")
    check("executeSearchPlan(plan" in text, "popup: calls executeSearchPlan")
    check("popup-overlay-run" in text, "popup: per-condition run buttons")
    check("formatHouseOrdinal" in text, "popup: ordinal house labels (no scoring)")

    # Part 2 — city readability
    check("CITY_VIEWPORT_CAP_BY_ZOOM" in text, "city: viewport cap table")
    check("getCityMarkerTier" in text, "city: marker tier logic")
    check("getCityMarkerStyle" in text, "city: tiered marker styles")
    check('tier === "major"' in text and 'tier === "minor"' in text, "city: major differs from minor")
    check(".slice(0, viewportCap)" in text, "city: viewport cap enforced")
    check("rm-city-label--major" in text, "city: optional major-city labels")

    # Regression guards
    check("smoothFactor: 0" in text, "unchanged: smoothFactor 0")
    check('generation_mode") || "truth_grid"' in text, "unchanged: truth_grid default")
    check("data-overlay-final" in text, "M1-B: overlay-final hook preserved")

    if failures:
        print(f"FAIL {len(failures)}/{checks} M1-C checks")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks} M1-C popup + city readability checks")

    for script in ("smoke_m1a_map_control_truth.py", "smoke_m1b_overlay_truth.py"):
        p = ROOT / "scripts" / script
        r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True)
        line = (r.stdout or r.stderr).strip().splitlines()[-1] if r.stdout or r.stderr else ""
        if r.returncode != 0:
            print(f"FAIL regression {script}: {line}")
            return 1
        print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
