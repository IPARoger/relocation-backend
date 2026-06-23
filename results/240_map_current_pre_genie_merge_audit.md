# 240 — map_CURRENT.html Pre-Genie-Merge Recovery Audit

**Mode:** Audit + Checkpoint only. No production behavior changed.
**Purpose:** Establish a recoverable protection checkpoint of the production
relocation truth surface (`map_CURRENT.html`) **before** any Genie v7
motion/UI integration touches it.

---

## Checkpoint identity

| Item | Value |
|------|-------|
| Protection tag | `map_current_pre_genie_merge` |
| Production baseline commit | `ac7c2b8` — `GENIE-V7-REGRESSION-REPAIR-1: restore identity stamp positioning after 056840e regression` |
| Audit commit | this commit (tag target; parent = `ac7c2b8`) |
| Date | 2026-06-23 |

> The tag is the single recovery anchor. It points at the audit commit, whose
> parent is the known-good production baseline `ac7c2b8`. Rolling back to the
> tag restores production code to its pre-merge state and carries these
> recovery instructions with it.

### Uncommitted at checkpoint time (intentionally NOT committed)

These were already modified in the working tree before this audit and are
dev-server conveniences, not production behavior. They are left uncommitted by
this checkpoint per the "no backend work / audit only" constraint:

- `main_centerline_FIXER.py` — static route for `map_SANDBOX_genie_v7.html`
  + `/vendor`, `/theme`, `/validation` static mounts (local sandbox serving).
- `TRANSFER_NEXT_GPT_RENDERER_HANDOFF.md` — handoff notes.

---

## Production flows documented (as-is, authoritative)

All line numbers refer to `map_CURRENT.html` at baseline `ac7c2b8`.

### 1. Search Map flow

Three entry points, all converging on `executeSearchPlan()`:

- **Legacy DOM panel:** `#findBtn` -> `findRegions()` (L7118) ->
  `buildPlanFromLegacyDom()` -> `executeSearchPlan(plan, {source:"legacy_dom"})`.
- **Genie render:** `executeGenieRender(payload)` (L7056) ->
  `RelocationGenieMapEngineAdapter.validateGenieRender()` ->
  `resolveBirthParamsForGenieRender()` -> `adapter.buildEngineExecutionPlan()` ->
  `executeSearchPlan(plan, {source:"genie_render"})`. Exposed for harness as
  `window.__rmExecuteGenieRender`.
- **App-shell handoff:** `maybeExecuteGenieRenderHandoff()` (L7132, URL
  `?handoff=app_shell`) loads a handoff payload -> `executeGenieRender()`.

### 2. Overlay generation flow

`executeSearchPlan(plan, meta)` (L6922):
1. Disables `#findBtn`, clears `polygonLayer` / `aspectLayer` / `auraLayer`.
2. Builds `basePayload` from `plan.birth` + `plan.house_conditions` +
   `plan.angle_sign_conditions`, with `resolution:1.5`,
   `generation_mode:"truth_grid"`, `truth_grid_resolution:0.75`,
   `truth_grid_boundary_refine:true`.
3. `dispatchOverlayRequest(basePayload)` (L6766) -> `postSearchRegions(payload)`
   (L5858) -> `fetch(API_BASE + "/search-regions", POST)` (`API_BASE=''`,
   same-origin) -> GeoJSON `FeatureCollection`.
4. `prepareDisplayFeatures(data)` -> `renderHouseFeatures(displayData)` (L5739)
   renders polygons via `L.geoJSON` on `polygonLayer`.
5. Aspect overlay (if present) runs staged (coarse 2.0 / medium 1.0 / final 0.5)
   -> `renderAspectFeatures()` (L5786) on `aspectLayer`.

### 3. Save investigation flow

- `collectSavedInvestigationConditions()` (L1995) builds `conditions_json`
  (house_conditions, angle_sign_conditions, aspect_overlay) with anchored birth
  params + `chart_record_id`.
- Captures `viewport_json` and `settings_snapshot_json`
  (`RMSettings.buildSettingsSnapshot()`, falls back to `{}`).
- Reads Supabase session token -> `POST /saved-investigations/create` (L2148)
  with `Authorization: Bearer <token>`, body `{profile_id, title,
  search_type:"map", conditions_json, viewport_json, settings_snapshot_json}`.
- Optional note is a secondary write (`#saveInvestigationNote`); its failure
  does not undo the save.

### 4. Reopen / replay flow

- `buildPlanFromSavedConditions(conditionsJson)` (L6874): uses anchored birth
  (`chart_record_id` + `birth_*` when present; else
  `getBirthParamsFromProfile()` legacy fallback), maps stored conditions ->
  `{source:"saved_investigation_json", birth, house_conditions,
  angle_sign_conditions, aspectOverlay}`.
- Replay calls `executeSearchPlan(savedPlan, ...)` (L2375, L2798).
- History replay: `window.executeSearchPlan(entry.plan,
  {source:'history_replay'})` (L7728); `enterExplore()` is skipped for
  `history_replay` (L8155).

