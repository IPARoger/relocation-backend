# WEB3 AI Implementation Roadmap

**Status:** Planning complete. Implementation tracks defined. No production implementation active.
**Date:** 2026-06-27
**Mode:** Documentation only — no code, no migrations, no UI changes
**Authority:** Subordinate to [`docs/constitutional/FOUNDATIONAL_CONSTITUTION.md`](../constitutional/FOUNDATIONAL_CONSTITUTION.md)

> **Promotion rule:** Nothing in this roadmap is active implementation. Each track becomes active only when it is promoted into a focused implementation document with scope, DB migration plan, validation gate, and rollback path. The Web2 instrument remains sovereign.

> **Permanent rule (FOUNDATIONAL_CONSTITUTION.md §7.5):** The non-AI professional Web2 core must remain fully usable without any AI component. AI is additive assistance, not replacement navigation.

---

## Overview

This roadmap defines the eight implementation tracks required to build the Web3 AI layer of the Relocation astrology platform. The AI layer extends the Web2 instrument — it does not replace it.

**What this roadmap covers:**
- How each AI subsystem is defined, what it depends on, and what it produces
- The sequencing of tracks: what must come first, what waits, what can proceed in parallel
- The gate conditions that prevent premature production use
- Cross-references to all existing canon documents that govern each track

**What this roadmap does NOT cover:**
- Production prompt engineering or model selection
- Database migration details (each track specifies those separately when promoted)
- UI implementation specs (see Track 3 and `docs/canon/AI_INTERACTION_SURFACES.md`)
- Pricing and packaging decisions (noted where relevant; deferred)
- Knowledge Ingestion (Track 8) — documented as future scope only

**Relationship to existing canons:**

This roadmap builds on and is governed by the following existing canon documents. It does not redesign them.

| Canon document | Role in this roadmap |
|----------------|----------------------|
| [`FOUNDATIONAL_CONSTITUTION.md`](../constitutional/FOUNDATIONAL_CONSTITUTION.md) | Supreme authority; all tracks subordinate to it |
| [`AI_CONSULTATION_ARCHITECTURE.md`](../canon/AI_CONSULTATION_ARCHITECTURE.md) | Defines five AI roles, Consultation Canon, layer model, evidence system |
| [`INTENT_TRANSLATION_ENGINE.md`](../canon/INTENT_TRANSLATION_ENGINE.md) | Defines three-stage translation; produces SearchSpec |
| [`AI_COMMUNICATION_DOCTRINE.md`](../canon/AI_COMMUNICATION_DOCTRINE.md) | Governs all AI voice and communication decisions |
| [`CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md`](../canon/CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md) | Defines birth-time resolution and tradeoff reasoning |
| [`PATTERN_RECOGNITION_AND_MEANING_DOCTRINE.md`](../canon/PATTERN_RECOGNITION_AND_MEANING_DOCTRINE.md) | Three-role model: astrology/AI/user |
| [`LAYER_2_AUTHORING_ARCHITECTURE.md`](../canon/LAYER_2_AUTHORING_ARCHITECTURE.md) | Entry-as-object model, type registry, versioning, inheritance |
| [`AI_RUNTIME_ARCHITECTURE.md`](../canon/AI_RUNTIME_ARCHITECTURE.md) | Runtime component definitions (Track 2 output) |
| [`AI_INTERACTION_SURFACES.md`](../canon/AI_INTERACTION_SURFACES.md) | Screen-aware surface definitions (Track 3 output) |

---

## Sequencing Overview

The tracks have hard dependencies. The diagram below shows the implementation sequence. "Parallel" means design or specification work can proceed in parallel with Web2 QA; implementation sequencing is strict.

```
                      +----------------------------------+
                      |  Web2 QA (current active work)  |
                      +----------------------------------+
                                      |
            +--------------------------+-------------------------+
            |                         |                         |
            v                         v                         v
  +------------------+    +----------------------+   +----------------------+
  |  Track 1         |    |  Track 2 (spec)      |   |  Track 3 (spec)      |
  |  Layer 2         |    |  Runtime Architecture |   |  Interaction Surfaces|
  |  Foundation      |    |  (design in parallel) |   |  (design in parallel)|
  +------------------+    +----------------------+   +----------------------+
            |                         |
            |   +---------------------+
            v   v
  +----------------------+
  |  Track 4             |
  |  SearchSpec + Engine |
  |  (depends on T1+T2)  |
  +----------------------+
            |
     +------+------+
     v             v
  +----------+  +--------------+
  | Track 5  |  |  Track 6     |
  | Navigator|  |  Astro Assist|
  +----------+  +--------------+
     |             |
     +------+------+
            |
            v
  +----------------------+
  |  Track 7             |  <- must gate ALL Track 5+6 output
  |  Guardian            |     before any display to user
  +----------------------+
            |
            v
  +----------------------+
  |  Track 3             |
  |  Interaction Surfaces|
  |  (implementation)    |
  +----------------------+
            |
            v
  +----------------------+
  |  Track 8             |
  |  Knowledge Ingestion |  <- FUTURE / NOT IMMEDIATE
  +----------------------+
```

