#!/usr/bin/env python3
"""Static smoke: SLICE-2-CHROME assertions for map_CURRENT.html.

Verifies chrome repositioning changes landed correctly.

Run:
    venv/bin/python scripts/smoke_layout_slice2.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def check(label: str, ok: bool) -> bool:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    return ok


def main() -> int:
    if not MAP.exists():
        print(f"ABORT: {MAP} not found", file=sys.stderr)
        return 1

    src = MAP.read_text(encoding="utf-8")
    results: list[bool] = []

    print("\nTopbar chrome (SLICE-2-CHROME):")
    results.append(check(".rm-brand present", 'class="rm-brand"' in src))
    results.append(check(".rm-mainmenu present", 'class="rm-mainmenu"' in src))
    results.append(check(".rm-topright present", 'class="rm-topright"' in src))
    results.append(check("hamburger #rm-menu-handle present", 'id="rm-menu-handle"' in src))
    results.append(check("topbar has nav links", 'class="rm-nav-link' in src))
    results.append(check("topbar has 'Relocation' brand text", ">Relocation<" in src))

    print("\nQuick Share placement:")
    results.append(check(
        "#quickShareBtn exists exactly once",
        src.count('id="quickShareBtn"') == 1,
    ))
    results.append(check(
        "#quickShareBtn is inside topbar (before </header>)",
        src.index('id="quickShareBtn"') < src.index('</header>'),
    ))
    results.append(check(
        "#quickShareBtn has rm-share-btn class (topbar style)",
        'class="rm-share-btn"' in src,
    ))

    print("\nCity search placement:")
    results.append(check(".rm-citysearch-wrap floating wrapper present", 'class="rm-citysearch-wrap"' in src))
    results.append(check(
        "#rm-map-loc-search-mount is inside .rm-citysearch-wrap",
        src.index('id="rm-map-loc-search-mount"') > src.index('rm-citysearch-wrap'),
    ))
    results.append(check("Location panel-section marked hidden", 'rm-panel-section-hidden' in src))
    results.append(check(".rm-citysearch-wrap fixed CSS present", '.rm-citysearch-wrap' in src))

    print("\nProfile selector:")
    results.append(check("#chartProfile still exists in DOM", 'id="chartProfile"' in src))
    results.append(check("Chart section has #rm-panel-chart-section id", 'id="rm-panel-chart-section"' in src))
    results.append(check("#rm-panel-chart-section CSS hidden", '#rm-panel-chart-section { display: none !important; }' in src))

    print("\nPin / history controls:")
    results.append(check("#rm-ctrl-back present", 'id="rm-ctrl-back"' in src))
    results.append(check("#rm-ctrl-fwd present", 'id="rm-ctrl-fwd"' in src))
    results.append(check("#rm-ctrl-pin present", 'id="rm-ctrl-pin"' in src))
    results.append(check("back/fwd have .rm-full/.rm-mini spans", 'class="rm-full"' in src and 'class="rm-mini"' in src))
    results.append(check("#rm-map-controls uses fixed positioning in CSS",
        bool(re.search(r'#rm-map-controls\s*\{[^}]*position:\s*fixed', src, re.DOTALL))))

    print("\nGV copy polish:")
    results.append(check('"Variable builder" section title removed',
        '<div class="panel-section-title">Variable builder</div>' not in src))
    results.append(check('"Choose Variable" placeholder present', '"Choose Variable"' in src))
    results.append(check('"Select variable" gone', '"Select variable"' not in src))

    print("\nPanel cleanup:")
    results.append(check("Panel <h1> brand removed/hidden", '<h1>Relocation Mapper</h1>' not in src))
    results.append(check("Exactly one #quickShareBtn", src.count('id="quickShareBtn"') == 1))

    print("\nTruth functions preserved:")
    for fn in [
        "executeSearchPlan",
        "__rmSaveCurrentInvestigation",
        "collectSavedInvestigationConditions",
        "gvVariablesToConditionSnapshot",
        "applySavedInvestigationConditions",
        "conditionsJsonToGvVariables",
        "buildGenieRenderPayloadFromGv",
        "invalidateMapSizeSoon",
    ]:
        results.append(check(f"{fn} present", fn in src))

    print("\nSlice 1 layout preserved:")
    map_rule = re.search(r"#map\s*\{([^}]+)\}", src)
    map_body = map_rule.group(1) if map_rule else ""
    results.append(check("#map position:fixed", "position: fixed" in map_body))
    panel_rule = re.search(r"#panel\s*\{([^}]+)\}", src)
    panel_body = panel_rule.group(1) if panel_rule else ""
    results.append(check("#panel position:fixed", "position: fixed" in panel_body))
    results.append(check("#panel 304px", "width: 304px" in panel_body))

    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} PASS")
    if passed < total:
        print(f"FAILED: {total - passed}", file=sys.stderr)
        return 1
    print("PASS SLICE-2-CHROME static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
