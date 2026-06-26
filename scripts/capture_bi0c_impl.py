#!/usr/bin/env python3
"""Capture BI-0C before/after screenshots for auth + birth intake."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "validation/mockups/beta/screenshots/bi0c_implementation/after"
PORT = 8012
BASE = f"http://127.0.0.1:{PORT}"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.8)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("WARN: playwright not installed — skipping after screenshots")
        server.terminate()
        return 0

    captured = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # Auth signup (default view after init)
        page.goto(f"{BASE}/auth.html", wait_until="networkidle")
        page.evaluate("""() => {
          document.getElementById('page').classList.remove('loading');
          document.querySelectorAll('[data-view]').forEach(v => v.classList.remove('active'));
          document.getElementById('view-signup').classList.add('active');
        }""")
        page.screenshot(path=str(OUT / "01_auth_signup.png"))
        captured.append("01_auth_signup.png")

        page.evaluate("""() => {
          document.querySelectorAll('[data-view]').forEach(v => v.classList.remove('active'));
          document.getElementById('view-login').classList.add('active');
        }""")
        page.screenshot(path=str(OUT / "02_auth_login.png"))
        captured.append("02_auth_login.png")

        page.evaluate("""() => {
          document.querySelectorAll('[data-view]').forEach(v => v.classList.remove('active'));
          document.getElementById('view-confirm').classList.add('active');
          document.getElementById('confirm-email-display').textContent = 'you@example.com';
        }""")
        page.screenshot(path=str(OUT / "03_auth_email_confirm.png"))
        captured.append("03_auth_email_confirm.png")

        # Birth intake default
        page.goto(f"{BASE}/map_CURRENT.html", wait_until="domcontentloaded")
        page.add_script_tag(url=f"{BASE}/first_profile_intake.js")
        page.evaluate("() => window.__showFirstProfileIntake()")
        page.wait_for_selector("#rm-first-profile-intake", timeout=10000)
        time.sleep(0.2)
        page.screenshot(path=str(OUT / "10_birth_intake_default.png"))
        captured.append("10_birth_intake_default.png")

        # Validation error
        page.click("#rm-intake-submit")
        time.sleep(0.2)
        page.screenshot(path=str(OUT / "12_birth_intake_validation_error.png"))
        captured.append("12_birth_intake_validation_error.png")

        browser.close()

    manifest = {"captured": captured, "base": BASE}
    (OUT / "capture_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    server.terminate()
    print(f"Captured {len(captured)} screenshots to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
