"""Rendering diagnosis pass: lat/lon grid vs screen-pixel truth.

Drives the two sandboxes side-by-side at the SAME viewport and zoom
so we can decide whether the visible gaps and dashed lines in the
brute-force renderer come from (a) lat/lon sampling step, (b) the
fixed-pixel drawing primitive, or (c) something projection-related.

For each of three conditions we capture two screenshots:

  A. map_SANDBOX_brute_force.html        (lat/lon grid + fixed dots)
  B. map_SANDBOX_screen_pixel_truth.html (screen-block sampling)

Conditions tested:

  1. Saturn ☌ MC  (meridian centerline; orb 1.0°)
  2. Saturn ☌ ASC (curved centerline; orb 1.0°)
  3. Sun in 1st   (planet-in-house polygon)

Viewport: Pacific 178°E (S/W/N/E = -65/150/65/180). Same bounds
used by orb-sensitivity cases 09 / 09b / 10 — already a known
reference frame for the brute-force renderer.

Both sandboxes already support the ?bounds=s,w,n,e URL parameter, so
the geographic region classified is byte-identical between A and B.

Outputs:
  validation/screenshots/screen_pixel_truth_diagnosis/
    01_saturn_mc_A_brute_force.png
    01_saturn_mc_B_screen_pixel.png
    02_saturn_asc_A_brute_force.png
    02_saturn_asc_B_screen_pixel.png
    03_sun_1st_A_brute_force.png
    03_sun_1st_B_screen_pixel.png
    manifest.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "screen_pixel_truth_diagnosis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BRUTE_URL = "http://127.0.0.1:8000/map_SANDBOX_brute_force.html"
SPT_URL   = "http://127.0.0.1:8000/map_SANDBOX_screen_pixel_truth.html"
PROFILE_ID = "baseline_validated"

# Same viewport for every capture so the comparison is honest.
BOUNDS = "-65,150,65,180"
# Grid + block settings that we expect to expose the diagnosis.
GRID_DEG = "0.1"   # brute-force lat/lon grid step
BLOCK_PX = "4"     # screen-pixel block size for SPT sandbox

CONDITIONS: list[dict[str, Any]] = [
    {
        "case_id": "01_saturn_mc",
        "label":   "Saturn ☌ MC, orb 1.0° (meridian centerline)",
        "slot_a":  "a2a:saturn:mc:conjunction:1.0",
    },
    {
        "case_id": "02_saturn_asc",
        "label":   "Saturn ☌ ASC, orb 1.0° (curved centerline)",
        "slot_a":  "a2a:saturn:asc:conjunction:1.0",
    },
    {
        "case_id": "03_sun_1st",
        "label":   "Sun in 1st house (planet-in-house polygon)",
        "slot_a":  "pih:sun:1",
    },
]

# Second capture set: same conditions, no `?bounds=` override. Both
# sandboxes start at viewport=world, and the brute-force sandbox uses
# `map.getBounds()` (the actual visible viewport, including the wider
# longitude band Leaflet shows after fitBounds-aspect-padding). This
# isolates Bug #2 (drawing primitive) from Bug #1 (sampling-area).
#
# We coarsen the brute-force grid to 0.25° for tractability at world
# scale (~1.5M cells), and bump the screen-pixel block to 6 to keep
# the request fast. Both still classify whatever is on screen.
APPLES_GRID_DEG = "0.25"
APPLES_BLOCK_PX = "6"
APPLES_VIEWPORT = "world"


def brute_url(slot_a: str, *, apples: bool = False) -> str:
    if apples:
        params = {
            "A":        slot_a,
            "gridDeg":  APPLES_GRID_DEG,
            "viewport": APPLES_VIEWPORT,
            "profile":  PROFILE_ID,
            "auto":     "1",
        }
    else:
        params = {
            "A":       slot_a,
            "gridDeg": GRID_DEG,
            "profile": PROFILE_ID,
            "auto":    "1",
            "bounds":  BOUNDS,
        }
    return f"{BRUTE_URL}?{urlencode(params)}"


def spt_url(slot_a: str, *, apples: bool = False) -> str:
    if apples:
        params = {
            "A":        slot_a,
            "block":    APPLES_BLOCK_PX,
            "viewport": APPLES_VIEWPORT,
            "profile":  PROFILE_ID,
            "auto":     "1",
        }
    else:
        params = {
            "A":       slot_a,
            "block":   BLOCK_PX,
            "profile": PROFILE_ID,
            "auto":    "1",
            "bounds":  BOUNDS,
        }
    return f"{SPT_URL}?{urlencode(params)}"


def _capture(page, url: str, image_path: Path,
             status_global: str, timings_global: str) -> dict[str, Any]:
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_function(
        f"() => window.{status_global} === 'complete' "
        f"   || window.{status_global} === 'error'",
        timeout=180_000,
    )
    status = page.evaluate(f"() => window.{status_global}")
    if status != "complete":
        err = page.evaluate(f"() => window.__sptLastError "
                            f"|| window.__bruteLastError")
        raise RuntimeError(f"sandbox status={status} error={err}")
    page.wait_for_timeout(400)
    map_box = page.evaluate(
        "() => { const el = document.getElementById('map'); "
        "const r = el.getBoundingClientRect(); "
        "return {x: r.x, y: r.y, width: r.width, height: r.height}; }"
    )
    page.screenshot(path=str(image_path), clip=map_box)
    timings = page.evaluate(
        f"() => JSON.parse(JSON.stringify(window.{timings_global}))"
    )
    return timings


def run_case(page, case: dict[str, Any]) -> dict[str, Any]:
    print(f"\n=== {case['case_id']}  {case['label']}  [bounded] ===")
    slot = case["slot_a"]

    a_url   = brute_url(slot)
    a_path  = OUT_DIR / f"{case['case_id']}_A_brute_force.png"
    print(f"  A (brute-force):       {a_url}")
    a_tim = _capture(page, a_url, a_path,
                     "__bruteStatus", "__bruteLastTimings")
    print(f"  A saved: {a_path.name}  "
          f"matches={a_tim['matches']:,}  "
          f"server={a_tim['server_compute_seconds']:.2f}s  "
          f"paint={a_tim['paint_ms']:.0f}ms")

    b_url   = spt_url(slot)
    b_path  = OUT_DIR / f"{case['case_id']}_B_screen_pixel.png"
    print(f"  B (screen-pixel):      {b_url}")
    b_tim = _capture(page, b_url, b_path,
                     "__sptStatus", "__sptLastTimings")
    print(f"  B saved: {b_path.name}  "
          f"matches={b_tim['match_count']:,}  "
          f"server={b_tim['server_compute_seconds']:.2f}s  "
          f"paint={b_tim['paint_ms']:.0f}ms")

    return {
        "case_id": case["case_id"],
        "label":   case["label"],
        "slot":    slot,
        "bounds":  BOUNDS,
        "A": {
            "renderer":    "lat_lon_grid_then_fixed_dots",
            "url":         a_url,
            "image":       a_path.name,
            "grid_deg":    float(GRID_DEG),
            "timings":     a_tim,
        },
        "B": {
            "renderer":    "screen_pixel_blocks",
            "url":         b_url,
            "image":       b_path.name,
            "block_px":    int(BLOCK_PX),
            "timings":     b_tim,
        },
    }


def run_case_apples(page, case: dict[str, Any]) -> dict[str, Any]:
    """Apples-to-apples: both renderers classify the same visible
    viewport (no `?bounds=` override on the brute-force side, so it
    uses ``map.getBounds()`` exactly like the SPT sandbox does).
    Isolates Bug #2 (drawing primitive) from Bug #1 (sampling-area).
    """
    print(f"\n=== {case['case_id']}  {case['label']}  [apples-to-apples] ===")
    slot = case["slot_a"]

    a_url   = brute_url(slot, apples=True)
    a_path  = OUT_DIR / f"{case['case_id']}_A_brute_force_apples.png"
    print(f"  A (brute-force, world): {a_url}")
    a_tim = _capture(page, a_url, a_path,
                     "__bruteStatus", "__bruteLastTimings")
    print(f"  A saved: {a_path.name}  "
          f"matches={a_tim['matches']:,}  "
          f"cells={a_tim['total_cells']:,}  "
          f"server={a_tim['server_compute_seconds']:.2f}s")

    b_url   = spt_url(slot, apples=True)
    b_path  = OUT_DIR / f"{case['case_id']}_B_screen_pixel_apples.png"
    print(f"  B (screen-pixel, world): {b_url}")
    b_tim = _capture(page, b_url, b_path,
                     "__sptStatus", "__sptLastTimings")
    print(f"  B saved: {b_path.name}  "
          f"matches={b_tim['match_count']:,}  "
          f"points={b_tim['point_count']:,}  "
          f"server={b_tim['server_compute_seconds']:.2f}s")

    return {
        "case_id": case["case_id"],
        "label":   case["label"],
        "slot":    slot,
        "viewport": APPLES_VIEWPORT,
        "A_apples": {
            "renderer":  "lat_lon_grid_then_fixed_dots",
            "url":       a_url,
            "image":     a_path.name,
            "grid_deg":  float(APPLES_GRID_DEG),
            "timings":   a_tim,
        },
        "B_apples": {
            "renderer":  "screen_pixel_blocks",
            "url":       b_url,
            "image":     b_path.name,
            "block_px":  int(APPLES_BLOCK_PX),
            "timings":   b_tim,
        },
    }


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed")
        return 2
    records: list[dict[str, Any]] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1480, "height": 900},
                                   device_scale_factor=2)
        page = ctx.new_page()
        page.on("pageerror", lambda exc: print(f"  pageerror: {exc}"))
        for case in CONDITIONS:
            try:
                bounded = run_case(page, case)
            except Exception as exc:
                print(f"  FAIL bounded: {exc}")
                bounded = {"case_id": case["case_id"], "label": case["label"],
                           "error_bounded": str(exc)}
            try:
                apples = run_case_apples(page, case)
            except Exception as exc:
                print(f"  FAIL apples: {exc}")
                apples = {"error_apples": str(exc)}
            merged = dict(bounded)
            for k in ("A_apples", "B_apples", "viewport", "error_apples"):
                if k in apples:
                    merged[k] = apples[k]
            records.append(merged)
        browser.close()
    manifest = {
        "schema":             "screen_pixel_truth_diagnosis@2",
        "profile_id":         PROFILE_ID,
        "bounded": {
            "bounds":         BOUNDS,
            "grid_deg":       float(GRID_DEG),
            "block_px":       int(BLOCK_PX),
        },
        "apples_to_apples": {
            "viewport":       APPLES_VIEWPORT,
            "grid_deg":       float(APPLES_GRID_DEG),
            "block_px":       int(APPLES_BLOCK_PX),
        },
        "viewport_px":        [1480, 900],
        "case_count":         len(CONDITIONS),
        "output_dir":         str(OUT_DIR.relative_to(REPO_ROOT)),
        "captures":           records,
    }
    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"\nmanifest: {manifest_path}")
    fail_count = sum(
        1 for r in records
        if r.get("error_bounded") or r.get("error_apples")
    )
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
