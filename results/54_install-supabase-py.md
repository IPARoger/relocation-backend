# RESULT: 54_install-supabase-py

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/54_install-supabase-py.md  
**Branch:** `cursor/install-supabase-py-c275`

## Files changed

| File | Change |
|------|--------|
| `requirements.txt` | Added `supabase` (PyPI package for `supabase-py`) alongside existing `playwright` |
| `results/54_install-supabase-py.md` | Closeout report (this file) |

## Exact changes

- Appended `supabase` to root `requirements.txt` so smoke-test environments install the official Supabase Python client via `pip install -r requirements.txt`.
- Recreated the local `venv/` on Linux (gitignored) because the checked-in macOS-origin symlink (`python3.11 -> /opt/homebrew/...`) was non-executable in this environment; then installed `requirements.txt` into that venv.

## Validation evidence

### requirements.txt includes supabase

```text
$ grep -i supabase requirements.txt
supabase
```

### pip install succeeds

```text
$ source venv/bin/activate && python3 -m pip install -r requirements.txt
...
Successfully installed ... supabase-2.31.0 ...
exit: 0
```

### Package version check (task-required command)

```text
$ source venv/bin/activate && python3 -m pip show supabase
Name: supabase
Version: 2.31.0
Summary: Supabase client for Python.
Home-page: https://github.com/supabase/supabase-py
Location: /workspace/venv/lib/python3.12/site-packages
exit: 0
```

### Import check (namespace not shadowed by repo `supabase/` dir)

```text
$ source venv/bin/activate && python3 -c "from supabase import create_client; print('create_client import ok')"
create_client import ok
exit: 0
```

### Existing dependency preserved

```text
$ source venv/bin/activate && python3 -m pip show playwright | head -2
Name: playwright
Version: 1.60.0
```

## Rollback procedure

```bash
pip uninstall -y supabase
# revert requirements.txt:
git checkout main -- requirements.txt
```

## Rejected scope

- **Schema / backend / database / migration / renderer / math / overlay changes** — hard stops; not authorized and not required for dependency install.
- **Credentials / secrets** — `.env.staging` is absent in this workspace; not read or modified (hard stop).
- **Smoke script changes, CI workflow changes, or running full Supabase-dependent smokes** — out of task scope; only dependency installation was authorized.
- **Committing `venv/`** — directory is gitignored; local venv was recreated for validation only.

## Remaining unknowns

- Supabase-dependent smoke scripts still require `.env.staging` credentials and a running backend; this task only adds the Python client package.
- Developers on macOS may need to recreate `venv/` locally if their existing venv symlink is stale; `pip install -r requirements.txt` is the canonical install path after merge.

## Result

**VERIFIED**
