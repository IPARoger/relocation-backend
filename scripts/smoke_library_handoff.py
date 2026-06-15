#!/usr/bin/env python3
"""Phase 2.1/2.2 — library-to-map handoff + saved-view replay smoke.

Validates:
  * /library/state survives a fresh start and an upsert
  * library.html "Open in Map" hands off via sessionStorage (covered indirectly
    here by directly POSTing then loading map_CURRENT with hash + storage)
  * map_CURRENT.html loads the chart selector with library charts merged
  * map_CURRENT.html applies the active selection from URL hash and from
    sessionStorage with no console errors
  * map_CURRENT.html exposes window.__rmLibraryHandoff() and the smoke state
    reflects the applied selection
  * "Save current view to library" POSTs against the active library chart
  * #libraryActive=<id>&view=<view_id> restores saved viewport without
    auto-running Find regions
  * library.html exposes saved-view map deep-link helpers
  * No production behaviour changed: rendererSubstrate stays legacy

This smoke does NOT exercise rendering. Three existing smokes still gate
that (scripts/smoke_map_current.py, scripts/smoke_substrate_adapter.py,
scripts/smoke_phase2_cache.py).

Run:
  ./venv/bin/python scripts/smoke_library_handoff.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
LIBRARY_FILE = ROOT / "library" / "library.json"


def api(method: str, path: str, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"{BASE}{path}", data=data, method=method,
        headers={"Content-Type": "application/json"} if body is not None else {},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as err:
        body = err.read().decode()
        try:
            return err.code, json.loads(body)
        except json.JSONDecodeError:
            return err.code, {"raw": body}


def reset_library() -> None:
    if LIBRARY_FILE.exists():
        LIBRARY_FILE.unlink()


def main() -> int:
    reset_library()
    results: list[dict] = []

    status, _ = api("GET", "/library/state")
    results.append({
        "test": "library_state_reachable",
        "pass": status == 200,
        "detail": {"status": status},
    })

    create_status, created = api("POST", "/library/charts", {
        "name": "Handoff MVP",
        "date": "1990-05-15",
        "time": "12:00",
        "timezone": "UTC",
        "place": "Test City",
        "lat": 40.0,
        "lon": -100.0,
    })
    chart_id = created.get("id")
    results.append({
        "test": "library_chart_created_for_handoff",
        "pass": create_status == 200 and isinstance(chart_id, str)
            and chart_id.startswith("lib_chart_"),
        "detail": {"status": create_status, "chart_id": chart_id},
    })
    if not chart_id:
        print(json.dumps({"results": results, "all_pass": False}, indent=2))
        return 1

    api("POST", "/library/active", {"chart_id": chart_id})

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        # 1. Hash-based handoff via #libraryActive=<id>.
        page_hash = browser.new_page(viewport={"width": 1024, "height": 720})
        hash_errors: list[str] = []
        page_hash.on(
            "console",
            lambda msg: hash_errors.append(f"{msg.type}:{msg.text}")
            if msg.type == "error" else None,
        )
        page_hash.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1#libraryActive={chart_id}",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        page_hash.wait_for_function(
            "() => window.__rmLibraryHandoff && document.getElementById('chartProfile').options.length > 0",
            timeout=15000,
        )
        hash_state = page_hash.evaluate(
            """() => ({
                smoke: window.__rmSmokeState?.() || null,
                handoff: window.__rmLibraryHandoff(),
                selectValue: document.getElementById('chartProfile').value,
                librarySection: document.getElementById('libraryHandoff')?.hidden === false,
                openLinkText: document.getElementById('libraryOpenLink')?.textContent,
                saveBtnHidden: document.getElementById('saveCurrentViewBtn')?.hidden,
            })"""
        )
        results.append({
            "test": "hash_handoff_selects_library_chart",
            "pass": hash_state["selectValue"] == chart_id
                and hash_state["handoff"]["selectionAppliedFrom"] == "hash"
                and hash_state["handoff"]["selectionAppliedId"] == chart_id
                and hash_state["handoff"]["libraryAvailable"] is True
                and hash_state["smoke"]["rendererSubstrate"] == "legacy_search_regions"
                and hash_state["smoke"]["libraryHandoff"]["selectionAppliedId"] == chart_id
                and hash_state["librarySection"] is True
                and hash_state["saveBtnHidden"] is False
                and not hash_errors,
            "detail": {"state": hash_state, "errors": hash_errors},
        })

        # 2. SessionStorage-based handoff (no hash).
        page_session = browser.new_page(viewport={"width": 1024, "height": 720})
        session_errors: list[str] = []
        page_session.on(
            "console",
            lambda msg: session_errors.append(f"{msg.type}:{msg.text}")
            if msg.type == "error" else None,
        )
        page_session.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        page_session.evaluate(
            "id => sessionStorage.setItem('rm_library_active', id)",
            chart_id,
        )
        page_session.evaluate("() => window.__rmLoadChartProfiles()")
        page_session.wait_for_function(
            "() => window.__rmLibraryHandoff().selectionAppliedId !== null",
            timeout=10000,
        )
        session_state = page_session.evaluate(
            """() => ({
                handoff: window.__rmLibraryHandoff(),
                selectValue: document.getElementById('chartProfile').value,
            })"""
        )
        results.append({
            "test": "session_storage_handoff_selects_library_chart",
            "pass": session_state["selectValue"] == chart_id
                and session_state["handoff"]["selectionAppliedFrom"] == "sessionStorage"
                and session_state["handoff"]["selectionAppliedId"] == chart_id
                and not session_errors,
            "detail": {"state": session_state, "errors": session_errors},
        })

        # 3. Save current view to library round-trip.
        save_page = browser.new_page(viewport={"width": 1024, "height": 720})
        save_errors: list[str] = []
        save_page.on(
            "console",
            lambda msg: save_errors.append(f"{msg.type}:{msg.text}")
            if msg.type == "error" else None,
        )
        save_page.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1#libraryActive={chart_id}",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        save_page.wait_for_function(
            "() => window.__rmSaveCurrentViewToLibrary && document.getElementById('chartProfile').value === " + json.dumps(chart_id),
            timeout=15000,
        )
        save_page.evaluate(
            """() => {
                document.getElementById('planetA').value = 'moon';
                document.getElementById('houseA').value = '4';
                document.getElementById('planetB').value = 'venus';
                document.getElementById('houseB').value = '7';
                document.getElementById('planetC').value = '';
                document.getElementById('angleSignAngle').value = 'MC';
                document.getElementById('angleSignSign').value = 'capricorn';
                document.getElementById('overlayPlanet').value = 'saturn';
                document.getElementById('overlayAspect').value = 'square';
                document.getElementById('overlayAngle').value = 'ASC';
            }"""
        )
        view = save_page.evaluate(
            "async () => await window.__rmSaveCurrentViewToLibrary()"
        )
        saved_investigation = (view.get("conditions") or [{}])[0] if view else {}
        serialized_conditions = json.dumps(view.get("conditions", [])) if view else ""
        results.append({
            "test": "save_current_view_round_trips_saved_investigation",
            "pass": view is not None and isinstance(view.get("id"), str)
                and view.get("chart_id") == chart_id
                and "viewport" in view
                and saved_investigation.get("schema_version") == 1
                and saved_investigation.get("kind") == "saved_investigation"
                and saved_investigation.get("chart_id") == chart_id
                and saved_investigation.get("house_conditions") == [
                    {"slot": "A", "type": "planet_in_house", "planet": "moon", "house": 4},
                    {"slot": "B", "type": "planet_in_house", "planet": "venus", "house": 7},
                ]
                and saved_investigation.get("angle_sign_conditions") == [
                    {"type": "angle_in_sign", "angle": "MC", "sign": "capricorn"}
                ]
                and saved_investigation.get("aspect_overlay") == {
                    "type": "aspect_to_angle",
                    "planet": "saturn",
                    "aspect": "square",
                    "angle": "ASC",
                }
                and "renderer_substrate" not in serialized_conditions
                and "generation_mode" not in serialized_conditions
                and "resolution" not in serialized_conditions
                and "debug" not in serialized_conditions.lower()
                and not save_errors,
            "detail": {"view": view, "errors": save_errors},
        })

        # 4. /library/state has the saved view linked to the active chart.
        _, state_after = api("GET", "/library/state")
        results.append({
            "test": "library_views_records_saved_view",
            "pass": any(
                v.get("chart_id") == chart_id and v.get("id") == (view or {}).get("id")
                for v in state_after.get("views", [])
            ) and state_after.get("active_chart_id") == chart_id,
            "detail": {
                "active": state_after.get("active_chart_id"),
                "view_ids": [v.get("id") for v in state_after.get("views", [])],
            },
        })

        # 5. Deep-link saved-view replay restores viewport and stays renderer-inert.
        replay_page = browser.new_page(viewport={"width": 1024, "height": 720})
        replay_errors: list[str] = []
        replay_page.on(
            "console",
            lambda msg: replay_errors.append(f"{msg.type}:{msg.text}")
            if msg.type == "error" else None,
        )
        replay_page.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1#libraryActive={chart_id}&view={view['id']}",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        replay_page.wait_for_function(
            "() => window.__rmLibraryHandoff && window.__rmLibraryHandoff().viewAppliedId !== null",
            timeout=15000,
        )
        replay_state = replay_page.evaluate(
            """() => {
                const smoke = window.__rmSmokeState?.() || null;
                const handoff = window.__rmLibraryHandoff();
                const center = window.__rmMap.getCenter();
                return {
                    smoke,
                    handoff,
                    selectValue: document.getElementById('chartProfile').value,
                    controls: {
                        planetA: document.getElementById('planetA').value,
                        houseA: document.getElementById('houseA').value,
                        planetB: document.getElementById('planetB').value,
                        houseB: document.getElementById('houseB').value,
                        planetC: document.getElementById('planetC').value,
                        angleSignAngle: document.getElementById('angleSignAngle').value,
                        angleSignSign: document.getElementById('angleSignSign').value,
                        overlayPlanet: document.getElementById('overlayPlanet').value,
                        overlayAspect: document.getElementById('overlayAspect').value,
                        overlayAngle: document.getElementById('overlayAngle').value,
                    },
                    center: { lat: center.lat, lon: center.lng },
                    zoom: window.__rmMap.getZoom(),
                    polygonLayers: smoke?.polygonLayers || 0,
                    renderStatus: document.getElementById('renderStatus')?.textContent || "",
                };
            }"""
        )
        saved_viewport = (view or {}).get("viewport", {})
        expected_lat = saved_viewport.get("center_lat")
        expected_lon = saved_viewport.get("center_lon")
        if expected_lat is None or expected_lon is None:
            expected_lat = (saved_viewport.get("north") + saved_viewport.get("south")) / 2
            expected_lon = (saved_viewport.get("east") + saved_viewport.get("west")) / 2
        results.append({
            "test": "saved_view_deep_link_replays_viewport_without_render",
            "pass": replay_state["selectValue"] == chart_id
                and replay_state["handoff"]["viewRequestedId"] == view["id"]
                and replay_state["handoff"]["viewAppliedId"] == view["id"]
                and replay_state["handoff"]["viewAppliedChartId"] == chart_id
                and replay_state["handoff"]["investigationConditionsApplied"] == 4
                and replay_state["controls"] == {
                    "planetA": "moon",
                    "houseA": "4",
                    "planetB": "venus",
                    "houseB": "7",
                    "planetC": "",
                    "angleSignAngle": "MC",
                    "angleSignSign": "capricorn",
                    "overlayPlanet": "saturn",
                    "overlayAspect": "square",
                    "overlayAngle": "ASC",
                }
                and abs(replay_state["center"]["lat"] - expected_lat) < 0.1
                and abs(replay_state["center"]["lon"] - expected_lon) < 0.1
                and abs(replay_state["zoom"] - saved_viewport.get("zoom")) < 0.01
                and replay_state["smoke"]["rendererSubstrate"] == "legacy_search_regions"
                and replay_state["polygonLayers"] == 0
                and replay_state["renderStatus"] == "Ready."
                and not replay_errors,
            "detail": {
                "state": replay_state,
                "expected": {"lat": expected_lat, "lon": expected_lon, "zoom": saved_viewport.get("zoom")},
                "errors": replay_errors,
            },
        })

        # 6. library.html exposes a saved-view map deep-link contract.
        library_page = browser.new_page(viewport={"width": 1100, "height": 800})
        library_errors: list[str] = []
        library_page.on(
            "console",
            lambda msg: library_errors.append(f"{msg.type}:{msg.text}")
            if msg.type == "error" else None,
        )
        library_page.goto(f"{BASE}/library.html", wait_until="domcontentloaded", timeout=30000)
        library_page.wait_for_function(
            "() => window.__rmLibrary && window.__rmLibrary.state && window.__rmLibrary.state.views.length > 0",
            timeout=15000,
        )
        library_state = library_page.evaluate(
            """view => ({
                chartShare: window.__rmLibrary.shareUrl(view.chart_id),
                mapViewShare: window.__rmLibrary.mapViewUrl(view),
                visibleViewButtons: document.querySelectorAll('[data-view-act="copy-map-link"]').length,
            })""",
            view,
        )
        expected_suffix = f"/map_CURRENT.html?skipOnboarding=1#libraryActive={chart_id}&view={view['id']}"
        results.append({
            "test": "library_exposes_saved_view_map_deep_link",
            "pass": library_state["chartShare"].endswith(f"/library.html?chart={chart_id}")
                and library_state["mapViewShare"].endswith(expected_suffix)
                and library_state["visibleViewButtons"] >= 1
                and not library_errors,
            "detail": {"state": library_state, "expected_suffix": expected_suffix, "errors": library_errors},
        })

        # 7. Built-in chart-profile flow still works (no library hash, no storage).
        baseline_page = browser.new_page(viewport={"width": 1024, "height": 720})
        baseline_errors: list[str] = []
        baseline_page.on(
            "console",
            lambda msg: baseline_errors.append(f"{msg.type}:{msg.text}")
            if msg.type == "error" else None,
        )
        baseline_page.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        baseline_page.evaluate("() => sessionStorage.removeItem('rm_library_active')")
        baseline_page.wait_for_function(
            "() => document.getElementById('chartProfile').options.length > 0",
            timeout=10000,
        )
        baseline_state = baseline_page.evaluate(
            """() => ({
                firstOption: document.getElementById('chartProfile').options[0]?.value,
                handoff: window.__rmLibraryHandoff(),
                smoke: window.__rmSmokeState?.() || null,
            })"""
        )
        results.append({
            "test": "baseline_chart_profiles_still_available",
            "pass": baseline_state["firstOption"] == "baseline_validated"
                and baseline_state["handoff"]["libraryAvailable"] is True
                and baseline_state["handoff"]["selectionAppliedId"] is None
                and baseline_state["smoke"]["rendererSubstrate"] == "legacy_search_regions"
                and not baseline_errors,
            "detail": {"state": baseline_state, "errors": baseline_errors},
        })

        browser.close()

    payload = {"results": results, "all_pass": all(r["pass"] for r in results)}
    print(json.dumps(payload, indent=2))
    return 0 if payload["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
