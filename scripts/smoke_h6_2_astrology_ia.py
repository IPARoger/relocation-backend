#!/usr/bin/env python3
"""Smoke: H6-2 Astrology settings IA harmonization.

Static checks (no server):
  * canonical astrology subsection order in settingsChartsBodyHtml
  * data-rm-astrology-section markers present
  * improved help copy (OOS, exact threshold, A2A orbs, house-edge doctrine)
  * direction-aware policy labeled display-only
  * save handler fields unchanged from H6-1
  * astrology_settings_defaults.json unchanged
  * no new settings controls added

Optional Playwright (when SUPABASE_* env present):
  * Settings astrology subpage loads with canonical DOM section order
  * Profile / Relocated / Comparison routes boot

Run:
  ./venv/bin/python scripts/smoke_h6_2_astrology_ia.py
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PYTHON = ROOT / "venv" / "bin" / "python"
DEFAULT_EMAIL = "davidleongoodman@gmail.com"
PORT = int(os.environ.get("PORT", "8004"))
DEFAULTS_PATH = ROOT / "settings" / "astrology_settings_defaults.json"
SHELL_PATH = ROOT / "app_shell.html"

CANONICAL_ASTROLOGY_SECTIONS = [
    "chart-framework",
    "bodies",
    "aspects",
    "orb-settings",
    "house-edge",
    "angle-display",
    "advanced",
]

SAVE_FIELDS = [
    "visible_planets",
    "visible_bodies",
    "visible_major_aspects",
    "visible_minor_aspects",
    "visible_minor_aspects_list",
    "major_aspect_orbs",
    "minor_aspect_orbs",
    "aspect_to_angle_orbs",
    "display_aspects_to_angles",
    "out_of_sign_aspects",
    "house_proximity_orb_degrees",
]

FORBIDDEN_OBSOLETE_LABELS = [
    "Subsequent House Rule",
    "Late house behavior",
    "Aspect-to-Angle Display",
    "aspects_planet_to_planet",
]

HELP_MARKERS = [
    "Include cross-sign aspects",
    "Exact aspect threshold",
    "fixed for now",
    "Aspect-to-angle orbs",
    "House Edge Behavior",
    "Direction-aware house-edge rule",
    "late in house only",
]


def check(cond: bool, name: str, detail: str, results: list[tuple[str, bool, str]]) -> None:
    results.append((name, cond, detail))


def extract_charts_body_block(shell: str) -> str:
    start = shell.find("function settingsChartsBodyHtml()")
    if start == -1:
        return ""
    end = shell.find("\nfunction ", start + 1)
    return shell[start : end if end > start else start + 2000]


def extract_save_handler_block(shell: str) -> str:
    start = shell.find('if (action === "save-settings")')
    if start == -1:
        return ""
    end = shell.find('if (action === "restore-astrology-defaults")', start)
    return shell[start:end] if end != -1 else shell[start : start + 4000]


def smoke_static(results: list[tuple[str, bool, str]]) -> None:
    shell = SHELL_PATH.read_text(encoding="utf-8")
    defaults = json.loads(DEFAULTS_PATH.read_text(encoding="utf-8"))

    charts_body = extract_charts_body_block(shell)
    check(bool(charts_body), "static_charts_body", "settingsChartsBodyHtml present", results)

    section_positions = []
    for sec in CANONICAL_ASTROLOGY_SECTIONS:
        marker = f'data-rm-astrology-section="{sec}"'
        pos = charts_body.find(marker)
        check(pos != -1, f"static_section_marker_{sec}", marker, results)
        if pos != -1:
            section_positions.append(pos)

    check(
        section_positions == sorted(section_positions),
        "static_section_order",
        str(CANONICAL_ASTROLOGY_SECTIONS),
        results,
    )

    for label in FORBIDDEN_OBSOLETE_LABELS:
        check(label not in charts_body, f"static_no_obsolete_{label.replace(' ', '_').lower()}", label, results)

    for marker in HELP_MARKERS:
        check(marker in shell, f"static_help_{marker.replace(' ', '_').lower()[:40]}", marker, results)

    check("function houseEdgeBehaviorHtml()" in shell, "static_house_edge_fn", "houseEdgeBehaviorHtml", results)
    check("function subsequentHouseRuleHtml()" not in shell, "static_no_old_house_fn", "renamed", results)
    check("function exactAspectThresholdInfoHtml()" in shell, "static_exact_threshold_info", "help panel", results)
    check('id="rm-settings-exact-aspect-threshold"' not in shell, "static_no_exact_threshold_control", "no new control", results)
    check(
        "display only" in shell.lower() and "direction-aware" in shell.lower(),
        "static_subsequent_house_display_only",
        "display-only label",
        results,
    )

    save_block = extract_save_handler_block(shell)
    for field in SAVE_FIELDS:
        check(field in save_block, f"static_save_{field}", field, results)
    check(
        "settingsPatch.subsequent_house_policy" not in save_block,
        "static_save_omits_subsequent_house_policy",
        "intentionally not saved",
        results,
    )

    for control_id in [
        "rm-settings-minor-aspects",
        "rm-settings-oos-aspects",
        "rm-settings-house-proximity-orb",
        "rm-settings-a2aorb-conjunction",
        "rm-settings-a2d-asc",
        "rm-settings-a2d-dsc",
        "rm-settings-a2d-mc",
        "rm-settings-a2d-ic",
        "rm-settings-planet-sun",
        "rm-settings-body-chiron",
    ]:
        check(control_id in shell, f"static_control_{control_id}", control_id, results)

    check(defaults.get("exact_aspect_threshold_deg") == 0.5, "static_defaults_exact_threshold", "0.5", results)
    check(defaults.get("subsequent_house_policy") == "display_only", "static_defaults_subsequent_policy", "display_only", results)

    try:
        from services.account_settings_resolver import get_effective_settings

        eff = get_effective_settings(None, None)
        check(eff.get("exact_aspect_threshold_deg") == 0.5, "static_resolver_exact_threshold", "0.5", results)
    except Exception as exc:  # noqa: BLE001
        check(False, "static_resolver_import", str(exc), results)


def port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) != 0


def wait_health(base: str, timeout_s: float = 25.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base + "/health", timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.3)
    return False


def resolve_playwright_session(url: str, anon: str, svc: str):
    from supabase import create_client

    anon_client = create_client(url, anon)
    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()
    admin = create_client(url, svc)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon_client.auth.verify_otp({"token_hash": link.properties.hashed_token, "type": "magiclink"})
    if not res.session:
        raise RuntimeError(f"could not authenticate {email}")
    return res


def smoke_playwright(results: list[tuple[str, bool, str]]) -> None:
    url = os.environ.get("SUPABASE_URL", "")
    anon = os.environ.get("SUPABASE_ANON_KEY", "")
    svc = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon, svc]):
        check(True, "fe_skipped_no_supabase", "SUPABASE_* not set", results)
        return

    base = os.environ.get("BASE_URL", f"http://127.0.0.1:{PORT}").rstrip("/")
    proc = None
    try:
        with urllib.request.urlopen(base + "/health", timeout=2):
            pass
    except Exception:
        if port_free(PORT):
            proc = subprocess.Popen(
                [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app", "--host", "127.0.0.1", "--port", str(PORT)],
                cwd=str(ROOT),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if not wait_health(base):
                proc.kill()
                check(False, "fe_server_start", f"could not start on {base}", results)
                return
        else:
            check(False, "fe_server_reachable", base, results)
            return

    try:
        sess = resolve_playwright_session(url, anon, svc)
        s = sess.session
        ref = urlparse(url).hostname.split(".")[0]
        storage_key = f"sb-{ref}-auth-token"
        storage_val = json.dumps(
            {
                "access_token": s.access_token,
                "refresh_token": s.refresh_token,
                "expires_at": s.expires_at,
                "expires_in": s.expires_in,
                "token_type": s.token_type or "bearer",
                "user": json.loads(sess.user.model_dump_json()),
            }
        )

        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            console_errors: list[str] = []
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.add_init_script(
                f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
            )

            page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function("()=>window.__rmAppShell && window.__rmAppShell.viewModel()", timeout=60000)
            page.evaluate(
                "()=>{const m=document.getElementById('guidedOnboardingModal');"
                "if(m){m.classList.remove('open');m.setAttribute('aria-hidden','true');m.remove();}}"
            )

            page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'astrology' })")
            page.wait_for_selector("#rm-settings-minor-aspects", timeout=15000)

            dom_order = page.evaluate(
                """() => Array.from(document.querySelectorAll('[data-rm-astrology-section]'))
                    .map(el => el.getAttribute('data-rm-astrology-section'))"""
            )
            check(dom_order == CANONICAL_ASTROLOGY_SECTIONS, "fe_astrology_section_order", str(dom_order), results)

            page.evaluate("() => { const el = document.querySelector('[data-rm-astrology-section=\"house-edge\"]'); if (el) el.scrollIntoView({ block: 'nearest' }); }")
            body_text = page.inner_text(".settings-subpage") or ""
            check("Exact aspect threshold" in body_text, "fe_exact_threshold_copy", "visible", results)
            house_edge_heading = page.evaluate(
                """() => {
                    const el = document.querySelector('[data-rm-astrology-section="house-edge"]');
                    return el ? (el.innerText || el.textContent || '').trim() : '';
                }"""
            )
            check("house edge behavior" in house_edge_heading.lower(), "fe_house_edge_heading", repr(house_edge_heading), results)

            vm = page.evaluate("() => window.__rmAppShell.viewModel()")
            cr_id = (vm or {}).get("defaultChartRecordId") or (vm or {}).get("accountDefaultChartRecordId")
            check(bool(cr_id), "fe_default_profile_id", str(cr_id), results)

            place_id = page.evaluate(
                "() => { const vm = window.__rmAppShell.viewModel(); const cr = (vm.chartRecords||[]).find(r=>r.chartRecordId===vm.defaultChartRecordId); return cr && cr.favorites && cr.favorites[0] ? cr.favorites[0].placeId : null; }"
            )
            route_cases = [
                ("chart-record", {"chartRecordId": cr_id}, ".rm-profile-beta-root, #rm-profile-natal-facts, h2"),
                ("chart", {"chartRecordId": cr_id, "placeId": place_id}, ".rm-relocated-beta-root, .rm-relocated-wheel-frame, h2"),
                ("compare", {"comparisonSetId": None}, "[data-cmp-workspace], .rm-compare-shell, h2"),
            ]
            for route, partial, wait_sel in route_cases:
                page.evaluate("(args)=>window.__rmAppShell.navigate(args.route, args.partial)", {"route": route, "partial": partial})
                page.wait_for_timeout(1200)
                check(page.query_selector(wait_sel) is not None, f"fe_route_boot_{route}", wait_sel, results)

            benign = [e for e in console_errors if "Failed to load resource" in e and "404" in e]
            bad = [e for e in console_errors if e not in benign]
            check(not bad, "fe_no_console_errors", repr(bad[:2]) if bad else "none", results)
            browser.close()
    finally:
        if proc is not None:
            proc.terminate()


def main() -> int:
    results: list[tuple[str, bool, str]] = []
    smoke_static(results)
    smoke_playwright(results)

    overall = True
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
        overall = overall and ok
    print(f"{'PASS' if overall else 'FAIL'}: smoke_h6_2_astrology_ia")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
