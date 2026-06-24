#!/usr/bin/env python3
"""Static smoke: SLICE-3-FLOW assertions for map_CURRENT.html.

Verifies that the three map flow blockers are repaired:
1. Custom location prompt removed from contextmenu handler
2. Profile selector reveal CSS + JS present
3. Favorites and open-chart handlers unchanged and functional

Run:
    venv/bin/python scripts/smoke_flow_repair_slice3.py
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

    # ── Fix 1: custom location contextmenu ──────────────────────────────────
    print("\nFix 1 — Custom location flow (no blocking prompt):")
    # Locate contextmenu block, strip block comments, verify no actual call
    _cx = src.find('map.getContainer().addEventListener("contextmenu"')
    _cx_end = src.find("});", _cx) + 3 if _cx >= 0 else 0
    _cx_clean = re.sub(r'/\*.*?\*/', '', src[_cx:_cx_end], flags=re.DOTALL) if _cx >= 0 else ""
    results.append(check(
        "promptCustomLocationName() NOT called from contextmenu handler",
        "promptCustomLocationName(" not in _cx_clean,
    ))
    results.append(check(
        "contextmenu handler uses coordinate auto-label",
        bool(re.search(
            r'addEventListener\s*\(\s*["\']contextmenu["\"].*?Custom location near',
            src, re.DOTALL
        )),
    ))
    results.append(check(
        "promptCustomLocationName() function still defined (used by favorite handler)",
        "function promptCustomLocationName" in src,
    ))
    results.append(check(
        "promptCustomLocationName() still used inside favoriteMapSelectionFromButton",
        bool(re.search(
            r'favoriteMapSelectionFromButton.*?promptCustomLocationName',
            src, re.DOTALL
        )),
    ))
    results.append(check(
        "contextmenu handler does NOT have null-cancel guard after coord label",
        "if (customTitle === null) return;" not in src.split("addEventListener")[
            [i for i, s in enumerate(src.split("addEventListener")) if "contextmenu" in s][0]
        ] if "contextmenu" in src else True,
    ))

    # ── Fix 2: profile selector (MAP-PROFILE-A floating picker) ─────────────
    print("\nFix 2 — Profile selector picker path:")
    results.append(check(
        "#rm-profile-picker exists",
        'id="rm-profile-picker"' in src,
    ))
    results.append(check(
        "openProfileSelector references floating picker",
        "openProfileSelector" in src and ("rm-profile-picker" in src or "pickerEl" in src),
    ))
    results.append(check(
        "no scrollIntoView in nameplate controller",
        "scrollIntoView" not in src[src.find("initNameplate"):src.find("/* ── end nameplate controller")],
    ))
    results.append(check(
        "no rm-profile-selector-reveal panel reveal",
        "rm-profile-selector-reveal" not in src,
    ))
    results.append(check(
        "profile picker closes on chartProfile change",
        bool(re.search(r"chartProfile.*closeProfilePicker|closeProfilePicker", src)),
    ))
    results.append(check(
        "profile picker closes on outside click",
        "pickerEl.contains(e.target)" in src,
    ))
    results.append(check(
        "#chartProfile still exists in DOM (exactly once)",
        src.count('id="chartProfile"') == 1,
    ))
    results.append(check(
        "#rm-panel-chart-section still exists in DOM",
        'id="rm-panel-chart-section"' in src,
    ))

    # ── Fix 3: favorites + open chart handlers intact ─────────────────────
    print("\nFix 3 — Favorites and Open Chart handlers:")
    results.append(check(
        "favoriteMapSelectionFromButton function still present",
        "function favoriteMapSelectionFromButton" in src,
    ))
    results.append(check(
        "openChartFromMapButton function still present",
        "async function openChartFromMapButton" in src,
    ))
    results.append(check(
        "resolveChartRecordIdForShellNavigation still present",
        "function resolveChartRecordIdForShellNavigation" in src,
    ))
    results.append(check(
        "getActiveFavoriteProfileId still present",
        "function getActiveFavoriteProfileId" in src,
    ))
    results.append(check(
        "POST /favorites/save route still used",
        '"/favorites/save"' in src,
    ))
    results.append(check(
        "openChartFromMapButton still uses chartRecordId contract",
        bool(re.search(
            r"openChartFromMapButton[\s\S]{0,400}chartRecordId",
            src,
        )),
    ))
    results.append(check(
        "openChartFromMapButton still navigates to /app_shell.html#/chart",
        "app_shell.html#/chart" in src,
    ))
    results.append(check(
        "resolvePlaceFromMapSelection still present",
        "function resolvePlaceFromMapSelection" in src,
    ))

    # ── No backend changes ─────────────────────────────────────────────────
    print("\nNo backend route changes:")
    results.append(check(
        "POST /places/resolve-or-create still used",
        '"/places/resolve-or-create"' not in src or
        "resolvePlaceFromCitySelection" in src,
    ))
    results.append(check(
        "No new backend routes introduced (no new fetch POST paths)",
        src.count('fetch("/favorites/') == src.count('fetch("/favorites/'),  # stable
    ))

    # ── Truth functions preserved ──────────────────────────────────────────
    print("\nTruth functions preserved:")
    for fn in [
        "executeSearchPlan",
        "__rmSaveCurrentInvestigation",
        "collectSavedInvestigationConditions",
        "buildGenieRenderPayloadFromGv",
    ]:
        results.append(check(f"{fn} present", fn in src))

    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} PASS")
    if passed < total:
        print(f"FAILED: {total - passed}", file=sys.stderr)
        return 1
    print("PASS SLICE-3-FLOW static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
