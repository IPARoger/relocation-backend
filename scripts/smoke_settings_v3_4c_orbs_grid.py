#!/usr/bin/env python3
"""Static smoke: SETTINGS-V3-4C — Orbs & Aspects grid alignment."""
from __future__ import annotations

import subprocess
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
    head_fn = text.split("function sv3OaHeadHtml()", 1)[1].split("function sv3AspectRow", 1)[0]
    row_fn = text.split("function sv3AspectRow", 1)[1].split("function settingsV3OrbsAspectsHtml", 1)[0]
    orbs_fn = text.split("function settingsV3OrbsAspectsHtml", 1)[1].split("function settingsV3AdvancedCalcHtml", 1)[0]
    apply_fn = text.split("function applySettingsV3AdvancedState", 1)[1].split("function wireSettingsV3", 1)[0]

    check("rm-sv3-oa-tbl" in row_fn and "rm-sv3-oa-cht" in row_fn and "rm-sv3-oa-orb" in row_fn, "row column order tbl/cht/orb")
    check(row_fn.find("rm-sv3-oa-tbl") < row_fn.find("rm-sv3-oa-cht") < row_fn.find("rm-sv3-oa-orb"), "Aspect Name | Tables | Chart | Orb order")
    check("rm-sv3-oa-h-tables" in head_fn and "rm-sv3-oa-h-chart" in head_fn and "rm-sv3-oa-h-orb" in head_fn, "header labels Tables/Chart/Orb")
    check("rm-sv3-oa-h-orbs" not in orbs_fn and "rm-sv3-oa-h-aspects" not in orbs_fn, "removed misaligned Orbs/Aspects umbrella headers")
    check("rm-sv3-oa-table" in orbs_fn, "orbs use HTML table for alignment")
    check("data-sv3-major-lock" in row_fn, "major aspect lock attribute")
    check("lockMajor: true" in orbs_fn, "major rows locked by default")
    check("Advanced Orbs &amp; Aspects" in orbs_fn, "advanced toggle renamed")
    check("#rm-sv3-advanced-orbs" in apply_fn and "data-sv3-major-lock" in apply_fn, "orbs advanced unlocks major controls")
    check("anyOpen" in apply_fn and "data-sv3-advanced-lock" in apply_fn, "any advanced unlocks body checkboxes")
    check("function planetsBodiesHtml" in text, "legacy settings untouched")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")

    for script in [
        ROOT / "scripts" / "smoke_settings_v3_4b_charts.py",
    ]:
        if not script.exists():
            continue
        proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        line = (proc.stdout or proc.stderr).strip().splitlines()[-1] if proc.stdout or proc.stderr else ""
        if proc.returncode != 0:
            failures.append(f"{script.name} failed: {line}")
        else:
            print(f"  {script.name}: {line}")

    if failures:
        print(f"REGRESSION FAIL ({len(failures)})")
        for f in failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
