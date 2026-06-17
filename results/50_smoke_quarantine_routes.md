# RESULT: 50_smoke_quarantine_routes

Task: `50_smoke_quarantine_routes`
Branch: `cursor/task-50-smoke-quarantine-routes`
Result: **PARTIALLY VERIFIED** (quarantine smokes pass; full gate smokes blocked by missing playwright)

## Files changed

| File | Change |
|------|--------|
| `scripts/smoke_account_store_read.py` | Expect HTTP 410 Gone on `/account-store` (auth + unauth); removed JWT/store-shape assertions |
| `scripts/smoke_app_shell_store_read.py` | Expect 410 on `/local-product-store.json`; shell asserts `SupabaseStoreReady` not local JSON URL; chart-records scaffold checks retained; browser hook optional when Supabase+playwright available |
| `scripts/smoke_app_shell_map_handoff.py` | `ensure_server()` probes `/app_shell.html` instead of quarantined store JSON |
| `scripts/smoke_app_shell_context_transport.py` | Same `ensure_server()` fix |

## Validation evidence

### Grep — no smoke still asserts 200 on quarantined routes

```text
$ rg 'account-store|local-product-store' scripts/smoke_*.py
# All references are 410 expectations, path constants, or negative shell-body checks
```

### Static checks

```text
$ python3 -m py_compile scripts/smoke_account_store_read.py scripts/smoke_app_shell_store_read.py \
    scripts/smoke_app_shell_map_handoff.py scripts/smoke_app_shell_context_transport.py
exit: 0
```

### Smoke runs

```text
$ python3 scripts/smoke_account_store_read.py
PASS: health_200, account_store_410, account_store_auth_410
exit: 0

$ python3 scripts/smoke_app_shell_store_read.py
PASS: app_shell_html_200, store_json_410_quarantine, chart_records_api_200, chart_records_three,
      map_current_200, rm_app_shell_zero_disables; shell_loads_store_view_model skipped (no playwright)
exit: 0

$ python3 scripts/smoke_map_current.py
FAIL: playwright not installed
exit: 1

$ python3 scripts/smoke_saved_investigations.py  (with .env.staging)
FAIL: ModuleNotFoundError: No module named 'playwright'
exit: 1
```

## Rollback command

```bash
git revert HEAD
```

## Rejected scope

- Product / backend route changes
- `app_shell.html` changes
- New profile-library smoke (no existing caller in `scripts/smoke_*.py`)

## Behavior summary

Legacy read routes `/account-store`, `/local-product-store.json` (and `/profile-library/*` per backend) return 410 with `{"error":"Gone","reason":"legacy read path retired"}`. Smokes that previously required 200 on those paths now assert quarantine or probe non-quarantined endpoints (`/app_shell.html`, `/chart-records`) for server readiness.

**PARTIALLY VERIFIED** — quarantine-focused smokes pass locally; `smoke_map_current` / `smoke_saved_investigations` still require playwright in this environment.
