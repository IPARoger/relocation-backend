# ARCHITECTURE_AND_BACKEND_CANON.md

**Document role:** definitive onboarding and system transfer manual for the current Astrological Geography / Relocation Map backend architecture.  
**Generated from:** `ALL_PROJECT_DOCUMENTS.txt` by local line/block parsing of all archive sections whose file headers matched architecture, backend, database, cache, GeoJSON, validation, rendering, API, Supabase, truth-grid, and migration keywords.  
**Scope:** active and near-active engineering architecture only. Long-term roadmap features are excluded from active setup and quarantined at the bottom under **Future Structural Excellence Inventory**.

---

## 0. Non-Negotiable Product Guardrail

**Reveal structure. Preserve judgment. Cities are secondary targets.**

The platform exists to strictly isolate and visualize geographical chart conditions. It must make chart conditions visible, searchable, inspectable, replayable, and comparable across geography. It must not convert those conditions into hidden interpretation, optimization scores, or product-authored verdicts. The software reveals where symbolic conditions hold; the interactive human user decides what they mean.

This guardrail has immediate engineering consequences:

1. **Layer 1 computation is sovereign.** Birth data, ephemeris inputs, house system, zodiac mode, and requested geographical conditions define the truth being searched. Display controls, AI copy, style presets, and convenience labels must not alter Layer 1 membership.
2. **The map is a condition field, not a city recommender.** Cities are searchable and selectable targets inside the computed geography, but the computational starting point is not a city list. The engine asks: “where on Earth does this chart condition hold?” Candidate cities are then discovered inside the resulting field.
3. **Interpretation remains human.** The system may later assist, explain, or compare, but active backend and persistence architecture must preserve factual chart conditions separately from interpretive notes.
4. **Popup truth wins.** Point inspection is the canonical truth for “what is true here.” Overlays are exploratory “where” fields. Account/chart pages carry the full scientific record.
5. **No hidden ranking.** Saved searches, favorites, comparisons, and overlays must not imply “best,” “winner,” or “ideal” unless the user has explicitly declared ranking criteria.

This manual therefore treats backend architecture as a trust machine: every endpoint, cache key, payload, data model, and validation harness exists to protect inspectable geometry.

---

## 1. Source Extraction and Audit Boundary

### 1.1 Programmatic block parsing

The archive was parsed by detecting file separators of the form:

```text
=== FILE: <path> ===
```

A matched engineering block was any file segment whose path contained one or more of:

```text
architecture, backend, cache, caching, geojson, database, validation,
truth_grid, api, supabase, render, endpoint, migration
```

The deeper pass used these matched blocks as the engineering corpus. Duplicate onboarding/archive copies were treated as corroborating mirrors rather than separate authorities when their content repeated a canonical file.

### 1.2 Principal authority order

When documents conflict, the active authority hierarchy is:

1. `relocation_map_architecture.md`
2. `PHASE_C_RENDERING_ARCHITECTURE.md`
3. `PHASE_C_PRODUCTION_MIGRATION_PLAN.md`
4. `PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`
5. `PHASE_C_IMPLEMENTATION_PROTOCOL.md`
6. Current contracts and data-model documents
7. Onboarding and archive copies as secondary mirrors

Historical and superseded files are preserved as archaeology. They may explain why decisions were made, but they do not override the current rendering, cache, or data-model doctrine.

---

## 2. System Identity and Layer Architecture

The platform is a chart-centered relocation geography system. Its current core capabilities include:

- truth-grid house overlays for Planet-in-House searches;
- staged/shared-grid ASC overlays for faster ASC all-major-aspect rendering;
- Angle-in-Sign MVP for ASC and MC;
- Planet Aspect to Angle overlays using backend centerlines;
- point-and-click popup truth checks for local relocated chart facts;
- debug geometry mode for tracing backend canonical features through frontend display features.

The product architecture is **map-first but not map-only**. The map is the primary instrument for geographical discovery, while chart records, saved explorations, favorites, comparison sets, and settings supply persistence and workflow continuity. The system has moved beyond a single map experiment into a chart-centric product platform.

### 2.1 Layer 1 vs Layer 2

Layer 1 contains the computational truth:

- birth datetime;
- birth place;
- timezone / ephemeris inputs;
- selected house system;
- zodiac mode;
- requested conditions such as planet in house, angle in sign, and aspect to angle;
- saved investigation conditions as semantic requests.

Layer 2 contains user or product preferences that influence presentation or defaults without changing core truth:

