# WHEEL-v2 — Canonical P2P Spokes and Motion Markers Closeout

**Date:** 2026-06-21  
**Commit:** (pending) — `WHEEL-v2: add canonical P2P spokes and motion markers`  
**Depends on:** P2P-ASPECTS-1 (`5cc9dd7`), RETRO-MOTION-1 (`1dbfb09`), WHEEL-1

---

## Summary

The relocated chart wheel (Screen 4) now draws **planet-to-planet aspect spokes** and **retrograde/station markers** exclusively from `canonical_chart`. No client ephemeris, no aspect math, no layout redesign.

---

## Files changed

| File | Change |
|------|--------|
| `app_shell.html` | WHEEL-v2: P2P chord spokes, motion marker tspans, spoke color mapping |
| `scripts/smoke_comparison_sets.py` | Updated `static_wheel_*`, `static_p2p_*`, `static_motion_*` for v2 contract |

---

## Spoke mapping (canonical source)

**Data:** `canonical_chart.aspects_planet_to_planet[]` — server rows only.

**Render rules:**

- Chord between `body_a` and `body_b` longitudes from `canonical_chart.planets`
- Skip row if either body not in `getVisibleBodyNamesSet()` (display parity with rim glyphs)
- No orb / separation / aspect-angle math on client
- Settings (majors, minors, out-of-sign, orbs) already applied at Layer 2 compute

**Stroke colors (technical lines — no glow):**

| Family | Aspects | Color |
|--------|---------|-------|
| Major harmonious | `trine`, `sextile` | `#2563eb` (blue) |
| Major challenging | `conjunction`, `opposition`, `square` | `#dc2626` (red) |
| Minor | `quincunx`, `semisextile`, `semisquare`, `sesquiquadrate`, `quintile`, `biquintile`, `septile`, `novile` | `#16a34a` (green) |

**Line weight:** major `1.1px`, minor `0.9px` dashed (`3 3`).

**Radius:** inner chord at `0.20 × viewBox` (between core and house numbers).

---

## Motion marker rules

**Data:** `canonical_chart.planets.{body}.motion_state` (fallback: `retrograde` bool).

| `motion_state` | Wheel marker | Tooltip |
|----------------|--------------|---------|
| `direct` | (none) | — |
| `retrograde` | ℞ tspan, gray `#6b7280` | `· retrograde` |
| `station_direct` | `··` tspan, `#374151` | `· station direct` |
| `station_retrograde` | underlined ℞, `#111827` | `· station retrograde` |

No legend, animation, or forecasting. Station visually distinct from ordinary retrograde via `··` vs ℞.

---

## Canonical audit (geometry unchanged)

Wheel still reads only:

| Field | Use |
|-------|-----|
| `houses.cusps_deg` | House lines |
| `angles.*.longitude_deg` | Rotation + angle labels |
| `planets.*.longitude_deg` | Glyph placement + spoke endpoints |
| `planets.*.motion_state` | Motion markers |
| `aspects_planet_to_planet[]` | Spokes |

**Not used:** legacy `planet_houses`, `asc_deg`, client `swe`, aspect orb math.

---

## Validation results

| Check | Result |
|-------|--------|
| `static_wheel_reads_p2p_spokes` | **PASS** |
| `static_wheel_reads_motion_state` | **PASS** |
| `static_wheel_no_client_aspect_math` | **PASS** |
| `static_p2p_spokes_from_canonical` | **PASS** |
| `static_motion_wheel_reads_motion_state` | **PASS** |
| `static_motion_station_markers_in_wheel` | **PASS** |
| All 17 static wheel/p2p/motion checks | **PASS** |

---

## Known limitations

1. **Relocated wheel only** — no natal or comparison wheels.
2. **No applying/separating/exact** coloring on spokes.
3. **No nodes** on wheel.
4. **Visibility filter** on spokes matches rim glyphs; re-fetch required after settings save (SETTINGS-SOURCE-1 path).
5. **Simple SVG** — mockup paper texture / glow not ported (by design: no glow on spokes).

---

## Rollback scope

Revert WHEEL-v2 commit:

- Remove P2P chord loop, motion tspans, color constants from `app_shell.html`
- Restore WHEEL-1 placeholder meta line if desired
- Revert `static_*` checks in `smoke_comparison_sets.py`

No backend changes to revert.

---

*WHEEL-v2 complete for relocated primary wheel.*
