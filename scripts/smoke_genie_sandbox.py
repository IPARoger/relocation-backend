#!/usr/bin/env python3
"""Smoke: Genie variable-builder sandbox (genie_SANDBOX_variable_builder.html).

Verifies:
  * Sandbox loads from local file (no backend)
  * window.__rmGenieSandbox / __rmAvailableObjectsRegistry hooks
  * Default registry vocabulary (core bodies on, advanced off)
  * Variable-card gating (incomplete blocks Add; max 12)
  * normalizePayload() Genie Render Payload Contract v1 shape
  * Registry mock toggles update dropdown vocabulary
  * Transit experimental gating (off by default)
  * Per-card Mute/Solo/polarity layer controls in payload
  * Card language registry (Search Map, type labels, angle display)
  * transit_aspect_to_angle canonical type id

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
              transitType: window.__rmGenieSandbox?.VARIABLE_TYPES?.some(
                (t) => t.id === 'transit_aspect_to_angle'
              ),
              noLegacyTransitType: !window.__rmGenieSandbox?.VARIABLE_TYPES?.some(
                (t) => t.id === 'transiting_aspect_to_angle'
              ),
            })"""
        )
        ok_hooks = all(hooks.values())
        results.append(("hooks_present", ok_hooks, json.dumps(hooks)))

        st0 = page.evaluate("() => window.__rmGenieSandbox.getState()")
        ok_init = (
            st0["variableCount"] == 1
            and st0["variables"][0]["type"] == ""
            and st0["variables"][0]["polarity"] == "include"
            and st0["transitEnabled"] is False
            and st0["registry"]["bodies"]["sun"] is True
            and st0["registry"]["bodies"]["north_node"] is False
        )
        results.append(("initial_state", ok_init, json.dumps({
            "count": st0["variableCount"],
            "transit": st0["transitEnabled"],
            "polarity": st0["variables"][0]["polarity"],
        })))

        bodies = page.evaluate("() => window.__rmAvailableObjectsRegistry.options('bodies').map(x => x[0])")
        results.append(("default_bodies", "sun" in bodies and "north_node" not in bodies, str(bodies[:4])))

        add_disabled = page.evaluate("() => document.getElementById('addVariableBtn').disabled")
        results.append(("add_blocked_incomplete", add_disabled, "addVariableBtn disabled"))

        lang_ui = page.evaluate(
            """() => {
              const typeOpts = [...document.querySelector('[data-type-select]').options].map((o) => o.text);
              return {
                primaryAction: document.getElementById('renderBtn').textContent.trim(),
                typeOpts,
                registry: window.__rmGenieSandbox.getCardLanguageRegistry?.(),
              };
            }"""
        )
        ok_lang_ui = (
            lang_ui["primaryAction"] == "Search Map"
            and "Planet · House" in lang_ui["typeOpts"]
            and "Angle · Sign" in lang_ui["typeOpts"]
            and "Aspect · Angle" in lang_ui["typeOpts"]
            and lang_ui["registry"]["separatorToken"] == "·"
            and lang_ui["registry"]["labels"]["planet_in_house"] == "Planet · House"
        )
        results.append(("language_registry_ui", ok_lang_ui, json.dumps({
            "primaryAction": lang_ui["primaryAction"],
            "typeOptsSample": lang_ui["typeOpts"][:5],
        })))

        page.select_option("[data-type-select]", "angle_in_sign")
        angle_opts = page.evaluate(
            """() => [...document.querySelector('[data-field=angle]').options]
              .map((o) => ({ text: o.text, value: o.value }))"""
        )
        asc = next((o for o in angle_opts if o["value"] == "ASC"), None)
        ok_angle_label = asc is not None and asc["text"] == "Ascendant (ASC)"
        results.append(("angle_dropdown_labels", ok_angle_label, json.dumps(asc)))

        # Single planet_in_house render — contract v1 shape
        page.select_option("[data-type-select]", "planet_in_house")
        page.select_option('[data-field="body"]', "sun")
        page.select_option('[data-field="house"]', "1")
        direct = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        v0 = direct["variables"][0]
        ok_direct = (
            direct["kind"] == "genie_render"
            and isinstance(direct.get("createdAt"), str)
            and direct["createdAt"]
            and direct.get("chartRecordId")
            and direct.get("layerControls") is not None
            and direct.get("settingsSnapshot", {}).get("transitModeEnabled") is False
            and direct.get("legacyCompatibility") is not None
            and v0["polarity"] == "include"
            and v0["type"] == "planet_in_house"
            and v0["fields"].get("body") == "sun"
            and "planet" not in v0["fields"]
            and v0["status"] == "complete"
            and direct["legacyCompatibility"]["house_conditions"][0]["planet"] == "sun"
            and direct["settingsSnapshot"]["registry"]["bodies"]["sun"] is True
            and direct["settingsSnapshot"]["cardLanguage"]["primaryAction"] == "Search Map"
            and direct["settingsSnapshot"]["cardLanguage"]["labels"]["aspect_to_angle"] == "Aspect · Angle"
            and v0["label"] == "Planet · House"
            and direct["settingsSnapshot"]["cardLanguage"]["controls"]["excludeLabel"] == "Exclude"
        )
        results.append(("normalize_payload_planet", ok_direct, json.dumps({
            "kind": direct.get("kind"),
            "body": v0["fields"].get("body"),
            "polarity": v0.get("polarity"),
            "label": v0.get("label"),
        })))

        exclude_label_ui = page.evaluate(
            """() => document.querySelector('[data-layer=not]')?.closest('label')?.textContent?.trim()"""
        )
        page.evaluate(
            """() => {
              const ex = document.querySelector('[data-layer=not]');
              if (ex) { ex.checked = true; ex.dispatchEvent(new Event('change', {bubbles:true})); }
            }"""
        )
        exclude_payload = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        ev = exclude_payload["variables"][0]
        ok_registry_exclude = (
            exclude_label_ui == "Exclude"
            and ev["label"] == "Planet · House"
            and ev["polarity"] == "exclude"
            and ev["id"] in exclude_payload["layerControls"]["excludeVariableIds"]
            and exclude_payload["settingsSnapshot"]["cardLanguage"]["controls"]["excludeCompactLabel"] == "⊘"
        )
        results.append(("registry_composed_labels", ok_registry_exclude, json.dumps({
            "excludeLabelUi": exclude_label_ui,
            "label": ev.get("label"),
            "polarity": ev.get("polarity"),
        })))

        page.click("#renderBtn")
        st1 = page.evaluate("() => window.__rmGenieSandbox.getState()")
        ok_render = st1["renderCount"] == 1 and st1["lastNormalizedPayload"] is not None
        results.append(("render_button", ok_render, f"renderCount={st1['renderCount']}"))

        # Exclude-only legacy: NOT planet_in_house must not enter positive legacy slots
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("#variableCards .variable-card")
        page.select_option("[data-type-select]", "planet_in_house")
        page.select_option('[data-field="body"]', "moon")
        page.select_option('[data-field="house"]', "4")
        page.evaluate(
            """() => {
              const not = document.querySelector('[data-layer=not]');
              if (not) { not.checked = true; not.dispatchEvent(new Event('change', {bubbles:true})); }
            }"""
        )
        exclude_only = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        var0 = exclude_only["variables"][0]
        legacy0 = exclude_only["legacyCompatibility"]
        ok_exclude_only = (
            var0["polarity"] == "exclude"
            and var0["id"] in exclude_only["layerControls"]["excludeVariableIds"]
            and len(legacy0["notExclusions"]) == 1
            and legacy0["notExclusions"][0]["planet"] == "moon"
            and legacy0["notExclusions"][0]["house"] == 4
            and len(legacy0["house_conditions"]) == 0
            and len(legacy0["angle_sign_conditions"]) == 0
            and legacy0["aspect_overlay"] is None
        )
        results.append(("legacy_exclude_only", ok_exclude_only, json.dumps({
            "polarity": var0["polarity"],
            "notExclusions": len(legacy0["notExclusions"]),
            "house_conditions": len(legacy0["house_conditions"]),
        })))

        # Mixed legacy: exclude Moon 4H + include Sun 1H
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("#variableCards .variable-card")
        page.select_option("[data-type-select]", "planet_in_house")
        page.select_option('[data-field="body"]', "moon")
        page.select_option('[data-field="house"]', "4")
        page.evaluate(
            """() => {
              const not = document.querySelector('[data-layer=not]');
              if (not) { not.checked = true; not.dispatchEvent(new Event('change', {bubbles:true})); }
            }"""
        )
        page.evaluate("() => document.getElementById('addVariableBtn').click()")
        page.evaluate(
            """() => {
              const cards = document.querySelectorAll('[data-type-select]');
              const sel = cards[cards.length - 1];
              sel.value = 'planet_in_house';
              sel.dispatchEvent(new Event('change', { bubbles: true }));
            }"""
        )
        page.evaluate(
            """() => {
              const bodies = document.querySelectorAll('[data-field=body]');
              const houses = document.querySelectorAll('[data-field=house]');
              if (bodies.length) {
                bodies[bodies.length - 1].value = 'sun';
                bodies[bodies.length - 1].dispatchEvent(new Event('change', { bubbles: true }));
              }
              if (houses.length) {
                houses[houses.length - 1].value = '1';
                houses[houses.length - 1].dispatchEvent(new Event('change', { bubbles: true }));
              }
            }"""
        )
        mixed = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        legacy_m = mixed["legacyCompatibility"]
        ok_mixed = (
            len(legacy_m["house_conditions"]) == 1
            and legacy_m["house_conditions"][0]["planet"] == "sun"
            and legacy_m["house_conditions"][0]["house"] == 1
            and len(legacy_m["notExclusions"]) == 1
            and legacy_m["notExclusions"][0]["planet"] == "moon"
            and legacy_m["notExclusions"][0]["house"] == 4
            and legacy_m["house_conditions"][0]["planet"] != "moon"
        )
        results.append(("legacy_exclude_mixed", ok_mixed, json.dumps({
            "house": legacy_m["house_conditions"][0] if legacy_m["house_conditions"] else None,
            "notExclusion": legacy_m["notExclusions"][0] if legacy_m["notExclusions"] else None,
        })))

        # Three-variable payload: Sun 1st, ASC Libra, Venus trine MC
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("#variableCards .variable-card")
        page.select_option("[data-type-select]", "planet_in_house")
        page.select_option('[data-field="body"]', "sun")
        page.select_option('[data-field="house"]', "1")
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
              const b = document.querySelectorAll('[data-field=body]');
              const a = document.querySelectorAll('[data-field=aspect]');
              const g = document.querySelectorAll('[data-field=angle]');
              if (b.length) { b[b.length-1].value = 'venus'; b[b.length-1].dispatchEvent(new Event('change', {bubbles:true})); }
              if (a.length) { a[a.length-1].value = 'trine'; a[a.length-1].dispatchEvent(new Event('change', {bubbles:true})); }
              if (g.length) { g[g.length-1].value = 'MC'; g[g.length-1].dispatchEvent(new Event('change', {bubbles:true})); }
            }"""
        )
        payload3 = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        complete = [v for v in payload3["variables"] if v["status"] == "complete"]
        legacy = payload3["legacyCompatibility"]
        ok_three = (
            len(complete) == 3
            and len(legacy["house_conditions"]) == 1
            and len(legacy["angle_sign_conditions"]) == 1
            and legacy["aspect_overlay"] is not None
            and all(v["fields"].get("body") or v["fields"].get("angle") for v in complete)
        )
        results.append(("three_variable_payload", ok_three, json.dumps({
            "completeCount": len(complete),
            "houses": len(legacy["house_conditions"]),
            "angles": len(legacy["angle_sign_conditions"]),
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
        lc = layer_payload["layerControls"]
        first_var = layer_payload["variables"][0]
        ok_layers = (
            len(lc["mutedVariableIds"]) >= 1
            and lc["soloVariableId"] is not None
            and len(lc["excludeVariableIds"]) >= 1
            and first_var["polarity"] == "exclude"
            and len(layer_payload["legacyCompatibility"]["house_conditions"]) == 0
        )
        results.append(("layer_controls", ok_layers, json.dumps({
            "layerControls": lc,
            "polarity": first_var["polarity"],
        })))

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
        transit_off = page.evaluate(
            """() => {
              const p = window.__rmGenieSandbox.normalizePayload();
              return p.settingsSnapshot.transitModeEnabled === false
                && !p.variables.some((v) => v.type === 'transit_aspect_to_angle' && v.status === 'experimental');
            }"""
        )
        results.append(("transit_off_by_default", modal_ok and transit_off, str(transit_off)))

        # Legacy degradation: 4 include planet_in_house → 4th unmapped
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("#variableCards .variable-card")
        page.select_option("[data-type-select]", "planet_in_house")
        page.select_option('[data-field="body"]', "sun")
        page.select_option('[data-field="house"]', "1")
        for body, house in [("moon", "2"), ("mercury", "3"), ("venus", "4")]:
            page.evaluate("() => document.getElementById('addVariableBtn').click()")
            page.evaluate(
                """() => {
                  const cards = document.querySelectorAll('[data-type-select]');
                  const sel = cards[cards.length - 1];
                  sel.value = 'planet_in_house';
                  sel.dispatchEvent(new Event('change', { bubbles: true }));
                }"""
            )
            page.evaluate(
                """(pair) => {
                  const bodies = document.querySelectorAll('[data-field=body]');
                  const houses = document.querySelectorAll('[data-field=house]');
                  if (bodies.length) {
                    bodies[bodies.length - 1].value = pair.body;
                    bodies[bodies.length - 1].dispatchEvent(new Event('change', { bubbles: true }));
                  }
                  if (houses.length) {
                    houses[houses.length - 1].value = pair.house;
                    houses[houses.length - 1].dispatchEvent(new Event('change', { bubbles: true }));
                  }
                }""",
                {"body": body, "house": house},
            )
        degrade4 = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        leg4 = degrade4["legacyCompatibility"]
        deg4 = leg4["degradation"]
        fourth_id = degrade4["variables"][3]["id"]
        ok_degrade4 = (
            len(leg4["house_conditions"]) == 3
            and fourth_id in deg4["unmappedVariableIds"]
            and len(deg4["warnings"]) >= 1
            and deg4["canonicalVariableCount"] == 4
            and deg4["legacyMappedCount"] == 3
        )
        results.append(("legacy_degradation_four_houses", ok_degrade4, json.dumps({
            "house_conditions": len(leg4["house_conditions"]),
            "unmapped": deg4["unmappedVariableIds"],
            "warnings": len(deg4["warnings"]),
        })))

        # Legacy degradation: 2 include aspect_to_angle → 2nd unmapped
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("#variableCards .variable-card")
        page.select_option("[data-type-select]", "aspect_to_angle")
        page.evaluate(
            """() => {
              const b = document.querySelectorAll('[data-field=body]');
              const a = document.querySelectorAll('[data-field=aspect]');
              const g = document.querySelectorAll('[data-field=angle]');
              if (b.length) { b[0].value = 'venus'; b[0].dispatchEvent(new Event('change', {bubbles:true})); }
              if (a.length) { a[0].value = 'trine'; a[0].dispatchEvent(new Event('change', {bubbles:true})); }
              if (g.length) { g[0].value = 'MC'; g[0].dispatchEvent(new Event('change', {bubbles:true})); }
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
              const b = document.querySelectorAll('[data-field=body]');
              const a = document.querySelectorAll('[data-field=aspect]');
              const g = document.querySelectorAll('[data-field=angle]');
              if (b.length) { b[b.length-1].value = 'mars'; b[b.length-1].dispatchEvent(new Event('change', {bubbles:true})); }
              if (a.length) { a[a.length-1].value = 'square'; a[a.length-1].dispatchEvent(new Event('change', {bubbles:true})); }
              if (g.length) { g[g.length-1].value = 'ASC'; g[g.length-1].dispatchEvent(new Event('change', {bubbles:true})); }
            }"""
        )
        degrade2a = page.evaluate("() => window.__rmGenieSandbox.normalizePayload()")
        leg2a = degrade2a["legacyCompatibility"]
        deg2a = leg2a["degradation"]
        second_aspect_id = degrade2a["variables"][1]["id"]
        first_aspect_id = degrade2a["variables"][0]["id"]
        ok_degrade2a = (
            leg2a["aspect_overlay"] is not None
            and leg2a["aspect_overlay"]["variableId"] == first_aspect_id
            and second_aspect_id in deg2a["unmappedVariableIds"]
            and len(deg2a["warnings"]) >= 1
            and deg2a["legacyMappedCount"] == 1
        )
        results.append(("legacy_degradation_two_aspects", ok_degrade2a, json.dumps({
            "aspect_overlay": leg2a["aspect_overlay"]["variableId"] if leg2a["aspect_overlay"] else None,
            "unmapped": deg2a["unmappedVariableIds"],
        })))

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
