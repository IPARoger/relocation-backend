# C4-7 Dead Route Quarantine — Results

## 1. Caller Check

Command run:
```
grep -rn "account-store|profile-library|saved-searches|saved-search" \
  --include="*.js" --include="*.html" \
  --exclude-dir=node_modules --exclude-dir=.git \
  --exclude="*results*" --exclude="*tasks*" --exclude="*smoke*" .
```

Result: **NO_CALLERS_FOUND** — 0 active callers across all JS/HTML source files.

## 2. Routes Quarantined

All 4 routes are in `main_centerline_FIXER.py`:

| Route | Function | Line (post-edit) | Prior state |
|---|---|---|---|
| `GET /saved-searches/{profile_id}` | `api_list_saved_searches` | 2601 | Called `list_saved_searches(profile_id)` |
| `GET /saved-search/{saved_search_id}` | `api_get_saved_search` | 2606 | Called `get_saved_search(saved_search_id)` with 404 logic |
| `GET /profile-library/{profile_id}` | `api_profile_library` | 3039 | Called `_quarantine_legacy_read(...)` (410, without closeout note) |
| `GET /account-store` | `api_account_store` | 3048 | Called `_quarantine_legacy_read(...)` (410, without closeout note) |

Each handler body replaced with:
```python
return JSONResponse({"error": "Gone", "reason": "legacy read path retired — see C4-7 closeout"}, status_code=410)
```

Decorators and function signatures preserved exactly. No functions deleted.

## 3. Smoke Results

### smoke_map_current.py
```
{"overall_pass": true}
EXIT_CODE: 0
```

### smoke_saved_investigations.py
```
PASS: be_create
PASS: be_rename
PASS: be_archive
PASS: be_already_archived
PASS: be_invalid_profile_404
PASS: be_cross_account_404
PASS: be_unauth_401
PASS: fe_map_save
PASS: fe_map_save_note
PASS: fe_rename
PASS: fe_archive
PASS: fe_no_reload
PASS: fe_replay
PASS: fe_no_console_errors
PASS: smoke_saved_investigations
EXIT_CODE: 0
```

## 4. VERIFIED
