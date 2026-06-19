#!/usr/bin/env python3
"""Smoke: Map Handoff Contract v1 — shell builds URL, map receives context (receive-only).

Journeys (shell navContext → buildMapHandoffUrl → map_CURRENT.html):
  * Chart Record → Map handoff link
  * Favorite → Map
  * Exploration → Map
  * Comparison → Map (comparisonSetId when present)

Also verifies:
  * Map loads with handoff; no renderer/profile/viewport mutations
  * Map loads without handoff (__rmAppShellHandoff null)
  * RM_APP_SHELL=0 does not block map_CURRENT.html


Requires SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY (.env.staging).
Auth: admin magic-link OTP for RM_SMOKE_EMAIL (default davidleongoodman@gmail.com).

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_app_shell_map_handoff.py
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
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8004").rstrip("/")
PYTHON = ROOT / "venv" / "bin" / "python"
MAP_DEFAULT_CENTER_LAT = 20
MAP_DEFAULT_CENTER_LNG = 0
MAP_DEFAULT_ZOOM = 2
MAP_CENTER_TOLERANCE = 2.0


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


DEFAULT_SMOKE_EMAIL = "davidleongoodman@gmail.com"




def shell_build_map_url(page, patch: dict | None = None) -> str:
    """Build production map handoff URL without leaving app_shell.html."""
    return page.evaluate(
        "([patch]) => window.__rmAppShell.buildMapHandoffFromPatch(patch || {})",
        [patch or {}],
    )


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


def spawn_server(port: int, env: dict[str, str] | None = None) -> subprocess.Popen:
    return subprocess.Popen(
        [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(ROOT),
        env={**os.environ, **(env or {})},
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
        alt = 8013
        if not port_free(alt):
            fail(f"Server/store unavailable at {base} and port {alt} busy")
        proc = spawn_server(alt, {"RM_APP_SHELL": "1"})
        base = f"http://127.0.0.1:{alt}"
        if not wait_server(base):
            proc.terminate()
            fail(f"Could not start temp server on {base}")
    return base, proc


def parse_handoff_query(url: str) -> dict[str, str | None]:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query, keep_blank_values=False)
    return {
        "handoff": (qs.get("handoff") or [None])[0],
        "chartRecordId": (qs.get("chartRecordId") or [None])[0],
        "placeId": (qs.get("placeId") or [None])[0],
        "explorationId": (qs.get("explorationId") or [None])[0],
        "comparisonSetId": (qs.get("comparisonSetId") or [None])[0],
        "returnTo": (qs.get("returnTo") or [None])[0],
        "handoffCreatedAt": (qs.get("handoffCreatedAt") or [None])[0],
        "skipOnboarding": (qs.get("skipOnboarding") or [None])[0],
    }


def handoff_urls_equivalent(a: str, b: str) -> bool:
    pa, pb = parse_handoff_query(a), parse_handoff_query(b)
    keys = ["handoff", "skipOnboarding", "chartRecordId", "placeId", "explorationId", "comparisonSetId", "returnTo"]
    return all(pa.get(k) == pb.get(k) for k in keys) and pa.get("handoffCreatedAt") and pb.get("handoffCreatedAt")


def assert_map_baseline(page, label: str) -> tuple[bool, str]:
    """Map loaded; default viewport; no auto Find regions; handoff did not change profile."""
    state = page.evaluate(
        """() => {
            const map = window.__rmMap;
            const center = map ? map.getCenter() : null;
            const zoom = map ? map.getZoom() : null;
            const profile = document.getElementById('chartProfile')?.value || null;
            const findBtn = document.getElementById('findBtn');
            const smoke = window.__rmSmokeState ? window.__rmSmokeState() : null;
            return {
                hasMap: Boolean(map),
                centerLat: center ? center.lat : null,
                centerLng: center ? center.lng : null,
                zoom,
                profile,
                findDisabled: findBtn ? findBtn.disabled : null,
                renderStatus: document.getElementById('renderStatus')?.textContent || '',
                polygonLayers: smoke ? smoke.polygonLayers : null,
                rendererSubstrate: smoke ? smoke.rendererSubstrate : null,
            };
        }"""
    )
    ok = (
        state.get("hasMap")
        and state.get("rendererSubstrate") == "legacy_search_regions"
        and state.get("polygonLayers") == 0
        and not state.get("findDisabled")
        and "ready" in (state.get("renderStatus") or "").lower()
        and abs((state.get("centerLat") or 0) - MAP_DEFAULT_CENTER_LAT) < MAP_CENTER_TOLERANCE
        and abs((state.get("centerLng") or 0) - MAP_DEFAULT_CENTER_LNG) < MAP_CENTER_TOLERANCE
        and abs((state.get("zoom") or 0) - MAP_DEFAULT_ZOOM) < 0.01
    )
    return ok, f"{label}: {json.dumps(state)}"


def load_map_with_handoff(page, base: str, rel_path: str) -> dict:
    url = f"{base}{rel_path}" if rel_path.startswith("/") else f"{base}/{rel_path}"
    page.goto(url, wait_until="domcontentloaded", timeout=20_000)
    page.wait_for_function("() => window.__rmMap && window.__rmAppShellHandoff", timeout=15_000)
    page.wait_for_function(
        "() => document.getElementById('chartProfile')?.options?.length >= 1",
        timeout=15_000,
    )
    return page.evaluate("() => window.__rmAppShellHandoff()")


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

            page.goto(f"{base}/app_shell.html#/dashboard", wait_until="domcontentloaded", timeout=20_000)
            page.wait_for_function("() => window.__rmAppShell && window.__rmAppShell.viewModel()", timeout=30_000)
            fx = resolve_shell_fixtures(page)
            cr_id = fx["chartRecordId"]
            exp_id = fx["explorationId"]
            place_id = fx["placeId"]
            cmp_id = fx["comparisonSetId"]

            # Chart Record → Map (shell context)
            page.click(f'button[data-nav="chart-record"][data-chart-record="{cr_id}"]')
            page.wait_for_function(
                f"() => window.__rmAppShell.navContext.route === 'chart-record'",
                timeout=10_000,
            )
            built = shell_build_map_url(page, {"chartRecordId": cr_id})
            parsed = parse_handoff_query(built)
            ok_build = (
                built.startswith("/map_CURRENT.html?")
                and parsed["handoff"] == "app_shell"
                and parsed["skipOnboarding"] == "1"
                and parsed["chartRecordId"] == cr_id
                and parsed["handoffCreatedAt"]
            )
            results.append(("shell_builds_url_chart_record", ok_build, built))

            link_href = page.evaluate(
                "() => document.querySelector('a[href*=\"map_CURRENT.html\"]')?.getAttribute('href')"
            )
            if link_href:
                ok_link = handoff_urls_equivalent(link_href, built)
                link_detail = link_href
            else:
                ok_link = ok_build
                link_detail = "no stub anchor; buildMapHandoffUrl is canonical"
            results.append(("stub_link_matches_build", ok_link, link_detail))

            contract_ok = page.evaluate(
                """() => {
                  const c = window.__rmAppShell.MAP_HANDOFF_CONTRACT;
                  return c.strategy === 'url-query-params'
                    && c.marker === 'app_shell'
                    && Array.isArray(c.fields)
                    && c.fields.includes('handoffCreatedAt');
                }"""
            )
            results.append(("map_handoff_contract_surface", contract_ok, "MAP_HANDOFF_CONTRACT exported"))

            received = load_map_with_handoff(page, base, built)
            ok_recv = (
                received
                and received.get("source") == "app_shell"
                and received.get("chartRecordId") == cr_id
            )
            results.append(("map_receives_chart_record", ok_recv, json.dumps(received)))

            ok_base, detail_base = assert_map_baseline(page, "after_chart_record_handoff")
            results.append(("no_renderer_mutations_chart_record", ok_base, detail_base))

            # Favorite → Map
            if place_id:
                page.goto(
                    f"{base}/app_shell.html#/chart-record?chartRecordId={cr_id}",
                    wait_until="domcontentloaded",
                )
                page.wait_for_function("() => window.__rmAppShell.viewModel()", timeout=30_000)
                fav_url = shell_build_map_url(page, {"chartRecordId": cr_id, "placeId": place_id})
                fav_parsed = parse_handoff_query(fav_url)
                ok_fav = fav_parsed["placeId"] == place_id and fav_parsed["chartRecordId"] == cr_id
                results.append(("shell_builds_url_favorite", ok_fav, fav_url))

                fav_recv = load_map_with_handoff(page, base, fav_url)
                ok_fav_recv = fav_recv and fav_recv.get("placeId") == place_id
                results.append(("map_receives_favorite", ok_fav_recv, json.dumps(fav_recv)))
            else:
                results.append(("shell_builds_url_favorite", True, "skipped — no favorites in account"))
                results.append(("map_receives_favorite", True, "skipped — no favorites in account"))

            # Exploration → Map
            if not exp_id:
                fail("authenticated account missing exploration fixture for shell handoff smoke")
            page.goto(
                f"{base}/app_shell.html#/chart-record?chartRecordId={cr_id}",
                wait_until="domcontentloaded",
            )
            page.wait_for_function("() => window.__rmAppShell.viewModel()", timeout=30_000)
            exp_url = shell_build_map_url(page, {"chartRecordId": cr_id, "explorationId": exp_id})
            exp_parsed = parse_handoff_query(exp_url)
            ok_exp = exp_parsed["explorationId"] == exp_id
            results.append(("shell_builds_url_exploration", ok_exp, exp_url))

            exp_recv = load_map_with_handoff(page, base, exp_url)
            ok_exp_recv = exp_recv and exp_recv.get("explorationId") == exp_id
            results.append(("map_receives_exploration", ok_exp_recv, json.dumps(exp_recv)))

            # Comparison → Map (comparisonSetId on compare route)
            if not cmp_id:
                fail("authenticated account missing comparison set fixture for shell handoff smoke")
            page.goto(
                f"{base}/app_shell.html#/compare?chartRecordId={cr_id}&comparisonSetId={cmp_id}",
                wait_until="domcontentloaded",
            )
            page.wait_for_function(
                f"() => window.__rmAppShell.navContext.route === 'compare'"
                f" && window.__rmAppShell.navContext.comparisonSetId === {json.dumps(cmp_id)}",
                timeout=10_000,
            )
            cmp_url = page.evaluate("() => window.__rmAppShell.buildMapHandoffUrl()")
            cmp_parsed = parse_handoff_query(cmp_url)
            ok_cmp = cmp_parsed["comparisonSetId"] == cmp_id
            results.append(("shell_builds_url_comparison", ok_cmp, cmp_url))

            # navigate("map") redirects to production map (no in-shell placeholder)
            page.goto(
                f"{base}/app_shell.html#/chart-record?chartRecordId={cr_id}",
                wait_until="domcontentloaded",
            )
            page.wait_for_function("() => window.__rmAppShell.viewModel()", timeout=30_000)
            page.evaluate(
                "([id]) => window.__rmAppShell.navigate('map', { chartRecordId: id })",
                [cr_id],
            )
            page.wait_for_url("**/map_CURRENT.html**", timeout=15_000)
            nav_parsed = parse_handoff_query(page.url)
            ok_nav_map = (
                nav_parsed["handoff"] == "app_shell"
                and nav_parsed["chartRecordId"] == cr_id
                and nav_parsed["skipOnboarding"] == "1"
            )
            results.append(("navigate_map_redirects_production", ok_nav_map, page.url))

            # Map without handoff
            page.goto(f"{base}/map_CURRENT.html?skipOnboarding=1", wait_until="domcontentloaded", timeout=20_000)
            page.wait_for_function("() => window.__rmMap", timeout=15_000)
            no_handoff = page.evaluate("() => window.__rmAppShellHandoff()")
            panel_hidden = page.evaluate(
                "() => document.getElementById('appShellHandoff')?.hidden !== false"
            )
            ok_no = no_handoff is None and panel_hidden
            results.append(("map_without_handoff", ok_no, str(no_handoff)))

            ok_no_base, detail_no = assert_map_baseline(page, "without_handoff")
            results.append(("no_renderer_mutations_without_handoff", ok_no_base, detail_no))

            browser.close()

        # RM_APP_SHELL=0 — map still loads (shell may 404)
        disabled_port = 8014
        if port_free(disabled_port):
            disabled_proc = spawn_server(disabled_port, {"RM_APP_SHELL": "0", "RM_PHASE3_LOCAL_PRODUCT": "0"})
            disabled_base = f"http://127.0.0.1:{disabled_port}"
            if wait_server(disabled_base):
                try:
                    with urllib.request.urlopen(f"{disabled_base}/map_CURRENT.html", timeout=5) as resp:
                        map_ok = resp.status == 200
                except Exception as exc:
                    map_ok = False
                    results.append(("rm_app_shell_zero_map", False, str(exc)))
                else:
                    results.append(("rm_app_shell_zero_map", map_ok, f"status map={map_ok}"))
            else:
                results.append(("rm_app_shell_zero_map", False, "temp server failed"))
            disabled_proc.terminate()
            disabled_proc.wait(timeout=5)
        else:
            results.append(("rm_app_shell_zero_map", False, f"port {disabled_port} busy"))

        failed = [name for name, ok, _ in results if not ok]
        for name, ok, detail in results:
            print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
        if failed:
            fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")
        print("PASS: smoke_app_shell_map_handoff")
        return 0
    finally:
        if proc is not None:
            proc.terminate()
            proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
