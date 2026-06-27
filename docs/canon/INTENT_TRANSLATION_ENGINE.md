# Intent Translation Engine Canon

**Status:** Canonical architecture doctrine — not active Beta implementation  
**Date:** 2026-06-27  
**Mode:** Documentation only — no code, no migrations, no UI changes  
**Authority:** Subordinate to [FOUNDATIONAL_CONSTITUTION.md](../constitutional/FOUNDATIONAL_CONSTITUTION.md)  
**Companions:** [AI_CONSULTATION_ARCHITECTURE.md](AI_CONSULTATION_ARCHITECTURE.md) · [AI_SYSTEMS_AND_PROMPT_PROTOCOLS.md](../ai/AI_SYSTEMS_AND_PROMPT_PROTOCOLS.md)

> **Promotion rule:** This document describes future AI capability. Nothing here becomes active until explicitly promoted into an implementation plan with scope, validation gate, and rollback path. The Web2 instrument remains sovereign.

---

## 0. Position in the architecture

Three subsystems collaborate in the AI-guided Relocation experience. They are independent.

| Subsystem | Responsibility |
|-----------|----------------|
| Consultation Engine | Guides the conversation; manages the Consultation Canon, evidence log, checkpoints, working hypotheses, and user relationship |
| **Intent Translation Engine** | Progressively reduces ambiguity; translates human intentions into structured astrological search specifications |
| Search Engine | Executes structured specifications against Layer 1 truth; returns candidate cities, overlays, and point conditions |

The Intent Translation Engine sits between the conversation and the search. It does not guide. It does not search. It translates.

---

## 1. Core principle

**The AI does not translate intentions once. Translation is continuous.**

Every new answer, reaction, preference, hesitation, discovery, and stated tradeoff may refine the current translation. The specification produced in session one is a starting draft — a progressively better approximation of what the user actually wants, not a final declaration.

The Translation Engine's success is measured by **increasing precision while preserving user agency.** The user should leave each session with a progressively clearer understanding of what they actually want — not merely a list of cities.

---

## 2. Three-stage translation

### Stage 1 — Natural language → human intentions

Raw user language is almost never directly searchable. Stage 1 identifies the underlying human intention.

| Raw statement | Underlying intention |
|---------------|---------------------|
| "I want a better career." | Advancement, recognition, or material improvement — unclear which |
| "I want to find love." | Partnership, companionship, intimacy — unclear which |
| "I want to build a family." | Stability, roots, home, continuity |
| "I need a reset." | Recovery, peace, reduced pressure |
| "I want to feel alive again." | Vitality, creativity, self-expression |

These are not yet searchable. They define the territory; they do not map it.

### Stage 2 — Human intentions → archetypal combinations

Stage 2 discovers which symbolic qualities the user is actually seeking. The target is **combinations of archetypes**, not single placements. Single-placement thinking misses the compositional nature of astrological conditions.

**Example: "I want a better career"**

| Path A | Path B |
|--------|--------|
| Creative Career | Structured Career |
| Recognition × Beauty × Influence | Mastery × Authority × Longevity |
| ↓ | ↓ |
| Sun × Venus × MC | Saturn × MC × Strong dignity |

Both are valid translations of "better career." They produce different search specifications. The Translation Engine's job is to discover which path the user is actually on — or whether they are seeking both in different proportions.

**Archetype clusters by domain (examples):**

| Domain | Cluster examples |
|--------|-----------------|
| Career | Recognition (Sun/MC), Structure (Saturn/MC), Innovation (Uranus/MC), Service (Virgo/6th), Authority (Cap/10th) |
| Partnership | Encounter (Venus/DSC/7th), Depth (Pluto/7th/8th), Freedom (Uranus/7th), Stability (Saturn/7th) |
| Home / family | Roots (Moon/4th/IC), Security (Taurus/4th), Expansion (Jupiter/4th), Transformation (Pluto/4th — flagged) |
| Vitality / health | Embodiment (Mars/1st/ASC), Restoration (Neptune/12th), Clarity (Mercury/6th) |
| Peace / recovery | Solitude (12th), Groundedness (Earth/4th), Release (Neptune/Pisces) |
| Creativity | Expression (Venus/5th/Leo), Performance (Sun/5th/Leo), Flow (Neptune/5th/Pisces) |

Archetype clusters are drawn from Layer 2 ontology. They are not hardcoded — they use whatever the active ontology provides.

### Stage 3 — Archetypal combinations → search specification

