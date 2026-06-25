#!/usr/bin/env python3
"""Static smoke: H4X V5-2 — canonical comparison mockup promoted behind flag."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_smoke_js_syntax import assert_v5_js_syntax

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
ROUTE = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_route.js"
ADAPTER = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_adapter.js"
MOCKUP = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_beta.html"
CSS = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_beta.css"


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
    route = ROUTE.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")
    screen_compare = shell.split("function screenCompare()", 1)[1].split("\nfunction ", 1)[0]

    # Flag
    check("RM_COMPARE_V5_CANONICAL" in route, "RM_COMPARE_V5_CANONICAL flag owned by route plugin")

    # V5 shell renderer
    check("renderShellHtml" in route, "route plugin renderShellHtml exists")
    check("SHELL_FRAGMENT" in route, "mockup shell fragment embedded in route plugin")
    check(CSS.is_file(), "scoped mockup CSS file exists")
    check("comparison_v5_beta.css" in shell, "mockup CSS linked from app_shell")

  # Gating in screenCompare
    check("ComparisonV5Route.shouldRenderCanonicalShell" in screen_compare, "screenCompare gates V5 shell via route plugin")
    check("ComparisonV5Route.renderShellHtml" in screen_compare, "screenCompare calls route plugin shell renderer")
    check("rm-comparison-beta-root" in screen_compare, "legacy beta root preserved for OFF path rollback")

    # V5 ON path must not include legacy leak strings in renderer output template
    frag_fn = route
    for bad in ("Module:", "comparison-workspace-state", "comparison-columns", "stateDebugBlock", "table.simple", 'data-a2a-shape="matrix"'):
        check(bad not in frag_fn, f"V5 shell fragment does not include {bad}")
    check("rm-comparison-beta-body" not in route.split("renderShellHtml", 1)[1].split("syncRouteChrome", 1)[0], "route shell renderer does not emit rm-comparison-beta-body")

    # Canonical mounts from mockup contract
    for mount in ("rm-cmp-v5-root", "rm-cmp-zone-b", "city-bar-inner", "table-ais", "table-pih", "table-ata", "ci-cards", "rm-cmp-note", "canonical-a2a-pills"):
        check(mount in frag_fn, f"V5 shell includes mount {mount}")

    # Hydration via adapter on visible root
    check("function hydrateCanonical" in route, "route plugin canonical hydration exists")
    check("ComparisonV5Adapter.hydrate(root" in route, "route plugin hydrates visible root via adapter")
    check("getElementById(\"rm-cmp-v5-root\")" in route, "hydration targets rm-cmp-v5-root")

    # AIS four rows + A2A single-angle in adapter (unchanged contract)
    check("AIS_ANGLE_ROWS" in adapter, "adapter AIS fixed angle rows")
    check(adapter.count('"ASC"') >= 1 and adapter.count('"IC"') >= 1, "adapter defines four angles")
    check('data-a2a-shape="matrix"' not in adapter, "adapter does not emit matrix shape")
    check("canonical-a2a-pills" in adapter, "adapter uses single-angle pill model")

    # OFF path rollback present
    check("renderComparisonAisBlockShellHtml" in screen_compare, "OFF path still renders H4 AIS bottle shell")
    check("rm-comparison-beta-body" in screen_compare, "OFF path still includes legacy beta body")

    # Body class for canonical styling
    check("rm-compare-v5-canonical" in route, "canonical body class toggled in route plugin")

    # Mockup reference unchanged
    mockup = MOCKUP.read_text(encoding="utf-8")
    check("data-cmp-mount" in mockup, "mockup contract file still present")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
