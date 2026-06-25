#!/usr/bin/env python3
"""Static smoke: H4B Slice 1 — Comparison authority shell."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    text = SHELL.read_text(encoding="utf-8")
    sc = text.split("function screenCompare() {", 1)[1].split("function screenExport()", 1)[0]

    check("COMPARISON_BETA_NAV" in text, "comparison beta nav defined")
    check('navContext.route === "compare"\n        ? COMPARISON_BETA_NAV' in text, "renderNav uses comparison beta nav")
    check("body.rm-beta-compare .app-header" in text, "compare beta header CSS")
    check("body.rm-beta-compare main" in text and "padding: 0 28px 70px" in text.split("body.rm-beta-compare main", 1)[1][:200], "compare main pad 70px")
    check("function renderComparisonZoneBHtml" in text, "cmp-zone-b renderer")
    check('class="cmp-zone-b' in text, "cmp-zone-b class in renderer")
    check("function renderComparisonCityBarHtml" in text, "city bar renderer")
    check('class="bar-authority"' in text, "bar-authority in city bar")
    check('id="rm-cmp-city-bar-mount"' in sc, "city bar mount in screenCompare")
    check('class="rm-comparison-beta-root"' in sc, "beta root wrapper")
    check("rm-comparison-legacy-chrome" in sc, "legacy chrome wrapper for hide")
    check('navContext.route === "compare"' in text.split("function render() {", 1)[1].split("function switchChartRecord", 1)[0] and "rm-beta-compare" in text.split("function render() {", 1)[1].split("function switchChartRecord", 1)[0], "render toggles rm-beta-compare")
    check("renderComparisonTableHtml" in text, "comparison table renderer preserved")
    check("hydrateComparisonColumns" in text, "hydration preserved")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")

    for script in [
        ROOT / "scripts" / "smoke_h2_profile_transplant.py",
        ROOT / "scripts" / "smoke_h3e_relocated_shell_completion.py",
        ROOT / "scripts" / "smoke_comparison_a2a_matrix.py",
    ]:
        proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        line = (proc.stdout or proc.stderr).strip().splitlines()[-1] if proc.stdout or proc.stderr else ""
        if proc.returncode != 0:
            failures.append(f"{script.name} failed: {line}")
        else:
            print(f"  {script.name}: {line}")

    if failures:
        print(f"REGRESSION FAIL ({len(failures)})")
        for f in failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
