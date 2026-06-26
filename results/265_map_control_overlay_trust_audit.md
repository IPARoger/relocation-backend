# M1 — Map Control + Overlay Trust Recovery Audit

**Date:** 2026-06-25  
**Status:** Read-first audit complete  
**Scope:** Production map surface (`map_CURRENT.html` served at `/map_CURRENT.html` via `main_centerline_FIXER.py`). No code changes in this pass — inventory, diagnosis, and recovery sequence only.

---

## Executive summary

The **only** production map HTML is **`map_CURRENT.html`**. Alternate map files (`map_SANDBOX_*`, archives, backups) are archaeology and must not be treated as shipping surfaces.

User trust in map controls and overlays has eroded for three independent reasons:

1. **Ghost / Genie control schizophrenia** — The GV builder is **wired** (`runGvSearch` → `__rmExecuteGenieRender` → `executeSearchPlan`) while HTML comments and `aria-label` still claim **“UI-only preview.”** Legacy `planetA`/`planetC` + **`findBtn`** (`findRegions` → `buildPlanFromLegacyDom`) duplicate the same engine path. The explore **ghost strip** shows Mute/Solo/Not affordances; QA **F-8** documented them as **visual-only** (map does not respond). Post–Beta-B code attempts `ghostRedrawFromState()` re-search for NOT/Solo/Mute, but engine v1 still **defers exclude polarity** in `genie_map_engine_adapter.js` while the strip **filters NOT client-side** — a partial, easy-to-misread contract.

2. **Duplicated search entry points** — Users can search from **GV “Search Map”**, **legacy Find regions**, saved-investigation replay, Genie handoff, and ghost redraw. Only one path should be canonical for Beta trust.

3. **Overlay path is correct in substrate choice but jagged at the edges** — Active pipeline: `executeSearchPlan` → `dispatchOverlayRequest` with default **`ACTIVE_RENDERER_SUBSTRATE = LEGACY_SEARCH_REGIONS`** → `POST /search-regions` with **`generation_mode: truth_grid`** (URL override `generation_mode`), **`truth_grid_resolution: 0.75`**, **`truth_grid_boundary_refine: true`**, Leaflet **`smoothFactor: 0`**. Jagged boundaries are **ranked** as truth-grid quantization (0.75° stairs), **aspect staging** (2.0 → 1.0 → 0.5) settling asynchronously, and optional **contour archaeology** if `generation_mode=contour` is forced — **not** missing Leaflet smoothing (cosmetic smoothing is **forbidden**).

**Recovery thesis:** M1 restores *truth in controls* (wire or hide), *truth in overlay metadata* (debug + screenshots), then popup/city readability, chrome polish, and P3 cache — without reintroducing contour/Gaussian cosmetic smoothing.

---

## 1. Ghost / Genie controls

### 1.1 Inventory

