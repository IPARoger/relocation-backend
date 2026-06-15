# SYSTEM_BOUNDARIES_AND_CANONS.md

**Status:** Canonical system manual for unbending product canons, mathematical limits, algorithmic boundaries, rendering restrictions, validation gates, AI discipline limits, persistence limits, and structural non-goals.  
**Source archive:** `ALL_PROJECT_DOCUMENTS.txt`  
**Generation method:** deeper three-pass local Python extraction and consolidation.  
**Total archive file blocks parsed:** 196  
**Canon/boundary source blocks matched:** 170  
**Audit hash:** `e5556d03341cef02`

---

## 0. Constitutional Boundary

**Reveal structure. Preserve judgment.**

This is the highest system canon. The platform exposes and tracks spatial geometric data derived from chart conditions. It makes those conditions visible, searchable, inspectable, comparable, saveable, and replayable. It does not own the final evaluation. Interpretation belongs one hundred percent to the interactive human user.

The system may show where a condition holds. It may expose a point popup with local relocated chart truth. It may show an overlap between selected conditions. It may preserve a saved search, a chart record, a favorite location, a comparison set, a settings snapshot, or an export. It may help the user inspect and reason. It must not silently declare a city “best,” infer a life decision, automate astrological judgment, or flatten symbolic tradeoffs into an unreviewed score.

Cities are secondary human markers inside coordinate space. They help users orient, shortlist, save, and compare. They are not the computational starting point. The computational starting point is geographic chart truth: chart inputs evaluated over coordinates, then rendered as inspectable spatial conditions.

---

## 1. Source Scope and Extraction Boundaries

The deeper pass matched files whose headers or bodies contained canon/boundary language: `canon`, `canonical`, `rule`, `constraint`, `strict`, `limit`, `unbending`, `hard constraint`, `non-negotiable`, `must`, `must not`, `never`, `do not`, `forbidden`, `authority`, `doctrine`, `boundary`, `cap`, `threshold`, `orb`, `latitude`, `truth`, `popup`, `validation`, `gate`, `rollback`, `anti-pattern`, `out of scope`, `non-goals`, `deferred`, and related structural terms.

The matched source set spans these boundary categories:

| Category | Matched blocks |
|---|---:|
| ai_and_interpretation_limits | 169 |
| api_and_payload_boundaries | 134 |
| constitutional_product_canons | 117 |
| deferred_and_non_goals | 155 |
| geometry_and_rendering_limits | 139 |
| mathematical_thresholds | 111 |
| persistence_and_cache_limits | 100 |
| ui_and_visual_constraints | 137 |
| validation_and_governance_gates | 134 |

These categories are not independent silos. A rendering limit can also be a product canon. A UI constraint can also protect validation truth. A cache key rule can also protect human trust. This document consolidates them as system boundaries: what must stay true even when implementation changes.

---

## 2. Authority Stack

### 2.1 Implemented reality

Current source code and current validation artifacts define what the system actually does. Implementation truth must be checked before any AI, developer, or document claims behavior. A recent document does not prove shipped implementation. A plausible chat summary does not override the repository. The current running server, active frontend file, endpoint response, and validation reports outrank memory.

### 2.2 Canonical doctrine

Canonical doctrine defines what the system is allowed to become. It can constrain implementation before implementation catches up. If code diverges from doctrine, the project must either fix the code or explicitly amend doctrine. Silent drift is forbidden.

### 2.3 Validation evidence

Validation evidence outranks confidence. Popups, smoke scripts, brute-force walls, screenshot reports, parity scripts, audit JSON, and regression narratives are proof surfaces. “Looks right” is not a pass when the question is geometry, cache correctness, overlay membership, or popup agreement.

### 2.4 Archaeology

Archaeology preserves failed paths and prior thinking. It is not automatically active law. Superseded documents must stay available because they explain why paths were rejected, but they must be labeled so future agents do not backslide.

### 2.5 Roadmap and future inventory

Roadmap ideas do not belong in active instructions. They can be preserved in future excellence inventories. They cannot be described as shipped or required unless promoted through current doctrine.

---

## 3. Product and Interpretation Canons

### 3.1 No automated conclusions

The software must not auto-interpret choices for the user. It can reveal “where,” “what,” and “how close.” It cannot decide “therefore move here.” Any future AI or comparison feature must label interpretation separately from factual chart conditions.

### 3.2 Human judgment remains sovereign

Professional and user judgment outrank machine suggestions. AI may assist discovery, but it cannot override the astrologer, the user’s intention, or the factual map. The product should support professional sovereignty and lay exploration without replacing human evaluation.

### 3.3 Symbolic tradeoffs must not be flattened

Relocation astrology is not a simple benefic/malefic score. A placement may support one intention and complicate another. The system must preserve tradeoffs, not erase them. Favorites, comparisons, and saved searches should avoid default ranking language unless the user explicitly defines optimization criteria.

### 3.4 “Good/bad place” language is structurally unsafe

The platform should avoid implying that a place is objectively good or bad. More accurate language: candidate location, selected overlap, excluded condition, user intention, tradeoff, emphasis, comparison, proximity, or inspectable structure.

### 3.5 Fact versus interpretation boundary

A factual claim says what the chart/geography engine reports. An interpretive claim explains what that might mean. The two must remain visibly separable in UI, exports, notes, AI outputs, onboarding, and comparison pages.

---

## 4. Geometry and Calculation Boundaries

### 4.1 Popup truth is the local authority

Point inspection is the canonical truth for a coordinate. Overlay impressions are exploratory. If an overlay seems to disagree with the popup, the popup and validated engine truth win. Any overlay system must be tested against point truth.

### 4.2 Overlays are where-fields, not final charts

Map overlays show where conditions hold. They are optimized for exploration and comparison. They are not substitutes for a full relocated chart. Dense details belong in chart pages, comparison pages, and inspectable popups.

### 4.3 Canonical truth and display adaptation remain separate

Frontend display geometry may wrap, clip, tile, paint, or simplify for screen display. It may not change underlying chart truth. Styling cannot move membership. Smoothing cannot become computation. Blurs cannot hide uncertainty or disagreement.

### 4.4 Truth-grid over cosmetic contours

The project canon favors honest sampled truth fields over contour smoothing when membership matters. The legacy contour path using Gaussian smoothing and `find_contours` is archaeology where it lies about topology or membership. Truth-grid or screen-space truth substrates are preferred because they preserve inspectability.

### 4.5 Screen-space truth is a paradigm boundary

The canonical screen-space adaptive substrate samples visible pixels and returns masks. Legacy GeoJSON polygons and canonical per-pixel masks are not equivalent data shapes. Migration must not mix them inside one render. Parity must be checked against brute-force truth or popup classification, not shape resemblance.

### 4.6 Centerline and aura separation

An aspect centerline is the exactness spine. Aura or material strip is an intensity language around that spine. Aura does not redefine membership. It communicates proximity to exactness and must remain subordinate to point truth and exact geometry.

### 4.7 House cusp softness and aspect aura are distinct systems

House cusp transition is categorical-boundary softness, often discussed around a small default such as approximately 2 degrees. Aspect aura is orb/intensity space around an exact angular relationship, often discussed in broader aspect-dependent ranges such as roughly 4–8 degrees depending on aspect family and settings. These must not use one muddy metaphor, one shared blur, or one copy language.

### 4.8 High-latitude and polar limits are policy surfaces

High-latitude behavior must not be hidden. Latitude caps, Placidus instability, polar clipping, and advanced-mode exceptions are product-policy boundaries. If a cap is active, overlays must not imply truth beyond the cap without disclosure. If cap is off, the system must not pretend polar behavior is ordinary.

### 4.9 Cities are not the sample grid

City datasets and geocoders are orientation systems. They do not define truth regions. A city may be queried as a point, but global search must not be reduced to city enumeration.

---

## 5. Rendering and Visual Canons

### 5.1 Map readability is a hard constraint

City labels, coastlines, political boundaries, and clickable candidate places must remain readable under overlays. A beautiful overlay that kills map readability fails. This is not polish; it is a truth-access constraint.

### 5.2 Beauty must emerge from truthful systems

Decorative fog, fake glow, ornamental gradients, Gaussian mush, neon spectacle, and “looks right” smoothing are rejected when they obscure or alter truth. Visual quality is welcome after geometry is trustworthy.

### 5.3 Overlap regions are discovery objects

Overlaps are not mere clutter. The user often searches for combinations. The visual system must preserve overlaps as meaningful structures while avoiding paternalistic ranking. Use neutral language such as candidate zone, notable overlap, or high-concentration area.

### 5.4 NOT/exclusion is a semantic polarity

NOT or exclusion conditions should render as quiet deprioritization: desaturation, muted veil, charcoal/redacted language, or low-contrast treatment. They must not become alarm red danger maps. They must not light up the entire allowed world as a positive overlay.

### 5.5 Layer controls are display controls unless explicitly semantic

Mute, solo, send-to-background, and send-to-foreground affect visibility and inspection priority. They must not alter Layer 1 truth. NOT/exclude is different: it is a semantic condition polarity and must be preserved as such.

### 5.6 Debug surfaces stay out of production UX

Debug banners, trace labels, sampling diagnostics, raw status strings, and validation internals must remain behind debug flags or developer surfaces. Production UX must stay calm, premium, and inspectable.

### 5.7 Palette is not proof

Current colors may validate overlap math and occupancy logic. They are not final brand language. Engineering validation of color visibility does not equal product palette approval.

---

## 6. Payload, Snapshot, and State Boundaries

### 6.1 Render snapshot immutability

The primary search action emits an immutable render payload. Save Search, Pin, history, replay, share, and export must refer to that rendered snapshot, not mutable live card state. Re-render creates a new snapshot.

### 6.2 Stable IDs outrank display labels

Type IDs, registry IDs, and payload field names are canonical. Display labels are swappable through language registries. The engine must not derive truth from button copy, visual strings, or beta wording.

### 6.3 Modular variable cards replace fixed A/B/C truth

Each variable card represents one semantic condition. Legacy A/B/C adapter limits may exist temporarily, but canonical `variables[]` is truth. Overflow must not be silently dropped; degradation metadata is required where adapter limits truncate representation.

### 6.4 NOT remains inside canonical variables

Exclude variables remain canonical variables with `polarity: "exclude"`. They must not be transformed into a separate fake variable family unless a doctrine amendment changes the schema.

### 6.5 Incomplete input must not render truth

Search Map or equivalent primary action should be disabled while required condition cards are incomplete. Add Variable may be blocked until existing cards are complete. The user should not generate ambiguous or half-formed search truth.

### 6.6 Chart context owns saved objects

Favorites, saved searches, history, saved explorations, comparisons, and notes belong to a chart record or client/chart context. Active chart context must not silently change under the map. Saved objects must remain replayable with the correct chart identity and settings snapshot.

### 6.7 Renderer internals are not semantic saved objects

Saved investigations store semantic conditions, chart context, viewport, settings snapshot, and replay information. They should not store arbitrary renderer internals as product truth unless explicitly marked as debug metadata.

---

## 7. Cache and Performance Boundaries

### 7.1 Cache cannot cross truth contexts

A cache key must include every parameter that affects output: chart identity, bounds, zoom, block size or resolution, selected conditions, substrate, latitude-cap policy, settings snapshot, and relevant renderer parameters. If a parameter changes truth or display membership, it belongs in the key or invalidation contract.

### 7.2 Cache is not proof of current computation

A cached correct result can hide current-code breakage. A stale cache can make correct code appear wrong. Cache validation must be separate from computation validation.

### 7.3 Substrate flags must not flip mid-session invisibly

Substrate migration requires deterministic operator-visible state. A page load may choose legacy or canonical. A single visible overlay must not mix substrates. Auto-fallback is forbidden because it masks regressions.

### 7.4 User action outranks background work

Schedulers and cache warmups must stop for user requests. The product should serve the user’s current exploration first. Background caching can resume only after active requests are handled.

### 7.5 Performance optimization follows truth wall

First define brute-force or high-confidence truth. Then optimize. Do not optimize before the wall exists. Do not reduce sample density for speed before convergence and popup agreement are measured.

---

## 8. Validation and Governance Boundaries

### 8.1 Every meaningful change needs a gate

A serious change requires hypothesis, controlled test, pass/fail criterion, evidence artifact, and rollback route. If a change cannot define its gate, it is not ready.

### 8.2 Smoke tests are project infrastructure

Smoke scripts prevent stale-server, wrong-file, endpoint, cache, and regression errors. They should remain small, repeatable, and focused. They do not need to be fancy; they need to catch drift.

### 8.3 Brute-force wall remains the referee

Dense truth sampling is the reference wall. It may be too expensive for production but is essential for proving whether adaptive methods lie. Deleting the wall requires explicit doctrine change and is strongly disfavored.

### 8.4 Regression artifacts must be retained

Validation reports, screenshot baselines, comparison narratives, and audit outputs are first-class assets. They keep future AI sessions from redoing or misremembering work.

### 8.5 Rollback is mandatory

Risky changes need a rollback path. Renderer migration, cache integration, database changes, schema changes, and major UX state changes must be reversible. No hidden migrations. No broad unscoped staging.

### 8.6 One instability source at a time

Do not debug math, styling, cache, browser state, and backend endpoints in the same change. Isolate the failure class before editing. Repeated AI failures often came from mixing categories.

---

## 9. AI and Machine Boundaries

### 9.1 AI cannot be system authority

