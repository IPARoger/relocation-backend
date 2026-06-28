# Settings V3 Charts Wiring Smoke

**Date:** 2026-06-29
**Scope:** Static wiring verification + simulated helper logic (Node.js)
**Result:** PASS (7/7 checks)

## Method

- Static analysis of `app_shell.html`, `map_CURRENT.html`, `settings_v3/settings_v3.js`, `main_centerline_FIXER.py`
- Simulated `getVisibleBodyNamesSet` / aspect visibility with representative settings payloads
- Simulated `pihHouseCellHtml` output for `near_cusp: true`
- No live browser session or authenticated save/reload (not required for this smoke pass)

## Results

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | Chart off / Tables on — hidden wheel & map, visible PIH | **PASS** | Static wiring confirmed in renderRelocatedWheelSvg, renderPihComparisonHtml, syncGenieBodySelectorsToSettings |
| 1-sim | Check 1 simulated (Mars chart off, tables on) | **PASS** | {'ok': True} |
| 2 | Chart on / Tables off — visible wheel & map, hidden PIH | **PASS** | Simulated Mars chart-on/table-off; renderComparisonTableHtml uses table context |
| 3 | Chart off / Tables on aspect — hidden wheel/map chart, visible aspect tables | **PASS** | Wheel P2P chart filter; A2A table filter; map chart aspect helper |
| 3-sim | Check 3 simulated (square chart off, tables on) | **PASS** |  |
| 4 | Late-in-house marker in Comparison PIH when near_cusp | **PASS** | pihHouseCellHtml renders ? marker; used by renderPihComparisonHtml and renderComparisonTableHtml |
| 5 | Unsupported bodies disabled, labeled, not persisted | **PASS** | settings_v3.js + collectSettingsV3ChartsPatch + refreshSettingsV3ChartsPanel |

## Check Details

### 1. Chart off / Tables on (planet)
- **Wheel:** `renderRelocatedWheelSvg` → `getVisibleBodyNamesSet("chart")`
- **Map selector:** `syncGenieBodySelectorsToSettings` → `__rmGetVisibleBodyNamesSet("chart")`
- **PIH tables:** `renderPihComparisonHtml` / `renderComparisonTableHtml` → `getVisibleBodyNamesSet("table")`

### 2. Chart on / Tables off (planet)
- Same split; simulation confirms Mars visible in chart Set only when `chart_planets` includes mars and `visible_planets` excludes it.

### 3. Chart off / Tables on (aspect)
- **Wheel/map chart:** `filterAspectsPlanetToPlanetRows(..., "chart")` + `__rmIsRmMajorAspectEnabled(id, "chart")`
- **Aspect tables:** `filterAspectsToAnglesRows(..., "table")`

### 4. Late-in-house in Comparison PIH
- `pihHouseCellHtml` now reads `info.near_cusp` and renders `?` marker (shared by comparison PIH renderers).

### 5. Unsupported body placeholders
- UI: disabled checkboxes + "· not in engine yet" copy in `settings_v3.js`
- Save: nodes stripped from `visible_bodies`; advanced bodies forced false in `helper_layers`

## Code change during smoke

One fix applied: `pihHouseCellHtml` gained `near_cusp` / `?` marker support for Comparison PIH (Check 4 was failing before fix).

## Ready to commit

All smoke checks passed. Awaiting commit instruction.
