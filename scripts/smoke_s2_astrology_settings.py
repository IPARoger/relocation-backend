#!/usr/bin/env python3
"""S2 — Astrology settings wiring smoke (static)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
DEFAULTS = ROOT / "settings" / "astrology_settings_defaults.json"


def main() -> int:
    text = SHELL.read_text(encoding="utf-8")
    checks: list[tuple[str, bool]] = []

    def ok(name: str, cond: bool) -> None:
        checks.append((name, cond))

    ok("majorAspectsPanelHtml", "function majorAspectsPanelHtml()" in text)
    ok("aspect list row", "_aspectListRow" in text and "settings-aspect-row" in text)
    ok("minor advanced gate", "Minor Aspects (Advanced)" in text)
    ok("custom orbs gate", "Custom Orbs (Advanced)" in text)
    ok("late house alert", "Late-house planet alert" in text)
    ok("house prox input", "rm-settings-house-proximity-orb" in text)
    ok("out of sign", "rm-settings-oos-aspects" in text)
    ok("a2a angles", "rm-settings-a2d-${key}" in text)
    ok("asteroids soon", "aspectsToAsteroidsHtml" in text and "rm-settings-aspects-asteroids" in text)
    ok("save major orbs", "major_aspect_orbs" in text and "${kind}orb-${id}" in text)
    ok("no orb presets", not re.search(r"\b(Strict|Normal|Loose|Generous)\b", text))
    ok("no house policy stub", "Direction-aware house-edge rule" not in text)
    ok("no legacy aspect panel", "function aspectsSettingsHtml()" not in text)

    defaults = DEFAULTS.read_text(encoding="utf-8")
    ok("defaults oos off", '"out_of_sign_aspects": false' in defaults)
    ok("defaults prox 2", '"house_proximity_orb_degrees": 2' in defaults)

    failed = [n for n, p in checks if not p]
    for name, passed in checks:
        print(f"  {'PASS' if passed else 'FAIL'} {name}")
    n = len(checks)
    print(f"\n{'PASS' if not failed else 'FAIL'} {n - len(failed)}/{n} S2 astrology settings checks")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
