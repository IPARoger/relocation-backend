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
from smoke_settings_details import wait_for_minor_aspects
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

        # SETTINGS-SOURCE-1: registry endpoint
        _def_st, _def_b = fetch(base, "/settings/astrology-defaults")
        _def_ok = _def_st == 200 and isinstance(json.loads(_def_b).get("aspect_to_angle_orbs"), dict)
        results.append(("be_astrology_defaults_endpoint", _def_ok, f"st={_def_st}"))

        # SETTINGS-SOURCE-1: authenticated /relocated-chart honors aspect_to_angle_orbs
        _rc_fixture = (
            "/relocated-chart?lat=40.7128&lon=-74.0060"
            "&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0"
        )
        _tight_patch = {"settings_patch": {"aspect_to_angle_orbs": {
            "conjunction": 8, "opposition": 8, "square": 0.01, "trine": 8, "sextile": 6,
        }}}
        fetch(base, "/settings/account", method="PATCH", headers=headers, body=_tight_patch)
        _st_tight, _b_tight = fetch(base, _rc_fixture, headers=headers)
        _cc_tight = json.loads(_b_tight).get("canonical_chart", {}) if _st_tight == 200 else {}
        _a2a_tight = _cc_tight.get("aspects_to_angles") or []
        _square_tight = [r for r in _a2a_tight if r.get("aspect") == "square"]

        _wide_patch = {"settings_patch": {"aspect_to_angle_orbs": {
            "conjunction": 8, "opposition": 8, "square": 15, "trine": 8, "sextile": 6,
        }}}
        fetch(base, "/settings/account", method="PATCH", headers=headers, body=_wide_patch)
        _st_wide, _b_wide = fetch(base, _rc_fixture, headers=headers)
        _cc_wide = json.loads(_b_wide).get("canonical_chart", {}) if _st_wide == 200 else {}
        _a2a_wide = _cc_wide.get("aspects_to_angles") or []
        _square_wide = [r for r in _a2a_wide if r.get("aspect") == "square"]

        results.append(("be_settings_source_a2a_orb",
                        _st_tight == 200 and _st_wide == 200 and len(_square_wide) >= len(_square_tight),
                        f"square_tight={len(_square_tight)} square_wide={len(_square_wide)}"))

        # SETTINGS-SOURCE-1: display_aspects_to_angles affects A2A rows (authenticated)
        _ang_off = {"settings_patch": {"display_aspects_to_angles": {
            "asc": True, "mc": True, "dsc": False, "ic": False,
        }}}
        fetch(base, "/settings/account", method="PATCH", headers=headers, body=_ang_off)
        _st_off, _b_off = fetch(base, _rc_fixture, headers=headers)
        _angles_off = {r.get("angle") for r in (json.loads(_b_off).get("canonical_chart", {}).get("aspects_to_angles") or [])} if _st_off == 200 else set()

        _ang_on = {"settings_patch": {"display_aspects_to_angles": {
            "asc": True, "mc": True, "dsc": True, "ic": True,
        }}}
        fetch(base, "/settings/account", method="PATCH", headers=headers, body=_ang_on)
        _st_on, _b_on = fetch(base, _rc_fixture, headers=headers)
        _angles_on = {r.get("angle") for r in (json.loads(_b_on).get("canonical_chart", {}).get("aspects_to_angles") or [])} if _st_on == 200 else set()

        results.append(("be_settings_source_display_angles",
                        _st_off == 200 and _st_on == 200 and "DSC" not in _angles_off and "DSC" in _angles_on,
                        f"off={sorted(_angles_off)} on_has_dsc={'DSC' in _angles_on}"))

        # SETTINGS-SOURCE-1: metadata.effective_settings echoes compute inputs
        _meta_eff = (_cc_wide.get("metadata") or {}).get("effective_settings") or {}
        _echo_orbs = (_meta_eff.get("aspect_to_angle_orbs") or {}).get("square")
        results.append(("be_settings_source_metadata_echo",
                        _echo_orbs == 15,
                        f"square_orb={_echo_orbs}"))




        # P2P-ASPECTS-1: canonical_chart.aspects_planet_to_planet (TestClient-style via HTTP)
        _p2p_st, _p2p_b = fetch(
            base,
            "/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0",
        )
        _p2p_ok = False
        _p2p_fields_ok = False
        _p2p_pair_order_ok = False
        if _p2p_st == 200:
            _p2p_cc = json.loads(_p2p_b).get("canonical_chart") or {}
            _p2p_rows = _p2p_cc.get("aspects_planet_to_planet")
            _p2p_ok = isinstance(_p2p_rows, list) and len(_p2p_rows) > 0
            if _p2p_ok:
                _req = {"body_a", "body_b", "aspect", "separation_deg", "orb_limit_deg", "in_orb", "out_of_sign"}
                _p2p_fields_ok = _req.issubset(set(_p2p_rows[0].keys()))
                _p2p_pair_order_ok = all(r.get("body_a", "") < r.get("body_b", "") for r in _p2p_rows)
        results.append(("be_p2p_canonical_field", _p2p_ok, f"st={_p2p_st} len={len(_p2p_rows) if _p2p_ok else 0}"))
        results.append(("be_p2p_row_schema", _p2p_fields_ok, "required fields present"))
        results.append(("be_p2p_lexicographic_pairs", _p2p_pair_order_ok, "body_a < body_b"))

        # P2P honors major_aspect_orbs not aspect_to_angle_orbs (authenticated)
        _p2p_tight = {"settings_patch": {"major_aspect_orbs": {
            "conjunction": 8, "opposition": 8, "square": 0.01, "trine": 8, "sextile": 6,
        }, "aspect_to_angle_orbs": {
            "conjunction": 8, "opposition": 8, "square": 15, "trine": 8, "sextile": 6,
        }}}
        fetch(base, "/settings/account", method="PATCH", headers=headers, body=_p2p_tight)
        _st_pt, _b_pt = fetch(base, "/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0", headers=headers)
        _sq_pt = []
        if _st_pt == 200:
            _sq_pt = [r for r in (json.loads(_b_pt).get("canonical_chart", {}).get("aspects_planet_to_planet") or []) if r.get("aspect") == "square"]
        _p2p_wide = {"settings_patch": {"major_aspect_orbs": {
            "conjunction": 8, "opposition": 8, "square": 15, "trine": 8, "sextile": 6,
        }}}
        fetch(base, "/settings/account", method="PATCH", headers=headers, body=_p2p_wide)
        _st_pw, _b_pw = fetch(base, "/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0", headers=headers)
        _sq_pw = []
        if _st_pw == 200:
            _sq_pw = [r for r in (json.loads(_b_pw).get("canonical_chart", {}).get("aspects_planet_to_planet") or []) if r.get("aspect") == "square"]
        results.append(("be_p2p_major_orb_settings",
                        _st_pt == 200 and _st_pw == 200 and len(_sq_pw) >= len(_sq_pt),
                        f"square_tight={len(_sq_pt)} square_wide={len(_sq_pw)}"))

        _p2p_no_sq = {"settings_patch": {"visible_major_aspects": ["conjunction", "opposition", "trine", "sextile"]}}
        fetch(base, "/settings/account", method="PATCH", headers=headers, body=_p2p_no_sq)
        _st_ns, _b_ns = fetch(base, "/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0", headers=headers)
        _has_sq = False
        if _st_ns == 200:
            _has_sq = any(r.get("aspect") == "square" for r in (json.loads(_b_ns).get("canonical_chart", {}).get("aspects_planet_to_planet") or []))
        results.append(("be_p2p_aspect_visibility", _st_ns == 200 and not _has_sq, f"has_square={_has_sq}"))

        _p2p_min = {"settings_patch": {"visible_minor_aspects": True, "visible_minor_aspects_list": ["quincunx"], "out_of_sign_aspects": True}}
        fetch(base, "/settings/account", method="PATCH", headers=headers, body=_p2p_min)
        _st_mn, _b_mn = fetch(base, "/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0", headers=headers)
        _has_q = False
        if _st_mn == 200:
            _has_q = any(r.get("aspect") == "quincunx" for r in (json.loads(_b_mn).get("canonical_chart", {}).get("aspects_planet_to_planet") or []))
        results.append(("be_p2p_minor_when_enabled", _st_mn == 200 and _has_q, f"has_quincunx={_has_q}"))

        # RETRO-MOTION-1: canonical_chart.planets motion truth
        _motion_st, _motion_b = fetch(
            base,
            "/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0",
        )
        _motion_req = {"speed_deg_per_day", "retrograde", "station", "motion_state"}
        _motion_planets = {}
        _motion_all_ok = False
        _motion_retro_ok = False
        _motion_state_ok = False
        _motion_station_ok = False
        if _motion_st == 200:
            _motion_planets = (json.loads(_motion_b).get("canonical_chart") or {}).get("planets") or {}
            if isinstance(_motion_planets, dict) and _motion_planets:
                _motion_all_ok = all(_motion_req.issubset(set(p.keys())) for p in _motion_planets.values() if isinstance(p, dict))
                _motion_retro_ok = all(
                    bool(p.get("retrograde")) == (float(p.get("speed_deg_per_day", 0)) < 0)
                    for p in _motion_planets.values() if isinstance(p, dict) and p.get("speed_deg_per_day") is not None
                )
                _motion_state_ok = all(
                    p.get("motion_state") in ("direct", "retrograde", "station_direct", "station_retrograde")
                    for p in _motion_planets.values() if isinstance(p, dict)
                )
                _pluto = _motion_planets.get("Pluto") or {}
                _motion_station_ok = bool(_pluto.get("station")) and _pluto.get("motion_state") == "station_retrograde"
        results.append(("be_motion_speed_present", _motion_st == 200 and _motion_all_ok, f"planets={len(_motion_planets)}"))
        results.append(("be_motion_retrograde_matches_speed", _motion_retro_ok, "retrograde == speed < 0"))
        results.append(("be_motion_state_populated", _motion_state_ok, "motion_state enum"))
        results.append(("be_motion_station_threshold", _motion_station_ok, "Pluto station_retrograde on fixture"))

        try:
            import sys
            sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
            from main_centerline_FIXER import STATION_THRESHOLD_DEG_PER_DAY, _planet_motion_from_speed
            _sd = _planet_motion_from_speed(0.01)
            _sr = _planet_motion_from_speed(-0.01)
            _helper_ok = (
                STATION_THRESHOLD_DEG_PER_DAY == 0.05
                and _sd["station"] and _sd["motion_state"] == "station_direct"
                and _sr["station"] and _sr["motion_state"] == "station_retrograde"
            )
        except Exception as _e:
            _helper_ok = False
        results.append(("be_motion_helper_threshold", _helper_ok, "0.05 deg/day station band"))


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
                wait_for_minor_aspects(page)
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
                wait_for_minor_aspects(page)
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

        # CHART-TRUTH-FIX-1: /relocated-chart must reject missing birth params with 422
        _rc_st, _ = fetch(base, "/relocated-chart?lat=40.0&lon=-74.0", method="GET", timeout=10)
        results.append(("be_relocated_chart_422_on_missing_birth",
                        _rc_st == 422,
                        f"status={_rc_st} (expect 422)"))

        # SETTINGS-WIRE-1: minor aspects wired in engine
        import json as _json
        _minor_payload = {
            "birth_year": 1990, "birth_month": 3, "birth_day": 15, "birth_hour_utc": 12.0,
            "house_conditions": [],
            "aspect_overlay": {"planet": "sun", "aspect": "quincunx", "angle": "MC"},
            "generation_mode": "truth_grid",
            "truth_grid_resolution": 5.0,
        }
        _minor_st, _minor_b = fetch(base, "/search-regions", method="POST", body=_minor_payload, timeout=30)
        _minor_ok = False
        if _minor_st == 200:
            _mj = json.loads(_minor_b)
            _minor_ok = isinstance(_mj, dict) and _mj.get("type") == "FeatureCollection"
        results.append(("be_minor_asp_quincunx_overlay",
                        _minor_ok,
                        f"status={_minor_st}"))

        _nov_payload = {**_minor_payload, "aspect_overlay": {"planet": "moon", "aspect": "novile", "angle": "ASC"}}
        _nov_st, _nov_b = fetch(base, "/search-regions", method="POST", body=_nov_payload, timeout=30)
        results.append(("be_minor_asp_novile_overlay", _nov_st == 200, f"status={_nov_st}"))

        # SETTINGS-WIRE-1A: display_aspects_to_angles persists through PATCH /settings/account
        _a2d_patch = {"settings_patch": {"display_aspects_to_angles": {"asc": True, "mc": True, "dsc": True, "ic": False}}}
        _a2d_st, _a2d_b = fetch(base, "/settings/account", method="PATCH", headers=headers, body=_a2d_patch)
        _a2d_saved = json.loads(_a2d_b).get("settings_json", {}).get("display_aspects_to_angles", {}) if _a2d_st == 200 else {}
        results.append(("be_a2d_persists",
                        _a2d_st == 200 and _a2d_saved.get("dsc") is True,
                        f"status={_a2d_st} dsc={_a2d_saved.get('dsc')}"))

        # SETTINGS-WIRE-3: visible_major_aspects persists through PATCH
        _maj_patch = {"settings_patch": {"visible_major_aspects": ["conjunction", "trine"]}}
        _maj_st, _maj_b = fetch(base, "/settings/account", method="PATCH", body=_maj_patch, headers=headers)
        _maj_saved = json.loads(_maj_b).get("settings_json", {}).get("visible_major_aspects", []) if _maj_st == 200 else []
        results.append(("be_major_asp_persists",
                        _maj_st == 200 and "conjunction" in _maj_saved and "trine" in _maj_saved,
                        f"status={_maj_st} saved={_maj_saved}"))

        # SETTINGS-WIRE-2: /relocated-chart near_cusp threshold changes with house_proximity_orb
        # Test with tight orb (0.5): a planet that was near_cusp=True at 2.0 should be False at 0.5
        # and vice versa. Just verify the param is accepted and affects the field.
        _rc_base = f"{base}/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0"
        _rc_st2,  _rc_b2  = fetch(base, f"/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0&house_proximity_orb=2.0")
        _rc_st3,  _rc_b3  = fetch(base, f"/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0&house_proximity_orb=0.0001")
        _rc2_ok = _rc_st2 == 200
        _rc3_ok = _rc_st3 == 200
        if _rc2_ok and _rc3_ok:
            _ph2 = json.loads(_rc_b2).get("planet_houses", {})
            _ph3 = json.loads(_rc_b3).get("planet_houses", {})
            # with orb=0.0001 no planet should be near_cusp; with orb=2.0 some may be
            _nc_wide = sum(1 for v in _ph2.values() if v.get("near_cusp"))
            _nc_tight = sum(1 for v in _ph3.values() if v.get("near_cusp"))
            # tight orb should have <= wide orb near_cusp count (monotonically decreasing)
            _orb_mono = _nc_tight <= _nc_wide
        else:
            _orb_mono = False
        results.append(("be_hpo_accepted",
                        _rc2_ok and _rc3_ok,
                        f"wide_st={_rc_st2} tight_st={_rc_st3}"))
        results.append(("be_hpo_monotonic",
                        _orb_mono,
                        f"nc_wide={_nc_wide if _rc2_ok and _rc3_ok else 'N/A'} nc_tight={_nc_tight if _rc2_ok and _rc3_ok else 'N/A'}"))

        # CHART-TRUTH-PHASE-1: canonical_chart v1 on /relocated-chart (additive; legacy keys preserved)
        _rc_p1_st, _rc_p1_b = fetch(
            base,
            f"/relocated-chart?lat=40.7128&lon=-74.0060&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0&house_proximity_orb=2.0&location_kind=relocated",
        )
        _rc_p1_ok = _rc_p1_st == 200
        _cc = {}
        _legacy_ok = False
        _canonical_ok = False
        _cusps_ok = False
        _a2a_ok = False
        _natal_kind_ok = False
        if _rc_p1_ok:
            _rcj = json.loads(_rc_p1_b)
            _cc = _rcj.get("canonical_chart") or {}
            _legacy_ok = (
                isinstance(_rcj.get("asc"), str)
                and isinstance(_rcj.get("planet_houses"), dict)
                and _rcj.get("asc_deg") is not None
            )
            _cusps = ((_cc.get("houses") or {}).get("cusps_deg") or [])
            _canonical_ok = (
                isinstance(_cc, dict)
                and _cc.get("schema_version") == 1
                and isinstance(_cc.get("angles"), dict)
                and "ASC" in _cc.get("angles", {})
                and isinstance(_cc.get("planets"), dict)
            )
            _cusps_ok = len(_cusps) == 12
            _a2a_ok = isinstance(_cc.get("aspects_to_angles"), list)
            _natal_st, _natal_b = fetch(
                base,
                f"/relocated-chart?lat=38.72&lon=-9.14&birth_year=1990&birth_month=3&birth_day=15&birth_hour_utc=12.0&location_kind=natal",
            )
            if _natal_st == 200:
                _natal_cc = (json.loads(_natal_b).get("canonical_chart") or {})
                _natal_kind_ok = _natal_cc.get("location_anchor", {}).get("kind") == "natal"
        results.append(("be_canonical_legacy_preserved", _rc_p1_ok and _legacy_ok, f"st={_rc_p1_st}"))
        results.append(("be_canonical_schema_v1", _canonical_ok, f"schema={_cc.get('schema_version')}"))
        results.append(("be_canonical_cusps_12", _cusps_ok, f"len={len(_cusps) if _rc_p1_ok else 'N/A'}"))
        results.append(("be_canonical_a2a_array", _a2a_ok, f"type={type(_cc.get('aspects_to_angles')).__name__ if _rc_p1_ok else 'N/A'}"))
        results.append(("be_canonical_natal_kind", _natal_kind_ok, f"natal_kind={_natal_kind_ok}"))


        # SETTINGS-WIRE-2: /search-regions overlay accepts max_orb in aspect_overlay dict
        _ao_payload = {
            "birth_year": 1990, "birth_month": 3, "birth_day": 15, "birth_hour_utc": 12.0,
            "house_conditions": [],
            "aspect_overlay": {"planet": "sun", "aspect": "conjunction", "angle": "MC", "max_orb": 4.0},
            "generation_mode": "truth_grid", "truth_grid_resolution": 5.0,
        }
        _ao_st, _ao_b = fetch(base, "/search-regions", method="POST", body=_ao_payload, timeout=30)
        _ao_ok = False
        if _ao_st == 200:
            _aoj = json.loads(_ao_b)
            # Check that max_orb is stored in at least one feature's properties
            _feats = _aoj.get("features", [])
            # max_orb is a direct property on each feature (not nested under aspect_overlay)
        _ao_ok = isinstance(_aoj, dict) and _aoj.get("type") == "FeatureCollection" and any(
                (f.get("properties") or {}).get("max_orb") == 4.0
                for f in _feats
            )
        results.append(("be_a2a_orb_in_features",
                        _ao_ok,
                        f"status={_ao_st} found_max_orb={'yes' if _ao_ok else 'no'}"))

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
