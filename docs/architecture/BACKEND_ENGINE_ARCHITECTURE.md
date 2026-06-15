# BACKEND_ENGINE_ARCHITECTURE.md

**Status:** Canonical engineering manual for backend engine architecture, calculation boundaries, coordinate-grid logic, GeoJSON and screen-space substrate relationships, endpoint contracts, cache/scheduler constraints, persistence models, and future infrastructure inventory.  
**Source archive:** `ALL_PROJECT_DOCUMENTS.txt`  
**Generation method:** deeper three-pass local Python extraction and consolidation.  
**Total archive file blocks parsed:** 196  
**Backend/architecture source blocks matched:** 196  
**Audit hash:** `90e1ae96336fd53e`

---

## 0. Constitutional Engineering Rule

**Reveal structure. Preserve judgment. Cities are secondary targets.**

The backend exists to compute, expose, validate, and preserve geographical chart-condition truth. It maps chart conditions onto coordinates. It makes those conditions visible, searchable, inspectable, comparable, replayable, and auditable. It must not incorporate automated interpretation logic into the core schemas or calculation paths.

The backend may compute: relocated Ascendant, Midheaven, house placements, angle signs, condition membership, aspect-to-angle proximity, truth-grid regions, screen-space masks, GeoJSON features, validation walls, cache keys, saved search payloads, and chart-record ownership. The backend may not decide whether a city is good, optimal, destined, safe, best, or spiritually correct. Those are interpretive judgments. The backend reveals structure; the human preserves judgment.

Cities remain secondary human markers. A city lookup is a coordinate query and a naming aid. The system’s core computation is not “search the city database for the best place.” The computation is “evaluate chart conditions over geography, then allow humans to inspect named and unnamed coordinates within that structure.”

---

## 1. Extraction Scope and Engineering Categories

The deeper extraction scanned architecture, backend, engine, GeoJSON, JSON, database, cache, calculation, endpoint, API, schema, payload, truth-grid, screen-space, Supabase, storage, coordinate, Swiss Ephemeris, relocated-chart, search-regions, screen-pixel-truth, classify-points, brute-force-grid, aura, centerline, aspect, house, adapter, migration, validation, scheduler, and persistence terms.

Matched backend source blocks were classified as follows:

| Engineering Category | Matched Blocks |
|---|---:|
| api_endpoints_and_payloads | 98 |
| backend_runtime_and_files | 196 |
| cache_scheduler_performance | 79 |
| coordinate_calculation_engine | 187 |
| database_and_persistence | 140 |
| frontend_backend_contract | 183 |
| future_infrastructure | 180 |
| geojson_and_truth_grid | 66 |
| screen_space_and_canonical_substrate | 79 |
| validation_and_rollback | 155 |

The high match count reflects that backend architecture is not isolated to one file family. It appears in rendering doctrine, migration plans, payload contracts, screen inventory, client/chart data models, validation doctrine, cache plans, and institutional memory. This manual consolidates the active engineering meaning while keeping future infrastructure in the final inventory.

---

## 2. Backend System Identity

The backend is the factual engine behind a map-first relocation astrology platform. Its primary job is to evaluate chart conditions at coordinates. It does not begin with cities; it begins with latitude/longitude and chart data. Cities, geocoder results, and saved location names are downstream labels attached to points or candidate areas.

The backend must support three families of truth:

1. **Point truth** — exact or local relocated chart facts at a clicked coordinate or named location.
2. **Field truth** — where a selected condition holds across geography.
3. **Replay truth** — enough chart context, settings, conditions, and viewport state to reproduce a saved investigation.

The backend must also support validation truth: independent or denser comparisons that prove production renderers have not drifted.

### 2.1 Active stack identity

The active stack described across the archive is a Python/FastAPI backend using Swiss Ephemeris-style chart calculations, serving a Leaflet/OpenStreetMap frontend. The frontend consumes endpoints such as relocated chart inspection, region search, screen-pixel truth, brute-force validation, and future payload contracts. The local development environment is intentionally simple and inspectable. Complexity belongs where it protects truth, not where it creates abstraction theater.

### 2.2 Engine morality

The engine’s authority is factual, not interpretive. This boundary matters in code. A response object should not contain “best city,” “recommended move,” “highly favorable,” or similar interpretive judgments as core backend truth. A future AI layer can generate optional downstream text. The engine should return structured facts, metadata, and validation fields.

---

## 3. Coordinate and Calculation Engine

### 3.1 Coordinate-first model

The engine evaluates conditions at coordinates. A coordinate is not merely a city record. It is a latitude/longitude point against which relocated chart facts can be computed. This enables arbitrary-point inspection, wilderness inspection, map-click validation, and city-independent search.

The fundamental loop is:

1. Receive chart inputs or chart record reference.
2. Receive coordinate(s), bounds, or screen sample points.
3. For each coordinate, compute relocated chart facts using the chosen chart parameters.
4. Classify requested conditions against those facts.
5. Return point facts, masks, GeoJSON features, or validation artifacts depending on endpoint.

### 3.2 Point truth calculation

The relocated-chart endpoint family is the local authority. Given a point, it should compute relocated angles and house placements directly from the chart/coordinate model. Popups and detail pages rely on this local truth. Overlay systems must be validated against it.

Point truth should include, as supported by current doctrine: Ascendant, Midheaven, implied Descendant/IC where relevant, house placements, degrees, signs, and relocation-specific facts. Full interplanetary aspects do not change by relocation and therefore should not clutter relocation-specific chart surfaces unless explicitly requested in the broader chart record.

### 3.3 House membership computation

Planet-in-house conditions are categorical. A condition like Sun in 1st is true or false at a coordinate under the chosen house system. Cusp softness may later be displayed, but it must not redefine membership without explicit doctrine. The engine should preserve the underlying categorical truth and expose any display softness separately.

### 3.4 Angle-in-sign computation

Angle-in-sign conditions classify whether a relocated angle lies in a selected sign. These are categorical geography fields and should not be conflated with planet-in-house regions or aspect-to-angle bands. They can be rendered as their own layer family with separate semantics and color/token treatment.

### 3.5 Aspect-to-angle computation

Aspect-to-angle systems require exact geometry. Centerlines or proximity fields must be computed from validated angular relationships, not fake longitude bands. Aspect overlays answer where a planet has a selected relationship to an angle such as ASC or MC. Aura/material-strip rendering around those lines is a display/intensity layer, not a replacement for exactness.

### 3.6 Latitude and polar policy

High-latitude behavior is a structural policy surface because house systems may become unstable or unintuitive near polar regions. The backend must preserve `apply_lat_cap` or equivalent cap semantics where used, expose cap behavior in validation, and avoid quietly implying truth beyond a product-defined cap. Advanced override can be future policy, not silent default.

---

## 4. GeoJSON, Truth Grid, and Legacy Region Pipeline

### 4.1 Legacy `/search-regions` model

The legacy region search path returns GeoJSON polygon FeatureCollections. It accepts birth/chart inputs and selected conditions, then samples geographic latitude/longitude grids. Current docs distinguish contour-style generation from truth-grid generation.

The contour path used smoothing and contour extraction. It is retained as archaeology where it risks cosmetic topology distortion. The truth-grid mode is the honest legacy substrate: classify grid cells by actual condition truth, refine boundaries where supported, and emit polygons grounded in per-cell classification.

### 4.2 Truth-grid architecture

Truth-grid architecture asks whether each sampled cell satisfies a condition. It then merges cells or creates manageable features. Its value is honesty: seams and topology are handled by sampled truth rather than visual smoothing. It supports planet-in-house overlays and similar categorical fields.

Truth-grid output exists to feed map rendering. It should not become interpretive content. A GeoJSON polygon means “this sampled region satisfies the condition under the engine and resolution,” not “this region is best.”

### 4.3 Boundary refinement

Boundary refinement improves visible edge fidelity by sampling near edges where classification changes. It should be tied to truth evaluation, not decorative smoothing. If refinement is disabled or coarse, output should remain honest about its resolution.

### 4.4 Dateline and seam handling

Dateline seams are a known risk for polygon and map rendering. Truth-grid and screen-space approaches were adopted partly because naive polygon approaches can lie at seams. Backend geometry must preserve world-copy and antimeridian correctness. Any seam repair that corrupts topology is rejected.

### 4.5 GeoJSON output contract

GeoJSON features should represent geometry and metadata required for display and inspection. They should not carry final interpretation. Feature properties may include condition identifiers, layer family, generation mode, resolution, refinement flags, and diagnostic metadata. Labels and display copy remain separate from engine truth where possible.

---

## 5. Canonical Screen-Space Substrate

### 5.1 `/screen-pixel-truth` model

The canonical screen-space substrate evaluates explicit screen-derived points. The frontend maps visible screen samples to coordinates and sends points such as `[[lat, lon], ...]` plus condition definitions. The backend returns dense masks in input order. The frontend paints masks to canvas.

This substrate differs fundamentally from GeoJSON polygons. It is not a smoother polygon path; it is a visible-pixel truth path. Each visible block or pixel is classified by the same coordinate truth used elsewhere.

### 5.2 Mask output

Mask output encodes which selected conditions are true at each sample point. Multi-condition overlap can be represented as bitmasks. The frontend compositing system interprets masks for display. Mask semantics must remain tied to stable condition IDs, not display strings.

### 5.3 Adaptive refinement

Adaptive refinement concentrates additional samples where boundaries, gradients, thin loci, or uncertainty about display classification matter. It should be governed by convergence metrics, sample budgets, and validation thresholds. It must not become unbounded recursion or hidden performance theater.

### 5.4 Screen-space migration boundary

Legacy polygons and canonical masks must not be mixed within a single visible render. Migration requires an adapter layer, explicit substrate flag, per-page-load selection, no auto-fallback, and separate validation gates. Canonical and legacy cache entries cannot be reused across the substrate boundary.

### 5.5 Display honesty

The canonical substrate may show block edges before refinement. That is honest if the block represents current sample precision. Blockiness is preferable to a smooth lie. Visual polish should follow measured convergence, not precede it.

---

## 6. Endpoint and Payload Architecture

### 6.1 Endpoint families

The archive identifies these backend endpoint families as central:

- `/relocated-chart` or equivalent point-inspection endpoint.
- `/search-regions` for legacy GeoJSON region output.
- `/screen-pixel-truth` for canonical screen-space masks.
- `/classify-points` for batch point classification or per-point house data.
- `/brute-force-grid` for validation wall and independent comparisons.
- Aura/raster endpoints retained as archaeology or debug where superseded.
- Future persistence endpoints for chart records, saved searches, favorites, comparisons, and shared views.

Endpoint names in code must be verified against current source before implementation. This manual preserves architectural roles, not a guarantee that every endpoint is active in production.

### 6.2 Render payload doctrine

The Genie/render payload is a canonical snapshot of a search. It contains chart record context, variables, settings snapshot, layer controls, viewport context, and metadata such as created time. The payload snapshot is search truth. Live DOM state after render is not search truth.

### 6.3 Variable schema

Canonical variables are modular. Supported or planned condition types include planet-in-house, angle-in-sign, aspect-to-angle, and later governed transit variants. NOT/exclusion is a polarity on the same condition type, not an unrelated variable family. Mute and solo are display controls, not Layer 1 truth.

### 6.4 Legacy adapter limits

Legacy adapters may map the first few canonical variables into older A/B/C-style payload slots. They must not silently drop overflow. Degradation metadata is required when canonical conditions exceed adapter capacity. Exclude variables should not enter positive condition arrays; they belong in explicit exclusion structures.

### 6.5 Stable IDs versus display labels

Backend truth must rely on stable IDs and structured fields. Display labels, language registry strings, button copy, and beta wording are not engine truth. The payload may snapshot labels for replay/debugging, but the engine should not classify from labels.

### 6.6 Error and debug metadata

Endpoint responses should expose enough metadata to validate sample count, resolution, generation mode, convergence, cap policy, and stop reason where relevant. Debug metadata should remain available to developers but not leak into commercial UX by default.

---

## 7. Cache, Scheduler, and Performance Architecture

### 7.1 Cache key invariants

Cache keys must include every parameter that affects result truth or visible classification: chart identity, chart inputs, bounds or explicit points, zoom, block size/resolution, selected conditions, substrate, latitude-cap policy, settings snapshot, and renderer/generation mode where relevant. A cache key that omits a truth parameter can serve false results.

### 7.2 Cache cannot cross substrates

Legacy GeoJSON cache entries and canonical screen-space mask entries are different objects. They cannot serve each other. Substrate flips must clear or separate cache. Auto-fallback is forbidden because it masks regression.

### 7.3 User-first scheduler

User requests outrank background cache warmups. On pan, zoom, condition edit, chart switch, or rerender, the scheduler should cancel or pause background work and serve the latest user request. Background warmup resumes only when user interaction stops.

### 7.4 Cache validation

Cache behavior must be tested independently from computation. Required validation families include identical-request hits, chart-change invalidation, substrate-flip behavior, interruption storms, budget enforcement, and no half-cached entries after aborted jobs.

### 7.5 Performance guardrails

Performance optimizations cannot compromise truth. Establish brute-force or high-confidence truth first, then back off. Adaptive sampling should be measured against wall or reference outputs. If sample budget is hit, the response should report it rather than pretending full convergence.

---

## 8. Database, Storage, and Persistence Architecture

### 8.1 Active local object model

Core product objects include user/account, professional workspace, client, birth chart or chart record, relocation search session, favorite/saved location, saved exploration/search, comparison set, notes, shared view, and settings. These objects should not collapse into a single mutable map-state blob.

### 8.2 Chart record ownership

Chart record context owns saved explorations, favorites, comparisons, history, settings snapshots, and notes. The active map must know which chart record it represents. Context switch must not silently mutate existing saved objects.

### 8.3 Saved search semantics

A saved search stores semantic conditions and render snapshot context, not arbitrary renderer internals. It should include chart identity, variables, polarity, settings snapshot, viewport, created time, and enough replay data to restore the investigation honestly.

### 8.4 Favorite location semantics

Favorite locations may be named cities or arbitrary coordinates. They belong to a chart context and should open a relocated chart or comparison view. Notes can attach to favorites, but favorites should not imply ranking by default.

### 8.5 Comparison semantics

Comparison objects store selected locations/charts and factual relocation data for side-by-side evaluation. They should not automatically declare a winner. Optional future AI summaries remain downstream and labeled.

### 8.6 Supabase future path

Supabase integration is planned future infrastructure, not active local truth unless current source verifies it. The migration should be explicit: schema design, row ownership, access policies, chart/client ACLs, saved-object replay, settings snapshot versioning, and migration tooling. Do not let local JSON become permanent product storage by accident.

---

## 9. Frontend/Backend Contract Boundaries

### 9.1 Map is consumer of truth

