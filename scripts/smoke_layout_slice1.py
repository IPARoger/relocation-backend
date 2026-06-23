#!/usr/bin/env python3
"""Static smoke: SLICE-1-LAYOUT assertions for map_CURRENT.html.

Verifies that the full-bleed map + fixed panel + topbar shell CSS/HTML changes
landed correctly, and that no production truth functions were altered.

Run:
    venv/bin/python scripts/smoke_layout_slice1.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def check(label: str, ok: bool) -> bool:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    return ok


def main() -> int:
    if not MAP.exists():
        print(f"ABORT: {MAP} not found", file=sys.stderr)
        return 1

    src = MAP.read_text(encoding="utf-8")
    results: list[bool] = []

    # ── Layout CSS ────────────────────────────────────────────────────────────
    print("\nLayout CSS (SLICE-1-LAYOUT):")

    map_rule = re.search(r"#map\s*\{([^}]+)\}", src)
    map_body = map_rule.group(1) if map_rule else ""
    results.append(check(
        "#map uses position: fixed",
        "position: fixed" in map_body,
    ))
    results.append(check(
        "#map uses inset (not flex:1)",
        "inset:" in map_body and "flex:" not in map_body,
    ))
    results.append(check(
        "#map has z-index: 0",
        "z-index: 0" in map_body,
    ))
    results.append(check(
        "#map does NOT use flex: 1",
        "flex: 1" not in map_body,
    ))

    panel_rule = re.search(r"#panel\s*\{([^}]+)\}", src)
    panel_body = panel_rule.group(1) if panel_rule else ""
    results.append(check(
        "#panel uses position: fixed",
        "position: fixed" in panel_body,
    ))
    results.append(check(
        "#panel right: 0",
        "right: 0" in panel_body,
    ))
    results.append(check(
        "#panel width: 304px",
        "width: 304px" in panel_body,
    ))
    results.append(check(
        "#panel top: 48px",
        "top: 48px" in panel_body,
    ))
    results.append(check(
        "#panel has z-index above map",
        "z-index: 100" in panel_body,
    ))
    results.append(check(
        "#panel does NOT use flex-shrink",
        "flex-shrink" not in panel_body,
    ))

    # ── Topbar CSS ────────────────────────────────────────────────────────────
    print("\nTopbar CSS:")
    topbar_rule = re.search(r"\.topbar\s*\{([^}]+)\}", src)
    topbar_body = topbar_rule.group(1) if topbar_rule else ""
    results.append(check(
        ".topbar CSS rule present",
        bool(topbar_rule),
    ))
    results.append(check(
        ".topbar position: fixed",
        "position: fixed" in topbar_body,
    ))
    results.append(check(
        ".topbar height: 48px",
        "height: 48px" in topbar_body,
    ))
    results.append(check(
        ".topbar z-index: 1200 (above panel, above map)",
        "z-index: 1200" in topbar_body,
    ))

    # ── Topbar HTML ───────────────────────────────────────────────────────────
    print("\nTopbar HTML:")
    results.append(check(
        '<header class="topbar"> element present',
        'class="topbar"' in src,
    ))
    results.append(check(
        "topbar is an empty shell (no nav links yet)",
        src.count('<a ') == src.replace('class="topbar"', '').count('<a '),
    ))

    # ── Bottle position unchanged ─────────────────────────────────────────────
    print("\nBottle position (unchanged, per Slice-1 decision):")
    bottle_rule = re.search(r"#rm-bottle\s*\{([^}]+)\}", src)
    bottle_body = bottle_rule.group(1) if bottle_rule else ""
    results.append(check(
        "#rm-bottle right: 18px (Slice-1 decision: stays in full-bleed map region)",
        "right: 18px" in bottle_body,
    ))
    results.append(check(
        "#rm-bottle position: absolute (inside #map)",
        "position: absolute" in bottle_body,
    ))

    # ── #app no longer flex ───────────────────────────────────────────────────
    print("\n#app layout:")
    app_rule = re.search(r"#app\s*\{([^}]+)\}", src)
    app_body = app_rule.group(1) if app_rule else ""
    results.append(check(
        "#app does NOT use display: flex",
        "display: flex" not in app_body,
    ))

    # ── Motion smoke dependencies preserved ───────────────────────────────────
    print("\nMotion/FLIP dependencies preserved:")
    results.append(check(
        ".rm-panel--flip-hidden still present",
        ".rm-panel--flip-hidden" in src,
    ))
    results.append(check(
        ".rm-bottle--revealed still present",
        ".rm-bottle--revealed" in src,
    ))
    results.append(check(
        "body.rm-explore #panel rule still present",
        "body.rm-explore #panel" in src,
    ))
    results.append(check(
        "enterExplore function still present",
        "function enterExplore()" in src,
    ))
    results.append(check(
        "exitExplore function still present",
        "function exitExplore()" in src,
    ))

    # ── Truth functions NOT changed ───────────────────────────────────────────
    print("\nTruth functions preserved:")
    for fn in [
        "executeSearchPlan",
        "__rmSaveCurrentInvestigation",
        "collectSavedInvestigationConditions",
        "gvVariablesToConditionSnapshot",
        "applySavedInvestigationConditions",
        "conditionsJsonToGvVariables",
        "buildGenieRenderPayloadFromGv",
        "invalidateMapSizeSoon",
    ]:
        results.append(check(f"{fn} still present", fn in src))

    # ── External scripts unchanged ────────────────────────────────────────────
    print("\nExternal script load order:")
    for script in [
        "/supabase_client.js",
        "/auth_guard.js",
        "/user_profile.js",
        "/supabase_store_bridge.js",
        "/genie_map_engine_adapter.js",
        "/substrate_adapter.js",
        "/quick_share.js",
    ]:
        results.append(check(f"{script} still loaded", f'src="{script}"' in src))

    # ── Summary ───────────────────────────────────────────────────────────────
    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} PASS")
    if passed < total:
        print(f"FAILED: {total - passed}", file=sys.stderr)
        return 1
    print("PASS SLICE-1-LAYOUT static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
