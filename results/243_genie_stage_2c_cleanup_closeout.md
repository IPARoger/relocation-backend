# 243 — Genie Stage 2C Visual Cleanup Closeout

**Scope:** Stage 2B required fixes only. No truth execution touched.

## Selectors changed

| Selector / rule | Change |
|-----------------|--------|
| `#panel` | `width: 300px` → `304px` |
| `#gv-bottle`, `#gv-ghoststrip`, `#gv-bottleBadge`, `.gv-shells` | **Removed** from DOM |
| `.gv-shells`, `.gv-bottle`, `.gv-badge`, `.gv-ghoststrip`, `.gv-gtok*` | **Removed** from `#gv-builder-styles` |
| `#saveInvestigationBtn`, `#saveInvestigationNote` | **Hidden** via `display: none !important` (remain in DOM) |
| `#gv-saveInline`, `#rm-save-pill` | Unchanged, visible |
| `#rm-map-nameplate`, `.authority-col-x`, `.authority-block-y` | **Unchanged** |

## Builder JS (gv IIFE only)

- Removed `ghost` / `badge` from `els`
- Removed `renderGhost()`, `syncGhost()`, ghost `data-gv-mini` click branch
- `renderAll()` → `renderChips()` + `renderBuildRow()` only

## Not touched (forbidden)

`executeSearchPlan`, `executeGenieRender`, `buildPlanFromLegacyDom`, saved-investigation logic, `#rm-ghost-strip` / `#rm-bottle` production logic, backend, adapters.

## Validation (1440×900)

| Check | Before | After |
|-------|--------|-------|
| Nameplate top / left / width | 132 / 160 / 250 | 132 / 160 / 250 |
| `#gv-bottle` visible | true | removed (not in DOM) |
| `#saveInvestigationBtn` visible | true | false (in DOM) |
| `#gv-saveInline` visible | true | true |
| `#rm-save-pill` visible | true | true |
| `#panel` width | 300 | 304 |
| Builder add variable | — | PASS (1 chip) |
| `smoke_map_production_motion_a.py` | — | PASS 12/12 |

Screenshots: `results/243_genie_stage_2c_cleanup_screenshots/before_setup.png`, `after_setup.png`
