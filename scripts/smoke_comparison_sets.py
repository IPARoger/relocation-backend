#!/usr/bin/env python3
"""Smoke: comparison set backend ownership (POST /comparison-sets/create|archive).

Backend:
  * create set + places (places need not be favorites)
  * archive + idempotent archive
  * invalid profile / place -> 404
  * cross-account -> 404
  * unauthenticated -> 401

Frontend (app_shell.html):
  * build comparison from favorites picker
  * compare screen opens with new set
  * archive from chart-record module
  * compare screen safe after archive (recovery)
  * in-memory updates, no reload, no console errors

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_comparison_sets.py
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
        st, _ = fetch(base, "/comparison-sets/create", method="POST",
                      body={"profile_id": "x", "place_ids": ["a", "b"]}, timeout=3)
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


def cmp_places(admin, set_id):
    return (
        admin.table("comparison_set_places")
        .select("place_id, sort_order")
        .eq("comparison_set_id", set_id)
        .order("sort_order")
        .execute()
    ).data or []


def ensure_two_favorites(admin, account_id, profile_id, stamp):
    """Return two place_ids with active favorites for frontend picker (admin setup only)."""
    favs = (
        admin.table("favorite_places")
        .select("place_id")
        .eq("account_id", account_id)
        .eq("profile_id", profile_id)
        .is_("archived_at", "null")
        .limit(5)
        .execute()
    ).data or []
    ids = [f["place_id"] for f in favs if f.get("place_id")]
    created_place_ids = []
    while len(ids) < 2:
        pid = (
            admin.table("places").insert({
                "display_name": f"Smoke Cmp Fav {stamp}-{len(ids)}",
                "latitude": 10.0 + len(ids), "longitude": 20.0 + len(ids),
                "provider": "map_custom", "country_code": "ZZ",
            }).execute()
        ).data[0]["id"]
        created_place_ids.append(pid)
        admin.table("favorite_places").insert({
            "account_id": account_id, "profile_id": profile_id,
            "place_id": pid, "label": f"Smoke fav {len(ids)}",
        }).execute()
        ids.append(pid)
    return ids[:2], created_place_ids


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
            fail(f"port {PORT} serving build without /comparison-sets/create")
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
    created_set_ids = []
    created_place_ids = []
    created_fav_place_ids = []
    profile_id = None
    stamp = uuid.uuid4().hex[:8]
    try:
        jwt, account_id, sess = resolve_ctx(url, anon_key, service_key)
        headers = {"Authorization": f"Bearer {jwt}"}

        profiles = (
            admin.table("profiles").select("id, display_name")
            .eq("account_id", account_id).is_("archived_at", "null")
            .order("created_at").limit(1).execute()
        ).data or []
        if not profiles:
            fail("no active profile")
        profile_id = profiles[0]["id"]

        # Two throwaway places — NOT favorites (backend must not require favorites)
        p1 = admin.table("places").insert({
            "display_name": f"Smoke Cmp A {stamp}", "latitude": 1.1, "longitude": 2.2,
            "provider": "map_custom", "country_code": "ZZ",
        }).execute().data[0]["id"]
        p2 = admin.table("places").insert({
            "display_name": f"Smoke Cmp B {stamp}", "latitude": 3.3, "longitude": 4.4,
            "provider": "map_custom", "country_code": "ZZ",
        }).execute().data[0]["id"]
        created_place_ids.extend([p1, p2])

        # create
        st, b = fetch(base, "/comparison-sets/create", headers=headers, method="POST",
                      body={"profile_id": profile_id, "place_ids": [p1, p2],
                            "title": f"Smoke comparison {stamp}"})
        created = json.loads(b) if st == 200 else {}
        set_id = created.get("id")
        if set_id:
            created_set_ids.append(set_id)
        rows = cmp_places(admin, set_id) if set_id else []
        results.append(("be_create_200",
                        st == 200 and created.get("status") == "created"
                        and created.get("place_ids") == [p1, p2] and len(rows) == 2,
                        f"status={st} id={set_id} places={len(rows)}"))

        # archive
        st, b = fetch(base, "/comparison-sets/archive", headers=headers, method="POST",
                      body={"comparison_set_id": set_id, "profile_id": profile_id})
        archived = json.loads(b) if st == 200 else {}
        results.append(("be_archive_200",
                        st == 200 and archived.get("status") == "archived"
                        and archived.get("archived_at"),
                        f"status={st} archived={archived.get('archived_at')}"))

        # idempotent archive
        st, b = fetch(base, "/comparison-sets/archive", headers=headers, method="POST",
                      body={"comparison_set_id": set_id})
        again = json.loads(b) if st == 200 else {}
        results.append(("be_archive_idempotent",
                        st == 200 and again.get("status") == "already_archived",
                        f"status={st} stat={again.get('status')}"))

        # invalid profile
        st, _ = fetch(base, "/comparison-sets/create", headers=headers, method="POST",
                      body={"profile_id": str(uuid.uuid4()), "place_ids": [p1, p2]})
        results.append(("be_invalid_profile_404", st == 404, f"status={st}"))

        # invalid place
        st, _ = fetch(base, "/comparison-sets/create", headers=headers, method="POST",
                      body={"profile_id": profile_id, "place_ids": [p1, str(uuid.uuid4())]})
        results.append(("be_invalid_place_404", st == 404, f"status={st}"))

        # cross-account profile
        other = (
            admin.table("profiles").select("id").neq("account_id", account_id)
            .is_("archived_at", "null").limit(1).execute()
        ).data
        if other:
            st, _ = fetch(base, "/comparison-sets/archive", headers=headers, method="POST",
                          body={"comparison_set_id": set_id, "profile_id": other[0]["id"]})
            results.append(("be_cross_account_404", st == 404, f"status={st}"))
        else:
            results.append(("be_cross_account_404", True, "skipped"))

        # unauth
        st, _ = fetch(base, "/comparison-sets/create", method="POST",
                      body={"profile_id": profile_id, "place_ids": [p1, p2]})
        results.append(("be_unauth_401", st == 401, f"status={st}"))

        # ================= FRONTEND =================
        fav_place_ids, new_fav_places = ensure_two_favorites(
            admin, account_id, profile_id, stamp,
        )
        created_fav_place_ids.extend(new_fav_places)

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
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.on("load", lambda _f: load_count.__setitem__("n", load_count["n"] + 1))
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
            page.evaluate(
                "()=>{const m=document.getElementById('guidedOnboardingModal');if(m)m.remove();}"
            )
            page.wait_for_function(
                "(pid)=>{try{const vm=window.__rmAppShell.viewModel();"
                "return !!vm && vm.chartRecords.some(r=>r.chartRecordId===pid);}catch(e){return false;}}",
                arg=profile_id, timeout=30000,
            )

            # Build comparison from compare screen
            loads_before = load_count["n"]
            page.evaluate(
                "(pid)=>{window.__rmAppShell.switchChartRecord(pid);"
                "window.__rmAppShell.navigate('compare', {chartRecordId: pid, comparisonSetId: null});}",
                profile_id,
            )
            page.wait_for_selector("[data-action='compare-build']", timeout=15000)
            page.wait_for_selector(".rm-cmp-pick", timeout=15000)

            picks = page.query_selector_all(".rm-cmp-pick")
            for el in picks[:2]:
                el.check()
            page.click("[data-action='compare-build']")
            page.wait_for_function(
                "()=>window.__rmAppShell.navContext.comparisonSetId",
                timeout=20000,
            )
            fe_set_id = page.evaluate("()=>window.__rmAppShell.navContext.comparisonSetId")
            if fe_set_id:
                created_set_ids.append(fe_set_id)
            mem_has = page.evaluate(
                "(id)=>{const r=window.__rmAppShell.storeRaw();"
                "return !!(r&&r.comparison_sets&&r.comparison_sets.some(c=>c.id===id));}",
                fe_set_id,
            )
            results.append(("fe_create_compare_opens",
                            bool(fe_set_id) and mem_has,
                            f"setId={fe_set_id} mem={mem_has}"))
            results.append(("fe_create_no_reload",
                            load_count["n"] == loads_before,
                            f"loads={load_count['n']} before={loads_before}"))

            # Archive from chart-record module
            page.evaluate(
                "(pid)=>{window.__rmAppShell.navigate('chart-record', {chartRecordId: pid});}",
                profile_id,
            )
            page.wait_for_selector("#rm-cr-comparison-sets", timeout=15000)
            page.wait_for_function(
                "(id)=>!!document.querySelector('.rm-cr-cmp-archive[data-cmp-id=\"'+id+'\"]')",
                arg=fe_set_id, timeout=20000,
            )
            loads_before_arch = load_count["n"]
            page.click(f".rm-cr-cmp-archive[data-cmp-id='{fe_set_id}']")
            page.wait_for_function(
                "(id)=>!document.querySelector('.rm-cr-cmp-archive[data-cmp-id=\"'+id+'\"]')",
                arg=fe_set_id, timeout=15000,
            )
            mem_after = page.evaluate(
                "(id)=>{const r=window.__rmAppShell.storeRaw();"
                "return !!(r&&r.comparison_sets&&r.comparison_sets.some(c=>c.id===id));}",
                fe_set_id,
            )
            db_arch = (
                admin.table("comparison_sets").select("archived_at")
                .eq("id", fe_set_id).single().execute()
            ).data
            results.append(("fe_archive_removed",
                            mem_after is False and db_arch and db_arch.get("archived_at"),
                            f"mem={mem_after} archived={db_arch.get('archived_at') if db_arch else None}"))
            results.append(("fe_archive_no_reload",
                            load_count["n"] == loads_before_arch,
                            f"loads={load_count['n']} before={loads_before_arch}"))

            # Compare screen recovery: reopen compare — should not error with stale set
            page.evaluate(
                "(pid)=>{window.__rmAppShell.navigate('compare',"
                "{chartRecordId: pid, comparisonSetId: null, placeId: null});}",
                profile_id,
            )
            page.wait_for_selector("[data-action='compare-build']", timeout=15000)
            broken = page.evaluate(
                "()=>{const cs=window.__rmAppShell.navContext.comparisonSetId;"
                "const fn=window.__rmAppShell.viewModel().comparisonSets.find("
                "c=>c.id===cs); return cs && !fn;}"
            )
            results.append(("fe_compare_recovery",
                            broken is False,
                            f"stale_broken={broken}"))

            app_errors = [e for e in console_errors
                          if "Failed to load resource" not in e and "net::ERR" not in e]
            results.append(("fe_no_console_errors", len(app_errors) == 0,
                            "; ".join(app_errors[:5]) or "none"))
            browser.close()

    finally:
        for sid in set(created_set_ids):
            admin.table("comparison_set_places").delete().eq("comparison_set_id", sid).execute()
            admin.table("comparison_sets").delete().eq("id", sid).execute()
        for pid in created_fav_place_ids:
            admin.table("favorite_places").delete().eq("profile_id", profile_id).eq("place_id", pid).execute()
        for pid in created_place_ids + created_fav_place_ids:
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
    print("PASS: smoke_comparison_sets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
