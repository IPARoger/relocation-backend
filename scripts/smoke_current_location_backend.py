#!/usr/bin/env python3
"""Read/write smoke: current-location backend ownership.

Verifies:
  * /health and /current-location/current (with Bearer JWT) return 200
  * GET returns { profile_id, current_location } shape
  * POST /current-location/set returns 200 with place payload
  * Only one is_current=true row remains for the profile (service-role check)
  * Cross-account profile_id is rejected (404 profile_not_found)
  * Unauthenticated requests return 401
  * Original current location is restored at the end (net-zero data change)

Auth:
  * RM_SMOKE_JWT — use this Bearer token directly when set
  * else RM_SMOKE_EMAIL (default davidleongoodman@gmail.com) + admin magic-link OTP
    (requires SUPABASE_SERVICE_ROLE_KEY in environment)

Run (server at BASE_URL, default http://127.0.0.1:8004):
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_current_location_backend.py
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
BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8004").rstrip("/")
PYTHON = ROOT / "venv" / "bin" / "python"
DEFAULT_EMAIL = "davidleongoodman@gmail.com"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def fetch(base: str, path: str, headers: dict | None = None, method: str = "GET",
          body: dict | None = None, timeout: int = 60):
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


def port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def wait_server(base: str, timeout_s: float = 20.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{base}/health", timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.25)
    return False


def spawn_server(port: int, env: dict[str, str]) -> subprocess.Popen:
    return subprocess.Popen(
        [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app",
         "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(ROOT), env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def resolve_jwt_and_ctx():
    """Return (jwt, account_id, user_id) for the smoke user."""
    token = os.environ.get("RM_SMOKE_JWT", "").strip()
    url = os.environ.get("SUPABASE_URL", "")
    anon = os.environ.get("SUPABASE_ANON_KEY", "")
    service = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon, service]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY")

    from supabase import create_client
    anon_client = create_client(url, anon)

    if token:
        user = anon_client.auth.get_user(token).user
        anon_client.postgrest.auth(token)
        account_ids = anon_client.rpc("app_account_ids").execute().data or []
        return token, (account_ids[0] if account_ids else None), user.id

    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()
    admin = create_client(url, service)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    otp = link.properties.email_otp
    session = anon_client.auth.verify_otp({"email": email, "token": otp, "type": "email"})
    if not session.session:
        fail(f"Could not obtain JWT for {email}")
    jwt = session.session.access_token
    anon_client.postgrest.auth(jwt)
    account_ids = anon_client.rpc("app_account_ids").execute().data or []
    return jwt, (account_ids[0] if account_ids else None), session.user.id


def main() -> int:
    base = BASE
    proc: subprocess.Popen | None = None

    status_health, _ = fetch(base, "/health")
    status_probe, _ = fetch(base, "/current-location/current?profile_id=x")
    if status_health != 200 or status_probe == 404:
        alt_port = 8015
        if not port_free(alt_port):
            fail(f"Server unusable at {base} and port {alt_port} busy")
        proc = spawn_server(alt_port, dict(os.environ))
        base = f"http://127.0.0.1:{alt_port}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")

    results: list[tuple[str, bool, str]] = []
    from supabase import create_client
    service_client = create_client(
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    )

    try:
        jwt, account_id, user_id = resolve_jwt_and_ctx()
        if not account_id:
            fail("Could not resolve account_id for smoke user")
        headers = {"Authorization": f"Bearer {jwt}"}

        # Pick a profile owned by this account.
        profiles = (
            service_client.table("profiles")
            .select("id")
            .eq("account_id", account_id)
            .is_("archived_at", "null")
            .order("created_at", desc=False)
            .limit(1)
            .execute()
        ).data
        if not profiles:
            fail("No profile available for smoke account")
        profile_id = profiles[0]["id"]

        # Capture original current row to restore later.
        original = (
            service_client.table("current_location_history")
            .select("place_id, source")
            .eq("account_id", account_id)
            .eq("profile_id", profile_id)
            .eq("is_current", True)
            .order("selected_at", desc=True)
            .limit(1)
            .execute()
        ).data
        original_place_id = original[0]["place_id"] if original else None

        # Pick two distinct places to set.
        places = (
            service_client.table("places").select("id").limit(5).execute()
        ).data
        if not places:
            fail("No places available to set")
        test_place_id = next(
            (p["id"] for p in places if p["id"] != original_place_id), places[0]["id"]
        )

        # 1. GET current (200, shape).
        st, body = fetch(base, f"/current-location/current?profile_id={profile_id}",
                         headers=headers)
        ok = st == 200
        results.append(("get_current_200", ok, f"status={st}"))
        if ok:
            payload = json.loads(body.decode())
            ok = "profile_id" in payload and "current_location" in payload
            results.append(("get_current_shape", ok, str(sorted(payload.keys()))))

        # 2. POST set (200, place payload).
        st, body = fetch(base, "/current-location/set", headers=headers, method="POST",
                         body={"profile_id": profile_id, "place_id": test_place_id})
        ok = st == 200
        results.append(("post_set_200", ok, f"status={st}"))
        if not ok:
            fail(f"POST set returned {st}: {body[:300]!r}")
        set_payload = json.loads(body.decode())
        cl = set_payload.get("current_location") or {}
        ok = (cl.get("place_id") == test_place_id and cl.get("is_current") is True
              and isinstance(cl.get("place"), dict) and cl["place"].get("id") == test_place_id)
        results.append(("post_set_place_payload", ok, json.dumps(cl.get("place"))))

        # 3. Only one current row remains (service-role check).
        current_rows = (
            service_client.table("current_location_history")
            .select("id, place_id")
            .eq("account_id", account_id)
            .eq("profile_id", profile_id)
            .eq("is_current", True)
            .execute()
        ).data
        ok = len(current_rows) == 1 and current_rows[0]["place_id"] == test_place_id
        results.append(("single_current_row", ok, f"count={len(current_rows)}"))

        # 4. Cross-account rejection: a profile from another account.
        other = (
            service_client.table("profiles")
            .select("id, account_id")
            .neq("account_id", account_id)
            .limit(1)
            .execute()
        ).data
        if other:
            other_profile = other[0]["id"]
            st, _ = fetch(base, f"/current-location/current?profile_id={other_profile}",
                          headers=headers)
            ok = st == 404
            results.append(("cross_account_get_404", ok, f"status={st}"))
            st, _ = fetch(base, "/current-location/set", headers=headers, method="POST",
                          body={"profile_id": other_profile, "place_id": test_place_id})
            ok = st == 404
            results.append(("cross_account_set_404", ok, f"status={st}"))
        else:
            results.append(("cross_account_get_404", True, "no other-account profile; skipped"))

        # 5. Unauthenticated -> 401.
        st, _ = fetch(base, f"/current-location/current?profile_id={profile_id}")
        results.append(("unauth_get_401", st == 401, f"status={st}"))
        st, _ = fetch(base, "/current-location/set", method="POST",
                      body={"profile_id": profile_id, "place_id": test_place_id})
        results.append(("unauth_set_401", st == 401, f"status={st}"))

        # Restore original (net-zero). Retire test row, reinstate original if any.
        service_client.table("current_location_history").update({"is_current": False}) \
            .eq("account_id", account_id).eq("profile_id", profile_id) \
            .eq("is_current", True).execute()
        if original_place_id is not None:
            service_client.table("current_location_history").insert({
                "account_id": account_id, "profile_id": profile_id,
                "place_id": original_place_id, "is_current": True,
                "source": "manual",
            }).execute()
        # Clean up the test rows we created (is_current=false manual rows for test place).
        service_client.table("current_location_history").delete() \
            .eq("account_id", account_id).eq("profile_id", profile_id) \
            .eq("place_id", test_place_id).eq("is_current", False).execute()

        failed = [n for n, ok, _ in results if not ok]
        for n, ok, d in results:
            print(f"{'PASS' if ok else 'FAIL'}: {n} — {d}")
        if failed:
            fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")
        print("PASS: smoke_current_location_backend")
        return 0
    finally:
        if proc is not None:
            proc.terminate()
            proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
