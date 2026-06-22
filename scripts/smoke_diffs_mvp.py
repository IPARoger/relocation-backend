#!/usr/bin/env python3
"""DIFFS-MVP-1 — static validation for comparison Diffs mode."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def static_checks() -> list[tuple[str, bool, str]]:
    shell = (ROOT / "app_shell.html").read_text(encoding="utf-8")
    out: list[tuple[str, bool, str]] = []
    out.append(("static_diffs_toggle", 'data-action="toggle-cmp-diffs"' in shell, "toggle exists"))
    out.append(("static_diffs_fade_class", "rm-cmp-diff-identical" in shell, "fade class"))
    out.append(("static_diffs_helpers_exported",
                "__rmCmpDiffTdClass" in shell and "__rmBuildComparisonDiffContext" in shell,
                "helpers on window"))
    out.append(("static_diffs_columns_table",
                'data-cmp-diff-source="canonical_chart"' in shell,
                "columns table marker"))
    out.append(("static_diffs_no_p2p_table",
                "renderP2pComparison" not in shell and "p2p-comparison" not in shell.lower(),
                "no P2P comparison table"))
    out.append(("static_diffs_no_summary",
                "diff-summary" not in shell.lower() and "renderDiffSummary" not in shell,
                "no summary panel"))
    chunk = shell[shell.find("DIFFS-MVP-1"):shell.find("DIFFS-MVP-1") + 5000] if "DIFFS-MVP-1" in shell else ""

    out.append(("static_diffs_ais_workbook",
                "renderAisComparisonHtml(cols, visiblePlaceIds, diffCtx)" in shell,
                "AIS workbook diffs"))
    out.append(("static_diffs_fade_opacity",
                "opacity: 0.28" in shell and "rm-cmp-diff-identical" in shell,
                "stronger fade opacity"))
    out.append(("static_diffs_angle_tab_filter",
                "cmpAngleTabMatchesRow" in shell and "data-cmp-a2a-angle" in shell,
                "angle tabs filter AIS/A2A"))
    out.append(("static_diffs_a2a_motion_display",
                "formatA2aMotionSuffix" in shell,
                "A2A motion suffix in cells"))
    out.append(("static_diffs_no_judgment_copy",
                not any(x in chunk.lower() for x in ("improved", "better", "worse", "stronger")),
                "no judgment language in diff block"))
    return out


def main() -> int:
    results = static_checks()
    passed = 0
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
        if ok:
            passed += 1
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
