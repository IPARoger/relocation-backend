# Relocation Backend

## Playwright CI smoke tests

Automated end-to-end smoke tests live in `tests/smoke/` and run with [`@playwright/test`](https://playwright.dev/docs/test-intro). They validate the map page and saved-searches read route against a local staging backend on port **8004**.

### Prerequisites

- **Node.js 20+** and **npm**
- **Python 3.11+** with `venv` support
- Staging Supabase credentials (never commit these):
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY`
- Optional: `RM_SMOKE_EMAIL` (defaults to the staging smoke account)

### One-time local setup

```bash
# Node test runner + browsers
npm ci
npx playwright install chromium

# Python session helper + backend (creates venv/ used by tests/smoke/session.cjs)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install fastapi uvicorn supabase pydantic numpy scipy scikit-image pyswisseph python-dotenv
```

### Run smokes locally

```bash
# Terminal 1 — start backend with staging env
set -a && source .env.staging && set +a
source venv/bin/activate
export PORT=8004
uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8004

# Terminal 2 — run Playwright
set -a && source .env.staging && set +a
export BASE_URL=http://127.0.0.1:8004
export PLAYWRIGHT_BROWSERS_PATH="$PWD/.playwright-browsers"   # optional local cache
npm run test:smoke
```

Expected output when credentials and server are healthy (see `results/55_55smoke-map-saved-investigation.md`):

```text
Running 2 tests using 2 workers
  2 passed
```

If Supabase env vars are missing, both specs **skip** (exit 0) with a message from `mint_session.py`.

### CI (GitHub Actions)

Workflow: [`.github/workflows/playwright-smoke.yml`](.github/workflows/playwright-smoke.yml)

Triggers:

- `push` to `main` (when smoke-related paths change)
- `pull_request` targeting `main`
- Manual **workflow_dispatch**

The workflow:

1. Installs Node and Python dependencies
2. Downloads Chromium via `npx playwright install chromium --with-deps`
3. Creates a Python `venv/` and starts `uvicorn main_centerline_FIXER:app` on `:8004`
4. Runs `npm run test:smoke:ci` with `CI=true` (GitHub reporter + single worker)

#### Required GitHub Actions secrets

Configure these under **Settings → Secrets and variables → Actions**:

| Secret | Purpose |
|--------|---------|
| `SUPABASE_URL` | Staging project URL for session minting |
| `SUPABASE_ANON_KEY` | Anon key for `mint_session.py` |
| `SUPABASE_SERVICE_ROLE_KEY` | Service role for profile lookup |

Without these secrets, smoke tests skip in CI (runner still validates tooling).

#### CI configuration (`playwright.config.js`)

- `BASE_URL` defaults to `http://127.0.0.1:8004`
- `CI=true` enables: `forbidOnly`, 1 retry, single worker, GitHub + line reporters
- Tests directory: `tests/smoke/`

### Smoke specs

| Spec | Validates |
|------|-----------|
| `tests/smoke/map-page-smoke.spec.js` | Leaflet map, `/profiles`, `engine-birth`, no JS errors |
| `tests/smoke/saved-investigation-smoke.spec.js` | `GET /saved-searches/{profile_id}` returns JSON 200 or 404 |

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Could not mint Supabase session` | Export `SUPABASE_*` vars or add GitHub secrets |
| `venv/bin/python: No such file` | Run `python3 -m venv venv` and install Python deps |
| Browser not found | Run `npx playwright install chromium` |
| Connection refused on `:8004` | Start uvicorn before running tests |
| All tests skipped in CI | Add the three `SUPABASE_*` GitHub secrets |
