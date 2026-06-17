# C5-1 Dead Code Audit

**Roadmap ID:** C5-1
**Date:** 2026-06-18
**Scope:** Dead routes, repository methods, smoke dependencies, bridge helpers, compatibility layers
**Mode:** Read-only audit — no source files modified

---

## 1. Quarantined Routes (410 Gone)

All found in `main_centerline_FIXER.py`.

| Line | Function | Route / Reason |
|------|----------|----------------|
| 2062 | `serve_local_product_store_json` | Calls `_quarantine_legacy_read("/local-product-store.json")` → 410 |
| 2391 | `_quarantine_legacy_read(route)` | Helper: prints quarantine log, returns 410 for all callers |
| 2398 | `_deprecated_legacy_write(replacement, message)` | Legacy write gate (inline at 2564) |
| 2564 | _(inline route body)_ | `status_code=410` — legacy write path retired |
| 2602 | `api_list_saved_searches(profile_id)` | Returns 410 — "legacy read path retired — see C4-7 closeout" |
| 2607 | `api_get_saved_search(saved_search_id)` | Returns 410 — "legacy read path retired — see C4-7 closeout" |
| 3040 | `api_profile_library(profile_id)` | Returns 410 — "legacy read path retired — see C4-7 closeout" |
| 3049 | `api_account_store(request)` | Returns 410 — "legacy read path retired — see C4-7 closeout" |

**Summary:** 6 routes return 410. The two helpers `_quarantine_legacy_read` and `_deprecated_legacy_write` are dead-path scaffolding that exist solely to serve these 410 responses.

---

## 2. Dead Repository Methods (Top 10 Checked)

Methods checked across `repositories/*.py`. Caller counts exclude the definition line; search covered `*.py`, `*.js`, `*.html`.

| Method | File | Callers | Status |
|--------|------|---------|--------|
| `create_saved_investigation` | `account_saved_investigations_repository.py:88` | 3 | LIVE |
| `rename_saved_investigation` | `account_saved_investigations_repository.py:130` | 3 | LIVE |
| `archive_saved_investigation` | `account_saved_investigations_repository.py:170` | 3 | LIVE |
| `get_saved_investigation_by_id` | `account_saved_investigations_repository.py:212` | 2 | LIVE |
| `merge_account_settings` | `account_settings_repository.py:52` | 3 | LIVE |
| `create_profile_with_birth` | `account_profiles_repository.py:49` | 3 | LIVE |
| `rename_profile` | `account_profiles_repository.py:205` | 3 | LIVE |
| `archive_profile` | `account_profiles_repository.py:237` | 4 | LIVE |
| `get_user_settings` | `user_settings_repository.py:10` | 3 | LIVE |
| `create_user_settings` | `user_settings_repository.py:28` | 1 | LIVE (marginal) |

**Summary:** No dead repository methods in top 10. `create_user_settings` has only 1 external caller — worth a follow-up trace but not flagged dead.

---

## 3. Dead Smoke Imports

Smoke files scanned: all `scripts/smoke_*.py`.

All smoke scripts import only Python stdlib modules:
- `json`, `os`, `socket`, `subprocess`, `sys`, `time`, `urllib.error`, `urllib.request`, `pathlib.Path`
- `playwright.sync_api` — conditional/lazy runtime import (not top-level)

**No smoke imports reference quarantined, retired, or non-existent modules.**

Files scanned: `smoke_account_store_read.py`, `smoke_app_shell_context_transport.py`, `smoke_app_shell_map_handoff.py`, `smoke_app_shell_store_read.py`, `smoke_chart_record_birth_bridge.py`, `smoke_chart_record_library_read.py`, `smoke_comparison_sets.py`, `smoke_legacy_writes_deprecated.py`.

---

## 4. Dead Bridge Helpers (`supabase_store_bridge.js`)

Functions from `supabase_store_bridge.js` checked against `app_shell.html` and `map_CURRENT.html`:

| Function | Line | HTML Refs | Notes |
|----------|------|-----------|-------|
| `toConfidenceTier(mode)` | 29 | 0 | Private IIFE helper; called internally at lines 398, 618 |
| `toRecordType(profile_type)` | 36 | 0 | Private IIFE helper; called internally at lines 413, 633 |
| `trimTime(pgTime)` | 43 | 0 | Private IIFE helper; called internally at lines 395, 615 |
| `getEffectiveSettings(...)` | 85 | 12 (app_shell.html) | `RM.getEffectiveSettings` / `window.RMSettings.getEffectiveSettings` — LIVE |
| `buildSettingsSnapshot(effective)` | 126 | 1 (map_CURRENT.html) | `window.RMSettings.buildSettingsSnapshot` — LIVE |
| `buildSupabaseStore()` | 162 | 0 external | Called internally at line 647 as IIFE entry point — LIVE |
| `refreshProfile(profileId)` | 556 | 1 (app_shell.html) | `window.refreshProfile(...)` — LIVE |

