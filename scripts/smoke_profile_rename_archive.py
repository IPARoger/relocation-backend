#!/usr/bin/env python3
"""Smoke: profile rename/archive backend ownership.

Backend:
  * rename, archive, only_profile_remaining, cross-account, unauth

Frontend (app_shell Profile Management):
  * rename updates UI/store
  * archive removes profile
  * default repoint on archiving default profile
  * no reload, no console errors

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_profile_rename_archive.py
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
import uuid
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PYTHON = ROOT / "venv" / "bin" / "python"
DEFAULT_EMAIL = "davidleongoodman@gmail.com"
PORT = 8004


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
        st, _ = fetch(base, "/profiles/rename", method="POST",
                      body={"profile_id": "x", "display_name": "y"}, timeout=3)
    except Exception:
        return None
    return st == 401


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
    token = res.session.access_token
    anon_client.postgrest.auth(token)
    account_ids = anon_client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        fail("no account for smoke user")
    return token, account_ids[0], res


def create_throwaway_profile(admin, account_id, account_user_id, stamp, suffix):
    prof = admin.table("profiles").insert({
        "account_id": account_id,
        "account_user_id": account_user_id,
        "display_name": f"Smoke Prof {stamp} {suffix}",
        "profile_type": "human",
    }).execute().data[0]
    admin.table("birth_records").insert({
        "account_id": account_id,
        "profile_id": prof["id"],
        "birth_date": "1990-01-01",
        "birth_time_mode": "unknown",
        "birth_place_id": None,
    }).execute()
    return prof["id"]


def cleanup_profile(admin, profile_id):
    if not profile_id:
        return
    admin.table("birth_records").delete().eq("profile_id", profile_id).execute()
    admin.table("profiles").delete().eq("id", profile_id).execute()


def main() -> int:
    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon_key, service_key]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY")

    from supabase import create_client
    admin = create_client(url, service_key)

    base = f"http://127.0.0.1:{PORT}"
    proc = None
    present = route_present(base)
    if present is not True:
        if present is False:
            fail(f"port {PORT} serving build without /profiles/rename")
        if not port_free(PORT):
            fail(f"port {PORT} occupied but route missing")
        proc = subprocess.Popen(
            [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app",
             "--host", "127.0.0.1", "--port", str(PORT)],
            cwd=str(ROOT), env=dict(os.environ),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if not wait_health(base):
            proc.terminate()
            fail(f"temp server did not start on {base}")

    results = []
    created_ids = []
    stamp = uuid.uuid4().hex[:8]
    try:
        jwt, account_id, sess = resolve_ctx(url, anon_key, service_key)
        headers = {"Authorization": f"Bearer {jwt}"}

        user_id = sess.user.id
        active = (
            admin.table("profiles").select("id, display_name")
            .eq("account_id", account_id).is_("archived_at", "null")
            .order("created_at").execute()
        ).data or []
        if len(active) < 2:
            for suffix in ("A", "B"):
                if len(active) + len(created_ids) >= 2:
                    break
                pid = create_throwaway_profile(admin, account_id, user_id, stamp, suffix)
                created_ids.append(pid)
            active = (
                admin.table("profiles").select("id, display_name")
                .eq("account_id", account_id).is_("archived_at", "null")
                .order("created_at").execute()
            ).data or []
        if len(active) < 2:
            fail("need at least two active profiles")

        rename_pid = active[0]["id"]
        archive_pid = active[1]["id"]
        renamed_title = f"Smoke Renamed {stamp}"

        st, b = fetch(base, "/profiles/rename", headers=headers, method="POST",
                      body={"profile_id": rename_pid, "display_name": renamed_title})
        renamed = json.loads(b) if st == 200 else {}
        db_name = (
            admin.table("profiles").select("display_name")
            .eq("id", rename_pid).single().execute()
        ).data if rename_pid else {}
        results.append(("be_rename",
                        st == 200 and renamed.get("status") == "renamed"
                        and db_name and db_name.get("display_name") == renamed_title,
                        f"status={st} name={db_name.get('display_name') if db_name else None}"))

        st, b = fetch(base, "/profiles/archive", headers=headers, method="POST",
                      body={"profile_id": archive_pid})
        archived = json.loads(b) if st == 200 else {}
        arch_db = (
            admin.table("profiles").select("archived_at")
            .eq("id", archive_pid).single().execute()
        ).data if archive_pid else {}
        results.append(("be_archive",
                        st == 200 and archived.get("status") == "archived"
                        and arch_db and arch_db.get("archived_at"),
                        f"status={st} archived={bool(arch_db and arch_db.get('archived_at'))}"))

        # restore archived for later frontend test — unarchive via admin
        admin.table("profiles").update({"archived_at": None}).eq("id", archive_pid).execute()

        # only profile remaining — use a temp single-profile account slice: archive all but one then try
        only_pid = active[0]["id"]
        for p in active[1:]:
            if p["id"] == only_pid:
                continue
            admin.table("profiles").update({
                "archived_at": "2020-01-01T00:00:00+00:00",
            }).eq("id", p["id"]).execute()
        st, b = fetch(base, "/profiles/archive", headers=headers, method="POST",
                      body={"profile_id": only_pid})
        detail = json.loads(b).get("detail", {}) if st == 422 else {}
        results.append(("be_only_profile_422",
                        st == 422 and detail.get("error") == "only_profile_remaining",
                        f"status={st} err={detail.get('error')}"))
        # restore archived profiles for frontend
        for p in active[1:]:
            admin.table("profiles").update({"archived_at": None}).eq("id", p["id"]).execute()

        other = (
            admin.table("profiles").select("id")
            .neq("account_id", account_id).is_("archived_at", "null").limit(1).execute()
        ).data
        if other:
            st, _ = fetch(base, "/profiles/rename", headers=headers, method="POST",
                          body={"profile_id": other[0]["id"], "display_name": "hack"})
            results.append(("be_cross_account_404", st == 404, f"status={st}"))
        else:
            results.append(("be_cross_account_404", True, "skipped"))

        st, _ = fetch(base, "/profiles/rename", method="POST",
                      body={"profile_id": rename_pid, "display_name": "x"})
        results.append(("be_unauth_401", st == 401, f"status={st}"))

        # ================= FRONTEND =================
        from playwright.sync_api import sync_playwright
        s = sess.session
        ref = urlparse(url).hostname.split(".")[0]
        storage_key = f"sb-{ref}-auth-token"
        storage_val = json.dumps({
            "access_token": s.access_token, "refresh_token": s.refresh_token,
            "expires_at": s.expires_at, "expires_in": s.expires_in,
            "token_type": s.token_type or "bearer",
            "user": json.loads(sess.user.model_dump_json()),
        })

        fe_rename_pid = create_throwaway_profile(admin, account_id, user_id, stamp, "FE-R")
        fe_archive_pid = create_throwaway_profile(admin, account_id, user_id, stamp, "FE-A")
        created_ids.extend([fe_rename_pid, fe_archive_pid])
        fe_rename_label = f"Smoke FE Rename {stamp}"
        fe_archive_label = f"Smoke Prof {stamp} FE-A"

        # Set default to archive target for repoint test
        st, _ = fetch(base, "/settings/account", headers=headers, method="PATCH",
                      body={"settings_patch": {"default_chart_record_id": fe_archive_pid}})

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            console_errors = []
            load_count = {"n": 0}
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.on("load", lambda _f: load_count.__setitem__("n", load_count["n"] + 1))
            def handle_dialog(dialog):
                if dialog.type == "prompt":
                    dialog.accept(fe_rename_label)
                else:
                    dialog.accept()
            page.on("dialog", handle_dialog)

            page.add_init_script(
                f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
            )
            page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.__rmAppShell && typeof window.__rmAppShell.navigate === 'function'",
                timeout=30000,
            )
            page.evaluate(
                "() => { const m = document.getElementById('guidedOnboardingModal'); if (m) m.remove(); }"
            )
            page.evaluate("() => window.__rmAppShell.navigate('profiles')")
            page.wait_for_selector("h2:has-text('Profile Management')", timeout=20000)
            page.wait_for_function(
                f"() => document.body.innerText.indexOf({json.dumps(fe_rename_label.split()[0] + ' Prof')}) !== -1 || "
                f"document.body.innerText.indexOf('Smoke Prof') !== -1",
                timeout=20000,
            )

            loads_before = load_count["n"]
            page.click(f"[data-action='pm-rename-profile'][data-chart-record='{fe_rename_pid}']")
            page.wait_for_function(
                f"() => document.body.innerText.indexOf({json.dumps(fe_rename_label)}) !== -1",
                timeout=15000,
            )
            mem_rename = page.evaluate(
                f"(pid) => {{ const r = window.__rmAppShell.storeRaw();"
                f"const c = r && r.clients && r.clients.find(x => x.id === pid);"
                f"return c && c.display_name; }}",
                fe_rename_pid,
            )
            results.append(("fe_rename_ui",
                            mem_rename == fe_rename_label,
                            f"mem={mem_rename}"))

            page.click(f"[data-action='pm-archive-profile'][data-chart-record='{fe_archive_pid}']")
            page.wait_for_function(
                f"() => document.body.innerText.indexOf({json.dumps(fe_archive_label)}) === -1",
                timeout=20000,
            )
            mem_gone = page.evaluate(
                f"(pid) => {{ const r = window.__rmAppShell.storeRaw();"
                f"return !(r && r.clients && r.clients.some(c => c.id === pid)); }}",
                fe_archive_pid,
            )
            default_id = page.evaluate("() => window.__rmAppShell.viewModel().defaultChartRecordId")
            settings_default = (
                admin.table("user_settings").select("settings_json")
                .eq("account_id", account_id).is_("profile_id", "null").limit(1).execute()
            ).data
            db_default = None
            if settings_default:
                db_default = (settings_default[0].get("settings_json") or {}).get("default_chart_record_id")
            results.append(("fe_archive_removed", mem_gone, f"mem_gone={mem_gone}"))
            results.append(("fe_default_repoint",
                            default_id != fe_archive_pid and db_default != fe_archive_pid
                            and default_id == db_default,
                            f"vm={default_id} db={db_default} archived={fe_archive_pid}"))
            results.append(("fe_no_reload",
                            load_count["n"] == loads_before,
                            f"loads={load_count['n']} before={loads_before}"))

            app_errors = [e for e in console_errors
                          if "Failed to load resource" not in e and "net::ERR" not in e]
            results.append(("fe_no_console_errors", len(app_errors) == 0,
                            "; ".join(app_errors[:5]) or "none"))
            browser.close()

    finally:
        for pid in set(created_ids):
            cleanup_profile(admin, pid)
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
    print("PASS: smoke_profile_rename_archive")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
