# AI Consultation Architecture Canon

**Status:** Canonical architecture doctrine — not active Beta implementation  
**Date:** 2026-06-27  
**Mode:** Documentation only — no code, no migrations, no UI changes  
**Authority:** Subordinate to [FOUNDATIONAL_CONSTITUTION.md](../constitutional/FOUNDATIONAL_CONSTITUTION.md)  
**Companions:** [AI_SYSTEMS_AND_PROMPT_PROTOCOLS.md](../ai/AI_SYSTEMS_AND_PROMPT_PROTOCOLS.md) · [AI_WORK_PROTOCOL.md](../governance/AI_WORK_PROTOCOL.md) · [FUTURE_FEATURES_ROADMAP.md](../product/FUTURE_FEATURES_ROADMAP.md)

> **Promotion rule:** This document describes future AI capability. Nothing here becomes active until explicitly promoted into an implementation plan with scope, migration plan, validation gate, and rollback path. The Web2 instrument remains sovereign.

---

## 0. Constitutional anchor

**Reveal structure. Preserve judgment.**

The AI is a guide, translator, consultation-memory manager, and decision-support assistant.

It is **not** an oracle.  
It is **not** a city-ranking engine.  
It is **not** a replacement for the factual map and chart system.  
It **may not** decide where the user should live.  
It **may not** create hidden rankings.  
It **may not** fabricate certainty.  
It **may not** treat astrology as deterministic life advice.

The non-AI professional Web2 core must remain fully usable without any AI component. AI navigation dependency recreates the oracle pattern; the instrument must remain sovereign.

---

## 1. Layer model

Five distinct layers govern the system. AI operates in Layers 2–4 only. It never touches Layer 1.

### Layer 1 — Truth

Astronomy, relocated charts, overlays, point truth, houses, angles, aspects, dignities, coordinates, birth-time uncertainty math.

**AI never edits this layer.** It reads Layer 1 to inform downstream reasoning, but it has no write path.

### Layer 2 — Ontology

Definitions, archetypes, cookbook entries, house/planet/aspect meanings, dignity preferences, orb defaults, minor-aspect settings, professional models.

Layer 2 may be:
- **Default** — application-supplied
- **AI-assisted** — suggested from reading uploads or user interaction
- **Astrologer-authored** — professional custom model (see Ontology Wizard, §9)

### Layer 3 — Intention and consultation state

What the user is currently trying to solve: constraints, certainty, emotional signals, cities under consideration, flexibility, rejected paths, and evolving priorities.

This layer is **user-driven**, not astrologer-driven. The AI reads and helps maintain it but does not override it. The Consultation Canon (§5) is the structured representation of Layer 3.

### Layer 4 — Search, refinement, optimization, and tradeoffs

Translation of intention into astrological search logic; overlays; substitutions; exclusions; constraint carving; A2A refinement; DIFFS; dignity comparison; relationship/family risk audit.

The AI's primary working layer. All outputs are labeled as interpretive assistance, not product truth.

### Layer 5 — City Intelligence

Non-astrological decision reality: cost, visa, schools, airports, hospitals, dialysis, culture, climate, safety, language, practical constraints.

City Intelligence is the **reality check and tiebreaker** after astrology narrows the field. The AI surfaces relevant CI data but does not let it silently override astrological structure.

---

## 2. AI roles

Five specialized roles. They are distinct agents that do not share scope.

### Navigator AI

**Voice to the user.** Handles intake, check-ins, education, and user-facing explanation. Conversational, non-technical. Asks soft feedback questions. Identifies intention shifts. Never speaks for the other agents directly — it mediates.

### Search Engineer AI

**Translates intention into structured search plans.** Generates substitutions, exclusions, constraint-carving specs, and A2A refinement parameters. Does not speak directly to the user; outputs are mediated through Navigator AI. Closer to a query compiler than a conversationalist.

### Ontology Assistant

**Helps professionals build Layer 2 models.** Can infer candidate ontology entries from uploaded anonymized readings. Separates inferred, approved, default, and conflicted entries. Never imposes; only suggests. See §9.

### Consultation Memory Agent

**Maintains the Consultation Canon.** Creates timestamped evidence events autonomously when users provide new data points. Flags contradictions without deleting prior evidence. Offers periodic confirmation to the user without interrupting every exchange.

### Reviewer / Ghost Boss AI

**Audits all AI output before user display.** Checks for:

