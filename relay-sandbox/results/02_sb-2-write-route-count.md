# RESULT: 02_sb-2-write-route-count

**Roadmap ID:** SB-2
**Author:** Cursor (execution half)
**Date:** 2026-06-18

## Objective

Count `@app.post/patch/put/delete` in `main_centerline_FIXER.py` — split live vs 410-deprecated.

## Summary

| Category | Count | POST | PATCH | PUT | DELETE |
|----------|------:|-----:|------:|----:|-------:|
| **Live** | **31** | 27 | 1 | 1 | 2 |
| **410-deprecated** | **26** | 18 | 7 | 0 | 1 |
| **Total** | **57** | 45 | 8 | 1 | 3 |

**Classification rule:** A write route is **410-deprecated** when its handler body calls `_deprecated_legacy_write(...)` or raises `HTTPException(status_code=410, detail={"error": "deprecated", ...})`. All other write routes are **live**.

## Live write routes (31)

| Line | Method | Route |
|-----:|--------|-------|
| 616 | POST | `/search-regions` |
| 944 | POST | `/aura-field` |
| 967 | POST | `/aura-raster` |
| 998 | POST | `/aura-raster-adaptive` |
| 1041 | POST | `/aura-raster-convergence` |
| 1094 | POST | `/classify-points` |
| 1180 | POST | `/brute-force-grid` |
| 1504 | POST | `/screen-pixel-truth` |
| 2225 | POST | `/library/charts` |
| 2257 | DELETE | `/library/charts/{chart_id}` |
| 2270 | POST | `/library/charts/{chart_id}/favorite` |
| 2291 | POST | `/library/active` |
| 2304 | POST | `/library/views` |
| 2333 | DELETE | `/library/views/{view_id}` |
| 2342 | PUT | `/library/settings` |
| 3101 | POST | `/current-location/set` |
| 3157 | POST | `/notes/chart-record` |
| 3177 | POST | `/notes/comparison-set` |
| 3204 | POST | `/notes/saved-investigation` |
| 3232 | PATCH | `/settings/account` |
| 3263 | POST | `/favorites/save` |
| 3288 | POST | `/favorites/archive` |
| 3339 | POST | `/comparison-sets/create` |
| 3364 | POST | `/comparison-sets/archive` |
| 3398 | POST | `/profiles/create-with-birth` |
| 3450 | POST | `/saved-investigations/create` |
| 3505 | POST | `/saved-investigations/rename` |
| 3533 | POST | `/saved-investigations/archive` |
| 3569 | POST | `/profiles/rename` |
| 3596 | POST | `/profiles/archive` |
| 3630 | POST | `/places/resolve-or-create` |

## 410-deprecated write routes (26)

| Line | Method | Route | Replacement (if any) |
|-----:|--------|-------|----------------------|
| 2409 | POST | `/profiles` | `/profiles/create-with-birth` |
| 2417 | PATCH | `/profiles/{profile_id}` | `/profiles/rename` |
| 2425 | POST | `/profiles/{profile_id}/archive` | `/profiles/archive` |
| 2482 | POST | `/birth-records` | `/profiles/create-with-birth` |
| 2490 | PATCH | `/birth-record/{record_id}` | *(none — not exposed)* |
| 2498 | POST | `/birth-record/{record_id}/archive` | *(none — not exposed)* |
| 2561 | POST | `/places` | `/places/resolve-or-create` |
| 2624 | POST | `/saved-searches` | `/saved-investigations/create` |
| 2632 | PATCH | `/saved-search/{saved_search_id}` | `/saved-investigations/rename` |
| 2640 | POST | `/saved-search/{saved_search_id}/archive` | `/saved-investigations/archive` |
| 2699 | POST | `/comparison-sets` | `/comparison-sets/create` |
| 2707 | PATCH | `/comparison-set/{comparison_set_id}` | *(none — not exposed)* |
| 2715 | POST | `/comparison-set/{comparison_set_id}/archive` | `/comparison-sets/archive` |
| 2731 | POST | `/comparison-set/{comparison_set_id}/places` | *(none — not exposed)* |
| 2739 | DELETE | `/comparison-set/{comparison_set_id}/places/{place_id}` | *(none — not exposed)* |
| 2795 | POST | `/favorite-places` | `/favorites/save` |
| 2803 | PATCH | `/favorite-place/{favorite_place_id}` | *(none — not exposed)* |
| 2811 | POST | `/favorite-place/{favorite_place_id}/archive` | `/favorites/archive` |
| 2856 | POST | `/visited-places` | *(none — not on JWT routes)* |
| 2915 | POST | `/notes` | scoped `/notes/*` routes |
| 2923 | PATCH | `/note/{note_id}` | scoped `/notes/*` routes |
| 2931 | POST | `/note/{note_id}/archive` | scoped `/notes/*` routes |
| 2970 | POST | `/user-settings` | `/settings/account` |
| 2978 | PATCH | `/user-settings/{settings_id}` | `/settings/account` |
| 3031 | POST | `/share-links` | *(none — not on JWT routes)* |
| 3039 | POST | `/share-link/{share_link_id}/revoke` | *(none — not on JWT routes)* |

## Files changed

- `relay-sandbox/results/02_sb-2-write-route-count.md` (this closeout only)
- No changes to `main_centerline_FIXER.py` or any other source files.

## Validation evidence

```text
$ rg -c '@app\.(post|patch|put|delete)' main_centerline_FIXER.py
57

$ python3 handler-body classifier (2026-06-18)
TOTAL 57
LIVE 31  {'POST': 27, 'PATCH': 1, 'PUT': 1, 'DELETE': 2}
410-DEPRECATED 26  {'POST': 18, 'PATCH': 7, 'PUT': 0, 'DELETE': 1}
```

Decorator scan (`rg -n '@app\.(post|patch|put|delete)' main_centerline_FIXER.py`) found 57 handlers. Each handler body was inspected for `_deprecated_legacy_write` or inline `HTTPException(status_code=410, detail={"error": "deprecated", ...})` (one case: `POST /places` at line 2561). No source files were modified.

## Rollback command

```bash
rm relay-sandbox/results/02_sb-2-write-route-count.md
```

## Rejected scope

- Editing `main_centerline_FIXER.py` or any backend routes (task scope: read-only count).
- Schema, database, secrets, migration, or renderer/math/overlay changes (not required; not attempted).
- Opening a PR (not requested).

## VERIFIED

Read-only inventory complete: **57** write routes in `main_centerline_FIXER.py` — **31 live**, **26** returning HTTP 410 via deprecated legacy-write stubs.
