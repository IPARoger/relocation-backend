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
    notes_mod = (ROOT / "validation" / "mockups" / "beta" / "notes_canonical.js")
    sc = text.split("function screenCompare() {", 1)[1].split("function screenExport()", 1)[0]
    notes_fn = text.split("function renderComparisonNotesRailHtml", 1)[1].split("function renderComparisonZoneBHtml", 1)[0]
    if "NotesCanonical.renderRailHtml" in notes_fn and notes_mod.exists():
        notes_fn = notes_mod.read_text(encoding="utf-8")

    check("function renderComparisonNotesRailHtml" in text, "notes rail renderer defined")
    check("NotesCanonical.renderRailHtml" in text or (notes_mod.exists() and "renderRailHtml" in notes_mod.read_text(encoding="utf-8")), "shared notes rail module wired")
    check('class="comparison-body-grid"' in sc, "comparison-body-grid in screenCompare")
    check("comparison-notes-rail" in notes_fn, "comparison-notes-rail class")
    check('id="cmp-notes-rail"' in notes_fn, "cmp-notes-rail id")
    check('id="notes-fab"' in notes_fn, "notes-fab id")
    check("general-notes-section" in notes_fn, "general-notes-section in rail")
    check("rm-cmp-note" in notes_fn, "rm-cmp-note preserved in rail")
    check('save-comparison-note' in notes_fn, "save-comparison-note action preserved")
    check("cmp-notes-hide" in notes_fn, "notes collapse action")
    check("cmp-notes-show" in notes_fn, "notes expand action")
    check("renderComparisonNotesRailHtml" in sc, "notes rail in screenCompare")
    check("Module: comparison-notepad" not in sc, "legacy notepad panel removed from screenCompare")
    check("async function saveComparisonSetNote" in text, "saveComparisonSetNote preserved")
    check('action === "save-comparison-note"' in text, "save-comparison-note handler preserved")
    check("body.rm-beta-compare .comparison-notes-rail" in text, "notes rail CSS scoped to beta compare")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")

    for script in [
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
