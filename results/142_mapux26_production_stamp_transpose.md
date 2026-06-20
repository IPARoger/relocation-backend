# MAP-UX-2.6 — Production Stamp Transpose

**Date:** 2026-06-20  
**Slice:** MAP-UX-2.6  
**Files changed:** `map_CURRENT.html`  
**Shared rule source:** `validation/mockups/beta/identity_stamp.css`

---

## Goal

Transpose the corrected zone-b identity stamp positioning/style from `map_SANDBOX_genie_v7.html`
into production `map_CURRENT.html`, so the stamp aligns mathematically with the Profile and
Relocated pages — not with local map controls.

---

## Changes Made to `map_CURRENT.html`

### 1. Added shared CSS link

Placed immediately after the Leaflet CSS link.
`<link rel="stylesheet" href="validation/mockups/beta/identity_stamp.css" />`

### 2. Replaced nameplate CSS block

Old (MAP-UX-1 interim): `position: absolute; top: 12px; left: 12px` — hardcoded relative to map controls; flat card with background/border/shadow; `.rm-np-name-row` flex, `.rm-np-name` max-width 200px, monolithic meta line.

New (MAP-UX-2.6):
- `:root` block adds `--serif`, `--ink`, `--ink-soft`, `--ink-faint`, `--accent` tokens
- `.identity-stamp { position: fixed; z-index: 1000; border: none; }` — viewport-anchored
- Map-specific text treatments: `-webkit-text-stroke` + `text-shadow` for legibility over tiles
- `.rm-np-loading { opacity: 0.5 }` — loading state preserved

### 3. Replaced HTML element

New structure (zone-b, matches beta v14 Profile/Relocated):
- `id="rm-map-nameplate"` preserved
- `data-role="map-profile-selector"` preserved
- Classes: `identity-stamp authority-col-x authority-block-y rm-np-loading`
- Inner: `.zone-b > .zb-name > .nmwrap > .nm#rm-np-name` + `.tools > .zb-caret#rm-np-caret`
- Separate lines: `#rm-np-date` (zb-primary), `#rm-np-place` (zb-primary), `#rm-np-meta` (zb-meta)

### 4. Updated `renderNameplate()` JS

- Added `dateEl` / `placeEl` vars; added `setLine(el, txt)` helper
- Date line: `prof.date` + `prof.time24/time` if present
- Place line: `prof.place`
- Meta line: `prof.lat`, `prof.lon`, `prof.offset` if present
- Any missing field stays hidden — graceful degradation

---

## Preserved (untouched)

MAP-UX-2 history/pin controls, MAP-UX-3 save pill, onboarding/walkthrough, rendering engine,
overlay calculations, Genie logic, `window.__rmChartProfilesReady` wiring, all Leaflet logic.

---

## Mathematical Verification

Selenium getBoundingClientRect at 1280x900 viewport:

| Page | zone-b x | zone-b y | zone-b w |
|------|----------|----------|----------|
| profile_standard.html | 80 | 132 | 250 |
| relocated_standard.html | 80 | 132 | 250 |
| map_CURRENT.html | **80** | **132** | 250 |

Delta production vs profile: dx=0, dy=0.

Name text center vs column center (205px): profile=205.2px, production=205.1px, delta=0.03px.

Computed style: `position: fixed`, `left: 80px`, `top: 132px`.

### Derivation at 1280px viewport

Horizontal (authority-col-x):
  x = 0 + 28 + (1224 - 1120)/2 = 80px
  where 1120 = 250 + 10 + 600 + 10 + 250 (columns + gaps)

Vertical (authority-block-y):
  y = 62 + 10 + (560 - 440)/2 = 132px
  (header + chart-stage margin + wheel/stack centering offset)

---

## Smoke Results

| Check | Result |
|-------|--------|
| zone-b present in production DOM | PASS |
| data-role="map-profile-selector" preserved | PASS |
| position: fixed on nameplate | PASS |
| dx=0, dy=0 vs profile/relocated | PASS |
| smoke_map_current.py / smoke_onboarding | SKIPPED (playwright not installed; passed in prior sessions) |

---

## Notes

Production map has no CSS theme tokens. A minimal `:root` block added in `map_CURRENT.html`
satisfies identity_stamp.css dependencies without conflicting with existing panel styles.
`position: fixed` anchors stamp to viewport regardless of the 300px side panel width.
Genie translucency / ghost mode deferred — stamp anchor is stable for teaching overlays.
