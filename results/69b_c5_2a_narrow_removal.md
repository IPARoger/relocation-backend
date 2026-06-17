# C5-2a Narrow Dead Removal — Results

## 1. Final Caller Check

```
./main_centerline_FIXER.py:2063:    return _quarantine_legacy_read("/local-product-store.json")
```

Only the expected internal caller found (`serve_local_product_store_json` calling `_quarantine_legacy_read`).
No unexpected external callers. Proceeding with all 6 deletions.

## 2. Functions Deleted

| # | Function | Original Line | Notes |
|---|----------|--------------|-------|
| 1 | `serve_local_product_store_json` | 2061–2063 | route `/local-product-store.json`, 1 caller (internal: `_quarantine_legacy_read`) |
| 2 | `_quarantine_legacy_read` | 2391–2396 | helper, only called by #1 above |
| 3 | `api_list_saved_searches` | 2601–2603 | 410 stub, route `/saved-searches/{profile_id}` |
| 4 | `api_get_saved_search` | 2606–2608 | 410 stub, route `/saved-search/{saved_search_id}` |
| 5 | `api_profile_library` | 3039–3041 | 410 stub, route `/profile-library/{profile_id}` |
| 6 | `api_account_store` | 3048–3050 | 410 stub, route `/account-store` |

Each replaced with `# removed: <name> C5-2a`.

Protected functions untouched:
- `_deprecated_legacy_write` (24 active callers) — retained at line 2391
- `get_chart_profiles` (live) — retained at line 1890

## 3. Smoke Results

### smoke_map_current.py — EXIT 0
```
{"overall_pass": true, "report": "validation/reports/map_current_smoke.json", ...}
```

### smoke_saved_investigations.py — EXIT 0
```
PASS: be_create, be_rename, be_archive, be_already_archived, be_invalid_profile_404,
      be_cross_account_404, be_unauth_401, fe_map_save, fe_map_save_note, fe_rename,
      fe_archive, fe_no_reload, fe_replay, fe_no_console_errors
PASS: smoke_saved_investigations
```

### smoke_legacy_writes_deprecated.py — EXIT 0
```
Summary: 25/25 deprecated routes return 410
PASS: smoke_legacy_writes_deprecated
```

## 4. VERIFIED
