#!/usr/bin/env python3
"""Smoke: saved investigation backend ownership (create/rename/archive).

Backend:
  * create, rename, archive, idempotent archive
  * cross-account, invalid profile, unauth

Frontend:
  * map save investigation + optional note
  * app_shell rename + archive (in-memory, no reload)
  * map replay after resume
  * no console errors

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_saved_investigations.py
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
        st, _ = fetch(base, "/saved-investigations/create", method="POST",
                      body={"profile_id": "x", "title": "t"}, timeout=3)
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


def cleanup_investigation(admin, search_id):
    if not search_id:
        return
    admin.table("notes").delete().eq("target_type", "saved_investigation").eq(
        "target_id", search_id,
    ).execute()
    admin.table("saved_searches").delete().eq("id", search_id).execute()


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
            fail(f"port {PORT} serving build without /saved-investigations/create")
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

        profiles = (
            admin.table("profiles").select("id")
            .eq("account_id", account_id).is_("archived_at", "null")
            .order("created_at").limit(1).execute()
        ).data or []
        if not profiles:
            fail("no active profile")
        profile_id = profiles[0]["id"]

        cond = {
            "schema_version": 1,
            "kind": "saved_investigation",
            "house_conditions": [],
            "angle_sign_conditions": [],
            "aspect_overlay": None,
        }
        viewport = {"center_lat": 40.7, "center_lon": -74.0, "zoom": 10}
        settings = {"snapshot_version": 1, "house_system": "placidus"}

        # create
        st, b = fetch(base, "/saved-investigations/create", headers=headers, method="POST",
                      body={"profile_id": profile_id, "title": f"Smoke Inv {stamp}",
                            "search_type": "map", "conditions_json": cond,
                            "viewport_json": viewport, "settings_snapshot_json": settings})
        created = json.loads(b) if st == 200 else {}
        sid = created.get("id")
        if sid:
            created_ids.append(sid)
        row = (
            admin.table("saved_searches").select("conditions_json, viewport_json, settings_snapshot_json")
            .eq("id", sid).single().execute()
        ).data if sid else {}
        results.append(("be_create",
                        st == 200 and created.get("status") == "created"
                        and row.get("conditions_json") == cond
                        and row.get("viewport_json") == viewport
                        and row.get("settings_snapshot_json") == settings,
                        f"status={st} id={sid}"))

        # rename
        new_title = f"Smoke Renamed {stamp}"
        st, b = fetch(base, "/saved-investigations/rename", headers=headers, method="POST",
                      body={"saved_search_id": sid, "title": new_title, "profile_id": profile_id})
        renamed = json.loads(b) if st == 200 else {}
        db_title = (
            admin.table("saved_searches").select("title, updated_at")
            .eq("id", sid).single().execute()
        ).data if sid else {}
        results.append(("be_rename",
                        st == 200 and renamed.get("status") == "renamed"
                        and renamed.get("title") == new_title
                        and db_title and db_title.get("title") == new_title,
                        f"status={st} title={renamed.get('title')}"))

        # archive
        st, b = fetch(base, "/saved-investigations/archive", headers=headers, method="POST",
                      body={"saved_search_id": sid, "profile_id": profile_id})
        archived = json.loads(b) if st == 200 else {}
        arch_db = (
            admin.table("saved_searches").select("archived_at")
            .eq("id", sid).single().execute()
        ).data if sid else {}
        results.append(("be_archive",
                        st == 200 and archived.get("status") == "archived"
                        and arch_db and arch_db.get("archived_at"),
                        f"status={st} archived_at={arch_db.get('archived_at') if arch_db else None}"))

        # already_archived
        st, b = fetch(base, "/saved-investigations/archive", headers=headers, method="POST",
                      body={"saved_search_id": sid})
        again = json.loads(b) if st == 200 else {}
        results.append(("be_already_archived",
                        st == 200 and again.get("status") == "already_archived",
                        f"status={st} stat={again.get('status')}"))

        # invalid profile
        st, _ = fetch(base, "/saved-investigations/create", headers=headers, method="POST",
                      body={"profile_id": str(uuid.uuid4()), "title": "x",
                            "conditions_json": cond})
        results.append(("be_invalid_profile_404", st == 404, f"status={st}"))

        # cross-account
        other = (
            admin.table("saved_searches").select("id")
            .neq("account_id", account_id).is_("archived_at", "null").limit(1).execute()
        ).data
        cross_id = None
        if other:
            cross_id = other[0]["id"]
        else:
            other_prof = (
                admin.table("profiles").select("id, account_id")
                .neq("account_id", account_id).is_("archived_at", "null").limit(1).execute()
            ).data
            if other_prof:
                cross_id = admin.table("saved_searches").insert({
                    "account_id": other_prof[0]["account_id"],
                    "profile_id": other_prof[0]["id"],
                    "title": f"Smoke Cross {stamp}", "search_type": "map",
                    "conditions_json": cond,
                }).execute().data[0]["id"]
                created_ids.append(cross_id)
        if cross_id:
            st, _ = fetch(base, "/saved-investigations/rename", headers=headers, method="POST",
                          body={"saved_search_id": cross_id, "title": "hack"})
            results.append(("be_cross_account_404", st == 404, f"status={st}"))
        else:
            results.append(("be_cross_account_404", True, "skipped"))

        # unauth
        st, _ = fetch(base, "/saved-investigations/create", method="POST",
                      body={"profile_id": profile_id, "title": "x"})
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

        fe_rename_title = f"Smoke FE Rename {stamp}"
        fe_archive_title = f"Smoke FE Archive {stamp}"
        fe_replay_title = f"Smoke FE Replay {stamp}"
        fe_note = f"smoke note {stamp}"

        # Seed two rows for shell rename/archive via backend (fresh shell load picks them up)
        fe_rename_id = None
        fe_archive_id = None
        fe_replay_id = None
        st, b = fetch(base, "/saved-investigations/create", headers=headers, method="POST",
                      body={"profile_id": profile_id, "title": fe_rename_title,
                            "conditions_json": cond, "viewport_json": viewport})
        if st == 200:
            fe_rename_id = json.loads(b).get("id")
            created_ids.append(fe_rename_id)
        st, b = fetch(base, "/saved-investigations/create", headers=headers, method="POST",
                      body={"profile_id": profile_id, "title": fe_archive_title,
                            "conditions_json": cond, "viewport_json": viewport})
        if st == 200:
            fe_archive_id = json.loads(b).get("id")
            created_ids.append(fe_archive_id)
        st, b = fetch(base, "/saved-investigations/create", headers=headers, method="POST",
                      body={"profile_id": profile_id, "title": fe_replay_title,
                            "conditions_json": cond, "viewport_json": viewport})
        if st == 200:
            fe_replay_id = json.loads(b).get("id")
            created_ids.append(fe_replay_id)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            console_errors = []
            load_count = {"n": 0}
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.on("load", lambda _f: load_count.__setitem__("n", load_count["n"] + 1))
            page.add_init_script(
                f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
            )

            # map save + note
            ids_before = {r["id"] for r in (
                admin.table("saved_searches").select("id").eq("account_id", account_id)
                .eq("profile_id", profile_id).execute()
            ).data}
            page.goto(f"{base}/map_CURRENT.html#profileId={profile_id}", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.__rmSaveCurrentInvestigation && !!window.CurrentUser",
                timeout=30000,
            )
            page.fill("#saveInvestigationNote", fe_note)
            page.evaluate("() => window.__rmSaveCurrentInvestigation()")
            page.wait_for_function(
                "() => { const e = document.getElementById('saveInvestigationStatus');"
                "return e && e.textContent.indexOf('(note attached)') !== -1; }",
                timeout=20000,
            )
            rows_after = (
                admin.table("saved_searches").select("id, conditions_json")
                .eq("account_id", account_id).eq("profile_id", profile_id).execute()
            ).data
            map_new = [r for r in rows_after if r["id"] not in ids_before]
            map_save_id = map_new[0]["id"] if len(map_new) == 1 else None
            if map_save_id:
                created_ids.append(map_save_id)
            note_ok = False
            if map_save_id:
                notes = (
                    admin.table("notes").select("body")
                    .eq("target_type", "saved_investigation").eq("target_id", map_save_id)
                    .is_("archived_at", "null").execute()
                ).data
                note_ok = bool(notes) and notes[0]["body"] == fe_note
            results.append(("fe_map_save", map_save_id is not None, f"id={map_save_id}"))
            results.append(("fe_map_save_note", note_ok, f"note_ok={note_ok}"))

            # app_shell rename + archive
            page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.__rmAppShell && typeof window.__rmAppShell.navigate === 'function'",
                timeout=30000,
            )
            page.evaluate("() => { const m = document.getElementById('guidedOnboardingModal'); if (m) m.remove(); }")
            page.wait_for_function(
                f"() => document.body.innerText.indexOf({json.dumps(fe_rename_title)}) !== -1",
                timeout=30000,
            )
            loads_before = load_count["n"]

            def dialog_handler(dialog):
                if dialog.type == "prompt":
                    dialog.accept(fe_rename_title + " OK")
                else:
                    dialog.accept()

            page.on("dialog", dialog_handler)
            page.click(f"[data-action='rename-exploration'][data-exploration='{fe_rename_id}']")
            page.wait_for_function(
                f"() => document.body.innerText.indexOf({json.dumps(fe_rename_title + ' OK')}) !== -1",
                timeout=15000,
            )
            renamed_db = (
                admin.table("saved_searches").select("title")
                .eq("id", fe_rename_id).single().execute()
            ).data if fe_rename_id else {}
            results.append(("fe_rename",
                            renamed_db and renamed_db.get("title") == fe_rename_title + " OK",
                            f"title={renamed_db.get('title') if renamed_db else None}"))

            page.click(f"[data-action='archive-exploration'][data-exploration='{fe_archive_id}']")
            page.wait_for_function(
                f"() => document.body.innerText.indexOf({json.dumps(fe_archive_title)}) === -1",
                timeout=15000,
            )
            arch_row = (
                admin.table("saved_searches").select("archived_at")
                .eq("id", fe_archive_id).single().execute()
            ).data if fe_archive_id else {}
            mem_gone = page.evaluate(
                f"() => {{ const r = window.__rmAppShell.storeRaw();"
                f"return !(r && r.saved_investigations && r.saved_investigations.some(s => s.id === {json.dumps(fe_archive_id)})); }}"
            )
            results.append(("fe_archive",
                            arch_row and arch_row.get("archived_at") and mem_gone,
                            f"archived={bool(arch_row and arch_row.get('archived_at'))} mem={mem_gone}"))
            results.append(("fe_no_reload",
                            load_count["n"] == loads_before,
                            f"loads={load_count['n']} before={loads_before}"))

            # replay via resume
            page.click(
                f"[data-action='resume-exploration'][data-exploration='{fe_replay_id}']"
            )
            page.wait_for_url("**/map_CURRENT.html**", timeout=20000)
            page.wait_for_function(
                "() => { const e = document.getElementById('reopenInvestigationStatus');"
                "return e && e.textContent.indexOf('Reopened:') !== -1; }",
                timeout=30000,
            )
            replay_status = page.eval_on_selector("#reopenInvestigationStatus", "el => el.textContent")
            results.append(("fe_replay",
                            replay_status and "Reopened:" in replay_status,
                            f"status={replay_status}"))

            app_errors = [e for e in console_errors
                          if "Failed to load resource" not in e and "net::ERR" not in e]
            results.append(("fe_no_console_errors", len(app_errors) == 0,
                            "; ".join(app_errors[:5]) or "none"))
            browser.close()

    finally:
        for sid in set(created_ids):
            cleanup_investigation(admin, sid)
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
    print("PASS: smoke_saved_investigations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
