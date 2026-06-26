#!/usr/bin/env python3
"""Static smoke for M1-B Overlay Trust instrumentation."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    if not MAP.is_file():
        print(f"FAIL map file missing: {MAP}")
        return 1

    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    check(
        'MAP_URL.get("generation_mode") || "truth_grid"' in text,
        "truth_grid remains default generation_mode",
    )
    check(text.count("smoothFactor: 0") >= 3, "smoothFactor remains 0 on overlay layers")
    check("truth_grid_boundary_refine: true" in text, "truth_grid_boundary_refine stays true")
    check(
        "ACTIVE_RENDERER_SUBSTRATE = RENDERER_SUBSTRATES.LEGACY_SEARCH_REGIONS" in text,
        "LEGACY_SEARCH_REGIONS remains active substrate",
    )
    check("executeSearchPlan" in text and "/search-regions" in text, "production overlay path intact")
    check(
        "contour generation_mode — archaeology" in text,
        "contour path warned when active",
    )
    check("publishOverlayTrust" in text, "publishOverlayTrust helper present")
    check("window.__rmOverlayTrust" in text, "__rmOverlayTrust metadata on window")
    check("ingestOverlayTrustFromResponse" in text, "response metadata ingestion present")
    check("data-overlay-phase" in text, "data-overlay-phase hook")
    check("data-overlay-final" in text, "data-overlay-final hook")
    check("data-overlay-ready" in text, "data-overlay-ready hook")
    check("data-overlay-stage" in text, "data-overlay-stage hook")
    check("rm-overlay-ready" in text, "rm-overlay-ready event")
    check("rm-overlay-stage" in text, "rm-overlay-stage event")
    check("rm-overlay-final" in text, "rm-overlay-final event")
    check("beginOverlayTrustRender" in text, "beginOverlayTrustRender lifecycle")
    check("signalOverlayTrustHousesReady" in text, "houses-ready signal")
    check("signalOverlayTrustAspectStage" in text, "aspect stage signals")
    check('"settling"' in text, "settling phase vocabulary")
    check("Overlay phase:" in text and "if (!debugGeometry) return" in text, "debug panel gated")
    check("smoothFactor: 1" not in text, "no smoothFactor increase")
    check(MAP.stat().st_size > 1000, "map_CURRENT.html non-empty")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks} M1-B overlay trust checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
