#!/usr/bin/env python3
"""Static smoke for MAP-PROFILE-A: floating profile picker in map_CURRENT.html."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []

    if 'id="rm-profile-picker"' not in text:
        failures.append("#rm-profile-picker must exist")
    if text.count('id="chartProfile"') != 1:
        failures.append("#chartProfile must exist exactly once")

    # chartProfile owned by picker, not panel section
    picker_block = text[text.find('id="rm-profile-picker"'):text.find('id="rm-profile-picker"') + 600]
    if 'id="chartProfile"' not in picker_block:
        failures.append("#chartProfile must live inside #rm-profile-picker")

    if "openProfileSelector" not in text:
        failures.append("openProfileSelector must exist")

    open_fn = re.search(r"function openProfileSelector\(\) \{[\s\S]{0,1200}?\n    \}", text)
    if not open_fn:
        failures.append("openProfileSelector function body not found")
    else:
        body = open_fn.group()
        if "rm-profile-picker" not in body and "pickerEl" not in body:
            failures.append("openProfileSelector must reference profile picker")
        if "scrollIntoView" in body:
            failures.append("openProfileSelector must not call scrollIntoView")
        if "rm-profile-selector-reveal" in body:
            failures.append("openProfileSelector must not use rm-profile-selector-reveal")
        if "rm-panel-chart-section" in body:
            failures.append("openProfileSelector must not depend on rm-panel-chart-section")

    if "scrollIntoView" in text[text.find("initNameplate"):text.find("initNameplate") + 4000]:
        failures.append("nameplate controller must not use scrollIntoView")

    if "rm-profile-selector-reveal" in text:
        failures.append("rm-profile-selector-reveal must be removed")

    if "closeProfilePicker" not in text:
        failures.append("closeProfilePicker must exist")

    # Outside-click close
    np_ctrl = text[text.find("initNameplate"):text.find("/* ── end nameplate controller")]
    if "pickerEl.contains(e.target)" not in np_ctrl:
        failures.append("picker must close on outside click")
    if 'e.key === "Escape"' not in np_ctrl and "e.key === 'Escape'" not in np_ctrl:
        failures.append("picker must close on Escape key")

    # Profile change still wired
    if "chartProfile" not in np_ctrl or "closeProfilePicker" not in np_ctrl:
        failures.append("profile change handler must remain on chartProfile")

    # Picker CSS
    if "#rm-profile-picker" not in text or ".rm-pp-open" not in text:
        failures.append("profile picker CSS must be present")

    # Truth paths untouched
    for fn in ["executeSearchPlan", "__rmSaveCurrentInvestigation", "loadChartProfiles"]:
        if fn not in text:
            failures.append(f"{fn} must remain present")

    if failures:
        print(f"FAIL {len(failures)}")
        for f in failures:
            print(f" - {f}")
        return 1

    print("PASS 14/14 MAP-PROFILE-A profile picker static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
