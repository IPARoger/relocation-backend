# Intent Compilation Engine

**Status:** Canonical architecture doctrine — not active Beta implementation
**Date:** 2026-06-27
**Mode:** Documentation only — no code, no migrations, no UI changes
**Authority:** Subordinate to [`FOUNDATIONAL_CONSTITUTION.md`](../constitutional/FOUNDATIONAL_CONSTITUTION.md)
**Companions:** [`AI_RUNTIME_ARCHITECTURE.md`](AI_RUNTIME_ARCHITECTURE.md) · [`INTENT_TRANSLATION_ENGINE.md`](INTENT_TRANSLATION_ENGINE.md) · [`SEARCHSPEC_SCHEMA.md`](SEARCHSPEC_SCHEMA.md) · [`AI_CONSULTATION_ARCHITECTURE.md`](AI_CONSULTATION_ARCHITECTURE.md) · [`CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md`](CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md) · [`WEB3_AI_IMPLEMENTATION_ROADMAP.md`](../roadmaps/WEB3_AI_IMPLEMENTATION_ROADMAP.md)

> **Promotion rule:** This document defines future AI capability. Nothing here becomes active until explicitly promoted into an implementation plan with scope, migration plan, validation gate, and rollback path. The Web2 instrument remains sovereign.

> **Overlay-first hard rule:** The Intent Compilation Engine produces SearchSpecs that generate overlay branches, viable geographic regions, and map exploration surfaces — not city lists or city rankings. The map is the primary exploration surface. Users choose places.

---

## §0 Design axiom

**The Intent Compilation Engine is a compiler, not a conversationalist.**

It is not the Navigator. The Navigator speaks to the user.
It is not the Engine. The Engine executes SearchSpecs against Layer 1 data.
It is a deterministic compiler that transforms an evolving human conversation into one or more immutable SearchSpec objects.

The compiler's input is messy. Its output is clean.

The compiler's input changes over time. Its output is frozen the moment it is confirmed.

The compiler holds contradictions. Its output separates them into branches.

The compiler infers from evidence. Its output documents those inferences transparently.

If the compiler cannot produce a well-formed SearchSpec from the current evidence, it returns the current working hypothesis with a gap analysis — not a fabricated spec.

---

## §1 Position in architecture

```
  User
   │
   ▼
  Navigator  ◄──── surfaces context, UI state, Consultation Canon
   │
   ▼
  Intent Compilation Engine          ◄── this document
   │
   │   reads: Consultation Canon (evidence events, working hypothesis)
   │   reads: Current Working Hypothesis
   │   reads: Prior SearchSpec (if any — for recompilation)
   │   reads: UI surface context
   │   reads: Layer 2 Model Resolver (Approved entries only)
   │
   ▼
  SearchSpec(s)                      (one per coherent branch)
   │
   ▼
  Engine                             (executes against Layer 1)
   │
   ▼
  Overlay Branches + Viable Geographic Regions
   │
   ▼
  Map                                (primary exploration surface)
   │
   ▼
  User exploration
   │   User pins a place / selects from map
   ▼
  City Intelligence (downstream, user-selected places only)
```

**What the compiler does not touch:**

| Layer | The compiler's relationship |
|-------|-----------------------------|
| Layer 1 — Truth | Read-only via Layer 2 grounding. Never edits chart data. |
| Layer 2 — Ontology | Read-only. Selects participating entries. Never authors or rewrites them. |
| Layer 3 — Consultation Canon | Read input. May propose evidence event labels. Never overwrites. |
| Navigator speech | Out of scope. Navigator decides what to say. |
| Guardian review | Downstream. All SearchSpec-derived user output passes through Guardian before display. |

---

## §2 Evidence accumulation

The compiler ingests raw evidence from the Consultation Canon's append-only event log and classifies each item before it participates in compilation.

Evidence classification is itself a compiler pass (see §5, Pass 1).

### Evidence types

Each type has a distinct lifecycle and compilation role.

