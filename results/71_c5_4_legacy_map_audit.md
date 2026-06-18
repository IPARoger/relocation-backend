# C5-4 Legacy Map Block Audit — map_CURRENT.html

**Roadmap ID:** C5-4
**Date:** 2026-06-18
**Auditor:** Read-only static analysis (no file modifications made)
**Method:** grep + targeted line reads (≤10 reads, ≤20 lines each)

---

## 1. Legacy Blocks Inventory

### Group A — LEGACY_SEARCH_REGIONS / Search Substrate

| Line(s) | Symbol / Block | Classification | Notes |
|---------|---------------|---------------|-------|
| 1054–1057 | `RENDERER_SUBSTRATES` const + `ACTIVE_RENDERER_SUBSTRATE = RENDERER_SUBSTRATES.LEGACY_SEARCH_REGIONS` | **LIVE** | Production renderer is permanently set to the legacy substrate. `CANONICAL_RENDERER_BRANCH_ACTIVE = false` (line 1058). |
| 2601 | `if (ACTIVE_RENDERER_SUBSTRATE !== RENDERER_SUBSTRATES.LEGACY_SEARCH_REGIONS)` | **LIVE** | Production smoke-check gate — fails if substrate deviates; pushes `"production_path_unchanged"` to `failedGates`. |
| 2704 | `legacySearchRegionsActive: ACTIVE_RENDERER_SUBSTRATE === RENDERER_SUBSTRATES.LEGACY_SEARCH_REGIONS` | **LIVE** | Telemetry field in production smoke object. |
| 5661–5672 | `dispatchOverlayRequest()` → LEGACY_SEARCH_REGIONS branch → `postSearchRegions(payload)` | **LIVE** | **This IS the production overlay pipeline.** Called for every map render. |

**IMPORTANT:** `LEGACY_SEARCH_REGIONS` is NOT a dead legacy artifact — it is the active production renderer substrate. The "legacy" name reflects its origin relative to the planned canonical renderer.

---

### Group B — Shadow Comparison Suite

| Line(s) | Symbol / Block | Classification | Notes |
|---------|---------------|---------------|-------|
| 4827–4834 | `summarizeLegacyShadowResult(legacyData, elapsedMs)` | **LIVE** | Called inside `dispatchOverlayRequest()` on every production request. Returns status, featureCount, generationMode, elapsedMs. |
| 4880–4902 | `summarizeShadowComparison(legacySummary, canonicalSummary)` | **PARTIAL** | Called only from `runCanonicalDryRun()`, gated by `ENABLE_CANONICAL_DRY_RUN = MAP_URL.has("canonicalDryRun") || ENABLE_CANONICAL_VISIBLE_DEBUG`. Not active in normal production. |
| 4968–4975 | `compileLegacyGeometryIndex(legacyGeojson)` | **PARTIAL** | Called only from `summarizeCanonicalLegacyParity()`, gated by `ENABLE_CANONICAL_VISIBLE_DEBUG` (`?canonicalVisible` URL flag). |
| 5016–5029 | `legacyIndexContainsPoint(legacyIndex, point, thresholdPx)` | **PARTIAL** | Called only from `summarizeMaskParity()`, URL-flag gated. Point-in-polygon check against legacy geometry index. |
| 5042–5092 | `summarizeMaskParity(points, masks, legacyGeojson, options)` | **PARTIAL** | Called only from `summarizeCanonicalLegacyParity()`, URL-flag gated. |
| 5096–5127 | `summarizeCanonicalLegacyParity(dryRunPayload, canonicalBody, refinement, legacyGeojson)` | **PARTIAL** | Guarded: `if (!ENABLE_CANONICAL_VISIBLE_DEBUG || !legacyGeojson) return null`. URL-flag gated. |
| 5585–5636 | `runCanonicalDryRun(payload, legacySummary, legacyGeojson)` | **PARTIAL** | Gated by `ENABLE_CANONICAL_DRY_RUN`. Never renders canonical output to production UI. |

