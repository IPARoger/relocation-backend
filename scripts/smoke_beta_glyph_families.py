#!/usr/bin/env python3
"""Beta glyph families — Pass 1 SVG validation."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"
MANIFEST = FONTS / "BETA_GLYPH_MANIFEST.json"
FAMILIES = ["premium", "architectural", "technical", "organic", "gentle"]
CATEGORIES = ["signs", "planets", "angles", "points", "aspects", "dignities"]
REQUIRED_ASPECTS = {"septile", "novile", "conjunction", "opposition", "square", "trine", "sextile", "quincunx"}
REQUIRED_POINTS = {"east-point", "north-node", "south-node", "chiron", "part-of-fortune", "vertex"}
REQUIRED_DIGNITIES = {"retrograde", "exaltation", "detriment", "fall"}
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF]")


def main() -> int:
    checks = []

    def ok(name, cond, detail=""):
        checks.append((name, cond, detail))

    ok("fonts_dir", FONTS.is_dir(), str(FONTS))
    ok("manifest", MANIFEST.is_file(), "")
    if MANIFEST.is_file():
        m = json.loads(MANIFEST.read_text())
        ok("five_families", len(m.get("families", {})) == 5, str(len(m.get("families", {}))))
        ok("pass1_note", "OTF" in m.get("pass", ""), m.get("pass", ""))

    for fam in FAMILIES:
        base = FONTS / fam
        ok(f"{fam}_dir", base.is_dir(), fam)
        ok(f"{fam}_glyph_map", (base / "glyph_map.json").is_file(), fam)
        ok(f"{fam}_specimen", (base / "specimen.html").is_file(), fam)
        ok(f"{fam}_unicode_map", (base / "UNICODE_MAP.md").is_file(), fam)
        svg_dir = base / "svg"
        for cat in CATEGORIES:
            ok(f"{fam}_{cat}_dir", (svg_dir / cat).is_dir(), cat)
        for asp in REQUIRED_ASPECTS:
            p = svg_dir / "aspects" / f"{asp}.svg"
            ok(f"{fam}_aspect_{asp}", p.is_file() and "needs_matching_original" not in p.read_text(), str(p))
        for pt in REQUIRED_POINTS:
            p = svg_dir / "points" / f"{pt}.svg"
            ok(f"{fam}_point_{pt}", p.is_file(), str(p))
        for d in REQUIRED_DIGNITIES:
            p = svg_dir / "dignities" / f"{d}.svg"
            ok(f"{fam}_dignity_{d}", p.is_file(), str(p))
        svgs = list(svg_dir.rglob("*.svg"))
        ok(f"{fam}_count_54", len(svgs) == 54, str(len(svgs)))
        tbd = [s for s in svgs if "needs_matching_original" in s.read_text() or ">TBD<" in s.read_text()]
        ok(f"{fam}_no_tbd", not tbd, str(len(tbd)))
        text_svgs = [s for s in svgs if "<text" in s.read_text() and "TBD" not in s.read_text()]
        ok(f"{fam}_no_text_fallback", not text_svgs, str(len(text_svgs)))
        emoji = [s for s in svgs if EMOJI.search(s.read_text())]
        ok(f"{fam}_no_emoji", not emoji, str(len(emoji)))
        ttfs = list(base.rglob("*.ttf")) + list(base.rglob("*.otf"))
        ok(f"{fam}_no_font_binaries", not ttfs, str(ttfs))

    failed = [n for n, p, _ in checks if not p]
    for name, passed, detail in checks:
        print(f"  {'PASS' if passed else 'FAIL'} {name}" + (f" ({detail})" if detail and not passed else ""))
    n = len(checks)
    print(f"\n{'PASS' if not failed else 'FAIL'} {n-len(failed)}/{n} beta glyph family checks")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