| Control / surface | Location | Wired to engine? | Beta vs debug | Notes |
|-------------------|----------|------------------|---------------|-------|
| **GV builder (`#gv-builder-host`)** | `map_CURRENT.html` panel | **Yes** — `runGvSearch()` calls `window.__rmExecuteGenieRender(buildPayload(vars))` | **Beta (production)** | Comment block says “NOT wired”; `aria-label` says “UI-only preview.” **Stale documentation — trust bug.** |
| **`__gvBuildPayloadForTesting`** | `map_CURRENT.html` | **Yes** — maps GV variables → `genie_render` payload | Beta | Bridge name says “Testing”; used in production search. |
| **`executeGenieRender`** | `map_CURRENT.html` | **Yes** → `RelocationGenieMapEngineAdapter.buildEngineExecutionPlan` → `executeSearchPlan` | Beta | Single Genie truth path. |
| **Legacy `planetA` / `planetB` / `planetC` + house selects** | Hidden DOM (GV port hides via JS) | **Yes** via `findBtn` → `buildPlanFromLegacyDom` | **Retire candidate** | Still hydrated for saved investigations; duplicates GV. |
| **`findBtn` (“Find regions”)** | Panel footer | **Yes** — `findRegions()` → `executeSearchPlan(..., legacy_dom)` | **Retire candidate** | Also disabled during any `executeSearchPlan`; hidden for quick-share recipients. |
| **Ghost strip (`#rm-ghost-strip`)** | Map chrome (MAP-UX-4) | **Partial** | Beta | Renders tokens from `activeConditions`; Mute/Solo/Not UI present. |
| **Mute (`data-gmini="mute"`)** | Ghost token row | **Partial** | Beta | Sets `v.mute`, patches GV preview, calls `ghostRedrawFromState()`. Payload sets `enabled: false` for muted vars. Strip shows `.rm-muted` opacity — **display always yes**; filter effect depends on re-search completing. |
| **Solo (`data-gmini="solo"`)** | Ghost token row | **Yes (client filter)** | Beta | Filters `renderList` to solo id before re-execute. Full backend round-trip. |
| **Not (`data-gmini="not"`)** | Ghost token row | **Partial** | Beta | Client omits `not:true` from render list; adapter marks `polarity: exclude` as **deferred** (`exclude_not_supported_in_engine_v1`). **Filters NOT in UI list, not in engine truth — QA F-8 class of false affordance.** |
| **Bottle (`#rm-bottle`)** | Map FAB | **Yes (UX)** | Beta | Exits explore mode; restores panel. |
| **Explore mode (`body.rm-explore`)** | CSS + JS FLIP | **Yes** | Beta | Entered after successful search (wrapper on `executeSearchPlan`); panel collapse + ghost strip reveal. |
| **History back/fwd (`MAP-UX-2`)** | `#rm-ctrl-back` / `#rm-ctrl-fwd` | **Yes** | Beta | Stack max **20**; replays `executeSearchPlan` with `history_replay`. **GV/ghost state not mirrored on replay (PB6-8 deferred).** |
| **Pin (`#rm-ctrl-pin`)** | MAP-UX-2 | **Partial** | Beta | Writes `rm_map_pinned_plan` to **sessionStorage**; `window.rmGetPinnedPlan()`. **No comparison consumer yet.** |
| **Dual city search** | `.rm-citysearch-wrap` | **Yes (navigation)** | Beta | `RMSavedLocationSearchUI.mount` on `#rm-map-loc-search-mount` (`citySearch` input) → `openSavedLocationSearchResult` / chart popup. **`place_search_client.js` loaded** for geocode path inside saved-location service — not a second visible search box, but **two resolution stacks** (favorites/saved vs provider geocode). |
| **Debug: `#debugStatus`** | Map corner | Overlay metadata | **Debug** (`?overlayDebug=1` etc.) | Point-in-polygon checks against `lastDisplayFeatureCollection`. |
| **Debug: `#genieRenderStatus`** | Panel | Genie execution JSON | **Debug** (`?debug=1`) | Birth resolution, degradation, plan shape. |
| **Debug: canonical canvas / dry-run** | `canonicalDebugCanvas` | Shadow only | **Debug** (`canonicalDryRun`, `canonicalVisible`) | `CANONICAL_SCREEN_SPACE` branch throws unless dry-run shadow. |
| **Debug: Aura PoC** | URL flags | Non-canonical overlay | **Debug** | `?rasterAura=1`, `?debugAdaptive=1`, `?debugProgressiveReveal=1`, `?aspectAura=1` — explicitly **not** production substrate. |
| **Walkthrough / onboarding** | `map_CURRENT.html` | N/A | Beta | Step 4 selector mismatch (`ghost-tools` vs `map-ghost-strip`) — teaches controls that may not match behavior (see `results/144_map_qa_pass1.md`). |

### 1.2 Beta vs debug classification

- **Beta (user-facing):** GV builder search, explore chrome (ghost strip, bottle, hamburger menu), MAP-UX-2 history/pin, floating city search, relocated chart popups, production `truth_grid` house overlays, staged aspect contours at 2.0/1.0/0.5.
- **Debug / archaeology (URL-gated or legend-disclaimed):** canonical screen-space dry-run, visible canonical debug canvas, aura raster/progressive PoC, `overlayDebug` click logging, `genieRenderStatus` panel, adaptive aura subdivision display.

