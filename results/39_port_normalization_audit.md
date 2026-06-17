# Task 39 — Port Normalization Audit

**Task:** `tasks/39_port_normalization_audit`  
**Type:** Read-only audit  
**Date:** 2026-06-17  
**Executor:** Cursor (Composer)

## VERDICT: VERIFIED

No files modified except this deliverable. No implementation proposed.

---

## 1. Grep: `8004` (production code — non-doc)

Command:
```bash
rg -n "8004" . --glob '*.html' --glob '*.js' --glob '*.py' \
  | rg -v '^./docs/' | rg -v 'backups/|archives/|Old File|map_SANDBOX|prototype_|validation/'
```

### map_CURRENT.html

| Line | Content | Classification |
|------|---------|----------------|
| 1416 | `// continue with an empty legacy list so the 8004 Supabase /profiles block` | COMMENT_ONLY |
| 1472 | `fetch(\`http://127.0.0.1:8004/profiles\`, {` | **HARDCODED_PORT** |
| 2272 | `{ apiBase: "http://127.0.0.1:8004", coordTolerance: 0.02 });` | **HARDCODED_PORT** (passed into place resolution) |
| 2388 | `// search against 8004. Read-only — does not create places.` | COMMENT_ONLY |
| 2404 | `` `http://127.0.0.1:8004/places/search?q=...` `` | **HARDCODED_PORT** |
| 4748 | `fetch("http://127.0.0.1:8004/search-regions", {` | **HARDCODED_PORT** |

**Note:** Line 1106 `maxSamples: 8000` is a sample-count constant, not a port (excluded).

### scripts/ (account-product smokes — PORT or base defaults)

| File | Line(s) | Content summary | Classification |
|------|---------|-----------------|----------------|
| smoke_saved_investigations.py | 38 | `PORT = 8004` | TEST_ONLY |
| smoke_place_resolution.py | 38 | `PORT = 8004` | TEST_ONLY |
| smoke_favorites.py | 23–25, 54 | Notes + `PORT = 8004` | TEST_ONLY |
| smoke_profile_create.py | 44 | `PORT = 8004` | TEST_ONLY |
| smoke_profile_rename_archive.py | 37 | `PORT = 8004` | TEST_ONLY |
| smoke_comparison_sets.py | 42 | `PORT = 8004` | TEST_ONLY |
| smoke_legacy_writes_deprecated.py | 28 | `PORT = 8004` | TEST_ONLY |
| smoke_account_store_read.py | 16, 36 | doc + `BASE_URL` default 8004 | TEST_ONLY / ENV_GUARDED |
| smoke_current_location_backend.py | 18, 38 | doc + `BASE_URL` default 8004 | TEST_ONLY / ENV_GUARDED |
| smoke_current_location_frontend.py | 85 | `base = "http://127.0.0.1:8004"` | TEST_ONLY |
| smoke_notes_backend.py | 124 | `base = "http://127.0.0.1:8004"` | TEST_ONLY |
| smoke_notes_frontend.py | 89 | `base = "http://127.0.0.1:8004"` | TEST_ONLY |
| smoke_settings_account.py | 133 | `base = "http://127.0.0.1:8004"` | TEST_ONLY |
| smoke_map_saved_investigation_note.py | 124 | `base = "http://127.0.0.1:8004"` | TEST_ONLY |

### False positive

| File | Classification | Note |
|------|----------------|------|
| cities.js | **UNRELATED** | `8004` appears inside embedded geodata JSON (population/coordinate digits), not a port reference |

### docs/ (grep summary)

`rg -c "8004" docs/` → **141 matches** across architecture docs (OPERATIONAL_SMOKE_TESTS, PRODUCTION_DEPENDENCY_MATRIX, DATA_OWNERSHIP, etc.). All are **COMMENT_ONLY** / documentation references to port 8004 as the Web2 server. Not executable code.

---

## 2. Grep: `localhost` and `127.0.0.1` (active html/js)

### `127.0.0.1` (production-relevant)

| File | Line | Content | Classification |
|------|------|---------|----------------|
| map_CURRENT.html | 1472 | `http://127.0.0.1:8004/profiles` | **HARDCODED_PORT** |
| map_CURRENT.html | 2272 | `apiBase: "http://127.0.0.1:8004"` | **HARDCODED_PORT** |
| map_CURRENT.html | 2404 | `http://127.0.0.1:8004/places/search` | **HARDCODED_PORT** |
| map_CURRENT.html | 4748 | `http://127.0.0.1:8004/search-regions` | **HARDCODED_PORT** |
| sampling_cache_fetch_bridge_dev.js | 13 | `http://127.0.0.1:8000/search-regions` | **TEST_ONLY** (dev bridge script) |

### `localhost`

No matches in `map_CURRENT.html`, `app_shell.html`, `place_resolution.js`, `first_profile_intake.js`, `auth.html`.

### Already relative (no port hardcode) — map_CURRENT.html

These use same-origin relative paths (inherit page port):

