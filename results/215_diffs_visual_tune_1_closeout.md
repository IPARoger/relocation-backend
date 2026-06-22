# DIFFS-VISUAL-TUNE-1 Closeout

**Date:** 2026-06-22  
**Goal:** Per-row duplicate fade without reference-column privilege; readable de-emphasis.

---

## Doctrine applied

| Rule | Implementation |
|------|----------------|
| Diffs do not hide cells | Opacity fade only — no `display:none`, rows always render |
| De-emphasize duplicates | `rm-cmp-diff-duplicate` at **opacity 0.48** + muted `#64748b` |
| No reference city | Removed `referencePlaceId` from `buildComparisonDiffContext` |
| Per-row semantics | `cmpDiffRowFadeKeys` — values appearing **≥2 times** in a row fade |
| Works with Dignities | Duplicate class on `pih-house-cell` including dignity variants |
| PIH / AIS / A2A | All comparison renderers use `rowKeys` + `cmpDiffTdClass(cellKey, rowKeys, diffsOn)` |

### Row semantics

| Row pattern | Result |
|-------------|--------|
| All unique | No cells faded |
| Some duplicated | Duplicated values faded; unique values normal |
| All identical | All cells faded |

---

## Changes

### `app_shell.html`

- Replaced `DIFFS-MVP-1` reference-column logic with `DIFFS-VISUAL-TUNE-1` per-row duplicate detection.
- New helpers: `cmpDiffRowFadeKeys`, updated `cmpDiffTdClass(cellKey, rowKeys, diffsOn)`.
- CSS: `.rm-cmp-diff-duplicate { opacity: 0.48; color: #64748b; }` (was 0.28 `.rm-cmp-diff-identical`).
- Updated: `renderComparisonAngleRowsHtml`, `renderAisComparisonHtml`, `renderPihComparisonHtml`, `renderA2aComparisonHtml`, `renderComparisonTableHtml`.

### `scripts/smoke_diffs_mvp.py`

- Python unit tests mirroring row fade logic (all unique / all identical / partial duplicate).
- Static checks: no `referencePlaceId`, opacity 0.42–0.55, duplicate class, dignity fade.

---

## Validation

```
python3 scripts/smoke_diffs_mvp.py
17/17 passed
```

---

## Files touched

- `app_shell.html`
- `scripts/smoke_diffs_mvp.py`
- `results/215_diffs_visual_tune_1_closeout.md`