### 1.3 Trust defects (controls)

1. **Comment / label lies** — GV builder documented as UI-only while executing full render pipeline.
2. **Dual builder paths** — Legacy DOM + GV both reach `executeSearchPlan`.
3. **Ghost strip** — High-affordance Mute/Solo/Not with **inconsistent semantics** (QA **F-8**: map appeared non-responsive; NOT/engine exclude mismatch remains).
4. **History without ghost hydration** — Back/forward replays plan only; ghost tokens and GV chips can desync.

---

## 2. Overlay rendering

### 2.1 Active production path

```
executeSearchPlan(plan)
  → dispatchOverlayRequest(basePayload)  // substrate default: LEGACY_SEARCH_REGIONS
  → postSearchRegions(payload)           // POST {API_BASE}/search-regions
  → prepareDisplayFeatures(data)
  → renderHouseFeatures(displayData)     // smoothFactor: 0
  → [optional] staged aspect passes via renderSingleOverlayStage
```

**Default payload flags** (house pass):

| Field | Value | Source |
|-------|-------|--------|
| `generation_mode` | `truth_grid` (default) | `MAP_URL.get("generation_mode") \|\| "truth_grid"` |
| `truth_grid_resolution` | `0.75` | `executeSearchPlan` |
| `truth_grid_boundary_refine` | `true` | `executeSearchPlan` |
| `resolution` | `1.5` | legacy contour field (house pass metadata) |
| Leaflet `smoothFactor` | `0` | `renderHouseFeatures`, aspect layers, aura GeoJSON |

Backend mirror: `main_centerline_FIXER.py` `SearchRegionsRequest` defaults `generation_mode="contour"` on model, but client sends `truth_grid`; `generate_truth_grid_house_features(..., truth_grid_resolution, ..., truth_grid_boundary_refine)` when mode is `truth_grid`.

### 2.2 Quarantined / non-production paths

| Path | Status |
|------|--------|
| **`RENDERER_SUBSTRATES.CANONICAL_SCREEN_SPACE`** | Dry-run / shadow only. `dispatchOverlayRequest` throws if selected without `ENABLE_CANONICAL_DRY_RUN`. |
| **`ENABLE_CANONICAL_DRY_RUN`** | Runs parallel canonical request; **never paints** canonical result in production. |
| **`ENABLE_CANONICAL_VISIBLE_DEBUG`** | Optional debug canvas overlay when `?canonicalVisible=1`. |
| **Aura / progressive** | `useRasterAura`, `useAdaptiveAura`, `debugProgressiveRevealMode` — **URL-flag only**; legend states not canonical production substrate. |
| **Contour `generation_mode`** | Backend archaeology: Gaussian + `find_contours` — **rejected** for trust; must not return as default. |

### 2.3 Jagged edge diagnosis (ranked)

| Rank | Hypothesis | Evidence | Mitigation (no cosmetic smoothing) |
|------|------------|----------|-------------------------------------|
| **1** | **Truth grid 0.75° quantization** | Client pins `truth_grid_resolution: 0.75`; rectangular run-merge produces stair-step boundaries along lat/lon grid. | Accept as truth artifact OR reduce resolution only with performance budget + metadata disclosure (not Leaflet smooth). |
| **2** | **Aspect staging (2.0 → 1.0 → 0.5)** | `executeSearchPlan` loops `renderSingleOverlayStage` for staged contour overlays; user may see coarse edges before final pass completes. | UI “settling” state; await final stage before declaring “ready”; screenshot audits at stage boundaries. |
| **3** | **`smoothFactor: 0` intentional** | All house/aspect GeoJSON layers set `smoothFactor: 0`. | **Do not** “fix” with Leaflet smoothing — violates doctrine. |
| **4** | **Display clipping ±65°** | Product policy cap on display features; backend truth unchanged. | Ensure popups/polar cap messaging consistent (already partially implemented). |
| **5** | **Contour archaeology** | If URL forces `generation_mode=contour`, backend uses smoothing pipeline (`main_centerline_FIXER.py` comments ARCHAEOLOGY). | Guardrails in smoke tests: assert `truth_grid` in production requests. |
| **6** | **Boundary refine artifact** | `truth_grid_boundary_refine: true` may expose refine seams vs raw grid. | Compare feature `boundary_refined` property in debug panel; A/B only with metadata. |

