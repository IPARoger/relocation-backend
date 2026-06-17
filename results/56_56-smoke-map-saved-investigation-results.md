# RESULT: 56_smoke-map-saved-investigation-results

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/56_56-smoke-map-saved-investigation-results.md  
**Source reviewed:** results/55_55smoke-map-saved-investigation.md (Task 55 closeout; task spec referenced `relay/55_55smoke-map-saved-investigation.md`, but the artifact lives under `results/`)  
**Date:** 2026-06-17 UTC

## Summary verdict

**PASSED**

Task 55 executed two Playwright smoke specs against a restarted staging server on `127.0.0.1:8004`. All six tracked assertions and both Playwright tests passed (`exit: 0`). No assertion failures, timeouts, or unhandled JS errors were recorded.

## Playwright / Chromium execution

| Check | Status | Evidence |
|-------|--------|----------|
| `@playwright/test` runner | **OK** | `@playwright/test@1.61.0` via local `node_modules` |
| Chromium launch | **OK** | Google Chrome for Testing **148.0.7778.96** (`.playwright-browsers`) |
| Playwright test run | **OK** | `2 passed (11.5s)` — `exit: 0` |
| Setup errors | **None** | No setup or config errors logged in Task 55 |

Verbatim Playwright output from Task 55:

```text
Running 2 tests using 2 workers

[1/2] tests/smoke/map-page-smoke.spec.js:7:1 › map page smoke: leaflet, /profiles, engine-birth, no JS errors
[2/2] tests/smoke/saved-investigation-smoke.spec.js:7:1 › saved-searches read route returns JSON 200 or 404
  2 passed (11.5s)
exit: 0
```

**Pre-test server note (not a test failure):** Task 55 found the prior `:8004` listener hung (matching Task 54). The executor killed the stale process and restarted `uvicorn main_centerline_FIXER:app` with `.env.staging` before smokes; preflight then returned `200` `{"status":"ok"}`.

## Test matrix

| Route / page | Playwright spec / probe | Status | Evidence quote |
|--------------|-------------------------|--------|----------------|
| `/map_CURRENT.html?skipOnboarding=1` | `map-page-smoke.spec.js` | **PASS** | Leaflet map container (`#map` or `.leaflet-container`) present after navigation with injected Supabase session |
| `GET /profiles` | Map smoke + direct probe | **PASS** | Direct probe: `200`; Playwright network listener observed `/profiles` during map load |
| `GET /supabase/chart-records/<profile_id>/engine-birth` | Map smoke + direct probe | **PASS** | Direct probe: `200` (profile UUID from `mint_session.py`) |
| `GET /saved-searches/<profile_id>` | `saved-investigation-smoke.spec.js` + direct probe | **PASS** | Direct probe: `200`; Playwright validated full JSON body (array); status in allowed set `{200, 404}` |
| Saved-searches JSON shape | `saved-investigation-smoke.spec.js` | **PASS** | Playwright parsed response successfully |
| Map page JS errors | `map-page-smoke.spec.js` | **PASS** | Zero actionable console/page errors after load wait |

### Per-assertion summary (Task 55)

| Assertion | Status |
|-----------|--------|
| Leaflet map container | **PASS** |
| `GET /profiles` → 200 | **PASS** |
| `GET /supabase/chart-records/<uuid>/engine-birth` → 200 | **PASS** |
| `GET /saved-searches/<profile_id>` → 200 or 404 (not 5xx) | **PASS** (`200`) |
| Saved-searches response valid JSON | **PASS** |
| No unhandled JS errors on map page load | **PASS** |

### Explicitly untested (documented in Task 55, not failures)

| Item | Reason |
|------|--------|
| `GET /saved-searches/{profile_id}` **404** branch | Smoke account returned `200` with data; 404 is valid when empty but was not exercised |
| `saved-investigations/*` write/rename/archive | Out of scope; covered by `scripts/smoke_saved_investigations.py` |
| Quarantine legacy read routes | Task 54 scope; deferred |

## Failures

**None.** Task 55 recorded no failing assertions, no Playwright timeouts, and no unhandled JS errors on the map page.

## Root cause classification

No failures to classify. The only pre-run blocker (stale hung `:8004` process) was resolved by restart before Playwright executed; classification if it had blocked smokes would be **server not running**.

## Recommended next action

**No action needed** — map and saved-searches read smokes passed on staging `:8004`. Optional follow-up (not required for pass): exercise the `GET /saved-searches/{profile_id}` **404** branch with a profile known to have no saved searches if empty-state coverage is desired.

## Files changed

| File | Change |
|------|--------|
| `results/56_56-smoke-map-saved-investigation-results.md` | **NEW** — Task 56 closeout record (this file) |

No source files, test scripts, CI config, or Playwright config were modified by Task 56.

## Validation evidence

| Criterion | Met |
|-----------|-----|
| Task 55 result file read in full | Yes — `results/55_55smoke-map-saved-investigation.md` (7439 bytes, non-empty) |
| Single top-level verdict word | Yes — **PASSED** |
| Per-route test matrix present | Yes — six rows above |
| Verbatim error quotes for failures | N/A — no failures |
| Recommended next action section | Yes |
| No source files modified by Task 56 | Yes |

Cross-reference (read-only):

- Task 54 quarantine context: `results/54_54run-quarantine-smoke-tests.md` — quarantine routes out of scope for Task 55
- Task 50 quarantine route list: `results/50_smoke_quarantine_routes.md`

## Rollback command

```bash
git rm results/56_56-smoke-map-saved-investigation-results.md
```

## Rejected scope

Per Task 56 hard stops, the following were **not** attempted:

- Re-running Playwright or HTTP smokes
- Editing `.js`, `.py`, `.html`, `.ts`, CI, or Playwright config
- Schema, backend, database, migration, or renderer changes
- Creating or modifying files under `relay/` (Task 55 artifact was reviewed from `results/` per repo lane convention)

## Result

**VERIFIED** — closeout artifact exists; verdict **PASSED**; all Task 55 routes and assertions recorded with per-route status; no failures; recommended next action documented.
