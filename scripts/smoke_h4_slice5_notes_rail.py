#!/usr/bin/env python3
"""Static smoke: H4 Slice 5 — Comparison notes rail shell."""
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
    rail_fn = text.split("function renderComparisonNotesRailHtml", 1)[1][:1400]

    check("function renderComparisonNotesRailHtml" in text, "notes rail renderer defined")
    check('class="comparison-notes-rail"' in text, "comparison-notes-rail class")
    check('id="cmp-notes-rail"' in text, "cmp-notes-rail id")
    check("comparison-body-grid" in sc, "comparison-body-grid in screenCompare")
    check("renderComparisonNotesRailHtml" in sc, "notes rail in screenCompare")
    check('id="rm-cmp-note"' in rail_fn, "rm-cmp-note in rail renderer")
    check('data-action="save-comparison-note"' in rail_fn, "save-comparison-note in rail")
    check('id="rm-cmp-note-msg"' in rail_fn, "rm-cmp-note-msg in rail")
    check('data-action="cmp-notes-collapse"' in rail_fn, "notes collapse control in rail")
    check('data-action="cmp-notes-expand"' in text, "notes expand fab action")
    check('async function saveComparisonSetNote(' in text, "saveComparisonSetNote preserved")
    check("saveComparisonSetNote(csId" in text, "save handler calls saveComparisonSetNote")
    check("Module: comparison-notepad" not in sc, "legacy notepad panel removed from screenCompare")
    check("body.rm-beta-compare .comparison-notes-rail" in text, "notes rail CSS scoped to beta compare")
    check("268px" in text.split("comparison-body-grid", 1)[1][:400], "268px rail column width")
    check("renderComparisonAisBlockShellHtml" in sc, "AIS bottle preserved in screenCompare")
    check("renderComparisonPihBlockShellHtml" in sc, "PIH bottle preserved in screenCompare")
    check("renderComparisonA2aBlockShellHtml" in sc, "A2A bottle preserved in screenCompare")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")

    for script in [
        ROOT / "scripts" / "smoke_h4_slice4_a2a_shell.py",
        ROOT / "scripts" / "smoke_h4b_comparison_authority.py",
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
