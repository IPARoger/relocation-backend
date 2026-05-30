#!/usr/bin/env python3
"""Smoke: Genie Product Integration Slice 1 — app shell drawer → map render.

Cases:
  P1  Sun in 1st → Search Map → map executes → polygons > 0
  P2  4 house variables → wire POST has 4 house_conditions
  P3  12 house variables → wire POST has 12 house_conditions
  P4  Mixed transit + exclude → degradation reasons preserved
  P5  Regression gate (5 smokes)

Run:
  ./venv/bin/python scripts/smoke_genie_product_integration_slice1.py
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

PLANETS = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]


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

    def builder_available(base: str) -> bool:
        try:
            with urllib.request.urlopen(f"{base}/genie_variable_builder.js", timeout=2) as resp:
                if resp.status != 200:
                    return False
            with urllib.request.urlopen(f"{base}/chart-records", timeout=2) as resp:
                return resp.status == 200
        except Exception:
            return False

    try:
        with urllib.request.urlopen(f"{BASE}/health", timeout=2) as resp:
            if resp.status != 200 or not builder_available(BASE):
                raise OSError("stale or incomplete server")
    except Exception:
        alt = 8016
        if not port_free(alt):
            fail(f"Server unavailable at {BASE} and port {alt} busy")
        proc = spawn_server(alt)
        base = f"http://127.0.0.1:{alt}"
        if not wait_server(base) or not builder_available(base):
            proc.terminate()
            fail(f"Could not start temp server with genie builder on {base}")
        return base, proc
    return BASE, proc


class SearchRegionsRecorder:
    def __init__(self) -> None:
        self.posts: list[dict] = []
        self._installed = False

    def install(self, page) -> None:
        if self._installed:
            return

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
        self._installed = True

    def clear(self) -> None:
        self.posts = []


def open_genie_drawer(page, base: str) -> None:
    page.goto(f"{base}/app_shell.html#/map?chartRecordId=cr-anna-rivera", wait_until="domcontentloaded")
    page.wait_for_function(
        "() => window.__rmAppShell && window.__rmAppShell.viewModel() && window.RelocationGenieVariableBuilder",
        timeout=15_000,
    )
    page.wait_for_selector("#genieDrawerMount #renderBtn", timeout=15_000)
    page.wait_for_selector("#variableCards .variable-card", timeout=10_000)


def card_selector(index: int) -> str:
    return f"#variableCards .variable-card:nth-child({index + 1})"


def configure_planet_house(page, index: int, body: str, house: int) -> None:
    root = card_selector(index)
    page.select_option(f"{root} [data-type-select]", "planet_in_house")
    page.select_option(f'{root} [data-field="body"]', body)
    page.select_option(f'{root} [data-field="house"]', str(house))


def add_variable(page) -> None:
    page.click("#addVariableBtn")


def search_map_from_shell(page) -> None:
    page.click("#renderBtn")
    page.wait_for_url("**/map_CURRENT.html**", timeout=15_000)
    page.wait_for_function(
        "() => window.__rmMap && window.__rmGenieRenderHandoff",
        timeout=15_000,
    )
    page.wait_for_function(
        "() => document.getElementById('chartProfile')?.options?.length >= 1",
        timeout=15_000,
    )


def wait_handoff_executed(page, timeout_ms: int = 120_000) -> None:
    page.wait_for_function(
        """() => {
            const h = window.__rmGenieRenderHandoff?.();
            if (!h) return false;
            if (h.error && h.error !== 'no_executable_include_variables') return true;
            if (h.executed === true) return !document.getElementById('findBtn')?.disabled;
            return h.executed === false && h.execution;
        }""",
        timeout=timeout_ms,
    )


def run_regression_smokes(base_url: str) -> tuple[bool, str]:
    scripts = [
        "scripts/smoke_genie_handoff_transport_v2.py",
        "scripts/smoke_genie_map_engine.py",
        "scripts/smoke_app_shell_map_handoff.py",
        "scripts/smoke_genie_sandbox.py",
        "scripts/smoke_map_current.py",
    ]
    env = {**os.environ, "BASE_URL": base_url}
    details: list[str] = []
    for script in scripts:
        proc = subprocess.run(
            [str(PYTHON), script],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
        )
        ok = proc.returncode == 0
        details.append(f"{'PASS' if ok else 'FAIL'}: {script}")
        if not ok:
            details.append(proc.stdout[-500:] if proc.stdout else "")
            details.append(proc.stderr[-500:] if proc.stderr else "")
            return False, "\n".join(details)
    return True, "\n".join(details)


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        fail(f"playwright required: {exc}")

    base, proc = ensure_server()
    os.environ["BASE_URL"] = base
    global BASE
    BASE = base
    results: list[tuple[str, bool, str]] = []

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            recorder = SearchRegionsRecorder()
            recorder.install(page)

            # P1 — Sun in 1st → map polygons
            open_genie_drawer(page, base)
            configure_planet_house(page, 0, "sun", 1)
            search_map_from_shell(page)
            wait_handoff_executed(page)
            smoke1 = page.evaluate("() => window.__rmSmokeState()")
            handoff1 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            ok1 = (
                handoff1
                and handoff1.get("executed") is True
                and smoke1.get("polygonLayers", 0) > 0
            )
            results.append((
                "P1_sun_1h_shell_to_map_polygons",
                ok1,
                json.dumps({"polygons": smoke1.get("polygonLayers"), "executed": handoff1.get("executed") if handoff1 else None}),
            ))

            # P2 — 4 houses wire proof
            open_genie_drawer(page, base)
            configure_planet_house(page, 0, "sun", 1)
            add_variable(page)
            configure_planet_house(page, 1, "moon", 2)
            add_variable(page)
            configure_planet_house(page, 2, "mercury", 3)
            add_variable(page)
            configure_planet_house(page, 3, "venus", 4)
            recorder.clear()
            search_map_from_shell(page)
            wait_handoff_executed(page)
            wire2 = recorder.posts[0] if recorder.posts else {}
            wire_h2 = len(wire2.get("house_conditions") or [])
            ok2 = wire_h2 == 4 and len(recorder.posts) >= 1
            results.append(("P2_four_houses_wire", ok2, json.dumps({"wire_houses": wire_h2, "posts": len(recorder.posts)})))

            # P3 — 12 houses wire proof
            open_genie_drawer(page, base)
            for i in range(12):
                if i > 0:
                    add_variable(page)
                configure_planet_house(page, i, PLANETS[i % len(PLANETS)], i + 1)
            recorder.clear()
            search_map_from_shell(page)
            wait_handoff_executed(page, timeout_ms=300_000)
            wire3 = recorder.posts[0] if recorder.posts else {}
            wire_h3 = len(wire3.get("house_conditions") or [])
            ok3 = wire_h3 == 12 and len(recorder.posts) >= 1
            results.append(("P3_twelve_houses_wire", ok3, json.dumps({"wire_houses": wire_h3})))

            # P4 — mixed transit + exclude degradation
            open_genie_drawer(page, base)
            for i in range(10):
                if i > 0:
                    add_variable(page)
                configure_planet_house(page, i, PLANETS[i % len(PLANETS)], i + 1)
            add_variable(page)
            root_ex = card_selector(10)
            page.select_option(f"{root_ex} [data-type-select]", "planet_in_house")
            page.select_option(f'{root_ex} [data-field="body"]', "moon")
            page.select_option(f'{root_ex} [data-field="house"]', "11")
            page.evaluate(
                """() => {
                  const card = document.querySelectorAll('#variableCards .variable-card')[10];
                  const ex = card?.querySelector('[data-layer=not]');
                  if (ex) { ex.checked = true; ex.dispatchEvent(new Event('change', {bubbles:true})); }
                }"""
            )
            add_variable(page)
            page.check("#transitEnabledToggle")
            page.wait_for_function("() => document.getElementById('transitEnabledToggle')?.checked === true")
            root_tr = card_selector(11)
            page.select_option(f"{root_tr} [data-type-select]", "transit_through_house")
            search_map_from_shell(page)
            wait_handoff_executed(page, timeout_ms=300_000)
            handoff4 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            exec4 = (handoff4 or {}).get("execution") or {}
            deg4 = exec4.get("degradation") or []
            plan_h4 = len((exec4.get("plan") or {}).get("house_conditions") or [])
            stored4 = page.evaluate(
                """() => {
                  const ref = window.__rmGenieRenderHandoff()?.ref;
                  if (!ref) return null;
                  const raw = sessionStorage.getItem('rm_genie_render:' + ref);
                  return raw ? JSON.parse(raw) : null;
                }"""
            )
            ok4 = (
                stored4
                and len(stored4.get("variables", [])) == 12
                and plan_h4 == 10
                and any(d.get("reason") == "exclude_not_supported_in_engine_v1" for d in deg4)
                and any(d.get("reason") == "transit_not_supported_in_engine_v1" for d in deg4)
            )
            results.append((
                "P4_mixed_degradation_honest",
                ok4,
                json.dumps({"stored": len((stored4 or {}).get("variables", [])), "plan_houses": plan_h4, "degradation": deg4}),
            ))

            browser.close()

        ok5, detail5 = run_regression_smokes(base)
        results.append(("P5_regression_smokes", ok5, detail5))

    finally:
        if proc:
            proc.terminate()
            proc.wait(timeout=5)

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail[:500]}")

    print(f"\n{passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
