# RESULT: 65_install-playwright-ci-2

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/65_install-playwright-ci-2.md  
**Branch:** `cursor/install-playwright-ci-2-b5aa`

## Files changed

| File | Change |
|------|--------|
| `tasks/62_install-playwright-ci.md` | Added CI installation findings, dual-stack inventory, recommended CI commands, and smoke-test notes (fulfills task 62 documentation requirement) |
| `results/65_install-playwright-ci-2.md` | Closeout report (this file) |

No schema, backend, CI workflow, `package.json`, or `requirements.txt` changes.

## Exact changes

- Installed Python Playwright from `requirements.txt` and Chromium browser binaries (`python3 -m playwright install chromium`).
- Installed Node Chromium binaries and Ubuntu system dependencies (`npx playwright install chromium`, `npx playwright install-deps chromium`).
- Validated headless browser launch for both Python and Node Playwright stacks.
- Ran `npx playwright test tests/smoke` — framework executed; both spec smokes skipped on missing Supabase env (not a Playwright failure).
- Documented CI install sequence and findings in `tasks/62_install-playwright-ci.md`.

## Validation evidence

### Python Playwright package install

```text
$ python3 -m pip install -r requirements.txt
Successfully installed greenlet-3.5.2 playwright-1.60.0 pyee-13.0.1
exit: 0
```

### Chromium browser binaries on disk

```text
$ ls ~/.cache/ms-playwright/
chromium-1223
chromium-1228
chromium_headless_shell-1223
chromium_headless_shell-1228
ffmpeg-1011
```

### Python browser launch

```text
$ python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('about:blank')
    browser.close()
    print('python-playwright: browser launched')
"
python-playwright: browser launched
exit: 0
```

### Node @playwright/test browser launch

```text
$ node -e "
const { chromium } = require('@playwright/test');
(async () => {
  const browser = await chromium.launch({ headless: true });
  await browser.close();
  console.log('node-playwright: browser launched');
})();
"
node-playwright: browser launched
exit: 0
```

### Playwright smoke specs execute (skipped on env, not Playwright)

```text
$ npx playwright test tests/smoke --reporter=line
Running 2 tests using 2 workers
  2 skipped
playwright test exit=0
```

Skip reason (expected): `mint_session.py` requires `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` which are not provisioned in this environment (credentials hard stop).

### System dependencies installed

```text
$ npx playwright install-deps chromium
# installs libgbm, xvfb, fonts, etc. on Ubuntu
exit: 0
```

## Rollback procedure

```bash
# Revert repo documentation changes
git checkout main -- tasks/62_install-playwright-ci.md results/65_install-playwright-ci-2.md

# Remove browser binaries from CI runner cache (no repo artifacts)
rm -rf ~/.cache/ms-playwright/

# Uninstall Python package (optional)
python3 -m pip uninstall -y playwright
```

## Rejected scope

- **Schema / backend / database / migration / renderer / math / overlay changes** — hard stops; not required.
- **Credentials / secrets** — Supabase staging env not provisioned; spec smokes skip at session mint; documented, not fixed.
- **CI workflow changes** (`.github/workflows/*.yml`) — not authorized in task 65 expected files.
- **`package.json` / `package-lock.json` changes** — `@playwright/test` not pinned; documented as follow-up; out of scope.
- **`requirements.txt` changes** — already contains `playwright` from task 51; no edit needed.
- **Full end-to-end map smoke pass** — requires backend on `8004` plus Supabase credentials; blocked by hard stops, not Playwright install.

## Remaining unknowns

- Whether a future CI workflow will use Python smokes (`scripts/smoke_*.py`), Node spec smokes (`tests/smoke/*.spec.js`), or both — both stacks are now documented.
- `@playwright/test` should be declared in `package.json` before CI relies on `node_modules` being pre-populated.
- `venv/bin/python` macOS symlink prevents `session.cjs` from minting sessions on Linux until venv is rebuilt.

## Result

**VERIFIED** — Playwright is installed correctly for CI: Python and Node stacks launch Chromium headless, system deps install cleanly, and `tests/smoke/*.spec.js` execute under Playwright (skipped only on missing Supabase env, not on framework failure).
