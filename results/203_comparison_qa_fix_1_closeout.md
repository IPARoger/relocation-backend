# 203 — COMPARISON-QA-FIX-1 Closeout

**Date:** 2026-06-22  
**Type:** Audit + implementation  
**Scope:** Comparison display/state defects only (no layout redesign, no P2P, no scoring)

---

## Manual QA issues addressed

| Issue | Root cause | Fix |
|-------|------------|-----|
| Diffs too subtle / unclear | `opacity: 0.38` fade hard to notice | Stronger fade: `opacity: 0.28` on `.rm-cmp-diff-identical` |
| Diffs missing on AIS workbook | `renderAisComparisonHtml` had no diff context | Wired `cmpDiffTdClass` + reference column in AIS workbook |
| Angle tabs appear dead | Only filtered columns table; hid planet rows; ignored AIS/A2A | Tabs now filter angle rows in **columns**, **AIS**, and **A2A**; planet house rows stay visible |
| PIH placeholder section | Workspace PIH body was static bookmark copy | Renders live multi-column PIH table (same data as columns, with Diffs + Dignities) |
| A2A no motion visible | `formatA2aComparisonCellText` showed orb only | Appends factual suffix: `exact`, `A` (applying), `S` (separating) |
| "Saved place" / missing coords | Geonames picks not registered in `storeRaw.places` before build | `ensureComparisonPickPlace()` resolves coords via item or `GET /place/{id}`, registers in memory; hydrate fallback fetches place meta |

---

## Changes by area

### 1. Diffs
- Comparison **columns**: unchanged logic; fade strengthened
- **AIS workbook**: now applies cell-level diffs (reference = first visible column)
- **A2A workbook**: already had diffs; motion now visible in cell text
- **PIH workbook**: new table honors Diffs + Dignities together (no dignity-as-diff)

### 2. Dignities
- House-correspondence coloring unchanged; works in columns + new PIH workbook section
- Combined CSS `td.rm-cmp-diff-identical.pih-house-cell.dignity-*` preserved at new opacity

### 3. Angle tabs
- Documented in workspace UI: *"Filters ASC / MC / DSC / IC rows in comparison columns, AIS, and A2A sections. Planet house rows stay visible."*
- `cmpAngleTabMatchesRow()` + `data-cmp-angle-row` / `data-cmp-a2a-angle` attributes

### 4. Saved place / Ubud
- `registerPlaceInMemory()` + `ensureComparisonPickPlace()` on comparison search select (overlay + compare screen)
- `hydrateComparisonColumns()` fetches `/place/{id}` when coords missing from store
- Compare-build copies `data-place-name` into `viewModel.placeNameById`

### 5. PIH workspace section
- Option **A** implemented: renders same PIH comparison table as workbook (not removed; PIH essential)
- Note points users to Diffs/Dignities toggles on comparison-columns panel

---

## Validation

```bash
venv/bin/python3 scripts/smoke_diffs_mvp.py      # 11/11 PASS
venv/bin/python3 scripts/smoke_dignities_house.py # 15/15 PASS
```

New static checks:
- AIS workbook diffs
- Stronger fade opacity
- Angle tab AIS/A2A filter
- A2A motion display suffix
- PIH workbook live
- Diffs + dignities combined CSS
- Comparison pick place resolution

---

## Files changed

- `app_shell.html` — comparison display, angle tabs, PIH workbook, place registration, A2A motion text
- `scripts/smoke_diffs_mvp.py` — extended checks
- `scripts/smoke_dignities_house.py` — extended checks

---

## Not changed (per scope)

- No P2P comparison
- No scoring / interpretation / summary panels
- No comparison wheel
- No layout redesign
- City Intelligence / Notes sections unchanged

---

## Rollback

Revert single commit touching files above.
