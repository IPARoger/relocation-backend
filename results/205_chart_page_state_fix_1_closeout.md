# CHART-PAGE-STATE-FIX-1 Closeout

**Date:** 2026-06-22  
**Goal:** Fix chart route state leaks without redesigning Screen 4.

---

## Problems fixed

| ID | Issue | Fix |
|----|-------|-----|
| CPS-1 | Primary nav to Chart preserved stale `placeId` | Primary nav now calls `navigate("chart", { placeId: null, … })` |
| CPS-2 | Profile switch on chart route kept old place | `switchChartRecord` + `selectProfile` clear `placeId` when `route === "chart"` |
| CPS-3 | Chart route without place could still hydrate | `screenChart` requires `explicitPlaceLaunch`; `hydrateRelocatedChart` bails without place context |

---

## Code changes (`app_shell.html`)

1. **Primary nav (Screen 4):** dedicated branch clears `placeId`, `explorationId`, `comparisonSetId` before entering chart route.
2. **Profile switch:** `switchChartRecord` / `selectProfile` null `placeId` on chart route; notice mentions relocated place cleared.
3. **`screenChart()`:** `explicitPlaceLaunch` gate (placeId, map coords in hash, or fresh handoff coords). Empty state directs users to map / favorites / comparison; clarifies this is not natal Chart Record.
4. **`hydrateRelocatedChart()`:** early return when no `navContext.placeId`, DOM `data-place-id`, or handoff/hash coords — prevents stale `/relocated-chart` fetch.
5. **`navigate()`:** clears `_screen4ChartCache` when chart navigation explicitly sets `placeId: null`.
6. **Copy:** nav label **4 Relocated Chart**; comparison column tooltips **Open Relocated Chart**; favorite button **View relocated chart**.

**Unchanged:** map `openChartFromMapButton`, favorite `data-nav="chart" data-place-id`, comparison `data-cmp-open` → chart with explicit `placeId`.

---

## Validation

`scripts/smoke_chart_page_state.py` — **7/7 PASS**:

- Primary nav Chart clears stale `placeId`
- Profile switch clears `placeId` on chart route (`switchChartRecord`, `selectProfile`)
- Chart without place does not fetch relocated chart (`hydrateRelocatedChart` guard)
- Map / favorite / comparison explicit place launch hooks preserved
- Relocated Chart copy present

Run: `python3 scripts/smoke_chart_page_state.py`

---

## Rollback

Revert `app_shell.html` and delete `scripts/smoke_chart_page_state.py`. No backend / migration changes.

---

## Files touched

- `app_shell.html`
- `scripts/smoke_chart_page_state.py` (new)
- `results/205_chart_page_state_fix_1_closeout.md` (this file)