The frontend renders backend truth and provides interaction. It should not invent membership. It may adapt display for Leaflet, Canvas, panes, zoom, and labels. It may not change chart condition truth.

### 9.2 Popup agreement

The frontend must allow point inspection that calls or reflects backend point truth. Overlay and popup disagreement is a blocker unless explained by explicit resolution/provisional status.

### 9.3 Layer controls

Mute, solo, background, foreground, and visual opacity controls affect display only. They should not mutate backend search conditions unless explicitly converted into semantic variables and re-rendered.

### 9.4 Dirty state

If the user changes variable cards after rendering, the UI must distinguish edited live state from rendered snapshot truth. Save Search attaches to rendered payload, not the current incomplete editor.

---

## 10. Validation and Rollback Architecture

### 10.1 Smoke gates

Backend changes require focused smoke gates. Region search, screen-pixel truth, cache behavior, popup parity, substrate migration, brute-force wall, and chart-change invalidation should each have independent tests.

### 10.2 Brute-force wall

The brute-force wall is the independent reference. It may sample densely or slowly, but it defines truth targets. Production renderers should be compared against it through XOR or suitable parity metrics where possible.

### 10.3 Popup-overlay parity

Sampled overlay classifications must agree with analytical point truth from relocated chart calculations. Any canonical failure blocks migration or release.

### 10.4 Rollback

Architecture changes require rollback paths: URL flags for substrate, default constants, git revert, no persistent cache dependencies, and no hidden migrations. A migration step that cannot roll back in one commit or documented procedure is too broad.

### 10.5 Archaeology marking

Superseded endpoints, documents, and renderer paths should remain labeled as archaeology if retained. Future developers must see why a path was rejected and what replaced it.

---

## 11. Active Engineering Non-Goals

Active backend architecture does not include automatic interpretation, city scoring, production AI advice, hidden ranking, full Supabase migration without schema/ACL plan, persistent browser cache, CDN chart tiles, Web3 storage, multi-substrate plugin frameworks, telemetry dashboards, feature-flag services, broad renderer rewrites for aesthetics, or aura/rain/virga productionization before truth substrate and validation are stable.

---

## 12. Engineering Checklist

Before accepting backend work, verify:

1. Does it preserve Reveal structure / Preserve judgment?
2. Does it avoid interpretation in core engine schemas?
3. Does it keep cities secondary to coordinate truth?
4. Does it preserve point truth and popup authority?
5. Does it use stable IDs, not labels, for engine semantics?
6. Does it include all truth parameters in cache keys?
7. Does it avoid mixing legacy GeoJSON and canonical masks in one render?
8. Does it define validation and rollback?
9. Does it distinguish active implementation from roadmap?
10. Does it avoid silent adapter overflow?
11. Does it preserve chart-record ownership?
12. Does it save semantic searches, not renderer accidents?
13. Does it keep debug metadata out of commercial UX?
14. Does it preserve archaeology labels?
15. Does it state unknowns and unverified status plainly?

---

## Future Architectural Excellence Inventory

This inventory tracks upcoming infrastructure updates without making them active implementation law.

### Supabase and persistence

- Supabase schema for users, professional workspaces, clients, chart records, saved locations, saved searches, comparison sets, notes, shared views, and settings snapshots.
- Row-level security and access-control design.
- Migration path from local JSON/library files.
- Replay-safe saved investigation schema.
- Shared-view permission model and client-safe projections.
- Audit/provenance fields for AI-generated content and exported views.

### Backend endpoints

- Production persistence endpoints for chart CRUD.
- Saved search CRUD with immutable render snapshots.
- Favorite location CRUD.
- Comparison creation and retrieval.
- Shared-view export endpoints.
- Settings snapshot version endpoints.
- Future AI assist endpoints clearly separated from factual engine endpoints.

### Cache and performance

- Phase-C production cache integration after substrate migration.
- Cache drainage, storm, chart-change, and substrate flip smokes.
- Future persistent cache only after privacy/invalidation contracts.
- Adaptive sampling thresholds by viewport and condition density.
- Server-side cache only if measured local/browser cache is insufficient.

### Rendering substrate

- Canonical screen-space substrate default after validation.
- Aspect overlay migration to canonical substrate.
- Aura/material-strip implementation from validated exactness fields.
- Cusp-gradient display prototype with separate semantics.
- Unified sampler strategy across house, angle-sign, aspect, and aura families.

### Validation infrastructure

- Golden screenshot CI.
- Popup-overlay parity harness.
- Brute-force wall fixture registry.
- Dateline, polar, dense-city, high-latitude, and cusp-heavy edge suites.
- Automated doctrine-drift and archaeology-banner checks.

### Operational infrastructure

- Structured migration templates.
- Endpoint contract index.
- Cache-key invariant checker.
- Audit JSON generation for canon documents.
- Source-to-output documentation verification tooling.
- AI-assisted review scripts constrained by governance.



---

## Appendix A — Backend Source Index

### A.1 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/AI_WORKFLOW_GOVERNANCE.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 14272; SHA-12: `570f3cca823a`; score: 94
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Engineering signals:
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in writing.
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisible engineering intent: infrastructure, …
  - Every phase closeout must ask whether it introduced or exposed:
  - * missing test, CI, regression, or rollback discipline;
  - * cache invalidation, synchronization, or migration risk;

### A.2 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/CURRENT_RENDERING_DOCTRINE.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 7576; SHA-12: `0b4a58929157`; score: 84
- Key headings: Current Rendering Doctrine — Summary; The stack (top to bottom); Non-negotiables; Legacy `/search-regions` Truth Grid; Phase-2 cache (product substrate); Evidence bundle (read in this order); Documents marked SUPERSEDED (archaeology preserved); Warnings against backsliding; Remaining gaps (structural, not aesthetic); Recommendation
- Engineering signals:
  - > **Status:** Canonical orientation page (fast to read).
  - | **Brute force** | Validation wall. Every optimisation must match it cell-for-cell (or pixel-for-pixel on screen). | Canonical control specimen |
  - | **Screen-space truth** | Production sampling axis for **visible overlays**. Classify what the user actually sees. | Canonical for rendering |
  - | **Adaptive refinement** | Production rendering substrate. Sparse → dense only where occupancy disagrees. | In use (`edge2_thin2_highlat2_probes` policy) |
  - | **Targeted escalation** | Extra halo / probes / lat-cap boundary rules **only** at known instability classes. | In use — not global |

### A.3 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DEFERRED_EXCELLENCE_REGISTRY.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 30563; SHA-12: `8fdc70fc996d`; score: 158
- Key headings: Deferred Excellence Registry; Purpose; Cross-Cutting Doctrine; Status Legend; 1. Renderer / Topology Improvements; 1.1 Stable component IDs across zoom/pan; 1.2 Graph / global path solver; 1.3 Canonical-default migration; 1.4 Continuous topology extraction refinement; 1.5 Subpixel/edge extraction refinement for narrow-orb ASC; 1.6 Seam-aware topology continuity; 1.7 Signed-distance-field experiments
- Engineering signals:
  - This registry captures everything we know we *could* improve in the renderer, architecture, UX, product, and reliability stack — and have intentionally deferred to protect MVP velocity. Its primary purpose is **not** to accumulate shiny feature ideas. Features are comparatively easy to remember beca…
  - The primary purpose is preserving hidden robustness and institutional memory: invisible infrastructure improvements, architecture refinements, reliability upgrades, governance ideas, performance optimizations, renderer trust improvements, scaling concerns, cache/system improvements, synchronization …
  - These are the things founders and AI systems tend to forget because users do not directly see them, they do not demo well, short-term success can mask their absence, and commercial pressure naturally favors visible product work. The registry exists to preserve long-term engineering intent and produc…
  - Short rule: when choosing what to capture here, prefer invisible engineering and infrastructure concerns over visible feature wishes. Feature wishes may be listed when they carry trust, platform, or operational consequences, but the registry's center of gravity is hidden robustness.
  - 1. **Anti-death-spiral doctrine (from Phase 1.19):** Do not continue math/rendering work unless it removes a named production blocker or protects future product trust. Items in this registry are evidence of restraint, not a to-do list.

### A.4 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DOCTRINE_INDEX.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 67
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Engineering signals:
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Older doctrine and archaeology:** Older docs listed below remain valuable context, evidence, and active companions where not superseded. Treat them as secondary to `docs/constitutional/` on layer sovereignty, forbidden crossings, epistemic humility, runtime/renderer sovereignty, and implementation…
  - **Pacing reminder:** **Philosophy and epistemology evolve slowly** (explicit revision). **Implementation details evolve quickly** (iterate with evidence), but **must not contradict** slow doctrine without updating the doctrine file.
  - These files govern **meaning, agency, fate, tradeoffs, tone, and long-form institutional character**. They are **foundational**. Typical change rate: **rare**; edits should be deliberate, often after architect or governance review.

### A.5 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/EXECUTIVE_TRANSFER_BRIEF_NEXT_CHAT.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9792; SHA-12: `d91200d72161`; score: 56
- Key headings: Executive Transfer Brief For Next Chat; 1. Current Project State; 2. What Is Considered Solved; 3. What Is Intentionally Deferred; 4. Current Renderer Status; 4.1 Renderer handoff state; 5. Governance Status; 6. Productization Status; 7. Immediate Next Recommended Phases; 8. Strategic Warnings; 9. Key Philosophical Doctrines; 10. How Future AI Should Behave
- Engineering signals:
  - The project has moved from renderer research into product platform construction. The relocation map now has enough validated rendering confidence to support Phase 2 product work: chart library, saved views, handoff links, deep links, onboarding, future accounts, and professional sharing.
  - The current product direction is focused: relocation astrology, map-based discovery, chart persistence, professional workflows, high-trust UX, and contemplative visual exploration. It is not a generic astrology suite or social/spiritual platform.
  - - Legacy production renderer is MVP-ready.
  - - Brute-force wall validation exists as the reference method.
  - - ASC/seam/high-latitude concerns are understood well enough to stop panic loops.

### A.6 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_1_2_EXTRACTION_AUDIT.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 31222; SHA-12: `99e7cbcf42db`; score: 478
- Key headings: Phase 1.2 Extraction Audit; Concise Findings; Files Inspected; Production and backend; Sandboxes; Validation / capture scripts; Doctrine used as constraints; Current Rendering Entry Points; Production renderer; Backend endpoints; Sandbox renderers; Validation harnesses and capture scripts
- Engineering signals:
  - > `docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md`,
  - > `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`, and
  - > **Non-goals:** No production renderer mutation. No cache rewrite. No
  - > astrology math change. No speculative optimization.
  - safe extraction boundaries, and rollback checkpoints before Phase 1.2