AI helps read, draft, review, and suggest. It does not determine truth, merge safety, product ethics, or final interpretation. Repository truth and validation evidence outrank AI confidence.

### 9.2 Development AI must state knowns and unknowns

For technical work, AI must identify known facts, unknowns, files involved, smallest change, validation method, rollback path, and rejected scope. Fake confidence is a system risk.

### 9.3 No hallucinated architecture

AI must not invent endpoints, schemas, tables, caches, or UI behavior that are not in source or explicitly proposed. It must label draft vs verified canon.

### 9.4 No comfort-spun interpretation

Future AI interpretation must preserve symbolic integrity. Difficult placements remain difficult. Tradeoffs remain tradeoffs. AI may contextualize and strategize; it must not rewrite structure to flatter.

### 9.5 No hidden ranking

AI must not create hidden “best city” ranking unless the user explicitly asks for ranking under declared criteria and the output is clearly labeled as interpretive assistance.

---

## 10. Persistence, Database, and Account Boundaries

### 10.1 Product data objects must remain coherent

User, professional workspace, client, chart record, saved location, saved search, comparison set, notes, and shared view are distinct objects. They must not collapse into one giant blob of UI state.

### 10.2 Local JSON is not permanent product storage by accident

Temporary local files and sandbox persistence must not become permanent architecture. Production storage requires explicit schema, ownership, permissions, replay contracts, and migration strategy.

### 10.3 Settings snapshots protect replay honesty

Saved searches and rendered investigations require settings snapshots. Future changes to defaults must not rewrite the meaning of old saved explorations.

### 10.4 Shared/client views are curated presentations

Shared views should expose selected overlays and limited exploration controls. Clients should not silently mutate professional-selected conditions unless the sharing model explicitly permits it.

---

## 11. Active Non-Goals

The active system boundaries exclude: automatic city optimization, full consumer AI oracle mode, hidden scoring engines, Web3 governance, social feeds, telemetry infrastructure, feature-flag services, broad AI agent autonomy, production rain/virga animation, final style preset system, premature map-library migration, persistent overlay caches, CDN chart tiles, formal enterprise regulatory apparatus, and multi-agent orchestration. These remain future inventory items unless explicitly promoted.

---

## 12. Merge and Change Checklist

Before accepting a change, ask:

1. Does it preserve Reveal structure / Preserve judgment?
2. Does it preserve human interpretation authority?
3. Does it keep cities secondary to geographic truth?
4. Does it preserve popup truth?
5. Does it separate overlay exploration from point inspection?
6. Does it avoid hidden ranking or auto-interpretation?
7. Does it avoid conflating cusp softness with aspect aura?
8. Does it preserve map readability?
9. Does it preserve Layer 1 truth versus display controls?
10. Does it keep debug surfaces out of production UX?
11. Does it preserve render snapshot immutability?
12. Does it avoid silent adapter overflow?
13. Does it include cache keys or invalidation for every truth parameter?
14. Does it include validation evidence or state validation pending?
15. Does it include rollback?
16. Does it avoid broad unrelated changes?
17. Does it avoid resurrecting superseded archaeology?
18. Does it state unknowns plainly?
19. Does it update doctrine if doctrine changed?
20. Does it belong in active instructions rather than future inventory?

---

## Future Structural Excellence Inventory

This inventory preserves structural opportunities without making them active instructions.

### Geometry and rendering

- Canonical screen-space substrate default after validated migration.
- Aspect overlay migration to canonical substrate after house overlays stabilize.
- Aura/material-strip refinement based on validated exactness fields.
- Cusp-gradient prototype with explicit fact/softness copy.
- Unified sampler strategy for house, angle-sign, aspect, and aura families.
- High-latitude policy finalization with advanced override wording.

### Cache and performance

- Production Phase-C cache integration after substrate path settles.
- Cache drainage, storm, chart-change, and substrate-flip smoke expansion.
- Adaptive refinement thresholds by viewport class.
- Future cache persistence only after invalidation and privacy contracts exist.
- Warmup priority tuning only after measured need.

### Validation

- Golden screenshot CI.
- Popup-overlay parity harness expansion.
- Brute-force wall fixture registry.
- Edge-case dossier for dateline, polar, high-north, dense city, and cusp-heavy charts.
- Automated doctrine drift checks.

### Data and persistence

- Supabase or database schema promotion only after local object model is stable.
- Saved investigation replay contracts.
- Shared-view permission model.
- Chart-record ownership enforcement.
- Settings snapshot versioning.

### Interface and controls

- Genie/drawer production component.
- LayerDisplayState, DrawerLayoutState, and ConditionDirtyFlag abstractions.
- NOT/exclusion display refinement.
- Mobile bottom-sheet pattern.
- City label and geocoder density strategy.

### AI and governance

- AI reviewer prompt packs.
- Prompt compliance audits.
- Anti-hallucination evaluation sets.
- Future AI interpretation policies with fact/interpretation labeling.
- Human-review gates for client-facing generated interpretation.



---

## Appendix A — System Canon Source Index

### A.1 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/AI_WORKFLOW_GOVERNANCE.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 14272; SHA-12: `570f3cca823a`; score: 118
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Requirement signals:
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in writing.
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisible engineering inte…
  - ## Ghost Boss Governance Doctrine
  - The Ghost Boss is the invisible engineering conscience for the project. It does not block visible product work by default; it preserves the hidden work that makes visible product promises trustworthy.
  - Every phase closeout must ask whether it introduced or exposed:

### A.2 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/CURRENT_RENDERING_DOCTRINE.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7576; SHA-12: `0b4a58929157`; score: 68
- Key headings: Current Rendering Doctrine — Summary; The stack (top to bottom); Non-negotiables; Legacy `/search-regions` Truth Grid; Phase-2 cache (product substrate); Evidence bundle (read in this order); Documents marked SUPERSEDED (archaeology preserved); Warnings against backsliding; Remaining gaps (structural, not aesthetic); Recommendation
- Requirement signals:
  - # Current Rendering Doctrine — Summary
  - > **Status:** Canonical orientation page (fast to read).
  - > **Authority:** `docs/relocation_map_architecture.md` wins on conflict.
  - | **Brute force** | Validation wall. Every optimisation must match it cell-for-cell (or pixel-for-pixel on screen). | Canonical control specimen |
  - | **Screen-space truth** | Production sampling axis for **visible overlays**. Classify what the user actually sees. | Canonical for rendering |

### A.3 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DEFERRED_EXCELLENCE_REGISTRY.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 30563; SHA-12: `8fdc70fc996d`; score: 245
- Key headings: Deferred Excellence Registry; Purpose; Cross-Cutting Doctrine; Status Legend; 1. Renderer / Topology Improvements; 1.1 Stable component IDs across zoom/pan; 1.2 Graph / global path solver; 1.3 Canonical-default migration; 1.4 Continuous topology extraction refinement; 1.5 Subpixel/edge extraction refinement for narrow-orb ASC; 1.6 Seam-aware topology continuity; 1.7 Signed-distance-field experiments
- Requirement signals:
  - # Deferred Excellence Registry
  - This registry captures everything we know we *could* improve in the renderer, architecture, UX, product, and reliability stack — and have intentionally deferred to protect MVP velocity. Its primary purpose is **not** to accumulate shiny feature ideas. Features are comparatively e…
  - The primary purpose is preserving hidden robustness and institutional memory: invisible infrastructure improvements, architecture refinements, reliability upgrades, governance ideas, performance optimizations, renderer trust improvements, scaling concerns, cache/system improvemen…
  - These are the things founders and AI systems tend to forget because users do not directly see them, they do not demo well, short-term success can mask their absence, and commercial pressure naturally favors visible product work. The registry exists to preserve long-term engineeri…
  - Short rule: when choosing what to capture here, prefer invisible engineering and infrastructure concerns over visible feature wishes. Feature wishes may be listed when they carry trust, platform, or operational consequences, but the registry's center of gravity is hidden robustne…

### A.4 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DOCTRINE_INDEX.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 101
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Requirement signals:
  - # Doctrine index
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…
  - **Older doctrine and archaeology:** Older docs listed below remain valuable context, evidence, and active companions where not superseded. Treat them as secondary to `docs/constitutional/` on layer sovereignty, forbidden crossings, epistemic humility, runtime/renderer sovereignty…

### A.5 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/EXECUTIVE_TRANSFER_BRIEF_NEXT_CHAT.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9792; SHA-12: `d91200d72161`; score: 85
- Key headings: Executive Transfer Brief For Next Chat; 1. Current Project State; 2. What Is Considered Solved; 3. What Is Intentionally Deferred; 4. Current Renderer Status; 4.1 Renderer handoff state; 5. Governance Status; 6. Productization Status; 7. Immediate Next Recommended Phases; 8. Strategic Warnings; 9. Key Philosophical Doctrines; 10. How Future AI Should Behave
- Requirement signals:
  - - Screen-space truth and adaptive refinement have proven the future truth substrate.
  - - Brute-force wall validation exists as the reference method.
  - - Renderer readiness gate explicitly unblocked product scaffolding.
  - - Governance artifacts, continuity volumes, and deferred-excellence tracking are now project infrastructure.
  - ## 3. What Is Intentionally Deferred

### A.6 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_1_2_EXTRACTION_AUDIT.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 31222; SHA-12: `99e7cbcf42db`; score: 256
- Key headings: Phase 1.2 Extraction Audit; Concise Findings; Files Inspected; Production and backend; Sandboxes; Validation / capture scripts; Doctrine used as constraints; Current Rendering Entry Points; Production renderer; Backend endpoints; Sandbox renderers; Validation harnesses and capture scripts
- Requirement signals:
  - > **Authority:** Follows `docs/PHASE_C_IMPLEMENTATION_PROTOCOL.md`,
  - > **Non-goals:** No production renderer mutation. No cache rewrite. No
  - safe extraction boundaries, and rollback checkpoints before Phase 1.2
  - must not change behavior and must not mix the legacy production overlay
  - with the canonical screen-space substrate.

### A.7 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 58355; SHA-12: `c6ef18d0c316`; score: 289
- Key headings: Phase-2 Cache Integration — Architecture & Implementation Planning; 0. Where this fits; 1. Grounding — what is true today, measured; 1.1 Sandbox state (measured, not asserted); 1.2 What this means; 1.3 Hard architectural finding — substrate mismatch; 2. Production Scheduler Architecture; 2.1 Single-active-job model; 2.2 Foreground vs background queues; 2.3 Cancellation / interruption behaviour; 2.4 Priority escalation rules; 2.5 Viewport ownership
- Requirement signals:
  - > **Status:** Architecture and planning doctrine. Design only. No code
  - > **Authority:** `docs/relocation_map_architecture.md` (§ "Phase 2 cache
  - > **Companion:** `validation/narratives/phase2_cache_implementation.md`
  - > **Stability:** Slow. Implementation details may rev; design rules here
  - > **Non-goals:** No aura styling. No aesthetic rendering changes. No

### A.8 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_IMPLEMENTATION_PROTOCOL.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 54962; SHA-12: `c32fcebbd584`; score: 419
- Key headings: Phase-C Implementation Protocol; Operational constitution for landing the validated architecture without future chaos; 0. Where this fits; 1. Implementation Phase Breakdown; Phase 1.1 — Documentation alignment (no code); Phase 1.2 — Archaeology fencing (low-risk cleanup); Phase 1.3 — Scheduler extraction (no behaviour change); Phase 1.4 — Substrate adapter scaffold (legacy-only); Phase 1.5 — Canonical substrate wiring (flag-gated); Phase 1.6 — Scheduler/cache wiring on canonical (flag-gated); Phase 1.7 — Parity validation harnesses; Phase 1.8 — Default flip + stabilisation
- Requirement signals:
  - > **Status:** Operational doctrine. Implementation planning only.
  - > **Authority on conflict:** `docs/relocation_map_architecture.md`,
  - > meta-governance cycle. Does not override slow doctrine.
  - > **Non-goals:** Aura aesthetics. Animation. Renderer rewrite. New
  - with — never duplicates — the existing meta-governance docs. Where

### A.9 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_PRODUCTION_MIGRATION_PLAN.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 64644; SHA-12: `af96b1d10c2e`; score: 646
- Key headings: Phase-C Production Migration Plan; Legacy overlay pipeline → canonical screen-space adaptive substrate; 0. Where this fits; 1. Legacy vs Canonical Substrate Audit; 1.1 The legacy overlay pipeline (what is in production today); 1.2 The canonical screen-space substrate (validated, sandbox-proven); 1.3 Semantic differences; 1.4 Rendering differences (visible); 1.5 Cache compatibility implications; 1.6 Validation differences; 1.7 Hidden assumptions; 1.8 Likely regression risks (ranked)
- Requirement signals:
  - ## Legacy overlay pipeline → canonical screen-space adaptive substrate
  - > **Status:** Migration architecture and planning doctrine. Design
  - > **Authority on conflict:** `docs/relocation_map_architecture.md`,
  - > **Non-goals:** No aura styling. No aesthetic rendering changes. No
  - validated screen-space adaptive substrate (`/screen-pixel-truth`).

### A.10 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_RENDERING_ARCHITECTURE.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 47288; SHA-12: `3744bf667647`; score: 328
- Key headings: Phase C — Rendering Substrate Architecture (Governing Laws); 0. Where this document sits; 1. Canonical Rendering Truths; 1.1 The four absolute statements; 1.2 Screen-space truth doctrine; 1.3 Adaptive refinement as production substrate; 1.4 Why visible output is canonical; 1.5 Globe truth vs screen truth; 2. Convergence Strategy; 2.1 Convergence is the contract; sample count is not; 2.2 Targeted escalation, never global slowdown; 2.3 Refinement economy — *truth where unstable*
- Requirement signals:
  - > **Authority:** `docs/relocation_map_architecture.md` wins on direct conflict.
  - > **Adopted draft:** 2026-05-21 (same-day as the rendering doctrine reset).
  - > **Stability:** Slow. Implementation details around this doctrine may rev;
  - | Orientation | `docs/CURRENT_RENDERING_DOCTRINE.md` | One-page “where we are now” |
  - | Foundational architecture | `docs/relocation_map_architecture.md` | Immediate-truth + opportunistic-expansion |

### A.11 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PROJECT_CONTINUITY_INDEX.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 2667; SHA-12: `303dae8aa89c`; score: 36
- Key headings: Project Continuity Index; Canonical Governance Docs; Canonical Archaeology Docs; Canonical Renderer Doctrine Docs; Deferred Excellence; Validation Narratives; Continuity Volume Convention; Recommended Future-AI Ingestion Order
- Requirement signals:
  - Purpose: short entry point for future AI/human rehydration. This file points to canonical governance, archaeology, renderer, deferred-excellence, and validation memory without replacing those sources.
  - ## Canonical Governance Docs
  - - `validation/narratives/renderer_readiness_decision_gate.md` — Phase 1.19 blocker taxonomy and anti-death-spiral doctrine.
  - ## Canonical Archaeology Docs
  - - `ai_context/archaeology/RAW_CONTINUITY_VOLUME_7.md` — canonical continuity volume container for this phase.

### A.12 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 93
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Requirement signals:
  - # AI Interpretation Truthfulness Doctrine v1
  - **CANONICAL** for **future** AI-assisted interpretation layers — not current product scope.
  - **Scope:** Documentation only. Defines interpretive discipline, forbidden patterns, and a future review architecture. **No AI implementation in dumb Web 2.0 v1.**
  - - `docs/constitutional/truth_vs_astrological_fact_vs_interpretation.md` — Layer 1 / 2 / 3 separation
  - - `docs/constitutional/professional_trust_and_ai_behavior_doctrine.md` — propose vs declare, layer sovereignty

### A.13 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai_constitution_and_review_architecture.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 13119; SHA-12: `d6ae8f16c65e`; score: 71
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Requirement signals:
  - **Status:** Internal **governance architecture** for future AI-assisted interpretation—not a shipping spec, not marketing, not ethics theater.
  - **Doctrine stack (read before changing AI behavior):**
  - - **`docs/intentionality_and_symbolic_constraints.md`** — fate/agency, tradeoffs, intentionality, AI governance implications.
  - - **`ai_context/core_product_truths.md`** — epistemic truth, interpretive integrity, tradeoff intelligence, professional-first stance.
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account); what software is allowed to **claim** at each surface.