| Type | Definition | Lifecycle rule |
|------|------------|----------------|
| **Evidence** | A stated fact, preference, or behavioral signal the user expressed | Append-only. Never deleted. Recency weighted. Preserved through all recompilations. |
| **Hypothesis** | A compiler-inferred interpretation of one or more evidence items | Labeled as inferred. Must be confirmed or rejected by user/Navigator before becoming a SearchSpec condition with `required` weight. |
| **Preference** | A soft inclination — "I'd prefer X" without making it a constraint | Compiles to `soft_preferences` in SearchSpec. Never promoted to `required` without explicit user confirmation. |
| **Constraint** | An explicit non-negotiable boundary | Compiles to `hard_avoids` or `geographic_bounds`. Cannot be relaxed by the compiler. |
| **Observation** | A behavioral signal the compiler noted (hesitation, enthusiasm, silence, return to a topic) | Contributes to Hypothesis formation. Never compiles directly to a condition. Must be mediated through Hypothesis. |
| **Assumption** | A gap-filling inference the compiler makes when evidence is thin | Must always be labeled as an assumption in `audit_transparency`. Cannot carry `required` weight. |
| **Question** | An unresolved item the compiler identifies as blocking confident compilation | Surfaced in the working hypothesis gap analysis. Not suppressed. |

### Evidence lifecycle rules

1. **No evidence is deleted.** The compiler may weight earlier evidence less than recent evidence, but it never removes it from the record. The evidence log is append-only.

2. **Contradictions are preserved, not resolved by the compiler.** When two evidence items conflict, the compiler holds both and — if they imply different astrological conditions — produces separate branches (§6). It does not silently choose one.

3. **Assumptions must be declared.** Every gap-filling inference that becomes a SearchSpec condition must appear in `audit_transparency.what_tried` and `audit_transparency.what_substituted` with the label `[assumption]`.

4. **Hypotheses require confirmation before `required` weight.** A compiler-inferred hypothesis compiles as `moderate` or `weak` weight until the user or Navigator explicitly confirms it. The Navigator asks; it does not silently promote.

5. **Questions block confident compilation.** When a Question exists that, if answered differently, would change the SearchSpec materially, the compiler marks `birth_time_uncertainty.disclosure_required = true` or records the open question in `audit_transparency`. It does not speculate.

---

## §3 Intention strength

Intention strength governs the weight assigned to a condition when it enters a SearchSpec. It is **inferred by the compiler from evidence patterns** — not derived from a questionnaire or a user-facing slider.

| Strength | Definition | Compiles to |
|----------|------------|-------------|
| **Hard** | User has stated this as non-negotiable, explicitly, at least once without contradiction | `desired_conditions[].weight: required` or `hard_avoids[]` |
| **Strong** | User has stated this clearly and returned to it; no significant hesitation observed | `desired_conditions[].weight: strong` |
| **Exploratory** | User has expressed interest but also expressed openness to alternatives; no repeated signal | `desired_conditions[].weight: moderate`; may generate a branch variant |
| **Emerging** | A pattern the compiler infers from multiple soft signals, not yet named by the user | Compiles as `hypothesis` first; requires Navigator confirmation before entering SearchSpec |
| **Unknown** | Insufficient evidence to infer strength; active Question exists | Does not compile; recorded as open question in gap analysis |

**Inference rules:**

| Signal | Strength implication |
|--------|---------------------|
| Repeated return to a topic across sessions | Elevates strength by one level |
| Explicit "I need this, not just want it" | Sets Hard |
| Explicit "if I can't have this, I don't want to go" | Sets Hard |
| Hesitation or "but also" adjacent to a stated preference | Reduces to Exploratory |
| Rejection of a variant that preserved this condition | Elevates; the user noticed its absence |
| Acceptance of a result without noticing this condition was missing | May reduce; the user did not prioritize it when absent |
| Session-ending silence on a topic previously raised | Recorded as Observation; no automatic strength change |

---

## §4 Compiler invariants

These invariants hold across all compilation passes, all branches, all recompilation cycles.

1. **No invented intentions.** The compiler does not add conditions the user has not expressed — directly or inferrably from evidence. When a condition is inferred, it is labeled `[inferred]` and carries at most `moderate` weight until confirmed.

