# TASK: 49_remove_local_store_fallback

**Author:** relay (manual bootstrap after task 48)
**Model (suggested):** Auto
**Status:** Proposed

## Objective

Remove the `app_shell.html` fallback to `GET /local-product-store.json` and quarantine that route, completing the unfinished scope from task 46.

## Scope

- `app_shell.html` store load path only
- `main_centerline_FIXER.py` legacy read quarantine for `/local-product-store.json`
- Relay data rule: small reversible frontend + backend read-route change only

## Files to read

- `app_shell.html` — `loadViewModelFromStore()`, `STORE_JSON_URL`, bootstrap error handling
- `main_centerline_FIXER.py` — `_quarantine_legacy_read()`, existing quarantined routes
- `results/46_quarantine_dead_read_routes.md` — caller audit and partial closeout
- `supabase_store_bridge.js` — confirm canonical read path stays intact

## Files expected to change

- `app_shell.html`
- `main_centerline_FIXER.py`

## Required behavior

1. In `loadViewModelFromStore()`: when `SupabaseStoreReady` is available, keep using it. Preserve `INTAKE_REQUIRED` behavior (no mock fallback).
2. Remove the block that `fetch`es `STORE_JSON_URL` when Supabase payload is null. Instead surface a clear load error (user-visible) when Supabase bridge is missing or fails (except intake path).
3. Quarantine `GET /local-product-store.json` via `_quarantine_legacy_read()` (410 Gone), matching account-store and profile-library.
4. Grep for remaining frontend callers of `/local-product-store.json` in js/html (exclude `map_CURRENT.html`). Report count; active callers block quarantine.

## Hard stops (stop and ask — do not proceed)

- schema change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes
- Do not quarantine if an active frontend caller remains

## Validation plan

- `python scripts/smoke_map_current.py` → exit 0
- `python scripts/smoke_saved_investigations.py` → exit 0
- Grep proof: zero active `app_shell` / bridge callers still depend on local-product-store fallback

## Rollback plan

- `git revert HEAD`

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
