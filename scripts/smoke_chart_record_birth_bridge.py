#!/usr/bin/env python3
"""Smoke: Chart Record → engine birth resolution bridge.

Cases:
  B1  cr-anna-rivera product path → wire POST uses Store v3 birth (1990), not baseline profile
  B2  unknown chartRecordId → fail visible, no search-regions POST
  B3  cr-jordan-lee (null birth_time) → fail visible, no search-regions POST
  B4  GET /chart-records/{id}/engine-birth endpoint
  B5  Legacy direct map (no handoff) regression via smoke_map_current.py
  B6  v1 context handoff unchanged (no genie ref)
  B7  URL/payload chartRecordId mismatch → fail visible, zero POSTs
  B8  genieRenderRef without URL chartRecordId → chart_record_id_required_for_handoff

Run:
  ./venv/bin/python scripts/smoke_chart_record_birth_bridge.py
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


def ensure_server() -> tuple[str, subprocess.Popen | None]:
    proc: subprocess.Popen | None = None
    try:
        with urllib.request.urlopen(f"{BASE}/chart-records/cr-anna-rivera/engine-birth", timeout=2) as resp:
            if resp.status != 200:
                raise OSError("engine-birth unavailable")
    except Exception:
        alt = 8017
        if not port_free(alt):
            fail(f"Server unavailable at {BASE} and port {alt} busy")
        proc = spawn_server(alt)
        base = f"http://127.0.0.1:{alt}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")
        return base, proc
    return BASE, proc


def fetch_json(url: str) -> tuple[int, dict]:
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as err:
        body = err.read().decode()
        try:
            return err.code, json.loads(body)
        except json.JSONDecodeError:
            return err.code, {"raw": body}


class SearchRegionsRecorder:
    def __init__(self) -> None:
        self.posts: list[dict] = []

    def install(self, page) -> None:
        def handler(route) -> None:
            req = route.request
            if req.method == "POST" and "/search-regions" in req.url:
                raw = req.post_data or "{}"
                try:
                    self.posts.append(json.loads(raw))
                except json.JSONDecodeError:
                    self.posts.append({"_parse_error": raw[:200]})
            route.continue_()

        page.route("**/search-regions", handler)

    def clear(self) -> None:
        self.posts = []


def open_genie_drawer(page, base: str, chart_record_id: str) -> None:
    page.goto(
        f"{base}/app_shell.html#/map?chartRecordId={chart_record_id}",
        wait_until="domcontentloaded",
    )
    page.wait_for_function(
        "() => window.__rmAppShell && window.RelocationGenieVariableBuilder",
        timeout=15_000,
    )
    page.wait_for_selector("#genieDrawerMount #renderBtn", timeout=15_000)


def configure_sun_first(page) -> None:
    root = "#variableCards .variable-card:nth-child(1)"
    page.select_option(f"{root} [data-type-select]", "planet_in_house")
    page.select_option(f'{root} [data-field="body"]', "sun")
    page.select_option(f'{root} [data-field="house"]', "1")


def search_map_from_shell(page) -> None:
    page.click("#renderBtn")
    page.wait_for_url("**/map_CURRENT.html**", timeout=15_000)
    page.wait_for_function(
        "() => window.__rmMap && window.__rmGenieRenderHandoff",
        timeout=15_000,
    )


def wait_handoff_done(page, timeout_ms: int = 120_000) -> None:
    page.wait_for_function(
        """() => {
            const h = window.__rmGenieRenderHandoff?.();
            if (!h) return false;
            if (h.error && h.error !== 'no_executable_include_variables') return true;
            if (h.executed === true) return !document.getElementById('findBtn')?.disabled;
            return h.executed === false && (h.execution || h.error);
        }""",
        timeout=timeout_ms,
    )


def base_genie_payload(**overrides: object) -> dict:
    payload = {
        "schema_version": 1,
        "kind": "genie_render",
        "createdAt": "2026-05-30T12:00:00.000Z",
        "chartRecordId": "cr-anna-rivera",
        "variables": [
            {
                "id": "v1",
                "type": "planet_in_house",
                "polarity": "include",
                "enabled": True,
                "status": "complete",
                "label": "Planet · House",
                "fields": {"body": "sun", "house": 1},
            }
        ],
        "layerControls": {
            "mutedVariableIds": [],
            "soloVariableId": None,
            "excludeVariableIds": [],
        },
        "settingsSnapshot": {"transitModeEnabled": False, "registry": {}},
        "legacyCompatibility": {
            "schema_version": 1,
            "kind": "saved_investigation",
            "chart_id": "cr-anna-rivera",
            "house_conditions": [],
            "angle_sign_conditions": [],
            "aspect_overlay": None,
            "notExclusions": [],
            "degradation": {
                "canonicalVariableCount": 0,
                "legacyMappedCount": 0,
                "unmappedVariableIds": [],
                "warnings": [],
            },
        },
    }
    payload.update(overrides)
    return payload


def handoff_url(base: str, chart_record_id: str, ref: str) -> str:
    params = (
        f"skipOnboarding=1&handoff=app_shell&handoffCreatedAt=2026-05-30T12%3A00%3A00.000Z"
        f"&chartRecordId={chart_record_id}&genieRenderRef={ref}"
    )
    return f"{base}/map_CURRENT.html?{params}"


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        fail(f"playwright required: {exc}")

    base, proc = ensure_server()
    os.environ["BASE_URL"] = base
    results: list[tuple[str, bool, str]] = []

    # B4 — resolver endpoint (no browser)
    st_anna, anna = fetch_json(f"{base}/chart-records/cr-anna-rivera/engine-birth")
    ok_b4a = (
        st_anna == 200
        and anna.get("birth_year") == 1990
        and anna.get("birth_month") == 3
        and anna.get("birth_day") == 15
        and abs(float(anna.get("birth_hour_utc", 0)) - 12.7) < 0.01
    )
    st_miss, miss = fetch_json(f"{base}/chart-records/cr-does-not-exist/engine-birth")
    detail_miss = miss.get("detail") if isinstance(miss.get("detail"), dict) else miss
    ok_b4b = st_miss == 404 and detail_miss.get("error") == "chart_record_not_found"
    st_j, jordan = fetch_json(f"{base}/chart-records/cr-jordan-lee/engine-birth")
    detail_j = jordan.get("detail") if isinstance(jordan.get("detail"), dict) else jordan
    ok_b4c = st_j == 422 and detail_j.get("error") == "birth_time_required"
    results.append(("B4_resolver_endpoint", ok_b4a and ok_b4b and ok_b4c, json.dumps({
        "anna_status": st_anna,
        "missing_status": st_miss,
        "jordan_status": st_j,
    })))

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            recorder = SearchRegionsRecorder()
            recorder.install(page)

            # B1 — Anna product path birth on wire (no #chartProfile select)
            open_genie_drawer(page, base, "cr-anna-rivera")
            configure_sun_first(page)
            recorder.clear()
            search_map_from_shell(page)
            wait_handoff_done(page)
            handoff1 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            smoke1 = page.evaluate("() => window.__rmSmokeState()")
            wire1 = recorder.posts[0] if recorder.posts else {}
            ok_b1 = (
                handoff1
                and handoff1.get("executed") is True
                and smoke1.get("polygonLayers", 0) > 0
                and wire1.get("birth_year") == 1990
                and wire1.get("birth_month") == 3
                and wire1.get("birth_day") == 15
                and wire1.get("birth_year") != 1976
            )
            results.append(("B1_anna_product_path_birth", ok_b1, json.dumps({
                "executed": handoff1.get("executed") if handoff1 else None,
                "wire_birth": {
                    "birth_year": wire1.get("birth_year"),
                    "birth_month": wire1.get("birth_month"),
                    "birth_day": wire1.get("birth_day"),
                    "birth_hour_utc": wire1.get("birth_hour_utc"),
                },
                "polygons": smoke1.get("polygonLayers"),
            })))

            # B2 — unknown chart record
            ref2 = "bridge-smoke-unknown-ref"
            page.evaluate(
                """([ref, payload]) => {
                    sessionStorage.setItem('rm_genie_render:' + ref, JSON.stringify(payload));
                }""",
                [ref2, base_genie_payload(chartRecordId="cr-does-not-exist")],
            )
            recorder.clear()
            page.goto(handoff_url(base, "cr-does-not-exist", ref2), wait_until="domcontentloaded")
            page.wait_for_function(
                "() => window.__rmGenieRenderHandoff && window.__rmExecuteGenieRender",
                timeout=15_000,
            )
            wait_handoff_done(page, timeout_ms=30_000)
            handoff2 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            ok_b2 = (
                handoff2
                and handoff2.get("executed") is False
                and handoff2.get("error") == "chart_record_not_found"
                and len(recorder.posts) == 0
            )
            results.append(("B2_unknown_chart_record", ok_b2, json.dumps({
                "error": handoff2.get("error") if handoff2 else None,
                "posts": len(recorder.posts),
            })))

            # B3 — Jordan null birth_time
            ref3 = "bridge-smoke-jordan-ref"
            page.evaluate(
                """([ref, payload]) => {
                    sessionStorage.setItem('rm_genie_render:' + ref, JSON.stringify(payload));
                }""",
                [ref3, base_genie_payload(chartRecordId="cr-jordan-lee")],
            )
            recorder.clear()
            page.goto(handoff_url(base, "cr-jordan-lee", ref3), wait_until="domcontentloaded")
            page.wait_for_function(
                "() => window.__rmGenieRenderHandoff && window.__rmExecuteGenieRender",
                timeout=15_000,
            )
            wait_handoff_done(page, timeout_ms=30_000)
            handoff3 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            ok_b3 = (
                handoff3
                and handoff3.get("executed") is False
                and handoff3.get("error") == "birth_time_required"
                and len(recorder.posts) == 0
            )
            results.append(("B3_jordan_birth_time_required", ok_b3, json.dumps({
                "error": handoff3.get("error") if handoff3 else None,
                "posts": len(recorder.posts),
            })))

            # B6 — v1 handoff without genie ref
            page.goto(
                f"{base}/map_CURRENT.html?skipOnboarding=1&handoff=app_shell"
                "&handoffCreatedAt=2026-05-30T12%3A00%3A00.000Z&chartRecordId=cr-anna-rivera",
                wait_until="domcontentloaded",
            )
            page.wait_for_function("() => window.__rmAppShellHandoff", timeout=15_000)
            v1 = page.evaluate("() => window.__rmAppShellHandoff()")
            genie_ref = page.evaluate("() => new URLSearchParams(window.location.search).get('genieRenderRef')")
            ok_b6 = (
                v1
                and v1.get("chartRecordId") == "cr-anna-rivera"
                and genie_ref is None
                and page.evaluate("() => window.__rmGenieRenderHandoff()?.ref") is None
            )
            results.append(("B6_v1_handoff_unchanged", ok_b6, json.dumps({
                "handoff": v1,
                "genieRenderRef": genie_ref,
            })))

            # B7 — URL/payload chartRecordId mismatch
            ref7 = "bridge-smoke-mismatch-ref"
            page.evaluate(
                """([ref, payload]) => {
                    sessionStorage.setItem('rm_genie_render:' + ref, JSON.stringify(payload));
                }""",
                [ref7, base_genie_payload(chartRecordId="other")],
            )
            recorder.clear()
            page.goto(handoff_url(base, "cr-anna-rivera", ref7), wait_until="domcontentloaded")
            page.wait_for_function(
                "() => window.__rmGenieRenderHandoff && window.__rmExecuteGenieRender",
                timeout=15_000,
            )
            wait_handoff_done(page, timeout_ms=30_000)
            handoff7 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            status7 = page.evaluate("() => document.getElementById('renderStatus')?.textContent || ''")
            ok_b7 = (
                handoff7
                and handoff7.get("executed") is False
                and handoff7.get("error") == "chart_record_id_mismatch"
                and len(recorder.posts) == 0
                and "chart_record_id_mismatch" in status7
            )
            results.append(("B7_chart_record_id_mismatch", ok_b7, json.dumps({
                "error": handoff7.get("error") if handoff7 else None,
                "posts": len(recorder.posts),
                "renderStatus": status7[:120],
            })))

            # B8 — genie handoff without URL chartRecordId
            ref8 = "bridge-smoke-no-chart-record-ref"
            page.evaluate(
                """([ref, payload]) => {
                    sessionStorage.setItem('rm_genie_render:' + ref, JSON.stringify(payload));
                }""",
                [ref8, base_genie_payload(chartRecordId="cr-anna-rivera")],
            )
            recorder.clear()
            page.goto(
                f"{base}/map_CURRENT.html?skipOnboarding=1&handoff=app_shell"
                f"&handoffCreatedAt=2026-05-30T12%3A00%3A00.000Z&genieRenderRef={ref8}",
                wait_until="domcontentloaded",
            )
            page.wait_for_function(
                "() => window.__rmGenieRenderHandoff && window.__rmExecuteGenieRender",
                timeout=15_000,
            )
            wait_handoff_done(page, timeout_ms=30_000)
            handoff8 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            status8 = page.evaluate("() => document.getElementById('renderStatus')?.textContent || ''")
            ok_b8 = (
                handoff8
                and handoff8.get("executed") is False
                and handoff8.get("error") == "chart_record_id_required_for_handoff"
                and len(recorder.posts) == 0
                and "chart_record_id_required_for_handoff" in status8
            )
            results.append(("B8_chart_record_id_required", ok_b8, json.dumps({
                "error": handoff8.get("error") if handoff8 else None,
                "posts": len(recorder.posts),
                "renderStatus": status8[:120],
            })))

            browser.close()
    finally:
        if proc is not None:
            proc.terminate()
            proc.wait(timeout=5)

    # B5 — legacy map regression
    env = {**os.environ, "BASE_URL": base}
    proc5 = subprocess.run(
        [str(PYTHON), "scripts/smoke_map_current.py"],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    ok_b5 = proc5.returncode == 0
    results.append(("B5_legacy_map_regression", ok_b5, proc5.stdout.strip()[-200:] if proc5.stdout else proc5.stderr[-200:]))

    failed = [name for name, ok, _ in results if not ok]
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
    if failed:
        fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")
    print("PASS: smoke_chart_record_birth_bridge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
