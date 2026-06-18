# T13: Port 8000 Endpoint Inventory

**Roadmap ID:** T13_1  
**Date:** 2026-06-18  
**Mode:** Read-only diagnosis (no code changes)

## Executive summary

The task spec references `frontend/map_CURRENT.html` and `frontend/app_shell.html`, but **no `frontend/` directory exists**. Active production HTML lives at the repo root: `map_CURRENT.html` and `app_shell.html`.

**Critical finding:** Active production UI **no longer hardcodes `http://127.0.0.1:8000`**. Zero URL matches in `map_CURRENT.html` or `app_shell.html`. Calls use same-origin relative paths (`API_BASE = ''`, `LIBRARY_API_BASE = ""`) and are served by `main_centerline_FIXER.py` (Web2 stack on port **8004**).

The only remaining "8000" strings in active `map_CURRENT.html` are unrelated (`maxSamples: 8000` at line 1107) and a **stale comment** at line 1416 ("Legacy /chart-profiles (port 8000)").

**Documentation drift:** `FEATURE_STATUS_BOARD.md` blocker **B-2**, `PRODUCTION_ACCEPTANCE_CHECKLIST.md` §3.3–3.4 and §3.5, and several architecture docs still describe five hardcoded port-8000 endpoints. That reflects a **pre-migration snapshot** (confirmed by `archives/validation_2026-05-15/html_snapshots/map_CURRENT.html` and `backups/` copies). B-2 should be reclassified after human review.

**Hardcoded port 8000 remains only in:** sandbox HTML, validation sandboxes, `Old File/`, backups, archives, one dev JS bridge, and stale docs — classified **ARCHAEOLOGY** or **dev-only**.

---

## Backend availability on port 8004 (`main_centerline_FIXER.py`)

Command run:

```bash
grep -n "^@app\." main_centerline_FIXER.py | grep -E "(relocated|aura|aspect-orb|screen-pixel|library|chart-profiles)"
```

| Line | Route | Method |
|------|-------|--------|
| 944 | `/aura-field` | POST |
| 967 | `/aura-raster` | POST |
| 998 | `/aura-raster-adaptive` | POST |
| 1041 | `/aura-raster-convergence` | POST |
| 1504 | `/screen-pixel-truth` | POST |
| 1735 | `/aspect-orb-at-point` | GET |
| 1780 | `/relocated-chart` | GET |
| 1889 | `/chart-profiles` | GET |
| 2217 | `/library/state` | GET |
| (+) | `/library/*` | various |

All B-2-named endpoints exist on the same FastAPI app used for port 8004 smokes. `/aura-raster-convergence` exists on backend but is **not called** from active production UI (ARCHAEOLOGY).

---

## Active production endpoint inventory

Sorted by migration effort (S → M → L), then impact.

