#!/usr/bin/env python3
"""Static smoke: H4X V5-4A — comparison V5 route isolation (plugin boundary)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
ROUTE = ROOT / "validation/mockups/beta/comparison_v5_route.js"
ADAPTER = ROOT / "validation/mockups/beta/comparison_v5_adapter.js"

V5_SYMBOLS = (
    "RM_COMPARE_V5_CANONICAL",
    "ComparisonV5Adapter",
    "ComparisonV5Route",
    "renderComparisonV5",
    "hydrateComparisonV5",
    "comparisonV5",
    "buildComparisonV5",
    "mountComparisonV5",
)

ISOLATED_ROUTE_MARKERS = (
    ("Profile (chart-record)", "function screenChartRecord"),
    ("Relocated (chart)", "function screenChart"),
    ("Map", "function screenMap"),
    ("Settings", "function screenSettings"),
    ("renderNav", "function renderNav"),
)

COMPARE_ONLY_MARKERS = (
    "function screenCompare()",
    "function mountComparisonV5Route",
    "function buildComparisonV5HydrationContext",
    "async function hydrateComparisonColumns",
    "function wireComparisonPlaceToggleButtons",
)


def chunk_after(src: str, marker: str) -> str:
    if marker not in src:
        return ""
    body = src.split(marker, 1)[1]
    end = body.find("\nfunction ")
    return body if end == -1 else body[:end]


def symbols_in(text: str) -> list[str]:
    return sorted({s for s in V5_SYMBOLS if s in text})


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    shell = SHELL.read_text(encoding="utf-8")
    route = ROUTE.read_text(encoding="utf-8")

    check(ROUTE.is_file(), "comparison_v5_route.js plugin exists")
    check(ADAPTER.is_file(), "comparison_v5_adapter.js exists")
    check('src="/validation/mockups/beta/comparison_v5_adapter.js"' in shell, "adapter loaded via script src")
    check('src="/validation/mockups/beta/comparison_v5_route.js"' in shell, "route plugin loaded via script src")

    main_script = re.search(
        r'<script>\n"use strict";([\s\S]*?)</script>\s*</body>',
        shell,
    )
    check(main_script is not None, "main app script block found")
    main_body = main_script.group(1) if main_script else ""
    check("RM_COMPARE_V5_CANONICAL" not in main_body, "RM_COMPARE_V5_CANONICAL absent from main app script")
    check("RM_COMPARE_V5_CANONICAL" in route, "RM_COMPARE_V5_CANONICAL owned by route plugin")

    check("ComparisonV5Adapter" not in main_body, "ComparisonV5Adapter absent from main app script")

    for label, marker in ISOLATED_ROUTE_MARKERS:
        hits = symbols_in(chunk_after(main_body, marker))
        check(not hits, f"{label} has zero V5 symbol references (found {hits})")

    render_chunk = chunk_after(main_body, "function render()")
    render_v5 = set(symbols_in(render_chunk))
    check(
        render_v5 <= {"ComparisonV5Route", "mountComparisonV5"},
        f"render() V5 references limited to compare mount (found {render_v5})",
    )
    check(
        'if (navContext.route === "compare")' in render_chunk
        and "mountComparisonV5Route" in render_chunk,
        "mountComparisonV5Route only wired from compare branch in render()",
    )
    check("renderComparisonV5Nav" not in main_body, "global renderComparisonV5Nav removed from main script")

    for marker in COMPARE_ONLY_MARKERS:
        check(marker in main_body, f"compare helper present: {marker}")

    screen_compare = chunk_after(main_body, "function screenCompare()")
    check("ComparisonV5Route.shouldRenderCanonicalShell" in screen_compare, "screenCompare gates canonical shell via plugin")
    check("ComparisonV5Route.renderShellHtml" in screen_compare, "screenCompare renders via plugin")

    check("global.ComparisonV5Route" in route, "route plugin exports ComparisonV5Route")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
