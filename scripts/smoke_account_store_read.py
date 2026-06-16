#!/usr/bin/env python3
"""Read-only smoke: GET /account-store returns Store v3 shape for authenticated user.

Verifies:
  * /health and /account-store (with Bearer JWT) return 200
  * Response top-level keys match supabase_store_bridge.js assembly
  * Row counts match direct build_account_store() for the same JWT
  * Unauthenticated request returns 401
  * No write endpoints exercised

Auth:
  * RM_SMOKE_JWT — use this Bearer token directly when set
  * else RM_SMOKE_EMAIL (default davidleongoodman@gmail.com) + admin magic-link OTP
    (requires SUPABASE_SERVICE_ROLE_KEY in environment)

Run (server at BASE_URL, default http://127.0.0.1:8004):
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_account_store_read.py
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

EXPECTED_TOP_LEVEL_KEYS = {
    "_storage",
    "_warning",
    "birth_profiles",
    "chart_record_history",
    "clients",
    "comparison_sets",
    "favorite_cities",
    "notes",
    "places",
    "professional_account",
    "saved_investigations",
    "storage_schema_version",
    "supabase_mirror_version",
    "tags",
    "user_settings",
}

COUNT_KEYS = (
    "clients",
    "birth_profiles",
    "places",
    "favorite_cities",
    "comparison_sets",
    "saved_investigations",
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def fetch_status(base: str, path: str, headers: dict | None = None, timeout: int = 30):
    req = urllib.request.Request(f"{base}{path}", headers=headers or {})
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
        [
            str(PYTHON),
            "-m",
            "uvicorn",
            "main_centerline_FIXER:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def resolve_jwt() -> str:
    token = os.environ.get("RM_SMOKE_JWT", "").strip()
    if token:
        return token

    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()
    url = os.environ.get("SUPABASE_URL", "")
    anon = os.environ.get("SUPABASE_ANON_KEY", "")
    service = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon, service]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY or RM_SMOKE_JWT")

    from supabase import create_client

    admin = create_client(url, service)
    anon_client = create_client(url, anon)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    otp = link.properties.email_otp
    session = anon_client.auth.verify_otp(
        {"email": email, "token": otp, "type": "email"}
    )
    if not session.session:
        fail(f"Could not obtain JWT for {email}")
    return session.session.access_token


def main() -> int:
    base = BASE
    proc: subprocess.Popen | None = None

    status_health, _ = fetch_status(base, "/health")
    status_probe, _ = fetch_status(base, "/account-store")

    if status_health != 200:
        alt_port = 8014
        if not port_free(alt_port):
            fail(f"Server not reachable at {base} and port {alt_port} busy")
        proc = spawn_server(alt_port, dict(os.environ))
        base = f"http://127.0.0.1:{alt_port}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")
    elif status_probe == 404:
        alt_port = 8014
        if port_free(alt_port):
            proc = spawn_server(alt_port, dict(os.environ))
            base = f"http://127.0.0.1:{alt_port}"
            if not wait_server(base):
                proc.terminate()
                fail(
                    f"/account-store missing on {BASE}; temp server failed on {base}"
                )
        else:
            fail(
                f"/account-store returned 404 on {base}; restart server to pick up route"
            )

    results: list[tuple[str, bool, str]] = []

    try:
        jwt = resolve_jwt()
        from repositories.account_store_repository import build_account_store

        direct = build_account_store(jwt)
        headers = {"Authorization": f"Bearer {jwt}"}

        st, body = fetch_status(base, "/account-store", headers=headers, timeout=60)
        ok = st == 200
        results.append(("account_store_200", ok, f"status={st}"))
        if st != 200:
            fail(f"/account-store returned {st}: {body[:300]!r}")

        store = json.loads(body.decode())
        ok = set(store.keys()) == EXPECTED_TOP_LEVEL_KEYS
        results.append(("top_level_keys", ok, str(sorted(store.keys()))))

        for key in COUNT_KEYS:
            direct_n = len(direct.get(key) or [])
            api_n = len(store.get(key) or [])
            ok = direct_n == api_n
            results.append((f"count_{key}", ok, f"direct={direct_n} api={api_n}"))

        st_unauth, _ = fetch_status(base, "/account-store")
        ok = st_unauth == 401
        results.append(("unauthenticated_401", ok, f"status={st_unauth}"))

        failed = [name for name, ok, _ in results if not ok]
        for name, ok, detail in results:
            mark = "PASS" if ok else "FAIL"
            print(f"{mark}: {name} — {detail}")

        if failed:
            fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")

        print("PASS: smoke_account_store_read")
        return 0
    finally:
        if proc is not None:
            proc.terminate()
            proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
