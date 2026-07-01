# TASK: 62

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Documented (CI install validated in task 65)

## Objective

Install the Playwright testing framework for use in continuous integration (CI).

## Scope

- CI tools integration
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md

## Files expected to change

- NONE — read-only inventory (documentation added by task 65 closeout)

## Required behavior

1. Follow the instructions within `51_install-playwright.md` to set up Playwright for CI.
2. Document any findings or issues related to this installation process.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Confirmation that Playwright is successfully installed and ready for CI use, evidenced by the output from the installation script.

## Rollback plan

- If installation fails or is not needed, remove any temporary changes made during the installation process.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED

---

## CI installation findings (documented by task 65)

Task 65 validated Playwright for CI smoke testing. See `results/65_install-playwright-ci-2.md` for full evidence.

### Dual Playwright stacks in this repo

| Stack | Source | Used by |
|-------|--------|---------|
| Python `playwright` | `requirements.txt` (task 51) | `scripts/smoke_*.py` browser smokes, `tests/smoke/mint_session.py` |
| Node `@playwright/test` | `node_modules/@playwright/test` (v1.61.0 present; not yet declared in `package.json`) | `tests/smoke/*.spec.js`, `playwright.config.js` |

Both stacks require a separate browser-binary install step after the package install.

### Recommended CI install sequence (Ubuntu)

```bash
# 1. Python Playwright (from task 51)
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium

# 2. Node Playwright Test (for tests/smoke/*.spec.js)
npx playwright install chromium
npx playwright install-deps chromium   # system libs (libgbm, fonts, xvfb, etc.)

# 3. Optional: verify browser launch
python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(headless=True); b.close(); p.stop(); print('python ok')"
node -e "const {chromium}=require('@playwright/test');(async()=>{const b=await chromium.launch({headless:true});await b.close();console.log('node ok')})()"
```

### Smoke test execution

```bash
# Playwright spec smokes (tests/smoke/)
npx playwright test tests/smoke --reporter=line

# Python browser smokes (scripts/)
python3 scripts/smoke_map_current.py   # example; requires backend + Supabase env
```

`playwright.config.js` sets `testDir: './tests/smoke'`, `baseURL` default `http://127.0.0.1:8004`, headless mode.

### Findings

1. **Installation succeeds** — both Python and Node Playwright launch Chromium headless after the steps above.
2. **Browser binaries are not in the repo** — they download to `~/.cache/ms-playwright/`; each CI runner must run `playwright install chromium`.
3. **`tests/smoke/*.spec.js` execute but skip without Supabase env** — `mint_session.py` requires `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`. Playwright itself is ready; full smoke pass needs staging credentials (hard stop for this task).
4. **`@playwright/test` is not declared in `package.json`** — it exists in `node_modules` but CI should pin it (e.g. `npm install -D @playwright/test`) in a future task; out of scope for task 62/65.
5. **System deps** — `npx playwright install-deps chromium` installs required Ubuntu packages (gbm, xvfb, fonts). Needed on fresh CI runners.

### Issues not blocking Playwright install

- `.env.staging` absent in sandbox → spec smokes skip at session mint
- `venv/bin/python` is a macOS Homebrew symlink → `session.cjs` cannot mint sessions on Linux until venv is rebuilt
- Full map-page smoke needs backend on port 8004 plus Supabase credentials