### A.14 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/client_chart_data_model_v1_2026-05-29.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 35789; SHA-12: `795365723409`; score: 153
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Requirement signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Scope:** Entity model, persistence boundaries, saved exploration shape, active context, and optional post-v1 behavioral capture — **documentation only**. Not SQL. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,

### A.15 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 20953; SHA-12: `db53e1e91227`; score: 82
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Requirement signals:
  - **ARCHITECTURE REVIEW — aligned with Map-First Product Doctrine (2026-05-31)**
  - **Date:** 2026-05-29 (original); **doctrine alignment:** 2026-05-31
  - **Governing doctrine:** `docs/constitutional/map_first_product_doctrine_v1.md` — supersedes dashboard-centric recommendations in v1.0–v1.1 of this review.
  - - `docs/architecture/client_chart_data_model_v1_2026-05-29.md` (data ownership authority)
  - - `docs/ux/2026-05-29_application_journey_architecture_v1.md` (screen/journey authority)

### A.16 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/aspect_aura_defaults.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, deferred_and_non_goals
- Characters: 1291; SHA-12: `2e467a76fee6`; score: 10
- Key headings: Aspect aura defaults (approximate display); Authority; Default screen weights (Leaflet `weight`, approximate); NOT done here
- Requirement signals:
  - # Aspect aura defaults (approximate display)
  - ## Authority
  - - **Popup** / API chart: exact longitudes and derived angles.
  - ## Default screen weights (Leaflet `weight`, approximate)
  - **Exact lines** still use API `weight` / `opacity` (MC ~4×95% opacity; contour angles ~2×100% in current defaults).

### A.17 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/brand_and_experience_foundations.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ui_and_visual_constraints, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 44
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Requirement signals:
  - **Important:** The emotional and atmospheric goals below are **experiential design constraints**—they govern how future UX and rendering choices should **feel** and **function**. They are **not** marketing fluff; they are institutional memory for product judgment.
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).
  - - **Pre-verbal / symbolic language:** Where possible, meaning is carried **through encodings**—overlay semantics, gradients, aura, softness, restraint, popup hierarchy—as a **language without words**, aligned with `docs/visual_semantic_style_guide.md`.
  - - **Fantasy with honesty:** The atmosphere supports **fantasy and exploration** while the system remains **epistemically honest** (popup vs overlay vs account truth hierarchy unchanged).
  - - **Beauty from truthful systems:** Beauty should **emerge** from **honest interaction and encoding**, not from **decorative** layers glued on top.

### A.18 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/cartographic_language_and_city_rendering.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 18608; SHA-12: `33b4db97eb55`; score: 83
- Key headings: Cartographic language and city rendering; 0. Basemap or tile strategy change ⇒ full visual identity re-test; 1. Map label language vs app language; 2. Provider evaluation (map + search); 2.1 Dimensions to score (required for any serious comparison); 2.2 Qualitative stack comparison (high level); 2.3 “Extra hour” vs “multi-day / multi-week”; 2.4 Effort bands for “whole solution” slices; 2.5 GeoNames bridge first vs “long-term now”; 3. City visibility under overlays (hard constraint); 4. City density and ranking (rendering); 5. Clickability: city vs blank map
- Requirement signals:
  - **Status:** Planning and constraints for **basemap language**, **city visibility**, and **interaction clarity**. Complements `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, and `docs/map_and_overlay_design_research.md`.
  - **Out of scope:** Aspect-to-angle **glow/aura** (not implemented; do not conflate with city-layer work).
  - **Institutional rule:** If the team changes **map provider**, **tile format** (raster → vector, host swap, style swap), or **label policy**, we must **re-validate the whole visual system**—not assume the current look “carries over.”
  - | **Popup contrast** | Popup chrome assumed light-gray UI; dark basemap or dark mode may need **two token sets** (`map_and_overlay_design_research.md` §8). |
  - | **Light / dark theme** | **Do not** assume one overlay palette works; plan **paired tokens** when dark mode is real. |

### A.19 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/README.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 30
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - truth integrity,
  - - conversational interpretation,
  - # Doctrine Categories

### A.20 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ai_conversational_modes.md`
- Categories: api_and_payload_boundaries, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 2887; SHA-12: `b796e2065486`; score: 18
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Requirement signals:
  - - canonical architectural principles,
  - - and deferred implementation ideas.
  - - constraints become clearer,
  - # Core Principle
  - The AI should adapt conversational style without violating constitutional doctrine.

### A.21 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/constitutional_ingestion_checklist.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 20
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Requirement signals:
  - - track doctrine ingestion,
  - Update this document whenever:
  - - doctrine evolves,
  - This project contains multiple categories of doctrine:
  - - AI behavior doctrine,

### A.22 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/future_excellence_vs_future_feature_excellence.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 20
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Requirement signals:
  - - canonical architectural principles,
  - # Core Principle
  - ## Infrastructure excellence and feature excellence must remain distinct.
  - - support future capabilities safely,
  - - rollback safety,

### A.23 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/implementation_governance_and_ai_workflow_protocol.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3988; SHA-12: `b127e5c52050`; score: 26
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Requirement signals:
  - This document is CANONICAL.
  - - rollback protocol,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - - rollback-safe,

### A.24 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer4_optimization_and_exploration_doctrine.md`
- Categories: api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 4341; SHA-12: `289b4552320f`; score: 13
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Requirement signals:
  - # Layer 4 Optimization And Exploration Doctrine
  - - canonical Layer 4 principles,
  - Core Layer 4 boundaries are canonical.
  - # Core Principle
  - # Important Constraint

### A.25 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer_sovereignty_and_forbidden_crossings.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ai_and_interpretation_limits
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 50
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Requirement signals:
  - # Layer Sovereignty And Forbidden Crossings
  - This document is CANONICAL.
  - These rules are mandatory architectural constraints.
  - - forbidden crossings,
  - # Core Principle

### A.26 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layered_symbolic_intelligence_architecture.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 4801; SHA-12: `5242de0598f3`; score: 23
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Requirement signals:
  - This document is CANONICAL.
  - All future systems must respect:
  - - forbidden crossings,
  - - and truth integrity.
  - - preserve truth integrity,

### A.27 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/map_first_product_doctrine_v1.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 41
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Requirement signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - Both are **primary surfaces**. The Chart Page must not become an afterthought.

### A.28 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 27
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Requirement signals:
  - - canonical architectural principles,
  - - and deferred implementation ideas.
  - - constraints become clearer,
  - # Core Principle
  - Truth computation must remain independent from symbolic interpretation systems.

### A.29 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_mode_vs_lay_mode_strategy.md`
- Categories: mathematical_thresholds, api_and_payload_boundaries, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3492; SHA-12: `c166907d611f`; score: 18
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Requirement signals:
  - Core principles are canonical.
  - # Core Principle
  - The system must avoid:
  - - oversimplifying truth,
  - - raw truth visibility,

### A.30 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_trust_and_ai_behavior_doctrine.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 32
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Requirement signals:
  - # Professional Trust And AI Behavior Doctrine
  - This document defines how AI systems inside the platform must behave.
  - The AI must never behave like:
  - # Core Principle
  - This principle is absolute.

### A.31 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/purification_audit_framework.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3639; SHA-12: `a43528565790`; score: 34
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Requirement signals:
  - This document is CANONICAL.
  - - and rollback discipline.
  - - or violate constitutional doctrine.
  - # Core Principle
  - - Has interpretation contaminated truth?

### A.32 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_and_renderer_sovereignty.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits
- Characters: 3826; SHA-12: `edda50b52a22`; score: 46
- Key headings: Runtime And Renderer Sovereignty; Purpose; Core Principle; Rendering must never alter truth.; Runtime Sovereignty; Renderer Sovereignty; Hydration Boundaries; Sandbox Boundaries; Observer Limitations; Renderer Substrate Integrity; Progressive Refinement; Ambiguity And Implication
- Requirement signals:
  - - and observer limitations.
  - - rollbackability,
  - # Core Principle
  - ## Rendering must never alter truth.
  - They do not compute symbolic reality.

### A.33 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, ai_and_interpretation_limits
- Characters: 3360; SHA-12: `554add110fa4`; score: 23
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Requirement signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - Truth belongs primarily to Layer 1.
  - ## Interpretation
  - Interpretation belongs primarily to Layer 3.

### A.34 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_app_shell_handoff_audit_v1_2026-05-30.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits
- Characters: 16528; SHA-12: `a7754235e25c`; score: 43
- Key headings: Genie → App Shell Handoff Audit v1; Status; Executive summary; A. Current Genie contract; Emitter; Trigger; Payload shape (as implemented); Variable semantics (canonical); Output destinations today; Not emitted / not connected; B. Current app shell contract; Navigation context (in-app)
- Requirement signals:
  - **Scope:** What Genie emits today, what app shell and map expect today, and what adapter/transport is required to connect them.
  - **Three distinct states (do not conflate):**
  - Map **default user path** still uses legacy DOM (Find regions). App shell handoff is **receive-only context** — no Genie payload.
  - There is **zero wired handoff** between Genie and app shell, or between shell navigation and automatic Genie search on map load. `legacyCompatibility` is emitted for diagnostics; map engine adapter **must not** use it as execution input.
  - "canonicalVariableCount": 0,

### A.35 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_render_payload_v1_2026-05-30.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 27674; SHA-12: `7e997018eed9`; score: 115
- Key headings: Genie Render Payload Contract v1; Status; Purpose; Architectural doctrine; Language stability doctrine; Principles; Therefore; Top-level payload; Field notes; Render immutability; Future references (not defined here); Variable object
- Requirement signals:
  - **CANONICAL** for the payload emitted when the Genie user presses **Search Map** (render / search submit).
  - **Scope:** Documentation / contract only. Defines shape, semantics, legacy adapter rules, and examples. Not implementation.
  - Define the **canonical, immutable snapshot** produced at Genie render time. This payload is the **search truth** handed to the map workspace, history, pin, and (later) save flows.
  - The Genie editor may hold **live, mutable card state**. Render freezes that state once. Downstream systems must treat the rendered payload as authoritative for “what was searched,” not the live card DOM.
  - # Architectural doctrine

