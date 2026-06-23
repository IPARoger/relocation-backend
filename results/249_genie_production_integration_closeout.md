# 249 — Genie Production Integration Closeout

**Mode:** Closeout only — no further implementation in this track.  
**Date:** 2026-06-23  
**Production surface:** `map_CURRENT.html`  
**Rollback anchor:** tag `map_current_pre_genie_merge`

---

## Rollback tag

| Item | Value |
|------|-------|
| Tag | `map_current_pre_genie_merge` |
| Tag target commit | `495b6e6` — `audit: map_current pre-genie-merge recovery checkpoint (240)` |
| Known-good production parent | `ac7c2b8` — `GENIE-V7-REGRESSION-REPAIR-1` |
| Recovery doc | `results/240_map_current_pre_genie_merge_audit.md` |

To restore pre-Genie-merge production map behavior:

```bash
git checkout map_current_pre_genie_merge -- map_CURRENT.html
```

The tag is the single recovery anchor. It documents authoritative pre-merge flows (search, overlay, save, replay) at baseline `ac7c2b8`.

---

## Commits — Stage 2A through Stage 4A

Integration work spans audit checkpoint **240** through **Stage 4A**. Commits on `main` from rollback tag to head of this track:

| Stage | Commit | Message |
|-------|--------|---------|
| **240 (checkpoint)** | `495b6e6` | audit: map_current pre-genie-merge recovery checkpoint (240) |
| **2A** | `aa6234f` | genie: port v7 builder UI (2A) and Stage 2C visual cleanup |
| **3B Slice 1** | `9ab045d` | genie: add gv→genie_render payload mapper (Stage 3B Slice 1) |
| **3B Slice 2** | `38c5196` | genie: wire gv Search Map to executeGenieRender (Stage 3B Slice 2) |
| **3B Slice 3** | `1ecf13e` | genie: route save and ghost snapshots through gv state (Stage 3B Slice 3) |
| **3C Slice 4A** | `5bf3cdc` | genie: rehydrate gv builder from saved conditions (Stage 3C Slice 4A) |
| **4A** | `6393557` | genie: wire gv Save Search to production save path (Stage 4A) |

**Head of track:** `6393557e48ec418aa080bef125997a6f9e55894e`

### Stage summary

| Stage | What shipped |
|-------|----------------|
| **2A** | GV builder UI port (`#gv-builder-host`, scoped `gv-*` CSS/JS, in-memory variables, ghost/bottle shells). Legacy panel hidden, not removed. |
| **2C** | Visual cleanup bundled with 2A (`results/243_genie_stage_2c_cleanup_closeout.md`). |
| **3B-1** | `buildGenieRenderPayloadFromGv()` / `__gvBuildPayloadForTesting` — GV variables → `genie_render` payload. |
| **3B-2** | `#gv-searchBtn` → `runGvSearch()` → `__rmExecuteGenieRender` → `executeSearchPlan` → `POST /search-regions`. |
| **3B-3** | `gvVariablesToConditionSnapshot()`; `snapshotConditions()` + `collectSavedInvestigationConditions()` read GV state; ghost strip matches GV chips. |
| **3C-4A** | `conditionsJsonToGvVariables()`; `__gvBuilderPreview.hydrate()`; `applySavedInvestigationConditions()` hydrates GV + legacy writes. |
| **4A** | `#gv-saveInline` enabled when `variables.length > 0`; click → `__rmSaveCurrentInvestigation()` → existing `POST /saved-investigations/create`. |

**Not in scope of this track:** Stage 2B (no separate commit), save-disk morph, FLIP/bottle motion, legacy DOM removal, sandbox retirement.

---

## Current working flow (production truth)

All user-facing Genie behavior on `map_CURRENT.html` now flows through the GV builder and existing production bridges. Backend routes and `conditions_json` shape are unchanged.

```
┌─────────────────────────────────────────────────────────────────┐
│  #gv-builder-host  (variables[], chips, ghost strip, bottle)    │
└────────────┬───────────────────────────────┬────────────────────┘
             │                               │
    #gv-searchBtn                    #gv-saveInline
             │                               │
             ▼                               ▼
 buildGenieRenderPayloadFromGv()    __rmSaveCurrentInvestigation()
             │                               │
             ▼                               ▼
 __rmExecuteGenieRender()           collectSavedInvestigationConditions()
  → executeGenieRender()              → gvVariablesToConditionSnapshot()
  → executeSearchPlan()                      │
  → POST /search-regions                     ▼
             │                    POST /saved-investigations/create
             ▼                               │
    polygonLayer / aspectLayer               │
    (overlay replay)                         │
                                             ▼
                              applySavedInvestigationConditions()
                               → __gvBuilderPreview.hydrate()
                               → legacy select writes (compat)
                               → buildPlanFromSavedConditions()
                               → executeSearchPlan() (replay)
```

