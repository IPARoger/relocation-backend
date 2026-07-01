# RESULT: 63_install-playwright-ci

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/63_install-playwright-ci.md  
**Branch:** `cursor/install-playwright-ci-e16b`

## Files changed

| File | Change |
|------|--------|
| `.github/workflows/playwright-smoke.yml` | **Created** — GitHub Actions workflow for Playwright smoke CI |
| `README.md` | **Created** — local + CI instructions for Playwright smokes |
| `playwright.config.js` | **Updated** — CI reporters, retries, `forbidOnly`, single worker |
| `package.json` | **Updated** — `@playwright/test` devDependency + `test:smoke` / `test:smoke:ci` scripts |
| `package-lock.json` | **Updated** — lockfile for reproducible `npm ci` in CI |

## Exact changes

- Added `playwright-smoke` workflow: installs Node/Python deps, Chromium (`--with-deps`), creates `venv/`, starts `uvicorn` on `:8004`, runs `npm run test:smoke:ci`.
- Documented required GitHub secrets (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`) and local run steps in `README.md`.
- `playwright.config.js` now sets `reporter: [['github'], ['line']]`, `forbidOnly`, `retries: 1`, and `workers: 1` when `CI=true`.

## Validation evidence

### `npm ci` (reproducible CI install)

```text
$ npm ci
added 3 packages, and audited 4 packages in 710ms
found 0 vulnerabilities
exit: 0
```

### Playwright test discovery

```text
$ npx playwright test --list
Listing tests:
  map-page-smoke.spec.js:7:1 › map page smoke: leaflet, /profiles, engine-birth, no JS errors
  saved-investigation-smoke.spec.js:7:1 › saved-searches read route returns JSON 200 or 404
Total: 2 tests in 2 files
exit: 0
```

### CI-mode smoke run (`npm run test:smoke:ci`)

```text
$ CI=true npm run test:smoke:ci
Running 2 tests using 1 worker
[1/2] tests/smoke/map-page-smoke.spec.js:7:1 › map page smoke: ...
[2/2] tests/smoke/saved-investigation-smoke.spec.js:7:1 › saved-searches read route ...
::notice title=🎭 Playwright Run Summary::  2 skipped
  2 skipped
exit: 0
```

Skipped because `SUPABASE_*` env vars are absent (hard stop on credentials/secrets). `mint_session.py` error surfaced in skip reason:

```text
{"error": "Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY"}
```

### CI backend bootstrap simulation (venv + uvicorn)

```text
$ python3 -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt fastapi uvicorn supabase pydantic numpy scipy scikit-image pyswisseph python-dotenv
$ uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8004 &
$ curl -sf http://127.0.0.1:8004/health
{"status":"ok"}
exit: 0
```

With server running and fresh `venv/` (so `tests/smoke/session.cjs` resolves `venv/bin/python`), CI-mode Playwright again exits 0 with 2 skipped (no secrets).

### Prior smoke PASS reference (task 55, with staging credentials)

`results/55_55smoke-map-saved-investigation.md` documents `2 passed (11.5s)` against `:8004` when `.env.staging` is sourced. CI workflow wires the same env via GitHub secrets.

## Rollback procedure

```bash
git checkout main -- README.md playwright.config.js package.json package-lock.json
git rm -f .github/workflows/playwright-smoke.yml
git commit -m "revert: Playwright CI tooling (task 63)"
```

## Rejected scope

- **Credentials / secrets** — `.env.staging` not present; GitHub secrets not provisioned. Tests skip rather than pass; README documents required secret names only.
- **Schema, backend, database, migration, renderer / math / overlay changes** — hard stops; not required.
- **Smoke script changes** (`tests/smoke/*.js`, `mint_session.py`, `session.cjs`) — out of expected file list; existing scripts used as-is.
- **Modifying `requirements.txt`** — task 51 already added `playwright`; backend CI deps installed inline in workflow per validation simulation.

## Remaining unknowns

- First GitHub Actions run on `main` after merge has not been observed in this environment; workflow YAML follows repo conventions (`actions/checkout@v4`, `setup-node@v4`, `setup-python@v5`).
- Smoke specs will **skip** until the three `SUPABASE_*` GitHub Actions secrets are configured; after that, task 55 evidence indicates they should **pass**.

## Result

**VERIFIED** — Playwright CI tooling installed: workflow, config, npm scripts, and README in place; `npm ci` + `npm run test:smoke:ci` execute successfully in CI mode (exit 0). Smoke assertions skip without Supabase secrets (hard stop); configure secrets per README for full `2 passed` behavior documented in task 55.
