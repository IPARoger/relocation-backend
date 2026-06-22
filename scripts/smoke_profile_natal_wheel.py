#!/usr/bin/env python3
"""PROFILE-NATAL-FACTS-1 — natal wheel panel on #/chart-record route."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"


def fn_body(text: str, name: str) -> str:
    m = re.search(rf"function {name}\([^)]*\) \{{", text)
    if not m:
        return ""
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[m.start() : i + 1]
    return text[m.start() : m.start() + 4000]


def main() -> int:
    shell = SHELL.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    checks.append((
        "static_natal_wheel_container",
        'id="rm-profile-natal-facts"' in shell and "function screenChartRecord" in shell,
        "chart-record screen includes natal facts container",
    ))

    hydrate = fn_body(shell, "hydrateProfileNatalFacts")
    checks.append((
        "static_hydrate_natal_wheel",
        "async function hydrateProfileNatalFacts" in shell,
        "hydrateProfileNatalFacts exists",
    ))
    checks.append((
        "static_natal_location_kind",
        'locationKind: "natal"' in hydrate,
        "natal hydration requests location_kind=natal",
    ))
    checks.append((
        "static_natal_reuses_wheel_renderer",
        "renderProfileNatalChartHtml" in hydrate and "fetchCanonicalRelocatedChart" in hydrate,
        "natal wheel reuses relocated-chart machinery",
    ))
    checks.append((
        "static_post_render_wires_natal",
        "hydrateProfileNatalFacts(root)" in shell,
        "post-render calls natal wheel hydration",
    ))
    checks.append((
        "static_birth_place_resolver",
        "function resolveBirthPlaceId" in shell,
        "birth place id resolver for natal coords",
    ))
    profile_block = shell[shell.find("function aisVgridCellHtml"):shell.find("function renderRelocatedChartHtml")]
    # PH-3: wheel extracted from the tables renderer into a dedicated wheel
    # renderer wired into the chart-stage wheel-slot (not nested in tables).
    checks.append((
        "static_profile_natal_wheel_section",
        "function renderProfileNatalWheelHtml" in shell
        and "renderRelocatedWheelHtml" in shell
        and 'id="rm-profile-wheel-slot"' in shell
        and "renderProfileNatalWheelHtml(canonical)" in hydrate,
        "profile wheel renders via dedicated wheel-slot (chart-stage), not nested in tables renderer",
    ))
    # PH-4: tband horizontal band with AIS -> PIH -> A2A -> Notes order.
    tband = profile_block[profile_block.find("function renderProfileTbandHtml"):]
    ai = tband.find("Angle in Sign"); pi = tband.find("Planet in House")
    a2 = tband.find("Aspect to Angle"); no = tband.find("renderProfileNotesCardHtml()")
    checks.append((
        "static_profile_tband_structure",
        'class="tband std rm-profile-tband"' in tband
        and -1 < ai < pi < a2 < no,
        "PH-4 tband: AIS -> PIH -> A2A -> Notes horizontal order",
    ))
    # PH-6: PIH house-only (no longitude) on Profile.
    checks.append((
        "static_profile_natal_pih_section",
        "function renderProfilePihTableHtml" in profile_block
        and "showLongitude: false" in profile_block
        and "Planet in House" in profile_block
        and "<th>Longitude</th>" not in profile_block,
        "PH-6 PIH card is house-only (no longitude column)",
    ))
    # PH-8: AIS deg/sign/min vgrid adapter.
    checks.append((
        "static_profile_natal_ais_section",
        "function renderProfileAisCardBodyHtml" in profile_block
        and "rm-ais-vgrid" in profile_block
        and "Angle in Sign" in profile_block,
        "PH-8 AIS card uses deg/sign/min vgrid",
    ))
    # PH-5: Notes card moved into tband col 4, save handler preserved.
    checks.append((
        "static_profile_notes_in_tband",
        "function renderProfileNotesCardHtml" in profile_block
        and 'data-action="save-chart-note"' in profile_block
        and 'id="rm-chart-note"' in profile_block
        and "notes-card notes-slot" in profile_block,
        "PH-5 Notes card in tband with preserved save handler",
    ))
    # PH-7: profile-scoped dignities toggle.
    checks.append((
        "static_profile_dignities_toggle",
        'pihDignitiesFooterHtml(on, "profile")' in profile_block
        and 'scope === "profile"' in shell
        and 'id="rm-profile-pih-slot"' in profile_block,
        "PH-7 profile dignities toggle re-renders PIH slot",
    ))
    checks.append((
        "static_profile_natal_a2a_section",
        "Aspect to Angle" in profile_block and "renderA2aSinglePlaceHtml" in profile_block,
        "profile natal renderer includes A2A",
    ))

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"\n{passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
