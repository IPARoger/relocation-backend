#!/usr/bin/env python3
"""RX-PARITY-1 — retrograde/station markers in PIH and A2A table surfaces."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"

MOTION_STATES = frozenset(
    {"direct", "retrograde", "station_direct", "station_retrograde"}
)


def static_table_checks() -> list[tuple[str, bool, str]]:
    shell = SHELL.read_text(encoding="utf-8")
    out: list[tuple[str, bool, str]] = []

    out.append((
        "static_resolve_motion_state",
        "function resolvePlanetMotionState" in shell
        and "entry.motion_state" in shell
        and "entry.retrograde" in shell,
        "reads canonical motion_state with retrograde fallback",
    ))
    out.append((
        "static_table_motion_markers",
        "function tablePlanetMotionMarkerHtml" in shell
        and "station_direct" in shell
        and "station_retrograde" in shell,
        "table markers for retrograde and station states",
    ))
    out.append((
        "static_format_table_planet_name",
        "function formatTablePlanetNameHtml" in shell,
        "shared planet label formatter for tables",
    ))

    pih_block = shell[
        shell.find("function renderPihTableRowsFromCanonical"): shell.find(
            "function renderComparisonAngleRowsHtml"
        )
    ]
    out.append((
        "static_pih_single_uses_motion",
        "formatTablePlanetNameHtml(name, entry)" in pih_block,
        "Screen 4 PIH planet column shows motion",
    ))

    cmp_pih = shell[
        shell.find("function renderPihComparisonHtml"): shell.find(
            "function renderPihWorkbookSectionBody"
        )
    ]
    out.append((
        "static_pih_comparison_uses_motion",
        "formatTablePlanetNameHtml(pn, motionEntry)" in cmp_pih,
        "comparison workbook PIH shows motion",
    ))

    cmp_cols = shell[
        shell.find("function renderComparisonTableHtml"): shell.find(
            "const CMP_WS_SECTIONS"
        )
    ]
    out.append((
        "static_comparison_columns_uses_motion",
        "formatTablePlanetNameHtml(pn, motionEntry)" in cmp_cols,
        "comparison columns planet rows show motion",
    ))

    a2a_block = shell[shell.find("// A2A-1:"): shell.find("function renderRelocatedChartHtml")]
    out.append((
        "static_a2a_single_planet_motion",
        "formatTablePlanetNameHtml(row.planet" in a2a_block
        and "canonicalChart.planets" in a2a_block,
        "Screen 4 A2A planet column shows motion",
    ))
    out.append((
        "static_a2a_comparison_contact_motion",
        "formatTablePlanetNameHtml(rowBody" in a2a_block
        and "rm-a2a-matrix" in a2a_block,
        "comparison A2A matrix row labels show planet motion",
    ))

    wh_start = shell.find("function wheelMotionMarkerTspans")
    wh_end = shell.find("// A2A-1:", wh_start)
    wheel_block = shell[wh_start:wh_end] if wh_start >= 0 and wh_end > wh_start else ""
    out.append((
        "static_wheel_block_unchanged",
        "function wheelMotionMarkerTspans" in wheel_block
        and "formatTablePlanetNameHtml" not in wheel_block,
        "wheel helpers not coupled to table formatter",
    ))
    table_block = shell[
        shell.find("function resolvePlanetMotionState"): shell.find(
            "function wheelMotionMarkerTspans"
        )
    ]

    out.append((
        "static_motion_marker_css",
        ".rm-motion-rx" in shell and "vertical-align: super" in shell,
        "table motion markers use superscript spacing CSS",
    ))
    out.append((
        "static_a2a_motion_marker_html",
        "function formatA2aMotionMarkerHtml" in shell
        and "formatA2aOrbCellHtml(row)" in shell,
        "A2A orb cells render applying/separating/exact markers",
    ))
    out.append((
        "static_no_client_speed_in_tables",
        "speed_deg_per_day" not in table_block,
        "table motion reads motion_state only",
    ))

    return out


def backend_checks() -> list[tuple[str, bool, str]]:
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        return [("be_skipped", True, "fastapi unavailable — static checks only")]

    sys.path.insert(0, str(ROOT))
    from main_centerline_FIXER import app

    client = TestClient(app)
    resp = client.get(
        "/relocated-chart?lat=40.7128&lon=-74.0060"
        "&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0"
    )
    out: list[tuple[str, bool, str]] = []
    if resp.status_code != 200:
        out.append(("be_relocated_chart", False, f"status={resp.status_code}"))
        return out

    planets = (resp.json().get("canonical_chart") or {}).get("planets") or {}
    motion_ok = bool(planets) and all(
        p.get("motion_state") in MOTION_STATES for p in planets.values()
    )
    fields_ok = bool(planets) and all(
        "motion_state" in p and "retrograde" in p and "station" in p
        for p in planets.values()
    )
    out.append(("be_motion_state_enum", motion_ok, f"bodies={len(planets)}"))
    out.append(("be_planet_motion_fields", fields_ok, "motion_state/retrograde/station on planets"))
    return out


def main() -> int:
    results = static_table_checks() + backend_checks()
    passed = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