**Forbidden:** Cosmetic smoothing (Leaflet `smoothFactor > 0`, splines, blur masks) to hide grid stairs.

---

## 3. Progressive / cache

### 3.1 Current house + aspect behavior

- **House overlay:** Single pass per search (no client-side progressive house refinement in production).
- **Aspect overlay (staged):** When `isStagedContourAngleOverlay`, three resolutions **2.0 / 1.0 / 0.5** (`aspect_resolution` per stage) — this is **staging**, not Phase-2 cache scheduler.

### 3.2 `phase2_cache_scheduler.js`

- **Exists** as extracted module from sandbox (`createPhase2CacheScheduler`, `cacheKey()` with sorted conditions + `birthKey`).
- **NOT wired** in `map_CURRENT.html` — renderer proof gates reference `scheduler_cache_execution: false` and `failedGates` may include `cache_scheduler_safety` when adapter expectations unmet.
- **Safe pattern:** Keys are JSON-stable; conditions sorted; host owns viewport point construction.

### 3.3 Intake prewarm (feasibility)

- Chart birth resolution already flows through **`chart_record`** / `fetchEngineBirthForChartRecord` and Genie `resolveBirthParamsForGenieRender`.
- **Feasible P3:** On profile/chart selection (intake or library handoff), prewarm cache entries keyed by `{ chart_record_id, birthKey, conditions hash }` for viewport-independent house truth — **only after** M1-B overlay trust restored and scheduler wired behind feature flag.

---

## 4. Popup plan — “View overlays here”

### 4.1 Reverse discovery (recommended UX)

**Goal:** From a **location** (map click or city), show which **planet-in-house** conditions the user’s **active search** would satisfy at that point — without inventing new ranking heuristics.

**Data already on map:**

1. `openDatasetCityPopup` / map click → `fetchRelocatedChart(lat, lon)` → `buildRelocatedPopupHtml`.
2. `buildPlanetHouseRowsFromData(data)` reads **`canonical_chart.planets[*].house`** — authoritative relocated houses at point.
3. Active search conditions live in **`executeSearchPlan` plan** / GV snapshot (`gvVariablesToConditionSnapshot`, `window.__gvBuilderPreview.variables`).

**Proposed flow (M1-C):**

1. User opens popup at `(lat, lon)` with chart loaded.
2. New action **“View overlays here”** lists **intersection** of:
   - `planet_in_house` conditions in current plan (not muted/not-excluded per ghost rules), and
   - planets whose **relocated house** at this point matches the condition house.
3. **No ranking** — stable order: plan order or planet table order.
4. User picks one row → call existing **`executeSearchPlan`** with **that single condition** (or highlight-only mode if multi-overlay policy forbids re-search) — prefer **highlight** first to avoid surprise full re-render.

### 4.2 Files to touch (implementation phase)

| File | Role |
|------|------|
| `map_CURRENT.html` | Popup HTML (`buildRelocatedPopupHtml`), plan access, `executeSearchPlan` entry |
| `genie_map_engine_adapter.js` | Ensure single-condition plans map cleanly to engine (already supports variable lists) |
| Optional: extract popup overlay matcher to small JS module if `map_CURRENT.html` size is a constraint |

### 4.3 Non-goals

- No ML ranking of “best” overlays.
- No new backend endpoint for popup — use existing relocated chart + in-memory plan.

---

## 5. City readability

### 5.1 Current `renderCities()` behavior

- **Source:** `citiesData` dataset; **OSM** base map via `L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")`.
- **Filtering:** Zoom-tiered **population thresholds** (e.g. z≤3 → 5M, …, z≤8 → 50k).
- **Markers:** Uniform **`L.circleMarker`** — radius 4 (z<7) or 6 (z≥7); white fill, dark stroke; **no text labels**.
- **Viewport:** `bounds.contains` culling on `moveend`.