**What proceeds in parallel with Web2 QA:**
- Track 1 design (entry type registry finalization, field schema definition, validator tooling)
- Track 2 specification (runtime component definitions — produced in this planning phase)
- Track 3 specification (interaction surface definitions — produced in this planning phase)
- Track 7 specification (Guardian review criteria — produced in this planning phase)

**What waits for Web2 release:**
- Track 4 implementation (SearchSpec schema + Engine)
- Track 5 implementation (Navigator)
- Track 6 implementation (Astro Assist)
- Track 3 implementation (surfaces wired to runtime)

**Hard gate — no production AI use until:**
1. At least the minimum required Layer 2 entry set is Approved (not Draft) through the Wizard review path (Track 1)
2. Guardian (Track 7) is operational and running on all AI output before display
3. Every consultation session is bound to a specific, pinned manifest version (Track 1)

---

## Track 1 — Layer 2 Foundation

**Cross-reference:** [`docs/canon/LAYER_2_AUTHORING_ARCHITECTURE.md`](../canon/LAYER_2_AUTHORING_ARCHITECTURE.md)

### Purpose

Establish the Layer 2 ontology infrastructure required before any AI system can responsibly use symbolic grammar. No AI output may claim astrological grounding unless the underlying Layer 2 entry is Approved (not Draft).

The Beta Reference Ontology v1 (`docs/layer2/beta_v1/`) is a Draft seed. It proves the entry model works. It does not authorize production use.

### Inputs

- `docs/layer2/beta_v1/` — 224 Draft entries (PIH x132, ASP x46, DIG x36, ORB x7, HEM x3)
- `docs/canon/LAYER_2_AUTHORING_ARCHITECTURE.md` — entry-as-object model, type registry, field schema principles, inheritance model
- `docs/layer2/beta_v1/MANIFEST.json` — model ID, version, entry inventory, deferred entry types

### Outputs / Deliverables

| Deliverable | Description |
|-------------|-------------|
| AI-L2-2: Entry type registry freeze | Closed vocabulary of entry types (PIH, PIS, ASP, DIG, ORB, HEM, SUB, REC, TRD, CLU, LNG) with typed field schemas per type |
| Import validator | Tool that validates any Layer 2 JSON file against the frozen schema; runs before any entry enters the system |
| Read-only model resolver | Given a manifest ID + entry type + subject, returns the resolved entry using the inheritance chain (professional override -> default) |
| Manifest/version pinning | Each consultation session records which manifest ID and version it was created under; results are reproducible against the same manifest |
| Review/approval path | Minimum: Draft -> Under Review -> Approved lifecycle with reviewer identity recorded in the envelope |

### Key Decisions

1. **AI-L2-2 field schema definition.** The typed field set per entry type must be frozen before the model resolver is built. This is a platform-level schema change. Decisions: which fields are required vs. optional; what fallback behavior applies when optional fields are empty (see LAYER_2_AUTHORING_ARCHITECTURE.md §6).

2. **Minimum approval threshold for production use.** All 224 entries are Draft. Production AI cannot use Draft entries. Decision: what is the minimum set of entries that must be Approved before a first Navigator session can run responsibly? (Proposed: at minimum all PIH entries for the planets used in first consultation workflows.)

3. **Who can approve entries.** The current model assumes a founder/professional reviewer. Decision: is a single approver sufficient for beta, or is a two-reviewer model required?

4. **Entry type additions.** The deferred entry types (SUB, REC, TRD, CLU) are Layer 3/4 operations excluded from the beta_v1 seed. Decision: which of these must exist before Track 4 (SearchSpec) can be implemented?

### Dependencies

- None. Track 1 is the foundation; all other tracks depend on it.

### Implementation Phase

**Phase 1** — can begin during or after Web2 QA. No dependency on Web2 release.

Sub-phases:
- 1a: Freeze entry type registry and typed field schemas (AI-L2-2)
- 1b: Build import validator and run against all beta_v1 files
- 1c: Build read-only model resolver with manifest pinning
- 1d: Implement Draft -> Approved lifecycle path (minimum: reviewer field + status transition)
- 1e: Founder/professional review of beta_v1 entries; approve minimum required set

