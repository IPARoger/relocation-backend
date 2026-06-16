#!/usr/bin/env python3
"""Smoke: place resolution backend ownership (POST /places/resolve-or-create).

Backend:
  * resolve existing place by name + coords -> 200, _status=existing, no duplicate
  * create missing place with coords -> 200, _status=created
  * resolve same coords again -> 200 existing, single row
  * no coords and no match -> 422
  * unauthenticated -> 401

Frontend (map_CURRENT.html favorite save via place resolution):
  * custom location favorite creates place + favorite row
  * second save -> "Already in favorites.", single place row

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_place_resolution.py
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


def route_present(base):
    try:
        st, _ = fetch(
            base,
            "/places/resolve-or-create",
            method="POST",
            body={"display_name": "x", "latitude": 1.0, "longitude": 2.0},
            timeout=3,
        )
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


def place_rows(admin, place_id):
    return admin.table("places").select("id, display_name").eq("id", place_id).execute().data or []


def count_places_named(admin, name):
    return (
        admin.table("places")
        .select("id", count="exact")
        .eq("display_name", name)
        .execute()
    ).count or 0


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
            fail(
                f"port {PORT} is serving a build without /places/resolve-or-create; "
                "restart that server so the new route is available"
            )
        if not port_free(PORT):
            fail(f"port {PORT} is occupied but not responding to /places/resolve-or-create")
        proc = subprocess.Popen(
            [
                str(PYTHON),
                "-m",
                "uvicorn",
                "main_centerline_FIXER:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(PORT),
            ],
            cwd=str(ROOT),
            env=dict(os.environ),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
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

        profiles = (
            admin.table("profiles")
            .select("id")
            .eq("account_id", account_id)
            .is_("archived_at", "null")
            .order("created_at")
            .limit(1)
            .execute()
        ).data or []
        if not profiles:
            fail("no active profile for smoke account")
        profile_id = profiles[0]["id"]

        place_name = f"Smoke Place Resolve {stamp}"
        lat, lon = 23.456789, 34.567890

        # unauthenticated -> 401
        st, _ = fetch(
            base,
            "/places/resolve-or-create",
            method="POST",
            body={"display_name": place_name, "latitude": lat, "longitude": lon},
        )
        results.append(("be_unauth_401", st == 401, f"status={st}"))

        # create missing place
        st, b = fetch(
            base,
            "/places/resolve-or-create",
            headers=headers,
            method="POST",
            body={
                "display_name": place_name,
                "latitude": lat,
                "longitude": lon,
                "origin": "map_custom",
                "coord_tolerance": 0.02,
            },
        )
        created = json.loads(b) if st == 200 else {}
        place_id = created.get("id")
        results.append(
            (
                "be_create_200",
                st == 200 and created.get("_status") == "created" and place_id,
                f"status={st} id={place_id} _status={created.get('_status')}",
            )
        )
        if not place_id:
            fail(f"create returned {st}: {b[:300]!r}")

        count_after_create = count_places_named(admin, place_name)
        results.append(
            ("be_single_row_after_create", count_after_create == 1, f"count={count_after_create}")
        )

        # resolve existing (same name + coords)
        st, b = fetch(
            base,
            "/places/resolve-or-create",
            headers=headers,
            method="POST",
            body={
                "display_name": place_name,
                "latitude": lat,
                "longitude": lon,
                "coord_tolerance": 0.02,
            },
        )
        existing = json.loads(b) if st == 200 else {}
        count_after_resolve = count_places_named(admin, place_name)
        results.append(
            (
                "be_resolve_existing_200",
                st == 200
                and existing.get("id") == place_id
                and existing.get("_status") == "existing"
                and count_after_resolve == 1,
                f"status={st} id={existing.get('id')} _status={existing.get('_status')} count={count_after_resolve}",
            )
        )

        # no coords, no match -> 422
        st, b = fetch(
            base,
            "/places/resolve-or-create",
            headers=headers,
            method="POST",
            body={"display_name": f"NoCoords {stamp}"},
        )
        detail = {}
        if b:
            try:
                detail = json.loads(b).get("detail", {})
            except json.JSONDecodeError:
                detail = {}
        results.append(
            (
                "be_no_coords_422",
                st == 422 and detail.get("error") == "place_unresolved",
                f"status={st} error={detail.get('error')}",
            )
        )

        # ===================== FRONTEND =====================
        from playwright.sync_api import sync_playwright

        storage_key = f"sb-{url.split('//')[-1].split('.')[0]}-auth-token"
        storage_val = json.dumps(
            {
                "access_token": sess.session.access_token,
                "refresh_token": sess.session.refresh_token,
                "expires_at": sess.session.expires_at,
                "expires_in": sess.session.expires_in,
                "token_type": sess.session.token_type or "bearer",
                "user": json.loads(sess.session.user.model_dump_json()),
            }
        )

        admin.table("favorite_places").delete().eq("profile_id", profile_id).eq(
            "place_id", place_id
        ).execute()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            console_errors = []
            page.on(
                "console",
                lambda m: console_errors.append(m.text) if m.type == "error" else None,
            )
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.add_init_script(
                f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
            )

            page.goto(
                base + f"/map_CURRENT.html#profileId={profile_id}",
                wait_until="domcontentloaded",
            )
            page.wait_for_function(
                "(pid) => !!(window.SupabaseClient||window._supabaseClient) "
                "&& typeof window.__rmGetActiveFavoriteProfileId === 'function' "
                "&& window.__rmGetActiveFavoriteProfileId() === pid",
                arg=profile_id,
                timeout=30000,
            )

            def inject_and_save(btn_id, name, flat, flon):
                page.evaluate(
                    """([id, nm, la, lo]) => {
                        const wrap = document.createElement('div');
                        wrap.className = 'popup-chart';
                        const b = document.createElement('button');
                        b.id = id; b.className = 'popup-action-favorite';
                        b.textContent = 'Favorite';
                        b.dataset.favName = nm;
                        b.dataset.favLat = String(la);
                        b.dataset.favLon = String(lo);
                        b.dataset.favOrigin = 'map_custom';
                        const st = document.createElement('span');
                        st.className = 'popup-action-status'; st.hidden = true;
                        wrap.appendChild(b); wrap.appendChild(st);
                        document.body.appendChild(wrap);
                        b.click();
                    }""",
                    [btn_id, name, flat, flon],
                )
                page.wait_for_function(
                    "(id)=>{const b=document.getElementById(id);"
                    "return b && b.textContent.indexOf('Favorited')!==-1;}",
                    arg=btn_id,
                    timeout=20000,
                )
                return page.evaluate(
                    "(id)=>{const b=document.getElementById(id);"
                    "const st=b.parentElement.querySelector('.popup-action-status');"
                    "return st?st.textContent:'';}",
                    btn_id,
                )

            fe_name = f"Smoke FE Place {stamp}"
            fe_lat, fe_lon = 45.111111, 56.222222
            msg1 = inject_and_save("smokePlace1", fe_name, fe_lat, fe_lon)
            fe_place_rows = (
                admin.table("places")
                .select("id")
                .eq("display_name", fe_name)
                .execute()
            ).data or []
            fe_place_id = fe_place_rows[0]["id"] if fe_place_rows else None
            fav_rows = (
                admin.table("favorite_places")
                .select("id, archived_at")
                .eq("profile_id", profile_id)
                .eq("place_id", fe_place_id)
                .execute()
            ).data or [] if fe_place_id else []
            results.append(
                (
                    "fe_map_resolve_create_favorite",
                    bool(fe_place_id)
                    and len(fe_place_rows) == 1
                    and len(fav_rows) == 1
                    and fav_rows[0]["archived_at"] is None
                    and "Saved to favorites." in msg1,
                    f"place_rows={len(fe_place_rows)} fav_rows={len(fav_rows)} msg={msg1!r}",
                )
            )

            msg2 = inject_and_save("smokePlace2", fe_name, fe_lat, fe_lon)
            fe_place_rows2 = (
                admin.table("places")
                .select("id")
                .eq("display_name", fe_name)
                .execute()
            ).data or []
            results.append(
                (
                    "fe_map_resolve_existing_favorite",
                    len(fe_place_rows2) == 1
                    and "Already in favorites." in msg2,
                    f"place_rows={len(fe_place_rows2)} msg={msg2!r}",
                )
            )

            if fe_place_id and fe_place_id != place_id:
                admin.table("favorite_places").delete().eq(
                    "profile_id", profile_id
                ).eq("place_id", fe_place_id).execute()
                admin.table("places").delete().eq("id", fe_place_id).execute()

            app_errors = [
                e
                for e in console_errors
                if "Failed to load resource" not in e and "net::ERR" not in e
            ]
            results.append(
                (
                    "fe_map_no_console_errors",
                    len(app_errors) == 0,
                    "; ".join(app_errors[:5]) or "none",
                )
            )
            browser.close()

    finally:
        if profile_id and place_id:
            admin.table("favorite_places").delete().eq("profile_id", profile_id).eq(
                "place_id", place_id
            ).execute()
        if place_id:
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
    print("PASS: smoke_place_resolution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
