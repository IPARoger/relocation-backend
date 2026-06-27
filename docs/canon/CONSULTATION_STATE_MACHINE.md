# Consultation State Machine

**Status:** Canonical architecture doctrine — not active Beta implementation
**Date:** 2026-06-27
**Mode:** Documentation only — no code, no migrations, no UI changes
**Authority:** Subordinate to [`FOUNDATIONAL_CONSTITUTION.md`](../constitutional/FOUNDATIONAL_CONSTITUTION.md)
**Companions:** [`AI_CONSULTATION_ARCHITECTURE.md`](AI_CONSULTATION_ARCHITECTURE.md) · [`INTENT_COMPILATION_ENGINE.md`](INTENT_COMPILATION_ENGINE.md) · [`SEARCHSPEC_SCHEMA.md`](SEARCHSPEC_SCHEMA.md) · [`AI_RUNTIME_ARCHITECTURE.md`](AI_RUNTIME_ARCHITECTURE.md) · [`AI_INTERACTION_SURFACES.md`](AI_INTERACTION_SURFACES.md) · [`CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md`](CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md)

> **Promotion rule:** Nothing here becomes active until explicitly promoted into an implementation plan with scope, migration plan, validation gate, and rollback path. The Web2 instrument remains sovereign.

> **Overlay-first hard rule:** Search produces overlay branches and viable geographic regions — not candidate city lists. The map is the primary exploration surface. Cities and places enter only after user selection, comparison context, or explicit city-helper mode.

---

## §0 Design principles

**The AI is not the product. The Web2 instrument is.**

The state machine governs how the AI layer moves through a session. At every state the Web2 map, chart, and comparison instruments remain fully usable without AI involvement. The AI is additive assistance, not navigation replacement.

**What this document defines:**

- The lifecycle states of an AI-assisted relocation consultation
- For each state: purpose, owner, inputs, outputs, transitions, persistence, and Guardian involvement
- How Navigator, Intent Compiler, SearchSpec, Engine, Guardian, Map, and Consultation Memory coordinate
- The rules that prevent premature commitment, silent state change, and oracle behavior

**What this document does not define:**

- Prompt engineering or model selection
- UI design or component layout
- Layer 2 entry authoring (Wizard surface — defined separately)
- City Intelligence data layer implementation
- Pricing or session billing

**Naming convention — three product surfaces, shared infrastructure:**

| Surface | User | Starts from | Shares |
|---------|------|-------------|--------|
| **Navigator** | Consumer | Intake; vague intentions | SearchSpec schema, Engine, Intent Compiler, Guardian |
| **Astro Assist** | Professional astrologer | Explicit technical criteria | Same |
| **Wizard** | Ontology author / professional | Layer 2 entry authoring | Layer 2 infrastructure only; not consultation flow |

These are three product surfaces drawing from shared infrastructure — not three separate AIs. Wizard is not part of ordinary relocation consultation and does not participate in this state machine.

---

## §1 State machine overview

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                       IDLE                                              │
  │  Session exists. No active consultation. Map/instrument available.      │
  └──────────────────────────┬──────────────────────────────────────────────┘
                             │ user starts consultation
                 ┌───────────▼──────────────┐
                 │   INTAKE                 │  (Navigator) or direct criteria (Astro Assist → skip to INTENT COMPILATION)
                 └───────────┬──────────────┘
                             │ birth data present
                 ┌───────────▼──────────────┐
                 │ BIRTH-TIME RESOLUTION    │
                 └───────────┬──────────────┘
                             │ certainty established
                 ┌───────────▼──────────────┐
                 │   DISCOVERY              │  Navigator explores intentions
                 └───────────┬──────────────┘
                             │ sufficient evidence
                 ┌───────────▼──────────────┐
                 │   WORKING HYPOTHESIS     │  Compiler holds draft
                 └───────────┬──────────────┘
                             │ compiler runs
                 ┌───────────▼──────────────┐
                 │   INTENT COMPILATION     │  Intent Compiler runs passes
                 └───────────┬──────────────┘
                             │ SearchSpec(s) produced
                 ┌───────────▼──────────────┐
                 │  SEARCHSPEC PROPOSED     │  User reviews branches
                 └───────────┬──────────────┘
                             │ user confirms branch
                 ┌───────────▼──────────────┐
                 │   OVERLAY SEARCH         │  Engine executes
                 └───────────┬──────────────┘
                             │ overlays returned
                 ┌───────────▼──────────────┐
                 │   OVERLAY REVIEW         │  User/Navigator reviews overlay output
                 └──────┬────────┬──────────┘
                        │        │ wants to explore tradeoffs
           needs carve  │        ▼
                        │   TRADEOFF DISCUSSION
                        │        │
                        │        ▼
                 ┌──────▼──────────────────┐
                 │ OPTIMIZATION / CARVING   │  Navigator + Intent Compiler
                 └───────────┬──────────────┘
                             │ new SearchSpec proposed
                             ▼
                   (→ SEARCHSPEC PROPOSED, loop)

  From OVERLAY REVIEW (satisfied):
                 ┌───────────▼──────────────┐
                 │  BRANCH CONFIRMATION     │  User confirms strategy
                 └───────────┬──────────────┘
                             │
                 ┌───────────▼──────────────┐
                 │   MAP EXPLORATION        │  User explores map with active overlays
                 └───────────┬──────────────┘
                             │ user pins / selects place
                 ┌───────────▼──────────────┐
                 │   PLACE SELECTION        │  First place enters scope
                 └──────┬────────┬──────────┘
                        │        │
                        ▼        ▼
                 COMPARISON    CITY INTELLIGENCE
                        │        │
                        └───┬────┘
                            │
                 ┌──────────▼───────────────┐
                 │ REFLECTION / CHECKPOINT  │  Summary + save state
                 └──────────┬───────────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
         RESUME       new evidence    ARCHIVED / CLOSED
         (→ DISCOVERY  (→ INTENT
           or WORKING   COMPILATION)
           HYPOTHESIS)
