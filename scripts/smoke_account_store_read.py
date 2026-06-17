#!/usr/bin/env python3
"""Read-only smoke: GET /account-store is quarantined (HTTP 410 Gone).

Verifies:
  * /health returns 200
  * /account-store returns 410 with legacy-read quarantine body (auth or unauth)
  * No write endpoints exercised

Run (server at BASE_URL, default http://127.0.0.1:8004):
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

QUARANTINE_BODY = {"error": "Gone", "reason": "legacy read path retired"}


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


def assert_quarantine_410(name: str, status: int, raw_body: bytes) -> tuple[bool, str]:
    if status != 410:
        return False, f"status={status}"
    try:
        body = json.loads(raw_body.decode())
    except json.JSONDecodeError:
        return False, f"non-json body: {raw_body[:200]!r}"
    ok = body == QUARANTINE_BODY
    return ok, json.dumps(body)


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
    elif status_probe != 410:
        alt_port = 8014
        if port_free(alt_port):
            proc = spawn_server(alt_port, dict(os.environ))
            base = f"http://127.0.0.1:{alt_port}"
            if not wait_server(base):
                proc.terminate()
                fail(
                    f"/account-store not quarantined on {BASE}; temp server failed on {base}"
                )
        else:
            fail(
                f"/account-store returned {status_probe} on {base} (expected 410); "
                f"restart server to pick up quarantine"
            )

    results: list[tuple[str, bool, str]] = []

    try:
        st_health, _ = fetch_status(base, "/health")
        results.append(("health_200", st_health == 200, f"status={st_health}"))

        st, body = fetch_status(base, "/account-store")
        ok, detail = assert_quarantine_410("account_store", st, body)
        results.append(("account_store_410", ok, detail))

        st_auth, body_auth = fetch_status(
            base,
            "/account-store",
            headers={"Authorization": "Bearer smoke-token"},
        )
        ok_auth, detail_auth = assert_quarantine_410("account_store_auth", st_auth, body_auth)
        results.append(("account_store_auth_410", ok_auth, detail_auth))

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
