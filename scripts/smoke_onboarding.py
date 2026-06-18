#!/usr/bin/env python3
"""Smoke: guided onboarding overlay in app_shell.html.

Verifies:
  * ONBOARDING_SLIDES config present (7 slides)
  * Modal auto-opens when rm_guided_onboarding_dismissed absent
  * Dismiss persists to localStorage
  * Replay from Help & Learn reopens tour

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_onboarding.py
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
PYTHON = ROOT / "venv" / "bin" / "python"
GUIDED_KEY = "rm_guided_onboarding_dismissed"


def is_benign_console_error(text: str) -> bool:
    return "Failed to load resource" in text and "404" in text


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def resolve_browser_auth() -> str:
    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon_key, service_key]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY")
    from supabase import create_client

    email = os.environ.get("RM_SMOKE_EMAIL", "davidleongoodman@gmail.com").strip()
    anon_client = create_client(url, anon_key)
    admin = create_client(url, service_key)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon_client.auth.verify_otp(
        {"token_hash": link.properties.hashed_token, "type": "magiclink"}
    )
    if not res.session:
        fail(f"could not authenticate {email}")
    ref = urlparse(url).hostname.split(".")[0]
    s = res.session
    storage_key = f"sb-{ref}-auth-token"
    storage_val = json.dumps({
        "access_token": s.access_token,
        "refresh_token": s.refresh_token,
        "expires_at": s.expires_at,
        "expires_in": s.expires_in,
        "token_type": s.token_type or "bearer",
        "user": json.loads(res.user.model_dump_json()),
    })
    return (
        f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
    )


def main() -> int:
    proc = None
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        fail("playwright not installed")

    port = int(urlparse(BASE).port or 8000)
    if port_free(port):
        proc = subprocess.Popen(
            [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app", "--host", "127.0.0.1", f"--port={port}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(40):
            try:
                with urllib.request.urlopen(f"{BASE}/health", timeout=1) as resp:
                    if resp.status == 200:
                        break
            except (urllib.error.URLError, TimeoutError):
                time.sleep(0.25)
        else:
            fail(f"server did not start on {BASE}")

    auth_script = resolve_browser_auth()
    results: list[tuple[str, bool, str]] = []
    console_errors: list[str] = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.on(
                "console",
                lambda m: console_errors.append(m.text)
                if m.type == "error" and not is_benign_console_error(m.text)
                else None,
            )
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.add_init_script(auth_script)
            page.add_init_script(f"try{{localStorage.removeItem({json.dumps(GUIDED_KEY)});}}catch(e){{}}")

            page.goto(f"{BASE}/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.__rmAppShell && Array.isArray(window.ONBOARDING_SLIDES)",
                timeout=30_000,
            )

            slide_count = page.evaluate("() => window.ONBOARDING_SLIDES.length")
            results.append(("slides_config", slide_count == 7, f"count={slide_count}"))

            page.wait_for_selector("#guidedOnboardingModal.open", timeout=15_000)
            title = page.inner_text("#guidedOnboardingTitle")
            results.append(("auto_open", title == "Welcome", f"title={title!r}"))

            page.click("[data-action=guided-onboarding-next]")
            page.wait_for_function(
                "() => document.getElementById('guidedOnboardingTitle').textContent === 'Meet Genie'",
                timeout=5_000,
            )
            results.append(("next_slide", True, "Meet Genie"))

            page.click("[data-action=guided-onboarding-dismiss]")
            page.wait_for_function(
                "() => !document.getElementById('guidedOnboardingModal').classList.contains('open')",
                timeout=5_000,
            )
            dismissed = page.evaluate(
                f"() => localStorage.getItem({json.dumps(GUIDED_KEY)}) === '1'"
            )
            results.append(("dismiss_persists", dismissed, f"key={GUIDED_KEY}"))

            page.evaluate("() => window.__rmAppShell.navigate('help')")
            page.wait_for_selector("[data-action='replay-guided-onboarding']", timeout=15_000)
            page.click("[data-action='replay-guided-onboarding']")
            page.wait_for_selector("#guidedOnboardingModal.open", timeout=10_000)
            replay_title = page.inner_text("#guidedOnboardingTitle")
            results.append(("replay_help", replay_title == "Welcome", f"title={replay_title!r}"))

            browser.close()
    finally:
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()

    failed = [n for n, ok, _ in results if not ok]
    for n, ok, d in results:
        print(f"{'PASS' if ok else 'FAIL'}: {n} — {d}")
    if console_errors:
        print("Console errors:", console_errors[:5], file=sys.stderr)
        failed.append("console_errors")
    if failed:
        fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")
    print("PASS: smoke_onboarding")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
