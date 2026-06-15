# map_CURRENT.html QA cleanup pass

**Date:** 2026-05-19  
**Scope:** Focused UX stabilization on `map_CURRENT.html` — no product redesign, no backend astrology math changes.

## Screenshot QA evidence (upload batch 2026-05-19)

| IDs | Issue | Evidence |
|-----|-------|----------|
| QA-01–05 | Map bounds / zoom / grey background / double-click zoom | Grey margin at max zoom reduced; double-click was inconsistent (zoom in/out, one-shot) |
| QA-06–09 | Dropdown highlight mismatch | ASC selected but DSC highlighted; house off-by-one (Saturn 6 → 7 highlight) |
| QA-10–13 | Popup layout imbalance | House column hugged planets; empty right margin |
| QA-14–18 | Wavy / bumpy aspect lines | Stepped centerlines vs earlier smooth curves |
| QA-19–22 | Jagged purple angle-sign polygons | Stair-step edges; uneven lat extent vs house overlays |
| QA-23–25 | Wording / spacing | “Angle” label too high in Aspect block; aspect group labels lowercase |
| QA-26+ | Max world view overlap | Slight L/R tile overlap at full zoom — acceptable interim |

## Blocking regression fix (2026-05-19 PM)

**Symptoms:** Dropdowns focused but never opened; map drag exposed persistent grey void; popup sometimes needed two clicks to dismiss; ASC line tail near Greenland.

| # | Root cause | Fix |
|---|------------|-----|
| 1 | `mousedown` + `preventDefault` on all panel `<select>` elements (added when removing `showPicker()`) **blocks native menu open** on Chrome/macOS — focus ring appears, no picker | **Removed mousedown handler entirely.** Kept wheel-scroll guard only. |
| 2 | `maxBoundsViscosity: 0.82` allowed partial overscroll; `bounceAtZoomLimits: false` + consolidated layout refresh dropped rAF double-`invalidateSize` so minZoom could compute before layout settled | **`maxBoundsViscosity: 1`**; restored rAF `invalidateMapSizeSoon`; added **`dragend` → `panInsideBounds`**; removed custom double-click handler (restored Leaflet default) |
| 3 | No explicit map click handler; focus/interaction state could consume first click | **`map.on('click', () => map.closePopup())`** |
| 4 | Per-point lat clamp on densified aspect **lines** created flat cap segments disjoint from clipped house polygons | **Removed lat clamp from line densification**; polygon clip at ±65° unchanged |

**Not changed:** Popup 3-column layout (acceptable). Aura/color tuning deferred.

## Root causes identified (prior pass)

### Double-click zoom (QA-01–05)

**Symptoms:** Double-click sometimes zoomed in, sometimes out; often stopped after first use.

**Root cause:** Leaflet’s built-in `DoubleClickZoom` handler interacted unpredictably with `maxBoundsViscosity`, fractional `zoomSnap`/`zoomDelta`, and repeated `invalidateSize()` + dynamic `minZoom` refresh on layout changes. The handler could appear to “reverse” when bounds viscosity corrected pan/zoom together, and subsequent clicks were dropped while zoom animation or bounds correction was in flight. Duplicate resize paths (`applyMapZoomLimits` + `invalidateMapSizeSoon`) added unnecessary layout churn.

**Fix:** Replace default handler with explicit deterministic zoom-in via `setZoomAround(latlng, getZoom() + zoomDelta)`; consolidate layout refresh into `onMapLayoutChange()`; set `bounceAtZoomLimits: false`. No timing hacks.

### Dropdown highlight mismatch (QA-06–09)

**Symptoms:** Visual highlight offset from actual selection (ASC → DSC, house 6 → 7).

**Root cause:** Prior pass added `mousedown` + `preventDefault` + **`showPicker()`** on all panel `<select>` elements. On Chrome/macOS, programmatic `showPicker()` opens a separate native menu whose hover/highlight index can desync from `selectedIndex` — classic off-by-one appearance while internal value stays correct.

**Fix:** Keep `mousedown` + `preventDefault` + `focus()` (prevents coordinate-based wrong option on first open); **remove `showPicker()` entirely**. Wheel guard unchanged.

### Line waviness (QA-14–18)

**Symptoms:** Aspect/angle centerlines looked stepped and “unstable.”

**Root cause:** Sparse backend sampling rendered directly; Leaflet default GeoJSON simplification during projection added visible segmentation between points.