- orb defaults;
- minor-aspect enablement;
- helper layers;
- ontology packs;
- visual settings;
- user settings snapshots.

**Layer 2 must not alter Layer 1 membership.** If a user changes style, mute state, or visual display mode, the underlying astrological set remains unchanged. If a settings snapshot is saved, it exists to replay the search honestly, not to smuggle renderer internals into the truth model.

### 2.2 Canonical truth vs display geometry

A repeated architecture law is the separation between canonical truth and display adaptation. Backend geometry and sampled truth determine membership. Frontend wrapping, clipping, pane ordering, color, and material presentation adapt that truth for display. Display adaptation must never change logical astrology semantics.

Acceptable imperfections for MVP include rough visual edges, visible discontinuities where the renderer is limited, and proof-of-concept colors. Not acceptable: false region membership, misleading fills, topology corruption, overlay identity changing at the dateline, or visual smoothing that causes popup truth to disagree with overlays.

---

## 3. Backend Endpoint Architecture

The current backend is centered in `main_centerline_FIXER.py` with several known production, canonical, validation, and archaeology endpoints.

### 3.1 `POST /search-regions` — legacy production overlay pipeline

`/search-regions` is the current legacy overlay endpoint. It accepts:

- birth parameters;
- `house_conditions`;
- `angle_sign_conditions`;
- `aspect_overlay`;
- `resolution`, defaulting around `1.5°`;
- `generation_mode`, either `truth_grid` or contour;
- `truth_grid_resolution`, defaulting around `0.75°`;
- `truth_grid_boundary_refine`.

Its output shape is a GeoJSON polygon `FeatureCollection`.

The legacy endpoint has two internal modes:

1. **Truth-grid mode.** This is the honest legacy substrate. It uses `truth_grid_engine.generate_truth_grid_house_features` with boundary refinement to produce polygon features grounded in per-cell classification.
2. **Contour mode.** This is the older smoothing path: per-cell `swe.houses` classification produces a boolean mask; `scipy.ndimage.gaussian_filter(sigma=1.2)` smooths it; `skimage.measure.find_contours(0.5)` extracts contours; `approximate_polygon(tolerance=0.08)` simplifies. Current doctrine marks this as archaeology because smoothing can make visual truth diverge from point truth.

The production frontend historically renders `/search-regions` through Leaflet vector polygons using `polygonLayer`, `aspectLayer`, and `auraLayer` in `map_CURRENT.html`. The current default in `map_CURRENT.html` is `generation_mode: "truth_grid"`, `truth_grid_resolution: 0.75`, and `truth_grid_boundary_refine: true`.

### 3.2 `POST /screen-pixel-truth` — canonical screen-space substrate

`/screen-pixel-truth` is the validated canonical substrate for visible overlays. It accepts:

- birth parameters;
- explicit screen-derived points: `points: [[lat, lon], ...]`;
- `conditions`, with documented maximum around six;
- `apply_lat_cap`.

It returns a dense `masks` array, one bitmask per input point, in input order. The client paints the result to a Canvas layer by screen block. This substrate samples the current Leaflet viewport at the current zoom, so every visible world copy can be classified independently and dateline behavior becomes correct by construction.

The semantic shift is important: legacy polygons say “this vector shape encloses cells classified as true,” while canonical screen-pixel truth says “this visible pixel block was classified at its screen-derived center.” The canonical path is therefore tighter against point popup truth, but it can show block edges until adaptive refinement converges.

### 3.3 `/relocated-chart` — point truth endpoint

The popup endpoint is independent of overlay rendering. It evaluates the clicked latitude/longitude directly using the same ephemeris/house calculation basis. It is the trust anchor for overlay validation: if a point popup says a planet is in a given house or an angle has a given degree/sign, the overlay must not imply otherwise.

### 3.4 Validation and archaeology endpoints

The architecture preserves several endpoints even when they are not production-default:

- `/brute-force-grid` is retained as the canonical validation wall.
- `/classify-points` is retained for per-point all-house or point-classification use cases.
- `/aura-raster`, `/aura-raster-adaptive`, and `/aura-field` are retained as archaeology or debug-gated proof-of-concept paths, not as default production architecture.
- `/search-regions` remains available during migration and may remain callable for archaeology/validation after canonical migration, but should not be extended as the future path.

---

## 4. GeoJSON, Truth Grid, and Rendering Substrate

### 4.1 Truth-grid house overlays