| Endpoint | Status | Frontend caller(s) | Line(s) | Function / context | Error handling | Feature(s) blocked (if 8004 down) | Effort | Next action |
|----------|--------|-------------------|---------|-------------------|----------------|-----------------------------------|--------|-------------|
| `/relocated-chart` | **MIGRATED** | `map_CURRENT.html` | 2125–2127, 2459, 3203, 3422 | `fetchRelocatedChart()` — contextmenu popup, debug overlay click, dataset city popup, genie summary | try/catch → fallback popup HTML + `console.error` | Popup relocated chart; city popup charts; debug overlay readout | **S** (frontend done) | Update B-2 docs; smoke on 8004-only stack |
| `/relocated-chart` | **MIGRATED** | `app_shell.html` | 1555, 1642 | `hydrateRelocatedChart()` Screen 4; `hydrateComparisonColumns()` Screen 5 | try/catch → `warn-box` UI | Screen 4 chart facts; Screen 5 comparison columns | **S** | Same as above |
| `/aspect-orb-at-point` | **PARTIAL** | `map_CURRENT.html` | 2473 | Inline in contextmenu popup handler (no `getAspectOrbAtPoint()` function); debug aura mode only | Silent skip if `!orbResp.ok`; outer try/catch on popup | Debug orb readout in popup (PoC overlay only) | **S** | Document PoC scope; optional UX error |
| `/aura-raster` | **PARTIAL** | `map_CURRENT.html` | 3664, 4203 | `postAuraRaster()` → `renderRasterAuraProgressive()` | Throws from `postAuraRaster`; outer genie render catch logs + rethrows | Angular raster aura overlay (Sun conjunct ASC PoC) | **M** | Verify 8004-only smoke; improve user-visible aura failure |
| `/aura-raster-adaptive` | **PARTIAL** | `map_CURRENT.html` | 3677, 4119 | `postAuraRasterAdaptive()` → `renderAdaptiveAuraProgressive()` | Same throw pattern | Adaptive aura overlay (PoC) | **M** | Same |
| `/aura-field` | **PARTIAL** | `map_CURRENT.html` | 3651, 4563 | `postAuraField()` → `renderAuraFieldProgressive()` (warns polygon path not deliverable) | Throws from `postAuraField` | Legacy polygon aura (superseded by raster) | **M** | Consider deprecating polygon path in UI |
| `/screen-pixel-truth` | **MIGRATED** | `map_CURRENT.html` | 5175+ | `postScreenPixelTruth()` — debug `?screenPixelTruth=1` | Returns `{ response, body }`; caller checks status | Debug / QA pixel-truth grid only | **S** | None for production |
| `/chart-profiles` | **MIGRATED** | `map_CURRENT.html` | 1421 | `loadChartProfiles()` — optional legacy list before Supabase `/profiles` | try/catch; continues with empty legacy list | Legacy local profile dropdown only (Supabase path is primary) | **S** | Remove stale "port 8000" comment at 1416 |
| `/library/state` | **MIGRATED** | `map_CURRENT.html` | 1286 | `fetchLibraryStateSafe()` — Phase 2 library handoff | try/catch → `libraryAvailable = false` | Library handoff banner (feature-flag `RM_PHASE2_LIBRARY`) | **S** | None |
| `/search-regions` | **MIGRATED** | `map_CURRENT.html` | 4752 | Find Regions / genie engine (`${API_BASE}/search-regions`) | `postSearchRegions()` throws on non-200 | Core Find Regions | **S** | Already on 8004 path via `API_BASE = ''` |

**Notes on PARTIAL:** Backend routes exist and are reachable on 8004, but `/aspect-orb-at-point` and aura endpoints enforce **Sun conjunct ASC PoC** scope (`is_aura_poc_overlay`, 400 on other overlays). Backend docstrings mark aura endpoints as archaeology/debug PoC. That is reduced functionality vs a full overlay matrix, not a port migration gap.

**`app_shell.html`:** No port 8000 references. No aura or aspect-orb calls.

---

## Hardcoded `127.0.0.1:8000` references (non-active)

Every `grep -rn "127.0.0.1:8000" --include="*.html" --include="*.js"` match (25 total, 0 in active production UI):

| Endpoint(s) used | File | Line | Status | Notes |
|------------------|------|------|--------|-------|
| `/search-regions` | `map_SANDBOX_truth_reveal.html` | 178 | ARCHAEOLOGY | `const API = "http://127.0.0.1:8000"` |
| `/search-regions` | `map_SANDBOX_polygon_reveal.html` | 231 | ARCHAEOLOGY | Same pattern |
| `/search-regions` | `map_SANDBOX_brute_force.html` | 186 | ARCHAEOLOGY | Same pattern |
| `/search-regions` | `map_SANDBOX_truth_pixels.html` | 129 | ARCHAEOLOGY | Same pattern |
| `/search-regions` | `map_SANDBOX_overlay_color_test.html` | 16, 272 | ARCHAEOLOGY | Comment + live fetch |
| `/search-regions` | `validation/sandboxes/phase3_*.html` (5 files) | 30–79 | ARCHAEOLOGY | `API_BASE = "http://127.0.0.1:8000"` |
| `/search-regions` | `sampling_cache_fetch_bridge_dev.js` | 13 | ARCHAEOLOGY | Dev bridge default |
| `/relocated-chart`, `/search-regions` | `Old File/map_*.html` (4 files) | various | ARCHAEOLOGY | Retired map variants |
| `/relocated-chart`, `/search-regions` | `archives/.../map_CURRENT.html` | 244, 364 | ARCHAEOLOGY | May 2026 snapshot (pre-migration) |
| `/chart-profiles`, `/relocated-chart`, `/search-regions` | `backups/*/map_CURRENT.html` (2 files) | various | ARCHAEOLOGY | Backup snapshots |
| favorites fallback | `prototype_profile_workspace_v11.html` | 667 | ARCHAEOLOGY | Prototype; uses `location.origin` when served over HTTP |