```

---

## §2 State definitions

> **Common fields for every state:**
> - **Owner component:** which component is primarily active
> - **Persistence:** what is written to the Consultation Canon at entry/exit
> - **Guardian involvement:** what passes through Guardian review
> - **User-visible behavior:** what the user sees/can do
> - **Failure / fallback:** what happens if the state cannot complete

---

### State 1 — Idle

**Purpose:** Default resting state. A session exists (profile, chart data) but no active AI consultation is in progress. The Web2 instrument is fully operational. No AI output is generated.

**Owner:** None (Web2 instrument; no AI component active)

**Required inputs:** Valid user session; at least a profile record

**Produced outputs:** None (AI-side); map/chart/comparison instruments available as normal

**Allowed transitions:**
- → Intake: user initiates a new consultation via Navigator entry point
- → Resume: user reopens a previously checkpointed consultation
- → Intake (Astro Assist): professional opens Astro Assist with a client profile

**Forbidden transitions:** None — Idle is always accessible; the instrument never forces AI entry

**Persistence:** No Canon writes

**Guardian involvement:** None

**User-visible behavior:** Normal Web2 map, chart, profile, comparison surfaces. AI entry point visible but not active.

**Failure / fallback:** N/A — the instrument is fully available in Idle

---

### State 2 — Intake

**Purpose:** Collect the information required to begin astrological relocation consultation: birth data (date, place, time), current location, and the user's first statement of relocation intention. Astro Assist skips most of this if the client profile is already complete and the professional supplies criteria directly.

**Owner:** Navigator (consumer) / Astro Assist (professional — may shorten or skip)

**Required inputs:** User session; profile record (may be incomplete)

**Produced outputs:**
- Birth data (date, place, time — or time range / uncertainty declaration)
- Current location baseline
- First statement of intention (natural language)
- Evidence events written to Canon

**Allowed transitions:**
- → Birth-Time Resolution: birth data captured; time certainty unresolved
- → Discovery: birth data complete with acceptable certainty; Astro Assist with explicit criteria may go directly to Intent Compilation

**Forbidden transitions:**
- → Overlay Search (cannot skip compilation entirely)
- → Place Selection (no places before intent is established)

**Persistence:** Canon writes — `birth_time_certainty`, `current_location_baseline`, first `evidence_events[]`

**Guardian involvement:** All Navigator utterances in Intake pass through Guardian (no fabricated reassurance about birth-time, no oracle framing of the session)

**User-visible behavior:** Conversational intake. Questions feel like a conversation, not a form. Navigator introduces itself and the consultation model. Educational framing appropriate to user's inferred fluency (AI_COMMUNICATION_DOCTRINE.md §3).

**Failure / fallback:** If birth data cannot be established (user does not know date or place), Navigator explains what is and is not possible without it. Session may continue with partial consultation scope. No fabricated birth data.

---

### State 3 — Birth-Time Resolution

**Purpose:** Determine birth-time certainty and its impact on which consultation features are reliable. Governed by CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md §1. The system never fabricates a birth time.

**Owner:** Navigator + Consultation Flow Engine

**Required inputs:** Birth date and place; raw time statement (or "I don't know")

**Produced outputs:**
- `birth_time_certainty`: `exact` / `range` / `unknown`
- `birth_time_range`: start/end if range
- Stability assessment: which placements are stable vs. uncertain
- Recommendation: `proceed` / `proceed_with_caution` / `recommend_narrowing` / `pause_angle_work`

**Allowed transitions:**
- → Discovery: resolution complete; any outcome except full pause
- → Idle: user decides not to proceed given uncertainty (rare; Navigator should not push this)
- → Intake: user wants to revise stated birth data before proceeding

**Forbidden transitions:**
- → Intent Compilation (cannot compile before certainty is assessed — `birth_time_uncertainty` block in SearchSpec would be incomplete)
- → Overlay Search (cannot search with unassessed uncertainty)

**Persistence:** Canon writes — `birth_time_certainty`, `birth_time_range`; SearchSpec `§3.8` block populated on first compilation

**Guardian involvement:** Navigator explanation of what is/isn't reliable under the current certainty level passes through Guardian (no overclaiming stability; no discouraging exploration)

**User-visible behavior:** Navigator explains in plain language what is reliable, what is uncertain, and what the options are. No judgment about why the user doesn't know their birth time.

**Failure / fallback:** If user cannot narrow beyond "I have no idea," Navigator describes what remains useful (planetary overlays, sign-based work) and flags that house/angle-based work will require a confirmed birth time. Session continues in reduced scope rather than stopping.

---

### State 4 — Discovery

**Purpose:** Accumulate sufficient evidence to form a working hypothesis. Navigator explores the user's intentions, desires, constraints, and emotional signals through natural conversation. Evidence accumulates in the Consultation Canon. The Intent Compiler is not yet running.

**Owner:** Navigator; Consultation Memory Agent (writes evidence events)

**Required inputs:** Established birth data with certainty assessment; first intention statement from Intake

**Produced outputs:**
- Evidence events (append-only) written to Canon
- Typed evidence table: Evidence, Hypothesis, Preference, Constraint, Observation, Question
- Working hypothesis draft (not yet compiled into SearchSpec)

**Allowed transitions:**
- → Working Hypothesis: Navigator judges sufficient evidence exists to form a coherent hypothesis
- → Birth-Time Resolution: user provides new or revised birth-time information during conversation
- → Reflection / Checkpoint: user explicitly pauses ("let's stop here and save")
- → Archived / Closed: user ends session

**Forbidden transitions:**
- → Overlay Search (cannot search without a compiled spec)
- → Place Selection (no places before intent is established)

**Persistence:** Canon writes — ongoing `evidence_events[]`, `emotional_signals[]`, `hard_constraints[]`, `soft_constraints[]`, `open_questions[]`

**Guardian involvement:** All Navigator explanations and question prompts pass through Guardian. Key check: no premature narrowing, no fabricated certainty about what the user wants, no leading questions that steer toward specific conditions.

**User-visible behavior:** Conversational exploration. Navigator asks open questions. User is not filling a form. Navigator may explain relevant astrological concepts when fluency and appetite signals indicate interest (AI_COMMUNICATION_DOCTRINE.md §4). Map is available in background; user may browse independently.

**Failure / fallback:** If evidence remains insufficient after extended Discovery (Navigator cannot form a hypothesis), Navigator may name the gap explicitly ("I'm having trouble understanding what you most want from a new location — can you tell me about a time you felt at home somewhere?") rather than fabricating a hypothesis.

---

### State 5 — Working Hypothesis

**Purpose:** The Navigator and Intent Compiler hold a draft interpretation of the user's intentions. This is the pre-compilation staging area. The hypothesis is visible to the user for correction before compilation begins.

**Owner:** Navigator (presents hypothesis); Intent Compiler (holds draft state)

**Required inputs:** Typed evidence table from Discovery; at least one `Hard` or `Strong` intention signal

**Produced outputs:**
- Working hypothesis (plain-language summary of the compiler's current interpretation)
- Open question list (gaps that would change the spec if answered differently)
- Proposed compilation trigger (Navigator asks user to confirm the hypothesis is accurate enough to compile)

**Allowed transitions:**
- → Intent Compilation: user confirms hypothesis is close enough; Navigator triggers compilation
- → Discovery: user corrects the hypothesis (new evidence → return to Discovery briefly, then back)
- → Reflection / Checkpoint: user pauses here
- → Archived / Closed

**Forbidden transitions:**
- → Overlay Search (cannot skip compilation)
- → Branch Confirmation (no confirmed branches yet)

**Persistence:** Canon writes — `ai_notes_awaiting_confirm[]` (hypothesis as proposed but unconfirmed update); `latest_confirmed_summary` updated when user confirms

**Guardian involvement:** The hypothesis presented to the user passes through Guardian. Key check: no invented intentions (every hypothesis item traceable to evidence); no hidden ranking of the user's stated values.

**User-visible behavior:** Navigator presents the working hypothesis in plain language: "Here's what I understand so far about what you're looking for. Does this sound right?" User may correct, add, or remove items. Open questions are surfaced gently.

**Failure / fallback:** If the user disputes the hypothesis significantly (Navigator's interpretation was wrong), return to Discovery. Do not persist a disputed hypothesis as confirmed.

---

### State 6 — Intent Compilation

**Purpose:** The Intent Compiler runs all six compilation passes and produces one or more proposed SearchSpec objects. This is a deterministic, non-conversational operation. The Navigator waits for the result; it does not run during compilation.

**Owner:** Intent Compiler (INTENT_COMPILATION_ENGINE.md)

> **Note:** "Intent Compiler" is the preferred name for this component. It is the concrete implementation of what earlier documents called the Intent Compilation Engine (ICE).

**Required inputs:**
- Confirmed working hypothesis (or explicit trigger from Navigator)
- Full evidence event log from Canon
- Layer 2 Model Resolver (Approved entries only)
- Birth-time uncertainty block (from State 3)
- UI surface context (from AI_INTERACTION_SURFACES.md)
- Prior SearchSpec (if recompilation)

**Produced outputs:**
- One or more SearchSpec objects, `status: proposed`
- Per spec: `branch_variants[]`, `tradeoff_scan`, `audit_transparency`
- Gap analysis (open questions that blocked compilation of any condition)
- Recompilation delta (if this is a recompile: what changed from prior spec)

**Allowed transitions:**
- → SearchSpec Proposed: compilation succeeded; at least one proposed spec produced
- → Working Hypothesis: compilation failed (insufficient evidence; gap analysis returned to Navigator)
- → Discovery: critical open question identified during compilation that requires user input

**Forbidden transitions:**
- → Overlay Search (Engine cannot be invoked directly; must pass through SearchSpec Proposed and user confirmation)
- → Branch Confirmation (user has not reviewed the spec yet)

**Persistence:** New SearchSpec objects written to spec store with `status: proposed`. No Canon mutations. Audit transparency block populated.

**Guardian involvement:** The compiled spec itself is not user-facing. When the Navigator presents the spec to the user (in State 7), those explanations pass through Guardian.

**User-visible behavior:** Navigator may say "I'm putting together your search strategy — one moment." Loading indicator appropriate. User may not see raw compiler output.

**Failure / fallback:** If compilation cannot produce a well-formed spec (e.g., all conditions map to Draft Layer 2 entries; geographic constraints leave no viable region), the compiler returns a gap analysis. Navigator presents the gap honestly: "I wasn't able to build a complete search strategy because [gap]. Could you help me understand [missing piece]?"

---

### State 7 — SearchSpec Proposed

**Purpose:** Navigator presents the proposed SearchSpec branches to the user in plain language. User reviews, questions, and confirms a branch. This is the consent gate before the Engine runs.

**Owner:** Navigator

**Required inputs:** One or more proposed SearchSpecs from Intent Compilation; Guardian approval for presentation

**Produced outputs:**
- User-confirmed `approved_variant_id` (one branch selected)
- SearchSpec `status` updated: chosen branch → `confirmed`; others → `proposed` or `paused`

**Allowed transitions:**
- → Overlay Search: user confirms a branch
- → Optimization / Carving: user wants to adjust conditions before confirming
- → Tradeoff Discussion: user wants to understand a branch more deeply before choosing
- → Intent Compilation: user rejects all branches; new evidence gathered → recompile
- → Discovery: user wants to revisit intentions before confirming

**Forbidden transitions:**
- → Branch Confirmation (that state comes after Overlay Review, not here)
- → Place Selection (no places yet)

**Persistence:** On confirmation: `user_confirmation.confirmed_at`, `approved_variant_id` set; spec status → `confirmed`. Non-confirmed branches: `status: proposed` (not discarded).

**Guardian involvement:** All Navigator explanations of branch options, tradeoffs, and strategy labels pass through Guardian. Key checks: no hidden ranking of branches; no presenting one branch as obviously correct; no fabricated certainty about what the overlays will show.

**User-visible behavior:** Navigator explains each branch in plain language with its tradeoff summary. User can ask questions about any branch. Multiple branches are presented as genuine options, not as one "recommended" and others as fallbacks.

**Failure / fallback:** If user cannot choose ("I don't know which is right"), Navigator may suggest starting with the branch that matches the user's most frequently stated signal, while keeping others paused. Never forces a choice.

---

### State 8 — Overlay Search

**Purpose:** Engine executes the confirmed SearchSpec against Layer 1 data and returns overlay branches and viable geographic regions.

**Owner:** Engine (AI_RUNTIME_ARCHITECTURE.md §2.2)

**Required inputs:** Confirmed SearchSpec (`status: confirmed`, `user_confirmation.confirmed_at` set); Layer 1 data access; Layer 2 Model Resolver

**Produced outputs:**
- Overlay branches (per `branch_variants[]` in SearchSpec)
- Viable geographic regions per branch
- Map overlay configuration (`handoffs.map_overlay_launch`)
- Transparency notes (what was tried, substituted, traded off)
- Partial match disclosures (when exact conditions unavailable in geography)
- Strategy variant labels (named categories, not raw scores)

**Allowed transitions:**
- → Overlay Review: results returned
- → SearchSpec Proposed: Engine cannot produce any viable overlay (geography cannot satisfy spec) → recompile path
- → Reflection / Checkpoint: user pauses before reviewing results

**Forbidden transitions:**
- → Place Selection (map has not been opened yet; user has not explored)
- → City Intelligence (no user-selected places yet)

**Persistence:** Engine result set written to session cache. `engine_run_id` recorded in SearchSpec `audit_transparency`.

**Guardian involvement:** Engine output (overlay branches, geographic regions) is not user-facing directly. When Navigator explains results, those explanations pass through Guardian.

**User-visible behavior:** Map overlay launches (`handoffs.map_overlay_launch`). User sees highlighted geographic regions. Navigator explains what the overlay represents in plain language. No city list shown by default.

**Failure / fallback:** If Engine cannot satisfy the SearchSpec (no viable geographic region exists), Navigator presents the partial match honestly: "The combination you confirmed doesn't have strong coverage anywhere globally. Here's what was closest…" Offer recompilation with relaxed conditions.

---

### State 9 — Overlay Review

**Purpose:** User and Navigator review the overlay results together. Navigator explains what the highlighted regions mean relative to the user's stated intention. User can explore the map, ask questions, request tradeoff discussion, or confirm they are ready to explore.

**Owner:** Navigator; Map instrument

**Required inputs:** Engine results (overlay branches, viable geographic regions, map overlay configuration); confirmed SearchSpec for reference

**Produced outputs:**
- User reactions captured as evidence events
- Navigator explanations (Guardian-reviewed)
- Decision to proceed: explore map, discuss tradeoffs, optimize, or recompile

**Allowed transitions:**
- → Map Exploration: user is ready to explore the overlaid map
- → Tradeoff Discussion: user wants to understand gains/gives-up before exploring
- → Optimization / Carving: user wants to tighten or relax conditions
- → Intent Compilation: user rejects results entirely; recompile with new direction
- → Reflection / Checkpoint: user pauses

**Forbidden transitions:**
- → Place Selection (user has not pinned anything yet; map exploration comes first)
- → City Intelligence (no selected places)

**Persistence:** Evidence events for user reactions; Canon `promising_paths[]` or `rejected_paths[]` updated based on response

**Guardian involvement:** All Navigator explanations of overlay results pass through Guardian. Key checks: no overclaiming about what the highlighted regions mean; no presenting them as the user's "destiny zones"; no suppressing partial match disclosures.

**User-visible behavior:** Map is live with overlays. Navigator explains in plain language. User may zoom, pan, explore freely. Genie available for conversational map refinement. No city list presented proactively.

**Failure / fallback:** If user cannot interpret what they see, Navigator should explain the overlay structure more simply. If overlays are too broad to be useful, suggest Optimization / Carving.

---

### State 10 — Tradeoff Discussion

**Purpose:** Navigator and user reason through what is gained and given up in each branch or in specific overlay conditions. Governed by CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md §2. This state may occur before or after overlay results are shown.

**Owner:** Navigator; Tradeoff Reasoning Engine

**Required inputs:** `tradeoff_scan` block from SearchSpec; user's stated intention from Canon

**Produced outputs:**
- User reactions captured as evidence events (may trigger recompilation)
- Updated Canon: new preferences, revised weights, confirmed tradeoffs
- Potential new working hypothesis if tradeoffs reveal new direction

**Allowed transitions:**
- → Overlay Review: user resolves tradeoff discussion; ready to explore overlays
- → Optimization / Carving: discussion reveals a specific condition to add or relax
- → Intent Compilation: discussion reveals a fundamentally different intention → recompile
- → Discovery: user uncovers something genuinely new about what they want
- → Reflection / Checkpoint

**Forbidden transitions:**
- → Branch Confirmation (cannot confirm a branch before seeing overlay results)
- → City Intelligence (no selected places)

**Persistence:** Evidence events for new constraints or confirmed priorities; `tradeoff_scan.cross_branch_tensions` visible to user on request

**Guardian involvement:** All tradeoff explanations pass through Guardian. Key checks: no false certainty about tradeoffs ("choosing career definitely means sacrificing home"); tradeoffs must be conditional, not absolute.

**User-visible behavior:** Navigator presents the tradeoff frame: "Here's what this path gives you. Here's what it gives up. Here's what becomes harder." User is given space to reflect and respond. Navigator does not pressure a choice.

**Failure / fallback:** If the tradeoff cannot be explained clearly (too many interacting conditions), Navigator may simplify to the two most significant gains and the most significant concession.

---

### State 11 — Optimization / Carving

**Purpose:** Refine the current SearchSpec by tightening or relaxing specific conditions. Every carve is visible and explicit. No silent optimization. The result is a new proposed SearchSpec.

**Owner:** Navigator; Intent Compiler (carve pass)

**Required inputs:** Current confirmed SearchSpec; user-stated carve direction; `optimization_carving` block

**Produced outputs:**
- New proposed SearchSpec with `parent_spec_id` pointing to prior spec
- Carve delta (what changed, what was relaxed, why)
- New `tradeoff_scan` for the carved spec

**Allowed transitions:**
- → SearchSpec Proposed: carve produces a new proposed spec → user reviews
- → Overlay Search: user confirms the carved spec immediately
- → Working Hypothesis: carve reveals a more fundamental direction change
- → Reflection / Checkpoint

**Forbidden transitions:**
- → Branch Confirmation (user has not reviewed the carved result)
- → Place Selection (map exploration follows confirmation)

**Persistence:** New SearchSpec written with prior spec's `spec_id` in `parent_spec_id`. Prior spec: `status: superseded`. `optimization_carving` block populated with carve rationale.

**Guardian involvement:** Navigator's explanation of what was carved passes through Guardian. Key checks: no silent optimization (all carves disclosed); no presenting carving as "finding the perfect place."

**User-visible behavior:** Navigator explains: "I've tightened [condition] and relaxed [condition]. Here's the tradeoff that introduces." User confirms or rejects before the carved spec is executed.

**Failure / fallback:** If carving produces an empty geographic region (conditions too tight), Navigator reports this before the user waits for a failed search. Offer to relax specific conditions.

---

### State 12 — Branch Confirmation

**Purpose:** User makes an explicit strategic choice: which overlay branch to carry forward into map exploration. This is the commitment gate before sustained map work begins.

**Owner:** Navigator

**Required inputs:** At least one overlay result reviewed; user has sufficient information to choose

**Produced outputs:**
- Confirmed branch (`user_confirmation.approved_variant_id` set)
- Other branches: `status: paused` (not discarded; resumable)
- Active overlay set for Map Exploration

**Allowed transitions:**
- → Map Exploration: branch confirmed; overlays active
- → Tradeoff Discussion: user wants more clarity before committing
- → SearchSpec Proposed: user wants to review other branches again

**Forbidden transitions:**
- → Intent Compilation (confirmation has already passed through compilation)
- → City Intelligence (no selected places yet)
- Cannot confirm a different branch without returning to SearchSpec Proposed first (paused branches are not quietly swapped in)

**Persistence:** `user_confirmation` block populated. Branch retirement state updated for non-selected branches (→ `paused`). Canon `latest_confirmed_summary` updated.

**Guardian involvement:** Navigator's summary of what the user has chosen passes through Guardian. Key check: no oracle framing ("you've found your path"); no suggesting the confirmed branch is objectively correct.

**User-visible behavior:** Navigator summarizes the confirmed choice in plain language. "You've decided to explore [label]. The other [n] paths are saved and you can come back to them. Here's what the map shows." Map opens with confirmed overlays.

**Failure / fallback:** User cannot decide → remain in Tradeoff Discussion or offer to start exploring the most evidence-supported branch with all others staying paused.

---

### State 13 — Map Exploration

**Purpose:** User explores the map with active overlays. This is the primary Web2 product state for an AI-assisted session. The AI is present as a question-answerer and annotation layer, not as the driver. The user is exploring.

**Owner:** Map instrument (Web2); Navigator available for questions

**Required inputs:** Confirmed branch; active map overlays from Engine output

**Produced outputs:**
- User map interactions (pans, zooms, overlay layer toggles) — captured as behavioral evidence
- User questions about what they see → Navigator responses (Guardian-reviewed)
- Genie conversational refinements (if user opens Genie from map)
- Pinned places (user selects a place → triggers Place Selection state)

**Allowed transitions:**
- → Place Selection: user pins or selects a place on the map
- → Tradeoff Discussion: user asks a "what if" question that requires tradeoff reasoning
- → Optimization / Carving: user asks to tighten or expand the overlay
- → Reflection / Checkpoint: user pauses
- → Archived / Closed: user ends session

**Forbidden transitions:**
- → City Intelligence (City Intelligence requires a user-selected place; cannot be initiated from map exploration without a pinned place)
- → Branch Confirmation (branch already confirmed; to change branch → SearchSpec Proposed)

**Persistence:** Behavioral evidence events (significant map interactions) appended to Canon. No forced writes.

**Guardian involvement:** Any Navigator responses to user questions while in Map Exploration pass through Guardian.

**User-visible behavior:** Map with overlays. Pinwheel available on map for AI context. Genie available for conversational refinement. AI does not interrupt unsolicited while user explores.

**Failure / fallback:** If overlays fail to load, Web2 map remains functional without overlays. User can still use Genie and manual search. Navigator explains the issue without disrupting the session.

---

### State 14 — Place Selection

**Purpose:** A user-selected or pinned place enters the session scope. This is the gateway into per-place analysis. Cities and places are downstream of user map exploration — they are never imposed by the AI.

**Owner:** Map instrument; Navigator (context annotation)

**Required inputs:** User-initiated pin or place selection on the map

**Produced outputs:**
- `selected_places[]` added to session scope and Canon
- Place-level chart data requested (relocated chart for selected place)
- Navigator may offer to explain the astrological conditions at this place (on request or gently proactive)

**Allowed transitions:**
- → Comparison: user has selected multiple places and wants to compare
- → City Intelligence: user asks about practical factors for this place
- → Map Exploration: user pins a place, notes it, and returns to exploring
- → Overlay Review: user wants to understand why this place appears in the overlay
- → Reflection / Checkpoint

**Forbidden transitions:**
- Cannot trigger City Intelligence automatically without user intent signal (pin alone is not a request for CI)
- Cannot add places to a saved comparison without user confirmation

**Persistence:** `selected_places[]` updated in Canon. Relocated chart cached for selected place. Evidence event: "User selected [place]."

**Guardian involvement:** Navigator's annotation of why this place appears in the overlay (if offered) passes through Guardian. Key check: no oracle framing ("this is your place").

**User-visible behavior:** Place card opens. Navigator may offer: "Would you like me to explain what the overlay shows for [place]?" or "Want to compare this to other places you've pinned?" User initiates next step.

**Failure / fallback:** If relocated chart cannot be loaded (data unavailable for this location), Navigator explains. Session continues; user may still add the place to a comparison with partial data.

---

### State 15 — Comparison

**Purpose:** User compares two or more selected places across astrological conditions. Navigator provides narrative tradeoff analysis. The comparison instrument is a Web2 feature; the AI annotates it.

**Owner:** Comparison instrument (Web2); Navigator (annotation and tradeoff explanation)

**Required inputs:** At least two user-selected places with loaded chart data; confirmed SearchSpec (for context)

**Produced outputs:**
- Comparison table (Web2 instrument)
- Navigator tradeoff narrative per condition and per place pair (Guardian-reviewed)
- User reactions captured as evidence (may trigger recompilation or carving)
- Saved comparison (on user request)

**Allowed transitions:**
- → City Intelligence: user wants practical information about one or more compared places
- → Place Selection: user wants to add another place to the comparison
- → Tradeoff Discussion: user wants deeper reasoning on a specific comparison difference
- → Optimization / Carving: comparison reveals a condition the user wants to add or remove
- → Reflection / Checkpoint: user saves the comparison and pauses

**Forbidden transitions:**
- Navigator may not rank compared places as objectively better (FOUNDATIONAL_CONSTITUTION.md §0.1)
- Navigator may not add places to the comparison without user request

**Persistence:** Saved comparison written on user request. Evidence events for user reactions to comparison results.

**Guardian involvement:** All Navigator tradeoff narratives about comparison results pass through Guardian. Key checks: no hidden ranking; all comparative language conditional on stated intention; no "Place A is better."

**User-visible behavior:** Comparison table visible. Navigator explains differences in plain language ("Place A gives you a stronger MC contact; Place B gives you a more stable 4th. Given what you said about wanting roots first, the difference matters most here."). User decides what to do with the comparison.

**Failure / fallback:** If chart data is unavailable for one of the compared places, comparison proceeds with available data; gap is disclosed.

---

### State 16 — City Intelligence

**Purpose:** User requests practical (non-astrological) information about one or more user-selected places. City Intelligence is explicitly downstream of Place Selection — never a default AI output. The AI surfaces CI data without letting it silently override astrological structure.

**Owner:** Navigator; City Intelligence data layer

**Required inputs:** At least one user-selected place (`selected_places[]` populated); user intent signal that CI is wanted

**Produced outputs:**
- City Intelligence cards for the requested place(s): cost, visa, climate, schools, airports, etc.
- Navigator framing: what CI reveals, what it doesn't, how to weigh it against astrological findings
- User reactions captured as evidence

**Allowed transitions:**
- → Comparison: user wants to compare CI data alongside astrological data
- → Place Selection: user wants to look at another place's CI
- → Tradeoff Discussion: CI data introduces a practical tradeoff worth discussing
- → Reflection / Checkpoint: user wants to pause and think

**Forbidden transitions:**
- → Overlay Search (CI does not trigger a new astrological search)
- City Intelligence data may not override astrological structure silently — both must be surfaced and the user decides

**Persistence:** CI data cached for the session. Evidence event if user's stated practical constraints are updated based on CI findings.

**Guardian involvement:** All Navigator framing of CI data passes through Guardian. Key checks: no claiming certainty about practical factors (visa rules change; cost data is approximate); no using CI to implicitly recommend or disqualify a place.

**User-visible behavior:** CI cards visible for selected place(s). Navigator may say: "Here's what City Intelligence shows for [place]. This is practical, not astrological — it's a reality check alongside the chart work." User decides how to weigh it.

**Failure / fallback:** If CI data is unavailable for a place, Navigator discloses this. Session continues; user may request other places or proceed without CI.

---

### State 17 — Reflection / Checkpoint

**Purpose:** User and Navigator pause to review progress, save the consultation state, and confirm the current understanding is accurate. Checkpoints allow session resumption without context loss. Governed by AI_CONSULTATION_ARCHITECTURE.md §10.

**Owner:** Consultation Memory Agent; Navigator

**Required inputs:** Active consultation Canon; at least one confirmed summary or progress milestone

**Produced outputs:**
- Checkpoint object: snapshot of Canon at this moment
- `latest_confirmed_summary` updated
- Confirmed list of selected places, branches, key constraints, open questions
- Optionally: saved comparison, saved search, exported summary

**Allowed transitions:**
- → Resume: user ends session; returns later
- → Map Exploration: user confirms the checkpoint and continues
- → Discovery: new evidence emerged during reflection → brief return to Discovery
- → Intent Compilation: reflection reveals a direction change requiring recompilation
- → Archived / Closed: user ends the consultation intentionally

**Forbidden transitions:**
- No state is skipped through a checkpoint; a checkpoint is a pause, not a jump

**Persistence:** Checkpoint object written. All Canon fields frozen at checkpoint moment. Evidence log remains append-only.

**Guardian involvement:** Navigator's checkpoint summary passes through Guardian. Key check: summary accurately represents user's confirmed intentions; no Navigator editorializing about what the user "should" do.

**User-visible behavior:** Navigator presents a summary: "Here's where we are. You've confirmed [branch]. You've pinned [n] places. Your open questions are [x, y]. Does this sound right?" User confirms or corrects. Checkpoint visible in session history.

**Failure / fallback:** If Canon is in an inconsistent state (contradicting evidence with no resolution), Navigator surfaces the contradiction honestly as an open question rather than silently choosing one side.

---

### State 18 — Resume

**Purpose:** User returns to a consultation after a pause (hours, days, weeks). System reconstructs context from the last checkpoint and Canon state. User does not have to re-explain their situation.

**Owner:** Consultation Memory Agent; Navigator

**Required inputs:** Prior checkpoint object; active Canon; user session

**Produced outputs:**
- Re-established session context
- Navigator resumption greeting (references prior state without assuming current intent is unchanged)
- Offer: continue from last checkpoint, revisit a prior branch, or start fresh

**Allowed transitions:**
- → Discovery: user wants to revisit or update their intentions
- → Working Hypothesis: user confirms prior hypothesis still holds; jump back in
- → Map Exploration: user wants to return directly to the map
- → Overlay Search: a confirmed SearchSpec exists and the user wants to re-run it
- → Archived / Closed: user decides not to continue this consultation

**Forbidden transitions:**
- → Intent Compilation (cannot jump straight to compilation without Navigator confirming prior context is still valid)
- → Branch Confirmation (cannot confirm a branch the user hasn't reviewed since returning)

**Persistence:** Resume event written to Canon. Prior checkpoint re-read; no Canon mutation.

**Guardian involvement:** Navigator's resumption message passes through Guardian. Key check: no assuming the user's intentions are unchanged ("You were looking for career conditions last time — should we pick up where we left off?"); user must affirm.

**User-visible behavior:** Navigator: "Welcome back. Last time we were looking at [summary]. Is that still where you want to focus, or has something changed?" Clear options. No forced re-intake if context is intact.

**Failure / fallback:** If checkpoint is corrupt or unavailable, Navigator offers a brief re-intake rather than failing silently. Prior evidence log still available; compilation can restart.

---

### State 19 — Archived / Closed

**Purpose:** Consultation is intentionally ended or archived. The Canon and all SearchSpecs are preserved for reference. No AI components are active. Web2 instrument remains fully available.

**Owner:** Consultation Memory Agent (preservation); no active AI

**Required inputs:** User intent to close or explicit inactivity threshold

**Produced outputs:**
- Final Canon snapshot
- All SearchSpecs preserved in archive state
- Saved comparisons and saved searches retained

**Allowed transitions:**
- → Idle: user may start a new consultation at any time
- → Resume: archived consultations may be reopened (→ Resume state)

**Forbidden transitions:** None — Archived / Closed is a stable terminal state that can always be re-entered via Resume

**Persistence:** Canon status → `archived`. SearchSpecs: `status: archived`. Evidence log retained. Checkpoints retained.

**Guardian involvement:** None (no active AI output)

**User-visible behavior:** Session is closed. Prior work (saved searches, saved comparisons, pinned places, checkpoint summaries) visible in the profile. User may reopen via Resume.

**Failure / fallback:** N/A — if archival fails, consultation simply remains in its prior state; no data loss.

---

## §3 Recompilation within the state machine

Recompilation is not a state — it is a trigger that routes back through Intent Compilation from various states.

**Events that trigger recompilation:**

| Trigger event | Originating state | Routing |
|---------------|------------------|---------|
| New `Hard` or `Strong` evidence changes SearchSpec conditions | Discovery, Overlay Review, Tradeoff Discussion, Comparison | → Working Hypothesis → Intent Compilation |
| User corrects the working hypothesis | Working Hypothesis | → Intent Compilation |
| User rejects all proposed branches | SearchSpec Proposed | → Discovery → Intent Compilation |
| Birth-time certainty changes materially | Any state | → Birth-Time Resolution → Intent Compilation |
| User adds or removes a hard constraint | Any state | → Intent Compilation (may skip Working Hypothesis if delta is minor) |
| User requests a new carve direction | Optimization / Carving | → Intent Compilation (carve pass only) |

**Recompilation rules:**
1. Confirmed SearchSpecs are never mutated — a new spec is produced with `parent_spec_id`
2. Navigator presents the delta: what changed between prior and new spec
3. Non-confirmed branches from the prior spec are preserved in history, not discarded
4. The user is not required to re-confirm everything — only the delta requires review

---

## §4 Astro Assist flow

Astro Assist uses the same state machine with a shortened path:

```
  Client profile present + professional supplies explicit criteria
          │
          ▼
  INTAKE  (abbreviated — birth data only; no vague-intention discovery)
          │
          ▼
  BIRTH-TIME RESOLUTION
          │
          ▼
  INTENT COMPILATION  (direct; professional criteria → SearchSpec; no Discovery loop)
          │
          ▼
  SEARCHSPEC PROPOSED
          │
          ▼
  (rest of flow identical: Overlay Search → Map Exploration → Place Selection → Comparison → CI)
