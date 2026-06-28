#!/usr/bin/env python3
"""Static smoke: SETTINGS-V3-4B — Charts section cleanup."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    text = SHELL.read_text(encoding="utf-8")
    bodies_fn = text.split("function sv3BodiesHeadHtml()", 1)[1].split("function settingsV3ZodiacHouseHtml", 1)[0]
    fold_const = text.split("const SV3_ABOVE_FOLD_BODIES", 1)[1].split("const SV3_ADVANCED_BODIES", 1)[0]
    zodiac_fn = text.split("function settingsV3ZodiacHouseHtml()", 1)[1].split("function sv3OaHeadHtml", 1)[0]
    patch_fn = text.split("function collectSettingsV3Patch()", 1)[1].split("function screenSettingsV3", 1)[0]

    check('"settings-v3": screenSettingsV3' in text, "settings-v3 route registered")
    check("function settingsV3ChartsBodyHtml" in text, "Charts body renderer")
    check('"Chiron"' in fold_const and "foldRows" in bodies_fn, "Chiron in main bodies table")
    check('"North Node"' in fold_const and '"South Node"' in fold_const, "Both lunar nodes in above-fold list")
    check("rm-sv3-advanced-bodies" in bodies_fn, "Advanced bodies dropdown separate")
    check(bodies_fn.find("foldRows") < bodies_fn.find("rm-sv3-advanced-bodies"), "Above-fold bodies before Advanced")
    check(bodies_fn.find("North Node") < bodies_fn.find("rm-sv3-advanced-bodies"), "North Node above Advanced")
    check(bodies_fn.find("South Node") < bodies_fn.find("rm-sv3-advanced-bodies"), "South Node above Advanced")
    check("Advanced Bodies" in bodies_fn, "Advanced Bodies label")
    check("rm-sv3-bodies-tbl" in bodies_fn and "rm-sv3-bodies-cht" in bodies_fn, "Tables/Chart columns on bodies")
    check("rm-sv3-oa-table" in text and "rm-sv3-oa-h-orb" in text, "table-based orbs grid with Orb header")
    check("rm-sv3-late-alert" in text, "late-in-house alert toggle")
    check("rm-sv3-late-orb" in text, "late-house orb adjustment control")
    check("rm-sv3-oos-aspects" in text, "out-of-sign aspects toggle")
    check("rm-sv3-show-a2a" in text, "show aspects to angles toggle")
    check('data-action="save-settings-v3"' in text, "save handler wired")
    check("collectSettingsV3Patch" in text, "V3 patch collector")
    check('collectTbl("body", bodyIds)' in patch_fn, "save collects north/south node with chiron")
    check("anyAdvOpen" in patch_fn, "any advanced section unlocks save for bodies")
    adv = text.split("function settingsV3AdvancedCalcHtml", 1)[1][:800]
    check("Minor aspects" not in adv or "configured in the sections above" in adv, "no duplicate Minor aspects row")
    check("Custom orbs" not in adv, "no duplicate Custom orbs row")
    check("House system" not in adv or "configured in the sections above" in adv, "no duplicate House system row")
    check(zodiac_fn.count("rm-sv3-house-system") == 1, "single House System control in Zodiac section")
    check("Sidereal" in zodiac_fn and "disabled" in zodiac_fn, "Sidereal greyed out")
    check("function planetsBodiesHtml" in text, "legacy settings bodies preserved")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