| Audit category | Description |
|----------------|-------------|
| Oracle behavior | "Move here," "this is best," "this is your perfect city" |
| Hidden ranking | Implicit ordering not disclosed to user |
| Flattery | Telling the user what they want to hear |
| Fabricated certainty | Claiming more confidence than the data supports |
| Mystical language | Cosmic guarantees, destiny language, fear-based warnings |
| Unsupported claims | Factual assertions not traceable to Layer 1 |
| Fact/interpretation confusion | Presenting interpretation as chart fact |
| Ontology drift | Using ontology the user/professional has not authorized |
| Ignored constraints | Ignoring a hard constraint the user stated |

The Reviewer is not optional. It is infrastructure, not a feature.

---

## 3. Consultation Canon

The **Consultation Canon** is a persistent structured object belonging to a user/profile/investigation. It is the structured representation of Layer 3.

This is **not** vague chat memory. It is product infrastructure.

### Fields

```
Consultation Canon
├── current_intention            — what the user is trying to solve right now
├── intention_certainty          — inferred: hard / exploring / evolving
├── hard_constraints             — non-negotiable requirements
├── soft_constraints             — strong preferences, not dealbreakers
├── cities_under_consideration   — current working list
├── current_location_baseline    — where the user is now
├── birth_time_certainty         — certain / range / unknown
├── birth_time_range             — if range: earliest/latest
├── emotional_signals            — enthusiasm, hesitation, concern (timestamped)
├── rejected_paths               — explicitly ruled out (with reason and timestamp)
├── promising_paths              — surfaced but not yet decided
├── relationship_family_risks    — flagged asymmetries and pressure placements
├── known_practical_constraints  — visa, budget, health, schools, etc.
├── open_questions               — unresolved items the user is sitting with
├── latest_confirmed_summary     — last summary the user agreed was accurate
├── evidence_events              — append-only log (§4)
├── ai_notes_awaiting_confirm    — proposed updates not yet confirmed by user
└── user_corrections             — corrections applied by user
```

### Ownership and review

- The user may view and correct the Consultation Canon at any time.
- AI-generated entries are labeled as such until confirmed.
- User corrections supersede AI entries.

---

## 4. Memory rules and evidence events

The Consultation Memory Agent creates timestamped evidence events **autonomously** when the user provides a new data point. No user action required; no interruption for every event.

**Triggers for evidence event creation:**

- User expresses enthusiasm about a city or condition
- User explicitly rejects a path
- User shifts apparent priority (e.g., career → peace/home)
- User adds or tightens a hard constraint
- User changes their working city list
- User clarifies birth-time certainty or range
- User reacts negatively to a proposed tradeoff
- User confirms a result makes sense
- User says a result does not make sense
- User expresses hesitation about a promising path

**Evidence entries are append-only.** Recency matters, but contradictions are preserved rather than deleted. The system holds the full history; the current state is a reconciliation of all prior evidence, weighted toward the most recent.

**Periodic confirmation pattern:**

The AI may occasionally say:

> "I've updated your file with a few notes from our conversation. Does this still sound right?"

This is not required for every event. Use judgment based on significance and elapsed time.

---

## 5. Feedback capture

The Navigator AI should routinely ask soft feedback questions where natural:

- "Does this make sense?"
- "Do you have questions about this?"
- "Is this still the question you want to answer?"
- "Would you rather go deeper here or step back?"
- "Do these tradeoffs feel relevant?"
- "Is this actually what you want, or just what sounded plausible at the start?"

Every response is a timestamped evidence event. Feedback is captured without ceremony.

---

## 6. Intention certainty

Do not ask crude 1–10 certainty questions by default. **Infer from context.**

### Hard-bounded intention

> "I must choose London, Tokyo, or Singapore for work."

**AI behavior:**
- Do not broaden the search unless explicitly invited
- Compare the stated cities directly
- Ask whether to include secondary factors (relationship, health, peace)
- Allow future side explorations without disrupting the main task

### Exploratory intention

> "I'm restless and want to see what's out there."

**AI behavior:**
- Broaden safely
- Check in often
- Invite curiosity
- Help the user notice changing priorities without forcing a direction

### Evolving intention

User begins with career, then repeatedly responds more strongly to peace/home/recovery signals.

**AI behavior:**
- Identify the shift gently, without accusing the user of being inconsistent
- Update the Consultation Canon
- Offer to run searches for both career and peace in parallel
- Do not cling to the initial stated intention

---

## 7. Search and refinement loop

The loop is **flexible, not linear**. It may open, close, repeat, or reverse based on user response.

