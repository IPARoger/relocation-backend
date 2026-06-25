#!/usr/bin/env python3
"""Smoke: H4X V5-5A — comparison build + saved-open route flow."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_smoke_js_syntax import assert_v5_js_syntax

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
MAIN = ROOT / "main_centerline_FIXER.py"


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
    main_py = MAIN.read_text(encoding="utf-8")
    main_body = re.search(r'<script>\n"use strict";([\s\S]*?)</script>\s*</body>', shell)
    main = main_body.group(1) if main_body else ""

    screen_compare = chunk_after(main, "function screenCompare()")
    create_fn = chunk_after(main, "async function createComparisonSetFromPlaceIds")
    wire_open = chunk_after(main, "function wireComparisonSetListActions")
    bind_fn = chunk_after(main, "function bindScreenActions")

    for asset in (
        "/validation/mockups/beta/comparison_v5_route.js",
        "/validation/mockups/beta/comparison_v5_adapter.js",
        "/validation/mockups/beta/comparison_v5_beta.css",
    ):
        check(asset in main_py, f"backend serves {asset}")

    check('action === "compare-build"' in bind_fn, "compare-build handler present")
    check("createComparisonSetFromPlaceIds(chartRecordId, placeIds)" in bind_fn, "build uses selected place ids")
    check("finishComparisonBuildStatus" in bind_fn, "build has Saving status exit helper")
    check("finally" in bind_fn.split("compare-build", 1)[1].split("compare-back-map", 1)[0], "build has finally for Saving exit")
    check("comparisonSetId: setId" in bind_fn, "build navigate includes comparisonSetId")
    check("ensureComparisonSetInViewModel(setId)" in bind_fn, "build ensures set in view model before navigate")

    check('fetch("/comparison-sets/create"' in create_fn, "create posts to /comparison-sets/create")
    check("place_ids" in create_fn, "create payload includes place_ids")
    check("return setId" in create_fn or "return created.id" in create_fn, "create returns comparisonSetId")

    check("rm-cr-cmp-open" in shell, "profile saved comparison Open button class")
    check("comparisonSetId: setId" in wire_open, "Open navigate includes comparisonSetId")
    check("ensureComparisonSetInViewModel(setId)" in wire_open, "Open hydrates comparison set before navigate")

    check("if (!navContext.comparisonSetId)" in screen_compare, "picker only when comparisonSetId missing")
    check('data-cmp-route-mode="missing-set"' in screen_compare, "missing set does not fall back to picker")
    check("comparisonV5Ready()" in screen_compare, "canonical path guarded when V5 route plugin missing")
    check("ComparisonV5Route.shouldRenderCanonicalShell" in screen_compare, "canonical shell gate present")

    mount_fn = chunk_after(main, "function mountComparisonV5Route")
    check("getComparisonSet(navContext.comparisonSetId)" in mount_fn, "canonical mount resolves comparison set id")
    check("comparisonV5Ready()" in mount_fn, "mount guarded when V5 plugin unavailable")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
