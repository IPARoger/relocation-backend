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
    sv3 = text.split("// ── SETTINGS-V3 Charts", 1)[1].split("function screenSettings()", 1)[0]
    bodies_fn = text.split("function settingsV3BodiesHtml()", 1)[1].split("function settingsV3ZodiacHouseHtml", 1)[0]
    sv3_const = text.split("const SV3_SPECIAL_BODIES", 1)[1].split("const SV3_ADVANCED_BODIES", 1)[0]
    zodiac_fn = text.split("function settingsV3ZodiacHouseHtml()", 1)[1].split("function sv3AspectRow", 1)[0]

    check('"settings-v3": screenSettingsV3' in text, "settings-v3 route registered")
    check("function settingsV3ChartsBodyHtml" in text, "Charts body renderer")
    check('"Chiron"' in sv3_const and "specialRows" in bodies_fn, "Chiron in main bodies table")
    check('"North Node"' in sv3_const and '"South Node"' in sv3_const, "Lunar nodes labeled in main list")
    check("rm-sv3-advanced-bodies" in bodies_fn, "Advanced bodies dropdown separate")
    check(bodies_fn.find("Chiron") < bodies_fn.find("rm-sv3-advanced-bodies"), "Chiron above Advanced dropdown")
    check(bodies_fn.find("North Node") < bodies_fn.find("rm-sv3-advanced-bodies"), "North Node above Advanced")
    check(bodies_fn.find("South Node") < bodies_fn.find("rm-sv3-advanced-bodies"), "South Node above Advanced")
    check(".rm-sv3-oa-h-orb { grid-column: 4;" in text, "Orb header above orb column")
    check("rm-sv3-oa-h-tables" in text and "rm-sv3-oa-h-chart" in text, "Tables/Chart headers present")
    check("rm-sv3-late-alert" in text, "late-in-house alert toggle")
    check("rm-sv3-late-orb" in text, "late-house orb adjustment control")
    check("rm-sv3-oos-aspects" in text, "out-of-sign aspects toggle")
    check("rm-sv3-show-a2a" in text, "show aspects to angles toggle")
    check("data-action=\"save-settings-v3\"" in text, "save handler wired")
    check("collectSettingsV3Patch" in text, "V3 patch collector")
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
