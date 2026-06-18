#!/usr/bin/env python3
"""Smoke: Web 2.0 shell Context Transport Contract (hash route + query params).

Journeys:
  * Dashboard → Chart Record → Map
  * Favorite → Map
  * Saved exploration → Map
  * Comparison → Map → Return (returnTo)


Requires SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY (.env.staging).
Auth: admin magic-link OTP for RM_SMOKE_EMAIL (default davidleongoodman@gmail.com).

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_app_shell_context_transport.py
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
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
PYTHON = ROOT / "venv" / "bin" / "python"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


DEFAULT_SMOKE_EMAIL = "davidleongoodman@gmail.com"




def shell_navigate(page, route: str, patch: dict | None = None) -> None:
    """Drive in-shell hash transport without leaving app_shell.html."""
    page.evaluate(
        "([route, patch]) => window.__rmAppShell.navigate(route, patch || {})",
        [route, patch or {}],
    )

def resolve_shell_fixtures(page) -> dict[str, str | None]:
    """Resolve chart/place/exploration/comparison IDs from the live Supabase viewModel."""
    page.wait_for_selector("button[data-chart-record]", timeout=15_000)
    fx = page.evaluate("""() => {
      const vm = window.__rmAppShell.viewModel();
      const cr = (vm.chartRecords || [])[0];
      if (!cr) return null;
      const explorationId = (cr.explorations && cr.explorations[0] && cr.explorations[0].id) || null;
      const fav = (cr.favoritePlaces && cr.favoritePlaces[0]) || null;
      const placeId = fav ? (fav.placeId || fav.id) : null;
      const cmp = (vm.comparisonSets || []).find((c) => c.clientId === cr.chartRecordId);
      return {
        chartRecordId: cr.chartRecordId,
        explorationId,
        placeId,
        comparisonSetId: cmp ? cmp.id : null,
      };
    }""")
    if not fx or not fx.get("chartRecordId"):
        fail("could not resolve shell fixtures from authenticated viewModel")
    return fx

def resolve_browser_auth() -> str:
    """Mint a real Supabase session for app_shell (auth_guard requires it)."""
    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon_key, service_key]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY for browser smokes")
    from supabase import create_client

    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_SMOKE_EMAIL).strip()
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


def port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def wait_server(base: str, timeout_s: float = 20.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{base}/health", timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.25)
    return False


def spawn_server(port: int) -> subprocess.Popen:
    return subprocess.Popen(
        [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(ROOT),
        env={**os.environ, "RM_APP_SHELL": "1"},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def ensure_server() -> tuple[str, subprocess.Popen | None]:
    base = BASE
    proc: subprocess.Popen | None = None
    try:
        with urllib.request.urlopen(f"{base}/health", timeout=2) as resp:
            if resp.status != 200:
                raise OSError("bad health")
        with urllib.request.urlopen(f"{base}/app_shell.html", timeout=2) as resp:
            if resp.status != 200:
                raise OSError("app shell missing")
    except Exception:
        alt = 8012
        if not port_free(alt):
            fail(f"Server/store unavailable at {base} and port {alt} busy")
        proc = spawn_server(alt)
        base = f"http://127.0.0.1:{alt}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")
    return base, proc


def parse_shell_hash(raw_hash: str) -> dict[str, str | None]:
    fragment = raw_hash.lstrip("#")
    if not fragment.startswith("/"):
        fragment = "/" + fragment
    parsed = urlparse(fragment)
    route = (parsed.path or "/dashboard").lstrip("/").split("/")[0] or "dashboard"
    qs = parse_qs(parsed.query, keep_blank_values=False)
    return {
        "route": route,
        "chartRecordId": (qs.get("chartRecordId") or [None])[0],
        "placeId": (qs.get("placeId") or [None])[0],
        "explorationId": (qs.get("explorationId") or [None])[0],
        "comparisonSetId": (qs.get("comparisonSetId") or [None])[0],
        "returnTo": unquote((qs.get("returnTo") or [None])[0]) if qs.get("returnTo") else None,
    }


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        fail(f"playwright required: {exc}")

    base, proc = ensure_server()
    results: list[tuple[str, bool, str]] = []

    try:
        auth_init_script = resolve_browser_auth()
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1100, "height": 900})
            context.add_init_script(auth_init_script)
            context.add_init_script(
                "try{localStorage.setItem('rm_guided_onboarding_dismissed','1');}catch(e){}"
            )
            page = context.new_page()

            def ctx():
                return page.evaluate("() => ({ ...window.__rmAppShell.navContext })")

            page.goto(f"{base}/app_shell.html#/dashboard", wait_until="domcontentloaded", timeout=20_000)
            page.wait_for_function(
                "() => window.__rmAppShell && window.__rmAppShell.viewModel()",
                timeout=30_000,
            )
            fx = resolve_shell_fixtures(page)
            cr_id = fx["chartRecordId"]
            exp_id = fx["explorationId"]
            place_id = fx["placeId"]
            cmp_id = fx["comparisonSetId"]

            # Dashboard → Chart Record → Map
            page.click(f'button[data-nav="chart-record"][data-chart-record="{cr_id}"]')
            page.wait_for_function(
                f"() => window.__rmAppShell.navContext.route === 'chart-record'"
                f" && window.__rmAppShell.navContext.chartRecordId === {json.dumps(cr_id)}",
                timeout=10_000,
            )
            shell_navigate(page, "map", {"chartRecordId": cr_id})
            page.wait_for_function(
                f"() => window.__rmAppShell.navContext.route === 'map'"
                f" && window.__rmAppShell.navContext.chartRecordId === {json.dumps(cr_id)}",
                timeout=10_000,
            )
            h1 = parse_shell_hash(page.evaluate("() => location.hash"))
            ok1 = (
                h1["route"] == "map"
                and h1["chartRecordId"] == cr_id
                and f"chartRecordId={cr_id}" in page.evaluate("() => location.hash")
            )
            results.append(("dashboard_chart_record_map", ok1, json.dumps(h1)))

            # Favorite → Map (skip when account has no favorites)
            if place_id:
                page.goto(
                    f"{base}/app_shell.html#/chart-record?chartRecordId={cr_id}",
                    wait_until="domcontentloaded",
                )
                page.wait_for_function("() => window.__rmAppShell.viewModel()", timeout=30_000)
                page.wait_for_selector(
                    f'button[data-action="open-map-favorite"][data-place-id="{place_id}"]',
                    timeout=10_000,
                )
                shell_navigate(page, "map", {"chartRecordId": cr_id, "placeId": place_id})
                page.wait_for_function(
                    f"() => window.__rmAppShell.navContext.route === 'map'"
                    f" && window.__rmAppShell.navContext.placeId === {json.dumps(place_id)}",
                    timeout=10_000,
                )
                h2 = parse_shell_hash(page.evaluate("() => location.hash"))
                ok2 = h2["placeId"] == place_id and h2["chartRecordId"] == cr_id
                results.append(("favorite_to_map", ok2, json.dumps(h2)))
            else:
                results.append(("favorite_to_map", True, "skipped — no favorites in account"))

            # Exploration → Map
            if not exp_id:
                fail("authenticated account missing exploration fixture for shell transport smoke")
            page.goto(f"{base}/app_shell.html#/chart-record?chartRecordId={cr_id}", wait_until="domcontentloaded")
            page.wait_for_function("() => window.__rmAppShell.viewModel()", timeout=30_000)
            shell_navigate(page, "map", {"chartRecordId": cr_id, "explorationId": exp_id})
            page.wait_for_function(
                f"() => window.__rmAppShell.navContext.route === 'map'"
                f" && window.__rmAppShell.navContext.explorationId === {json.dumps(exp_id)}",
                timeout=10_000,
            )
            h3 = parse_shell_hash(page.evaluate("() => location.hash"))
            ok3 = h3["explorationId"] == exp_id and h3["chartRecordId"] == cr_id
            results.append(("exploration_to_map", ok3, json.dumps(h3)))

            # Comparison → Map → Return
            if not cmp_id:
                fail("authenticated account missing comparison set fixture for shell transport smoke")
            page.click('button[data-nav="compare"]')
            page.wait_for_function(
                f"() => window.__rmAppShell.navContext.route === 'compare'"
                f" && window.__rmAppShell.navContext.comparisonSetId === {json.dumps(cmp_id)}",
                timeout=10_000,
            )
            h4 = parse_shell_hash(page.evaluate("() => location.hash"))
            ok4 = h4["comparisonSetId"] == cmp_id and h4.get("returnTo")
            page.click('button[data-action="compare-back-map"]')
            page.wait_for_function(
                f"() => window.__rmAppShell.navContext.route === 'map'"
                f" && window.__rmAppShell.navContext.chartRecordId === {json.dumps(cr_id)}",
                timeout=10_000,
            )
            after = ctx()
            h5 = parse_shell_hash(page.evaluate("() => location.hash"))
            ok5 = (
                after.get("route") == "map"
                and after.get("chartRecordId") == cr_id
                and after.get("explorationId") == exp_id
                and after.get("returnTo") is None
            )
            results.append(("compare_to_map_return", ok4 and ok5, json.dumps({"compare": h4, "return": h5, "ctx": after})))

            contract_ok = page.evaluate(
                """() => {
                  const c = window.__rmAppShell.ROUTE_CONTEXT_CONTRACT;
                  return c.map.chartRecordId === 'required'
                    && c.compare.comparisonSetId === 'required'
                    && window.__rmAppShell.CONTEXT_TRANSPORT_STRATEGY === 'hash-route-query';
                }"""
            )
            results.append(("contract_surface", contract_ok, "ROUTE_CONTEXT_CONTRACT exported"))

            browser.close()

        failed = [name for name, ok, _ in results if not ok]
        for name, ok, detail in results:
            print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
        if failed:
            fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")
        print("PASS: smoke_app_shell_context_transport")
        return 0
    finally:
        if proc is not None:
            proc.terminate()
            proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
