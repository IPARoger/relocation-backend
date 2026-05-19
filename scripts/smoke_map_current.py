#!/usr/bin/env python3
"""
Browser smoke test for map_CURRENT.html — catastrophic regression gate only.

Philosophy:
  - Lightweight, one script, one JSON report. Not enterprise test architecture.
  - Smoke must NOT drive production abstractions (minimal hooks: __rmMap, __rmSmokeState).
  - Human QA still owns astrology, aesthetics, overlap semantics, trust.

Workflow:
  IMPLEMENT → validate_sprint_dc_ic.py → this script → report → human QA → commit

Requires:
  - Running server: uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000
  - Playwright: pip install playwright && playwright install chromium

Usage:
  python3 scripts/smoke_map_current.py

Incremental backlog (add when useful — see validation/narratives/smoke_and_handoff_workflow.md):
  - empty GeoJSON, polygon winding, seam/pole fragments, popup stress cycles, API NaN pre-render
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
REPORT_DIR = Path(__file__).resolve().parent.parent / "validation" / "reports"
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BROWSER_PATH = ROOT / ".playwright-browsers"

# Prefer project-local browsers when present (repeatable across sandboxes).
if DEFAULT_BROWSER_PATH.exists():
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(DEFAULT_BROWSER_PATH)


def server_ok() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE}/health", timeout=5) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def run_backend_validation() -> dict:
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "validate_sprint_dc_ic.py")],
        capture_output=True,
        text=True,
        env={**os.environ, "BASE_URL": BASE},
        timeout=180,
    )
    overall_pass = False
    try:
        payload = json.loads(proc.stdout.strip() or "{}")
        overall_pass = bool(payload.get("overall_pass"))
    except json.JSONDecodeError:
        pass
    return {
        "exit_code": proc.returncode,
        "overall_pass": overall_pass,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def bounds_within_max(page) -> bool:
    return page.evaluate(
        """() => {
            const map = window.__rmMap;
            const max = map?.options?.maxBounds;
            if (!map || !max) return false;
            const b = map.getBounds();
            const tol = 0.25;
            return (
                b.getNorth() <= max.getNorth() + tol &&
                b.getSouth() >= max.getSouth() - tol &&
                b.getWest() >= max.getWest() - tol &&
                b.getEast() <= max.getEast() + tol
            );
        }"""
    )


def map_drag_snapback_ok(page) -> dict:
    """Drag past edge at mid zoom; after dragend map must remain inside maxBounds."""
    page.evaluate("() => window.__rmMap.setZoom(3, { animate: false })")
    page.wait_for_timeout(250)
    before = bounds_within_max(page)
    map_box = page.locator("#map").bounding_box()
    assert map_box
    cx = map_box["x"] + map_box["width"] / 2
    cy = map_box["y"] + map_box["height"] / 2
    page.mouse.move(cx, cy)
    page.mouse.down()
    page.mouse.move(cx, cy - 240, steps=14)
    page.mouse.up()
    page.wait_for_timeout(500)
    after = bounds_within_max(page)
    return {"within_max_bounds_before": before, "within_max_bounds_after_drag": after}


def select_opens_and_changes(page, selector: str, target_value: str) -> dict:
    """Click native select, change via select_option, verify DOM value."""
    before = page.evaluate(
        f"() => document.querySelector({json.dumps(selector)}).value"
    )
    page.locator(selector).click()
    focused = page.evaluate(
        f"() => document.activeElement === document.querySelector({json.dumps(selector)})"
    )
    page.select_option(selector, target_value)
    after = page.evaluate(
        f"() => document.querySelector({json.dumps(selector)}).value"
    )
    return {
        "focused_on_click": focused,
        "value_changed": after == target_value and after != before,
        "before": before,
        "after": after,
    }


def trigger_find_regions_and_wait(page, timeout_ms: int = 120000) -> dict:
    """Find Regions uses 400ms debounce; wait for render start then completion."""
    page.locator("#findBtn").click()
    page.wait_for_timeout(450)
    page.wait_for_function(
        """() => {
            const btn = document.getElementById('findBtn');
            const st = document.getElementById('renderStatus')?.textContent || '';
            return btn.disabled || /Rendering|Calculating/i.test(st);
        }""",
        timeout=15000,
    )
    page.wait_for_function(
        """() => {
            const btn = document.getElementById('findBtn');
            const st = document.getElementById('renderStatus')?.textContent || '';
            const s = window.__rmSmokeState();
            return btn && !btn.disabled && /ready/i.test(st) && s.polygonLayers > 0;
        }""",
        timeout=timeout_ms,
    )
    return page.evaluate("() => window.__rmSmokeState()")


def main() -> int:
    if not server_ok():
        print(json.dumps({"overall_pass": False, "error": f"Server not reachable at {BASE}/health"}))
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            json.dumps(
                {
                    "overall_pass": False,
                    "error": "playwright not installed. Run: pip install playwright && playwright install chromium",
                }
            )
        )
        return 1

    bust = int(time.time())
    url = f"{BASE}/map_CURRENT.html?bust={bust}&skipOnboarding=1"
    checks: list[dict] = []
    console_errors: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.on("pageerror", lambda exc: console_errors.append(f"pageerror: {exc}"))
        page.on(
            "console",
            lambda msg: console_errors.append(f"console.{msg.type}: {msg.text}")
            if msg.type == "error"
            else None,
        )

        resp = page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_function(
            "() => document.getElementById('chartProfile')?.options?.length >= 3",
            timeout=15000,
        )

        checks.append(
            {
                "id": "page_loads",
                "pass": resp is not None
                and resp.status == 200
                and page.title() == "Relocation Mapper",
                "detail": {"status": resp.status if resp else None, "title": page.title()},
            }
        )

        profile_labels = page.evaluate(
            """() => [...document.getElementById('chartProfile').options].map(o => o.textContent.trim())"""
        )
        expected_profiles = [
            "Baseline Validated Chart",
            "Edge Case — High Northern Birth",
            "Edge Case — Southern Hemisphere Birth",
        ]
        checks.append(
            {
                "id": "profile_options",
                "pass": profile_labels == expected_profiles,
                "detail": {"labels": profile_labels},
            }
        )

        profile_change = select_opens_and_changes(
            page, "#chartProfile", "edge_high_north"
        )
        checks.append(
            {
                "id": "profile_select_changes",
                "pass": profile_change["value_changed"] and profile_change["focused_on_click"],
                "detail": profile_change,
            }
        )

        planet_change = select_opens_and_changes(page, "#planetA", "moon")
        checks.append(
            {
                "id": "planet_select_changes",
                "pass": planet_change["value_changed"] and planet_change["focused_on_click"],
                "detail": planet_change,
            }
        )

        house_change = select_opens_and_changes(page, "#houseA", "7")
        checks.append(
            {
                "id": "house_select_changes",
                "pass": house_change["value_changed"] and house_change["focused_on_click"],
                "detail": house_change,
            }
        )

        angle_change = select_opens_and_changes(page, "#angleSignAngle", "ASC")
        checks.append(
            {
                "id": "angle_select_changes",
                "pass": angle_change["value_changed"] and angle_change["focused_on_click"],
                "detail": angle_change,
            }
        )

        sign_change = select_opens_and_changes(page, "#angleSignSign", "sagittarius")
        checks.append(
            {
                "id": "sign_select_changes",
                "pass": sign_change["value_changed"] and sign_change["focused_on_click"],
                "detail": sign_change,
            }
        )

        aspect_labels = page.evaluate(
            """() => [...document.getElementById('overlayAspect').options].map(o => o.textContent.trim())"""
        )
        aspect_has_full_labels = all(
            label in aspect_labels
            for label in ["All Major Aspects", "All Hard Aspects", "All Soft Aspects"]
        )
        aspect_change = select_opens_and_changes(page, "#overlayAspect", "any")
        checks.append(
            {
                "id": "aspect_select",
                "pass": aspect_has_full_labels
                and aspect_change["value_changed"]
                and aspect_change["focused_on_click"],
                "detail": {"labels": aspect_labels, **aspect_change},
            }
        )

        find_btn = page.locator("#findBtn")
        find_visible = find_btn.is_visible()
        find_enabled = find_btn.is_enabled()
        find_box = find_btn.bounding_box()
        viewport = page.viewport_size or {"width": 0, "height": 0}
        find_in_viewport = bool(
            find_box
            and find_box["y"] >= 0
            and find_box["y"] + find_box["height"] <= viewport["height"]
        )
        overlay_state = trigger_find_regions_and_wait(page)
        checks.append(
            {
                "id": "find_regions_clickable",
                "pass": find_visible and find_enabled and find_in_viewport,
                "detail": {"visible": find_visible, "enabled": find_enabled, "in_viewport": find_in_viewport},
            }
        )
        checks.append(
            {
                "id": "overlay_generation",
                "pass": overlay_state["polygonLayers"] > 0
                and overlay_state["aspectLayers"] > 0
                and overlay_state["nonFiniteCoords"] == 0,
                "detail": overlay_state,
            }
        )

        overlay_state_2 = trigger_find_regions_and_wait(page)
        checks.append(
            {
                "id": "find_regions_repeat",
                "pass": overlay_state_2["polygonLayers"] > 0
                and overlay_state_2["aspectLayers"] > 0
                and overlay_state_2["nonFiniteCoords"] == 0,
                "detail": overlay_state_2,
            }
        )

        page.select_option("#chartProfile", "baseline_validated")
        overlay_state_3 = trigger_find_regions_and_wait(page)
        checks.append(
            {
                "id": "profile_switch_rerender",
                "pass": overlay_state_3["polygonLayers"] > 0
                and overlay_state_3["nonFiniteCoords"] == 0,
                "detail": overlay_state_3,
            }
        )

        drag_result = map_drag_snapback_ok(page)
        checks.append(
            {
                "id": "map_bounds_snapback",
                "pass": drag_result["within_max_bounds_before"]
                and drag_result["within_max_bounds_after_drag"],
                "detail": drag_result,
            }
        )

        map_box = page.locator("#map").bounding_box()
        assert map_box
        cx = map_box["x"] + map_box["width"] / 2
        cy = map_box["y"] + map_box["height"] / 2

        zoom_before = page.evaluate("() => window.__rmMap.getZoom()")
        page.mouse.dblclick(cx, cy)
        page.wait_for_timeout(400)
        zoom_after = page.evaluate("() => window.__rmMap.getZoom()")
        page.mouse.dblclick(cx, cy)
        page.wait_for_timeout(400)
        zoom_after_2 = page.evaluate("() => window.__rmMap.getZoom()")
        checks.append(
            {
                "id": "double_click_zoom",
                "pass": zoom_after > zoom_before and zoom_after_2 >= zoom_after,
                "detail": {
                    "before": zoom_before,
                    "after_first": zoom_after,
                    "after_second": zoom_after_2,
                },
            }
        )

        page.mouse.click(cx, cy, button="right")
        page.wait_for_selector(".leaflet-popup", timeout=10000)
        popup_open_1 = page.locator(".leaflet-popup").count() > 0
        page.mouse.click(cx + 40, cy + 40)
        page.wait_for_timeout(300)
        popup_open_2 = page.locator(".leaflet-popup").count() > 0
        checks.append(
            {
                "id": "popup_open_and_close",
                "pass": popup_open_1 and not popup_open_2,
                "detail": {"opened": popup_open_1, "closed_after_map_click": not popup_open_2},
            }
        )

        checks.append(
            {
                "id": "console_clean",
                "pass": len(console_errors) == 0,
                "detail": {"errors": console_errors},
            }
        )

        browser.close()

    backend = run_backend_validation()
    checks.append(
        {
            "id": "backend_validation",
            "pass": backend["overall_pass"] and backend["exit_code"] == 0,
            "detail": backend,
        }
    )

    overall_pass = all(c["pass"] for c in checks)
    report = {
        "description": "map_CURRENT.html browser smoke test",
        "url": url,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "overall_pass": overall_pass,
        "checks": checks,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "map_current_smoke.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"overall_pass": overall_pass, "report": str(report_path), "url": url}, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
