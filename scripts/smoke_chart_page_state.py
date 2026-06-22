#!/usr/bin/env python3
"""Static smoke: CHART-PAGE-STATE-FIX-1 chart route state contract in app_shell.html."""
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
    return text[m.start() : m.start() + 2000]


def main() -> int:
    text = SHELL.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    checks.append((
        "primary_nav_chart_clears_placeId",
        bool(re.search(r'r\.id === "chart"[\s\S]{0,500}placeId:\s*null', text)),
        "primary nav chart branch must pass placeId: null",
    ))

    switch_body = fn_body(text, "switchChartRecord")
    checks.append((
        "profile_switch_clears_placeId_on_chart",
        'route === "chart"' in switch_body and "patch.placeId = null" in switch_body,
        "switchChartRecord must clear placeId on chart route",
    ))

    select_body = fn_body(text, "selectProfile")
    checks.append((
        "select_profile_clears_placeId_on_chart",
        'route === "chart"' in select_body and "patch.placeId = null" in select_body,
        "selectProfile must clear placeId on chart route",
    ))

    hydrate_body = fn_body(text, "hydrateRelocatedChart")
    checks.append((
        "chart_without_place_skips_relocated_fetch",
        "do not hydrate stale chart" in hydrate_body and "fetchCanonicalRelocatedChart" not in hydrate_body.split("do not hydrate stale chart")[0],
        "hydrateRelocatedChart must bail without explicit place context",
    ))

    checks.append((
        "chart_empty_state_without_place",
        "Choose a place to view a relocated chart." in text and "explicitPlaceLaunch" in text,
        "screenChart must use explicitPlaceLaunch empty state",
    ))

    map_text = (ROOT / "map_CURRENT.html").read_text(encoding="utf-8")
    checks.append((
        "explicit_place_launch_paths_preserved",
        'navigate("chart", { chartRecordId, placeId: btn.getAttribute("data-cmp-open")' in text
        and 'data-nav="chart" data-place-id' in text
        and "openChartFromMapButton" in map_text,
        "comparison/favorite/map explicit place launch hooks must remain",
    ))

    checks.append((
        "relocated_chart_copy",
        "Screen 4 — Relocated Chart" in text
        and "Relocated Chart nav does not resume a previous place" in text,
        "user-facing copy should say Relocated Chart",
    ))

    failed = [name for name, ok, _ in checks if not ok]
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
    if failed:
        print(f"FAIL {len(failed)}/{len(checks)}", file=sys.stderr)
        return 1
    print(f"PASS {len(checks)}/{len(checks)} CHART-PAGE-STATE-FIX-1 static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
