#!/usr/bin/env python3
"""Static smoke: H4X V5-1 — comparison V5 shadow hydration adapter."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_smoke_js_syntax import assert_v5_js_syntax

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_adapter.js"
ROUTE = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_route.js"
SHELL = ROOT / "app_shell.html"
MOCKUP = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_beta.html"


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    assert_v5_js_syntax(check)
    adapter = ADAPTER.read_text(encoding="utf-8")
    route = ROUTE.read_text(encoding="utf-8")
    shell = SHELL.read_text(encoding="utf-8")

    check(ADAPTER.is_file(), "adapter file exists at validation/mockups/beta/comparison_v5_adapter.js")
    check("ComparisonV5Adapter" in adapter, "adapter exports ComparisonV5Adapter")
    check("function hydrate" in adapter or "hydrate:" in adapter, "adapter defines hydrate")

    # No new fetch routes / backend contracts in adapter
    check("fetch(" not in adapter, "adapter does not define fetch routes")
    check("/supabase/" not in adapter, "adapter does not call supabase paths")
    check("getA2aDisplayAngles" not in adapter, "adapter does not call getA2aDisplayAngles")

    # Authority mapping
    check("mapAuthority" in adapter, "adapter maps authority")
    check('data-cmp-mount="authority"' in adapter or "authority" in adapter, "authority mount referenced")

    # City bar
    check("mapCityBar" in adapter, "adapter maps city bar")
    check("city-card" in adapter and "bname-line-primary" in adapter, "city bar two-line name contract")
    check("data-place-id" in adapter and "data-action" in adapter, "city bar data hooks")
    check("bar-city-slot-empty" in adapter, "blank capacity slots in city bar")

    # AIS — four fixed angle rows
    check("mapAisTable" in adapter, "adapter maps AIS table")
    check(adapter.count('"ASC"') >= 1 and adapter.count('"DSC"') >= 1, "AIS includes ASC/DSC keys")
    check(adapter.count('"MC"') >= 1 and adapter.count('"IC"') >= 1, "AIS includes MC/IC keys")
    check("AIS_ANGLE_ROWS" in adapter, "AIS uses fixed angle row constant")
    check(adapter.count('key: "ASC"') >= 1 and adapter.count('key: "IC"') >= 1, "AIS_ANGLE_ROWS defines four fixed angles")

    # PIH
    check("mapPihTable" in adapter, "adapter maps PIH table")
    check("fact-table" in adapter, "adapter emits mockup fact-table class")

    # A2A single-angle model, not matrix
    check("mapA2aTable" in adapter, "adapter maps A2A table")
    check('data-a2a-shape="matrix"' not in adapter, "adapter does not emit matrix shape")
    check("canonical-a2a-pills" in adapter or "ATA_PLANETS" in adapter, "A2A single-angle planet rows")

    # Notes
    check("mapNotes" in adapter, "adapter maps notes")
    check('notes-input' in adapter, "notes textarea mount populated by adapter path")
    check("rm-cmp-note" in adapter, "notes anchor id rm-cmp-note in adapter path")

    # CI structure
    check("mapCiSection" in adapter, "adapter maps CI section")
    check("ci-card" in adapter and "data-ci-category" in adapter, "CI structure preserved")
    check("CI_CATEGORY_LABELS" in adapter or "CI_PLACEHOLDER_SNIPPETS" in adapter, "CI categories/placeholders")

    # Shadow shell + app integration without live route promotion
    check("buildShadowShellHtml" in adapter, "shadow shell builder present")
    check("rm-cmp-v5-shadow" in adapter, "shadow mount id in adapter")
    check("ComparisonV5Route.hydrateShadow" in shell, "app_shell shadow hydration delegates to route plugin")
    check("function hydrateShadow" in route, "route plugin defines shadow hydration")

    # Live compare route: V5-2 promotes canonical shell behind flag; OFF path unchanged
    screen_compare = shell.split("function screenCompare()", 1)[1].split("\nfunction ", 1)[0]
    check("RM_COMPARE_V5_CANONICAL" in route, "canonical flag owned by route plugin")
    check("renderShellHtml" in route, "route plugin shell renderer present")
    check("rm-comparison-beta-root" in screen_compare, "screenCompare still uses beta root for OFF path")
    check("hydrateShadow" not in screen_compare, "shadow hydration not wired inside screenCompare template")

    # Canonical mockup unchanged contract still valid
    mockup = MOCKUP.read_text(encoding="utf-8")
    check("data-cmp-mount" in mockup, "mockup mount contract still present")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
