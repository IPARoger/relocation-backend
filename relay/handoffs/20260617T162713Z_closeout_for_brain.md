# Closeout ingested for next Claude/GPT plan

This replaces pasting Cursor output back into Claude by hand.
On the next `relay_robot.py` plan step, this file is included in the context pack.

## Source: results/55_55smoke-map-saved-investigation.md

# RESULT: 55_smoke-map-saved-investigation

**Overall verdict:** VERIFIED

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/55_55smoke-map-saved-investigation.md  
**Date/time of run:** 2026-06-17T16:26:37Z (Playwright run ~16:26:20Z)

## Files changed

| File | Change |
|------|--------|
| `results/55_55smoke-map-saved-investigation.md` | Closeout report (this file) |
| `tests/smoke/map-page-smoke.spec.js` | **Created** — Playwright map page smoke |
| `tests/smoke/saved-investigation-smoke.spec.js` | **Created** — Playwright saved-searches read smoke |
| `tests/smoke/mint_session.py` | **Created** — Supabase session + profile_id helper for smokes |
| `tests/smoke/session.cjs` | **Created** — Node wrapper calling `mint_session.py` |
| `playwright.config.js` | **Created** — minimal Playwright test config |
| `package.json` / `node_modules/@playwright/test` | **Created** — local `@playwright/test@1.61.0` runner (required by `npx playwright test`; no browser re-install) |

No application, schema, backend route, or production HTML/Python source files were modified.

## Step 1 — Smoke script audit

| Location | Finding |
|----------|---------|
| `tests/smoke/` (before task) | **Did not exist** — no Playwright JS smokes for map or saved-investigation |
| `scripts/smoke_map_current.py` | Exists (Python/Playwright); broader regression gate; failed in task 53 without dedicated map-route Playwright specs |
| `scripts/smoke_saved_investigations.py` | Exists (Python); covers `saved-investigations/*` CRUD + frontend, not `GET /saved-searches/{profile_id}` |
| Task 54 deferral | Quarantine-route smokes only (`/account-store`, `/local-product-store.json`, `/profile-library/*`); map + saved-searches explicitly out of scope |

## Server state

| Check | Result |
|-------|--------|
| Initial `:8004` listener | **Hung** — stale PID 45092; `GET /health` timed out (matches task 54 finding) |
| Operational action | Killed stale process; started fresh `uvicorn main_centerline_FIXER:app` with `.env.staging` sourced (not a source change) |
| Preflight before Playwright | `GET /health` → `200` `{"status":"ok"}` |
| Port | `127.0.0.1:8004` (staging only) |

## Environment (variable names only)

From `.env.staging` (values not logged):

- `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` — session minting via `mint_session.py`
- `RM_SMOKE_EMAIL` — optional; defaults to smoke user email in helper
- No dedicated `TEST_PROFILE_UUID` env var; profile UUID resolved at runtime from first active profile for smoke account

## Tooling versions

| Tool | Version |
|------|---------|
| `@playwright/test` (Node) | 1.61.0 |
| `playwright` (Python venv) | 1.60.0 |
| Chromium (`.playwright-browsers`) | Google Chrome for Testing **148.0.7778.96** (also downloaded headless-shell **149.0.7827.55** during first npx run) |

## Invocation

```bash
cd /Users/davegoodman/Desktop/relocation-backend
set -a && source .env.staging && set +a
export PLAYWRIGHT_BROWSERS_PATH="$PWD/.playwright-browsers"
export BASE_URL=http://127.0.0.1:8004
# ensure uvicorn listening on :8004
./node_modules/.bin/playwright test \
  tests/smoke/map-page-smoke.spec.js \
  tests/smoke/saved-investigation-smoke.spec.js \
  --reporter=line
```

Task-specified equivalent (after local `@playwright/test` install):

```bash
npx playwright test tests/smoke/map-page-smoke.spec.js tests/smoke/saved-investigation-smoke.spec.js --reporter=line
```

## Per-assertion table

