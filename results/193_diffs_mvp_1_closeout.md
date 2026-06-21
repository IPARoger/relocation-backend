# DIFFS-MVP-1 Closeout

**Date:** 2026-06-21  
**Scope:** Comparisons page cell-level Diffs readability mode (PIH, AIS, A2A). No summary panels, P2P, wheels, scoring, or AI.

---

## Summary

When **Diffs** is ON on the Comparisons page, identical cells across visible place columns fade (`opacity: 0.38`); differing cells stay fully readable. Rows remain present. Reference column = **first visible place** in workspace column order.

---

## Files changed

| File | Change |
|------|--------|
| `app_shell.html` | Diff helpers, CSS, toggle, PIH/AIS/A2A/columns cell classes |
| `scripts/smoke_comparison_sets.py` | `static_diffs_mvp_checks` (7) |
| `scripts/smoke_diffs_mvp.py` | Standalone static smoke (7) |

---

## Behavior

### Toggle

- **Label:** `Diffs` (checkbox in comparison columns table footer, beside Dignities)
- **Persisted:** `comparison_workspace_state.diffs_enabled` (existing key)
- **Default:** OFF

### Reference column

First place ID from `resolveVisibleOrderedPlaceIds(ws, placeIds)` — first visible column in saved order.

### Cell comparison keys

| Surface | Same → fade | Different → readable |
|---------|-------------|----------------------|
| **PIH** (columns table) | Same `planets.*.house` | Different house number |
| **AIS** (columns + workbook) | Same formatted angle (`sign` + degree in sign) | Different AIS display |
| **A2A** (workbook) | Same contact presence + `separation_deg` + `motion` + `out_of_sign` | Different orb, motion, or missing contact (`—`) |

### Explicit non-goals (honored)

- No P2P comparison tables or diff logic
- No summary / narrative panel
- No “improved”, “better/worse”, ranking, or AI text
- No comparison wheels
- No dignity diff logic in this slice

---

## Dignities doctrine note (future)

Product **“Dignities”** on Comparisons PIH cells today applies **house-correspondence / ontology styling** (supportive vs challenging families via `RMDignityOntology`) to the **house result cell** — not traditional sign essential dignity alone.

Because **houses change with relocation**, house-correspondence dignities **are relocation-relevant** when that doctrine is finalized.

This is **not** the same as “sign dignity changed across places” (sign is birth-invariant). Final wiring requires **DIGNITIES-HOUSE-DOCTRINE** before treating dignity styling as a relocation diff category.

**DIFFS-MVP-1 does not implement dignity diffs** — only the existing Dignities display toggle remains separate.

---

## Validation

| Script | Result |
|--------|--------|
| `python3 scripts/smoke_diffs_mvp.py` | **7/7 PASS** |
| `static_diffs_mvp_checks` in `smoke_comparison_sets.py` | **7/7 PASS** |

Checks prove: Diffs toggle exists, `rm-cmp-diff-identical` class wired, PIH/AIS/A2A diff keys, reference column logic, no P2P in diff block, no summary panel, no interpretive language in diff code block.

---

## Known limits

1. **Columns table only** has Diffs toggle; workbook AIS/A2A inherit state but no duplicate toggle.
2. **Near-cusp** not a separate diff key in PIH cells (house number only); near-cusp flag diff deferred.
3. **A2A display** still shows orb text only; motion affects fade comparison key, not cell label.
4. **Workbook PIH section** still placeholder — PIH diffs apply on columns table only.
5. **Reference column** not user-selectable — always first visible place.

---

## Rollback scope

Revert DIFFS-MVP-1 commit. Remove diff CSS/helpers/toggle; comparison tables render as before; `diffs_enabled` state key harmless if ignored.

---

## Commit

```
DIFFS-MVP-1: fade identical comparison cells
```