### A.7 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 58355; SHA-12: `c6ef18d0c316`; score: 617
- Key headings: Phase-2 Cache Integration — Architecture & Implementation Planning; 0. Where this fits; 1. Grounding — what is true today, measured; 1.1 Sandbox state (measured, not asserted); 1.2 What this means; 1.3 Hard architectural finding — substrate mismatch; 2. Production Scheduler Architecture; 2.1 Single-active-job model; 2.2 Foreground vs background queues; 2.3 Cancellation / interruption behaviour; 2.4 Priority escalation rules; 2.5 Viewport ownership
- Engineering signals:
  - # Phase-2 Cache Integration — Architecture & Implementation Planning
  - > **Authority:** `docs/relocation_map_architecture.md` (§ "Phase 2 cache
  - > **Companion:** `validation/narratives/phase2_cache_implementation.md`
  - > **Stability:** Slow. Implementation details may rev; design rules here
  - cache orchestrator that preserves correctness, user responsiveness,

### A.8 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_IMPLEMENTATION_PROTOCOL.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 54962; SHA-12: `c32fcebbd584`; score: 430
- Key headings: Phase-C Implementation Protocol; Operational constitution for landing the validated architecture without future chaos; 0. Where this fits; 1. Implementation Phase Breakdown; Phase 1.1 — Documentation alignment (no code); Phase 1.2 — Archaeology fencing (low-risk cleanup); Phase 1.3 — Scheduler extraction (no behaviour change); Phase 1.4 — Substrate adapter scaffold (legacy-only); Phase 1.5 — Canonical substrate wiring (flag-gated); Phase 1.6 — Scheduler/cache wiring on canonical (flag-gated); Phase 1.7 — Parity validation harnesses; Phase 1.8 — Default flip + stabilisation
- Engineering signals:
  - > then `docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md` (substrate swap),
  - > then `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` (cache shape),
  - > endpoints. Astrology-math changes. Validated-adaptive-refinement
  - with — never duplicates — the existing meta-governance docs. Where
  - those already legislate, this defers; where they are silent on

### A.9 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_PRODUCTION_MIGRATION_PLAN.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 64644; SHA-12: `af96b1d10c2e`; score: 757
- Key headings: Phase-C Production Migration Plan; Legacy overlay pipeline → canonical screen-space adaptive substrate; 0. Where this fits; 1. Legacy vs Canonical Substrate Audit; 1.1 The legacy overlay pipeline (what is in production today); 1.2 The canonical screen-space substrate (validated, sandbox-proven); 1.3 Semantic differences; 1.4 Rendering differences (visible); 1.5 Cache compatibility implications; 1.6 Validation differences; 1.7 Hidden assumptions; 1.8 Likely regression risks (ranked)
- Engineering signals:
  - # Phase-C Production Migration Plan
  - ## Legacy overlay pipeline → canonical screen-space adaptive substrate
  - > **Status:** Migration architecture and planning doctrine. Design
  - > then `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`.
  - > **Companion:** `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`

### A.10 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_RENDERING_ARCHITECTURE.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 47288; SHA-12: `3744bf667647`; score: 289
- Key headings: Phase C — Rendering Substrate Architecture (Governing Laws); 0. Where this document sits; 1. Canonical Rendering Truths; 1.1 The four absolute statements; 1.2 Screen-space truth doctrine; 1.3 Adaptive refinement as production substrate; 1.4 Why visible output is canonical; 1.5 Globe truth vs screen truth; 2. Convergence Strategy; 2.1 Convergence is the contract; sample count is not; 2.2 Targeted escalation, never global slowdown; 2.3 Refinement economy — *truth where unstable*
- Engineering signals:
  - > thinking, cache-over-user-responsiveness, or erasure of archaeology.
  - | Experience tone | `docs/ux_principles_and_emotional_tone.md`, `docs/brand_and_experience_foundations.md` | How the product *feels* |
  - renderer computes, classifies, refines, caches, and exposes truth. It does
  - ## 1. Canonical Rendering Truths
  - renderer never invents geometry. It classifies reality, reveals the

### A.11 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PROJECT_CONTINUITY_INDEX.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 2667; SHA-12: `303dae8aa89c`; score: 14
- Key headings: Project Continuity Index; Canonical Governance Docs; Canonical Archaeology Docs; Canonical Renderer Doctrine Docs; Deferred Excellence; Validation Narratives; Continuity Volume Convention; Recommended Future-AI Ingestion Order
- Engineering signals:
  - Purpose: short entry point for future AI/human rehydration. This file points to canonical governance, archaeology, renderer, deferred-excellence, and validation memory without replacing those sources.
  - ## Canonical Governance Docs
  - - `validation/narratives/renderer_readiness_decision_gate.md` — Phase 1.19 blocker taxonomy and anti-death-spiral doctrine.
  - ## Canonical Archaeology Docs
  - - `ai_context/archaeology/RAW_CONTINUITY_VOLUME_7.md` — canonical continuity volume container for this phase.

### A.12 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 75
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Engineering signals:
  - **CANONICAL** for **future** AI-assisted interpretation layers — not current product scope.
  - This doctrine governs **language, posture, and review** — not model choice, prompt templates, or UI implementation.
  - Relocation decisions touch housing, career, relationships, health, and identity. Users arrive with hope, anxiety, and real constraints. An interpretive layer that **declares outcomes** or **names perfect places** does three harms:
  - 1. **Epistemic harm** — astrology describes **archetypal structure**, not literal life scripts. Conflating pattern with destiny is false precision.
  - 2. **Agency harm** — the user’s values, budget, visa status, family, and timing determine meaning. The app must **support judgment**, not replace it.

### A.13 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai_constitution_and_review_architecture.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 13119; SHA-12: `d6ae8f16c65e`; score: 46
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Engineering signals:
  - - **`docs/review_contracts_and_governance.md`** — lightweight **implementation review** prompts (AI behavior, UX, symbolic integrity, contemplative space); complements this file’s Layer 2 duties.
  - - **`docs/DOCTRINE_INDEX.md`** — canonical map of doctrine docs, stability, and reading order.
  - | **Preserve symbolic integrity** | Outputs must stay **accountable** to chart structure—not **rewritten** for likability. |
  - | **Prevent emotional manipulation and dependency** | No **oracle intimacy**, **certainty addiction**, or **replacing** the user’s judgment with model cheerleading. |
  - | **Flattery** | User feels **clever, chosen, spiritually advanced** regardless of chart cost. |

### A.14 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/client_chart_data_model_v1_2026-05-29.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 35789; SHA-12: `795365723409`; score: 186
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Engineering signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/supabase_schema_sandbo…
  - - what durable records exist,
  - - what belongs on each record,
  - - what must never be persisted as product truth,

### A.15 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 20953; SHA-12: `db53e1e91227`; score: 86
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Engineering signals:
  - **Scope:** Web 2.0 account/chart workflow architecture. Not implementation. Not schema migration.
  - **Purpose:** Stress-test and **propose** a coherent navigation tree, map entry/return paths, screen payloads, active-context rules, and future boxes — ready for canonical adoption after human review.
  - Web 2.0 is a **Chart Record–centric** non-AI product. **Map and Chart Page are co-primary surfaces.** Chart Record utility route, favorites, saved explorations, and comparison are **supporting surfaces** — not a SaaS dashboard home.
  - **Primary ownership unit:** Chart Record (user-facing client / chart / research row).
  - **One user-facing chart per Chart Record.** Event and research charts are **separate Chart Records**, not nested lists.

### A.16 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/aspect_aura_defaults.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, frontend_backend_contract, future_infrastructure
- Characters: 1291; SHA-12: `2e467a76fee6`; score: 22
- Key headings: Aspect aura defaults (approximate display); Authority; Default screen weights (Leaflet `weight`, approximate); NOT done here
- Engineering signals:
  - - **Popup** / API chart: exact longitudes and derived angles.
  - - **Centerline** GeoJSON from `/search-regions`: exact aspect-to-angle spine.
  - - **Aura**: widened, low-opacity stroke **under** the centerline; **screen-pixel weight** scales by selected aspect **preset** only.
  - **Exact lines** still use API `weight` / `opacity` (MC ~4×95% opacity; contour angles ~2×100% in current defaults).
  - - No latitude-aware geographic σ for aura width (future refinement).

### A.17 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/brand_and_experience_foundations.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 34
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Engineering signals:
  - **What this is not:** A brand book, logo spec, marketing narrative, campaign, or visual identity system. **No** speculative public branding.
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).
  - - **Warm, safe containment:** The environment should feel like a **warm blanket** or **safe, contemplative room**—**breathable, calm, trustworthy, spacious, emotionally safe**—so users can **inhabit** it comfortably for **hours**.
  - - **Long sessions without fatigue:** Typography, color restraint, spacing, and low noise support **sustained** exploratory use; the product should feel like a **home** for serious play, not a sprint through a flashy demo.
  - - **Instrument, not dashboard:** A core principle—see below; the tool **serves** the user’s inner work, it does not **perform** for them.

### A.18 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/cartographic_language_and_city_rendering.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 18608; SHA-12: `33b4db97eb55`; score: 58
- Key headings: Cartographic language and city rendering; 0. Basemap or tile strategy change ⇒ full visual identity re-test; 1. Map label language vs app language; 2. Provider evaluation (map + search); 2.1 Dimensions to score (required for any serious comparison); 2.2 Qualitative stack comparison (high level); 2.3 “Extra hour” vs “multi-day / multi-week”; 2.4 Effort bands for “whole solution” slices; 2.5 GeoNames bridge first vs “long-term now”; 3. City visibility under overlays (hard constraint); 4. City density and ranking (rendering); 5. Clickability: city vs blank map
- Engineering signals:
  - **Out of scope:** Aspect-to-angle **glow/aura** (not implemented; do not conflate with city-layer work).
  - **Institutional rule:** If the team changes **map provider**, **tile format** (raster → vector, host swap, style swap), or **label policy**, we must **re-validate the whole visual system**—not assume the current look “carries over.”
  - | **Light / dark theme** | **Do not** assume one overlay palette works; plan **paired tokens** when dark mode is real. |
  - **Doctrine:** **Do not assume the current palette survives a map-provider change.** Promote tuned values only after **documented** QA pass (screenshots, overlap cases, polar/dateline, international sample).
  - - **Implication:** Future **tile/provider strategy** should evaluate **vector tiles** or hosts with **explicit language parameters** (Mapbox, MapTiler, Google Maps Platform, CARTO, Stadia/Stamen-style stacks, self-hosted OSM vector pipelines—not prescribing a single vendor here).

### A.19 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/README.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 6
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Engineering signals:
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - The system is a layered symbolic intelligence platform, not a monolithic astrology AI, recommendation engine, or chatbot with symbolic flavor.
  - ## Canonical
  - ## Semi-Canonical
  - These documents contain canonical principles plus exploratory or future-facing implementation detail. Treat their core boundaries as binding and their implementation models as revisable.

### A.20 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ai_conversational_modes.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 2887; SHA-12: `b796e2065486`; score: 6
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Engineering signals:
  - - canonical architectural principles,
  - - and guide long-term extensibility.
  - # Core Principle
  - The AI should adapt conversational style without violating constitutional doctrine.
  - It must not fabricate comfort.

### A.21 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/constitutional_ingestion_checklist.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 14
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Engineering signals:
  - Update this document whenever:
  - # Canonical Constitutional Docs
  - # Semi-Canonical / Strategic Docs
  - * and architecture may require rollback.
  - * and long-term symbolic integrity.

### A.22 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/conversational_discovery_and_intentionality.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, frontend_backend_contract, future_infrastructure
- Characters: 4218; SHA-12: `c7b5d8b9fc8e`; score: 14
- Key headings: Conversational Discovery And Intentionality; Status; Purpose; Core Principle; User intentionality is sovereign.; Intentionality Discovery; Examples; Archetypal Exploration; Example Exploratory Style; Intentionality Strength; Examples; Layer Relationship
- Engineering signals:
  - This document is PARTIALLY CANONICAL.
  - The principles of:
  - are canonical.
  - This document defines how the platform should:
  - - manipulative,

### A.23 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/epistemic_integrity_and_symbolic_humility.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract
- Characters: 3739; SHA-12: `242cc62cfae5`; score: 7
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior; Good Behavior; Collaborative Discovery
- Engineering signals:
  - This document is CANONICAL.
  - All AI and interpretive systems must follow these principles.
  - This document establishes the philosophical and operational rules governing:
  - The system must prefer:
  - # Core Principle

### A.24 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/future_excellence_vs_future_feature_excellence.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 17
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Engineering signals:
  - - canonical architectural principles,
  - # Core Principle
  - ## Infrastructure excellence and feature excellence must remain distinct.
  - - rollback safety,
  - - rollback discipline,

### A.25 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/implementation_governance_and_ai_workflow_protocol.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3988; SHA-12: `b127e5c52050`; score: 26
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Engineering signals:
  - This document is CANONICAL.
  - - rollback protocol,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - - speculative patch spirals,

### A.26 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer4_optimization_and_exploration_doctrine.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 4341; SHA-12: `289b4552320f`; score: 12
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Engineering signals:
  - - canonical Layer 4 principles,
  - Core Layer 4 boundaries are canonical.
  - - user-intent violations,
  - # Core Principle
  - - reducing chronic 12th-house isolation,

### A.27 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer_sovereignty_and_forbidden_crossings.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract, future_infrastructure
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 13
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Engineering signals:
  - This document is CANONICAL.
  - These rules are mandatory architectural constraints.
  - # Core Principle
  - # Constitutional Rule
  - but may NEVER rewrite lower-layer truth.

### A.28 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layered_symbolic_intelligence_architecture.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract, future_infrastructure
- Characters: 4801; SHA-12: `5242de0598f3`; score: 24
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Engineering signals:
  - This document is CANONICAL.
  - It defines the constitutional layer architecture of the platform.
  - All future systems must respect:
  - This document defines the core architectural philosophy of the platform.
  - The platform is intentionally divided into distinct symbolic intelligence layers.

### A.29 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/map_first_product_doctrine_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 28
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Engineering signals:
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - - an account management platform
  - - a client record system with a map attached

### A.30 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/mvp_beta_and_future_feature_roadmap.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, cache_scheduler_performance, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 4767; SHA-12: `c904d8af5d1e`; score: 17
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes; Stage 2 — Professional Beta; Goal
- Engineering signals:
  - This document defines the broad strategic build sequence for the platform.
  - # Core Principle
  - - and long-term slowdown.
  - The platform is expected to evolve in several major stages.
  - - cache/runtime discipline,

### A.31 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract, future_infrastructure
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 18
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Engineering signals:
  - - canonical architectural principles,
  - - and guide long-term extensibility.
  - This document defines how multiple astrological systems may coexist within the platform.
  - The platform is constitutionally designed to support:
  - # Core Principle

### A.32 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_mode_vs_lay_mode_strategy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 3492; SHA-12: `c166907d611f`; score: 5
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Engineering signals:
  - Core principles are canonical.
  - # Core Principle
  - ## The platform should remain professionally trustworthy while still accessible to non-professionals.
  - The system must avoid:
  - - do not know astrological terminology,

### A.33 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_trust_and_ai_behavior_doctrine.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, frontend_backend_contract, future_infrastructure
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 10
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Engineering signals:
  - This document defines how AI systems inside the platform must behave.
  - The AI must never behave like:
  - - a manipulative mystic,
  - # Core Principle
  - This principle is absolute.

### A.34 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/purification_audit_framework.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3639; SHA-12: `a43528565790`; score: 18
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Engineering signals:
  - This document is CANONICAL.
  - - and rollback discipline.
  - As the platform evolves,
  - - accumulate hidden assumptions,
  - - or violate constitutional doctrine.

### A.35 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/relocation_strategy_framework.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, frontend_backend_contract, future_infrastructure
- Characters: 2978; SHA-12: `5542c6b3c8b9`; score: 11
- Key headings: Relocation Strategy Framework; Status; Purpose; Core Principle; Subtractive relocation comes before additive optimization.; Subtractive Relocation; Additive Relocation; Strong Relocations Often Do Both; Tradeoff Reality; Archetypes Are Contextual; Optimization Delusion; Layer 4 Behavior
- Engineering signals:
  - - canonical architectural principles,
  - - and guide long-term extensibility.
  - This document defines the broad relocation strategy philosophy of the platform.
  - - escaping negatives,
  - It is the strategic reshaping of symbolic atmosphere.

### A.36 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_and_renderer_sovereignty.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3826; SHA-12: `edda50b52a22`; score: 18
- Key headings: Runtime And Renderer Sovereignty; Purpose; Core Principle; Rendering must never alter truth.; Runtime Sovereignty; Renderer Sovereignty; Hydration Boundaries; Sandbox Boundaries; Observer Limitations; Renderer Substrate Integrity; Progressive Refinement; Ambiguity And Implication
- Engineering signals:
  - - rollbackability,
  - # Core Principle
  - ## Rendering must never alter truth.
  - They do not compute symbolic reality.
  - - cache behavior,

### A.37 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_build_sequence_and_timeline.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 4934; SHA-12: `12aea4343437`; score: 20
- Key headings: Runtime Build Sequence And Timeline; Status; Maintenance Notes; Purpose; Core Principle; Build irreversible foundations first.; Phase Family 1 — Truth And Runtime Foundation; Goal; Includes; Status; Phase Family 2 — Renderer Reintegration; Goal
- Engineering signals:
  - - and preserve constitutional architecture during rapid iteration.
  - # Core Principle
  - - cache discipline,
  - - renderer isolation,
  - - and rollback safety.

### A.38 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/symbolic_language_style_guide.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, future_infrastructure
- Characters: 1703; SHA-12: `11e6dd9bdb1a`; score: 6
- Key headings: Symbolic Language Style Guide; Purpose; Core Principle; Preferred Style; Avoid; Good Examples; Bad Examples; Archetypal Precision; Symbolic Humility; Constitutional Goal
- Engineering signals:
  - This document defines how symbolic language should be expressed by the platform.
  - # Core Principle
  - - mystical for performance,
  - - manipulative certainty,
  - - "This pattern often relates to..."

### A.39 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract
- Characters: 3360; SHA-12: `554add110fa4`; score: 19
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Engineering signals:
  - This document defines one of the most important distinctions in the platform:
  - Truth belongs primarily to Layer 1.
  - Astrological fact belongs primarily to Layer 2.
  - Interpretation belongs primarily to Layer 3.
  - - coordinate geometry,

### A.40 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_app_shell_handoff_audit_v1_2026-05-30.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 16528; SHA-12: `a7754235e25c`; score: 163
- Key headings: Genie → App Shell Handoff Audit v1; Status; Executive summary; A. Current Genie contract; Emitter; Trigger; Payload shape (as implemented); Variable semantics (canonical); Output destinations today; Not emitted / not connected; B. Current app shell contract; Navigation context (in-app)
- Engineering signals:
  - **Scope:** What Genie emits today, what app shell and map expect today, and what adapter/transport is required to connect them.
  - - `docs/contracts/genie_render_payload_v1_2026-05-30.md`
  - - `scripts/smoke_app_shell_map_handoff.py`
  - Genie (sandbox) **emits a full `genie_render` payload in memory** on Search Map. App shell **transports navigation context only** via Map Handoff Contract v1 URL params.
  - **Three distinct states (do not conflate):**