**Flagged:** `toConfidenceTier`, `toRecordType`, and `trimTime` have 0 references in the two HTML consumers. They are private closure helpers with internal callers only — not externally reachable. Safe to inline or consolidate when the bridge is refactored.

---

## 5. Compatibility Layer Findings

Matches from project `*.py`, `*.js`, `*.html` (excluding `venv/`, `.playwright-browsers/`, `.tmp-chrome-*`):

### `main_centerline_FIXER.py`
- **Line 1902:** `# migration / account sync stays backwards-compatible.`

### `app_shell.html`
- **Line 391:** `/** Back-compat test surface — mirrors navContext field names used by earlier shell smokes. */`
- **Line 1194:** Comment — legacy/offline note path when no account note exists yet
- **Line 2960:** `settingsPatch.orb_defaults = mo; // legacy mirror; single source of truth is the Aspect Registry`
- **Line 3228:** `// profileId is retained for caller compatibility; the backend resolves the`

### `map_CURRENT.html`
- **Line 960:** `Adapter reads variables[] only — not legacyCompatibility.` (genie render UI note)
- **Line 1054:** `LEGACY_SEARCH_REGIONS: "legacy_search_regions"` — active renderer substrate constant
- **Lines 1349, 1351:** Phase 2.5A — preferred over legacy library handoff
- **Line 1417:** Empty legacy list fallback for 8004 Supabase /profiles block
- **Line 1440:** Selector identical for renderer smoke and legacy flow
- **Line 1500:** Legacy library handoff fallback: `#libraryActive / rm_library_active`
- **Line 1940:** `window.__rmSavedInvestigationReplaySource = "legacy_dom"`
- **Lines 2083–2089:** Both legacy `dataset.profile` and Supabase paths noted
- **Line 2704:** `legacySearchRegionsActive: ACTIVE_RENDERER_SUBSTRATE === RENDERER_SUBSTRATES.LEGACY_SEARCH_REGIONS`
- **Lines 3539, 3560:** Fallback to legacy mock-store endpoint on 404 for legacy IDs / not-yet-migrated records
- **Lines 4827–5096:** `summarizeLegacyShadowResult`, `compileLegacyGeometryIndex`, `summarizeCanonicalLegacyParity`, `summarizeMaskParity` — full shadow comparison suite with extensive legacy geometry path
- **Lines 5585–5672:** `runCanonicalDryRun` with `legacySummary` + `legacyGeojson` params
- **Lines 5727, 5752, 5998:** "Legacy DOM → engine plan (compatibility path; not canonical truth)" — `source: "legacy_dom"` handoff still active

### `aura_field_engine.py`
- **Lines 1645–1646:** `# Doctrine compatibility — convergence engine never relies on max_depth; legacy adaptive callers may still inspect these fields.`

### `sampling_cache_orchestration_contract.js`
- **Lines 129–183:** `classifyJobCompatibility` / `compatible` / `compatibility` — active job-compatibility classification (functional logic, not a dead shim)

---

## 6. Priority Order for Removal (Smallest / Safest First)

| Priority | Item | File | Rationale |
|----------|------|------|-----------|
| 1 | `_quarantine_legacy_read` helper | `main_centerline_FIXER.py:2391` | Pure scaffolding; inline 410 directly in each route stub |
| 2 | `_deprecated_legacy_write` helper | `main_centerline_FIXER.py:2398` | Same pattern; no callers outside the 410 stubs |
| 3 | `serve_local_product_store_json` (410 stub) | `main_centerline_FIXER.py:2062` | Single-route stub; safe once FE stops hitting it |
| 4 | `api_list_saved_searches` + `api_get_saved_search` (410 stubs) | `main_centerline_FIXER.py:2602–2608` | Paired; confirm smoke_legacy_writes_deprecated still covers |
| 5 | `api_profile_library` + `api_account_store` (410 stubs) | `main_centerline_FIXER.py:3040–3050` | Higher blast radius; check FE fallback at map_CURRENT.html:3539 first |
| 6 | `toConfidenceTier`, `toRecordType`, `trimTime` | `supabase_store_bridge.js:29–45` | Inline into callers inside IIFE — low-risk refactor |
| 7 | `orb_defaults` legacy mirror | `app_shell.html:2960` | Remove once Aspect Registry confirmed sole source of truth |
| 8 | `LEGACY_SEARCH_REGIONS` substrate + shadow comparison suite | `map_CURRENT.html:1054, 4827–5096` | Large blast radius; requires canonical substrate fully promoted first |
| 9 | Legacy DOM handoff path (`source: "legacy_dom"`) | `map_CURRENT.html:5727–5998` | Remove after legacy_dom source fully retired and smoke coverage confirmed |

---

## VERIFIED

All grep searches completed. No source files were modified. Findings are based solely on static grep analysis of project source files (excluding `venv/`, `.playwright-browsers/`, `.tmp-chrome-*`, `node_modules/`, `.git/`).
