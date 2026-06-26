#!/usr/bin/env python3
"""S5 — Glyph library settings smoke (static)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
DEFAULTS = ROOT / "settings" / "astrology_settings_defaults.json"
REGISTRY = ROOT / "settings" / "glyph_library_registry.json"
GLYPHS_JS = ROOT / "theme" / "glyphs.js"
GLYPHS_CSS = ROOT / "theme" / "glyphs.css"
RESOLVER = ROOT / "services" / "account_settings_resolver.py"
BRIDGE = ROOT / "supabase_store_bridge.js"
SERVER = ROOT / "main_centerline_FIXER.py"
STUB = ROOT / "theme" / "glyphs" / "stubs" / "pluto_traditional.svg"
ZLZX = ROOT / "theme" / "fonts" / "AstroZLzx.ttf"


def main() -> int:
    shell = SHELL.read_text(encoding="utf-8")
    defs = json.loads(DEFAULTS.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    glyphs = GLYPHS_JS.read_text(encoding="utf-8")
    css = GLYPHS_CSS.read_text(encoding="utf-8")
    resolver = RESOLVER.read_text(encoding="utf-8")
    bridge = BRIDGE.read_text(encoding="utf-8")
    server = SERVER.read_text(encoding="utf-8")
    checks: list[tuple[str, bool]] = []

    def ok(name: str, cond: bool) -> None:
        checks.append((name, cond))

    entities = registry.get("entities", {})
    ok("registry mars", "mars" in entities and len(entities["mars"].get("variants", {})) >= 2)
    ok("registry uranus", "uranus" in entities)
    ok("registry pluto", "pluto" in entities)
    ok("registry capricorn", "capricorn" in entities)
    ok("pluto stub variant", entities.get("pluto", {}).get("variants", {}).get("traditional", {}).get("asset_status") == "stub")
    ok("capricorn euro font", entities.get("capricorn", {}).get("variants", {}).get("euro_v", {}).get("font_family") == "AstroZLzx")

    ok("defaults glyph_selections", isinstance(defs.get("glyph_selections"), dict))
    ok("defaults mars", defs.get("glyph_selections", {}).get("mars") == "standard")
    ok("defaults uranus", defs.get("glyph_selections", {}).get("uranus") == "herschel")

    ok("glyphs registry api", "setGlyphRegistry" in glyphs and "setGlyphSelections" in glyphs)
    ok("glyphs svg fragment", "formatGlyphSvgFragment" in glyphs)
    ok("glyphs no emoji resolver", "UNICODE" not in glyphs)
    ok("zlzx font file", ZLZX.is_file())
    ok("pluto stub file", STUB.is_file() and "stub" in STUB.read_text(encoding="utf-8").lower())
    ok("css zlzx face", "AstroZLzx" in css)

    ok("resolver glyph_selections", "glyph_selections" in resolver)
    ok("bridge glyph_selections", "glyph_selections" in bridge)

    ok("ui sec appearance glyphs", 'id="sec-appearance-glyphs"' in shell)
    ok("ui variant buttons", "rm-glyph-variant-btn" in shell and "data-glyph-entity" in shell)
    ok("ui apply glyph", "applyGlyphSettingsFromEff" in shell)
    ok("ui collect glyph", "collectGlyphSelectionsFromDom" in shell)
    ok("save glyph_selections", "settingsPatch.glyph_selections" in shell)
    ok("no glyph future row variants", 'settingsFutureRow("Glyph variants"' not in shell)
    ok("appearance restore glyphs", "patch.glyph_selections" in shell)

    ok("wheel svg fragment", "formatGlyphSvgFragment" in shell)
    ok("server registry route", "/settings/glyph-library-registry" in server)
    ok("server zlzx route", "/theme/fonts/AstroZLzx.ttf" in server)
    ok("server pluto stub route", "pluto_traditional.svg" in server)

    # production assets: no unicode fake substitutes in registry
    reg_text = REGISTRY.read_text(encoding="utf-8")
    ok("registry no unicode escapes", chr(92) + "u264" not in reg_text)

    failed = [n for n, p in checks if not p]
    for name, passed in checks:
        print(f"  {'PASS' if passed else 'FAIL'} {name}")
    n = len(checks)
    print(f"\n{'PASS' if not failed else 'FAIL'} {n - len(failed)}/{n} S5 glyph library checks")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
