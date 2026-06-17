# RESULT: 64_install-playwright-ci

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/64_install-playwright-ci.md  
**Branch:** `cursor/install-playwright-ci-9235`

## Files changed

| File | Change |
|------|--------|
| `results/64_install-playwright-ci.md` | Closeout report (this file) |

No application, schema, or dependency files were modified. `requirements.txt` already contained `playwright` from task 51 (read-only inventory). Playwright Python package and Chromium browser binaries were installed to the local environment cache.

## Exact changes

- Reviewed `tasks/51_install-playwright.md` — dependency is the `playwright` Python package in `requirements.txt`.
- Reviewed `tasks/62_install-playwright-ci.md` — CI setup follows task 51; no additional repo file changes required.
- Ran `python3 -m pip install -r requirements.txt` to install Playwright 1.60.0 and its dependencies (`greenlet`, `pyee`).
- Ran `python3 -m playwright install chromium` to download Chromium, Chrome Headless Shell, and FFmpeg into `~/.cache/ms-playwright/`.
- Validated with import check and a minimal headless browser launch/goto/close script.

## Validation evidence

### requirements.txt includes Playwright (read-only inventory)

```text
$ grep -i playwright requirements.txt
playwright
```

### pip install succeeds

```text
$ python3 -m pip install -r requirements.txt
Collecting playwright (from -r requirements.txt (line 1))
  Downloading playwright-1.60.0-py3-none-manylinux1_x86_64.whl.metadata (3.5 kB)
...
Successfully installed greenlet-3.5.2 playwright-1.60.0 pyee-13.0.1
exit: 0
```

### Playwright Python package present

```text
$ python3 -m pip show playwright | head -3
Name: playwright
Version: 1.60.0
Summary: A high-level API to automate web browsers
```

### `playwright install chromium` succeeded

```text
$ python3 -m playwright install chromium
Chrome for Testing 148.0.7778.96 (playwright chromium v1223) downloaded to /home/ubuntu/.cache/ms-playwright/chromium-1223
FFmpeg (playwright ffmpeg v1011) downloaded to /home/ubuntu/.cache/ms-playwright/ffmpeg-1011
Chrome Headless Shell 148.0.7778.96 (playwright chromium-headless-shell v1223) downloaded to /home/ubuntu/.cache/ms-playwright/chromium_headless_shell-1223
exit: 0
```

### Browser cache on disk

```text
$ ls ~/.cache/ms-playwright/
chromium-1223
chromium_headless_shell-1223
ffmpeg-1011
```

### Import check

```text
$ python3 -c "from playwright.sync_api import sync_playwright; print('import ok')"
import ok
exit: 0
```

### Preliminary headless browser test

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

## Rollback procedure

```bash
# Uninstall Python package
python3 -m pip uninstall -y playwright greenlet pyee

# Remove downloaded browser binaries from local cache
rm -rf ~/.cache/ms-playwright/chromium-1223 ~/.cache/ms-playwright/chromium_headless_shell-1223 ~/.cache/ms-playwright/ffmpeg-1011

# Revert requirements.txt (only if playwright line was added in this task; it was not)
git checkout main -- requirements.txt
```

## Rejected scope

- Modifying `requirements.txt` — already contains `playwright` from task 51; no change needed.
- Schema, backend, database, credentials/secrets, migration, or renderer/math/overlay changes — hard stops; not required.
- CI workflow changes (`.github/workflows/`), `playwright.config.js`, or `README.md` updates — out of task scope (deferred to task 63).
- Running full smoke suite (`scripts/smoke_*.py`) — out of task scope; only preliminary launch/goto/close check performed.
- Installing non-Chromium Playwright browsers (firefox, webkit) — not requested.

## Remaining unknowns

- Browser binaries live in the user cache (`~/.cache/ms-playwright/`); other CI/relay environments must run `pip install -r requirements.txt` and `playwright install chromium` independently.
- GitHub Actions workflows do not yet include Playwright install steps; smoke execution in CI requires a future workflow task.

## Result

**VERIFIED**
