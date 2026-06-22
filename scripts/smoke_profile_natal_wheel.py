#!/usr/bin/env python3
"""PROFILE-NATAL-FACTS-1 — natal wheel panel on #/chart-record route."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"


def fn_body(text: str, name: str) -> str:
    m = re.search(rf"function {name}\([^)]*\) \{{", text)
    if not m:
        return ""
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[m.start() : i + 1]
    return text[m.start() : m.start() + 4000]


def main() -> int:
    shell = SHELL.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    checks.append((
        "static_natal_wheel_container",
        'id="rm-profile-natal-facts"' in shell and "function screenChartRecord" in shell,
        "chart-record screen includes natal facts container",
    ))

    hydrate = fn_body(shell, "hydrateProfileNatalFacts")
    checks.append((
        "static_hydrate_natal_wheel",
        "async function hydrateProfileNatalFacts" in shell,
        "hydrateProfileNatalFacts exists",
    ))
    checks.append((
        "static_natal_location_kind",
        'locationKind: "natal"' in hydrate,
        "natal hydration requests location_kind=natal",
    ))
    checks.append((
        "static_natal_reuses_wheel_renderer",
        "renderProfileNatalChartHtml" in hydrate and "fetchCanonicalRelocatedChart" in hydrate,
        "natal wheel reuses relocated-chart machinery",
    ))
    checks.append((
        "static_post_render_wires_natal",
        "hydrateProfileNatalFacts(root)" in shell,
        "post-render calls natal wheel hydration",
    ))
    checks.append((
        "static_birth_place_resolver",
        "function resolveBirthPlaceId" in shell,
        "birth place id resolver for natal coords",
    ))
    profile_block = shell[shell.find("function renderProfileNatalChartHtml"):shell.find("function renderRelocatedChartHtml")]
    checks.append((
        "static_profile_natal_wheel_section",
        "Natal wheel" in profile_block and "renderRelocatedWheelHtml" in profile_block,
        "profile natal renderer includes wheel",
    ))
    checks.append((
        "static_profile_natal_pih_section",
        "Planet houses" in profile_block and "renderPihTableRowsFromCanonical" in profile_block,
        "profile natal renderer includes PIH",
    ))
    checks.append((
        "static_profile_natal_ais_section",
        "Angles in Signs (AIS)" in profile_block and "renderAisSinglePlaceHtml" in profile_block,
        "profile natal renderer includes AIS",
    ))
    checks.append((
        "static_profile_natal_a2a_section",
        "Aspect to Angle" in profile_block and "renderA2aSinglePlaceHtml" in profile_block,
        "profile natal renderer includes A2A",
    ))

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"\n{passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
