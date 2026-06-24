#!/usr/bin/env python3
"""Static smoke for MAP-SAVE-C: save dialog (title + notes) in map_CURRENT.html."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []

    # Modal element
    if 'id="rm-save-dialog"' not in text:
        failures.append("#rm-save-dialog element must exist")

    # Required form fields
    if 'id="rm-sdlg-title-input"' not in text:
        failures.append("#rm-sdlg-title-input (title input) must exist")
    if 'id="rm-sdlg-note-input"' not in text:
        failures.append("#rm-sdlg-note-input (notes textarea) must exist")
    if 'id="rm-sdlg-confirm"' not in text:
        failures.append("#rm-sdlg-confirm (Save button) must exist")
    if 'id="rm-sdlg-cancel"' not in text:
        failures.append("#rm-sdlg-cancel (Cancel button) must exist")

    # Dialog controller
    if "window.__rmOpenSaveDialog" not in text:
        failures.append("window.__rmOpenSaveDialog must be exposed")
    if "window.__rmCloseSaveDialog" not in text:
        failures.append("window.__rmCloseSaveDialog must be exposed")
    if "initSaveDialog" not in text:
        failures.append("initSaveDialog IIFE must exist")

    # Disk click now routes through dialog
    if "__rmOpenSaveDialog" not in text[text.find("initSaveDisk"):text.find("initSaveDisk") + 2500]:
        failures.append("initSaveDisk click handler must call __rmOpenSaveDialog")

    # Title override hook
    if "window.__rmSaveDialogTitle" not in text:
        failures.append("window.__rmSaveDialogTitle must be used in save flow")
    if "window.__rmSaveDialogTitle = null" not in text:
        failures.append("window.__rmSaveDialogTitle must be cleared after use")

    # Save still routes through canonical function
    dialog_ctrl = text[text.find("initSaveDialog"):text.find("initSaveDialog") + 3500]
    if "__rmSaveCurrentInvestigation" not in dialog_ctrl:
        failures.append("save dialog must call __rmSaveCurrentInvestigation")

    # Notes still flow through legacy textarea
    if "saveInvestigationNote" not in dialog_ctrl:
        failures.append("dialog must set saveInvestigationNote for note path")

    # CSS assertions
    if "#rm-save-dialog" not in text or ".rm-sdlg-card" not in text:
        failures.append("save dialog CSS must be present")
    dlg_css = re.search(r"#rm-save-dialog\s*\{[^}]+\}", text, re.DOTALL)
    if dlg_css and "z-index" not in dlg_css.group():
        failures.append("#rm-save-dialog must have z-index set")

    # Truth functions untouched
    for fn in [
        "__rmSaveCurrentInvestigation",
        "collectSavedInvestigationConditions",
        "executeSearchPlan",
    ]:
        if fn not in text:
            failures.append(f"{fn} must remain present")

    # Backend route untouched
    if 'fetch("/saved-investigations/create"' not in text:
        failures.append("POST /saved-investigations/create must remain")

    if failures:
        print(f"FAIL {len(failures)}")
        for f in failures:
            print(f" - {f}")
        return 1

    print("PASS 16/16 MAP-SAVE-C save dialog static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
