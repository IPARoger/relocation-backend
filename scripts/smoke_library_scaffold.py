#!/usr/bin/env python3
"""Phase 2.0 — account + chart-library scaffold smoke.

Validates:
  * library scaffold is feature-flag gated (RM_PHASE2_LIBRARY)
  * state shape matches the chart-profile contract
  * chart CRUD + favorites + active selection + view save + settings PATCH work
  * library.html serves and exposes the documented window.__rmLibrary hooks
  * /chart-profiles and /health continue to respond
  * library persistence does not touch renderer state

This smoke does NOT exercise map_CURRENT rendering. It only verifies the
Phase 2.0 scaffold endpoints and dashboard load. Renderer smokes remain
in scripts/smoke_map_current.py and scripts/smoke_substrate_adapter.py.

Run:
  RM_PHASE2_LIBRARY=1 ./venv/bin/python scripts/smoke_library_scaffold.py
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

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]

PYTHON = ROOT / "venv" / "bin" / "python"
LIBRARY_SMOKE_PORT = int(os.environ.get("RM_LIBRARY_SMOKE_PORT", "8005"))


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


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


def _library_state_status(base: str) -> int:
    try:
        with urllib.request.urlopen(base + "/library/state", timeout=5) as resp:
            return resp.status
    except urllib.error.HTTPError as err:
        return err.code
    except Exception:
        return 0


def ensure_library_enabled_base(base: str) -> tuple[str, subprocess.Popen | None]:
    """Opt in to library scaffold; spawn a dedicated server if BASE has it disabled."""
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

LIBRARY_FILE = ROOT / "library" / "library.json"


def request(method: str, path: str, body: dict | None = None, timeout: int = 10):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json"} if body is not None else {},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as err:
        body = err.read().decode()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"raw": body}
        return err.code, payload


def fetch_text(path: str) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=10) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode()


def reset_persistence() -> None:
    if LIBRARY_FILE.exists():
        LIBRARY_FILE.unlink()


def run_dashboard_browser_check() -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover
        return {"skipped": True, "reason": str(exc)}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1024, "height": 720})
        errors: list[str] = []
        page.on(
            "console",
            lambda msg: errors.append(f"console.{msg.type}: {msg.text}")
            if msg.type == "error"
            else None,
        )
        page.goto(f"{BASE}/library.html", wait_until="domcontentloaded", timeout=20_000)
        page.wait_for_function(
            "() => window.__rmLibrary && Array.isArray(window.__rmLibrary.state?.charts)",
            timeout=15_000,
        )
        hooks = page.evaluate(
            """() => ({
                hooks: Object.keys(window.__rmLibrary || {}).sort(),
                stateChartCount: window.__rmLibrary.state?.charts?.length || 0,
                schemaVersion: window.__rmLibrary.state?.schema_version,
                shareUrl: window.__rmLibrary.shareUrl('lib_chart_1')
            })"""
        )
        browser.close()
        return {"hooks": hooks, "errors": errors}


def main() -> int:
    results: list[dict] = []
    server_proc: subprocess.Popen | None = None

    # 1. Feature flag — default off; explicit 0 off; explicit 1 on.
    proc_default = subprocess.run(
        [sys.executable, "-c",
         "import os; os.environ.pop('RM_PHASE2_LIBRARY', None); "
         "from main_centerline_FIXER import _library_enabled; print(_library_enabled())"],
        cwd=str(ROOT),
        env={k: v for k, v in os.environ.items() if k != "RM_PHASE2_LIBRARY"},
        capture_output=True, text=True, timeout=20,
    )
    results.append({
        "test": "feature_flag_default_off_when_unset",
        "pass": proc_default.returncode == 0 and "False" in proc_default.stdout,
        "detail": {"stdout": proc_default.stdout.strip(), "stderr": proc_default.stderr.strip()},
    })

    proc = subprocess.run(
        [sys.executable, "-c", "import os; os.environ['RM_PHASE2_LIBRARY']='0'; "
         "from main_centerline_FIXER import _library_enabled; "
         "print(_library_enabled())"],
        cwd=str(ROOT),
        env={**os.environ, "RM_PHASE2_LIBRARY": "0"},
        capture_output=True, text=True, timeout=20,
    )
    results.append({
        "test": "feature_flag_disable_path_observable",
        "pass": proc.returncode == 0 and "False" in proc.stdout,
        "detail": {"stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()},
    })

    proc_on = subprocess.run(
        [sys.executable, "-c", "import os; os.environ['RM_PHASE2_LIBRARY']='1'; "
         "from main_centerline_FIXER import _library_enabled; "
         "print(_library_enabled())"],
        cwd=str(ROOT),
        env={**os.environ, "RM_PHASE2_LIBRARY": "1"},
        capture_output=True, text=True, timeout=20,
    )
    results.append({
        "test": "feature_flag_enable_path_observable",
        "pass": proc_on.returncode == 0 and "True" in proc_on.stdout,
        "detail": {"stdout": proc_on.stdout.strip(), "stderr": proc_on.stderr.strip()},
    })

    global BASE
    BASE, server_proc = ensure_library_enabled_base(BASE)

    # 2. Live server with RM_PHASE2_LIBRARY=1 (opt-in).
    status, state = request("GET", "/library/state")
    results.append({
        "test": "library_state_initial_shape",
        "pass": status == 200
            and state.get("schema_version") == 1
            and isinstance(state.get("charts"), list)
            and isinstance(state.get("views"), list)
            and isinstance(state.get("favorites"), list)
            and "active_chart_id" in state
            and isinstance(state.get("settings"), dict)
            and state["settings"].get("default_substrate") == "legacy_search_regions",
        "detail": {"status": status, "state_keys": sorted(state.keys()) if isinstance(state, dict) else None},
    })

    # 3. Chart create + share_url contract.
    payload = {
        "name": "Smoke MVP",
        "date": "1990-05-15",
        "time": "12:00",
        "timezone": "UTC",
        "place": "Test City",
        "lat": 40.0,
        "lon": -100.0,
        "notes": "phase2 smoke",
    }
    status, created = request("POST", "/library/charts", payload)
    results.append({
        "test": "chart_create_returns_id_and_share_url",
        "pass": status == 200
            and isinstance(created.get("id"), str)
            and created["id"].startswith("lib_chart_")
            and created.get("share_url") == f"/library.html?chart={created['id']}",
        "detail": {"status": status, "record": created},
    })
    chart_id = created.get("id")

    # 4. Update (upsert with id) keeps record stable.
    update_payload = {**payload, "id": chart_id, "notes": "updated", "name": "Smoke MVP v2"}
    status, updated = request("POST", "/library/charts", update_payload)
    results.append({
        "test": "chart_upsert_preserves_id",
        "pass": status == 200 and updated.get("id") == chart_id and updated.get("name") == "Smoke MVP v2",
        "detail": {"status": status, "record": updated},
    })

    # 5. Favorite toggle on + off.
    _, fav_on = request("POST", f"/library/charts/{chart_id}/favorite", {"favorite": True})
    _, after_on = request("GET", "/library/state")
    _, fav_off = request("POST", f"/library/charts/{chart_id}/favorite", {"favorite": False})
    _, after_off = request("GET", "/library/state")
    results.append({
        "test": "favorite_toggle_persists",
        "pass": fav_on.get("favorite") is True
            and chart_id in after_on.get("favorites", [])
            and fav_off.get("favorite") is False
            and chart_id not in after_off.get("favorites", []),
        "detail": {"fav_on": fav_on, "fav_off": fav_off},
    })

    # 6. Active selection round-trip.
    status_active, active = request("POST", "/library/active", {"chart_id": chart_id})
    _, after_active = request("GET", "/library/state")
    results.append({
        "test": "active_chart_selection_round_trip",
        "pass": status_active == 200
            and active.get("active_chart_id") == chart_id
            and after_active.get("active_chart_id") == chart_id,
        "detail": {"active": active},
    })

    # 7. View save references active chart and persists.
    view_payload = {
        "chart_id": chart_id,
        "label": "Americas baseline",
        "north": 55.0, "south": 20.0, "east": -60.0, "west": -130.0,
        "zoom": 4.0,
        "conditions": [{
            "schema_version": 1,
            "kind": "saved_investigation",
            "chart_id": chart_id,
            "house_conditions": [{"slot": "A", "type": "planet_in_house", "planet": "sun", "house": 1}],
            "angle_sign_conditions": [{"type": "angle_in_sign", "angle": "ASC", "sign": "aries"}],
            "aspect_overlay": {"type": "aspect_to_angle", "planet": "saturn", "aspect": "square", "angle": "MC"},
        }],
        "notes": "Saved by smoke",
    }
    status_v, view = request("POST", "/library/views", view_payload)
    _, after_view = request("GET", "/library/state")
    results.append({
        "test": "view_save_persists_and_links_chart",
        "pass": status_v == 200
            and isinstance(view.get("id"), str)
            and view.get("chart_id") == chart_id
            and view["viewport"]["zoom"] == 4.0
            and view["conditions"][0]["kind"] == "saved_investigation"
            and "renderer_substrate" not in json.dumps(view["conditions"])
            and "debug" not in json.dumps(view["conditions"]).lower()
            and any(v["id"] == view["id"] for v in after_view.get("views", [])),
        "detail": {"view": view},
    })

    # 8. Settings PATCH persists supplied keys only.
    status_s, settings = request("PUT", "/library/settings", {"experimental_mode_enabled": True})
    _, after_settings = request("GET", "/library/state")
    results.append({
        "test": "settings_patch_persists",
        "pass": status_s == 200
            and settings.get("experimental_mode_enabled") is True
            and after_settings["settings"].get("default_substrate") == "legacy_search_regions"
            and after_settings["settings"].get("experimental_mode_enabled") is True,
        "detail": {"settings": settings},
    })

    # 9. /chart-profiles still works (renderer doctrine preserved).
    status_p, profiles = request("GET", "/chart-profiles")
    results.append({
        "test": "chart_profiles_endpoint_untouched",
        "pass": status_p == 200 and isinstance(profiles, list) and len(profiles) >= 1
            and "id" in profiles[0],
        "detail": {"status": status_p, "count": len(profiles) if isinstance(profiles, list) else None},
    })

    # 10. library.html serves and exposes window.__rmLibrary hooks.
    page_status, body = fetch_text("/library.html")
    expected_hook_signatures = [
        "window.__rmLibrary",
        "/library/state",
        "rm_library_active",
    ]
    results.append({
        "test": "library_html_serves_with_hooks",
        "pass": page_status == 200 and all(s in body for s in expected_hook_signatures),
        "detail": {"status": page_status, "size": len(body)},
    })

    # 11. Dashboard JS loads cleanly via headless browser (best-effort).
    browser_check = run_dashboard_browser_check()
    if browser_check.get("skipped"):
        results.append({
            "test": "library_dashboard_browser_check",
            "pass": True,
            "detail": {"skipped": browser_check["reason"]},
        })
    else:
        hooks = browser_check.get("hooks", {})
        results.append({
            "test": "library_dashboard_browser_check",
            "pass": isinstance(hooks, dict)
                and isinstance(hooks.get("hooks"), list)
                and "saveChart" in hooks["hooks"]
                and "favoriteChart" in hooks["hooks"]
                and "deleteChart" in hooks["hooks"]
                and "setActive" in hooks["hooks"]
                and "saveView" in hooks["hooks"]
                and "shareUrl" in hooks["hooks"]
                and hooks.get("schemaVersion") == 1
                and not browser_check.get("errors"),
            "detail": browser_check,
        })

    # 12. Delete cleans favorites/views and clears active.
    request("POST", f"/library/charts/{chart_id}/favorite", {"favorite": True})
    request("POST", "/library/active", {"chart_id": chart_id})
    status_d, deleted = request("DELETE", f"/library/charts/{chart_id}")
    _, after_delete = request("GET", "/library/state")
    results.append({
        "test": "delete_clears_dependents",
        "pass": status_d == 200
            and deleted.get("deleted") == chart_id
            and chart_id not in after_delete.get("favorites", [])
            and after_delete.get("active_chart_id") is None
            and all(v.get("chart_id") != chart_id for v in after_delete.get("views", [])),
        "detail": {"deleted": deleted, "state_after": after_delete},
    })

    payload_out = {"results": results, "all_pass": all(r["pass"] for r in results)}
    print(json.dumps(payload_out, indent=2))
    rc = 0 if payload_out["all_pass"] else 1
    if server_proc is not None:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
