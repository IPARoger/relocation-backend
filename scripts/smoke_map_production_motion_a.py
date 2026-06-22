#!/usr/bin/env python3
"""Static smoke for MAP-PRODUCTION-MOTION-A object-permanence architecture."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def main() -> int:
    text = MAP.read_text(encoding="utf-8")
    failures: list[str] = []

    bottle = re.search(r"#rm-bottle \{[^}]+\}", text, re.DOTALL)
    if not bottle or "display: flex" not in bottle.group():
        failures.append("#rm-bottle must use display:flex (always in DOM)")
    if bottle and "display: none" in bottle.group():
        failures.append("#rm-bottle must not use display:none")

    if "@keyframes rmBottleIn" in text:
        failures.append("rmBottleIn keyframes must be removed")
    if "body.rm-explore #rm-bottle" in text:
        failures.append("body.rm-explore #rm-bottle display toggle must be removed")

    panel_explore = re.search(r"body\.rm-explore #panel \{[^}]+\}", text)
    if not panel_explore or "width: 0" in panel_explore.group():
        failures.append("body.rm-explore #panel must not collapse via width:0")

    ghost = re.search(r"#rm-ghost-strip \{[^}]+\}", text, re.DOTALL)
    if not ghost or "display: flex" not in ghost.group():
        failures.append("#rm-ghost-strip must use display:flex (always in DOM)")
    if ghost and "display: none" in ghost.group():
        failures.append("#rm-ghost-strip must not use display:none")
    ghost_explore = re.search(r"body\.rm-explore #rm-ghost-strip \{[^}]+\}", text, re.DOTALL)
    if ghost_explore and "display: flex" in ghost_explore.group():
        failures.append("body.rm-explore #rm-ghost-strip must not toggle display")

    if ".rm-bottle--revealed" not in text:
        failures.append(".rm-bottle--revealed class missing")
    if ".rm-panel--flip-hidden" not in text:
        failures.append(".rm-panel--flip-hidden class missing")

    enter = re.search(r"function enterExplore\(\) \{", text)
    exitf = re.search(r"function exitExplore\(\) \{", text)
    if not enter or not exitf:
        failures.append("enterExplore/exitExplore functions missing")
    else:
        enter_body = text[enter.start() : exitf.start()]
        exit_body = text[exitf.start() : exitf.start() + 2500]
        if enter_body.count("requestAnimationFrame") < 2:
            failures.append("enterExplore must use two-rAF FLIP pattern")
        if exit_body.count("requestAnimationFrame") < 2:
            failures.append("exitExplore must use two-rAF FLIP pattern")

    setpill = re.search(r"function setPillState\(state, msg\) \{[^}]+\}", text, re.DOTALL)
    if not setpill:
        failures.append("setPillState missing")
    elif "innerHTML" in setpill.group():
        failures.append("setPillState must not use innerHTML")

    for cls in (".rsp-idle", ".rsp-saving", ".rsp-saved", ".rsp-error"):
        if cls not in text:
            failures.append(f"save pill pre-render span {cls} missing")

    if failures:
        print("FAIL", len(failures))
        for f in failures:
            print(" -", f)
        return 1

    print("PASS 12/12 MAP-PRODUCTION-MOTION-A static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