### A.36 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/variable_card_language_v1_2026-05-30.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 15184; SHA-12: `bde701502163`; score: 56
- Key headings: Variable Card Language Contract v1; Status; Purpose; Core doctrine; Canonical internal type IDs; Language registry concept; Composition rule; Registry ownership; Snapshot rule (Saved Explorations); Beta display label candidates; `planet_in_house`; `angle_in_sign`
- Requirement signals:
  - **CANONICAL** for Genie variable-card **user-facing language** — labels, shorthand, dropdown copy, and presentation tokens.
  - - `docs/contracts/genie_render_payload_v1_2026-05-30.md` — stable type ids, `variables[].label` snapshots, language stability doctrine
  - # Core doctrine
  - | Principle | Meaning |
  - | **Stable IDs are canonical** | `planet_in_house`, registry ids (`sun`, `ASC`, `trine`), and payload fields are the source of truth — never derived from display strings. |

### A.37 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/local_first_data_objects_v1.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 8758; SHA-12: `90256838acac`; score: 54
- Key headings: Local-First Data Objects v1; Status; Purpose; Architectural boundary; Entity glossary; ProfessionalAccount; Client; BirthProfile; RelocatedChart (future durable object); Place; FavoriteCity; OverlayCondition
- Requirement signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **product-layer entities**, **persistence boundaries**, and **local-first scaffold rules**. Not a database schema. Not implementation.
  - - renderer output becoming durable truth,
  - │  investigation intent + viewport scope → sampled truth    │
  - │  RENDERER / DISPLAY (never persisted as truth)            │

### A.38 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/supabase_schema_sandbox_plan_v1.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 16155; SHA-12: `8fac31540a5b`; score: 59
- Key headings: Supabase Schema Sandbox Plan v1; Status; Explicit non-goals (current phase); Architectural boundary; 1. Proposed table list; 2. Columns per table; `professional_accounts`; `clients`; `birth_profiles`; `places`; `saved_charts`; `saved_investigations`
- Requirement signals:
  - **Reads with:** `docs/data_model/local_first_data_objects_v1.md`, `docs/future/birth_time_uncertainty_and_confidence_doctrine.md`, `validation/narratives/phase2_3_saved_investigation_replay.md`, `library/library.json` (legacy scaffold).
  - ## Explicit non-goals (current phase)
  - │  RENDERER / DISPLAY (never persisted as truth)          │
  - | 10 | `user_settings` | Account-level Layer 2 defaults (1:1 with account) |
  - | `schema_version` | `smallint` NOT NULL DEFAULT 1 | |

### A.39 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/design/brand_visual_language_and_design_doctrine.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 47
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Requirement signals:
  - # Brand, Visual Language, and Design Doctrine
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - | **Fantasy** | Allowed in user meaning-making; forbidden in fake certainty |
  - ## Visual epistemology (truth hierarchy)

### A.40 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 42
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Requirement signals:
  - # Birth Time Uncertainty and Confidence Doctrine
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `validation/narratives…
  - - AI intake may help later — **MVP must handle tiers without AI**.
  - ## Core principle

### A.41 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/layer5_experiential_education_through_travel_v1.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 34
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Requirement signals:
  - **Dependency:** Requires mature AI guidance, relocation exploration substrate, and user observation capture — **after** standalone Web 2.0 facts-first product is proven.
  - **Reads with (boundary context only):** `docs/ux/2026-05-29_application_journey_architecture_v1.md` §Future Rooms, `docs/constitutional/layer_sovereignty_and_forbidden_crossings.md`.
  - **Must not be read as:** screen spec, sprint backlog, course marketplace brief, or Layer 1–3 implementation requirement.
  - | Notice what changed when you relocated or slowed down | Memorize rules without location context |
  - Reading may support the journey — glossaries, brief context, safety notes — but **reading is never the main pedagogical engine**. The main engine is **lived geographic comparison** grounded in the same factual substrate the professional instrument provides.

### A.42 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_and_city_identity_strategy.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 22
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Requirement signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - **Related:** `memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `docs/geocoder_dataset_feasibility.md`, `docs/cartographic_language_and_city_rendering.md` (basemap change ⇒ **§0** full visual re-test), `docs/relocation_app_product_roadmap.md` §7–8, `docs/m…
  - **Out of scope here:** Aspect-to-angle **glow/aura** visualization (not implemented; separate docs).
  - ## 1. Doctrine: city search is core systems engineering
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`). The map binds **h…

### A.43 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_dataset_feasibility.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 16429; SHA-12: `6ba544bcfafd`; score: 29
- Key headings: Geocoder dataset feasibility (planning pass); 1. Summary recommendation; 2. Option-by-option evaluation; 2.1 GeoNames — `cities500` / `cities1000` / `allCountries`; 2.2 Natural Earth — populated places (`ne_10m_populated_places`); 2.3 Who’s On First (WOF); 2.4 Pelias / Geocode Earth (open-data stack vs hosted); 2.5 Mapbox / Google (hosted geocoding & Places); 3. Licensing notes (high level — verify before ship); 4. Rough import plan (GeoNames-first); 5. Data fields needed (canonical `Place` record); 6. Proposed ranking formula (v1 — heuristic, explainable)
- Requirement signals:
  - **Non-goals here:** Astrology/math/overlay changes; shipping a full geocoder integration; vendor contracts.
  - **Companion docs:** `docs/cartographic_language_and_city_rendering.md`, `docs/next_implementation_sequence.md` (Priority band 4), `validation/narratives/city_data_and_search_notes.md`.
  - **Aspect-to-angle glow/aura:** unrelated; out of scope.
  - - **`feature code`** (e.g. PPLC capital, PPLA admin) supports **prominence heuristics**.
  - - **Ranking “fame”** beyond population is **not** a single column—you derive it from feature codes, capitals, optional external scores, or user locale.

### A.44 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/governance/anti_cursor_bullshit_governance_rules.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 72
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Requirement signals:
  - # Anti-Cursor Bullshit Governance Rules
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountability_failure_audit.md` …
  - 3. **rollback path** — how to revert,

### A.45 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_memory_synthesis.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 16257; SHA-12: `04f378dc370d`; score: 89
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Requirement signals:
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.
  - **Orientation index (all doctrine files, pacing, reading order):** `docs/DOCTRINE_INDEX.md`
  - ### Chronology and authority
  - Archaeology files are **mostly chronological**. When two extracts disagree, **prefer the later thread** for *current architectural and UX doctrine* unless the synthesis explicitly marks the topic **unresolved**. Examples that repeatedly matured across chats:

### A.46 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_philosophical_synthesis.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 128
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Requirement signals:
  - **Status:** Foundational doctrine for **future training**, **reviewer systems**, **UX design**, **product strategy**, **conversational architecture**, and **interpretive governance**.
  - **Authority:** Synthesizes durable texts in `ai_context/`, `docs/`, and `memory_archaeology_raw/consolidated_notes/`. It **does not** supersede those sources on technical implementation; it **weaves** them into one training-readable whole.
  - The relocation astrology platform is built on a paradox that mature users already live inside: **structure is real, and agency is real**. The chart is treated as **structurally real** for product purposes—not as an infinitely rewriteable “vibe,” not as a story generator that owes…
  - Underneath lies a technical moral that keeps philosophy honest: **inspectable precision**. If the map shows a region or line, it must mean something **precise** in the relocated model. “Plausible-looking geometry” is not validation. **False membership** is rejected even when cosm…
  - ### 2.2 Truth hierarchy (epistemology of surfaces)

### A.47 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/intentionality_and_symbolic_constraints.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 8365; SHA-12: `d1c233003983`; score: 44
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Requirement signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**
  - - **`ai_context/core_product_truths.md`** — parallel **interpretive integrity** and **tradeoff intelligence** sections.

### A.48 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/map_and_overlay_design_research.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 5149; SHA-12: `f3943cdf7cf9`; score: 21
- Key headings: Map and Overlay Design Research; 1. Leaflet vs MapLibre vs Google Maps (philosophical comparison); 2. Current Leaflet strengths (for this codebase); 3. Actual blockers to watch for (hypothesis list—not confirmed); 4. Overlay transparency strategy (research directions); 5. Semantic overlap colors; 6. Aura rendering directions (non-commitments); 7. Map-edge and world-wrap ideas; 8. Dark / light mode implications; 9. Multilingual city rendering; 10. Decision rule (when to reopen migration); Related docs
- Requirement signals:
  - | **Fit for this product** | Strong when overlays are **GeoJSON + careful projection/wrap discipline** and the team values **direct control** over truth vs display separation. | Strong if **vector basemaps**, **pitch**, **client-side style**, or **dense label collision** become c…
  - | **Non-technical cost** | You maintain more glue (wrap, performance quirks). | Investment in style JSON, shader-era debugging. | Billing, keys, usage caps, compliance narrative. |
  - - **Separation story aligns:** canonical backend GeoJSON + **display-layer** wrap/duplicate logic matches institutional architecture (`decisions.md`).
  - - **Lower migration tax** while overlay **truth** and **overlap readability** are still evolving—**avoid rewriting two crises at once**.
  - - **Debug mode** to visualize overlap counts or layer order without shipping noise to default UI.

### A.49 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/next_implementation_sequence.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 10690; SHA-12: `ced0e563c90b`; score: 65
- Key headings: Next Implementation Sequence; Priority band 1 — UX polish (minimal architecture risk); Chunk 1.1 — Sidebar density and “debug vs ship” clarity; Chunk 1.2 — Popup and typography refinement; Chunk 1.3 — Native select stability + legend clutter reduction; Priority band 2 — Validator / stress tooling; Chunk 2.1 — Fixture manifest + “run these five” script; Chunk 2.2 — Latitude / polar stress suite expansion; Chunk 2.3 — Brute-force / truth export hygiene; Priority band 3 — Account + birth-data workflows; Chunk 3.1 — Birth data model (local-only MVP); Chunk 3.2 — Chart list + “open on map”
- Requirement signals:
  - - **Validation:** Visual pass; confirm map remains primary; no regression on popup/dropdown behavior.
  - - **Do not overengineer:** No new framework, no drawer rewrite here—**incremental compression** only.
  - ### Chunk 1.2 — Popup and typography refinement
  - - **Why:** Popup is diagnostic truth; typography should match premium, calm instrument tone.
  - - **Validation:** Side-by-side screenshots; high-north / southern fixtures; dateline popups unchanged logically.

### A.50 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: constitutional_product_canons, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 153
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Requirement signals:
  - **CANONICAL** for non-AI application UX architecture (Web 2.0 standalone product).
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doct…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - **Product identity (2026-05-31):** See `docs/constitutional/map_first_product_doctrine_v1.md`. The app is a **relocation discovery instrument** — not a CRM, SaaS dashboard, or record-management platform with a map attached. **Center of gravity:** Map → Analysis → Administration.

### A.51 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 101
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Requirement signals:
  - # Doctrine index
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…
  - **Older doctrine and archaeology:** Older docs listed below remain valuable context, evidence, and active companions where not superseded. Treat them as secondary to `docs/constitutional/` on layer sovereignty, forbidden crossings, epistemic humility, runtime/renderer sovereignty…

### A.52 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/README.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 30
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - truth integrity,
  - - conversational interpretation,
  - # Doctrine Categories

### A.53 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 142
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Requirement signals:
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - - the authority when UX behavior is ambiguous
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - **Reads with (secondary):** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` (indexed catalog), `docs/constitutional/map_first_product_doctrine_v1.md`, journey and workflow architecture docs.

### A.54 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 210
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Requirement signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.55 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 35789; SHA-12: `795365723409`; score: 153
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Requirement signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Scope:** Entity model, persistence boundaries, saved exploration shape, active context, and optional post-v1 behavioral capture — **documentation only**. Not SQL. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,

### A.56 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 8365; SHA-12: `d1c233003983`; score: 44
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Requirement signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**
  - - **`ai_context/core_product_truths.md`** — parallel **interpretive integrity** and **tradeoff intelligence** sections.

### A.57 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 41
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Requirement signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - Both are **primary surfaces**. The Chart Page must not become an afterthought.

### A.58 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 57
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Requirement signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.

### A.59 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9566; SHA-12: `3de8663545ba`; score: 59
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Requirement signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - and trust depends on inspectable geometry, not interpretation theater.

### A.60 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, ai_and_interpretation_limits
- Characters: 3360; SHA-12: `554add110fa4`; score: 23
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Requirement signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - Truth belongs primarily to Layer 1.
  - ## Interpretation
  - Interpretation belongs primarily to Layer 3.

### A.61 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/DOCTRINE_INDEX.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 101
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Requirement signals:
  - # Doctrine index
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…
  - **Older doctrine and archaeology:** Older docs listed below remain valuable context, evidence, and active companions where not superseded. Treat them as secondary to `docs/constitutional/` on layer sovereignty, forbidden crossings, epistemic humility, runtime/renderer sovereignty…

### A.62 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/README.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 30
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - truth integrity,
  - - conversational interpretation,
  - # Doctrine Categories

