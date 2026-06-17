# RESULT: 49_remove_local_store_fallback

**Author:** Cursor (results/ lane)
**Originating task:** tasks/49_remove_local_store_fallback.md

## Files changed

- `app_shell.html`
- `main_centerline_FIXER.py`

## Exact changes

- `loadViewModelFromStore()` — removed `fetch(STORE_JSON_URL)` fallback; requires `window.SupabaseStoreReady`. Preserves `INTAKE_REQUIRED` when bridge rejects with "Intake overlay required". Throws user-visible errors when bridge is missing or load fails.
- `STORE_JSON_URL` → `STORE_LOAD_SOURCE` (`"supabase"`); updated `loadSource`, loading/error UI copy, and `__rmAppShell` export.
- `serve_local_product_store_json()` — quarantined via `_quarantine_legacy_read("/local-product-store.json")` (410 Gone), matching `/account-store` and `/profile-library/{id}`.

## Validation evidence

**Grep — active frontend callers (js/html, excluding `map_CURRENT.html`):**

```bash
grep -rn "local-product-store\|STORE_JSON_URL" --include="*.js" --include="*.html" . | grep -v map_CURRENT.html | grep -v venv
```

Result: **0 active callers**. One comment-only hit in `supabase_store_bridge.js` (canonical bridge path unchanged).

**`app_shell.html` — no remaining fetch to local store:**

```bash
grep -n "fetch.*local-product\|STORE_JSON\|local-product-store" app_shell.html
# (no matches)
```

**Smoke tests (required by task — blocked in this environment):**

```bash
python3 scripts/smoke_map_current.py
# {"overall_pass": false, "error": "Server not reachable at http://127.0.0.1:8004/health"}
# exit 1

python3 scripts/smoke_saved_investigations.py
# FAIL: Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
# exit 1
```

Blockers: no `.env.staging` / Supabase credentials in cloud agent; repo `venv` is macOS Homebrew Python 3.11 (non-executable here); cannot start `main_centerline_FIXER` or run authenticated browser smokes without staging secrets.

**Static backend quarantine check (code review):** route handler now returns `_quarantine_legacy_read("/local-product-store.json")` — same pattern as quarantined `/account-store`.

## Rollback procedure

```bash
git revert HEAD
```

## Rejected scope

- `supabase_store_bridge.js` — not modified; canonical Supabase read path left intact (comment-only mention of legacy route).
- `/chart-records` and other scaffold-backed routes — still read `LOCAL_PRODUCT_STORE_SCAFFOLD`; task scoped only `/local-product-store.json` quarantine.
- `scripts/smoke_app_shell_store_read.py` and related app_shell smokes — still reference legacy URL; not in task validation plan.
- Schema, database writes, credentials, migrations, renderer/math/overlay changes — none attempted (hard stops).

## Remaining unknowns

- Live 410 response on `GET /local-product-store.json` not exercised in this environment (server could not be started).
- Required smokes (`smoke_map_current.py`, `smoke_saved_investigations.py`) not run to exit 0 — need staging env on a host with a working Python 3.11 venv.

## Result

NOT VERIFIED
