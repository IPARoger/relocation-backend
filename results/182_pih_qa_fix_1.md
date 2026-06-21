# PIH-QA-FIX-1 — Scoped PIH QA Selectors Closeout

**Date:** 2026-06-21  
**Commit:** (pending) — `PIH-QA-FIX-1: scope PIH QA selectors to canonical table`  
**Audit:** `results/181_pih_display_audit_1.md`

---

## Summary

Fixed false PIH mismatches in WHEEL-v2 QA caused by unscoped `table.simple tr` selectors. Product PIH/A2A/wheel rendering unchanged.

---

## What was wrong

WHEEL-v2 Playwright QA used:

```javascript
Array.from(root.querySelectorAll('table.simple tr'))
  .filter(tr => tr.querySelector('td')?.textContent === 'Sun')
```

Because A2A renders **before** PIH, Sun rows with ASC conjunction/opposition were read as “PIH house” (`Conjunction` / `Opposition`).

---

## Replacement

Scoped extractors in `scripts/smoke_comparison_sets.py`:

| Helper | Scope |
|--------|--------|
| `PIH_ROW_EXTRACT_JS` | `.rm-pih-table[data-pih-source="canonical_chart"]` |
| `A2A_ROWS_FOR_PLANET_JS` | `.rm-a2a-table[data-a2a-source="canonical_chart"]` |

Playwright cross-check: `wheel_v2_pih_crosscheck()` + `resolve_wheel_v2_qa_locations()`.

Static guards: `static_pih_qa_*` (3 checks).

---

## Corrected PIH cross-check results

| Location | Expected | Displayed (scoped PIH) | Result |
|----------|----------|------------------------|--------|
| Kansas City | 1 | 1 | **PASS** |
| Custom/NY | 12 | 12 | **PASS** |
| Moscow | 7 | 7 | **PASS** |

Contamination checks: PIH rows have **3 columns**; A2A Sun rows present separately where expected (NY: 2, Moscow: 1).

Machine-readable: `results/182_pih_qa_fix_1_data.json`

---

## WHEEL-v2 acceptance

**Stands ACCEPTED.** Checklist item 9 (Sun PIH) is **PASS** with corrected selector. No wheel/P2P/motion regression.

---

## Files changed

| File | Change |
|------|--------|
| `scripts/smoke_comparison_sets.py` | Scoped JS extractors, static checks, `wheel_v2_pih_crosscheck` in main Playwright path |
| `results/182_pih_qa_fix_1.md` | This closeout |
| `results/182_pih_qa_fix_1_data.json` | Cross-check output |

---

## Recommended next slice

**A2A-MOTION-1** — applying/separating/exact on aspect rows (backend-first).
