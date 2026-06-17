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
  * POST /library/views (API seed) persists investigation-shaped conditions
  * #libraryActive=<id>&view=<view_id> handoff reads view id and chart selection
  * library.html exposes saved-view map deep-link helpers
  * No production behaviour changed: rendererSubstrate stays legacy

This smoke does NOT exercise rendering. Three existing smokes still gate
that (scripts/smoke_map_current.py, scripts/smoke_substrate_adapter.py,
scripts/smoke_phase2_cache.py).

Run:
  set -a && source .env.staging && set +a
  RM_PHASE2_LIBRARY=1 ./venv/bin/python scripts/smoke_library_handoff.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8004").rstrip("/")
LIBRARY_FILE = ROOT / "library" / "library.json"

PYTHON = ROOT / "venv" / "bin" / "python"
LIBRARY_SMOKE_PORT = int(os.environ.get("RM_LIBRARY_SMOKE_PORT", "8005"))


def _library_state_status(base: str) -> int:
    try:
        with urllib.request.urlopen(base + "/library/state", timeout=5) as resp:
            return resp.status
    except urllib.error.HTTPError as err:
        return err.code
    except Exception:
        return 0


def _port_free(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) != 0


def _wait_health(base: str, timeout_s: float = 25.0) -> bool:
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


def ensure_library_enabled_base(base: str) -> tuple[str, subprocess.Popen | None]:
    os.environ["RM_PHASE2_LIBRARY"] = "1"
    if _library_state_status(base) == 200:
        return base, None
    alt = f"http://127.0.0.1:{LIBRARY_SMOKE_PORT}"
    if not _port_free(LIBRARY_SMOKE_PORT):
        _fail(
            f"{base}/library/state is disabled and port {LIBRARY_SMOKE_PORT} is busy; "
            "restart server with RM_PHASE2_LIBRARY=1 or free the port"
        )
    proc = subprocess.Popen(
        [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app",
         "--host", "127.0.0.1", "--port", str(LIBRARY_SMOKE_PORT)],
        cwd=str(ROOT),
        env={**os.environ, "RM_PHASE2_LIBRARY": "1"},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if not _wait_health(alt):
        proc.terminate()
        _fail(f"library smoke server did not start on {alt}")
    return alt, proc



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




def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def resolve_browser_auth():
    """Mint a real Supabase session for map_CURRENT (auth_guard requires it)."""
    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon_key, service_key]):
        _fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY for browser smokes")
    from supabase import create_client

    email = os.environ.get("RM_SMOKE_EMAIL", "davidleongoodman@gmail.com").strip()
    anon_client = create_client(url, anon_key)
    admin = create_client(url, service_key)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon_client.auth.verify_otp(
        {"token_hash": link.properties.hashed_token, "type": "magiclink"}
    )
    if not res.session:
        _fail(f"could not authenticate {email}")
    ref = urlparse(url).hostname.split(".")[0]
    s = res.session
    storage_key = f"sb-{ref}-auth-token"
    storage_val = json.dumps({
        "access_token": s.access_token,
        "refresh_token": s.refresh_token,
        "expires_at": s.expires_at,
        "expires_in": s.expires_in,
        "token_type": s.token_type or "bearer",
        "user": json.loads(res.user.model_dump_json()),
    })
    return (
        f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
    )


def new_authed_context(browser, auth_init_script: str, viewport: dict):
    context = browser.new_context(viewport=viewport)
    context.add_init_script(auth_init_script)
    return context


def new_authed_page(browser, auth_init_script: str, viewport: dict):
    return new_authed_context(browser, auth_init_script, viewport).new_page()

def reset_library() -> None:
    if LIBRARY_FILE.exists():
        LIBRARY_FILE.unlink()


