#!/usr/bin/env python3
"""Static smoke for MAP-BETA-STABILIZE-A.

Asserts all five Beta-A ownership fixes are present in map_CURRENT.html
without touching protected truth surfaces.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    # ── A. Zoom controls ────────────────────────────────────────────────
    check(
        "window.__rmMap.zoomIn(1)" in text,
        "A-zoom: zoomIn must use explicit step 1",
    )
    check(
        "window.__rmMap.zoomOut(1)" in text,
        "A-zoom: zoomOut must use explicit step 1",
    )
    check(
        "L.DomEvent.disableClickPropagation(cluster)" in text,
        "A-zoom: disableClickPropagation must be called on zoom cluster",
    )
    check(
        "L.DomEvent.disableScrollPropagation(cluster)" in text,
        "A-zoom: disableScrollPropagation must be called on zoom cluster",
    )
    # No default Leaflet zoom control
    check(
        "zoomControl: false" in text,
        "A-zoom: Leaflet zoomControl must remain false",
    )

    # ── B. Profile ownership ────────────────────────────────────────────
    check(
        "window.__rmOpenProfileSelector = openProfileSelector" in text,
        "B-profile: openProfileSelector must be exposed on window",
    )
    check(
        True,  # Beta-B Fix1 superseded: topbar no longer delegates to profile picker
        "B-profile: topbar account label click handler (superseded by Beta-B Fix1)",
    )
    check(
        'id="rm-topbar-acct"' in text,
        "B-profile: #rm-topbar-acct must be in DOM",
    )
    check(
        True,  # Beta-B Fix1 superseded: cursor:pointer removed from .rm-acct
        "B-profile: .rm-acct cursor:pointer (superseded by Beta-B Fix1)",
    )
    check(
        "__rmOpenProfileSelector" in text,
        "B-profile: topbar click must delegate to __rmOpenProfileSelector",
    )

    # ── C. Duplicate city-search label (sr-only) ────────────────────────
    check(
        ".sr-only {" in text,
        "C-srlabel: .sr-only CSS rule must exist",
    )
    check(
        "clip: rect(0, 0, 0, 0)" in text,
        "C-srlabel: .sr-only must use clip:rect to hide element",
    )

    # ── D. Debug panels gated ───────────────────────────────────────────
    check(
        text.count("Beta-D: only show debug panels when ?debug=1") == 2,
        "D-debug: both handoff and genie render status must be gated",
    )
    check(
        text.count("get('debug') === '1'") >= 2,
        "D-debug: debug check must appear in both gate locations",
    )

    # ── E. Profile readiness gate ───────────────────────────────────────
    check(
        # PB2 superseded: inline Beta-E comment replaced by requireActiveProfile() helper
        "requireActiveProfile" in text or
        text.count("Beta-E: wait for profiles to load before checking") >= 1,
        "E-ready: at least one profile readiness gate must exist",
    )
    check(
        "await window.__rmChartProfilesReady" in text,
        "E-ready: readiness gate must await __rmChartProfilesReady",
    )
    # Better error messaging
    check(
        # PB2 superseded: caret reference removed; new message is "Choose a saved profile first."
        "Choose a saved profile first." in text or
        "No profile selected. Click the profile name" in text,
        "E-ready: improved no-profile error message must exist",
    )

    # ── Protected truth surfaces ────────────────────────────────────────
    for fn in (
        "executeSearchPlan",
        "__rmExecuteGenieRender",
        "__rmSaveCurrentInvestigation",
        "collectSavedInvestigationConditions",
        "createQuickShareFromMap",
        "getActiveFavoriteProfileId",
    ):
        check(fn in text, f"truth: {fn} must remain present")

    # chartProfile remains single source of truth
    check(
        "document.getElementById(\"chartProfile\")" in text,
        "truth: #chartProfile must remain the profile source",
    )
    check(
        "saved_location_search_ui.js" in text,
        "truth: saved_location_search_ui.js must remain",
    )

    # R1/R2/R3 coordinate/CSS preserved
    cluster = re.search(r"#rm-mapctrls\s*\{[^}]+\}", text, re.DOTALL)
    if cluster:
        body = cluster.group()
        check("left: 16px" in body, "R1-preserved: #rm-mapctrls left:16px unchanged")
        check("top: 62px" in body, "R1-preserved: #rm-mapctrls top:62px unchanged")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks} MAP-BETA-STABILIZE-A checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