Truth-grid generation is the adopted architecture for honest house regions in the legacy substrate. It samples a geographic grid, classifies each cell according to the requested condition, and merges truth cells into manageable polygon features. This approach replaced earlier comfort with contour-only pipelines because seams and topology can lie if the renderer smooths or closes shapes incorrectly.

Truth-grid output remains GeoJSON-oriented, which works with Leaflet polygons. Its current strength is honest categorical membership. Its limitation is that it remains a geographic grid; visual exactness at display scale can still diverge from point inspection near edges.

### 4.2 Screen-space adaptive truth

The canonical target substrate is screen-space classification. Instead of sampling the world on a fixed lat/lon grid and then projecting to the screen, the system samples the visible screen, converts those pixels to lat/lon, classifies them, and paints masks directly. This solves classes of dateline/world-copy issues because each visible world copy gets its own sampled points.

The canonical substrate uses adaptive refinement. Coarse block sizes can refine toward smaller blocks in regions where conditions change, edges are near, gradients are strong, or convergence requires it. It prioritizes the visible viewport first and treats adaptive refinement as targeted policy, not global slowdown.

### 4.3 Centerlines and aura

Aspect-to-angle centerlines are mathematically exact anchors. Aura or material-strip rendering must not be a blur, glow, or widened stroke pretending to be truth. Aura doctrine defines it as occupancy widening from exactness: discrete bands at increasing orb thresholds such as exact, `≤ 0.5°`, `≤ 1°`, `≤ 2°`, and outward as product settings allow.

Rendering intensity is then a weighted visual composition over truthful bands. The intensity must be non-linear: the outer aura remains restrained, the strongest intensity is reserved for the exact line or near-exact band, and the mid-orb must not become a broad opaque corridor.

The engine remains authoritative for exact line geometry and popup truth. Aura is a non-certifying field. It communicates proximity to exactness, not membership in a categorical astrological condition.

### 4.4 Cusp softness is separate from aura

House cusp presentation softness, often discussed around a `~2°` display gradient, is not the same as aspect aura, which is an orb/intensity field often in the `~5–8°` range depending on aspect family and settings. These systems must not share the same blur, ramp, or metaphor. House regions are categorical membership fields; aspect aura is angular intensification around a centerline.

---

## 5. Cache Architecture

### 5.1 Current cache boundary

The Phase-2 cache is designed around `/screen-pixel-truth`, not `/search-regions`. The key shape is based on:

```text
(chart, bounds, zoom, block, conditions, lat_cap)
```

Legacy `/search-regions` would require a different key shape involving `resolution`, `generation_mode`, `truth_grid_resolution`, `truth_grid_boundary_refine`, `house_conditions`, `angle_sign_conditions`, and `aspect_overlay`. Therefore, cache entries are not reusable between legacy and canonical substrates. A substrate flag flip must invalidate or bypass old cache entries.

### 5.2 Scheduler model

The production cache architecture uses a single-active-job scheduler. It distinguishes foreground user requests from background warming jobs.

Core rules:

- one active job at a time;
- user requests outrank background expansion;
- user gestures interrupt background work;
- no half-cached entries;
- cache only on full success;
- cache coherence must survive chart change, zoom change, condition change, and lat-cap change;
- background jobs must never block immediate user-visible work.

The canonical path uses `AbortController` for fetch cancellation. Legacy currently uses `currentRenderToken` checks in `map_CURRENT.html`. During migration the adapter must honor both cancellation primitives.

### 5.3 Priority protocol

The cache system supports immediate visible truth first, then opportunistic expansion. The active viewport is rendered first. Neighboring zoom levels and likely next-use requests can be warmed only after the user’s current request is served. Priority A–H doctrine exists for cache planning, but no predictive cache layer may override user input.

### 5.4 Memory, disk, and persistence

The current cache is browser-session oriented. Persistent disk cache, IndexedDB, server-side overlay cache, distributed cache, CDN tiles, and cross-session overlay reuse are intentionally deferred. Persistent cache is dangerous before invalidation rules, account identity, privacy, chart ownership, and substrate stability are settled.

### 5.5 Cache failure doctrine

Primary cache failure classes include stale chart contamination, zoom incoherence, substrate mismatch, adaptive runaway, and interruption storms. The containment strategy is deliberately simple: cache lives in browser memory, reload clears it, substrate flag is per page load, chart changes invalidate by key, and smokes prove chart-change behavior.

---