Stage 3 converts the current archetype hypothesis into a structured, executable search specification.

**Example output:**

```
Search specification
├── primary
│   └── Sun in 10th
├── secondary
│   ├── Venus sextile MC
│   └── Jupiter trine ASC
├── prefer
│   └── Solar dignity (Sun in Leo or Aries, or strong dignities)
├── avoid
│   ├── Saturn in 12th
│   └── Saturn in 1st
└── flexible
    └── MC sign (not constrained)
```

The Search Engine operates on this specification. It does not know about the conversation that produced it.

---

## 3. Progressive refinement

Translation never reaches a final state during an active consultation. Every step in the search/refinement loop may feed back and modify the current specification.

| Dimension | Example modification |
|-----------|---------------------|
| Archetype weights | User responds more strongly to Venus placements than Sun; Venus weight increases |
| Priorities | User sees a strong Saturn/MC city and responds positively; Structured Career hypothesis gains confidence |
| Exclusions | User reacts negatively to Saturn in 12th in a candidate city; that exclusion strengthens |
| Preferred substitutions | User prefers Sun trine ASC over Sun in 10th when exact 10th is unavailable |
| Tradeoff tolerance | User reveals they will accept Uranus in 4th if career conditions are strong enough |

Each refinement is recorded as an evidence event in the Consultation Canon.

---

## 4. Competing hypotheses

The Translation Engine maintains **multiple simultaneous hypotheses** about what the user actually wants. Certainty accumulates as evidence resolves the competition.

**Example: career consultation in progress**

| Hypothesis | Confidence |
|------------|------------|
| Creative Career (Sun/Venus/MC) | 58% |
| Structured Career (Saturn/MC/dignity) | 28% |
| Technical Innovation (Uranus/MC/Mercury) | 14% |

Confidence values do not surface to the user as raw numbers. They determine which questions are asked next and which search specification is currently active.

Questions are chosen specifically to **distinguish between competing hypotheses** — not to confirm the leading one.

When one hypothesis reaches sufficient confidence, the Translation Engine consolidates around it and updates the Working Hypothesis in the Consultation Canon. Alternatives are not discarded; they become secondary goals or rejected paths.

---

## 5. Translation question library

Questions reduce ambiguity without requiring astrological knowledge from the user.

The library is organized by domain. Questions are selected based on which competing hypothesis they most efficiently distinguish.

**Career**

| Question | Distinguishes |
|----------|--------------|
| "When you imagine your career improving, what feels most exciting — visibility, mastery, or breaking new ground?" | Creative vs. Structured vs. Innovation |
| "Do you want to be known for something, or do you want to quietly build something that lasts?" | Recognition vs. Mastery |
| "Does the idea of authority or influence feel energizing or burdensome?" | Saturn/MC vs. Sun/MC |

**Partnership**

| Question | Distinguishes |
|----------|--------------|
| "When you imagine a stronger relationship, what feels most important — meeting someone new, deepening an existing bond, or more freedom within connection?" | Encounter vs. Depth vs. Freedom |
| "Is the relationship question the primary reason you're considering relocation, or a secondary factor?" | Weight of relationship intention |

**Home / family**

| Question | Distinguishes |
|----------|--------------|
| "What kind of home are you hoping to create — settled and rooted, expansive, or open to change?" | Roots vs. Expansion vs. Flexibility |
| "How important is staying near your current community compared to starting fresh?" | Stability vs. Reset |

**General principles for question design:**

- Ask the smallest number of questions needed to distinguish competing hypotheses
- Prefer concrete imagery over abstract language
- Do not introduce astrological terminology unless the user has demonstrated familiarity
- Never ask a question whose answer is already clear from prior evidence
- If a hypothesis is already dominant, do not ask redundant confirmation questions

---

## 6. Compositional search specifications

Search specifications consist of **combinations of archetypes**, not isolated placements.

An isolated placement search (e.g., "Sun in 10th") produces a broad zone. A compositional search (e.g., "Sun in 10th AND Venus sextile MC AND avoid Saturn 12th") produces a refined zone that reflects the user's actual intention.

**Example:**

```
Sun in 10th
  × Venus sextile MC
  × Jupiter dignity
  × Avoid Saturn 12th
```

These are handed to Layer 4 (Search, Refinement, Optimization) for execution. The Translation Engine produces the specification; Layer 4 executes it.

---

## 7. Optimization

Layer 4 optimization attempts to **preserve desired combinations while carving away undesirable co-factors**. The Translation Engine provides the specification; optimization works within it.