```
Intake
  → Current situation
    → Intention
      → Astrological translation
        → Initial search
          → Inspect overlays
            → Point truth
              → Overlaps
                → Compare cities
                  → DIFFS
                    → A2A refinement
                      → Dignity checks
                        → Constraint carving
                          → City Intelligence
                            → Decision support
                              → Check-in
                                → Revise intention / continue / narrow / exit
```

At any step, the user may jump backward, pause, ask a clarifying question, or change stated intention. The loop accommodates this without loss of context.

---

## 8. Constraint carving and optimization

Constraint carving is a **Layer 4 operation** — not generic ranking.

**Example:**

> Preserve: Sun in 1st  
> Avoid: Saturn in 12th, Saturn in 1st  
> Prefer: Saturn in 11th if available

The AI may say:

> "We found a Sun-in-1st region, but it also places Saturn in the 12th. If you have flexibility on location, we can try to carve that out while preserving the solar emphasis."

**All "better/worse" language must be conditional:**
- "Better under this intention"
- "Easier all things being equal"
- "More supportive of the stated goal"
- Never: "objectively best"

---

## 9. Substitutions

If a desired condition is unavailable or impractical, the Search Engineer AI may suggest symbolic substitutes.

**Example:** If Sun in 1st is mostly over ocean:
- Sun trine ASC
- Sun sextile ASC
- Sun in 5th
- Leo rising
- Strong solar dignity
- Jupiter support to ASC

**Substitutions must be described as related strategies, not equivalents.** The user decides whether a substitute is acceptable given their intention.

---

## 10. DIFFS

DIFFS answer: **"What actually changes between these places?"**

The AI uses DIFFS to help the user weigh:

| Factor | Example |
|--------|---------|
| Dignities | Ruler vs. detriment in key houses |
| A2A exactness | Tighter orb for a desired angle contact |
| House shifts | MC shifts from 10th to 9th across longitude |
| Angle changes | ASC sign changes, MC changes |
| Lost positives | What the user gives up by choosing B over A |
| Reduced negatives | Saturn pressure that relaxes in the alternate city |
| New risks | Pluto contact that appears in B |
| City Intelligence differences | Cost, visa, practical reality |

The AI must ask how the user personally weighs these factors. It does not assume the user values dignity over exactness, or solar conditions over peace.

---

## 11. Relationship and family mode

Future subsystem: **Relationship / Family Relocation Audit**.

### Inputs
- Person A (natal + relocated charts)
- Person B (natal + relocated charts)
- Composite chart
- Optional: children, family composite/group
- Cities under consideration
- Shared constraints

### Governing principles

- V1 scope: Person A, Person B, Composite only. No synastry unless explicitly promoted later.
- **Examine relationship risks before optimization.** Do not optimize for one person's rare alignment if it harms the other or the relationship.
- Surface asymmetry honestly without fear language.
- Look for substitutions that work well enough for both people.
- Do not let one person's extraordinary placement dominate a decision without the other's explicit awareness of the tradeoff.

### Placements to flag cautiously

These are **not** prohibitions. They require honest surfacing and discussion.

| Placement | Context |
|-----------|---------|
| Uranus in 4th | Disruption to home/roots |
| Pluto in 4th | Intensity/transformation in home life |
| Uranus in 7th | Disruption to partnership patterns |
| Pluto in 7th | Intensity/transformation in partnership |
| Saturn in 4th (both) | Heaviness in home/roots |

**No fear language. No deterministic breakup language.** These are structural observations. The user decides how to weigh them.

---

## 12. Rare alignment

When a location shows unusually coherent placements across multiple meaningful conditions:

**Label:** "Rare Alignment" or "Unusual Congruence"  
**Never:** "Magic City," "perfect city," "you should move here," "objectively best"

**Allowed behavior:**

If the user is in exploratory mode, the AI may surface an unrequested congruence:

> "This isn't what you originally asked for, but this location shows unusually coherent career placements across multiple conditions. Would you like to inspect it?"

The user decides whether to pursue it. The AI does not insert it into the main recommendation stream uninvited.

---

## 13. Birth-time uncertainty

If the user has a birth-time range rather than a precise time:

- Calculate earliest plausible chart and latest plausible chart
- Render same-condition overlays in the same hue with opacity variation
- Stable overlap = higher confidence
- Translucent fringe = uncertain region
- Flag unstable house and angle placements explicitly

**Verbal rule:**

> "Across your stated time range, these placements remain stable. These others depend on the exact time, so we'll treat them cautiously and note the uncertainty."

**Do not:**
- Default to noon, sunrise, or any fabricated time
- Overpromise houses or angles when the birth-time is unstable
- Silently compute a single chart from an uncertain range

---

## 14. Ontology Wizard