**Fix (display-only):** Densify LineString coordinates in `prepareDisplayFeatureGeometry()` (~0.4° step), clamp to ±65° for display, render with `smoothFactor: 0`. Backend geometry unchanged.

### Purple polygon jaggedness / lat extent (QA-19–22)

**Symptoms:** Angle-sign fills had stair-step edges and extended visually past the ±65° product cap.

**Root cause:** Grid/contour truth for angle-sign regions (piecewise cells) plus no display clipping policy on polygon rings.

**Fix (display-only):** Clip all overlay coordinates to ±65° in display prep; one-pass Chaikin smooth on angle-sign exterior rings only. Validation integrity preserved — cosmetic display path.

### Popup layout (QA-10–13)

**Fix:** Three-column table — planet (left), house (center), invisible spacer (right) for balance without widening popup or adding scroll.

### Sidebar spacing / wording (QA-23–25)

**Fix:** Tighter `.field-single` label→select gap for Aspect “Angle” row; aspect group options Title Case: **All Major Aspects**, **All Hard Aspects**, **All Soft Aspects**.

### Trackpad / wheel (QA-01)

**Change:** `wheelPxPerZoomLevel` **320 → 270** (~16% faster feel); `wheelDebounceTime` unchanged at 100ms. Still restrained vs pre-patch overshoot.

### Map max-bounds overlap (QA-26+, document only)

Grey void collapse is fixed. Slight left/right tile overlap at max world view remains because map flex width includes sidebar proportion — **defer final correction to sidebar/layout redesign** so world fit uses true map viewport, not full window.

## Fixed in this pass

| Area | Change |
|------|--------|
| **Debug legend** | Panel multicolor legend only with `?debugGeometry` or `?showLegend`. |
| **Double-click zoom** | Deterministic always-zoom-in handler; consolidated layout/minZoom refresh. |
| **Map zoom** | Dynamic `minZoom`; `zoomSnap`/`zoomDelta` 0.25; wheel 270px/level; `bounceAtZoomLimits: false`. |
| **Popup** | 3-column planet table; ASC + MC only; no-scroll compact layout. |
| **Select dropdown** | Native open without `showPicker()` — highlight matches selection. |
| **Overlay display** | ±65° clip; line densification; angle-sign ring smooth (display-only). |
| **Labels** | Aspect group Title Case; Aspect “Angle” label spacing tightened. |
| **City search** | Exact name only on placeholder `cities.js`. |
| **Aura** | Prototype disabled; clean centerlines only. |

## Deferred / documented (not fixed)

| Item | Notes |
|------|--------|
| **Max world view sidebar overlap** | Interim acceptable; fix with layout redesign. |
| **Optional condition A** | First planet-in-house row still required for payload. |
| **Backend angle-sign resolution** | Display smooth helps; grid stair-steps may remain at high zoom until backend parity. |
| **Real city search** | Geocoder integration deferred. |

## Automated smoke (required before human QA)

```bash
# one-time
./venv/bin/pip install playwright && ./venv/bin/playwright install chromium

# each handoff (server running)
./venv/bin/python3 scripts/smoke_map_current.py
```

Report: `validation/reports/map_current_smoke.json`

**2026-05-19 run:** `overall_pass: true` (all 12 checks)

## Manual smoke checklist (run before commit)

- [ ] `map_CURRENT.html?bust=1` — no debug legend
- [ ] `?debugGeometry=1` — legend + debug status visible
- [ ] Double-click map repeatedly — **always zoom in**, no reversal, no one-shot failure
- [ ] Trackpad/wheel — slightly faster than prior patch, still controlled
- [ ] Reset ○ — default world view
- [ ] Planet/angle/house select — open highlight **matches current value** (no off-by-one)
- [ ] Aspect select — **All Major Aspects** / **All Hard Aspects** / **All Soft Aspects**
- [ ] Aspect block — “Angle” label spacing matches other fields
- [ ] City popup — 3-column balance, house centered, no scroll
- [ ] Aspect lines — smoother centerlines (display densification)
- [ ] Purple angle-sign — clipped to ±65°, softer edges (display-only)
- [ ] Max world view — note slight L/R overlap (known interim)

## Automated validation

```bash
python3 scripts/validate_sprint_dc_ic.py
```

**2026-05-19 run (post-fix):** `python3 scripts/validate_sprint_dc_ic.py` → **`overall_pass: true`**

## Backend / math

Unchanged. Display-layer clipping/densification/smoothing does not alter API payloads or validation geometry.
