# CORE_CONCEPTS_AND_LAYERS.md

**Status:** Canonical product-concept and structural-layer manual for the Astrological Geography platform.  
**Source archive:** `ALL_PROJECT_DOCUMENTS.txt`  
**Generation method:** deeper three-pass local Python extraction and consolidation.  
**Total archive file blocks parsed:** 196  
**Concept/philosophy/layer source blocks matched:** 196  
**Audit hash:** `90e1ae96336fd53e`

---

## 0. Constitutional Product Rule

**Reveal structure. Preserve judgment.**

This is the foundational concept of the platform. The application exists to make geographical chart conditions visible, searchable, inspectable, comparable, saveable, and replayable. It reveals where symbolic conditions hold in space. It preserves the human’s right and responsibility to decide what those conditions mean.

The software must not automate conclusions. It must not silently rank cities as objectively best. It must not convert symbolic complexity into a hidden score. It must not behave as an oracle. It must not replace the professional astrologer, the exploratory user, or the human act of interpretation. Its job is to expose structure; the human’s job is to judge.

This single rule gives the product its uniqueness. The platform is not just an astrocartography map, not a generic astrology suite, not a city recommender, and not a dashboard dressed in celestial imagery. It is an instrument for geographic symbolic search. A user can ask, “Where does this condition hold?” then inspect the answer at the level of coordinates, cities, saved locations, charts, overlays, and comparisons.

Cities are secondary human markers. They help users orient, shortlist, discuss, save, and compare. They are not the computational starting point. The computational subject is the Earth as a coordinate field evaluated through chart conditions.

---

## 1. Source Scope and Extraction Boundaries

This canon consolidates source blocks whose names or contents referenced concepts, philosophy, layers, stages, uniqueness, value, Web3/future variants, geometry, ontology, purpose, positioning, intentionality, symbolic structures, progressive reveal, rain, virga, and related conceptual frameworks.

The deeper extraction classified matched source blocks into the following concept families:

| Concept Family | Matched Blocks |
|---|---:|
| core_identity_and_market_position | 176 |
| future_web3_v2 | 166 |
| human_usage_and_workflows | 196 |
| layer_1_geometry | 185 |
| layer_2_ontology | 172 |
| layer_3_intent | 178 |
| layer_4_interpretation_ai | 192 |
| layer_5_experience | 155 |
| stage_reveal_systems | 176 |
| validation_and_guardrails | 187 |

The matched set confirms that the product concept is not a loose brand idea. It is an operating model. Geometry, ontology, intent, interpretation, and experience are distinct layers. Searchability depends on keeping those layers separate. Trust depends on never letting a downstream layer pretend to be an upstream truth source.

---

## 2. What the Platform Is

The platform is an astrological geography instrument. Its primary act is not interpretation but spatial revelation. It computes where chart conditions exist across geography, renders those conditions on a map, lets the user inspect any coordinate or city, and preserves selected explorations as reusable objects.

The product begins with a natal chart or client chart. From that chart, the system can compute relocation-specific facts at any coordinate. Instead of forcing the user to check one city at a time, the map lets them search for fields: planet-in-house regions, angle-in-sign regions, aspect-to-angle bands, exclusions, overlaps, and later additional governed condition families. This turns relocation astrology from isolated city lookup into structured geographic exploration.

The user does not need the app to say “this place is good.” The user needs the app to reveal where conditions are true, where they overlap, where unwanted conditions are absent, and which cities or locations live inside those fields. The app’s value lies in changing the search unit from isolated city to condition field.

### 2.1 Why this is unique

Traditional relocation workflows often begin with known cities or with line-based astrocartography conventions. This product begins with selected chart conditions and lets geography answer. The user can search for “Sun in 1st,” “Venus in 7th,” “ASC Libra,” or “Sun trine Ascendant,” and later combine them with exclusions such as “not Saturn in 4th.” The result is not just a line or a chart. It is an inspectable condition landscape.

This changes the cognitive workflow:

1. The user chooses symbolic conditions.
2. The map reveals where those conditions hold.
3. The user inspects locations inside or near those fields.
4. The user saves candidates and searches.
5. The user compares facts across locations.
6. The human interprets tradeoffs.

The uniqueness is not that astrology is mapped. The uniqueness is that chart conditions become searchable geography while human judgment remains intact.

### 2.2 What it is not

It is not a generic astrocartography clone. It does not reduce meaning to planetary lines without relocated chart context. It is not a generic astrology dashboard, because the map is not one widget among many; the map is the instrument face. It is not a travel app, because city desirability is not the product’s truth source. It is not an AI oracle, because AI remains optional, downstream, and subordinate to factual chart structure. It is not a scoring engine, because symbolic value depends on human intention.

---

## 3. How People Use It

### 3.1 Professional astrologer workflow

The professional begins with a client or chart record. They configure search conditions based on the client’s intention or the astrologer’s analysis. They search the map for regions where desired conditions hold. They inspect cities and arbitrary coordinates, save promising locations, exclude unwanted patterns, and compare selected candidates.

The professional may export a curated map or share selected overlays with a client. The client may inspect, zoom, and perhaps mute/solo layers, but the professional controls the symbolic framing. AI, if present, acts as an assistant that can suggest alternatives or organize comparisons; it does not override the astrologer.

### 3.2 Advanced self-guided user workflow

An advanced user may know what chart conditions they want. They use the map directly: choose conditions, search, inspect, save, compare, and decide. The app should not slow them down with over-explaining or AI pressure. Their core need is precision, replay honesty, and a calm interface.

### 3.3 Lay exploratory workflow

A lay user may start with intentions rather than technical astrology. Future AI or education can help translate intentions into possible search structures. Even then, the user must see and approve the conditions. The AI cannot silently decide what matters. The lay workflow still ends in human judgment: the user explores places, reads explanations, and chooses what resonates.

### 3.4 Comparison workflow

Comparison is not ranking by default. It is a side-by-side presentation of factual relocated chart conditions and user notes. A comparison may show why Location A better preserves one selected condition while Location B avoids a different excluded condition. It can help the user think. It must not declare a universal winner.

### 3.5 Saved investigation workflow

A saved investigation preserves semantic intent: selected conditions, chart context, viewport, settings snapshot, and rendered payload. It is not a dump of random renderer internals. Replaying a saved search should restore the user’s inquiry, not freeze a fragile visual accident.

---

## 4. The Five Structural Layers

The project’s conceptual architecture can be understood as five layers. These layers are not decorative taxonomy; they protect truth, usability, and human agency.

### 4.1 Layer 1 — Geometry and Factual Computation

Layer 1 is the factual substrate. It includes birth data, chart identity, coordinates, house system, zodiac mode, ephemeris calculations, angle geometry, truth grids, screen-space sampling, centerlines, per-point relocated chart facts, and condition membership. This is where the system decides what is true at a coordinate.

Layer 1 answers factual questions:

- What is the relocated Ascendant here?
- What is the relocated Midheaven here?
- Which house is the Sun in at this coordinate?
- Is Venus in the 7th here?
- Is the selected angle in the selected sign here?
- How close is this point to the selected aspect-to-angle exactness?
- Does this coordinate fall inside an excluded condition?

Layer 1 must be inspectable. The popup is the local truth anchor. Overlays must agree with point truth within the stated precision of the substrate. Any visual layer that contradicts Layer 1 must be corrected or labeled as provisional/debug.

Layer 1 does not interpret. It does not know whether Venus in 7th is “good” for this person. It knows whether the condition is present.

### 4.2 Layer 2 — Ontology, Vocabulary, and Settings

Layer 2 defines what kinds of questions the user can ask and how those questions are named. It includes condition types, variable cards, language registries, aspect families, orb defaults, zodiac or house-system settings, helper categories, professional dictionaries, and future ontology packs.

Layer 2 turns raw geometric capability into usable symbolic vocabulary. A condition such as `planet_in_house` is more than a UI row; it is a structured query type. A future ontology may let professionals expose different symbolic frameworks, but the ontology must not rewrite Layer 1 truth. It can define categories and defaults. It cannot make a coordinate true or false by rhetoric.

Layer 2 must remain versionable and replayable. Saved searches need settings snapshots because changing defaults later must not silently alter past investigations. Display labels are swappable; stable IDs are canonical.

### 4.3 Layer 3 — Intent and Workflow Framing

Layer 3 is the human inquiry. It includes the user’s purpose, constraints, move-toward and move-away-from themes, professional strategy, client context, saved search names, notes, comparison intention, and why a particular condition set matters.

This layer is where the product becomes useful without becoming authoritarian. The same chart condition may be desirable or undesirable depending on intention. A user seeking public visibility may evaluate a location differently from a user seeking retreat. A professional may deliberately choose a difficult condition for maturity or discipline. The app must preserve that contextuality.

Layer 3 can organize searches and comparisons. It cannot replace interpretation. It creates the frame for human evaluation.

### 4.4 Layer 4 — Interpretation and AI Assistance

Layer 4 is optional interpretation, education, AI assistance, symbolic explanation, tradeoff language, professional assist, consumer intake, and future generated summaries. It must remain subordinate to Layers 1–3.

AI may explain. AI may suggest alternatives. AI may help a lay user understand terms. AI may notice that a selected condition is mostly over ocean and suggest related conditions near populated places. AI may help compare factual differences under user-stated intent. AI may not become the final authority.

Layer 4 has special risks: flattery, deterministic overclaiming, invented biography, comfort-spinning difficult placements, hidden ranking, and oracle behavior. Therefore all Layer 4 output must label fact versus interpretation and preserve symbolic humility.

### 4.5 Layer 5 — Experience and Visual Atmosphere

Layer 5 is the product’s felt surface: calm, premium, restrained, contemplative, long-session comfortable, map-first, emotionally non-interfering. It includes visual language, typography, spacing, motion, drawer behavior, brand posture, and interaction tone.

Layer 5 supports imagination without competing with it. The interface should create a safe room for exploration. It should not hook users with neon, dopamine mechanics, aggressive alerts, cosmic hype, or debug clutter. The emotional intensity belongs to the user’s discovery and the symbolism, not to the chrome.

Layer 5 must never override Layer 1. Beauty that lies is worse than rough honesty.

---

## 5. Data Mapping Constraints Across Layers

The layers must communicate through explicit mappings.

Layer 1 produces factual outputs: point facts, masks, polygons, centerlines, aspect distances, and chart facts. Layer 2 names those facts through condition types, registries, and settings. Layer 3 stores why the user searched and what context matters. Layer 4 may generate interpretive text based on explicit facts and stated intent. Layer 5 renders the system in a calm, legible, emotionally non-coercive way.

The forbidden mapping is upward contamination: Layer 5 styling cannot change Layer 1 membership. Layer 4 AI cannot invent Layer 1 facts. Layer 3 desire cannot make a condition true. Layer 2 vocabulary cannot silently redefine a saved search without versioning. Layer 1 cannot decide meaning.

A correct product interaction might look like:

- Layer 3: user wants “more public vitality, less home pressure.”
- Layer 2: interface maps this into reviewed conditions such as Sun angular or Sun in 1st, and exclude Saturn in 4th.
- Layer 1: engine computes where these conditions hold.
- Layer 5: map renders overlaps and exclusions legibly.
- Layer 4: AI optionally explains tradeoffs and alternatives, clearly labeled as interpretation.

---

## 6. Stage and Reveal Systems

The project distinguishes truth computation from theatrical animation. Stage/reveal concepts are allowed only when they respect the truth substrate.

### 6.1 Progressive truth reveal

A legitimate stage reveal shows real computation stages: coarse grid, adaptive refinement, truth sample count, stable cells, final raster, or validated overlay generation. It must be tied to actual engine artifacts. It cannot be random dots, fake scanning, timed progress bars, or symbolic theater detached from computation.

### 6.2 Rain and Virga concepts

Rain and Virga are future temporal visual grammars. Rain represents discovery or reveal of selected conditions. Virga represents partial/aborted sibling discovery: ghost implications that fade before completion. These concepts are visually and philosophically valuable, but they are not active implementation requirements.

The key canon is that reveal must not lie. If Rain/Virga returns, it should be driven by already-computed truth or explicitly act as restrained reveal pacing over known truth. It must not pretend random particles are solving the map.

### 6.3 Stage reveal versus loading animation

A loading animation says “wait.” A stage reveal says “this is the level of truth currently available.” The product’s future reveal language must choose the second path or not use reveal at all.

