#!/usr/bin/env python3
"""DIFFS-VISUAL-TUNE-1 — per-row duplicate fade (no reference column)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cmp_diff_row_fade_keys(row_keys: list[str]) -> set[str]:
    """Mirror app_shell cmpDiffRowFadeKeys for unit checks."""
    counts: dict[str, int] = {}
    for k in row_keys:
        key = "—" if k is None else str(k)
        counts[key] = counts.get(key, 0) + 1
    return {key for key, count in counts.items() if count >= 2}


def cmp_diff_td_class(cell_key: str, row_keys: list[str], diffs_on: bool) -> str:
    if not diffs_on:
        return ""
    key = "—" if cell_key is None else str(cell_key)
    return " rm-cmp-diff-duplicate" if key in cmp_diff_row_fade_keys(row_keys) else ""


def unit_checks() -> list[tuple[str, bool, str]]:
    out: list[tuple[str, bool, str]] = []
    row = ["1", "2", "3"]
    fades = [cmp_diff_td_class(k, row, True).strip() for k in row]
    out.append(("unit_all_unique_none_faded", fades == ["", "", ""], str(fades)))
    row = ["2", "2", "2"]
    fades = [cmp_diff_td_class(k, row, True).strip() for k in row]
    out.append(("unit_all_identical_all_faded", all(f == "rm-cmp-diff-duplicate" for f in fades), str(fades)))
    row = ["1", "1", "2"]
    fades = [cmp_diff_td_class(k, row, True).strip() for k in row]
    out.append((
        "unit_partial_duplicate",
        fades[0] == "rm-cmp-diff-duplicate" and fades[1] == "rm-cmp-diff-duplicate" and fades[2] == "",
        str(fades),
    ))
    out.append(("unit_diffs_off", cmp_diff_td_class("1", ["1", "1"], False) == "", "no class when off"))
    return out


def static_checks() -> list[tuple[str, bool, str]]:
    shell = (ROOT / "app_shell.html").read_text(encoding="utf-8")
    out: list[tuple[str, bool, str]] = []
    out.append(("static_diffs_toggle", 'data-action="toggle-cmp-diffs"' in shell, "toggle exists"))
    out.append(("static_no_reference_place_id", "referencePlaceId" not in shell, "no reference column"))
    out.append((
        "static_per_row_duplicate_helper",
        "function cmpDiffRowFadeKeys" in shell and "count >= 2" in shell,
        "row duplicate detection",
    ))
    out.append((
        "static_duplicate_fade_class",
        "rm-cmp-diff-duplicate" in shell and "rm-cmp-diff-identical" not in shell,
        "duplicate fade class",
    ))
    out.append((
        "static_diffs_helpers_exported",
        "__rmCmpDiffTdClass" in shell and "__rmCmpDiffRowFadeKeys" in shell,
        "helpers on window",
    ))
    m = re.search(r"\.rm-cmp-diff-duplicate\s*\{[^}]+\}", shell)
    opacity_ok = False
    readability_ok = False
    detail = "css block missing"
    if m:
        block = m.group(0)
        om = re.search(r"opacity:\s*(0\.\d+)", block)
        if om:
            op = float(om.group(1))
            opacity_ok = 0.42 <= op <= 0.55
            detail = f"opacity={op}"
        readability_ok = "color:" in block and "opacity: 0.28" not in block
    out.append(("static_fade_opacity_range", opacity_ok, detail))
    out.append(("static_fade_readability", readability_ok, "muted color, not 0.28"))
    out.append((
        "static_dignity_duplicate_fade",
        "td.rm-cmp-diff-duplicate.pih-house-cell.dignity-supportive" in shell,
        "dignity PIH cells share duplicate fade",
    ))
    out.append(("static_diffs_columns_table",
                'data-cmp-diff-source="canonical_chart"' in shell,
                "columns table marker"))
    out.append(("static_diffs_ais_workbook",
                "renderAisComparisonHtml(cols, visiblePlaceIds, diffCtx)" in shell,
                "AIS workbook diffs"))
    out.append(("static_diffs_row_keys_ais",
                "const rowKeys = places.map" in shell and "cmpDiffTdClass(cellKey, rowKeys" in shell,
                "AIS uses rowKeys"))
    out.append(("static_diffs_no_p2p_table",
                "renderP2pComparison" not in shell,
                "no P2P comparison table"))
    chunk = shell[shell.find("DIFFS-VISUAL-TUNE-1"):shell.find("DIFFS-VISUAL-TUNE-1") + 4000] if "DIFFS-VISUAL-TUNE-1" in shell else ""
    out.append(("static_diffs_no_judgment_copy",
                not any(x in chunk.lower() for x in ("improved", "better", "worse", "stronger")),
                "no judgment language"))
    return out


def main() -> int:
    results = unit_checks() + static_checks()
    passed = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