## 6. Migration Architecture: Legacy to Canonical

### 6.1 Migration strategy

The migration plan rejects direct replacement in favor of an adapter layer. A unified `runOverlay(payload, substrate)` dispatches to either:

- legacy `/search-regions`, returning polygons; or
- canonical `/screen-pixel-truth`, returning masks painted to Canvas.

The adapter exists for reversibility. Default starts as legacy, then flips to canonical after validation gates pass. No in-session substrate flipping is allowed; the flag is per page load.

### 6.2 Feature flag

The substrate flag is intentionally minimal:

```text
?substrate=legacy
?substrate=canonical
```

A Python constant such as `DEFAULT_SUBSTRATE` can provide the default. URL parameter wins over the constant. There is no feature-flag service, rollout percentage, user-segment flag, cookie persistence, localStorage preference, or A/B infrastructure.

### 6.3 Rollback

Rollback must be deterministic:

- reload with `?substrate=legacy` for per-session recovery;
- change `DEFAULT_SUBSTRATE` back to legacy for deploy rollback;
- standard git revert for commit rollback;
- no auto-fallback, because auto-fallback masks regressions.

### 6.4 Integration order

The planned order is:

1. Record the substrate-path decision.
2. Fence aura proof-of-concept endpoints behind debug flags.
3. Mark contour generation mode as archaeology.
4. Extract the Phase-2 scheduler.
5. Build adapter legacy-only.
6. Wire canonical substrate behind the adapter.
7. Wire scheduler/cache onto canonical.
8. Run parity validation.
9. Flip default to canonical.
10. Maintain a stabilization window.
11. Retire or mark legacy paths.

---

## 7. Payload and Search Contract

### 7.1 Genie render payload

When the user presses Search Map, the Genie emits an immutable `genie_render` payload. Live card state is not search truth after render. Pinning, saving, and replaying reference the rendered snapshot, not current DOM state. Re-rendering creates a new timestamp or render identity; prior snapshots are not mutated.

### 7.2 Variable model

Supported variable types are:

- `planet_in_house`;
- `angle_in_sign`;
- `aspect_to_angle`;
- `transit_through_house` as experimental/off-by-default;
- `transit_aspect_to_angle` as experimental/off-by-default.

Explicitly excluded from v1 Genie are planet-aspect-to-planet variables, sign presets as separate variable types, and standalone exclusion types.

### 7.3 Polarity and NOT

NOT is not a separate variable type. It is `polarity: "exclude"` on the same variable type. Excluded variables stay in canonical `variables[]`. In the legacy adapter, exclude variables do not enter positive `house_conditions`, `angle_sign_conditions`, or `aspect_overlay`; they go to `notExclusions[]` only.

### 7.4 Mute and solo

Mute and solo are display controls in `layerControls`; they are not Layer 1 search truth. A muted condition remains part of the investigation; it is visually hidden or de-emphasized. Solo isolates temporarily. Neither should change backend membership or saved semantic conditions unless explicitly designed as display state.

### 7.5 Legacy adapter limits

The legacy adapter maps only a limited subset:

- first three `planet_in_house` variables to A/B/C;
- first `angle_in_sign`;
- first `aspect_to_angle`.

Overflow must not be silently dropped. The contract requires degradation metadata when canonical payloads exceed legacy capacity. The sandbox has historically omitted some degradation metadata, and that drift is explicitly tracked.

---

## 8. Data Model and Persistence Architecture

### 8.1 Core objects

The product data hierarchy is chart-centered:

- Professional Account / User;
- Professional Workspace, where applicable;
- Client;
- Chart Record / Birth Profile;
- Places;
- Saved Charts;
- Saved Investigations;
- Favorite Cities / Favorite Locations;
- Comparison Sets;
- Notes;
- Settings.

A Chart Record owns favorites, saved explorations, history, and comparisons. Active chart context must never switch silently. `activeChartRecordId` or equivalent is required in map render payloads and map workflow state.

### 8.2 Chart Record

A Chart Record stores the natal data required to compute relocation conditions. Current Web 2.0 scope assumes accurate birth time. Unknown or ambiguous birth time workflows are future boxes, not active requirements. House system is a hard compute parameter. Current location may become a first-class analytical object, but it must not confuse natal chart identity.

### 8.3 Saved explorations

A saved exploration persists semantic search conditions and map context. It should include:

- chart ownership;
- condition list;
- map center;
- zoom;
- bounds/viewport facts where relevant;
- settings snapshot;
- optional title and notes.

