#!/usr/bin/env python3
"""Read-only smoke for M2 Map Surface + Genie Harmonization audit.

Static checks only — no overlay math, no renderer changes.
Optional: set RUN_M2_SCREENSHOTS=1 with SUPABASE_* + network for Playwright captures.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"
SHOT_DIR = ROOT / "validation/mockups/beta/screenshots/m2_map_genie_audit"


def static_checks(text: str) -> tuple[list[str], int]:
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    # M1 regressions (control truth + overlay hooks)
    check("data-overlay-final" in text, "M1-B: data-overlay-final hook present")
    check("window.__rmOverlayTrust" in text, "M1-B: __rmOverlayTrust present")
    check('id="gv-searchBtn"' in text and "Search Map" in text, "M1-A: canonical Search Map CTA")
    check('class="rm-panel-section-hidden" aria-hidden="true">Find regions' in text or (
        'id="findBtn"' in text and "rm-panel-section-hidden" in text
    ), "M1-A: legacy findBtn hidden")
    check("popup-action-view-overlays" in text, "M1-C: View overlays here button")
    check("CITY_VIEWPORT_CAP_BY_ZOOM" in text, "M1-C: city viewport caps")
    check("data-role=\"map-save-search\"" in text or "rm-save-disk" in text, "M1-D: explore save disk")
    check("syncGhostFromReplayedPlan" in text, "M1-D: ghost sync on replay")

    # Material harmonization gaps (documented risks)
    check("family_resemblance.css" in text, "M2-X: family_resemblance.css linked")
    check("rm-map-workspace" in text, "M2-X: map workspace body class")
    check("--gv-card: var(--rm-card)" in text, "M2-X: GV tokens alias to rm material")
    check("Avenir Next" in text and "#panel" in text, "M2-X: panel uses Avenir instrument stack")

    # Debug gating
    check('MAP_URL.has("debugGeometry")' in text, "M2: debugGeometry URL gate")
    check("if (!debugGeometry) return" in text, "M2: debug rows gated off default path")
    check("genieRenderStatus" in text and "?debug=1" in text, "M2: genie debug panel URL-gated")

    # NOT honesty
    check("ENGINE_EXCLUDE_SUPPORTED" in text, "M2: NOT gated on engine exclude support")

    # Production map surface
    check(MAP.name == "map_CURRENT.html", "M2: auditing production map file")
    check(MAP.stat().st_size > 100_000, "M2: map_CURRENT.html non-trivial size")

    return failures, checks


def main() -> int:
    if not MAP.is_file():
        print(f"FAIL map file missing: {MAP}")
        return 1

    text = MAP.read_text(encoding="utf-8")
    failures, checks = static_checks(text)

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks} M2 map surface static audit checks")

    if os.environ.get("RUN_M2_SCREENSHOTS") == "1":
        print("NOTE: RUN_M2_SCREENSHOTS=1 — run scripts/capture_m2_map_genie_audit.py when SUPABASE network available")

    expected_shots = [
        "01_initial_map.png",
        "02_genie_builder_panel.png",
        "04_overlay_final.png",
        "07_explore_mode.png",
        "07b_ghost_strip.png",
        "10_popup_view_overlays_here.png",
    ]
    missing = [s for s in expected_shots if not (SHOT_DIR / s).exists()]
    if missing:
        print(f"WARN screenshot evidence incomplete ({len(missing)} missing): {', '.join(missing)}")
        print("      PO QA: authenticated session required; wait for data-overlay-final=true")

    return 0


if __name__ == "__main__":
    sys.exit(main())