### 5.2 Issues

| Issue | Symptom | Severity |
|-------|---------|----------|
| Weak major/minor distinction | Capital vs town looks identical modulo radius step | Medium |
| **Bubble cloud z7–8** | Many 50k+ cities in dense regions — overlapping dots | High |
| No label at useful zooms | Users cannot correlate dot with name without click | Medium |
| Contrast on OSM | White fill can wash out on pale tiles | Low |

### 5.3 Recommendations (M1-C)

1. **Tiered markers** — pop buckets: mega (stroke weight 3), major, minor; optional ring for admin capitals if dataset flags exist.
2. **Viewport cap** — max N markers per frame (e.g. 200), prefer highest pop in view.
3. **Labels** — optional `L.tooltip` permanent only for top-K pop at z≥8; otherwise keep click-for-popup.
4. **Do not** change overlay engine for city layer — pure Leaflet presentation.

---

## 6. Chrome / browser state

### 6.1 Implemented (MAP-UX-2 / MAP-UX-4)

| Mechanism | Behavior |
|-----------|----------|
| **History stack** | 20 entries; wraps `executeSearchPlan`; truncates forward branch on new search |
| **Pin** | `sessionStorage` key `rm_map_pinned_plan`; visual `.rm-ctrl-pinned` |
| **Map routing** | Separate page `/map_CURRENT.html` — **not** app-shell hash route for map body |
| **Browser back** | Exits map page (standard history) — **does not** map to in-map history stack |
| **Explore chrome** | Panel FLIP hidden; ghost strip + bottle + hamburger; city search collapses to mini until hover (`body.rm-explore .rm-citysearch-wrap`) |

### 6.2 Gaps

| Gap | Impact |
|-----|--------|
| **Explore chrome treatment** | Panel hidden but legacy `findBtn` / hidden selects still in DOM — risk of harness confusion |
| **Pin consumer** | No comparison workspace reads `rmGetPinnedPlan()` |
| **Notes in explore** | Investigation notes / save affordances partially hidden (`#gv-saveInline` hidden in explore; save disk morph) — users may not find save |
| **popstate / GV hydration** | PB6-8 deferred — browser back on map page ≠ in-map history |
| **Walkthrough** | Ghost strip steps may not run in explore timing |

---

## 7. Prioritized sequence

| Phase | ID | Focus | Deliverables |
|-------|-----|-------|--------------|
| **1** | **M1-A Control truth** | Wire or hide ghost filters; retire legacy `findBtn`/DOM path; fix stale UI-only comments and aria labels | Single search CTA; NOT/Solo/Mute either fully engine-backed or hidden; remove duplicate `findRegions` from user path |
| **2** | **M1-B Overlay trust** | Metadata debug, screenshot audit, staging settle messaging; **no smoothing** | `overlayDebug` / feature props documented; Playwright captures at final aspect stage; smoke asserts `truth_grid` + `smoothFactor: 0` |
| **3** | **M1-C Popup + cities** | “View overlays here”; tiered city markers + viewport cap | Popup matcher; city readability pass |
| **4** | **M1-D Chrome polish** | Explore save path, pin/history clarity, walkthrough selectors | PB6-8 decision: implement or hide back/fwd until hydrated |
| **5** | **M1-E Cache progressive (P3)** | Wire `phase2_cache_scheduler.js` behind flag; intake prewarm | chart_record-keyed cache; scheduler gates green |

---

## 8. Validation plan

### 8.1 Static smoke — `scripts/smoke_m1_map_trust.py` (to add)

- Assert `map_CURRENT.html` contains exactly one production `executeSearchPlan` definition path wired to `/search-regions`.
- Regex scan: `truth_grid_boundary_refine: true`, `truth_grid_resolution: 0.75`, `smoothFactor: 0`.
- Fail if `generation_mode` default drifts to `contour` without URL guard.
- Verify `runGvSearch` references `__rmExecuteGenieRender` and flag stale “UI-only” comment for CI warning (optional gate).

### 8.2 Playwright

