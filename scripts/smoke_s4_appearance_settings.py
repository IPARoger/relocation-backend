#!/usr/bin/env python3
"""S4 — Appearance palette settings smoke (static)."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    shell = (ROOT / "app_shell.html").read_text(encoding="utf-8")
    palettes = (ROOT / "theme/appearance_palettes.js").read_text(encoding="utf-8")
    defs = json.loads((ROOT / "settings/astrology_settings_defaults.json").read_text())
    appear = json.loads((ROOT / "settings/appearance_settings_defaults.json").read_text())
    resolver = (ROOT / "services/account_settings_resolver.py").read_text(encoding="utf-8")
    bridge = (ROOT / "supabase_store_bridge.js").read_text(encoding="utf-8")
    map_html = (ROOT / "map_CURRENT.html").read_text(encoding="utf-8")
    checks = []

    def ok(name, cond):
        checks.append((name, cond))

    ok("appearance defaults file", appear.get("overlay_palette") == "optimistic-primary")
    ok("merged astrology defaults", defs.get("overlay_palette") == "optimistic-primary")
    ok("palette module", "RMAppearancePalettes" in palettes and "optimistic-primary" in palettes)
    ok("spring overlay twelve", palettes.count("#6E93AE") >= 1 and "SPRING_OVERLAY" in palettes)
    ok("no google rainbow placeholder", "#2f9e8f" not in map_html or "pinwheelColors" in map_html)
    ok("resolver appearance keys", "overlay_palette" in resolver and "load_appearance_settings_defaults" in resolver)
    ok("bridge appearance keys", "overlay_palette" in bridge and "loadAppearanceSettingsDefaults" in bridge)
    ok("appearance panel ui", "sec-appearance-palettes" in shell and "data-appearance-palette" in shell)
    ok("five palette groups", "inner_glow" in shell.split("collectAppearancePalettePatch")[0][-200:] or '["overlay", "aspect", "dignity", "chart", "inner_glow"]' in shell)
    ok("no custom color picker in appearance", "sec-appearance-palettes" in shell and "type=\"color\"" not in shell.split("appearancePalettesPanelHtml")[1][:1200] if "appearancePalettesPanelHtml" in shell else False)
    ok("apply appearance hook", "applyAppearanceSettingsFromEff" in shell)
    ok("save appearance patch", "collectAppearancePalettePatch" in shell)
    ok("restore appearance", "restore-appearance-defaults" in shell)
    ok("wheel css vars", "--rm-wheel-p2p-harmonious" in palettes)
    ok("aspect motion css vars", "--rm-aspect-applying" in palettes)
    ok("dignity palette integration", "patch.dignity_colors = AP.dignityColorsFromResolved" in shell)
    ok("map uses pinwheel", "RMAppearancePalettes" in map_html and "pinwheelColors" in map_html)
    ok("script include", "appearance_palettes.js" in shell)
    ok("display save bar", "showRestoreAppearance" in shell)
    ok("removed dignity stub override", shell.count("function dignitiesDisplayHtml") == 1)
    ok("optimistic dignity default", defs["dignity_colors"]["supportive"] == "#e8f5ec")
    ok("api route", "appearance_settings_defaults" in (ROOT / "main_centerline_FIXER.py").read_text(encoding="utf-8"))

    failed = [n for n,p in checks if not p]
    for n,p in checks:
        print(f"  {'PASS' if p else 'FAIL'} {n}")
    print(f"\n{'PASS' if not failed else 'FAIL'} {len(checks)-len(failed)}/{len(checks)} S4 appearance checks")
    return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())
