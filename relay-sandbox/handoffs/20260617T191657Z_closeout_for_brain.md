# Closeout ingested for next Claude/GPT plan

This replaces pasting Cursor output back into Claude by hand.
On the next `relay_robot.py` plan step, this file is included in the context pack.

## Source: relay-sandbox/results/03_sb-3-production-fetch-writes.md

# RESULT: 03_sb-3-production-fetch-writes

**Roadmap ID:** SB-3
**Author:** Cursor (execution half)
**Date:** 2026-06-18

## Objective

List POST/PATCH/PUT `fetch()` calls in `map_CURRENT.html` and `app_shell.html` (paths only).

## Summary

| File | POST | PATCH | PUT | Total write fetches |
|------|-----:|------:|----:|--------------------:|
| `map_CURRENT.html` | 8 | 0 | 0 | 8 |
| `app_shell.html` | 9 | 1 | 0 | 10 |
| **Combined** | **17** | **1** | **0** | **18** |

**Classification rule:** A `fetch()` is a write when its options object sets `method` to `POST`, `PATCH`, or `PUT`. Calls with no explicit `method` default to GET and are excluded.

## `map_CURRENT.html` write fetch paths (8)

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

Note: line 4752 uses `` `${API_BASE}/search-regions` ``; path listed without the base prefix.

## `app_shell.html` write fetch paths (10)

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

## Files changed

- `relay-sandbox/results/03_sb-3-production-fetch-writes.md` (this closeout only)
- No changes to `map_CURRENT.html`, `app_shell.html`, or any other source files.

## Validation evidence

```text
$ rg -n 'method.*(POST|PATCH|PUT)' map_CURRENT.html app_shell.html
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
(18 matches)

$ python3 fetch-block classifier (2026-06-18)
map_CURRENT.html: 8 write fetches (8 POST, 0 PATCH, 0 PUT)
app_shell.html: 10 write fetches (9 POST, 1 PATCH, 0 PUT)
TOTAL: 18
```

Each `fetch()` block was scanned for an explicit `method` option. All 18 write calls map one-to-one to the paths above. No PUT `fetch()` calls found in either file.

## Rollback command

```bash
rm relay-sandbox/results/03_sb-3-production-fetch-writes.md
```

## Rejected scope

- Editing `map_CURRENT.html` or `app_shell.html` (task scope: read-only inventory).
- Schema, database, secrets, migration, or renderer/math/overlay changes (not required; not attempted).
- Opening a PR (not requested).

## VERIFIED

Read-only inventory complete: **18** POST/PATCH/PUT `fetch()` calls across production UI — **8** in `map_CURRENT.html`, **10** in `app_shell.html` (17 POST, 1 PATCH, 0 PUT).
