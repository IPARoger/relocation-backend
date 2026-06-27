# WEB2 Final QA Prep

**Date:** 2026-06-27  
**HEAD (pre-commit):** `035bdbeb` — `fix(shell): restore settings browser smoke initialization`  
**Prep commit:** *(see git log after `fix(web2): final qa prep cleanup`)*

---

## David — start here

| Item | Value |
|------|-------|
| **URL** | http://127.0.0.1:8004/app_shell.html |
| **Server** | `uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8004` (`.env.staging` present) |
| **Alt port** | http://127.0.0.1:8000/app_shell.html (also healthy) |
| **Health** | `GET /health` → 200 on both 8000 and 8004 |

Use **8004** for QA — it matches the smoke harness and staging-backed data.

---

## What changed (this prep)

| Change | File(s) | Why |
|--------|---------|-----|
| Serve `theme/family_resemblance.css` | `main_centerline_FIXER.py` | Was 404; shell references it |
| Restore `/local-product-store.json` quarantine → **410 Gone** | `main_centerline_FIXER.py` | Legacy read path must not silently 404 |
| Settings smoke helper opens Advanced `<details>` | `scripts/smoke_settings_details.py` (new) | Minor-aspects controls live in closed details |
| Browser smokes use helper + `state="attached"` | `smoke_settings_*.py`, `smoke_h6_*.py` | Fixes Playwright visibility timeout on hidden checkbox |

**Suggested commit:** `fix(web2): final qa prep cleanup`

---

## What was only verified (no code change)

| Surface | Status | Notes |
|---------|--------|-------|
| Shell init | OK | `__rmAppShell`, `viewModel()` load; no pageerror (035bdbeb) |
| Settings palette | OK | `/theme/appearance_palettes.js` → 200 |
| Settings static smokes | OK | S2–S5 all pass (89 checks) |
| Auth assets | OK | `/auth.html`, `/auth_guard.js` served; sign-in via shell |
| First profile intake | OK | `/first_profile_intake.js` → 200 |
| Profile / Chart / Compare route boot | OK | Playwright smokes reach beta roots, wheels, compare workspace |
| City Intelligence assets | OK | `city_intelligence_canonical.js/css` → 200 |
| Saved objects panels | OK | Profile lower panels (Favorites, Comparisons, Searches) render shells |
| Server ↔ working tree | OK | 8004 already serving uncommitted centerline fixes (410, family CSS 200) |

---

## Smoke results (this run)

| Script | Result | Detail |
|--------|--------|--------|
| `smoke_s2_astrology_settings.py` | **PASS** 25/25 | |
| `smoke_s3_dignities_settings.py` | **PASS** 13/13 | |
| `smoke_s4_appearance_settings.py` | **PASS** 22/22 | |
| `smoke_s5_glyph_settings.py` | **PASS** 29/29 | |
| `smoke_settings_account.py` | **PASS** | Minor-aspects persistence after details fix |
| `smoke_settings_navigation.py` | **FAIL** 24/28 | 3 product-expectation drifts (see below) |
| `smoke_h6_settings_slice1.py` | **FAIL** | Static spec checks (CI settings copy, house-edge doctrine) |
| `smoke_h6_3_settings_wire.py` | **FAIL** | Static spec checks (CI settings, house-edge H6.2) |

### Navigation smoke failures (not runtime blockers)

- `fe_a2d_defaults` — angle-to-dignity defaults differ from smoke expectations
- `fe_oos_disabled` — out-of-sign control not disabled as smoke expects
- `fe_oos_disclosed` — disclosure copy mismatch

These are **settings product/spec drift**, not shell-init or route failures.

### H6 static failures (deferred spec)

- `static_forbidden_city_intelligence_settings` — CI settings surface not in scope
- `static_house_edge_doctrine_copy` / `static_h6_2_house_edge` — house-edge copy not yet in shell

---

## Known blockers / stubs for David to QA manually

| Item | Severity | Notes |
|------|----------|-------|
| **Profile natal tband** — PIH / Notes / A2A cards | Medium | `hydrateProfileNatalFacts` loads wheel + tband via engine; verify cards appear for a real profile with birth coords. Mockups (`profile_standard.html`) show full tband; live shell may differ. |
| **City Intelligence comparison panel** | Stub | `renderComparisonCiWorkbookSectionBody()` returns placeholder: `wired: false` |
| **Notes canonical assets** | 404 | `/validation/mockups/beta/notes_canonical.js` not served; help canonical same |
| **Logout UI** | Missing | No sign-out control in shell (from prior QA audit) |
| **Comparison visual parity** | Deferred | V5 parity audits exist; not a runtime crash risk |

### Fixed in this prep

| Item | Before | After |
|------|--------|-------|
| `/local-product-store.json` | 404 | **410 Gone** (quarantine) |
| `/theme/family_resemblance.css` | 404 | **200** |
| Settings browser smokes (minor aspects) | Timeout on hidden `#rm-settings-minor-aspects` | Opens Advanced details; account smoke passes |

---

## Deferred (do not expand during QA)

- City Intelligence content engine + comparison panel wiring
- Profile tband card parity with mockups (PIH dignities toggle exists; full Notes/A2A cards TBD)
- Notes / Help canonical static routes
- Settings smoke updates for A2D defaults and out-of-sign disclosure copy
- H6 house-edge doctrine settings copy
- Web3 AI roadmap items (Layer 2 ontology is docs-only)

---

## Git state at prep time

- **Committed baseline:** `035bdbeb`, `c8c89472` (settings palette), shell init fixed
- **Dirty (intentional prep):** `main_centerline_FIXER.py`, smoke scripts, `scripts/smoke_settings_details.py`
- **Untracked artifacts:** prior `results/WEB2_QA_READY_REPORT.md`, glyph catalog, city intelligence migration — not part of this commit

---

## Quick manual QA checklist for David (~1 hr)

1. Open http://127.0.0.1:8004/app_shell.html — confirm no console errors on load
2. **Auth** — Google sign-in; confirm session persists across refresh
3. **First profile** — create or open default profile; birth data saves
4. **Map** — popup: Favorite, View chart, Pinwheel render
5. **Profile** — natal wheel + facts table; check for PIH / Notes / A2A tband cards
6. **Comparison** — workspace loads; note CI section is placeholder only
7. **Settings** — all subpages; Advanced → Minor Aspects opens
8. **Saved** — Favorites, Comparisons, Searches panels on profile
