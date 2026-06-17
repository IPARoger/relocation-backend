"""Truth-target evidence bundle for the polygon-reveal sandbox.

Produces three sets of stills under
``validation/screenshots/polygon_reveal_topology/``:

  A. Final fully-densified topology, three targets:
        final_sun_1st_dense.png
        final_moon_4th_dense.png
        final_mars_2nd_dense.png

  B. Phase frame exports for Sun-in-1st only (six PNGs, one per phase):
        phase_00_initial_sparse.png
        phase_01_broad_cluster.png
        phase_02_regional_focus.png
        phase_03_boundary_hunt.png
        phase_04_dense_fill.png
        phase_05_final_topology.png

  C. Density experiments at Sun-in-1st (constant tiny probes; only the
     probe COUNT changes between renders, never the radius):
        density_sparse_micro.png
        density_medium_micro.png
        density_extreme_micro.png

All stills are captured at the Americas viewport so the polygon fills the
frame at a useful scale. Every dot drawn is a real ``/classify-points``
classification. The probe radius is constant for the lifetime of each
probe — refinement contributes more probes, not bigger probes.

Usage:
    PLAYWRIGHT_BROWSERS_PATH=./venv/lib/python3.11/site-packages/playwright/driver/package/.local-browsers \\
        ./venv/bin/python3 scripts/capture_polygon_topology_targets.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "polygon_reveal_topology"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_URL = "http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html"
PROFILE_ID = "baseline_validated"
SEED = 42


# ---------------------------------------------------------------------------
# A. Final topology — three targets at dense pacing
# ---------------------------------------------------------------------------
FINAL_TARGETS = [
    {
        "case_id": "final_sun_1st_dense",
        "description": "Sun in 1st house, dense pacing, all 6 phases, Americas viewport. "
                       "Constant 1.1px probes; topology emerges from probe density only.",
        "params": {"pacing": "dense", "viewport": "americas",
                   "planet": "sun", "house": "1"},
    },
    {
        "case_id": "final_moon_4th_dense",
        "description": "Moon in 4th house, dense pacing, all 6 phases, Americas viewport. "
                       "Reference for a second target's topology under the same chart.",
        "params": {"pacing": "dense", "viewport": "americas",
                   "planet": "moon", "house": "4"},
    },
    {
        "case_id": "final_mars_2nd_dense",
        "description": "Mars in 2nd house, dense pacing, all 6 phases, Americas viewport. "
                       "Third target for visual topology comparison.",
        "params": {"pacing": "dense", "viewport": "americas",
                   "planet": "mars", "house": "2"},
    },
]


# ---------------------------------------------------------------------------
# B. Phase frame exports for Sun-in-1st (dense pacing)
# ---------------------------------------------------------------------------
PHASE_LABEL_BY_INDEX = {
    0: "phase_00_initial_sparse",
    1: "phase_01_broad_cluster",
    2: "phase_02_regional_focus",
    3: "phase_03_boundary_hunt",
    4: "phase_04_dense_fill",
    5: "phase_05_final_topology",
}
PHASE_FRAMES = [
    {
        "case_id": PHASE_LABEL_BY_INDEX[i],
        "description": f"Sun in 1st, dense pacing, captured immediately after "
                       f"{PHASE_LABEL_BY_INDEX[i]} (phase index {i}).",
        "params": {"pacing": "dense", "viewport": "americas",
                   "planet": "sun", "house": "1",
                   "stopAtPhase": str(i)},
    }
    for i in range(6)
]


# ---------------------------------------------------------------------------
# C. Density experiments at Sun-in-1st
# ---------------------------------------------------------------------------
# Same topology, only probe COUNT changes. probeRadius=1.0 kept constant for
# the eye to compare occupancy honestly.
DENSITY_VARIANTS = [
    {
        "case_id": "density_sparse_micro",
        "description": "Same topology, sparse micro density: bloom pacing × 0.6 density mult, "
                       "constant 1.0px probes. Target: see whether sparse occupancy can "
                       "communicate the polygon at all.",
        "params": {"pacing": "bloom", "viewport": "americas",
                   "planet": "sun", "house": "1",
                   "probeRadius": "1.0", "densityMult": "0.6"},
    },
    {
        "case_id": "density_medium_micro",
        "description": "Same topology, medium micro density: dense pacing × 1.0 density mult, "
                       "constant 1.0px probes. Target: 'reads as geography' threshold.",
        "params": {"pacing": "dense", "viewport": "americas",
                   "planet": "sun", "house": "1",
                   "probeRadius": "1.0", "densityMult": "1.0"},
    },
    {
        "case_id": "density_extreme_micro",
        "description": "Same topology, extreme micro density: micro pacing × 1.5 density mult, "
                       "constant 0.85px probes. Stresses the SVG renderer; expect "
                       "noticeable load time. Target: 'pixel-indistinguishable' threshold.",
        "params": {"pacing": "micro", "viewport": "americas",
                   "planet": "sun", "house": "1",
                   "probeRadius": "0.85", "densityMult": "1.5"},
    },
]


ALL_CASES: list[dict[str, Any]] = FINAL_TARGETS + PHASE_FRAMES + DENSITY_VARIANTS


def build_url(case: dict[str, Any]) -> str:
    params = dict(case["params"])
    params.setdefault("profile", PROFILE_ID)
    params.setdefault("seed", str(SEED))
    params["auto"] = "1"
    return f"{SANDBOX_URL}?{urlencode(params)}"


def capture_case(page, case: dict[str, Any]) -> dict[str, Any]:
    url = build_url(case)
    print(f"\n=== {case['case_id']} ===")
    print(f"  url: {url}")
    page.goto(url, wait_until="domcontentloaded")
    # Extend the wait for the micro-density extreme case (lots of SVG nodes).
    timeout_ms = 180_000 if "micro" in case["params"].get("pacing", "") else 90_000
    page.wait_for_function(
        "() => window.__sandboxStatus === 'complete' || window.__sandboxStatus === 'error'",
        timeout=timeout_ms,
    )
    status = page.evaluate("() => window.__sandboxStatus")
    last_error = page.evaluate("() => window.__sandboxLastError")
    if status != "complete":
        raise RuntimeError(f"sandbox status={status}, error={last_error}")

    snapshots = page.evaluate(
        "() => JSON.parse(JSON.stringify(window.__sandboxSnapshots))"
    )
    classify_calls = page.evaluate("() => window.__classifyCallCount || 0")
    if not snapshots:
        raise RuntimeError("no snapshots captured")
    last_snap = snapshots[-1]

    page.wait_for_timeout(900)  # let final CSS opacity transitions settle

    map_box = page.evaluate(
        "() => { const el = document.getElementById('map'); "
        "const r = el.getBoundingClientRect(); "
        "return {x: r.x, y: r.y, width: r.width, height: r.height}; }"
    )
    image_path = OUT_DIR / f"{case['case_id']}.png"
    page.screenshot(path=str(image_path), clip=map_box)

    phases = [
        {
            "phase_id": s["phase_id"],
            "phase_idx": s["phase_idx"],
            "probe_count": s["probe_count"],
            "matches": s["matches"],
            "non_matches": s["non_matches"],
            "capped": s["capped"],
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
        "target_planet": last_snap["planet"],
        "target_house": last_snap["house"],
        "phases": phases,
    }
    print(f"  saved: {image_path.name}")
    print(f"  probes={record['final_probe_count']}  "
          f"match={record['final_match_count']}  "
          f"calls={record['classify_endpoint_calls']}  "
          f"target={record['target_planet']}-{record['target_house']}")
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
        # Wider viewport so the Americas band fills usefully.
        ctx = browser.new_context(viewport={"width": 1480, "height": 900},
                                   device_scale_factor=2)
        page = ctx.new_page()
        page.on("pageerror", lambda exc: page_errors.append(f"pageerror: {exc}"))
        for case in ALL_CASES:
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
        "schema": "polygon_reveal_topology_v1@1",
        "sandbox_url": SANDBOX_URL,
        "profile_id": PROFILE_ID,
        "seed": SEED,
        "output_dir": str(OUT_DIR.relative_to(REPO_ROOT)),
        "case_count": len(ALL_CASES),
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
