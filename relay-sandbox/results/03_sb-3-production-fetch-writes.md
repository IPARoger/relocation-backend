# RESULT: 03_sb-3-production-fetch-writes

**Roadmap ID:** SB-3
**Author:** Cursor (execution half)
**Date:** 2026-06-18

## Objective

List POST/PATCH/PUT `fetch()` calls in `map_CURRENT.html` and `app_shell.html` (paths only).

## Summary

| File | Write fetches | POST | PATCH | PUT |
|------|-------------:|-----:|------:|----:|
| `app_shell.html` | 10 | 9 | 1 | 0 |
| `map_CURRENT.html` | 8 | 8 | 0 | 0 |
| **Total** | **18** | **17** | **1** | **0** |

**Classification rule:** A `fetch()` call is a write when its options object sets `method` to `POST`, `PATCH`, or `PUT`. Calls with no explicit `method` default to GET and are excluded.

## `app_shell.html` write fetches (10)

| Line | Method | Path |
|-----:|--------|------|
| 1356 | POST | `/comparison-sets/archive` |
| 2558 | POST | `/saved-investigations/rename` |
| 2605 | POST | `/saved-investigations/archive` |
| 2651 | POST | `/favorites/archive` |
| 2706 | POST | `/comparison-sets/create` |
| 2881 | POST | `/profiles/archive` |
| 3257 | PATCH | `/settings/account` |
| 3300 | POST | `/notes/chart-record` |
| 3341 | POST | `/notes/comparison-set` |
| 3386 | POST | `/profiles/rename` |

## `map_CURRENT.html` write fetches (8)

| Line | Method | Path |
|-----:|--------|------|
| 1648 | POST | `/saved-investigations/create` |
| 1681 | POST | `/notes/saved-investigation` |
| 2316 | POST | `/favorites/save` |
| 3651 | POST | `/aura-field` |
| 3664 | POST | `/aura-raster` |
| 3677 | POST | `/aura-raster-adaptive` |
| 4752 | POST | `/search-regions` |
| 5175 | POST | `/screen-pixel-truth` |

Note: `${API_BASE}/search-regions` at line 4752 resolves to `/search-regions` because `API_BASE` is `''` in this file.

## Unique write paths (18)

```
/comparison-sets/archive
/comparison-sets/create
/favorites/archive
/favorites/save
/notes/chart-record
/notes/comparison-set
/notes/saved-investigation
/profiles/archive
/profiles/rename
/saved-investigations/archive
/saved-investigations/create
/saved-investigations/rename
/settings/account
/aura-field
/aura-raster
/aura-raster-adaptive
/search-regions
/screen-pixel-truth
```

## Files changed

- `relay-sandbox/results/03_sb-3-production-fetch-writes.md` (this closeout only)
- No changes to `map_CURRENT.html`, `app_shell.html`, or any other source files.

## Validation evidence

```text
$ rg -n 'method\s*:' map_CURRENT.html app_shell.html
map_CURRENT.html:1649:            method: "POST",
map_CURRENT.html:1682:                    method:  "POST",
map_CURRENT.html:2317:            method: "POST",
map_CURRENT.html:3652:        method: "POST",
map_CURRENT.html:3665:        method: "POST",
map_CURRENT.html:3678:        method: "POST",
map_CURRENT.html:4753:        method: "POST",
map_CURRENT.html:5176:        method: "POST",
app_shell.html:1357:              method: "POST",
app_shell.html:2559:              method: "POST",
app_shell.html:2606:              method: "POST",
app_shell.html:2652:              method: "POST",
app_shell.html:2707:              method: "POST",
app_shell.html:2882:              method: "POST",
app_shell.html:3258:    method: "PATCH",
app_shell.html:3301:    method: "POST",
app_shell.html:3342:    method: "POST",
app_shell.html:3387:    method: "POST",

$ python3 fetch-write classifier (2026-06-18)
Total write fetches: 18
  app_shell.html: 10 (POST 9, PATCH 1, PUT 0)
  map_CURRENT.html: 8 (POST 8, PATCH 0, PUT 0)
```

All `fetch()` calls without an explicit `method` in both files were inspected; each defaults to GET and was excluded. No `PUT` write fetches found in either file.

## Rollback command

```bash
rm relay-sandbox/results/03_sb-3-production-fetch-writes.md
```

## Rejected scope

- Editing `map_CURRENT.html`, `app_shell.html`, or any backend routes (task scope: read-only inventory).
- Schema, database, secrets, migration, or renderer/math/overlay changes (not required; not attempted).
- Opening a PR (not requested).

## VERIFIED

Read-only inventory complete: **18** POST/PATCH/PUT `fetch()` calls across production UI files — **10** in `app_shell.html`, **8** in `map_CURRENT.html`; **17 POST**, **1 PATCH**, **0 PUT**.