- Load `/map_CURRENT.html` with test profile + chart fixture.
- GV search → wait `setRenderStatus` house ready → screenshot overlay bounds.
- Toggle ghost NOT/Solo — assert network `search-regions` call count and plan payload shape.
- Aspect search — screenshots at coarse/medium/final stage timestamps.
- City layer: count circle markers at z7/z8 under cap policy once implemented.

### 8.3 Popup truth

- Open known city; assert `buildPlanetHouseRowsFromData` houses match API `canonical_chart`.
- Future: “View overlays here” list length equals deterministic match against frozen fixture.

### 8.4 Route / history checks

- Navigate to map from app shell; `history.back()` leaves map (document title/URL).
- In-map back button replays prior plan (`source: history_replay`) without double-push to stack.
- Pin → reload → `rm_map_pinned_plan` present in sessionStorage.

### 8.5 Screenshot audit artifacts

- Store under `validation/mockups/beta/screenshots/m1_map_trust/` (mirror v5 parity audit layout).
- Side-by-side: same plan, final stage only, ±65° clip boundary visible.

---

## 9. Files examined

| File | Relevance |
|------|-----------|
| `map_CURRENT.html` | Production map — controls, overlays, ghost strip, cities, popups, executeSearchPlan |
| `genie_map_engine_adapter.js` | Genie → engine plan; exclude/transit degradation |
| `main_centerline_FIXER.py` | `/map_CURRENT.html` route; `/search-regions`; truth_grid vs contour |
| `truth_field_regions.py` | Truth grid benchmarks; merge metadata |
| `phase2_cache_scheduler.js` | Cache scheduler (unwired) |
| `place_search_client.js` | `RMPlaceSearch` geocode API |
| `saved_location_search_ui.js` | Floating city search UI mount |
| `saved_location_search_service.js` | Saved + provider search orchestration |
| `results/144_map_qa_pass1.md` | QA F-8 ghost strip / Mute-Solo-Not findings |
| `results/135_map_ux_source_truth_audit.md` | UX chrome migration context |
| `results/241_genie_builder_port_audit.md` | GV builder port history |
| `validation/reports/truth_grid_integration_validation.json` | Truth grid integration evidence |
| `validation/reports/async_overlay_decoupling_note.md` | Overlay async notes |
| `docs/design/control_and_action_doctrine_audit.md` | Control doctrine |
| `docs/architecture/PROFILE_TO_MAP_WIRING_AUDIT.md` | Profile → map wiring |

---

## Appendix A — Key code anchors (for implementers)

- GV search wiring: `runGvSearch` → `__rmExecuteGenieRender` (~L2146+ in `map_CURRENT.html`).
- Overlay dispatch: `dispatchOverlayRequest` / `executeSearchPlan` (~L8063, ~L8222).
- Ghost redraw: `ghostRedrawFromState` (MAP-GHOST-B, ~L9937+).
- History: `initMapControls` MAP-UX-2 (~L9140+).
- Cities: `renderCities` (~L5699).
- Popup houses: `buildPlanetHouseRowsFromData` (~L4233).

---

*End of M1 read-first audit.*

---

## M1-B implementation closeout (2026-06-25)

**Commit slice:** `map: improve overlay trust instrumentation`  
**Smoke:** `scripts/smoke_m1b_overlay_truth.py`

### What shipped

Lightweight overlay trust instrumentation in `map_CURRENT.html`:

| Surface | Purpose | Normal UI? |
|---------|---------|------------|
| `window.__rmOverlayTrust` | Frozen snapshot after each render phase | No |
| `html[data-overlay-phase]` | `idle` · `rendering` · `settling` · `final` | No (DOM hook only) |
| `html[data-overlay-ready]` | House regions painted; aspect may still settle | No |
| `html[data-overlay-stage]` | Current aspect stage name (`coarse`/`medium`/`final`) | No |
| `html[data-overlay-final]` | `true` only when final stage complete | No |
| `rm-overlay-ready` / `rm-overlay-stage` / `rm-overlay-final` | Playwright `waitForEvent` hooks | No |
| `#debugStatus` extra rows | generation_mode, substrate, boundary_refine, phase | Only `?debugGeometry=1` |

