#!/usr/bin/env python3
"""GLYPH-WIRING-1 smoke — AstroDotBasic central glyph resolver."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLYPHS_JS = ROOT / "theme" / "glyphs.js"
SHELL = ROOT / "app_shell.html"
SERVER = ROOT / "main_centerline_FIXER.py"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def extract_object_block(text: str, name: str) -> str:
    m = re.search(rf"const {name} = \{{", text)
    if not m:
        fail(f"missing {name} in glyphs.js")
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    fail(f"unterminated {name}")


def parse_simple_object(block: str) -> dict[str, str]:
    pattern = r'([A-Za-z_][A-Za-z0-9_]*):\s*"([^"]*)"'
    return {k: v for k, v in re.findall(pattern, block)}


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    for path in [GLYPHS_JS, ROOT / "theme/glyphs.css", ROOT / "theme/fonts/AstroDotBasic.ttf"]:
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")

    glyphs_text = GLYPHS_JS.read_text(encoding="utf-8")
    shell_text = SHELL.read_text(encoding="utf-8")
    server_text = SERVER.read_text(encoding="utf-8")

    checks.append(("glyphs_exports_resolve", "function resolveGlyph" in glyphs_text and "window.__rmGlyphs" in glyphs_text, "resolveGlyph exported"))
    checks.append(("glyphs_format_html", "formatGlyphHtml" in glyphs_text, "formatGlyphHtml present"))
    checks.append(("glyphs_format_svg", "formatGlyphSvgText" in glyphs_text, "formatGlyphSvgText present"))

    planet = parse_simple_object(extract_object_block(glyphs_text, "PLANET_FONT"))
    sign = parse_simple_object(extract_object_block(glyphs_text, "SIGN_FONT"))
    aspect = parse_simple_object(extract_object_block(glyphs_text, "ASPECT_FONT"))
    angle = parse_simple_object(extract_object_block(glyphs_text, "ANGLE_FONT"))

    checks.append(("planet_font_map", planet == {
        "Sun": "A", "Moon": "B", "Mercury": "C", "Venus": "D", "Mars": "E",
        "Jupiter": "F", "Saturn": "G", "Uranus": "H", "Neptune": "I", "Pluto": "J", "Chiron": "U",
    }, "PLANET_FONT AstroDotBasic keys (A=Sun …)"))

    checks.append(("sign_font_map", sign == {
        "Aries": "a", "Taurus": "b", "Gemini": "c", "Cancer": "d", "Leo": "e", "Virgo": "f",
        "Libra": "g", "Scorpio": "h", "Sagittarius": "i", "Capricorn": "j", "Aquarius": "k", "Pisces": "l",
    }, "SIGN_FONT AstroDotBasic keys (a=Aries …)"))

    expected_aspect = {
        "conjunction": "m", "conjunct": "m", "opposition": "n", "square": "o", "trine": "p", "sextile": "q",
        "semisextile": "r", "quincunx": "s", "inconjunct": "s",
        "semisquare": "t", "sesquiquadrate": "u", "biquintile": "v", "quintile": "w",
    }
    checks.append(("aspect_font_map", all(aspect.get(k) == v for k, v in expected_aspect.items()), "ASPECT_FONT AstroDotBasic keys"))

    checks.append(("angle_font_map", angle == {"ASC": "P", "MC": "Q"}, "ANGLE_FONT AstroDotBasic (DSC/IC fallback)"))

    checks.append(("shell_links_glyphs_css", "/theme/glyphs.css" in shell_text, "app_shell links glyphs.css"))
    checks.append(("shell_links_glyphs_js", "/theme/glyphs.js" in shell_text, "app_shell links glyphs.js"))
    checks.append(("shell_rm_glyphs_helper", "function rmGlyphs()" in shell_text, "rmGlyphs helper"))
    checks.append(("shell_no_wheel_body_glyph", "WHEEL_BODY_GLYPH" not in shell_text, "WHEEL_BODY_GLYPH removed"))
    checks.append(("shell_planet_name_glyph", 'formatGlyphHtml("planet"' in shell_text, "planet table glyphs"))
    checks.append(("shell_sign_longitude_glyph", "formatCanonicalPlanetLongitudeHtml" in shell_text, "PIH sign glyphs"))
    checks.append(("shell_a2a_aspect_glyph", "formatA2aAspectLabelHtml" in shell_text, "A2A aspect glyphs"))
    checks.append(("server_theme_glyphs_js", "/theme/glyphs.js" in server_text, "server serves glyphs.js"))
    checks.append(("server_theme_glyphs_css", "/theme/glyphs.css" in server_text, "server serves glyphs.css"))
    checks.append(("server_theme_font", "/theme/fonts/AstroDotBasic.ttf" in server_text, "server serves font"))

    failed = [c for c in checks if not c[1]]
    for name, ok, desc in checks:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {desc}")
    if failed:
        fail(f"{len(failed)} check(s) failed")
    print(f"OK: GLYPH-WIRING-1 ({len(checks)} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