```

**States skipped in Astro Assist:**

| State | Reason skipped |
|-------|---------------|
| Discovery | Professional supplies explicit criteria; no vague-intention exploration needed |
| Working Hypothesis | Professional's criteria are the hypothesis; no Navigator confirmation loop |
| Branch Confirmation (extended) | Professional may move faster; tradeoff discussion abbreviated |

**States never skipped in Astro Assist:**

| State | Why preserved |
|-------|---------------|
| Birth-Time Resolution | Uncertainty still affects overlay reliability |
| Guardian review | All output passes through Guardian regardless of surface |
| Branch retirement rules | Branches still preserved; never silently discarded |
| Confirmed spec immutability | Same rule; recompilation produces new specs |

---

## §5 Cross-cutting rules

These rules apply in every state, every transition, every surface.

| Rule | Source |
|------|--------|
| Web2 instrument fully usable without AI at all times | FOUNDATIONAL_CONSTITUTION.md §7.5 |
| All user-facing AI output passes through Guardian before display | AI_RUNTIME_ARCHITECTURE.md §2.3 |
| Search produces overlay branches — not city lists | SEARCHSPEC_SCHEMA.md §1 |
| Cities / places enter scope only after user selection | INTENT_COMPILATION_ENGINE.md §14 |
| Confirmed SearchSpecs are immutable | SEARCHSPEC_SCHEMA.md §3.15 |
| New evidence triggers recompilation, not mutation | INTENT_COMPILATION_ENGINE.md §10 |
| Branches are never silently discarded | INTENT_COMPILATION_ENGINE.md §7 |
| Contradictory intentions produce separate branches | INTENT_COMPILATION_ENGINE.md §8 |
| Compiler confidence is not the user's confidence | INTENT_COMPILATION_ENGINE.md §9 |
| Navigator, Astro Assist, Wizard are surfaces — not separate AIs | §0 of this document |
| No oracle language, destiny framing, or fabricated certainty | FOUNDATIONAL_CONSTITUTION.md §4.3 |

---

## §6 Relationship to other canons

| Document | Relationship |
|----------|--------------|
| INTENT_COMPILATION_ENGINE.md | States 6, 11 (and all recompilation triggers) invoke the Intent Compiler |
| SEARCHSPEC_SCHEMA.md | States 6–9, 11 produce and consume SearchSpecs per this schema |
| AI_RUNTIME_ARCHITECTURE.md | Component definitions (Navigator, Engine, Guardian, Consultation Memory, Genie/Map Adapter) |
| AI_CONSULTATION_ARCHITECTURE.md | Consultation Canon fields; evidence event rules; checkpoint structure |
| CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md | State 3 (Birth-Time Resolution) and State 10 (Tradeoff Discussion) governed by this doc |
| AI_INTERACTION_SURFACES.md | Each state maps to one or more interaction surfaces; context object schema |
| AI_COMMUNICATION_DOCTRINE.md | Navigator speech in every conversational state governed by this doctrine |
| FOUNDATIONAL_CONSTITUTION.md | §7 governs Guardian behavior; §0.1 First Law applies in all states |

---

## §7 Open questions (deferred to implementation)

| Question | Status |
|----------|--------|
| Inactivity threshold before auto-archival | Open |
| Maximum Discovery session duration before forced checkpoint | Open |
| Recompilation delta presentation format | Open |
| Astro Assist session initialization via API vs. in-product | Open |
| Checkpoint export format (PDF, structured JSON, both) | Open |
| Multi-profile consultation (two people's charts compared) | Deferred |

---

*Planning complete. Documentation only. No code changes. No database migrations. No production AI active.*
