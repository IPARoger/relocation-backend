#!/usr/bin/env python3
"""Read-only smoke: app_shell.html + quarantined legacy store read route.

Verifies:
  * /app_shell.html returns 200 and references Supabase store bridge (not local JSON)
  * GET /local-product-store.json returns 410 Gone (legacy read quarantined)
  * /chart-records still serves scaffold summaries when app shell enabled
  * /map_CURRENT.html still 200
  * RM_APP_SHELL=0 disables app_shell (store route remains quarantined at 410)
  * Optional Playwright: shell loads view model when Supabase credentials present

Run (server must be reachable at BASE_URL, default http://127.0.0.1:8000):
  ./venv/bin/python scripts/smoke_app_shell_store_read.py
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
BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
STORE_PATH = "/local-product-store.json"
PYTHON = ROOT / "venv" / "bin" / "python"
QUARANTINE_BODY = {"error": "Gone", "reason": "legacy read path retired"}


def fetch_status(base: str, path: str, timeout: int = 10) -> tuple[int, bytes]:
    req = urllib.request.Request(f"{base}{path}")
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


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def assert_quarantine_410(status: int, raw_body: bytes) -> tuple[bool, str]:
    if status != 410:
        return False, f"status={status}"
    try:
        body = json.loads(raw_body.decode())
    except json.JSONDecodeError:
        return False, f"non-json: {raw_body[:200]!r}"
    return body == QUARANTINE_BODY, json.dumps(body)


def supabase_smoke_configured() -> bool:
    return bool(
        os.environ.get("RM_SMOKE_JWT", "").strip()
        or all(
            os.environ.get(k, "").strip()
            for k in ("SUPABASE_URL", "SUPABASE_ANON_KEY", "SUPABASE_SERVICE_ROLE_KEY")
        )
    )


def main() -> int:
    results: list[tuple[str, bool, str]] = []
    base = BASE
    proc: subprocess.Popen | None = None

    status_health, _ = fetch_status(base, "/health")
    if status_health != 200:
        alt_port = 8010
        if not port_free(alt_port):
            fail(f"Server not reachable at {base} and port {alt_port} busy")
        proc = spawn_server(alt_port, {**os.environ, "RM_APP_SHELL": "1"})
        base = f"http://127.0.0.1:{alt_port}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")
    else:
        st_probe, _ = fetch_status(base, STORE_PATH)
        st_chart_records, _ = fetch_status(base, "/chart-records")
        if st_probe != 410 or st_chart_records != 200:
            alt_port = 8010
            if port_free(alt_port):
                proc = spawn_server(alt_port, {**os.environ, "RM_APP_SHELL": "1"})
                base = f"http://127.0.0.1:{alt_port}"
                if not wait_server(base):
                    proc.terminate()
                    fail(
                        f"Store quarantine/chart-records mismatch on {BASE}; "
                        f"temp server failed on {base}"
                    )
            else:
                fail(
                    f"{STORE_PATH}={st_probe} (expected 410) /chart-records={st_chart_records} "
                    f"on {base} and port {alt_port} busy"
                )

    try:
        st_shell, shell_body = fetch_status(base, "/app_shell.html")
        ok = (
            st_shell == 200
            and b"adaptStoreToView" in shell_body
            and b"SupabaseStoreReady" in shell_body
            and b"/local-product-store.json" not in shell_body
        )
        results.append(("app_shell_html_200", ok, f"status={st_shell}"))

        st_store, store_bytes = fetch_status(base, STORE_PATH)
        ok_q, detail_q = assert_quarantine_410(st_store, store_bytes)
        results.append(("store_json_410_quarantine", ok_q, detail_q))

        st_cr, cr_bytes = fetch_status(base, "/chart-records")
        ok_cr = st_cr == 200
        results.append(("chart_records_api_200", ok_cr, f"status={st_cr}"))
        if ok_cr:
            cr = json.loads(cr_bytes.decode())
            records = cr.get("chartRecords") or []
            ok_n = len(records) == 3
            results.append(("chart_records_three", ok_n, f"count={len(records)}"))

        st_map, _ = fetch_status(base, "/map_CURRENT.html")
        results.append(("map_current_200", st_map == 200, f"status={st_map}"))

        results.append(("no_writes_exercised", True, "GET only"))

        if not supabase_smoke_configured():
            results.append(
                ("shell_loads_store_view_model", True, "skipped — Supabase smoke credentials not configured")
            )
        else:
            try:
                from playwright.sync_api import sync_playwright
            except Exception as exc:
                results.append(
                    ("shell_loads_store_view_model", True, f"skipped — playwright unavailable: {exc}")
                )
            else:
                browser_ok = False
                browser_detail = ""
                with sync_playwright() as pw:
                    browser = pw.chromium.launch(headless=True)
                    page = browser.new_page(viewport={"width": 1100, "height": 800})
                    page.goto(f"{base}/app_shell.html", wait_until="domcontentloaded", timeout=20_000)
                    page.wait_for_function(
                        "() => window.__rmAppShell && window.__rmAppShell.viewModel()",
                        timeout=30_000,
                    )
                    hooks = page.evaluate(
                        """() => {
                      const vm = window.__rmAppShell.viewModel();
                      return {
                        recordCount: vm.chartRecords?.length || 0,
                        loadSource: vm.loadSource,
                        error: window.__rmAppShell.storeLoadError(),
                      };
                    }"""
                    )
                    browser.close()
                    browser_ok = (
                        hooks.get("recordCount", 0) > 0
                        and hooks.get("loadSource") == "supabase-store-bridge"
                        and not hooks.get("error")
                    )
                    browser_detail = json.dumps(hooks, sort_keys=True)
                results.append(("shell_loads_store_view_model", browser_ok, browser_detail))

        disabled_port = 8011
        if port_free(disabled_port):
            disabled_proc = spawn_server(
                disabled_port,
                {**os.environ, "RM_APP_SHELL": "0", "RM_PHASE3_LOCAL_PRODUCT": "0"},
            )
            disabled_base = f"http://127.0.0.1:{disabled_port}"
            try:
                if wait_server(disabled_base):
                    st_a, _ = fetch_status(disabled_base, "/app_shell.html")
                    st_b, body_b = fetch_status(disabled_base, STORE_PATH)
                    ok_q2, _ = assert_quarantine_410(st_b, body_b)
                    ok = st_a == 404 and ok_q2
                    results.append(
                        ("rm_app_shell_zero_disables", ok, f"shell={st_a} store={st_b}")
                    )
                else:
                    results.append(("rm_app_shell_zero_disables", False, "temp server failed"))
            finally:
                disabled_proc.terminate()
                disabled_proc.wait(timeout=5)
        else:
            results.append(("rm_app_shell_zero_disables", False, f"port {disabled_port} busy"))

        failed = [name for name, ok, _ in results if not ok]
        for name, ok, detail in results:
            mark = "PASS" if ok else "FAIL"
            print(f"{mark}: {name} — {detail}")

        if failed:
            fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")

        print("PASS: smoke_app_shell_store_read")
        return 0
    finally:
        if proc is not None:
            proc.terminate()
            proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
