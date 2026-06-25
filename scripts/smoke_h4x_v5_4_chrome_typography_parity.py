#!/usr/bin/env python3
"""Static smoke: H4X V5-4 — comparison chrome + typography parity fixes."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_smoke_js_syntax import assert_v5_js_syntax

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
ROUTE = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_route.js"
CSS = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_beta.css"
ADAPTER = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_adapter.js"


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
    css = CSS.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")

    # Mockup nav chrome
    check('id="rm-cmp-v5-nav"' in shell, "V5 mockup nav mount exists")
    check("function syncRouteChrome" in route, "route plugin syncRouteChrome exists")
    check("mountComparisonV5Route" in shell, "compare-only mountComparisonV5Route exists")
    nav_fn = route.split("function syncRouteChrome", 1)[1].split("\n  function ", 1)[0]
    for label in ("Relocation", "Map", "Charts", "Compare", "Settings"):
        check(label in nav_fn, f"V5 nav includes label {label}")
    check("cmp-v5-nav-charts" in route, "Charts nav action in route plugin nav")
    check('header.hidden = on' in nav_fn or "header.hidden = on" in nav_fn.replace(" ", ""), "generic app-header hidden on V5 path")

    # Body class + geometry overrides
    check("rm-compare-v5-canonical" in route, "canonical body class toggled in route plugin")
    check("V5-4 chrome + typography parity" in css, "V5-4 CSS block present")
    check("body.rm-compare-v5-canonical.rm-beta-compare main" in css, "main geometry override for canonical")
    check("max-width:none" in css.split("V5-4", 1)[1], "beta main max-width neutralized under canonical")
    check("body.rm-compare-v5-canonical body{" not in css, "invalid double-body selector removed")

    # Typography tokens on V5 root
    check("font-family:var(--serif)" in css and ".rm-cmp-v5-root .block-title" in css, "serif on block titles")
    check(".rm-cmp-v5-root .fact-table" in css or ".rm-cmp-v5-root .label-col" in css, "sans on table text")

    # Authority plate tools + formatting deps
    check("profile-caret" in adapter and "profile-btn" in adapter, "adapter authority tools markup")
    check("formatComparisonAuthorityBirthDate" in route, "birth date formatting helper in route plugin")
    check("comparisonAuthorityGlyphHtml" in route, "glyph slot helper in route plugin")
    check("formatComparisonAuthorityBirthDate" in route.split("withAdapterDeps", 1)[1], "formatting deps passed to adapter hydrate")

    # City bar rhythm CSS-only
    check("city-ctrls" in css.split("V5-4", 1)[1] and "flex-wrap:nowrap" in css.split("V5-4", 1)[1], "city controls nowrap in V5-4 CSS")

    # No regressions on structural mounts / legacy leak guards
    screen_compare = shell.split("function screenCompare()", 1)[1].split("\nfunction ", 1)[0]
    check("ComparisonV5Route.renderShellHtml" in screen_compare, "V5 shell renderer still gated via plugin")
    check("rm-comparison-beta-root" in screen_compare, "OFF path rollback preserved")
    for mount in ("table-ais", "table-pih", "table-ata", "rm-cmp-zone-b", "city-bar-inner"):
        check(mount in route, f"mount preserved in route plugin: {mount}")

    check("Module:" not in route, "V5 shell has no Module leak")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