**Hard gate:** No Track 5 or Track 6 implementation until Phase 1e is partially complete and the resolver (1c) is operational.

---

## Track 2 — Runtime Architecture

**Separate spec file:** [`docs/canon/AI_RUNTIME_ARCHITECTURE.md`](../canon/AI_RUNTIME_ARCHITECTURE.md)

**Cross-reference:** [`docs/canon/AI_CONSULTATION_ARCHITECTURE.md`](../canon/AI_CONSULTATION_ARCHITECTURE.md)

### Purpose

Define the runtime components of the AI system — the concrete, deployable objects that implement the five AI roles defined in AI_CONSULTATION_ARCHITECTURE.md. The runtime architecture translates the role model into what actually gets built and deployed.

This track produces a specification document (`AI_RUNTIME_ARCHITECTURE.md`) that governs all subsequent AI implementation. The specification is created in this planning phase. Implementation waits for Track 1 to be operational.

### Inputs

- `docs/canon/AI_CONSULTATION_ARCHITECTURE.md` — five AI roles, Consultation Canon, layer model
- `docs/canon/INTENT_TRANSLATION_ENGINE.md` — translation pipeline, competing hypotheses, SearchSpec dependency
- `docs/canon/CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md` — birth-time resolution, tradeoff engine

### Outputs / Deliverables

| Deliverable | Description |
|-------------|-------------|
| `docs/canon/AI_RUNTIME_ARCHITECTURE.md` | Full spec document defining each runtime component |
| Component contract definitions | For each component: purpose, inputs, outputs, scope limits, must-not-do list |
| Data flow diagram | Text-based diagram of how data moves between components |
| Implementation phase plan | Sequenced build order for runtime components |

**Runtime components defined in this track:**

1. **Navigator** — consumer-facing orchestrator; manages intake to refinement loop; speaks to user
2. **Engine** — executes SearchSpec against Layer 1 data layer; returns results; does not speak to users
3. **Guardian** — runs on all AI output before display; see Track 7
4. **Consultation Memory** — manages Consultation Canon object; append-only evidence log
5. **Layer 2 Model Resolver** — read-only lookup of Layer 2 ontology entries by manifest ID + entry address
6. **SearchSpec** — structured object bridging Navigator/Astro Assist output to Engine input; see Track 4
7. **Genie/Map adapter** — connects AI output to map layer; launches overlays, saved searches, and pins

### Key Decisions

1. **Deployment model.** Each runtime component maps to deployable units. Decision: monolith vs. microservice boundary for initial AI layer.

2. **State persistence boundary.** The Consultation Memory (Consultation Canon) must be persisted across sessions. Decision: which fields live in the database vs. session state vs. request context?

3. **Genie/Map adapter scope.** Decision: does AI-to-map handoff happen via shared state bus, URL-based handoff, or a dedicated adapter API?

4. **Guardian execution model.** Decision: does the Guardian run synchronously (blocking display until review passes) or asynchronously (brief review window before display)?

### Dependencies

- Track 1 (Layer 2 Foundation): Layer 2 Model Resolver requires the operational resolver from Track 1
- Track 4 (SearchSpec): SearchSpec definition must be finalized before Engine can be built

### Implementation Phase

**Phase 0** (specification): this document, plus AI_RUNTIME_ARCHITECTURE.md
**Phase 2** (implementation): after Track 1 Phase 1c is operational

---

## Track 3 — Interaction Surfaces

**Separate spec file:** [`docs/canon/AI_INTERACTION_SURFACES.md`](../canon/AI_INTERACTION_SURFACES.md)

**Cross-reference:** [`docs/canon/AI_CONSULTATION_ARCHITECTURE.md`](../canon/AI_CONSULTATION_ARCHITECTURE.md) · [`docs/canon/AI_COMMUNICATION_DOCTRINE.md`](../canon/AI_COMMUNICATION_DOCTRINE.md)

### Purpose

Define each surface where the AI appears, what context the AI automatically receives from that surface, what the AI can initiate, and what it must not do. The AI must be screen-aware: the user must not have to explain what they are looking at.

### Inputs

- Current Web2 surface inventory: map, Genie, comparison, profile, saved searches, City Intelligence, notes, help
- `docs/canon/AI_CONSULTATION_ARCHITECTURE.md` — Navigator role, Consultation Canon
- `docs/canon/AI_COMMUNICATION_DOCTRINE.md` — communication and fluency principles

### Outputs / Deliverables