### 6.4 Active boundary

Rain/Virga, broad animation systems, and stage theater remain future inventory until truth substrate, performance, and map readability are stable. The active system definition does not depend on them.

---

## 7. Unique Value Proposition

The platform’s value is the combination of:

1. **Condition-first search.** Users search for chart conditions geographically rather than checking known cities one by one.
2. **Map-first instrument design.** The map is the main experience, not a thumbnail inside a dashboard.
3. **Coordinate truth.** Arbitrary points can be inspected; cities are helpers, not the search universe.
4. **Human judgment preservation.** The system reveals structure without claiming final meaning.
5. **Professional sovereignty.** Astrologers can use the tool without surrendering interpretation to AI.
6. **Saved inquiry structure.** Searches, favorites, comparisons, and shared views preserve meaningful work.
7. **Layer separation.** Geometry, ontology, intent, interpretation, and experience do not collapse into each other.
8. **Truth-first visual doctrine.** Overlays must remain accountable to popups and validation.
9. **Future assistive intelligence.** AI can expand discovery while remaining governed and subordinate.
10. **Contemplative trust.** The product can be used for long sessions without emotional noise.

This is why the product is not simply “astrocartography with nicer UI.” It changes the epistemology of relocation search.

---

## 8. Conceptual Non-Goals

The active concept excludes automatic city optimization, universal ranking, deterministic advice, AI oracle flows, social/engagement loops, speculative Web3 ownership systems, broad consumer prediction, gamified map discovery, final visual style marketplaces, and unsupported symbolic scoring. These can be explored later only if they preserve the constitutional rule.

---

## 9. Active Definition Checklist

A feature belongs in the active core only if it:

1. Reveals structure without stealing judgment.
2. Makes chart conditions visible, searchable, or inspectable.
3. Keeps Layer 1 factual truth separate from interpretation.
4. Preserves stable IDs and settings snapshots where replay matters.
5. Supports city inspection without making cities the computation source.
6. Avoids hidden ranking.
7. Avoids AI authority over human interpretation.
8. Keeps map readability and popup truth intact.
9. Fits a coherent chart/client/saved-object workflow.
10. Has a validation or audit path.

If a feature fails this checklist, it belongs in future inventory or should be rejected.

---

## Future Conceptual Excellence Inventory

This inventory tracks conceptual expansions without making them active definitions.

### Web3 and ownership variations

- Possible future user-owned ontology packs.
- Portable chart/search objects with provenance.
- Shared professional templates or dictionaries.
- Client-authorized access layers.
- Cryptographic or decentralized audit trails only if a real product need emerges.

### Version 2.0 product variants

- Consumer guided relocation journey.
- Professional collaborative workspace.
- Education/certification layer.
- Client-facing shared exploration mode.
- Multi-intention comparison portfolios.
- Advanced ontology libraries.
- Optional AI-assisted intake and comparison summaries.

### Stage and reveal evolution

- Rain reveal for selected conditions.
- Virga sibling-condition ghosting.
- Truth-driven progressive refinement display.
- Show-calculation mode.
- Debug-to-education bridge.
- Reduced-motion and professional fast-mode controls.

### Expanded symbolic intelligence

- Intent-to-condition translation with human review.
- Alternative placement discovery.
- Tradeoff-aware comparison assistant.
- Archetypal integrity evaluation.
- Human-edited AI reports.
- Professional sovereignty controls.

### Conceptual governance

- Layer-version registry.
- Ontology-version registry.
- Interpretation safety rubrics.
- Web3 feasibility review.
- Future AI model-version registry.
- Concept drift audits.



---

## Appendix A — Concept Source Index

### A.1 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/AI_WORKFLOW_GOVERNANCE.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 14272; SHA-12: `570f3cca823a`; score: 59
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Concept signals:
  - # AI Workflow Governance Protocol
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in writing.
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisible engineering inte…
  - ## Ghost Boss Governance Doctrine
  - Every phase closeout must ask whether it introduced or exposed:

### A.2 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/CURRENT_RENDERING_DOCTRINE.md`
- Categories: human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 7576; SHA-12: `0b4a58929157`; score: 67
- Key headings: Current Rendering Doctrine — Summary; The stack (top to bottom); Non-negotiables; Legacy `/search-regions` Truth Grid; Phase-2 cache (product substrate); Evidence bundle (read in this order); Documents marked SUPERSEDED (archaeology preserved); Warnings against backsliding; Remaining gaps (structural, not aesthetic); Recommendation
- Concept signals:
  - # Current Rendering Doctrine — Summary
  - describe geographic-grid sampling, polygon-reveal pacing, or global
  - | Layer | Role | Status |
  - | **Brute force** | Validation wall. Every optimisation must match it cell-for-cell (or pixel-for-pixel on screen). | Canonical control specimen |
  - | **Screen-space truth** | Production sampling axis for **visible overlays**. Classify what the user actually sees. | Canonical for rendering |

### A.3 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DEFERRED_EXCELLENCE_REGISTRY.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 30563; SHA-12: `8fdc70fc996d`; score: 135
- Key headings: Deferred Excellence Registry; Purpose; Cross-Cutting Doctrine; Status Legend; 1. Renderer / Topology Improvements; 1.1 Stable component IDs across zoom/pan; 1.2 Graph / global path solver; 1.3 Canonical-default migration; 1.4 Continuous topology extraction refinement; 1.5 Subpixel/edge extraction refinement for narrow-orb ASC; 1.6 Seam-aware topology continuity; 1.7 Signed-distance-field experiments
- Concept signals:
  - Date: 2026-05-22. Preservation-of-intent pass. Read-only architectural memory.
  - This registry captures everything we know we *could* improve in the renderer, architecture, UX, product, and reliability stack — and have intentionally deferred to protect MVP velocity. Its primary purpose is **not** to accumulate shiny feature ideas. Features are comparatively e…
  - The primary purpose is preserving hidden robustness and institutional memory: invisible infrastructure improvements, architecture refinements, reliability upgrades, governance ideas, performance optimizations, renderer trust improvements, scaling concerns, cache/system improvemen…
  - These are the things founders and AI systems tend to forget because users do not directly see them, they do not demo well, short-term success can mask their absence, and commercial pressure naturally favors visible product work. The registry exists to preserve long-term engineeri…
  - Short rule: when choosing what to capture here, prefer invisible engineering and infrastructure concerns over visible feature wishes. Feature wishes may be listed when they carry trust, platform, or operational consequences, but the registry's center of gravity is hidden robustne…

### A.4 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DOCTRINE_INDEX.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 154
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Concept signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…

### A.5 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/EXECUTIVE_TRANSFER_BRIEF_NEXT_CHAT.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9792; SHA-12: `d91200d72161`; score: 68
- Key headings: Executive Transfer Brief For Next Chat; 1. Current Project State; 2. What Is Considered Solved; 3. What Is Intentionally Deferred; 4. Current Renderer Status; 4.1 Renderer handoff state; 5. Governance Status; 6. Productization Status; 7. Immediate Next Recommended Phases; 8. Strategic Warnings; 9. Key Philosophical Doctrines; 10. How Future AI Should Behave
- Concept signals:
  - Purpose: human/operator bootstrap for the next major AI session. This is not archaeology, not raw continuity, and not a replacement for `ai_context/archaeology/RAW_CONTINUITY_VOLUME_7.md`. It is the short strategic operating brief.
  - The project has moved from renderer research into product platform construction. The relocation map now has enough validated rendering confidence to support Phase 2 product work: chart library, saved views, handoff links, deep links, onboarding, future accounts, and professional …
  - The current product direction is focused: relocation astrology, map-based discovery, chart persistence, professional workflows, high-trust UX, and contemplative visual exploration. It is not a generic astrology suite or social/spiritual platform.
  - - Screen-space truth and adaptive refinement have proven the future truth substrate.
  - - Governance artifacts, continuity volumes, and deferred-excellence tracking are now project infrastructure.

### A.6 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_1_2_EXTRACTION_AUDIT.md`
- Categories: human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 31222; SHA-12: `99e7cbcf42db`; score: 217
- Key headings: Phase 1.2 Extraction Audit; Concise Findings; Files Inspected; Production and backend; Sandboxes; Validation / capture scripts; Doctrine used as constraints; Current Rendering Entry Points; Production renderer; Backend endpoints; Sandbox renderers; Validation harnesses and capture scripts
- Concept signals:
  - > scheduler implementation. No aura/reveal/animation implementation. No
  - begins. It is intentionally conservative: the first extraction target
  - must not change behavior and must not mix the legacy production overlay
  - polygon/vector layers.
  - - `/screen-pixel-truth` is validated and used by sandboxes and capture

### A.7 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 58355; SHA-12: `c6ef18d0c316`; score: 134
- Key headings: Phase-2 Cache Integration — Architecture & Implementation Planning; 0. Where this fits; 1. Grounding — what is true today, measured; 1.1 Sandbox state (measured, not asserted); 1.2 What this means; 1.3 Hard architectural finding — substrate mismatch; 2. Production Scheduler Architecture; 2.1 Single-active-job model; 2.2 Foreground vs background queues; 2.3 Cancellation / interruption behaviour; 2.4 Priority escalation rules; 2.5 Viewport ownership
- Concept signals:
  - > **Status:** Architecture and planning doctrine. Design only. No code
  - > **Stability:** Slow. Implementation details may rev; design rules here
  - cache orchestrator that preserves correctness, user responsiveness,
  - | Layer | Doc | Role |
  - | Substrate governing laws | `docs/PHASE_C_RENDERING_ARCHITECTURE.md` | Substrate-level cache doctrine (§5) |

### A.8 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_IMPLEMENTATION_PROTOCOL.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 54962; SHA-12: `c32fcebbd584`; score: 213
- Key headings: Phase-C Implementation Protocol; Operational constitution for landing the validated architecture without future chaos; 0. Where this fits; 1. Implementation Phase Breakdown; Phase 1.1 — Documentation alignment (no code); Phase 1.2 — Archaeology fencing (low-risk cleanup); Phase 1.3 — Scheduler extraction (no behaviour change); Phase 1.4 — Substrate adapter scaffold (legacy-only); Phase 1.5 — Canonical substrate wiring (flag-gated); Phase 1.6 — Scheduler/cache wiring on canonical (flag-gated); Phase 1.7 — Parity validation harnesses; Phase 1.8 — Default flip + stabilisation
- Concept signals:
  - ## Operational constitution for landing the validated architecture without future chaos
  - > **Status:** Operational doctrine. Implementation planning only.
  - > `docs/process/*` and `ai_context/memory_workflow.md`.
  - > meta-governance cycle. Does not override slow doctrine.
  - > behaviour changes. Telemetry infrastructure. Bureaucracy.

### A.9 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_PRODUCTION_MIGRATION_PLAN.md`
- Categories: human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 64644; SHA-12: `af96b1d10c2e`; score: 234
- Key headings: Phase-C Production Migration Plan; Legacy overlay pipeline → canonical screen-space adaptive substrate; 0. Where this fits; 1. Legacy vs Canonical Substrate Audit; 1.1 The legacy overlay pipeline (what is in production today); 1.2 The canonical screen-space substrate (validated, sandbox-proven); 1.3 Semantic differences; 1.4 Rendering differences (visible); 1.5 Cache compatibility implications; 1.6 Validation differences; 1.7 Hidden assumptions; 1.8 Likely regression risks (ranked)
- Concept signals:
  - > **Status:** Migration architecture and planning doctrine. Design
  - validated screen-space adaptive substrate (`/screen-pixel-truth`).
  - | Layer | Doc | Role |
  - | Current rendering doctrine | `docs/CURRENT_RENDERING_DOCTRINE.md` | Status board of the stack |
  - | Inputs | birth params, `house_conditions`, `angle_sign_conditions`, `aspect_overlay`, `resolution` (default 1.5°), `generation_mode` (`truth_grid` or contour), `truth_grid_resolution` (0.75°), `truth_grid_boundary_refine` |

