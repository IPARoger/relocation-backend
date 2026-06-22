# COMPARISON-PROFILE-REALITY-FIX-1 Closeout

**Date:** 2026-06-22  
**Ticket:** COMPARISON-PROFILE-REALITY-FIX-1  
**Scope:** Comparison A2A matrix parity, Profile natal facts hydration, diffs wiring sanity

---

## Summary

Replaced sparse comparison A2A contact list with a fixed planet×angle matrix aligned to approved mockups. Expanded Profile `#/chart-record` hydration to render full natal facts (wheel, PIH, AIS, A2A) via existing `/relocated-chart` + `location_kind=natal`. Confirmed diffs classes on PIH/AIS/A2A comparison tables use per-row duplicate semantics without a reference city.

---

## Task A — A2A matrix parity

**Before:** `renderA2aComparisonHtml` built rows only for contacts that existed (sparse list).

**After:**
- Fixed matrix: rows = all visible PIH bodies + ASC/MC angle rows; columns = enabled angles (ASC/DSC/MC/IC) × visible comparison places.
- Empty cells render `—`.
- Populated cells show aspect label + orb + A/S/exact markers (`formatA2aMatrixCellHtml`).
- Row labels use `formatTablePlanetNameHtml` (℞ / station spacing preserved).
- Angle tabs filter matrix **columns** via `data-cmp-a2a-col-angle` (full matrix rendered; tabs hide/show columns).
- No P2P; no interpretation copy.

New helpers: `getA2aMatrixRowLabels`, `resolveA2aMatrixAngles`, `buildA2aContactIndex`, `formatA2aMatrixCellHtml`, `a2aMatrixCellDiffKey`.

---

## Task B — Profile natal facts

**Before:** Profile had wheel-only hydration in `#rm-profile-natal-wheel`.

**After:**
- Container `#rm-profile-natal-facts` hydrated by `hydrateProfileNatalFacts()`.
- `renderProfileNatalChartHtml()` reuses existing renderers:
  - Natal wheel (`renderRelocatedWheelHtml`)
  - PIH (`renderPihTableRowsFromCanonical`)
  - AIS (`renderAisSinglePlaceHtml`)
  - A2A (`renderA2aSinglePlaceHtml`)
- Same fetch path: engine-birth → birth-place coords → `fetchCanonicalRelocatedChart({ locationKind: "natal" })`.

Identity, notes, favorites, saved explorations, comparison sets, and launch buttons unchanged.

---

## Task C — Diffs minimum sanity

No visual redesign. Verified / preserved:
- `cmpDiffTdClass` + `cmpDiffRowFadeKeys` (count ≥ 2 duplicates per row) on PIH, AIS, and A2A matrix cells.
- Diffs never hide rows (opacity class on `<td>` only).
- No `rm-cmp-diff-identical` / reference-column privilege.
- A2A matrix diff keys include aspect + orb/motion via `a2aMatrixCellDiffKey`.

---

## Validation

```text
python3 scripts/smoke_comparison_a2a_matrix.py  → 10/10
python3 scripts/smoke_profile_natal_wheel.py     → 10/10
python3 scripts/smoke_rx_parity.py               → 13/13
python3 scripts/smoke_chart_page_state.py        → 7/7
```

New: `scripts/smoke_comparison_a2a_matrix.py`  
Updated: `scripts/smoke_profile_natal_wheel.py`, `scripts/smoke_rx_parity.py`

---

## Files touched

| File | Change |
|------|--------|
| `app_shell.html` | A2A matrix, profile natal facts, angle-tab column filter |
| `scripts/smoke_comparison_a2a_matrix.py` | New |
| `scripts/smoke_profile_natal_wheel.py` | Natal PIH/AIS/A2A checks |
| `scripts/smoke_rx_parity.py` | Matrix row-label motion check |
| `results/218_comparison_profile_reality_fix_1_closeout.md` | This doc |

---

## Follow-ups (not in scope)

- Diffs visual study (Variant G) — separate track
- Single-place relocated A2A matrix (profile/relocated still use list shape for one chart)
- Profile page layout polish / final design
