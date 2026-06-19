#!/usr/bin/env python3
"""Smoke: favorites backend ownership (POST /favorites/save, /favorites/archive).

Backend:
  * save new favorite -> 200 active row
  * save existing active favorite -> 200 same id, no duplicate (idempotent)
  * archive favorite -> 200 archived
  * save archived favorite -> 200 same id, reactivated, no duplicate
  * invalid profile -> 404
  * invalid place -> 404
  * cross-account profile -> 404
  * unauthenticated -> 401

Frontend (map_CURRENT.html favorite save):
  * save favorite (button -> "Favorited"), DB row active, dropdown refresh
  * save already-active favorite -> "Already in favorites.", single row
  * archive (admin) + re-save -> reactivation, single row
  * no app console errors

Frontend (app_shell.html archive):
  * archive favorite from chart-record screen, in-memory removal, no reload

NOTE: map_CURRENT.html resolves places against http://127.0.0.1:8004, so this
smoke must run with the page served from port 8004. It uses an existing 8004
server if it already exposes /favorites/save, else spawns a temp server on 8004.

Auth: admin magic-link OTP for RM_SMOKE_EMAIL (default davidleongoodman@gmail.com).
Requires SUPABASE_* env. Creates a throwaway place + favorite and cleans up.

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_favorites.py
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
        st, _ = fetch(base, "/favorites/save", method="POST",
                      body={"profile_id": "x", "place_id": "y"}, timeout=3)
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


def fav_rows(admin, profile_id, place_id):
    return (
        admin.table("favorite_places")
        .select("id, archived_at")
        .eq("profile_id", profile_id)
        .eq("place_id", place_id)
        .execute()
    ).data or []


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
            fail(f"port {PORT} is serving a build without /favorites/save; "
                 f"restart that server so place resolution + the new route line up")
        if not port_free(PORT):
            fail(f"port {PORT} is occupied but not responding to /favorites/save")
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
    place_id = None
    profile_id = None
    stamp = uuid.uuid4().hex[:8]
    try:
        jwt, account_id, sess = resolve_ctx(url, anon_key, service_key)
        headers = {"Authorization": f"Bearer {jwt}"}

        # Active profile owned by the caller account.
        profiles = (
            admin.table("profiles").select("id")
            .eq("account_id", account_id).is_("archived_at", "null")
            .order("created_at").limit(1).execute()
        ).data or []
        if not profiles:
            fail("no active profile for smoke account")
        profile_id = profiles[0]["id"]

        # Throwaway global place (unique name + coords for clean resolution).
        place_name = f"Smoke Fav City {stamp}"
        lat, lon = 12.345678, 65.432109
        place_id = (
            admin.table("places").insert({
                "display_name": place_name,
                "latitude": lat,
                "longitude": lon,
                "provider": "map_custom",
                "country_code": "ZZ",
            }).execute()
        ).data[0]["id"]

        # Clean slate for (profile, place).
        admin.table("favorite_places").delete() \
            .eq("profile_id", profile_id).eq("place_id", place_id).execute()

        # ===================== BACKEND =====================
        # save new
        st, b = fetch(base, "/favorites/save", headers=headers, method="POST",
                      body={"profile_id": profile_id, "place_id": place_id,
                            "label": place_name})
        ok = st == 200
        saved = json.loads(b) if ok else {}
        fav_id = saved.get("id")
        results.append(("be_save_new_200", ok and saved.get("archived_at") is None
                        and saved.get("reactivated") is False,
                        f"status={st} id={fav_id} archived={saved.get('archived_at')}"))
        if not fav_id:
            fail(f"save new returned {st}: {b[:300]!r}")

        # save active again (idempotent)
        st, b = fetch(base, "/favorites/save", headers=headers, method="POST",
                      body={"profile_id": profile_id, "place_id": place_id,
                            "label": place_name})
        s2 = json.loads(b) if st == 200 else {}
        rows = fav_rows(admin, profile_id, place_id)
        results.append(("be_save_active_idempotent",
                        st == 200 and s2.get("id") == fav_id and len(rows) == 1,
                        f"status={st} id={s2.get('id')} rows={len(rows)}"))

        # archive
        st, b = fetch(base, "/favorites/archive", headers=headers, method="POST",
                      body={"favorite_id": fav_id})
        a = json.loads(b) if st == 200 else {}
        results.append(("be_archive_200",
                        st == 200 and a.get("id") == fav_id
                        and a.get("archived_at") is not None,
                        f"status={st} archived={a.get('archived_at')}"))

        # save archived -> reactivation, same id, single row
        st, b = fetch(base, "/favorites/save", headers=headers, method="POST",
                      body={"profile_id": profile_id, "place_id": place_id,
                            "label": place_name})
        r = json.loads(b) if st == 200 else {}
        rows = fav_rows(admin, profile_id, place_id)
        results.append(("be_save_reactivate",
                        st == 200 and r.get("id") == fav_id
                        and r.get("archived_at") is None
                        and r.get("reactivated") is True and len(rows) == 1,
                        f"status={st} id={r.get('id')} reactivated={r.get('reactivated')} rows={len(rows)}"))

        # invalid profile -> 404
        st, _ = fetch(base, "/favorites/save", headers=headers, method="POST",
                      body={"profile_id": str(uuid.uuid4()), "place_id": place_id})
        results.append(("be_invalid_profile_404", st == 404, f"status={st}"))

        # invalid place -> 404
        st, _ = fetch(base, "/favorites/save", headers=headers, method="POST",
                      body={"profile_id": profile_id, "place_id": str(uuid.uuid4())})
        results.append(("be_invalid_place_404", st == 404, f"status={st}"))

        # cross-account profile -> 404
        other = (
            admin.table("profiles").select("id").neq("account_id", account_id)
            .is_("archived_at", "null").limit(1).execute()
        ).data
        if other:
            st, _ = fetch(base, "/favorites/save", headers=headers, method="POST",
                          body={"profile_id": other[0]["id"], "place_id": place_id})
            results.append(("be_cross_account_404", st == 404, f"status={st}"))
        else:
            results.append(("be_cross_account_404", True, "no other-account profile; skipped"))

        # unauthenticated -> 401
        st, _ = fetch(base, "/favorites/save", method="POST",
                      body={"profile_id": profile_id, "place_id": place_id})
        results.append(("be_unauth_401", st == 401, f"status={st}"))

        # ===================== FRONTEND =====================
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

        # Start each frontend phase from a clean (no favorite) state.
        admin.table("favorite_places").delete() \
            .eq("profile_id", profile_id).eq("place_id", place_id).execute()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            console_errors = []
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.add_init_script(
                f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
            )

            # ---------- MAP ----------
            page.goto(base + f"/map_CURRENT.html#profileId={profile_id}",
                      wait_until="domcontentloaded")
            page.evaluate(
                "async () => { if (window.__rmChartProfilesReady) await window.__rmChartProfilesReady; }"
            )
            page.wait_for_function(
                "(pid) => [...document.getElementById('chartProfile').options]"
                ".some((o) => o.value === pid)",
                arg=profile_id, timeout=60000,
            )
            page.evaluate(
                """(pid) => {
                    const sel = document.getElementById('chartProfile');
                    if (!sel) return;
                    sel.value = pid;
                    sel.dispatchEvent(new Event('change', { bubbles: true }));
                }""",
                profile_id,
            )
            page.wait_for_function(
                "(pid) => typeof window.__rmGetActiveFavoriteProfileId === 'function' "
                "&& window.__rmGetActiveFavoriteProfileId() === pid",
                arg=profile_id, timeout=30000,
            )

            def inject_and_save(btn_id):
                page.evaluate(
                    """([id, name, lat, lon]) => {
                        const wrap = document.createElement('div');
                        wrap.className = 'popup-chart';
                        const b = document.createElement('button');
                        b.id = id; b.className = 'popup-action-favorite';
                        b.textContent = 'Favorite';
                        b.dataset.favName = name;
                        b.dataset.favLat = String(lat);
                        b.dataset.favLon = String(lon);
                        b.dataset.favOrigin = 'map_custom';
                        const st = document.createElement('span');
                        st.className = 'popup-action-status'; st.hidden = true;
                        wrap.appendChild(b); wrap.appendChild(st);
                        document.body.appendChild(wrap);
                        b.click();
                    }""",
                    [btn_id, place_name, lat, lon],
                )
                page.wait_for_function(
                    "(id)=>{const wrap=document.getElementById(id)?.parentElement;"
                    "if(!wrap) return false;"
                    "if(wrap.querySelector('.popup-action-favorited')) return true;"
                    "const st=wrap.querySelector('.popup-action-status');"
                    "if(st && !st.hidden && /favorite/i.test(st.textContent||'')) return true;"
                    "const b=document.getElementById(id);"
                    "return b && b.textContent.indexOf('Favorited')!==-1;}",
                    arg=btn_id, timeout=45000,
                )
                return page.evaluate(
                    "(id)=>{const wrap=document.getElementById(id)?.parentElement;"
                    "const st=wrap?wrap.querySelector('.popup-action-status'):null;"
                    "return st?st.textContent:'';}",
                    btn_id,
                )

            # save favorite (new)
            msg1 = inject_and_save("smokeFav1")
            rows = fav_rows(admin, profile_id, place_id)
            results.append(("fe_map_save_new",
                            len(rows) == 1 and rows[0]["archived_at"] is None
                            and "Saved to favorites." in msg1,
                            f"rows={len(rows)} msg={msg1!r}"))

            # dropdown refresh -> option with the new place_id appears
            page.wait_for_function(
                "(pid)=>{const s=document.getElementById('savedPlaces');"
                "return s && Array.from(s.options).some(o=>o.value===pid);}",
                arg=place_id, timeout=15000,
            )
            results.append(("fe_map_dropdown_refresh", True, "place present in #savedPlaces"))

            # save already-active favorite -> "Already in favorites.", single row
            msg2 = inject_and_save("smokeFav2")
            rows = fav_rows(admin, profile_id, place_id)
            results.append(("fe_map_save_active",
                            len(rows) == 1 and "Already in favorites." in msg2,
                            f"rows={len(rows)} msg={msg2!r}"))

            # archive (admin) + re-save -> reactivation, single row
            admin.table("favorite_places").update(
                {"archived_at": "2020-01-01T00:00:00+00:00"}
            ).eq("id", rows[0]["id"]).execute()
            msg3 = inject_and_save("smokeFav3")
            rows = fav_rows(admin, profile_id, place_id)
            results.append(("fe_map_resave_reactivates",
                            len(rows) == 1 and rows[0]["archived_at"] is None
                            and "Saved to favorites." in msg3,
                            f"rows={len(rows)} msg={msg3!r}"))

            app_errors = [e for e in console_errors
                          if "Failed to load resource" not in e and "net::ERR" not in e]
            results.append(("fe_map_no_console_errors", len(app_errors) == 0,
                            "; ".join(app_errors[:5]) or "none"))

            # Let in-flight map favorites fetches finish; shell gets a clean console buffer.
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                page.wait_for_timeout(1000)
            console_errors.clear()

            # ---------- SHELL (archive) ----------
            # Ensure exactly one active favorite to archive.
            rows = fav_rows(admin, profile_id, place_id)
            fav_id_shell = rows[0]["id"] if rows else None
            if not fav_id_shell:
                fav_id_shell = (
                    admin.table("favorite_places").insert({
                        "account_id": account_id, "profile_id": profile_id,
                        "place_id": place_id, "label": place_name,
                    }).execute()
                ).data[0]["id"]
            else:
                admin.table("favorite_places").update({"archived_at": None}) \
                    .eq("id", fav_id_shell).execute()

            page.on("dialog", lambda d: d.accept())
            load_count = {"n": 0}
            page.on("load", lambda _f: load_count.__setitem__("n", load_count["n"] + 1))

            page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.CurrentUser && !!window.CurrentUser.accountId "
                "&& !!window.__rmAppShell && typeof window.__rmAppShell.navigate === 'function'",
                timeout=30000,
            )
            page.evaluate(
                "()=>{const m=document.getElementById('guidedOnboardingModal');"
                "if(m){m.remove();}}"
            )
            page.wait_for_function(
                "(pid)=>{try{const vm=window.__rmAppShell.viewModel();"
                "return !!vm && Array.isArray(vm.chartRecords) "
                "&& vm.chartRecords.some(r=>r.chartRecordId===pid);}catch(e){return false;}}",
                arg=profile_id, timeout=30000,
            )
            page.evaluate(
                "(pid)=>{window.__rmAppShell.switchChartRecord(pid);"
                "window.__rmAppShell.navigate('chart-record');}",
                profile_id,
            )
            sel = f"[data-action='archive-favorite'][data-favorite-id='{fav_id_shell}']"
            page.wait_for_selector(sel, timeout=15000)

            mem_before = page.evaluate(
                "()=>{const r=window.__rmAppShell.storeRaw();"
                "return r&&Array.isArray(r.favorite_cities)?r.favorite_cities.length:null;}")
            loads_before = load_count["n"]
            page.click(sel)
            page.wait_for_selector(sel, state="detached", timeout=15000)

            mem_after = page.evaluate(
                "()=>{const r=window.__rmAppShell.storeRaw();"
                "return r&&Array.isArray(r.favorite_cities)?r.favorite_cities.length:null;}")
            still_present = page.evaluate(
                "(id)=>{const r=window.__rmAppShell.storeRaw();"
                "return !!(r&&Array.isArray(r.favorite_cities)&&r.favorite_cities.some(f=>f.id===id));}",
                fav_id_shell)
            db_rows = fav_rows(admin, profile_id, place_id)
            db_archived = bool(db_rows) and db_rows[0]["archived_at"] is not None

            results.append(("fe_shell_archive_db", db_archived,
                            f"archived_at={db_rows[0]['archived_at'] if db_rows else None}"))
            results.append(("fe_shell_inmemory_removed",
                            still_present is False
                            and (mem_before is None or mem_after == mem_before - 1),
                            f"before={mem_before} after={mem_after} present={still_present}"))
            results.append(("fe_shell_no_reload", load_count["n"] == loads_before,
                            f"loads_before={loads_before} after={load_count['n']}"))

            sh_errors = [e for e in console_errors
                         if "Failed to load resource" not in e and "net::ERR" not in e]
            results.append(("fe_shell_no_console_errors", len(sh_errors) == 0,
                            "; ".join(sh_errors[:5]) or "none"))

            browser.close()

    finally:
        # Remove the throwaway favorite + place.
        if profile_id is not None and place_id is not None:
            admin.table("favorite_places").delete() \
                .eq("profile_id", profile_id).eq("place_id", place_id).execute()
        if place_id is not None:
            admin.table("places").delete().eq("id", place_id).execute()
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
    print("PASS: smoke_favorites")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