### A.10 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_RENDERING_ARCHITECTURE.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 47288; SHA-12: `3744bf667647`; score: 268
- Key headings: Phase C — Rendering Substrate Architecture (Governing Laws); 0. Where this document sits; 1. Canonical Rendering Truths; 1.1 The four absolute statements; 1.2 Screen-space truth doctrine; 1.3 Adaptive refinement as production substrate; 1.4 Why visible output is canonical; 1.5 Globe truth vs screen truth; 2. Convergence Strategy; 2.1 Convergence is the contract; sample count is not; 2.2 Targeted escalation, never global slowdown; 2.3 Refinement economy — *truth where unstable*
- Concept signals:
  - > **Adopted draft:** 2026-05-21 (same-day as the rendering doctrine reset).
  - > **Stability:** Slow. Implementation details around this doctrine may rev;
  - > **Purpose:** Define the governing laws of the *rendering civilization* so
  - > future agents, contributors, and reviewers cannot quietly regress toward
  - > renderer-wide slowdown for local instability, visual mush, geometry-first

### A.11 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PROJECT_CONTINUITY_INDEX.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, future_web3_v2, validation_and_guardrails
- Characters: 2667; SHA-12: `303dae8aa89c`; score: 15
- Key headings: Project Continuity Index; Canonical Governance Docs; Canonical Archaeology Docs; Canonical Renderer Doctrine Docs; Deferred Excellence; Validation Narratives; Continuity Volume Convention; Recommended Future-AI Ingestion Order
- Concept signals:
  - Purpose: short entry point for future AI/human rehydration. This file points to canonical governance, archaeology, renderer, deferred-excellence, and validation memory without replacing those sources.
  - - `docs/AI_WORKFLOW_GOVERNANCE.md` — mandatory closeout, Ghost Boss governance, continuity volume protocol, hidden robustness review.
  - - `validation/narratives/renderer_readiness_decision_gate.md` — Phase 1.19 blocker taxonomy and anti-death-spiral doctrine.
  - - `docs/process/archaeology_and_synthesis_workflow.md` — raw archaeology intake and synthesis workflow.
  - - `memory_archaeology_raw/README.md` — raw intake rules.

### A.12 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 264
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Concept signals:
  - # AI Interpretation Truthfulness Doctrine v1
  - **CANONICAL** for **future** AI-assisted interpretation layers — not current product scope.
  - **Scope:** Documentation only. Defines interpretive discipline, forbidden patterns, and a future review architecture. **No AI implementation in dumb Web 2.0 v1.**
  - - `docs/ai_constitution_and_review_architecture.md` — layered governance, anti-patterns, reviewer duties
  - - `docs/constitutional/epistemic_integrity_and_symbolic_humility.md` — honest uncertainty, symbolic restraint

### A.13 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai_constitution_and_review_architecture.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 13119; SHA-12: `d6ae8f16c65e`; score: 214
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Concept signals:
  - **Status:** Internal **governance architecture** for future AI-assisted interpretation—not a shipping spec, not marketing, not ethics theater.
  - **Tone contract:** Structured, skeptical, operational. **Anti-handwave, anti-hype.**
  - **Doctrine stack (read before changing AI behavior):**
  - - **`docs/intentionality_and_symbolic_constraints.md`** — fate/agency, tradeoffs, intentionality, AI governance implications.
  - - **`docs/brand_and_experience_foundations.md`** — **Interpretive language and emotional transparency**; **Interpretive integrity and archetypal honesty**; emotionally **non-interfering** design.

### A.14 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/client_chart_data_model_v1_2026-05-29.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 35789; SHA-12: `795365723409`; score: 199
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Concept signals:
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - - how behavioral facts may be captured **without interpretation**,
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`. Record management is **supporting infrastructure**, not the center of gravity.

### A.15 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 20953; SHA-12: `db53e1e91227`; score: 71
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Concept signals:
  - # Web 2.0 Account / Chart Workflow Architecture — Review Proposal
  - **ARCHITECTURE REVIEW — aligned with Map-First Product Doctrine (2026-05-31)**
  - **Date:** 2026-05-29 (original); **doctrine alignment:** 2026-05-31
  - **Scope:** Web 2.0 account/chart workflow architecture. Not implementation. Not schema migration.
  - **Governing doctrine:** `docs/constitutional/map_first_product_doctrine_v1.md` — supersedes dashboard-centric recommendations in v1.0–v1.1 of this review.

### A.16 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/aspect_aura_defaults.md`
- Categories: human_usage_and_workflows, layer_1_geometry, layer_5_experience, stage_reveal_systems, future_web3_v2
- Characters: 1291; SHA-12: `2e467a76fee6`; score: 0
- Key headings: Aspect aura defaults (approximate display); Authority; Default screen weights (Leaflet `weight`, approximate); NOT done here
- Concept signals:
  - - No latitude-aware geographic σ for aura width (future refinement).

### A.17 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/brand_and_experience_foundations.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 155
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Concept signals:
  - # Brand and Experience Foundations
  - **What this is:** A **foundations** note for tone, judgment, and honesty in the product experience.
  - **What this is not:** A brand book, logo spec, marketing narrative, campaign, or visual identity system. **No** speculative public branding.
  - **Important:** The emotional and atmospheric goals below are **experiential design constraints**—they govern how future UX and rendering choices should **feel** and **function**. They are **not** marketing fluff; they are institutional memory for product judgment.
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).

### A.18 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/cartographic_language_and_city_rendering.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 18608; SHA-12: `33b4db97eb55`; score: 104
- Key headings: Cartographic language and city rendering; 0. Basemap or tile strategy change ⇒ full visual identity re-test; 1. Map label language vs app language; 2. Provider evaluation (map + search); 2.1 Dimensions to score (required for any serious comparison); 2.2 Qualitative stack comparison (high level); 2.3 “Extra hour” vs “multi-day / multi-week”; 2.4 Effort bands for “whole solution” slices; 2.5 GeoNames bridge first vs “long-term now”; 3. City visibility under overlays (hard constraint); 4. City density and ranking (rendering); 5. Clickability: city vs blank map
- Concept signals:
  - **Status:** Planning and constraints for **basemap language**, **city visibility**, and **interaction clarity**. Complements `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, and `docs/map_and_overlay_design_research.md`.
  - **Out of scope:** Aspect-to-angle **glow/aura** (not implemented; do not conflate with city-layer work).
  - **Institutional rule:** If the team changes **map provider**, **tile format** (raster → vector, host swap, style swap), or **label policy**, we must **re-validate the whole visual system**—not assume the current look “carries over.”
  - | **Emotional tone** | “Instrument not dashboard” (`brand_and_experience_foundations.md`) can drift toward **gadget** or **murky** if basemap + overlay clash. |
  - | **Light / dark theme** | **Do not** assume one overlay palette works; plan **paired tokens** when dark mode is real. |

### A.19 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/README.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 54
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Concept signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - layer sovereignty,
  - - truth integrity,
  - - ontology boundaries,

### A.20 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ai_conversational_modes.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 2887; SHA-12: `b796e2065486`; score: 32
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Concept signals:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - exploratory feature concepts,
  - - prevent future contradictions,
  - This document should be periodically reviewed and updated as:

### A.21 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/constitutional_ingestion_checklist.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 46
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Concept signals:
  - This document is operational infrastructure.
  - - track doctrine ingestion,
  - Update this document whenever:
  - - doctrine evolves,
  - - or roadmap structure changes.

### A.22 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/conversational_discovery_and_intentionality.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 4218; SHA-12: `c7b5d8b9fc8e`; score: 52
- Key headings: Conversational Discovery And Intentionality; Status; Purpose; Core Principle; User intentionality is sovereign.; Intentionality Discovery; Examples; Archetypal Exploration; Example Exploratory Style; Intentionality Strength; Examples; Layer Relationship
- Concept signals:
  - # Conversational Discovery And Intentionality
  - The principles of:
  - - intentionality discovery,
  - This document defines how the platform should:
  - - discover user goals,

### A.23 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/epistemic_integrity_and_symbolic_humility.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 3739; SHA-12: `242cc62cfae5`; score: 39
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior; Good Behavior; Collaborative Discovery
- Concept signals:
  - - and anti-bullshit doctrine.
  - All AI and interpretive systems must follow these principles.
  - This document establishes the philosophical and operational rules governing:
  - - interpretation,
  - - symbolic restraint,

### A.24 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/future_excellence_vs_future_feature_excellence.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 34
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Concept signals:
  - # Future Excellence vs Future Feature Excellence
  - - canonical architectural principles,
  - - future-oriented planning,
  - Some implementation concepts are exploratory and subject to revision.
  - This document should be periodically reviewed for:

### A.25 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/implementation_governance_and_ai_workflow_protocol.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3988; SHA-12: `b127e5c52050`; score: 40
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Concept signals:
  - # Implementation Governance And AI Workflow Protocol
  - - AI workflow behavior,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - This project intentionally rejects:

### A.26 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer4_optimization_and_exploration_doctrine.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4341; SHA-12: `289b4552320f`; score: 74
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Concept signals:
  - # Layer 4 Optimization And Exploration Doctrine
  - - canonical Layer 4 principles,
  - - exploratory optimization philosophy,
  - - and future-facing interaction concepts.
  - Core Layer 4 boundaries are canonical.

### A.27 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer_sovereignty_and_forbidden_crossings.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 100
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Concept signals:
  - # Layer Sovereignty And Forbidden Crossings
  - It defines hard constitutional boundaries between layers.
  - These rules are mandatory architectural constraints.
  - - layer sovereignty,
  - The purpose is to prevent:

### A.28 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layered_symbolic_intelligence_architecture.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4801; SHA-12: `5242de0598f3`; score: 120
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Concept signals:
  - # Layered Symbolic Intelligence Architecture
  - It defines the constitutional layer architecture of the platform.
  - All future systems must respect:
  - - layer sovereignty,
  - - and truth integrity.

### A.29 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/map_first_product_doctrine_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 77
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Concept signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.

### A.30 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/mvp_beta_and_future_feature_roadmap.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4767; SHA-12: `c904d8af5d1e`; score: 85
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes; Stage 2 — Professional Beta; Goal
- Concept signals:
  - # MVP, Beta, And Future Feature Roadmap
  - - and future feature concepts.
  - not immutable constitutional doctrine.
  - This roadmap should be periodically reviewed for:
  - # Core Principle

### A.31 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 56
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Concept signals:
  - # Ontology Plugin And Symbolic Framework Architecture
  - - canonical architectural principles,
  - - tentative future architecture,
  - - exploratory feature concepts,
  - - prevent future contradictions,

### A.32 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_mode_vs_lay_mode_strategy.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3492; SHA-12: `c166907d611f`; score: 66
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Concept signals:
  - - strategic UX philosophy,
  - - and future product direction.
  - Core principles are canonical.
  - This document should be periodically reviewed for:
  - - professional workflow needs,

### A.33 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_trust_and_ai_behavior_doctrine.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 106
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Concept signals:
  - # Professional Trust And AI Behavior Doctrine
  - This document defines how AI systems inside the platform must behave.
  - - symbolic restraint,
  - The AI must never behave like:
  - # Core Principle

### A.34 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/purification_audit_framework.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3639; SHA-12: `a43528565790`; score: 64
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Concept signals:
  - - contaminate neighboring layers,
  - - or violate constitutional doctrine.
  - # Core Principle
  - A purification audit is a structured review of:
  - - Does this system still belong to its declared layer?

### A.35 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/relocation_strategy_framework.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 2978; SHA-12: `5542c6b3c8b9`; score: 37
- Key headings: Relocation Strategy Framework; Status; Purpose; Core Principle; Subtractive relocation comes before additive optimization.; Subtractive Relocation; Additive Relocation; Strong Relocations Often Do Both; Tradeoff Reality; Archetypes Are Contextual; Optimization Delusion; Layer 4 Behavior
- Concept signals:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - exploratory feature concepts,
  - - prevent future contradictions,
  - This document should be periodically reviewed and updated as:

### A.36 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_and_renderer_sovereignty.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 3826; SHA-12: `edda50b52a22`; score: 42
- Key headings: Runtime And Renderer Sovereignty; Purpose; Core Principle; Rendering must never alter truth.; Runtime Sovereignty; Renderer Sovereignty; Hydration Boundaries; Sandbox Boundaries; Observer Limitations; Renderer Substrate Integrity; Progressive Refinement; Ambiguity And Implication
- Concept signals:
  - # Core Principle
  - ## Rendering must never alter truth.
  - They do not compute symbolic reality.
  - They do not own:
  - - symbolic interpretation,

### A.37 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_build_sequence_and_timeline.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4934; SHA-12: `12aea4343437`; score: 68
- Key headings: Runtime Build Sequence And Timeline; Status; Maintenance Notes; Purpose; Core Principle; Build irreversible foundations first.; Phase Family 1 — Truth And Runtime Foundation; Goal; Includes; Status; Phase Family 2 — Renderer Reintegration; Goal
- Concept signals:
  - not immutable doctrine.
  - This document should be periodically reviewed for:
  - - AI layering,
  - - and future expansion.
  - The purpose is to:

### A.38 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/symbolic_language_style_guide.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems
- Characters: 1703; SHA-12: `11e6dd9bdb1a`; score: 17
- Key headings: Symbolic Language Style Guide; Purpose; Core Principle; Preferred Style; Avoid; Good Examples; Bad Examples; Archetypal Precision; Symbolic Humility; Constitutional Goal
- Concept signals:
  - This document defines how symbolic language should be expressed by the platform.
  - # Core Principle
  - The system should sound:
  - It should not sound:
  - The AI should discuss:

### A.39 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 3360; SHA-12: `554add110fa4`; score: 60
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Concept signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - # Layer Distinction
  - Truth belongs primarily to Layer 1.
  - Astrological fact belongs primarily to Layer 2.

### A.40 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_app_shell_handoff_audit_v1_2026-05-30.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_4_interpretation_ai, layer_5_experience, future_web3_v2, validation_and_guardrails
- Characters: 16528; SHA-12: `a7754235e25c`; score: 24
- Key headings: Genie → App Shell Handoff Audit v1; Status; Executive summary; A. Current Genie contract; Emitter; Trigger; Payload shape (as implemented); Variable semantics (canonical); Output destinations today; Not emitted / not connected; B. Current app shell contract; Navigation context (in-app)
- Concept signals:
  - **Three distinct states (do not conflate):**
  - Map **default user path** still uses legacy DOM (Find regions). App shell handoff is **receive-only context** — no Genie payload.
  - There is **zero wired handoff** between Genie and app shell, or between shell navigation and automatic Genie search on map load. `legacyCompatibility` is emitted for diagnostics; map engine adapter **must not** use it as execution input.
  - "layerControls": {
  - | Search truth | `complete` and `experimental` variables with `enabled: true` |

### A.41 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_render_payload_v1_2026-05-30.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, future_web3_v2, validation_and_guardrails
- Characters: 27674; SHA-12: `7e997018eed9`; score: 64
- Key headings: Genie Render Payload Contract v1; Status; Purpose; Architectural doctrine; Language stability doctrine; Principles; Therefore; Top-level payload; Field notes; Render immutability; Future references (not defined here); Variable object
- Concept signals:
  - **CANONICAL** for the payload emitted when the Genie user presses **Search Map** (render / search submit).
  - **Scope:** Documentation / contract only. Defines shape, semantics, legacy adapter rules, and examples. Not implementation.
  - Define the **canonical, immutable snapshot** produced at Genie render time. This payload is the **search truth** handed to the map workspace, history, pin, and (later) save flows.
  - The Genie editor may hold **live, mutable card state**. Render freezes that state once. Downstream systems must treat the rendered payload as authoritative for “what was searched,” not the live card DOM.
  - # Architectural doctrine

### A.42 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/variable_card_language_v1_2026-05-30.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 15184; SHA-12: `bde701502163`; score: 69
- Key headings: Variable Card Language Contract v1; Status; Purpose; Core doctrine; Canonical internal type IDs; Language registry concept; Composition rule; Registry ownership; Snapshot rule (Saved Explorations); Beta display label candidates; `planet_in_house`; `angle_in_sign`
- Concept signals:
  - **CANONICAL** for Genie variable-card **user-facing language** — labels, shorthand, dropdown copy, and presentation tokens.
  - **Scope:** Documentation / contract only. Defines a modular language layer. **Not final branding.**
  - - `docs/contracts/genie_render_payload_v1_2026-05-30.md` — stable type ids, `variables[].label` snapshots, language stability doctrine
  - Define the **user-facing language system** for Genie variable cards so that:
  - # Core doctrine

### A.43 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/current_sidebar_ux_audit.md`
- Categories: human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4992; SHA-12: `c07666b5828f`; score: 9
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces; 9. Condition model — **next structural UX step (documented)**; 10. Location search placement (documented)
- Concept signals:
  - **Intent:** Describe friction, record implemented fixes, and flag **documented-only** next steps (no redesign commitment).
  - - **`#renderStatus` / `#debugStatus`:** gated on `?debugGeometry` — unchanged.
  - **Behavior goal:** first row may default to planet-in-house, but users should eventually run **only** angle-in-sign or **only** aspect-to-angle without dummy planet rows.
  - **Engineering note:** needs coordinated **API/payload** and validation work later—**do not** half-migrate UI alone.
  - ## 11. First-use onboarding (implemented + future)

