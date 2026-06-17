# Task 46 — Quarantine Dead Read Routes

**Date:** 2026-06-17

---

## 1. Caller check (step 1)

```
./app_shell.html:6:  ... (/local-product-store.json).
./app_shell.html:230:const STORE_JSON_URL = "/local-product-store.json";
./supabase_store_bridge.js:21: * ... comment only
./main_centerline_FIXER.py:2061:@app.get("/local-product-store.json")
./main_centerline_FIXER.py:3046:@app.get("/profile-library/{profile_id}")
./main_centerline_FIXER.py:3083:@app.get("/account-store")
```

**Zero frontend callers (js/ts/html, excl. map_CURRENT):**
- `GET /account-store` — none
- `GET /profile-library/{id}` — none

**Active caller found — NOT quarantined:**
- `GET /local-product-store.json` — `app_shell.html` (`STORE_JSON_URL` + fallback `fetch`) — hard stop applied

Smoke scripts still reference `/account-store` and `/local-product-store.json` (not product callers).

---

## 2. Files modified

| File | Lines | Change |
|------|-------|--------|
| `main_centerline_FIXER.py` | ~3 | `JSONResponse` import added |
| `main_centerline_FIXER.py` | ~2395–2401 | `_quarantine_legacy_read()` helper (410 + log) |
| `main_centerline_FIXER.py` | 3056–3058 | `api_profile_library` → 410 quarantine |
| `main_centerline_FIXER.py` | 3065–3067 | `api_account_store` → 410 quarantine |

`/local-product-store.json` route **unchanged** (active `app_shell.html` caller).

No files deleted.

---

## 3. Smoke results

| Script | Exit code |
|--------|-----------|
| `scripts/smoke_map_current.py` | **0** |
| `scripts/smoke_saved_investigations.py` | **0** |

---

## 4. Status

**NOT VERIFIED** (full task scope) — 2 of 3 routes quarantined; `/local-product-store.json` blocked by step-1 hard stop (active `app_shell.html` fallback caller).

**Partial:** account-store and profile-library return 410 with `{"error":"Gone","reason":"legacy read path retired"}`.
