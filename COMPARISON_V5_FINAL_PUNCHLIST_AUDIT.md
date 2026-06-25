# Comparison V5 — Final Punch-List Audit

**Date:** 2026-06-25  
**Scope:** Canonical V5 compare (`#/compare` + `comparisonSetId`)  
**Mode:** Read-first audit + minimal safe fixes only

---

## Executive summary

| # | Item | Verdict | Notes |
|---|------|---------|-------|
| 1 | Add city persist | **PASS** (code + route) | `POST /comparison-sets/places`. Prior `405 Method Not Allowed` was stale server / missing route reload. |
| 2 | Replace city persist | **PASS** (code + route) | Same endpoint via `applyComparisonV5PlacePick`. |
| 3 | Diffs toggle visible | **PASS** (conditional) | Fades duplicate row values (`.rm-cmp-diff-duplicate`). Visible when ≥2 cities share a value in a row. |
| 4 | Dignities toggle visible | **PASS** (conditional) | Tints PIH cells `.dignity-supportive` / `.dignity-challenging` when ontology matches. |
| 5 | Hidden restore target | **PASS** | `.stub-restore` min 88×44px (V5-6B); removed conflicting compact rule (V5-7). |
| 6 | City reorder animation | **PASS** | `runComparisonV5CityReorderAnim` + `.cmp-city-reorder-anim` @ 280ms. |
| 7 | Second city centering | **FIXED** (V5-7) | Info `(i)` gutter no longer pulls name block left. |
| 8 | Add button placement | **PASS** (V5-6B) | No reserved empty slots; `+ Add` immediately after last city. |
| 9 | A2A pill offset | **PASS** (V5-6B) | `.angle-tabs { margin-left: 18px }`. |
| 10 | A2A data truth | **UNVERIFIED** | See §A2A below. Do not claim parity with Relocated. |
| 11 | Notes harmonization | **DEFERRED** | Popout/RTE unchanged. |
| 12 | Authority placement | **PASS** (token) | `padding: 28px 32px 16px`, `max-width: 1320px` aligned to Profile/Map H2/H3 tokens. Scroll morph still deferred. |

---

## 1–2. Add / Replace — diagnosis

| | |
|---|---|
| **Client request** | `POST /comparison-sets/places` |
| **Body** | `{ profile_id, comparison_set_id, place_ids }` |
| **Auth** | `Authorization: Bearer <supabase access_token>` |
| **Backend** | `@app.post("/comparison-sets/places")` → `update_comparison_set_places()` |
| **Legacy (deprecated)** | `POST /comparison-set/{id}/places` → `_deprecated_legacy_write` |

**Why users saw `405 Method Not Allowed`:** Client was wired before backend route existed, or uvicorn was not restarted after `main_centerline_FIXER.py` gained the owned endpoint. A live probe without auth returns **401/422**, not 405 — confirming route registration.

**Flow:** `cmp-add-place` / `cmp-replace-place` → overlay picker (`_cmpV5PlacePick`) → `applyComparisonV5PlacePick` → `persistComparisonSetPlaceIds` → `refreshComparisonV5Dom`.

**Browser QA (2026-06-25):** Automated Playwright timed out on test set load in shell; manual verification recommended on a known `comparisonSetId`.

---

## 3–4. Diffs / Dignities

### Diffs
- **Data:** `cmpDiffTdClass` in `app_shell.html`; passed to V5 adapter.
- **DOM:** `rm-cmp-diff-duplicate` on `val-col` when duplicate keys in row.
- **Toggle:** `refreshComparisonDiffSurfaces` → `ComparisonV5Route.hydrateCanonical`.
- **Tooltip (V5-7):** Fade duplicate values within each row across visible cities.

### Dignities
- **Data:** `pihDignityClass` + `/dignity_ontology.js`.
- **DOM:** `pih-house-cell dignity-*` on PIH cells.
- **Tooltip (V5-7):** Sign–house correspondence overlay.

Support exists; toggles are not fake-disabled.

---

## §A2A — truth audit (UNVERIFIED)

**Source:** `canonical_chart.aspects_to_angles[]` per city.

**V5:** `buildA2aContactIndex` → `formatA2aCellHtml` (abbr + orb).

**Relocated:** `formatA2aOrbCellHtml` / matrix — same array, different markup.

Index keys match legacy. No automated cross-surface parity test. **UNVERIFIED.**

---

## Hatch / texture separators

**Column hatch (`cmp-col-texture-a/b`):** Compare V5 only (`comparison_v5_adapter.js` + `comparison_v5_beta.css`).

**Profile/Relocated:** `texture-stripe` row banding (`tband_foundation.css`) — different mechanism.

**Map:** No comparison column hatch.

**Future token in CSS:** Do not transpose column hatch without design review.

---

## Validation

```bash
python3 scripts/smoke_h4x_v5_7_final_punchlist.py
python3 scripts/smoke_h4x_v5_6b_controls_reality.py
python3 scripts/smoke_h4x_v5_6_interactions_controls.py
python3 scripts/v5_smoke_js_syntax.py
```