| Deliverable | Description |
|-------------|-------------|
| `docs/canon/AI_INTERACTION_SURFACES.md` | Full surface specification with context propagation per surface |
| Surface context contract | Structured data automatically passed to AI when user opens each surface |
| Initiation rules | What AI may initiate from each surface without explicit user request |
| Scope limits per surface | What AI must not do from each surface |

**Surfaces covered:**
1. Intake / first experience
2. Map pinwheel
3. Saved searches
4. Genie
5. Comparison
6. Profile
7. City Intelligence
8. Professional Astro Assist

### Key Decisions

1. **Context payload schema.** Decision: what is the canonical schema for the surface context object, and who owns it?

2. **AI entry point placement.** Decision: consistent placement across all surfaces vs. surface-specific placement?

3. **Astro Assist separation.** Decision: separate route/view or mode within the same interface?

4. **Genie coexistence.** Genie exists as a Web2 search tool today. Decision: how does the AI Genie conversational mode coexist with the existing Web2 Genie without breaking it?

### Dependencies

- Track 1: surfaces displaying AI interpretive output require Approved Layer 2 entries
- Track 2: surface implementation depends on Navigator and Guardian being operational
- Track 5: consumer surfaces depend on Navigator
- Track 6: Astro Assist surface depends on Track 6

### Implementation Phase

**Phase 0** (specification): this document, plus AI_INTERACTION_SURFACES.md
**Phase 4** (implementation): after Tracks 1, 2, 4, 5, and 7 are operational

---

## Track 4 — SearchSpec + Engine

**Cross-reference:** [`docs/canon/INTENT_TRANSLATION_ENGINE.md`](../canon/INTENT_TRANSLATION_ENGINE.md) §§3, 12, 13

### Purpose

Define the SearchSpec structured object — the formal serialization format that bridges Navigator/Astro Assist output to Engine input — and implement the Engine that executes SearchSpecs against the Layer 1 astrological data layer.

INTENT_TRANSLATION_ENGINE.md §13 explicitly flags this as AI-3: Search Specification Schema (future slice). This track delivers it.

### Inputs

- `docs/canon/INTENT_TRANSLATION_ENGINE.md` — SearchSpec field requirements (§13), viability probing strategy (§12)
- `docs/canon/AI_CONSULTATION_ARCHITECTURE.md` — Layer 4 search/refinement/optimization operations (§§7–9)
- Track 1 output — Layer 2 Model Resolver (Engine uses Layer 2 entries to ground search logic)
- Track 2 output — Runtime Architecture (Engine is a defined runtime component)
- Layer 1 data layer — astronomy, relocated charts, overlays (Engine reads; never writes)

### Outputs / Deliverables

| Deliverable | Description |
|-------------|-------------|
| SearchSpec schema | JSON schema for the SearchSpec object (see field list below) |
| SearchSpec serialization format | How a SearchSpec is persisted, versioned, and referenced |
| Engine implementation spec | How the Engine executes a SearchSpec against Layer 1 data |
| Saved search handoff spec | How a SearchSpec becomes a saved search |
| Genie launch spec | How a SearchSpec launches the Genie conversational interface |
| Map overlay launch spec | How a SearchSpec launches the map overlay |
| Viable alternatives mechanism | How Engine produces alternative strategy results when exact specs cannot be satisfied |

**SearchSpec object — required fields:**

```
SearchSpec
  spec_id                  -- stable ID for this spec instance
  manifest_id              -- Layer 2 manifest pinned to this spec
  desired_placements       -- list of { planet, house | angle | aspect, weight }
  avoids                   -- list of { planet, house | angle | aspect, reason }
  soft_preferences         -- list of { description, weight }
  geographic_constraints   -- { regions, countries, max_distance_from,
                               min_distance_from, exclude_regions }
  climate_city_filters     -- { climate_type, city_size, cost_of_living }
                              (schema present; execution deferred)
  viable_alternatives      -- boolean: request alternative compositional strategies
  recalculate_more         -- boolean: request additional alternatives if first results
                              are unsatisfactory
  saved_search_handoff     -- { trigger, name_suggestion, description_suggestion }
  genie_launch             -- { trigger, context }
  map_overlay_launch       -- { trigger, overlay_params }
  transparency_notes       -- { what_tried, what_worked, what_substituted,
                               tradeoff_introduced }
  user_approved_path       -- which strategy variant the user selected
  created_from             -- { consultation_id, session_id, intent_snapshot }
```

### Key Decisions

0. **Overlay-first doctrine.** SearchSpec primary output is map overlay configuration and viable geographic conditions — not city lists. The Engine returns overlay branches per strategy variant. Cities enter only after the user pins or selects a place on the map, or after an explicit city-helper request from a professional. This is a hard architectural constraint, not a preference.

