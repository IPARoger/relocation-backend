# RX-PARITY-1 Closeout

**Date:** 2026-06-22  
**Ticket:** RX-PARITY-1  
**Scope:** Retrograde/station markers on PIH and A2A table surfaces

---

## Goal

Show `canonical_chart.planets.*.motion_state` consistently anywhere planet names appear in fact tables — matching wheel semantics without changing wheel code.

---

## Changes

### `app_shell.html`

Added table-only helpers (wheel block untouched):

| Helper | Role |
|--------|------|
| `resolvePlanetMotionState(entry)` | Reads `motion_state` with `retrograde` fallback (same rule as wheel) |
| `tablePlanetMotionMarkerHtml(motionState)` | ℞ · `··` · underlined ℞ for retrograde / station_direct / station_retrograde |
| `formatTablePlanetNameHtml(name, entry)` | Escaped planet label + motion marker |
| `planetEntryForMotionLookup(cols, name, refCol)` | Motion invariant across places — lookup from reference column |
| `formatA2aContactRowHtml(planet, aspect, angle, planets)` | A2A contact label with planet motion |

**Surfaces updated:**

1. **Screen 4 PIH** — `renderPihTableRowsFromCanonical` planet column
2. **Comparison workbook PIH** — `renderPihComparisonHtml` planet column
3. **Comparison columns** — `renderComparisonTableHtml` `{Planet} house` row labels
4. **Screen 4 A2A** — planet column in `renderA2aSinglePlaceHtml`
5. **Comparison A2A** — contact column via `formatA2aContactRowHtml` + `refPlanets`

**Not changed:** `wheelMotionMarkerTspans`, `renderRelocatedWheelSvg`, AIS tables (angles only).

### `scripts/smoke_rx_parity.py` (new)

- 10 static assertions on table wiring + wheel isolation
- Backend motion payload check when FastAPI available; skips gracefully otherwise

---

## Validation

```text
python3 scripts/smoke_rx_parity.py
11/11 passed (static; backend skipped when fastapi unavailable)
```

---

## Marker legend (tables)

| `motion_state` | Display |
|----------------|---------|
| `direct` | (none) |
| `retrograde` | ℞ |
| `station_direct` | ·· |
| `station_retrograde` | ℞ (underlined) |

Source: `canonical_chart.planets[name].motion_state` — no client speed math.

---

## Files touched

- `app_shell.html`
- `scripts/smoke_rx_parity.py`
- `results/213_rx_parity_1_closeout.md`