2. **No hidden substitutions.** Every substitution (planet moved from house to aspect, angle replaced by dignity condition, etc.) is documented in `audit_transparency.what_substituted`. Nothing is swapped silently.

3. **No silent optimization.** The compiler does not rank or prefer branches internally without disclosure. Strategy selection belongs to the user.

4. **No forgotten evidence.** Every evidence event that contributed to a condition must be traceable in `audit_transparency`. If the compiler ignored an evidence item (e.g., it was superseded by later evidence), the reason for ignoring it must be recorded.

5. **No erased branches.** A branch is never silently deleted. It may be archived, paused, or superseded — but always with a reason, and always visible to the user on request.

6. **No mutating confirmed SearchSpecs.** Once `user_confirmation.confirmed_at` is set on a SearchSpec, the compiler never modifies it. Recompilation produces a new spec with `parent_spec_id` pointing to the prior one.

7. **No city lists as default output.** Compiled SearchSpecs produce overlay branches. Cities are downstream of user-selected places. `city_helper_mode` is not set by the compiler; it is set only by explicit user or professional request.

---

## §5 Compilation passes

The compiler runs in six sequential passes. Passes are deterministic — the same evidence, run through the same passes, produces the same output. Passes do not produce user-facing output directly; all explanation flows through the Navigator.

### Pass 1 — Evidence classification

**Input:** Raw evidence event log (from Consultation Canon)
**Output:** Typed evidence table (see §2)

- Classify each event as Evidence, Hypothesis, Preference, Constraint, Observation, Assumption, or Question
- Assign recency weight (more recent evidence weighted higher)
- Flag contradictions: any two items that would compile to opposite conditions
- Produce open question list

### Pass 2 — Ambiguity resolution

**Input:** Typed evidence table
**Output:** Resolved evidence table; unresolved question list

- For each contradiction: determine whether evidence is temporally ordered (later supersedes earlier), mutually exclusive (requires separate branches), or ambiguous (requires Navigator question)
- For each Assumption: validate that it is genuinely necessary to complete a condition; flag as assumption in audit
- Produce `unresolved_questions[]` list for Navigator to surface when appropriate

### Pass 3 — Symbolic grammar mapping

**Input:** Resolved evidence table; Layer 2 Model Resolver
**Output:** Candidate conditions linked to Approved Layer 2 entries

- Map each resolved evidence item to one or more Layer 2 astrological conditions (planet, house, angle, aspect)
- For each mapping: verify the underlying Layer 2 entry is Approved, not Draft
- For each unmappable evidence item: record as `what_tried` without a candidate condition
- For each mapped condition: assign intention strength (§3) as weight

### Pass 4 — SearchSpec candidate generation

**Input:** Candidate conditions
**Output:** One or more candidate SearchSpec structures (one per coherent strategy path)

- Group compatible conditions into candidate branches
- Separate incompatible conditions into distinct candidate branches
- For each candidate: produce a `variant_label` and `variant_description`
- Assign `is_partial_match: true` where geography is unlikely to satisfy all required conditions simultaneously
- Produce the `tradeoff_scan` block per candidate (what you gain / what you give up)

### Pass 5 — Condition merging

**Input:** Candidate SearchSpec structures
**Output:** Merged SearchSpec structures where conditions are compatible

- Merge conditions that are compatible within a branch (e.g., two aspects to the same angle can coexist)
- Do not merge conditions that represent distinct life strategies (see §6)
- Produce the `desired_conditions[]` array with deduplicated, weighted conditions per branch
- Record any merge operations in `audit_transparency`

### Pass 6 — Branch separation

**Input:** Merged candidate SearchSpec structures
**Output:** Final set of distinct SearchSpec objects, one per coherent branch

- Confirm that each branch is internally consistent
- Apply `birth_time_uncertainty` to each branch (see SEARCHSPEC_SCHEMA.md §3.8)
- Populate `handoffs.map_overlay_launch` for each branch
- Set `status: proposed` on each output spec (not `confirmed`)
- Surface to Navigator for user presentation

---

## §6 Branch formation

The compiler must not collapse competing life strategies into a single averaged SearchSpec.

