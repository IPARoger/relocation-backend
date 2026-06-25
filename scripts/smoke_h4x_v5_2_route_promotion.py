#!/usr/bin/env python3
"""Static smoke: H4X V5-2 — canonical comparison mockup promoted behind flag."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
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

    shell = SHELL.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")
    screen_compare = shell.split("function screenCompare()", 1)[1].split("\nfunction ", 1)[0]

    # Flag
    check("RM_COMPARE_V5_CANONICAL" in shell, "RM_COMPARE_V5_CANONICAL flag exists")

    # V5 shell renderer
    check("function renderComparisonV5ShellHtml" in shell, "renderComparisonV5ShellHtml exists")
    check("comparisonV5ShellFragmentHtml" in shell, "mockup shell fragment renderer exists")
    check(CSS.is_file(), "scoped mockup CSS file exists")
    check("comparison_v5_beta.css" in shell, "mockup CSS linked from app_shell")

  # Gating in screenCompare
    check("RM_COMPARE_V5_CANONICAL && cs && navContext.comparisonSetId" in screen_compare, "screenCompare gates V5 shell on flag + comparisonSetId")
    check("renderComparisonV5ShellHtml(origin, cs, ws)" in screen_compare, "screenCompare calls V5 shell renderer")
    check("rm-comparison-beta-root" in screen_compare, "legacy beta root preserved for OFF path rollback")

    # V5 ON path must not include legacy leak strings in renderer output template
    v5_renderer = shell.split("function renderComparisonV5ShellHtml", 1)[1].split("\nfunction ", 1)[0]
    frag_fn = shell.split("function comparisonV5ShellFragmentHtml", 1)[1].split("\nfunction ", 1)[0]
    for bad in ("Module:", "comparison-workspace-state", "comparison-columns", "stateDebugBlock", "table.simple", 'data-a2a-shape="matrix"'):
        check(bad not in frag_fn, f"V5 shell fragment does not include {bad}")
    check("rm-comparison-beta-body" not in v5_renderer, "V5 shell renderer does not emit rm-comparison-beta-body")

    # Canonical mounts from mockup contract
    for mount in ("rm-cmp-v5-root", "rm-cmp-zone-b", "city-bar-inner", "table-ais", "table-pih", "table-ata", "ci-cards", "rm-cmp-note", "canonical-a2a-pills"):
        check(mount in frag_fn, f"V5 shell includes mount {mount}")

    # Hydration via adapter on visible root
    check("function hydrateComparisonV5Canonical" in shell, "canonical hydration function exists")
    check("ComparisonV5Adapter.hydrate(root" in shell, "adapter hydrates visible root")
    check("getElementById(\"rm-cmp-v5-root\")" in shell, "hydration targets rm-cmp-v5-root")

    # AIS four rows + A2A single-angle in adapter (unchanged contract)
    check("AIS_ANGLE_ROWS" in adapter, "adapter AIS fixed angle rows")
    check(adapter.count('"ASC"') >= 1 and adapter.count('"IC"') >= 1, "adapter defines four angles")
    check('data-a2a-shape="matrix"' not in adapter, "adapter does not emit matrix shape")
    check("canonical-a2a-pills" in adapter, "adapter uses single-angle pill model")

    # OFF path rollback present
    check("renderComparisonAisBlockShellHtml" in screen_compare, "OFF path still renders H4 AIS bottle shell")
    check("rm-comparison-beta-body" in screen_compare, "OFF path still includes legacy beta body")

    # Body class for canonical styling
    check("rm-compare-v5-canonical" in shell, "canonical body class toggled")

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
