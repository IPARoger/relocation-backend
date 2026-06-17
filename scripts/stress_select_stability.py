#!/usr/bin/env python3
"""
Playwright stress test: open/close native selects repeatedly and verify value stability.

Targets intermittent profile-select auto-advance / focus-highlight desync (Mac trackpad).
Not wheel-scroll — uses click-to-focus only.

Requires:
  - uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000
  - playwright install chromium

Usage:
  ./venv/bin/python3 scripts/stress_select_stability.py
  ./venv/bin/python3 scripts/stress_select_stability.py --cycles 150 --select chartProfile
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
REPORT_DIR = Path(__file__).resolve().parent.parent / "validation" / "reports"
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BROWSER_PATH = ROOT / ".playwright-browsers"

if DEFAULT_BROWSER_PATH.exists():
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(DEFAULT_BROWSER_PATH)

SELECTORS = {
    "chartProfile": "#chartProfile",
    "planetA": "#planetA",
    "houseA": "#houseA",
    "angleSignAngle": "#angleSignAngle",
    "angleSignSign": "#angleSignSign",
    "overlayAspect": "#overlayAspect",
}


def server_ok() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE}/health", timeout=5) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def stress_select(page, selector: str, cycles: int) -> dict:
    page.select_option(selector, page.evaluate(f"() => document.querySelector({json.dumps(selector)}).options[0].value"))
    expected = page.evaluate(f"() => document.querySelector({json.dumps(selector)}).value")
    mismatches: list[dict] = []

    for i in range(cycles):
        page.locator(selector).click()
        page.wait_for_timeout(30)
        current = page.evaluate(f"() => document.querySelector({json.dumps(selector)}).value")
        if current != expected:
            mismatches.append({"cycle": i + 1, "expected": expected, "actual": current})
            expected = current
        page.keyboard.press("Escape")
        page.wait_for_timeout(20)

    return {
        "selector": selector,
        "cycles": cycles,
        "final_value": page.evaluate(f"() => document.querySelector({json.dumps(selector)}).value"),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:10],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycles", type=int, default=120)
    parser.add_argument(
        "--select",
        dest="selects",
        action="append",
        default=["chartProfile"],
        choices=list(SELECTORS.keys()),
        help="Select id to stress (repeat flag for multiple)",
    )
    args = parser.parse_args()

    if not server_ok():
        print(json.dumps({"overall_pass": False, "error": f"Server not reachable at {BASE}/health"}))
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(json.dumps({"overall_pass": False, "error": "playwright not installed"}))
        return 1

    bust = int(time.time())
    url = f"{BASE}/map_CURRENT.html?bust={bust}&skipOnboarding=1"
    results: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_function(
            "() => document.getElementById('chartProfile')?.options?.length >= 3",
            timeout=15000,
        )

        for name in args.selects:
            sel = SELECTORS[name]
            if name == "chartProfile":
                page.select_option(sel, "edge_high_north")
            results.append(stress_select(page, sel, args.cycles))

        browser.close()

    overall_pass = all(r["mismatch_count"] == 0 for r in results)
    report = {
        "description": "Native select open/close stability stress test",
        "url": url,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cycles_per_select": args.cycles,
        "overall_pass": overall_pass,
        "results": results,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "select_stability_stress.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall_pass": overall_pass, "report": str(report_path)}, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