### A.41 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_render_payload_v1_2026-05-30.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 27674; SHA-12: `7e997018eed9`; score: 269
- Key headings: Genie Render Payload Contract v1; Status; Purpose; Architectural doctrine; Language stability doctrine; Principles; Therefore; Top-level payload; Field notes; Render immutability; Future references (not defined here); Variable object
- Engineering signals:
  - # Genie Render Payload Contract v1
  - **CANONICAL** for the payload emitted when the Genie user presses **Search Map** (render / search submit).
  - **Scope:** Documentation / contract only. Defines shape, semantics, legacy adapter rules, and examples. Not implementation.
  - - `scripts/smoke_genie_sandbox.py` — behavioral smoke for sandbox payload hooks
  - - `map_CURRENT.html` — `collectSavedInvestigationConditions()` legacy map collector

### A.42 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/variable_card_language_v1_2026-05-30.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 15184; SHA-12: `bde701502163`; score: 113
- Key headings: Variable Card Language Contract v1; Status; Purpose; Core doctrine; Canonical internal type IDs; Language registry concept; Composition rule; Registry ownership; Snapshot rule (Saved Explorations); Beta display label candidates; `planet_in_house`; `angle_in_sign`
- Engineering signals:
  - **CANONICAL** for Genie variable-card **user-facing language** — labels, shorthand, dropdown copy, and presentation tokens.
  - - `docs/contracts/genie_render_payload_v1_2026-05-30.md` — stable type ids, `variables[].label` snapshots, language stability doctrine
  - - Copy can evolve without breaking **payload type ids**, **registry ids**, or **renderer logic**
  - - Beta can ship with **boring, obvious** wording while leaving room for visual polish later
  - This document governs **presentation language only**. It does **not** define search semantics, engine contracts, or persistence schema (see Genie Render Payload Contract v1).

### A.43 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/current_sidebar_ux_audit.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 4992; SHA-12: `c07666b5828f`; score: 33
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces; 9. Condition model — **next structural UX step (documented)**; 10. Location search placement (documented)
- Engineering signals:
  - **Intent:** Describe friction, record implemented fixes, and flag **documented-only** next steps (no redesign commitment).
  - - **Aspect overlay:** less neon fallback teal; unchanged API/staging logic.
  - - **Chart popup:** ASC/MC show **one formatted line each** from API `asc` / `mc` (`format_zodiac` strings); duplicate sign-only lines removed; planet table **bold headers**, normal planet names, **centered** house column.
  - - Fixed panel still trades width vs map; **reset control** mitigates **lost world** after heavy panning.
  - - Popups use **`.popup-chart`** patterns; **angle-sign** no longer reads as striped/strobed at some zooms (stroke removed).

### A.44 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/local_first_data_objects_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 8758; SHA-12: `90256838acac`; score: 76
- Key headings: Local-First Data Objects v1; Status; Purpose; Architectural boundary; Entity glossary; ProfessionalAccount; Client; BirthProfile; RelocatedChart (future durable object); Place; FavoriteCity; OverlayCondition
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **product-layer entities**, **persistence boundaries**, and **local-first scaffold rules**. Not a database schema. Not implementation.
  - - cache keys tied to graphics instead of semantics,
  - - Layer 2 settings silently rewriting Layer 1 records.
  - │  PRODUCT RECORDS (local-first → future sync)            │

### A.45 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/local_product_store_v2.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 2604; SHA-12: `0fee91b48aed`; score: 34
- Key headings: Local Product Store v2; Status; Purpose; File location; Python module; Validation rules; Scripts; Explicit non-goals (Phase 3.0a); Rollback; Revision
- Engineering signals:
  - Parallel to `library/library.json`. Not connected to map, HTTP, Supabase, or UI.
  - **Reads with:** `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/supabase_schema_sandbox_plan_v1.md`.
  - - saved investigations / searches with `settings_snapshot`,
  - scaffold/local_product/TEMPORARY_product_store.json   # committed empty template
  - Runtime smokes write to **temp paths** only. Do not promote this file to product storage without explicit migration approval.

### A.46 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/supabase_schema_sandbox_plan_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 16155; SHA-12: `8fac31540a5b`; score: 115
- Key headings: Supabase Schema Sandbox Plan v1; Status; Explicit non-goals (current phase); Architectural boundary; 1. Proposed table list; 2. Columns per table; `professional_accounts`; `clients`; `birth_profiles`; `places`; `saved_charts`; `saved_investigations`
- Engineering signals:
  - # Supabase Schema Sandbox Plan v1
  - **PLANNING ONLY — SCHEMA SANDBOX**
  - This document defines a **local-first schema plan** that can later mirror to Supabase. It is **not** implementation, **not** a runtime dependency, and **not** authorized to replace existing scaffolds.
  - **Reads with:** `docs/data_model/local_first_data_objects_v1.md`, `docs/future/birth_time_uncertainty_and_confidence_doctrine.md`, `validation/narratives/phase2_3_saved_investigation_replay.md`, `library/library.json` (legacy scaffold).
  - - integrate auth or Supabase client packages,

### A.47 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/design/brand_visual_language_and_design_doctrine.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 29
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - - contemplative symbolic geographic instrument,
  - | **Category** | Relocation astrology exploration — not generic astrocartography clone |
  - | **Emotion** | Contemplative long-session comfort |

### A.48 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 34
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **epistemic tiers**, **user-facing honesty**, **data recording**, and **engine behavior boundaries** for uncertain birth times. Not implementation. Not rectification software spec.
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `validation/narratives/post_truth_grid_sta…
  - - houses and angles move rapidly with time,
  - - AI intake may help later — **MVP must handle tiers without AI**.

### A.49 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/layer5_experiential_education_through_travel_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 17
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Engineering signals:
  - **Dependency:** Requires mature AI guidance, relocation exploration substrate, and user observation capture — **after** standalone Web 2.0 facts-first product is proven.
  - **Must not be read as:** screen spec, sprint backlog, course marketplace brief, or Layer 1–3 implementation requirement.
  - The platform already supports **facts at locations** (Layer 1) and will eventually support **interpretive assistance** (AI layers). Layer 5 education sits **above** those — it organizes **experience over time** into curricula that reward observation, travel, and personal comparison.
  - | Notice what changed when you relocated or slowed down | Memorize rules without location context |
  - Reading may support the journey — glossaries, brief context, safety notes — but **reading is never the main pedagogical engine**. The main engine is **lived geographic comparison** grounded in the same factual substrate the professional instrument provides.

### A.50 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_and_city_identity_strategy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 42
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Engineering signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - **Related:** `memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `docs/geocoder_dataset_feasibility.md`, `docs/cartographic_language_and_city_rendering.md` (basemap change ⇒ **§0** full visual re-test), `docs/relocation_app_product_roadmap.md` §7–8, `docs/map_and_overlay_desig…
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`). The map binds **human geography** to …
  - Current prototype list search (`cities.js`) is a **stand-in** only: **name, lat/lng, population (and minimal fields)**—**no reliable country/admin**, **no alternate names**, **no stable place IDs**, and **no** trustworthy global ranking (e.g. Paris, France vs Paris, Texas; London vs Londonderry). **…
  - - **Exact-coordinate entry** (lat/lon or paste) is required for parity with **right-click truth** and for places not in any city list.

### A.51 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_dataset_feasibility.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 16429; SHA-12: `6ba544bcfafd`; score: 68
- Key headings: Geocoder dataset feasibility (planning pass); 1. Summary recommendation; 2. Option-by-option evaluation; 2.1 GeoNames — `cities500` / `cities1000` / `allCountries`; 2.2 Natural Earth — populated places (`ne_10m_populated_places`); 2.3 Who’s On First (WOF); 2.4 Pelias / Geocode Earth (open-data stack vs hosted); 2.5 Mapbox / Google (hosted geocoding & Places); 3. Licensing notes (high level — verify before ship); 4. Rough import plan (GeoNames-first); 5. Data fields needed (canonical `Place` record); 6. Proposed ranking formula (v1 — heuristic, explainable)
- Engineering signals:
  - **Companion docs:** `docs/cartographic_language_and_city_rendering.md`, `docs/next_implementation_sequence.md` (Priority band 4), `validation/narratives/city_data_and_search_notes.md`.
  - **Aspect-to-angle glow/aura:** unrelated; out of scope.
  - | **Long-term architecture** | **Product place ID** stable in your DB (geonames-based or WOF-based) + **optional Pelias-style search stack** *or* **hosted Maps HTTP API** for address-level and best-in-class ranking—depending on ops budget, attribution burden, and offline needs. **Who’s On First** is…
  - | **cities500** | ~185,000 | Cities **population &gt; 500** *or* admin seats down to **PPLA4**. Broad coverage; more noise and import size. |
  - | **cities1000** | ~130,000 | Cities **population &gt; 1000** *or* admin seats down to **PPLA3**. Reasonable **MVP tradeoff** (smaller than cities500, still includes many admin centers). |

### A.52 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/governance/anti_cursor_bullshit_governance_rules.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 37
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Engineering signals:
  - # Anti-Cursor Bullshit Governance Rules
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountability_failure_audit.md` §Anti-Bullshit Rules…
  - 3. **rollback path** — how to revert,

### A.53 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_memory_synthesis.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 16257; SHA-12: `04f378dc370d`; score: 73
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Engineering signals:
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.
  - Archaeology files are **mostly chronological**. When two extracts disagree, **prefer the later thread** for *current architectural and UX doctrine* unless the synthesis explicitly marks the topic **unresolved**. Examples that repeatedly matured across chats:
  - Older contradictory ideas stay valuable in **raw** archaeology (why pivots happened); they must not be silently erased from history—but they should not be copied into **durable current truth** without a reconciliation note.
  - | **What** | `ai_context/`, `docs/`, themed `consolidated_notes/`, validation narratives | Ephemeral thread context, model state, one-off instructions |

### A.54 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_philosophical_synthesis.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 115
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Engineering signals:
  - **Tone:** Institutional, explicit about **tensions** the product refuses to flatten.
  - The relocation astrology platform is built on a paradox that mature users already live inside: **structure is real, and agency is real**. The chart is treated as **structurally real** for product purposes—not as an infinitely rewriteable “vibe,” not as a story generator that owes the user a flatteri…
  - Underneath lies a technical moral that keeps philosophy honest: **inspectable precision**. If the map shows a region or line, it must mean something **precise** in the relocated model. “Plausible-looking geometry” is not validation. **False membership** is rejected even when cosmetics are rough; **r…
  - ### 2.1 Symbolic realism (not mythic inflation)
  - - **Right-click / point popup** is **canonical for “here”**—what holds at that coordinate in the relocated technical sense.

### A.55 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/intentionality_and_symbolic_constraints.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 8365; SHA-12: `d1c233003983`; score: 23
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Engineering signals:
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account): symbolic exploration on the map must stay **accountable** to structure.
  - - **Tradeoffs and limitations are real.** The system is designed for users who can hold that **not every relocation yields an unmitigated win.**
  - - **Astrology is not “manifestation culture.”** The product rejects the implication that belief or wording alone reshuffles symbolic structure without cost or constraint.
  - **Product consequence:** Math, overlays, and popups must remain **honest** about membership and relocated facts; interpretive layers must not **contradict** point truth for comfort.

### A.56 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/local_archive_policy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 1554; SHA-12: `5f3f7178bbfa`; score: 9
- Key headings: Local Archive Policy; Archive/Junk Drawer Candidates; Do Not Commit; Rule Of Thumb
- Engineering signals:
  - - Failed experiments that may teach something later.
  - - Temporary validation outputs worth keeping for proof-of-work.
  - - `archive_temp_validation/`
  - ## Do Not Commit
  - Do not commit disposable local/browser/system artifacts:

### A.57 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/map_and_overlay_design_research.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 5149; SHA-12: `f3943cdf7cf9`; score: 34
- Key headings: Map and Overlay Design Research; 1. Leaflet vs MapLibre vs Google Maps (philosophical comparison); 2. Current Leaflet strengths (for this codebase); 3. Actual blockers to watch for (hypothesis list—not confirmed); 4. Overlay transparency strategy (research directions); 5. Semantic overlap colors; 6. Aura rendering directions (non-commitments); 7. Map-edge and world-wrap ideas; 8. Dark / light mode implications; 9. Multilingual city rendering; 10. Decision rule (when to reopen migration); Related docs
- Engineering signals:
  - **Planning and research only.** No map migration is prescribed here. The project **stays on Leaflet for MVP** unless concrete blockers emerge (`ai_context/decisions.md`, `current_state.md`).
  - | Dimension | Leaflet (current) | MapLibre | Google Maps Platform |
  - | **Philosophy** | Small, composable, OSS tiles; you own interaction logic. | Vector-first, style-driven, OSS-core continuity from Mapbox GL patterns. | Full-stack commercial stack; deepest place data; platform coupling. |
  - | **Fit for this product** | Strong when overlays are **GeoJSON + careful projection/wrap discipline** and the team values **direct control** over truth vs display separation. | Strong if **vector basemaps**, **pitch**, **client-side style**, or **dense label collision** become central; learning cur…
  - | **Non-technical cost** | You maintain more glue (wrap, performance quirks). | Investment in style JSON, shader-era debugging. | Billing, keys, usage caps, compliance narrative. |

### A.58 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/next_implementation_sequence.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 10690; SHA-12: `ced0e563c90b`; score: 104
- Key headings: Next Implementation Sequence; Priority band 1 — UX polish (minimal architecture risk); Chunk 1.1 — Sidebar density and “debug vs ship” clarity; Chunk 1.2 — Popup and typography refinement; Chunk 1.3 — Native select stability + legend clutter reduction; Priority band 2 — Validator / stress tooling; Chunk 2.1 — Fixture manifest + “run these five” script; Chunk 2.2 — Latitude / polar stress suite expansion; Chunk 2.3 — Brute-force / truth export hygiene; Priority band 3 — Account + birth-data workflows; Chunk 3.1 — Birth data model (local-only MVP); Chunk 3.2 — Chart list + “open on map”
- Engineering signals:
  - Small, **low-risk**, **testable**, **isolated** chunks—ordered by current product priorities. This is **sequencing and planning only**, not a commitment to build everything listed.
  - - **Why:** Prototype sidebar is tall and noisy; professionals need long-session focus (`current_state.md`).
  - - **Dependencies:** None structural; CSS/layout in `map_CURRENT.html` (or extracted styles later).
  - - **Validation:** Visual pass; confirm map remains primary; no regression on popup/dropdown behavior.
  - - **Do not overengineer:** No new framework, no drawer rewrite here—**incremental compression** only.

### A.59 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/00_OPERATOR_START_HERE.md`
- Categories: backend_runtime_and_files, validation_and_rollback
- Characters: 697; SHA-12: `a0e79ddfcf29`; score: 2
- Key headings: AI Onboarding Entry Point
- Engineering signals:
  - - Complete Product Comprehension Gate
  - Understanding must be demonstrated, not claimed.

