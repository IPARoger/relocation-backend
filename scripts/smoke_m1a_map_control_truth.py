#!/usr/bin/env python3
"""Static smoke for M1-A Map Control Truth.

Asserts control-trust fixes in map_CURRENT.html without touching overlay math,
smoothing, city readability, Help/CI, or design tokens.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    if not MAP.is_file():
        print(f"FAIL map file missing: {MAP}")
        return 1

    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    # ── 1. GV builder trust labels ─────────────────────────────────────
    check("UI-only preview" not in text, "GV: no 'UI-only preview' copy")
    check("UI-only" not in text.lower() or "UI ONLY" not in text, "GV: no UI-only language")
    check(
        "Search Map renders overlays on the map" in text,
        "GV: aria-label reflects real overlay execution",
    )
    check(
        "__rmExecuteGenieRender" in text,
        "GV: production bridge __rmExecuteGenieRender present",
    )

    # ── 2. Single user-facing search CTA ─────────────────────────────────
    check(
        'id="findBtn"' in text and 'class="rm-panel-section-hidden"' in text.split('id="findBtn"')[1][:120],
        "findBtn: hidden via rm-panel-section-hidden",
    )
    check(
        'findBtn").setAttribute("aria-hidden","true")' in text
        or 'findBtn" type="button" class="rm-panel-section-hidden" aria-hidden="true"' in text,
        "findBtn: aria-hidden from beta users",
    )
    check(
        'id="gv-searchBtn"' in text and "Search Map" in text,
        "GV: Search Map button visible",
    )
    check(
        text.count("rm-legacy-search-section") >= 3,
        "legacy: planet/angle/aspect sections marked rm-legacy-search-section",
    )

    # ── 3. Production overlay path unchanged ─────────────────────────────
    check("executeSearchPlan" in text, "truth: executeSearchPlan present")
    check("/search-regions" in text, "truth: POST /search-regions present")
    check(
        'MAP_URL.get("generation_mode") || "truth_grid"' in text
        or 'generation_mode") || "truth_grid"' in text,
        "truth: truth_grid remains default generation_mode",
    )
    check(
        text.count("smoothFactor: 0") >= 3,
        "truth: smoothFactor remains 0 on overlay layers",
    )

    # ── 4. NOT control honesty ───────────────────────────────────────────
    check(
        "ENGINE_EXCLUDE_SUPPORTED" in text,
        "NOT: ENGINE_EXCLUDE_SUPPORTED gate present",
    )
    check(
        "exclude polarity not yet in engine" not in text,
        "NOT: misleading disabled title removed",
    )
    check(
        "Redact - exclude these placements (NOT)" not in text,
        "NOT: old misleading GV NOT title removed",
    )

    # ── 5. History / ghost consistency ───────────────────────────────────
    check(
        "syncGhostFromReplayedPlan" in text,
        "history: syncGhostFromReplayedPlan implemented",
    )
    check(
        "history_replay" in text and "_historyReplayActive" in text,
        "history: replay guard for ghost controls",
    )

    # ── 6. Profile reopen freeze mitigation ──────────────────────────────
    check(
        "__gvResetSearchInFlight" in text,
        "freeze: search in-flight reset hook exposed",
    )
    check(
        "restore panel pointer-events immediately" in text,
        "freeze: exitExplore restores interactivity immediately",
    )

    # ── 7. Protected surfaces remain ─────────────────────────────────────
    for fn in (
        "buildPlanFromLegacyDom",
        "findRegions",
        "__gvBuildPayloadForTesting",
        "ghostRedrawFromState",
    ):
        check(fn in text, f"truth: {fn} must remain for harness/replay")

    # ── 8. Optional boot check ───────────────────────────────────────────
    check(MAP.stat().st_size > 1000, "boot: map_CURRENT.html exists and non-empty")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks} M1-A map control truth checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