### A.63 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_CONSTITUTION.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 142
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Requirement signals:
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - - the authority when UX behavior is ambiguous
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - **Reads with (secondary):** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` (indexed catalog), `docs/constitutional/map_first_product_doctrine_v1.md`, journey and workflow architecture docs.

### A.64 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_DOCTRINE_MASTER.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 210
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Requirement signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.65 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/constitutional_summary.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits
- Characters: 4609; SHA-12: `8238f401edb1`; score: 40
- Key headings: Constitutional Summary; Purpose; Layer Architecture; Layer 1 - Truth; Layer 2 - Symbolic Ontology; Layer 3 - Intentional Interpretation; Layer 4 - Exploratory Optimization; Forbidden Crossings; Epistemic Doctrine; Runtime And Renderer Sovereignty; Purification Principle; Professional Trust And AI Behavior
- Requirement signals:
  - ## Layer 1 - Truth
  - Layer 1 owns astronomical and geometric truth:
  - Layer 1 is deterministic, inspectable, objective, and independently verifiable. It must not interpret, optimize, moralize, psychologically frame, or alter truth to satisfy user desire.
  - - orb doctrines,
  - Layer 2 may interpret truth through a declared symbolic framework, but it may never rewrite geometry. Symbolic systems may disagree; no ontology is permanently privileged as universal truth.

### A.66 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/epistemic_integrity_and_symbolic_humility.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ai_and_interpretation_limits
- Characters: 3739; SHA-12: `242cc62cfae5`; score: 13
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior; Good Behavior; Collaborative Discovery
- Requirement signals:
  - This document is CANONICAL.
  - - and anti-bullshit doctrine.
  - All AI and interpretive systems must follow these principles.
  - This document establishes the philosophical and operational rules governing:
  - - interpretation,

### A.67 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/intentionality_and_symbolic_constraints.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 8365; SHA-12: `d1c233003983`; score: 44
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Requirement signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**
  - - **`ai_context/core_product_truths.md`** — parallel **interpretive integrity** and **tradeoff intelligence** sections.

### A.68 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layer_sovereignty_and_forbidden_crossings.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ai_and_interpretation_limits
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 50
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Requirement signals:
  - # Layer Sovereignty And Forbidden Crossings
  - This document is CANONICAL.
  - These rules are mandatory architectural constraints.
  - - forbidden crossings,
  - # Core Principle

### A.69 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layered_symbolic_intelligence_architecture.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 4801; SHA-12: `5242de0598f3`; score: 23
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Requirement signals:
  - This document is CANONICAL.
  - All future systems must respect:
  - - forbidden crossings,
  - - and truth integrity.
  - - preserve truth integrity,

### A.70 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/map_first_product_doctrine_v1.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 41
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Requirement signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - Both are **primary surfaces**. The Chart Page must not become an afterthought.

### A.71 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, ai_and_interpretation_limits
- Characters: 3360; SHA-12: `554add110fa4`; score: 23
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Requirement signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - Truth belongs primarily to Layer 1.
  - ## Interpretation
  - Interpretation belongs primarily to Layer 3.

### A.72 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/2026-05-29_application_journey_architecture_v1.md`
- Categories: constitutional_product_canons, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 153
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Requirement signals:
  - **CANONICAL** for non-AI application UX architecture (Web 2.0 standalone product).
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doct…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - **Product identity (2026-05-31):** See `docs/constitutional/map_first_product_doctrine_v1.md`. The app is a **relocation discovery instrument** — not a CRM, SaaS dashboard, or record-management platform with a map attached. **Center of gravity:** Map → Analysis → Administration.

### A.73 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_constitution_and_review_architecture.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 13121; SHA-12: `96b9567947d8`; score: 71
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Requirement signals:
  - **Status:** Internal **governance architecture** for future AI-assisted interpretation—not a shipping spec, not marketing, not ethics theater.
  - **Doctrine stack (read before changing AI behavior):**
  - - **`docs/intentionality_and_symbolic_constraints.md`** — fate/agency, tradeoffs, intentionality, AI governance implications.
  - - **`ai_context/core_product_truths.md`** — epistemic truth, interpretive integrity, tradeoff intelligence, professional-first stance.
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account); what software is allowed to **claim** at each surface.

### A.74 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 93
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Requirement signals:
  - # AI Interpretation Truthfulness Doctrine v1
  - **CANONICAL** for **future** AI-assisted interpretation layers — not current product scope.
  - **Scope:** Documentation only. Defines interpretive discipline, forbidden patterns, and a future review architecture. **No AI implementation in dumb Web 2.0 v1.**
  - - `docs/constitutional/truth_vs_astrological_fact_vs_interpretation.md` — Layer 1 / 2 / 3 separation
  - - `docs/constitutional/professional_trust_and_ai_behavior_doctrine.md` — propose vs declare, layer sovereignty

### A.75 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 42
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Requirement signals:
  - # Birth Time Uncertainty and Confidence Doctrine
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `validation/narratives…
  - - AI intake may help later — **MVP must handle tiers without AI**.
  - ## Core principle

### A.76 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_and_experience_foundations.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ui_and_visual_constraints, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 44
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Requirement signals:
  - **Important:** The emotional and atmospheric goals below are **experiential design constraints**—they govern how future UX and rendering choices should **feel** and **function**. They are **not** marketing fluff; they are institutional memory for product judgment.
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).
  - - **Pre-verbal / symbolic language:** Where possible, meaning is carried **through encodings**—overlay semantics, gradients, aura, softness, restraint, popup hierarchy—as a **language without words**, aligned with `docs/visual_semantic_style_guide.md`.
  - - **Fantasy with honesty:** The atmosphere supports **fantasy and exploration** while the system remains **epistemically honest** (popup vs overlay vs account truth hierarchy unchanged).
  - - **Beauty from truthful systems:** Beauty should **emerge** from **honest interaction and encoding**, not from **decorative** layers glued on top.

### A.77 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_visual_language_and_design_doctrine.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 47
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Requirement signals:
  - # Brand, Visual Language, and Design Doctrine
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - | **Fantasy** | Allowed in user meaning-making; forbidden in fake certainty |
  - ## Visual epistemology (truth hierarchy)

### A.78 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/client_chart_data_model_v1_2026-05-29.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 35789; SHA-12: `795365723409`; score: 153
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Requirement signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Scope:** Entity model, persistence boundaries, saved exploration shape, active context, and optional post-v1 behavioral capture — **documentation only**. Not SQL. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,

### A.79 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/core_product_truths.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9535; SHA-12: `9d9048f7cab4`; score: 66
- Key headings: Core Product Truths; Astrology Truth; Inspectability; Map and Overlay UX; Product Experience; Visual / Semantic Product Identity; Emotionally non-interfering design (experiential constraints); Interpretive language and emotional transparency (doctrine); Interpretive integrity and archetypal honesty (doctrine); Development Discipline; Where the nuanced history lives
- Requirement signals:
  - # Core Product Truths
  - These are durable principles that should survive individual implementation chunks, UI experiments, and future chat transitions.
  - ## Astrology Truth
  - - Map overlays must agree with point-and-click astrology truth.
  - - Popup point-truth validation is authoritative for local membership checks.

### A.80 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/geocoder_and_city_identity_strategy.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 22
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Requirement signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - **Related:** `memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `docs/geocoder_dataset_feasibility.md`, `docs/cartographic_language_and_city_rendering.md` (basemap change ⇒ **§0** full visual re-test), `docs/relocation_app_product_roadmap.md` §7–8, `docs/m…
  - **Out of scope here:** Aspect-to-angle **glow/aura** visualization (not implemented; separate docs).
  - ## 1. Doctrine: city search is core systems engineering
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`). The map binds **h…

### A.81 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/map_drawer_and_layer_control_doctrine.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7226; SHA-12: `181a6ad8f6bd`; score: 32
- Key headings: Map Drawer and Layer Control Doctrine; Status; Purpose; Control hierarchy (map screen); Drawer architecture (target); Zones; Genie-into-corner collapse; Deferral (current phase); Condition editor doctrine; Target model; Card visual language; Search action
- Requirement signals:
  - # Map Drawer and Layer Control Doctrine
  - **CANONICAL** for Phase 3 strategic product architecture.
  - **Reads with:** `docs/overlay_and_aura_visual_strategy.md` §H, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/visual_semantic_style_guide.md` §9, `docs/product_workflows/product_screen_and_transition_architecture.md`.
  - Keep the **map sacred**. Controls must:
  - **Rule:** if a control hides coastlines, labels, or overlap evidence, it fails.

### A.82 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/product_screen_and_transition_architecture.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 57
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Requirement signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.

### A.83 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_mode_vs_lay_mode_strategy.md`
- Categories: mathematical_thresholds, api_and_payload_boundaries, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3492; SHA-12: `c166907d611f`; score: 18
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Requirement signals:
  - Core principles are canonical.
  - # Core Principle
  - The system must avoid:
  - - oversimplifying truth,
  - - raw truth visibility,

### A.84 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_non_ai_workflow_v1.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9566; SHA-12: `3de8663545ba`; score: 59
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Requirement signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - and trust depends on inspectable geometry, not interpretation theater.

### A.85 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_trust_and_ai_behavior_doctrine.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 32
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Requirement signals:
  - # Professional Trust And AI Behavior Doctrine
  - This document defines how AI systems inside the platform must behave.
  - The AI must never behave like:
  - # Core Principle
  - This principle is absolute.

### A.86 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_workflow_and_explanatory_language.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 11541; SHA-12: `1814ff883a7c`; score: 49
- Key headings: Professional Workflow And Explanatory Language; Status; Purpose; Professional Map Workflow; Desired Placement Search; Exclude / NOT Variables; Solo And Mute Controls; Inspection Workflow; Helper Layers; Intention Remains Primary; Astro Assist Substitution Guidance; Additive And Subtractive Relocation
- Requirement signals:
  - - popup copy candidates,
  - This is NOT constitutional doctrine.
  - Update this document whenever product explanation language, professional workflow guidance, or popup copy concepts are clarified.
  - This document preserves explanatory language and professional workflow doctrine for later use in:
  - - help popups,

### A.87 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ux_principles_and_emotional_tone.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 4906; SHA-12: `3924025d2ba8`; score: 27
- Key headings: UX Principles and Emotional Tone; 1. Core temperament; 2. Map-first atmosphere; 3. Delight without spectacle; 4. Overlap readability philosophy; 5. Typography and color tone; 6. Layout cautions: drawer / genie / chrome; 7. Mobile and tablet; 8. When to stop designing; 9. Where philosophy is already strong in the repo; 10. Where philosophy could still drift; Related docs
- Requirement signals:
  - # UX Principles and Emotional Tone
  - | Principle | Meaning |
  - | **Anti-overdesign** | No speculative chrome before map truth and readability are solid. |
  - - **Professional trustworthiness:** numbers, regions, and overlaps must **mean** something inspectable; visual polish never substitutes for false certainty.
  - - **Subtle delight:** smooth staging (e.g. progressive overlays), thoughtful typography, readable defaults.

### A.88 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/visual_semantic_style_guide.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 9451; SHA-12: `93105f1b5ba9`; score: 58
- Key headings: Visual & Semantic Style Guide (Relocation Map System); 1. Visual epistemology (truth hierarchy); 2. House field semantics (categorical + cusp softness); 3. Aspect-to-angle aura semantics (intensity, not category); 4. Overlay texture semantics (almost subconscious); 5. NOT / exclusion overlays; 6. Color philosophy; 7. Popup visual language; 8. Interface tone; 9. Map and control relationship; 10. Account / chart page relationship; 11. Implementation discipline
- Requirement signals:
  - **Status:** Planning and doctrine. This document defines **what visuals mean** and **how they should behave**. It does **not** mandate implementation order or ship dates.
  - **Companion docs:** `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/map_and_overlay_design_research.md`, `docs/brand_and_experience_foundations.md`, `docs/intentionality_and_symbolic_constraints.md` (fate/agency/tradeoffs), `docs/ai_c…
  - ## 1. Visual epistemology (truth hierarchy)
  - | **Right-click / point popup** | **Canonical point truth** for the queried location | Authoritative for “what is true *here*” at that click (degrees, houses, etc.). |
  - | **Cards / favorites / comparison UI (future)** | Same **information language** as popups where possible—shorthand and calm, not a second dialect. |

### A.89 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ai_conversational_modes.md`
- Categories: api_and_payload_boundaries, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 2887; SHA-12: `b796e2065486`; score: 18
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Requirement signals:
  - - canonical architectural principles,
  - - and deferred implementation ideas.
  - - constraints become clearer,
  - # Core Principle
  - The AI should adapt conversational style without violating constitutional doctrine.

### A.90 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/archaeology_and_synthesis_workflow.md`
- Categories: api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9005; SHA-12: `d3add7674811`; score: 60
- Key headings: Archaeology and synthesis workflow; 1. Pipeline overview; 2. When to create an archaeology pass; 3. When to create or update synthesis docs; 4. Durable truths vs transient implementation; 5. How to avoid flattening nuance during synthesis; 6. Preserving contradictory but valuable tensions; 7. Doctrine canonicalization; 8. Open tension preservation; 9. Institutional memory updating (rhythm); 10. Governance refresh; 11. Review bundle generation
- Requirement signals:
  - **Purpose:** Capture chat and session intelligence **without** flattening nuance, **without** treating the latest thread as law, and **without** losing rejected paths that explain pivots.
  - **Reads with:** `ai_context/memory_workflow.md`, `docs/institutional_memory_synthesis.md`, `docs/project_memory_taxonomy.md`, `docs/process/doctrine_review_cycle.md`.
  - Raw capture → themed synthesis → doctrine canonicalization → open tension preservation
  - | **Raw capture** | `memory_archaeology_raw/pending_imports/` | Evidence, chronology, quotes, failure stories |
  - | **Canonical doctrine** | `docs/`, `ai_context/core_product_truths.md` | Slow law |

