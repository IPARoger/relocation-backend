#!/usr/bin/env python3
"""Frontend smoke: app_shell.html note saves -> backend note endpoints.

Drives the real chart-record notepad and comparison notepad and verifies:
  * chart note save shows "Saved." and persists across a full reload
  * comparison note save shows "Saved." and persists across a full reload
  * exactly one active note row per target (backend-owned upsert)
  * no console errors

Auth: admin magic-link OTP for RM_SMOKE_EMAIL (default davidleongoodman@gmail.com),
session injected into localStorage. Creates a temporary comparison set if the
account has none; restores all created data afterwards.

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_notes_frontend.py
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
PYTHON = ROOT / "venv" / "bin" / "python"
DEFAULT_EMAIL = "davidleongoodman@gmail.com"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def notes_route_present(base):
    data = json.dumps({"profile_id": "x"}).encode()
    req = urllib.request.Request(base + "/notes/chart-record", data=data,
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        urllib.request.urlopen(req, timeout=3)
        return False
    except urllib.error.HTTPError as err:
        return err.code == 401
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


def main() -> int:
    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon_key, service_key]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY")
    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()

    from supabase import create_client
    from playwright.sync_api import sync_playwright

    admin = create_client(url, service_key)
    anon = create_client(url, anon_key)

    proc = None
    base = "http://127.0.0.1:8004"
    if not notes_route_present(base):
        port = 8025 if port_free(8025) else 8026
        proc = subprocess.Popen(
            [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app",
             "--host", "127.0.0.1", "--port", str(port)],
            cwd=str(ROOT), env=dict(os.environ),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        base = f"http://127.0.0.1:{port}"
        if not wait_health(base):
            proc.terminate()
            fail(f"temp server did not start on {base}")

    # Auth + session injection.
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon.auth.verify_otp({"token_hash": link.properties.hashed_token, "type": "magiclink"})
    s = res.session
    if not s:
        fail(f"could not authenticate {email}")
    ref = urlparse(url).hostname.split(".")[0]
    storage_key = f"sb-{ref}-auth-token"
    storage_val = json.dumps({
        "access_token": s.access_token, "refresh_token": s.refresh_token,
        "expires_at": s.expires_at, "expires_in": s.expires_in,
        "token_type": s.token_type or "bearer",
        "user": json.loads(res.user.model_dump_json()),
    })

    anon.postgrest.auth(s.access_token)
    account_id = (anon.rpc("app_account_ids").execute().data or [None])[0]
    if not account_id:
        fail("no account for smoke user")

    profiles = (
        admin.table("profiles").select("id").eq("account_id", account_id)
        .is_("archived_at", "null").order("created_at", desc=False).limit(1).execute()
    ).data
    if not profiles:
        fail("no profile for smoke account")
    profile_id = profiles[0]["id"]

    cs = (
        admin.table("comparison_sets").select("id").eq("account_id", account_id)
        .is_("archived_at", "null").limit(1).execute()
    ).data
    created_cs_id = None
    if cs:
        comparison_set_id = cs[0]["id"]
    else:
        comparison_set_id = admin.table("comparison_sets").insert({
            "account_id": account_id, "profile_id": profile_id, "title": "smoke notes set",
        }).execute().data[0]["id"]
        created_cs_id = comparison_set_id

    stamp = str(int(time.time()))
    chart_text = f"chart note {stamp}"
    cmp_text = f"cmp note {stamp}"
    results = []

    try:
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
                page.wait_for_function(
                    "() => !!window.CurrentUser && !!window.CurrentUser.accountId "
                    "&& !!window.__rmAppShell && typeof window.__rmAppShell.navigate === 'function'",
                    timeout=30000,
                )
                # Dismiss the guided onboarding modal so it cannot intercept clicks.
                page.evaluate(
                    "()=>{const m=document.getElementById('guidedOnboardingModal');"
                    "if(m){m.classList.remove('open');m.setAttribute('aria-hidden','true');m.remove();}}"
                )

            # --- Chart note ---
            load()
            page.evaluate("(pid)=>window.__rmAppShell.navigate('chart-record',{chartRecordId:pid})", profile_id)
            page.wait_for_selector("#rm-chart-note", timeout=15000)
            page.fill("#rm-chart-note", chart_text)
            page.click("[data-action='save-chart-note']")
            page.wait_for_function(
                "()=>{const m=document.getElementById('rm-chart-note-msg');return m&&m.textContent.trim()==='Saved.';}",
                timeout=15000,
            )
            results.append(("chart_save_saved_msg", True, "Saved."))

            # Reload persistence.
            load()
            page.evaluate("(pid)=>window.__rmAppShell.navigate('chart-record',{chartRecordId:pid})", profile_id)
            page.wait_for_selector("#rm-chart-note", timeout=15000)
            val = page.eval_on_selector("#rm-chart-note", "el=>el.value")
            results.append(("chart_reload_persist", val == chart_text, f"value={val!r}"))

            # --- Comparison note ---
            page.evaluate(
                "(a)=>window.__rmAppShell.navigate('compare',{chartRecordId:a.pid,comparisonSetId:a.cid})",
                {"pid": profile_id, "cid": comparison_set_id},
            )
            page.wait_for_selector("#rm-cmp-note", timeout=15000)
            page.fill("#rm-cmp-note", cmp_text)
            page.click("[data-action='save-comparison-note']")
            page.wait_for_function(
                "()=>{const m=document.getElementById('rm-cmp-note-msg');return m&&m.textContent.trim()==='Saved.';}",
                timeout=15000,
            )
            results.append(("cmp_save_saved_msg", True, "Saved."))

            # Reload persistence.
            load()
            page.evaluate(
                "(a)=>window.__rmAppShell.navigate('compare',{chartRecordId:a.pid,comparisonSetId:a.cid})",
                {"pid": profile_id, "cid": comparison_set_id},
            )
            page.wait_for_selector("#rm-cmp-note", timeout=15000)
            cval = page.eval_on_selector("#rm-cmp-note", "el=>el.value")
            results.append(("cmp_reload_persist", cval == cmp_text, f"value={cval!r}"))

            results.append(("no_console_errors", len(console_errors) == 0,
                            "; ".join(console_errors[:5]) or "none"))
            browser.close()

        # DB: one active row each, correct bodies.
        chart_rows = (
            admin.table("notes").select("id, body").eq("account_id", account_id)
            .eq("profile_id", profile_id).eq("target_type", "chart_record")
            .is_("archived_at", "null").execute()
        ).data
        results.append(("chart_single_active_row", len(chart_rows) == 1, f"count={len(chart_rows)}"))
        results.append(("chart_db_body", bool(chart_rows) and chart_rows[0]["body"] == chart_text,
                        f"body={chart_rows[0]['body'] if chart_rows else None!r}"))

        cmp_rows = (
            admin.table("notes").select("id, body").eq("account_id", account_id)
            .eq("target_type", "comparison_set").eq("target_id", comparison_set_id)
            .is_("archived_at", "null").execute()
        ).data
        results.append(("cmp_single_active_row", len(cmp_rows) == 1, f"count={len(cmp_rows)}"))
        results.append(("cmp_db_body", bool(cmp_rows) and cmp_rows[0]["body"] == cmp_text,
                        f"body={cmp_rows[0]['body'] if cmp_rows else None!r}"))

    finally:
        admin.table("notes").delete().eq("account_id", account_id) \
            .eq("profile_id", profile_id).eq("target_type", "chart_record").execute()
        admin.table("notes").delete().eq("account_id", account_id) \
            .eq("target_type", "comparison_set").eq("target_id", comparison_set_id).execute()
        if created_cs_id:
            admin.table("comparison_sets").delete().eq("id", created_cs_id).execute()
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()

    failed = [n for n, ok, _ in results if not ok]
    for n, ok, d in results:
        print(f"{'PASS' if ok else 'FAIL'}: {n} — {d}")
    if failed:
        fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")
    print("PASS: smoke_notes_frontend")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