### A.44 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/local_first_data_objects_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 8758; SHA-12: `90256838acac`; score: 73
- Key headings: Local-First Data Objects v1; Status; Purpose; Architectural boundary; Entity glossary; ProfessionalAccount; Client; BirthProfile; RelocatedChart (future durable object); Place; FavoriteCity; OverlayCondition
- Concept signals:
  - Defines **product-layer entities**, **persistence boundaries**, and **local-first scaffold rules**. Not a database schema. Not implementation.
  - **Reads with:** `docs/relocation_app_product_roadmap.md` §8 (Saved Object Taxonomy, Phase 2.x), `docs/geocoder_and_city_identity_strategy.md`, `docs/constitutional/runtime_and_renderer_sovereignty.md`, `docs/product_workflows/professional_non_ai_workflow_v1.md`.
  - - renderer output becoming durable truth,
  - - Layer 2 settings silently rewriting Layer 1 records.
  - │  PRODUCT RECORDS (local-first → future sync)            │

### A.45 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/local_product_store_v2.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 2604; SHA-12: `0fee91b48aed`; score: 4
- Key headings: Local Product Store v2; Status; Purpose; File location; Python module; Validation rules; Scripts; Explicit non-goals (Phase 3.0a); Rollback; Revision
- Concept signals:
  - Runtime smokes write to **temp paths** only. Do not promote this file to product storage without explicit migration approval.
  - | `save_investigation(...)` | Requires `settings_snapshot` (defaults from `user_settings`) |
  - ## Validation rules
  - - `_storage` must be `TEMPORARY_LOCAL_SCAFFOLD`
  - - `storage_schema_version` must be `2`

### A.46 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/supabase_schema_sandbox_plan_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, future_web3_v2, validation_and_guardrails
- Characters: 16155; SHA-12: `8fac31540a5b`; score: 60
- Key headings: Supabase Schema Sandbox Plan v1; Status; Explicit non-goals (current phase); Architectural boundary; 1. Proposed table list; 2. Columns per table; `professional_accounts`; `clients`; `birth_profiles`; `places`; `saved_charts`; `saved_investigations`
- Concept signals:
  - **Reads with:** `docs/data_model/local_first_data_objects_v1.md`, `docs/future/birth_time_uncertainty_and_confidence_doctrine.md`, `validation/narratives/phase2_3_saved_investigation_replay.md`, `library/library.json` (legacy scaffold).
  - Supabase is a **schema mirror / future sync target** only.
  - │  PRODUCT RECORDS (local-first → future Supabase sync)   │
  - │  RENDERER / DISPLAY (never persisted as truth)          │
  - | 1 | `professional_accounts` | Professional owner (future auth subject; no auth now) |

### A.47 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/design/brand_visual_language_and_design_doctrine.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 73
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Concept signals:
  - # Brand, Visual Language, and Design Doctrine
  - Consolidates **brand foundations**, **visual epistemology**, and **restrained premium language** for the professional non-AI MVP. Not a logo guide. Not marketing.
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - - calm, restrained, inspectable, premium, trustworthy, professional.
  - - mystical rainbow dashboard,

