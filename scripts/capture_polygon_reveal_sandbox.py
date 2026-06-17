"""Visual QA capture harness for ``map_SANDBOX_polygon_reveal.html``.

Drives the polygon-reveal sandbox through a deterministic matrix of
(pacing, viewport, target, lat-cap, stop-phase) cases via Playwright.

For every case, the script:

* loads the sandbox with explicit URL params (no rendering changes),
* waits for ``window.__sandboxStatus === "complete"``,
* captures a PNG of the map pane only (control panel cropped out),
* reads engine state directly out of ``window.__sandboxSnapshots`` —
  i.e. every probe's real classification, never a perceptual claim,
* writes per-case metrics + a consolidated ``manifest.json`` to
  ``validation/screenshots/polygon_reveal_sandbox/``.

The harness asserts only what the sandbox + ``/classify-points`` actually
reported. It is silent on whether anything "looks magical".

Usage:
    ./venv/bin/python3 scripts/capture_polygon_reveal_sandbox.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "polygon_reveal_sandbox"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_URL = "http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html"
PROFILE_ID = "baseline_validated"
SEED = 42

# Cases. Each row exercises one rendering question. Params drive existing
# sandbox URL hooks only.
CASES: list[dict[str, Any]] = [
    # 1-4. Pacing variants at the world viewport — same chart, same target,
    # same seed. Compare how the polygon emerges across tempos.
    {
        "case_id": "calm_final_world",
        "description": "Calm scatter pacing, final state at world viewport. 60 "
                       "initial probes + 4 refinement passes; longest dwell.",
        "params": {"pacing": "calm", "viewport": "world"},
    },
    {
        "case_id": "bloom_final_world",
        "description": "Cosmic bloom pacing, final state at world viewport. 140 "
                       "initial probes + 3 refinement passes; medium tempo.",
        "params": {"pacing": "bloom", "viewport": "world"},
    },
    {
        "case_id": "eager_final_world",
        "description": "Eager reveal pacing, final state at world viewport. 280 "
                       "initial probes + 3 refinement passes; fast tempo.",
        "params": {"pacing": "eager", "viewport": "world"},
    },
    {
        "case_id": "instant_final_world",
        "description": "Instant baseline: single 600-probe classify call, no "
                       "staging. The emotionally-sterile reference.",
        "params": {"pacing": "instant", "viewport": "world"},
    },
    # 5-6. Continental zoom comparisons — same pacing, two viewports.
    {
        "case_id": "bloom_final_americas",
        "description": "Cosmic bloom at Americas viewport; band-zoom view of "
                       "the Sun-in-1st polygon center.",
        "params": {"pacing": "bloom", "viewport": "americas"},
    },
    {
        "case_id": "eager_final_eurasia",
        "description": "Eager reveal at Eurasia viewport. Sun-in-1st should be "
                       "largely absent here; non-match probes dominate.",
        "params": {"pacing": "eager", "viewport": "eurasia"},
    },
    # 7-8. Phase progression for the calm variant (stage stills).
    {
        "case_id": "calm_phase0_scatter_world",
        "description": "Calm pacing halted after initial scatter (60 probes). "
                       "No boundary refinement yet — the random probe field.",
        "params": {"pacing": "calm", "viewport": "world", "stopAtPhase": "0"},
    },
    {
        "case_id": "calm_phase2_refine_world",
        "description": "Calm pacing halted after refine pass 2/4. Boundary "
                       "densification visible but polygon edge not yet sharp.",
        "params": {"pacing": "calm", "viewport": "world", "stopAtPhase": "2"},
    },
    # 9. Cache demo: complete calm run, then swap target Sun-in-1st → Moon-in-4th
    # using the cached per-point houses (zero new engine calls).
    {
        "case_id": "calm_cache_swap_to_moon4_world",
        "description": "Calm pacing world reveal completed, then target swapped "
                       "from Sun-in-1st to Moon-in-4th. New colors come purely "
                       "from the all-planets cache; classify_calls should not "
                       "increase.",
        "params": {"pacing": "calm", "viewport": "world", "swapTo": "moon:4"},
    },
    # 10. High-latitude honesty — same viewport, lat-cap on vs off.
    {
        "case_id": "latcap_off_world",
        "description": "Eager pacing, world view, latCap=0. Probes above ±65° "
                       "are classified rather than declared outside_lat_cap.",
        "params": {"pacing": "eager", "viewport": "world", "latCap": "0"},
    },
]


def build_url(case: dict[str, Any]) -> str:
    from urllib.parse import urlencode
    params = dict(case["params"])
    params.setdefault("planet", "sun")
    params.setdefault("house", "1")
    params.setdefault("profile", PROFILE_ID)
    params.setdefault("seed", str(SEED))
    params["auto"] = "1"
    return f"{SANDBOX_URL}?{urlencode(params)}"


def capture_case(page, case: dict[str, Any]) -> dict[str, Any]:
    url = build_url(case)
    print(f"\n=== {case['case_id']} ===")
    print(f"  url: {url}")
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_function(
        "() => window.__sandboxStatus === 'complete' || window.__sandboxStatus === 'error'",
        timeout=90_000,
    )
    status = page.evaluate("() => window.__sandboxStatus")
    last_error = page.evaluate("() => window.__sandboxLastError")
    if status != "complete":
        raise RuntimeError(f"sandbox status={status}, error={last_error}")

    snapshots: list[dict[str, Any]] = page.evaluate(
        "() => JSON.parse(JSON.stringify(window.__sandboxSnapshots))"
    )
    classify_calls: int = page.evaluate("() => window.__classifyCallCount || 0")
    if not snapshots:
        raise RuntimeError("no snapshots captured")
    last_snap = snapshots[-1]

    # Settle any final per-probe fade-in transitions before screenshot
    # (CSS transition durations are 600-700 ms; wait 800 ms to be safe).
    page.wait_for_timeout(800)

    map_box = page.evaluate(
        "() => { const el = document.getElementById('map'); "
        "const r = el.getBoundingClientRect(); "
        "return {x: r.x, y: r.y, width: r.width, height: r.height}; }"
    )
    image_path = OUT_DIR / f"{case['case_id']}.png"
    page.screenshot(path=str(image_path), clip=map_box)

    # Reduce snapshots into a per-phase metrics array (omit per-probe arrays
    # from the manifest to keep it small; per-probe arrays are still in
    # window.__sandboxSnapshots if needed).
    phases = [
        {
            "phase_id": s["phase_id"],
            "phase_idx": s["phase_idx"],
            "probe_count": s["probe_count"],
            "matches": s["matches"],
            "non_matches": s["non_matches"],
            "capped": s["capped"],
            "errors": s["errors"],
        }
        for s in snapshots
    ]
    record: dict[str, Any] = {
        "case_id": case["case_id"],
        "description": case["description"],
        "image": image_path.name,
        "url": url,
        "params": case["params"],
        "classify_endpoint_calls": classify_calls,
        "final_probe_count": last_snap["probe_count"],
        "final_match_count": last_snap["matches"],
        "final_non_match_count": last_snap["non_matches"],
        "final_capped_count": last_snap["capped"],
        "final_error_count": last_snap["errors"],
        "target_planet_final": last_snap["planet"],
        "target_house_final": last_snap["house"],
        "phases": phases,
    }
    print(f"  saved: {image_path.name}")
    print(f"  probes={record['final_probe_count']} "
          f"match={record['final_match_count']} "
          f"non={record['final_non_match_count']} "
          f"capped={record['final_capped_count']} "
          f"calls={record['classify_endpoint_calls']} "
          f"target={record['target_planet_final']}-{record['target_house_final']}")
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
        "schema": "polygon_reveal_sandbox_visual_qa@1",
        "sandbox_url": SANDBOX_URL,
        "profile_id": PROFILE_ID,
        "seed": SEED,
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
          f"{manifest['fail_count']} fail, "
          f"{len(page_errors)} page errors")
    return 0 if manifest["fail_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
