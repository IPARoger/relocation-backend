#!/usr/bin/env python3
"""Static smoke for MAP-ZOOM-A: Leaflet zoom control fix in map_CURRENT.html."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []

    # D-15: zoomControl:false in L.map init suppresses default top-left blank bar
    if "zoomControl: false," not in text:
        failures.append("zoomControl: false must be present in L.map() init")

    # Default zoom control must NOT be added separately at topleft
    topleft_zoom = re.findall(
        r"L\.control\.zoom\([^)]*position\s*:\s*['\"]topleft['\"]", text
    )
    if topleft_zoom:
        failures.append("L.control.zoom at topleft must not exist (causes blank bar)")

    # D-03: zoom added at bottomright
    if 'L.control.zoom({ position: "bottomright" }).addTo(map)' not in text:
        failures.append('L.control.zoom({ position: "bottomright" }) must be added')

    # CSS: .leaflet-bottom.leaflet-right positioned to clear save disk
    br_rule = re.search(
        r"\.leaflet-bottom\.leaflet-right\s*\{[^}]+\}", text, re.DOTALL
    )
    if not br_rule:
        failures.append(".leaflet-bottom.leaflet-right CSS rule must exist")
    else:
        body = br_rule.group()
        if "bottom:" not in body:
            failures.append(".leaflet-bottom.leaflet-right must set bottom offset")
        if "right:" not in body:
            failures.append(".leaflet-bottom.leaflet-right must set right offset")
        # Verify offset clears save disk (bottom: 34px + 48px height = 82px; zoom must be > 82px)
        m = re.search(r"bottom:\s*(\d+)px", body)
        if m:
            offset = int(m.group(1))
            if offset <= 82:
                failures.append(
                    f".leaflet-bottom.leaflet-right bottom:{offset}px collides with "
                    f"#rm-save-disk (occupies bottom 34–82px); must be >82px"
                )

    # Truth functions untouched
    for fn in [
        "executeSearchPlan",
        "__rmSaveCurrentInvestigation",
        "collectSavedInvestigationConditions",
    ]:
        if fn not in text:
            failures.append(f"{fn} must remain present")

    # Zoom CSS must not broaden to affect other controls unintentionally
    if ".leaflet-control {" in text and ".leaflet-zoom" not in text:
        failures.append("bare .leaflet-control rule without zoom scope is too broad")

    if failures:
        print(f"FAIL {len(failures)}")
        for f in failures:
            print(f" - {f}")
        return 1

    print("PASS 7/7 MAP-ZOOM-A static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
