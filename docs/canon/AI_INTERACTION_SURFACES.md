# AI Interaction Surfaces

**Status:** Canonical architecture doctrine — not active Beta implementation
**Date:** 2026-06-27
**Mode:** Documentation only — no code, no migrations, no UI changes
**Authority:** Subordinate to [`FOUNDATIONAL_CONSTITUTION.md`](../constitutional/FOUNDATIONAL_CONSTITUTION.md)
**Companions:** [`AI_CONSULTATION_ARCHITECTURE.md`](AI_CONSULTATION_ARCHITECTURE.md) · [`AI_RUNTIME_ARCHITECTURE.md`](AI_RUNTIME_ARCHITECTURE.md) · [`AI_COMMUNICATION_DOCTRINE.md`](AI_COMMUNICATION_DOCTRINE.md) · [`WEB3_AI_IMPLEMENTATION_ROADMAP.md`](../roadmaps/WEB3_AI_IMPLEMENTATION_ROADMAP.md)

> **Promotion rule:** This document describes future AI interaction surfaces. Nothing here becomes active until explicitly promoted into an implementation plan with scope, migration plan, validation gate, and rollback path. The Web2 instrument remains sovereign.

> **Relationship to AI_RUNTIME_ARCHITECTURE.md:** That document defines the runtime components (Navigator, Engine, Guardian, etc.). This document defines where those components appear to the user: which surfaces they attach to, what context they receive automatically, and what they may and may not initiate.

---

## §1 Screen-Awareness Doctrine

**Core rule:** The AI must know what the user is looking at. The user must not have to explain their current context to the AI.

This doctrine is the architectural constraint that governs every surface definition in this document. Each surface entry specifies what context the AI receives automatically the moment the user activates the AI from that surface. The AI enters every conversation already knowing:

- Which surface the user is on
- What data is visible to the user on that surface
- What the user has been doing (active overlays, open cities, current comparison, etc.)

A user who opens the AI from the map pinwheel is looking at the map. The AI knows this and knows which overlays are active, which city is currently pinned, and what the user's last map interaction was. The user does not say "I'm looking at the map." The AI already knows.

**Why this matters:**

Requiring users to re-explain context is not just inconvenient — it is unconstitutional. The system exists to reveal structure that is already present. An AI that makes the user narrate their own screen is hiding the instrument behind the AI.

**How screen-awareness is implemented:**

Each surface passes a structured context object to the AI when the user activates it. The context object schema is defined per surface in §3. The context object is the mechanism by which the AI becomes screen-aware. It is not derived from chat history or user narration — it is injected from the application state.

**Screen-awareness does not mean surveillance:**

The AI receives the context that is directly relevant to what the user is looking at. It does not receive the full user history, browsing behavior, or cross-session data by default. The scope of the context object is bounded per surface.

---

## §2 Surface Definitions

### §2.1 Intake / First Experience

**AI component:** Navigator (AI_RUNTIME_ARCHITECTURE.md §2.1)

**Purpose:** The entry point into AI-assisted relocation consultation. The first experience is Navigator-led: it introduces the consultation model, collects the birth data needed for the session, resolves birth-time certainty, and captures the user's relocation intention. This surface is the only surface where AI initiation is unrestricted — it is the product's designed AI entry point.

**Context the AI receives automatically:**
- User's existing profile data (name, birth data if already entered, current location if known)
- Whether this is a first session or a resumed session
- If resumed: Consultation Canon (current intention, evidence log, cities under consideration, confirmed summary)
- Application locale and language

