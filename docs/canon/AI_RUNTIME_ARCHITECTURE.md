# AI Runtime Architecture

**Status:** Canonical architecture doctrine — not active Beta implementation
**Date:** 2026-06-27
**Mode:** Documentation only — no code, no migrations, no UI changes
**Authority:** Subordinate to [`FOUNDATIONAL_CONSTITUTION.md`](../constitutional/FOUNDATIONAL_CONSTITUTION.md)
**Companions:** [`AI_CONSULTATION_ARCHITECTURE.md`](AI_CONSULTATION_ARCHITECTURE.md) · [`INTENT_TRANSLATION_ENGINE.md`](INTENT_TRANSLATION_ENGINE.md) · [`AI_COMMUNICATION_DOCTRINE.md`](AI_COMMUNICATION_DOCTRINE.md) · [`WEB3_AI_IMPLEMENTATION_ROADMAP.md`](../roadmaps/WEB3_AI_IMPLEMENTATION_ROADMAP.md)

> **Promotion rule:** This document describes future AI capability. Nothing here becomes active until explicitly promoted into an implementation plan with scope, migration plan, validation gate, and rollback path. The Web2 instrument remains sovereign.

> **Relationship to AI_CONSULTATION_ARCHITECTURE.md:** That document defines the five AI roles conceptually (Navigator AI, Engine, Ontology Assistant, Consultation Memory Agent, Guardian). This document translates those roles into concrete runtime components: what gets deployed, what each component's API surface is, what it reads and writes, and what it must not do. These documents are complementary. This document does not redesign the role definitions.

---

## §1 Purpose and Scope

This document defines the runtime components of the AI system — the concrete, deployable objects that implement the AI roles established in AI_CONSULTATION_ARCHITECTURE.md.

**In scope:**
- Component definitions: purpose, inputs, outputs, scope limits
- Data contracts between components
- Data flow through the system
- Constitutional scope limits enforced at the component boundary
- Implementation sequencing

**Out of scope:**
- Prompt engineering and model selection (separate implementation documents)
- UI implementation (see `docs/canon/AI_INTERACTION_SURFACES.md`)
- Layer 2 entry authoring (see `docs/canon/LAYER_2_AUTHORING_ARCHITECTURE.md`)
- Pricing and packaging decisions
- Knowledge Ingestion pipeline (Track 8; explicitly deferred)

**Constitutional anchor:** Reveal structure. Preserve judgment. (FOUNDATIONAL_CONSTITUTION.md §0.1)

The runtime components exist to illuminate astrological structure in geography. They do not replace the Layer 1 instrument. They do not make decisions for the user. They do not produce hidden rankings. They are instruments of clarity, not authority.

---

## §2 Runtime Components

### §2.1 Navigator

**Role mapping:** Navigator AI (AI_CONSULTATION_ARCHITECTURE.md §2)

**Purpose:** The consumer-facing orchestrator. Manages the full consultation loop from intake through search refinement and result presentation. The Navigator is the only AI component that speaks directly to the user in the consumer experience. It mediates between the user and all other components.

