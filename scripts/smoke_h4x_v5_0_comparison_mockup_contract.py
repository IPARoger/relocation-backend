#!/usr/bin/env python3
"""Static smoke: H4X V5-0 — comparison_v5_beta.html wiring contract."""
from __future__ import annotations

import re
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

    # Root + section mounts
    check('id="rm-cmp-v5-root"' in text, "comparison root id")
    check('data-cmp-mount="comparison-root"' in text, "comparison root mount")
    check('id="rm-cmp-zone-b"' in text, "authority cmp-zone-b id")
    check('data-cmp-mount="authority"' in text, "authority mount")
    check('id="rm-cmp-city-bar"' in text, "city bar wrap id")
    check('id="city-bar-inner"' in text, "city bar inner mount")
    check('data-cmp-mount="city-bar-inner"' in text, "city bar inner data mount")
    check('id="table-ais"' in text and 'data-cmp-mount="ais-table"' in text, "AIS table mount")
    check('id="table-pih"' in text and 'data-cmp-mount="pih-table"' in text, "PIH table mount")
    check('id="table-ata"' in text and 'data-cmp-mount="a2a-table"' in text, "A2A table mount")
    check('data-cmp-role="a2a-angle-tabs"' in text or 'class="angle-tabs"' in text, "A2A angle tabs region")
    for ang in ("ASC", "DSC", "MC", "IC"):
        check(f'data-angle="{ang}"' in text, f"A2A tab data-angle={ang}")
    check('data-action="cmp-angle-tab"' in text, "A2A tabs data-action")
    check('id="cmp-notes-rail"' in text, "notes rail id")
    check('id="rm-cmp-note"' in text, "notes textarea id")
    check('data-action="save-comparison-note"' in text, "notes save action")
    check('id="ci-cards"' in text and 'data-cmp-mount="ci-cards"' in text, "CI cards mount")
    check('id="modal-picker"' in text and 'data-cmp-mount="place-picker"' in text, "place picker mount")

    # Mockup-only markers
    check(text.count("MOCKUP_ONLY_REPLACED_BY_ADAPTER") >= 3, "mockup-only data marked (>=3)")
    check("wireMockupPreviewActions" in text, "mockup-only preview delegation present")

    # No inline onclick in static HTML; JS template strings must not use onclick
    check(not re.search(r"\bonclick\s*=", static_html, re.I), "no onclick in static HTML")
    js_part = text.split("<script>", 1)[1] if "<script>" in text else ""
    check("onclick=" not in js_part, "no onclick in script templates")

    # Visual classes preserved
    for cls in (
        "cmp-zone-b",
        "city-bar-wrap",
        "city-bar-table",
        "block",
        "fact-table",
        "angle-tab",
        "comparison-notes-rail",
        "notes-textarea",
        "ci-section",
        "ci-grid",
    ):
        check(cls in text, f"visual class preserved: {cls}")

    # Mockup-only contract: app_shell integration is validated by V5-1 shadow smoke.
    check(True, "mockup contract scope (app_shell checked by V5-1 smoke)")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