### A.60 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, cache_scheduler_performance, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 110
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Engineering signals:
  - **CANONICAL** for non-AI application UX architecture (Web 2.0 standalone product).
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doctrine.md`, `docs/data…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - Define the complete user journey for the **non-AI relocation platform**.

### A.61 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 67
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Engineering signals:
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Older doctrine and archaeology:** Older docs listed below remain valuable context, evidence, and active companions where not superseded. Treat them as secondary to `docs/constitutional/` on layer sovereignty, forbidden crossings, epistemic humility, runtime/renderer sovereignty, and implementation…
  - **Pacing reminder:** **Philosophy and epistemology evolve slowly** (explicit revision). **Implementation details evolve quickly** (iterate with evidence), but **must not contradict** slow doctrine without updating the doctrine file.
  - These files govern **meaning, agency, fate, tradeoffs, tone, and long-form institutional character**. They are **foundational**. Typical change rate: **rare**; edits should be deliberate, often after architect or governance review.

### A.62 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/README.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 6
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Engineering signals:
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - The system is a layered symbolic intelligence platform, not a monolithic astrology AI, recommendation engine, or chatbot with symbolic flavor.
  - ## Canonical
  - ## Semi-Canonical
  - These documents contain canonical principles plus exploratory or future-facing implementation detail. Treat their core boundaries as binding and their implementation models as revisable.

### A.63 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 80
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Engineering signals:
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - - implementation guidance, component specs, API contracts, or route definitions
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - ### Principle

### A.64 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 201
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Engineering signals:
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.
  - - `docs/ux_principles_and_emotional_tone.md`
  - - **Principle** — binding statement

### A.65 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 35789; SHA-12: `795365723409`; score: 186
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Engineering signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/supabase_schema_sandbo…
  - - what durable records exist,
  - - what belongs on each record,
  - - what must never be persisted as product truth,

### A.66 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 8365; SHA-12: `d1c233003983`; score: 23
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Engineering signals:
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account): symbolic exploration on the map must stay **accountable** to structure.
  - - **Tradeoffs and limitations are real.** The system is designed for users who can hold that **not every relocation yields an unmitigated win.**
  - - **Astrology is not “manifestation culture.”** The product rejects the implication that belief or wording alone reshuffles symbolic structure without cost or constraint.
  - **Product consequence:** Math, overlays, and popups must remain **honest** about membership and relocated facts; interpretive layers must not **contradict** point truth for comfort.

### A.67 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 28
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Engineering signals:
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - - an account management platform
  - - a client record system with a map attached

### A.68 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 33
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`.
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - Chart Record utility (optional route)

### A.69 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9566; SHA-12: `3de8663545ba`; score: 29
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - The workflow must remain **fully usable** without Astro Assist, scoring engines, or conversational intake.
  - ## Core workflow principle
  - **Browse, do not oracle.**

### A.70 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract
- Characters: 3360; SHA-12: `554add110fa4`; score: 19
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Engineering signals:
  - This document defines one of the most important distinctions in the platform:
  - Truth belongs primarily to Layer 1.
  - Astrological fact belongs primarily to Layer 2.
  - Interpretation belongs primarily to Layer 3.
  - - coordinate geometry,

### A.71 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/DOCTRINE_INDEX.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 67
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Engineering signals:
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Older doctrine and archaeology:** Older docs listed below remain valuable context, evidence, and active companions where not superseded. Treat them as secondary to `docs/constitutional/` on layer sovereignty, forbidden crossings, epistemic humility, runtime/renderer sovereignty, and implementation…
  - **Pacing reminder:** **Philosophy and epistemology evolve slowly** (explicit revision). **Implementation details evolve quickly** (iterate with evidence), but **must not contradict** slow doctrine without updating the doctrine file.
  - These files govern **meaning, agency, fate, tradeoffs, tone, and long-form institutional character**. They are **foundational**. Typical change rate: **rare**; edits should be deliberate, often after architect or governance review.

### A.72 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/README.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 6
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Engineering signals:
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - The system is a layered symbolic intelligence platform, not a monolithic astrology AI, recommendation engine, or chatbot with symbolic flavor.
  - ## Canonical
  - ## Semi-Canonical
  - These documents contain canonical principles plus exploratory or future-facing implementation detail. Treat their core boundaries as binding and their implementation models as revisable.

### A.73 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_CONSTITUTION.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 80
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Engineering signals:
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - - implementation guidance, component specs, API contracts, or route definitions
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - ### Principle

### A.74 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_DOCTRINE_MASTER.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 201
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Engineering signals:
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.
  - - `docs/ux_principles_and_emotional_tone.md`
  - - **Principle** — binding statement

### A.75 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/constitutional_summary.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 4609; SHA-12: `8238f401edb1`; score: 21
- Key headings: Constitutional Summary; Purpose; Layer Architecture; Layer 1 - Truth; Layer 2 - Symbolic Ontology; Layer 3 - Intentional Interpretation; Layer 4 - Exploratory Optimization; Forbidden Crossings; Epistemic Doctrine; Runtime And Renderer Sovereignty; Purification Principle; Professional Trust And AI Behavior
- Engineering signals:
  - The Relocation App is a layered symbolic intelligence platform. It is not a monolithic astrology chatbot, hidden recommendation engine, or mystical certainty machine.
  - - coordinate validity,
  - Layer 1 is deterministic, inspectable, objective, and independently verifiable. It must not interpret, optimize, moralize, psychologically frame, or alter truth to satisfy user desire.
  - Layer 2 may interpret truth through a declared symbolic framework, but it may never rewrite geometry. Symbolic systems may disagree; no ontology is permanently privileged as universal truth.
  - Layer 3 owns contextual interpretation relative to user goals, lived context, priorities, and tradeoffs.

### A.76 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/epistemic_integrity_and_symbolic_humility.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract, future_infrastructure
- Characters: 3739; SHA-12: `242cc62cfae5`; score: 7
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior; Good Behavior; Collaborative Discovery
- Engineering signals:
  - This document is CANONICAL.
  - All AI and interpretive systems must follow these principles.
  - This document establishes the philosophical and operational rules governing:
  - The system must prefer:
  - # Core Principle

### A.77 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/intentionality_and_symbolic_constraints.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 8365; SHA-12: `d1c233003983`; score: 23
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Engineering signals:
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account): symbolic exploration on the map must stay **accountable** to structure.
  - - **Tradeoffs and limitations are real.** The system is designed for users who can hold that **not every relocation yields an unmitigated win.**
  - - **Astrology is not “manifestation culture.”** The product rejects the implication that belief or wording alone reshuffles symbolic structure without cost or constraint.
  - **Product consequence:** Math, overlays, and popups must remain **honest** about membership and relocated facts; interpretive layers must not **contradict** point truth for comfort.

### A.78 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layer_sovereignty_and_forbidden_crossings.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract, future_infrastructure
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 13
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Engineering signals:
  - This document is CANONICAL.
  - These rules are mandatory architectural constraints.
  - # Core Principle
  - # Constitutional Rule
  - but may NEVER rewrite lower-layer truth.

### A.79 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layered_symbolic_intelligence_architecture.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract, future_infrastructure
- Characters: 4801; SHA-12: `5242de0598f3`; score: 24
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Engineering signals:
  - This document is CANONICAL.
  - It defines the constitutional layer architecture of the platform.
  - All future systems must respect:
  - This document defines the core architectural philosophy of the platform.
  - The platform is intentionally divided into distinct symbolic intelligence layers.

### A.80 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/map_first_product_doctrine_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 28
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Engineering signals:
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - - an account management platform
  - - a client record system with a map attached

### A.81 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract, future_infrastructure
- Characters: 3360; SHA-12: `554add110fa4`; score: 19
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Engineering signals:
  - This document defines one of the most important distinctions in the platform:
  - Truth belongs primarily to Layer 1.
  - Astrological fact belongs primarily to Layer 2.
  - Interpretation belongs primarily to Layer 3.
  - - coordinate geometry,

### A.82 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/2026-05-29_application_journey_architecture_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, cache_scheduler_performance, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 110
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Engineering signals:
  - **CANONICAL** for non-AI application UX architecture (Web 2.0 standalone product).
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doctrine.md`, `docs/data…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - Define the complete user journey for the **non-AI relocation platform**.

### A.83 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/PLAIN_LANGUAGE_PRODUCT_EXPLANATION_v1_2026-06-01.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback
- Characters: 6093; SHA-12: `0c7a9042f0a5`; score: 19
- Key headings: Plain Language Product Explanation; What Problem Does The Product Solve?; Why Relocation Astrology Is Geographic; Why The Map Is The Primary Discovery Instrument; What Overlays Represent; Why Cities Are Not The Primary Object Of Analysis; Natal Chart; Current Location Chart; Candidate Location Chart; Favorites; Saved Searches; Comparison
- Engineering signals:
  - This document explains the relocation astrology platform in ordinary language.
  - The same birth moment produces different houses, angles, and angle relationships when cast for different locations.
  - Cities are human labels attached to coordinates.
  - The astrology exists at coordinates.
  - - aspect-to-angle relationships

### A.84 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_constitution_and_review_architecture.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 13121; SHA-12: `96b9567947d8`; score: 46
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Engineering signals:
  - - **`docs/review_contracts_and_governance.md`** — lightweight **implementation review** prompts (AI behavior, UX, symbolic integrity, contemplative space); complements this file’s Layer 2 duties.
  - - **`docs/DOCTRINE_INDEX.md`** — canonical map of doctrine docs, stability, and reading order.
  - | **Preserve symbolic integrity** | Outputs must stay **accountable** to chart structure—not **rewritten** for likability. |
  - | **Prevent emotional manipulation and dependency** | No **oracle intimacy**, **certainty addiction**, or **replacing** the user’s judgment with model cheerleading. |
  - | **Flattery** | User feels **clever, chosen, spiritually advanced** regardless of chart cost. |

### A.85 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 75
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Engineering signals:
  - **CANONICAL** for **future** AI-assisted interpretation layers — not current product scope.
  - This doctrine governs **language, posture, and review** — not model choice, prompt templates, or UI implementation.
  - Relocation decisions touch housing, career, relationships, health, and identity. Users arrive with hope, anxiety, and real constraints. An interpretive layer that **declares outcomes** or **names perfect places** does three harms:
  - 1. **Epistemic harm** — astrology describes **archetypal structure**, not literal life scripts. Conflating pattern with destiny is false precision.
  - 2. **Agency harm** — the user’s values, budget, visa status, family, and timing determine meaning. The app must **support judgment**, not replace it.

### A.86 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 34
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **epistemic tiers**, **user-facing honesty**, **data recording**, and **engine behavior boundaries** for uncertain birth times. Not implementation. Not rectification software spec.
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `validation/narratives/post_truth_grid_sta…
  - - houses and angles move rapidly with time,
  - - AI intake may help later — **MVP must handle tiers without AI**.

### A.87 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_and_experience_foundations.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 34
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Engineering signals:
  - **What this is not:** A brand book, logo spec, marketing narrative, campaign, or visual identity system. **No** speculative public branding.
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).
  - - **Warm, safe containment:** The environment should feel like a **warm blanket** or **safe, contemplative room**—**breathable, calm, trustworthy, spacious, emotionally safe**—so users can **inhabit** it comfortably for **hours**.
  - - **Long sessions without fatigue:** Typography, color restraint, spacing, and low noise support **sustained** exploratory use; the product should feel like a **home** for serious play, not a sprint through a flashy demo.
  - - **Instrument, not dashboard:** A core principle—see below; the tool **serves** the user’s inner work, it does not **perform** for them.

### A.88 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_visual_language_and_design_doctrine.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 29
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - - contemplative symbolic geographic instrument,
  - | **Category** | Relocation astrology exploration — not generic astrocartography clone |
  - | **Emotion** | Contemplative long-session comfort |

### A.89 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/client_chart_data_model_v1_2026-05-29.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 35789; SHA-12: `795365723409`; score: 186
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Engineering signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/supabase_schema_sandbo…
  - - what durable records exist,
  - - what belongs on each record,
  - - what must never be persisted as product truth,

### A.90 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/conversational_discovery_and_intentionality.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, frontend_backend_contract, future_infrastructure
- Characters: 4218; SHA-12: `c7b5d8b9fc8e`; score: 14
- Key headings: Conversational Discovery And Intentionality; Status; Purpose; Core Principle; User intentionality is sovereign.; Intentionality Discovery; Examples; Archetypal Exploration; Example Exploratory Style; Intentionality Strength; Examples; Layer Relationship
- Engineering signals:
  - This document is PARTIALLY CANONICAL.
  - The principles of:
  - are canonical.
  - This document defines how the platform should:
  - - manipulative,

### A.91 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/core_product_truths.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9535; SHA-12: `9d9048f7cab4`; score: 33
- Key headings: Core Product Truths; Astrology Truth; Inspectability; Map and Overlay UX; Product Experience; Visual / Semantic Product Identity; Emotionally non-interfering design (experiential constraints); Interpretive language and emotional transparency (doctrine); Interpretive integrity and archetypal honesty (doctrine); Development Discipline; Where the nuanced history lives
- Engineering signals:
  - These are durable principles that should survive individual implementation chunks, UI experiments, and future chat transitions.
  - - Map overlays must agree with point-and-click astrology truth.
  - - Popup point-truth validation is authoritative for local membership checks.
  - - Canonical backend truth must not be altered to satisfy frontend display constraints.
  - - Frontend wrapping, clipping, or rendering should never change logical astrology membership.

### A.92 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/geocoder_and_city_identity_strategy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 42
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Engineering signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - **Related:** `memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `docs/geocoder_dataset_feasibility.md`, `docs/cartographic_language_and_city_rendering.md` (basemap change ⇒ **§0** full visual re-test), `docs/relocation_app_product_roadmap.md` §7–8, `docs/map_and_overlay_desig…
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`). The map binds **human geography** to …
  - Current prototype list search (`cities.js`) is a **stand-in** only: **name, lat/lng, population (and minimal fields)**—**no reliable country/admin**, **no alternate names**, **no stable place IDs**, and **no** trustworthy global ranking (e.g. Paris, France vs Paris, Texas; London vs Londonderry). **…
  - - **Exact-coordinate entry** (lat/lon or paste) is required for parity with **right-click truth** and for places not in any city list.

### A.93 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/map_drawer_and_layer_control_doctrine.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 7226; SHA-12: `181a6ad8f6bd`; score: 20
- Key headings: Map Drawer and Layer Control Doctrine; Status; Purpose; Control hierarchy (map screen); Drawer architecture (target); Zones; Genie-into-corner collapse; Deferral (current phase); Condition editor doctrine; Target model; Card visual language; Search action
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **Reads with:** `docs/overlay_and_aura_visual_strategy.md` §H, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/visual_semantic_style_guide.md` §9, `docs/product_workflows/product_screen_and_transition_architecture.md`.
  - Keep the **map sacred**. Controls must:
  - **Rule:** if a control hides coastlines, labels, or overlap evidence, it fails.
  - - flexible **Add condition** rows exist (API coordinated),

