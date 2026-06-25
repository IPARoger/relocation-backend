#!/usr/bin/env python3
"""Static smoke: H4 Slice 6 — Comparison City Intelligence bottled shell."""
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
    ci_fn = text.split("function renderComparisonCiBlockShellHtml", 1)[1][:1200]

    check("function renderComparisonCiBlockShellHtml" in text, "CI bottle renderer defined")
    check("function renderComparisonCiWorkbookSectionBody" in text, "CI workbook body defined")
    check('class="cmp-block cmp-block-ci ci-section"' in text, "cmp-block-ci class")
    check('id="rm-cmp-bottle-ci-body"' in text, "bottle CI body id")
    check('data-action="cmp-toggle-bottle-ci"' in text, "bottle CI collapse action")
    check("City Intelligence" in ci_fn, "CI title in bottle")
    check('data-cmp-ci-wired="false"' in ci_fn, "wired false marker in bottle")
    check("renderComparisonCiBlockShellHtml" in sc, "CI bottle in screenCompare")
    check(
        'rm-cmp-section[data-cmp-section="city_intelligence"] { display: none' in text,
        "workspace CI hidden in beta",
    )
    check(
        "rm-cmp-bottle-ci-body" in text.split("function refreshComparisonCiSection", 1)[1][:500],
        "refresh targets bottle body",
    )
    check("renderComparisonAisBlockShellHtml" in sc, "AIS bottle preserved in screenCompare")
    check("renderComparisonPihBlockShellHtml" in sc, "PIH bottle preserved in screenCompare")
    check("renderComparisonA2aBlockShellHtml" in sc, "A2A bottle preserved in screenCompare")
    check("renderComparisonNotesRailHtml" in sc, "notes rail preserved in screenCompare")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")

    for script in [
        ROOT / "scripts" / "smoke_h4_slice5_notes_rail.py",
        ROOT / "scripts" / "smoke_h4_slice4_a2a_shell.py",
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