1. **Climate/city filters.** Schema must accommodate climate_city_filters, but execution is deferred until a separate data layer integration track is completed. The schema field must be present in v1.

2. **Viable alternatives depth.** When viable_alternatives is true, how many alternative strategies does the Engine return? (Proposed: up to 4 named strategy variants, following viability probing model in INTENT_TRANSLATION_ENGINE.md §12.)

3. **Scoring model.** Engine returns scored results, but scores must never surface to users as raw numbers. Decision: Engine returns named strategy-match categories, not numeric scores.

4. **Layer 1 read path.** Decision: does the Engine call the existing Layer 1 API directly, or go through a dedicated data service?

### Dependencies

- Track 1: Engine uses Layer 2 entries; Model Resolver must be operational
- Track 2: Engine is a defined runtime component

### Implementation Phase

**Phase 2** — SearchSpec schema can be finalized during Phase 1. Engine implementation begins after Track 1 Phase 1c (model resolver) is operational.

---

## Track 5 — Navigator

**Cross-reference:** [`docs/canon/AI_CONSULTATION_ARCHITECTURE.md`](../canon/AI_CONSULTATION_ARCHITECTURE.md) §§2–10 · [`docs/canon/INTENT_TRANSLATION_ENGINE.md`](../canon/INTENT_TRANSLATION_ENGINE.md) · [`docs/canon/CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md`](../canon/CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md) · [`docs/constitutional/FOUNDATIONAL_CONSTITUTION.md`](../constitutional/FOUNDATIONAL_CONSTITUTION.md) §§7.6–7.9

### Purpose

Implement the Navigator: the consumer-facing research companion that orchestrates the relocation consultation experience from intake through search refinement. The Navigator is an astro sherpa, not a general chatbot.

### Inputs

- Consultation Canon (managed by Consultation Memory component; see Track 2)
- Layer 2 entries (via Model Resolver; see Track 1)
- SearchSpec produced by Intent Translation Engine; passed to Engine (see Track 4)
- User input from active surface (structured context from Track 3)
- Guardian approval (all Navigator output passes through Guardian before display; see Track 7)

### Outputs / Deliverables

| Deliverable | Description |
|-------------|-------------|
| Navigator implementation | Running AI component orchestrating the consultation loop |
| Intake flow | Collects birth data, location history, relocation intention in natural conversation |
| Consultation Canon management | Creates and updates evidence events; manages the Canon object |
| Intent translation integration | Calls Intent Translation Engine; manages competing hypotheses; asks disambiguation questions |
| SearchSpec handoff | Produces SearchSpec from accumulated intention evidence; passes to Engine |
| Tradeoff presentation | Explains overlay result conditions in narrative-level tradeoff language per CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md §3 — not city lists; the user has selected the places being discussed |
| Search refinement loop | Narrows results through conversation; updates SearchSpec; re-runs Engine |
| Checkpointing | Saves consultation progress; allows user to resume |

**Navigator responsibilities:**

| Responsibility | Description |
|----------------|-------------|
| Intake | Collect birth data, current location, relocation intention conversationally |
| Birth-time confidence resolution | Follow resolution stages from CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md §1 |
| Intention clarification | Translate vague desires into astrological parameters using translation question library |
| Fluency and appetite tracking | Infer user's astrological vocabulary level; adapt explanations per AI_COMMUNICATION_DOCTRINE.md §§3-4 |
| Tradeoff discussion | Present what-you-gain/what-you-give-up for each location option in narrative language |
| Search refinement | Narrow results through conversation; update SearchSpec; re-run Engine |
| Educational explanation | Teach relevant astrological principles when fluency and appetite signals indicate interest |
| Checkpointing | Save progress points; allow user to return to the same consultation state |
| Scope control | Redirect off-topic requests; refuse general-assistant behavior |

**Scope limits — Navigator must NOT:**

| Prohibited | Why |
|------------|-----|
| Function as a general astrology chatbot | Oracle pattern; violates FOUNDATIONAL_CONSTITUTION.md §7.1 |
| Function as a life coach | Not within scope; violates constitutional First Law |
| Generate predictions about specific life events | FOUNDATIONAL_CONSTITUTION.md §§4.3, 7.2 |
| Build psychological profiles from placements | FOUNDATIONAL_CONSTITUTION.md §§4.4, 7.2 |
| Rank cities without disclosing tradeoffs | FOUNDATIONAL_CONSTITUTION.md §§0.1, 2.4 |
| Claim certainty beyond what Layer 2 model supports | FOUNDATIONAL_CONSTITUTION.md §§3.1, 7.1 |
| Use destiny or fate language | AI_COMMUNICATION_DOCTRINE.md §9 |
| Display output that has not passed Guardian review | Track 7 is mandatory infrastructure |