### A.94 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/product_screen_and_transition_architecture.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 33
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`.
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - Chart Record utility (optional route)

### A.95 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_mode_vs_lay_mode_strategy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 3492; SHA-12: `c166907d611f`; score: 5
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Engineering signals:
  - Core principles are canonical.
  - # Core Principle
  - ## The platform should remain professionally trustworthy while still accessible to non-professionals.
  - The system must avoid:
  - - do not know astrological terminology,

### A.96 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_non_ai_workflow_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9566; SHA-12: `3de8663545ba`; score: 29
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - The workflow must remain **fully usable** without Astro Assist, scoring engines, or conversational intake.
  - ## Core workflow principle
  - **Browse, do not oracle.**

### A.97 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_trust_and_ai_behavior_doctrine.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, frontend_backend_contract, future_infrastructure
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 10
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Engineering signals:
  - This document defines how AI systems inside the platform must behave.
  - The AI must never behave like:
  - - a manipulative mystic,
  - # Core Principle
  - This principle is absolute.

### A.98 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_workflow_and_explanatory_language.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 11541; SHA-12: `1814ff883a7c`; score: 89
- Key headings: Professional Workflow And Explanatory Language; Status; Purpose; Professional Map Workflow; Desired Placement Search; Exclude / NOT Variables; Solo And Mute Controls; Inspection Workflow; Helper Layers; Intention Remains Primary; Astro Assist Substitution Guidance; Additive And Subtractive Relocation
- Engineering signals:
  - Update this document whenever product explanation language, professional workflow guidance, or popup copy concepts are clarified.
  - This document preserves explanatory language and professional workflow doctrine for later use in:
  - 5. Use solo and mute controls to isolate or declutter layers.
  - Professionals may also select placements they explicitly do not want.
  - These helper layers must remain optional and explanatory.

### A.99 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/symbolic_language_style_guide.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, future_infrastructure
- Characters: 1703; SHA-12: `11e6dd9bdb1a`; score: 6
- Key headings: Symbolic Language Style Guide; Purpose; Core Principle; Preferred Style; Avoid; Good Examples; Bad Examples; Archetypal Precision; Symbolic Humility; Constitutional Goal
- Engineering signals:
  - This document defines how symbolic language should be expressed by the platform.
  - # Core Principle
  - - mystical for performance,
  - - manipulative certainty,
  - - "This pattern often relates to..."

### A.100 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ux_principles_and_emotional_tone.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 4906; SHA-12: `3924025d2ba8`; score: 18
- Key headings: UX Principles and Emotional Tone; 1. Core temperament; 2. Map-first atmosphere; 3. Delight without spectacle; 4. Overlap readability philosophy; 5. Typography and color tone; 6. Layout cautions: drawer / genie / chrome; 7. Mobile and tablet; 8. When to stop designing; 9. Where philosophy is already strong in the repo; 10. Where philosophy could still drift; Related docs
- Engineering signals:
  - # UX Principles and Emotional Tone
  - A concise distillation of how the product should **feel** and **behave**. Complements `docs/relocation_app_product_roadmap.md` (strategy) and `docs/overlay_and_aura_visual_strategy.md` (visual planning).
  - | Principle | Meaning |
  - | **Anti-overdesign** | No speculative chrome before map truth and readability are solid. |
  - - **Contemplative** pacing: users may spend long sessions panning and comparing—comfort matters more than initial “wow.”

### A.101 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/visual_semantic_style_guide.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9451; SHA-12: `93105f1b5ba9`; score: 52
- Key headings: Visual & Semantic Style Guide (Relocation Map System); 1. Visual epistemology (truth hierarchy); 2. House field semantics (categorical + cusp softness); 3. Aspect-to-angle aura semantics (intensity, not category); 4. Overlay texture semantics (almost subconscious); 5. NOT / exclusion overlays; 6. Color philosophy; 7. Popup visual language; 8. Interface tone; 9. Map and control relationship; 10. Account / chart page relationship; 11. Implementation discipline
- Engineering signals:
  - **Companion docs:** `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/map_and_overlay_design_research.md`, `docs/brand_and_experience_foundations.md`, `docs/intentionality_and_symbolic_constraints.md` (fate/agency/tradeoffs), `docs/ai_constitution_and_revi…
  - | **Right-click / point popup** | **Canonical point truth** for the queried location | Authoritative for “what is true *here*” at that click (degrees, houses, etc.). |
  - **Popups are appetizers, not full chart reports.** They must stay information-dense but **legible**; the heavy tables belong off-map.
  - - **Planet-in-house regions are categorical fields:** inside/outside membership for the chosen house rule must stay **truthful** (already a product moral).
  - - **Visual breadth:** regions may read **broad and soft** at the polygon edge as long as **membership** remains correct for the engine’s definition.

### A.102 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ai_conversational_modes.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 2887; SHA-12: `b796e2065486`; score: 6
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Engineering signals:
  - - canonical architectural principles,
  - - and guide long-term extensibility.
  - # Core Principle
  - The AI should adapt conversational style without violating constitutional doctrine.
  - It must not fabricate comfort.

### A.103 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/archaeology_and_synthesis_workflow.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9005; SHA-12: `d3add7674811`; score: 21
- Key headings: Archaeology and synthesis workflow; 1. Pipeline overview; 2. When to create an archaeology pass; 3. When to create or update synthesis docs; 4. Durable truths vs transient implementation; 5. How to avoid flattening nuance during synthesis; 6. Preserving contradictory but valuable tensions; 7. Doctrine canonicalization; 8. Open tension preservation; 9. Institutional memory updating (rhythm); 10. Governance refresh; 11. Review bundle generation
- Engineering signals:
  - **Purpose:** Capture chat and session intelligence **without** flattening nuance, **without** treating the latest thread as law, and **without** losing rejected paths that explain pivots.
  - Raw capture → themed synthesis → doctrine canonicalization → open tension preservation
  - | **Bridge / labels** | `docs/institutional_memory_synthesis.md` | Implemented / roadmap / speculative |
  - | **Canonical doctrine** | `docs/`, `ai_context/core_product_truths.md` | Slow law |
  - | **External audit package** | `docs/review_bundle/` | Snapshot copies + tensions summary |

### A.104 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/decision_and_uncertainty_framework.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9068; SHA-12: `4b8f251dada4`; score: 45
- Key headings: Decision and uncertainty framework; 1. Bounded uncertainty; 2. Heuristic vs exact truth; 3. Symbolic plausibility vs fake precision; 4. Exploratory guidance vs deterministic recommendation; 5. Preserving ambiguity intentionally; 6. Reversible decisions; 7. Experimentation doctrine; 8. User-facing confidence vs backend uncertainty; 9. “Good enough for exploration” vs “authoritative truth”; 10. Case study: aura philosophy; 11. Visual approximation doctrine
- Engineering signals:
  - | **Symbolic ambiguity** (paradox, multi-valence) | **Preserve intentionally**; do not force single verdict in software. |
  - **Bounded uncertainty** means: be precise where the engine is precise; be honest where the engine is silent; do not **smuggle certainty** through UI fluency or model confidence.
  - Some questions **should remain open** until practitioner feedback or long-session stress testing—not because the team is indecisive, but because **premature certainty** would lie.
  - - Relocated chart values at a point (popup / API).
  - - Binary region membership for defined rules (truth grid / validated contours).

### A.105 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/doctrine_review_cycle.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9902; SHA-12: `00598386986c`; score: 37
- Key headings: Doctrine review cycle; 1. What this cycle protects; 2. Slow docs policy; 3. Implementation vs philosophy separation; 4. Tension-preservation doctrine; 5. Rationale preservation rules (“why”, not just “what”); 6. Review cadences (suggested, not ceremonial); 6.1 Doctrine coherence review; 6.2 AI drift audit; 6.3 UX coherence review; 6.4 Archaeology / synthesis refresh; 6.5 Review bundle / external audit
- Engineering signals:
  - **Purpose:** Periodic coherence maintenance so the project does not **silently drift**, **forget reasoning**, **flatten tensions**, or **confuse fast implementation with slow philosophy**.
  - This is **not** bureaucracy. It is a **lightweight rhythm** for a long-lived symbolic instrument: enough structure that future contributors inherit **why**, not only **what**.
  - - **Experiential coherence** — map-first calm, contemplative space, overlap readability, truth hierarchy.
  - - **Implementation sanity** — fast layers may iterate without rewriting meaning in code alone.
  - **Fast docs** govern **what is true now** and **how we ship**: `ai_context/current_state.md`, `ai_context/decisions.md`, validation narratives, tactical tuning notes.

### A.106 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/future_excellence_vs_future_feature_excellence.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 17
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Engineering signals:
  - - canonical architectural principles,
  - # Core Principle
  - ## Infrastructure excellence and feature excellence must remain distinct.
  - - rollback safety,
  - - rollback discipline,

### A.107 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer4_optimization_and_exploration_doctrine.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 4341; SHA-12: `289b4552320f`; score: 12
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Engineering signals:
  - - canonical Layer 4 principles,
  - Core Layer 4 boundaries are canonical.
  - - user-intent violations,
  - # Core Principle
  - - reducing chronic 12th-house isolation,

### A.108 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer5_experiential_education_through_travel_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 17
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Engineering signals:
  - **Dependency:** Requires mature AI guidance, relocation exploration substrate, and user observation capture — **after** standalone Web 2.0 facts-first product is proven.
  - **Must not be read as:** screen spec, sprint backlog, course marketplace brief, or Layer 1–3 implementation requirement.
  - The platform already supports **facts at locations** (Layer 1) and will eventually support **interpretive assistance** (AI layers). Layer 5 education sits **above** those — it organizes **experience over time** into curricula that reward observation, travel, and personal comparison.
  - | Notice what changed when you relocated or slowed down | Memorize rules without location context |
  - Reading may support the journey — glossaries, brief context, safety notes — but **reading is never the main pedagogical engine**. The main engine is **lived geographic comparison** grounded in the same factual substrate the professional instrument provides.

### A.109 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/local_archive_policy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 1554; SHA-12: `5f3f7178bbfa`; score: 9
- Key headings: Local Archive Policy; Archive/Junk Drawer Candidates; Do Not Commit; Rule Of Thumb
- Engineering signals:
  - - Failed experiments that may teach something later.
  - - Temporary validation outputs worth keeping for proof-of-work.
  - - `archive_temp_validation/`
  - ## Do Not Commit
  - Do not commit disposable local/browser/system artifacts:

### A.110 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/memory_workflow.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 6877; SHA-12: `0a90f034aa1f`; score: 28
- Key headings: Memory Maintenance Workflow; Purpose; Sources; Mining Old Chats; Processing Extraction Docs; Consolidating Raw Archaeology (optional phase); Updating Durable Memory; Memory Types; Raw Extraction; Durable Memory; Roadmap; Current Implementation State
- Engineering signals:
  - This document explains how project memory should be maintained without turning old chats, reports, and speculative ideas into an unstructured pile.
  - - Cursor task reports in `cursor_latest_report.md`.
  - - AI reviews in `review_latest.md`.
  - - Validation reports and narratives under `validation/`.
  - - Durable product principles.

### A.111 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/mvp_beta_and_future_feature_roadmap.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, cache_scheduler_performance, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 4767; SHA-12: `c904d8af5d1e`; score: 17
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes; Stage 2 — Professional Beta; Goal
- Engineering signals:
  - This document defines the broad strategic build sequence for the platform.
  - # Core Principle
  - - and long-term slowdown.
  - The platform is expected to evolve in several major stages.
  - - cache/runtime discipline,

### A.112 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract, future_infrastructure
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 18
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Engineering signals:
  - - canonical architectural principles,
  - - and guide long-term extensibility.
  - This document defines how multiple astrological systems may coexist within the platform.
  - The platform is constitutionally designed to support:
  - # Core Principle

### A.113 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_continuity_workflow.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 5184; SHA-12: `8a80bdfb8e6e`; score: 17
- Key headings: Project Continuity Workflow; 1. Goals; 2. Memory lanes (what goes where); 3. Archaeology intake workflow; 4. Consolidation workflow (when to run); 5. Reviewer workflow; 6. Proposed updates workflow; 7. Raw archaeology vs durable truths; 8. How future chats should initialize; 9. How to continue safely after context loss; 10. Related docs
- Engineering signals:
  - - **Clear separation:** raw archaeology vs curated principles vs implementation state.
  - - **Safe recovery** after long breaks or context loss.
  - | **Raw archaeology** | `memory_archaeology_raw/pending_imports/` | Verbatim / chronological extracts; **not** canonical alone. |
  - | **Durable truths** | `ai_context/core_product_truths.md`, `decisions.md`, `product_brief.md` | Stable principles and decisions. |
  - - Several new `pending_imports` files accumulate.

