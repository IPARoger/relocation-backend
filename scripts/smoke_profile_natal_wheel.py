#!/usr/bin/env python3
"""PROFILE-NATAL-WHEEL-1 — natal wheel panel on #/chart-record route."""

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
        'id="rm-profile-natal-wheel"' in shell and "function screenChartRecord" in shell,
        "chart-record screen includes natal wheel container",
    ))

    hydrate = fn_body(shell, "hydrateProfileNatalWheel")
    checks.append((
        "static_hydrate_natal_wheel",
        "async function hydrateProfileNatalWheel" in shell,
        "hydrateProfileNatalWheel exists",
    ))
    checks.append((
        "static_natal_location_kind",
        'locationKind: "natal"' in hydrate,
        "natal hydration requests location_kind=natal",
    ))
    checks.append((
        "static_natal_reuses_wheel_renderer",
        "renderRelocatedWheelHtml" in hydrate and "fetchCanonicalRelocatedChart" in hydrate,
        "natal wheel reuses relocated-chart machinery",
    ))
    checks.append((
        "static_post_render_wires_natal",
        "hydrateProfileNatalWheel(root)" in shell,
        "post-render calls natal wheel hydration",
    ))
    checks.append((
        "static_birth_place_resolver",
        "function resolveBirthPlaceId" in shell,
        "birth place id resolver for natal coords",
    ))

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"\n{passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
