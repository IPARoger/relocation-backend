"""Phase 3.15 — Capture one static screenshot of the real Sun-in-1 polygon.

This script does NOT generate the polygon. It only loads the sandbox HTML
(which fetches the GeoJSON already produced by /search-regions) and saves a
single PNG. No animation control, no metrics, no state sampling.
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
URL = "http://127.0.0.1:8722/validation/sandboxes/phase3_15_real_single_polygon.html"
OUT = ROOT / "validation/screenshots/phase3_15_real_single_polygon/01_real_single_polygon.png"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle")
        page.wait_for_function(
            "() => document.getElementById('status') && "
            "document.getElementById('status').textContent.startsWith('Rendered')",
            timeout=15000,
        )
        page.wait_for_timeout(750)
        page.screenshot(path=str(OUT), full_page=False)
        status = page.evaluate("() => document.getElementById('status').textContent")
        print(f"status: {status}")
        print(f"saved:  {OUT}")
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
