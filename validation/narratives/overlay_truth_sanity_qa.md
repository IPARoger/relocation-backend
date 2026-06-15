# Overlay truth sanity QA (manual + `?traceConditions`)

## Purpose

Validate that colored **house/angle-sign** regions, popups at overlap points, and the **active condition** UI tell a consistent story—especially when multiple house conditions, angle-in-sign, and aspect overlay are combined.

## Sidebar legend (normal vs debug)

- In **normal** use, the bottom **region color key** is **hidden** to reduce scroll pressure; condition **A/B/C** tints in the panel still match map colors.
- To show the compact key: add **`?debugGeometry`** or **`?showLegend`** to the map URL.

## Debug: condition trace

1. Open the map with query flag:  
   `map_CURRENT.html?traceConditions` (append to your file URL as needed).
2. Set **multiple planet-in-house** rows, optional **angle in sign**, optional **aspect to angle**.
3. Click **Find regions**.
4. In the browser devtools **Console**, each polygon feature logs one line:

   `[traceConditions] i … planet … house … condition_index … condition_type … angle … sign`

**How to read it**

- `condition_type === "house"` (or absent): usual house region; `condition_index` maps to condition A/B/C (0-based) and to the color cycle in the UI.
- `condition_type === "angle_sign"`: purple styling path; check `angle` and `sign` in the log.
- Aspect overlay lines/markers are **not** polygon house features; they come from a separate `search-regions` pass—use map popups / visual layer for those.

## Saturn / “wrong house” style reports

When QA suspects a planet is “not in the expected house”:

1. **Confirm data, not color:** Open a **right-click** popup at the suspect point and read the **planet/house table** from `/relocated-chart`. That is the chart truth for that coordinate.
2. **Match region to condition:** At the same point, use `traceConditions` to see which `condition_index` / `planet` / `house` the polygon under the cursor is supposed to represent (via debug geometry popup if `?debugGeometry` is enabled, or by temporarily toggling conditions off one at a time).
3. **Classify the finding**

| Observation | Likely cause |
|------------|----------------|
| Popup table matches one overlay but color “feels” wrong | **Color/overlap ambiguity** or translucent stacking |
| Popup table disagrees with expected house for that planet | **Logic bug** or wrong **active** condition payload (investigate backend + request body) |
| Table correct but layer lags after changing controls | **Stale UI/render** (rerender, check token/cancel path) |
| User relied on legend only, not popup | **User confusion** |

## Representative manual cases

- Baseline mid-latitude chart profile.
- High northern latitude (within ±65° cap).
- Southern hemisphere.
- **Multi-overlay overlap:** at least two house colors intersecting; click inside intersection, read city vs right-click parity.
- **Dateline-adjacent** pan (e.g. ±180°); confirm regions and popups still load.
- After aggressive panning, use the **○ reset** control (stacked with zoom) and confirm the map recenters without snapping fight.

This document does **not** change astrology or truth-grid math; it is a QA checklist only.
