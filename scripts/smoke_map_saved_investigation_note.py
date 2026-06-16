#!/usr/bin/env python3
"""Smoke: map saved-investigation note (backend + frontend).

Backend (POST /notes/saved-investigation):
  * authenticated save returns 200 with the note payload
  * a second save updates the SAME row (no duplicate active note)
  * cross-account saved_search is rejected (404)
  * unauthenticated request returns 401

Frontend (map_CURRENT.html):
  * Save Investigation with note text creates a saved_searches row AND a
    saved_investigation note row (body matches), shows "(note attached)"
  * saved_searches row keeps replay data intact (search_type='map',
    conditions_json.kind='saved_investigation') and round-trips via
    GET /saved-search/{id} (no search/replay regression)
  * no console errors

Auth: RM_SMOKE_JWT, else admin magic-link OTP for RM_SMOKE_EMAIL
(default davidleongoodman@gmail.com). Requires SUPABASE_* env.
Restores all rows it creates.

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_map_saved_investigation_note.py
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
    # New POST route requires auth -> 401 when present; 404/405 means stale/missing.
    st, _ = fetch(base, "/notes/saved-investigation", method="POST",
                  body={"saved_search_id": "x"})
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


def resolve_jwt_ctx(url, anon, svc):
    from supabase import create_client
    anon_client = create_client(url, anon)
    token = os.environ.get("RM_SMOKE_JWT", "").strip()
    sess = None
    if not token:
        email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()
        admin = create_client(url, svc)
        link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
        res = anon_client.auth.verify_otp(
            {"token_hash": link.properties.hashed_token, "type": "magiclink"}
        )
        if not res.session:
            fail(f"could not authenticate {email}")
        token = res.session.access_token
        sess = res
    anon_client.postgrest.auth(token)
    account_ids = anon_client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        fail("no account for smoke user")
    return token, account_ids[0], sess


def main() -> int:
    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon_key, service_key]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY")

    from supabase import create_client
    admin = create_client(url, service_key)

    base = "http://127.0.0.1:8004"
    proc = None
    if not route_present(base):
        port = next((p for p in (8031, 8032, 8033) if port_free(p)), 8031)
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

    results = []
    account_id = None
    profile_id = None
    be_search_id = None
    cross_search_id = None
    created_cross = False
    fe_search_ids = []
    saved_session = None
    try:
        jwt, account_id, saved_session = resolve_jwt_ctx(url, anon_key, service_key)
        headers = {"Authorization": f"Bearer {jwt}"}

        profiles = (
            admin.table("profiles").select("id").eq("account_id", account_id)
            .is_("archived_at", "null").order("created_at", desc=False).limit(1).execute()
        ).data
        if not profiles:
            fail("no profile for smoke account")
        profile_id = profiles[0]["id"]

        # ---- Backend: create an owned saved_search to attach a note to ----
        be_search_id = admin.table("saved_searches").insert({
            "account_id": account_id, "profile_id": profile_id,
            "title": "smoke saved-investigation (backend)", "search_type": "map",
            "conditions_json": {"schema_version": 1, "kind": "saved_investigation"},
        }).execute().data[0]["id"]

        st, b = fetch(base, "/notes/saved-investigation", headers=headers, method="POST",
                      body={"saved_search_id": be_search_id, "body": "investigation note v1"})
        ok = st == 200
        results.append(("be_save_200", ok, f"status={st}"))
        if not ok:
            fail(f"backend save returned {st}: {b[:300]!r}")
        first = json.loads(b)
        first_id = first.get("id")
        results.append(("be_target_type", first.get("target_type") == "saved_investigation",
                        f"target_type={first.get('target_type')}"))
        results.append(("be_target_id", first.get("target_id") == be_search_id,
                        f"target_id={first.get('target_id')}"))
        results.append(("be_profile_from_search", first.get("profile_id") == profile_id,
                        f"profile_id={first.get('profile_id')}"))

        st, b = fetch(base, "/notes/saved-investigation", headers=headers, method="POST",
                      body={"saved_search_id": be_search_id, "body": "investigation note v2"})
        second = json.loads(b)
        results.append(("be_update_same_row", st == 200 and second.get("id") == first_id,
                        f"id1={first_id} id2={second.get('id')}"))
        results.append(("be_body_updated", second.get("body") == "investigation note v2",
                        f"body={second.get('body')!r}"))
        active = (
            admin.table("notes").select("id").eq("account_id", account_id)
            .eq("target_type", "saved_investigation").eq("target_id", be_search_id)
            .is_("archived_at", "null").execute()
        ).data
        results.append(("be_single_active_row", len(active) == 1, f"count={len(active)}"))

        # ---- Cross-account rejection ----
        other = (
            admin.table("saved_searches").select("id, account_id")
            .neq("account_id", account_id).is_("archived_at", "null").limit(1).execute()
        ).data
        if other:
            cross_search_id = other[0]["id"]
        else:
            other_profile = (
                admin.table("profiles").select("id, account_id")
                .neq("account_id", account_id).is_("archived_at", "null").limit(1).execute()
            ).data
            if other_profile:
                cross_search_id = admin.table("saved_searches").insert({
                    "account_id": other_profile[0]["account_id"],
                    "profile_id": other_profile[0]["id"],
                    "title": "smoke cross-account", "search_type": "map",
                }).execute().data[0]["id"]
                created_cross = True
        if cross_search_id:
            st, _ = fetch(base, "/notes/saved-investigation", headers=headers, method="POST",
                          body={"saved_search_id": cross_search_id, "body": "x"})
            results.append(("be_cross_account_404", st == 404, f"status={st}"))
        else:
            results.append(("be_cross_account_404", True, "no other-account search; skipped"))

        # ---- Unauthenticated ----
        st, _ = fetch(base, "/notes/saved-investigation", method="POST",
                      body={"saved_search_id": be_search_id, "body": "x"})
        results.append(("be_unauth_401", st == 401, f"status={st}"))

        # ================= FRONTEND (map_CURRENT.html) =================
        from playwright.sync_api import sync_playwright

        if saved_session is None:
            fail("frontend test needs a fresh session (set RM_SMOKE_EMAIL flow, not RM_SMOKE_JWT)")
        s = saved_session.session
        ref = urlparse(url).hostname.split(".")[0]
        storage_key = f"sb-{ref}-auth-token"
        storage_val = json.dumps({
            "access_token": s.access_token, "refresh_token": s.refresh_token,
            "expires_at": s.expires_at, "expires_in": s.expires_in,
            "token_type": s.token_type or "bearer",
            "user": json.loads(saved_session.user.model_dump_json()),
        })

        stamp = str(int(time.time()))
        note_text = f"map investigation note {stamp}"

        ids_before = {
            r["id"] for r in (
                admin.table("saved_searches").select("id").eq("account_id", account_id)
                .eq("profile_id", profile_id).execute()
            ).data
        }

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            console_errors = []
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.add_init_script(
                f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
            )
            page.goto(f"{base}/map_CURRENT.html#profileId={profile_id}",
                      wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!(window.SupabaseClient) && !!(window.CurrentUser && window.CurrentUser.accountId) "
                "&& typeof window.__rmSaveCurrentInvestigation === 'function' "
                "&& typeof window.__rmGetActiveFavoriteProfileId === 'function'",
                timeout=30000,
            )
            # Active profile resolves from the #profileId hash handoff.
            active_pid = page.evaluate("()=>window.__rmGetActiveFavoriteProfileId()")
            results.append(("fe_active_profile", active_pid == profile_id, f"pid={active_pid}"))

            page.wait_for_selector("#saveInvestigationNote", timeout=15000)
            page.fill("#saveInvestigationNote", note_text)
            page.evaluate("()=>window.__rmSaveCurrentInvestigation()")
            page.wait_for_function(
                "()=>{const e=document.getElementById('saveInvestigationStatus');"
                "return e && e.textContent.indexOf('(note attached)') !== -1;}",
                timeout=20000,
            )
            results.append(("fe_note_attached_status", True, "(note attached)"))
            status_is_error = page.eval_on_selector(
                "#saveInvestigationStatus", "el=>el.classList.contains('is-error')")
            results.append(("fe_status_not_error", status_is_error is False,
                            f"is-error={status_is_error}"))
            results.append(("fe_no_console_errors", len(console_errors) == 0,
                            "; ".join(console_errors[:5]) or "none"))
            browser.close()

        # Identify the saved_searches row created by the frontend save.
        rows_after = (
            admin.table("saved_searches").select("id, search_type, conditions_json, profile_id")
            .eq("account_id", account_id).eq("profile_id", profile_id).execute()
        ).data
        new_rows = [r for r in rows_after if r["id"] not in ids_before]
        fe_search_ids = [r["id"] for r in new_rows]
        results.append(("fe_saved_search_created", len(new_rows) == 1, f"count={len(new_rows)}"))

        if new_rows:
            fe_row = new_rows[0]
            results.append(("fe_replay_search_type", fe_row.get("search_type") == "map",
                            f"search_type={fe_row.get('search_type')}"))
            cj = fe_row.get("conditions_json") or {}
            results.append(("fe_replay_conditions_kind", cj.get("kind") == "saved_investigation",
                            f"kind={cj.get('kind')}"))
            # Replay round-trip via backend GET (reopen path data source).
            st, gb = fetch(base, f"/saved-search/{fe_row['id']}")
            results.append(("fe_replay_get_roundtrip", st == 200, f"status={st}"))

            note_rows = (
                admin.table("notes").select("id, body, target_type, profile_id")
                .eq("account_id", account_id).eq("target_type", "saved_investigation")
                .eq("target_id", fe_row["id"]).is_("archived_at", "null").execute()
            ).data
            results.append(("fe_note_single_active", len(note_rows) == 1, f"count={len(note_rows)}"))
            results.append(("fe_note_body", bool(note_rows) and note_rows[0]["body"] == note_text,
                            f"body={note_rows[0]['body'] if note_rows else None!r}"))
            results.append(("fe_note_profile_from_search",
                            bool(note_rows) and note_rows[0]["profile_id"] == profile_id,
                            f"profile_id={note_rows[0]['profile_id'] if note_rows else None}"))

    finally:
        # Restore: delete all notes + saved_searches this run created.
        target_ids = [i for i in [be_search_id] + fe_search_ids if i]
        for tid in target_ids:
            admin.table("notes").delete().eq("target_type", "saved_investigation") \
                .eq("target_id", tid).execute()
            admin.table("saved_searches").delete().eq("id", tid).execute()
        if created_cross and cross_search_id:
            admin.table("notes").delete().eq("target_type", "saved_investigation") \
                .eq("target_id", cross_search_id).execute()
            admin.table("saved_searches").delete().eq("id", cross_search_id).execute()
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
    print("PASS: smoke_map_saved_investigation_note")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
