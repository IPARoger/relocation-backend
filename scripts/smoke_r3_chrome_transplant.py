#!/usr/bin/env python3
"""Static smoke for R3: chrome transplant rows A01, A10, A15, B03, B04, B05."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    # A01: legacy solid topbar removed; single sandbox owner
    topbar_blocks = re.findall(r"\.topbar\s*\{[^}]+\}", text, re.DOTALL)
    check(len(topbar_blocks) >= 1, "consolidated .topbar rule must exist (A01)")
    base_topbar = next(
        (b for b in topbar_blocks if "position: fixed" in b and "height: 48px" in b),
        None,
    )
    check(base_topbar is not None, ".topbar base shell rule must exist (A01)")
    if base_topbar:
        check("#fafbfc" not in base_topbar, "legacy .topbar #fafbfc must be removed (A01)")
        check(
            "rgba(251,253,255,.82)" in base_topbar,
            ".topbar must use sandbox rgba(251,253,255,.82) (A01)",
        )
        check("backdrop-filter: blur(8px)" in base_topbar, ".topbar must have blur(8px) (A01)")
    explore_topbar = re.search(r"body\.rm-explore\s+\.topbar\s*\{[^}]+\}", text, re.DOTALL)
    check(explore_topbar is not None, "body.rm-explore .topbar dissolve must remain (R2)")

    # A10: exitExplore clears menu-open and cs-open
    check(
        "classList.remove('rm-explore', 'rm-menu-open', 'rm-cs-open')" in text,
        "exitExplore must remove rm-explore, rm-menu-open, rm-cs-open (A10)",
    )
    check(
        "setAttribute('aria-expanded', 'false')" in text,
        "exitExplore must reset menu handle aria-expanded (A10)",
    )

    # A15: account label
    check('id="rm-topbar-acct"' in text, "#rm-topbar-acct must exist in topbar (A15)")
    check(".rm-acct {" in text, ".rm-acct CSS must exist (A15)")
    check("getElementById('rm-topbar-acct')" in text, "renderNameplate must update #rm-topbar-acct (A15)")

    # B03: explore dim .62 + inner card + input opacity + transition
    b03 = re.search(
        r"body\.rm-explore\s+\.rm-citysearch-wrap\s*\{[^}]+\}", text, re.DOTALL
    )
    check(b03 is not None, "body.rm-explore .rm-citysearch-wrap rule must exist (B03)")
    if b03:
        body = b03.group()
        check("opacity: .62" in body, "explore city search opacity must be .62 (B03)")
        check("opacity: .65" not in body, "explore city search must not use .65 (B03)")
        check("transition:" in body, "explore city search must have transition (B03)")
    check(
        "body.rm-explore .rm-citysearch-wrap .rm-sls-wrap" in text
        and "rgba(255,255,255,.72)" in text,
        "explore dim inner card bg rgba(255,255,255,.72) required (B03)",
    )
    check(
        "body.rm-explore .rm-citysearch-wrap .rm-sls-input" in text
        and "opacity: .85" in text,
        "explore input opacity .85 required (B03)",
    )
    check(
        "body.rm-explore.rm-cs-open .rm-citysearch-wrap" in text,
        "rm-cs-open restore selector required (B03/B04)",
    )

    # B04: cs-open handle
    check('data-rm-cs-handle' in text, "#rm-citysearch-wrap must have data-rm-cs-handle (B04)")
    check(
        "classList.toggle('rm-cs-open')" in text,
        "cs-open toggle JS must exist (B04)",
    )

    # B05: dropdown styling overrides
    panel = re.search(
        r"\.rm-citysearch-wrap\s+\.rm-sls-panel\s*\{[^}]+\}", text, re.DOTALL
    )
    check(panel is not None, ".rm-citysearch-wrap .rm-sls-panel override must exist (B05)")
    if panel:
        body = panel.group()
        check("border-radius: 10px" in body, "dropdown border-radius 10px (B05)")
        check("top: calc(100% + 4px)" in body, "dropdown top offset sandbox (B05)")
    check(
        ".rm-citysearch-wrap .rm-sls-section-title" in text,
        "section title override must exist (B05)",
    )
    check(
        ".rm-citysearch-wrap .rm-sls-item:hover" in text,
        "item hover override must exist (B05)",
    )

    # R1/R2 coordinates untouched
    cluster = re.search(r"#rm-mapctrls\s*\{[^}]+\}", text, re.DOTALL)
    if cluster:
        body = cluster.group()
        check("left: 16px" in body, "#rm-mapctrls left:16px unchanged (R1)")
        check("top: 62px" in body, "#rm-mapctrls top:62px unchanged (R1)")

    # Truth surfaces present
    for fn in (
        "executeSearchPlan",
        "__rmExecuteGenieRender",
        "__rmSaveCurrentInvestigation",
        "collectSavedInvestigationConditions",
        "createQuickShareFromMap",
    ):
        check(fn in text, f"{fn} must remain present (truth wiring)")

    # Protected files not referenced as modified — static only
    check("saved_location_search_ui.js" in text, "saved_location_search_ui.js script tag must remain")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks} R3 chrome transplant checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