**Example:**

> Keep: Sun in 10th  
> Improve: Shift Uranus from 4th to 3rd (if geographic flexibility allows)  
> Goal: Preserve creative recognition while reducing domestic instability

Optimization is always conditional on user-stated priorities. The AI may say:

> "We can preserve the Sun-in-10th zone, but Uranus is also active in the 4th in this region. If you have flexibility of even a few hundred kilometers, we may find a corridor where Uranus moves into the 3rd. Would that be worth exploring?"

The user decides. The AI does not optimize silently.

---

## 8. Cookbook relationship

The Web2 Cookbook and the Translation Engine use the **same underlying recipes**.

| Mode | User role |
|------|-----------|
| Web2 direct | User manually selects a Cookbook recipe |
| AI-assisted | Conversation progressively assembles or modifies a recipe |

The recipes are identical. The difference is the path to selecting them.

**The AI should be able to explain:**
- Which Cookbook recipe most closely resembles the current specification
- Where and why it diverged from the canonical recipe

This transparency reduces the oracle pattern and allows experienced users to take over and drive the Cookbook directly.

**Example:**

> "The search we've assembled is close to the 'Creative Recognition' Cookbook recipe — Sun/Venus/MC emphasis with solar dignity. The main difference is that you've added a preference for Jupiter in the 1st, which isn't in the default recipe."

---

## 9. Ontology relationship

Professional Layer 2 models (Ontology Wizard) provide:
- Placement and aspect definitions
- Search cookbook recipes
- Tradeoff preferences
- Preferred substitutions
- Archetype cluster definitions

The Translation Engine **uses** these models but does not rewrite ontology. Inferred ontology updates go through the Ontology Assistant review process (see AI_CONSULTATION_ARCHITECTURE.md §14).

If a professional has authored a custom Layer 2 model, the Translation Engine uses that model's definitions — not the defaults.

---

## 10. Explicit constraints

| Constraint | Rule |
|------------|------|
| No fabrication | The engine may not infer a placement preference the user has not expressed or implied |
| No silent completion | Missing specification components are asked for, not guessed |
| No hidden ranking | Competing hypotheses inform the specification; they do not produce a ranked city list |
| No goal substitution | If stated goal conflicts with inferred goal, the stated goal wins |
| Transparency on request | The user may ask "What are you currently searching for?" and receive a plain-language description of the current specification |

---

## 12. Overlap Search Strategy and viability probing

### Definition

**Overlap Search Strategy** is the process of testing multiple structured versions of a compositional intention to identify viable geographic overlap areas before presenting results to the user.

This is **search preparation**, not final recommendation.

The Translation Engine may produce a specification with several desired archetypes. Many ideal combinations do not exist cleanly in geography. Viability probing tests whether a given combination has geographic coverage — and what the realistic variants look like — before committing to a full search.

### Core principle

The AI may save the user time by avoiding obvious dead ends.

It may not rob the user of discovery.

It may pre-search variations, but it must disclose:

- Whether an exact match was found or not found
- Whether a partial match was found
- What substitutions were used
- Which desired archetypes were preserved
- Which desired archetypes were weakened
- What co-factors were introduced
- What options remain worth exploring manually

### Example

**User intention:** Career — expressive, stable, beautiful.

**Archetype family:** Sun × Saturn × Venus × MC / 10th

**Ideal specification:**
- Sun in 10th
- Venus in 10th or Venus trine/sextile MC
- Saturn in 10th or Saturn trine/sextile MC

If no clean three-factor overlap exists, the AI tests variants:

| Variant | Conditions | Character |
|---------|-----------|-----------|
| A | Sun in 10th · Venus sextile MC · Saturn trine MC | Sun and Saturn direct; Venus through aspect |
| B | Sun conjunct MC · Venus in 10th · Saturn dignity | Venus and solar emphasis direct; Saturn supportive |
| C | Sun in 10th · Saturn in 10th · Venus square MC | Sun and Saturn direct; Venus with tension/activation |
| D | Sun in 10th · Venus trine MC · Saturn in 11th | Avoids Saturn 12th/1st pressure; Saturn slightly off-axis |

**Report style:**

> "The clean three-factor version is rare. I found two workable strategies: one preserves Sun and Saturn most strongly while bringing Venus through an MC aspect; the other preserves Sun and Venus while Saturn becomes a supporting factor rather than the main career signature."

### Required transparency

Every viability probe must produce a visible summary before the user sees results:

