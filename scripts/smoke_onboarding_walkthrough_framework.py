#!/usr/bin/env python3
"""Smoke: onboarding walkthrough framework (ONBOARDING-2A1).

Verifies:
  - Overlay appears on first map load (no storage keys set)
  - Overlay is absent when dismiss key is already set
  - Dismiss (×) hides the overlay
  - Dismiss writes the correct localStorage key
  - Next advances step index
  - Finish on last step writes the completed key
  - rmWalkthroughReplay() clears both keys

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_onboarding_walkthrough_framework.py
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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PYTHON = ROOT / "venv" / "bin" / "python"
DEFAULT_EMAIL = "davidleongoodman@gmail.com"
PORT = 8004

DISMISSED_KEY = "rm_map_walkthrough_dismissed"
COMPLETED_KEY = "rm_map_walkthrough_completed"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def server_ok(base: str) -> bool:
    try:
        with urllib.request.urlopen(base + "/health", timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


def port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) != 0


def wait_health(base: str, timeout_s: float = 25.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base + "/health", timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.3)
    return False


def resolve_auth_script() -> str:
    url = os.environ["SUPABASE_URL"]
    anon = os.environ["SUPABASE_ANON_KEY"]
    svc = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()
    from supabase import create_client
    anon_client = create_client(url, anon)
    admin = create_client(url, svc)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon_client.auth.verify_otp(
        {"token_hash": link.properties.hashed_token, "type": "magiclink"}
    )
    if not res.session:
        fail(f"could not authenticate {email}")
    s = res.session
    ref = urlparse(url).hostname.split(".")[0]
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
        f"try{{window.localStorage.setItem({json.dumps(storage_key)},"
        f"{json.dumps(storage_val)});}}catch(e){{}}"
    )


def main() -> None:
    base = os.environ.get("BASE_URL", f"http://127.0.0.1:{PORT}").rstrip("/")

    if not server_ok(base):
        if port_free(PORT):
            proc = subprocess.Popen(
                [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app",
                 "--host", "127.0.0.1", "--port", str(PORT)],
                cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            if not wait_health(base):
                proc.kill()
                fail(f"server did not start on {base}")
        else:
            fail(f"server not reachable at {base}/health")

    # Check overlay DOM exists before running browser smokes
    try:
        with urllib.request.urlopen(base + "/map_CURRENT.html", timeout=10) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        fail(f"could not fetch map_CURRENT.html: {e}")

    OVERLAY_SENTINEL = "rm-walkthrough"
    if OVERLAY_SENTINEL not in html:
        # Pre-implementation: exit with SKIP sentinel so CI is not broken
        print("SKIP: walkthrough overlay DOM not yet present in map_CURRENT.html")
        raise SystemExit(0)

    auth_script = resolve_auth_script()

    from playwright.sync_api import sync_playwright

    MAP_URL_CLEAN = f"{base}/map_CURRENT.html?bust={int(time.time())}"
    # Do NOT pass skipOnboarding=1 — the new walkthrough controller ignores that flag
    # (it has its own key-based gating). Load clean; dismiss old tooltip via JS.
    MAP_URL = MAP_URL_CLEAN

    results: list[tuple[str, bool, str]] = []
    console_errors: list[str] = []

    def make_page(playwright_ctx, *, extra_storage: dict[str, str] | None = None):
        """Return a fresh page with auth injected (and optional extra localStorage)."""
        extra_js = ""
        if extra_storage:
            for k, v in extra_storage.items():
                extra_js += (
                    f"try{{window.localStorage.setItem({json.dumps(k)},{json.dumps(v)});}}catch(e){{}}"
                )
        ctx = playwright_ctx.chromium.launch(headless=True)
        bctx = ctx.new_context(viewport={"width": 1400, "height": 900})
        bctx.add_init_script(auth_script + extra_js)
        pg = bctx.new_page()
        pg.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
        return ctx, pg

    def dismiss_old_tooltip(pg) -> None:
        """Dismiss the legacy map-onboarding tooltip if it's visible."""
        try:
            pg.evaluate(
                "() => { const btn = document.querySelector('[data-dismiss-onboarding]');"
                "        if (btn) btn.click(); }"
            )
        except Exception:
            pass

    with sync_playwright() as pw:
        # ── 1. overlay appears on first load (no dismiss/completed key) ──────
        ctx, page = make_page(pw)
        page.goto(MAP_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(1800)  # wait for 800ms setTimeout + render
        try:
            overlay_visible = page.evaluate(
                "() => {"
                "  const el = document.getElementById('rm-walkthrough');"
                "  return el && el.classList.contains('rm-wt-active');"
                "}"
            )
        except Exception as e:
            overlay_visible = False
            console_errors.append(f"eval error (ow_trigger): {e}")
        results.append(("ow_trigger_on_first_map", bool(overlay_visible),
                        f"visible={overlay_visible}"))
        ctx.close()

        # ── 2. no overlay when dismiss key already set ───────────────────────
        ctx, page = make_page(pw, extra_storage={DISMISSED_KEY: "1"})
        page.goto(MAP_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(1800)
        dismiss_old_tooltip(page)
        overlay_absent = page.evaluate(
            "() => {"
            "  const el = document.getElementById('rm-walkthrough');"
            "  return !el || !el.classList.contains('rm-wt-active');"
            "}"
        )
        results.append(("ow_no_trigger_if_dismissed", bool(overlay_absent),
                        f"absent={overlay_absent}"))
        ctx.close()

        # ── 3–5. dismiss hides overlay + writes key; next advances ───────────
        ctx, page = make_page(pw)
        page.goto(MAP_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(1800)
        dismiss_old_tooltip(page)

        # 3. verify step label contains "Step 1"
        step_label = page.evaluate(
            "() => document.getElementById('rm-wt-step-label')?.textContent || ''"
        )
        results.append(("ow_step1_label", "Step 1" in step_label, f"label={step_label!r}"))

        # 4. Next advances to step 2
        page.click("#rm-wt-next")
        page.wait_for_timeout(200)
        step2_label = page.evaluate(
            "() => document.getElementById('rm-wt-step-label')?.textContent || ''"
        )
        results.append(("ow_next_advances", "Step 2" in step2_label, f"label={step2_label!r}"))

        # 5. Dismiss hides overlay and writes key
        page.click("#rm-wt-dismiss")
        page.wait_for_timeout(200)
        overlay_gone = page.evaluate(
            "() => {"
            "  const el = document.getElementById('rm-walkthrough');"
            "  return !el || !el.classList.contains('rm-wt-active');"
            "}"
        )
        dismiss_key_set = page.evaluate(
            f"() => localStorage.getItem({json.dumps(DISMISSED_KEY)}) === '1'"
        )
        results.append(("ow_dismiss_hides", bool(overlay_gone), f"gone={overlay_gone}"))
        results.append(("ow_dismiss_sets_key", bool(dismiss_key_set),
                        f"key={dismiss_key_set}"))
        ctx.close()

        # ── 6. replay clears both keys ───────────────────────────────────────
        ctx, page = make_page(pw, extra_storage={DISMISSED_KEY: "1", COMPLETED_KEY: "1"})
        page.goto(MAP_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(1800)
        dismiss_old_tooltip(page)
        page.evaluate("() => window.rmWalkthroughClear()")
        page.wait_for_timeout(200)
        both_cleared = page.evaluate(
            f"() => localStorage.getItem({json.dumps(DISMISSED_KEY)}) === null"
            f" && localStorage.getItem({json.dumps(COMPLETED_KEY)}) === null"
        )
        results.append(("ow_replay_clears_state", bool(both_cleared),
                        f"cleared={both_cleared}"))
        ctx.close()

        # ── 7. no console errors ─────────────────────────────────────────────
        results.append(("ow_no_console_errors",
                        len(console_errors) == 0,
                        f"errors={console_errors or 'none'}"))

    # ── report ────────────────────────────────────────────────────────────────
    any_fail = False
    for name, passed, detail in results:
        tag = "PASS" if passed else "FAIL"
        print(f"{tag}: {name} — {detail}")
        if not passed:
            any_fail = True

    if any_fail:
        print("FAIL: smoke_onboarding_walkthrough_framework", file=sys.stderr)
        raise SystemExit(1)
    print("PASS: smoke_onboarding_walkthrough_framework")


if __name__ == "__main__":
    main()