**Completeness:** 25 repo-wide HTML/JS matches; 0 in active production UI; all matches accounted above.

---

## B-2 cross-check (`FEATURE_STATUS_BOARD.md` §4)

| B-2 claim | Inventory finding |
|-----------|-------------------|
| Five endpoints hardcode `http://127.0.0.1:8000` in `map_CURRENT.html` | **Stale.** Active file uses relative URLs; archived/backup snapshots still show hardcoded URLs. |
| Functions: `renderRasterAura()`, `renderAdaptiveAuraProgressive()`, `renderAuraField()`, `fetchRelocatedChart()`, `getAspectOrbAtPoint()` | Names mostly match (`renderRasterAuraProgressive`, `postAura*`, `fetchRelocatedChart`; orb is inline fetch, not `getAspectOrbAtPoint`) |
| Silent failure when port 8000 down | Partially still true for **aura** outer catch (console only); **popup chart** now shows fallback HTML on error |
| Fix: re-implement on 8004 | **Already implemented** in `main_centerline_FIXER.py`; frontend rewired to same origin |

**PRODUCTION_ACCEPTANCE_CHECKLIST.md §3.3–3.4:** Still lists aura and popup endpoints as "hardcode port 8000" and BLOCKED — **contradicts live frontend**.

**Recommended B-2 update:** Downgrade from "hardcoded port 8000" to "verify 8004-only operational smoke + update architecture docs + optional aura error surfacing."

---

## Feature blocking map (current code, 8004-only stack)

| Feature | Endpoints | Blocked by missing port 8000? | Blocked by other issues? |
|---------|-----------|--------------------------------|--------------------------|
| Angular overlays (aura) | `/aura-raster`, `/aura-raster-adaptive`, `/aura-field` | **No** (same-origin 8004) | PoC overlay scope; silent console-only failures |
| Popup relocated chart | `/relocated-chart`, `/aspect-orb-at-point` | **No** | Birth profile resolution; ±65° lat cap; orb debug PoC-only |
| Screen 4 / 5 charts | `/relocated-chart` | **No** | Birth data / place coords |
| Find Regions | `/search-regions` | **No** | — |
| Library handoff | `/library/state`, `/chart-profiles` | **No** | `RM_PHASE2_LIBRARY` flag |
| Comparison facts (B-4) | `/relocated-chart` | **No** (endpoint available) | Separate wiring task; Screen 5 now fetches real charts |

---

## Validation commands (read-only, executed 2026-06-18)

```bash
# Zero hardcoded 8000 in active production HTML
grep -rn "127.0.0.1:8000" map_CURRENT.html app_shell.html
# → no matches

# All hardcoded refs in repo (HTML/JS)
grep -rn "127.0.0.1:8000" --include="*.html" --include="*.js" . | grep -v node_modules
# → 25 matches (all sandbox/archaeology/dev/backups)

# Backend routes
grep -n "^@app\." main_centerline_FIXER.py | grep -E "(relocated|aura|aspect-orb|screen-pixel|library|chart-profiles)"

# Active endpoint fetch sites
grep -n 'fetch.*"/aura\|fetch.*`/relocated\|fetch.*`/aspect-orb\|fetch.*"/screen-pixel\|chart-profiles\|library/' \
  map_CURRENT.html app_shell.html
```

---

## Rollback

None required — read-only diagnosis. Delete this file and `results/13_t13port-8000-endpoint-inventory.md` to revert documentation only.

---

**Inventory status:** Complete for active codebase + archaeology sweep.  
**Human review:** Required before migration planning — B-2 register contradicts live frontend wiring.
