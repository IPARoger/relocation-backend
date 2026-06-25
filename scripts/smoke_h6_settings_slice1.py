#!/usr/bin/env python3
"""Smoke: H6-1 Settings layout + astrology wiring slice 1.

Static checks (no server):
  * seven-section production nav; no Technical/Personalization nav
  * astrology controls + save handler fields
  * display_aspects_to_angles defaults all four true
  * no City Intelligence / unit / animation settings
  * house-edge doctrine copy; direction-aware policy labeled display-only

Optional Playwright (when SUPABASE_* env present):
  * Settings boots; Profile / Relocated / Comparison routes boot

Run:
  ./venv/bin/python scripts/smoke_h6_settings_slice1.py
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_h6_settings_slice1.py
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
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

CANONICAL_SECTIONS = [
    "account",
    "data",
    "astrology",
    "display",
    "notifications",
    "exports",
    "about",
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

FORBIDDEN_PATTERNS = [
    (r"city[_\s-]?intelligence", "City Intelligence settings"),
    (r"\bkm\s*/\s*mi\b", "km/mi unit settings"),
    (r"°C\s*/\s*°F|celsius|fahrenheit", "temperature unit settings"),
    (r"animation[-_\s]?speed", "animation speed settings"),
]

OBSOLETE_NAV = ["technical", "personalization"]


def check(cond: bool, name: str, detail: str, results: list[tuple[str, bool, str]]) -> None:
    results.append((name, cond, detail))


def extract_settings_sections_block(shell: str) -> str:
    start = shell.find("const SETTINGS_SECTIONS = [")
    if start == -1:
        return ""
    end = shell.find("];", start)
    return shell[start : end + 2] if end != -1 else ""


def extract_save_handler_block(shell: str) -> str:
    start = shell.find('if (action === "save-settings")')
    if start == -1:
        return ""
    end = shell.find('if (action === "restore-astrology-defaults")', start)
    return shell[start:end] if end != -1 else shell[start : start + 4000]


def smoke_static(results: list[tuple[str, bool, str]]) -> None:
    shell = SHELL_PATH.read_text(encoding="utf-8")
    defaults = json.loads(DEFAULTS_PATH.read_text(encoding="utf-8"))

    sections_block = extract_settings_sections_block(shell)
    check(bool(sections_block), "static_settings_sections_block", "SETTINGS_SECTIONS present", results)

    for sec_id in CANONICAL_SECTIONS:
        check(
            f'id: "{sec_id}"' in sections_block,
            f"static_nav_{sec_id}",
            f"section {sec_id}",
            results,
        )
    id_count = sections_block.count('id: "')
    check(
        id_count == 7,
        "static_nav_count_7",
        f"ids={id_count}",
        results,
    )

    for obsolete in OBSOLETE_NAV:
        in_nav = re.search(
            rf'label:\s*"[^{{}}]*{obsolete.title()}[^{{}}]*"[^}}]*id:\s*"{obsolete}"',
            sections_block,
            re.I,
        )
        check(in_nav is None, f"static_no_nav_{obsolete}", f"obsolete nav {obsolete}", results)

    check(
        "function screenSettings()" in shell,
        "static_screen_settings",
        "screenSettings renderer",
        results,
    )
    for marker in [
        "rm-settings-minor-aspects",
        "rm-settings-oos-aspects",
        "rm-settings-a2d-asc",
        "rm-settings-a2d-mc",
        "rm-settings-a2d-dsc",
        "rm-settings-a2d-ic",
        "rm-settings-house-proximity-orb",
        "rm-settings-a2aorb-conjunction",
    ]:
        check(marker in shell, f"static_astrology_{marker}", marker, results)

    a2a_defaults = defaults.get("display_aspects_to_angles") or {}
    for angle in ("asc", "mc", "dsc", "ic"):
        check(
            a2a_defaults.get(angle) is True,
            f"static_defaults_a2a_{angle}",
            f"{angle}={a2a_defaults.get(angle)}",
            results,
        )

    save_block = extract_save_handler_block(shell)
    for field in SAVE_FIELDS:
        check(field in save_block, f"static_save_{field}", field, results)
    check(
        "settingsPatch.subsequent_house_policy" not in save_block,
        "static_save_omits_subsequent_house_policy",
        "intentionally not saved until live",
        results,
    )
    check(
        "house_system intentionally omitted" in save_block,
        "static_save_omits_house_system",
        "house system display-only",
        results,
    )

    settings_slice = shell[shell.find("const SETTINGS_SECTIONS"): shell.find("function screenProfileList")]
    for pattern, label in FORBIDDEN_PATTERNS:
        check(
            re.search(pattern, settings_slice, re.I) is None,
            f"static_forbidden_{label.replace(' ', '_').lower()}",
            label,
            results,
        )

    check(
        "effectiveConfigPanelHtml" not in shell,
        "static_no_debug_effective_panel",
        "removed debug effective-config panel",
        results,
    )
    check(
        "late in house only" in shell.lower() or "late house only" in shell.lower(),
        "static_house_edge_doctrine_copy",
        "direction-aware house-edge copy present",
        results,
    )
    check(
        "display only" in shell.lower() and "direction-aware" in shell.lower(),
        "static_subsequent_house_display_only",
        "subsequent house labeled display-only",
        results,
    )
    check(
        "function rehydrateSettingsConsumers()" in shell
        and '"chart-record"' in shell.split("function rehydrateSettingsConsumers()")[1].split("function applyAccountSettingsPatch")[0],
        "static_rehydrate_profile_route",
        "chart-record in rehydrateSettingsConsumers",
        results,
    )

    try:
        from services.account_settings_resolver import get_effective_settings

        eff = get_effective_settings(None, None)
        for field in [
            "visible_planets",
            "visible_bodies",
            "visible_major_aspects",
            "aspect_to_angle_orbs",
            "display_aspects_to_angles",
            "out_of_sign_aspects",
            "exact_aspect_threshold_deg",
        ]:
            check(field in eff, f"static_resolver_{field}", field, results)
        a2a = eff.get("display_aspects_to_angles") or {}
        check(
            all(a2a.get(k) is True for k in ("asc", "mc", "dsc", "ic")),
            "static_resolver_a2a_all_four",
            str(a2a),
            results,
        )
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
    res = anon_client.auth.verify_otp(
        {"token_hash": link.properties.hashed_token, "type": "magiclink"}
    )
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

            def load_shell():
                page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
                page.wait_for_function("()=>window.__rmAppShell && window.__rmAppShell.viewModel()", timeout=60000)
                page.evaluate(
                    "()=>{const m=document.getElementById('guidedOnboardingModal');"
                    "if(m){m.classList.remove('open');m.setAttribute('aria-hidden','true');m.remove();}}"
                )

            load_shell()
            page.evaluate("()=>window.__rmAppShell.navigate('settings')")
            page.wait_for_selector(".settings-landing-grid", timeout=15000)
            nav_count = page.eval_on_selector_all(".settings-nav .settings-nav-item", "els=>els.length")
            check(nav_count == 7, "fe_settings_boot", f"nav_items={nav_count}", results)

            page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'astrology' })")
            page.wait_for_selector("#rm-settings-minor-aspects", timeout=15000)
            check(page.query_selector("#rm-settings-planet-sun") is not None, "fe_astrology_controls", "present", results)

            for angle in ("asc", "mc", "dsc", "ic"):
                el = page.query_selector(f"#rm-settings-a2d-{angle}")
                on = page.eval_on_selector(f"#rm-settings-a2d-{angle}", "el=>el.checked") if el else False
                check(on, f"fe_a2d_default_{angle}", f"checked={on}", results)

            labels = page.evaluate(
                "() => Array.from(document.querySelectorAll('.settings-nav-item')).map(el => el.textContent.trim())"
            )
            check(
                "Technical" not in labels and "Personalization" not in labels,
                "fe_no_obsolete_nav_labels",
                str(labels),
                results,
            )

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
                page.evaluate(
                    "(args)=>window.__rmAppShell.navigate(args.route, args.partial)",
                    {"route": route, "partial": partial},
                )
                page.wait_for_timeout(1200)
                ok = page.query_selector(wait_sel) is not None
                check(ok, f"fe_route_boot_{route}", wait_sel, results)

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
    print(f"{'PASS' if overall else 'FAIL'}: smoke_h6_settings_slice1")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