| Assertion | Result | Notes |
|-----------|--------|-------|
| Leaflet map container (`#map` or `.leaflet-container`) | **PASS** | Present after navigation to `/map_CURRENT.html?skipOnboarding=1` with injected Supabase session |
| `GET /profiles` returns 200 | **PASS** | Direct probe: `200`; Playwright network listener observed `/profiles` during map load |
| `GET /supabase/chart-records/<uuid>/engine-birth` returns 200 | **PASS** | Profile UUID from `mint_session.py` (first active account profile); direct probe: `200` |
| `GET /saved-searches/<profile_id>` returns 200 or 404 (not 5xx) | **PASS** | Direct probe: `200`; Playwright spec validated full JSON body (array) |
| Saved-searches response valid JSON | **PASS** | Playwright parsed response successfully |
| No unhandled JS errors on map page load | **PASS** | Playwright spec: zero actionable console/page errors after load wait |

## Raw Playwright output

```text
Running 2 tests using 2 workers

[1/2] tests/smoke/map-page-smoke.spec.js:7:1 › map page smoke: leaflet, /profiles, engine-birth, no JS errors
[2/2] tests/smoke/saved-investigation-smoke.spec.js:7:1 › saved-searches read route returns JSON 200 or 404
  2 passed (11.5s)
exit: 0
```

## Direct HTTP probe evidence (post-restart server)

```text
GET /profiles -> 200
GET /supabase/chart-records/<profile_id>/engine-birth -> 200
GET /saved-searches/<profile_id> -> 200
curl http://127.0.0.1:8004/health -> {"status":"ok"}
```

## Map page console errors

None captured during passing Playwright run (actionable console/page error list empty).

## New smoke script files

- `tests/smoke/map-page-smoke.spec.js`
- `tests/smoke/saved-investigation-smoke.spec.js`
- `tests/smoke/mint_session.py`
- `tests/smoke/session.cjs`

## Remains untested (and why)

| Item | Reason |
|------|--------|
| `GET /saved-searches/{profile_id}` **404** path | Smoke account returned `200` with data; 404 branch not exercised (acceptable per task — 404 is valid when empty) |
| `saved-investigations/*` write/rename/archive routes | Out of scope; covered by existing Python `scripts/smoke_saved_investigations.py` |
| Map overlay / Find Regions / popup interactions | Out of scope; covered by `scripts/smoke_map_current.py` regression gate |
| Quarantine legacy read routes | Task 54 scope; deferred intentionally |
| Port **8000** endpoints | Blocked per FEATURE_STATUS_BOARD B-2 |
| `supabase_store_bridge.js` frontend saved-search UI | Documented as not wired; this task validated backend read route only |
| Auth flow UI (login page) | Smokes inject Supabase session via `localStorage` init script (same pattern as `scripts/smoke_map_current.py`) |

## Validation evidence

| Criterion | Met |
|-----------|-----|
| Closeout file exists | Yes |
| Map container PASS | Yes |
| `/profiles` 200 PASS or SKIP | PASS |
| `engine-birth` PASS or SKIP | PASS |
| Saved-searches 200/404 not 5xx | PASS (`200`) |
| No unhandled JS errors (or documented) | PASS (none) |

## Rollback command

```bash
rm -f results/55_55smoke-map-saved-investigation.md
rm -f playwright.config.js package.json package-lock.json
rm -rf tests/smoke node_modules
# Optional: remove downloaded headless-shell if undesired
# rm -rf .playwright-browsers/chromium_headless_shell-1228
```

## Rejected scope

Per task hard stops, the following were **not** attempted:

- Modifying `map_CURRENT.html`, `main_centerline_FIXER.py`, or any backend route/schema
- Running against production (staging `127.0.0.1:8004` only)
- Logging secret values from `.env.staging`
- Migrating or testing port 8000 endpoints
- Playwright/Chromium re-installation beyond local `@playwright/test` npm package needed to execute JS specs (browsers already present from tasks 51–52)

## Result

**VERIFIED** — closeout artifact exists; all required assertions **PASS**; Playwright smoke scripts created and executed successfully against a restarted staging server on `:8004`.
