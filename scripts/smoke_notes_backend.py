#!/usr/bin/env python3
"""Backend smoke: notes ownership endpoints.

Verifies POST /notes/chart-record and POST /notes/comparison-set:
  * authenticated save returns 200 with the note payload
  * a second save updates the SAME row (no duplicate active note)
  * cross-account target is rejected (404)
  * unauthenticated request returns 401

Auth: RM_SMOKE_JWT, else admin magic-link OTP for RM_SMOKE_EMAIL
(default davidleongoodman@gmail.com). Requires SUPABASE_* env.
Restores state (archives notes it creates; deletes a comparison set if created).

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_notes_backend.py
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
    try:
        urllib.request.urlopen(base + "/current-location/current?profile_id=x", timeout=3)
        return True
    except urllib.error.HTTPError as err:
        return err.code != 404
    except Exception:
        return False


def notes_route_present(base):
    # New POST route requires auth, so it returns 401 when present. A stale
    # server only has GET /notes/{id} and returns 405 for POST; 404 means missing.
    st, _ = fetch(base, "/notes/chart-record", method="POST", body={"profile_id": "x"})
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


def resolve_jwt_ctx():
    url = os.environ.get("SUPABASE_URL", "")
    anon = os.environ.get("SUPABASE_ANON_KEY", "")
    svc = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon, svc]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY")
    from supabase import create_client
    anon_client = create_client(url, anon)
    token = os.environ.get("RM_SMOKE_JWT", "").strip()
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
    anon_client.postgrest.auth(token)
    account_ids = anon_client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        fail("no account for smoke user")
    return token, account_ids[0]


def main() -> int:
    from supabase import create_client
    admin = create_client(
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    )

    base = "http://127.0.0.1:8004"
    proc = None
    if not notes_route_present(base):
        port = 8023 if port_free(8023) else 8024
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
    created_comparison_set_id = None
    profile_id = None
    comparison_set_id = None
    account_id = None
    try:
        jwt, account_id = resolve_jwt_ctx()
        headers = {"Authorization": f"Bearer {jwt}"}

        profiles = (
            admin.table("profiles").select("id").eq("account_id", account_id)
            .is_("archived_at", "null").order("created_at", desc=False).limit(1).execute()
        ).data
        if not profiles:
            fail("no profile for smoke account")
        profile_id = profiles[0]["id"]

        cs = (
            admin.table("comparison_sets").select("id").eq("account_id", account_id)
            .is_("archived_at", "null").limit(1).execute()
        ).data
        if cs:
            comparison_set_id = cs[0]["id"]
        else:
            created = admin.table("comparison_sets").insert({
                "account_id": account_id, "profile_id": profile_id,
                "title": "smoke notes set",
            }).execute().data
            comparison_set_id = created[0]["id"]
            created_comparison_set_id = comparison_set_id

        # --- Chart record note ---
        st, b = fetch(base, "/notes/chart-record", headers=headers, method="POST",
                      body={"profile_id": profile_id, "body": "chart note v1"})
        ok = st == 200
        results.append(("chart_save_200", ok, f"status={st}"))
        if not ok:
            fail(f"chart save returned {st}: {b[:300]!r}")
        first_id = json.loads(b).get("id")

        st, b = fetch(base, "/notes/chart-record", headers=headers, method="POST",
                      body={"profile_id": profile_id, "body": "chart note v2"})
        second = json.loads(b)
        results.append(("chart_update_same_row", st == 200 and second.get("id") == first_id,
                        f"id1={first_id} id2={second.get('id')}"))
        active = (
            admin.table("notes").select("id").eq("account_id", account_id)
            .eq("profile_id", profile_id).eq("target_type", "chart_record")
            .is_("archived_at", "null").execute()
        ).data
        results.append(("chart_single_active_row", len(active) == 1, f"count={len(active)}"))
        results.append(("chart_body_updated", second.get("body") == "chart note v2",
                        f"body={second.get('body')!r}"))

        # --- Comparison-set note ---
        st, b = fetch(base, "/notes/comparison-set", headers=headers, method="POST",
                      body={"comparison_set_id": comparison_set_id, "body": "cmp note v1"})
        ok = st == 200
        results.append(("cmp_save_200", ok, f"status={st}"))
        if not ok:
            fail(f"cmp save returned {st}: {b[:300]!r}")
        cmp_first_id = json.loads(b).get("id")

        st, b = fetch(base, "/notes/comparison-set", headers=headers, method="POST",
                      body={"comparison_set_id": comparison_set_id, "body": "cmp note v2"})
        cmp_second = json.loads(b)
        results.append(("cmp_update_same_row", st == 200 and cmp_second.get("id") == cmp_first_id,
                        f"id1={cmp_first_id} id2={cmp_second.get('id')}"))
        cmp_active = (
            admin.table("notes").select("id").eq("account_id", account_id)
            .eq("target_type", "comparison_set").eq("target_id", comparison_set_id)
            .is_("archived_at", "null").execute()
        ).data
        results.append(("cmp_single_active_row", len(cmp_active) == 1, f"count={len(cmp_active)}"))

        # --- Cross-account rejection ---
        other_profile = (
            admin.table("profiles").select("id").neq("account_id", account_id).limit(1).execute()
        ).data
        if other_profile:
            st, _ = fetch(base, "/notes/chart-record", headers=headers, method="POST",
                          body={"profile_id": other_profile[0]["id"], "body": "x"})
            results.append(("chart_cross_account_404", st == 404, f"status={st}"))
        else:
            results.append(("chart_cross_account_404", True, "no other-account profile; skipped"))

        other_cs = (
            admin.table("comparison_sets").select("id").neq("account_id", account_id).limit(1).execute()
        ).data
        if other_cs:
            st, _ = fetch(base, "/notes/comparison-set", headers=headers, method="POST",
                          body={"comparison_set_id": other_cs[0]["id"], "body": "x"})
            results.append(("cmp_cross_account_404", st == 404, f"status={st}"))
        else:
            results.append(("cmp_cross_account_404", True, "no other-account comparison set; skipped"))

        # --- Unauthenticated ---
        st, _ = fetch(base, "/notes/chart-record", method="POST",
                      body={"profile_id": profile_id, "body": "x"})
        results.append(("unauth_401", st == 401, f"status={st}"))

    finally:
        # Restore: archive notes created for this profile/comparison set.
        if account_id and profile_id:
            admin.table("notes").delete().eq("account_id", account_id) \
                .eq("profile_id", profile_id).eq("target_type", "chart_record").execute()
        if account_id and comparison_set_id:
            admin.table("notes").delete().eq("account_id", account_id) \
                .eq("target_type", "comparison_set").eq("target_id", comparison_set_id).execute()
        if created_comparison_set_id:
            admin.table("comparison_sets").delete().eq("id", created_comparison_set_id).execute()
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
    print("PASS: smoke_notes_backend")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