### 5. Onboarding behavior

- `skipOnboarding` (L1628) is true when the URL has `skipOnboarding` **or** any
  debug flag (debugGeometry, traceConditions, overlayDebug, aura/adaptive/
  progressive/noLatCap modes).
- Map onboarding card (L2916): shown unless
  `sessionStorage["rm_map_onboarding_dismissed"] === "1"` or `skipOnboarding`.
  Dismiss persists to `sessionStorage`.

### 6. Auth behavior

- `auth_guard.js` loaded in `<head>` (L1104): waits for `window.SupabaseReady`,
  checks for an active Supabase session; if none -> immediate redirect to
  `/auth.html` **before** rendering or data fetching.
- Exposes `window.logout()`.
- Observed live: with no session, `GET /profiles` -> `401` -> redirect to
  `/auth.html`, which aborts any in-flight `fetch` (this is the auth gate that
  blocks unauthenticated browser harnesses -- see validation notes).

---

## Validation -- current production functionality

Server: `uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8004`
(`.env.staging` sourced).

| # | Check | Command | Result |
|---|-------|---------|--------|
| 1 | Static motion-permanence | `scripts/smoke_map_production_motion_a.py` | **PASS 12/12** |
| 2 | `map_CURRENT.html` serves | `curl .../map_CURRENT.html?skipOnboarding=1` | **PASS** (HTTP 200) |
| 3 | **Overlay generation** | `POST /search-regions` (sun in 1st) | **PASS** -- HTTP 200, `FeatureCollection`, **278 features** (also logged 3x server-side) |
| 4 | **Save** (backend) | `scripts/smoke_saved_investigations.py` -> `be_create` | **PASS** (200, id returned) |
| 5 | Save birth-anchored | same -> `be_birth_anchored` | **PASS** |
| 6 | Save rename/archive/auth | same -> `be_rename`,`be_archive`,`be_already_archived`,`be_invalid_profile_404`,`be_cross_account_404`,`be_unauth_401` | **PASS** (all) |
| 7 | **Save** (frontend) | same -> `fe_map_save`, `fe_map_save_note` | **PASS** |
| 8 | FE rename/archive/no-reload | same -> `fe_rename`,`fe_archive`,`fe_no_reload` | **PASS** |
| 9 | **Replay** | same -> `fe_replay` | **PASS** ("Reopened: ...") |
| 10 | Console-error gate | same -> `fe_no_console_errors` | **FAIL** -- non-functional: `[RMSettings] defaults not loaded` settings-load timing warning. Does not affect save/replay. |
| 11 | Genie render path (browser) | `scripts/smoke_genie_map_engine.py` | **FAIL (harness/auth)** -- unauthenticated page redirected to `/auth.html` (`GET /profiles 401`), aborting the `/search-regions` fetch ("Failed to fetch"). Endpoint reachability proven independently in check #3. |
| 12 | Full map smoke (browser) | `scripts/smoke_map_current.py` | **FAIL (harness/UI)** -- `#findBtn` click intercepted by `#rm-bottle` motion overlay (pointer-events). Not a backend regression. |

### Required proofs

- **Search still works:** YES -- code path intact; `POST /search-regions`
  reached and returned 200 (server log) before the unauthenticated redirect.
- **Overlay rendering still works:** YES -- 278 features returned and rendered
  via `renderHouseFeatures` (`L.geoJSON`).
- **Save still works:** YES -- `be_create` + `fe_map_save` + `fe_map_save_note`
  all PASS (real `POST /saved-investigations/create`).
- **Replay still works:** YES -- `fe_replay` PASS ("Reopened").

### Known harness caveats (pre-existing, not regressions)

- Browser smokes require an authenticated Supabase session; without one,
  `auth_guard.js` redirects to `/auth.html` and aborts in-flight fetches.
  (`smoke_saved_investigations.py` injects a staging session and therefore
  passes its FE checks.)
- `smoke_map_current.py` click on `#findBtn` is intercepted by the revealed
  `#rm-bottle` motion element -- relevant to Stage 2/5 of the integration plan.

---

## Rollback instructions

To restore production to this pre-Genie-merge checkpoint:

```bash
# Inspect the checkpoint
git show map_current_pre_genie_merge --stat

# Safe rollback (keeps a branch pointer; review before reset)
git checkout map_current_pre_genie_merge

# Hard rollback of the working branch to the checkpoint
git reset --hard map_current_pre_genie_merge
```

Production baseline (parent of the tagged audit commit) is `ac7c2b8`. To roll
back only the production code and discard the audit commit as well:

```bash
git reset --hard ac7c2b8
```

> Note: the uncommitted `main_centerline_FIXER.py` / handoff-doc edits listed
> above are not part of this tag. A hard reset will revert tracked-file
> modifications; stash them first (`git stash`) if you need to keep them.
