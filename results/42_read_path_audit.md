# Task 42 — Read Path Consolidation Audit

**Date:** 2026-06-17  
**Scope:** Frontend read paths only (how data GETs to the browser).  
**Method:** Grep-first audit per `tasks/42_read_path_consolidation_audit`. No files modified except this deliverable.

---

## 1. Files Found (Step 1)

```text
find . -maxdepth 4 \
  -name "account-store*" \
  -o -name "supabase_store_bridge*" \
  -o -name "profile-library*" \
  -o -name "*store*bridge*" \
  -o -name "*saved-search*"
```

**Result (1 file):**

| Path | Notes |
|------|-------|
| `./supabase_store_bridge.js` | Only match at maxdepth 4 |

**Not found as frontend files:**

| Expected name | Status |
|---------------|--------|
| `account-store*` | No frontend module. Backend route `GET /account-store` exists in `main_centerline_FIXER.py` but **no frontend caller** found. |
| `profile-library*` | No frontend module. Backend route `GET /profile-library/{profile_id}` exists in `main_centerline_FIXER.py` but **no frontend caller** found. |
| `*saved-search*` | No dedicated frontend module filename. Saved-search reads live inside `supabase_store_bridge.js` and `map_CURRENT.html`. |

**Related scaffold (not returned by step-1 find):**

- `scaffold/local_product/TEMPORARY_product_store.json` — local store source artifact
- `app_shell.html` references `GET /local-product-store.json` (file not present at repo root in this audit)

---

## 2. Per-Source Classification

| Source | Purpose | Classification | Caller count |
|--------|---------|------------------|--------------|
| `supabase_client.js` | Fetch `/config/supabase`, load CDN client, expose `window.SupabaseReady` | **CANONICAL** (client bootstrap) | **6** HTML/JS consumers |
| `user_profile.js` | Load `CurrentUser` via RPC + `accounts` / `account_memberships` SELECT | **CANONICAL** | **4** |
| `supabase_store_bridge.js` | Assemble product store from Supabase tables; `window.SupabaseStoreReady` | **CANONICAL** + **BRIDGE** | **2** script includes + **1** intake listener |
| `app_shell.html` → `loadViewModelFromStore()` | `SupabaseStoreReady` → `adaptStoreToView` | **CANONICAL** (orchestrator) | Shell entry |
| `app_shell.html` → `fetch(STORE_JSON_URL)` | Fallback `GET /local-product-store.json` | **LEGACY** | Fallback branch only |
| `app_shell.html` → `attachEngineSummaries()` | `GET /chart-records` | **CANONICAL** (geometry supplement) | Shell init |
| `app_shell.html` → `hydrateChartRecordComparisonSets()` | Direct Supabase SELECT `comparison_sets` | **LEGACY** (parallel to bridge) | Chart-record route |
| `app_shell.html` → `appendCreatedProfileToStore()` | Direct Supabase SELECT after create | **BRIDGE** (incremental patch) | Post-create flow |
| `app_shell.html` → `planProfileArchive()` | Direct Supabase SELECT `profiles` | **LEGACY** | Archive planning UI |
| `current_location_editor.js` | `places` SELECT for search | **BRIDGE** | **2** |
| `first_profile_intake.js` | `places` SELECT for search | **BRIDGE** | **3** |
| `account_drawer.js` | Reads `CurrentUser` + view model only | **CANONICAL** (UI consumer) | **1** |
| `auth_guard.js` | Session gate | **CANONICAL** (auth) | **5** |
| `map_CURRENT.html` → `/library/state`, `/chart-profiles` | Legacy library handoff | **LEGACY** | Map init |
| `map_CURRENT.html` → `GET /profiles` | Optional JWT profile list | **LEGACY** | `loadChartProfiles()` |
| `map_CURRENT.html` → direct Supabase SELECT | `saved_searches`, `favorite_places`, `places` | **LEGACY** (parallel) | Map helpers |
| `map_CURRENT.html` → geometry GETs | search-regions, aura, screen-pixel-truth, etc. | **CANONICAL** (map compute) | Map pipeline |
| Backend `GET /account-store` | Server-assembled store | **DEAD** (frontend) | **0** |
| Backend `GET /profile-library/{id}` | Server profile library | **DEAD** (frontend) | **0** |

**Files opened for targeted read (9 / 10 limit):**  
`supabase_store_bridge.js`, `supabase_client.js`, `user_profile.js`, `current_location_editor.js`, `first_profile_intake.js`, `account_drawer.js`, `auth_guard.js`, `place_resolution.js`, `app_shell.html` (section reads only).

---

## 3. Direct Supabase Reads Outside Bridge/Store (Step 3)

| File | Tables / operation |
|------|--------------------|
| `user_profile.js` | `accounts`, `account_memberships` SELECT |
| `current_location_editor.js` | `places` SELECT |
| `first_profile_intake.js` | `places` SELECT |
| `app_shell.html` | `comparison_sets`, `comparison_set_places`, `profiles`, `birth_records`, `places` SELECT |
| `map_CURRENT.html` | `saved_searches`, `favorite_places`, `places` SELECT |

---

## 4. JWT / HTTP GET Routes in Use (Step 4)

**Account / store reads:** `/config/supabase`, `/local-product-store.json`, `/chart-records`, `/supabase/chart-records/{id}/engine-birth`, `/chart-records/{id}/engine-birth`, `/library/state`, `/chart-profiles`, `/profiles`, `/places/search`.

**Task-listed routes used as writes only (POST):** `/profiles/*`, `/saved-investigations/*`, `/favorites/*`, `/comparison-sets/*`, `/current-location/set`.

**Backend GET with zero frontend callers:** `/account-store`, `/profile-library/{id}`.

---

## 5. Flagged Items

- **Supabase writes in frontend:** none found in product files (writes use JWT POST).
- **Dead frontend read paths:** `GET /account-store`, `GET /profile-library/{id}`.
- **Stale comment:** `first_profile_intake.js` header describes direct INSERT; code uses `POST /profiles/create-with-birth`.
- **Duplication:** bridge vs inline shell SELECTs; bridge vs map direct SELECTs; bridge vs unused `/account-store` API.

---

## 6. Canonical Read Path (evidence)

**`app_shell.html`:** `supabase_client.js` → `auth_guard.js` → `user_profile.js` → **`supabase_store_bridge.js`** → `loadViewModelFromStore()` → `adaptStoreToView()`, plus `GET /chart-records` for engine summaries.

**`map_CURRENT.html`:** split — bridge loaded, but also legacy `/library/state`, `/chart-profiles`, `GET /profiles`, direct Supabase SELECTs, and geometry API GETs.

---

## 7. Validation

| Criterion | Status |
|-----------|--------|
| Greps ran | Yes |
| Sources classified | Yes |
| Caller counts for LEGACY/BRIDGE | Yes |
| No other files modified | Yes |
| ≤10 files opened | Yes (9) |

## **VERIFIED**