**Rule:** Any two conditions that represent meaningfully distinct life directions — where choosing one would produce materially different geographic overlap than choosing the other — must be compiled into separate branches.

### Examples of conditions that must not be merged

| Strategy A | Strategy B | Why separate |
|------------|------------|--------------|
| Career recognition (Sun/10th) | Home and family stability (Moon/4th) | Geographically anticorrelated in many charts |
| Adventure and novelty (Uranus/1st or 9th) | Settled creative practice (Venus/Saturn/5th) | Different signatures; different regions |
| Deep partnership (Venus/7th) | Independent expression (Sun/1st, Mars/1st) | Often in geographic tension |
| Spiritual withdrawal (Neptune/12th) | Public engagement (Jupiter/10th) | Different geographic character |

### Branch strategy labeling

Each branch receives a `variant_label` the Navigator can describe in plain language:

| Example variant label | What it represents |
|----------------------|-------------------|
| `"Career recognition path"` | MC emphasis — outer recognition, structured achievement |
| `"Family and home path"` | 4th house emphasis — roots, stability, place |
| `"Creative vitality path"` | Sun/Venus 5th — self-expression, enjoyment, generativity |
| `"Fresh start path"` | Uranus/1st or 9th — disruption, novelty, expansion |
| `"A2A workaround"` | Angle-to-angle aspects used when house placements are thin |

Branches are **never hidden** from the user. The Navigator presents them as distinct options, not as variants the system has already ranked.

---

## §7 Branch retirement

Branches are not deleted. They pass through explicit lifecycle states.

| State | Definition | User visibility |
|-------|------------|----------------|
| `active` | In current working hypothesis; presented to user | Fully visible |
| `proposed` | Compiled; awaiting user acknowledgment | Visible as new option |
| `confirmed` | User selected this branch via `user_approval_path` | Visible; immutable body |
| `paused` | User said "set this aside for now" | Visible on request; may be resumed |
| `archived` | User explicitly retired this path | Visible in history; not presented by default |
| `superseded` | Replaced by a new spec via recompilation | Visible via `parent_spec_id`; not presented by default |
| `merged_into` | Absorbed into another branch (conditions fully compatible) | Audit record preserved |

### Rules for each transition

**archive:** Only when the user explicitly says so ("I don't want to consider that path anymore"). The compiler never archives a branch on its own authority.

**merge:** Only when conditions are genuinely fully compatible and the user has confirmed. The compiler may propose a merge; it does not execute one silently.

**supersede:** On recompilation after material evidence change. The prior spec receives `status: superseded` and the new spec records `parent_spec_id`.

**pause:** When the user wants to defer a direction without retiring it ("Let's focus on career first, come back to the family question later"). Paused branches are fully resumable.

**resume:** From `paused` only. User or Navigator re-activates. Branch re-enters the working hypothesis without loss of prior state.

---

## §8 Contradiction handling

The compiler **preserves contradictions rather than resolving them prematurely.**

Contradictions are a signal about the user's real situation, not a bug to be fixed.

```
"I want stability."        evidence_id: e-014
"I also want adventure."   evidence_id: e-019
```

These do not cancel each other. They are both true for this user at this time. They compile into **separate branches** rather than into a single averaged condition.

### Contradiction types

| Type | Compiler response |
|------|------------------|
| **Temporal resolution** — user held belief A, then clearly stated belief B replacing it | Weight B higher; preserve A in audit. Do not erase A. |
| **Additive tension** — user genuinely wants both; they exist in geographic tension | Produce separate branches. Disclose the tension in `tradeoff_scan.cross_branch_tensions`. |
| **Apparent contradiction** — surface inconsistency that resolves at the archetypal level | Resolve in Pass 2. Document the resolution in audit. No branch split required. |
| **Unresolvable without user input** | Do not compile to a condition. Record as open Question. |

### What the compiler may not do with contradictions

- Silently choose one side
- Average the two into a compromise condition the user did not express
- Suppress either item from the evidence log
- Present one side as the user's "real" intention

---

## §9 Confidence

**Confidence belongs to the compiler's interpretation — not to the user's goals.**

