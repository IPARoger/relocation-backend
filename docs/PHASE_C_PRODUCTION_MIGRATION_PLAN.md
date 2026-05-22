# Phase-C Production Migration Plan
## Legacy overlay pipeline → canonical screen-space adaptive substrate

> **Status:** Migration architecture and planning doctrine. Design
> only. No code changes authorised by this document.
> **Authority on conflict:** `docs/relocation_map_architecture.md`,
> then `docs/PHASE_C_RENDERING_ARCHITECTURE.md`, then this document,
> then `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`.
> **Operationalises:** `docs/PHASE_C_RENDERING_ARCHITECTURE.md` §10
> step 2 ("adaptive renderer production integration").
> **Companion:** `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`
> (Step 0 of the cache integration is settled by Step 1 of this plan).
> **Adopted draft:** 2026-05-21.
> **Stability:** Slow. The plan changes only by explicit edit naming
> the prior stance.
> **Non-goals:** No aura styling. No aesthetic rendering changes. No
> astrology math changes. No validated-adaptive-refinement-behaviour
> changes. No new endpoints. No revival of any superseded path.

This document plans a controlled migration of `map_CURRENT.html` away
from the legacy `/search-regions` overlay pipeline toward the
validated screen-space adaptive substrate (`/screen-pixel-truth`).
The plan is built for **reversibility** at every step. Every step
has a smoke gate. Every step is independently testable. Every step
is small enough to revert in one commit.

---

## 0. Where this fits

| Layer | Doc | Role |
|------|-----|------|
| Foundational architecture | `docs/relocation_map_architecture.md` | Architecture canon |
| Substrate charter | `docs/PHASE_C_RENDERING_ARCHITECTURE.md` | Substrate-level governing laws |
| Cache integration plan | `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` | Scheduler/cache shape |
| **Migration plan (this doc)** | `docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md` | How to safely cross over from legacy to canonical without destabilising the production map |
| Current rendering doctrine | `docs/CURRENT_RENDERING_DOCTRINE.md` | Status board of the stack |

When this doc and the substrate charter disagree, the charter wins.
When this doc and the cache integration plan disagree, this doc wins
(because the cache cannot wrap a substrate the production renderer
does not use; the substrate swap is the dependency).

---

## 1. Legacy vs Canonical Substrate Audit

### 1.1 The legacy overlay pipeline (what is in production today)

| Surface | Implementation |
|---------|----------------|
| Endpoint | `POST /search-regions` (`main_centerline_FIXER.py:466`) |
| Inputs | birth params, `house_conditions`, `angle_sign_conditions`, `aspect_overlay`, `resolution` (default 1.5°), `generation_mode` (`truth_grid` or contour), `truth_grid_resolution` (0.75°), `truth_grid_boundary_refine` |
| Sampling axis | **Geographic lat/lon grid**, fixed step in degrees |
| Output shape | **GeoJSON polygon FeatureCollection** |
| Polygon-mode internals | Per-cell `swe.houses` → boolean mask → `scipy.ndimage.gaussian_filter(sigma=1.2)` → `skimage.measure.find_contours(0.5)` → `approximate_polygon(tolerance=0.08)` |
| `truth_grid` mode internals | `truth_grid_engine.generate_truth_grid_house_features` with boundary refinement; produces polygon features grounded in honest per-cell classification |
| Production renderer | Leaflet vector polygons via `polygonLayer`, `aspectLayer`, `auraLayer` in `map_CURRENT.html` |
| Cancellation | `currentRenderToken` integer compared at multiple await points (10+ check-sites in the file) |
| Cache | None (every gesture re-fetches) |
| World-copy handling | Polygon at lat/lon X; Leaflet decides where to draw it |
| Default in `map_CURRENT.html` | `generation_mode: "truth_grid"`, `truth_grid_resolution: 0.75`, `truth_grid_boundary_refine: true` |

### 1.2 The canonical screen-space substrate (validated, sandbox-proven)

| Surface | Implementation |
|---------|----------------|
| Endpoint | `POST /screen-pixel-truth` (`main_centerline_FIXER.py:1324`) |
| Inputs | birth params, explicit list `points: [[lat, lon], …]`, `conditions` (max 6), `apply_lat_cap` |
| Sampling axis | **Screen-pixel grid**, anchored to current Leaflet viewport projection at current zoom |
| Output shape | **Dense `masks` array**, one bitmask per input point, in input order |
| Renderer behaviour | Canvas painter draws per-pixel blocks at `block_px` resolution; no polygon stroke, no smoothing |
| Refinement | Client-side adaptive (16 → 8 → 4 → 2 → 1 px on demand, `screen_pixel_adaptive_refinement.md`); per-region escalation policy (`screen_pixel_adaptive_targeted.md`) |
| Cancellation | `AbortController` per fetch (sandbox); composes cleanly with scheduler |
| Cache | Phase-2 cache with priority A–H protocol |
| World-copy handling | Each visible world copy generates its own screen pixels; correct by construction |
| Production status | **Not yet wired into `map_CURRENT.html`** |

### 1.3 Semantic differences

| Axis | Legacy `/search-regions` | Canonical `/screen-pixel-truth` |
|------|--------------------------|-------------------------------|
| What "the truth at this place" means | Polygon whose interior is classified `true` | Per-pixel mask bit at the screen pixel center |
| Edge representation | Polygon stroke / fill (smoothed, contour-traced) | Block-boundary tiles, no smoothing |
| Zoom scaling | Polygon vector scales linearly with zoom (Leaflet handles SVG) | Each zoom is a fresh classification pass at that zoom's screen pixels |
| World-copy correctness | Polygon at lat/lon X is implicit in projection | Each world copy is independently classified |
| Aspect overlay (ASC/MC/DC/IC) | Staged at 2.0/1.0/0.5 aspect_resolution; uses `find_contours` on aspect grids | Not yet ported; aspect overlay is a separate migration phase (Phase 2 of this plan) |
| Angle-in-sign | `generate_angle_sign_features` → polygons | Not yet ported; same condition class fits the screen-space mask shape but no production wiring |

### 1.4 Rendering differences (visible)

| Property | Legacy | Canonical |
|----------|--------|-----------|
| Edge sharpness | Smoothed polygon strokes; visually soft | Block edges; visually staircased at low zoom |
| Anti-aliasing | Leaflet SVG renderer's path AA | None (canvas-fillRect on integer block coordinates) |
| Inter-condition overlap | Polygons rendered with their own fill opacity | Mask-bit composite via `MASK_PALETTE` opacity-stacking |
| Fill opacity behaviour | Per-feature opacity | Per-mask-bit opacity |
| Centerline / aura | Separate `auraLayer` polygon path | Aura is **not yet implemented** on the canonical substrate (deferred per Phase C charter §10) |
| High zoom appearance | Smooth polygons | Visible blocks until adaptive 1 px local convergence completes |
| Pixel-perfect display agreement | No (polygon may visibly disagree with click-popup) | Yes within block precision (mask is pixel-honest) |

### 1.5 Cache compatibility implications

| Concern | Notes |
|---------|-------|
| Phase-2 cache today | Caches `/screen-pixel-truth` responses by `(chart, bounds, zoom, block, conditions, lat_cap)` |
| Phase-2 cache on legacy | Would have to key on the legacy payload (`resolution`, `generation_mode`, `truth_grid_resolution`, `truth_grid_boundary_refine`, `house_conditions`, `angle_sign_conditions`, `aspect_overlay`) — a different key shape |
| Cache reuse across migration | **None** — different endpoints, different outputs, different keys. A cache populated by the legacy path cannot serve a canonical request and vice versa |
| Migration consequence | The cache must be invalidated (or simply not carry across) when the substrate flag flips |

### 1.6 Validation differences