### A.114 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_memory_taxonomy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 5641; SHA-12: `e630f6401456`; score: 28
- Key headings: Project Memory Taxonomy; Architecture; UX Philosophy; Visual doctrine vs rendering experiments vs temporary UX; Implementation State; Future Features; Rejected Approaches; Validation Methodology; Edge Cases; Unresolved Questions; AI Strategy; Product Philosophy
- Engineering signals:
  - This taxonomy keeps project memory organized as the app grows across chats, validation passes, experiments, and external reviews.
  - - Canonical backend truth versus frontend display geometry.
  - Stable experience principles and design constraints.
  - **Doctrine vs experiments:** Stable UX principles live here and in `ai_context/core_product_truths.md` (“Visual / Semantic Product Identity”). **Durable visual doctrine** (epistemology: what overlays *mean* vs what popups *prove*) is expanded in **`docs/visual_semantic_style_guide.md`** and **`docs/…
  - **Experimental rendering implementation** — How a doctrine might be encoded (SVG vs Canvas, aura ramp, cusp edge blend, faint textures). Belongs in planning/spec docs (`docs/overlay_and_aura_visual_strategy.md`) and **feature-flagged** or branch prototypes until validated; must not be treated as can…

### A.115 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/relocation_strategy_framework.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, frontend_backend_contract, future_infrastructure
- Characters: 2978; SHA-12: `5542c6b3c8b9`; score: 11
- Key headings: Relocation Strategy Framework; Status; Purpose; Core Principle; Subtractive relocation comes before additive optimization.; Subtractive Relocation; Additive Relocation; Strong Relocations Often Do Both; Tradeoff Reality; Archetypes Are Contextual; Optimization Delusion; Layer 4 Behavior
- Engineering signals:
  - - canonical architectural principles,
  - - and guide long-term extensibility.
  - This document defines the broad relocation strategy philosophy of the platform.
  - - escaping negatives,
  - It is the strategic reshaping of symbolic atmosphere.

### A.116 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ai_and_professional_workflow_strategy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 4077; SHA-12: `093c412a15e4`; score: 19
- Key headings: AI and Professional Workflow Strategy (From Archaeology); Institutional memory vs chat memory (anti–vibe-chaos); AI reviewer infrastructure (evolution); Non-negotiable product stance; AI collaboration failures as institutional risk; Second-opinion models; Practitioner assist vision (future); Consumer / intake AI (later); Strategic business hypotheses (treat as archaeology, not commitments); Tension to preserve
- Engineering signals:
  - - **Project memory** (`ai_context/`, `docs/`, themed consolidated notes) is **slow, deliberate, and reconciled to the codebase**—the antidote to treating the latest model reply as law.
  - **Anti–vibe-chaos principles** (from repeated archaeology):
  - - **Direction in archaeology:** reviewer prompts should carry **exact scripts, expected outputs, and hypotheses**; screenshots alone are fragile.
  - - **Non-AI / “dumb mode” remains sacred:** the app must be fully usable without automated interpretation—professional sovereignty matters ethically and commercially.
  - - **AI is augmentation, not authority:** aids with alternatives, intake translation, summaries—does not replace judgment.

### A.117 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/current_sidebar_ux_audit.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 4992; SHA-12: `c07666b5828f`; score: 33
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces; 9. Condition model — **next structural UX step (documented)**; 10. Location search placement (documented)
- Engineering signals:
  - **Intent:** Describe friction, record implemented fixes, and flag **documented-only** next steps (no redesign commitment).
  - - **Aspect overlay:** less neon fallback teal; unchanged API/staging logic.
  - - **Chart popup:** ASC/MC show **one formatted line each** from API `asc` / `mc` (`format_zodiac` strings); duplicate sign-only lines removed; planet table **bold headers**, normal planet names, **centered** house column.
  - - Fixed panel still trades width vs map; **reset control** mitigates **lost world** after heavy panning.
  - - Popups use **`.popup-chart`** patterns; **angle-sign** no longer reads as striped/strobed at some zooms (stroke removed).

### A.118 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/foundational_product_truths.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 4380; SHA-12: `9c5286269c09`; score: 18
- Key headings: Foundational Product Truths (From Archaeology); Trust and truth; Overlap and decision-making; Precision vs cosmetics (non-negotiable vs acceptable); Separation of concerns (recurring architectural moral); Human + AI collaboration stance; Emotional tone and moat; Repetition as signal
- Engineering signals:
  - **Status labels:** *Durable principle* = should guide decisions for years. *Product stance* = strategic positioning. *Process principle* = how the team builds.
  - - **Durable principle — Inspectable precision:** If the map shows a region, line, or overlap, it must mean something **precise** in the relocated chart model. “Plausible geometry” is not validation. Trust is built through reproducible checks, not visual confidence.
  - - **Durable principle — The map is the primary model (not an illustration):** Users explore **geography as astrology**. The map is not decoration around a chart calculator; it is the main instrument.
  - - **Durable principle — Professional rigor before lay simplification:** Build a **neutral, powerful professional engine first**; simplify for lay users only after the foundation is trustworthy.
  - - **Durable principle — Overlap is often the answer:** The deepest product value is where conditions coincide—house + house, house + angle sign, angle + aspect corridor, multi-condition intersection. Overlap is a **semantic object**, not a rendering accident.

### A.119 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/geocoder_and_city_strategy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract
- Characters: 1799; SHA-12: `098e8b02e313`; score: 12
- Key headings: Geocoder and City Strategy (From Archaeology); Why cities are core (not decoration); Readability and density; Search and disambiguation; Internationalization; Provider strategy tension (open); Dataset anecdotes (process lessons); UX details that affect trust
- Engineering signals:
  - Relocation decisions happen at **named places**; the map must connect semantically rich astrology overlays to **human geography**.
  - - Philosophy appears: optimize **cities per square inch / screen area**, not population alone.
  - - Zoom-threshold approaches and bounding-box rendering recur as prototypes.
  - - Need structured results: city + region/state + country + coordinates + optional population; **ranking by human relevance**, not only database order.
  - - Non-Latin labels and mixed scripts complicated manual validation.

### A.120 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_memory_synthesis.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 16257; SHA-12: `04f378dc370d`; score: 73
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Engineering signals:
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.
  - Archaeology files are **mostly chronological**. When two extracts disagree, **prefer the later thread** for *current architectural and UX doctrine* unless the synthesis explicitly marks the topic **unresolved**. Examples that repeatedly matured across chats:
  - Older contradictory ideas stay valuable in **raw** archaeology (why pivots happened); they must not be silently erased from history—but they should not be copied into **durable current truth** without a reconciliation note.
  - | **What** | `ai_context/`, `docs/`, themed `consolidated_notes/`, validation narratives | Ephemeral thread context, model state, one-off instructions |

### A.121 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_philosophical_synthesis.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 115
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Engineering signals:
  - **Tone:** Institutional, explicit about **tensions** the product refuses to flatten.
  - The relocation astrology platform is built on a paradox that mature users already live inside: **structure is real, and agency is real**. The chart is treated as **structurally real** for product purposes—not as an infinitely rewriteable “vibe,” not as a story generator that owes the user a flatteri…
  - Underneath lies a technical moral that keeps philosophy honest: **inspectable precision**. If the map shows a region or line, it must mean something **precise** in the relocated model. “Plausible-looking geometry” is not validation. **False membership** is rejected even when cosmetics are rough; **r…
  - ### 2.1 Symbolic realism (not mythic inflation)
  - - **Right-click / point popup** is **canonical for “here”**—what holds at that coordinate in the relocated technical sense.

### A.122 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/map_workspace_behavior_audit_v1_2026-05-30.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 15325; SHA-12: `7567f30ce7ff`; score: 106
- Key headings: Map Workspace Behavior Audit v1; Status; Purpose; Language and ID doctrine (applies to all sections); 1. Behavior already decided; Genie modes; Reasons to reopen Genie (decided intents); Search and render; Variable model; Legacy adapter (handoff to production map path); Map surface and overlay doctrine; Clear Map
- Engineering signals:
  - **AUDIT** — records what is decided, partially decided, and undecided for the map workspace (Genie + map surface + exploration chrome).
  - - `docs/contracts/genie_render_payload_v1_2026-05-30.md`
  - This document does **not** add features, layouts, or architecture. It consolidates decisions already present in contracts and related doctrine.
  - | Rule | Status |
  - | **Stable IDs are canonical** | Decided — type ids (`planet_in_house`, …), registry ids, payload field names |

### A.123 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/open_questions_and_unresolved_areas.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, cache_scheduler_performance, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3871; SHA-12: `c86a26458dc6`; score: 20
- Key headings: Open Questions and Unresolved Areas (From Archaeology); Geometry and calculation semantics; Rendering architecture; Validation systems; UX systems; Data + search; Product scope and ethics; Renderer beta stabilization questions (Chat 08); Operational workflow; Weak archaeology coverage (second pass, 2026-05); Human review gate
- Engineering signals:
  - ## Geometry and calculation semantics
  - - Formal spec for **MC** presentation: relocated ecliptic MC vs culmination/RA line products—must be explicit in user-facing language and internal tests.
  - - **Polar / high-latitude policy:** reconcile archaeology’s mixed numbers (±60, ±65, grids -60..86) into a user-understandable policy + advanced override stance.
  - - Long-term **display adapter** strategy: world copies, fragment IDs, picking behavior, performance budgets.
  - ## Validation systems

### A.124 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/product_brief.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3080; SHA-12: `ba708a2f1745`; score: 18
- Key headings: Product Brief; Product; Current Core Capabilities; Product Philosophy; Overlay Truth Standard; Current Architecture Direction; Validation Corpus; Institutional memory (archaeology)
- Engineering signals:
  - - `truth_grid` house overlays for Planet-in-House searches.
  - - Debug geometry mode for tracing backend canonical features through frontend display features.
  - - AI should support the professional core later, not replace it.
  - The app should not casually accept mathematical inaccuracies. Canonical backend geometry must be trustworthy and stable. Frontend wrapping, clipping, and display adaptation must never change logical astrology semantics.
  - - Keep canonical truth and display geometry conceptually separate.

### A.125 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/rejected_or_obsolete_approaches.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, validation_and_rollback, frontend_backend_contract
- Characters: 2949; SHA-12: `9bccda948bdc`; score: 19
- Key headings: Rejected or Obsolete Approaches (From Archaeology); Geometry / seam handling; Rendering / signal processing mistakes; Aspect / line extraction misconceptions (historic debugging); Incorrect astronomical short-cuts (explicit catastrophic failures); UX / workflow paths; Institutional / AI process paths; Overlap representation (product iteration); Possibly obsolete but historically explanatory; Not “rejected,” but **dangerous if misunderstood**
- Engineering signals:
  - This list preserves **why** certain paths were abandoned or flagged dangerous. Do not revive without explicit human re-approval.
  - - **Seam repair by altering canonical polygon topology** (boundary-walking / forced closure along map window edges): caused **house identity leakage**, collapsed distinct houses, Southern Hemisphere artifacts—**rejected as architecture**.
  - - **Gaussian blur** (or similar) on astronomical fields used for truth extraction: can **shift** solutions and create false loops—rejected for truth; aesthetics belong in frontend-only layers.
  - - Confusing **RA** targets with **ASC ecliptic longitude** work—**rejected** as conceptual error (ASC/MC coordinate framing must match the chosen product definition).
  - - **“NOT in house” as a giant inverse paint** (whole-world exclusion visuals): rejected as unusable map semantics (may reappear as subtler constraints later).

### A.126 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/relocation_app_product_roadmap.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 27057; SHA-12: `24ab9bae5cb8`; score: 141
- Key headings: Relocation App Product Roadmap; 1. Current Stable Milestone; 2. Product Philosophy; 3. Core Search Types; 4. Overlay/Color System Roadmap; 5. Aspect Aura Roadmap; 6. UX/Layout Roadmap; 7. City Search / Geocoder Roadmap; 8. Birth Data / Accounts / Professional Mode Roadmap; Saved Object Taxonomy; Phase 2.4 Sampling / Cache Scaffold; Phase 2.5 Sampling / Cache Population Strategy
- Engineering signals:
  - This document preserves the current product strategy, development sequence, UX philosophy, and validation priorities for future work.
  - - `truth_grid` house overlays are working and remain opt-in.
  - - Popup truth generally matches overlays in current validation.
  - - Validation contradictions are `0` in current truth-grid and angle-sign tests.
  - - `truth_grid` is not yet default.

### A.127 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/travel_and_future_modes.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, cache_scheduler_performance, database_and_persistence, validation_and_rollback, future_infrastructure
- Characters: 1279; SHA-12: `c351ba13dcef`; score: 11
- Key headings: Travel and Future Modes (From Archaeology); Road-trip / GPS mode; Offline / airplane scenarios; Transit overlays and relocated houses (debated); Positioning consequence; Dependencies called out
- Engineering signals:
  - **Status:** Mostly **speculative / roadmap**; repeatedly described as differentiator, not MVP requirement.
  - - Route-based UX appears in multiple places: slider along a path; “chart evolution mile by mile.”
  - GPS can work without network; archaeology suggests **pre-downloaded tiles/caches/routes** so travel mode works in constrained connectivity.
  - Travel mode reframes the app from static comparison to **lived movement**—high engineering and validation complexity; likely **late-phase** feature family.
  - - reliable caching, performance, mobile UX, clear disclosure of what is being computed (natal vs relocated vs transits), and likely a different map interaction model.

### A.128 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ux_and_design_language.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3849; SHA-12: `ac5f86eb3a13`; score: 16
- Key headings: UX and Design Language (From Archaeology); Map-first and spatial reading; Trust UX vs explanation UX; Typography and popups (professional validation patterns); Interaction pitfalls called out repeatedly; Emotional tone; Product positioning language (from archaeology); Tensions to preserve (not resolve here); Chat 08 update: style presets and mobile layer control
- Engineering signals:
  - - **Map dominance:** Controls exist to serve exploration; they must not steal the primary visual field during validation or professional use.
  - - **Global map ergonomics:** Users must pan freely near **Pacific/dateline/polar** regions during validation; artificial snap-back is disqualifying for this product class.
  - - **Professionals still need an oracle:** Right-click / precise coordinate inspection is framed as **truth instrumentation**. It must have onboarding (hint, mode toggle), and mobile needs long-press equivalent.
  - ## Typography and popups (professional validation patterns)
  - - **Debug UX must allow rapid re-runs:** disabling buttons after one run blocked validation flows.

### A.129 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 20953; SHA-12: `db53e1e91227`; score: 86
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Engineering signals:
  - **Scope:** Web 2.0 account/chart workflow architecture. Not implementation. Not schema migration.
  - **Purpose:** Stress-test and **propose** a coherent navigation tree, map entry/return paths, screen payloads, active-context rules, and future boxes — ready for canonical adoption after human review.
  - Web 2.0 is a **Chart Record–centric** non-AI product. **Map and Chart Page are co-primary surfaces.** Chart Record utility route, favorites, saved explorations, and comparison are **supporting surfaces** — not a SaaS dashboard home.
  - **Primary ownership unit:** Chart Record (user-facing client / chart / research row).
  - **One user-facing chart per Chart Record.** Event and research charts are **separate Chart Records**, not nested lists.

### A.130 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/00_OPERATOR_START_HERE.md`
- Categories: backend_runtime_and_files, validation_and_rollback
- Characters: 697; SHA-12: `a0e79ddfcf29`; score: 2
- Key headings: AI Onboarding Entry Point
- Engineering signals:
  - - Complete Product Comprehension Gate
  - Understanding must be demonstrated, not claimed.

### A.131 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_EVALUATION_LOG.md`
- Categories: backend_runtime_and_files, validation_and_rollback
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.132 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_WORKFLOW_GOVERNANCE.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 14272; SHA-12: `570f3cca823a`; score: 94
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Engineering signals:
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in writing.
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisible engineering intent: infrastructure, …
  - Every phase closeout must ask whether it introduced or exposed:
  - * missing test, CI, regression, or rollback discipline;
  - * cache invalidation, synchronization, or migration risk;

