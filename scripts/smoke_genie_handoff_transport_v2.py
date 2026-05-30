#!/usr/bin/env python3
"""Smoke: Genie Handoff Transport v2 — sessionStorage ref + same-tab map navigation.

Cases:
  H1  Ref round-trip (shell store → map load)
  H2  Auto execute after map load
  H3  4-house payload survives transport
  H4  12-variable payload survives transport unchanged
  H5  12 executable houses reach engine (wire proof)
  H6  10 houses + 1 exclude + 1 transit — 12 variables, honest degradation
  H7  v1 handoff unchanged (no genieRenderRef)
  H7b Contract surface includes optional genieRenderRef; stub link omits it
  H8  Invalid ref — no execute, clear failure state

Run:
  ./venv/bin/python scripts/smoke_genie_handoff_transport_v2.py
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
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
PYTHON = ROOT / "venv" / "bin" / "python"
SHELL_PREFIX = "rm_genie_render:"


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
        with urllib.request.urlopen(f"{BASE}/health", timeout=2) as resp:
            if resp.status != 200:
                raise OSError("bad health")
    except Exception:
        alt = 8015
        if not port_free(alt):
            fail(f"Server unavailable at {BASE} and port {alt} busy")
        proc = spawn_server(alt)
        base = f"http://127.0.0.1:{alt}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")
        return base, proc
    return BASE, proc


def base_genie_payload(**overrides: object) -> dict:
    payload = {
        "schema_version": 1,
        "kind": "genie_render",
        "createdAt": "2026-05-30T12:00:00.000Z",
        "chartRecordId": "smoke-chart",
        "variables": [],
        "layerControls": {
            "mutedVariableIds": [],
            "soloVariableId": None,
            "excludeVariableIds": [],
        },
        "settingsSnapshot": {"transitModeEnabled": False, "registry": {}},
        "legacyCompatibility": {
            "schema_version": 1,
            "kind": "saved_investigation",
            "chart_id": "smoke-chart",
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


def var_planet_in_house(vid: str, body: str, house: int) -> dict:
    return {
        "id": vid,
        "type": "planet_in_house",
        "polarity": "include",
        "enabled": True,
        "status": "complete",
        "label": "Planet · House",
        "fields": {"body": body, "house": house},
    }


def var_exclude_house(vid: str, body: str, house: int) -> dict:
    return {
        "id": vid,
        "type": "planet_in_house",
        "polarity": "exclude",
        "enabled": True,
        "status": "complete",
        "label": "Planet · House",
        "fields": {"body": body, "house": house},
    }


def var_transit_house(vid: str) -> dict:
    return {
        "id": vid,
        "type": "transit_through_house",
        "polarity": "include",
        "enabled": True,
        "status": "experimental",
        "label": "Transit · House",
        "fields": {
            "transitBody": "jupiter",
            "house": 10,
            "datePreset": "today",
            "startDate": None,
            "endDate": None,
            "experimental": True,
        },
    }


def parse_ref_from_url(url: str) -> str | None:
    qs = parse_qs(urlparse(url).query)
    return (qs.get("genieRenderRef") or [None])[0]


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


def wait_handoff_settled(page, timeout_ms: int = 120_000) -> None:
    page.wait_for_function(
        """() => {
            const h = window.__rmGenieRenderHandoff?.();
            if (!h) return false;
            if (h.error) return true;
            if (h.executed === true) {
                return !document.getElementById('findBtn')?.disabled;
            }
            if (h.executed === false && h.execution) return true;
            return h.executed === false && h.validation && h.validation.ok === false;
        }""",
        timeout=timeout_ms,
    )


def prepare_and_navigate(page, base: str, payload: dict) -> dict:
    """Same-tab handoff: shell stores payload, map loads with genieRenderRef."""
    page.goto(f"{base}/app_shell.html#/map?chartRecordId=cr-anna-rivera", wait_until="domcontentloaded")
    page.wait_for_function("() => window.__rmAppShell?.prepareGenieRenderHandoff", timeout=15_000)
    handoff = page.evaluate(
        """(p) => window.__rmAppShell.prepareGenieRenderHandoff(null, p)""",
        payload,
    )
    page.goto(f"{base}{handoff['url']}", wait_until="domcontentloaded")
    page.wait_for_function(
        "() => window.__rmMap && window.__rmGenieRenderHandoff && window.__rmExecuteGenieRender",
        timeout=15_000,
    )
    page.wait_for_function(
        "() => document.getElementById('chartProfile')?.options?.length >= 1",
        timeout=15_000,
    )
    page.select_option("#chartProfile", "baseline_validated")
    return handoff


def read_stored_payload(page, ref: str) -> dict | None:
    return page.evaluate(
        """(ref) => {
            const raw = sessionStorage.getItem('rm_genie_render:' + ref);
            return raw ? JSON.parse(raw) : null;
        }""",
        ref,
    )


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
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            recorder = SearchRegionsRecorder()
            recorder.install(page)

            bodies = [
                "sun", "moon", "mercury", "venus", "mars", "jupiter",
                "saturn", "uranus", "neptune", "pluto",
                "sun", "moon",
            ]

            # H1 — ref round-trip
            p1 = base_genie_payload(variables=[var_planet_in_house("v1", "sun", 1)])
            handoff1 = prepare_and_navigate(page, base, p1)
            ref1 = handoff1.get("ref")
            url_ref1 = parse_ref_from_url(handoff1.get("url", ""))
            stored1 = read_stored_payload(page, ref1)
            page.wait_for_function(
                "(ref) => window.__rmGenieRenderHandoff()?.ref === ref",
                arg=ref1,
                timeout=15_000,
            )
            loaded1 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            ok1 = (
                ref1
                and url_ref1 == ref1
                and stored1 == p1
                and loaded1
                and loaded1.get("ref") == ref1
                and loaded1.get("variableCount") == 1
            )
            results.append(("H1_ref_round_trip", ok1, json.dumps({"ref": ref1, "urlRef": url_ref1})))

            # H2 — auto execute after map load
            wait_handoff_settled(page)
            smoke2 = page.evaluate("() => window.__rmSmokeState()")
            handoff2 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            ok2 = (
                handoff2.get("executed") is True
                and smoke2.get("genieRenderHandoff", {}).get("ref") == ref1
                and smoke2.get("polygonLayers", 0) > 0
            )
            results.append((
                "H2_auto_execute_after_load",
                ok2,
                json.dumps({
                    "executed": handoff2.get("executed"),
                    "polygons": smoke2.get("polygonLayers"),
                }),
            ))

            # H3 — 4-house payload survives transport
            p3 = base_genie_payload(
                variables=[
                    var_planet_in_house("v1", "sun", 1),
                    var_planet_in_house("v2", "moon", 2),
                    var_planet_in_house("v3", "mercury", 3),
                    var_planet_in_house("v4", "venus", 4),
                ]
            )
            handoff3 = prepare_and_navigate(page, base, p3)
            stored3 = read_stored_payload(page, handoff3["ref"])
            wait_handoff_settled(page)
            handoff3_state = page.evaluate("() => window.__rmGenieRenderHandoff()")
            sum3 = (handoff3_state or {}).get("execution") or {}
            plan3_h = len(sum3.get("plan", {}).get("house_conditions", []))
            ok3 = stored3 == p3 and handoff3_state.get("executed") is True and plan3_h == 4
            results.append(("H3_four_house_survives", ok3, json.dumps({"plan_houses": plan3_h})))

            # H4 — 12-variable payload unchanged
            vars12 = [var_planet_in_house(f"v{i}", bodies[i - 1], i) for i in range(1, 13)]
            p4 = base_genie_payload(variables=vars12)
            handoff4 = prepare_and_navigate(page, base, p4)
            stored4 = read_stored_payload(page, handoff4["ref"])
            ok4 = stored4 == p4 and len(stored4.get("variables", [])) == 12
            results.append(("H4_twelve_variables_unchanged", ok4, json.dumps({"count": len(stored4.get("variables", []))})))

            # H5 — 12 executable houses reach engine (wire proof)
            recorder.clear()
            prepare_and_navigate(page, base, p4)
            wait_handoff_settled(page, timeout_ms=180_000)
            handoff5_state = page.evaluate("() => window.__rmGenieRenderHandoff()")
            sum5 = page.evaluate("() => window.__rmGenieRenderExecutionSummary()") or {}
            smoke5 = page.evaluate("() => window.__rmSmokeState()") or {}
            req5 = sum5.get("requestPayload") or smoke5.get("lastEngineRequestPayload") or {}
            wire5 = recorder.posts[0] if recorder.posts else {}
            wire_h5 = len(wire5.get("house_conditions") or [])
            plan_h5 = len(sum5.get("plan", {}).get("house_conditions", [])) or wire_h5
            req_h5 = len(req5.get("house_conditions") or [])
            ok5 = (
                (handoff5_state or {}).get("variableCount") == 12
                and req_h5 == 12
                and wire_h5 == 12
                and len(recorder.posts) >= 1
            )
            results.append((
                "H5_twelve_houses_engine_wire",
                ok5,
                json.dumps({
                    "plan_houses": plan_h5,
                    "request_houses": req_h5,
                    "wire_houses": wire_h5,
                    "wire_posts": len(recorder.posts),
                }),
            ))

            # H6 — 10 houses + 1 exclude + 1 transit
            vars6 = [var_planet_in_house(f"h{i}", bodies[i - 1], i) for i in range(1, 11)]
            vars6.append(var_exclude_house("ex1", "moon", 11))
            vars6.append(var_transit_house("tr1"))
            p6 = base_genie_payload(
                variables=vars6,
                layerControls={
                    "mutedVariableIds": [],
                    "soloVariableId": None,
                    "excludeVariableIds": ["ex1"],
                },
            )
            handoff6 = prepare_and_navigate(page, base, p6)
            stored6 = read_stored_payload(page, handoff6["ref"])
            wait_handoff_settled(page)
            handoff6_state = page.evaluate("() => window.__rmGenieRenderHandoff()")
            sum6 = (handoff6_state or {}).get("execution") or {}
            deg6 = sum6.get("degradation") or []
            plan_h6 = len(sum6.get("plan", {}).get("house_conditions", []))
            ok6 = (
                len(stored6.get("variables", [])) == 12
                and handoff6_state.get("variableCount") == 12
                and sum6.get("executed") is True
                and plan_h6 == 10
                and any(d.get("reason") == "exclude_not_supported_in_engine_v1" for d in deg6)
                and any(d.get("reason") == "transit_not_supported_in_engine_v1" for d in deg6)
            )
            results.append((
                "H6_mixed_twelve_degradation_honest",
                ok6,
                json.dumps({
                    "stored_count": len(stored6.get("variables", [])),
                    "plan_houses": plan_h6,
                    "degradation": deg6,
                }),
            ))

            # H7 — v1 handoff without genieRenderRef (unchanged)
            page.goto(f"{base}/app_shell.html#/map?chartRecordId=cr-anna-rivera", wait_until="domcontentloaded")
            page.wait_for_function("() => window.__rmAppShell", timeout=15_000)
            contract_ok = page.evaluate(
                """() => {
                  const c = window.__rmAppShell.MAP_HANDOFF_CONTRACT;
                  return Array.isArray(c.optionalFields) && c.optionalFields.includes('genieRenderRef');
                }"""
            )
            results.append((
                "H7_contract_includes_genieRenderRef",
                contract_ok,
                "MAP_HANDOFF_CONTRACT.optionalFields includes genieRenderRef",
            ))

            stub_href = page.evaluate(
                '() => document.querySelector(\'a[href*="map_CURRENT.html"]\')?.getAttribute("href") || ""'
            )
            stub_no_ref = parse_ref_from_url(stub_href) is None
            results.append((
                "H7_stub_link_no_genieRenderRef",
                stub_no_ref,
                stub_href or "missing stub link",
            ))

            v1_url = page.evaluate("() => window.__rmAppShell.buildMapHandoffUrl()")
            page.goto(f"{base}{v1_url}", wait_until="domcontentloaded")
            page.wait_for_function("() => window.__rmMap && window.__rmAppShellHandoff", timeout=15_000)
            page.wait_for_timeout(500)
            handoff7 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            smoke7 = page.evaluate("() => window.__rmSmokeState()")
            app7 = page.evaluate("() => window.__rmAppShellHandoff()")
            ok7 = (
                parse_ref_from_url(v1_url) is None
                and handoff7 is None
                and smoke7.get("genieRenderHandoff") is None
                and app7
                and app7.get("chartRecordId") == "cr-anna-rivera"
                and smoke7.get("polygonLayers") == 0
            )
            results.append(("H7_v1_handoff_unchanged", ok7, json.dumps({"handoff": handoff7, "appShell": app7})))

            # H8 — invalid ref
            invalid_url = (
                f"{base}/map_CURRENT.html?skipOnboarding=1&handoff=app_shell"
                "&chartRecordId=cr-anna-rivera&genieRenderRef=invalid-missing-ref"
            )
            page.goto(invalid_url, wait_until="domcontentloaded")
            page.wait_for_function("() => window.__rmGenieRenderHandoff", timeout=15_000)
            page.wait_for_timeout(500)
            handoff8 = page.evaluate("() => window.__rmGenieRenderHandoff()")
            smoke8 = page.evaluate("() => window.__rmSmokeState()")
            sum8 = page.evaluate("() => window.__rmGenieRenderExecutionSummary()")
            ok8 = (
                handoff8
                and handoff8.get("executed") is False
                and handoff8.get("error") == "payload_not_found"
                and handoff8.get("ref") == "invalid-missing-ref"
                and (sum8 is None or sum8.get("executed") is not True)
                and smoke8.get("polygonLayers") == 0
            )
            results.append(("H8_invalid_ref_no_execute", ok8, json.dumps(handoff8)))

            browser.close()
    finally:
        if proc:
            proc.terminate()
            proc.wait(timeout=5)

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")

    print(f"\n{passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
