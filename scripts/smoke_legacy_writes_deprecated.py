#!/usr/bin/env python3
"""Smoke: legacy service-role write routes return 410 Gone.

Each retired write route must respond with HTTP 410 and detail.error == "deprecated"
before any database write. Safe to run repeatedly (no side effects).

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_legacy_writes_deprecated.py
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
PORT = 8004
DUMMY = "00000000-0000-4000-8000-000000000001"

LEGACY_WRITE_ROUTES: list[tuple[str, str, dict | None]] = [
    ("POST", "/profiles", {"display_name": "smoke", "account_user_id": DUMMY}),
    ("PATCH", f"/profiles/{DUMMY}", {"display_name": "smoke"}),
    ("POST", f"/profiles/{DUMMY}/archive", None),
    ("POST", "/birth-records", {"profile_id": DUMMY}),
    ("PATCH", f"/birth-record/{DUMMY}", {}),
    ("POST", f"/birth-record/{DUMMY}/archive", None),
    ("POST", "/saved-searches", {"profile_id": DUMMY, "title": "smoke"}),
    ("PATCH", f"/saved-search/{DUMMY}", {"title": "smoke"}),
    ("POST", f"/saved-search/{DUMMY}/archive", None),
    ("POST", "/comparison-sets", {"profile_id": DUMMY, "title": "smoke"}),
    ("PATCH", f"/comparison-set/{DUMMY}", {"title": "smoke"}),
    ("POST", f"/comparison-set/{DUMMY}/archive", None),
    ("POST", f"/comparison-set/{DUMMY}/places", {"place_id": DUMMY}),
    ("DELETE", f"/comparison-set/{DUMMY}/places/{DUMMY}", None),
    ("POST", "/favorite-places", {"profile_id": DUMMY, "place_id": DUMMY}),
    ("PATCH", f"/favorite-place/{DUMMY}", {"label": "smoke"}),
    ("POST", f"/favorite-place/{DUMMY}/archive", None),
    ("POST", "/visited-places", {"profile_id": DUMMY, "place_id": DUMMY}),
    ("POST", "/notes", {"profile_id": DUMMY, "target_type": "chart_record", "body": "smoke"}),
    ("PATCH", f"/note/{DUMMY}", {"body": "smoke"}),
    ("POST", f"/note/{DUMMY}/archive", None),
    ("POST", "/user-settings", {"account_user_id": DUMMY, "settings_json": {}}),
    ("PATCH", f"/user-settings/{DUMMY}", {"settings_json": {}}),
    ("POST", "/share-links", {
        "profile_id": DUMMY,
        "target_type": "chart_record",
        "target_id": DUMMY,
        "slug": "smoke-legacy",
    }),
    ("POST", f"/share-link/{DUMMY}/revoke", None),
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def fetch(base, path, method="GET", body=None, timeout=15):
    data = json.dumps(body).encode() if body is not None else None
    hdrs = {}
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
        st, body = fetch(
            base,
            "/profiles",
            method="POST",
            body={"display_name": "x", "account_user_id": DUMMY},
            timeout=3,
        )
    except Exception:
        return None
    if st != 410:
        return False
    try:
        detail = json.loads(body.decode()).get("detail", {})
    except Exception:
        return False
    return detail.get("error") == "deprecated"


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


def assert_deprecated_410(name, status, raw_body):
    if status != 410:
        return False, f"status={status}"
    try:
        payload = json.loads(raw_body.decode())
    except Exception as exc:
        return False, f"invalid json: {exc}"
    detail = payload.get("detail")
    if not isinstance(detail, dict):
        return False, f"detail type={type(detail).__name__}"
    if detail.get("error") != "deprecated":
        return False, f"error={detail.get('error')!r}"
    if "replacement" not in detail:
        return False, "missing replacement key"
    return True, f"replacement={detail.get('replacement')!r}"


def main() -> int:
    base = f"http://127.0.0.1:{PORT}"
    proc = None
    present = route_present(base)
    if present is not True:
        if present is False:
            fail(
                f"port {PORT} is serving a build without legacy-write 410 quarantine; "
                "restart that server with the updated main_centerline_FIXER.py"
            )
        if not port_free(PORT):
            fail(f"port {PORT} is occupied but not responding with 410 on POST /profiles")
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
            proc.kill()
            fail(f"server on port {PORT} did not become healthy")
    else:
        print(f"using existing server on port {PORT}")

    results: list[tuple[str, bool, str]] = []
    try:
        for method, path, body in LEGACY_WRITE_ROUTES:
            label = f"{method} {path}"
            status, raw = fetch(base, path, method=method, body=body)
            ok, detail = assert_deprecated_410(label, status, raw)
            results.append((label, ok, detail))
    finally:
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()

    failed = [name for name, ok, _ in results if not ok]
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
    passed = len(results) - len(failed)
    print(f"Summary: {passed}/{len(results)} deprecated routes return 410")
    if failed:
        fail(f"{len(failed)} route(s) failed: {', '.join(failed)}")
    print("PASS: smoke_legacy_writes_deprecated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
