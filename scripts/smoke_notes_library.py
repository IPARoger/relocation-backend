#!/usr/bin/env python3
"""Smoke: Notes Library v1 (W2-NOTES-1)."""

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
PYTHON = ROOT / "venv" / "bin" / "python"
DEFAULT_EMAIL = "davidleongoodman@gmail.com"
PORT = 8004


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def route_present(base):
    try:
        with urllib.request.urlopen(base + "/health", timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


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
    from supabase import create_client
    admin = create_client(url, svc)
    anon_client = create_client(url, anon)
    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon_client.auth.verify_otp({"token_hash": link.properties.hashed_token, "type": "magiclink"})
    s = res.session
    if not s:
        fail(f"could not authenticate {email}")
    ref = urlparse(url).hostname.split(".")[0]
    storage_key = f"sb-{ref}-auth-token"
    storage_val = json.dumps({
        "access_token": s.access_token,
        "refresh_token": s.refresh_token,
        "expires_at": s.expires_at,
        "expires_in": s.expires_in,
        "token_type": s.token_type or "bearer",
        "user": json.loads(res.user.model_dump_json()),
    })

    from playwright.sync_api import sync_playwright

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
        page.add_init_script(
            f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
        )

        page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
        page.wait_for_function("()=>window.__rmAppShell && window.__rmAppShell.viewModel()", timeout=60000)
        page.evaluate(
            "()=>{const m=document.getElementById('guidedOnboardingModal');"
            "if(m){m.classList.remove('open');m.setAttribute('aria-hidden','true');m.remove();}}"
        )

        profile_id = page.evaluate("()=>window.__rmAppShell.viewModel().defaultChartRecordId")

        page.evaluate(
            "(pid)=>window.__rmAppShell.navigate('notes-library',{chartRecordId:pid})",
            profile_id,
        )
        page.wait_for_selector("[data-notes-library]", timeout=15000)
        layout = page.query_selector(".notes-library-layout")
        collections = page.eval_on_selector_all(".notes-lib-cat", "els=>els.length")
        search = page.query_selector("#rm-notes-search")
        editor_host = page.query_selector("#rm-notes-editor")
        hash_ok = page.evaluate("()=>location.hash.indexOf('/notes-library')!==-1")
        results.append(("fe_layout", layout is not None and collections == 7, f"collections={collections}"))
        results.append(("fe_search", search is not None, "search input"))
        results.append(("fe_editor_host", editor_host is not None, "editor panel"))
        results.append(("fe_hash", hash_ok, f"hash={page.evaluate('()=>location.hash')}"))
        results.append(("fe_no_scratchpad", page.query_selector("[data-action='new-general-note']") is None, "no scratchpad btn"))

        page.click(".notes-lib-cat[data-collection='map_notes']")
        page.wait_for_selector("text=Not wired yet", timeout=10000)
        results.append(("fe_unwired_placeholder", True, "map notes"))

        page.evaluate("(pid)=>window.__rmAppShell.navigate('chart-record',{chartRecordId:pid})", profile_id)
        page.wait_for_selector("#rm-chart-note", timeout=15000)
        results.append(("fe_chart_note_preserved", True, "chart-record note module"))

        bad = [e for e in errors if not ("Failed to load resource" in e and "404" in e)]
        results.append(("fe_no_console_errors", not bad, repr(bad[:2]) if bad else "none"))
        browser.close()

    ok = True
    for name, passed, detail in results:
        print(f"{'PASS' if passed else 'FAIL'}: {name} — {detail}")
        ok = ok and passed
    print(f"{'PASS' if ok else 'FAIL'}: smoke_notes_library")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