### A.48 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 59
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Concept signals:
  - # Birth Time Uncertainty and Confidence Doctrine
  - Defines **epistemic tiers**, **user-facing honesty**, **data recording**, and **engine behavior boundaries** for uncertain birth times. Not implementation. Not rectification software spec.
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `validation/narratives…
  - - lay users often know approximate times only,
  - - AI intake may help later — **MVP must handle tiers without AI**.

### A.49 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/layer5_experiential_education_through_travel_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 86
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Concept signals:
  - # Layer 5 — Experiential Education Through Travel
  - **FUTURE ONLY — QUARANTINED**
  - **Layer:** 5 — Experiential education (meaning-making through lived experience)
  - **Dependency:** Requires mature AI guidance, relocation exploration substrate, and user observation capture — **after** standalone Web 2.0 facts-first product is proven.
  - **Reads with (boundary context only):** `docs/ux/2026-05-29_application_journey_architecture_v1.md` §Future Rooms, `docs/constitutional/layer_sovereignty_and_forbidden_crossings.md`.

### A.50 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_and_city_identity_strategy.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 36
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Concept signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - ## 1. Doctrine: city search is core systems engineering
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`). The map binds **h…
  - Current prototype list search (`cities.js`) is a **stand-in** only: **name, lat/lng, population (and minimal fields)**—**no reliable country/admin**, **no alternate names**, **no stable place IDs**, and **no** trustworthy global ranking (e.g. Paris, France vs Paris, Texas; London…
  - - The user should **choose from ranked results**, not depend on **mystery freeform** “first match” resolution (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`; Chunk 4.1: disambiguation **before** ML ranking).

### A.51 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_dataset_feasibility.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 16429; SHA-12: `6ba544bcfafd`; score: 30
- Key headings: Geocoder dataset feasibility (planning pass); 1. Summary recommendation; 2. Option-by-option evaluation; 2.1 GeoNames — `cities500` / `cities1000` / `allCountries`; 2.2 Natural Earth — populated places (`ne_10m_populated_places`); 2.3 Who’s On First (WOF); 2.4 Pelias / Geocode Earth (open-data stack vs hosted); 2.5 Mapbox / Google (hosted geocoding & Places); 3. Licensing notes (high level — verify before ship); 4. Rough import plan (GeoNames-first); 5. Data fields needed (canonical `Place` record); 6. Proposed ranking formula (v1 — heuristic, explainable)
- Concept signals:
  - **Purpose:** Choose an off-the-shelf gazetteer strategy that fits institutional goals in **`docs/geocoder_and_city_identity_strategy.md`** without replacing `map_CURRENT.html` search in this document.
  - | **allCountries** | Full gazetteer | **All feature classes** (terrain, streams, …)—**not** a drop-in “city list”; use only if you explicitly need non-PPL features or will **filter heavily** by `feature class` / `feature code`. |
  - - **Ranking “fame”** beyond population is **not** a single column—you derive it from feature codes, capitals, optional external scores, or user locale.
  - - Useful as a **visual density reference** or **lightweight “known dots” layer** on the map.
  - - **Best-in-class ontology** for “this place is inside these parents” (locality → region → country).

### A.52 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/governance/anti_cursor_bullshit_governance_rules.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 72
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Concept signals:
  - # Anti-Cursor Bullshit Governance Rules
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountability_failure_audit.md` …
  - | Rule | Rationale |
  - | **No rain/virga implementation** | theater risk |

### A.53 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_memory_synthesis.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 16257; SHA-12: `04f378dc370d`; score: 160
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Concept signals:
  - - **Roadmap:** intentional next-direction supported by archaeology and/or roadmap docs, not claimed shipped.
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.
  - **Orientation index (all doctrine files, pacing, reading order):** `docs/DOCTRINE_INDEX.md`
  - **Foundational training synthesis (philosophy + governance + tensions):** `docs/institutional_philosophical_synthesis.md`

### A.54 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_philosophical_synthesis.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 322
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Concept signals:
  - **Status:** Foundational doctrine for **future training**, **reviewer systems**, **UX design**, **product strategy**, **conversational architecture**, and **interpretive governance**.
  - **Authority:** Synthesizes durable texts in `ai_context/`, `docs/`, and `memory_archaeology_raw/consolidated_notes/`. It **does not** supersede those sources on technical implementation; it **weaves** them into one training-readable whole.
  - ## 1. Core philosophy
  - The relocation astrology platform is built on a paradox that mature users already live inside: **structure is real, and agency is real**. The chart is treated as **structurally real** for product purposes—not as an infinitely rewriteable “vibe,” not as a story generator that owes…
  - This posture has a deliberate audience: **astrology for grownups**—intellectually serious, skepticism-friendly, **sober without cynicism**. Warmth is expressed through **restraint**, not through neon spiritual retail. Excitement is expected to arise from **exploration and judgmen…

### A.55 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/intentionality_and_symbolic_constraints.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 8365; SHA-12: `d1c233003983`; score: 118
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Concept signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Not:** Marketing narrative, mystical prose, or public brand voice.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**

### A.56 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/local_archive_policy.md`
- Categories: human_usage_and_workflows, layer_4_interpretation_ai, validation_and_guardrails
- Characters: 1554; SHA-12: `5f3f7178bbfa`; score: 6
- Key headings: Local Archive Policy; Archive/Junk Drawer Candidates; Do Not Commit; Rule Of Thumb
- Concept signals:
  - This project benefits from preserving useful archaeology, but the repository should not collect random local machine junk.
  - ## Do Not Commit
  - Do not commit disposable local/browser/system artifacts:
  - Examples that should usually stay untracked or be deleted:
  - ## Rule Of Thumb

### A.57 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/map_and_overlay_design_research.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 5149; SHA-12: `f3943cdf7cf9`; score: 21
- Key headings: Map and Overlay Design Research; 1. Leaflet vs MapLibre vs Google Maps (philosophical comparison); 2. Current Leaflet strengths (for this codebase); 3. Actual blockers to watch for (hypothesis list—not confirmed); 4. Overlay transparency strategy (research directions); 5. Semantic overlap colors; 6. Aura rendering directions (non-commitments); 7. Map-edge and world-wrap ideas; 8. Dark / light mode implications; 9. Multilingual city rendering; 10. Decision rule (when to reopen migration); Related docs
- Concept signals:
  - | **Philosophy** | Small, composable, OSS tiles; you own interaction logic. | Vector-first, style-driven, OSS-core continuity from Mapbox GL patterns. | Full-stack commercial stack; deepest place data; platform coupling. |
  - | **Fit for this product** | Strong when overlays are **GeoJSON + careful projection/wrap discipline** and the team values **direct control** over truth vs display separation. | Strong if **vector basemaps**, **pitch**, **client-side style**, or **dense label collision** become c…
  - - **Proven** for the MVP: panes, GeoJSON layers, and manual QA workflows already invested.
  - - **Separation story aligns:** canonical backend GeoJSON + **display-layer** wrap/duplicate logic matches institutional architecture (`decisions.md`).
  - - **Lower migration tax** while overlay **truth** and **overlap readability** are still evolving—**avoid rewriting two crises at once**.

### A.58 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/next_implementation_sequence.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 10690; SHA-12: `ced0e563c90b`; score: 39
- Key headings: Next Implementation Sequence; Priority band 1 — UX polish (minimal architecture risk); Chunk 1.1 — Sidebar density and “debug vs ship” clarity; Chunk 1.2 — Popup and typography refinement; Chunk 1.3 — Native select stability + legend clutter reduction; Priority band 2 — Validator / stress tooling; Chunk 2.1 — Fixture manifest + “run these five” script; Chunk 2.2 — Latitude / polar stress suite expansion; Chunk 2.3 — Brute-force / truth export hygiene; Priority band 3 — Account + birth-data workflows; Chunk 3.1 — Birth data model (local-only MVP); Chunk 3.2 — Chart list + “open on map”
- Concept signals:
  - - **UX risks:** Hiding too much—power users lose discoverability. Mitigation: progressive disclosure, keep debug behind explicit mode.
  - - **Do not overengineer:** No new framework, no drawer rewrite here—**incremental compression** only.
  - - **Why:** Popup is diagnostic truth; typography should match premium, calm instrument tone.
  - - **Do not overengineer:** Avoid custom tooltip framework; tune CSS and copy.
  - - **Dependencies:** Prior click-through / select fixes must remain intact.

### A.59 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/00_OPERATOR_START_HERE.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_4_interpretation_ai, validation_and_guardrails
- Characters: 697; SHA-12: `a0e79ddfcf29`; score: 5
- Key headings: AI Onboarding Entry Point
- Concept signals:
  - - Demonstrate understanding before proposing UX, architecture, features, or workflows
  - - repeating doctrine without understanding doctrine
  - Understanding must be demonstrated, not claimed.

### A.60 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 200
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Concept signals:
  - **Scope:** User journey, screen responsibilities, mood states, and control architecture for the **dumb version** — facts-first exploration without AI dependency.
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doct…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - Define the complete user journey for the **non-AI relocation platform**.

### A.61 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 154
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Concept signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…

### A.62 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/README.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 54
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Concept signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - layer sovereignty,
  - - truth integrity,
  - - ontology boundaries,

### A.63 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 182
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Concept signals:
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - **Scope:** Durable UX laws governing workflow, hierarchy, transformation, and continuity across all product surfaces.
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - **Reads with (secondary):** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` (indexed catalog), `docs/constitutional/map_first_product_doctrine_v1.md`, journey and workflow architecture docs.

### A.64 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 308
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Concept signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.65 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 35789; SHA-12: `795365723409`; score: 199
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Concept signals:
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - - how behavioral facts may be captured **without interpretation**,
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`. Record management is **supporting infrastructure**, not the center of gravity.

### A.66 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 8365; SHA-12: `d1c233003983`; score: 118
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Concept signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Not:** Marketing narrative, mystical prose, or public brand voice.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**

### A.67 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 77
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Concept signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.

### A.68 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 41
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Concept signals:
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.
  - **Must not contain:** activity feeds, recents, owner hero cards, favorites, charts, map as primary surface, widgets, metrics.
  - 6. Favorites (high continuity value)

### A.69 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9566; SHA-12: `3de8663545ba`; score: 119
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Concept signals:
  - # Professional Non-AI Workflow v1
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - the map is the primary experience,

### A.70 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 3360; SHA-12: `554add110fa4`; score: 60
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Concept signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - # Layer Distinction
  - Truth belongs primarily to Layer 1.
  - Astrological fact belongs primarily to Layer 2.

### A.71 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/DOCTRINE_INDEX.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 154
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Concept signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…

### A.72 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/README.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 54
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Concept signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - layer sovereignty,
  - - truth integrity,
  - - ontology boundaries,

### A.73 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_CONSTITUTION.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 182
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Concept signals:
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - **Scope:** Durable UX laws governing workflow, hierarchy, transformation, and continuity across all product surfaces.
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - **Reads with (secondary):** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` (indexed catalog), `docs/constitutional/map_first_product_doctrine_v1.md`, journey and workflow architecture docs.

### A.74 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_DOCTRINE_MASTER.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 308
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Concept signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.75 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/constitutional_summary.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 4609; SHA-12: `8238f401edb1`; score: 103
- Key headings: Constitutional Summary; Purpose; Layer Architecture; Layer 1 - Truth; Layer 2 - Symbolic Ontology; Layer 3 - Intentional Interpretation; Layer 4 - Exploratory Optimization; Forbidden Crossings; Epistemic Doctrine; Runtime And Renderer Sovereignty; Purification Principle; Professional Trust And AI Behavior
- Concept signals:
  - The Relocation App is a layered symbolic intelligence platform. It is not a monolithic astrology chatbot, hidden recommendation engine, or mystical certainty machine.
  - # Layer Architecture
  - ## Layer 1 - Truth
  - Layer 1 owns astronomical and geometric truth:
  - - relocation geometry,

### A.76 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/epistemic_integrity_and_symbolic_humility.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 3739; SHA-12: `242cc62cfae5`; score: 39
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior; Good Behavior; Collaborative Discovery
- Concept signals:
  - - and anti-bullshit doctrine.
  - All AI and interpretive systems must follow these principles.
  - This document establishes the philosophical and operational rules governing:
  - - interpretation,
  - - symbolic restraint,

### A.77 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/intentionality_and_symbolic_constraints.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 8365; SHA-12: `d1c233003983`; score: 118
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Concept signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Not:** Marketing narrative, mystical prose, or public brand voice.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**

### A.78 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layer_sovereignty_and_forbidden_crossings.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 100
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Concept signals:
  - # Layer Sovereignty And Forbidden Crossings
  - It defines hard constitutional boundaries between layers.
  - These rules are mandatory architectural constraints.
  - - layer sovereignty,
  - The purpose is to prevent:

### A.79 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layered_symbolic_intelligence_architecture.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4801; SHA-12: `5242de0598f3`; score: 120
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Concept signals:
  - # Layered Symbolic Intelligence Architecture
  - It defines the constitutional layer architecture of the platform.
  - All future systems must respect:
  - - layer sovereignty,
  - - and truth integrity.

### A.80 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/map_first_product_doctrine_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 77
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Concept signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.

### A.81 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 3360; SHA-12: `554add110fa4`; score: 60
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Concept signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - # Layer Distinction
  - Truth belongs primarily to Layer 1.
  - Astrological fact belongs primarily to Layer 2.

### A.82 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/2026-05-29_application_journey_architecture_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 200
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Concept signals:
  - **Scope:** User journey, screen responsibilities, mood states, and control architecture for the **dumb version** — facts-first exploration without AI dependency.
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doct…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - Define the complete user journey for the **non-AI relocation platform**.

### A.83 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/PLAIN_LANGUAGE_PRODUCT_EXPLANATION_v1_2026-06-01.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems
- Characters: 6093; SHA-12: `0c7a9042f0a5`; score: 37
- Key headings: Plain Language Product Explanation; What Problem Does The Product Solve?; Why Relocation Astrology Is Geographic; Why The Map Is The Primary Discovery Instrument; What Overlays Represent; Why Cities Are Not The Primary Object Of Analysis; Natal Chart; Current Location Chart; Candidate Location Chart; Favorites; Saved Searches; Comparison
- Concept signals:
  - The user asks:
  - That is useful if the user already knows Lisbon matters.
  - Instead of starting with a city, the user starts with astrological conditions and discovers geography first.
  - The map allows users to see where chart conditions exist across the world.
  - Users can see:

### A.84 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_constitution_and_review_architecture.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 13121; SHA-12: `96b9567947d8`; score: 214
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Concept signals:
  - **Status:** Internal **governance architecture** for future AI-assisted interpretation—not a shipping spec, not marketing, not ethics theater.
  - **Tone contract:** Structured, skeptical, operational. **Anti-handwave, anti-hype.**
  - **Doctrine stack (read before changing AI behavior):**
  - - **`docs/intentionality_and_symbolic_constraints.md`** — fate/agency, tradeoffs, intentionality, AI governance implications.
  - - **`docs/brand_and_experience_foundations.md`** — **Interpretive language and emotional transparency**; **Interpretive integrity and archetypal honesty**; emotionally **non-interfering** design.

### A.85 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 264
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Concept signals:
  - # AI Interpretation Truthfulness Doctrine v1
  - **CANONICAL** for **future** AI-assisted interpretation layers — not current product scope.
  - **Scope:** Documentation only. Defines interpretive discipline, forbidden patterns, and a future review architecture. **No AI implementation in dumb Web 2.0 v1.**
  - - `docs/ai_constitution_and_review_architecture.md` — layered governance, anti-patterns, reviewer duties
  - - `docs/constitutional/epistemic_integrity_and_symbolic_humility.md` — honest uncertainty, symbolic restraint

### A.86 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 59
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Concept signals:
  - # Birth Time Uncertainty and Confidence Doctrine
  - Defines **epistemic tiers**, **user-facing honesty**, **data recording**, and **engine behavior boundaries** for uncertain birth times. Not implementation. Not rectification software spec.
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `validation/narratives…
  - - lay users often know approximate times only,
  - - AI intake may help later — **MVP must handle tiers without AI**.

### A.87 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_and_experience_foundations.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 155
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Concept signals:
  - # Brand and Experience Foundations
  - **What this is:** A **foundations** note for tone, judgment, and honesty in the product experience.
  - **What this is not:** A brand book, logo spec, marketing narrative, campaign, or visual identity system. **No** speculative public branding.
  - **Important:** The emotional and atmospheric goals below are **experiential design constraints**—they govern how future UX and rendering choices should **feel** and **function**. They are **not** marketing fluff; they are institutional memory for product judgment.
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).

### A.88 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_visual_language_and_design_doctrine.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 73
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Concept signals:
  - # Brand, Visual Language, and Design Doctrine
  - Consolidates **brand foundations**, **visual epistemology**, and **restrained premium language** for the professional non-AI MVP. Not a logo guide. Not marketing.
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - - calm, restrained, inspectable, premium, trustworthy, professional.
  - - mystical rainbow dashboard,

### A.89 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/client_chart_data_model_v1_2026-05-29.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 35789; SHA-12: `795365723409`; score: 199
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Concept signals:
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - - how behavioral facts may be captured **without interpretation**,
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`. Record management is **supporting infrastructure**, not the center of gravity.

### A.90 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/conversational_discovery_and_intentionality.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 4218; SHA-12: `c7b5d8b9fc8e`; score: 52
- Key headings: Conversational Discovery And Intentionality; Status; Purpose; Core Principle; User intentionality is sovereign.; Intentionality Discovery; Examples; Archetypal Exploration; Example Exploratory Style; Intentionality Strength; Examples; Layer Relationship
- Concept signals:
  - # Conversational Discovery And Intentionality
  - The principles of:
  - - intentionality discovery,
  - This document defines how the platform should:
  - - discover user goals,

### A.91 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/core_product_truths.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9535; SHA-12: `9d9048f7cab4`; score: 112
- Key headings: Core Product Truths; Astrology Truth; Inspectability; Map and Overlay UX; Product Experience; Visual / Semantic Product Identity; Emotionally non-interfering design (experiential constraints); Interpretive language and emotional transparency (doctrine); Interpretive integrity and archetypal honesty (doctrine); Development Discipline; Where the nuanced history lives
- Concept signals:
  - # Core Product Truths
  - These are durable principles that should survive individual implementation chunks, UI experiments, and future chat transitions.
  - ## Astrology Truth
  - - Map overlays must agree with point-and-click astrology truth.
  - - Popup point-truth validation is authoritative for local membership checks.

### A.92 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/geocoder_and_city_identity_strategy.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 36
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Concept signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - ## 1. Doctrine: city search is core systems engineering
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`). The map binds **h…
  - Current prototype list search (`cities.js`) is a **stand-in** only: **name, lat/lng, population (and minimal fields)**—**no reliable country/admin**, **no alternate names**, **no stable place IDs**, and **no** trustworthy global ranking (e.g. Paris, France vs Paris, Texas; London…
  - - The user should **choose from ranked results**, not depend on **mystery freeform** “first match” resolution (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`; Chunk 4.1: disambiguation **before** ML ranking).

### A.93 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/map_drawer_and_layer_control_doctrine.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 7226; SHA-12: `181a6ad8f6bd`; score: 32
- Key headings: Map Drawer and Layer Control Doctrine; Status; Purpose; Control hierarchy (map screen); Drawer architecture (target); Zones; Genie-into-corner collapse; Deferral (current phase); Condition editor doctrine; Target model; Card visual language; Search action
- Concept signals:
  - # Map Drawer and Layer Control Doctrine
  - Defines **map-primary control hierarchy**, **drawer/collapse behavior**, and **layer interaction semantics**. Not a component spec. Not implementation.
  - **Reads with:** `docs/overlay_and_aura_visual_strategy.md` §H, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/visual_semantic_style_guide.md` §9, `docs/product_workflows/product_screen_and_transition_architecture.md`.
  - Keep the **map sacred**. Controls must:
  - Priority order — highest wins when space is constrained:

### A.94 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/product_screen_and_transition_architecture.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 41
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Concept signals:
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.
  - **Must not contain:** activity feeds, recents, owner hero cards, favorites, charts, map as primary surface, widgets, metrics.
  - 6. Favorites (high continuity value)

### A.95 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_mode_vs_lay_mode_strategy.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3492; SHA-12: `c166907d611f`; score: 66
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Concept signals:
  - - strategic UX philosophy,
  - - and future product direction.
  - Core principles are canonical.
  - This document should be periodically reviewed for:
  - - professional workflow needs,

### A.96 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_non_ai_workflow_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9566; SHA-12: `3de8663545ba`; score: 119
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Concept signals:
  - # Professional Non-AI Workflow v1
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - the map is the primary experience,

### A.97 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_trust_and_ai_behavior_doctrine.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 106
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Concept signals:
  - # Professional Trust And AI Behavior Doctrine
  - This document defines how AI systems inside the platform must behave.
  - - symbolic restraint,
  - The AI must never behave like:
  - # Core Principle

### A.98 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_workflow_and_explanatory_language.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 11541; SHA-12: `1814ff883a7c`; score: 124
- Key headings: Professional Workflow And Explanatory Language; Status; Purpose; Professional Map Workflow; Desired Placement Search; Exclude / NOT Variables; Solo And Mute Controls; Inspection Workflow; Helper Layers; Intention Remains Primary; Astro Assist Substitution Guidance; Additive And Subtractive Relocation
- Concept signals:
  - # Professional Workflow And Explanatory Language
  - This is a living product-training and explanatory-language document.
  - - professional workflow guidance,
  - - draft user-facing explanations,
  - - future help text,

### A.99 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/symbolic_language_style_guide.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems
- Characters: 1703; SHA-12: `11e6dd9bdb1a`; score: 17
- Key headings: Symbolic Language Style Guide; Purpose; Core Principle; Preferred Style; Avoid; Good Examples; Bad Examples; Archetypal Precision; Symbolic Humility; Constitutional Goal
- Concept signals:
  - This document defines how symbolic language should be expressed by the platform.
  - # Core Principle
  - The system should sound:
  - It should not sound:
  - The AI should discuss:

### A.100 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ux_principles_and_emotional_tone.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4906; SHA-12: `3924025d2ba8`; score: 36
- Key headings: UX Principles and Emotional Tone; 1. Core temperament; 2. Map-first atmosphere; 3. Delight without spectacle; 4. Overlap readability philosophy; 5. Typography and color tone; 6. Layout cautions: drawer / genie / chrome; 7. Mobile and tablet; 8. When to stop designing; 9. Where philosophy is already strong in the repo; 10. Where philosophy could still drift; Related docs
- Concept signals:
  - # UX Principles and Emotional Tone
  - A concise distillation of how the product should **feel** and **behave**. Complements `docs/relocation_app_product_roadmap.md` (strategy) and `docs/overlay_and_aura_visual_strategy.md` (visual planning).
  - | Principle | Meaning |
  - | **Restraint** | Premium is **quiet**; confidence without shouting. No astrology hype aesthetic. |
  - | **Anti-overdesign** | No speculative chrome before map truth and readability are solid. |

### A.101 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/visual_semantic_style_guide.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9451; SHA-12: `93105f1b5ba9`; score: 66
- Key headings: Visual & Semantic Style Guide (Relocation Map System); 1. Visual epistemology (truth hierarchy); 2. House field semantics (categorical + cusp softness); 3. Aspect-to-angle aura semantics (intensity, not category); 4. Overlay texture semantics (almost subconscious); 5. NOT / exclusion overlays; 6. Color philosophy; 7. Popup visual language; 8. Interface tone; 9. Map and control relationship; 10. Account / chart page relationship; 11. Implementation discipline
- Concept signals:
  - **Status:** Planning and doctrine. This document defines **what visuals mean** and **how they should behave**. It does **not** mandate implementation order or ship dates.
  - **Companion docs:** `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/map_and_overlay_design_research.md`, `docs/brand_and_experience_foundations.md`, `docs/intentionality_and_symbolic_constraints.md` (fate/agency/tradeoffs), `docs/ai_c…
  - **Discipline:** Future rendering work should follow this guide so the product does not drift toward **debuggy/generic** UIs or **beautiful-but-unusable** spectacle.
  - ## 1. Visual epistemology (truth hierarchy)
  - | **Right-click / point popup** | **Canonical point truth** for the queried location | Authoritative for “what is true *here*” at that click (degrees, houses, etc.). |

### A.102 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ai_conversational_modes.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 2887; SHA-12: `b796e2065486`; score: 32
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Concept signals:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - exploratory feature concepts,
  - - prevent future contradictions,
  - This document should be periodically reviewed and updated as:

### A.103 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/archaeology_and_synthesis_workflow.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9005; SHA-12: `d3add7674811`; score: 50
- Key headings: Archaeology and synthesis workflow; 1. Pipeline overview; 2. When to create an archaeology pass; 3. When to create or update synthesis docs; 4. Durable truths vs transient implementation; 5. How to avoid flattening nuance during synthesis; 6. Preserving contradictory but valuable tensions; 7. Doctrine canonicalization; 8. Open tension preservation; 9. Institutional memory updating (rhythm); 10. Governance refresh; 11. Review bundle generation
- Concept signals:
  - # Archaeology and synthesis workflow
  - **Purpose:** Capture chat and session intelligence **without** flattening nuance, **without** treating the latest thread as law, and **without** losing rejected paths that explain pivots.
  - **Reads with:** `ai_context/memory_workflow.md`, `docs/institutional_memory_synthesis.md`, `docs/project_memory_taxonomy.md`, `docs/process/doctrine_review_cycle.md`.
  - Human merge remains authoritative. This workflow is **not** an autonomous agent pipeline.
  - Raw capture → themed synthesis → doctrine canonicalization → open tension preservation

### A.104 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/decision_and_uncertainty_framework.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9068; SHA-12: `4b8f251dada4`; score: 92
- Key headings: Decision and uncertainty framework; 1. Bounded uncertainty; 2. Heuristic vs exact truth; 3. Symbolic plausibility vs fake precision; 4. Exploratory guidance vs deterministic recommendation; 5. Preserving ambiguity intentionally; 6. Reversible decisions; 7. Experimentation doctrine; 8. User-facing confidence vs backend uncertainty; 9. “Good enough for exploration” vs “authoritative truth”; 10. Case study: aura philosophy; 11. Visual approximation doctrine
- Concept signals:
  - **Status:** Meta-governance — how the institution handles **uncertainty**, **ambiguity**, **heuristics**, and **judgment** without premature closure.
  - **Purpose:** Prevent fake precision, oracle UX, and tension-erasure while still allowing **fast exploration** and **reversible experiments**.
  - **Reads with:** `docs/visual_semantic_style_guide.md` §1, `docs/overlay_and_aura_visual_strategy.md` (aura doctrine), `docs/intentionality_and_symbolic_constraints.md`, `docs/process/doctrine_review_cycle.md`.
  - | **Interpretive meaning** (what does this mean for a life?) | **User-led**; AI assists within structure; **no false closure**. |
  - | **Symbolic ambiguity** (paradox, multi-valence) | **Preserve intentionally**; do not force single verdict in software. |

### A.105 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/doctrine_review_cycle.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9902; SHA-12: `00598386986c`; score: 83
- Key headings: Doctrine review cycle; 1. What this cycle protects; 2. Slow docs policy; 3. Implementation vs philosophy separation; 4. Tension-preservation doctrine; 5. Rationale preservation rules (“why”, not just “what”); 6. Review cadences (suggested, not ceremonial); 6.1 Doctrine coherence review; 6.2 AI drift audit; 6.3 UX coherence review; 6.4 Archaeology / synthesis refresh; 6.5 Review bundle / external audit
- Concept signals:
  - # Doctrine review cycle
  - **Purpose:** Periodic coherence maintenance so the project does not **silently drift**, **forget reasoning**, **flatten tensions**, or **confuse fast implementation with slow philosophy**.
  - **Reads with:** `docs/DOCTRINE_INDEX.md`, `docs/review_contracts_and_governance.md`, `docs/process/decision_and_uncertainty_framework.md`, `ai_context/memory_workflow.md`.
  - This is **not** bureaucracy. It is a **lightweight rhythm** for a long-lived symbolic instrument: enough structure that future contributors inherit **why**, not only **what**.
  - - **Philosophical coherence** — intentionality, restraint, tradeoff intelligence, non-oracle AI posture stay aligned across years.

### A.106 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/future_excellence_vs_future_feature_excellence.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 34
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Concept signals:
  - # Future Excellence vs Future Feature Excellence
  - - canonical architectural principles,
  - - future-oriented planning,
  - Some implementation concepts are exploratory and subject to revision.
  - This document should be periodically reviewed for:

### A.107 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer4_optimization_and_exploration_doctrine.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4341; SHA-12: `289b4552320f`; score: 74
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Concept signals:
  - # Layer 4 Optimization And Exploration Doctrine
  - - canonical Layer 4 principles,
  - - exploratory optimization philosophy,
  - - and future-facing interaction concepts.
  - Core Layer 4 boundaries are canonical.

### A.108 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer5_experiential_education_through_travel_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 86
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Concept signals:
  - # Layer 5 — Experiential Education Through Travel
  - **FUTURE ONLY — QUARANTINED**
  - **Layer:** 5 — Experiential education (meaning-making through lived experience)
  - **Dependency:** Requires mature AI guidance, relocation exploration substrate, and user observation capture — **after** standalone Web 2.0 facts-first product is proven.
  - **Reads with (boundary context only):** `docs/ux/2026-05-29_application_journey_architecture_v1.md` §Future Rooms, `docs/constitutional/layer_sovereignty_and_forbidden_crossings.md`.

### A.109 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/local_archive_policy.md`
- Categories: human_usage_and_workflows, layer_4_interpretation_ai, validation_and_guardrails
- Characters: 1554; SHA-12: `5f3f7178bbfa`; score: 6
- Key headings: Local Archive Policy; Archive/Junk Drawer Candidates; Do Not Commit; Rule Of Thumb
- Concept signals:
  - This project benefits from preserving useful archaeology, but the repository should not collect random local machine junk.
  - ## Do Not Commit
  - Do not commit disposable local/browser/system artifacts:
  - Examples that should usually stay untracked or be deleted:
  - ## Rule Of Thumb

### A.110 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/memory_workflow.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 6877; SHA-12: `0a90f034aa1f`; score: 47
- Key headings: Memory Maintenance Workflow; Purpose; Sources; Mining Old Chats; Processing Extraction Docs; Consolidating Raw Archaeology (optional phase); Updating Durable Memory; Memory Types; Raw Extraction; Durable Memory; Roadmap; Current Implementation State
- Concept signals:
  - # Memory Maintenance Workflow
  - This document explains how project memory should be maintained without turning old chats, reports, and speculative ideas into an unstructured pile.
  - The goal is durable continuity. Cursor and external reviewers should be able to understand the product direction, current state, and important constraints without rereading every past chat.
  - This workflow is not an autonomous agent system. The user remains the final editor and approver.
  - **Institutional map (broader pipeline):** `docs/process/archaeology_and_synthesis_workflow.md` — raw → synthesis → doctrine → review bundle → rehydration. **Cadence:** `docs/process/doctrine_review_cycle.md`.

### A.111 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/mvp_beta_and_future_feature_roadmap.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4767; SHA-12: `c904d8af5d1e`; score: 85
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes; Stage 2 — Professional Beta; Goal
- Concept signals:
  - # MVP, Beta, And Future Feature Roadmap
  - - and future feature concepts.
  - not immutable constitutional doctrine.
  - This roadmap should be periodically reviewed for:
  - # Core Principle

### A.112 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 56
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Concept signals:
  - # Ontology Plugin And Symbolic Framework Architecture
  - - canonical architectural principles,
  - - tentative future architecture,
  - - exploratory feature concepts,
  - - prevent future contradictions,

### A.113 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_continuity_workflow.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, future_web3_v2, validation_and_guardrails
- Characters: 5184; SHA-12: `8a80bdfb8e6e`; score: 35
- Key headings: Project Continuity Workflow; 1. Goals; 2. Memory lanes (what goes where); 3. Archaeology intake workflow; 4. Consolidation workflow (when to run); 5. Reviewer workflow; 6. Proposed updates workflow; 7. Raw archaeology vs durable truths; 8. How future chats should initialize; 9. How to continue safely after context loss; 10. Related docs
- Concept signals:
  - # Project Continuity Workflow
  - How to keep **coherence** across sessions, models, and months—without turning the repo into chaos. Complements `ai_context/memory_workflow.md` (detailed file rhythm) and `docs/institutional_memory_synthesis.md` (archaeology → durable truth).
  - - **Clear separation:** raw archaeology vs curated principles vs implementation state.
  - | **Themed synthesis** | `memory_archaeology_raw/consolidated_notes/` | Onboarding-friendly themes; still subordinate to **human-reviewed** `ai_context/` for “current doctrine.” |
  - | **Durable truths** | `ai_context/core_product_truths.md`, `decisions.md`, `product_brief.md` | Stable principles and decisions. |

### A.114 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_memory_taxonomy.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 5641; SHA-12: `e630f6401456`; score: 67
- Key headings: Project Memory Taxonomy; Architecture; UX Philosophy; Visual doctrine vs rendering experiments vs temporary UX; Implementation State; Future Features; Rejected Approaches; Validation Methodology; Edge Cases; Unresolved Questions; AI Strategy; Product Philosophy
- Concept signals:
  - System structure, boundaries, and durable technical direction.
  - - Canonical backend truth versus frontend display geometry.
  - - Truth-grid generation strategy.
  - - Leaflet versus future map-library evaluation.
  - ## UX Philosophy

### A.115 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/relocation_strategy_framework.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 2978; SHA-12: `5542c6b3c8b9`; score: 37
- Key headings: Relocation Strategy Framework; Status; Purpose; Core Principle; Subtractive relocation comes before additive optimization.; Subtractive Relocation; Additive Relocation; Strong Relocations Often Do Both; Tradeoff Reality; Archetypes Are Contextual; Optimization Delusion; Layer 4 Behavior
- Concept signals:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - exploratory feature concepts,
  - - prevent future contradictions,
  - This document should be periodically reviewed and updated as:

### A.116 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ai_and_professional_workflow_strategy.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2
- Characters: 4077; SHA-12: `093c412a15e4`; score: 37
- Key headings: AI and Professional Workflow Strategy (From Archaeology); Institutional memory vs chat memory (anti–vibe-chaos); AI reviewer infrastructure (evolution); Non-negotiable product stance; AI collaboration failures as institutional risk; Second-opinion models; Practitioner assist vision (future); Consumer / intake AI (later); Strategic business hypotheses (treat as archaeology, not commitments); Tension to preserve
- Concept signals:
  - # AI and Professional Workflow Strategy (From Archaeology)
  - - **Persistent cognition** here means **workflow**: reports → reviewer → proposed patches → human merge—not expecting cross-session recall from the model.
  - **Anti–vibe-chaos principles** (from repeated archaeology):
  - - Prefer **diff-grounded** edits for indentation-critical Python; giant unstructured pastes are an institutional hazard.
  - ## AI reviewer infrastructure (evolution)

### A.117 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/current_sidebar_ux_audit.md`
- Categories: human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 4992; SHA-12: `c07666b5828f`; score: 9
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces; 9. Condition model — **next structural UX step (documented)**; 10. Location search placement (documented)
- Concept signals:
  - **Intent:** Describe friction, record implemented fixes, and flag **documented-only** next steps (no redesign commitment).
  - - **`#renderStatus` / `#debugStatus`:** gated on `?debugGeometry` — unchanged.
  - **Behavior goal:** first row may default to planet-in-house, but users should eventually run **only** angle-in-sign or **only** aspect-to-angle without dummy planet rows.
  - **Engineering note:** needs coordinated **API/payload** and validation work later—**do not** half-migrate UI alone.
  - ## 11. First-use onboarding (implemented + future)

### A.118 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/foundational_product_truths.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 4380; SHA-12: `9c5286269c09`; score: 39
- Key headings: Foundational Product Truths (From Archaeology); Trust and truth; Overlap and decision-making; Precision vs cosmetics (non-negotiable vs acceptable); Separation of concerns (recurring architectural moral); Human + AI collaboration stance; Emotional tone and moat; Repetition as signal
- Concept signals:
  - # Foundational Product Truths (From Archaeology)
  - **Scope:** Cross-chat themes that appeared repeatedly or were corrected forcefully by the user.
  - **Status labels:** *Durable principle* = should guide decisions for years. *Product stance* = strategic positioning. *Process principle* = how the team builds.
  - ## Trust and truth
  - - **Durable principle — Inspectable precision:** If the map shows a region, line, or overlap, it must mean something **precise** in the relocated chart model. “Plausible geometry” is not validation. Trust is built through reproducible checks, not visual confidence.

### A.119 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/geocoder_and_city_strategy.md`
- Categories: human_usage_and_workflows, layer_1_geometry, layer_3_intent, layer_4_interpretation_ai, validation_and_guardrails
- Characters: 1799; SHA-12: `098e8b02e313`; score: 9
- Key headings: Geocoder and City Strategy (From Archaeology); Why cities are core (not decoration); Readability and density; Search and disambiguation; Internationalization; Provider strategy tension (open); Dataset anecdotes (process lessons); UX details that affect trust
- Concept signals:
  - Relocation decisions happen at **named places**; the map must connect semantically rich astrology overlays to **human geography**.
  - - Philosophy appears: optimize **cities per square inch / screen area**, not population alone.
  - - Need structured results: city + region/state + country + coordinates + optional population; **ranking by human relevance**, not only database order.
  - **Archaeology consensus:** do not migrate prematurely; separate canonical geometry from display; reassess after display adapter maturity.
  - GeoNames-style parsing mistakes (wrong column for population → empty city lists) show **schema verification** must be part of ingestion—not assumed.

### A.120 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_memory_synthesis.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 16257; SHA-12: `04f378dc370d`; score: 160
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Concept signals:
  - - **Roadmap:** intentional next-direction supported by archaeology and/or roadmap docs, not claimed shipped.
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.
  - **Orientation index (all doctrine files, pacing, reading order):** `docs/DOCTRINE_INDEX.md`
  - **Foundational training synthesis (philosophy + governance + tensions):** `docs/institutional_philosophical_synthesis.md`

### A.121 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_philosophical_synthesis.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 322
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Concept signals:
  - **Status:** Foundational doctrine for **future training**, **reviewer systems**, **UX design**, **product strategy**, **conversational architecture**, and **interpretive governance**.
  - **Authority:** Synthesizes durable texts in `ai_context/`, `docs/`, and `memory_archaeology_raw/consolidated_notes/`. It **does not** supersede those sources on technical implementation; it **weaves** them into one training-readable whole.
  - ## 1. Core philosophy
  - The relocation astrology platform is built on a paradox that mature users already live inside: **structure is real, and agency is real**. The chart is treated as **structurally real** for product purposes—not as an infinitely rewriteable “vibe,” not as a story generator that owes…
  - This posture has a deliberate audience: **astrology for grownups**—intellectually serious, skepticism-friendly, **sober without cynicism**. Warmth is expressed through **restraint**, not through neon spiritual retail. Excitement is expected to arise from **exploration and judgmen…

### A.122 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/map_workspace_behavior_audit_v1_2026-05-30.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 15325; SHA-12: `7567f30ce7ff`; score: 45
- Key headings: Map Workspace Behavior Audit v1; Status; Purpose; Language and ID doctrine (applies to all sections); 1. Behavior already decided; Genie modes; Reasons to reopen Genie (decided intents); Search and render; Variable model; Legacy adapter (handoff to production map path); Map surface and overlay doctrine; Clear Map
- Concept signals:
  - - `docs/ui/map_drawer_and_layer_control_doctrine.md` — map-primary hierarchy (strategic)
  - This document does **not** add features, layouts, or architecture. It consolidates decisions already present in contracts and related doctrine.
  - # Language and ID doctrine (applies to all sections)
  - | Rule | Status |
  - | **Do not hardcode final wording into payload semantics** | Decided — snapshot `variables[].label` at render; do not derive engine truth from display strings |

### A.123 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/open_questions_and_unresolved_areas.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3871; SHA-12: `c86a26458dc6`; score: 23
- Key headings: Open Questions and Unresolved Areas (From Archaeology); Geometry and calculation semantics; Rendering architecture; Validation systems; UX systems; Data + search; Product scope and ethics; Renderer beta stabilization questions (Chat 08); Operational workflow; Weak archaeology coverage (second pass, 2026-05); Human review gate
- Concept signals:
  - ## Geometry and calculation semantics
  - - Formal spec for **MC** presentation: relocated ecliptic MC vs culmination/RA line products—must be explicit in user-facing language and internal tests.
  - - Full **DC/IC** surface area: ASC+180 heuristics vs distinct professional semantics; staged rollout vs early completeness.
  - - **Polar / high-latitude policy:** reconcile archaeology’s mixed numbers (±60, ±65, grids -60..86) into a user-understandable policy + advanced override stance.
  - - Formal **aspect-group** tests as semantic entitlements (hard/soft/major) independent of geometry engine.

### A.124 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/product_brief.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3080; SHA-12: `ba708a2f1745`; score: 36
- Key headings: Product Brief; Product; Current Core Capabilities; Product Philosophy; Overlay Truth Standard; Current Architecture Direction; Validation Corpus; Institutional memory (archaeology)
- Concept signals:
  - This is a relocation astrology mapping app. Its core value is a map-first professional workflow where astrologers can search for geographically meaningful relocation conditions and visually inspect candidate places.
  - The app should become a calm, premium, trustworthy instrument for exploration, not a cluttered dashboard.
  - - `truth_grid` house overlays for Planet-in-House searches.
  - - Staged/shared-grid ASC overlays for faster ASC all-major aspect rendering.
  - - Point-and-click popup truth checks for local chart details.

### A.125 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/rejected_or_obsolete_approaches.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, validation_and_guardrails
- Characters: 2949; SHA-12: `9bccda948bdc`; score: 20
- Key headings: Rejected or Obsolete Approaches (From Archaeology); Geometry / seam handling; Rendering / signal processing mistakes; Aspect / line extraction misconceptions (historic debugging); Incorrect astronomical short-cuts (explicit catastrophic failures); UX / workflow paths; Institutional / AI process paths; Overlap representation (product iteration); Possibly obsolete but historically explanatory; Not “rejected,” but **dangerous if misunderstood**
- Concept signals:
  - This list preserves **why** certain paths were abandoned or flagged dangerous. Do not revive without explicit human re-approval.
  - ## Geometry / seam handling
  - - **Gaussian blur** (or similar) on astronomical fields used for truth extraction: can **shift** solutions and create false loops—rejected for truth; aesthetics belong in frontend-only layers.
  - ## Aspect / line extraction misconceptions (historic debugging)
  - - Confusing **RA** targets with **ASC ecliptic longitude** work—**rejected** as conceptual error (ASC/MC coordinate framing must match the chosen product definition).

### A.126 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/relocation_app_product_roadmap.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 27057; SHA-12: `24ab9bae5cb8`; score: 211
- Key headings: Relocation App Product Roadmap; 1. Current Stable Milestone; 2. Product Philosophy; 3. Core Search Types; 4. Overlay/Color System Roadmap; 5. Aspect Aura Roadmap; 6. UX/Layout Roadmap; 7. City Search / Geocoder Roadmap; 8. Birth Data / Accounts / Professional Mode Roadmap; Saved Object Taxonomy; Phase 2.4 Sampling / Cache Scaffold; Phase 2.5 Sampling / Cache Population Strategy
- Concept signals:
  - This document preserves the current product strategy, development sequence, UX philosophy, and validation priorities for future work.
  - - `truth_grid` house overlays are working and remain opt-in.
  - - Staged/shared-grid ASC overlays are working.
  - - Popup truth generally matches overlays in current validation.
  - - Validation contradictions are `0` in current truth-grid and angle-sign tests.

### A.127 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/travel_and_future_modes.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 1279; SHA-12: `c351ba13dcef`; score: 7
- Key headings: Travel and Future Modes (From Archaeology); Road-trip / GPS mode; Offline / airplane scenarios; Transit overlays and relocated houses (debated); Positioning consequence; Dependencies called out
- Concept signals:
  - # Travel and Future Modes (From Archaeology)
  - - Continuous relocation shifts as the user moves; notifications when crossing **house boundaries** or **aspect-to-angle corridors**.
  - GPS can work without network; archaeology suggests **pre-downloaded tiles/caches/routes** so travel mode works in constrained connectivity.
  - - User’s personal stance appears: transits against **natal houses** feel truer than transits against relocated houses.

### A.128 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ux_and_design_language.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3849; SHA-12: `ac5f86eb3a13`; score: 32
- Key headings: UX and Design Language (From Archaeology); Map-first and spatial reading; Trust UX vs explanation UX; Typography and popups (professional validation patterns); Interaction pitfalls called out repeatedly; Emotional tone; Product positioning language (from archaeology); Tensions to preserve (not resolve here); Chat 08 update: style presets and mobile layer control
- Concept signals:
  - - **Map dominance:** Controls exist to serve exploration; they must not steal the primary visual field during validation or professional use.
  - - **Panel vs drawer tension:** Fixed panels repeatedly **hid map evidence** (lines behind UI). Future direction: adjacent panel, collapsible drawer, draggable rail—anything that preserves inspectability.
  - - **Global map ergonomics:** Users must pan freely near **Pacific/dateline/polar** regions during validation; artificial snap-back is disqualifying for this product class.
  - - **Lay users cannot be expected to reconcile** overlay edges with chart tables; that is a **developer failure mode**, not a user skill issue.
  - - **Professionals still need an oracle:** Right-click / precise coordinate inspection is framed as **truth instrumentation**. It must have onboarding (hint, mode toggle), and mobile needs long-press equivalent.

### A.129 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 20953; SHA-12: `db53e1e91227`; score: 71
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Concept signals:
  - # Web 2.0 Account / Chart Workflow Architecture — Review Proposal
  - **ARCHITECTURE REVIEW — aligned with Map-First Product Doctrine (2026-05-31)**
  - **Date:** 2026-05-29 (original); **doctrine alignment:** 2026-05-31
  - **Scope:** Web 2.0 account/chart workflow architecture. Not implementation. Not schema migration.
  - **Governing doctrine:** `docs/constitutional/map_first_product_doctrine_v1.md` — supersedes dashboard-centric recommendations in v1.0–v1.1 of this review.

### A.130 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/00_OPERATOR_START_HERE.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_4_interpretation_ai, validation_and_guardrails
- Characters: 697; SHA-12: `a0e79ddfcf29`; score: 5
- Key headings: AI Onboarding Entry Point
- Concept signals:
  - - Demonstrate understanding before proposing UX, architecture, features, or workflows
  - - repeating doctrine without understanding doctrine
  - Understanding must be demonstrated, not claimed.

### A.131 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_EVALUATION_LOG.md`
- Categories: human_usage_and_workflows, layer_4_interpretation_ai, validation_and_guardrails
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.132 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_WORKFLOW_GOVERNANCE.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 14272; SHA-12: `570f3cca823a`; score: 59
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Concept signals:
  - # AI Workflow Governance Protocol
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in writing.
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisible engineering inte…
  - ## Ghost Boss Governance Doctrine
  - Every phase closeout must ask whether it introduced or exposed:

### A.133 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/KILL_TEST.md`
- Categories: human_usage_and_workflows, layer_4_interpretation_ai, validation_and_guardrails
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.134 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/PRODUCT_COMPREHENSION_GATE.md`
- Categories: human_usage_and_workflows, layer_4_interpretation_ai, validation_and_guardrails
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.135 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/ai_drift_audit_framework.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9541; SHA-12: `889f1d9b2f3a`; score: 83
- Key headings: AI drift audit framework; 1. Healthy AI posture (target); 2. Audit dimensions and warning signs; 2.1 Excessive certainty; 2.2 Flattery; 2.3 Manipulative spirituality; 2.4 Optimization obsession; 2.5 Over-helpfulness; 2.6 Premature closure; 2.7 Reducing exploratory play; 2.8 Guru behavior; 2.9 Dependency framing
- Concept signals:
  - **Purpose:** Catch **comfort bias**, **oracle creep**, and **flattening** before they ship—not after user dependency forms.
  - **Reads with:** `docs/ai_constitution_and_review_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/brand_and_experience_foundations.md`, `docs/process/doctrine_review_cycle.md`.
  - The model (or assist layer) should behave like:
  - - A **symbolic translator** and **comparison aide**—structure-forward, biography-light unless user-supplied.
  - - A **GPS recalculator** under constraints—not a prophet, not a therapist replacement, not a spiritual authority.

### A.136 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/anti_cursor_bullshit_governance_rules.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 72
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Concept signals:
  - # Anti-Cursor Bullshit Governance Rules
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountability_failure_audit.md` …
  - | Rule | Rationale |
  - | **No rain/virga implementation** | theater risk |

### A.137 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/constitutional_ingestion_checklist.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 46
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Concept signals:
  - This document is operational infrastructure.
  - - track doctrine ingestion,
  - Update this document whenever:
  - - doctrine evolves,
  - - or roadmap structure changes.

### A.138 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/implementation_governance_and_ai_workflow_protocol.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3988; SHA-12: `b127e5c52050`; score: 40
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Concept signals:
  - # Implementation Governance And AI Workflow Protocol
  - - AI workflow behavior,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - This project intentionally rejects:

### A.139 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/purification_audit_framework.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 3639; SHA-12: `a43528565790`; score: 64
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Concept signals:
  - - contaminate neighboring layers,
  - - or violate constitutional doctrine.
  - # Core Principle
  - A purification audit is a structured review of:
  - - Does this system still belong to its declared layer?

### A.140 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/review_contracts_and_governance.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 12252; SHA-12: `18cc9636738c`; score: 112
- Key headings: Review contracts and governance (implementation layer); 1. What a “review contract” is here; 2. Principles reviewers hold in tension; 3. Implementation review questions; 4. UX review questions; 5. AI behavior review questions; 6. Symbolic integrity review questions; 7. Exploratory and play preservation checks; 8. Anti-chaos visual checks; 9. Anti-guru and anti-coercion checks; 10. Does this preserve contemplative space?; 11. Intelligent exceptions (examples)
- Concept signals:
  - # Review contracts and governance (implementation layer)
  - **Status:** Lightweight operational doctrine—**not** a compliance checklist, **not** a substitute for judgment, **not** corporate policy theater.
  - **Reads with:** `docs/ai_constitution_and_review_architecture.md` (interpretive AI layers and anti-patterns), `docs/DOCTRINE_INDEX.md` (where each doctrine lives), `docs/institutional_philosophical_synthesis.md` (foundational synthesis for training), `docs/process/doctrine_review…
  - **Purpose:** give reviewers and implementers **shared guardrails** so work preserves **symbolic honesty, restraint, readability, agency, intentionality, exploratory freedom, professional seriousness, and emotional tone**—while still allowing **fast iteration** and **intelligent i…
  - Contracts are **guardrails**, not formulas. They do not award points for mechanical compliance. A change can satisfy every literal question below and still be wrong in context—or violate one question deliberately for a **documented, rare, intelligent exception**. The reviewer’s j…

### A.141 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 200
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Concept signals:
  - **Scope:** User journey, screen responsibilities, mood states, and control architecture for the **dumb version** — facts-first exploration without AI dependency.
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doct…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - Define the complete user journey for the **non-AI relocation platform**.

### A.142 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 154
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Concept signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…

### A.143 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/README.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 54
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Concept signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - layer sovereignty,
  - - truth integrity,
  - - ontology boundaries,

### A.144 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 182
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Concept signals:
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - **Scope:** Durable UX laws governing workflow, hierarchy, transformation, and continuity across all product surfaces.
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - **Reads with (secondary):** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` (indexed catalog), `docs/constitutional/map_first_product_doctrine_v1.md`, journey and workflow architecture docs.

### A.145 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 308
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Concept signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.146 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 35789; SHA-12: `795365723409`; score: 199
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Concept signals:
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - - how behavioral facts may be captured **without interpretation**,
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`. Record management is **supporting infrastructure**, not the center of gravity.

### A.147 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 8365; SHA-12: `d1c233003983`; score: 118
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Concept signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Not:** Marketing narrative, mystical prose, or public brand voice.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**

### A.148 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 77
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Concept signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.

### A.149 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 41
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Concept signals:
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.
  - **Must not contain:** activity feeds, recents, owner hero cards, favorites, charts, map as primary surface, widgets, metrics.
  - 6. Favorites (high continuity value)

### A.150 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: core_identity_and_market_position, human_usage_and_workflows, layer_1_geometry, layer_2_ontology, layer_3_intent, layer_4_interpretation_ai, layer_5_experience, stage_reveal_systems, future_web3_v2, validation_and_guardrails
- Characters: 9566; SHA-12: `3de8663545ba`; score: 119
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Concept signals:
  - # Professional Non-AI Workflow v1
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - the map is the primary experience,



---

## Appendix B — Audit Statement

Programmatic pass selected 196 concept/philosophy/layer source blocks from 196 total archive blocks. The audit JSON stores matched file names, hashes, headings, concept signals, category counts, central sources, and source metadata. Final generated word count before this statement: 21834 words.
