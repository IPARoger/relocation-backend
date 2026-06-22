# PROFILE-RX-AS-VISIBILITY-FIX-1 Closeout

**Date:** 2026-06-22  
**Ticket:** PROFILE-RX-AS-VISIBILITY-FIX-1  
**Scope:** Rx table typography, A2A applying/separating/exact visibility, Profile natal wheel wiring

---

## Summary

Three focused fixes in `app_shell.html` — table typography only, A2A motion markers on relocated + comparison surfaces, and natal wheel hydration on `#/chart-record` using existing `/relocated-chart` with `location_kind=natal`. No backend or wheel renderer changes.

---

## Task A — Rx table polish

**Problem:** Retrograde markers (`Saturn℞`) ran flush against planet names.

**Fix:**
- Added `.rm-motion-rx`, `.rm-motion-station`, `.rm-motion-station-rx` CSS: `margin-left`, smaller superscript sizing, station dot spacing.
- Station markers get `title` tooltips.
- `formatTablePlanetNameHtml` unchanged in structure; markers remain HTML spans appended after escaped planet name.
- Wheel `wheelMotionMarkerTspans` untouched.

---

## Task B — A/S visibility

**Problem:** Relocated Chart A2A orb column showed separation only — no applying/separating/exact. Comparison had plain-text ` A` / ` S` suffixes that were easy to miss.

**Fix:**
- Replaced `formatA2aMotionSuffix` / `formatA2aComparisonCellText` with:
  - `formatA2aMotionMarkerHtml(row)` — compact superscript `A` (green), `S` (slate), `=` (blue exact)
  - `formatA2aOrbCellHtml(row)` — orb degrees + motion marker HTML
- Wired into `renderA2aSinglePlaceHtml` (Screen 4) and `renderA2aComparisonHtml` (comparison workbook).
- Comparison contact column still uses `formatA2aContactRowHtml` for planet ℞ markers.

---

## Task C — Profile natal wheel (PROFILE-NATAL-WHEEL-1)

**Problem:** `#/chart-record` had identity/notes/favorites/explorations but no natal wheel.

**Fix:**
- Added `#rm-profile-natal-wheel` panel to `screenChartRecord()` after Identity summary.
- Added `resolveBirthPlaceId()` + `hydrateProfileNatalWheel()`:
  - `GET /supabase/chart-records/{id}/engine-birth`
  - Birth place lat/lon via `resolvePlaceLatLon(birth_place_id)`
  - `fetchCanonicalRelocatedChart({ …, locationKind: "natal" })`
  - `renderRelocatedWheelHtml(canonical)` (existing WHEEL-1 renderer)
- Post-render calls `hydrateProfileNatalWheel(root)` alongside comparison sets hydration.
- Light outline cleanup on Profile route: user-facing section titles (Identity, Natal chart, Notes, Favorites, Saved explorations, Comparison sets); removed `stateDebugBlock()` and must-not dev box from this screen only.

---

## Validation

```text
python3 scripts/smoke_rx_parity.py          → 13/13 passed (backend skipped — no fastapi in default env)
python3 scripts/smoke_profile_natal_wheel.py → 6/6 passed
python3 scripts/smoke_chart_page_state.py  → 7/7 passed
python3 scripts/smoke_a2a_motion.py        → skipped (fastapi unavailable in default python3)
```

New smoke: `scripts/smoke_profile_natal_wheel.py` — static contract for natal wheel container, hydration, `location_kind=natal`, post-render wiring.

Updated: `scripts/smoke_rx_parity.py` — motion CSS + A2A marker helpers; fixed comparison contact check (`motionPlanets`).

---

## Files touched

| File | Change |
|------|--------|
| `app_shell.html` | Rx CSS, A2A motion markers, natal wheel panel + hydration, Profile labels |
| `scripts/smoke_rx_parity.py` | Extended static checks |
| `scripts/smoke_profile_natal_wheel.py` | New |
| `results/217_profile_rx_as_visibility_fix_1_closeout.md` | This doc |

---

## Not in scope

- Profile page visual redesign
- AIS table motion (angles only — unchanged)
- New endpoints or wheel SVG changes
- `smoke_a2a_motion.py` backend run (requires venv/fastapi)
