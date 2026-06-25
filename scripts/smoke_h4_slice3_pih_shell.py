#!/usr/bin/env python3
"""Static smoke: H4 Slice 3 — Comparison PIH bottled shell."""
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
    pih_fn = text.split("function renderComparisonPihBlockShellHtml", 1)[1][:800]

    check("function renderComparisonPihBlockShellHtml" in text, "PIH bottle renderer defined")
    check('class="cmp-block cmp-block-pih"' in text, "cmp-block-pih class")
    check('id="rm-cmp-bottle-pih-body"' in text, "bottle PIH body id")
    check('data-action="cmp-toggle-bottle-pih"' in text, "bottle PIH collapse action")
    check("Planet in House" in pih_fn, "PIH title in bottle")
    check("renderComparisonPihBlockShellHtml" in sc, "PIH bottle in screenCompare")
    check('rm-cmp-section[data-cmp-section="pih"] { display: none' in text, "workspace PIH hidden in beta")
    check("rm-cmp-bottle-pih-body" in text.split("function refreshPihWorkbookSection", 1)[1][:500], "refresh targets bottle body")
    check("renderPihComparisonHtml" in text, "canonical PIH renderer preserved")
    check("renderPihWorkbookSectionBody" in text, "PIH workbook body preserved")
    check("renderComparisonAisBlockShellHtml" in sc, "AIS bottle preserved in screenCompare")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")

    for script in [
        ROOT / "scripts" / "smoke_h4_slice2_ais_shell.py",
        ROOT / "scripts" / "smoke_h4b_comparison_authority.py",
        ROOT / "scripts" / "smoke_h2_profile_transplant.py",
        ROOT / "scripts" / "smoke_h3e_relocated_shell_completion.py",
        ROOT / "scripts" / "smoke_comparison_a2a_matrix.py",
    ]:
        if not script.exists():
            print(f"  {script.name}: SKIP (not on disk)")
            continue
        proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        out = (proc.stdout or "") + (proc.stderr or "")
        line = out.strip().splitlines()[-1] if out.strip() else ""
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