### A.91 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/decision_and_uncertainty_framework.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9068; SHA-12: `4b8f251dada4`; score: 60
- Key headings: Decision and uncertainty framework; 1. Bounded uncertainty; 2. Heuristic vs exact truth; 3. Symbolic plausibility vs fake precision; 4. Exploratory guidance vs deterministic recommendation; 5. Preserving ambiguity intentionally; 6. Reversible decisions; 7. Experimentation doctrine; 8. User-facing confidence vs backend uncertainty; 9. “Good enough for exploration” vs “authoritative truth”; 10. Case study: aura philosophy; 11. Visual approximation doctrine
- Requirement signals:
  - **Reads with:** `docs/visual_semantic_style_guide.md` §1, `docs/overlay_and_aura_visual_strategy.md` (aura doctrine), `docs/intentionality_and_symbolic_constraints.md`, `docs/process/doctrine_review_cycle.md`.
  - | **Membership / math** (in house? on line?) | Drive toward **exact**, validated, inspectable answers; popup authority. |
  - | **Symbolic ambiguity** (paradox, multi-valence) | **Preserve intentionally**; do not force single verdict in software. |
  - **Bounded uncertainty** means: be precise where the engine is precise; be honest where the engine is silent; do not **smuggle certainty** through UI fluency or model confidence.
  - ## 2. Heuristic vs exact truth

### A.92 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/doctrine_review_cycle.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9902; SHA-12: `00598386986c`; score: 54
- Key headings: Doctrine review cycle; 1. What this cycle protects; 2. Slow docs policy; 3. Implementation vs philosophy separation; 4. Tension-preservation doctrine; 5. Rationale preservation rules (“why”, not just “what”); 6. Review cadences (suggested, not ceremonial); 6.1 Doctrine coherence review; 6.2 AI drift audit; 6.3 UX coherence review; 6.4 Archaeology / synthesis refresh; 6.5 Review bundle / external audit
- Requirement signals:
  - # Doctrine review cycle
  - **Reads with:** `docs/DOCTRINE_INDEX.md`, `docs/review_contracts_and_governance.md`, `docs/process/decision_and_uncertainty_framework.md`, `ai_context/memory_workflow.md`.
  - - **Experiential coherence** — map-first calm, contemplative space, overlap readability, truth hierarchy.
  - **Slow docs** govern **meaning, tone, epistemology, and interpretive ethics**. They change **deliberately**, with explicit revision notes when practical. Examples: `docs/intentionality_and_symbolic_constraints.md`, `docs/brand_and_experience_foundations.md`, `docs/visual_semantic…
  - **Fast docs** govern **what is true now** and **how we ship**: `ai_context/current_state.md`, `ai_context/decisions.md`, validation narratives, tactical tuning notes.

### A.93 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/future_excellence_vs_future_feature_excellence.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 20
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Requirement signals:
  - - canonical architectural principles,
  - # Core Principle
  - ## Infrastructure excellence and feature excellence must remain distinct.
  - - support future capabilities safely,
  - - rollback safety,

### A.94 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer4_optimization_and_exploration_doctrine.md`
- Categories: api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 4341; SHA-12: `289b4552320f`; score: 13
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Requirement signals:
  - # Layer 4 Optimization And Exploration Doctrine
  - - canonical Layer 4 principles,
  - Core Layer 4 boundaries are canonical.
  - # Core Principle
  - # Important Constraint

### A.95 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer5_experiential_education_through_travel_v1.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 34
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Requirement signals:
  - **Dependency:** Requires mature AI guidance, relocation exploration substrate, and user observation capture — **after** standalone Web 2.0 facts-first product is proven.
  - **Reads with (boundary context only):** `docs/ux/2026-05-29_application_journey_architecture_v1.md` §Future Rooms, `docs/constitutional/layer_sovereignty_and_forbidden_crossings.md`.
  - **Must not be read as:** screen spec, sprint backlog, course marketplace brief, or Layer 1–3 implementation requirement.
  - | Notice what changed when you relocated or slowed down | Memorize rules without location context |
  - Reading may support the journey — glossaries, brief context, safety notes — but **reading is never the main pedagogical engine**. The main engine is **lived geographic comparison** grounded in the same factual substrate the professional instrument provides.

### A.96 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/memory_workflow.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 6877; SHA-12: `0a90f034aa1f`; score: 29
- Key headings: Memory Maintenance Workflow; Purpose; Sources; Mining Old Chats; Processing Extraction Docs; Consolidating Raw Archaeology (optional phase); Updating Durable Memory; Memory Types; Raw Extraction; Durable Memory; Roadmap; Current Implementation State
- Requirement signals:
  - The goal is durable continuity. Cursor and external reviewers should be able to understand the product direction, current state, and important constraints without rereading every past chat.
  - **Institutional map (broader pipeline):** `docs/process/archaeology_and_synthesis_workflow.md` — raw → synthesis → doctrine → review bundle → rehydration. **Cadence:** `docs/process/doctrine_review_cycle.md`.
  - - Validation reports and narratives under `validation/`.
  - - Durable product principles.
  - - Edge cases and validation lessons.

### A.97 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 27
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Requirement signals:
  - - canonical architectural principles,
  - - and deferred implementation ideas.
  - - constraints become clearer,
  - # Core Principle
  - Truth computation must remain independent from symbolic interpretation systems.

### A.98 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_continuity_workflow.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 5184; SHA-12: `8a80bdfb8e6e`; score: 24
- Key headings: Project Continuity Workflow; 1. Goals; 2. Memory lanes (what goes where); 3. Archaeology intake workflow; 4. Consolidation workflow (when to run); 5. Reviewer workflow; 6. Proposed updates workflow; 7. Raw archaeology vs durable truths; 8. How future chats should initialize; 9. How to continue safely after context loss; 10. Related docs
- Requirement signals:
  - How to keep **coherence** across sessions, models, and months—without turning the repo into chaos. Complements `ai_context/memory_workflow.md` (detailed file rhythm) and `docs/institutional_memory_synthesis.md` (archaeology → durable truth).
  - - **Clear separation:** raw archaeology vs curated principles vs implementation state.
  - | **Raw archaeology** | `memory_archaeology_raw/pending_imports/` | Verbatim / chronological extracts; **not** canonical alone. |
  - | **Themed synthesis** | `memory_archaeology_raw/consolidated_notes/` | Onboarding-friendly themes; still subordinate to **human-reviewed** `ai_context/` for “current doctrine.” |
  - | **Durable truths** | `ai_context/core_product_truths.md`, `decisions.md`, `product_brief.md` | Stable principles and decisions. |

### A.99 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_memory_taxonomy.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 5641; SHA-12: `e630f6401456`; score: 51
- Key headings: Project Memory Taxonomy; Architecture; UX Philosophy; Visual doctrine vs rendering experiments vs temporary UX; Implementation State; Future Features; Rejected Approaches; Validation Methodology; Edge Cases; Unresolved Questions; AI Strategy; Product Philosophy
- Requirement signals:
  - This taxonomy keeps project memory organized as the app grows across chats, validation passes, experiments, and external reviews.
  - - Canonical backend truth versus frontend display geometry.
  - - Truth-grid generation strategy.
  - Stable experience principles and design constraints.
  - **Doctrine vs experiments:** Stable UX principles live here and in `ai_context/core_product_truths.md` (“Visual / Semantic Product Identity”). **Durable visual doctrine** (epistemology: what overlays *mean* vs what popups *prove*) is expanded in **`docs/visual_semantic_style_guid…

### A.100 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/foundational_product_truths.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits
- Characters: 4380; SHA-12: `9c5286269c09`; score: 23
- Key headings: Foundational Product Truths (From Archaeology); Trust and truth; Overlap and decision-making; Precision vs cosmetics (non-negotiable vs acceptable); Separation of concerns (recurring architectural moral); Human + AI collaboration stance; Emotional tone and moat; Repetition as signal
- Requirement signals:
  - # Foundational Product Truths (From Archaeology)
  - **Status labels:** *Durable principle* = should guide decisions for years. *Product stance* = strategic positioning. *Process principle* = how the team builds.
  - ## Trust and truth
  - - **Durable principle — Inspectable precision:** If the map shows a region, line, or overlap, it must mean something **precise** in the relocated chart model. “Plausible geometry” is not validation. Trust is built through reproducible checks, not visual confidence.
  - - **Durable principle — The map is the primary model (not an illustration):** Users explore **geography as astrology**. The map is not decoration around a chart calculator; it is the main instrument.

### A.101 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_memory_synthesis.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 16257; SHA-12: `04f378dc370d`; score: 89
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Requirement signals:
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.
  - **Orientation index (all doctrine files, pacing, reading order):** `docs/DOCTRINE_INDEX.md`
  - ### Chronology and authority
  - Archaeology files are **mostly chronological**. When two extracts disagree, **prefer the later thread** for *current architectural and UX doctrine* unless the synthesis explicitly marks the topic **unresolved**. Examples that repeatedly matured across chats:

### A.102 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_philosophical_synthesis.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 128
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Requirement signals:
  - **Status:** Foundational doctrine for **future training**, **reviewer systems**, **UX design**, **product strategy**, **conversational architecture**, and **interpretive governance**.
  - **Authority:** Synthesizes durable texts in `ai_context/`, `docs/`, and `memory_archaeology_raw/consolidated_notes/`. It **does not** supersede those sources on technical implementation; it **weaves** them into one training-readable whole.
  - The relocation astrology platform is built on a paradox that mature users already live inside: **structure is real, and agency is real**. The chart is treated as **structurally real** for product purposes—not as an infinitely rewriteable “vibe,” not as a story generator that owes…
  - Underneath lies a technical moral that keeps philosophy honest: **inspectable precision**. If the map shows a region or line, it must mean something **precise** in the relocated model. “Plausible-looking geometry” is not validation. **False membership** is rejected even when cosm…
  - ### 2.2 Truth hierarchy (epistemology of surfaces)

### A.103 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/map_workspace_behavior_audit_v1_2026-05-30.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 15325; SHA-12: `7567f30ce7ff`; score: 59
- Key headings: Map Workspace Behavior Audit v1; Status; Purpose; Language and ID doctrine (applies to all sections); 1. Behavior already decided; Genie modes; Reasons to reopen Genie (decided intents); Search and render; Variable model; Legacy adapter (handoff to production map path); Map surface and overlay doctrine; Clear Map
- Requirement signals:
  - - `docs/ui/map_drawer_and_layer_control_doctrine.md` — map-primary hierarchy (strategic)
  - This document does **not** add features, layouts, or architecture. It consolidates decisions already present in contracts and related doctrine.
  - # Language and ID doctrine (applies to all sections)
  - | Rule | Status |
  - | **Stable IDs are canonical** | Decided — type ids (`planet_in_house`, …), registry ids, payload field names |

### A.104 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/product_brief.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 3080; SHA-12: `ba708a2f1745`; score: 23
- Key headings: Product Brief; Product; Current Core Capabilities; Product Philosophy; Overlay Truth Standard; Current Architecture Direction; Validation Corpus; Institutional memory (archaeology)
- Requirement signals:
  - ## Current Core Capabilities
  - - `truth_grid` house overlays for Planet-in-House searches.
  - - Point-and-click popup truth checks for local chart details.
  - - Debug geometry mode for tracing backend canonical features through frontend display features.
  - ## Overlay Truth Standard

### A.105 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/relocation_app_product_roadmap.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 27057; SHA-12: `24ab9bae5cb8`; score: 154
- Key headings: Relocation App Product Roadmap; 1. Current Stable Milestone; 2. Product Philosophy; 3. Core Search Types; 4. Overlay/Color System Roadmap; 5. Aspect Aura Roadmap; 6. UX/Layout Roadmap; 7. City Search / Geocoder Roadmap; 8. Birth Data / Accounts / Professional Mode Roadmap; Saved Object Taxonomy; Phase 2.4 Sampling / Cache Scaffold; Phase 2.5 Sampling / Cache Population Strategy
- Requirement signals:
  - This document preserves the current product strategy, development sequence, UX philosophy, and validation priorities for future work.
  - - `truth_grid` house overlays are working and remain opt-in.
  - - Popup truth generally matches overlays in current validation.
  - - Validation contradictions are `0` in current truth-grid and angle-sign tests.
  - - `truth_grid` is not yet default.

### A.106 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ux_and_design_language.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3849; SHA-12: `ac5f86eb3a13`; score: 25
- Key headings: UX and Design Language (From Archaeology); Map-first and spatial reading; Trust UX vs explanation UX; Typography and popups (professional validation patterns); Interaction pitfalls called out repeatedly; Emotional tone; Product positioning language (from archaeology); Tensions to preserve (not resolve here); Chat 08 update: style presets and mobile layer control
- Requirement signals:
  - - **Map dominance:** Controls exist to serve exploration; they must not steal the primary visual field during validation or professional use.
  - - **Global map ergonomics:** Users must pan freely near **Pacific/dateline/polar** regions during validation; artificial snap-back is disqualifying for this product class.
  - - **Professionals still need an oracle:** Right-click / precise coordinate inspection is framed as **truth instrumentation**. It must have onboarding (hint, mode toggle), and mobile needs long-press equivalent.
  - ## Typography and popups (professional validation patterns)
  - - Popups evolved toward **lean relocated truth**: emphasize relocated angles and relocated house table; avoid cluttering with globally static natal detail in the same surface.

### A.107 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 20953; SHA-12: `db53e1e91227`; score: 82
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Requirement signals:
  - **ARCHITECTURE REVIEW — aligned with Map-First Product Doctrine (2026-05-31)**
  - **Date:** 2026-05-29 (original); **doctrine alignment:** 2026-05-31
  - **Governing doctrine:** `docs/constitutional/map_first_product_doctrine_v1.md` — supersedes dashboard-centric recommendations in v1.0–v1.1 of this review.
  - - `docs/architecture/client_chart_data_model_v1_2026-05-29.md` (data ownership authority)
  - - `docs/ux/2026-05-29_application_journey_architecture_v1.md` (screen/journey authority)

### A.108 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/00_OPERATOR_START_HERE.md`
- Categories: ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits
- Characters: 697; SHA-12: `a0e79ddfcf29`; score: 4
- Key headings: AI Onboarding Entry Point
- Requirement signals:
  - - Complete Product Comprehension Gate
  - - repeating doctrine without understanding doctrine
  - Understanding must be demonstrated, not claimed.

