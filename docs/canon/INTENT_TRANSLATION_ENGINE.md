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

## 11. Explicitly deferred to future implementation

| Item | Note |
|------|------|
| Archetype cluster definitions | Require Layer 2 ontology finalization first |
| Question library population | Requires product testing and iteration |
| Competing hypothesis confidence model | Requires evidence weighting scheme design |
| Cookbook cross-reference logic | Requires Cookbook schema to be formalized |
| Optimization boundary logic | Requires geographic precision spec (how many km is "flexible"?) |

---

*AI-1B complete. Documentation only. No code changes. No database migrations.*
