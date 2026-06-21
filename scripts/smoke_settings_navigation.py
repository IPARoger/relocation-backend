#!/usr/bin/env python3
"""Smoke: Settings navigation framework (W2-SETTINGS-1).

Verifies canonical settings subpages, sidebar navigation, legacy URL aliases,
and landing grid without testing save persistence (see smoke_settings_account.py).

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_settings_navigation.py
"""

from __future__ import annotations

import json
import os
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
PORT = 8004

CANONICAL_SUBPAGES = [
    ("account", "#sec-account-identity"),
    ("astrology", "#rm-settings-minor-aspects"),
    ("display", "#sec-display"),
    ("notifications", "#sec-notifications"),
    ("exports", "#sec-exports"),
    ("data", "#sec-data-profiles"),
    ("about", "#sec-about"),
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def fetch(base, path, headers=None, method="GET", body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    hdrs = dict(headers or {})
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{base}{path}", headers=hdrs, method=method, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read()


def route_present(base):
    try:
        st, _ = fetch(base, "/health", timeout=3)
    except Exception:
        return None
    return st == 200


def port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) != 0


def wait_health(base, timeout_s=25.0):
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


def resolve_ctx(url, anon, svc):
    from supabase import create_client
    anon_client = create_client(url, anon)
    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()
    admin = create_client(url, svc)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon_client.auth.verify_otp(
        {"token_hash": link.properties.hashed_token, "type": "magiclink"}
    )
    if not res.session:
        fail(f"could not authenticate {email}")
    return res


def main():
    base = os.environ.get("BASE_URL", f"http://127.0.0.1:{PORT}").rstrip("/")
    if not route_present(base):
        if port_free(PORT):
            proc = subprocess.Popen(
                [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app",
                 "--host", "127.0.0.1", "--port", str(PORT)],
                cwd=str(ROOT),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if not wait_health(base):
                proc.kill()
                fail(f"server did not start on {base}")
        else:
            fail(f"server not reachable at {base}/health")

    url = os.environ["SUPABASE_URL"]
    anon = os.environ["SUPABASE_ANON_KEY"]
    svc = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    sess = resolve_ctx(url, anon, svc)
    s = sess.session
    ref = urlparse(url).hostname.split(".")[0]
    storage_key = f"sb-{ref}-auth-token"
    storage_val = json.dumps({
        "access_token": s.access_token,
        "refresh_token": s.refresh_token,
        "expires_at": s.expires_at,
        "expires_in": s.expires_in,
        "token_type": s.token_type or "bearer",
        "user": json.loads(sess.user.model_dump_json()),
    })

    from playwright.sync_api import sync_playwright

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        console_errors = []
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
        page.add_init_script(
            f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
        )

        def load():
            page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function("()=>window.__rmAppShell && window.__rmAppShell.viewModel()", timeout=60000)
            page.evaluate(
                "()=>{const m=document.getElementById('guidedOnboardingModal');"
                "if(m){m.classList.remove('open');m.setAttribute('aria-hidden','true');m.remove();}}"
            )

        load()
        page.evaluate("()=>window.__rmAppShell.navigate('settings')")
        page.wait_for_selector(".settings-landing-grid", timeout=15000)
        nav_count = page.eval_on_selector_all(".settings-nav .settings-nav-item", "els=>els.length")
        results.append(("fe_settings_landing", nav_count == 7 and page.query_selector(".settings-landing-grid"),
                        f"nav_items={nav_count}"))


        labels = page.evaluate(
            """() => Array.from(document.querySelectorAll('.settings-nav-item'))
              .map(el => el.textContent.trim())"""
        )
        results.append(("fe_nav_labels",
                        labels == ["Account", "My Data", "Astrology", "Appearance",
                                   "Notifications", "Exports", "About"],
                        f"labels={labels}"))

        disp_label = page.eval_on_selector(
            ".settings-nav-item[data-settings-sub='display']", "el => el.textContent.trim()")
        data_label = page.eval_on_selector(
            ".settings-nav-item[data-settings-sub='data']", "el => el.textContent.trim()")
        results.append(("fe_label_display", disp_label == "Appearance", f"display={disp_label}"))
        results.append(("fe_label_data", data_label == "My Data", f"data={data_label}"))

        # Legacy URL aliases: appearance / my-data
        page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'appearance' })")
        page.wait_for_selector("#sec-display", timeout=15000)
        alias_app = page.evaluate("()=>window.__rmAppShell.navContext.settingsSubpage")
        results.append(("fe_legacy_appearance_alias", alias_app == "display", f"ctx={alias_app}"))
        page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'my-data' })")
        page.wait_for_selector("#sec-data-profiles", timeout=15000)
        alias_data = page.evaluate("()=>window.__rmAppShell.navContext.settingsSubpage")
        results.append(("fe_legacy_my_data_alias", alias_data == "data", f"ctx={alias_data}"))

        for sub, marker in CANONICAL_SUBPAGES:
            page.evaluate(
                "(sub)=>window.__rmAppShell.navigate('settings', { settingsSubpage: sub })",
                sub,
            )
            page.wait_for_selector("[data-settings-framework]", timeout=15000)
            page.wait_for_selector(marker, timeout=15000)
            active = page.eval_on_selector(
                f".settings-nav-item[data-settings-sub='{sub}']",
                "el=>el && el.classList.contains('active')",
            )
            hash_ok = page.evaluate(
                "(sub)=>location.hash.indexOf('/settings/' + sub) !== -1",
                sub,
            )
            results.append((f"fe_sub_{sub}", active and hash_ok, f"active={active} hash={hash_ok}"))

        # Legacy alias: charts -> astrology
        page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'charts' })")
        page.wait_for_selector("#rm-settings-minor-aspects", timeout=15000)
        alias_ctx = page.evaluate("()=>window.__rmAppShell.navContext.settingsSubpage")
        results.append(("fe_legacy_charts_alias", alias_ctx == "astrology", f"ctx={alias_ctx}"))

        # Nav click: notifications via sidebar
        page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'account' })")
        page.wait_for_selector("#sec-account-identity", timeout=15000)
        page.click(".settings-nav-item[data-settings-sub='notifications']")
        page.wait_for_selector("#sec-notifications", timeout=15000)
        results.append(("fe_nav_click_notifications", True, "sidebar navigation"))

        benign = [e for e in console_errors if "Failed to load resource" in e and "404" in e]
        bad = [e for e in console_errors if e not in benign]
        results.append(("fe_no_console_errors", not bad, repr(bad[:3]) if bad else "none"))

        # CHART-TRUTH-FIX-1/FIX-3: North Node and South Node controls must be disabled
        page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'astrology' })")
        page.wait_for_selector("#rm-settings-body-north_node", timeout=10000)
        nn_disabled = page.eval_on_selector("#rm-settings-body-north_node", "el=>el.disabled")
        sn_disabled = page.eval_on_selector("#rm-settings-body-south_node", "el=>el.disabled")
        nn_checked  = page.eval_on_selector("#rm-settings-body-north_node", "el=>el.checked")
        sn_checked  = page.eval_on_selector("#rm-settings-body-south_node", "el=>el.checked")
        results.append(("fe_nodes_disabled",
                        nn_disabled and sn_disabled,
                        f"north_node_disabled={nn_disabled} south_node_disabled={sn_disabled}"))
        results.append(("fe_nodes_unchecked",
                        not nn_checked and not sn_checked,
                        f"north_checked={nn_checked} south_checked={sn_checked}"))

        browser.close()

    overall = True
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
        overall = overall and ok
    print(f"{'PASS' if overall else 'FAIL'}: smoke_settings_navigation")
    if not overall:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
