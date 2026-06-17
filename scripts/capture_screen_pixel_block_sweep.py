"""Screen-pixel block-size sweep against the lat/lon-grid renderer.

This is the "deliberately dumb maximal proof" capture. For each test
condition (5 total), we hold the visible map identical between the
existing brute-force lat/lon-grid sandbox and the screen-pixel truth
sandbox via `?fitBounds=`. The brute-force sandbox then queries whatever
Leaflet actually shows (map.getBounds()), so the two renderers see the
same screen-space surface. The screen-pixel sandbox is run four times
per condition, at block_px ∈ {1, 2, 4, 8}, to map the speed/coverage
trade-off.

Output:
    validation/screenshots/screen_pixel_block_sweep/
        <case>_brute_ref.png
        <case>_spt_block_1.png
        <case>_spt_block_2.png
        <case>_spt_block_4.png
        <case>_spt_block_8.png
        manifest.json

Each manifest entry includes server compute time, client total, match
counts, and the actual visible bounds Leaflet ended up with so the
comparison can be reproduced.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000"
PROFILE = "baseline_validated"
VIEWPORT = (1480, 900)
FIT_BOUNDS = (-65.0, 150.0, 65.0, 180.0)  # south, west, north, east

OUT_DIR = Path("validation/screenshots/screen_pixel_block_sweep")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Condition slot strings use the brute-force sandbox URL syntax.
CASES: list[dict] = [
    {
        "id": "01_sun_in_1st",
        "label": "Sun in 1st House",
        "slot": "pih:sun:1",
    },
    {
        "id": "02_saturn_conj_mc_orb_1",
        "label": "Saturn ☌ MC, orb 1°",
        "slot": "a2a:saturn:mc:conjunction:1.0",
    },
    {
        "id": "03_saturn_conj_asc_orb_1",
        "label": "Saturn ☌ ASC, orb 1°",
        "slot": "a2a:saturn:asc:conjunction:1.0",
    },
    {
        "id": "04_saturn_conj_mc_orb_6",
        "label": "Saturn ☌ MC, orb 6°",
        "slot": "a2a:saturn:mc:conjunction:6.0",
    },
    {
        "id": "05_saturn_conj_asc_orb_6",
        "label": "Saturn ☌ ASC, orb 6°",
        "slot": "a2a:saturn:asc:conjunction:6.0",
    },
]

BLOCK_SIZES = [1, 2, 4, 8]
BRUTE_GRID_DEG = 0.5  # makes the lat/lon-grid gap problem obvious at zoom


def fit_bounds_param() -> str:
    s, w, n, e = FIT_BOUNDS
    return f"{s},{w},{n},{e}"


def brute_url(slot: str) -> str:
    fb = fit_bounds_param()
    return (
        f"{BASE}/map_SANDBOX_brute_force.html"
        f"?profile={PROFILE}"
        f"&fitBounds={fb}"
        f"&gridDeg={BRUTE_GRID_DEG}"
        f"&A={slot}"
    )


def spt_url(slot: str, block_px: int) -> str:
    fb = fit_bounds_param()
    return (
        f"{BASE}/map_SANDBOX_screen_pixel_truth.html"
        f"?profile={PROFILE}"
        f"&fitBounds={fb}"
        f"&block={block_px}"
        f"&A={slot}"
    )


def wait_for_status(page, var: str, value: str, timeout_ms: int = 60_000) -> None:
    """Wait until `window[var]` becomes `value` or 'error'.

    Treating 'error' as terminal lets us fail fast on bad slot syntax /
    misconfiguration instead of burning the entire timeout.
    """
    page.wait_for_function(
        f"window.{var} === '{value}' || window.{var} === 'error'",
        timeout=timeout_ms,
    )
    actual = page.evaluate(f"window.{var}")
    if actual == "error":
        err_var = var.replace("Status", "LastError")
        last_err = page.evaluate(f"window.{err_var}")
        raise RuntimeError(f"{var} reached 'error' (waiting for '{value}'): {last_err}")


def capture_brute(page, slot: str, out_png: Path) -> dict:
    url = brute_url(slot)
    page.goto(url, wait_until="domcontentloaded")
    wait_for_status(page, "__bruteStatus", "ready", timeout_ms=30_000)
    # Let basemap tiles settle so the screenshot includes the geography.
    page.wait_for_timeout(800)
    t0 = time.time()
    page.evaluate("window.__runBruteForce()")
    wait_for_status(page, "__bruteStatus", "complete", timeout_ms=120_000)
    wall = time.time() - t0
    timings = page.evaluate("window.__bruteLastTimings")
    page.screenshot(path=str(out_png), full_page=False)
    return {
        "url": url,
        "wall_seconds": wall,
        "timings": timings,
    }


def capture_spt(page, slot: str, block_px: int, out_png: Path) -> dict:
    url = spt_url(slot, block_px)
    page.goto(url, wait_until="domcontentloaded")
    wait_for_status(page, "__sptStatus", "ready", timeout_ms=30_000)
    page.wait_for_timeout(800)
    t0 = time.time()
    page.evaluate("window.__runScreenPixelTruth()")
    # 1px @ 1480x900 = 1.33M points → ~4 chunks * ~2s + paint. Empirically
    # ~9s wall; 60s leaves comfortable headroom while still failing fast on
    # silent hangs.
    wait_for_status(page, "__sptStatus", "complete", timeout_ms=60_000)
    wall = time.time() - t0
    timings = page.evaluate("window.__sptLastTimings")
    page.screenshot(path=str(out_png), full_page=False)
    return {
        "url": url,
        "wall_seconds": wall,
        "timings": timings,
    }


def main() -> None:
    started = time.time()
    manifest: dict = {
        "viewport": {"width": VIEWPORT[0], "height": VIEWPORT[1]},
        "fit_bounds": {
            "south": FIT_BOUNDS[0], "west": FIT_BOUNDS[1],
            "north": FIT_BOUNDS[2], "east": FIT_BOUNDS[3],
        },
        "brute_grid_deg": BRUTE_GRID_DEG,
        "block_sizes": BLOCK_SIZES,
        "profile": PROFILE,
        "cases": [],
    }

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": VIEWPORT[0], "height": VIEWPORT[1]})
        page = ctx.new_page()
        page.set_default_timeout(120_000)

        for case in CASES:
            print(f"\n=== {case['id']}  {case['label']} ===", flush=True)
            case_entry: dict = {
                "id": case["id"],
                "label": case["label"],
                "slot": case["slot"],
            }

            ref_png = OUT_DIR / f"{case['id']}_brute_ref.png"
            try:
                ref = capture_brute(page, case["slot"], ref_png)
                t = ref["timings"] or {}
                print(
                    f"  brute-force ref · cells={t.get('total_cells', '?'):>9} "
                    f"matches={t.get('match_count', '?'):>7} "
                    f"server={t.get('server_compute_seconds', 0):.2f}s "
                    f"wall={ref['wall_seconds']:.2f}s",
                    flush=True,
                )
                case_entry["brute_ref"] = {
                    "screenshot": str(ref_png),
                    **ref,
                }
            except Exception as err:
                print(f"  brute-force ref FAILED: {err}", flush=True)
                case_entry["brute_ref"] = {
                    "screenshot": str(ref_png) if ref_png.exists() else None,
                    "error": str(err),
                }

            case_entry["spt"] = {}
            for bpx in BLOCK_SIZES:
                spt_png = OUT_DIR / f"{case['id']}_spt_block_{bpx}.png"
                try:
                    spt = capture_spt(page, case["slot"], bpx, spt_png)
                    t = spt["timings"] or {}
                    print(
                        f"  spt block_px={bpx:<2} · points={t.get('point_count', '?'):>9} "
                        f"matches={t.get('match_count', '?'):>7} "
                        f"server={t.get('server_compute_seconds', 0):.2f}s "
                        f"wall={spt['wall_seconds']:.2f}s",
                        flush=True,
                    )
                    case_entry["spt"][str(bpx)] = {
                        "screenshot": str(spt_png),
                        **spt,
                    }
                except Exception as err:
                    print(f"  spt block_px={bpx} FAILED: {err}", flush=True)
                    case_entry["spt"][str(bpx)] = {
                        "screenshot": str(spt_png) if spt_png.exists() else None,
                        "error": str(err),
                    }

            manifest["cases"].append(case_entry)

        ctx.close()
        browser.close()

    manifest["wall_seconds_total"] = time.time() - started
    out_manifest = OUT_DIR / "manifest.json"
    out_manifest.write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest written to {out_manifest}", flush=True)
    print(f"Total wall: {manifest['wall_seconds_total']:.1f}s", flush=True)


if __name__ == "__main__":
    main()
