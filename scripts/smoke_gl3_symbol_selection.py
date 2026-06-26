#!/usr/bin/env python3
"""GL-3 — static validation for final symbol selection assets."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GL3 = ROOT / "validation/glyph_catalog/gl3_final_selection"
MANIFEST = GL3 / "implementation_manifest.json"

REQUIRED_CATEGORIES = {"planets", "signs", "angles", "aspects", "other"}
THEME_FOLDERS = [
    "default_theme",
    "alternate_theme_1",
    "alternate_theme_2",
    "alternate_theme_3",
    "alternate_theme_4",
]
UNICODE_SUB_RE = re.compile(r"data-status=[\"']unicode_substitute[\"']|<!--\s*unicode\s*-->", re.I)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF]")


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    def ok(name: str, cond: bool, detail: str = "") -> None:
        checks.append((name, cond, detail))

    ok("gl3_dir_exists", GL3.is_dir(), str(GL3))
    ok("manifest_exists", MANIFEST.is_file(), str(MANIFEST))
    ok("missing_brief_exists", (GL3 / "missing_originals_brief.md").is_file(), "")
    ok("matrix_exists", (GL3 / "symbol_theme_matrix.md").is_file(), "")

    if not MANIFEST.is_file():
        _report(checks)
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ok("default_theme_refined", manifest.get("default_theme_id") == "refined", manifest.get("default_theme_id", ""))
    ok("deferred_gl4", manifest.get("implementation_deferred") == "GL-4", "")
    ok("five_themes_in_manifest", len(manifest.get("themes", {})) == 5, str(len(manifest.get("themes", {}))))

    for folder in THEME_FOLDERS:
        ok(f"folder_{folder}", (GL3 / folder).is_dir(), folder)
        ok(f"attribution_{folder}", (GL3 / folder / "ATTRIBUTION.md").is_file(), folder)
        theme = manifest.get("themes", {}).get(folder, {})
        symbols = theme.get("symbols", {})
        cats = {k.split("/")[0] for k in symbols}
        ok(f"categories_{folder}", REQUIRED_CATEGORIES <= cats, str(sorted(cats)))
        missing = [k for k, v in symbols.items() if v.get("status") == "needs_matching_original"]
        ok(f"missing_listed_{folder}", theme.get("needs_original_count") == len(missing), f"{theme.get('needs_original_count')} vs {len(missing)}")
        for key in missing:
            svg = GL3 / folder / f"{key}.svg"
            if svg.is_file():
                txt = svg.read_text(encoding="utf-8")
                ok(f"missing_marker_{folder}_{key}", "needs_matching_original" in txt, key)
            else:
                ok(f"missing_file_{folder}_{key}", False, str(svg))

    # scan all SVGs for emoji / unicode substitute policy
    bad_emoji = []
    bad_unicode = []
    for svg in GL3.rglob("*.svg"):
        txt = svg.read_text(encoding="utf-8", errors="ignore")
        if EMOJI_RE.search(txt):
            bad_emoji.append(str(svg.relative_to(GL3)))
        if UNICODE_SUB_RE.search(txt):
            bad_unicode.append(str(svg.relative_to(GL3)))
    ok("no_emoji_in_svgs", not bad_emoji, ", ".join(bad_emoji[:3]))
    ok("no_unicode_substitute_flag", not bad_unicode, ", ".join(bad_unicode[:3]))

    # no vendor TTF copied into gl3
    ttfs = list(GL3.rglob("*.ttf")) + list(GL3.rglob("*.otf"))
    ok("no_font_binaries_in_gl3", not ttfs, str(ttfs))

    return _report(checks)


def _report(checks: list[tuple[str, bool, str]]) -> int:
    failed = [n for n, p, _ in checks if not p]
    for name, passed, detail in checks:
        tag = "PASS" if passed else "FAIL"
        extra = f" ({detail})" if detail and not passed else ""
        print(f"  {tag} {name}{extra}")
    n = len(checks)
    print(f"\n{'PASS' if not failed else 'FAIL'} {n - len(failed)}/{n} GL-3 symbol selection checks")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