### A.133 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/KILL_TEST.md`
- Categories: backend_runtime_and_files, validation_and_rollback
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.134 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/PRODUCT_COMPREHENSION_GATE.md`
- Categories: backend_runtime_and_files, validation_and_rollback
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.135 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/ai_drift_audit_framework.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9541; SHA-12: `889f1d9b2f3a`; score: 37
- Key headings: AI drift audit framework; 1. Healthy AI posture (target); 2. Audit dimensions and warning signs; 2.1 Excessive certainty; 2.2 Flattery; 2.3 Manipulative spirituality; 2.4 Optimization obsession; 2.5 Over-helpfulness; 2.6 Premature closure; 2.7 Reducing exploratory play; 2.8 Guru behavior; 2.9 Dependency framing
- Engineering signals:
  - **Purpose:** Catch **comfort bias**, **oracle creep**, and **flattening** before they ship—not after user dependency forms.
  - - A **symbolic translator** and **comparison aide**—structure-forward, biography-light unless user-supplied.
  - - A **GPS recalculator** under constraints—not a prophet, not a therapist replacement, not a spiritual authority.
  - - **Brief by default**, expansive when the user asks—preserving **contemplative space**.
  - - **Subordinate** to popup/line truth and slow doctrine—never contradicting certified point data for comfort.

### A.136 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/anti_cursor_bullshit_governance_rules.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 37
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Engineering signals:
  - # Anti-Cursor Bullshit Governance Rules
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountability_failure_audit.md` §Anti-Bullshit Rules…
  - 3. **rollback path** — how to revert,

### A.137 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/constitutional_ingestion_checklist.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 14
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Engineering signals:
  - Update this document whenever:
  - # Canonical Constitutional Docs
  - # Semi-Canonical / Strategic Docs
  - * and architecture may require rollback.
  - * and long-term symbolic integrity.

### A.138 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/implementation_governance_and_ai_workflow_protocol.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3988; SHA-12: `b127e5c52050`; score: 26
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Engineering signals:
  - This document is CANONICAL.
  - - rollback protocol,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - - speculative patch spirals,

### A.139 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/purification_audit_framework.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 3639; SHA-12: `a43528565790`; score: 18
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Engineering signals:
  - This document is CANONICAL.
  - - and rollback discipline.
  - As the platform evolves,
  - - accumulate hidden assumptions,
  - - or violate constitutional doctrine.

### A.140 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/review_contracts_and_governance.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 12252; SHA-12: `18cc9636738c`; score: 35
- Key headings: Review contracts and governance (implementation layer); 1. What a “review contract” is here; 2. Principles reviewers hold in tension; 3. Implementation review questions; 4. UX review questions; 5. AI behavior review questions; 6. Symbolic integrity review questions; 7. Exploratory and play preservation checks; 8. Anti-chaos visual checks; 9. Anti-guru and anti-coercion checks; 10. Does this preserve contemplative space?; 11. Intelligent exceptions (examples)
- Engineering signals:
  - Contracts are **guardrails**, not formulas. They do not award points for mechanical compliance. A change can satisfy every literal question below and still be wrong in context—or violate one question deliberately for a **documented, rare, intelligent exception**. The reviewer’s job is **directionali…
  - **Doctrine** (meaning, tone, truth hierarchy, interpretive ethics) should evolve **slowly** and with **explicit revision**. **Implementation** (controls, performance, map options, geocoder choice, rendering tactics) may iterate **rapidly**—as long as it **does not contradict** slow doctrine without …
  - ## 2. Principles reviewers hold in tension
  - **Improvisation is preferred when** the risk is low, the change is reversible, the truth stack is unchanged, and the change is **grounded** (metrics, screenshots, validator output, or a short rationale). **Doctrine bends rather than rigidifies when** a rule was written for an older renderer or audie…
  - Use as prompts, not as a gate with a single pass/fail score.

### A.141 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, cache_scheduler_performance, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 110
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Engineering signals:
  - **CANONICAL** for non-AI application UX architecture (Web 2.0 standalone product).
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doctrine.md`, `docs/data…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - Define the complete user journey for the **non-AI relocation platform**.

### A.142 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 67
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Engineering signals:
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Older doctrine and archaeology:** Older docs listed below remain valuable context, evidence, and active companions where not superseded. Treat them as secondary to `docs/constitutional/` on layer sovereignty, forbidden crossings, epistemic humility, runtime/renderer sovereignty, and implementation…
  - **Pacing reminder:** **Philosophy and epistemology evolve slowly** (explicit revision). **Implementation details evolve quickly** (iterate with evidence), but **must not contradict** slow doctrine without updating the doctrine file.
  - These files govern **meaning, agency, fate, tradeoffs, tone, and long-form institutional character**. They are **foundational**. Typical change rate: **rare**; edits should be deliberate, often after architect or governance review.

### A.143 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/README.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 6
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Engineering signals:
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - The system is a layered symbolic intelligence platform, not a monolithic astrology AI, recommendation engine, or chatbot with symbolic flavor.
  - ## Canonical
  - ## Semi-Canonical
  - These documents contain canonical principles plus exploratory or future-facing implementation detail. Treat their core boundaries as binding and their implementation models as revisable.

### A.144 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 80
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Engineering signals:
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - - implementation guidance, component specs, API contracts, or route definitions
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - ### Principle

### A.145 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 201
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Engineering signals:
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.
  - - `docs/ux_principles_and_emotional_tone.md`
  - - **Principle** — binding statement

### A.146 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 35789; SHA-12: `795365723409`; score: 186
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Engineering signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/supabase_schema_sandbo…
  - - what durable records exist,
  - - what belongs on each record,
  - - what must never be persisted as product truth,

### A.147 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 8365; SHA-12: `d1c233003983`; score: 23
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Engineering signals:
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account): symbolic exploration on the map must stay **accountable** to structure.
  - - **Tradeoffs and limitations are real.** The system is designed for users who can hold that **not every relocation yields an unmitigated win.**
  - - **Astrology is not “manifestation culture.”** The product rejects the implication that belief or wording alone reshuffles symbolic structure without cost or constraint.
  - **Product consequence:** Math, overlays, and popups must remain **honest** about membership and relocated facts; interpretive layers must not **contradict** point truth for comfort.

### A.148 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 28
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Engineering signals:
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - - an account management platform
  - - a client record system with a map attached

### A.149 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 33
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`.
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - Chart Record utility (optional route)

### A.150 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, screen_space_and_canonical_substrate, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9566; SHA-12: `3de8663545ba`; score: 29
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Engineering signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - The workflow must remain **fully usable** without Astro Assist, scoring engines, or conversational intake.
  - ## Core workflow principle
  - **Browse, do not oracle.**

### A.151 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, frontend_backend_contract
- Characters: 3360; SHA-12: `554add110fa4`; score: 19
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Engineering signals:
  - This document defines one of the most important distinctions in the platform:
  - Truth belongs primarily to Layer 1.
  - Astrological fact belongs primarily to Layer 2.
  - Interpretation belongs primarily to Layer 3.
  - - coordinate geometry,

### A.152 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/README.md`
- Categories: backend_runtime_and_files, validation_and_rollback
- Characters: 389; SHA-12: `8b67f5632de1`; score: 2
- Key headings: Onboarding Structure
- Engineering signals:
  - 04_ai_validation
  - Comprehension gates, kill tests, onboarding evaluations

### A.153 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/application_screen_inventory_v1.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, frontend_backend_contract, future_infrastructure
- Characters: 17867; SHA-12: `07e2c973e29d`; score: 35
- Key headings: Application Screen Inventory v1; Core Philosophy; Global Product Principles; Primary Product Objects; User; Professional Workspace; Client; Birth Chart; Relocation Search Session; Dashboard will have user's birth chart at the tomp along with name, birth details etc BEAUTIFULLY and tastefull laid out ; Favorite LocationS; Comparison Set
- Engineering signals:
  - * object relationships
  - # Global Product Principles
  - * Professional workflows must remain coherent
  - * Preserve contemplative/premium feeling
  - * User data objects must persist coherently

### A.154 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/MISSING_ONBOARDING_ARTIFACTS.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 7542; SHA-12: `225bf21b32b7`; score: 21
- Key headings: Missing Onboarding Artifacts; Purpose; Important Onboarding Docs That Do Not Yet Exist; Empty Validation Docs / Validation Slots; Missing Comprehension Gates; Missing Kill Test Content; Missing Evaluation Rubrics; Existing Empty / Underpopulated Onboarding Folders
- Engineering signals:
  - This file does not create doctrine and does not define product behavior. It records gaps in the onboarding system.
  - ## Important Onboarding Docs That Do Not Yet Exist
  - | AI validation folder README | `04_ai_validation` needs a short explanation of how comprehension gates, kill tests, drift audits, and review contracts should be used. | `docs/onboarding/04_ai_validation/README.md` |
  - ## Empty Validation Docs / Validation Slots
  - | Product Comprehension Gate template | Repeated chat-based comprehension gates exist, but there is no reusable written evaluation template. | `docs/onboarding/04_ai_validation/PRODUCT_COMPREHENSION_GATE.md` |

### A.155 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/ONBOARDING_CLASSIFICATION_REPORT.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 19329; SHA-12: `87759b54a243`; score: 55
- Key headings: Onboarding Classification Report; Purpose; Exclusions; Destination Folders; Classification Table; Important Excluded Material
- Engineering signals:
  - This report does not create new doctrine. It inventories and classifies existing doctrine, product philosophy, UX philosophy, workflow, AI governance, product training, institutional memory, and onboarding-related documents.
  - The onboarding package intentionally excludes validation reports, smoke tests, renderer experiments, implementation-only documents, phase reports, debugging artifacts, cache architecture, performance investigations, code contracts, payload contracts, and proof artifacts.
  - | `04_ai_validation` | AI behavior checks, evaluation/governance protocols, anti-drift rules, and validation-style review frameworks. |
  - | `docs/constitutional/README.md` | `01_core_authority` | Canonical index for constitutional doctrine categories. | Authoritative constitutional index. | N/A |
  - | `docs/ux/UX_CONSTITUTION.md` | `01_core_authority` | Newest canonical product behavior and UX law document. | Canonical, superseding for UX Truth. | N/A |

### A.156 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/README.md`
- Categories: backend_runtime_and_files, validation_and_rollback
- Characters: 389; SHA-12: `8b67f5632de1`; score: 2
- Key headings: Onboarding Structure
- Engineering signals:
  - 04_ai_validation
  - Comprehension gates, kill tests, onboarding evaluations

### A.157 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/overlay_and_aura_visual_strategy.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, geojson_and_truth_grid, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 22591; SHA-12: `ec6491f35a58`; score: 135
- Key headings: Overlay And Aura Visual Strategy; Separating cusp softness from aspect aura (do not conflate); A. Overlap Philosophy; A.1 Overlap hot zones; B. Child-Color Strategy; C. NOT/Exclusion Visual Language; D. Aura Philosophy; D.0 Aura is occupancy widening from exactness — never blur; D.1 Intensity must be non-linear from edge to centerline; D.2 The other long-standing principles still apply; D.3 Proportional compression; Doctrine: non-certifying field, samples, and adaptation
- Engineering signals:
  - ## Separating cusp softness from aspect aura (do not conflate)
  - Two different physical/semantic ideas must stay **visually and verbally distinct**:
  - | **House cusp transition** | Softens **categorical** house boundary presentation | **~2°** default gradient along cusp | *Astrological cusp softness*—not “uncertainty.” |
  - | **Aspect-to-angle aura** | **Angular** intensification toward exact aspect | Often **~5–8°** (or **aspect-dependent**: e.g. tighter for sextile ~4–5°, wider for conj/opp ~5–8°, user-tunable later) | *Energetic strength toward exactness*—not house category bleed. |
  - **Implementation risk:** reusing the same blur, same ramp curve, or same color for both reads as **one muddy metaphor** and breaks visual epistemology. House fields stay **membership/categorical** (with optional **cusp display** softness); aspect auras stay **orb/intensity** around a **centerline**.…

### A.158 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/process/ai_drift_audit_framework.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, cache_scheduler_performance, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9541; SHA-12: `889f1d9b2f3a`; score: 37
- Key headings: AI drift audit framework; 1. Healthy AI posture (target); 2. Audit dimensions and warning signs; 2.1 Excessive certainty; 2.2 Flattery; 2.3 Manipulative spirituality; 2.4 Optimization obsession; 2.5 Over-helpfulness; 2.6 Premature closure; 2.7 Reducing exploratory play; 2.8 Guru behavior; 2.9 Dependency framing
- Engineering signals:
  - **Purpose:** Catch **comfort bias**, **oracle creep**, and **flattening** before they ship—not after user dependency forms.
  - - A **symbolic translator** and **comparison aide**—structure-forward, biography-light unless user-supplied.
  - - A **GPS recalculator** under constraints—not a prophet, not a therapist replacement, not a spiritual authority.
  - - **Brief by default**, expansive when the user asks—preserving **contemplative space**.
  - - **Subordinate** to popup/line truth and slow doctrine—never contradicting certified point data for comfort.

### A.159 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/process/archaeology_and_synthesis_workflow.md`
- Categories: backend_runtime_and_files, coordinate_calculation_engine, api_endpoints_and_payloads, database_and_persistence, validation_and_rollback, frontend_backend_contract, future_infrastructure
- Characters: 9005; SHA-12: `d3add7674811`; score: 21
- Key headings: Archaeology and synthesis workflow; 1. Pipeline overview; 2. When to create an archaeology pass; 3. When to create or update synthesis docs; 4. Durable truths vs transient implementation; 5. How to avoid flattening nuance during synthesis; 6. Preserving contradictory but valuable tensions; 7. Doctrine canonicalization; 8. Open tension preservation; 9. Institutional memory updating (rhythm); 10. Governance refresh; 11. Review bundle generation
- Engineering signals:
  - **Purpose:** Capture chat and session intelligence **without** flattening nuance, **without** treating the latest thread as law, and **without** losing rejected paths that explain pivots.
  - Raw capture → themed synthesis → doctrine canonicalization → open tension preservation
  - | **Bridge / labels** | `docs/institutional_memory_synthesis.md` | Implemented / roadmap / speculative |
  - | **Canonical doctrine** | `docs/`, `ai_context/core_product_truths.md` | Slow law |
  - | **External audit package** | `docs/review_bundle/` | Snapshot copies + tensions summary |

### A.160 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/process/current_technical_blockers_and_unknowns.md`
- Categories: backend_runtime_and_files
- Characters: 2; SHA-12: `75a11da44c80`; score: 0



---

## Appendix B — Audit Statement

Programmatic pass selected 196 backend/architecture source blocks from 196 total archive blocks. The audit JSON stores matched file names, hashes, headings, engineering signals, category counts, central sources, and source metadata. Final generated word count before this statement: 24038 words.
