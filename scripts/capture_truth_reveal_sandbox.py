"""Visual QA capture harness for ``map_SANDBOX_truth_reveal.html``.

Drives the sandbox through a deterministic matrix of (mode, stage, viewport,
lat-cap) cases via Playwright. For every case, the script:

* loads the sandbox with explicit URL params (no rendering-logic changes),
* waits for ``window.__sandboxStatus === "complete"`` (a control signal
  set by the sandbox's existing run loop),
* captures a PNG of the map pane only (panel cropped out),
* reads the per-stage engine response (real ``properties.*`` fields from
  ``/aura-raster-convergence``) directly out of ``window.__sandboxStageResults``,
* writes both PNG and per-case metrics JSON to
  ``validation/screenshots/truth_field_sandbox/``.

The harness asserts only what the engine actually reported. It does not
claim "looks calm" or any perceptual property. A consolidated manifest is
written at ``manifest.json`` for the QA narrative to link.

Usage:
    ./venv/bin/python3 scripts/capture_truth_reveal_sandbox.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "truth_field_sandbox"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_URL = "http://127.0.0.1:8000/map_SANDBOX_truth_reveal.html"
PROFILE_ID = "baseline_validated"

# Each case explicitly states what is being captured. The query params drive
# the existing sandbox control hooks (?mode, ?viewport, ?stopAtStage,
# ?latCap, ?profile, ?auto=1) — they do NOT alter rendering.
CASES: list[dict[str, Any]] = [
    # 1. Mode A — Silent Convergence: stage 0 + final, same viewport
    {
        "case_id": "mode_a_silent_stage0_asc_band",
        "mode": "silent",
        "stage_target": "stage_0",
        "viewport": "asc_band",
        "lat_cap": "on",
        "params": {"mode": "silent", "viewport": "asc", "stopAtStage": "0"},
        "description": "Mode A, seed stage only (max_samples=240). Same viewport "
                       "as the final-stage capture so QA can compare directly.",
    },
    {
        "case_id": "mode_a_silent_final_asc_band",
        "mode": "silent",
        "stage_target": "final",
        "viewport": "asc_band",
        "lat_cap": "on",
        "params": {"mode": "silent", "viewport": "asc"},
        "description": "Mode A, all four stages (seed→coarse→refine→converge). "
                       "Final raster after the convergence engine halts.",
    },
    # 2. Mode B — Pointillist Discovery: early / mid / final
    {
        "case_id": "mode_b_pointillist_early_asc_band",
        "mode": "pointillist",
        "stage_target": "stage_0",
        "viewport": "asc_band",
        "lat_cap": "on",
        "params": {"mode": "pointillist", "viewport": "asc", "stopAtStage": "0"},
        "description": "Mode B, early: leaf centers from the 240-sample seed pass only. "
                       "Dots are real leaf centers, not random particles.",
    },
    {
        "case_id": "mode_b_pointillist_mid_asc_band",
        "mode": "pointillist",
        "stage_target": "stage_1",
        "viewport": "asc_band",
        "lat_cap": "on",
        "params": {"mode": "pointillist", "viewport": "asc", "stopAtStage": "1"},
        "description": "Mode B, mid: leaf centers accumulated through stages 0+1 "
                       "(stage_1 max_samples=900). Stage 2 budget already converges "
                       "the engine at this viewport, so stage_1 is the meaningful "
                       "intermediate state.",
    },
    {
        "case_id": "mode_b_pointillist_final_asc_band",
        "mode": "pointillist",
        "stage_target": "final",
        "viewport": "asc_band",
        "lat_cap": "on",
        "params": {"mode": "pointillist", "viewport": "asc"},
        "description": "Mode B, final: all leaf centers; raster fades in only if "
                       "the engine reports converged=true.",
    },
    # 3. Mode C — Frontier Visualization, two viewports
    {
        "case_id": "mode_c_frontier_final_asc_band",
        "mode": "frontier",
        "stage_target": "final",
        "viewport": "asc_band",
        "lat_cap": "on",
        "params": {"mode": "frontier", "viewport": "asc"},
        "description": "Mode C at the Sun–ASC band. Dashed outlines = leaves that "
                       "the engine left non-settled OR bottomed out with debt > 0.",
    },
    {
        "case_id": "mode_c_frontier_final_greenland",
        "mode": "frontier",
        "stage_target": "final",
        "viewport": "greenland",
        "lat_cap": "on",
        "params": {"mode": "frontier", "viewport": "greenland"},
        "description": "Mode C at the high-lat Greenland viewport. With the 65° "
                       "cap on, most leaves should clip; frontier count should be ~0.",
    },
    # 4. Mode Off — final raster only
    {
        "case_id": "mode_off_final_asc_band",
        "mode": "off",
        "stage_target": "final",
        "viewport": "asc_band",
        "lat_cap": "on",
        "params": {"mode": "off", "viewport": "asc"},
        "description": "Off mode at Sun–ASC band. Single engine call at the "
                       "full sample budget; no staging visuals.",
    },
    # 5. Lat-cap A/B at Greenland, lat-cap on vs lat-cap off
    {
        "case_id": "latcap_capped_greenland",
        "mode": "silent",
        "stage_target": "final",
        "viewport": "greenland",
        "lat_cap": "on",
        "params": {"mode": "silent", "viewport": "greenland", "latCap": "1"},
        "description": "Lat-cap A/B: cap ON at Greenland. Leaves above ±65° "
                       "should be flagged outside_lat_cap; raster should be empty "
                       "across high-lat land.",
    },
    {
        "case_id": "latcap_uncapped_greenland",
        "mode": "silent",
        "stage_target": "final",
        "viewport": "greenland",
        "lat_cap": "off",
        "params": {"mode": "silent", "viewport": "greenland", "latCap": "0"},
        "description": "Lat-cap A/B: cap OFF at Greenland. Engine samples to the "
                       "viewport edge regardless of latitude — exposes whatever "
                       "the raw Sun–ASC field reports near the pole.",
    },
]


def build_url(case: dict[str, Any]) -> str:
    params = dict(case["params"])
    params.setdefault("profile", PROFILE_ID)
    params["auto"] = "1"
    from urllib.parse import urlencode
    return f"{SANDBOX_URL}?{urlencode(params)}"


def capture_case(page, case: dict[str, Any]) -> dict[str, Any]:
    url = build_url(case)
    print(f"\n=== {case['case_id']} ===")
    print(f"  url: {url}")
    page.goto(url, wait_until="domcontentloaded")
    # Wait until the sandbox finishes its full run loop. The sandbox sets
    # __sandboxStatus = "complete" only after every stage has been rendered
    # AND its result pushed to __sandboxStageResults.
    page.wait_for_function(
        "() => window.__sandboxStatus === 'complete' || window.__sandboxStatus === 'error'",
        timeout=90_000,
    )
    status = page.evaluate("() => window.__sandboxStatus")
    last_error = page.evaluate("() => window.__sandboxLastError")
    if status != "complete":
        raise RuntimeError(f"sandbox status={status}, error={last_error}")

    # Read all per-stage engine responses (real properties.*).
    stage_results: list[dict[str, Any]] = page.evaluate(
        "() => JSON.parse(JSON.stringify(window.__sandboxStageResults))"
    )
    if not stage_results:
        raise RuntimeError("no stage results captured")
    last = stage_results[-1]

    # Allow the very last paint transition to settle (CSS opacity transition
    # in the sandbox is 220ms; we wait 350ms to be safe).
    page.wait_for_timeout(350)

    # Screenshot the map area only (panel cropped out).
    map_box = page.evaluate(
        "() => { const el = document.getElementById('map'); "
        "const r = el.getBoundingClientRect(); "
        "return {x: r.x, y: r.y, width: r.width, height: r.height}; }"
    )
    image_path = OUT_DIR / f"{case['case_id']}.png"
    page.screenshot(path=str(image_path), clip=map_box)

    # Build the per-case metrics block straight from the engine response.
    props = last["properties"]
    cv = props.get("convergence_vs_reference") or {}
    record: dict[str, Any] = {
        "case_id": case["case_id"],
        "description": case["description"],
        "image": image_path.name,
        "url": url,
        "mode": case["mode"],
        "stage_target": case["stage_target"],
        "stage_id_observed": last["stage_id"],
        "viewport": case["viewport"],
        "viewport_bounds": last["bounds"],
        "lat_cap": case["lat_cap"],
        "apply_lat_cap_request": last["apply_lat_cap"],
        "truth_sample_count": props.get("truth_sample_count"),
        "leaf_count": last["leaf_count"],
        "frontier_count": last["frontier_count"],
        "residual_count": last["residual_count"],
        "passes_executed": props.get("passes_executed"),
        "max_delta_vs_reference": cv.get("max_delta_vs_reference"),
        "mean_delta_vs_reference": cv.get("mean_delta_vs_reference"),
        "pixels_above_threshold_pct": cv.get("pixels_above_threshold_pct"),
        "convergence_delta_threshold": cv.get("delta_threshold")
            or cv.get("convergence_delta_threshold"),
        "converged": props.get("converged"),
        "overshoot_detected": props.get("overshoot_detected"),
        "stop_reason": props.get("stop_reason"),
        "compute_seconds": props.get("compute_seconds"),
        "reference_compute_seconds": props.get("reference_compute_seconds"),
        "stage_count_run": len(stage_results),
    }
    print(f"  saved: {image_path.name}")
    print(f"  samples={record['truth_sample_count']} "
          f"leaves={record['leaf_count']} "
          f"frontier={record['frontier_count']} "
          f"residual={record['residual_count']} "
          f"maxΔ={record['max_delta_vs_reference']} "
          f"stop={record['stop_reason']}")
    return record


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed; install via `./venv/bin/pip install playwright`")
        return 2
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 800},
                                   device_scale_factor=2)
        page = ctx.new_page()
        page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
        page.on("console", lambda msg: None)
        for case in CASES:
            try:
                records.append(capture_case(page, case))
            except Exception as exc:
                print(f"  FAIL: {exc}")
                records.append({
                    "case_id": case["case_id"],
                    "image": None,
                    "error": str(exc),
                    "mode": case["mode"],
                    "stage_target": case["stage_target"],
                    "viewport": case["viewport"],
                    "lat_cap": case["lat_cap"],
                    "url": build_url(case),
                })
        browser.close()

    manifest = {
        "schema": "truth_field_sandbox_visual_qa@1",
        "sandbox_url": SANDBOX_URL,
        "output_dir": str(OUT_DIR.relative_to(REPO_ROOT)),
        "case_count": len(CASES),
        "pass_count": sum(1 for r in records if not r.get("error")),
        "fail_count": sum(1 for r in records if r.get("error")),
        "page_errors": errors,
        "captures": records,
    }
    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"\nmanifest: {manifest_path}")
    print(f"captures: {manifest['pass_count']}/{manifest['case_count']} ok, "
          f"{manifest['fail_count']} fail, "
          f"{len(errors)} page errors")
    return 0 if manifest["fail_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