| Validation surface | Legacy | Canonical |
|--------------------|--------|-----------|
| Primary harness | `scripts/validate_sprint_dc_ic.py` (validated against legacy polygon output) | `scripts/smoke_map_current.py` (the same fixture set, mode-agnostic) and several screen-pixel-* harnesses |
| Brute-force wall | `scripts/capture_brute_force_*` (canonical specimens) — substrate-agnostic in principle | Same wall; canonical substrate consistently agrees with the wall within validated XOR thresholds |
| XOR threshold today | Not measured for the legacy polygon path (it's a polygon, not a mask; XOR is undefined without rasterisation) | Worst measured: **0.386%** for dense 5-condition Americas (`screen_pixel_dense_residue.md`) |
| Popup-overlay parity | Both paths share Swiss Ephemeris ground truth, so click-popup vs overlay should agree at any (lat, lon). Today the legacy renderer may show a *polygon* edge that doesn't quite coincide with the popup's classification cell, especially after polygon smoothing | Canonical path: the visible block at (lat, lon) was classified using `swe.houses(lat, lon)` at the block centre. Popup-overlay agreement is mechanically tight |
| Seam validation | Implicit via Leaflet projection | Explicit via per-world-copy independent classification |
| High-latitude (`lat_cap`) | `apply_lat_cap` is honoured in both paths (server-side); legacy via grid bounds, canonical via per-point opt-in |

### 1.7 Hidden assumptions

These are assumptions baked into the production code that the migration must not break silently:

| Assumption | Where it lives | Migration impact |
|-----------|----------------|------------------|
| `prepareDisplayFeatures(canonicalGeojson)` expects polygon FeatureCollection | `map_CURRENT.html:1408` | Replacement must either feed it polygons (adapter), or be bypassed entirely (direct canvas render) |
| `renderHouseFeatures(displayData)` expects polygon features | `map_CURRENT.html:2937` | Same as above |
| `polygonLayer.clearLayers()`, `aspectLayer.clearLayers()`, `auraLayer.clearLayers()` | Used in `findRegions()` to reset state | Canonical substrate writes to a canvas layer, not vector layers. Both must be cleared on flag flip |
| `currentRenderToken` is the cancellation primitive | 10+ check-sites | Scheduler integration must compose with — or supplant — this token chain |
| `/aura-raster` and `/aura-raster-adaptive` are still called from `map_CURRENT.html` (lines 1968, 1981) | These are the Phase A/B aura PoC paths, declared **superseded archaeology** by the Phase C charter, but the production code still calls them | Step 0 of this migration must fence these calls behind a debug flag or retire them; otherwise the doctrine and implementation disagree silently |
| `/relocated-chart` (popup) is independent of the overlay path | `map_CURRENT.html:1177` | Popup truth is engine-direct (`swe.houses` at clicked point). Migration must not affect popup behaviour. Popup is the **truth hierarchy** anchor; parity tests compare overlay to popup, not overlay to legacy overlay |
| Aspect overlay uses staged resolutions (coarse → medium → final) | `findRegions()` lines 3146-3148 | Canonical substrate's progressive reveal pipeline is structurally different (refinement stage model from Phase B); aspect-overlay migration is its own phase, deferred until houses are stable |
| `auraDebugStatus`, `latCapDebugLabel`, and other debug surfaces assume legacy state | Scattered | Each must either be cleared, made substrate-aware, or deferred until per-substrate debug surfaces land |

### 1.8 Likely regression risks (ranked)

| Risk | Likelihood | Severity | Mitigation surface |
|------|-----------|----------|--------------------|
| Block edges visibly chunky at high zoom before adaptive 1 px refinement converges | High | Medium | Substrate adaptive policy already handles this; ensure 1 px local refinement is wired into production, not just sandbox |
| Aspect overlay missing during transition | High (if aspect is in the same phase) | High | Keep aspect overlay on legacy path during Phase 1; migrate aspect in Phase 2 |
| Polygon visual style that users expected (smooth strokes) gone | High | Low | This is the *intended* outcome of the rendering reset; the substrate charter explicitly accepts visible blocks as honest |
| Aura PoC layers break when the legacy aura raster endpoints are not migrated in this pass | High (if aura is touched) | Medium | Step 0 cleanup: fence the aura PoC endpoints behind a debug flag (they were archaeology already) |
| Popup-overlay disagreement at click points | Low (math is identical) | Catastrophic if it happens | Mandatory popup-parity validation (§4.4) |
| Cache populated with legacy entries then served against canonical (or vice versa) on flag flip | Medium | High | Cache must invalidate on flag flip (§2.4) |
| `currentRenderToken` token-check failures during transition because the new scheduler uses `AbortController` | Medium | Medium | Adapter layer routes both cancellation primitives until legacy is fully retired |
| Performance regression for very dense overlays (6 conditions) | Low (canonical measured 0.386% XOR at 5 conditions, near-budget) | Medium | Honour the validated budget (`233 118` samples); accept `deferred_budget` for warm-up jobs on dense viewports |
| Aspect-overlay-staging assumption that does not survive | High if aspect is migrated alongside houses | High | Defer aspect to Phase 2 |
| World-copy duplicate or missing classification at dateline | Low | High | Canonical substrate handles this by construction; explicit seam smoke test (§4.6) |

---

## 2. Migration Architecture

### 2.1 Adapter layer vs direct replacement

Two shapes are possible:

| Shape | Description | Cost |
|------|-------------|------|
| **Adapter layer** | A unified `runOverlay(payload)` function that dispatches to either `/search-regions` (returns polygons) or `/screen-pixel-truth` (returns masks → painted to canvas) based on a substrate flag. Both code paths coexist temporarily | Larger transitional surface; both paths must remain green |
| **Direct replacement** | Replace `findRegions()` to call `/screen-pixel-truth` only; delete the legacy path entirely | Smaller code; no rollback unless we restore from git |

**Choice (this doctrine):** **Adapter layer.** Reversibility is the
governing constraint of this migration. The adapter coexists for the
validation window (Phase 1 stabilisation), then the legacy branch is
retired in a separate explicit step (Phase 4 of §3).

### 2.2 Transitional coexistence doctrine

While the adapter coexists, the rules are:

| Rule | Reason |
|------|--------|
| The substrate flag is **per-page-load**, set via URL param (`?substrate=legacy` or `?substrate=canonical`) or env constant | No mid-session flag flips; flips require a page reload that clears all layers and caches |
| Default = `legacy` for one validation window, then default = `canonical` | Default flip is its own validation gate |
| Both paths must pass the canonical smoke set on every commit | Otherwise the rollback path is silently broken |
| The adapter never mixes substrates within one render | A single visible overlay always comes from one substrate; no half-and-half painting |
| Cache is per-substrate-keyed (or cleared on flag change) | A legacy-populated cache entry must never be served to a canonical request |
| Aura PoC paths (`/aura-raster`, `/aura-raster-adaptive`) are fenced behind `?debugAuraPoc=1` during the entire migration | They are archaeology; treating them as production-required would block the migration |
| Aspect overlay stays on legacy `/search-regions` until Phase 2 | One thing at a time |

### 2.3 Feature-flag philosophy

The substrate flag is the **simplest possible thing**:

| Property | Choice |
|----------|--------|
| Storage | URL param `?substrate=canonical|legacy`, with fallback to a Python constant `DEFAULT_SUBSTRATE` in `main_centerline_FIXER.py` that the page template substitutes into HTML at serve time |
| Scope | Per page load |
| Granularity | Per substrate (legacy vs canonical); **not** per condition family, not per region, not per chart |
| Persistence | None (URL or constant, no cookies, no localStorage) |
| Operator override | URL param wins over constant; constant wins over default |
| Telemetry | None (the flag's effect is observable in the network tab; no separate metric needed) |
| Lifecycle | Active during Phase 1–3; retired in Phase 4 when the legacy branch is deleted |

**Forbidden:** a feature-flag service, a rollout-percentage system, a
user-segment flag, an A/B testing infrastructure. Two paths, one
URL param, one default constant. That is the entire flag surface.

### 2.4 Rollback doctrine

| Rollback layer | How |
|----------------|-----|
| **In-session** (a user reports a bug mid-session) | Page reload with `?substrate=legacy`; the legacy path is fully functional and recovers them immediately |
| **Per-deploy** (a deploy regressed) | Revert the default constant to `legacy`; deploy. No data migration required because the cache is per-session-per-substrate |
| **Per-commit** (a specific change to the canonical path regressed) | Standard git revert; the canonical path's last-known-good remains accessible via flag |
| **Catastrophic** (the canonical path is broken in a way the legacy path is not) | Default to `legacy`; leave the canonical code in tree behind a `?substrate=canonical` flag; resume development on a branch |

Rollback **cannot** be triggered by the canonical substrate trying to
do something on its own. There is no auto-fallback. The user-visible
state must be deterministic: the URL or the constant tells you which
substrate is rendering. Auto-fallback would mask regressions.

### 2.5 Isolation boundaries

The adapter layer enforces these boundaries:

| Boundary | What stays on each side |
|----------|------------------------|
| **Backend** | `/search-regions` and `/screen-pixel-truth` continue to live side-by-side; they share `swe.houses` and Swiss Ephemeris but nothing else. Neither imports from the other |
| **Endpoint adapter (frontend)** | `runOverlay(payload, substrate)` → either `postSearchRegions(payload)` (returns polygons) or `postScreenPixelTruth(payload)` (returns masks). The two functions never call each other |
| **Renderer adapter (frontend)** | `renderOverlay(result, substrate)` → either `renderHouseFeatures(displayData)` (polygon path) or `paintMaskToCanvas(result)` (canonical path). Layers cleared appropriately on every render |
| **Cancellation adapter** | Both `currentRenderToken` (legacy) and `AbortController` (canonical) are honoured; on user action, both are signalled, both cancel cleanly |
| **Cache adapter** | The Phase-2 cache is only enabled on the canonical substrate. The legacy substrate runs with no cache (its today behaviour) |
| **Debug surfaces** | Each debug panel declares which substrate it understands; mismatched panels render `n/a` or are hidden |

### 2.6 Validation checkpoints (gates)

Every step of §3 has a smoke gate. No step proceeds without its
gate green:

| Step | Gate |
|------|------|
| Step 0 (cleanup) | Existing smoke set still green (`smoke_map_current.py`, `validate_sprint_dc_ic.py`, `smoke_phase2_cache.py`) |
| Step 1 (adapter) | Both substrates produce visible overlays; flag flip via URL reload swaps the substrate cleanly |
| Step 2 (parity) | New `smoke_substrate_parity.py` proves canonical agrees with the brute-force wall at the validated XOR threshold for the fixture set |
| Step 3 (canonical default) | Same smoke set still passes; `?substrate=legacy` still works |
| Step 4 (legacy retirement) | Substrate flag removed; canonical-only smoke still passes; legacy code marked archaeology |

### 2.7 Observability requirements (minimal)

| Surface | What |
|---------|------|
| `window.__substrate` | Read-only value: `"legacy"` or `"canonical"` |
| Console log on overlay completion | One line: `substrate=canonical samples=5130 ms=487 status=ok` (or `legacy ms=812 status=ok`) |
| Network tab | Already shows the endpoint; this is the operator's primary instrument |
| Debug panel `currentDebugMetrics.substrate` | The active substrate name |
| New: error event `substrate_render_error` | Fired on overlay failure; carries substrate name and error message; logged to console only |

That is the entire observability surface for migration. No
dashboards, no time-series, no alerting. The page is the dashboard.

### 2.8 Where the adapter lives in the file tree

| Surface | File / location |
|---------|-----------------|
| Adapter dispatch | `static/substrate_adapter.js` (new) or inline at the top of `map_CURRENT.html` |
| Legacy fetcher | Existing `postSearchRegions()` in `map_CURRENT.html` |
| Canonical fetcher | New `postScreenPixelTruth()` in `map_CURRENT.html` (or moved into the adapter module) |
| Legacy renderer | Existing `renderHouseFeatures()` |
| Canonical renderer | New `paintMaskToCanvas()` (informed by the sandboxes' `TruthCanvas` Leaflet layer) |
| Scheduler | Extracted from `map_SANDBOX_phase2_cache.html` per cache-integration Step 1 |

This document **does not mandate** file boundaries beyond
endpoint-adapter and renderer-adapter being separately swappable.
Inlining or extracting is the implementer's choice as long as the
isolation in §2.5 holds.

---

## 3. Production Integration Order

The migration is a sequence of small, reversible, separately-validated
steps. Each step lands in one commit (or commit cluster), passes its
gate, and is independently revertible.

### Phase 0 — Cleanup & substrate path decision

#### Step 0.1 — Record the substrate-path decision

Per `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` §10 Step 0, the
substrate-path decision is recorded in `ai_context/decisions.md`:

> **2026-05-21: Phase-C production migration path.** The production
> visible-overlay path for `map_CURRENT.html` will be migrated to
> `/screen-pixel-truth` via a substrate-adapter layer (Path A in
> `PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` §10 Step 0). The
> Phase-2 cache integration follows the substrate migration.

This sentence is the binding decision. Once landed, the cache
integration plan's Step 0 is satisfied.

#### Step 0.2 — Fence the aura PoC endpoints behind a debug flag

The `/aura-raster` and `/aura-raster-adaptive` calls in
`map_CURRENT.html` (lines 1968, 1981) are Phase A/B archaeology per
the Phase C charter. They remain wired in production today; this is
a doctrine-vs-implementation gap.

**Action:** wrap the two `postAuraRaster*` calls behind a check on
`?debugAuraPoc=1` (or equivalent debug flag); default is `off`.
This is **not** a deletion; the code stays in tree for archaeology
visibility but no longer fires on default page loads.

**Gate:** `scripts/smoke_map_current.py` still passes with no
debug flag; the aura PoC chrome (banner, raster overlay) does not
render on default load.

**Why this is Step 0:** the substrate migration cannot land cleanly
while the aura PoC paths inject their own state into the same
renderer chain. Fencing them is the smallest cleanup that removes
the cross-coupling.

#### Step 0.3 — Mark `contour` generation mode as archaeology

The legacy `/search-regions` has two modes (§1.1). The `contour`
mode uses `gaussian_filter` + `find_contours` + `approximate_polygon`
— the rejected cosmetic-smoothing path. The `truth_grid` mode is
honest.

**Action:** add a doctrine note to `main_centerline_FIXER.py` at
the `contour` branch (the `else:` block at line 491) tagging it
`# ARCHAEOLOGY: contour mode is the rejected polygon-smoothing path. truth_grid mode is the honest legacy substrate.`. No code change; the migration touches **only** the `truth_grid` branch of `/search-regions` for parity testing.

**Gate:** existing smoke still passes (no behaviour change).

### Phase 1 — Adapter layer & canonical wiring

#### Step 1.1 — Extract the Phase-2 scheduler

Per `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` §10 Step 1.
Pre-condition for canonical wiring; produces a substrate-agnostic
scheduler module.

**Gate:** `scripts/smoke_phase2_cache.py` still passes against the
extracted scheduler driving the sandbox.

#### Step 1.2 — Build the substrate adapter (legacy-only at first)

Land `runOverlay(payload, substrate)` and `renderOverlay(result, substrate)` adapters in `map_CURRENT.html` that **only support
`substrate="legacy"`** in this step. The adapter wraps the existing
`postSearchRegions` and `renderHouseFeatures` calls; behaviour is
identical.

**Gate:** existing smoke unchanged; `?substrate=legacy` and no flag
both yield identical behaviour.

#### Step 1.3 — Wire the canonical substrate behind the adapter

Add `postScreenPixelTruth()` and `paintMaskToCanvas()` to the
adapter; enable `?substrate=canonical`. Default remains `legacy`.

**Gate:**

- `?substrate=legacy` (default): unchanged
- `?substrate=canonical`: overlay paints via canvas; visual diff
  visible but not yet validated for parity

#### Step 1.4 — Wire scheduler + cache onto the canonical path

Route canonical USER requests through the Phase-2 scheduler. Legacy
requests stay on the direct fetch path (no cache). After this step
the canonical substrate has scheduler + cache; the legacy substrate
remains as today (no cache).

**Gate:**

- `?substrate=canonical`: Phase-2 cache populates; subsequent
  identical requests hit cache
- `?substrate=legacy`: unchanged
- Both pass `smoke_map_current.py`
- Canonical passes `smoke_phase2_cache.py`

### Phase 2 — Parity validation

#### Step 2.1 — Side-by-side smoke (`smoke_substrate_parity.py`, new)

A new smoke harness that, for each canonical chart fixture
(`Default Sample`, `Sprint DC/IC`, dense Americas, Greenland/Iceland,
etc.):

1. Hits `?substrate=legacy` for the fixture; captures the overlay
   as a rasterised PNG via Playwright.
2. Hits `?substrate=canonical` for the same fixture; captures the
   overlay PNG.
3. Hits `/brute-force-grid` for the same fixture; captures the
   ground-truth raster.
4. Computes XOR of canonical vs brute-force; asserts ≤ validated
   threshold (worst observed: **0.386%** dense-5, `screen_pixel_dense_residue.md`).
5. Computes XOR of legacy (after rasterisation) vs brute-force;
   records the value; does **not** assert (this is observational —
   legacy polygon paths may visibly disagree with raster truth at
   sub-pixel scale).
6. Computes XOR of canonical vs legacy (after rasterisation);
   records; does not assert.

**Gate:** canonical-vs-brute-force XOR within thresholds for all
fixtures. Legacy-vs-brute-force XOR captured for the record.

#### Step 2.2 — Popup-overlay parity smoke (`smoke_popup_overlay_parity.py`, new)

For N random points within the visible overlay's classified regions
(per substrate):

1. Compute the overlay's classification at that point (the mask bit
   at the closest screen pixel for canonical; the polygon
   containment test for legacy).
2. Fetch `/relocated-chart` for the same point.
3. Compute the same classification analytically from the chart.
4. Assert overlay-classification == analytical-classification.

The expected result: both substrates pass (they share the same
ephemeris). If either fails, the substrate has a correctness bug
that **must** block the migration.

**Gate:** ≥ N=200 sample points per fixture, 100% match for the
canonical substrate; legacy substrate result captured.

#### Step 2.3 — Seam validation

Run `smoke_substrate_parity.py` with a dateline-crossing viewport
(e.g. Pacific basin centered at lon=180). The canonical substrate
must classify both world copies independently and consistently.

**Gate:** XOR within threshold across the seam.

#### Step 2.4 — High-latitude validation

Run with Greenland/Iceland fixture and lat-cap on/off. Verify
canonical substrate honours `apply_lat_cap` (per-point) and matches
legacy (per-grid) in coverage area within the validated XOR.

**Gate:** XOR within threshold; cap behaviour visible / invisible
matches operator expectation.

#### Step 2.5 — Interruption validation

Adapt `smoke_phase2_cache.py` to run against `map_CURRENT.html`
with `?substrate=canonical`. Verify scheduler cancellation,
priority order, budget, and H-deferred-inactive behave as in the
sandbox.

**Gate:** all sandbox-smoke tests still pass when the scheduler is
hosted by `map_CURRENT.html`.

### Phase 3 — Default flip

#### Step 3.1 — Flip the default to `canonical`

Change `DEFAULT_SUBSTRATE = "canonical"` in `main_centerline_FIXER.py`.
Page loads without a flag now render via canonical. `?substrate=legacy` continues to work.

**Gate:** every smoke from Phases 1 and 2 passes again; legacy still
operative under the flag.

#### Step 3.2 — Stabilisation window

A defined period (e.g. 1–2 weeks of working with the page) during
which:

- Every observed regression that traces to the substrate flip is
  triaged and resolved on the canonical branch.
- Operator may flip back to `?substrate=legacy` for any chart that
  appears wrong.
- No deletions yet; the legacy branch remains a working safety net.

**Gate:** zero unresolved substrate-attributed regressions at the
end of the window. (Subjective gate; the operator decides.)

### Phase 4 — Legacy retirement

#### Step 4.1 — Remove the legacy branch from `runOverlay()` and `renderOverlay()`

The substrate flag is removed. `runOverlay()` calls
`postScreenPixelTruth()` directly. `renderOverlay()` paints to
canvas directly. The legacy adapter functions are deleted.

**Gate:** all smokes pass; `?substrate=legacy` is a no-op (the URL
param is ignored, not error-raising).

#### Step 4.2 — Mark `/search-regions` as legacy in the backend

Add a doctrine-banner docstring atop the `search_regions` handler:

> **STATUS: legacy.** Replaced in production by `/screen-pixel-truth`
> as of <date>. Retained for archaeology and for the
> `/brute-force-grid` parity wall (which uses the same conditioning
> logic). Do not extend this endpoint.

Do not delete the endpoint code. It remains callable for offline
validation and historical inspection.

#### Step 4.3 — Mark legacy code paths in `map_CURRENT.html` as archaeology

The `postSearchRegions`, `renderHouseFeatures`,
`prepareDisplayFeatures`, `polygonLayer`, `aspectLayer`, `auraLayer`
that no longer serve production are either:

- Deleted (if completely unused), with a final commit message
  explaining the supersession, OR
- Retained behind a clear `// ARCHAEOLOGY: legacy substrate. See
  docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md` comment if they remain
  referenced by `?debugLegacy=1` for inspection.

Choice depends on what is actually referenced; the doctrine does not
mandate either path, but mandates that whatever survives is **clearly
marked**.

#### Step 4.4 — Update doctrine index

Update `docs/DOCTRINE_INDEX.md` and `docs/CURRENT_RENDERING_DOCTRINE.md` to reflect canonical-only production. The migration plan itself
(this document) becomes `STATUS: completed`. The legacy archaeology
notes are cross-linked.

---

## 4. Validation Doctrine

### 4.1 Parity tests (per Phase 2)

| Test | Asserts |
|------|---------|
| `smoke_substrate_parity.py` | Canonical-vs-brute-force XOR within threshold across fixture set |
| `smoke_popup_overlay_parity.py` | Overlay classification matches analytical classification at sampled points (100%) |
| `smoke_aspect_overlay_legacy.py` | Aspect overlay (still on legacy until Phase 2 of aspect migration) remains visually unchanged |

### 4.2 Screenshot regression tests

For the canonical chart fixtures listed below, a Playwright PNG
capture is stored in `validation/screenshots/migration_baseline/`
and diffed on every commit:

| Fixture | Why |
|---------|-----|
| Default sample (world view) | Baseline general appearance |
| Sprint DC/IC | Validated trickiest case from `validation/reports/sprint_dc_ic_validation.json` |
| Dense 5-condition Americas | Highest sample budget (`screen_pixel_dense_residue.md`) |
| Greenland/Iceland (lat_cap on) | High-latitude edge case |
| Pacific basin (dateline crossing) | Seam case |

Diffs above a pixel-tolerance threshold (TBD per fixture; not specified
in this doctrine) flag the commit. Visual diffs are reviewed by
operator; mechanical XOR thresholds are reviewed by `smoke_substrate_parity.py`.

### 4.3 XOR thresholds

| Case | Threshold |
|------|-----------|
| Single condition, typical viewport | ≤ 0.10% (from `screen_pixel_adaptive_refinement.md`) |
| 3-condition overlap | ≤ 0.20% |
| Dense 5–6 conditions | ≤ 0.40% (worst observed 0.386%) |
| Greenland/Iceland (lat_cap) | ≤ 0.50% (allow polar wiggle within cap policy) |
| Seam (dateline) | ≤ threshold of the underlying case (seam handling is by construction) |

The thresholds are **measured ceilings**, not goals. The doctrine is
"meet the measured ceiling, do not regress." Improvements are
welcome but not required.

### 4.4 Popup truth checks (mandatory)

The truth hierarchy from `docs/visual_semantic_style_guide.md` § 2:

> Popup is the canonical truth; overlay is exploratory. The two must
> agree.

The migration cannot break this:

| Check | Method |
|-------|--------|
| Overlay-popup agreement | `smoke_popup_overlay_parity.py` (§4.1) |
| Pass rate target | 100% on canonical (the math is identical to popup); ≥ 99% on legacy (legacy polygon smoothing may shift edges sub-pixel-ly) |
| Failure handling | Any single failure blocks the migration step; investigate before proceeding |

The legacy substrate's < 100% pass is not a bug per se (polygon
smoothing is documented behaviour) but is one of the reasons the
canonical substrate is the production target.

### 4.5 Seam validation

| Scenario | Expected |
|----------|----------|
| Viewport spanning lon ∈ [-200, -160] (crosses lon=-180/+180) | Canonical: identical classification in both world copies of any lat/lon. Legacy: Leaflet projects the polygon across the dateline; no per-world-copy distinction |
| World-copy duplicate cell at (lat, +179) and (lat, -181) | Both should classify identically (same `swe.houses` answer) |

The canonical substrate handles seams by construction (per
`screen_pixel_truth_diagnosis.md`); the smoke just confirms.

### 4.6 High-latitude validation

| Scenario | Expected |
|----------|----------|
| Lat-cap on at 65°, Greenland visible | Polar tiles classified per `apply_lat_cap=True` (the cap is opt-in per `screen-pixel-truth` request schema) |
| Lat-cap off, Greenland visible | Polar tiles classified naively; differences from the cap-on case are visible and accepted |
| Svalbard fixture | Per `screen_pixel_adaptive_targeted.md`: targeted high-latitude refinement should be visibly active; sample count visible in debug panel |

### 4.7 Interruption validation

Adapt `smoke_phase2_cache.py` against `map_CURRENT.html` with
`?substrate=canonical`. Test cases:

| Case | Expected |
|------|----------|
| First paint completes | Pass (USER job populates cache) |
| User action pauses background | Pass (scheduler aborts) |
| Priority order registered | Pass (A → H) |
| Immediate render after interrupt | Pass (next user request runs immediately) |
| No half-cached entries | Pass (cache only on full success) |
| Budget enforced | Pass (`233 118`) |
| New: Substrate flip mid-session prohibited | Pass (URL flip requires page reload; no in-session swap) |

### 4.8 Cache correctness validation

Per `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` §7. The new
smokes (`drainage`, `storm`, `chart_change`) become mandatory when
the canonical substrate is the default (Phase 3 of §3).

### 4.9 Rollback validation

| Test | Asserts |
|------|---------|
| Default flip rollback | Setting `DEFAULT_SUBSTRATE = "legacy"` after a default-flip yields identical behaviour to pre-flip |
| Flag-flip rollback (per user) | Page load with `?substrate=legacy` after one with `?substrate=canonical` yields a clean legacy render with no canonical artefacts |
| Per-commit rollback | `git revert` of any single migration commit leaves the page in a consistent (pre-revert) state |

These are **manual** validations except for the default-flip case,
which is covered by running the existing smokes against
`DEFAULT_SUBSTRATE = "legacy"` periodically (e.g. once per
migration phase boundary).

---

## 5. Legacy Archaeology Doctrine

### 5.1 What legacy code remains (after Phase 4)

| Surface | Disposition |
|---------|-------------|
| `/search-regions` endpoint in `main_centerline_FIXER.py` | **Retained**, marked legacy. Continues to back `/brute-force-grid` parity comparisons. Not extended |
| `truth_grid_engine.py` | **Retained**, separate module. Used by `/search-regions` and historically by the validation wall. Migration may or may not retire it later; not in scope here |
| `/aura-raster`, `/aura-raster-adaptive`, `/aura-field` | **Retained**, marked archaeology per Phase C charter. Fenced behind `?debugAuraPoc=1` in `map_CURRENT.html` from Step 0.2 onward |
| `/classify-points` | **Retained** (different purpose from `/screen-pixel-truth`; per-point all-houses cache) |
| `/brute-force-grid` | **Retained** as the canonical validation wall |
| Sandbox HTML files (`map_SANDBOX_*`) | **Retained** as the substrate's reference implementations |
| Legacy adapter functions in `map_CURRENT.html` after Phase 4 | **Either deleted or retained behind `?debugLegacy=1`**; choice is per Step 4.3 |

### 5.2 What gets marked superseded

| Surface | How |
|---------|-----|
| `/search-regions` | Docstring banner per Step 4.2 |
| `contour` generation mode of `/search-regions` | Inline comment per Step 0.3 |
| Aura PoC endpoints | Docstring banner referencing Phase C charter §8 archaeology |
| Phase A/B aura narratives (`sun_conjunct_asc_truth_field_spine_phase_a.md`, `progressive_reveal_phase_b.md`) | Already marked superseded per `PHASE_C_RENDERING_ARCHITECTURE.md`; revisit during Step 4.4 |
| Legacy fetcher and renderer functions in `map_CURRENT.html` | Per Step 4.3 |

### 5.3 What gets preserved permanently

Per `docs/PHASE_C_RENDERING_ARCHITECTURE.md` §8 (archaeology doctrine):

| Permanent | Reason |
|-----------|--------|
| Every superseded narrative and sandbox | Institutional memory; preserves *why* the path was rejected |
| `/brute-force-grid` and the canonical control specimens | The validation wall must remain accessible forever |
| Documents marked SUPERSEDED with explicit supersession reason and date | Discoverable history |
| `docs/CURRENT_RENDERING_DOCTRINE.md` archaeology references | The shortest path back to "what we tried and why we stopped" |
| This migration doctrine (after completion) | Provides the rationale for future similar migrations |

### 5.4 Anti-backsliding principles

| Anti-pattern | Prevention |
|--------------|-----------|
| "Let's bring back polygon smoothing for the aura" | The `contour` generation mode is marked archaeology; any PR reintroducing `find_contours` or `gaussian_filter` in a render path fails review at the doctrine line |
| "Let's add a third substrate" | Migration plan explicitly forbids substrate-pluggable architecture for N>2 (§9). Adding a third substrate requires a new doctrine doc |
| "Let's quietly delete the brute-force validation wall" | The wall is permanent (§5.3); deletion requires explicit doctrine update |
| "Let's reuse legacy polygons in the canonical canvas painter" | The substrate change is a paradigm swap; polygons in the canonical path violate the screen-space-truth doctrine |
| "Let's auto-fallback to legacy if canonical errors" | Forbidden by §2.4 (no auto-fallback; the substrate flip is operator-visible only) |

### 5.5 Preserving rationale without confusing future development

The pattern, enforced across this migration:

| Surface | Required content |
|---------|------------------|
| Every superseded doc | A header banner: `> **Status:** SUPERSEDED on <date> by <doc>. Reason: <one sentence>. Retained as archaeology.` |
| Every archaeology endpoint | A docstring banner with the same shape |
| Every archaeology JS function | A leading comment with the same shape |
| Index updates | `docs/CURRENT_RENDERING_DOCTRINE.md` and `docs/DOCTRINE_INDEX.md` cross-reference the supersession |

If a future developer reads an archaeology surface, they see in the
first line: "this is superseded, here's why, the replacement is X."
That is the entire anti-confusion contract.

---

## 6. Production Observability

The aim of this section is to **minimise** observability surface to
what is directly justified by the current validated architecture. Any
observability we add is observability someone must read and decide
on. Adding observability nobody reads is its own anti-pattern.

### 6.1 Metrics worth logging

| Metric | Format | Why |
|--------|--------|-----|
| Substrate name | `console.log("substrate=canonical")` once per page load | Confirms the flag took effect |
| Per-render completion | One line: `substrate=X status=ok samples=N ms=T` per overlay completion | Operator can read this in console |
| Scheduler events (canonical) | The existing `__phase2.events` ring buffer, accessible via `window.__phase2.events` | Inspection-on-demand, not push |
| Cache size (canonical) | `window.__phase2.cache.size`, read on demand | Same |
| Substrate render errors | `console.error("substrate=X render failed:", err)` | Alerts the operator |
| Brute-force wall result (validation) | Per-run report in `validation/reports/` | The wall is a smoke-test artefact, not a runtime metric |

### 6.2 Metrics NOT worth logging yet

| Metric | Why deferred |
|--------|--------------|
| User-action sequence telemetry | No telemetry infrastructure; speculation today |
| Per-cell classification time | Sub-millisecond; aggregate sample count + total ms is sufficient |
| Cache hit rate over a session | Operator can read `__phase2.metrics.cacheHits` at any time; aggregate-over-time requires storage |
| Time spent in each scheduler state (idle, user_serving, etc.) | Same |
| Per-priority warm-up completion latency | Phase-2 cache priority is static; latency profile would only inform telemetry-deferred reordering |
| Server-side handler duration breakdown | `swe.houses` is the bottleneck; further breakdown is server-side work, not migration scope |
| Memory growth over session | Validate manually during stabilisation window (§3 Phase 3); no runtime metric needed |
| User dwell / cursor hover | Speculative |

### 6.3 How to detect cache incoherence

The migration could re-introduce cache incoherence if the substrate
flag flips while cached entries exist. Detection:

| Symptom | Detection |
|---------|-----------|
| User reports "I see Sun-in-1st, but the popup says Sun-in-2nd" | Popup-overlay parity smoke (§4.4) catches this in regression; in production, operator inspects via debug click |
| Cache key collision (same key, different result) | Forbidden by cache-key shape (per `PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` §2.7); not possible if key shape is correct |
| Stale entry after chart change | Per-chart cache key invalidates by construction; smoke `smoke_phase2_cache_chart_change.py` proves |
| Substrate-mismatched cache | If the cache survives a substrate flip without invalidation: rule per §2.2 mandates cache invalidation on flip |

No runtime metric. The cache is per-session; incoherence shows up as
visibly-wrong overlay and is investigated then.

### 6.4 How to detect refinement runaway

The substrate's adaptive refinement could in principle run away
(unbounded subdivision). Detection:

| Surface | Detection |
|---------|-----------|
| `stop_reason` in response properties | Already exposed; runaway shows as `max_depth_reached` or `sample_budget_hit` |
| `sample_count` in response properties | If > the validated budget for the viewport, the substrate violated its policy |
| Response wall-time | If a single USER request takes > 5 s on a typical viewport, the substrate is doing too much |

These are all already exposed in the canonical substrate's response
properties (per `screen_pixel_adaptive_refinement.md`). The migration
doesn't add new metrics; it ensures the existing ones flow to the
debug panel.

### 6.5 How to detect stalled convergence

A USER job that resolves but the adaptive convergence flag is
`false`:

| Surface | Detection |
|---------|-----------|
| `converged: false` in response properties | Already exposed (Phase A added `convergence_vs_reference` metrics) |
| Visible block-edges that never resolve to 1 px | Operator-visible; reported as a bug |
| `pixels_above_threshold_pct > 0` after final refinement | Operator alert in debug panel |

No new metric. Use the existing convergence metrics already in the
substrate response.

### 6.6 How to detect interruption storms

| Surface | Detection |
|---------|-----------|
| `__phase2.metrics.abortsObserved` | Read on demand |
| Rapid sequence of `events` of type `user_action` | Inspect the events ring buffer |
| `status` stuck in `paused` for > 10 s after user action | Bug; operator can read `__phase2.status` |

If interruption storms become a measurable problem, this is when a
telemetry case opens. Today the smoke covers the storm correctness
(§4.7); runtime detection is operator-driven.

### 6.7 What we explicitly do not build

| Surface | Why |
|---------|-----|
| Prometheus / StatsD metrics | No metrics infrastructure; would build infrastructure to maintain metrics nobody reads |
| Sentry / error-tracking integration | One operator's local dev today; no aggregation surface |
| Real User Monitoring (RUM) | No telemetry; per-user data is privacy-laden |
| Distributed tracing across endpoints | Single-backend, single-handler; nothing to trace |
| Health dashboards | `/health` endpoint exists; operator reads it on demand |

The page is the dashboard. The console is the alert channel. The
smokes are the regression detectors. That is the entire production
observability surface for this migration.

---

## 7. Failure Doctrine

For each worst-case migration failure: **detection**, **containment**,
**rollback**.

### 7.1 Silent correctness drift

**Description:** the canonical overlay shows X at (lat, lon); the
popup shows Y. The user trusts the wrong answer.

| Surface | Strategy |
|---------|----------|
| Detection | `smoke_popup_overlay_parity.py` (§4.4) catches in regression; operator notices in manual exploration |
| Containment | Flip default to `legacy` immediately; legacy popup-parity is ≥ 99% (lower bar but acceptable) |
| Rollback | Per-deploy: `DEFAULT_SUBSTRATE = "legacy"`. Per-commit: revert. No data migration required |
| Prevention | The popup-overlay parity smoke runs on every commit on the canonical substrate |

### 7.2 Stale cache contamination

**Description:** the cache serves a stale entry for a different
chart / substrate / lat-cap state.

| Surface | Strategy |
|---------|----------|
| Detection | Per-chart cache key (already in cache doctrine §2.7) prevents cross-chart contamination; `smoke_phase2_cache_chart_change.py` proves invalidation on chart change; substrate-flip clears the cache (§2.2) |
| Containment | Cache lives in browser memory only; reload clears it entirely |
| Rollback | Same as above; no persistent state to roll back |
| Prevention | Cache-key invariant + invalidation rules in cache doctrine §3.6 |

### 7.3 Zoom incoherence

**Description:** the overlay was rendered at zoom Z; the map is
now at zoom Y; the overlay paints at Y but its data is from Z.

| Surface | Strategy |
|---------|----------|
| Detection | Cache key includes zoom; entries for zoom Z cannot be served to zoom Y. Visual symptom: bands at wrong positions; operator sees and reports |
| Containment | `zoomend` event fires re-render; existing cache hits at the new zoom serve, others miss and re-fetch |
| Rollback | Per-session: page reload; per-deploy: legacy default (legacy has no cache so no zoom incoherence vector) |
| Prevention | Zoom in cache key + `currentRenderToken` / `AbortController` cancellation on `zoomstart` |

### 7.4 Adaptive runaway

**Description:** the canonical substrate's adaptive refinement
subdivides without bound, consuming the budget and producing a slow,
expensive, possibly-wrong render.

| Surface | Strategy |
|---------|----------|
| Detection | `sample_count` > budget; `stop_reason` = `max_depth_reached` or `sample_budget_hit`; wall-time > 5 s. All already exposed in canonical substrate's response properties |
| Containment | Refinement budgets are enforced per the targeted policy (`screen_pixel_adaptive_targeted.md`); the substrate stops at `max_depth` (default 6 from Phase A) regardless of convergence |
| Rollback | Per-deploy: legacy default; legacy has no adaptive runaway risk because it's static-grid |
| Prevention | The substrate's stopping doctrine (Phase C charter §4) is already in place; the migration must not weaken any of its stop conditions |

### 7.5 Overlay mismatch (canonical vs brute-force wall)

**Description:** canonical XOR vs brute-force exceeds validated
thresholds for a fixture.

| Surface | Strategy |
|---------|----------|
| Detection | `smoke_substrate_parity.py` fails its gate |
| Containment | Don't ship; investigate before proceeding past the failing migration step |
| Rollback | Per-commit: revert the offending change. Per-phase: do not advance to next phase until gate is green |
| Prevention | Run the parity smoke on every commit during Phase 1 and Phase 2 |

### 7.6 Rollback corruption

**Description:** rolling back the migration leaves the page in a
broken state (cache full of canonical entries, layers not cleared,
scheduler in a stuck state).

| Surface | Strategy |
|---------|----------|
| Detection | Rollback validation tests (§4.9); operator manual reload after a flag flip |
| Containment | Page reload is the universal recovery primitive; the substrate flag is per-page-load (§2.3) so a reload guarantees a clean state |
| Rollback | The rollback itself is the recovery; no nested rollback needed |
| Prevention | URL-param + constant flag (no localStorage / sessionStorage / cookies) means there is no rollback state to corrupt |

### 7.7 Interruption-storm pathology

**Description:** rapid user actions cause the scheduler to spend more
time aborting than rendering; net rate of completed renders drops.

| Surface | Strategy |
|---------|----------|
| Detection | `__phase2.metrics.abortsObserved` rises rapidly; `backgroundCompleted` stalls; operator perceives sluggish responsiveness |
| Containment | Existing debounce (400 ms) absorbs most storms; canonical scheduler's idle-grace (200 ms) absorbs gesture flurries |
| Rollback | Per-deploy: legacy substrate has no scheduler so no storm pathology vector (it just runs the latest USER request) |
| Prevention | Smoke `smoke_phase2_cache_storm.py` (per cache doctrine §7.6) covers the case |

### 7.8 Backend regression

**Description:** a backend change (e.g. to `swe.houses` integration,
condition compilation, lat-cap policy) breaks one substrate without
the other.

| Surface | Strategy |
|---------|----------|
| Detection | Smoke run against both substrates; divergence flags the case |
| Containment | Both substrates share Swiss Ephemeris; most backend regressions affect both |
| Rollback | Standard backend revert |
| Prevention | Run both `?substrate=legacy` and `?substrate=canonical` smokes on every backend change during Phases 1–3 |

### 7.9 Aspect overlay regression (deferred phase)

**Description:** aspect overlay (still on legacy `/search-regions` in
Phase 1) breaks because the legacy path changes.

| Surface | Strategy |
|---------|----------|
| Detection | `smoke_aspect_overlay_legacy.py` (new) covers visible aspect features |
| Containment | Aspect overlay is in scope for a separate migration phase (after houses are stable on canonical); during Phases 1–3, aspect remains on legacy |
| Rollback | Standard for the contributing change |
| Prevention | Aspect smoke runs alongside the others |

---

## 8. UX Continuity Doctrine

The user must not perceive a paradigm shift mid-session. Specifically:

### 8.1 Contemplative tone

| Constraint | Migration response |
|------------|--------------------|
| No new animations on substrate flip | The flip requires a page reload; the reload is the only "transition" |
| No "we're migrating!" banner | The substrate flag is operator-visible (URL or console); never user-visible |
| No new spinner classes | Existing render-status text covers progress; debug-only |
| No celebratory paints | The user receives a faster, more honest overlay; that is the only reward |

### 8.2 Responsiveness

| Constraint | Migration response |
|------------|--------------------|
| First paint must not regress | Canonical USER fetch at single-condition / 720×450 is ~0.5 s (per substrate timing); comparable to legacy |
| Subsequent identical requests must be faster | Cache hits on canonical serve instantly; legacy has no cache, so canonical is strictly faster on repeat |
| Pan/zoom continuity | Existing 400 ms debounce + scheduler pause-on-gesture continues |
| No multi-second blocking states | Scheduler is single-active; no concurrency penalty |

### 8.3 Trust

| Constraint | Migration response |
|------------|--------------------|
| Popup-overlay agreement | Mandatory parity (§4.4); 100% on canonical |
| Visible bands match analytical bands | Brute-force wall validation (§4.3) within XOR thresholds |
| No hidden auto-fallback | Substrate is operator-set, operator-visible; user always knows (via the console) which substrate is running |
| No silent approximation hiding | The canonical substrate's block edges are visibly honest; visible mismatch (when present) signals "more refinement needed" |

### 8.4 Readability

| Constraint | Migration response |
|------------|--------------------|
| Map readability sacred | Both substrates respect the basemap; canonical's block-paint is opacity-stacked per `MASK_PALETTE`, never opaque |
| Cities, labels remain visible under overlay | No change to `CITY_MARKER_PANE` z-index handling |
| Aspect overlay remains visible | Stays on legacy through Phase 1; visible behaviour identical |
| Aura PoC chrome doesn't bleed in | Step 0.2 fences it behind a debug flag |

### 8.5 Continuity during zoom/pan

| Constraint | Migration response |
|------------|--------------------|
| Zoom doesn't blank-then-paint | Existing `currentRenderToken` and (canonical) scheduler ensure prior overlay stays until new is ready |
| Pan-and-stop renders new viewport once | Debounce + single-active scheduler enforces this |
| Mid-gesture aborts don't leave artefacts | `clearLayers()` + canvas-clear on every render start |
| Rapid gestures don't queue | Scheduler clears pending on every gesture |

### 8.6 Absence of visual chaos

| Anti-pattern | Migration response |
|--------------|---------------------|
| Stacked layers from successive renders | Per-render `clearLayers()` for vector; per-render canvas-clear for canonical |
| Half-painted blocks during canonical refinement | Acceptable per Phase C charter §9 (refinement is visible computation); not chaos |
| Substrate-mismatch artefacts (legacy polygon + canonical canvas at once) | Forbidden by §2.2 (adapter never mixes substrates per render) |
| Aspect overlay flickering during migration | Aspect stays on legacy through Phase 1; flicker risk avoided |

---

## 9. Anti-Overengineering

This section enumerates temptations specific to substrate migration
and rejects each. Append new temptations as they arise; doctrine
drift is the primary failure mode of migration work.

### 9.1 What not to build yet

| Tempting feature | Why deferred |
|------------------|--------------|
| Substrate-pluggable architecture for N>2 substrates | Two substrates with a single flag is all this migration requires; N>2 is YAGNI |
| Feature-flag service / rollout-percentage system | URL param + Python constant covers per-page-load + per-deploy; nothing more is needed |
| A/B testing infrastructure | No telemetry → cannot measure A/B outcomes; speculative |
| User-segment flags | No user identity layer; out of scope |
| Cookie-based substrate preference | Per-page-load flag is correct; persistence introduces stale-flag risk |
| Auto-fallback on canonical error | Forbidden by §2.4; mask regressions |
| Backend response caching (cross-session) | Cache integration plan defers this explicitly |
| Persistent cache (`localStorage` / `IndexedDB`) | Same; deferred there, deferred here |
| Web Workers for cache management | Browser main thread handles current load |
| Substrate-level streaming | Single-shot fetches are fine; streaming is not yet justified |
| Server-side substrate decision | Frontend-driven flag is simpler; flip moment is on page load |
| Aspect overlay migration in same phase as houses | Phase 1 = houses only; aspect = Phase 2 (out of this doc's scope) |
| Aura migration in same phase | Aura is deferred per Phase C charter §10; substrate migration unblocks it but doesn't include it |
| Geocoder integration | Out of scope; the substrate change doesn't depend on geocoder |
| Account / authentication | Out of scope; cache is per-session anyway |
| Migration progress dashboard | The console / smoke reports are the dashboard |
| Animation between legacy and canonical overlays | Reload is the transition; no in-page animation |
| "Hybrid" rendering that uses legacy polygons for some conditions and canonical for others | Forbidden by §2.2 isolation rule |

### 9.2 Unnecessary abstraction risks

| Pattern | Risk |
|---------|------|
| `SubstrateProvider` interface with `register()`, `unregister()`, `enumerate()` | Premature framework; one flag, two paths, no plugin system |
| Generic "RenderEngine" abstraction | Same; the renderer is "paint polygons" or "paint mask," not a pluggable framework |
| Strategy pattern for cancellation primitives | Two primitives, both honoured at the adapter; no strategy framework needed |
| Event bus for substrate state changes | Console logs are enough |
| Migration state machine | Per-phase smoke gates are the state machine |

### 9.3 Speculative infrastructure

| Item | Why speculative |
|------|-----------------|
| Centralised migration log service | No service infrastructure to host it |
| Migration metrics aggregation | No metrics surface to aggregate |
| Cross-migration migration plan template | This doc *is* the template; future migrations inherit by reference, not by abstraction |

### 9.4 Telemetry fantasies

| Telemetry | Why fantasy |
|-----------|-------------|
| Per-substrate user engagement metrics | No engagement metric surface |
| Per-substrate "satisfaction" measurements | Subjective; no infrastructure |
| Heatmaps of user-visible substrate flips | No telemetry collection |
| Cache hit rate trended over time | Aggregation requires storage |
| Per-fixture brute-force XOR trended over time | Smoke runs produce a JSON report per run; trending requires aggregation infra |

### 9.5 Premature distributed-cache thinking

| Pattern | Why deferred |
|---------|--------------|
| Server-side cache shared across sessions | Cache doctrine defers this; no auth / privacy / invalidation infra |
| CDN-cached overlay tiles | Tiles are per-chart; CDN cache wouldn't help; substrate is not tile-based today |
| Distributed scheduler across clients | Single-client browser sessions; no multi-client coordination |
| Cache mirroring / replication | None of the persistence-layer prerequisites exist |

### 9.6 Premature persistence layers

| Layer | Why deferred |
|-------|--------------|
| `localStorage` cache | Per-cache doctrine; invalidation contract unsolved |
| `IndexedDB` cache | Same |
| Server-side database for charts / overlays | Charts are per-session; no persistence requirement |
| Session-restore feature | Out of scope; reload is the universal primitive |

---

## 10. Final Deliverable Statement

| Deliverable | Status |
|-------------|--------|
| Migration doctrine / architecture document | **This document** |
| Production renderer replacement | **Not in this delivery.** Sequenced by §3 with gates |
| Speculative rewrites | **None.** Each step is minimal |
| Aura implementation | **Out of scope.** Deferred per Phase C charter §10 |
| Animation implementation | **Out of scope.** Forbidden per substrate charter |
| New endpoints | **None.** Migration uses existing `/screen-pixel-truth` |
| Astrology-math changes | **None** |

This document is the migration plan. The migration itself is a
sequence of small commits, each landing under its own gate. The
plan deliberately does not pre-write any code. Each step's
implementation lives in its own commit with its own scope.

---

## 11. Discoveries While Grounding This Document

These were surfaced during the audit and are recorded here so future
work can address them; this document does not solve them.

### 11.1 Aura PoC endpoints are still wired in production

`map_CURRENT.html` calls `/aura-raster` and `/aura-raster-adaptive`
(lines 1968, 1981) despite the Phase C charter declaring the
`aura_field_engine.py` substrate superseded archaeology. **Step 0.2**
of §3 addresses this by fencing them behind a debug flag. The
broader question — whether the aura PoC code should be deleted or
retained behind the flag — is left to the implementer.

### 11.2 Legacy `/search-regions` has two modes; only one is honest

`truth_grid` mode (default) is grounded in honest per-cell
classification with boundary refinement. `contour` mode is the
gaussian-smoothing + skimage path that the rendering reset rejected.
**Step 0.3** marks `contour` mode as archaeology in place. The
migration treats `truth_grid` as the "legacy" baseline for parity
comparison.

### 11.3 The substrate change is a paradigm swap

Legacy returns polygons; canonical returns per-pixel masks. There is
no feature-by-feature parity test; the only honest parity is
**pixel-level XOR against the brute-force wall** (§4.3). Polygon-shape
parity is meaningless across this boundary.

### 11.4 Multiple `currentRenderToken` consumers in `map_CURRENT.html`

At least 10 check-sites exist (lines 2322, 2346, 2419, 2439, 2502,
2519, 2863, 2881, 3042, 3130, 3159). The scheduler integration must
compose with — or supplant — every one of these. Step 1.4 of §3
handles this for the house path; aspect / aura paths are deferred.

### 11.5 Aspect overlay is a separate migration phase

`/search-regions`' aspect overlay uses staged coarse/medium/final
resolutions; the substrate's adaptive refinement is structurally
different. Migrating aspect alongside houses would balloon scope
and risk. **Aspect migration is explicitly Phase 2** (after houses
are stable on canonical). This doc does not specify aspect
migration; it requires its own doctrine doc when sequenced.

### 11.6 The Phase-2 cache integration plan's Step 0 is satisfied here

`docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` §10 Step 0
requires recording the substrate-path decision. **Step 0.1** of this
document is that record. Cache integration begins after Phase 1 of
this migration.

### 11.7 No telemetry, ever (in this scope)

The migration is operator-driven; observability surface is the
console, the network tab, and the smoke reports. The doctrine
forbids building any telemetry infrastructure as part of this
migration. Telemetry is its own doctrine pass, gated on need.

---

## 12. Recommended Next Implementation Step

**Step 0.1 — record the substrate-path decision in
`ai_context/decisions.md`**. The exact wording is given in §3 Phase
0 Step 0.1 above. This is the smallest reversible commit; it
authorises every subsequent step.

After Step 0.1:

1. **Step 0.2** — fence the aura PoC calls (one PR, low risk).
2. **Step 0.3** — annotate `contour` mode as archaeology (one PR,
   no behaviour change).
3. **Step 1.1** — extract the Phase-2 scheduler (one PR, no
   `map_CURRENT.html` change yet).
4. **Step 1.2** — build the substrate adapter (legacy-only)
   (one PR, no behaviour change).

Each of these is reversible in one commit. Each has a smoke gate.
None changes user-visible behaviour. Only after all four are green
does Step 1.3 (canonical wiring behind the flag) land.

---

## 13. Document Provenance

| Field | Value |
|------|------|
| Author surface | Architecture draft, this conversation |
| Reviewed against | `main_centerline_FIXER.py` (endpoints), `map_CURRENT.html` (current production state), `map_SANDBOX_phase2_cache.html` (canonical scheduler reference), `truth_grid_engine.py` (legacy truth-grid mode), `validation/reports/*.json` (validated thresholds and budgets), all current Phase C doctrine docs |
| Authority on conflict | Foundational architecture, then Phase C charter, then this doc, then cache integration plan |
| Supersedes | Nothing |
| Operationalises | `docs/PHASE_C_RENDERING_ARCHITECTURE.md` §10 step 2 |
| Status | Design only; no code authorised by this document |

When this document and any other doc disagree, this document yields
to the foundational architecture and to the Phase C charter, and
otherwise wins until explicitly amended in writing.