| Required disclosure | Example |
|--------------------|---------|
| What was tried | "Tested three-factor Sun/Venus/Saturn MC combination" |
| What worked | "Sun in 10th has strong coverage in central Europe and East Asia" |
| What did not work | "Clean three-factor overlap is rare; fewer than 5 viable metro areas globally" |
| What was substituted | "Saturn moved to trine MC rather than conjunction; Venus via sextile rather than conjunction" |
| What tradeoff was introduced | "Venus-square variant carries more tension or activation than ease" |
| Why this path | "Variant A preserves the career recognition signature most directly" |

The user should be able to open the underlying Web2 search specification in Genie at any point.

### Exploration preservation rule

Do not collapse viable alternatives too early.

If multiple viable paths are meaningfully different, **preserve them as strategy options** and present them to the user for selection.

**Examples of distinct paths that must not be merged:**
- Recognition path (Sun/MC emphasis)
- Mastery path (Saturn/MC emphasis)
- Creative path (Venus/5th emphasis)
- Innovative path (Uranus/MC emphasis)
- Stable-home-preserving path (Moon/4th preserved alongside career factors)

The AI may recommend inspecting one path first. It must not hide the others.

### Partial-match honesty

A partial match is not failure. Partial matches are surfaced with honest characterization.

**Allowed phrasing:**

- "We got 2 of the 3 desired archetypes cleanly. The third appears through a narrower A2A band."
- "The Venus signature is available, but it comes through a square rather than a trine, so it may carry more tension or activation than ease."
- "The Saturn factor is easier to preserve if we let it move into the 11th rather than forcing it into the 10th."

**Forbidden phrasing:**

- "This is basically the same."
- "This is just as good."
- "This is the best result."

All comparison language must be conditional on the user's stated intention, as defined in §8 of AI_CONSULTATION_ARCHITECTURE.md.

### Relationship to optimization

Viability probing and optimization are sequential, not simultaneous.

| Stage | Question |
|-------|----------|
| Viability probing | "Can this combination exist in geography?" |
| Optimization | "Can we preserve what works while carving out undesirable co-factors?" |

Optimization begins only after a viable region or strategy is identified. Running optimization against a non-viable combination wastes effort and produces misleading results.

### Relationship to the Cookbook

The Web2 Cookbook should expose viability strategies manually, organized as recipe trees.

**Example structure for a Cookbook recipe:**

```
Career → Expressive + Stable + Beautiful
├── Ideal version          (Sun/Venus/Saturn all in 10th)
├── A2A workaround         (aspects to MC substituted for house placements)
├── Dignity-support version (strong solar/Venusian dignity compensates for weaker house placement)
├── Tension/activation version (square aspects included; activation character acknowledged)
└── Home-preserving version (Saturn shifted to avoid 4th disruption)
```

The AI uses the same recipe tree but tests branches faster than manual exploration. The result is the same discovery process, accelerated.

---

## 13. Search specification serialization (future dependency)

The Overlap Search Strategy and full Translation Engine pipeline depend on a formal serialization format for search specifications. This is flagged here as a future dependency; the schema is not designed in this document.

A complete search specification format must be capable of representing:

| Field | Purpose |
|-------|---------|
| `ideal_conditions` | Primary archetype targets |
| `acceptable_substitutions` | Named fallback conditions per archetype |
| `weighted_priorities` | Relative importance of each component |
| `hard_avoids` | Conditions that disqualify a region |
| `soft_avoids` | Conditions to minimize if possible |
| `variant_branches` | Named strategy variants (A, B, C…) |
| `partial_matches` | Regions satisfying a subset, with disclosure |
| `transparency_notes` | What was tried, what was substituted, what tradeoff was introduced |
| `user_approved_path` | Which strategy the user selected |

**Design owner:** AI-3 — Search Specification Schema (future slice).


---

## 14. Explicitly deferred to future implementation

| Item | Note |
|------|------|
| Archetype cluster definitions | Require Layer 2 ontology finalization first |
| Question library population | Requires product testing and iteration |
| Competing hypothesis confidence model | Requires evidence weighting scheme design |
| Cookbook cross-reference logic | Requires Cookbook schema to be formalized |
| Optimization boundary logic | Requires geographic precision spec (how many km is "flexible"?) |
| Overlap Search Strategy execution | Requires Search Engine API and specification serialization format (AI-3) |
| Cookbook recipe tree format | Requires Cookbook schema formalization |

---

*AI-1B / AI-1C complete. Documentation only. No code changes. No database migrations.*
