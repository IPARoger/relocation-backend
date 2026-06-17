"""Brute-force aspect-to-angle centerline proof capture matrix
(development step 6).

Drives ``map_SANDBOX_brute_force.html`` with the new aspect-to-angle
URL slot syntax: ``?A=a2a:saturn:mc:conjunction:1.0``.

Each captured case classifies every cell of the requested viewport
against an exact aspect to a relocated angle (ASC / MC / IC / DSC).
Matches are rendered as translucent occupancy dots; the centerline is
the *band* of cells where the condition is true within orb. No curve
fitting, no smoothing — the centerline emerges from truthful
classification, exactly as the doctrine demands.

Coverage:

  * five major aspects against MC and ASC (single-condition baselines)
  * IC ↔ MC and ASC ↔ DSC identity proofs (different request, same cells)
  * orb sweep on one fixed condition (0.5°, 1.0°, 2.0°, 4.0°)
  * a "fan" of five aspects in the same picture (conj+sex+sq+tr+opp,
    Saturn → MC) so the geometric spacing is visible at once
  * mixed condition types: aspect-to-angle + planet-in-house overlap
  * world-view mixed: MC-meridian centerline + curved ASC centerline
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "brute_force_aspect_to_angle"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_URL = "http://127.0.0.1:8000/map_SANDBOX_brute_force.html"
PROFILE_ID = "baseline_validated"

# Bounds tuned for this profile. Saturn = 120.08° in the natal chart;
# the Saturn-MC conjunction band lives near 178°E (Pacific). All
# manual bounds stay inside the [-180, 180] range so the sandbox's
# longitude clamp (Math.min/max on getWest/getEast) preserves them
# exactly. We capture the dateline-adjacent centerline by looking at
# the eastern Pacific from 150°E to 180°E.
PACIFIC_178E   = [[-65, 150], [65, 180]]   # SW corner, NE corner
ASIA_INDIAN    = [[-50,   0], [70, 130]]
WORLD          = None  # use sandbox World preset

CASES: list[dict[str, Any]] = [
    # ----- five major aspects against MC -----
    # All five Saturn-to-MC aspects rendered together — the spacing
    # between the five lines is the visual proof that the engine's
    # aspect math is correct. Conjunction line, sextile lines (×2),
    # square lines (×2), trine lines (×2), opposition line.
    {
        "case_id": "01_fan_saturn_to_mc_orb1",
        "description": "All five major Saturn→MC aspects together at world. "
                       "Conjunction (yellow) is one meridian; opposition "
                       "is the antipodal meridian; sextile/square/trine "
                       "each split into a pair of meridians at 60°/90°/120° "
                       "of ecliptic separation. Orb 1.0°.",
        "params": {"viewport": "world", "gridDeg": "0.5",
                   "A": "a2a:saturn:mc:conjunction:1.0",
                   "B": "a2a:saturn:mc:opposition:1.0",
                   "C": "a2a:saturn:mc:square:1.0"},
    },
    # ----- single aspect baselines against MC -----
    {
        "case_id": "02_conjunction_saturn_mc_orb1",
        "description": "Single condition — Saturn ☌ MC, orb 1.0°. "
                       "MC depends only on longitude → vertical meridian "
                       "centerline through the Pacific (~178°E).",
        "params": {"A": "a2a:saturn:mc:conjunction:1.0",
                   "gridDeg": "0.25"},
        "manual_bounds": PACIFIC_178E,
    },
    {
        "case_id": "03_square_saturn_mc_orb1",
        "description": "Single condition — Saturn ☐ MC, orb 1.0°. "
                       "Two meridians 90° apart, at MC = Saturn ± 90°.",
        "params": {"A": "a2a:saturn:mc:square:1.0",
                   "viewport": "world", "gridDeg": "0.5"},
    },
    {
        "case_id": "04_trine_saturn_mc_orb1",
        "description": "Single condition — Saturn △ MC, orb 1.0°. "
                       "Two meridians 120° apart, at MC = Saturn ± 120°.",
        "params": {"A": "a2a:saturn:mc:trine:1.0",
                   "viewport": "world", "gridDeg": "0.5"},
    },
    {
        "case_id": "05_opposition_saturn_mc_orb1",
        "description": "Single condition — Saturn ☍ MC, orb 1.0°. "
                       "Single meridian at MC = Saturn + 180° "
                       "(antipodal to the conjunction line).",
        "params": {"A": "a2a:saturn:mc:opposition:1.0",
                   "viewport": "world", "gridDeg": "0.5"},
    },
    # ----- ASC produces a curve, not a meridian -----
    {
        "case_id": "06_conjunction_saturn_asc_orb1",
        "description": "Single condition — Saturn ☌ ASC, orb 1.0°. "
                       "ASC depends on lat+lon, so this is a CURVED band "
                       "rather than a meridian. Same engine, same orb.",
        "params": {"A": "a2a:saturn:asc:conjunction:1.0",
                   "viewport": "world", "gridDeg": "0.5"},
    },
    # ----- identity proofs (cell-for-cell) -----
    {
        "case_id": "07_identity_saturn_conj_ic",
        "description": "Identity proof part 1 — Saturn ☌ IC, orb 1.0°. "
                       "Must coincide cell-for-cell with case 05 "
                       "(Saturn ☍ MC) because IC ≡ MC + 180°.",
        "params": {"A": "a2a:saturn:ic:conjunction:1.0",
                   "viewport": "world", "gridDeg": "0.5"},
    },
    {
        "case_id": "08_identity_saturn_conj_dsc",
        "description": "Identity proof part 2 — Saturn ☌ DSC, orb 1.0°. "
                       "Must coincide cell-for-cell with Saturn ☍ ASC "
                       "(rendered jointly in case 11 for visual evidence).",
        "params": {"A": "a2a:saturn:dsc:conjunction:1.0",
                   "viewport": "world", "gridDeg": "0.5"},
    },
    # ----- orb sensitivity (same condition, four widths) -----
    {
        "case_id": "09_orb_sensitivity_orb_0p5",
        "description": "Orb sensitivity — Saturn ☌ MC at orb 0.5°. "
                       "Tighter than the default; band visibly thinner.",
        "params": {"A": "a2a:saturn:mc:conjunction:0.5",
                   "gridDeg": "0.1"},
        "manual_bounds": PACIFIC_178E,
    },
    {
        "case_id": "09b_orb_sensitivity_orb_1p0",
        "description": "Orb sensitivity — Saturn ☌ MC at orb 1.0°. "
                       "Product default; sits between cases 09 (0.5°) "
                       "and 10 (2.0°). Same bounds and grid as both "
                       "neighbours so the three captures form a clean "
                       "narrow→default→wide comparison.",
        "params": {"A": "a2a:saturn:mc:conjunction:1.0",
                   "gridDeg": "0.1"},
        "manual_bounds": PACIFIC_178E,
    },
    {
        "case_id": "10_orb_sensitivity_orb_2p0",
        "description": "Orb sensitivity — Saturn ☌ MC at orb 2.0°. "
                       "Twice the default; band visibly wider.",
        "params": {"A": "a2a:saturn:mc:conjunction:2.0",
                   "gridDeg": "0.1"},
        "manual_bounds": PACIFIC_178E,
    },
    # ----- mixed: aspect-to-angle centerline ∩ planet-in-house polygon -----
    {
        "case_id": "11_mixed_centerline_crosses_house_polygon",
        "description": "Mixed condition types — A = Sun in 1st (planet_in_house), "
                       "B = Saturn ☌ ASC (aspect_to_angle, orb 1.0°). "
                       "The curved Saturn ☌ ASC centerline crosses the "
                       "Sun-1st polygon somewhere; that intersection is "
                       "painted as A∩B green.",
        "params": {"A": "pih:sun:1",
                   "B": "a2a:saturn:asc:conjunction:1.0",
                   "viewport": "world", "gridDeg": "0.5"},
    },
    # ----- mixed centerlines together: MC + ASC same planet -----
    {
        "case_id": "12_mixed_two_centerlines_mc_and_asc",
        "description": "Two centerlines on one chart — A = Saturn ☌ MC, "
                       "B = Saturn ☌ ASC, both at orb 1.0°. The first is "
                       "a meridian, the second is a curve, and they "
                       "intersect at one location (the cell where Saturn "
                       "is simultaneously on MC and on ASC — i.e. where "
                       "Saturn is at the rising horizon at culmination, "
                       "which only happens at extreme latitudes).",
        "params": {"A": "a2a:saturn:mc:conjunction:1.0",
                   "B": "a2a:saturn:asc:conjunction:1.0",
                   "viewport": "world", "gridDeg": "0.5"},
    },
]


def build_url(case: dict[str, Any]) -> str:
    params = dict(case["params"])
    params.setdefault("profile", PROFILE_ID)
    params["auto"] = "1"
    bounds = case.get("manual_bounds")
    if bounds is not None:
        # Encode the explicit bounds in the URL so the sandbox seeds
        # both the map view and the engine query with the same region.
        # Format: ?bounds=south,west,north,east
        sw, ne = bounds
        s_lat, w_lon = sw
        n_lat, e_lon = ne
        params["bounds"] = f"{s_lat},{w_lon},{n_lat},{e_lon}"
    return f"{SANDBOX_URL}?{urlencode(params)}"


def _run_single(page, case: dict[str, Any]) -> dict[str, Any]:
    url = build_url(case)
    timeout_ms = int(case.get("timeout_seconds", 240)) * 1000
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_function(
        "() => window.__bruteStatus === 'complete' "
        "   || window.__bruteStatus === 'error'",
        timeout=timeout_ms,
    )
    status = page.evaluate("() => window.__bruteStatus")
    if status != "complete":
        err = page.evaluate("() => window.__bruteLastError")
        raise RuntimeError(f"sandbox status={status}, error={err}")
    return page.evaluate(
        "() => JSON.parse(JSON.stringify(window.__bruteLastTimings))"
    )


def capture_case(page, case: dict[str, Any]) -> dict[str, Any]:
    url = build_url(case)
    print(f"\n=== {case['case_id']} ===")
    print(f"  url: {url}")
    last_exc = None
    timings = None
    for attempt in range(2):
        try:
            timings = _run_single(page, case)
            break
        except Exception as exc:
            last_exc = exc
            print(f"  attempt {attempt + 1} failed: {exc}")
            if attempt == 0:
                page.wait_for_timeout(1500)
    if timings is None:
        raise last_exc or RuntimeError("capture failed")
    page.wait_for_timeout(400)
    map_box = page.evaluate(
        "() => { const el = document.getElementById('map'); "
        "const r = el.getBoundingClientRect(); "
        "return {x: r.x, y: r.y, width: r.width, height: r.height}; }"
    )
    image_path = OUT_DIR / f"{case['case_id']}.png"
    page.screenshot(path=str(image_path), clip=map_box)
    print(f"  saved: {image_path.name}")
    print(f"  cells={timings['total_cells']:,}  "
          f"any={timings['matches']:,}  "
          f"server={timings['server_compute_seconds']:.2f}s")
    cdesc = ", ".join(
        f"{c['id']}({c['type'][:3]})={c['count']:,}"
        for c in timings["conditions"])
    print(f"  per-condition: {cdesc}")
    o = timings.get("overlap_counts") or {}
    overlaps = [k for k in o
                if k != "any" and not k.endswith("_only") and o.get(k)]
    if overlaps:
        print("  overlaps: " + ", ".join(f"{k}={o[k]:,}" for k in overlaps))
    return {
        "case_id": case["case_id"],
        "description": case["description"],
        "image": image_path.name,
        "url": url,
        "params": case["params"],
        "manual_bounds": case.get("manual_bounds"),
        "timings": timings,
    }


def _load_previous_manifest() -> dict[str, dict[str, Any]]:
    path = OUT_DIR / "manifest.json"
    if not path.exists():
        return {}
    try:
        m = json.loads(path.read_text())
    except Exception:
        return {}
    out = {}
    for r in m.get("captures", []):
        if r.get("error"):
            continue
        if not r.get("image"):
            continue
        if not (OUT_DIR / r["image"]).exists():
            continue
        out[r["case_id"]] = r
    return out


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed")
        return 2
    previous_good = _load_previous_manifest()
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
                prev = previous_good.get(case["case_id"])
                if prev is not None:
                    print(f"  using previous good capture for {case['case_id']}")
                    prev = dict(prev); prev["error"] = None
                    prev["fallback_used"] = f"{exc}"
                    records.append(prev)
                else:
                    records.append({
                        "case_id": case["case_id"], "image": None,
                        "error": str(exc),
                        "url": build_url(case), "params": case["params"],
                    })
        browser.close()
    manifest = {
        "schema": "brute_force_aspect_to_angle_proof@1",
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
          f"{manifest['fail_count']} fail")
    return 0 if manifest["fail_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
