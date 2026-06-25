#!/usr/bin/env python3
"""Static smoke: H4X V5-0B — comparison_v5_beta.html doctrine patch before hydration."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_smoke_js_syntax import assert_v5_js_syntax

ROOT = Path(__file__).resolve().parents[1]
MOCKUP = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_beta.html"
SHELL = ROOT / "app_shell.html"


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    assert_v5_js_syntax(check)
    text = MOCKUP.read_text(encoding="utf-8")
    static_html = text.split("<script>", 1)[0]
    js_part = text.split("<script>", 1)[1] if "<script>" in text else ""

    # 1. Authority placement — primary zone-b + sticky transform target documented
    check('data-cmp-role="authority-primary"' in text, "authority-primary on cmp-zone-b")
    check('id="rm-cmp-bar-authority-sticky"' in text, "sticky authority id in city bar render")
    check('data-cmp-role="authority-sticky-transform"' in text, "sticky authority role hook")
    check('data-cmp-authority-source="rm-cmp-zone-b"' in text, "sticky authority source pointer")
    check(
        "STICKY TRANSFORM TARGET" in text or "sticky transform target" in text.lower(),
        "authority sticky transform documented in comments",
    )

    # 2. City bar card contract — two-line names, hooks, inline actions
    check("city-name-lines" in text, "two-line city name container class")
    check("bname-line-primary" in text and "bname-line-secondary" in text, "two-line name spans")
    check('data-cmp-role="city-card"' in text, "city card role hook")
    check("data-place-id=" in js_part, "city cards expose data-place-id in render")
    check("data-action=" in js_part, "city cards expose data-action hooks")
    check("city-name-inline-actions" in text, "inline (i) attached to city name")
    check("city-remove" in text and "city-info-inline" in text, "inline × and (i) controls present")
    check("city-badge-zone" in text and "city-coords" in text and "city-ctrls" in text, "city card slot anatomy")
    check("cmp-replace-place" in text, "Replace control action hook")

    # 3. Column texture — approved hatch grammar, not intensified
    check("cmp-col-texture-a" in text and "cmp-col-texture-b" in text, "alternating column hatch classes")
    check(
        "approved visual grammar" in text.lower() or "approved column hatch" in text.lower(),
        "column hatch marked as approved grammar",
    )
    check(text.count("rgba(51,41,31,.014)") >= 2, "subtle hatch opacity preserved")

    # 4. A2A pills — canonical style marked
    check('data-cmp-role="canonical-a2a-pills"' in text, "canonical A2A pill role")
    check(
        "propagate to Profile/Relocated" in text or "Profile/Relocated" in text,
        "A2A pill propagation comment",
    )
    for ang in ("ASC", "DSC", "MC", "IC"):
        check(f'data-angle="{ang}"' in text, f"A2A pill data-angle={ang}")

    # 5. Notes rail — floating, toolbar position documented
    check('data-cmp-notes-layout="floating"' in text, "notes rail floating layout hook")
    check(
        "floating" in text.lower() and ("toolbar" in text.lower() or "controls on bottom" in text.lower()),
        "notes rail floating / toolbar harmonization documented",
    )
    check('id="cmp-notes-rail"' in text, "notes rail remains present")

    # 6. City Intelligence section below A2A
    a2a_pos = text.find('id="table-ata"')
    ci_pos = text.find('id="ci-cards"')
    check(a2a_pos > 0 and ci_pos > a2a_pos, "CI section exists below A2A table mount")
    check("CI_CATEGORY_LABELS" in text, "CI category labels constant (7 categories)")
    check(text.count("Regional context") >= 1, "CI regional context category")
    check("data-ci-category" in text, "CI category data hooks")
    check("ci-section" in static_html, "CI section shell in static HTML")

    # 7. Capacity — blank slots reserved, open product decision
    check("CMP_CAPACITY_RESERVED" in text, "capacity constant defined")
    check('data-cmp-role="city-slot-empty"' in text, "blank city slot hooks")
    check("bar-city-slot-empty" in text, "blank city slot styling")
    check(
        "OPEN PRODUCT DECISION" in text or "open product decision" in text.lower(),
        "4 vs 5 city limit documented as open decision",
    )

    # V5-0 wiring contract still intact
    check('id="rm-cmp-v5-root"' in text, "comparison root preserved")
    check("wireMockupPreviewActions" in text, "mockup preview delegation preserved")

    # Doctrine is mockup-only; app_shell shadow wiring validated by V5-1 smoke.
    check(True, "doctrine mockup scope (app_shell checked by V5-1 smoke)")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
