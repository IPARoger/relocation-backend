"""Multi-condition brute-force proof capture matrix.

Drives ``map_SANDBOX_brute_force.html`` with the new condition-slot
URL parameters (``?A=sun:1&B=moon:4&C=mars:2``) and captures:

  * one-condition baseline (A only)
  * two-condition result (A + B)
  * three-condition result (A + B + C)
  * overlap close-up (zoomed onto the A∩B region for the same chart)

Each case records the engine's reported per-condition counts, every
pairwise overlap count, the triple overlap count, and server/client/paint
timings. No optimisation; the same `/brute-force-grid` endpoint is hit
for every case.

Output: ``validation/screenshots/brute_force_multi/``
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "brute_force_multi"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_URL = "http://127.0.0.1:8000/map_SANDBOX_brute_force.html"
PROFILE_ID = "baseline_validated"
GRID_DEG = "0.25"

# Each case enables 1, 2, or 3 condition slots via URL params. Slot
# values are encoded as `planet:house`. Disabled slots are omitted
# (sandbox defaults them to "disabled checkbox" state).
CASES: list[dict[str, Any]] = [
    {
        "case_id": "01_one_condition_sun_1st",
        "description": "Baseline — single condition A = Sun in 1st, Americas, 0.25°.",
        "params": {"A": "sun:1", "viewport": "americas"},
    },
    {
        "case_id": "02_two_conditions_sun_1st_moon_4th",
        "description": "Two conditions — A = Sun in 1st, B = Moon in 4th. "
                       "Per the chart there should be a real intersection "
                       "(rendered as the yellow+blue→green blend).",
        "params": {"A": "sun:1", "B": "moon:4", "viewport": "americas"},
    },
    {
        "case_id": "03_three_conditions_sun_1st_moon_4th_mars_2nd",
        "description": "Three conditions — A = Sun in 1st, B = Moon in 4th, "
                       "C = Mars in 2nd. Tests that the renderer handles all "
                       "seven mask states.",
        "params": {"A": "sun:1", "B": "moon:4", "C": "mars:2", "viewport": "americas"},
    },
    {
        "case_id": "04_overlap_closeup_sun_1st_moon_4th",
        "description": "Same A + B as case 02, zoomed onto the A∩B region "
                       "(eastern US) so the green overlap polygon is clearly "
                       "legible against the basemap.",
        "params": {"A": "sun:1", "B": "moon:4"},
        "manual_bounds": {"south": 24.0, "north": 50.0, "west": -97.0, "east": -67.0},
    },
    # Bonus: same multi-condition setup at world view so the
    # whole-Earth shape relationship is visible.
    {
        "case_id": "05_three_conditions_world_0.5deg",
        "description": "Same three conditions but at world viewport with 0.5° "
                       "grid (cheap, shows the global topology of overlap).",
        "params": {"A": "sun:1", "B": "moon:4", "C": "mars:2",
                   "viewport": "world", "gridDeg": "0.5"},
        "override_grid_deg": "0.5",
    },
]


def build_url(case: dict[str, Any]) -> str:
    params = dict(case["params"])
    params.setdefault("profile", PROFILE_ID)
    params.setdefault("gridDeg", case.get("override_grid_deg", GRID_DEG))
    params.setdefault("auto", "1")
    return f"{SANDBOX_URL}?{urlencode(params)}"


def capture_case(page, case: dict[str, Any]) -> dict[str, Any]:
    url = build_url(case)
    print(f"\n=== {case['case_id']} ===")
    print(f"  url: {url}")
    timeout_ms = int(case.get("timeout_seconds", 90)) * 1000
    page.goto(url, wait_until="domcontentloaded")

    # For the close-up case, wait for the auto-run to complete, then
    # tighten the bounds and re-run on the same page.
    if case.get("manual_bounds"):
        b = case["manual_bounds"]
        page.wait_for_function(
            "() => window.__bruteStatus === 'complete' || window.__bruteStatus === 'error'",
            timeout=timeout_ms,
        )
        page.evaluate(
            "(b) => { if (!window.__map) throw new Error('window.__map missing'); "
            "window.__map.fitBounds([[b.south, b.west], [b.north, b.east]]); "
            "window.__bruteStatus = 'ready'; }",
            b,
        )
        page.wait_for_timeout(400)  # let bounds settle
        page.evaluate("() => document.getElementById('runBtn').click()")

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
    page.wait_for_timeout(400)

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
    o = timings.get("overlap_counts") or {}
    print(f"  saved: {image_path.name}")
    print(f"  cells={timings['total_cells']:,}  "
          f"any={timings['matches']:,}  "
          f"server={timings['server_compute_seconds']:.2f}s")
    print(f"  per-condition: " + ", ".join(
        f"{c['id']}={c['count']:,}" for c in timings["conditions"]))
    overlap_keys = [k for k in o if k != "any" and not k.endswith("_only")]
    if overlap_keys:
        print(f"  overlaps: " + ", ".join(f"{k}={o[k]:,}" for k in overlap_keys))
    return record


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed")
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
        "schema": "brute_force_multi_condition_proof@1",
        "sandbox_url": SANDBOX_URL,
        "profile_id": PROFILE_ID,
        "grid_deg": GRID_DEG,
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
