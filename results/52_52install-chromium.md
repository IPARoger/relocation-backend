# RESULT: 52_install-chromium

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/52_52install-chromium.md  
**Branch:** `cursor/install-chromium-746d`

## Files changed

| File | Change |
|------|--------|
| `results/52_52install-chromium.md` | Closeout report (this file) |

No application, schema, or dependency files were modified. Browser binaries were installed to the local Playwright cache only.

## Exact changes

- Ran `python3 -m pip install -r requirements.txt` to ensure the Playwright Python package was available (prerequisite from task 51).
- Ran `python3 -m playwright install chromium` to download Chromium, Chrome Headless Shell, and FFmpeg into `~/.cache/ms-playwright/`.
- Validated with a minimal headless Playwright script that launches Chromium, opens a page, and closes cleanly.

## Validation evidence

### requirements.txt inventory (read-only)

```text
$ cat requirements.txt
playwright
```

### Playwright Python package present

```text
$ python3 -m pip show playwright | head -3
Name: playwright
Version: 1.60.0
Summary: A high-level API to automate web browsers
exit: 0
```

### `playwright install chromium` succeeded

```text
$ python3 -m playwright install chromium
Downloading Chrome for Testing 148.0.7778.96 (playwright chromium v1223) ...
Chrome for Testing 148.0.7778.96 (playwright chromium v1223) downloaded to /home/ubuntu/.cache/ms-playwright/chromium-1223
Downloading FFmpeg (playwright ffmpeg v1011) ...
FFmpeg (playwright ffmpeg v1011) downloaded to /home/ubuntu/.cache/ms-playwright/ffmpeg-1011
Downloading Chrome Headless Shell 148.0.7778.96 (playwright chromium-headless-shell v1223) ...
Chrome Headless Shell 148.0.7778.96 (playwright chromium-headless-shell v1223) downloaded to /home/ubuntu/.cache/ms-playwright/chromium_headless_shell-1223
exit: 0
```

### Browser cache on disk

```text
$ ls /home/ubuntu/.cache/ms-playwright/
chromium-1223
chromium_headless_shell-1223
ffmpeg-1011
```

### Sample Playwright script opens a browser instance

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
# Remove downloaded browser binaries from local cache (no repo files to revert)
rm -rf ~/.cache/ms-playwright/chromium-1223 ~/.cache/ms-playwright/chromium_headless_shell-1223 ~/.cache/ms-playwright/ffmpeg-1011

# Reinstall later if needed
python3 -m playwright install chromium
```

## Rejected scope

- Schema, backend, database, credentials/secrets, migration, or renderer/math/overlay changes — hard stops; not required.
- Modifying `requirements.txt`, smoke scripts, or CI workflows — out of task scope (read-only inventory for requirements).
- Installing non-Chromium Playwright browsers (firefox, webkit) — not requested.

## Remaining unknowns

- Full smoke suite (`scripts/smoke_*.py`) was not executed; only a minimal launch/goto/close check was run per the validation plan.
- Browser binaries live in the user cache (`~/.cache/ms-playwright/`); other environments must run `playwright install chromium` independently.

## Result

**VERIFIED**
