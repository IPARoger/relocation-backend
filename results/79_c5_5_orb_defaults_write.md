# RESULT: 79_c5_5_orb_defaults_write

**Roadmap ID:** C5-5  
**Checkpoint:** `ec0a21b`  
**Date:** 2026-06-18

---

## Files Changed

| File | Change |
|------|--------|
| `app_shell.html` | Removed legacy `settingsPatch.orb_defaults = mo` write mirror (~line 2961) |

**Not touched (per scope):** `supabase_store_bridge.js`, `account_settings_resolver.py`, backend routes, renderer, bridge helpers.

---

## Pre-flight Classification

| Location | Classification |
|----------|----------------|
| `app_shell.html:1762` | **read fallback** — `eff.major_aspect_orbs \|\| eff.orb_defaults` |
| `app_shell.html:2961` | **write mirror target** — sole app_shell write; removed |
| `supabase_store_bridge.js:63,91–97,103,135,441` | **bridge compatibility** — defaults, read fallbacks, persist mirrors |
| `services/account_settings_resolver.py:7,79,81,95` | **backend resolver compatibility** |
| `repositories/account_store_repository.py:395` | **backend resolver compatibility** |
| `local_product_store.py:44` | **unrelated** — static product defaults fixture |

**Pre-flight verdict:** Exactly one `app_shell.html` write mirror target confirmed before edit.

---

## Change Made

In the Settings save path (`rm-settings-majasp-*` block), removed:

```javascript
settingsPatch.orb_defaults = mo; // legacy mirror; single source of truth is the Aspect Registry
```

Retained:

```javascript
settingsPatch.major_aspect_orbs = mo;
```

Read fallback at line 1762 unchanged:

```javascript
const orb = eff.major_aspect_orbs || eff.orb_defaults || {};
```

---

## Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_settings_account.py
```

**Exit code:** 0

```
PASS: be_save_create_200
PASS: be_create_value
PASS: be_single_row_after_create
PASS: be_update_merge
PASS: be_single_row_after_update
PASS: be_invalid_default_404
PASS: be_cross_account_404
PASS: be_unauth_401
PASS: fe_saved_msg
PASS: fe_no_reload
PASS: fe_inmemory_update
PASS: fe_default_update
PASS: fe_reload_default
PASS: fe_reload_minor
PASS: fe_no_console_errors
PASS: fe_db_default
PASS: smoke_settings_account
```

---

## Remaining orb_defaults References

| File | Role | Status |
|------|------|--------|
| `app_shell.html:1762` | read fallback | **kept** |
| `supabase_store_bridge.js` | bridge compatibility (defaults + mirrors) | **unchanged** |
| `account_settings_resolver.py` | resolver read/write mirror | **unchanged** |
| `account_store_repository.py:395` | backend mirror on persist | **unchanged** |
| `local_product_store.py:44` | unrelated fixture | **unchanged** |

**Post-change grep:** no `settingsPatch.orb_defaults` or other app_shell write references remain.

---

## C5-5 Verdict

**VERIFIED**

Canonical `major_aspect_orbs` write preserved. Legacy app_shell write mirror removed. Read fallback and bridge/resolver compatibility layers intact. Smoke green.
