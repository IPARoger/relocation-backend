#!/usr/bin/env python3
"""Static smoke for R1: Sandbox-aligned map control cluster in map_CURRENT.html.

Replaces MAP-ZOOM-A assertions (bottom-right Leaflet control) with R1 assertions
(sandbox-unified top-left cluster: custom zoomcol + navgrp at left:16 top:62).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []

    # 1. zoomControl:false must still suppress Leaflet default control
    if "zoomControl: false," not in text:
        failures.append("zoomControl: false must be present in L.map() init")

    # 2. Leaflet native zoom control must NOT be added (removed in R1)
    if "L.control.zoom(" in text:
        failures.append(
            "L.control.zoom() must not be present — R1 uses custom .rm-zoomcol buttons"
        )

    # 3. Unified cluster element must exist
    if 'id="rm-mapctrls"' not in text:
        failures.append('#rm-mapctrls cluster element must exist')

    # 4. Custom zoom buttons must exist with correct IDs
    for btn_id in ("rm-zoom-in", "rm-zoom-out", "rm-recenter"):
        if f'id="{btn_id}"' not in text:
            failures.append(f'#{btn_id} button must exist in cluster')

    # 5. Cluster CSS must be at sandbox coordinates: left:16px top:62px
    cluster_css = re.search(
        r"#rm-mapctrls\s*\{[^}]+\}", text, re.DOTALL
    )
    if not cluster_css:
        failures.append("#rm-mapctrls CSS rule must exist")
    else:
        body = cluster_css.group()
        if "left: 16px" not in body:
            failures.append("#rm-mapctrls must have left: 16px (sandbox coordinate)")
        if "top: 62px" not in body:
            failures.append("#rm-mapctrls must have top: 62px (sandbox coordinate)")

    # 6. Nav button IDs preserved for JS truth wiring
    for nav_id in ("rm-ctrl-back", "rm-ctrl-fwd", "rm-ctrl-pin"):
        if f'id="{nav_id}"' not in text:
            failures.append(f'#{nav_id} must be preserved (JS history controller wires by ID)')

    # 7. Custom zoom buttons wired to Leaflet map API
    if "rm-zoom-in" not in text or "__rmMap" not in text:
        failures.append("Custom zoom buttons must be wired via window.__rmMap")

    # 8. No bottom-right .leaflet-bottom.leaflet-right positioning rule
    if ".leaflet-bottom.leaflet-right" in text and "bottom: 100px" in text:
        failures.append(
            ".leaflet-bottom.leaflet-right bottom:100px must be removed (R1 moved zoom to cluster)"
        )

    # 9. Truth functions untouched
    for fn in (
        "executeSearchPlan",
        "__rmSaveCurrentInvestigation",
        "collectSavedInvestigationConditions",
    ):
        if fn not in text:
            failures.append(f"{fn} must remain present (truth wiring)")

    if failures:
        print(f"FAIL {len(failures)}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("PASS 9/9 R1 spatial cluster checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
