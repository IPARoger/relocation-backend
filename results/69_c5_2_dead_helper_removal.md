# C5-2 Dead Helper Removal — Results

**Date:** 2026-06-18  
**Roadmap ID:** C5-2  
**Status:** NOT VERIFIED — HARD STOP triggered on caller checks

---

## 1. Caller Check Output

### `_quarantine_legacy_read`

```
./main_centerline_FIXER.py:2063:    return _quarantine_legacy_read("/local-product-store.json")
./main_centerline_FIXER.py:2391:def _quarantine_legacy_read(route: str) -> JSONResponse:   <- definition
```

**Finding:** 1 external caller (`serve_local_product_store_json`, line 2062). This corresponds to the task's `get_local_product_store` stub target. Caller is within a candidate stub; if that stub were also deleted, the helper would reach 0 callers.

---

### `_deprecated_legacy_write`

**24 callers** found across `main_centerline_FIXER.py` (outside its definition at line 2398):

| Line | Enclosing Function |
|------|-------------------|
| 2411 | api_create_profile |
| 2419 | api_update_profile |
| 2427 | api_archive_profile |
| 2484 | api_create_birth_record |
| 2492 | api_update_birth_record |
| 2500 | api_archive_birth_record |
| 2613 | api_create_saved_search |
| 2621 | api_update_saved_search |
| 2629 | api_archive_saved_search |
| 2688 | api_create_comparison_set |
| 2696 | api_update_comparison_set |
| 2704 | api_archive_comparison_set |
| 2720 | api_add_place_to_comparison_set |
| 2728 | api_remove_place_from_comparison_set |
| 2784 | api_create_favorite_place |
| 2792 | api_update_favorite_place |
| 2800 | api_archive_favorite_place |
| 2845 | api_create_visited_place |
| 2904 | api_create_note |
| 2912 | api_update_note |
| 2920 | api_archive_note |
| 2959 | api_create_user_settings |
| 2967 | api_update_user_settings |
| 3020 | api_create_share_link |
| 3028 | api_revoke_share_link |

**HARD STOP:** Task assumed 0 callers outside the 6 stubs. Actual count: 24 callers across active 410 shim routes. These callers are NOT being deleted. `_deprecated_legacy_write` cannot be removed.

---

### 410 Stub External Caller Check (step 2 grep)

```
grep -rn "get_account_store|get_profile_library|get_saved_searches|get_saved_search|get_local_product_store|get_chart_profiles" ... | grep -v "def |410|Gone"
-> Exit code 1 (0 external callers found for the stubs themselves)
```

The stubs have no external callers.

---

## 2. Additional Discrepancies Found

### `get_chart_profiles` is a LIVE route — not a 410 stub

Task listed `get_chart_profiles` as one of the 6 quarantined 410 stubs. Actual code:

```
Line 1889-1892 of main_centerline_FIXER.py:
@app.get("/chart-profiles")
def get_chart_profiles():
    return load_chart_profiles()   <- LIVE, serves real data
```

HARD STOP: "Do not touch any live route." This function is live and must not be deleted.

### Scope mismatch on `_deprecated_legacy_write`

Task assumed `_deprecated_legacy_write` was used by only 6 stubs. It is actually a shared helper for 24 active 410 deprecation shims covering: profiles, birth records, saved searches, comparison sets, favorite places, visited places, notes, user settings, and share links. These are not orphaned; they actively serve 410 responses to deprecated client write paths.

---

## 3. Functions Deleted

None. No code was modified.

---

## 4. Smoke Results

Not run — no changes were made.

---

## 5. Verdict

NOT VERIFIED

### Hard Stops Triggered

1. `_deprecated_legacy_write` has 24 callers outside its own definition (task assumed 0). Deleting it would break 24 active 410 routes. PAUSED per hard stop rule.
2. `get_chart_profiles` (line 1890) is a live route returning real data via load_chart_profiles(). It is not a quarantined 410 stub. PAUSED per "do not touch any live route" rule.

### What Would Need to Change to Proceed

- A revised task would need to either: (a) remove all 24 routes calling `_deprecated_legacy_write` as a group, or (b) replace the per-function helper calls with inline 410 raises before deleting the helper.
- `get_chart_profiles` retirement would be a separate scope change with its own impact assessment.
- The 4 direct 410 stubs with 0 external callers (api_list_saved_searches, api_get_saved_search, api_profile_library, api_account_store) and `serve_local_product_store_json` + `_quarantine_legacy_read` could be safely removed in a narrower follow-up task.
