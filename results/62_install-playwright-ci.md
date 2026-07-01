# RESULT: 62_install-playwright-ci

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/62_install-playwright-ci.md  
**Branch:** `cursor/install-playwright-ci-1d0d`

## Files changed

| File | Change |
|------|--------|
| `results/62_install-playwright-ci.md` | Closeout report (this file) |

No application, dependency, or CI workflow files were modified. Browser binaries were installed to the local Playwright cache only (`~/.cache/ms-playwright/`).

## Exact changes

- Read `tasks/51_install-playwright.md` and confirmed its prerequisite (`requirements.txt` contains `playwright`) is already satisfied from task 51.
- Executed the task-51 installation path on this Linux sandbox (CI-like `ubuntu-latest` environment):
  1. `python3 -m pip install -r requirements.txt`
  2. `python3 -m playwright install chromium` (Python stack)
  3. `npx playwright install --with-deps chromium` (Node/CI stack with OS dependencies)
- Validated import, browser launch, and test discovery.
- Inventoried `.github/workflows/` — no workflow currently installs or runs Playwright/smoke tests.

## Validation evidence

### Task 51 prerequisite (read-only)

```text
$ cat requirements.txt
playwright
```

### `pip install -r requirements.txt` succeeds

```text
$ python3 -m pip install -r requirements.txt
Installing collected packages: pyee, greenlet, playwright
Successfully installed greenlet-3.5.2 playwright-1.60.0 pyee-13.0.1
exit: 0
```

### Python Playwright import check

```text
$ python3 -c "from playwright.sync_api import sync_playwright; print('import ok')"
import ok
exit: 0
```

### `python3 -m playwright install chromium` succeeds

```text
$ python3 -m playwright install chromium
Chrome for Testing 148.0.7778.96 (playwright chromium v1223) downloaded to /home/ubuntu/.cache/ms-playwright/chromium-1223
FFmpeg (playwright ffmpeg v1011) downloaded to /home/ubuntu/.cache/ms-playwright/ffmpeg-1011
Chrome Headless Shell 148.0.7778.96 (playwright chromium-headless-shell v1223) downloaded to /home/ubuntu/.cache/ms-playwright/chromium_headless_shell-1223
exit: 0
```

### CI-style install with OS dependencies (`npx playwright install --with-deps chromium`)

```text
$ npx playwright install --with-deps chromium
Chrome for Testing 149.0.7827.55 (playwright chromium v1228) downloaded to /home/ubuntu/.cache/ms-playwright/chromium-1228
Chrome Headless Shell 149.0.7827.55 (playwright chromium-headless-shell v1228) downloaded to /home/ubuntu/.cache/ms-playwright/chromium_headless_shell-1228
exit: 0
```

(`--with-deps` installs Ubuntu system libraries required for headless Chromium in CI.)

### Browser cache on disk

```text
$ ls ~/.cache/ms-playwright/
chromium-1223
chromium-1228
chromium_headless_shell-1223
chromium_headless_shell-1228
ffmpeg-1011
```

### Minimal headless browser launch (Python)

```text
$ python3 << 'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("about:blank")
    title = page.title()
    browser.close()
    print(f"browser launched, page title={title!r}")
PY
browser launched, page title=''
exit: 0
```

### Node Playwright test runner discovers specs

```text
$ npx playwright --version
Version 1.61.0

$ npx playwright test --list
Listing tests:
  map-page-smoke.spec.js:7:1 › map page smoke: leaflet, /profiles, engine-birth, no JS errors
  saved-investigation-smoke.spec.js:7:1 › saved-searches read route returns JSON 200 or 404
Total: 2 tests in 2 files
exit: 0
```

### CI workflow inventory (read-only)

```text
$ ls .github/workflows/
cursor_trigger.yml
email_test.yml.disabled
relay_automerge.yml
relay_checkin.yml
relay.yml
telegram_test.yml
```

No workflow references `playwright`, `chromium`, or `smoke_*.py` / `playwright test`.

## Rollback procedure

```bash
# Revert closeout only (no repo dependency or workflow changes were made)
git checkout main -- results/62_install-playwright-ci.md && rm -f results/62_install-playwright-ci.md

# Remove browser binaries downloaded during validation (local cache only)
rm -rf ~/.cache/ms-playwright/chromium-1223 ~/.cache/ms-playwright/chromium-1228 \
       ~/.cache/ms-playwright/chromium_headless_shell-1223 ~/.cache/ms-playwright/chromium_headless_shell-1228 \
       ~/.cache/ms-playwright/ffmpeg-1011

# Uninstall Python package if desired
python3 -m pip uninstall -y playwright
```

## Rejected scope

- **CI workflow creation or edits** (`.github/workflows/*.yml`) — task declares `Files expected to change: NONE` and relay read-only rule; wiring Playwright into GitHub Actions requires a separate authorized task.
- **`package.json` / `package-lock.json` changes** — `@playwright/test` is present in `node_modules/` (v1.61.0) and used by `playwright.config.js` + `tests/smoke/*.spec.js`, but is not declared in `package.json` and there is no lockfile; fixing that is out of scope here.
- **Schema, backend, database, credentials/secrets, migration, or renderer/math/overlay changes** — hard stops; not required.
- **Running full smoke suites or starting the app server** — out of scope; only installation and discovery were validated.
- **Installing non-Chromium browsers** — not requested.

## Remaining unknowns

- **CI is not wired yet.** A future authorized task should add a workflow job along these lines on `ubuntu-latest`:
  ```yaml
  - uses: actions/setup-python@v5
    with:
      python-version: "3.11"
  - run: pip install -r requirements.txt
  - run: python3 -m playwright install --with-deps chromium
  ```
  For Node specs (`tests/smoke/*.spec.js`), also pin `@playwright/test` in `package.json` and run `npx playwright install --with-deps chromium` after `npm ci`.
- **Dual Playwright stacks:** Python smokes (`scripts/smoke_*.py`) use the `playwright` pip package (1.60.0); JS specs use `@playwright/test` from `node_modules` (1.61.0). Versions differ; CI should pin both explicitly.
- **Server and secrets:** Most smokes need a running backend (`uvicorn` on port 8004) and some need Supabase env (`.env.staging`); those are separate from Playwright installation.
- **Browser cache in CI:** GitHub Actions runners are ephemeral; each job must run `playwright install` (with `--with-deps` on Linux). Caching `~/.cache/ms-playwright` is optional optimization.

## Result

**VERIFIED**

Playwright installs cleanly on Linux via both the task-51 Python path and the CI-recommended `--with-deps` path. Browser launch and test discovery succeed. CI workflow integration itself was not performed (read-only inventory per task scope).
