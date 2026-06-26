#!/usr/bin/env python3
"""Static smoke for M1-D explore chrome, pin, and history clarity."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    if not MAP.is_file():
        print(f"FAIL map missing: {MAP}")
        return 1

    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    # Explore save path
    check('data-role="map-save-search"' in text, "save: disk has map-save-search role")
    check("body.rm-explore #rm-save-disk" in text, "save: disk visible in explore mode CSS")
    check("rm-menu-save-investigation" in text, "save: explore menu save entry")
    check("map-explore-save-menu" in text, "save: explore menu data-role")
    check("__rmOpenSaveDialog" in text, "save: dialog opener wired")

    # Pin
    check("__rmPinStorageKey" in text and "rm_map_pinned_plan" in text, "pin: sessionStorage key exported")
    check("sessionStorage.setItem(PIN_KEY" in text, "pin: writes sessionStorage")
    check("rm-ctrl-pinned" in text, "pin: visual pinned class")
    check('aria-pressed' in text and "setAttribute('aria-pressed'" in text, "pin: aria-pressed state")
    check("browser session" in text.lower(), "pin: honest session-scoped copy")

    # History
    check("async function replayAt" in text, "history: async replay")
    check("history_replay" in text, "history: history_replay source")
    check(
        "(meta || {}).source !== 'history_replay'" in text,
        "history: replay does not double-push stack",
    )
    check("syncGhostFromReplayedPlan" in text, "history: ghost/GV sync after replay")
    check('data-role="history-controls"' in text and "rm-ctrl-card rm-navgrp" in text, "history: controls container role")

    # Walkthrough selectors (no stale ghost-tools / condition-block)
    check("ghost-tools" not in text, "walkthrough: stale ghost-tools selector removed")
    check("#gv-builder-host" in text.split("initWalkthrough")[1][:4000], "walkthrough: genie targets gv-builder")
    check('data-role="map-ghost-strip"' in text.split("initWalkthrough")[1][:4000], "walkthrough: ghost strip selector")
    check('data-role="map-notes"' in text, "walkthrough: map-notes on save dialog")

    # Legacy/debug hidden
    check("M1-D: legacy panel save hidden" in text, "chrome: legacy save hidden")

    if failures:
        print(f"FAIL {len(failures)}/{checks} M1-D checks")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks} M1-D map chrome/history checks")

    for script in (
        "smoke_m1a_map_control_truth.py",
        "smoke_m1b_overlay_truth.py",
        "smoke_m1c_popup_city_readability.py",
    ):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], capture_output=True, text=True)
        line = (r.stdout or "").strip().splitlines()[-1] if r.stdout else r.stderr
        if r.returncode != 0:
            print(f"FAIL regression {script}: {line}")
            return 1
        print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