The user's goals are not uncertain. They are what they are, even when incompletely expressed. Confidence is the compiler's assessment of how well it has understood those goals.

| Confidence applies to | Confidence does not apply to |
|----------------------|------------------------------|
| The compiler's inference from evidence | The user's stated intentions |
| A hypothesis before confirmation | A confirmed condition |
| A gap-filled assumption | An explicit user statement |
| An inferred strength level | A strength level the user stated explicitly |

### Confidence in the compiled spec

Each compiled `desired_conditions` entry carries an internal annotation (not user-facing) representing compilation confidence:

| Confidence level | Meaning |
|-----------------|---------|
| `direct_evidence` | Condition maps directly to at least one explicit user statement |
| `inferred` | Condition inferred from behavioral signals or pattern; labeled as Hypothesis until confirmed |
| `assumed` | Gap-filling; must appear in audit_transparency as `[assumption]` |

Only `direct_evidence` and confirmed `inferred` conditions may carry `required` or `strong` weight in the final SearchSpec. `assumed` conditions carry at most `weak` weight.

**What the compiler may not do:**

- Claim `direct_evidence` for a condition inferred from silence, absence, or indirect signal
- Promote an `assumed` condition to `strong` or `required` weight without Navigator confirmation
- Express its own confidence level to the user as if it were the user's certainty about their goal

---

## §10 Recompilation

The compiler recompiles whenever any of the following events occurs:

| Trigger | Action |
|---------|--------|
| New evidence event arrives in the Canon | Recompile from Pass 1 |
| User updates birth-time certainty or range | Recompile from Pass 3 |
| User adds, changes, or removes a hard constraint | Recompile from Pass 1 |
| User confirms or rejects a compiler hypothesis | Recompile from Pass 3 |
| User explicitly changes a tradeoff weighting | Recompile from Pass 4 |
| User resumes a paused branch | Recompile from Pass 6 to integrate resumed branch |
| Professional overrides a condition directly (Astro Assist) | Recompile from Pass 4 |

### Recompilation rules

1. **Confirmed SearchSpecs are never mutated.** Recompilation produces a new spec. The prior spec transitions to `superseded` with the new spec's `spec_id` recorded as successor.

2. **Prior branches are preserved in history.** The user may ask "what did we try before?" and receive a complete history.

3. **Evidence is re-weighted, not re-classified.** Recompilation re-applies recency weighting to the full evidence log. It does not change a prior evidence event's type.

4. **The Navigator presents the delta.** After recompilation, the Navigator should explain what changed between the prior and new spec. It does not silently replace the prior one without acknowledgment.

5. **Unconfirmed specs may be recompiled in place.** Only confirmed specs are immutable. Draft and proposed specs may be overwritten by a recompilation result.

---

## §11 Transparency

The user may inspect the compiler's current state at any time. This is a constitutional requirement (FOUNDATIONAL_CONSTITUTION.md §5.1).

| Inspectable view | What it shows |
|-----------------|---------------|
| **Current Understanding** | The compiler's current reading of the user's intentions, in plain language |
| **Current Hypothesis** | The working hypothesis before it has been compiled into a spec — including open questions |
| **Current SearchSpec** | The proposed or confirmed spec in user-readable form (not raw JSON) |
| **Current Branches** | All active and proposed branches with their labels and tradeoff summaries |
| **Previous Branches** | Paused, archived, and superseded branches available on request |

**What the user does not see:**

| Internal field | Why hidden |
|----------------|-----------|
| Raw numeric weights | Internal compiler state; never user-facing |
| Confidence annotations (`direct_evidence`, `inferred`, `assumed`) | Internal audit; presented in Navigator language instead |
| Pass-by-pass compiler trace | Implementation detail; audit log available to developers |
| Layer 2 entry IDs | Internal references; user sees plain-language condition descriptions |

**The user's right to correct:** Any item in the Current Understanding or Current Hypothesis may be challenged and corrected by the user. User corrections supersede compiler interpretations and trigger recompilation.

---

## §12 Guardian hooks

Every compiled SearchSpec must satisfy the following Guardian preconditions before it may be shown to a user or executed by the Engine.

