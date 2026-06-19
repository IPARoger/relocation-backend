#!/usr/bin/env python3
"""Smoke: account settings backend ownership (PATCH /settings/account).

Backend:
  * save settings (creates row if missing) returns merged settings_json
  * update same row shallow-merges (no duplicate account-level row)
  * invalid default profile -> 404
  * cross-account default profile -> 404
  * unauthenticated -> 401

Frontend (app_shell.html Settings screen):
  * Save Settings shows the saved message, no reload, no navigation
  * in-memory store + account default update
  * reload persistence
  * no console errors

Auth: RM_SMOKE_JWT (backend only) or admin magic-link OTP for RM_SMOKE_EMAIL
(default davidleongoodman@gmail.com). Requires SUPABASE_* env.
Captures and restores the account-level user_settings row.

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_settings_account.py
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


def is_benign_console_error(text: str) -> bool:
    """Chromium logs missing static assets as console errors on the dev server."""
    return "Failed to load resource" in text and "404" in text


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
        st, _ = fetch(base, "/settings/account", method="PATCH", body={"settings_patch": {}}, timeout=3)
    except Exception:
        return False
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


def read_account_row(admin, account_id):
    rows = (
        admin.table("user_settings").select("id, account_user_id, settings_json")
        .eq("account_id", account_id).is_("profile_id", "null").execute()
    ).data or []
    return rows[0] if rows else None


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
        port = next((p for p in (8041, 8042, 8043) if port_free(p)), 8041)
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
    original = None  # snapshot of the account-level row to restore
    original_existed = False
    try:
        jwt, account_id, sess = resolve_ctx(url, anon_key, service_key)
        headers = {"Authorization": f"Bearer {jwt}"}

        original = read_account_row(admin, account_id)
        original_existed = original is not None
        original_settings = (original or {}).get("settings_json") or {}
        original_user_id = (original or {}).get("account_user_id")

        # Force "row missing" to exercise create-if-missing.
        admin.table("user_settings").delete().eq("account_id", account_id) \
            .is_("profile_id", "null").execute()

        # save (create if missing)
        st, b = fetch(base, "/settings/account", headers=headers, method="PATCH",
                      body={"settings_patch": {"visible_minor_aspects": True}})
        ok = st == 200
        results.append(("be_save_create_200", ok, f"status={st}"))
        if not ok:
            fail(f"save returned {st}: {b[:300]!r}")
        sj = json.loads(b).get("settings_json") or {}
        results.append(("be_create_value", sj.get("visible_minor_aspects") is True,
                        f"visible_minor_aspects={sj.get('visible_minor_aspects')}"))
        rows = (
            admin.table("user_settings").select("id").eq("account_id", account_id)
            .is_("profile_id", "null").execute()
        ).data
        results.append(("be_single_row_after_create", len(rows) == 1, f"count={len(rows)}"))
        created_id = rows[0]["id"] if rows else None

        # update same row (shallow merge)
        st, b = fetch(base, "/settings/account", headers=headers, method="PATCH",
                      body={"settings_patch": {"out_of_sign_aspects": True}})
        sj2 = json.loads(b).get("settings_json") or {}
        results.append(("be_update_merge", st == 200
                        and sj2.get("visible_minor_aspects") is True
                        and sj2.get("out_of_sign_aspects") is True,
                        f"merged={ {k: sj2.get(k) for k in ('visible_minor_aspects','out_of_sign_aspects')} }"))
        rows2 = (
            admin.table("user_settings").select("id").eq("account_id", account_id)
            .is_("profile_id", "null").execute()
        ).data
        results.append(("be_single_row_after_update",
                        len(rows2) == 1 and rows2[0]["id"] == created_id,
                        f"count={len(rows2)} same_id={bool(rows2) and rows2[0]['id']==created_id}"))

        # invalid default profile -> 404
        st, _ = fetch(base, "/settings/account", headers=headers, method="PATCH",
                      body={"settings_patch": {"default_chart_record_id": str(uuid.uuid4())}})
        results.append(("be_invalid_default_404", st == 404, f"status={st}"))

        # cross-account default profile -> 404
        other = (
            admin.table("profiles").select("id").neq("account_id", account_id)
            .is_("archived_at", "null").limit(1).execute()
        ).data
        if other:
            st, _ = fetch(base, "/settings/account", headers=headers, method="PATCH",
                          body={"settings_patch": {"default_chart_record_id": other[0]["id"]}})
            results.append(("be_cross_account_404", st == 404, f"status={st}"))
        else:
            results.append(("be_cross_account_404", True, "no other-account profile; skipped"))

        # unauthenticated -> 401
        st, _ = fetch(base, "/settings/account", method="PATCH",
                      body={"settings_patch": {"visible_minor_aspects": True}})
        results.append(("be_unauth_401", st == 401, f"status={st}"))

        # ================= FRONTEND =================
        if sess is None:
            results.append(("fe_skipped", True, "RM_SMOKE_JWT set; frontend needs fresh session"))
        else:
            want_orb = None
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

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                console_errors = []
                load_count = {"n": 0}
                page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" and not is_benign_console_error(m.text) else None)
                page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
                page.on("load", lambda _f: load_count.__setitem__("n", load_count["n"] + 1))
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
                    page.evaluate(
                        "()=>{const m=document.getElementById('guidedOnboardingModal');"
                        "if(m){m.classList.remove('open');m.setAttribute('aria-hidden','true');m.remove();}}"
                    )

                load()
                page.evaluate("()=>window.__rmAppShell.navigate('settings')")
                page.wait_for_selector(".settings-landing-grid", timeout=15000)
                results.append(("fe_settings_landing", page.query_selector(".settings-landing-grid") is not None,
                                "settings landing grid"))

                page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'about' })")
                page.wait_for_selector("#sec-about", timeout=15000)
                results.append(("fe_settings_ia_about",
                                page.query_selector("#sec-about") is not None
                                and "GeoNames" in (page.inner_text("#sec-about") or ""),
                                "about data sources section"))

                page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'charts' })")
                page.wait_for_selector("#rm-settings-majorb-conjunction", timeout=15000)
                results.append(("fe_settings_charts_sub", True, "charts subpage"))

                # My Data subpage: default profile persistence
                page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'data' })")
                page.wait_for_selector("#rm-settings-default-cr", timeout=15000)
                page.wait_for_selector("[data-action='save-settings']", timeout=15000)

                opts = page.eval_on_selector_all(
                    "#rm-settings-default-cr option", "els=>els.map(e=>e.value)")
                cur_default = page.eval_on_selector("#rm-settings-default-cr", "el=>el.value")
                target_default = next((o for o in opts if o != cur_default), cur_default)
                page.eval_on_selector(
                    "#rm-settings-default-cr",
                    "(el,v)=>{el.value=v;}", target_default)

                loads_before = load_count["n"]
                page.click("[data-action='save-settings']")
                page.wait_for_function(
                    "()=>{const m=document.getElementById('rm-settings-msg');"
                    "return m && m.textContent.indexOf('Saved') !== -1;}",
                    timeout=15000,
                )
                results.append(("fe_saved_msg", True, "saved"))
                results.append(("fe_no_reload", load_count["n"] == loads_before,
                                f"loads_before={loads_before} after={load_count['n']}"))

                mem_default = page.evaluate("()=>window.__rmAppShell.getAccountDefaultChartRecordId()")
                results.append(("fe_default_update", mem_default == target_default,
                                f"default={mem_default} want={target_default}"))

                load()
                page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'data' })")
                page.wait_for_selector("#rm-settings-default-cr", timeout=15000)
                rl_default = page.eval_on_selector("#rm-settings-default-cr", "el=>el.value")
                results.append(("fe_reload_default", rl_default == target_default,
                                f"default={rl_default} want={target_default}"))

                # Charts subpage: visible_minor_aspects persistence
                page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'charts' })")
                page.wait_for_selector("#rm-settings-minor-aspects", timeout=15000)
                cur_minor = page.eval_on_selector("#rm-settings-minor-aspects", "el=>el.checked")
                want_minor = not cur_minor
                page.eval_on_selector("#rm-settings-minor-aspects", "(el,v)=>{el.checked=v;}", want_minor)
                page.click("[data-action='save-settings']")
                page.wait_for_function(
                    "()=>{const m=document.getElementById('rm-settings-msg');"
                    "return m && m.textContent.indexOf('Saved') !== -1;}",
                    timeout=15000,
                )
                mem_minor = page.evaluate(
                    "()=>{const r=window.__rmAppShell.storeRaw();return r&&r.user_settings?r.user_settings.visible_minor_aspects:null;}")
                results.append(("fe_inmemory_update", mem_minor == want_minor,
                                f"mem={mem_minor} want={want_minor}"))
                load()
                page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'charts' })")
                page.wait_for_selector("#rm-settings-minor-aspects", timeout=15000)
                rl_minor = page.eval_on_selector("#rm-settings-minor-aspects", "el=>el.checked")
                results.append(("fe_reload_minor", rl_minor == want_minor,
                                f"minor={rl_minor} want={want_minor}"))

                # major_aspect_orbs persistence: toggle conjunction orb on Charts subpage
                page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'charts' })")
                page.wait_for_selector("#rm-settings-majorb-conjunction", timeout=15000)
                maj_orb_sel = "#rm-settings-majorb-conjunction"
                if page.query_selector(maj_orb_sel):
                    cur_orb = float(page.eval_on_selector(maj_orb_sel, "el=>parseFloat(el.value)"))
                    want_orb = 7.5 if cur_orb != 7.5 else 8.5
                    page.eval_on_selector(maj_orb_sel, "(el,v)=>{el.value=String(v);}", want_orb)
                    page.click("[data-action='save-settings']")
                    page.wait_for_function(
                        "()=>{const m=document.getElementById('rm-settings-msg');"
                        "return m && m.textContent.indexOf('Saved') !== -1;}",
                        timeout=15000,
                    )
                    mem_orb = page.evaluate(
                        "()=>{const r=window.__rmAppShell.storeRaw();"
                        "const o=r&&r.user_settings&&r.user_settings.major_aspect_orbs;"
                        "return o&&o.conjunction!=null?o.conjunction:null;}")
                    results.append(("fe_inmemory_major_orb", mem_orb == want_orb,
                                    f"mem={mem_orb} want={want_orb}"))
                    load()
                    page.evaluate("()=>window.__rmAppShell.navigate('settings', { settingsSubpage: 'charts' })")
                    page.wait_for_selector(maj_orb_sel, timeout=15000)
                    rl_orb = float(page.eval_on_selector(maj_orb_sel, "el=>parseFloat(el.value)"))
                    results.append(("fe_reload_major_orb", rl_orb == want_orb,
                                    f"orb={rl_orb} want={want_orb}"))

                results.append(("fe_no_console_errors", len(console_errors) == 0,
                                "; ".join(console_errors[:5]) or "none"))
                browser.close()

            # DB reflects the patch
            db_row = read_account_row(admin, account_id)
            db_sj = (db_row or {}).get("settings_json") or {}
            results.append(("fe_db_default", db_sj.get("default_chart_record_id") == target_default,
                            f"db_default={db_sj.get('default_chart_record_id')}"))
            if want_orb is not None:
                maj_db = (db_sj.get("major_aspect_orbs") or {}).get("conjunction")
                results.append(("fe_db_major_orb", maj_db == want_orb, f"db_conj={maj_db} want={want_orb}"))

    finally:
        # Restore the original account-level row exactly.
        if account_id is not None:
            admin.table("user_settings").delete().eq("account_id", account_id) \
                .is_("profile_id", "null").execute()
            if original_existed:
                admin.table("user_settings").insert({
                    "account_id": account_id,
                    "account_user_id": original_user_id,
                    "profile_id": None,
                    "settings_json": original_settings,
                }).execute()
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
    print("PASS: smoke_settings_account")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