It must not save renderer internals as product truth. Prohibited data includes debug flags, generation mode, transient cache keys, DOM state, internal renderer substrate, and mutable visual-only artifacts unless explicitly stored as display state.

### 8.4 Favorites and comparisons

Favorites belong to one Chart Record. A favorite city or map point opens a relocated chart for that location. Comparison sets compare selected places under the same chart context unless explicitly designed otherwise. “Best place on Earth” is rejected as a frame; constrained comparison is the product story.

### 8.5 Supabase schema sandbox

The schema sandbox plan is local-first and not yet a runtime dependency. Proposed tables include:

- `professional_accounts`;
- `clients`;
- `birth_profiles`;
- `places`;
- `saved_charts`;
- `saved_investigations`;
- `favorite_cities`;
- `comparison_sets`;
- `comparison_set_places`;
- `user_settings`;
- `tags`;
- `entity_tags`;
- `notes`.

The migration plan proposes SQL migrations `00001`–`00005`, JSON schemas for saved investigation conditions and settings snapshots, and a local/dev Supabase reset only after approval. It explicitly forbids adding Supabase client packages, environment keys, or changes to `map_CURRENT.html` during schema planning.

### 8.6 JSON vs normalized fields

Stable identity, ownership, and queryable relationships should be normalized. Flexible condition payloads and settings snapshots may live as JSON with schema validation. Conditions JSON is Layer 1 semantic request data; settings snapshot JSON is Layer 2 replay data. A linter should reject renderer keys in saved conditions.

---

## 9. Validation Framework

### 9.1 Validation corpus

Validation records, reports, screenshots, narratives, and smoke outputs are part of the proof corpus. They preserve evidence for baseline charts, high northern charts, high southern charts, antimeridian behavior, truth-grid contradictions, Angle-in-Sign behavior, staged ASC overlays, dropdown regressions, and UX regressions.

### 9.2 Brute-force wall

The brute-force wall is the reference method. It must remain available as a control specimen. The architecture repeatedly instructs: build the wall first, then intelligently back off. Optimization is allowed only after the final truth target is known.

### 9.3 Required smoke categories

Important validation scripts and planned smokes include:

- `smoke_map_current.py`;
- `validate_sprint_dc_ic.py`;
- `smoke_phase2_cache.py`;
- `smoke_substrate_parity.py`;
- `smoke_popup_overlay_parity.py`;
- aspect overlay legacy smoke during staged migration;
- cache chart-change, storm, drainage, and interruption smokes.

### 9.4 Parity rules

Canonical substrate parity is measured against brute-force raster truth with XOR thresholds. Example doctrine thresholds include approximately:

- typical single condition: `≤ 0.10%`;
- three-condition overlap: `≤ 0.20%`;
- dense five/six condition cases: `≤ 0.40%`;
- high-latitude cap cases: `≤ 0.50%`.

Popup-overlay parity targets 100% on canonical because the classification basis should be identical. Legacy may be observational near smoothed polygon edges.

### 9.5 Edge cases

Named high-risk cases include:

- high northern charts;
- southern hemisphere cases;
- antimeridian/seam crossing;
- Greenland/Iceland;
- Svalbard/high-latitude refinement;
- dense Americas multi-condition tests;
- cusp-heavy charts;
- polar/above-cap stress tests;
- dense city regions;
- mobile/narrow desktop layout.

---

## 10. File Interaction Boundaries

### 10.1 Frontend map shell

`map_CURRENT.html` is the production map surface. It contains legacy renderer assumptions around polygon FeatureCollections, layer clearing, render tokens, aspect staging, and debug labels. Migration must not rewrite broad unrelated UI while changing substrate. One instability source at a time.

### 10.2 Adapter files

The migration plan allows adapter dispatch either in a new `static/substrate_adapter.js` or inline near the top of `map_CURRENT.html`. What matters is isolation:

- endpoint adapter separate from renderer adapter;
- legacy fetcher separate from canonical fetcher;
- vector rendering separate from canvas mask rendering;
- cancellation semantics preserved;
- cache enabled only on canonical until doctrine changes.

### 10.3 Backend modules

`truth_grid_engine.py` is retained as the honest legacy truth-grid mechanism. `main_centerline_FIXER.py` hosts endpoints and should mark superseded branches clearly. Sandbox HTML files and validation scripts remain reference implementations and proof artifacts.

### 10.4 Doctrine and governance