**Constitutional alignment:** FOUNDATIONAL_CONSTITUTION.md §§7.6-7.9 — the three-role model governs all Navigator behavior.

### Key Decisions

1. **Prompt architecture.** How are constitutional constraints encoded into the prompt, and how is the Guardian used to enforce them at runtime (not relying on prompt alone)?

2. **Session model.** Decision: session lifecycle — how long does a session stay active, how is it resumed, how is it closed?

3. **Fluency inference model.** What are the specific signals the Navigator uses to update its fluency estimate per AI_COMMUNICATION_DOCTRINE.md §3?

4. **Checkpoint UX.** Decision: are checkpoints automatic (timed), user-triggered, or both?

### Dependencies

- Track 1: requires Approved entries and operational Model Resolver
- Track 2: Navigator is a runtime component; depends on Consultation Memory and Guardian
- Track 4: Navigator must produce SearchSpecs and hand off to Engine
- Track 7: Navigator output must pass Guardian before display

### Implementation Phase

**Phase 3** — after Tracks 1, 2, and 4 are operational.

---

## Track 6 — Astro Assist

**Cross-reference:** [`docs/canon/AI_CONSULTATION_ARCHITECTURE.md`](../canon/AI_CONSULTATION_ARCHITECTURE.md) §2 (Engine role) · [`docs/canon/INTENT_TRANSLATION_ENGINE.md`](../canon/INTENT_TRANSLATION_ENGINE.md) §§7-8

### Purpose

Implement Astro Assist: the professional copilot for practicing astrologers doing client relocation work. Astro Assist is a distinct product from Navigator. It does not guide a consumer through gradual intention clarification — it accepts explicit professional search criteria and translates them directly into SearchSpecs.

### Inputs