### Search

1. User adds variables in GV builder (Planet–House, Angle–Sign, Aspect–Angle).
2. **Search Map** commits any in-progress draft, maps GV → `genie_render` via `buildGenieRenderPayloadFromGv`, executes through `window.__rmExecuteGenieRender` → `executeSearchPlan` → `POST /search-regions`.
3. Overlays render on `polygonLayer` / `aspectLayer` as before.

### Ghost / snapshot

- Ghost strip tokens derive from GV via `snapshotConditions()` (Slice 3B-3).
- Ghost chips match committed GV variable labels.

### Save

1. **Save search** (`#gv-saveInline`) enabled when at least one GV variable exists.
2. Click sets `window.__gvLastSaveTrigger = "gv-saveInline"` and calls `window.__rmSaveCurrentInvestigation()`.
3. `collectSavedInvestigationConditions()` snapshots GV through `gvVariablesToConditionSnapshot()`.
4. Auto-title `Investigation YYYY-MM-DD HH:MM`; optional note via hidden `#saveInvestigationNote`.
5. `POST /saved-investigations/create` with anchored birth params, viewport, settings snapshot — unchanged backend contract.

### Reopen / replay

1. Saved investigation or quick-share payload → `applySavedInvestigationConditions()`.
2. `conditionsJsonToGvVariables()` + `__gvBuilderPreview.hydrate()` restore GV chips.
3. Legacy overlay selects still written for compatibility.
4. Replay: `buildPlanFromSavedConditions(conditions_json)` → `executeSearchPlan` (primary path). Fallback: `findRegions()` → `buildPlanFromLegacyDom()` if needed.

### Harness / fallback DOM (still present)

- `#saveInvestigationBtn`, `#saveInvestigationNote`, `#saveInvestigationStatus` remain in DOM; CSS-hidden. Wired to same `saveCurrentInvestigation()`.
- `#findBtn` and legacy condition blocks remain in DOM; visually hidden by `hideLegacyShell()`.

---

## What is still legacy

These are intentional carryovers. Production users interact with GV; legacy DOM is compatibility scaffolding.

| Area | Legacy artifact | Why it remains |
|------|-----------------|----------------|
| **Search panel** | `#planetA`, `#angleSignAngle`, `#overlayPlanet`, `.condition-block`, `#findBtn` | Hidden via `hideLegacyShell()`; `buildPlanFromLegacyDom()` replay fallback; `executeSearchPlan` still toggles `#findBtn.disabled` |
| **Save UI** | `#saveInvestigationBtn`, `#saveInvestigationNote` | Hidden via CSS; harness + smoke fallback; same save path as `#gv-saveInline` |
| **Rehydration** | `applySavedInvestigationConditions()` writes legacy `<select>` values | Dual-write until legacy path can be retired |
| **Settings** | `syncGenieBodySelectorsToSettings()` targets `#planetA`, `#planetB`, `#planetC`, `#overlayPlanet` | Settings visibility still wired to legacy selectors |
| **Walkthrough** | Step 2 may target `.condition-block` (hidden) | Not retargeted to `#gv-builder-host` |
| **Motion / chrome** | `#gv-bottle` shell static; no FLIP, no save-disk morph | Visual port only in 2A; motion deferred |
| **Sandbox** | `map_SANDBOX_genie_v7.html` + dev static mounts | QA reference; not production truth |
| **Adapter note** | `genie-render-status-note` re legacyCompatibility | Informational; GV is source of truth for variables |

---

## What is still deferred

Explicitly out of scope for Stages 2A–4A. Do not treat as regressions.

