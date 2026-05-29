#!/usr/bin/env python3
"""Smoke: Genie variable-builder sandbox (genie_SANDBOX_variable_builder.html).

Verifies:
  * Sandbox loads from local file (no backend)
  * window.__rmGenieSandbox / __rmAvailableObjectsRegistry hooks
  * Default registry vocabulary (core bodies on, advanced off)
  * Variable-card gating (incomplete blocks Add; max 12)
  * normalizePayload() and Render output shape
  * Registry mock toggles update dropdown vocabulary
  * Transit experimental gating (off by default)
  * Per-card Mute/Solo/NOT layer toggles in payload

Run:
  ./venv/bin/python scripts/smoke_genie_sandbox.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SANDBOX = ROOT / "genie_SANDBOX_variable_builder.html"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not SANDBOX.is_file():
        fail(f"Missing sandbox: {SANDBOX}")

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        fail(f"playwright required: {exc}")

    url = SANDBOX.resolve().as_uri()
    results: list[tuple[str, bool, str]] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=20_000)
        page.wait_for_selector("#variableCards .variable-card", timeout=10_000)

        hooks = page.evaluate(
            """() => ({
              genie: typeof window.__rmGenieSandbox?.getState === 'function',
              norm: typeof window.__rmGenieSandbox?.normalizePayload === 'function',
              reg: typeof window.__rmAvailableObjectsRegistry?.options === 'function',
              max: window.__rmGenieSandbox?.MAX_VARIABLES === 12,
            })"""
        )
        ok_hooks = all(hooks.values())
        results.append(("hooks_present", ok_hooks, json.dumps(hooks)))

        st0 = page.evaluate("() => window.__rmGenieSandbox.getState()")
        ok_init = (
            st0["variableCount"] == 1
            and st0["variables"][0]["type"] == ""
            and st0["transitEnabled"] is False
            and st0["registry"]["bodies"]["sun"] is True
            and st0["registry"]["bodies"]["north_node"] is False
        )
        results.append(("initial_state", ok_init, json.dumps({
            "count": st0["variableCount"],
            "transit": st0["transitEnabled"],
        })))

        bodies = page.evaluate("() => window.__rmAvailableObjectsRegistry.options('bodies').map(x => x[0])")
        results.append(("default_bodies", "sun" in bodies and "north_node" not in bodies, str(bodies[:4])))

        add_disabled = page.evaluate("() => document.getElementById('addVariableBtn').disabled")
        results.append(("add_blocked_incomplete", add_disabled, "addVariableBtn disabled"))

        # Single planet_in_house render
        page.select_option("[data-type-select]", "planet_in_house")
        page.select_option('[data-field="planet"]', "sun")
        page.select_option('[data-field="house"]', "1")
        direct = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        ok_direct = (
            direct["kind"] == "genie_sandbox_render"
            and direct["variableCount"] == 1
            and len(direct["normalized"]["house_conditions"]) == 1
            and direct["normalized"]["house_conditions"][0]["planet"] == "sun"
            and direct["registry_snapshot"]["bodies"]["sun"] is True
        )
        results.append(("normalize_payload_planet", ok_direct, json.dumps({
            "count": direct.get("variableCount"),
            "house": direct["normalized"]["house_conditions"][0] if direct["normalized"]["house_conditions"] else None,
        })))

        page.click("#renderBtn")
        st1 = page.evaluate("() => window.__rmGenieSandbox.getState()")
        ok_render = st1["renderCount"] == 1 and st1["lastNormalizedPayload"] is not None
        results.append(("render_button", ok_render, f"renderCount={st1['renderCount']}"))

        # Three-variable payload: Sun 1st, ASC Libra, Venus trine MC
        page.evaluate(
            """() => {
              document.getElementById('addVariableBtn').click();
              const cards = document.querySelectorAll('[data-type-select]');
              const sel = cards[cards.length - 1];
              sel.value = 'angle_in_sign';
              sel.dispatchEvent(new Event('change', { bubbles: true }));
            }"""
        )
        page.evaluate(
            """() => {
              const signSelects = document.querySelectorAll('[data-field=sign]');
              const angleSelects = document.querySelectorAll('[data-field=angle]');
              if (angleSelects.length) {
                angleSelects[angleSelects.length - 1].value = 'ASC';
                angleSelects[angleSelects.length - 1].dispatchEvent(new Event('change', { bubbles: true }));
              }
              if (signSelects.length) {
                signSelects[signSelects.length - 1].value = 'libra';
                signSelects[signSelects.length - 1].dispatchEvent(new Event('change', { bubbles: true }));
              }
            }"""
        )
        page.evaluate("() => document.getElementById('addVariableBtn').click()")
        page.evaluate(
            """() => {
              const cards = document.querySelectorAll('[data-type-select]');
              const sel = cards[cards.length - 1];
              sel.value = 'aspect_to_angle';
              sel.dispatchEvent(new Event('change', { bubbles: true }));
            }"""
        )
        page.evaluate(
            """() => {
              const p = document.querySelectorAll('[data-field=planet]');
              const a = document.querySelectorAll('[data-field=aspect]');
              const g = document.querySelectorAll('[data-field=angle]');
              if (p.length) { p[p.length-1].value = 'venus'; p[p.length-1].dispatchEvent(new Event('change', {bubbles:true})); }
              if (a.length) { a[a.length-1].value = 'trine'; a[a.length-1].dispatchEvent(new Event('change', {bubbles:true})); }
              if (g.length) { g[g.length-1].value = 'MC'; g[g.length-1].dispatchEvent(new Event('change', {bubbles:true})); }
            }"""
        )
        payload3 = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        ok_three = (
            payload3["variableCount"] == 3
            and len(payload3["normalized"]["house_conditions"]) == 1
            and len(payload3["normalized"]["angle_sign_conditions"]) == 1
            and len(payload3["normalized"]["aspect_conditions"]) == 1
            and payload3["normalized"]["legacy_compatible"]["aspect_overlay"] is not None
        )
        results.append(("three_variable_payload", ok_three, json.dumps({
            "variableCount": payload3.get("variableCount"),
            "houses": len(payload3["normalized"]["house_conditions"]),
            "angles": len(payload3["normalized"]["angle_sign_conditions"]),
            "aspects": len(payload3["normalized"]["aspect_conditions"]),
        })))

        # NOT / mute / solo on first card
        page.evaluate(
            """() => {
              const not = document.querySelector('[data-layer=not]');
              const mute = document.querySelector('[data-layer=mute]');
              const solo = document.querySelector('[data-layer=solo]');
              if (not) { not.checked = true; not.dispatchEvent(new Event('change', {bubbles:true})); }
              if (mute) { mute.checked = true; mute.dispatchEvent(new Event('change', {bubbles:true})); }
              if (solo) { solo.checked = true; solo.dispatchEvent(new Event('change', {bubbles:true})); }
            }"""
        )
        layer_payload = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        lc = layer_payload["normalized"]["layer_controls"]
        ok_layers = (
            len(lc["muted"]) >= 1
            and lc["solo"] is not None
            and len(lc["not"]) >= 1
        )
        results.append(("layer_controls", ok_layers, json.dumps(lc)))

        # Registry toggle: North Node appears in body dropdown
        page.check('input[data-registry-id="north_node"]')
        has_nn = page.evaluate(
            """() => window.__rmAvailableObjectsRegistry.options('bodies').some(x => x[0] === 'north_node')"""
        )
        results.append(("registry_toggle_bodies", has_nn, "north_node enabled"))

        # Transit off by default — type option disabled; modal readable
        page.click("#transitInfoBtn")
        modal_ok = page.evaluate(
            """() => !document.getElementById('transitModalBackdrop').hidden
              && document.getElementById('transitModalBody').textContent.includes('Experimental relocation-transit')"""
        )
        page.click("#transitModalCloseBtn")
        transit_empty = page.evaluate(
            "() => window.__rmGenieSandbox.normalizePayload().normalized.transit_conditions"
        )
        results.append(("transit_off_by_default", modal_ok and len(transit_empty) == 0, str(len(transit_empty))))

        # Max 12 variables (fresh page)
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("#variableCards .variable-card")
        page.select_option("[data-type-select]", "planet_in_house")
        page.evaluate(
            """() => {
              while (window.__rmGenieSandbox.getState().variableCount < 12) {
                if (document.getElementById('addVariableBtn').disabled) break;
                document.getElementById('addVariableBtn').click();
                const cards = document.querySelectorAll('[data-type-select]');
                const sel = cards[cards.length - 1];
                sel.value = 'planet_in_house';
                sel.dispatchEvent(new Event('change', { bubbles: true }));
              }
            }"""
        )
        st_max = page.evaluate("() => window.__rmGenieSandbox.getState()")
        add_hidden = page.evaluate(
            "() => document.getElementById('addVariableBtn').style.display === 'none'"
        )
        results.append(("max_twelve_variables", st_max["variableCount"] == 12 and add_hidden, str(st_max["variableCount"])))

        # No backend HTTP (file:// load only)
        http_reqs: list[str] = []

        def on_request(req):
            if req.url.startswith("http://") or req.url.startswith("https://"):
                http_reqs.append(req.url)

        page.on("request", on_request)
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector("#variableCards .variable-card")
        results.append(("no_http_backend", len(http_reqs) == 0, http_reqs[:3] if http_reqs else "none"))

        browser.close()

    failed = [name for name, ok, _ in results if not ok]
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {detail}")
    if failed:
        fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")
    print("PASS: smoke_genie_sandbox")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
