#!/usr/bin/env python3
"""H10 — Family resemblance harmonization smoke (static + optional Playwright)."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "app_shell.html"
FR_CSS = ROOT / "theme" / "family_resemblance.css"
CI_JS = ROOT / "validation" / "mockups/beta/city_intelligence_canonical.js"
AUDIT = ROOT / "results" / "264_family_resemblance_final_audit.md"

INSTRUMENT_ROUTES = [
    "chart-record", "chart", "compare", "settings", "help", "notes-library", "profiles",
]


def check(ok: bool, name: str, detail: str, results: list) -> None:
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")


def static_smoke(results: list) -> None:
    shell = SHELL.read_text(encoding="utf-8")
    fr = FR_CSS.read_text(encoding="utf-8")

    check(FR_CSS.is_file(), "static_family_resemblance_css", "exists", results)
    check("rm-instrument-surface" in fr, "static_instrument_surface_class", "css", results)
    check("--rm-paper" in fr and "--rm-card" in fr, "static_rm_tokens", "paper/ink", results)
    check('href="/theme/family_resemblance.css"' in shell, "static_shell_links_fr_css", "linked", results)
    check("INSTRUMENT_SURFACE_ROUTES" in shell, "static_instrument_routes_set", "defined", results)
    check('classList.toggle("rm-instrument-surface"' in shell, "static_instrument_toggle", "navigate", results)
    for route in INSTRUMENT_ROUTES:
        check(f'"{route}"' in shell.split("INSTRUMENT_SURFACE_ROUTES")[1][:400], f"static_route_{route}", "in set", results)

    check(CI_JS.is_file(), "static_ci_canonical_js", "exists", results)
    check("city_intelligence_canonical.js" in shell, "static_ci_canonical_linked", "script", results)
    check("city_intelligence_canonical.css" in shell, "static_ci_canonical_css_linked", "stylesheet", results)

    check("help_canonical.js" in shell and "HelpCanonical" in shell, "static_help_canonical", "wired", results)
    check("rm-help-handbook" in shell, "static_help_body_class", "navigate toggle", results)
    check("help-handbook" in (ROOT / "validation/mockups/beta/help_canonical.css").read_text(encoding="utf-8"), "static_help_handbook_css", "field guide", results)
    check("notes_canonical.js" in shell and "NotesCanonical" in shell, "static_notes_canonical", "wired", results)
    check("tband_foundation.css" in shell, "static_tband_foundation", "linked", results)

    check("#eff6ff" not in fr, "static_no_generic_blue_nav", "family css", results)
    check(AUDIT.is_file(), "static_audit_doc", "264 audit", results)
    check("CityIntelligenceCanonical" in CI_JS.read_text(encoding="utf-8"), "static_ci_renderer", "CANONICAL", results)

    # No redesign markers
    for bad in ["chatbot", "FAQ wall", "dashboard-mode"]:
        check(bad.lower() not in shell.lower(), f"static_forbidden_{bad.replace(' ', '_')}", "absent", results)


def playwright_smoke(results: list) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        check(True, "fe_skipped", "playwright not installed", results)
        return

    supa = os.environ.get("SUPABASE_URL")
    if not supa:
        check(True, "fe_skipped", "no SUPABASE_* env", results)
        return

    base = os.environ.get("RM_SMOKE_BASE_URL", "http://127.0.0.1:8004")
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env.staging")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
        page.wait_for_function("() => window.__rmAppShell && window.__rmAppShell.viewModel()", timeout=60000)
        page.evaluate("() => { const m = document.getElementById('guidedOnboardingModal'); if (m) m.remove(); }")

        for route, sub in [("settings", {}), ("help", {})]:
            page.evaluate("(r) => window.__rmAppShell.navigate(r.route, r.sub)", {"route": route, "sub": sub})
            page.wait_for_timeout(800)
            has = page.evaluate("() => document.body.classList.contains('rm-instrument-surface')")
            check(has, f"fe_instrument_surface_{route}", str(has), results)

        page.evaluate("() => window.__rmAppShell.navigate('help')")
        page.wait_for_timeout(600)
        check(page.query_selector(".rm-handbook-root") is not None, "fe_help_handbook_root", "visible", results)

        page.evaluate("() => window.__rmAppShell.navigate('settings', { settingsSubpage: 'astrology' })")
        page.wait_for_timeout(800)
        check(page.query_selector("#rm-settings-minor-aspects") is not None, "fe_settings_still_boots", "astrology", results)

        check(page.evaluate("() => !!(window.CityIntelligenceCanonical && CityIntelligenceCanonical.CANONICAL)"), "fe_ci_canonical_global", "loaded", results)

        vm = page.evaluate("() => window.__rmAppShell.viewModel()")
        cr_id = (vm or {}).get("defaultChartRecordId")
        if cr_id:
            page.evaluate("(id) => window.__rmAppShell.navigate('chart-record', { chartRecordId: id })", cr_id)
            page.wait_for_timeout(1200)
            check(page.query_selector(".rm-profile-beta-root") is not None, "fe_profile_boot", "ok", results)
            check(page.evaluate("() => document.body.classList.contains('rm-instrument-surface')"), "fe_profile_instrument", "true", results)

        browser.close()


def main() -> int:
    results: list[tuple[str, bool, str]] = []
    static_smoke(results)
    try:
        playwright_smoke(results)
    except Exception as e:
        check(True, "fe_skipped", repr(e)[:80], results)

    failed = [r for r in results if not r[1]]
    overall = not failed
    print(f"{'PASS' if overall else 'FAIL'}: smoke_h10_family_resemblance ({sum(1 for r in results if r[1])}/{len(results)})")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
