#!/usr/bin/env python3
"""Read-only smoke: app_shell.html loads Store v3 scaffold via GET /local-product-store.json.

Verifies:
  * /app_shell.html and /local-product-store.json return 200
  * Store JSON has 3 Chart Records and default cr-anna-rivera
  * Shell browser hook loads view model from store (no demo fallback)
  * Jordan uncertainty, favorites, explorations, comparison set resolve
  * No write endpoints exercised
  * /map_CURRENT.html still 200
  * RM_APP_SHELL=0 disables app_shell + store read on temp server

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
        if st_probe != 200 or st_chart_records != 200:
            alt_port = 8010
            if port_free(alt_port):
                proc = spawn_server(alt_port, {**os.environ, "RM_APP_SHELL": "1"})
                base = f"http://127.0.0.1:{alt_port}"
                if not wait_server(base):
                    proc.terminate()
                    fail(f"Store/chart-records missing on {BASE}; temp server failed on {base}")
            else:
                fail(
                    f"{STORE_PATH}={st_probe} /chart-records={st_chart_records} on {base} "
                    f"and port {alt_port} busy"
                )

    try:
        st_shell, shell_body = fetch_status(base, "/app_shell.html")
        ok = st_shell == 200 and b"adaptStoreToView" in shell_body and b"/local-product-store.json" in shell_body
        results.append(("app_shell_html_200", ok, f"status={st_shell}"))

        # 2. store JSON endpoint
        st_store, store_bytes = fetch_status(base, STORE_PATH)
        ok = st_store == 200
        results.append(("store_json_200", ok, f"status={st_store}"))

        if st_store != 200:
            fail(f"{STORE_PATH} returned {st_store}")

        store = json.loads(store_bytes.decode())

        # 3. three Chart Records
        clients = store.get("clients") or []
        ok = len(clients) == 3
        results.append(("three_chart_records", ok, f"count={len(clients)}"))

        # 4. default_chart_record_id
        default_id = (store.get("user_settings") or {}).get("default_chart_record_id")
        ok = default_id == "cr-anna-rivera"
        results.append(("default_chart_record_anna", ok, f"default={default_id!r}"))

        # 5–9. store-side resolution checks (mirror shell adapters)
        places = {p["id"]: p for p in store.get("places") or []}
        bps = {b["id"]: b for b in store.get("birth_profiles") or []}
        jordan = next(c for c in clients if c["id"] == "cr-jordan-lee")
        jbp = bps[jordan["birth_profile_id"]]
        meta = jbp.get("confidence_metadata") or {}
        ok = jbp.get("birth_time") is None and "9:47 AM" in meta.get("time_range_display", "")
        results.append(("jordan_uncertainty_metadata", ok, str(meta)))

        favs = [f for f in store.get("favorite_cities") or [] if f.get("client_id") == "cr-anna-rivera"]
        ok = len(favs) == 3 and all(places[f["place_id"]]["display_name"] for f in favs)
        results.append(("anna_favorites_resolve", ok, f"count={len(favs)}"))

        exps = [i for i in store.get("saved_investigations") or [] if i.get("client_id") == "cr-anna-rivera"]
        ok = len(exps) >= 2 and any(i.get("id") == "exp-a1" for i in exps)
        results.append(("anna_explorations_resolve", ok, f"count={len(exps)}"))

        cmp_sets = store.get("comparison_sets") or []
        ok = len(cmp_sets) >= 1 and len(cmp_sets[0].get("place_ids") or []) in range(2, 6)
        cmp_names = [places[pid]["display_name"] for pid in cmp_sets[0]["place_ids"]] if cmp_sets else []
        results.append(("comparison_set_resolves", ok, f"places={cmp_names}"))

        # 10. no write routes in this smoke (read-only GETs only)
        results.append(("no_writes_exercised", True, "GET only"))

        # 11. map still serves
        st_map, _ = fetch_status(base, "/map_CURRENT.html")
        ok = st_map == 200
        results.append(("map_current_200", ok, f"status={st_map}"))

        st_cr, _ = fetch_status(base, "/chart-records")
        ok = st_cr == 200
        results.append(("chart_records_api_200", ok, f"status={st_cr}"))

        # Browser hook: shell loads store view model
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
                page.goto(f"{base}/app_shell.html", wait_until="domcontentloaded", timeout=20_000)
                page.wait_for_function(
                    "() => window.__rmAppShell && window.__rmAppShell.viewModel()",
                    timeout=15_000,
                )
                hooks = page.evaluate(
                    """() => {
                      const vm = window.__rmAppShell.viewModel();
                      const anna = vm.chartRecords.find(r => r.chartRecordId === 'cr-anna-rivera');
                      const jordan = vm.chartRecords.find(r => r.chartRecordId === 'cr-jordan-lee');
                      return {
                        recordCount: vm.chartRecords.length,
                        defaultId: vm.defaultChartRecordId,
                        annaFavorites: anna?.favorites?.length || 0,
                        annaExplorations: anna?.explorations?.length || 0,
                        jordanUncertainty: !!jordan?.hasTimeUncertainty,
                        annaEngineOk: anna?.engineBirth?.ok === true,
                        jordanEngineBlocked: jordan?.engineBirth?.ok === false
                          && jordan?.engineBirth?.reason === 'birth_time_required',
                        comparisonPlaces: vm.comparisonSets[0]?.placeNames || [],
                        loadSource: vm.loadSource,
                        error: window.__rmAppShell.storeLoadError(),
                      };
                    }"""
                )
                page.goto(f"{base}/app_shell.html#/dashboard", wait_until="domcontentloaded", timeout=20_000)
                page.wait_for_function(
                    "() => window.__rmAppShell && window.__rmAppShell.viewModel()",
                    timeout=15_000,
                )
                page.click('button[data-action="open-map-default"]')
                page.wait_for_function(
                    "() => window.__rmAppShell.state.activeChartRecordId === 'cr-anna-rivera'",
                    timeout=10_000,
                )
                browser.close()
                browser_ok = (
                    hooks.get("recordCount") == 3
                    and hooks.get("defaultId") == "cr-anna-rivera"
                    and hooks.get("annaFavorites") == 3
                    and hooks.get("annaExplorations") == 2
                    and hooks.get("jordanUncertainty") is True
                    and hooks.get("annaEngineOk") is True
                    and hooks.get("jordanEngineBlocked") is True
                    and len(hooks.get("comparisonPlaces") or []) == 3
                    and hooks.get("loadSource") == "/local-product-store.json"
                    and not hooks.get("error")
                )
                browser_detail = json.dumps(hooks, sort_keys=True)
                results.append(("dashboard_open_map_uses_anna", True, "activeChartRecordId=cr-anna-rivera"))

        results.append(("shell_loads_store_view_model", browser_ok, browser_detail))

        # 12. RM_APP_SHELL=0 disables routes (temp server)
        disabled_port = 8011
        if port_free(disabled_port):
            disabled_proc = spawn_server(
                disabled_port,
                {**os.environ, "RM_APP_SHELL": "0", "RM_PHASE3_LOCAL_PRODUCT": "0"},
            )
            disabled_base = f"http://127.0.0.1:{disabled_port}"
            try:
                if wait_server(disabled_base):
                    st_a, _ = fetch_status_on(disabled_base, "/app_shell.html")
                    st_b, _ = fetch_status_on(disabled_base, STORE_PATH)
                    ok = st_a == 404 and st_b == 404
                    results.append(("rm_app_shell_zero_disables", ok, f"shell={st_a} store={st_b}"))
                else:
                    results.append(("rm_app_shell_zero_disables", False, "temp server failed"))
            finally:
                disabled_proc.terminate()
                disabled_proc.wait(timeout=5)
        else:
            results.append(("rm_app_shell_zero_disables", False, f"port {disabled_port} busy"))

        # 13. no renderer changes asserted by scope (manual guard — this script touches none)

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


def fetch_status_on(base: str, path: str) -> tuple[int, bytes]:
    req = urllib.request.Request(f"{base}{path}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read()


if __name__ == "__main__":
    raise SystemExit(main())