### A.109 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_EVALUATION_LOG.md`
- Categories: validation_and_governance_gates, ai_and_interpretation_limits
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.110 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_WORKFLOW_GOVERNANCE.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 14272; SHA-12: `570f3cca823a`; score: 118
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Requirement signals:
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in writing.
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisible engineering inte…
  - ## Ghost Boss Governance Doctrine
  - The Ghost Boss is the invisible engineering conscience for the project. It does not block visible product work by default; it preserves the hidden work that makes visible product promises trustworthy.
  - Every phase closeout must ask whether it introduced or exposed:

### A.111 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/KILL_TEST.md`
- Categories: validation_and_governance_gates, ai_and_interpretation_limits
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.112 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/PRODUCT_COMPREHENSION_GATE.md`
- Categories: validation_and_governance_gates, ai_and_interpretation_limits
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.113 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/ai_drift_audit_framework.md`
- Categories: constitutional_product_canons, mathematical_thresholds, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 9541; SHA-12: `889f1d9b2f3a`; score: 26
- Key headings: AI drift audit framework; 1. Healthy AI posture (target); 2. Audit dimensions and warning signs; 2.1 Excessive certainty; 2.2 Flattery; 2.3 Manipulative spirituality; 2.4 Optimization obsession; 2.5 Over-helpfulness; 2.6 Premature closure; 2.7 Reducing exploratory play; 2.8 Guru behavior; 2.9 Dependency framing
- Requirement signals:
  - **Reads with:** `docs/ai_constitution_and_review_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/brand_and_experience_foundations.md`, `docs/process/doctrine_review_cycle.md`.
  - - A **GPS recalculator** under constraints—not a prophet, not a therapist replacement, not a spiritual authority.
  - - **Brief by default**, expansive when the user asks—preserving **contemplative space**.
  - - **Subordinate** to popup/line truth and slow doctrine—never contradicting certified point data for comfort.
  - **Severity:** **High** — conflicts with intentionality doctrine.

### A.114 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/anti_cursor_bullshit_governance_rules.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 72
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Requirement signals:
  - # Anti-Cursor Bullshit Governance Rules
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountability_failure_audit.md` …
  - 3. **rollback path** — how to revert,

### A.115 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/constitutional_ingestion_checklist.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 20
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Requirement signals:
  - - track doctrine ingestion,
  - Update this document whenever:
  - - doctrine evolves,
  - This project contains multiple categories of doctrine:
  - - AI behavior doctrine,

### A.116 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/implementation_governance_and_ai_workflow_protocol.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3988; SHA-12: `b127e5c52050`; score: 26
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Requirement signals:
  - This document is CANONICAL.
  - - rollback protocol,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - - rollback-safe,

### A.117 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/purification_audit_framework.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 3639; SHA-12: `a43528565790`; score: 34
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Requirement signals:
  - This document is CANONICAL.
  - - and rollback discipline.
  - - or violate constitutional doctrine.
  - # Core Principle
  - - Has interpretation contaminated truth?

### A.118 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/review_contracts_and_governance.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 12252; SHA-12: `18cc9636738c`; score: 57
- Key headings: Review contracts and governance (implementation layer); 1. What a “review contract” is here; 2. Principles reviewers hold in tension; 3. Implementation review questions; 4. UX review questions; 5. AI behavior review questions; 6. Symbolic integrity review questions; 7. Exploratory and play preservation checks; 8. Anti-chaos visual checks; 9. Anti-guru and anti-coercion checks; 10. Does this preserve contemplative space?; 11. Intelligent exceptions (examples)
- Requirement signals:
  - **Status:** Lightweight operational doctrine—**not** a compliance checklist, **not** a substitute for judgment, **not** corporate policy theater.
  - **Reads with:** `docs/ai_constitution_and_review_architecture.md` (interpretive AI layers and anti-patterns), `docs/DOCTRINE_INDEX.md` (where each doctrine lives), `docs/institutional_philosophical_synthesis.md` (foundational synthesis for training), `docs/process/doctrine_review…
  - Contracts are **guardrails**, not formulas. They do not award points for mechanical compliance. A change can satisfy every literal question below and still be wrong in context—or violate one question deliberately for a **documented, rare, intelligent exception**. The reviewer’s j…
  - **Doctrine** (meaning, tone, truth hierarchy, interpretive ethics) should evolve **slowly** and with **explicit revision**. **Implementation** (controls, performance, map options, geocoder choice, rendering tactics) may iterate **rapidly**—as long as it **does not contradict** sl…
  - ## 2. Principles reviewers hold in tension

### A.119 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: constitutional_product_canons, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 153
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Requirement signals:
  - **CANONICAL** for non-AI application UX architecture (Web 2.0 standalone product).
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doct…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - **Product identity (2026-05-31):** See `docs/constitutional/map_first_product_doctrine_v1.md`. The app is a **relocation discovery instrument** — not a CRM, SaaS dashboard, or record-management platform with a map attached. **Center of gravity:** Map → Analysis → Administration.

### A.120 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 101
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Requirement signals:
  - # Doctrine index
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…
  - **Older doctrine and archaeology:** Older docs listed below remain valuable context, evidence, and active companions where not superseded. Treat them as secondary to `docs/constitutional/` on layer sovereignty, forbidden crossings, epistemic humility, runtime/renderer sovereignty…

### A.121 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/README.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 30
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - truth integrity,
  - - conversational interpretation,
  - # Doctrine Categories

### A.122 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 142
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Requirement signals:
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - - the authority when UX behavior is ambiguous
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - **Reads with (secondary):** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` (indexed catalog), `docs/constitutional/map_first_product_doctrine_v1.md`, journey and workflow architecture docs.

### A.123 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 210
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Requirement signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.124 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 35789; SHA-12: `795365723409`; score: 153
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Requirement signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Scope:** Entity model, persistence boundaries, saved exploration shape, active context, and optional post-v1 behavioral capture — **documentation only**. Not SQL. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,

### A.125 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 8365; SHA-12: `d1c233003983`; score: 44
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Requirement signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**
  - - **`ai_context/core_product_truths.md`** — parallel **interpretive integrity** and **tradeoff intelligence** sections.

### A.126 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 41
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Requirement signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - Both are **primary surfaces**. The Chart Page must not become an afterthought.

### A.127 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 57
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Requirement signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.

### A.128 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9566; SHA-12: `3de8663545ba`; score: 59
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Requirement signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - and trust depends on inspectable geometry, not interpretation theater.

### A.129 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, ai_and_interpretation_limits
- Characters: 3360; SHA-12: `554add110fa4`; score: 23
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Requirement signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - Truth belongs primarily to Layer 1.
  - ## Interpretation
  - Interpretation belongs primarily to Layer 3.

### A.130 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/application_screen_inventory_v1.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, ui_and_visual_constraints, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 17867; SHA-12: `07e2c973e29d`; score: 32
- Key headings: Application Screen Inventory v1; Core Philosophy; Global Product Principles; Primary Product Objects; User; Professional Workspace; Client; Birth Chart; Relocation Search Session; Dashboard will have user's birth chart at the tomp along with name, birth details etc BEAUTIFULLY and tastefull laid out ; Favorite LocationS; Comparison Set
- Requirement signals:
  - # Global Product Principles
  - * Professional workflows must remain coherent
  - * User data objects must persist coherently
  - * Mobile complexity must remain manageable later
  - Question is do we have a separate screen where they're all laid out at once with th option to sleect, edit, delete etc. Also do we cap the nuber (probably yes)

### A.131 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/MISSING_ONBOARDING_ARTIFACTS.md`
- Categories: constitutional_product_canons, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 7542; SHA-12: `225bf21b32b7`; score: 49
- Key headings: Missing Onboarding Artifacts; Purpose; Important Onboarding Docs That Do Not Yet Exist; Empty Validation Docs / Validation Slots; Missing Comprehension Gates; Missing Kill Test Content; Missing Evaluation Rubrics; Existing Empty / Underpopulated Onboarding Folders
- Requirement signals:
  - This file does not create doctrine and does not define product behavior. It records gaps in the onboarding system.
  - ## Important Onboarding Docs That Do Not Yet Exist
  - | Updated top-level onboarding index for the new folder structure | Existing `docs/onboarding/README.md` still references old folders and does not explain the new authority layers. | `docs/onboarding/README.md` |
  - | Core authority folder README | `01_core_authority` needs a short explanation that this folder wins over product-understanding and historical folders. | `docs/onboarding/01_core_authority/README.md` |
  - | Product understanding folder README | `02_product_understanding` needs a short explanation that these docs explain product behavior but defer to core authority on conflicts. | `docs/onboarding/02_product_understanding/README.md` |

### A.132 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/ONBOARDING_CLASSIFICATION_REPORT.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 19329; SHA-12: `87759b54a243`; score: 215
- Key headings: Onboarding Classification Report; Purpose; Exclusions; Destination Folders; Classification Table; Important Excluded Material
- Requirement signals:
  - Classify existing repository material into onboarding authority layers for future AIs and product managers.
  - This report does not create new doctrine. It inventories and classifies existing doctrine, product philosophy, UX philosophy, workflow, AI governance, product training, institutional memory, and onboarding-related documents.
  - The onboarding package intentionally excludes validation reports, smoke tests, renderer experiments, implementation-only documents, phase reports, debugging artifacts, cache architecture, performance investigations, code contracts, payload contracts, and proof artifacts.
  - | `01_core_authority` | Binding product, UX, truth, neutrality, intent, and authority-chain documents. |
  - | `03_extended_context` | Future direction, exploratory doctrine, governance process, doctrine maintenance, and memory process. |

### A.133 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/overlay_and_aura_visual_strategy.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, ui_and_visual_constraints, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 22591; SHA-12: `ec6491f35a58`; score: 102
- Key headings: Overlay And Aura Visual Strategy; Separating cusp softness from aspect aura (do not conflate); A. Overlap Philosophy; A.1 Overlap hot zones; B. Child-Color Strategy; C. NOT/Exclusion Visual Language; D. Aura Philosophy; D.0 Aura is occupancy widening from exactness — never blur; D.1 Intensity must be non-linear from edge to centerline; D.2 The other long-standing principles still apply; D.3 Proportional compression; Doctrine: non-certifying field, samples, and adaptation
- Requirement signals:
  - **Formal epistemology and tone:** see **`docs/visual_semantic_style_guide.md`** (truth hierarchy, texture semantics, popup language, implementation discipline).
  - ## Separating cusp softness from aspect aura (do not conflate)
  - Two different physical/semantic ideas must stay **visually and verbally distinct**:
  - | **House cusp transition** | Softens **categorical** house boundary presentation | **~2°** default gradient along cusp | *Astrological cusp softness*—not “uncertainty.” |
  - - Overlap must remain city-readable.

### A.134 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/process/ai_drift_audit_framework.md`
- Categories: constitutional_product_canons, mathematical_thresholds, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 9541; SHA-12: `889f1d9b2f3a`; score: 26
- Key headings: AI drift audit framework; 1. Healthy AI posture (target); 2. Audit dimensions and warning signs; 2.1 Excessive certainty; 2.2 Flattery; 2.3 Manipulative spirituality; 2.4 Optimization obsession; 2.5 Over-helpfulness; 2.6 Premature closure; 2.7 Reducing exploratory play; 2.8 Guru behavior; 2.9 Dependency framing
- Requirement signals:
  - **Reads with:** `docs/ai_constitution_and_review_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/brand_and_experience_foundations.md`, `docs/process/doctrine_review_cycle.md`.
  - - A **GPS recalculator** under constraints—not a prophet, not a therapist replacement, not a spiritual authority.
  - - **Brief by default**, expansive when the user asks—preserving **contemplative space**.
  - - **Subordinate** to popup/line truth and slow doctrine—never contradicting certified point data for comfort.
  - **Severity:** **High** — conflicts with intentionality doctrine.

### A.135 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/process/archaeology_and_synthesis_workflow.md`
- Categories: api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9005; SHA-12: `d3add7674811`; score: 60
- Key headings: Archaeology and synthesis workflow; 1. Pipeline overview; 2. When to create an archaeology pass; 3. When to create or update synthesis docs; 4. Durable truths vs transient implementation; 5. How to avoid flattening nuance during synthesis; 6. Preserving contradictory but valuable tensions; 7. Doctrine canonicalization; 8. Open tension preservation; 9. Institutional memory updating (rhythm); 10. Governance refresh; 11. Review bundle generation
- Requirement signals:
  - **Purpose:** Capture chat and session intelligence **without** flattening nuance, **without** treating the latest thread as law, and **without** losing rejected paths that explain pivots.
  - **Reads with:** `ai_context/memory_workflow.md`, `docs/institutional_memory_synthesis.md`, `docs/project_memory_taxonomy.md`, `docs/process/doctrine_review_cycle.md`.
  - Raw capture → themed synthesis → doctrine canonicalization → open tension preservation
  - | **Raw capture** | `memory_archaeology_raw/pending_imports/` | Evidence, chronology, quotes, failure stories |
  - | **Canonical doctrine** | `docs/`, `ai_context/core_product_truths.md` | Slow law |