**What the AI can initiate:**
- Full intake flow: birth data collection, birth-time confidence resolution, intention capture
- Session resumption: offer to continue from last confirmed checkpoint
- Educational introduction to the consultation model (what the Navigator does, what it doesn't do)

**What the AI must NOT do from this surface:**
- Skip birth-time confidence resolution and assume an exact time (CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md §1)
- Begin running searches before intention is sufficiently established
- Introduce astrological vocabulary before gauging the user's fluency (AI_COMMUNICATION_DOCTRINE.md §3)
- Claim to know what the user wants before they have expressed it
- Make the intake feel like a form — it is a conversation

**Intake completion criteria:** The intake is complete when the AI has sufficient confidence in:
- Birth data (date, place; time with certainty level)
- Current location (baseline for relocation comparison)
- Primary intention (sufficient to begin translation)
- Practical constraints (visa, geography, urgency) if applicable

These are inferred from conversation, not checked off as a form. The Navigator proceeds when confidence is sufficient, not when all fields are filled (CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md §2).

---

### §2.2 Map Pinwheel

**AI component:** Navigator (AI_RUNTIME_ARCHITECTURE.md §2.1), via Genie/Map Adapter (§2.7)

**Purpose:** Screen-aware AI surface launched from the map UI. The user is looking at the map. The AI enters already knowing what is on the map and can interpret it, explain it, or extend it without the user having to describe what they see.

**Context the AI receives automatically:**
- Active overlays (which planet/house/angle/aspect overlays are currently displayed)
- Current map viewport (approximate geographic center and zoom level)
- Most recently pinned city (if any)
- Active saved search (if a saved search is loaded)
- Current Consultation Canon (if an active consultation session exists)
- Whether the user is in an active consultation or browsing independently

**What the AI can initiate:**
- Explain what the active overlays mean in plain language (per the user's fluency level)
- Explain why the currently visible geography is relevant to the user's intention
- Suggest adjacent overlays that might be worth adding based on current context
- Identify and name the astrological condition visible at a pinned city
- Offer to run a more refined search based on the visible overlap zone
- Open a Genie session pre-populated with the current search context

**What the AI must NOT do from this surface:**
- Ignore what is on the map and treat this as a general chat entry point
- Explain overlays in technical language without gauging the user's fluency
- Suggest running searches that are outside the user's stated intention without noting the departure
- Claim that what is visible on the map is "the best" zone without surfacing the conditional tradeoffs
- Modify the map state without user confirmation (the AI suggests; the user confirms)
- Override the user's current map session with a new one

---

### §2.3 Saved Searches

**AI component:** Navigator (AI_RUNTIME_ARCHITECTURE.md §2.1), via Genie/Map Adapter (§2.7)

**Purpose:** AI surface for working with saved searches. The user has an existing saved search open. The AI knows what that saved search contains (its SearchSpec) and can help name it, describe it, refine it, or explain what it is actually searching for.

**Context the AI receives automatically:**
- The SearchSpec of the currently open saved search
- The name and description of the saved search (if any)
- The result set or last-run results (if available)
- The current Consultation Canon (if an active consultation session exists)
- When the saved search was created

**What the AI can initiate:**
- Name a saved search in plain language if it is unnamed or has a cryptic name
- Describe what a saved search is actually looking for in non-technical language
- Explain what the saved search results mean relative to the user's stated intention
- Suggest refinements to the saved search based on the Consultation Canon
- Offer to open a Genie session to refine the saved search conversationally
- Offer to run the search again (if criteria have changed)

**What the AI must NOT do from this surface:**
- Modify the saved search without explicit user confirmation
- Delete or archive saved searches
- Rename a saved search without confirming the new name with the user
- Claim the saved search results are better or worse than alternatives without surfacing tradeoffs
- Create new saved searches without user request

---

### §2.4 Genie

**AI component:** Navigator (AI_RUNTIME_ARCHITECTURE.md §2.1), via SearchSpec (§2.6) and Genie/Map Adapter (§2.7)

**Purpose:** The conversational search refinement interface. Genie already exists as a Web2 structured search tool. The AI Genie surface extends it with natural-language conversation: the user can refine a search through dialogue rather than through UI controls alone. The AI Genie operates on the current SearchSpec and updates it through conversation.

**Context the AI receives automatically:**
- Current SearchSpec (the structured search that Genie is currently working on)
- Current result set (what the search has returned so far)
- Active Consultation Canon (if an active consultation session exists)
- Which surface the user came from when opening Genie

**What the AI can initiate:**
- Explain the current SearchSpec in plain language ("Here is what we are currently searching for...")
- Propose SearchSpec refinements based on the current results and the user's reactions
- Suggest alternative strategy variants when the current specification produces unsatisfactory results
- Explain the tradeoffs between the current search and a proposed refinement
- Execute a refined SearchSpec and present results
- Hand off a confirmed SearchSpec to the map overlay or save it as a saved search

**What the AI must NOT do from this surface:**
- Produce search results without passing them through the Guardian
- Replace the Web2 Genie's direct search controls — the AI layer is additive
- Modify the SearchSpec without presenting the proposed change to the user
- Execute searches that are materially outside the user's stated intention without noting the departure
- Collapse all alternative strategies into a single result before presenting options

---

### §2.5 Comparison

**AI component:** Navigator (AI_RUNTIME_ARCHITECTURE.md §2.1)

**Purpose:** AI surface for annotating and explaining city comparison results. The user has a comparison open between two or more cities. The AI knows which cities are being compared and which conditions are being compared, and can provide narrative-level tradeoff analysis.

**Context the AI receives automatically:**
- Cities being compared (list)
- Conditions being compared (overlay/planet/house/angle columns visible in the comparison)
- The comparison result data (actual values per city per condition)
- Current Consultation Canon (if an active consultation session exists)
- User's stated intention (from Canon, if available)

**What the AI can initiate:**
- Provide narrative-level tradeoff analysis for the cities being compared ("City A supports X; City B supports Y. Given your stated intention of Z, the relevant difference is...")
- Explain what a specific condition means in plain language when the user focuses on a column
- Identify which conditions are most relevant to the user's stated intention
- Flag conditions that are outside the user's stated intention but may be worth noting
- Suggest additional cities worth adding to the comparison based on the current search context

**What the AI must NOT do from this surface:**
- Rank cities as objectively better or worse — all comparative language must be conditional on the user's stated intention (AI_CONSULTATION_ARCHITECTURE.md §8)
- Present a single "recommended" city from the comparison
- Add cities to the comparison without user request
- Ignore the tradeoffs in the comparison and only emphasize positive conditions
- Use raw numeric scores or position rankings

---

### §2.6 Profile

**AI component:** Navigator (AI_RUNTIME_ARCHITECTURE.md §2.1)

**Purpose:** AI surface for explaining chart elements in the context of relocation. The user is looking at their birth chart or a relocated chart view. The AI knows which chart is open, which placement or overlay is active, and can explain what it means for relocation — not as a general personality reading.

**Context the AI receives automatically:**
- Which chart is open (birth chart or relocated to a specific city)
- If relocated: which city the chart is relocated to
- Which placement or element the user is currently focused on (if any)
- Active overlay (if the user came from a map overlay to this profile view)
- Current Consultation Canon (if an active consultation session exists)
- User's stated intention (from Canon, if available)

**What the AI can initiate:**
- Explain the astrological significance of the currently focused placement in the context of relocation
- Explain what changes between the birth chart and the relocated chart, and why those changes matter for the user's stated intention
- Provide tradeoff context when the user asks about a specific city's relocated chart
- Explain technical astrological terms in plain language appropriate to the user's fluency level
- Connect the chart element to the user's stated intention if one exists

**What the AI must NOT do from this surface:**
- Provide general personality readings from the chart — scope is relocation context only (FOUNDATIONAL_CONSTITUTION.md §7.1)
- Build psychological profiles from placements (FOUNDATIONAL_CONSTITUTION.md §§4.4, 7.2)
- Describe placements as deterministic life statements ("This placement means you will...")
- Speculate about the user's biography from chart elements
- Ignore the relocation context and treat this as a general natal chart reading surface

---

### §2.7 City Intelligence

**AI component:** Navigator (AI_RUNTIME_ARCHITECTURE.md §2.1), referencing City Intelligence data

**Purpose:** AI surface for generating and explaining City Intelligence cards. City Intelligence provides non-astrological decision reality: cost of living, visa, schools, hospitals, climate, safety, language, practical constraints. The AI can surface, explain, and contextualize City Intelligence data in relation to the user's astrological search results.

City Intelligence is the reality check and tiebreaker after astrology narrows the field (AI_CONSULTATION_ARCHITECTURE.md §1, Layer 5). The AI must not let City Intelligence data silently override astrological structure — it surfaces practical data alongside astrological findings, not after them as a hidden filter.

**Context the AI receives automatically:**
- Which city's City Intelligence is open
- Which City Intelligence cards are available and what they contain
- Current Consultation Canon (if an active consultation session exists)
- User's stated practical constraints (from Canon: visa, budget, health requirements, schools, etc.)
- Current astrological result context (what astrological conditions apply to this city)

**What the AI can initiate:**
- Explain what a City Intelligence card means in plain language
- Surface City Intelligence data that is directly relevant to the user's stated practical constraints
- Flag City Intelligence factors that may affect the user's stated intention (e.g., "You mentioned visa access; this city requires sponsorship")
- Provide a combined summary: what the astrological conditions suggest AND what the practical factors indicate
- Note when astrological and practical factors point in different directions (without collapsing the tension)

**What the AI must NOT do from this surface:**
- Let City Intelligence data override astrological structure silently — both must be surfaced and the user chooses (AI_CONSULTATION_ARCHITECTURE.md §1)
- Present a City Intelligence factor as a disqualification without noting that the user decides
- Generate City Intelligence data that is not sourced from the actual City Intelligence data layer
- Claim certainty about practical factors (visa rules change; cost data is approximate; AI must reflect this)
- Collapse astrological and practical factors into a single recommendation

---

### §2.8 Professional Astro Assist

**AI component:** Astro Assist (AI_RUNTIME_ARCHITECTURE.md §2.1, drawing on Astro Assist component from Track 6)

**Purpose:** Separate from Navigator. Designed for professional astrologers doing client relocation work. The professional enters with explicit search criteria, not vague intentions. Astro Assist operates with less scaffolding and produces output suited for client-facing reports.

This surface is a distinct UI entry point from the consumer Navigator. It is not a mode within Navigator. It is a separate product surface — likely premium/pro tier.

**Context the AI receives automatically:**
- Active professional Layer 2 model (professional's override model if one exists; default model otherwise)
- Active client profile (birth data for the client being researched)
- Any saved searches or investigations already open for this client
- Professional's previously stated criteria for this session (if resuming)

**What the AI can initiate:**
- Accept explicit professional search criteria and produce a SearchSpec directly (no consumer-level clarification loop)
- Identify viable locations satisfying the stated criteria
- Find symbolically related substitutes when ideal placements are unavailable in target geography
- Thread the needle: identify cities satisfying multiple competing criteria simultaneously
- Identify major cities within viable regions
- Produce client report material (location rationale text, tradeoff summaries, condition explanations) suitable for client-facing use
- Offer to recalculate with additional alternative strategies on request

**What the AI must NOT do from this surface:**
- Use the consumer Navigator pattern (no gradual intention clarification, no educational scaffolding)
- Override the professional's explicit criteria with inferred alternatives without disclosure
- Claim symbolic equivalence between substitutes — substitutes are related strategies, not equivalents
- Produce client reports without passing them through the Guardian
- Access or reference client birth data in a way that is not scoped to this session
- Grant professional mode access to non-professional users (authentication/authorization enforcement at the application layer)

**Distinction from Navigator (summary):**

| Dimension | Navigator (Consumer) | Astro Assist (Professional) |
|-----------|----------------------|-----------------------------|
| User | Consumer | Professional astrologer |
| Starting point | Vague intentions | Explicit criteria |
| Clarification style | Progressive, educational | Direct, technical |
| SearchSpec path | Built through conversation | Produced directly from criteria |
| Output style | Narrative, inviting | Precise, report-ready |
| Layer 2 model | Default | Professional's override model |

---

## §3 Context Propagation

Each surface passes a structured context object to the AI when activated. This is the mechanism for screen-awareness (§1). The context object is injected from application state — not derived from chat history or user narration.

**Base context object (all surfaces):**

```
BaseContext
  surface_id          -- which surface (intake, map_pinwheel, saved_search, genie,
                         comparison, profile, city_intelligence, astro_assist)
  user_id             -- authenticated user
  profile_id          -- which profile/chart is active
  session_id          -- current application session
  consultation_id     -- current AI consultation session (if any)
  consultation_canon  -- current Consultation Canon state (if consultation active)
  manifest_id         -- Layer 2 manifest version pinned to this session
```

**Surface-specific context extensions:**

| Surface | Additional context fields |
|---------|--------------------------|
| Intake | existing_profile_data, is_resumed_session, prior_canon_summary |
| Map pinwheel | active_overlays, viewport_center, viewport_zoom, pinned_city, active_saved_search_id |
| Saved searches | search_spec, saved_search_name, saved_search_description, last_run_results |
| Genie | current_search_spec, current_result_set, origin_surface |
| Comparison | cities_compared, conditions_compared, comparison_result_data |
| Profile | chart_type (birth or relocated), relocated_city, focused_placement, active_overlay |
| City Intelligence | city_id, available_ci_cards, stated_practical_constraints |
| Astro Assist | active_professional_model, client_profile, prior_session_criteria |

**Context propagation rules:**

1. Context is injected at the moment the user activates the AI from a surface — not at session start.
2. The context object reflects the application state at the time of activation, not historical state.
3. If the user navigates to a new surface while the AI is active, the context is updated to reflect the new surface.
4. Context updates from surface navigation are passed to the Navigator so it can acknowledge the transition without the user having to re-explain.
5. No context field may contain raw personally identifiable information beyond what is necessary for the session (birth data is session-scoped; it is not stored in the context object persistently).

---

## §4 Scope Limits Per Surface

**System-level scope limits — apply to all surfaces:**

| Prohibited | Basis |
|------------|-------|
| AI output displayed without Guardian review | Mandatory infrastructure (AI_RUNTIME_ARCHITECTURE.md §2.3) |
| AI output grounded in Draft Layer 2 entries | Draft entries not approved for production |
| AI making decisions the user should make | FOUNDATIONAL_CONSTITUTION.md §7.6 |
| AI ranking cities as objectively better without surfacing tradeoffs | FOUNDATIONAL_CONSTITUTION.md §§0.1, 2.4 |
| AI using destiny or fate language | FOUNDATIONAL_CONSTITUTION.md §4.3 |
| AI claiming certainty beyond what Layer 2 supports | FOUNDATIONAL_CONSTITUTION.md §7.1 |
| AI using astrology to demonstrate its own expertise | FOUNDATIONAL_CONSTITUTION.md §7.7 |

**Per-surface scope limits (summary):**

| Surface | Key prohibition |
|---------|----------------|
| Intake | May not skip birth-time resolution; may not begin searches before intention is established |
| Map pinwheel | May not modify map state without user confirmation; may not ignore active overlays |
| Saved searches | May not modify saved searches without explicit user confirmation |
| Genie | May not collapse alternative strategies before presenting them to the user |
| Comparison | May not rank cities without conditional tradeoff language; may not present a single "recommended" city |
| Profile | May not provide general personality readings; scope is relocation context only |
| City Intelligence | May not let CI data silently override astrological structure |
| Astro Assist | May not use consumer Navigator pattern; may not grant access to non-professional users |

---

## §5 Constitutional Alignment

**Three-role model (PATTERN_RECOGNITION_AND_MEANING_DOCTRINE.md §0):**

> Astrology provides structure. The AI reveals patterns. The user discovers meaning.

Every surface definition in this document is an application of this model:

- The surface context object reveals the structure the AI has access to.
- The AI reveals patterns visible in that structure.
- The user retains all decisions about what those patterns mean for their life.

**Per-surface constitutional alignment:**

| Surface | Reveals | Preserves |
|---------|---------|-----------|
| Intake | Structure of the user's relocation question | User's right to define their own intention |
| Map pinwheel | What the active overlays show geographically | User's right to interpret what they see |
| Saved searches | What a saved search is actually looking for | User's right to decide whether to refine or keep it |
| Genie | What a SearchSpec finds and what alternatives exist | User's choice between strategies |
| Comparison | What the astrological conditions actually differ between cities | User's choice about which difference matters |
| Profile | What the chart conditions mean in a relocation context | User's interpretation of their own chart |
| City Intelligence | What practical factors are relevant to this city | User's decision about whether practical factors are dealbreakers |
| Astro Assist | What the professional's search criteria find | Professional's judgment about what to do with the results |

**Relevant constitutional sections:**

| Section | Governs |
|---------|---------|
| FOUNDATIONAL_CONSTITUTION.md §0 (First Law, Design Spirit, Operational Test) | All surfaces |
| FOUNDATIONAL_CONSTITUTION.md §2 (Human Agency) | All surfaces; especially Comparison and Profile |
| FOUNDATIONAL_CONSTITUTION.md §4 (Symbolic Humility) | All surfaces; especially Profile and Comparison |
| FOUNDATIONAL_CONSTITUTION.md §7 (AI Constitutional Limits) | All surfaces; Guardian enforces |
| AI_COMMUNICATION_DOCTRINE.md §§3-4 (Fluency and appetite tracking) | Intake, Map Pinwheel, Profile, Genie |
| AI_COMMUNICATION_DOCTRINE.md §14 (Participatory meaning) | Profile, Comparison, City Intelligence |
| CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md §§1-2 (Birth-time resolution, intake) | Intake surface |
| CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md §3 (Tradeoff reasoning) | Comparison, Genie |

---

*Planning complete. Documentation only. No code changes. No database migrations. No production AI active.*
