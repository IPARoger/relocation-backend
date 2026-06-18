#!/usr/bin/env python3
"""Smoke: signup bootstrap (handle_new_user trigger chain).

Verifies that creating a new auth.users row bootstraps required account records:
  * accounts row (Personal / personal / created_by = user id)
  * account_memberships row (owner, accepted_at set)
  * app_account_ids() returns the new account for the user's JWT
  * GET /profiles succeeds (empty list OK for new user)

Uses admin.create_user(email_confirm=True) — same auth.users INSERT path as
signUp() per Phase 6 closeout. Cleans up the disposable user and account rows.

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_signup_bootstrap.py
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

import httpx

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PYTHON = ROOT / "venv" / "bin" / "python"
MIGRATION = ROOT / "supabase/migrations/2026_06_13_phase6_signup_bootstrap.sql"
PORT = 8004
HTTP_TIMEOUT = httpx.Timeout(60.0, connect=30.0)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def fetch(base, path, headers=None, method="GET", body=None, timeout=30):
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


def make_clients(url, anon, svc):
    from supabase import create_client
    from supabase.client import ClientOptions

    http = httpx.Client(timeout=HTTP_TIMEOUT)
    opts = ClientOptions(httpx_client=http)
    return (
        create_client(url, svc, options=opts),
        create_client(url, anon, options=opts),
        http,
    )


def cleanup_bootstrap(admin, user_id, account_id):
    if user_id:
        try:
            admin.auth.admin.delete_user(user_id)
        except Exception:
            pass
    if user_id:
        try:
            admin.table("account_memberships").delete().eq("user_id", user_id).execute()
        except Exception:
            pass
    if account_id:
        try:
            admin.table("accounts").delete().eq("id", account_id).execute()
        except Exception:
            pass


def main() -> int:
    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon_key, service_key]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY")

    results = []

    results.append((
        "migration_file_present",
        MIGRATION.is_file(),
        str(MIGRATION),
    ))
    if not MIGRATION.is_file():
        fail(f"migration missing: {MIGRATION}")

    migration_text = MIGRATION.read_text()
    for needle in ("handle_new_user", "on_auth_user_created", "account_memberships"):
        ok = needle in migration_text
        results.append((f"migration_contains_{needle}", ok, needle))
        if not ok:
            fail(f"migration missing {needle}")

    admin, anon_client, http = make_clients(url, anon_key, service_key)
    user_id = None
    account_id = None

    base = f"http://127.0.0.1:{PORT}"
    proc = None
    try:
        try:
            with urllib.request.urlopen(base + "/health", timeout=2):
                pass
        except Exception:
            if not port_free(PORT):
                fail(f"port {PORT} occupied but /health unreachable")
            proc = subprocess.Popen(
                [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app",
                 "--host", "127.0.0.1", "--port", str(PORT)],
                cwd=str(ROOT), env=dict(os.environ),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            if not wait_health(base):
                proc.terminate()
                fail(f"temp server did not start on {base}")

        email = f"smoke-bootstrap-{uuid.uuid4().hex[:12]}@example.com"
        password = f"SmokeTest-{uuid.uuid4().hex[:16]}!"

        create_resp = admin.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
        })
        user_id = create_resp.user.id
        results.append(("auth_user_created", bool(user_id), f"user_id={user_id}"))
        if not user_id:
            fail("admin.create_user returned no user id")

        accounts = (
            admin.table("accounts")
            .select("id, name, account_type, created_by")
            .eq("created_by", user_id)
            .execute()
        ).data or []
        results.append(("accounts_row_created", len(accounts) == 1, f"count={len(accounts)}"))
        if len(accounts) != 1:
            fail(f"expected 1 accounts row, got {len(accounts)}")

        account = accounts[0]
        account_id = account["id"]
        results.append((
            "accounts_personal",
            account.get("name") == "Personal" and account.get("account_type") == "personal",
            json.dumps(account),
        ))

        mems = (
            admin.table("account_memberships")
            .select("account_id, user_id, role, accepted_at")
            .eq("user_id", user_id)
            .execute()
        ).data or []
        results.append(("membership_row_created", len(mems) == 1, f"count={len(mems)}"))
        if len(mems) != 1:
            fail(f"expected 1 account_memberships row, got {len(mems)}")

        mem = mems[0]
        results.append((
            "membership_owner_accepted",
            mem.get("role") == "owner"
            and mem.get("account_id") == account_id
            and bool(mem.get("accepted_at")),
            json.dumps(mem, default=str),
        ))

        signin = anon_client.auth.sign_in_with_password({"email": email, "password": password})
        token = signin.session.access_token if signin.session else None
        results.append(("sign_in_succeeds", bool(token), f"session={bool(signin.session)}"))
        if not token:
            fail("new user could not sign in")

        anon_client.postgrest.auth(token)
        rpc_ids = anon_client.rpc("app_account_ids").execute().data or []
        results.append((
            "app_account_ids_returns_account",
            account_id in rpc_ids,
            f"rpc={rpc_ids}",
        ))
        if account_id not in rpc_ids:
            fail(f"app_account_ids missing account {account_id}: {rpc_ids}")

        st, body = fetch(base, "/profiles", headers={"Authorization": f"Bearer {token}"})
        profiles_ok = st == 200
        profile_count = len(json.loads(body)) if profiles_ok else -1
        results.append((
            "get_profiles_200",
            profiles_ok,
            f"status={st} count={profile_count}",
        ))
        if not profiles_ok:
            fail(f"GET /profiles returned {st}")

    finally:
        cleanup_bootstrap(admin, user_id, account_id)
        http.close()
        if proc:
            proc.terminate()
            proc.wait(timeout=10)

    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
        if not ok:
            fail(name)

    print("PASS: smoke_signup_bootstrap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
