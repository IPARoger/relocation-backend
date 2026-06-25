#!/usr/bin/env python3
"""Smoke: H4X V5-7 — final comparison punch-list audit guards."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_smoke_js_syntax import assert_v5_js_syntax

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
ADAPTER = ROOT / "validation/mockups/beta/comparison_v5_adapter.js"
CSS = ROOT / "validation/mockups/beta/comparison_v5_beta.css"
ROUTE = ROOT / "validation/mockups/beta/comparison_v5_route.js"
MAIN = ROOT / "main_centerline_FIXER.py"
AUDIT = ROOT / "COMPARISON_V5_FINAL_PUNCHLIST_AUDIT.md"


def chunk_after(src: str, marker: str) -> str:
    if marker not in src:
        return ""
    body = src.split(marker, 1)[1]
    end = body.find("\nfunction ")
    return body if end == -1 else body[:end]


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    assert_v5_js_syntax(check)
    shell = SHELL.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    route = ROUTE.read_text(encoding="utf-8")
    main_py = MAIN.read_text(encoding="utf-8")
    main_body = re.search(r'<script>\n"use strict";([\s\S]*?)</script>\s*</body>', shell)
    main = main_body.group(1) if main_body else ""

    persist_fn = chunk_after(main, "async function persistComparisonSetPlaceIds")
    move_fn = chunk_after(main, "function handleComparisonV5CanonicalAction")

    check(AUDIT.is_file(), "COMPARISON_V5_FINAL_PUNCHLIST_AUDIT.md exists")

    # Add/Replace — POST route, not legacy 405 path
    check('fetch("/comparison-sets/places"' in persist_fn, "client POST /comparison-sets/places")
    check('method: "POST"' in persist_fn, "client uses POST")
    check('@app.post("/comparison-sets/places")' in main_py, "backend POST /comparison-sets/places")
    check("_deprecated_legacy_write" in main_py, "legacy places route deprecated")
    check("applyComparisonV5PlacePick" in main, "add/replace apply path exists")

    # Diffs/Dignities — wired + honest tooltips
    check("cmpDiffTdClass" in adapter and "diffTdClass" in adapter, "adapter applies diff classes")
    check("pihDignityClass" in adapter or "dignity-supportive" in css, "dignities styling present")
    check("ComparisonV5Route.hydrateCanonical" in chunk_after(main, "function refreshComparisonDiffSurfaces"),
          "diff toggle rehydrates V5")
    check('title="Fade duplicate values' in route or 'title="Fade duplicate values' in shell,
          "diffs toggle has honest tooltip")

    # Layout / interaction polish
    check(bool(re.search(r"\.stub-restore\s*\{[^}]*min-height", css)),
          "hidden restore expanded target")
    check("cmp-city-reorder-anim" in css and "runComparisonV5CityReorderAnim" in main,
          "city reorder animation present")
    check("V5-7: city card centering" in css, "city centering V5-7 rule present")
    check("margin-left: 18px" in css, "A2A pills offset present")
    check("bar-city-slot-empty" not in adapter.split("mapCityBar", 1)[1].split("function mapAisTable", 1)[0],
          "add button adjacent (no reserved empty slots)")

    # Hatch future token
    check("FUTURE-TOKEN" in css and "cmp-col-texture" in css, "hatch future token documented in CSS")

    # Authority alignment tokens
    check("padding:28px 32px 16px" in css, "authority padding matches Profile/Map token")
    check("max-width:1320px" in css, "compare max-width token present")

    # A2A consumes canonical only (audit guard, not correctness claim)
    check("aspects_to_angles" in adapter and "buildA2aContactIndex" in adapter,
          "A2A reads canonical aspects_to_angles")

    # No legacy leaks
    render_shell = route.split("function renderShellHtml", 1)[1].split("function syncRouteChrome", 1)[0]
    check("Module:" not in render_shell, "no Module leak in shell")
    check("stateDebugBlock" not in render_shell, "no debug block in shell")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