The **Ontology Wizard** is a Layer 2 authoring system for professional astrologers.

Professionals can create custom:
- Placement definitions and cookbook entries
- Aspect definitions
- Dignity rules
- Default orbs and minor-aspect defaults
- House emphasis and weighting
- Search cookbook entries
- Tradeoff preferences
- Explanatory language and terminology

They may leave entries blank to fall back to application defaults.

### Reading upload

Professionals may upload **anonymized** readings. The Ontology Assistant extracts:

| Extracted item | Status type |
|----------------|-------------|
| Candidate interpretive language | Inferred |
| Recurring themes | Inferred |
| Communication style | Style (separate from ontology) |
| Tradeoff preferences | Inferred |
| Substitution patterns | Inferred |

Inferred entries require approval before becoming active. Entries have four states: **inferred → approved → active / conflict needing review**.

If readings reveal a discrepancy between stated ontology and actual practice, the system handles it non-confrontationally:

> "Your uploaded readings often discuss Moon in the 2nd through emotional security and resource stability. Would you like to add that language to your Moon-in-2nd entry?"

Never embarrass or accuse. Surface the discrepancy as an opportunity.

### Style extraction (separate)

Reading uploads may also inform communication style:
- Paragraph length and density
- Warmth level
- Terminology complexity
- Caution level and hedging patterns
- Directness
- Teaching and summary habits

Style is modeled separately from ontology and applied only to AI-generated outputs, not to factual surfaces.

---

## 15. Experiential education / travel course

Deferred future module. Preserve as a complete future capability.

The AI may generate "learn astrology through travel" courses based on:
- The user's own relocated chart
- Current route or planned itinerary
- GPS / current location (if enabled)
- ASC changes across longitude
- House shifts
- A2A zones entered and exited

**Core rule:** Teach observation, not prediction.

**Example:**
> "As you move through this region, your relocated Ascendant shifts from Capricorn to Aquarius. Use this as a field lesson: notice how introductions and first impressions feel different. Don't force a conclusion; observe what you notice and record it."

**Potential audiences:**
- Van lifers and digital nomads
- Road trippers
- Astrology students
- Relocation explorers

---

## 16. Cost and model architecture principles

Do not select vendors here. These are **routing principles** only.

| Principle | Description |
|-----------|-------------|
| Tiered routing | Do not use one expensive frontier model for every task |
| Task complexity routing | Route by task class: intake/check-ins → cheaper; complex tradeoffs/reports → stronger |
| Ontology/session caching | Cache layer context to reduce token overhead |
| Structured tools | Use tool-calling and structured output rather than giant prose prompts |
| Reviewer economy | Reviewer runs on a smaller model where possible |
| Budget per tier | Define token/cost budgets per user tier before production |
| Provider portability | Design prompts and connectors so the model can be swapped without product-layer rewrites |

---

## 17. Possible future product packages

No final pricing. These are structural possibilities for future product thinking.

| Package | Description |
|---------|-------------|
| Single decision | One relocation decision, limited AI sessions |
| Ongoing travel exploration | Rolling exploration with persistent Consultation Canon |
| Digital nomad / van life | Route-based, GPS-enabled, experiential education included |
| Couple / family relocation | Multi-chart audit mode |
| Professional tier | Ontology Wizard, reading upload, client-facing exports |
| Report / export credits | AI-generated summary export, reviewed and labeled |
| AI top-ups | Additional AI consultation sessions |

---

## 18. What the Web2 instrument remains

The Web2 application — map, overlays, chart pages, comparison tables, A2A, settings, notes, City Intelligence, saved searches — remains **fully functional without AI**. AI layers are additive, not replacements.

This must remain true permanently. The instrument is the product. AI is assistance.

---

## 19. Explicitly deferred to future implementation

| Item | Deferral reason |
|------|----------------|
| Consultation Canon DB schema | Requires architecture decision before migration |
| Navigator AI prompt design | Requires product iteration and safety review |
| Reviewer AI prompt design | Requires structured tool-call spec |
| Ontology Wizard UI | Requires Settings extension planning |
| Reading upload pipeline | Requires security and anonymization spec |
| Birth-time uncertainty rendering | Requires renderer extension |
| Relationship/family mode | Requires multi-profile chart pipeline |
| Experiential travel module | Requires GPS integration and mobile spec |
| OTF glyph font pipeline | See GL-3/GL-4 |

**Promotion path:** Any item above requires a focused implementation document, scope decision, validation gate, and rollback plan before becoming active work.

---

*AI-1 complete. Documentation only. No code changes. No database migrations.*