**⚠️ OVERLAY FLAG — DO NOT REMOVE:** The shadow comparison suite receives `legacyGeojson` (the raw GeoJSON from `postSearchRegions`) for geometry parity analysis. These functions process the same data that drives production overlays.

---

### Group C — Legacy DOM / buildPlanFromLegacyDom

| Line(s) | Symbol / Block | Classification | Notes |
|---------|---------------|---------------|-------|
| ~5742–5758 | `buildPlanFromLegacyDom()` | **LIVE** | Primary production path. Reads DOM form controls; returns `{ source: "legacy_dom", birth, house_conditions, angle_sign_conditions, aspectOverlay, degradation }`. Called by `findRegions()`. |
| 5998 | `await executeSearchPlan(plan, { source: "legacy_dom" })` | **LIVE** | Direct call site inside `findRegions()` — the main "Find Regions" user action. |
| 1940 | `window.__rmSavedInvestigationReplaySource = "legacy_dom"` | **LIVE** | Set in fallback branch of saved-investigation replay when saved conditions JSON build fails. Telemetry tag only; not a control flow branch. |

---

### Group D — App Shell / Library Handoff

| Line(s) | Symbol / Block | Classification | Notes |
|---------|---------------|---------------|-------|
| 421–433 | CSS: `.library-handoff`, `.app-shell-handoff`, `.app-shell-handoff-*` classes | **LIVE** | Styles for active handoff UI panels in the sidebar. |
| 945–953 | HTML: `#libraryHandoff`, `#appShellHandoff` DOM elements | **LIVE** | Rendered in sidebar; shown/hidden by JS on handoff detection. |
| 984–992 | `readAppShellHandoff()` | **LIVE** | Reads URL params `handoff=app_shell`, `chartRecordId`, `placeId`, `explorationId`, etc. Stored as `lastAppShellHandoff`. |
| 998–1044 | Genie render handoff v2 — `readGenieRenderRefFromUrl()`, `loadGenieRenderPayloadFromHandoff()` | **LIVE** | sessionStorage side-channel for same-tab genie render navigation. |
| 1334–1345 | Library chart handoff application → select update | **LIVE** | Applies active chart from URL/session to dropdown; stores in sessionStorage. |
| 1382–1392 | Active profile handoff application | **LIVE** | Applies active profileId from URL/session to profile dropdown. |
| 1444–1449, 1801–1809 | Library/view handoff application in chartProfilesLoaded flow | **LIVE** | Matches handoff ID to library charts/views after library state loads. |
| 3504–3512 | `handoffChartRecordIdForBirth()` | **LIVE** | Returns `lastAppShellHandoff.chartRecordId` when `handoff=app_shell`. Used in birth data resolution. |
| 6002–6010 | `maybeExecuteGenieRenderHandoff()` | **LIVE** | Dispatches genie render from sessionStorage payload on page load. |

No handoff paths are dead. All are active production or active debug-path code.

---

### Group E — Other / Disabled

| Line(s) | Symbol / Block | Classification | Notes |
|---------|---------------|---------------|-------|
| 4674–4677 | `renderBellAuraBandsAroundLine(_feature, _color, _aspectKey)` | **DEAD** | Explicitly commented: "Prototype aura bands disabled — see validation/narratives/map_current_qa_cleanup_pass.md". Body is `if (!aspectAuraMode) return;` — exits immediately. No callers observed in production path. |
| 1058 | `CANONICAL_RENDERER_BRANCH_ACTIVE = false` | **DEAD** | Constant defined but never read by any conditional. CANONICAL_SCREEN_SPACE branch in `dispatchOverlayRequest()` throws regardless. Dead assignment. |
| 960 | `legacyCompatibility` reference in UI note string | **N/A** | Appears only in a display string: "Adapter reads variables[] only — not legacyCompatibility." Not a code block; no variable by this name is defined anywhere. |

---

## 2. Overlay Dependency Map

The overlay pipeline has three parallel tracks:

### Track 1 — Aspect/House Overlays (production, always active)
```
DOM controls (overlayPlanet, overlayAspect, overlayAngle selects)
  → getSelectedAspectOverlay()
  → buildPlanFromLegacyDom() or buildPlanFromSavedConditions()
  → executeSearchPlan()
  → dispatchOverlayRequest()
  → [LEGACY_SEARCH_REGIONS branch] → postSearchRegions(payload)
  → raw GeoJSON → renderAspectFeatures() → polygonLayer / aspectLayer (Leaflet)
```

### Track 2 — Aura Overlays (PoC/debug, URL-flag gated)
```
?rasterAura=1 / ?adaptiveAura=1 / ?aspectAura=1
  → renderRasterAuraProgressive() / renderAdaptiveAuraProgressive() / renderAuraFieldProgressive()
  → fetch("/aura-raster") / fetch("/aura-raster-adaptive") / fetch("/aura-field")
  → auraRasterCanvas (HTMLCanvasElement) or auraLayer (Leaflet)
```
Birth data for aura: dynamic from profile chain. `aspect_overlay` hardcoded to `{ planet: "sun", aspect: "conjunction", angle: "ASC" }` within aura functions only.

### Track 3 — Shadow Comparison (debug only, URL-flag gated)
```
?canonicalDryRun=1 or ?canonicalVisible=1
  → runCanonicalDryRun(payload, legacySummary, legacyGeojson)
  → summarizeCanonicalLegacyParity() [if ?canonicalVisible]
  → compileLegacyGeometryIndex(legacyGeojson) → legacyIndexContainsPoint()
  → summarizeMaskParity() → comparison logged / DEV debug overlay container
```
Never renders canonical data to production map.

**Overlay legacy dependency summary:**
- `dispatchOverlayRequest()` routes through `ACTIVE_RENDERER_SUBSTRATE` which is `LEGACY_SEARCH_REGIONS`. Overlays ARE fed by the legacy substrate — intentionally.
- Shadow suite receives overlay GeoJSON output for analysis, does not drive rendering.
- No overlay or aura function references `LEGACY_SEARCH_REGIONS` by name; they go through `dispatchOverlayRequest()`.

---

## 3. Birth Data Source Location and Type

**Type: Dynamic — NOT hardcoded inline.**

Birth data is resolved at render-time via a priority waterfall:

| Priority | Path | Lines | Mechanism |
|----------|------|-------|-----------|
| A (primary) | `getBirthParamsFromProfile()` | ~2086–2091 | Reads selected `#chartProfile` option — parses inline `dataset.profile` JSON (legacy profiles) or async-fetches from Supabase via `fetchEngineBirthForChartRecord()` |
| B (fallback) | App shell handoff `chartRecordId` | ~2097–2115 | `lastAppShellHandoff.chartRecordId` → `fetchEngineBirthForChartRecord()` |
| C (fallback) | Bare `?chartRecordId=<uuid>` URL param | ~2110–2122 | `fetchEngineBirthForChartRecord()` |

**Exception — aura PoC only:** Aura calls hardcode `aspect_overlay: { planet: "sun", aspect: "conjunction", angle: "ASC" }` as the planet/aspect for Sun conjunct ASC. Birth year/time still comes from the profile resolution chain. No birth data numeric values are hardcoded in the HTML.

---

## 4. Handoff / Legacy DOM Classification

| Path | Classification | Detail |
|------|---------------|--------|
| `buildPlanFromLegacyDom()` | **LIVE** | Primary production search plan builder |
| `source: "legacy_dom"` tag (lines 5752, 5998, 1940) | **LIVE** | Source tag in search plans and telemetry |
| `readAppShellHandoff()` / `lastAppShellHandoff` | **LIVE** | Active navigation contract between app_shell.html and map_CURRENT.html |
| Genie render handoff v2 (sessionStorage) | **LIVE** | Same-tab navigation side channel |
| Library/profile handoff application (lines 1334–1392) | **LIVE** | Applies URL/session selections to dropdowns |
| `handoffChartRecordIdForBirth()` | **LIVE** | Used in birth data resolution path B |
| `maybeExecuteGenieRenderHandoff()` | **LIVE** | Dispatches genie render payload on page load |