Significant implementation tasks require closeout covering deferred registry effects, rendering doctrine effects, validation narrative decisions, blocker/trust/deferred/rejected classification, rollback scope, rejected scope, and next-step recommendation. Broad rewrites without measurement are prohibited.

---

## 11. Active Setup Rules for Engineers

1. Do not silently switch rendering substrates.
2. Do not treat visual mismatch as astrology math failure without popup and brute-force evidence.
3. Do not migrate aspect overlays in the same step as house substrate migration.
4. Do not add persistent cache before invalidation doctrine is fully proven.
5. Do not save renderer internals inside saved investigations.
6. Do not let mute/solo/foreground/background mutate Layer 1 search truth.
7. Do not hardcode display labels into engine semantics.
8. Do not stamp variable labels onto map regions.
9. Do not hide debug or validation uncertainty behind polish.
10. Do not use AI, scoring, or generated summaries as navigation structure in the current non-AI core.
11. Do not add full accounts/auth/payments/client ACL until local chart persistence and saved exploration replay are proven.
12. Do not extend superseded contour or aura proof-of-concept paths as if they are current production doctrine.
13. Do not build feature-flag services, telemetry dashboards, or distributed cache infrastructure for the migration.
14. Do not claim a region is good or bad. Store and reveal factual chart conditions.

---

## 12. Audit Findings and Drift Risks

The deeper pass found several known drift points already documented in the archive:

- `Search Map` is the adopted payload language, but some sandbox UI still says `Render`.
- Degradation metadata is required when canonical Genie variables overflow legacy adapter capacity; sandbox behavior has lagged.
- Aura proof-of-concept endpoints remain wired historically and must be debug-fenced.
- Legacy contour mode exists but is superseded by truth-grid and canonical screen-space truth.
- Store v3 / backend classify bodies / renderer GeoJSON contracts are explicitly out of scope in some UI audit documents and should not be invented prematurely.
- Latitude cap policy and copy remain unresolved and require a single user-facing explanation.
- MC framing language needs one documented calculation-assumptions source.
- Validator permanence must be decided explicitly where older docs treat tools as temporary.

---

## 13. Future Structural Excellence Inventory

This section quarantines future structural opportunities. Items here are not active setup instructions and must not be implemented without a new scoped plan.

### 13.1 Cache and performance

- Persistent browser cache using IndexedDB after chart identity, substrate, condition schema, and invalidation rules are stable.
- Server-side overlay cache after auth/privacy/data-retention rules exist.
- Probabilistic cache warming based on likely pan/zoom behavior.
- Adaptive “bacteria” clustering around borders for efficient sampling, after brute-force wall target is proven.
- Reuse between adjacent zoom levels, neighboring tiles, and condition families, gated by correctness smokes.
- Negative-space inheritance for NOT/exclusion searches once positive layer semantics are stable.

### 13.2 Rendering substrate

- Full canonical migration of aspect overlays after house canonical migration stabilizes.
- Centerline/aura unification on a single sampled truth field.
- Production-grade aura material strip with proportional compression and non-linear centerline intensification.
- Child-color overlap system replacing naive alpha mud.
- Style presets that alter palette/material finish without changing math truth.
- Screen-space topology IDs only after canonical substrate is stable enough to need them.

### 13.3 Validation

- Golden screenshot CI.
- Formal regression dossier automation.
- Expanded polar/latitude stress suite.
- Long-term fixture manifest with “run these five” command.
- Curated brute-force export hygiene and storage policy for large GeoJSON/raster artifacts.

### 13.4 Persistence and product infrastructure

- Supabase migration after local-first objects prove themselves.
- Auth/account/client ACL.
- Share links and professional export with permission model.
- Comparison storage with stable replay semantics.
- Birth time uncertainty ranges and outer-bound geography fields.

### 13.5 Geocoder and city intelligence

- Global disambiguation UX beyond population ranking.
- Provider-level geocoder caching.
- City identity normalization, transliteration, and ranking heuristics.
- Candidate-city discovery inside computed fields without converting the engine into a city-first recommender.

### 13.6 AI and interpretation

- AI intake that translates user intent into explicit search conditions.
- AI comparison support grounded in saved facts.
- Professional assist suggestions that remain subordinate to human judgment.
- Interpretation outputs stored separately from chart facts and labeled as interpretive content.

**Closing law:** Future excellence is welcome only when it preserves the core guardrail: **Reveal structure. Preserve judgment. Cities are secondary targets.**
