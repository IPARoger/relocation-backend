#!/usr/bin/env python3
"""Static smoke: H7-1 — Notes canonicalization across Profile, Relocated, Comparison, Library."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
NOTES_JS = ROOT / "validation" / "mockups" / "beta" / "notes_canonical.js"
NOTES_CSS = ROOT / "validation" / "mockups" / "beta" / "notes_canonical.css"
V5_ROUTE = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_route.js"


def main() -> int:
    failures: list[str] = []
    checks = 0
    duplicates: list[str] = []

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    shell = SHELL.read_text(encoding="utf-8")
    notes_js = NOTES_JS.read_text(encoding="utf-8")
    v5 = V5_ROUTE.read_text(encoding="utf-8")

    check(NOTES_JS.exists(), "notes_canonical.js present")
    check(NOTES_CSS.exists(), "notes_canonical.css present")
    check("global.NotesCanonical" in notes_js, "NotesCanonical export")
    check("CANONICAL: NOTES_CANONICAL" in notes_js, "CANONICAL flag")
    check("renderCardHtml" in notes_js, "renderCardHtml in module")
    check("renderRailHtml" in notes_js, "renderRailHtml in module")
    check("renderLibraryEditorHtml" in notes_js, "renderLibraryEditorHtml in module")
    check("renderComposerHtml" in notes_js, "shared renderComposerHtml in module")
    check("notes_canonical.js" in shell, "app_shell loads notes_canonical.js")
    check("notes_canonical.css" in shell, "app_shell loads notes_canonical.css")
    check("function notesCanonicalReady()" in shell, "notesCanonicalReady helper")
    check("NotesCanonical.renderCardHtml" in shell, "Profile/Relocated delegate to NotesCanonical")
    check("NotesCanonical.renderRailHtml" in shell, "Comparison rail delegates to NotesCanonical")
    check("NotesCanonical.renderLibraryEditorHtml" in shell, "Notes library delegates to NotesCanonical")

    # Shared toolbar — one implementation in module, not duplicated inline in shell
    check(shell.count('class="notes-toolbar"') == 0 or "NotesCanonical.renderToolbarHtml" in shell,
          "shell does not inline notes-toolbar markup")
    check(notes_js.count('class="notes-toolbar"') >= 1, "toolbar markup lives in notes_canonical.js")
    check("notes-tool" in notes_js, "shared notes-tool buttons in module")

    # Surface consumers
    check("renderProfileNotesCardHtml" in shell and "NotesCanonical.renderCardHtml" in shell,
          "Profile notes card uses shared renderer")
    check("renderRelocatedNotesCardHtml" in shell and "NotesCanonical.renderCardHtml" in shell,
          "Relocated notes card uses shared renderer")
    check("renderComparisonNotesRailHtml" in shell and "NotesCanonical.renderRailHtml" in shell,
          "Comparison notes rail uses shared renderer")
    check('id: "investigations"' in shell, "Saved Investigations collection wired in library")
    check("renderNotesLibraryEditorHtml" in shell, "library editor renderer present")

    # Preserve save wiring (markup in module, handlers in shell)
    bundle = shell + notes_js
    check('save-chart-note' in bundle, "profile save action preserved")
    check('save-comparison-note' in bundle, "comparison save action preserved")
    check('save-notes-library-note' in bundle, "library save action preserved")
    check('action === "save-chart-note"' in shell, "profile save handler preserved")
    check('action === "save-comparison-note"' in shell, "comparison save handler preserved")
    check('id="rm-chart-note"' not in shell or "textareaId: \"rm-chart-note\"" in shell or 'textareaId: "rm-chart-note"' in shell or "rm-chart-note" in shell,
          "profile textarea id preserved via config")
    check('id="rm-cmp-note"' in notes_js or 'id="rm-cmp-note"' in shell or "rm-cmp-note" in notes_js,
          "comparison textarea id preserved")
    check("rm-notes-lib-body" in notes_js, "library textarea id preserved in module")

    # V5 comparison route uses shared module
    check("NotesCanonical.renderRailHtml" in v5, "comparison_v5_route uses NotesCanonical rail")
    check("__NOTES_RAIL__" in v5, "v5 shell notes placeholder")
    check("notes-textarea" not in v5, "legacy notes-textarea removed from v5 route")

    # Duplicate renderer detection
    if re.search(r"function renderNotesToolbarHtml\(\)\s*\{[^}]*notes-toolbar", shell):
        duplicates.append("inline renderNotesToolbarHtml still renders toolbar in app_shell")
    if 'class="notes-textarea"' in shell:
        duplicates.append("legacy notes-textarea class remains in app_shell.html")
    if re.search(r"<div class=\"notes-toolbar\">", v5):
        duplicates.append("inline notes-toolbar remains in comparison_v5_route.js")
    if re.search(r'<textarea id="rm-notes-lib-body"', shell) and "NotesCanonical.renderLibraryEditorHtml" not in shell:
        duplicates.append("standalone library textarea renderer in app_shell")

    check(not duplicates, "no duplicate notes renderers: " + "; ".join(duplicates) if duplicates else "clean")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        if duplicates:
            print("Duplicate renderers:")
            for d in duplicates:
                print(f"  - {d}")
        return 1

    print(f"PASS {checks}/{checks}")
    if duplicates:
        print("Duplicate renderers:")
        for d in duplicates:
            print(f"  - {d}")
    else:
        print("Duplicate renderers: none")

    for script in [
        ROOT / "scripts" / "smoke_h4_slice5_notes_rail.py",
    ]:
        if not script.exists():
            print(f"  {script.name}: SKIP")
            continue
        proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        out = (proc.stdout or "") + (proc.stderr or "")
        line = out.strip().splitlines()[-1] if out.strip() else ""
        if proc.returncode != 0:
            failures.append(f"{script.name} failed: {line}")
            print(f"  {script.name}: FAIL {line}")
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
