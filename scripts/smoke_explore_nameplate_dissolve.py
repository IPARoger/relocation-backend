#!/usr/bin/env python3
"""Static smoke for R2: explore-mode nameplate dissolve in map_CURRENT.html.

Asserts that the sandbox body.explore identity-stamp dissolve rules are present,
scoped correctly to body.rm-explore, and that no R1 coordinates were altered.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []

    # ── Dissolve rule: body.rm-explore .identity-stamp ─────────────────────
    explore_stamp = re.search(
        r"body\.rm-explore\s+\.identity-stamp\s*\{[^}]+\}", text, re.DOTALL
    )
    if not explore_stamp:
        failures.append("body.rm-explore .identity-stamp rule must exist")
    else:
        body = explore_stamp.group()
        if "background: transparent" not in body:
            failures.append("body.rm-explore .identity-stamp must set background: transparent")
        if "box-shadow: none" not in body:
            failures.append("body.rm-explore .identity-stamp must set box-shadow: none")

    # ── Name stroke (ghost outline effect) ─────────────────────────────────
    if "body.rm-explore .zb-name .nm" not in text:
        failures.append("body.rm-explore .zb-name .nm rule must exist (name stroke)")
    else:
        nm_rule = re.search(
            r"body\.rm-explore\s+\.zb-name\s+\.nm\s*\{[^}]+\}", text, re.DOTALL
        )
        if nm_rule:
            body = nm_rule.group()
            if "-webkit-text-fill-color: transparent" not in body:
                failures.append("body.rm-explore .zb-name .nm must set text-fill-color transparent")
            if "-webkit-text-stroke" not in body:
                failures.append("body.rm-explore .zb-name .nm must set -webkit-text-stroke outline")

    # ── Primary text fade ───────────────────────────────────────────────────
    if "body.rm-explore .zb-primary" not in text:
        failures.append("body.rm-explore .zb-primary fade rule must exist")

    # ── Tools/caret fade ───────────────────────────────────────────────────
    tools_rule = re.search(
        r"body\.rm-explore\s+\.identity-stamp\s+\.tools\s*\{[^}]+\}", text, re.DOTALL
    )
    if not tools_rule:
        failures.append("body.rm-explore .identity-stamp .tools fade rule must exist")
    else:
        body = tools_rule.group()
        if "opacity: 0" not in body:
            failures.append("tools must set opacity:0 in explore")
        if "pointer-events: none" not in body:
            failures.append("tools must set pointer-events:none in explore")

    # ── Meta collapse ───────────────────────────────────────────────────────
    meta_rule = re.search(
        r"body\.rm-explore\s+\.zb-meta\s*\{[^}]+\}", text, re.DOTALL
    )
    if not meta_rule:
        failures.append("body.rm-explore .zb-meta collapse rule must exist")
    else:
        body = meta_rule.group()
        if "max-height: 0" not in body:
            failures.append("body.rm-explore .zb-meta must collapse max-height to 0")
        if "opacity: 0" not in body:
            failures.append("body.rm-explore .zb-meta must set opacity:0")

    # ── Base transitions wired for dissolve ────────────────────────────────
    stamp_base = re.search(
        r"\.identity-stamp\s*\{[^}]+\}", text, re.DOTALL
    )
    if stamp_base:
        body = stamp_base.group()
        if "3.5s" not in body:
            failures.append(
                ".identity-stamp base transition must use sandbox 3.5s timing for dissolve to animate"
            )

    # ── R1 coordinates must be untouched ───────────────────────────────────
    cluster_css = re.search(r"#rm-mapctrls\s*\{[^}]+\}", text, re.DOTALL)
    if cluster_css:
        body = cluster_css.group()
        if "left: 16px" not in body:
            failures.append("#rm-mapctrls left:16px must not be changed by R2")
        if "top: 62px" not in body:
            failures.append("#rm-mapctrls top:62px must not be changed by R2")
    else:
        failures.append("#rm-mapctrls CSS rule must still exist (R1 coordinate)")

    save_disk = re.search(r"#rm-save-disk\s*\{[^}]+\}", text, re.DOTALL)
    if save_disk:
        body = save_disk.group()
        if "right: 46px" not in body:
            failures.append("#rm-save-disk right:46px must not be changed by R2")
        if "bottom: 34px" not in body:
            failures.append("#rm-save-disk bottom:34px must not be changed by R2")

    # ── No truth functions altered ─────────────────────────────────────────
    for fn in (
        "executeSearchPlan",
        "__rmSaveCurrentInvestigation",
        "collectSavedInvestigationConditions",
    ):
        if fn not in text:
            failures.append(f"{fn} must remain present (truth wiring)")

    if failures:
        print(f"FAIL {len(failures)}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("PASS 14/14 R2 explore nameplate dissolve checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