**Inputs:**
- User messages (from the active interaction surface)
- Surface context object (what surface the user is on; what they are looking at; see AI_INTERACTION_SURFACES.md §3)
- Consultation Canon read access (current state of the session's intention, constraints, evidence log)
- SearchSpec results (returned by Engine after execution)
- Guardian approval decision (the Guardian must pass Navigator output before it reaches the user)

**Outputs:**
- User-facing messages (all subject to Guardian review before display)
- Updated Consultation Canon fields (passed to Consultation Memory for persistence)
- SearchSpec (produced from accumulated intention evidence; passed to Engine)
- Surface action requests (e.g., launch map overlay, open saved search, open Genie) — passed to Genie/Map adapter

**Scope limits — Navigator must NOT:**

| Prohibited | Constitutional basis |
|------------|----------------------|
| Speak to users without passing Guardian review | Guardian is mandatory infrastructure; no exceptions |
| Function as a general astrology chatbot | Oracle pattern; FOUNDATIONAL_CONSTITUTION.md §7.1 |
| Build psychological profiles from chart placements | FOUNDATIONAL_CONSTITUTION.md §§4.4, 7.2 |
| Generate predictions about specific life events | FOUNDATIONAL_CONSTITUTION.md §§4.3, 7.2 |
| Rank cities without surfacing the conditional tradeoffs | FOUNDATIONAL_CONSTITUTION.md §§0.1, 2.4 |
| Claim certainty beyond what the active Layer 2 model supports | FOUNDATIONAL_CONSTITUTION.md §§3.1, 7.1 |
| Use destiny, fate, or cosmic guarantee language | AI_COMMUNICATION_DOCTRINE.md §9 |
| Make decisions the user should make | FOUNDATIONAL_CONSTITUTION.md §7.6 |
| Call Engine directly — must go through SearchSpec handoff | Keeps Engine decoupled from conversation |

---

### §2.2 Engine

**Role mapping:** Engine (AI_CONSULTATION_ARCHITECTURE.md §2)

**Purpose:** Executes a SearchSpec against the Layer 1 astrological data layer and returns scored results. The Engine does not speak to users. It does not manage conversation state. It is closer to a query compiler and executor than a conversationalist.

**Inputs:**
- SearchSpec (produced by Navigator or Astro Assist)
- Layer 1 data access (astronomy, relocated charts, overlay positions, point conditions)
- Layer 2 Model Resolver (to verify that search logic is grounded in approved symbolic grammar)

**Outputs:**
- Scored result set (candidate cities/regions for each SearchSpec strategy variant)
- Strategy variant descriptions (named variants, not raw scores — e.g., "Creative Recognition path," "Mastery path")
- Transparency notes (what was tried, what worked, what was substituted, what tradeoff was introduced)
- Partial match disclosures (when exact specification cannot be satisfied in geography)

**Scope limits — Engine must NOT:**

| Prohibited | Reason |
|------------|--------|
| Speak directly to users | Navigator mediates all user communication |
| Return raw numeric scores to the user-facing layer | Scores must be translated into named categories before user display |
| Use Draft Layer 2 entries to ground search logic | Draft entries are not approved; only Approved entries may be used in production |
| Produce a single "best city" answer | Hidden ranking; FOUNDATIONAL_CONSTITUTION.md §0.1 |
| Silently collapse viable alternatives | Must preserve strategy variants as separate outputs |
| Execute climate_city_filters in v1 | Schema field present; execution deferred |
| Write to Layer 1 | Layer 1 is read-only for the AI system |

---

### §2.3 Guardian

**Role mapping:** Guardian (AI_CONSULTATION_ARCHITECTURE.md §2)

**Purpose:** Audits all AI output before display to any user. The Guardian is mandatory infrastructure — not a feature, not optional. It enforces the constitutional doctrine structurally, at the component boundary.

The Guardian is NOT a content filter. It does not remove difficult astrological content. It does not comfort-smooth hard placements. It reviews whether the AI's output respects the constitutional doctrine defined in FOUNDATIONAL_CONSTITUTION.md §7 and AI_CONSULTATION_ARCHITECTURE.md §2.

**Inputs:**
- AI output (from Navigator, Astro Assist, or any AI component)
- Active Consultation Canon (to check consistency with session state)
- Active SearchSpec (to check that output is grounded in the current search context)
- Layer 2 Model Resolver (to verify claims are traceable to Approved entries)

**Outputs:**
- Review decision: Pass or Revise
- On Revise: specific failure category + description of the violation (returned to the generating component for revision)
- Audit log entry: output hash, decision, failure category, timestamp (internal; not user-facing)

**Review criteria (full list):**

| Category | What triggers it |
|----------|-----------------|
| Hallucination | Claim about a city or placement not supported by Layer 2 entries or Layer 1 data |
| Overclaiming | Statement of certainty beyond what the symbolic grammar warrants ("this will," "this guarantees") |
| Jargon overload | Technical astrological language used without appropriate translation for the user's inferred fluency level |
| Goal substitution | AI optimizing for user engagement or comfort rather than accuracy |
| Unsupported astrology | Astrological claim not traceable to the active Layer 2 model |
| Hidden ranking | One location presented as objectively better without surfacing the conditional tradeoffs |
| Irrelevant chatbot behavior | Off-topic, personality-like, or general-assistant behavior |
| Failure to preserve user judgment | AI making a decision the user should make; closing interpretive space prematurely |
| Oracle behavior | "Move here," "this is your best city," "this is your ideal location" |
| Fabricated certainty | Confidence in specific outcomes not derivable from chart conditions |
| Fact/interpretation confusion | Interpretation presented as a factual chart condition without labeling |
| Destiny or fate language | Cosmic guarantee language, prophecy voice, or manipulative certainty |

**Review criteria sourced from:**
- FOUNDATIONAL_CONSTITUTION.md §7 (all AI constitutional limits)
- PATTERN_RECOGNITION_AND_MEANING_DOCTRINE.md §5 (five evaluation questions)
- AI_CONSULTATION_ARCHITECTURE.md §2 (Guardian audit categories)

**Scope limits — Guardian must NOT:**

| Prohibited | Reason |
|------------|--------|
| Censor astrological content because it is difficult | Not a content filter; FOUNDATIONAL_CONSTITUTION.md §4.2 |
| Suppress legitimate tradeoff language | Tradeoffs are constitutional; FOUNDATIONAL_CONSTITUTION.md §4.5 |
| Block output because it is long or complex | Complexity is not a failure category |
| Rewrite output | Guardian passes or fails; revision belongs to the generating component |
| Be bypassed for any reason | Hard infrastructure requirement; no exception path |

**Revision loop:** When Guardian returns a Revise decision, the output is returned to the generating component with the failure category. The generating component revises and resubmits. Maximum revision attempts before fallback: 2 (proposed for beta). After 2 failed attempts, a fallback response is displayed to the user. The fallback must not expose the failure category.

---

### §2.4 Consultation Memory

**Role mapping:** Consultation Memory Agent (AI_CONSULTATION_ARCHITECTURE.md §2)

**Purpose:** Manages the Consultation Canon object for each user/profile/investigation. Creates timestamped evidence events autonomously when users provide new data points. Flags contradictions without deleting prior evidence. Offers periodic confirmation to the user without interrupting every exchange.

The Consultation Canon is not vague chat memory. It is product infrastructure: a persistent, structured object that represents the current state of a consultation session.

**Inputs:**
- Evidence events (from Navigator, triggered by user messages)
- User corrections (explicit user overrides of AI-generated entries)
- Periodic confirmation responses (user confirmations of the current Canon state)

**Outputs:**
- Consultation Canon (read access provided to Navigator, Engine, and Guardian)
- Evidence event log (append-only; contradiction entries preserved)
- Periodic confirmation requests (presented to user by Navigator at appropriate moments)

**Consultation Canon fields (from AI_CONSULTATION_ARCHITECTURE.md §3):**

```
Consultation Canon
  current_intention            -- what the user is trying to solve right now
  intention_certainty          -- inferred: hard / exploring / evolving
  hard_constraints             -- non-negotiable requirements
  soft_constraints             -- strong preferences, not dealbreakers
  cities_under_consideration   -- current working list
  current_location_baseline    -- where the user is now
  birth_time_certainty         -- certain / range / unknown
  birth_time_range             -- if range: earliest/latest
  emotional_signals            -- enthusiasm, hesitation, concern (timestamped)
  rejected_paths               -- explicitly ruled out (with reason and timestamp)
  promising_paths              -- surfaced but not yet decided
  relationship_family_risks    -- flagged asymmetries and pressure placements
  known_practical_constraints  -- visa, budget, health, schools, etc.
  open_questions               -- unresolved items the user is sitting with
  latest_confirmed_summary     -- last summary the user agreed was accurate
  evidence_events              -- append-only log
  ai_notes_awaiting_confirm    -- proposed updates not yet confirmed by user
  user_corrections             -- corrections applied by user
```

**Scope limits — Consultation Memory must NOT:**

| Prohibited | Reason |
|------------|--------|
| Delete evidence events | Evidence log is append-only; FOUNDATIONAL_CONSTITUTION.md §5.4 |
| Override user corrections with AI entries | User corrections supersede AI entries; FOUNDATIONAL_CONSTITUTION.md §2.1 |
| Allow the Canon to be modified without a session binding | Canon updates must be traceable to a session and evidence event |
| Expose raw Canon data to the user unprompted | Periodic confirmation pattern is controlled; not a raw data dump |

---

### §2.5 Layer 2 Model Resolver

**Role mapping:** Enables the Engine and Navigator to ground their outputs in approved symbolic grammar.

**Purpose:** A read-only lookup service. Given a manifest ID + entry type + subject (e.g., `beta_reference_ontology_v1`, `PIH`, `{planet: SUN, house: 10}`), returns the resolved entry using the inheritance chain: professional override model first, default model as fallback. The resolver never writes to Layer 2; it only reads.

**Inputs:**
- Manifest ID (binds the lookup to a specific, pinned version of the ontology)
- Entry type (e.g., PIH, ASP, DIG, ORB)
- Subject (structured: planet, house, aspect, dignity type, etc.)

**Outputs:**
- Resolved entry object (content payload + envelope, with status confirmed as Approved)
- Resolution trace (which model provided the entry: override or default)
- Null if no Approved entry exists for the given address

**Scope limits — Layer 2 Model Resolver must NOT:**

| Prohibited | Reason |
|------------|--------|
| Return Draft entries to the production AI pipeline | Draft entries are not approved for production use; BETA_V1_README.md §Review status |
| Write to the Layer 2 data store | Read-only; authoring goes through the Wizard (LAYER_2_AUTHORING_ARCHITECTURE.md) |
| Resolve entries against an unpinned manifest | Manifest pinning is required for session reproducibility |
| Return entries from a model the user/session has not selected | Models are scoped to the session's active model selection |

---

### §2.6 SearchSpec

**Role mapping:** Bridges Navigator/Astro Assist (intent) to Engine (execution).

**Purpose:** The SearchSpec is the structured object that formally serializes a consultation's current astrological search intent. It is produced by the Intent Translation Engine (INTENT_TRANSLATION_ENGINE.md §3) and consumed by the Engine. It is the contract between the conversation layer and the data layer.

Full SearchSpec schema is defined in the Web3 AI Implementation Roadmap, Track 4, and in the Track 4 implementation document when promoted.

**Inputs to SearchSpec production:**
- Accumulated intention evidence from the Consultation Canon
- Intent Translation Engine competing-hypothesis resolution
- User-approved strategy variant (from viability probing; INTENT_TRANSLATION_ENGINE.md §12)

**Outputs of SearchSpec consumption:**
- Engine result set (scored candidates per strategy variant)
- Map overlay parameters
- Saved search candidates
- Genie launch context

**Key SearchSpec fields (summary):**

| Field | Purpose |
|-------|---------|
| spec_id | Stable ID for this spec instance |
| manifest_id | Layer 2 manifest pinned to this spec |
| desired_placements | list of { planet, house or angle or aspect, weight } |
| avoids | list of { planet, house or angle or aspect, reason } |
| soft_preferences | list of { description, weight } |
| geographic_constraints | regions, countries, distance constraints |
| climate_city_filters | schema present; execution deferred |
| viable_alternatives | boolean: request alternative compositional strategies |
| recalculate_more | boolean: request additional alternatives |
| saved_search_handoff | trigger + name and description suggestions |
| genie_launch | trigger + context |
| map_overlay_launch | trigger + overlay parameters |
| transparency_notes | what was tried, substituted, tradeoff introduced |
| user_approved_path | which strategy variant the user selected |

**Scope limits — SearchSpec must NOT:**

| Prohibited | Reason |
|------------|--------|
| Contain raw numeric ranking scores | Hidden ranking; scores are translated into named categories by Engine |
| Be modified after user_approved_path is set without creating a new spec | Immutability of confirmed search; FOUNDATIONAL_CONSTITUTION.md §5.4 |
| Execute climate_city_filters in v1 | Deferred; schema field present but Engine does not execute it |

---

### §2.7 Genie/Map Adapter

**Role mapping:** Connects the AI system to the map and search UI layer.

**Purpose:** Translates AI-initiated actions into map and search layer operations. When the Navigator or Astro Assist determines that a search result should be shown on the map, launched as a saved search, or refined through the Genie conversational interface, the Genie/Map Adapter is the component that executes that transition. It preserves the connection between AI consultation state and the Web2 map instrument.

**Inputs:**
- Surface action request (from Navigator or Astro Assist)
- SearchSpec (provides the structured parameters for map and search operations)
- Consultation Canon excerpt (current session context)

**Outputs:**
- Map overlay launch (opens or updates map overlays matching the SearchSpec)
- Saved search creation (creates a saved search from the current SearchSpec)
- Genie launch (opens Genie pre-populated with the current SearchSpec context)
- Pin/favorites action (pins a city to the user's investigation)

**Scope limits — Genie/Map Adapter must NOT:**

| Prohibited | Reason |
|------------|--------|
| Modify the map state without user confirmation | User controls map state; AI initiates, user confirms |
| Create saved searches the user has not requested | FOUNDATIONAL_CONSTITUTION.md §5.1 |
| Expose internal SearchSpec fields to the Genie UI as raw JSON | SearchSpec is internal; Genie receives a user-readable version |
| Break the existing Web2 Genie experience | Genie adapter extends the Web2 Genie; it must not replace or corrupt it |

---

## §3 Data Flow Diagram

```
User message / surface context
          |
          v
    +----------+
    | Navigator |  <-- reads Consultation Canon (read-only)
    +----------+
          |
    +-----+-----+
    |           |
    v           v
+----------+  +--------------------+
|Consultation|  | Intent Translation |
|  Memory   |  |      Engine        |
| (Canon    |  | (produces SearchSpec|
|  updates) |  |  from evidence)    |
+----------+  +--------------------+
                     |
                     v
               +----------+
               |  Engine   |  <-- reads Layer 1 (astronomy, charts)
               +----------+       reads Layer 2 Model Resolver
                     |
                     v
               Result set + transparency notes
                     |
                     v
    +----------+<----+
    | Navigator |  (translates results into user language)
    +----------+
          |
          v
    +----------+
    | Guardian  |  (reviews all output before display)
    +----------+
          |
    Pass / Revise
          |
    Pass  +---> User display
          |
    Revise+---> Navigator revision (max 2 attempts) --> Fallback if fails
```

**Parallel paths:**

- Consultation Memory updates run asynchronously alongside the main conversation flow; they do not block Navigator responses.
- Layer 2 Model Resolver is called synchronously when Engine needs to ground a claim; result is cached within the session.
- Guardian runs synchronously before any output reaches the user.

**Map/Genie handoff (when AI initiates):**

```
Navigator (or Astro Assist)
     |
     v
SearchSpec (confirmed by user_approved_path)
     |
     v
Genie/Map Adapter
     |
     +---> Map overlay launch (updates map state)
     |
     +---> Genie launch (pre-populates Genie with SearchSpec context)
     |
     +---> Saved search creation (creates saved search from SearchSpec)
```

---

## §4 Scope Limits

**System-level prohibitions — no component may:**

| Prohibited | Constitutional basis |
|------------|----------------------|
| Write to Layer 1 | Layer 1 is truth; AI never edits truth (AI_CONSULTATION_ARCHITECTURE.md §1) |
| Display output that has not passed Guardian review | Guardian is mandatory infrastructure |
| Use Draft Layer 2 entries in production | Draft entries require Wizard approval (BETA_V1_README.md) |
| Produce a single "best city" answer | Hidden ranking; FOUNDATIONAL_CONSTITUTION.md §0.1 |
| Operate outside a pinned manifest version | Manifest pinning required for session reproducibility |
| Make the Web2 instrument non-functional | AI is additive; FOUNDATIONAL_CONSTITUTION.md §7.5 |
| Claim authority the user has not delegated | FOUNDATIONAL_CONSTITUTION.md §§2.1-2.3 |

---

## §5 Constitutional Alignment

Every runtime component is governed by the constitutional chain:

**First Law (FOUNDATIONAL_CONSTITUTION.md §0.1):** Reveal structure. Preserve judgment.

| Component | How it reveals structure | How it preserves judgment |
|-----------|--------------------------|---------------------------|
| Navigator | Guides user through astrological search; explains symbolic language | Does not decide; surfaces tradeoffs; invites user to choose |
| Engine | Executes search; returns named strategy variants | Does not select; returns multiple viable paths |
| Guardian | Reviews output for constitutional compliance | Enforces judgment preservation at infrastructure level |
| Consultation Memory | Preserves session evidence and corrections | User corrections supersede AI entries; Canon is user-auditable |
| Layer 2 Model Resolver | Returns approved symbolic grammar | Read-only; does not author or impose meaning |
| SearchSpec | Serializes user-approved search intent | Only executes user_approved_path; does not auto-select |
| Genie/Map Adapter | Connects AI session to map instrument | Initiates; user confirms before map state changes |

**Relevant constitutional sections:**

| Section | Governs |
|---------|---------|
| FOUNDATIONAL_CONSTITUTION.md §0 (First Law, Design Spirit, Operational Test) | All components |
| FOUNDATIONAL_CONSTITUTION.md §2 (Human Agency) | Navigator, Guardian |
| FOUNDATIONAL_CONSTITUTION.md §3 (Epistemic Integrity) | Engine, Guardian, Layer 2 Resolver |
| FOUNDATIONAL_CONSTITUTION.md §4 (Symbolic Humility) | Navigator, Guardian |
| FOUNDATIONAL_CONSTITUTION.md §5 (Moral Limits of Data Use) | Consultation Memory |
| FOUNDATIONAL_CONSTITUTION.md §7 (AI Constitutional Limits) | All components; Guardian specifically |
| AI_CONSULTATION_ARCHITECTURE.md §1 (Layer model) | All components; Layer 1 write prohibition |
| AI_COMMUNICATION_DOCTRINE.md (all sections) | Navigator, Astro Assist |
| PATTERN_RECOGNITION_AND_MEANING_DOCTRINE.md §5 (Guardian criteria) | Guardian |

---

## §6 Implementation Phases

| Phase | Components | Description |
|-------|------------|-------------|
| Phase 1 | Layer 2 Model Resolver | Requires Track 1 (entry type freeze, model resolver, approval lifecycle) |
| Phase 2 | SearchSpec schema, Engine (spec), Guardian | SearchSpec schema finalized; Guardian built and tested; Engine specified |
| Phase 3 | Navigator, Astro Assist, Engine (impl) | Full AI consultation loop; requires Guardian operational |
| Phase 4 | Genie/Map Adapter, surface wiring | Connects AI consultation to map and search UI |

**Deployment order within Phase 2/3:**
1. Guardian first — no AI output reaches users until Guardian is operational
2. SearchSpec schema second — Engine and Navigator both depend on it
3. Engine third — Navigator requires Engine to produce results
4. Navigator fourth — first user-facing AI component
5. Astro Assist fifth — parallel to or after Navigator

---

## §7 Open Questions / Deferred

| Question | Status | Depends on |
|----------|--------|-----------|
| Deployment model: monolith vs. microservice boundary for AI layer | Open | Architecture decision at Phase 2 start |
| State persistence boundary for Consultation Canon | Open | DB schema decision at Phase 2 start |
| Genie/Map Adapter mechanism: state bus vs. URL handoff vs. adapter API | Open | UI architecture decision at Phase 4 start |
| Guardian execution model: synchronous vs. asynchronous | Open; synchronous recommended for beta | Phase 2 decision |
| Guardian revision attempt limit | Open; 2 proposed for beta | Phase 2 decision |
| Climate/city filters execution | Deferred | Separate data layer integration track |
| Knowledge Ingestion pipeline | Deferred | Track 8; Phase 5 |
| Astro Assist professional model selection mechanism | Deferred | Requires Layer 2 model selection in Wizard (LAYER_2_AUTHORING_ARCHITECTURE.md) |
| Pricing model for Astro Assist | Deferred | Product roadmap decision |

---

*Planning complete. Documentation only. No code changes. No database migrations. No production AI active.*
