#!/usr/bin/env python3
"""Smoke: Web 2.0 shell Context Transport Contract (hash route + query params).

Journeys:
  * Dashboard → Chart Record → Map
  * Favorite → Map
  * Saved exploration → Map
  * Comparison → Map → Return (returnTo)

Run:
  ./venv/bin/python scripts/smoke_app_shell_context_transport.py
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
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
PYTHON = ROOT / "venv" / "bin" / "python"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


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
        env={**os.environ, "RM_APP_SHELL": "1"},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def ensure_server() -> tuple[str, subprocess.Popen | None]:
    base = BASE
    proc: subprocess.Popen | None = None
    try:
        with urllib.request.urlopen(f"{base}/health", timeout=2) as resp:
            if resp.status != 200:
                raise OSError("bad health")
        with urllib.request.urlopen(f"{base}/local-product-store.json", timeout=2) as resp:
            if resp.status != 200:
                raise OSError("store missing")
    except Exception:
        alt = 8012
        if not port_free(alt):
            fail(f"Server/store unavailable at {base} and port {alt} busy")
        proc = spawn_server(alt)
        base = f"http://127.0.0.1:{alt}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")
    return base, proc


def parse_shell_hash(raw_hash: str) -> dict[str, str | None]:
    fragment = raw_hash.lstrip("#")
    if not fragment.startswith("/"):
        fragment = "/" + fragment
    parsed = urlparse(fragment)
    route = (parsed.path or "/dashboard").lstrip("/").split("/")[0] or "dashboard"
    qs = parse_qs(parsed.query, keep_blank_values=False)
    return {
        "route": route,
        "chartRecordId": (qs.get("chartRecordId") or [None])[0],
        "placeId": (qs.get("placeId") or [None])[0],
        "explorationId": (qs.get("explorationId") or [None])[0],
        "comparisonSetId": (qs.get("comparisonSetId") or [None])[0],
        "returnTo": unquote((qs.get("returnTo") or [None])[0]) if qs.get("returnTo") else None,
    }


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        fail(f"playwright required: {exc}")

    base, proc = ensure_server()
    results: list[tuple[str, bool, str]] = []

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1100, "height": 900})

            def ctx():
                return page.evaluate("() => ({ ...window.__rmAppShell.navContext })")

            page.goto(f"{base}/app_shell.html#/dashboard", wait_until="domcontentloaded", timeout=20_000)
            page.wait_for_function(
                "() => window.__rmAppShell && window.__rmAppShell.viewModel()",
                timeout=15_000,
            )
            page.wait_for_selector('button[data-chart-record="cr-anna-rivera"]', timeout=10_000)

            # Dashboard → Chart Record → Map
            page.click('button[data-nav="chart-record"][data-chart-record="cr-anna-rivera"]')
            page.wait_for_function(
                "() => window.__rmAppShell.navContext.route === 'chart-record'"
                " && window.__rmAppShell.navContext.chartRecordId === 'cr-anna-rivera'",
                timeout=10_000,
            )
            page.click('button[data-action="open-map-record"]')
            page.wait_for_function(
                "() => window.__rmAppShell.navContext.route === 'map'"
                " && window.__rmAppShell.navContext.chartRecordId === 'cr-anna-rivera'",
                timeout=10_000,
            )
            h1 = parse_shell_hash(page.evaluate("() => location.hash"))
            ok1 = (
                h1["route"] == "map"
                and h1["chartRecordId"] == "cr-anna-rivera"
                and "chartRecordId=cr-anna-rivera" in page.evaluate("() => location.hash")
            )
            results.append(("dashboard_chart_record_map", ok1, json.dumps(h1)))

            # Favorite → Map
            page.goto(
                f"{base}/app_shell.html#/chart-record?chartRecordId=cr-anna-rivera",
                wait_until="domcontentloaded",
            )
            page.wait_for_function("() => window.__rmAppShell.viewModel()", timeout=15_000)
            page.wait_for_selector('button[data-action="open-map-favorite"][data-place-id="place_portland"]', timeout=10_000)
            page.click('button[data-action="open-map-favorite"][data-place-id="place_portland"]')
            page.wait_for_function(
                "() => window.__rmAppShell.navContext.route === 'map'"
                " && window.__rmAppShell.navContext.placeId === 'place_portland'",
                timeout=10_000,
            )
            h2 = parse_shell_hash(page.evaluate("() => location.hash"))
            ok2 = h2["placeId"] == "place_portland" and h2["chartRecordId"] == "cr-anna-rivera"
            results.append(("favorite_to_map", ok2, json.dumps(h2)))

            # Exploration → Map
            page.goto(f"{base}/app_shell.html#/chart-record?chartRecordId=cr-anna-rivera", wait_until="domcontentloaded")
            page.wait_for_function("() => window.__rmAppShell.viewModel()", timeout=15_000)
            page.click('button[data-action="resume-exploration"][data-exploration="exp-a1"]')
            page.wait_for_function(
                "() => window.__rmAppShell.navContext.route === 'map'"
                " && window.__rmAppShell.navContext.explorationId === 'exp-a1'",
                timeout=10_000,
            )
            h3 = parse_shell_hash(page.evaluate("() => location.hash"))
            ok3 = h3["explorationId"] == "exp-a1" and h3["chartRecordId"] == "cr-anna-rivera"
            results.append(("exploration_to_map", ok3, json.dumps(h3)))

            # Comparison → Map → Return
            page.click('button[data-nav="compare"]')
            page.wait_for_function(
                "() => window.__rmAppShell.navContext.route === 'compare'"
                " && window.__rmAppShell.navContext.comparisonSetId === 'cmp_anna_001'",
                timeout=10_000,
            )
            h4 = parse_shell_hash(page.evaluate("() => location.hash"))
            ok4 = h4["comparisonSetId"] == "cmp_anna_001" and h4.get("returnTo")
            page.click('button[data-action="compare-back-map"]')
            page.wait_for_function(
                "() => window.__rmAppShell.navContext.route === 'map'"
                " && window.__rmAppShell.navContext.chartRecordId === 'cr-anna-rivera'",
                timeout=10_000,
            )
            after = ctx()
            h5 = parse_shell_hash(page.evaluate("() => location.hash"))
            ok5 = (
                after.get("route") == "map"
                and after.get("chartRecordId") == "cr-anna-rivera"
                and after.get("explorationId") == "exp-a1"
                and after.get("returnTo") is None
            )
            results.append(("compare_to_map_return", ok4 and ok5, json.dumps({"compare": h4, "return": h5, "ctx": after})))

            contract_ok = page.evaluate(
                """() => {
                  const c = window.__rmAppShell.ROUTE_CONTEXT_CONTRACT;
                  return c.map.chartRecordId === 'required'
                    && c.compare.comparisonSetId === 'required'
                    && window.__rmAppShell.CONTEXT_TRANSPORT_STRATEGY === 'hash-route-query';
                }"""
            )
            results.append(("contract_surface", contract_ok, "ROUTE_CONTEXT_CONTRACT exported"))

            browser.close()

        failed = [name for name, ok, _ in results if not ok]
        for name, ok, detail in results:
            print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
        if failed:
            fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")
        print("PASS: smoke_app_shell_context_transport")
        return 0
    finally:
        if proc is not None:
            proc.terminate()
            proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
