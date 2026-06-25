#!/usr/bin/env python3
"""Smoke: V5 AiS format — deg / sign / min vgrid, PIH retrograde + late."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_smoke_js_syntax import assert_v5_js_syntax

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
ADAPTER = ROOT / "validation/mockups/beta/comparison_v5_adapter.js"
CSS = ROOT / "validation/mockups/beta/comparison_v5_beta.css"


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

    check('class="rm-ais-vgrid"' in shell, "aisFormatAngleDisplayHtml emits rm-ais-vgrid")
    check("formatSignDisplayHtml(angleEntry.sign)" not in shell.split("function aisFormatAngleDisplayHtml")[1].split("function formatCanonicalPlanetLongitudeHtml")[0],
          "AiS html formatter has no sign glyph html")
    check("°" not in shell.split("function aisFormatAngleDisplayHtml")[1].split("function formatCanonicalPlanetLongitudeHtml")[0]
          and "′" not in shell.split("function aisFormatAngleDisplayHtml")[1].split("function formatCanonicalPlanetLongitudeHtml")[0],
          "AiS html formatter has no degree/minute glyphs")

    check("comparisonPihHouseValueHtml" in shell, "comparisonPihHouseValueHtml helper exists")
    check("near_cusp" in shell.split("function comparisonPihHouseValueHtml")[1].split("function profilePihHouseCellHtml")[0],
          "late-in-house uses near_cusp")
    check("comparisonPihHouseValueHtml" in shell.split("deps: {")[1].split("},\n  };")[0],
          "V5 hydration passes comparisonPihHouseValueHtml")
    check("formatTablePlanetNameHtml" in adapter and "labelHtml" in adapter,
          "PIH adapter uses retrograde labelHtml")
    check("comparisonPihHouseValueHtml" in adapter, "PIH adapter uses late house value html")
    check(".rm-ais-vgrid" in css, "AIS vgrid CSS present")
    check(".cmp-pih-late" in css, "PIH late CSS present")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
