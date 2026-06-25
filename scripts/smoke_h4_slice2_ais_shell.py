#!/usr/bin/env python3
"""Static smoke: H4 Slice 2 — Comparison AIS bottled shell."""
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

    check("function renderComparisonAisBlockShellHtml" in text, "AIS bottle renderer defined")
    check('class="cmp-block cmp-block-ais"' in text, "cmp-block-ais class")
    check('id="rm-cmp-bottle-ais-body"' in text, "bottle AIS body id")
    check('data-action="cmp-toggle-bottle-ais"' in text, "bottle AIS collapse action")
    check("Angle in Sign" in text.split("renderComparisonAisBlockShellHtml", 1)[1][:600], "AIS title in bottle")
    check('comparison-main' in sc and "renderComparisonAisBlockShellHtml" in sc, "comparison-main in screenCompare")
    check('rm-cmp-section[data-cmp-section="ais"] { display: none' in text, "workspace AIS hidden in beta")
    check("rm-cmp-bottle-ais-body" in text.split("function refreshAisWorkbookSection", 1)[1][:400], "refresh targets bottle body")
    check("renderAisComparisonHtml" in text, "canonical AIS renderer preserved")
    check("renderAisWorkbookSectionBody" in text, "AIS workbook body preserved")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")

    for script in [
        ROOT / "scripts" / "smoke_h4b_comparison_authority.py",
        ROOT / "scripts" / "smoke_h2_profile_transplant.py",
        ROOT / "scripts" / "smoke_h3e_relocated_shell_completion.py",
        ROOT / "scripts" / "smoke_comparison_a2a_matrix.py",
    ]:
        if not script.exists():
            print(f"  {script.name}: SKIP (not on disk)")
            continue
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