Metadata fields: `generation_mode`, `truth_grid_resolution`, `truth_grid_boundary_refine`, `boundary_refined` (from feature properties), `renderer_substrate`, stage index/total, `final_complete`.

### Why jagged edges are expected (not bugs)

House overlays use **truth_grid** at **0.75°** with **`smoothFactor: 0`**. Polygon vertices follow grid cell boundaries — stair-steps are **truth artifacts**, not missing anti-aliasing. Aspect overlays for ASC/DSC/IC may pass through **coarse → medium → final** (2.0° / 1.0° / 0.5°); intermediate frames look rougher than the settled final.

### Why smoothing is forbidden

`contour` mode (Gaussian mask + `find_contours`) is **archaeology** in `main_centerline_FIXER.py`. Leaflet smoothing would change visible geometry without changing astrological truth. Beta contract: show engine output faithfully.

### QA: determining final render completion

**Do not screenshot during `settling`.** Wait for any of:

1. `html[data-overlay-final="true"]`
2. `window.__rmOverlayTrust.final_complete === true`
3. `page.waitForEvent('rm-overlay-final')` (Playwright)

House-only searches: `rm-overlay-final` fires immediately after `rm-overlay-ready`. Staged aspect searches: wait for `rm-overlay-final` after up to three `rm-overlay-stage` events.

**Playwright example:**

```javascript
await page.goto(mapUrl);
await page.click("#gv-searchBtn");
await page.waitForFunction(() => document.documentElement.getAttribute("data-overlay-final") === "true");
```

Optional debug: add `?debugGeometry=1` to read `#debugStatus` overlay phase rows.

### Unchanged (per constraints)

- No renderer rewrites, contour smoothing, `smoothFactor` changes, or truth-grid algorithm changes
- No normal-user UI redesign

---

## M1-C implementation closeout

**Smoke:** `scripts/smoke_m1c_popup_city_readability.py` (includes M1-A + M1-B regression)

### Popup — View overlays here

- Button on every chart-success popup (`buildRelocatedPopupHtml`)
- Expands inline list derived from `canonical_chart.planets[*].house` in **CANONICAL_PLANET_ORDER**
- Row click → `buildPlanForPopupOverlayDiscovery` → `executeSearchPlan({ source: "popup_overlay_discovery" })`
- GV + ghost sync via `__rmSyncGhostFromReplayedPlan`
- No ranking, scoring, or recommendation copy

### City readability

- `CITY_VIEWPORT_CAP_BY_ZOOM` caps markers per zoom (14–60), highest population wins
- `getCityMarkerTier`: major (≥1M), mid (≥250k), minor (≥50k)
- Distinct radius/weight/color per tier; permanent tooltip labels for **major** only at z≥5

---

## M1-D implementation closeout

**Smoke:** `scripts/smoke_m1d_map_chrome_history.py`

### Explore chrome
- Save disk (`#rm-save-disk`, `data-role="map-save-search"`) visible in explore; opens save dialog (title + notes).
- Hamburger menu adds **Save investigation** (`data-role="map-explore-save-menu"`) in explore.
- Legacy `#saveInvestigationBtn` / `#saveInvestigationNote` hidden from map surface.
- Bottle title clarifies reopening Genie exits explore layout.

### Pin
- Stores current search **plan JSON** in `sessionStorage` key `rm_map_pinned_plan`.
- `aria-pressed` + `rm-ctrl-pinned` + label toggles Pin search / Pinned.
- Copy states **browser session** scope (no Comparison consumer yet).
- `window.rmGetPinnedPlan()` / `__rmPinStorageKey` exported.

### History
- `replayAt` awaits `executeSearchPlan` with `source: history_replay`.
- Stack push skips when `meta.source === history_replay`.
- `syncGhostFromReplayedPlan` runs after replay completes.

### Walkthrough
- Genie step → `#gv-builder-host`; ghost step → `map-ghost-strip` (Mute/Solo only); removed stale `ghost-tools` / `.condition-block`.
- Notes step → `data-role="map-notes"` on save dialog textarea.

