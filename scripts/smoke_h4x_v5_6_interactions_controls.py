#!/usr/bin/env python3
"""Smoke: H4X V5-6 — comparison interaction controls and placeholders."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_smoke_js_syntax import assert_v5_js_syntax

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
ROUTE = ROOT / "validation/mockups/beta/comparison_v5_route.js"
ADAPTER = ROOT / "validation/mockups/beta/comparison_v5_adapter.js"
MAIN = ROOT / "main_centerline_FIXER.py"

REQUIRED_ACTIONS = (
    "cmp-add-place",
    "cmp-replace-place",
    "cmp-remove-place",
    "cmp-toggle-place",
    "cmp-move-place",
    "cmp-city-info",
    "cmp-toggle-block",
    "cmp-toggle-ci-section",
    "toggle-pih-dignities",
    "toggle-cmp-diffs",
)

FORBIDDEN_VISIBLE = (
    "Open slot",
    "City Intelligence pending",
)


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
    route = ROUTE.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")
    main_py = MAIN.read_text(encoding="utf-8")
    main_body = re.search(r'<script>\n"use strict";([\s\S]*?)</script>\s*</body>', shell)
    main = main_body.group(1) if main_body else ""

    handle_fn = chunk_after(main, "function handleComparisonV5CanonicalAction")
    wire_fn = chunk_after(main, "function wireComparisonV5CanonicalActions")
    collapse_fn = chunk_after(main, "function applyComparisonV5SectionCollapse")
    persist_fn = chunk_after(main, "async function persistComparisonSetPlaceIds")
    refresh_fn = chunk_after(main, "async function refreshComparisonV5Dom")
    pick_fn = chunk_after(main, "function openComparisonV5PlacePicker")

    for action in REQUIRED_ACTIONS:
        check(f'data-action="{action}"' in adapter or f"data-action='{action}'" in adapter or action in route,
              f"adapter/route exposes {action}")
        if action.startswith("cmp-"):
            check(f'action === "{action}"' in handle_fn or f"action === '{action}'" in handle_fn,
                  f"handleComparisonV5CanonicalAction handles {action}")

    check("wireComparisonV5CanonicalActions" in route, "route defines wireComparisonV5CanonicalActions")
    check("ComparisonV5Route.wireComparisonV5CanonicalActions" in wire_fn, "shell wires canonical actions")
    check("onAction" in wire_fn, "canonical wire passes onAction hook")

    check("cmp-add-place" in handle_fn and "openComparisonV5PlacePicker" in handle_fn, "Add opens picker")
    check("cmp-replace-place" in handle_fn and "replacePlaceId" in pick_fn, "Replace opens picker for slot")
    check("cmp-remove-place" in handle_fn and "persistComparisonSetPlaceIds" in handle_fn, "Remove persists places")
    check("cmp-toggle-place" in handle_fn and "hidden_place_ids" in handle_fn, "Hide toggles hidden_place_ids")
    check("cmp-move-place" in handle_fn and "column_order_place_ids" in handle_fn, "Move updates column order")
    check("cmp-city-info" in handle_fn, "City info handler present")

    check("collapsed_sections" in collapse_fn, "section collapse reads collapsed_sections")
    check("cmp-toggle-block" in handle_fn and "applyComparisonV5SectionCollapse" in handle_fn,
          "block caret toggles collapse state")
    check("cmp-toggle-ci-section" in handle_fn, "CI caret toggles collapse")
    check("scheduleComparisonWorkspaceSave" in handle_fn, "collapse persists via workspace save")

    check("bindCmpDiffsToggle" in main and "bindPihDignitiesToggle" in main, "dignities/diffs binders exist")
    check("toggle-cmp-diffs" in route and "toggle-pih-dignities" in route, "V5 shell has Diffs/Dignities controls")
    check("bindCmpDiffsToggle(v5root)" in main, "mount binds diffs on V5 root")

    check('fetch("/comparison-sets/places"' in persist_fn, "persist posts to /comparison-sets/places")
    check("/comparison-sets/places" in main_py, "backend serves comparison-sets/places")

    check("refreshComparisonV5Dom" in handle_fn or "refreshComparisonV5Dom" in refresh_fn,
          "place mutations refresh V5 DOM")

    for bad in FORBIDDEN_VISIBLE:
        check(bad not in adapter, f"adapter has no user-visible '{bad}'")

    check('class="wheel-note"' in route and "hidden" in route.split("wheel-note", 1)[1][:80],
          "wheel-note hidden in route shell")

    render_shell = route.split("function renderShellHtml", 1)[1].split("function syncRouteChrome", 1)[0]
    check("Module:" not in render_shell, "canonical shell has no Module leak")
    check("stateDebugBlock" not in render_shell, "canonical shell has no debug block")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
