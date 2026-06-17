# RESULT: 55_install-supabase-py

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/55_install-supabase-py.md  
**Branch:** `cursor/install-supabase-py-f310`

## Files changed

| File | Change |
|------|--------|
| `results/55_install-supabase-py.md` | Closeout report (this file) |

No application, schema, dependency manifest, or smoke-script files were modified.

## Exact changes

- Checked the system Python 3.12 environment for `supabase-py` (`pip` package name: `supabase`).
- Package was absent; installed it with `python3 -m pip install supabase` (user site-packages).
- Confirmed installation via `python3 -m pip show supabase`.
- Spot-checked `from supabase import create_client` from `/workspace` (repo contains a `supabase/migrations/` directory that previously shadowed imports per task 53); import succeeds after pip install.

## Validation evidence

### Pre-install check (package absent)

```text
$ python3 -m pip show supabase
WARNING: Package(s) not found: supabase

$ python3 --version
Python 3.12.3

$ which python3
/usr/bin/python3
```

### Install

```text
$ python3 -m pip install supabase
...
Successfully installed ... supabase-2.31.0 supabase-auth-2.31.0 supabase-functions-2.31.0 ...
exit: 0
```

### Post-install verification (required)

```text
$ python3 -m pip show supabase
Name: supabase
Version: 2.31.0
Summary: Supabase client for Python.
Location: /home/ubuntu/.local/lib/python3.12/site-packages
Requires: httpx, postgrest, realtime, storage3, supabase-auth, supabase-functions, yarl
Required-by:
exit: 0
```

### Import spot-check

```text
$ cd /workspace && python3 -c "from supabase import create_client; print('import OK:', create_client)"
import OK: <function create_client at 0x7f7c6e84b380>
exit: 0
```

## Rollback procedure

```bash
# Uninstall supabase-py if necessary.
pip uninstall -y supabase

# Remove this closeout file only (no repo application changes to revert).
git checkout main -- results/55_install-supabase-py.md && rm -f results/55_install-supabase-py.md
```

## Rejected scope

- **Schema / backend / database / migration / renderer / math / overlay changes** — hard stops; not authorized and not required for package installation.
- **Credentials / secrets** — `.env.staging` provisioning is out of scope; smoke tests requiring Supabase env vars were not run.
- **`requirements.txt` update** — task 55 scope is environment setup only; manifest pinning is deferred to task 54.
- **Fixing `venv/bin/python` macOS symlink** — would modify repo/environment layout; out of scope.
- **Running smoke tests or CI changes** — not authorized by this task.

## Remaining unknowns

- Whether `supabase-py` is installed in the project `venv` (broken macOS-origin symlink on Linux) vs. system/user Python used here (`/usr/bin/python3`).
- Supabase-dependent smokes still require staging credentials (`.env.staging` absent per task 53).

## Result

**VERIFIED** — `supabase-py` (pip name `supabase`) version 2.31.0 is installed in the active Python 3.12 environment and confirmed via `python3 -m pip show supabase`.
