#!/usr/bin/env python3
"""Read-only smoke: Chart Record library summary API (Store v3).

Verifies:
  * GET /chart-records returns 3 summaries
  * GET /chart-records/cr-anna-rivera → engineBirth.ok, birth_hour_utc ≈ 12.7
  * GET /chart-records/cr-jordan-lee → engineBirth blocked (birth_time_required)
  * Unknown id → 404
  * No write routes exercised

Run:
  ./venv/bin/python scripts/smoke_chart_record_library_read.py
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
PYTHON = ROOT / "venv" / "bin" / "python"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def fetch_json(base: str, path: str) -> tuple[int, object]:
    req = urllib.request.Request(f"{base}{path}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as err:
        body = err.read().decode()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = body
        return err.code, payload


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


def spawn_server(port: int) -> subprocess.Popen:
    return subprocess.Popen(
        [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def fetch_status(base: str, path: str) -> int:
    req = urllib.request.Request(f"{base}{path}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status
    except urllib.error.HTTPError as err:
        return err.code


def ensure_server() -> tuple[str, subprocess.Popen | None]:
    proc: subprocess.Popen | None = None
    base = BASE
    if fetch_status(base, "/health") != 200:
        alt = 8016
        if not port_free(alt):
            fail(f"Server unavailable at {BASE} and port {alt} busy")
        proc = spawn_server(alt)
        base = f"http://127.0.0.1:{alt}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")
        return base, proc

    st, _ = fetch_json(base, "/chart-records")
    if st != 200:
        alt = 8016
        if not port_free(alt):
            fail(f"/chart-records unavailable on {BASE} and port {alt} busy")
        proc = spawn_server(alt)
        base = f"http://127.0.0.1:{alt}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")
    return base, proc


def main() -> int:
    base, proc = ensure_server()
    results: list[tuple[str, bool, str]] = []

    try:
        st_list, list_payload = fetch_json(base, "/chart-records")
        records = (list_payload or {}).get("chartRecords") if isinstance(list_payload, dict) else None
        ids = {r.get("chartRecordId") for r in (records or []) if isinstance(r, dict)}
        ok_list = (
            st_list == 200
            and isinstance(records, list)
            and len(records) == 3
            and ids == {"cr-anna-rivera", "cr-jordan-lee", "cr-research-event"}
        )
        results.append(("list_three_chart_records", ok_list, json.dumps({"status": st_list, "ids": sorted(ids)})))

        st_anna, anna = fetch_json(base, "/chart-records/cr-anna-rivera")
        eb_anna = anna.get("engineBirth") if isinstance(anna, dict) else {}
        hour_utc = eb_anna.get("birth_hour_utc")
        ok_anna = (
            st_anna == 200
            and eb_anna.get("ok") is True
            and anna.get("displayName") == "Anna Rivera"
            and isinstance(hour_utc, (int, float))
            and abs(float(hour_utc) - 12.7) < 0.01
        )
        results.append((
            "anna_executable_summary",
            ok_anna,
            json.dumps({"status": st_anna, "engineBirth": eb_anna}),
        ))

        st_jordan, jordan = fetch_json(base, "/chart-records/cr-jordan-lee")
        eb_jordan = jordan.get("engineBirth") if isinstance(jordan, dict) else {}
        ok_jordan = (
            st_jordan == 200
            and eb_jordan.get("ok") is False
            and eb_jordan.get("reason") == "birth_time_required"
        )
        results.append((
            "jordan_blocked_summary",
            ok_jordan,
            json.dumps({"status": st_jordan, "engineBirth": eb_jordan}),
        ))

        st_missing, missing = fetch_json(base, "/chart-records/cr-does-not-exist")
        ok_missing = st_missing == 404
        results.append(("unknown_chart_record_404", ok_missing, json.dumps({"status": st_missing, "body": missing})))

        browser_ok = False
        browser_detail = "playwright not run"
        try:
            from playwright.sync_api import sync_playwright
        except Exception as exc:
            browser_detail = f"playwright unavailable: {exc}"
        else:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1100, "height": 800})
                page.goto(f"{base}/app_shell.html#/dashboard", wait_until="domcontentloaded", timeout=20_000)
                page.wait_for_function(
                    "() => window.__rmAppShell && window.__rmAppShell.viewModel()",
                    timeout=15_000,
                )
                dash_html = page.content()
                page.goto(
                    f"{base}/app_shell.html#/chart-record?chartRecordId=cr-jordan-lee",
                    wait_until="domcontentloaded",
                    timeout=20_000,
                )
                page.wait_for_function(
                    "() => window.__rmAppShell && window.__rmAppShell.viewModel()",
                    timeout=15_000,
                )
                jordan_html = page.content()
                page.goto(
                    f"{base}/app_shell.html#/map?chartRecordId=cr-anna-rivera&explorationId=exp-a1",
                    wait_until="domcontentloaded",
                    timeout=20_000,
                )
                page.wait_for_function(
                    "() => window.__rmAppShell && window.__rmAppShell.viewModel()",
                    timeout=15_000,
                )
                map_html = page.content()
                browser.close()
                stub = "Resume passes context only; saved conditions not replayed on map (v1)."
                browser_ok = (
                    "Engine: executable" in dash_html
                    and "Engine: blocked — birth_time_required" in jordan_html
                    and stub in dash_html
                    and stub in map_html
                )
                browser_detail = json.dumps({
                    "dash_executable": "Engine: executable" in dash_html,
                    "jordan_blocked": "Engine: blocked — birth_time_required" in jordan_html,
                    "resume_stub_dash": stub in dash_html,
                    "resume_stub_map": stub in map_html,
                })

        results.append(("shell_truth_panel_labels", browser_ok, browser_detail))

        failed = [name for name, ok, _ in results if not ok]
        for name, ok, detail in results:
            print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")

        if failed:
            fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")

        print("PASS: smoke_chart_record_library_read")
        return 0
    finally:
        if proc is not None:
            proc.terminate()
            proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
