#!/usr/bin/env python3
"""
Debug/prototype smoke for map_CURRENT.html aura paths.

This is NOT production default smoke, NOT evidence of production aura
integration, and NOT a renderer substrate flip. It only validates explicitly
debug-gated raster/adaptive aura behavior on map_CURRENT.html.

Requires:
  - Running server: uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000
  - Playwright: pip install playwright && playwright install chromium

Usage:
  python3 scripts/smoke_map_current_aura_debug.py
"""

from __future__ import annotations

import json
import os
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


def trigger_aura_and_wait(page, timeout_ms: int = 180000) -> dict:
    """Find Regions uses 400ms debounce; wait for debug aura completion."""
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
            return btn && !btn.disabled && /ready/i.test(st)
                && s.rasterAura?.initialized === true;
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

        raster_bust = int(time.time())
        raster_url = (
            f"{BASE}/map_CURRENT.html?bust={raster_bust}&skipOnboarding=1"
            f"&rasterAura=1&debugAura=1"
        )
        raster_resp = page.goto(raster_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_function(
            "() => document.getElementById('chartProfile')?.options?.length >= 3",
            timeout=45000,
        )
        checks.append(
            {
                "id": "raster_debug_page_loads",
                "pass": raster_resp is not None
                and raster_resp.status == 200
                and page.title() == "Relocation Mapper",
                "detail": {"status": raster_resp.status if raster_resp else None, "url": raster_url},
            }
        )
        page.select_option("#overlayPlanet", "sun")
        page.select_option("#overlayAspect", "conjunction")
        page.select_option("#overlayAngle", "ASC")
        raster_console_before = len(console_errors)
        raster_state = trigger_aura_and_wait(page, timeout_ms=180000)
        raster_hook = page.evaluate("() => window.__rmRasterAuraState?.() || null")
        raster_canvas_visible = page.evaluate(
            """() => {
                const c = document.getElementById('auraRasterCanvas');
                return c && c.style.display !== 'none' && c.width > 0;
            }"""
        )
        checks.append(
            {
                "id": "raster_aura_initializes",
                "pass": bool(
                    raster_hook
                    and raster_hook.get("initialized")
                    and raster_hook.get("stage") == "final"
                    and raster_canvas_visible
                ),
                "detail": {"hook": raster_hook, "canvas_visible": raster_canvas_visible},
            }
        )
        checks.append(
            {
                "id": "raster_aura_no_runaway_layers",
                "pass": raster_state["auraLayers"] == 0
                and (raster_hook or {}).get("sampleCount", 0) < 150000,
                "detail": {
                    "aura_polygon_layers": raster_state["auraLayers"],
                    "raster": raster_hook,
                },
            }
        )
        profile_repeat = select_opens_and_changes(page, "#chartProfile", "edge_high_north")
        checks.append(
            {
                "id": "raster_page_dropdown_stable",
                "pass": profile_repeat["value_changed"] and profile_repeat["focused_on_click"],
                "detail": profile_repeat,
            }
        )
        checks.append(
            {
                "id": "raster_console_clean",
                "pass": len(console_errors) == raster_console_before,
                "detail": {
                    "new_errors": console_errors[raster_console_before:],
                },
            }
        )

        adaptive_bust = int(time.time()) + 1
        adaptive_url = (
            f"{BASE}/map_CURRENT.html?bust={adaptive_bust}&skipOnboarding=1"
            f"&debugAdaptive=1&debugAura=1"
        )
        adaptive_resp = page.goto(adaptive_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_function(
            "() => document.getElementById('chartProfile')?.options?.length >= 3",
            timeout=45000,
        )
        checks.append(
            {
                "id": "adaptive_debug_page_loads",
                "pass": adaptive_resp is not None
                and adaptive_resp.status == 200
                and page.title() == "Relocation Mapper",
                "detail": {"status": adaptive_resp.status if adaptive_resp else None, "url": adaptive_url},
            }
        )
        adaptive_console_before = len(console_errors)
        adaptive_api = page.evaluate(
            """async () => {
                const r = await fetch("http://127.0.0.1:8000/aura-raster-adaptive", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        birth_year: 1990,
                        birth_month: 6,
                        birth_day: 21,
                        birth_hour_utc: 12,
                        aspect_overlay: { planet: "sun", aspect: "conjunction", angle: "ASC" },
                        north: 40,
                        south: 20,
                        west: -20,
                        east: 20,
                        paint_width: 48,
                        paint_height: 36,
                        max_depth: 5,
                        initial_divisions: 4,
                        max_samples: 8000,
                        max_leaves: 2000
                    })
                });
                if (!r.ok) return { ok: false, status: r.status };
                const data = await r.json();
                const conv = data.properties?.convergence_vs_reference;
                const reveal = await fetch("http://127.0.0.1:8000/aura-raster-adaptive", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        birth_year: 1990,
                        birth_month: 6,
                        birth_day: 21,
                        birth_hour_utc: 12,
                        aspect_overlay: { planet: "sun", aspect: "conjunction", angle: "ASC" },
                        north: 10,
                        south: -10,
                        west: -100,
                        east: -80,
                        paint_width: 32,
                        paint_height: 24,
                        max_depth: 4,
                        initial_divisions: 5,
                        include_reveal_transport: true,
                        refinement_stage_id: "regional_refine"
                    })
                });
                const revealData = reveal.ok ? await reveal.json() : null;
                const rt = revealData?.reveal_transport;
                return {
                    ok: true,
                    render_mode: data.properties?.render_mode,
                    samples: data.properties?.truth_sample_count,
                    cells: data.properties?.cell_count,
                    stop_reason: data.properties?.stop_reason,
                    converged: conv?.converged,
                    max_delta: conv?.max_delta_vs_reference,
                    reveal_ok: Boolean(rt?.replace_prior_snapshot),
                    reveal_stage: rt?.requested_stage?.stage_id,
                    reveal_samples: rt?.truth_sample_count_reported || 0
                };
            }"""
        )
        checks.append(
            {
                "id": "adaptive_aura_api",
                "pass": bool(
                    adaptive_api.get("ok")
                    and adaptive_api.get("render_mode") == "adaptive_raster"
                    and adaptive_api.get("samples", 0) > 0
                    and adaptive_api.get("stop_reason")
                    and adaptive_api.get("converged") is not None
                    and adaptive_api.get("reveal_ok")
                    and adaptive_api.get("reveal_stage") == "regional_refine"
                    and adaptive_api.get("reveal_samples", 0) > 0
                ),
                "detail": adaptive_api,
            }
        )
        page.select_option("#overlayPlanet", "sun")
        page.select_option("#overlayAspect", "conjunction")
        page.select_option("#overlayAngle", "ASC")
        adaptive_ui_before = len(console_errors)
        adaptive_state = trigger_aura_and_wait(page, timeout_ms=240000)
        adaptive_hook = page.evaluate("() => window.__rmRasterAuraState?.() || null")
        adaptive_canvas = page.evaluate(
            """() => {
                const c = document.getElementById('auraRasterCanvas');
                return c && c.style.display !== 'none' && c.width > 0;
            }"""
        )
        checks.append(
            {
                "id": "adaptive_aura_ui_initializes",
                "pass": bool(
                    adaptive_hook
                    and adaptive_hook.get("initialized")
                    and adaptive_hook.get("stage") == "final"
                    and adaptive_hook.get("renderMode") == "adaptive"
                    and adaptive_canvas
                    and adaptive_state["auraLayers"] == 0
                ),
                "detail": {
                    "hook": adaptive_hook,
                    "canvas_visible": adaptive_canvas,
                    "aura_polygon_layers": adaptive_state["auraLayers"],
                },
            }
        )
        checks.append(
            {
                "id": "adaptive_console_clean",
                "pass": len(console_errors) == adaptive_console_before
                and len(console_errors) == adaptive_ui_before,
                "detail": {
                    "new_errors_after_api": console_errors[adaptive_console_before:],
                    "new_errors_after_ui": console_errors[adaptive_ui_before:],
                },
            }
        )

        browser.close()

    overall_pass = all(c["pass"] for c in checks)
    report = {
        "description": "map_CURRENT.html aura debug/prototype smoke test",
        "status": "debug/prototype validation only; not production default smoke",
        "base_url": BASE,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "overall_pass": overall_pass,
        "checks": checks,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "map_current_aura_debug_smoke.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"overall_pass": overall_pass, "report": str(report_path)}, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