- `/relocated-chart?...` (line ~2125)
- `/aspect-orb-at-point?...` (line ~2469)
- `/aura-field`, `/aura-raster`, `/aura-raster-adaptive` (lines ~3647–3673)
- `/chart-profiles` via `LIBRARY_API_BASE` empty string (line ~1420)
- `app_shell.html`, `first_profile_intake.js`, `current_location_editor.js` — JWT routes use relative paths (`/saved-investigations/...`, `/profiles/create-with-birth`, `/current-location/set`)

---

## 3. Context reads (±5 lines) — production hits only

### map_CURRENT.html:1472 — GET /profiles

Fetches Supabase profile list for `#chartProfile` dropdown. Uses JWT from session when available. **Bypasses same-origin** by forcing port 8004 even when map is served from 8000.

### map_CURRENT.html:2272 — RMPlaceResolution apiBase

Passes hardcoded `apiBase` into `resolvePlaceFromCitySelection`. `place_resolution.js` defaults to `""` (relative) when `apiBase` omitted — map overrides to 8004.

### map_CURRENT.html:2404 — GET /places/search

Favorite popup read-path place lookup. Hardcoded 8004.

### map_CURRENT.html:4748 — POST /search-regions

Find Regions compute path. Hardcoded 8004.

### place_resolution.js (not in grep 8004 list)

`resolveApiBase()` returns `options.apiBase`, `LIBRARY_API_BASE`, or `""`. Write path `/places/resolve-or-create` is **already relative-capable**. Map is the caller that injects `:8004`.

---

## 4. Classification summary

| Classification | Count (executable) | Files |
|----------------|-------------------|-------|
| **HARDCODED_PORT** | 4 lines | `map_CURRENT.html` only |
| **ENV_GUARDED** | 0 in production UI | Smokes use `BASE_URL` env override |
| **TEST_ONLY** | 15+ lines | `scripts/smoke_*.py` (split 8000 vs 8004 defaults) |
| **COMMENT_ONLY** | 2 lines + 141 doc lines | map comments + `docs/architecture/*` |
| **DEAD_CODE / DEV** | 1 line | `sampling_cache_fetch_bridge_dev.js` (:8000) |
| **UNRELATED** | 1 file | `cities.js` geodata false positive |

---

## 5. Canonical port config

| Question | Answer |
|----------|--------|
| Single source of truth for backend port? | **MISSING** |
| `.env.example` | No `PORT` or `BASE_URL` variable |
| `.env.staging` | Supabase keys only; no port |
| Smoke scripts | Split defaults: **8000** (map/library/renderer smokes) vs **8004** (account-product smokes) |
| Production UI | Mixed: `map_CURRENT.html` hardcodes **8004** for 4 calls; other endpoints already **relative** |
| `LIBRARY_API_BASE` | Empty string in map (same-origin) — pattern exists but not used for the four 8004 calls |

**Flag:** Operational docs (`OPERATIONAL_SMOKE_TESTS.md`) instruct uvicorn on **8004**; checkpoint smokes for map/library use **8000**. This mismatch is a known operational hazard.

---

## 6. Human-review flag (hard-stop check)

All hardcoded ports found are `127.0.0.1` (local dev/staging pattern). **No production-host config file** (e.g. deployed domain) contains `:8004`.

The **production UI risk** is: map served from one port while four API calls target another. This is a local/staging wiring bug, not a leaked production URL.

---

## 7. Recommended fix scope (files likely needing change — audit only)

**Primary (product):**

| File | Why |
|------|-----|
| `map_CURRENT.html` | 4 hardcoded `127.0.0.1:8004` URLs |

**Secondary (validation alignment — when product fix lands):**

| File | Why |
|------|-----|
| `scripts/smoke_favorites.py` | Documents dependency on map :8004 |
| Account smokes with `PORT = 8004` or hardcoded base | May unify when single server port is chosen |

**Out of scope for port-normalization implementation (unless explicitly authorized):**

- `docs/architecture/*` — update after port decision (docs-only)
- `cities.js` — false positive
- `sampling_cache_fetch_bridge_dev.js` — dev-only
- Smokes already on `BASE_URL` / `PORT = 8000` — may stay if 8000 becomes canonical

**Not required for port fix:**

- `place_resolution.js` — already supports relative URLs; remove hardcoded `apiBase` from map caller
- `app_shell.html`, `first_profile_intake.js`, `current_location_editor.js` — already relative

---

## 8. Architectural note (for Chat 3 planning)

Port normalization is **narrower** than read-path consolidation. Map is **partially migrated**: render/popup/aura paths are relative; profile list, place search, search-regions, and place-resolution apiBase are not.

---

## 9. Validation checklist

| Criterion | Met |
|-----------|-----|
| All grep commands ran | Yes |
| Every production hit classified | Yes |
| Canonical port config assessed | Yes — **missing** |
| No source files modified | Yes |
| Deliverable written | Yes |

**VERIFIED**
