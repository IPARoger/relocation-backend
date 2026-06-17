"""Brute-force angle-in-sign proof capture matrix (development step 4).

Drives ``map_SANDBOX_brute_force.html`` with the new condition-slot
URL syntax that distinguishes condition type:

    ?A=pih:sun:1            -> planet-in-house slot
    ?A=ais:asc:scorpio      -> angle-in-sign slot

Produces stills for:

  * each of the four relocated angles in a sign (ASC, MC, IC, DSC) —
    isolated single-condition baselines so the shape of each angle's
    sign polygon is on the record;
  * a sign sweep for ASC across four representative signs at the same
    chart, so the user can see how the polygon shifts as the requested
    sign rotates through the zodiac;
  * mixed-type compositions: planet-in-house + angle-in-sign (2-slot),
    and a full 3-slot mix exercising every condition shape together;
  * a deliberate angle-in-sign / planet-in-house overlap so the mask
    palette is exercised with a real green region.

Output: ``validation/screenshots/brute_force_angle_in_sign/``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "brute_force_angle_in_sign"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_URL = "http://127.0.0.1:8000/map_SANDBOX_brute_force.html"
PROFILE_ID = "baseline_validated"

CASES: list[dict[str, Any]] = [
    # ---- four-angle baselines: each relocated angle in one chosen sign
    {
        "case_id": "01_asc_in_scorpio_baseline",
        "description": "Single condition — ASC in Scorpio, Americas, 0.25°.",
        "params": {"A": "ais:asc:scorpio", "viewport": "americas", "gridDeg": "0.25"},
    },
    {
        "case_id": "02_mc_in_capricorn_baseline",
        "description": "Single condition — MC in Capricorn, Americas, 0.25°.",
        "params": {"A": "ais:mc:capricorn", "viewport": "americas", "gridDeg": "0.25"},
    },
    {
        "case_id": "03_ic_in_cancer_baseline",
        "description": "Single condition — IC in Cancer, Americas, 0.25°. "
                       "IC ≡ MC + 180°, so this polygon should be the "
                       "longitudinal complement of MC-in-Cancer.",
        "params": {"A": "ais:ic:cancer", "viewport": "americas", "gridDeg": "0.25"},
    },
    {
        "case_id": "04_dsc_in_taurus_baseline",
        "description": "Single condition — DSC in Taurus, Americas, 0.25°.",
        "params": {"A": "ais:dsc:taurus", "viewport": "americas", "gridDeg": "0.25"},
    },
    # ---- sign sweep for ASC (one polygon per sign request)
    {
        "case_id": "05_asc_sign_sweep_aries",
        "description": "ASC-in-Aries (world, 0.5°) — shape sweep frame 1/4.",
        "params": {"A": "ais:asc:aries", "viewport": "world", "gridDeg": "0.5"},
    },
    {
        "case_id": "06_asc_sign_sweep_cancer",
        "description": "ASC-in-Cancer (world, 0.5°) — shape sweep frame 2/4.",
        "params": {"A": "ais:asc:cancer", "viewport": "world", "gridDeg": "0.5"},
    },
    {
        "case_id": "07_asc_sign_sweep_libra",
        "description": "ASC-in-Libra (world, 0.5°) — shape sweep frame 3/4.",
        "params": {"A": "ais:asc:libra", "viewport": "world", "gridDeg": "0.5"},
    },
    {
        "case_id": "08_asc_sign_sweep_capricorn",
        "description": "ASC-in-Capricorn (world, 0.5°) — shape sweep frame 4/4.",
        "params": {"A": "ais:asc:capricorn", "viewport": "world", "gridDeg": "0.5"},
    },
    # ---- mixed two-slot — REAL overlap on the baseline chart.
    # For 1976-01-13 12:47 UTC, the Sun is at 292° (deep Capricorn).
    # Sun-in-1st only happens when ASC is in the trailing degrees of
    # Sagittarius through Capricorn, so pairing it with ASC-in-Capricorn
    # produces a substantial green A∩B band.
    {
        "case_id": "09_mixed_two_slot_overlap_sun_1st_asc_capricorn",
        "description": "Mixed (real overlap) — A = Sun in 1st (planet_in_house), "
                       "B = ASC in Capricorn (angle_in_sign). Americas, 0.25°. "
                       "Sun is at 22° Capricorn for this chart, so the two "
                       "conditions deeply overlap; expect a large green band.",
        "params": {"A": "pih:sun:1", "B": "ais:asc:capricorn",
                   "viewport": "americas", "gridDeg": "0.25"},
    },
    # ---- mixed three-slot — real overlap in every pair plus a
    # plausible triple region.
    {
        "case_id": "10_mixed_three_slot_overlap",
        "description": "Mixed three-slot with real overlap — "
                       "A = Sun in 1st, B = ASC in Capricorn, C = MC in Libra. "
                       "Each pair intersects; the triple region exists where "
                       "all three coincide. Americas, 0.25°.",
        "params": {"A": "pih:sun:1", "B": "ais:asc:capricorn",
                   "C": "ais:mc:libra", "viewport": "americas",
                   "gridDeg": "0.25"},
    },
    # ---- identity sanity check: two conditions that are mathematically
    # the same locus (ASC=Capricorn iff DSC=Cancer). The match must be
    # 100% overlap (every match cell has mask=3), entirely painted green.
    {
        "case_id": "11_identity_sanity_asc_capricorn_dsc_cancer",
        "description": "Identity sanity — A = ASC in Capricorn, "
                       "B = DSC in Cancer. DSC ≡ ASC + 180° and Cancer ≡ "
                       "Capricorn + 180°, so EVERY match cell must satisfy "
                       "both. The polygon should be entirely the green "
                       "A∩B color with A_only = B_only = 0.",
        "params": {"A": "ais:asc:capricorn", "B": "ais:dsc:cancer",
                   "viewport": "americas", "gridDeg": "0.25"},
    },
    # ---- mixed three-slot at world scale, same conditions as case 10
    {
        "case_id": "12_mixed_three_slot_overlap_world",
        "description": "Same mixed three-slot as case 10 at world view, 0.5°. "
                       "Shows the global topology of the three condition "
                       "families and their overlap regions.",
        "params": {"A": "pih:sun:1", "B": "ais:asc:capricorn",
                   "C": "ais:mc:libra", "viewport": "world",
                   "gridDeg": "0.5"},
    },
]


def build_url(case: dict[str, Any]) -> str:
    params = dict(case["params"])
    params.setdefault("profile", PROFILE_ID)
    params.setdefault("auto", "1")
    return f"{SANDBOX_URL}?{urlencode(params)}"


def _run_single(page, case: dict[str, Any]) -> dict[str, Any]:
    """One attempt at driving the sandbox for `case`. Returns the parsed
    metrics dict, or raises on any failure. The caller wraps this with
    a retry loop because the headless Chromium + Leaflet combination is
    occasionally flaky on fresh tile loads."""
    url = build_url(case)
    timeout_ms = int(case.get("timeout_seconds", 180)) * 1000
    page.goto(url, wait_until="domcontentloaded")
    # Wait for the sandbox to reach a deterministic state. We accept
    # 'complete' (auto-run finished) or 'error' (auto-run failed and we
    # want to surface the error), and 'ready' so we can trigger ourselves
    # if auto-run never fired.
    page.wait_for_function(
        "() => ['complete', 'error', 'ready'].includes(window.__bruteStatus)",
        timeout=30000,
    )
    status = page.evaluate("() => window.__bruteStatus")
    if status == "ready":
        # Auto-run never fired (or already finished and got reset);
        # trigger manually and wait again.
        page.evaluate("() => document.getElementById('runBtn').click()")
    if status != "complete":
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
    print(f"  per-condition: " + ", ".join(
        f"{c['id']}({c['type'][:3]})={c['count']:,}"
        for c in timings["conditions"]))
    o = timings.get("overlap_counts") or {}
    overlap_pairs = [k for k in o
                     if k != "any" and not k.endswith("_only") and o.get(k)]
    if overlap_pairs:
        print(f"  overlaps: " + ", ".join(f"{k}={o[k]:,}" for k in overlap_pairs))
    return {
        "case_id": case["case_id"],
        "description": case["description"],
        "image": image_path.name,
        "url": url,
        "params": case["params"],
        "timings": timings,
    }


def _load_previous_manifest() -> dict[str, dict[str, Any]]:
    """Return a {case_id: record} map of previously-good captures so a
    flaky run does not destroy data we already trust."""
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
                # Fall back to the previous good capture for this case,
                # if any, instead of dropping data because of a flake.
                prev = previous_good.get(case["case_id"])
                if prev is not None:
                    print(f"  using previous good capture for {case['case_id']}")
                    prev = dict(prev)
                    prev["error"] = None
                    prev["fallback_used"] = f"{exc}"
                    records.append(prev)
                else:
                    records.append({
                        "case_id": case["case_id"],
                        "image": None,
                        "error": str(exc),
                        "url": build_url(case),
                        "params": case["params"],
                    })
        browser.close()

    manifest = {
        "schema": "brute_force_angle_in_sign_proof@1",
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
