#!/usr/bin/env python3
"""Smoke: H4X V5-6B — comparison controls reality (add/replace, diffs, move anim)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_smoke_js_syntax import assert_v5_js_syntax

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
ADAPTER = ROOT / "validation/mockups/beta/comparison_v5_adapter.js"
CSS = ROOT / "validation/mockups/beta/comparison_v5_beta.css"
MAIN = ROOT / "main_centerline_FIXER.py"


def chunk_after(src: str, marker: str) -> str:
    if marker not in src:
        return ""
    body = src.split(marker, 1)[1]
    end = body.find("\nfunction ")
    return body if end == -1 else body[:end]


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    assert_v5_js_syntax(check)
    shell = SHELL.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    main_py = MAIN.read_text(encoding="utf-8")
    main_body = re.search(r'<script>\n"use strict";([\s\S]*?)</script>\s*</body>', shell)
    main = main_body.group(1) if main_body else ""

    persist_fn = chunk_after(main, "async function persistComparisonSetPlaceIds")
    refresh_fn = chunk_after(main, "function refreshComparisonDiffSurfaces")
    move_fn = chunk_after(main, "function handleComparisonV5CanonicalAction")

    check('fetch("/comparison-sets/places"' in persist_fn, "persist uses POST /comparison-sets/places")
    check('method: "POST"' in persist_fn or "method: 'POST'" in persist_fn, "persist uses POST method")
    check("@app.post(\"/comparison-sets/places\")" in main_py, "backend defines POST /comparison-sets/places")
    check("update_comparison_set_places" in main_py, "backend calls update_comparison_set_places")
    check("place_ids" in persist_fn, "persist sends place_ids payload")

    check("cmpDiffTdClass" in adapter and "diffTdClass" in adapter, "adapter wires diff classes")
    check("pihDignityClass" in adapter or "pih-house-cell" in adapter, "adapter wires dignities")
    check("cmpDiffTdClass" in chunk_after(main, "function buildComparisonV5HydrationContext"), "deps pass diff helpers")

    check("ComparisonV5Route.hydrateCanonical" in refresh_fn, "diff/dignity refresh rehydrates V5")
    check("bindCmpDiffsToggle" in refresh_fn and "bindPihDignitiesToggle" in refresh_fn,
          "V5 toggles rebound after diff refresh")

    check("runComparisonV5CityReorderAnim" in main, "city reorder animation helper exists")
    check("cmp-city-reorder-anim" in move_fn or "runComparisonV5CityReorderAnim" in move_fn,
          "move action uses reorder animation")
    check("cmp-city-reorder-anim" in css, "move animation CSS class exists")

    check(bool(re.search(r"\.stub-restore\s*\{[^}]*min-height", css)),
          "hidden restore affordance has expanded target")
    check("bar-city-slot-empty" not in adapter.split("mapCityBar", 1)[1].split("function mapAisTable", 1)[0],
          "add button not separated by reserved empty slots")

    check("text-align: center" in css.split("V5-6B", 1)[1], "city/value columns centered in V5 CSS")
    check("angle-tabs" in css and "margin-left: 18px" in css, "A2A pills have right offset")

    # Route must not be legacy deprecated POST only
    legacy_block = main_py.split("@app.post(\"/comparison-set/{comparison_set_id}/places\")", 1)[1][:400]
    check("_deprecated_legacy_write" in legacy_block, "legacy per-place POST remains deprecated")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