---

## 5. Safe-to-Remove Candidates (DEAD, no overlay dependency)

| Line(s) | Symbol | Reason |
|---------|--------|--------|
| 4674–4677 | `renderBellAuraBandsAroundLine()` | Explicitly disabled in comment referencing QA cleanup pass. Function body exits immediately via `if (!aspectAuraMode) return`. No production callers. No overlay dependency (never executes). |
| 1058 | `CANONICAL_RENDERER_BRANCH_ACTIVE = false` | Constant defined but never read. Dead assignment. Removing is safe but low value. |

**Note:** These are classification findings only. Actual deletion requires a separate change task and regression check.

---

## 6. Do-Not-Touch List (overlay/aura dependencies)

⚠️ The following blocks must NOT be removed, modified, or structurally altered without a dedicated overlay safety review:

| Block | Lines | Reason |
|-------|-------|--------|
| `ACTIVE_RENDERER_SUBSTRATE` constant | 1057 | Controls which renderer branch runs. Changing to CANONICAL_SCREEN_SPACE breaks production overlays. |
| `RENDERER_SUBSTRATES` object | 1054–1056 | Substrate enum; referenced by overlay dispatch and smoke-check. |
| `dispatchOverlayRequest()` | 5659–5681 | IS the production overlay dispatch. Contains LEGACY_SEARCH_REGIONS branch and shadow hook. |
| `summarizeLegacyShadowResult()` | 4827–4834 | Called every production overlay request. Feeds shadow comparison on flagged runs. |
| `summarizeShadowComparison()` | 4880–4902 | Receives legacy + canonical summaries; feeds DEV debug overlay container. |
| `compileLegacyGeometryIndex()` / `legacyIndexContainsPoint()` / `summarizeMaskParity()` / `summarizeCanonicalLegacyParity()` | 4968–5127 | Process overlay GeoJSON for geometry parity analysis. Touch legacy polygon geometry. |
| `runCanonicalDryRun()` | 5585–5636 | Shadow validation path; accepts and processes legacyGeojson from production overlay fetch. |
| `renderRasterAuraProgressive()` | ~4192+ | Active raster aura overlay rendering. Direct canvas mutations. |
| `renderAdaptiveAuraProgressive()` | ~4108+ | Active adaptive aura overlay rendering. |
| `renderAuraFieldProgressive()` | ~4554+ | Polygon aura PoC rendering. |
| `renderAspectFeatures()` | ~4678+ | Main production polygon/aspect overlay rendering. |
| `auraStrengthTier()`, `auraTierStyle()`, `renderAuraPoCBanner()`, `renderAuraFieldLegend()` | ~4278–4373 | Aura overlay UI support functions. |
| `aspect_overlay` construction and normalization | 3454–3456, 4802–4808, 1253–1256 | Drives what overlay is requested from backend. |
| Production smoke-check self-check block | 2595–2720 | Contains `ACTIVE_RENDERER_SUBSTRATE` gate and `production-shadow-dev-overlay` container. |

---

## 7. Verification Status

**VERIFIED**

All grep queries completed successfully. 10 targeted line reads performed (≤20 lines each). No files were modified during this audit.

**Key findings summary:**
- `LEGACY_SEARCH_REGIONS` is the **active production renderer substrate** — not dead
- `buildPlanFromLegacyDom()` is the **primary production search path** — not dead
- App shell handoff is the **active navigation contract** — not dead
- Shadow comparison suite is **PARTIAL** (URL-flag gated) but touches overlay geometry — do not remove
- Only 2 blocks are cleanly DEAD with no overlay dependency: `renderBellAuraBandsAroundLine()` and `CANONICAL_RENDERER_BRANCH_ACTIVE`
- Birth data is dynamically resolved from Supabase / profile dataset — **not hardcoded**
