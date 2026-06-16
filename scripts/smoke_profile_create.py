#!/usr/bin/env python3
"""Smoke: profile+birth creation backend ownership (POST /profiles/create-with-birth).

Backend:
  * create exact birth -> 200
  * create unknown birth -> 200
  * invalid place -> 404
  * missing required fields -> 422
  * unauthenticated -> 401

Frontend (first_profile_intake.js):
  * first-profile mode redirect payload
  * add-profile mode onCreated flow
  * profile row created
  * birth_record row created
  * no console errors
  * add mode: no reload

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_profile_create.py
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
import uuid
from pathlib import Path
from urllib.parse import parse_qs, urlparse

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
        st, _ = fetch(base, "/profiles/create-with-birth", method="POST",
                      body={"display_name": "x", "birth_date": "2000-01-01",
                            "birth_time_mode": "unknown", "birth_place_id": str(uuid.uuid4())},
                      timeout=3)
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


def make_place(admin, stamp, suffix=""):
    row = admin.table("places").insert({
        "display_name": f"Smoke Profile {stamp}{suffix}",
        "latitude": 40.7, "longitude": -74.0,
        "provider": "map_custom", "country_code": "US",
        "timezone_id": "America/New_York",
    }).execute().data[0]
    return row["id"], row["display_name"]


def cleanup_profile(admin, profile_id):
    if not profile_id:
        return
    admin.table("birth_records").delete().eq("profile_id", profile_id).execute()
    admin.table("profiles").delete().eq("id", profile_id).execute()


def fill_intake(page, name, birth_date, birth_time, place_query):
  page.fill("#rm-intake-name", name)
  page.fill("#rm-intake-date", birth_date)
  if birth_time:
    page.fill("#rm-intake-time", birth_time)
  page.fill("#rm-intake-place-input", place_query)
  page.wait_for_selector("#rm-intake-place-results .place-result", timeout=15000)
  page.click("#rm-intake-place-results .place-result")


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
            fail(f"port {PORT} serving build without /profiles/create-with-birth")
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
    created_profile_ids = []
    created_place_ids = []
    stamp = uuid.uuid4().hex[:8]
    try:
        jwt, account_id, sess = resolve_ctx(url, anon_key, service_key)
        headers = {"Authorization": f"Bearer {jwt}"}

        place_id, place_name = make_place(admin, stamp, " A")
        created_place_ids.append(place_id)
        search_prefix = f"Smoke Profile {stamp}"

        # exact birth
        st, b = fetch(base, "/profiles/create-with-birth", headers=headers, method="POST",
                      body={"display_name": f"Smoke Exact {stamp}",
                            "birth_date": "1990-05-15",
                            "birth_time_mode": "exact",
                            "birth_time_start": "14:30:00",
                            "birth_place_id": place_id,
                            "timezone_id": "America/New_York"})
        exact = json.loads(b) if st == 200 else {}
        exact_pid = exact.get("profile_id")
        if exact_pid:
            created_profile_ids.append(exact_pid)
        br_exact = (
            admin.table("birth_records").select("id, birth_time_mode, birth_time_start")
            .eq("profile_id", exact_pid).limit(1).execute()
        ).data if exact_pid else []
        results.append(("be_create_exact",
                        st == 200 and exact.get("status") == "created"
                        and exact.get("birth_record_id")
                        and br_exact and br_exact[0].get("birth_time_mode") == "exact"
                        and br_exact[0].get("birth_time_start"),
                        f"status={st} pid={exact_pid} br={bool(br_exact)}"))

        # unknown birth
        st, b = fetch(base, "/profiles/create-with-birth", headers=headers, method="POST",
                      body={"display_name": f"Smoke Unknown {stamp}",
                            "birth_date": "1985-01-01",
                            "birth_time_mode": "unknown",
                            "birth_place_id": place_id})
        unknown = json.loads(b) if st == 200 else {}
        unknown_pid = unknown.get("profile_id")
        if unknown_pid:
            created_profile_ids.append(unknown_pid)
        br_unknown = (
            admin.table("birth_records").select("id, birth_time_mode, birth_time_start")
            .eq("profile_id", unknown_pid).limit(1).execute()
        ).data if unknown_pid else []
        results.append(("be_create_unknown",
                        st == 200 and unknown.get("status") == "created"
                        and br_unknown and br_unknown[0].get("birth_time_mode") == "unknown"
                        and br_unknown[0].get("birth_time_start") is None,
                        f"status={st} pid={unknown_pid}"))

        # invalid place
        st, b = fetch(base, "/profiles/create-with-birth", headers=headers, method="POST",
                      body={"display_name": "x", "birth_date": "2000-01-01",
                            "birth_time_mode": "unknown",
                            "birth_place_id": str(uuid.uuid4())})
        detail = json.loads(b).get("detail", {}) if st == 404 else {}
        results.append(("be_invalid_place_404",
                        st == 404 and detail.get("error") == "place_not_found",
                        f"status={st} err={detail.get('error')}"))

        # missing required fields
        st, b = fetch(base, "/profiles/create-with-birth", headers=headers, method="POST",
                      body={"display_name": "", "birth_date": "2000-01-01",
                            "birth_time_mode": "unknown", "birth_place_id": place_id})
        miss = json.loads(b).get("detail", {}) if st == 422 else {}
        results.append(("be_missing_fields_422",
                        st == 422 and miss.get("error") == "invalid_display_name",
                        f"status={st} err={miss.get('error')}"))

        # unauth
        st, _ = fetch(base, "/profiles/create-with-birth", method="POST",
                      body={"display_name": "x", "birth_date": "2000-01-01",
                            "birth_time_mode": "unknown", "birth_place_id": place_id})
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

        fe_place_id, _ = make_place(admin, stamp, " FE")
        created_place_ids.append(fe_place_id)
        fe_name = f"Smoke FE Add {stamp}"
        fe_date = "1992-03-04"
        fe_time = "09:15"

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

            # --- add mode (app_shell) ---
            page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.CurrentUser && !!window.__showFirstProfileIntake",
                timeout=30000,
            )
            page.evaluate(
                "()=>{const m=document.getElementById('guidedOnboardingModal');if(m)m.remove();}"
            )
            loads_before_add = load_count["n"]
            page.evaluate("() => { window.__smokeIntake = { called: false, profileId: null, opts: null }; }")
            page.evaluate(
                "() => window.__showFirstProfileIntake({"
                "mode: 'add',"
                "onCreated: (id, opts) => { window.__smokeIntake = { called: true, profileId: id, opts }; }"
                "})"
            )
            page.wait_for_selector("#rm-first-profile-intake", timeout=10000)
            fill_intake(page, fe_name, fe_date, fe_time, search_prefix)
            page.click("#rm-intake-submit")
            page.wait_for_function("() => window.__smokeIntake && window.__smokeIntake.called", timeout=20000)
            add_handoff = page.evaluate("() => window.__smokeIntake")
            add_pid = add_handoff.get("profileId")
            if add_pid:
                created_profile_ids.append(add_pid)
            prof_row = (
                admin.table("profiles").select("id, display_name")
                .eq("id", add_pid).single().execute()
            ).data if add_pid else None
            br_row = (
                admin.table("birth_records").select("id, profile_id, birth_date, birth_time_mode")
                .eq("profile_id", add_pid).limit(1).execute()
            ).data if add_pid else []
            overlay_gone = page.evaluate("() => !document.getElementById('rm-first-profile-intake')")
            results.append(("fe_add_onCreated",
                            add_handoff.get("called") and add_pid
                            and add_handoff.get("opts", {}).get("switchToNew") is True
                            and overlay_gone,
                            f"called={add_handoff.get('called')} pid={add_pid} overlay_gone={overlay_gone}"))
            results.append(("fe_add_profile_row",
                            prof_row and prof_row.get("display_name") == fe_name,
                            f"row={prof_row}"))
            results.append(("fe_add_birth_row",
                            bool(br_row) and br_row[0].get("birth_date") == fe_date,
                            f"br={br_row[0] if br_row else None}"))
            results.append(("fe_add_no_reload",
                            load_count["n"] == loads_before_add,
                            f"loads={load_count['n']} before={loads_before_add}"))

            # --- first mode redirect (map_CURRENT) ---
            fe_first_name = f"Smoke FE First {stamp}"
            page.goto(base + "/map_CURRENT.html", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.CurrentUser && !!window.__showFirstProfileIntake",
                timeout=30000,
            )
            page.evaluate("() => window.__showFirstProfileIntake()")
            page.wait_for_selector("#rm-first-profile-intake", timeout=10000)
            page.click("#rm-mode-unknown")
            fill_intake(page, fe_first_name, "1988-07-07", None, search_prefix)
            with page.expect_navigation(timeout=30000) as nav_info:
                page.click("#rm-intake-submit")
            redirect_url = nav_info.value.url
            qs = parse_qs(urlparse(redirect_url).query)
            first_pid = (qs.get("chartRecordId") or [None])[0]
            if first_pid:
                created_profile_ids.append(first_pid)
            results.append(("fe_first_redirect_payload",
                            "map_CURRENT.html" in redirect_url
                            and qs.get("skipOnboarding") == ["1"]
                            and qs.get("handoff") == ["app_shell"]
                            and bool(qs.get("handoffCreatedAt"))
                            and bool(first_pid),
                            f"url={redirect_url}"))
            first_prof = (
                admin.table("profiles").select("id").eq("id", first_pid).limit(1).execute()
            ).data if first_pid else []
            first_br = (
                admin.table("birth_records").select("id")
                .eq("profile_id", first_pid).limit(1).execute()
            ).data if first_pid else []
            results.append(("fe_first_profile_row", bool(first_prof), f"pid={first_pid}"))
            results.append(("fe_first_birth_row", bool(first_br), f"br={len(first_br)}"))

            app_errors = [e for e in console_errors
                          if "Failed to load resource" not in e and "net::ERR" not in e
                          and "[intake]" not in e]
            results.append(("fe_no_console_errors", len(app_errors) == 0,
                            "; ".join(app_errors[:5]) or "none"))
            browser.close()

    finally:
        for pid in set(created_profile_ids):
            cleanup_profile(admin, pid)
        for pid in created_place_ids:
            admin.table("places").delete().eq("id", pid).execute()
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
    print("PASS: smoke_profile_create")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