| Precondition | Enforcement |
|--------------|-------------|
| No invented intentions | All conditions in `desired_conditions` must trace to at least one evidence event in `audit_transparency` |
| No hidden substitutions | All substitutions documented in `audit_transparency.what_substituted` |
| No silent optimization | No condition may be added by carving or optimization without appearing in `optimization_carving` |
| No forgotten evidence | All evidence events used in compilation traceable through audit; all skipped evidence with skip reason documented |
| No erased branches | Transition log for all non-active branches; archived/paused/superseded branches visible on request |
| No mutated confirmed specs | `confirmed` status specs immutable; recompilation produces new `spec_id` |
| No city lists as default | `city_helper_mode` absent or `enabled: false` by default; Engine must not receive city-list trigger without explicit invocation |

The Guardian does not audit the compiler's internal passes — only the compiled output. These preconditions ensure the output is auditable when the Guardian inspects it.

---

## §13 Relationship to Layer 2

The compiler **selects** which Layer 2 ontology entries participate in a SearchSpec. It does not author, modify, or extend them.

| Compiler's relationship to Layer 2 | Prohibited |
|-------------------------------------|-----------|
| Reads Approved entries via Model Resolver | Modifying existing entries |
| Selects entries relevant to the current evidence | Adding new entries |
| References entry IDs in `layer2_entry_ref` | Merging entries |
| Respects entry orb defaults and dignity preferences | Overriding entry-level orb values without disclosure |
| Uses Draft entries to inform hypotheses (labeled) | Using Draft entries in confirmed SearchSpecs |

When no Approved Layer 2 entry exists for a compiler-inferred condition, the compiler records the condition as an Assumption and does not compile it as `required`. The absence of ontology coverage is a gap, not an invitation to invent.

---

## §14 Overlay-first doctrine (compiler-level enforcement)

The compiler enforces the overlay-first doctrine at the output boundary.

**What the compiler always produces:**
- SearchSpecs whose primary output path is `handoffs.map_overlay_launch`
- Overlay branches named for human life strategies, not for geographic locations
- Viable geographic regions, not city lists

**What the compiler never sets by default:**
- `city_helper_mode.enabled: true`
- Any field that would cause the Engine to return a named city as a first-class result

**City identification is downstream of user action.** It is not a compiler decision.

After a user pins a place on the map, the Navigator may surface City Intelligence for that selected place. This is a user-triggered downstream path, not a compiler-initiated one.

---

## §15 Relationship to other canons

| Document | Relationship to Intent Compilation Engine |
|----------|------------------------------------------|
| INTENT_TRANSLATION_ENGINE.md | Describes the conceptual translation pipeline (three stages, viability probing). The ICE is the concrete compiler that executes it. They are complementary. |
| AI_CONSULTATION_ARCHITECTURE.md | Defines Consultation Canon fields (§3) that the ICE reads as evidence input; defines Engine and Guardian roles |
| CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md | Birth-time resolution output feeds §3.8 of SearchSpec; tradeoff language feeds ICE Pass 4 |
| SEARCHSPEC_SCHEMA.md | The authoritative schema for all ICE output |
| AI_RUNTIME_ARCHITECTURE.md | Runtime context; ICE is the "produces SearchSpec" step between Navigator and Engine |
| AI_INTERACTION_SURFACES.md | Surface context object feeds ICE `source_context` (§3.3 of SearchSpec) |
| FOUNDATIONAL_CONSTITUTION.md | All six compiler invariants (§4) trace to constitutional obligations |

---

## §16 Open questions (deferred to implementation)

| Question | Status |
|----------|--------|
| Compiler trigger model: event-driven vs. on-demand recompilation | Open |
| Maximum evidence events before forced checkpoint | Open |
| Contradiction detection algorithm | Open |
| Pass 3 Layer 2 mapping: fuzzy matching vs. strict entry lookup | Open |
| Branch count limit per compilation run | Proposed: 4 active branches maximum |
| Assumption confidence threshold: when to surface to Navigator vs. silently carry | Open |
| Audit log retention policy | Open |

---

*Planning complete. Documentation only. No code changes. No database migrations. No production AI active.*
