#!/usr/bin/env python3
"""Frontend smoke: current_location_editor.js -> POST /current-location/set.

Drives the real "Set Current Location" overlay in app_shell.html and verifies:
  * set current location via the editor UI
  * DB current row changes to the chosen place
  * exactly one is_current=true row remains
  * shell label (Current city) updates in place
  * no full page reload occurred
  * no console errors
  * original current location restored afterwards

Auth: admin magic-link OTP for RM_SMOKE_EMAIL (default davidleongoodman@gmail.com),
session injected into localStorage (same pattern as existing shell QA scripts).

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_current_location_frontend.py
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


def route_present(base: str) -> bool:
    try:
        urllib.request.urlopen(base + "/current-location/current?profile_id=x", timeout=3)
        return True
    except urllib.error.HTTPError as err:
        return err.code != 404
    except Exception:
        return False


def port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def wait_health(base: str, timeout_s: float = 25.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base + "/health", timeout=2) as resp:
                if resp.status == 200:
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

    proc = None
    base = "http://127.0.0.1:8004"
    if not route_present(base):
        port = 8021
        if not port_free(port):
            port = 8022
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

    admin = create_client(url, service_key)
    anon = create_client(url, anon_key)

    # Auth via admin magic-link OTP.
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    hashed = link.properties.hashed_token
    res = anon.auth.verify_otp({"token_hash": hashed, "type": "magiclink"})
    s = res.session
    if not s:
        fail(f"could not authenticate {email}")
    ref = urlparse(url).hostname.split(".")[0]
    storage_key = f"sb-{ref}-auth-token"
    session_obj = {
        "access_token": s.access_token,
        "refresh_token": s.refresh_token,
        "expires_at": s.expires_at,
        "expires_in": s.expires_in,
        "token_type": s.token_type or "bearer",
        "user": json.loads(res.user.model_dump_json()),
    }
    storage_val = json.dumps(session_obj)

    anon.postgrest.auth(s.access_token)
    account_ids = anon.rpc("app_account_ids").execute().data or []
    if not account_ids:
        fail("no account for smoke user")
    account_id = account_ids[0]

    profiles = (
        admin.table("profiles").select("id")
        .eq("account_id", account_id).is_("archived_at", "null")
        .order("created_at", desc=False).limit(1).execute()
    ).data
    if not profiles:
        fail("no profile for smoke account")
    profile_id = profiles[0]["id"]

    original = (
        admin.table("current_location_history")
        .select("place_id").eq("account_id", account_id).eq("profile_id", profile_id)
        .eq("is_current", True).order("selected_at", desc=True).limit(1).execute()
    ).data
    original_place_id = original[0]["place_id"] if original else None

    places = admin.table("places").select("id, display_name").limit(25).execute().data
    test = next((p for p in places if p["id"] != original_place_id), None)
    if not test:
        fail("no test place available")
    test_place_id = test["id"]
    test_name = test["display_name"]

    results: list[tuple[str, bool, str]] = []
    try:
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
            page.wait_for_function(
                "() => !!window.CurrentUser && !!window.CurrentUser.accountId", timeout=30000
            )
            page.evaluate("(pid)=>{location.hash='#/chart-record?chartRecordId='+pid;}", profile_id)
            page.wait_for_timeout(1500)

            # Reload sentinel: cleared if the page does a full reload.
            page.evaluate("()=>{window.__rm_smoke_marker='alive';}")

            # Open the real editor overlay and perform a UI search + select + save.
            page.evaluate("(pid)=>window.__showCurrentLocationEditor(pid)", profile_id)
            page.wait_for_selector("#rm-cl-place-input", timeout=10000)
            page.fill("#rm-cl-place-input", "")
            page.locator("#rm-cl-place-input").press_sequentially(test_name, delay=20)
            # Wait for the matching result then click it.
            page.wait_for_function(
                """(name)=>{
                    const els=[...document.querySelectorAll('#rm-cl-place-results .place-result')];
                    return els.some(e=>e.textContent.trim()===name);
                }""",
                arg=test_name, timeout=10000,
            )
            page.evaluate(
                """(name)=>{
                    const els=[...document.querySelectorAll('#rm-cl-place-results .place-result')];
                    const el=els.find(e=>e.textContent.trim()===name);
                    el.click();
                }""",
                test_name,
            )
            page.click("#rm-cl-submit")

            # Wait for overlay to close (success path).
            page.wait_for_function(
                "()=>!document.getElementById('rm-current-location-editor')", timeout=15000
            )

            # Shell label update is applied on the next in-place render; poll for it.
            label_ok = False
            try:
                page.wait_for_function(
                    "(name)=>document.body && document.body.innerText.includes(name)",
                    arg=test_name, timeout=8000,
                )
                label_ok = True
            except Exception:
                pass
            results.append(("shell_label_updated", label_ok, f"'{test_name}' in shell"))

            marker = page.evaluate("()=>window.__rm_smoke_marker")
            no_reload = marker == "alive"
            results.append(("no_reload", no_reload, f"marker={marker!r}"))

            results.append(("no_console_errors", len(console_errors) == 0,
                            "; ".join(console_errors[:5]) or "none"))

            browser.close()

        # DB checks (service-role).
        current_rows = (
            admin.table("current_location_history")
            .select("id, place_id").eq("account_id", account_id).eq("profile_id", profile_id)
            .eq("is_current", True).execute()
        ).data
        results.append(("single_current_row", len(current_rows) == 1, f"count={len(current_rows)}"))
        changed = len(current_rows) == 1 and current_rows[0]["place_id"] == test_place_id
        results.append(("db_row_changed", changed,
                        f"place_id={current_rows[0]['place_id'] if current_rows else None}"))

    finally:
        # Restore original current location (net-zero).
        admin.table("current_location_history").update({"is_current": False}) \
            .eq("account_id", account_id).eq("profile_id", profile_id) \
            .eq("is_current", True).execute()
        if original_place_id is not None:
            admin.table("current_location_history").insert({
                "account_id": account_id, "profile_id": profile_id,
                "place_id": original_place_id, "is_current": True, "source": "manual",
            }).execute()
        admin.table("current_location_history").delete() \
            .eq("account_id", account_id).eq("profile_id", profile_id) \
            .eq("place_id", test_place_id).eq("is_current", False).execute()
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
    print("PASS: smoke_current_location_frontend")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
