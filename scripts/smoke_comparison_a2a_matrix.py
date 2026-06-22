#!/usr/bin/env python3
"""COMPARISON-PROFILE-REALITY-FIX-1 — comparison A2A matrix + diffs wiring checks."""

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
    return text[m.start() : m.start() + 8000]


def main() -> int:
    shell = SHELL.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    matrix_fn = fn_body(shell, "renderA2aComparisonHtml")
    checks.append((
        "static_a2a_matrix_shape",
        'data-a2a-shape="matrix"' in matrix_fn and "getA2aMatrixRowLabels" in matrix_fn,
        "comparison A2A uses fixed matrix renderer",
    ))
    checks.append((
        "static_a2a_matrix_all_body_rows",
        "getA2aMatrixRowLabels()" in matrix_fn and "formatA2aMatrixCellHtml(hit)" in matrix_fn,
        "matrix renders all body rows with cell formatter",
    ))
    checks.append((
        "static_a2a_matrix_empty_dash",
        'formatA2aMatrixCellHtml(hit)' in matrix_fn and 'return "—"' in shell[shell.find("function formatA2aMatrixCellHtml"):shell.find("function a2aMatrixCellDiffKey")],
        "empty matrix cells render em dash",
    ))
    checks.append((
        "static_a2a_matrix_rx_labels",
        "formatTablePlanetNameHtml(rowBody" in matrix_fn,
        "matrix row labels include Rx markers",
    ))
    checks.append((
        "static_a2a_matrix_angle_column_filter",
        "data-cmp-a2a-col-angle" in shell and "table.rm-a2a-matrix" in shell,
        "angle tabs filter A2A matrix columns",
    ))
    checks.append((
        "static_a2a_matrix_diffs",
        "a2aMatrixCellDiffKey" in matrix_fn and "cmpDiffTdClass" in matrix_fn,
        "A2A matrix cells participate in diffs",
    ))
    checks.append((
        "static_no_p2p_comparison_table",
        "aspects_planet_to_planet" not in fn_body(shell, "renderA2aComparisonHtml")
        and "p2p" not in shell[shell.find("CMP_WS_SECTIONS"):shell.find("function renderComparisonTableHtml")].lower(),
        "comparison workspace has no P2P table section",
    ))
    checks.append((
        "static_pih_comparison_diffs",
        "cmpDiffTdClass" in fn_body(shell, "renderPihComparisonHtml"),
        "PIH comparison uses diffs classes",
    ))
    checks.append((
        "static_ais_comparison_diffs",
        "cmpDiffTdClass" in fn_body(shell, "renderAisComparisonHtml"),
        "AIS comparison uses diffs classes",
    ))
    checks.append((
        "static_diffs_per_row_no_reference",
        "cmpDiffRowFadeKeys" in shell and "count >= 2" in shell and "rm-cmp-diff-identical" not in shell,
        "diffs use per-row duplicate semantics without reference column",
    ))

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"\n{passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
