#!/usr/bin/env python3
"""Smoke: PIH dignities display (DIGNITIES-1).

Validates:
  * dignity_ontology.js loads and lookupFamily works
  * PIH footer toggle labeled "Dignities", default OFF
  * Supportive/challenging classes on house cells only when ON
  * No +/- glyphs in PIH cells
  * dignities_enabled persists in comparison workspace state

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_dignities_pih.py
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


def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env.staging")
    url = os.environ.get("SUPABASE_URL", "").strip()
    anon = os.environ.get("SUPABASE_ANON_KEY", "").strip()
    svc = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not url or not anon or not svc:
        fail("missing Supabase env (.env.staging)")

    def ontology_route_ok(b):
        try:
            st, body = fetch(b, "/dignity_ontology.js", timeout=3)
            return st == 200 and b"RMDignityOntology" in body
        except Exception:
            return False

    proc = None
    base = f"http://127.0.0.1:{PORT}"
    if not (wait_health(base) and ontology_route_ok(base)):
        port = next((p for p in (8041, 8042, 8043, 8044) if port_free(p)), None)
        if port is None:
            fail("no free port for temp server")
        base = f"http://127.0.0.1:{port}"
        proc = subprocess.Popen(
            [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app", "--host", "127.0.0.1", "--port", str(port)],
            cwd=ROOT,
            env={**os.environ},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if not wait_health(base) or not ontology_route_ok(base):
            if proc:
                proc.terminate()
            fail("server did not start with dignity_ontology.js")
    results = []
    created_set_ids = []
    created_place_ids = []
    try:
        st, ont = fetch(base, "/dignity_ontology.js")
        results.append(("ontology_served", st == 200 and b"RMDignityOntology" in ont, f"status={st}"))

        token, account_id, sess = resolve_ctx(url, anon, svc)
        admin_headers = {"Authorization": f"Bearer {token}"}
        from urllib.parse import urlparse
        ref = urlparse(url).hostname.split(".")[0]
        storage_key = f"sb-{ref}-auth-token"
        s = sess.session
        storage_val = json.dumps({
            "access_token": s.access_token, "refresh_token": s.refresh_token,
            "expires_at": s.expires_at, "expires_in": s.expires_in,
            "token_type": s.token_type or "bearer",
            "user": json.loads(sess.user.model_dump_json()),
        })

        admin = __import__("supabase").create_client(url, svc)
        profiles = (
            admin.table("profiles").select("id, display_name")
            .eq("account_id", account_id).is_("archived_at", "null")
            .order("created_at").limit(1).execute()
        ).data or []
        if not profiles:
            fail("no active profile")
        profile_id = profiles[0]["id"]
        stamp = uuid.uuid4().hex[:8]

        p1 = admin.table("places").insert({
            "display_name": f"Smoke Dignity A {stamp}", "latitude": 35.6762, "longitude": 139.6503,
            "provider": "map_custom", "country_code": "JP",
        }).execute().data[0]["id"]
        p2 = admin.table("places").insert({
            "display_name": f"Smoke Dignity B {stamp}", "latitude": 1.3521, "longitude": 103.8198,
            "provider": "map_custom", "country_code": "SG",
        }).execute().data[0]["id"]
        created_place_ids.extend([p1, p2])

        st, create_body = fetch(
            base, "/comparison-sets/create", method="POST", headers=admin_headers,
            body={"profile_id": profile_id, "place_ids": [p1, p2], "title": "Dignities smoke"},
        )
        create = json.loads(create_body.decode()) if create_body else {}
        set_id = create.get("comparison_set_id") or create.get("id")
        if st != 200 or not set_id:
            fail(f"could not create comparison set: {st} {create_body[:200]}")
        created_set_ids.append(set_id)

        from playwright.sync_api import sync_playwright
        console_errors = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.on("dialog", lambda d: d.accept())
            page.add_init_script(
                f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
            )
            page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.CurrentUser && !!window.__rmAppShell "
                "&& typeof window.__rmAppShell.navigate === 'function'",
                timeout=30000,
            )
            page.wait_for_function(
                "(pid)=>{try{const vm=window.__rmAppShell.viewModel();"
                "return !!vm && vm.chartRecords.some(r=>r.chartRecordId===pid);}catch(e){return false;}}",
                arg=profile_id, timeout=30000,
            )
            page.wait_for_function("() => !!window.RMDignityOntology", timeout=10000)

            ont_lookup = page.evaluate(
                "() => ({"
                "sunLeo: window.RMDignityOntology.lookupFamily('Sun','Leo'),"
                "sunLibra: window.RMDignityOntology.lookupFamily('Sun','Libra'),"
                "marsNull: window.RMDignityOntology.lookupFamily('Uranus','Aries')"
                "})"
            )
            results.append(("ontology_lookup", ont_lookup.get("sunLeo") == "supportive"
                            and ont_lookup.get("sunLibra") == "challenging"
                            and ont_lookup.get("marsNull") is None,
                            str(ont_lookup)))

            page.evaluate(
                "()=>{const m=document.getElementById('guidedOnboardingModal');if(m){m.remove();}}"
            )
            page.evaluate(
                "(args)=>{window.__rmAppShell.navigate('compare',"
                "{chartRecordId: args.pid, comparisonSetId: args.sid});}",
                {"pid": profile_id, "sid": set_id},
            )
            page.wait_for_selector("[data-action='toggle-pih-dignities'][data-pih-scope='compare']", timeout=30000)

            footer = page.evaluate(
                """() => {
                  const el = document.querySelector("[data-action='toggle-pih-dignities'][data-pih-scope='compare']");
                  const label = el && el.parentElement ? el.parentElement.textContent.trim() : '';
                  return {exists: !!el, checked: el ? el.checked : null, label};
                }"""
            )
            results.append(("footer_default_off",
                            footer.get("exists") and footer.get("checked") is False
                            and footer.get("label") == "Dignities",
                            str(footer)))

            off_classes = page.evaluate(
                "() => document.querySelectorAll('td.pih-house-cell.dignity-supportive, td.pih-house-cell.dignity-challenging').length"
            )
            results.append(("no_classes_when_off", off_classes == 0, f"count={off_classes}"))

            page.click("[data-action='toggle-pih-dignities'][data-pih-scope='compare']")
            page.wait_for_function(
                "() => document.querySelectorAll('td.pih-house-cell.dignity-supportive, td.pih-house-cell.dignity-challenging').length > 0",
                timeout=15000,
            )
            on_state = page.evaluate(
                """() => ({
                  colored: document.querySelectorAll('td.pih-house-cell.dignity-supportive, td.pih-house-cell.dignity-challenging').length,
                  pihCells: document.querySelectorAll('td.pih-house-cell').length,
                  plusMinus: Array.from(document.querySelectorAll('#rm-screen5-columns td')).some(td => /^[+-]$/.test(td.textContent.trim())),
                  glyphs: !!document.querySelector('#rm-screen5-columns .dignity-glyph')
                })"""
            )
            results.append(("classes_when_on",
                            on_state.get("colored", 0) > 0 and on_state.get("pihCells", 0) > 0,
                            str(on_state)))
            results.append(("no_plus_minus", not on_state.get("plusMinus"), str(on_state)))
            results.append(("no_glyphs", not on_state.get("glyphs"), str(on_state)))

            page.click("[data-action='toggle-pih-dignities'][data-pih-scope='compare']")
            page.wait_for_function(
                "() => document.querySelectorAll('td.pih-house-cell.dignity-supportive, td.pih-house-cell.dignity-challenging').length === 0",
                timeout=10000,
            )

            page.click("[data-action='toggle-pih-dignities'][data-pih-scope='compare']")
            page.wait_for_function(
                """() => document.querySelector("[data-action='toggle-pih-dignities'][data-pih-scope='compare']").checked""",
                timeout=5000,
            )
            page.evaluate("async ()=>{ await window.__rmAppShell.flushComparisonWorkspaceState(); }")
            page.wait_for_function(
                "()=>{const m=document.getElementById('rm-cmp-ws-msg');"
                "return m && m.textContent.indexOf('saved') !== -1;}",
                timeout=15000,
            )
            db_row = (
                admin.table("comparison_sets").select("settings_snapshot_json")
                .eq("id", set_id).single().execute()
            ).data
            db_ws = ((db_row or {}).get("settings_snapshot_json") or {}).get("comparison_workspace_state") or {}
            results.append(("workspace_persist", db_ws.get("dignities_enabled") is True,
                            f"dignities_enabled={db_ws.get('dignities_enabled')}"))

            app_errors = [e for e in console_errors
                          if "Failed to load resource" not in e and "net::ERR" not in e]
            results.append(("no_console_errors", len(app_errors) == 0,
                            "; ".join(app_errors[:5]) or "none"))
            browser.close()
    finally:
        admin = __import__("supabase").create_client(url, svc)
        for sid in set(created_set_ids):
            admin.table("comparison_set_places").delete().eq("comparison_set_id", sid).execute()
            admin.table("comparison_sets").delete().eq("id", sid).execute()
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
    print("PASS: smoke_dignities_pih")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
