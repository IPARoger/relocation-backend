# 241 — Genie v7 Builder UI Port (Stage 2, UI ONLY)

**Mode:** Implementation — UI only. No truth execution touched.
**Scope rule honored:** Search NOT connected · Save NOT connected · backend NOT
connected · overlays NOT connected · no motion · no FLIP.

---

## What was ported

The dynamic Genie v7 variable builder shell was ported from
`map_SANDBOX_genie_v7.html` into `map_CURRENT.html`, fully self-contained and
namespaced so it cannot collide with or alter production behavior.

| Ported piece | Source (v7) | Destination (map_CURRENT) |
|--------------|-------------|---------------------------|
| Builder structure | `#builder` | `#gv-builder-host > .gv-builder` |
| Chips (vertical list) | `#chips` / `renderChips` | `#gv-chips` / `renderChips` |
| Build rows + master row | `#buildrow` / `renderBuildRow` | `#gv-buildrow` / `renderBuildRow` |
| Custom dropdown UI | `.g-dd` / `.gddmenu` / `openGdd` | `.gv-g-dd` / `.gv-gddmenu` / `openGdd` |
| Sub-field row | `.subs` / `renderSubs` | `.gv-subs` / `renderSubs` |
| NOT / redact toggle | `.not-box` | `.gv-not-box` |
| Add Variable button | `#addBtn` | `#gv-addBtn` (functional, in-memory) |
| Genie empty hint | `#genieHint` | `#gv-genieHint` |
| Ghost strip visual shell | `#ghoststrip` / `renderGhost` | `#gv-ghoststrip` / `renderGhost` (mute/solo/NOT, in-memory) |
| Bottle visual shell | `#bottle` + badge | `#gv-bottle` + `#gv-bottleBadge` (static, visual) |
| Clear control | `data-act="clearmap"` | `data-gv-act="clearmap"` (in-memory) |

### Categories ported (in-memory model only)
`Planet – House`, `Angle – Sign`, `Aspect – Angle` (with PLANETS / SIGNS /
ANGLES / HOUSES / ASPECTS sources).

---

## Isolation strategy (why production is untouched)

1. **Namespacing:** every ported class is prefixed `gv-` and every attribute is
   `data-gv-*`. Production has no `builder` / `chips` / `g-dd` / `gddmenu` /
   `gtok` classes (verified), so there is zero CSS or selector collision. The
   production ghost token class is `rm-gtok` (distinct from ported `gv-gtok`).
2. **Scoped CSS:** all rules live under `#gv-builder-styles` and reference
   `--gv-*` tokens defined on `#gv-builder-host` (literal v7 defaults), so the
   builder renders correctly regardless of production theme and leaks nothing.
3. **Scoped events:** listeners are bound to `#gv-builder-host` and the ported
   `.gv-gddmenu`. The only document-level listener closes the ported dropdown
   and has no other side effect. Uses `data-gv-*` so it never triggers any
   production `data-act` / `data-role` handler.
4. **In-memory only:** the builder maintains a local `variables[]` / `build`
   state. Add / edit / remove / clear / mute / solo / NOT all mutate memory and
   re-render. There is **no** call to `executeSearchPlan`, `executeGenieRender`,
   `postSearchRegions`, `drawOverlays`, save, or any `fetch`.
5. **Search & Save shells disabled:** `#gv-searchBtn` ("Search Map") and
   `#gv-saveInline` ("Save search") render with the `disabled` attribute and
   `aria-disabled="true"`, with no click handlers.
6. **Legacy shell preserved:** the production static condition sections
   (`Planet in house`, `Angle in sign`, `Aspect to angle`) and the production
   `#findBtn` are kept in the DOM and only **visually hidden** via JS
   (`hideLegacyShell()`, wrapped in try/catch). This is required because
   `buildPlanFromLegacyDom()`, `collectSavedInvestigationConditions()`, and the
   production ghost-strip `snapshotConditions()` all read those elements. Hiding
   (not removing) keeps the production engine, save, and ghost code intact.

### Production pieces kept authoritative (unchanged)
`executeSearchPlan`, `executeGenieRender`, `postSearchRegions`,
`renderHouseFeatures`, `renderAspectFeatures`, `buildPlanFromSavedConditions`,
`collectSavedInvestigationConditions`, `POST /saved-investigations/create`,
`__rmSaveCurrentInvestigation`, `#saveInvestigationNote` / `#saveInvestigationBtn`,
`auth_guard.js`, onboarding (`skipOnboarding` / `rm_map_onboarding_dismissed`).

---

## Files changed

| File | Change |
|------|--------|
| `map_CURRENT.html` | Inserted one scoped block after the `Location` panel section: `<style id="gv-builder-styles">` + `#gv-builder-host` markup (builder, chips, buildrow, dropdown host, add/search/save buttons, ghost + bottle shells) + one scoped `<script>` IIFE. ~+27 KB. No existing production HTML/JS removed; legacy condition sections + `#findBtn` hidden via JS. |

No other files changed. Backend, adapters, and smoke scripts untouched.

---

## Validation

Server: `uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8004`.
Harness: Playwright (auth redirect to `/auth.html` aborted so the page stays for
interaction; this is a test-only measure, not a product change). Builder logic
runs on `DOMContentLoaded` independent of auth.

Result artifact: `results/241_gv_builder_port_validation.json`

**34 / 34 checks PASS.**

Required proofs:

| Required | Check(s) | Result |
|----------|----------|--------|
| **Builder renders** | builder_renders, buildrow_dropdown_present, genie_hint_visible_empty, clear/add btn present, bottle + ghoststrip shells | PASS |
| **Variables can be added** | add_seq1_complete, chip_added_1, chip_label_has_Sun, ghost_token_added_1, badge_1, memory_count_1; add_seq2_complete, chip_added_2, memory_count_2; remove_chip_works; clear_all_works; ghost_mute_class_applied; redact_preview_class | PASS |
| **No JS errors** | no_gv_page_errors (zero builder-originated console/page errors) | PASS |
| **Production map still loads** | prod_executeSearchPlan_fn, prod_map_present, prod_genie_adapter_loaded, prod_save_fn_present, prod_saveNote_present, prod_findBtn_still_in_dom | PASS |
| **Search visible + disabled** | search_btn_visible_and_disabled | PASS |
| **Save visible + disabled** | save_btn_visible_and_disabled | PASS |
| **Legacy selects kept in DOM** | legacy_planetA / overlayPlanet / angleSign kept; legacy_findBtn_hidden_kept_in_dom | PASS |

Regression checks:

| Check | Result |
|-------|--------|
| `scripts/smoke_map_production_motion_a.py` | PASS 12/12 |
| `GET /map_CURRENT.html?skipOnboarding=1` | HTTP 200 |

### Pre-existing (not introduced by this port)
The only page error observed is the pre-existing
`[RMSettings] defaults not loaded` timing warning; console errors are the
pre-existing unauthenticated-harness artifacts (`/profiles` 401, favicon/library
404). None originate from the ported builder.

---

## Explicitly NOT done (per scope)

- No wiring of `#gv-searchBtn` to `executeGenieRender` / `executeSearchPlan`.
- No wiring of `#gv-saveInline` to `/saved-investigations/create`.
- No overlay generation, no `seededZones` / mock circles, no real overlays.
- No motion, no FLIP, no bottle/explore-mode animation.
- No removal of any production control (legacy shell hidden, not deleted).

These are the subjects of integration Stages 3–5 (see
`results/240_*` checkpoint and the integration plan).