1. **Save UI consolidation** — Remove duplicate save controls; wire save-disk morph from v7 sandbox.
2. **Legacy DOM removal** — Drop hidden `#findBtn` / condition blocks after audit proves no runtime dependency.
3. **executeSearchPlan decoupling** — Stop referencing `#findBtn` for disabled state.
4. **Motion / morph port** — FLIP transitions, bottle persistence, flySave save-disk animation (`GENIE-V7-SAVEDISK-FIX-1` patterns from sandbox).
5. **Walkthrough retarget** — Onboarding step 2 → `#gv-builder-host`.
6. **Sandbox retirement** — Stop using `map_SANDBOX_genie_v7.html` as QA primary; `map_CURRENT.html` is truth.
7. **Human QA pass** — Interactive browser QA on real profiles, z-index/pointer issues after map search (headless locator click on `#gv-saveInline` can miss when map overlay is active; DOM `.click()` works).
8. **Stage 2B** — No dedicated slice landed; any intermediate truth-bridge audit was read-only.

---

## Validation artifacts

| Artifact | Stage | Result | Key evidence |
|----------|-------|--------|--------------|
| `results/241_gv_builder_port_validation.json` | 2A | **34/34 checks pass** | Builder renders; add variable; Search/Save shells present (Save disabled at 2A); bottle shell; no blocking page errors |
| `results/245_gv_slice2_validation.json` | 3B-2 | **PASS** | `gv-searchBtn` trigger; `executed: true`; `POST /search-regions` 200; motion 12/12 |
| `results/246_gv_slice3_validation.json` | 3B-3 | **PASS** | Ghost matches chips; `collectSavedInvestigationConditions()` matches GV snapshot; replay 137 features; motion 12/12 |
| `results/247_gv_slice4a_rehydration_validation.json` | 3C-4A | **PASS** | Chips restore Sun–1st + ASC–Aries; GV search after rehydrate; replay 137 features; quick-share hydrate; motion 12/12 |
| `results/248_gv_slice4a_save_validation.json` | 4A | **PASS** | `gv-saveInline` trigger; `POST /saved-investigations/create` 200; `conditions_json` sun/1st house; reopen chips; replay features; motion 12/12 |

Supporting audit docs (not validation JSON):

- `results/240_map_current_pre_genie_merge_audit.md` — pre-merge baseline
- `results/241_genie_builder_port_audit.md` — 2A port isolation strategy
- `results/243_genie_stage_2c_cleanup_closeout.md` — 2C visual cleanup

**Motion smoke:** all listed artifacts report `PASS 12/12 MAP-PRODUCTION-MOTION-A` (`scripts/smoke_map_production_motion_a.py`).

---

## Next recommended slices

Ordered for lowest risk and highest user-visible payoff:

### 1. Human QA on `map_CURRENT`

Interactive pass with real Supabase profiles: add/edit/remove variables, NOT toggle, solo/mute ghost, search, save, reopen from library, quick-share recipient. Confirm `#gv-saveInline` click hit-testing after map search (panel z-index). File issues only — no code in this slice.

### 2. Legacy DOM removal audit

Read-only dependency map: every caller of `buildPlanFromLegacyDom`, legacy selects, `#findBtn`, `snapshotConditions` legacy path, walkthrough selectors. Gate removal on zero runtime references except explicit fallback.

### 3. Save UI consolidation

Single visible save affordance; retire hidden `#saveInvestigationBtn` from user path (keep harness until smokes migrate). Do not change `conditions_json` or backend route.

### 4. Motion / morph port

Port v7 FLIP, bottle object persistence, save-disk flySave from sandbox. Scope to GV chrome only; do not alter `executeSearchPlan` or overlay math.

### 5. Retire sandbox from QA

Point smokes and manual QA at `map_CURRENT.html` only. Demote `map_SANDBOX_genie_v7.html` to archaeology reference. Remove dev-only static mounts when no longer needed.

---

## Closeout statement

Genie v7 builder UI is integrated into production `map_CURRENT.html` with end-to-end truth wiring:

- **Search** — GV → genie_render → executeSearchPlan  
- **Ghost / snapshot** — GV state  
- **Save** — GV → collectSavedInvestigationConditions → `/saved-investigations/create`  
- **Reopen / replay** — conditions_json → GV hydrate + buildPlanFromSavedConditions  

Rollback remains one tag away. Legacy DOM and duplicate save controls are documented scaffolding, not user-facing product. Motion, morph, and cleanup slices are deferred with explicit next steps above.

**Track complete. No further implementation authorized under GENIE-PRODUCTION-INTEGRATION-CLOSEOUT-1.**