- Professional's explicit search criteria (explicit planet/house/aspect targets)
- Active Layer 2 model (professional's override model if one exists; default model otherwise)
- Layer 2 entries (via Model Resolver)
- SearchSpec schema (Track 4)
- Guardian (all output passes through Guardian before display; Track 7)

### Outputs / Deliverables

| Deliverable | Description |
|-------------|-------------|
| Astro Assist implementation | Running AI component for professional use |
| Direct SearchSpec translation | Translates explicit professional criteria into SearchSpec without consumer-level clarification loop |
| Viable substitute finder | When ideal placements are geographically unavailable, finds related alternatives and explains tradeoffs |
| Threading the needle | Identifies locations satisfying multiple competing criteria |
| Overlay strategy output | Returns overlay branches, viable geographic conditions, and shareable map configurations — not city lists |
| City identification (downstream) | On explicit professional request after user-selected places, identifies cities within confirmed viable regions |
| Recalculate more | On request, generates additional alternative strategies |
| Client report material | Produces location rationale text, summaries, and tradeoff explanations suitable for client use |

**Distinction from Navigator:**

| Dimension | Navigator | Astro Assist |
|-----------|-----------|--------------|
| Target user | Consumer; may have no astrological vocabulary | Professional astrologer |
| Starting point | Vague intentions | Explicit search criteria |
| Clarification style | Progressive, conversational, education-rich | Direct, technical, minimal scaffolding |
| SearchSpec path | Built gradually through competing hypotheses | Produced directly from stated criteria |
| Output style | Narrative, educating, inviting | Precise, technical, client-report-ready |

**Scope limits — Astro Assist must NOT:**

| Prohibited | Why |
|------------|-----|
| Override professional judgment | FOUNDATIONAL_CONSTITUTION.md §2.2 — professional sovereignty |
| Act as a general astrology consultant | Same oracle constraint as Navigator |
| Produce reports without Guardian review | Track 7 is mandatory infrastructure |
| Use the consumer Navigator pattern | Different product; different UX |
| Claim symbolic equivalence between substitutes | Substitutes are related strategies, not equivalents (AI_CONSULTATION_ARCHITECTURE.md §9) |

**Pricing note:** Astro Assist is a likely premium or pro-tier feature. Pricing implications must be specified in the product roadmap before implementation.

### Key Decisions

1. **Professional Layer 2 model access.** If the professional has a custom Layer 2 model, Astro Assist uses it. Decision: how does the session detect and load the professional's active model?

2. **Client report generation.** AI-generated text must be distinguishable from factual chart data (FOUNDATIONAL_CONSTITUTION.md §5.5). Decision: format and labeling for client report material.

3. **Recalculate more UX.** Decision: how many strategy variants are returned on request, and how are they presented?

### Dependencies

- Track 1: requires Approved entries, operational Model Resolver, professional model support
- Track 2: Astro Assist is a runtime component
- Track 4: produces SearchSpecs; receives Engine results
- Track 7: all output passes through Guardian

### Implementation Phase

**Phase 3** — can run in parallel with Navigator after Track 5 establishes the core runtime infrastructure both share.

---

## Track 7 — Guardian

**Cross-reference:** [`docs/constitutional/FOUNDATIONAL_CONSTITUTION.md`](../constitutional/FOUNDATIONAL_CONSTITUTION.md) §7 · [`docs/canon/AI_CONSULTATION_ARCHITECTURE.md`](../canon/AI_CONSULTATION_ARCHITECTURE.md) §2 · [`docs/canon/PATTERN_RECOGNITION_AND_MEANING_DOCTRINE.md`](../canon/PATTERN_RECOGNITION_AND_MEANING_DOCTRINE.md) §5

### Purpose

Implement the Guardian: the review contract that audits all AI output before it is displayed to any user. The Guardian is mandatory infrastructure, not an optional feature. No output from Navigator, Astro Assist, or any other AI component reaches the user without passing through the Guardian.

The Guardian is NOT a content filter. It is a structural review of whether AI output respects constitutional doctrine.

### Inputs

- AI output (from Navigator, Astro Assist, or any other AI component)
- Active Consultation Canon (to verify consistency with session state)
- Active SearchSpec (to verify output is grounded in the current search context)
- Layer 2 entries (via Model Resolver, to verify claims are grounded in approved symbolic grammar)
- FOUNDATIONAL_CONSTITUTION.md §7 (the constitutional standard)

### Outputs / Deliverables

| Deliverable | Description |
|-------------|-------------|
| Guardian implementation | Running review contract gating all AI output |
| Review decision | Pass / Revise with specific failure category |
| Failure explanations | When output fails, Guardian returns the specific category and violation description for revision |
| Audit log | Every Guardian decision logged with output hash, decision, and failure category |

**Review criteria — Guardian checks all AI output for:**

| Category | Description |
|----------|-------------|
| Hallucination | Claims about specific cities or placements not supported by Layer 2 entries or Layer 1 data (FOUNDATIONAL_CONSTITUTION.md §7.3) |
| Overclaiming | Statements of certainty beyond what the symbolic grammar warrants |
| Jargon overload | Technical astrological language used without appropriate translation for the current user's fluency level |
| Goal substitution | AI optimizing for engagement or comfort rather than accuracy; telling the user what they want to hear (FOUNDATIONAL_CONSTITUTION.md §7.4) |
| Unsupported astrology | Claims about astrological symbolism not grounded in the active Layer 2 model |
| Hidden ranking | Presenting one location as objectively better than another without surfacing conditional tradeoffs |
| Irrelevant chatbot behavior | Off-topic responses, personality-like behavior, general-assistant behavior outside consultation scope |
| Failure to preserve user judgment | AI making a decision the user should make; closing interpretive space prematurely (FOUNDATIONAL_CONSTITUTION.md §7.6) |
| Oracle behavior | Declarations such as "move here," "this is your best city," "this is your ideal location" |
| Fabricated certainty | Implying confidence in specific outcomes not derivable from chart conditions (FOUNDATIONAL_CONSTITUTION.md §7.2) |
| Fact/interpretation confusion | Presenting an interpretation as a factual chart condition without appropriate labeling |
| Destiny or fate language | Cosmic guarantee language, prophecy voice, or manipulative certainty (FOUNDATIONAL_CONSTITUTION.md §4.3) |

**Scope limits — Guardian must NOT:**

| Prohibited | Reason |
|------------|--------|
| Censor astrological content for comfort | Not a content filter; must not flatten difficult placements |
| Suppress legitimate tradeoff language | Tradeoffs are constitutional (FOUNDATIONAL_CONSTITUTION.md §4.5) |
| Block output because it is complex | Complexity is not a failure category |
| Rewrite output | Guardian passes or fails; it does not rephrase |

### Key Decisions

1. **Synchronous vs. asynchronous review.** Decision: synchronous (safest; higher latency) or asynchronous (brief hold window)? Synchronous recommended for beta.

2. **Revision loop.** When Guardian returns a failure, the output returns to the generating component for revision. Decision: how many revision attempts before the output is dropped and a fallback is shown?

3. **Fallback response.** If output cannot pass review after revision attempts, the user receives a fallback. Decision: what does the fallback say? It must not expose the failure category.

4. **Audit log access.** Decision: who has access, at what granularity, and how long is it retained?

### Dependencies

- Track 2: Guardian is defined as a runtime component
- Track 1: Guardian needs the Model Resolver to verify claims are grounded in Layer 2

### Implementation Phase

**Phase 2** — Guardian specification and implementation must be complete before any Track 5 or Track 6 code ships to users. The Guardian does not wait for Navigator to be production-ready; it is a prerequisite.

---

## Track 8 — Knowledge Ingestion (Future, Not Immediate)

**Status:** Future scope. Not for immediate implementation.

**Cross-reference:** [`docs/canon/LAYER_2_AUTHORING_ARCHITECTURE.md`](../canon/LAYER_2_AUTHORING_ARCHITECTURE.md) §§5, 9 · [`docs/canon/AI_CONSULTATION_ARCHITECTURE.md`](../canon/AI_CONSULTATION_ARCHITECTURE.md) §§9, 13, 14

### Purpose

Define the future Knowledge Ingestion pipeline allowing professional astrologers to upload their own body of work and extract structured knowledge assets from it. This track is explicitly deferred and must not be implemented until Tracks 1-7 are stable and the Layer 2 Wizard platform is operational.

### Scope

**What knowledge ingestion covers:**

| Capability | Description |
|------------|-------------|
| Source material upload | Upload readings, transcripts, voice notes, books, articles |
| Relocation grammar extraction | Extract PIH/ASP/DIG entry candidates for professional review |
| Voice and style extraction | Extract the professional's characteristic communication style |
| Methodology extraction | Extract the professional's approach to relocation consultation |
| Client data anonymization | Anonymize client names and birth data before any extraction processing |
| Source deletion | Delete source material by default after extraction is complete |
| Approved assets only | Preserve only knowledge assets the professional has reviewed and approved |
| Deletion audit log | User-auditable log of what was uploaded and deleted |

**What knowledge ingestion does NOT do:**

| Prohibited | Reason |
|------------|--------|
| Retain identifiable client data | Privacy; moral data use limits (FOUNDATIONAL_CONSTITUTION.md §5) |
| Use extracted content without professional review | Extracted entries are candidates, not approved grammar |
| Auto-publish extracted entries to a marketplace | Marketplace is explicitly deferred |
| Override the professional's existing Layer 2 model silently | All extractions are new candidates; no silent rewrites |

**Future visibility tiers (all deferred):**

| Tier | Scope |
|------|-------|
| Private | Used only within the professional's own Layer 2 model |
| Practice-internal | Shared within a practice or small team |
| Marketplace | Available to other professionals (requires explicit opt-in and commercial terms) |
| Commercial | Sold as a premium ontology pack |

**Marketplace/store is explicitly deferred.** Infrastructure for private ingestion may be built earlier, but public marketplace functionality waits for a separate track and a specific product decision.

### Implementation Phase

**Phase 5** — after all Tracks 1-7 are stable and the Layer 2 Wizard platform (LAYER_2_AUTHORING_ARCHITECTURE.md L2-P0 through L2-P8) is operational.

---

## Implementation Phase Summary

| Phase | Tracks | Description | Prerequisite |
|-------|--------|-------------|--------------|
| Phase 0 | 1 (spec), 2 (spec), 3 (spec), 7 (spec) | Planning and specification. This document. | None — runs in parallel with Web2 QA |
| Phase 1 | Track 1 | Layer 2 Foundation: entry type freeze, validator, model resolver, approval lifecycle, review pass | None |
| Phase 2 | Tracks 2, 4, 7 | Runtime Architecture implementation; SearchSpec schema; Guardian build | Track 1 Phase 1c operational |
| Phase 3 | Tracks 5, 6 | Navigator and Astro Assist implementation | Tracks 1, 2, 4, 7 operational |
| Phase 4 | Track 3 | Interaction Surface implementation | Tracks 1-7 operational |
| Phase 5 | Track 8 | Knowledge Ingestion | Tracks 1-7 stable; Layer 2 Wizard operational |

---

## Hard Gates — No Production AI Without

1. At least the minimum required Layer 2 entry set is Approved (not Draft) through the Wizard review path
2. Guardian is operational and running synchronously on all AI output before display
3. Every consultation session is bound to a specific, pinned manifest version
4. No AI component displays output that has not passed Guardian review
5. Web2 instrument remains fully functional with all AI components disabled (FOUNDATIONAL_CONSTITUTION.md §7.5)

---

*Planning complete. Documentation only. No code changes. No database migrations. No production AI active.*
