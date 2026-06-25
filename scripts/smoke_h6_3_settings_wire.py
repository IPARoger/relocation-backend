#!/usr/bin/env python3
"""Smoke: H6-3 Appearance / Map / Sharing settings wire.

Static checks (no server):
  * theme picker + regional date/time controls wired
  * map + export future rows marked coming soon
  * no City Intelligence / unit / animation settings
  * prior H6-1/H6-2 astrology wiring intact

Optional Playwright (when SUPABASE_* env present):
  * Settings boots; Appearance, Map, Exports sections render cleanly
  * Profile / Relocated / Comparison routes boot

Run:
  ./venv/bin/python scripts/smoke_h6_3_settings_wire.py
"""

from __future__ import annotations

import json
import os
import re
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
SHELL_PATH = ROOT / "app_shell.html"

FORBIDDEN_PATTERNS = [
    (r"city[_\s-]?intelligence", "City Intelligence settings"),
    (r"\bkm\s*/\s*mi\b", "km/mi unit settings"),
    (r"°C\s*/\s*°F|celsius|fahrenheit", "temperature unit settings"),
    (r"animation[-_\s]?speed", "animation speed settings"),
]

WIRED_MARKERS = [
    "relocation_theme.js",
    "settingsThemePickerHtml",
    "initAppearanceSettingsControls",
    "rm-settings-theme-grid",
    "rm-settings-date-fmt",
    "rm-settings-time-seg",
    "loadRegionalPrefs",
    "formatRegionalDate",
]

FUTURE_MARKERS = [
    'data-settings-future="map-overlays"',
    'data-settings-future="export-defaults"',
    'data-settings-future="chart-wheel"',
    "Aspect notation",
    "PNG / PDF presets",
]

ASTROLOGY_SAVE_FIELDS = [
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


def check(cond: bool, name: str, detail: str, results: list[tuple[str, bool, str]]) -> None:
    results.append((name, cond, detail))


def extract_settings_slice(shell: str) -> str:
    start = shell.find("const SETTINGS_SECTIONS = [")
    end = shell.find("function screenProfileList()")
    return shell[start:end] if start != -1 and end != -1 else ""


def extract_save_handler_block(shell: str) -> str:
    start = shell.find('if (action === "save-settings")')
    if start == -1:
        return ""
    end = shell.find('if (action === "restore-astrology-defaults")', start)
    return shell[start:end] if end != -1 else shell[start : start + 4000]


def smoke_static(results: list[tuple[str, bool, str]]) -> None:
    shell = SHELL_PATH.read_text(encoding="utf-8")
    settings_slice = extract_settings_slice(shell)

    for marker in WIRED_MARKERS:
        check(marker in shell, f"static_wired_{marker}", marker, results)

    for marker in FUTURE_MARKERS:
        check(marker in shell, f"static_future_{marker[:32]}", marker, results)

    check("function settingsFutureRow(" in shell, "static_settings_future_row", "helper", results)
    check("function settingsStubRow(" in shell, "static_settings_stub_row", "legacy helper", results)

    for pattern, label in FORBIDDEN_PATTERNS:
        check(
            re.search(pattern, settings_slice, re.I) is None,
            f"static_forbidden_{label.replace(' ', '_').lower()}",
            label,
            results,
        )

    save_block = extract_save_handler_block(shell)
    for field in ASTROLOGY_SAVE_FIELDS:
        check(field in save_block, f"static_astrology_save_{field}", field, results)
    check(
        "settingsPatch.subsequent_house_policy" not in save_block,
        "static_save_omits_subsequent_house_policy",
        "unchanged from H6-2",
        results,
    )

    check('data-rm-astrology-section="house-edge"' in shell, "static_h6_2_house_edge", "present", results)
    check("effectiveConfigPanelHtml" not in shell, "static_no_debug_panel", "absent", results)


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

            page.evaluate("()=>window.__rmAppShell.navigate('settings')")
            page.wait_for_selector(".settings-landing-grid", timeout=15000)
            check(page.query_selector(".settings-landing-grid") is not None, "fe_settings_boot", "landing", results)

            page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'display' })")
            page.wait_for_selector("#rm-settings-theme-grid", timeout=15000)
            theme_count = page.eval_on_selector_all("#rm-settings-theme-grid .settings-theme-card", "els=>els.length")
            check(theme_count >= 4, "fe_appearance_theme_picker", f"cards={theme_count}", results)
            check(page.query_selector("#rm-settings-date-fmt") is not None, "fe_appearance_date_fmt", "present", results)
            check(page.query_selector("#rm-settings-time-seg") is not None, "fe_appearance_time_seg", "present", results)

            display_text = page.inner_text("#sec-display") or ""
            check("Coming soon" in display_text, "fe_appearance_future_markers", "stubs labeled", results)
            check("Interface language" in display_text, "fe_appearance_language_stub", "deferred", results)

            map_text = page.inner_text("#sec-map-display") or ""
            check("Exact aspect lines" in map_text and "Coming soon" in map_text, "fe_map_future_rows", "stubs", results)

            page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'exports' })")
            page.wait_for_selector("#sec-exports", timeout=15000)
            exports_text = page.inner_text("#sec-exports") or ""
            check("Quick Share" in exports_text, "fe_exports_copy", "honest copy", results)
            check("PNG / PDF presets" in exports_text and "Coming soon" in exports_text, "fe_exports_future", "stubs", results)

            page_body = page.inner_text("main") or ""
            for forbidden in ["City Intelligence", "km/mi", "°C/°F", "animation speed"]:
                check(forbidden.lower() not in page_body.lower(), f"fe_forbidden_{forbidden.replace('/', '_')}", "absent", results)

            page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'astrology' })")
            page.wait_for_selector("#rm-settings-minor-aspects", timeout=15000)
            check(page.query_selector("#rm-settings-a2d-asc") is not None, "fe_astrology_still_wired", "present", results)

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
    print(f"{'PASS' if overall else 'FAIL'}: smoke_h6_3_settings_wire")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