def main() -> int:
    global BASE
    server_proc: subprocess.Popen | None = None
    reset_library()
    results: list[dict] = []

    BASE, server_proc = ensure_library_enabled_base(BASE)

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

    auth_init_script = resolve_browser_auth()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        handoff_viewport = {"width": 1024, "height": 720}
        handoff_context = new_authed_context(browser, auth_init_script, handoff_viewport)

        # 1. Hash-based handoff via #libraryActive=<id>.
        page_hash = handoff_context.new_page()
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
            "() => window.__rmLibraryHandoff && window.__rmLibraryHandoff().selectionAppliedId === "
            + json.dumps(chart_id),
            timeout=15000,
        )
        hash_state = page_hash.evaluate(
            """() => ({
                smoke: window.__rmSmokeState?.() || null,
                handoff: window.__rmLibraryHandoff(),
                selectValue: document.getElementById('chartProfile').value,
                librarySection: document.getElementById('libraryHandoff')?.hidden === false,
                openLinkText: document.getElementById('libraryOpenLink')?.textContent,
                saveBtnAbsent: document.getElementById('saveCurrentViewBtn') === null,
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
                and hash_state["saveBtnAbsent"] is True
                and not hash_errors,
            "detail": {"state": hash_state, "errors": hash_errors},
        })

        # 2. SessionStorage-based handoff (no hash).
        # Reuse the same tab: test 1 persisted rm_library_active before navigation.
        page_hash.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        page_hash.wait_for_function(
            "() => window.__rmLibraryHandoff && window.__rmLibraryHandoff().selectionAppliedId === "
            + json.dumps(chart_id)
            + " && window.__rmLibraryHandoff().selectionAppliedFrom === 'sessionStorage'",
            timeout=15000,
        )
        session_state = page_hash.evaluate(
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
                and not hash_errors,
            "detail": {"state": session_state, "errors": hash_errors},
        })
        page_hash.close()
        handoff_context.close()

        # 3. Library view persistence (API seed; map no longer writes /library/views).
        view_payload = {
            "chart_id": chart_id,
            "label": "Smoke handoff view",
            "north": 55.0,
            "south": 20.0,
            "east": -60.0,
            "west": -130.0,
            "zoom": 4.0,
            "center_lat": 37.5,
            "center_lon": -95.0,
            "conditions": [{
                "schema_version": 1,
                "kind": "saved_investigation",
                "chart_id": chart_id,
                "house_conditions": [
                    {"slot": "A", "type": "planet_in_house", "planet": "moon", "house": 4},
                    {"slot": "B", "type": "planet_in_house", "planet": "venus", "house": 7},
                ],
                "angle_sign_conditions": [
                    {"type": "angle_in_sign", "angle": "MC", "sign": "capricorn"},
                ],
                "aspect_overlay": {
                    "type": "aspect_to_angle",
                    "planet": "saturn",
                    "aspect": "square",
                    "angle": "ASC",
                },
            }],
            "notes": "",
        }
        status_v, view = api("POST", "/library/views", view_payload)
        saved_investigation = (view.get("conditions") or [{}])[0] if view else {}
        serialized_conditions = json.dumps(view.get("conditions", [])) if view else ""
        results.append({
            "test": "library_view_api_persists_saved_investigation_shape",
            "pass": status_v == 200 and isinstance(view.get("id"), str)
                and view.get("chart_id") == chart_id
                and "viewport" in view
                and saved_investigation.get("schema_version") == 1
                and saved_investigation.get("kind") == "saved_investigation"
                and saved_investigation.get("chart_id") == chart_id
                and saved_investigation.get("house_conditions") == view_payload["conditions"][0]["house_conditions"]
                and saved_investigation.get("angle_sign_conditions") == view_payload["conditions"][0]["angle_sign_conditions"]
                and saved_investigation.get("aspect_overlay") == view_payload["conditions"][0]["aspect_overlay"]
                and "renderer_substrate" not in serialized_conditions
                and "generation_mode" not in serialized_conditions
                and "resolution" not in serialized_conditions
                and "debug" not in serialized_conditions.lower(),
            "detail": {"view": view, "status": status_v},
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

        # 5. Deep-link saved-view handoff reads #view= and selects library chart (read path).
        replay_page = new_authed_page(browser, auth_init_script, {"width": 1024, "height": 720})
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
            "() => window.__rmLibraryHandoff && window.__rmLibraryHandoff().selectionAppliedId === "
            + json.dumps(chart_id)
            + " && window.__rmLibraryHandoff().viewRequestedId === "
            + json.dumps(view["id"]),
            timeout=15000,
        )
        replay_state = replay_page.evaluate(
            """() => ({
                handoff: window.__rmLibraryHandoff(),
                selectValue: document.getElementById('chartProfile').value,
            })"""
        )
        results.append({
            "test": "saved_view_deep_link_handoff_reads_view_id",
            "pass": replay_state["selectValue"] == chart_id
                and replay_state["handoff"]["viewRequestedId"] == view["id"]
                and replay_state["handoff"]["selectionAppliedId"] == chart_id
                and not replay_errors,
            "detail": {"state": replay_state, "errors": replay_errors},
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
        baseline_page = new_authed_page(browser, auth_init_script, {"width": 1024, "height": 720})
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
    rc = 0 if payload["all_pass"] else 1
    if server_proc is not None:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