### A.136 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/process/decision_and_uncertainty_framework.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9068; SHA-12: `4b8f251dada4`; score: 60
- Key headings: Decision and uncertainty framework; 1. Bounded uncertainty; 2. Heuristic vs exact truth; 3. Symbolic plausibility vs fake precision; 4. Exploratory guidance vs deterministic recommendation; 5. Preserving ambiguity intentionally; 6. Reversible decisions; 7. Experimentation doctrine; 8. User-facing confidence vs backend uncertainty; 9. “Good enough for exploration” vs “authoritative truth”; 10. Case study: aura philosophy; 11. Visual approximation doctrine
- Requirement signals:
  - **Reads with:** `docs/visual_semantic_style_guide.md` §1, `docs/overlay_and_aura_visual_strategy.md` (aura doctrine), `docs/intentionality_and_symbolic_constraints.md`, `docs/process/doctrine_review_cycle.md`.
  - | **Membership / math** (in house? on line?) | Drive toward **exact**, validated, inspectable answers; popup authority. |
  - | **Symbolic ambiguity** (paradox, multi-valence) | **Preserve intentionally**; do not force single verdict in software. |
  - **Bounded uncertainty** means: be precise where the engine is precise; be honest where the engine is silent; do not **smuggle certainty** through UI fluency or model confidence.
  - ## 2. Heuristic vs exact truth

### A.137 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/process/doctrine_review_cycle.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9902; SHA-12: `00598386986c`; score: 54
- Key headings: Doctrine review cycle; 1. What this cycle protects; 2. Slow docs policy; 3. Implementation vs philosophy separation; 4. Tension-preservation doctrine; 5. Rationale preservation rules (“why”, not just “what”); 6. Review cadences (suggested, not ceremonial); 6.1 Doctrine coherence review; 6.2 AI drift audit; 6.3 UX coherence review; 6.4 Archaeology / synthesis refresh; 6.5 Review bundle / external audit
- Requirement signals:
  - # Doctrine review cycle
  - **Reads with:** `docs/DOCTRINE_INDEX.md`, `docs/review_contracts_and_governance.md`, `docs/process/decision_and_uncertainty_framework.md`, `ai_context/memory_workflow.md`.
  - - **Experiential coherence** — map-first calm, contemplative space, overlap readability, truth hierarchy.
  - **Slow docs** govern **meaning, tone, epistemology, and interpretive ethics**. They change **deliberately**, with explicit revision notes when practical. Examples: `docs/intentionality_and_symbolic_constraints.md`, `docs/brand_and_experience_foundations.md`, `docs/visual_semantic…
  - **Fast docs** govern **what is true now** and **how we ship**: `ai_context/current_state.md`, `ai_context/decisions.md`, validation narratives, tactical tuning notes.

### A.138 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/product_doctrine/UX_DOCTRINE_MASTER.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 210
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Requirement signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.139 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/product_training/professional_workflow_and_explanatory_language.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 11541; SHA-12: `1814ff883a7c`; score: 49
- Key headings: Professional Workflow And Explanatory Language; Status; Purpose; Professional Map Workflow; Desired Placement Search; Exclude / NOT Variables; Solo And Mute Controls; Inspection Workflow; Helper Layers; Intention Remains Primary; Astro Assist Substitution Guidance; Additive And Subtractive Relocation
- Requirement signals:
  - - popup copy candidates,
  - This is NOT constitutional doctrine.
  - Update this document whenever product explanation language, professional workflow guidance, or popup copy concepts are clarified.
  - This document preserves explanatory language and professional workflow doctrine for later use in:
  - - help popups,

### A.140 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/product_workflows/product_screen_and_transition_architecture.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 57
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Requirement signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.

### A.141 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/product_workflows/professional_non_ai_workflow_v1.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9566; SHA-12: `3de8663545ba`; score: 59
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Requirement signals:
  - **CANONICAL** for Phase 3 strategic product architecture.
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - and trust depends on inspectable geometry, not interpretation theater.

### A.142 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/project_continuity_workflow.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 5184; SHA-12: `8a80bdfb8e6e`; score: 24
- Key headings: Project Continuity Workflow; 1. Goals; 2. Memory lanes (what goes where); 3. Archaeology intake workflow; 4. Consolidation workflow (when to run); 5. Reviewer workflow; 6. Proposed updates workflow; 7. Raw archaeology vs durable truths; 8. How future chats should initialize; 9. How to continue safely after context loss; 10. Related docs
- Requirement signals:
  - How to keep **coherence** across sessions, models, and months—without turning the repo into chaos. Complements `ai_context/memory_workflow.md` (detailed file rhythm) and `docs/institutional_memory_synthesis.md` (archaeology → durable truth).
  - - **Clear separation:** raw archaeology vs curated principles vs implementation state.
  - | **Raw archaeology** | `memory_archaeology_raw/pending_imports/` | Verbatim / chronological extracts; **not** canonical alone. |
  - | **Themed synthesis** | `memory_archaeology_raw/consolidated_notes/` | Onboarding-friendly themes; still subordinate to **human-reviewed** `ai_context/` for “current doctrine.” |
  - | **Durable truths** | `ai_context/core_product_truths.md`, `decisions.md`, `product_brief.md` | Stable principles and decisions. |

### A.143 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/project_memory_taxonomy.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 5641; SHA-12: `e630f6401456`; score: 51
- Key headings: Project Memory Taxonomy; Architecture; UX Philosophy; Visual doctrine vs rendering experiments vs temporary UX; Implementation State; Future Features; Rejected Approaches; Validation Methodology; Edge Cases; Unresolved Questions; AI Strategy; Product Philosophy
- Requirement signals:
  - This taxonomy keeps project memory organized as the app grows across chats, validation passes, experiments, and external reviews.
  - - Canonical backend truth versus frontend display geometry.
  - - Truth-grid generation strategy.
  - Stable experience principles and design constraints.
  - **Doctrine vs experiments:** Stable UX principles live here and in `ai_context/core_product_truths.md` (“Visual / Semantic Product Identity”). **Durable visual doctrine** (epistemology: what overlays *mean* vs what popups *prove*) is expanded in **`docs/visual_semantic_style_guid…

### A.144 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/relocation_app_product_roadmap.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 27057; SHA-12: `24ab9bae5cb8`; score: 154
- Key headings: Relocation App Product Roadmap; 1. Current Stable Milestone; 2. Product Philosophy; 3. Core Search Types; 4. Overlay/Color System Roadmap; 5. Aspect Aura Roadmap; 6. UX/Layout Roadmap; 7. City Search / Geocoder Roadmap; 8. Birth Data / Accounts / Professional Mode Roadmap; Saved Object Taxonomy; Phase 2.4 Sampling / Cache Scaffold; Phase 2.5 Sampling / Cache Population Strategy
- Requirement signals:
  - This document preserves the current product strategy, development sequence, UX philosophy, and validation priorities for future work.
  - - `truth_grid` house overlays are working and remain opt-in.
  - - Popup truth generally matches overlays in current validation.
  - - Validation contradictions are `0` in current truth-grid and angle-sign tests.
  - - `truth_grid` is not yet default.

### A.145 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/relocation_map_architecture.md`
- Categories: geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 32916; SHA-12: `2567f925f38a`; score: 190
- Key headings: Relocation Map Architecture — Immediate Truth + Opportunistic Expansion; Core Principle; Brute Force as Control Specimen; Aura Rendering Principles; 1. Aura is deterministic occupancy widening, never blur; 2. Intensity must be non-linear from edge to centerline; 3. Map readability is sacred; 4. The intensity profile must compress proportionally; 5. The current palette is proof-of-concept only; Immediate UX Strategy; Phase 1 — Immediate Response; Phase 2 — Background Opportunistic Expansion
- Requirement signals:
  - # Relocation Map Architecture — Immediate Truth + Opportunistic Expansion
  - > **Status:** Foundational architecture doctrine.
  - > `docs/technical_philosophy/truth_field_rendering_path.md`. Brute-force
  - > classification is now the canonical truth layer; reveal/animation is
  - > a stylistic choice layered on top, never a substitute for truth.

### A.146 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/review_bundle/DOCTRINE_INDEX.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9384; SHA-12: `22902213ef1c`; score: 48
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating); Live application surface (fastest iteration); Suggested reading order (new contributor or agent)
- Requirement signals:
  - # Doctrine index
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Pacing reminder:** **Philosophy and epistemology evolve slowly** (explicit revision). **Implementation details evolve quickly** (iterate with evidence), but **must not contradict** slow doctrine without updating the doctrine file.
  - | `docs/intentionality_and_symbolic_constraints.md` | Fate and agency, relocation as repositioning within structure, tradeoff intelligence, dynamic participation, AI implications at the **meaning** layer. | **Very slow** |
  - | `docs/institutional_memory_synthesis.md` | Bridge from archaeology to repo: Implemented, roadmap, speculative labels; UX and visual doctrine summaries; AI strategy summary; unresolved tensions. | **Medium** |

### A.147 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/review_bundle/README.md`
- Categories: geometry_and_rendering_limits, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 5463; SHA-12: `ec30ad3fc90e`; score: 37
- Key headings: Review bundle — institutional doctrine and governance; Recommended reading order; Files in this bundle and what they govern; Regenerating this bundle; Re-copy or edit docs/review_bundle/open_questions_and_tensions.md as needed; Re-copy docs/review_bundle/README.md if instructions change; Contact surface for feedback
- Requirement signals:
  - # Review bundle — institutional doctrine and governance
  - **Purpose:** A **self-contained snapshot** of core doctrine and governance texts for **external philosophical audit, coherence review, or contributor onboarding** without crawling the whole repository.
  - **What this is not:** It does not replace canonical sources in `docs/` and `ai_context/`. After review, changes belong in those canonical paths; this folder can be **regenerated** by copying fresh snapshots.
  - 1. **`DOCTRINE_INDEX.md`** — orientation: what governs what, pacing, stability labels. Start here for navigation.
  - 3. **`intentionality_and_symbolic_constraints.md`** — fate, agency, tradeoffs, intentionality; meaning-layer AI implications.

### A.148 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/review_bundle/ai_constitution_and_review_architecture.md`
- Categories: constitutional_product_canons, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 13121; SHA-12: `96b9567947d8`; score: 71
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Requirement signals:
  - **Status:** Internal **governance architecture** for future AI-assisted interpretation—not a shipping spec, not marketing, not ethics theater.
  - **Doctrine stack (read before changing AI behavior):**
  - - **`docs/intentionality_and_symbolic_constraints.md`** — fate/agency, tradeoffs, intentionality, AI governance implications.
  - - **`ai_context/core_product_truths.md`** — epistemic truth, interpretive integrity, tradeoff intelligence, professional-first stance.
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account); what software is allowed to **claim** at each surface.

### A.149 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/review_bundle/brand_and_experience_foundations.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, ui_and_visual_constraints, ai_and_interpretation_limits, deferred_and_non_goals
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 44
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Requirement signals:
  - **Important:** The emotional and atmospheric goals below are **experiential design constraints**—they govern how future UX and rendering choices should **feel** and **function**. They are **not** marketing fluff; they are institutional memory for product judgment.
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).
  - - **Pre-verbal / symbolic language:** Where possible, meaning is carried **through encodings**—overlay semantics, gradients, aura, softness, restraint, popup hierarchy—as a **language without words**, aligned with `docs/visual_semantic_style_guide.md`.
  - - **Fantasy with honesty:** The atmosphere supports **fantasy and exploration** while the system remains **epistemically honest** (popup vs overlay vs account truth hierarchy unchanged).
  - - **Beauty from truthful systems:** Beauty should **emerge** from **honest interaction and encoding**, not from **decorative** layers glued on top.

### A.150 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/review_bundle/core_product_truths.md`
- Categories: constitutional_product_canons, geometry_and_rendering_limits, mathematical_thresholds, api_and_payload_boundaries, ui_and_visual_constraints, validation_and_governance_gates, ai_and_interpretation_limits, persistence_and_cache_limits, deferred_and_non_goals
- Characters: 9535; SHA-12: `9d9048f7cab4`; score: 66
- Key headings: Core Product Truths; Astrology Truth; Inspectability; Map and Overlay UX; Product Experience; Visual / Semantic Product Identity; Emotionally non-interfering design (experiential constraints); Interpretive language and emotional transparency (doctrine); Interpretive integrity and archetypal honesty (doctrine); Development Discipline; Where the nuanced history lives
- Requirement signals:
  - # Core Product Truths
  - These are durable principles that should survive individual implementation chunks, UI experiments, and future chat transitions.
  - ## Astrology Truth
  - - Map overlays must agree with point-and-click astrology truth.
  - - Popup point-truth validation is authoritative for local membership checks.



---

## Appendix B — Audit Statement

Programmatic pass selected 170 canon/boundary source blocks from 196 total archive blocks. The audit JSON stores matched file names, hashes, headings, requirement signals, category counts, central sources, and source metadata. Final generated word count before this statement: 22918 words.
