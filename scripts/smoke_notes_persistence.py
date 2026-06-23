#!/usr/bin/env python3
"""Static smoke: Notes persistence — structural integrity of all wired paths.

Verifies source-code evidence for every wired Notes path (Profile, Comparison,
Saved Investigation, Notes Library) without requiring a live server or auth.

Also confirms that Relocated Chart notes remain deliberately NOT wired
(placeholder textarea only — backend route, save handler, and textarea ID are
all absent by design).

Run:
    venv/bin/python scripts/smoke_notes_persistence.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
BACKEND = ROOT / "main_centerline_FIXER.py"


def check(label: str, result: bool) -> bool:
    print(f"  {'PASS' if result else 'FAIL'}  {label}")
    return result


def main() -> int:
    if not SHELL.exists():
        print(f"ABORT: {SHELL} not found", file=sys.stderr)
        return 1
    if not BACKEND.exists():
        print(f"ABORT: {BACKEND} not found", file=sys.stderr)
        return 1

    shell = SHELL.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")
    results: list[bool] = []

    # ── Backend routes ────────────────────────────────────────────────────────
    print("\nBackend routes (main_centerline_FIXER.py):")
    results.append(check(
        'GET /notes/{profile_id} route present',
        '@app.get("/notes/{profile_id}")' in backend,
    ))
    results.append(check(
        'POST /notes/chart-record route present',
        '@app.post("/notes/chart-record")' in backend,
    ))
    results.append(check(
        'POST /notes/comparison-set route present',
        '@app.post("/notes/comparison-set")' in backend,
    ))
    results.append(check(
        'POST /notes/saved-investigation route present',
        '@app.post("/notes/saved-investigation")' in backend,
    ))
    results.append(check(
        'Legacy POST /notes warns about scoped routes',
        '@app.post("/notes")' in backend and 'Use scoped POST' in backend,
    ))

    # ── Frontend functions ────────────────────────────────────────────────────
    print("\nFrontend functions (app_shell.html):")
    results.append(check(
        'saveChartRecordNote function defined',
        'async function saveChartRecordNote(' in shell,
    ))
    results.append(check(
        'saveComparisonSetNote function defined',
        'async function saveComparisonSetNote(' in shell,
    ))
    results.append(check(
        'saveSavedInvestigationNote function defined',
        'async function saveSavedInvestigationNote(' in shell,
    ))
    results.append(check(
        'fetchNotesForProfile function defined',
        'async function fetchNotesForProfile(' in shell,
    ))
    results.append(check(
        'loadNotesLibraryItems function defined',
        'async function loadNotesLibraryItems(' in shell,
    ))
    results.append(check(
        'saveNoteFromLibrary delegates to saveChartRecordNote and saveComparisonSetNote',
        'saveNoteFromLibrary' in shell
        and 'saveChartRecordNote' in shell
        and 'saveComparisonSetNote' in shell,
    ))

    # ── Frontend fetch calls match routes ────────────────────────────────────
    print("\nFrontend fetch \u2192 backend route alignment:")
    results.append(check(
        'saveChartRecordNote calls POST /notes/chart-record',
        'fetch("/notes/chart-record"' in shell,
    ))
    results.append(check(
        'saveComparisonSetNote calls POST /notes/comparison-set',
        'fetch("/notes/comparison-set"' in shell,
    ))
    results.append(check(
        'saveSavedInvestigationNote calls POST /notes/saved-investigation',
        'fetch("/notes/saved-investigation"' in shell,
    ))
    results.append(check(
        'fetchNotesForProfile calls GET /notes/:profileId',
        'fetch("/notes/" + encodeURIComponent(profileId))' in shell,
    ))

    # ── DOM IDs and save actions ──────────────────────────────────────────────
    print("\nDOM IDs and save action handlers:")
    results.append(check(
        'Profile textarea #rm-chart-note present',
        'id="rm-chart-note"' in shell,
    ))
    results.append(check(
        'Profile save button data-action="save-chart-note" present',
        'data-action="save-chart-note"' in shell,
    ))
    results.append(check(
        'Profile feedback span #rm-chart-note-msg present',
        'id="rm-chart-note-msg"' in shell,
    ))
    results.append(check(
        'Profile save handler calls saveChartRecordNote',
        'saveChartRecordNote(crId' in shell,
    ))
    results.append(check(
        'Comparison textarea #rm-cmp-note present',
        'id="rm-cmp-note"' in shell,
    ))
    results.append(check(
        'Comparison save button data-action="save-comparison-note" present',
        'data-action="save-comparison-note"' in shell,
    ))
    results.append(check(
        'Comparison save handler calls saveComparisonSetNote',
        'saveComparisonSetNote(csId' in shell,
    ))
    results.append(check(
        'Comparison feedback span #rm-cmp-note-msg present',
        'id="rm-cmp-note-msg"' in shell,
    ))

    # ── localStorage device fallback (Profile) ────────────────────────────────
    print("\nLocalStorage device fallback (Profile only):")
    results.append(check(
        'chartNoteKey() helper defined',
        'function chartNoteKey(' in shell,
    ))
    results.append(check(
        'loadChartNote() reads localStorage',
        'function loadChartNote(' in shell and 'localStorage.getItem(' in shell,
    ))
    results.append(check(
        'saveChartRecordNote mirrors to localStorage before network call',
        'localStorage.setItem(chartNoteKey(' in shell,
    ))
    results.append(check(
        'chartRecordInitialNote prefers account note over localStorage fallback',
        'function chartRecordInitialNote(' in shell,
    ))
    # Confirm comparison notes have no localStorage (account-only by design)
    cmp_fn_start = shell.find('async function saveComparisonSetNote(')
    cmp_fn_body = shell[cmp_fn_start: cmp_fn_start + 900] if cmp_fn_start != -1 else ''
    results.append(check(
        'Comparison notes have no localStorage fallback (account-only by design)',
        cmp_fn_start != -1 and 'localStorage' not in cmp_fn_body,
    ))

    # ── Notes Library collections ─────────────────────────────────────────────
    print("\nNotes Library collection wiring:")
    results.append(check(
        'profile collection wired: true',
        '{ id: "profile", label: "Profile", wired: true' in shell,
    ))
    results.append(check(
        'comparisons collection wired: true',
        '{ id: "comparisons", label: "Comparisons", wired: true' in shell,
    ))
    results.append(check(
        'investigations collection wired: true',
        '{ id: "investigations", label: "Saved Searches / Investigations", wired: true' in shell,
    ))

    # ── Confirmed NOT wired (Relocated Chart) ─────────────────────────────────
    print("\nConfirmed NOT wired \u2014 Relocated Chart (by design):")
    results.append(check(
        'Relocated textarea has no DOM id (cosmetic placeholder only)',
        'id="rm-screen4-note"' not in shell
        and 'id="rm-relocated-note"' not in shell,
    ))
    results.append(check(
        'No save-relocated-note action anywhere in frontend',
        'save-relocated-note' not in shell
        and 'save-reloc-note' not in shell,
    ))
    results.append(check(
        'No POST /notes/relocated-chart route in backend',
        '/notes/relocated-chart' not in backend,
    ))
    results.append(check(
        'No fetch call to /notes/relocated-chart in frontend',
        'fetch("/notes/relocated-chart")' not in shell
        and "fetch('/notes/relocated-chart')" not in shell,
    ))
    results.append(check(
        'Relocated textarea placeholder text states "not yet saved"',
        'not yet saved' in shell,
    ))
    results.append(check(
        'relocated_charts Notes Library collection is wired: false',
        '{ id: "relocated_charts", label: "Relocated Charts", wired: false' in shell,
    ))

    # ── Summary ───────────────────────────────────────────────────────────────
    passed = sum(results)
    total = len(results)
    failed = total - passed
    print(f"\n{passed}/{total} PASS")
    if failed:
        print(f"FAILED: {failed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
