#!/usr/bin/env python3
"""Static smoke: H4X V5-4B — compare route state ownership."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
ROUTE = ROOT / "validation/mockups/beta/comparison_v5_route.js"

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

    shell = SHELL.read_text(encoding="utf-8")
    route = ROUTE.read_text(encoding="utf-8")
    main_body = re.search(r'<script>\n"use strict";([\s\S]*?)</script>\s*</body>', shell)
    main = main_body.group(1) if main_body else ""

    screen_compare = chunk_after(main, "function screenCompare()")
    picker = chunk_after(main, "function renderComparisonPickerShell")
    mount_fn = chunk_after(main, "function mountComparisonV5Route")
    hydrate_fn = chunk_after(main, "async function hydrateComparisonColumns")
    bind_fn = chunk_after(main, "function bindScreenActions")

    # A — no comparisonSetId → picker only, no partial V5
    check("if (!navContext.comparisonSetId)" in screen_compare, "screenCompare branches on missing comparisonSetId")
    check("renderComparisonPickerShell(origin)" in screen_compare, "no-set id uses picker shell")
    check("rm-cmp-v5-root" not in picker, "picker shell has no V5 root")
    check("Module:" not in picker, "picker shell has no Module leak")
    check("stateDebugBlock" not in picker, "picker shell has no debug JSON block")

    # A — valid comparisonSetId → canonical shell
    check("ComparisonV5Route.shouldRenderCanonicalShell" in screen_compare, "canonical gated via plugin")
    check("ComparisonV5Route.renderShellHtml" in screen_compare, "canonical renders via plugin")
    check("rm-cmp-v5-root" in route, "route plugin embeds V5 root")
    for mount in ("city-bar-inner", "table-ais", "table-pih", "table-ata", "ci-cards", "rm-cmp-note"):
        check(mount in route, f"route plugin includes mount {mount}")

    # Hydration after cols populated
    check("Array.isArray(v5ctx.cols) && v5ctx.cols.length" in hydrate_fn, "canonical hydrate waits for cols")
    check("ComparisonV5Route.hydrateCanonical" in hydrate_fn, "hydrateComparisonColumns calls canonical hydrate")
    check("_comparisonColsCache = cols" in hydrate_fn, "cols cache assigned before canonical hydrate")

    # No duplicate hydration race on compare
    check('if (navContext.route !== "compare")' in bind_fn and "hydrateComparisonColumns" in bind_fn,
          "bindScreenActions skips compare hydration (owned by mountComparisonV5Route)")
    check("canonicalActive" in mount_fn, "mountComparisonV5Route computes canonicalActive")
    check("hydrateComparisonColumns(root)" in mount_fn, "mountComparisonV5Route owns compare column hydration")

    # Valid V5 path must not include legacy Module/debug in canonical renderer
    render_shell = route.split("function renderShellHtml", 1)[1].split("function syncRouteChrome", 1)[0]
    check("Module:" not in render_shell, "canonical shell renderer has no Module leak")
    check("stateDebugBlock" not in render_shell, "canonical shell has no debug block")

    # syncRouteChrome requires canonicalActive not bare comparisonSetId
    sync_fn = route.split("function syncRouteChrome", 1)[1].split("function ensureShadowMount", 1)[0]
    check("opts.canonicalActive" in sync_fn, "syncRouteChrome uses canonicalActive flag")
    check("comparisonSetId &&" not in sync_fn.split("const on", 1)[1].split("\n", 3)[0], "syncRouteChrome on-flag not comparisonSetId-only")

    # Profile isolation
    profile = chunk_after(main, "function screenChartRecord")
    hits = [s for s in V5_SYMBOLS if s in profile]
    check(not hits, f"Profile screen has no V5 symbols (found {hits})")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
