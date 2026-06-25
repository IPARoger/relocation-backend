#!/usr/bin/env python3
"""Static smoke: H4 Slice 4 — Comparison A2A bottled shell."""
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
    a2a_block = text.split("const CMP_A2A_ANGLE_PILLS", 1)[1].split("function renderComparisonZoneBHtml", 1)[0]

    check("function renderComparisonA2aBlockShellHtml" in text, "A2A bottle renderer defined")
    check('class="cmp-block cmp-block-a2a"' in text, "cmp-block-a2a class")
    check('id="rm-cmp-bottle-a2a-body"' in text, "bottle A2A body id")
    check('data-action="cmp-toggle-bottle-a2a"' in text, "bottle A2A collapse action")
    check("Aspect to Angle" in a2a_block, "A2A title in bottle")
    check("cmp-angle-pill" in a2a_block and "cmp-angle-pills" in a2a_block, "angle pill strip in bottle header")
    check("renderComparisonA2aBlockShellHtml" in sc, "A2A bottle in screenCompare")
    check('rm-cmp-section[data-cmp-section="a2a"] { display: none' in text, "workspace A2A hidden in beta")
    check("rm-cmp-bottle-a2a-body" in text.split("function refreshA2aWorkbookSection", 1)[1][:500], "refresh targets bottle body")
    check("renderA2aComparisonHtml" in text, "canonical A2A renderer preserved")
    check('data-a2a-shape="matrix"' in text.split("function renderA2aComparisonHtml", 1)[1].split("function renderA2aWorkbookSectionBody", 1)[0], "matrix shape preserved in renderer")
    check("renderA2aWorkbookSectionBody" in text, "A2A workbook body preserved")
    check("renderComparisonAisBlockShellHtml" in sc, "AIS bottle preserved in screenCompare")
    check("renderComparisonPihBlockShellHtml" in sc, "PIH bottle preserved in screenCompare")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")

    for script in [
        ROOT / "scripts" / "smoke_h4_slice3_pih_shell.py",
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
