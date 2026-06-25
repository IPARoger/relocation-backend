#!/usr/bin/env python3
"""Static smoke: H9 — Help handbook (field guide) in app_shell."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
HELP_JS = ROOT / "validation" / "mockups" / "beta" / "help_canonical.js"
HELP_CSS = ROOT / "validation" / "mockups" / "beta" / "help_canonical.css"
MOCKUP = ROOT / "validation" / "mockups" / "beta" / "help_handbook.html"
DRAWER = ROOT / "account_drawer.js"


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    shell = SHELL.read_text(encoding="utf-8")
    help_js = HELP_JS.read_text(encoding="utf-8")
    mockup = MOCKUP.read_text(encoding="utf-8")
    drawer = DRAWER.read_text(encoding="utf-8")

    check(HELP_JS.exists(), "help_canonical.js present")
    check(HELP_CSS.exists(), "help_canonical.css present")
    check(MOCKUP.exists(), "help_handbook.html mockup present")
    check("global.HelpCanonical" in help_js, "HelpCanonical export")
    check("CANONICAL: HELP_CANONICAL" in help_js, "CANONICAL flag")
    check("HANDBOOK_SECTIONS" in help_js, "HANDBOOK_SECTIONS content")
    check("renderPageHtml" in help_js, "renderPageHtml in module")
    check("help-handbook-entry" in help_js, "progressive disclosure markup")
    check("help_canonical.js" in shell, "app_shell loads help_canonical.js")
    check("help_canonical.css" in shell, "app_shell loads help_canonical.css")
    check("function helpCanonicalReady()" in shell, "helpCanonicalReady helper")
    check("HelpCanonical.renderPageHtml" in shell, "screenHelp delegates to HelpCanonical")
    check("function wireHelpHandbook" in shell, "wireHelpHandbook present")
    check('wireHelpHandbook($("#main"))' in shell, "render wires help handbook")
    check("rm-help-handbook" in shell, "help body class toggled")

    check("help: screenHelp" in shell, "help route in SCREEN_RENDERERS")
    check('{ id: "help"' in shell, "help in ALL_ROUTES")
    check("navigate(\"help\")" in drawer, "account drawer navigates to help")

    bundle = shell + help_js + mockup

    check("help-handbook-toc" in bundle, "TOC nav present")
    check("rm-help-search" in bundle, "search input present")
    check('placeholder="Search handbook' in bundle, "search placeholder")
    check("help-handbook" in bundle, "help-handbook root class")
    check("help-handbook-section" in bundle, "paper section cards")
    check("help-handbook-plate" in bundle, "field-guide plates")
    check("help-kicker" in bundle, "ink whisper kicker")

    for route in ("map", "settings", "chart-record", "compare", "notes-library", "profiles"):
        check(f'data-nav="{route}"' in bundle, f"product link: {route}")

    anti_patterns = [
        (r"chatbot", "chatbot pattern"),
        (r"faq-wall|faq_wall", "FAQ wall pattern"),
        (r"ask-ai|ai-advisor", "AI advisor chat pattern"),
        (r"Get started free|Sign up now|limited time", "marketing copy pattern"),
    ]
    for pat, label in anti_patterns:
        if re.search(pat, bundle, re.I):
            check(False, f"forbidden {label} found")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
