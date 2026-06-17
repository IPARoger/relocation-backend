# RESULT: 49_remove_local_store_fallback

Task: `49_remove_local_store_fallback`
Branch: `cursor/remove-local-store-fallback-35ef`
Result: **NOT VERIFIED** (smoke gates blocked — see validation)

## Files changed

| File | Change |
|------|--------|
| `app_shell.html` | Removed `GET /local-product-store.json` fallback from `loadViewModelFromStore()`; require `SupabaseStoreReady`; surface user-visible errors when bridge missing or fails (preserves `INTAKE_REQUIRED`); replaced `STORE_JSON_URL` with `STORE_LOAD_SOURCE`; updated load-pending/error copy |
| `main_centerline_FIXER.py` | `GET /local-product-store.json` now returns `_quarantine_legacy_read()` → HTTP 410 Gone |

## Validation evidence

### Grep — frontend callers (`*.js` / `*.html`, excluding `map_CURRENT.html`)

```text
$ rg 'local-product-store' --glob '*.html' --glob '*.js' | grep -v map_CURRENT
/workspace/supabase_store_bridge.js: * Does not replace /local-product-store.json — it is an alternative input.
```

- **Active caller count: 0** (one stale comment in `supabase_store_bridge.js` only; no `fetch` / runtime reference)
- `app_shell.html`: zero matches for `local-product-store`, `STORE_JSON_URL`, or `fetch(STORE`

### Static checks

- `python3 -m py_compile main_centerline_FIXER.py` → exit 0

### Smoke gates (required by task — not run to completion)

```text
$ python3 scripts/smoke_map_current.py
{"overall_pass": false, "error": "Server not reachable at http://127.0.0.1:8004/health"}
exit: 1

$ python3 scripts/smoke_saved_investigations.py
FAIL: Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
exit: 1
```

Blockers in this sandbox:

- No `.env.staging` / Supabase credentials in environment
- Committed `venv/bin/python` symlinks to macOS Homebrew (`/opt/homebrew/...`); server could not be started via project venv

Canonical read path (`supabase_store_bridge.js` → `SupabaseStoreReady` → `adaptStoreToView`) unchanged; only the local JSON fallback was removed.

## Rollback command

```bash
git revert HEAD
```

## Rejected scope

- Schema / database / migration changes
- Credentials or secrets
- Renderer / math / overlay changes
- `supabase_store_bridge.js` comment-only reference (not an active caller; left unchanged)
- `map_CURRENT.html` (explicitly excluded from caller audit)
- `scripts/smoke_app_shell_store_read.py` and other app-shell smokes that still assert `/local-product-store.json` (out of task file list; not updated)
- Quarantine of `/chart-records` or other routes still backed by `LOCAL_PRODUCT_STORE_SCAFFOLD`

## Behavior summary

1. **`loadViewModelFromStore()`** — uses `SupabaseStoreReady` when present; throws on bridge missing or failure; `INTAKE_REQUIRED` still routes to first-profile intake overlay (no mock fallback).
2. **`GET /local-product-store.json`** — 410 Gone via `_quarantine_legacy_read()`, matching `/account-store` and `/profile-library/{id}`.

**NOT VERIFIED**
