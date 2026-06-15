#!/usr/bin/env python3
"""Smoke: Genie render → map engine adapter (Web 2.0 slice 1).

Proves genie_render executes via variables[] only — not legacyCompatibility.
Key proof: four house conditions reach /search-regions without A/B/C cap.

Run:
  ./venv/bin/python scripts/smoke_genie_map_engine.py

Regression (must pass):
  ./venv/bin/python scripts/smoke_map_current.py
  ./venv/bin/python scripts/smoke_genie_sandbox.py
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
        with urllib.request.urlopen(f"{BASE}/health", timeout=2) as resp:
            if resp.status != 200:
                raise OSError("bad health")
    except Exception:
        alt = 8014
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


def var_aspect(vid: str, body: str, aspect: str, angle: str) -> dict:
    return {
        "id": vid,
        "type": "aspect_to_angle",
        "polarity": "include",
        "enabled": True,
        "status": "complete",
        "label": "Aspect · Angle",
        "fields": {"body": body, "aspect": aspect, "angle": angle},
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


def wait_genie_render_done(page, timeout_ms: int = 120_000) -> None:
    page.wait_for_function(
        """() => {
            const s = window.__rmGenieRenderExecutionSummary?.();
            return s && s.executed === true && !document.getElementById('findBtn')?.disabled;
        }""",
        timeout=timeout_ms,
    )


class SearchRegionsRecorder:
    """Capture POST /search-regions bodies during a test window."""

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

    def count(self) -> int:
        return len(self.posts)


def snapshot_engine_payload(page) -> dict | None:
    return page.evaluate("() => window.__rmSmokeState()?.lastEngineRequestPayload ?? null")


def payloads_equal(a: dict | None, b: dict | None) -> bool:
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


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
            page.goto(
                f"{base}/map_CURRENT.html?skipOnboarding=1&bust={int(time.time())}",
                wait_until="domcontentloaded",
            )
            page.wait_for_function(
                "() => window.__rmExecuteGenieRender && window.__rmGenieMapAdapter && window.__rmMap",
                timeout=15_000,
            )
            page.wait_for_function(
                "() => document.getElementById('chartProfile')?.options?.length >= 1",
                timeout=15_000,
            )
            page.select_option("#chartProfile", "baseline_validated")

            recorder = SearchRegionsRecorder()
            recorder.install(page)

            # CASE 1 — Sun 1H → polygons
            p1 = base_genie_payload(variables=[var_planet_in_house("v1", "sun", 1)])
            page.evaluate("async (p) => await window.__rmExecuteGenieRender(p)", p1)
            wait_genie_render_done(page)
            smoke1 = page.evaluate("() => window.__rmSmokeState()")
            sum1 = page.evaluate("() => window.__rmGenieRenderExecutionSummary()")
            ok1 = (
                sum1.get("executed") is True
                and smoke1.get("polygonLayers", 0) > 0
                and sum1.get("plan", {}).get("house_conditions", [])[0].get("planet") == "sun"
            )
            results.append((
                "case1_sun_1h_polygons",
                ok1,
                json.dumps({"polygons": smoke1.get("polygonLayers"), "executed": sum1.get("executed")}),
            ))

            # CASE 2 — four houses → plan + request both length 4 (+ wire proof)
            p2 = base_genie_payload(
                variables=[
                    var_planet_in_house("v1", "sun", 1),
                    var_planet_in_house("v2", "moon", 2),
                    var_planet_in_house("v3", "mercury", 3),
                    var_planet_in_house("v4", "venus", 4),
                ]
            )
            recorder.clear()
            page.evaluate("async (p) => await window.__rmExecuteGenieRender(p)", p2)
            wait_genie_render_done(page)
            sum2 = page.evaluate("() => window.__rmGenieRenderExecutionSummary()")
            plan_h = len(sum2.get("plan", {}).get("house_conditions", []))
            req_h = len(sum2.get("requestPayload", {}).get("house_conditions", []))
            smoke_req_h = len(
                (page.evaluate("() => window.__rmSmokeState()") or {})
                .get("lastEngineRequestPayload", {})
                .get("house_conditions", [])
            )
            wire_posts = recorder.posts
            wire_house_lens = [len(p.get("house_conditions") or []) for p in wire_posts]
            first_house_post = wire_posts[0] if wire_posts else {}
            wire_h = len(first_house_post.get("house_conditions") or [])
            ok2 = (
                sum2.get("executed") is True
                and plan_h == 4
                and req_h == 4
                and smoke_req_h == 4
                and wire_h == 4
                and len(wire_posts) >= 1
            )
            results.append((
                "case2_four_houses_engine",
                ok2,
                json.dumps({
                    "plan_house_conditions": plan_h,
                    "requestPayload_house_conditions": req_h,
                    "smoke_lastEngineRequestPayload_house_conditions": smoke_req_h,
                    "wire_search_regions_posts": len(wire_posts),
                    "wire_first_post_house_conditions": wire_h,
                    "wire_all_house_lens": wire_house_lens,
                    "planets": [c.get("planet") for c in sum2.get("plan", {}).get("house_conditions", [])],
                }),
            ))

            # CASE 3 — two aspects: first executes, second degraded
            p3 = base_genie_payload(
                variables=[
                    var_aspect("a1", "mars", "square", "ASC"),
                    var_aspect("a2", "jupiter", "trine", "MC"),
                ]
            )
            page.evaluate("async (p) => await window.__rmExecuteGenieRender(p)", p3)
            wait_genie_render_done(page)
            sum3 = page.evaluate("() => window.__rmGenieRenderExecutionSummary()")
            deg3 = sum3.get("degradation") or []
            aspect_plan = sum3.get("plan", {}).get("aspectOverlay")
            ok3 = (
                sum3.get("executed") is True
                and aspect_plan is not None
                and aspect_plan.get("planet") == "mars"
                and any(
                    d.get("variableId") == "a2"
                    and d.get("reason") == "additional_aspect_not_executed_v1"
                    for d in deg3
                )
            )
            results.append((
                "case3_two_aspects_degradation",
                ok3,
                json.dumps({"aspectOverlay": aspect_plan, "degradation": deg3}),
            ))

            # CASE 4 — exclude only: no execution
            p4 = base_genie_payload(
                variables=[var_exclude_house("x1", "moon", 4)],
                layerControls={
                    "mutedVariableIds": [],
                    "soloVariableId": None,
                    "excludeVariableIds": ["x1"],
                },
            )
            page.evaluate("async (p) => await window.__rmExecuteGenieRender(p)", p4)
            page.wait_for_function(
                "() => { const s = window.__rmGenieRenderExecutionSummary?.(); return s && s.executed === false; }",
                timeout=15_000,
            )
            sum4 = page.evaluate("() => window.__rmGenieRenderExecutionSummary()")
            deg4 = sum4.get("degradation") or []
            ok4 = (
                sum4.get("executed") is False
                and sum4.get("requestPayload") is None
                and any(d.get("reason") == "exclude_not_supported_in_engine_v1" for d in deg4)
            )
            results.append(("case4_exclude_only_no_execute", ok4, json.dumps(sum4)))

            # CASE 5 — transit only: no execution
            p5 = base_genie_payload(variables=[var_transit_house("t1")])
            page.evaluate("async (p) => await window.__rmExecuteGenieRender(p)", p5)
            page.wait_for_function(
                "() => { const s = window.__rmGenieRenderExecutionSummary?.(); return s && s.executed === false; }",
                timeout=15_000,
            )
            sum5 = page.evaluate("() => window.__rmGenieRenderExecutionSummary()")
            deg5 = sum5.get("degradation") or []
            ok5 = (
                sum5.get("executed") is False
                and sum5.get("requestPayload") is None
                and any(d.get("reason") == "transit_not_supported_in_engine_v1" for d in deg5)
            )
            results.append(("case5_transit_only_no_execute", ok5, json.dumps(sum5)))

            # Adapter reads variables[] only — legacyCompatibility must not drive plan
            legacy_trap = base_genie_payload(
                variables=[var_planet_in_house("only", "sun", 1)],
            )
            legacy_trap["legacyCompatibility"]["house_conditions"] = [
                {"slot": "A", "type": "planet_in_house", "planet": "pluto", "house": 12, "variableId": "trap"},
            ]
            plan_trap = page.evaluate(
                """(p) => window.__rmGenieMapAdapter.buildEngineExecutionPlan(
                    p,
                    { birth_year: 1976, birth_month: 1, birth_day: 13, birth_hour_utc: 12.0 }
                )""",
                legacy_trap,
            )
            ok_trap = (
                len(plan_trap.get("house_conditions", [])) == 1
                and plan_trap["house_conditions"][0].get("planet") == "sun"
                and plan_trap["house_conditions"][0].get("variableId") == "only"
            )
            results.append((
                "adapter_ignores_legacy_compatibility",
                ok_trap,
                json.dumps(plan_trap.get("house_conditions")),
            ))

            # CASE 6 — invalid payload: validation failure, no engine call
            invalid_payload = {
                "schema_version": 1,
                "kind": "wrong",
                "variables": [],
            }
            baseline6 = snapshot_engine_payload(page)
            recorder.clear()
            sum6 = page.evaluate(
                "async (p) => await window.__rmExecuteGenieRender(p)",
                invalid_payload,
            )
            after6 = snapshot_engine_payload(page)
            validation6 = sum6.get("validation") or {}
            errors6 = validation6.get("errors") or []
            ok6 = (
                (sum6.get("ok") is False or validation6.get("ok") is False)
                and sum6.get("executed") is False
                and len(errors6) >= 1
                and 'kind must be "genie_render"' in errors6
                and recorder.count() == 0
                and payloads_equal(baseline6, after6)
                and sum6.get("requestPayload") is None
            )
            results.append((
                "case6_invalid_payload_no_engine",
                ok6,
                json.dumps({
                    "ok": sum6.get("ok"),
                    "validationOk": validation6.get("ok"),
                    "errors": errors6,
                    "searchRegionsPosts": recorder.count(),
                    "payloadUnchanged": payloads_equal(baseline6, after6),
                }),
            ))

            # CASE 7 — empty include payload: no executable conditions, no engine call
            empty_payload = {
                "schema_version": 1,
                "kind": "genie_render",
                "createdAt": "2026-05-30T12:00:00.000Z",
                "chartRecordId": "sandbox-chart-record",
                "variables": [],
                "layerControls": {
                    "mutedVariableIds": [],
                    "soloVariableId": None,
                    "excludeVariableIds": [],
                },
                "settingsSnapshot": {},
                "legacyCompatibility": {},
            }
            baseline7 = snapshot_engine_payload(page)
            recorder.clear()
            sum7 = page.evaluate(
                "async (p) => await window.__rmExecuteGenieRender(p)",
                empty_payload,
            )
            after7 = snapshot_engine_payload(page)
            render_status7 = page.evaluate(
                "() => document.getElementById('renderStatus')?.textContent || ''"
            )
            ok7 = (
                (sum7.get("ok") is False or sum7.get("executed") is False)
                and sum7.get("executed") is False
                and sum7.get("requestPayload") is None
                and recorder.count() == 0
                and payloads_equal(baseline7, after7)
                and "no executable" in render_status7.lower()
                and not (
                    sum7.get("executed") is True
                    and (page.evaluate("() => window.__rmSmokeState()?.polygonLayers") or 0) > 0
                )
            )
            results.append((
                "case7_empty_include_no_engine",
                ok7,
                json.dumps({
                    "ok": sum7.get("ok"),
                    "executed": sum7.get("executed"),
                    "renderStatus": render_status7,
                    "searchRegionsPosts": recorder.count(),
                    "payloadUnchanged": payloads_equal(baseline7, after7),
                }),
            ))

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
