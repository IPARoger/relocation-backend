"""Brute-force polygon proof capture matrix.

For each (target, viewport, grid_resolution, lat_cap_policy) case, drives
``map_SANDBOX_brute_force.html`` to:

  * classify every cell of a regular lat/lon grid covering the visible
    viewport via real ``swe.houses`` (no sampling, no smoothing),
  * draw ONLY the matching cells as tiny translucent yellow squares,
  * screenshot the map pane only,
  * record server compute time, client wall time, paint ms, total cell
    count, match count, and points/second.

A consolidated ``manifest.json`` is written next to the stills. No
optimisation; the request body and timings are exactly what the engine
returns.

Output: ``validation/screenshots/brute_force_proof/``

Usage:
    PLAYWRIGHT_BROWSERS_PATH=./venv/lib/python3.11/site-packages/playwright/driver/package/.local-browsers \\
        ./venv/bin/python3 scripts/capture_brute_force_proof.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "brute_force_proof"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_URL = "http://127.0.0.1:8000/map_SANDBOX_brute_force.html"
PROFILE_ID = "baseline_validated"

# Each case is one brute-force call. They run sequentially in a single
# headless Chromium so the cache stays warm and timings are comparable.
CASES: list[dict[str, Any]] = [
    # --- Resolution sweep: same target + viewport, varying grid_deg.
    # This is the "convergence to a continuous shape" demonstration.
    {
        "case_id": "sun_1st_americas_grid_1.0deg",
        "description": "Sun in 1st, Americas viewport, 1.0° grid (coarse — fast).",
        "params": {"planet": "sun", "house": "1", "viewport": "americas",
                   "gridDeg": "1.0", "dotRadius": "1.4", "dotAlpha": "0.55"},
    },
    {
        "case_id": "sun_1st_americas_grid_0.5deg",
        "description": "Sun in 1st, Americas, 0.5° grid (default).",
        "params": {"planet": "sun", "house": "1", "viewport": "americas",
                   "gridDeg": "0.5", "dotRadius": "1.2", "dotAlpha": "0.45"},
    },
    {
        "case_id": "sun_1st_americas_grid_0.25deg",
        "description": "Sun in 1st, Americas, 0.25° grid (fine).",
        "params": {"planet": "sun", "house": "1", "viewport": "americas",
                   "gridDeg": "0.25", "dotRadius": "1.0", "dotAlpha": "0.4"},
    },
    {
        "case_id": "sun_1st_americas_grid_0.1deg",
        "description": "Sun in 1st, Americas, 0.1° grid (very fine — ~3M cells).",
        "params": {"planet": "sun", "house": "1", "viewport": "americas",
                   "gridDeg": "0.1", "dotRadius": "0.7", "dotAlpha": "0.30"},
        "timeout_seconds": 240,
    },
    # --- World viewport with a feasible grid; confirms shape at world scale.
    {
        "case_id": "sun_1st_world_grid_0.5deg",
        "description": "Sun in 1st, World viewport, 0.5° grid.",
        "params": {"planet": "sun", "house": "1", "viewport": "world",
                   "gridDeg": "0.5", "dotRadius": "1.0", "dotAlpha": "0.45"},
        "timeout_seconds": 180,
    },
    # --- Other targets at the proof-quality resolution.
    {
        "case_id": "moon_4th_americas_grid_0.25deg",
        "description": "Moon in 4th, Americas, 0.25° grid.",
        "params": {"planet": "moon", "house": "4", "viewport": "americas",
                   "gridDeg": "0.25", "dotRadius": "1.0", "dotAlpha": "0.4"},
    },
    {
        "case_id": "mars_2nd_americas_grid_0.25deg",
        "description": "Mars in 2nd, Americas, 0.25° grid.",
        "params": {"planet": "mars", "house": "2", "viewport": "americas",
                   "gridDeg": "0.25", "dotRadius": "1.0", "dotAlpha": "0.4"},
    },
    {
        "case_id": "saturn_12th_americas_grid_0.25deg",
        "description": "Saturn in 12th, Americas, 0.25° grid (matches one of "
                       "the user reference screenshots).",
        "params": {"planet": "saturn", "house": "12", "viewport": "americas",
                   "gridDeg": "0.25", "dotRadius": "1.0", "dotAlpha": "0.4"},
    },
    # --- Lat-cap A/B at fine resolution: cap ON suppresses polar Placidus
    # error rows; cap OFF shows the raw engine behaviour at high latitude.
    {
        "case_id": "sun_1st_americas_grid_0.25deg_latcap_on",
        "description": "Sun in 1st, Americas, 0.25° grid, ±65° lat-cap ON. "
                       "Polar error rows should disappear; the polygon should "
                       "be flat-topped at the cap.",
        "params": {"planet": "sun", "house": "1", "viewport": "americas",
                   "gridDeg": "0.25", "latCap": "1",
                   "dotRadius": "1.0", "dotAlpha": "0.4"},
    },
    # --- Pacific zoom at very fine resolution; tests perception threshold.
    {
        "case_id": "sun_1st_world_grid_1.0deg",
        "description": "Sun in 1st, World viewport, 1.0° grid (baseline density "
                       "for the world-scale shape).",
        "params": {"planet": "sun", "house": "1", "viewport": "world",
                   "gridDeg": "1.0", "dotRadius": "1.4", "dotAlpha": "0.55"},
    },
]


def build_url(case: dict[str, Any]) -> str:
    params = dict(case["params"])
    params.setdefault("profile", PROFILE_ID)
    params["auto"] = "1"
    return f"{SANDBOX_URL}?{urlencode(params)}"


def capture_case(page, case: dict[str, Any]) -> dict[str, Any]:
    url = build_url(case)
    print(f"\n=== {case['case_id']} ===")
    print(f"  url: {url}")
    timeout_ms = int(case.get("timeout_seconds", 90)) * 1000
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_function(
        "() => window.__bruteStatus === 'complete' || window.__bruteStatus === 'error'",
        timeout=timeout_ms,
    )
    status = page.evaluate("() => window.__bruteStatus")
    if status != "complete":
        err = page.evaluate("() => window.__bruteLastError")
        raise RuntimeError(f"sandbox status={status}, error={err}")

    timings = page.evaluate(
        "() => JSON.parse(JSON.stringify(window.__bruteLastTimings))"
    )
    page.wait_for_timeout(400)  # let canvas paint settle

    map_box = page.evaluate(
        "() => { const el = document.getElementById('map'); "
        "const r = el.getBoundingClientRect(); "
        "return {x: r.x, y: r.y, width: r.width, height: r.height}; }"
    )
    image_path = OUT_DIR / f"{case['case_id']}.png"
    page.screenshot(path=str(image_path), clip=map_box)

    record: dict[str, Any] = {
        "case_id": case["case_id"],
        "description": case["description"],
        "image": image_path.name,
        "url": url,
        "params": case["params"],
        "timings": timings,
    }
    print(f"  saved: {image_path.name}")
    print(f"  cells={timings['total_cells']:,}  "
          f"matches={timings['matches']:,}  "
          f"server={timings['server_compute_seconds']:.2f}s  "
          f"client={timings['client_total_seconds']:.2f}s  "
          f"paint={timings['paint_ms']:.0f}ms  "
          f"rate={timings['points_per_second_server']:,.0f} pts/s")
    return record


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed; install via `./venv/bin/pip install playwright`")
        return 2
    records: list[dict[str, Any]] = []
    page_errors: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1480, "height": 900},
                                   device_scale_factor=2)
        page = ctx.new_page()
        page.on("pageerror", lambda exc: page_errors.append(f"pageerror: {exc}"))
        for case in CASES:
            try:
                records.append(capture_case(page, case))
            except Exception as exc:
                print(f"  FAIL: {exc}")
                records.append({
                    "case_id": case["case_id"],
                    "image": None,
                    "error": str(exc),
                    "url": build_url(case),
                    "params": case["params"],
                })
        browser.close()

    manifest = {
        "schema": "brute_force_polygon_proof@1",
        "sandbox_url": SANDBOX_URL,
        "profile_id": PROFILE_ID,
        "output_dir": str(OUT_DIR.relative_to(REPO_ROOT)),
        "case_count": len(CASES),
        "pass_count": sum(1 for r in records if not r.get("error")),
        "fail_count": sum(1 for r in records if r.get("error")),
        "page_errors": page_errors,
        "captures": records,
    }
    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"\nmanifest: {manifest_path}")
    print(f"captures: {manifest['pass_count']}/{manifest['case_count']} ok, "
          f"{manifest['fail_count']} fail, {len(page_errors)} page errors")
    return 0 if manifest["fail_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
