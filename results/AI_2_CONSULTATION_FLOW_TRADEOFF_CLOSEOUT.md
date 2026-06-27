# AI-2 — Consultation Flow and Tradeoff Engine Closeout

**Date:** 2026-06-27  
**Task:** AI-2 — Consultation Flow, Birth-Time Resolution & Tradeoff Reasoning  
**Mode:** Documentation only — no code, no migrations, no UI changes  
**Status:** Complete

---

## Files created / updated

| File | Action |
|------|--------|
| `docs/canon/CONSULTATION_FLOW_AND_TRADEOFF_ENGINE.md` | **Created** — 10-section specification (~1,850 words) |
| `docs/canon/AI_CONSULTATION_ARCHITECTURE.md` | **Updated** — §27 added introducing Birth-Time Resolution Engine and Tradeoff Engine |
| `docs/canon/INTENT_TRANSLATION_ENGINE.md` | **Updated** — §7 optimization cross-references Tradeoff Engine |
| `docs/canon/AI_COMMUNICATION_DOCTRINE.md` | **Updated** — §9 constitutional truth boundary cross-references dignity language spec |
| `docs/BETA_MASTER_CHECKLIST.md` | **Updated** — canon table row added |
| `results/AI_2_CONSULTATION_FLOW_TRADEOFF_CLOSEOUT.md` | **Created** — this file |

---

## Core decisions captured

| Decision | Location |
|----------|----------|
| Birth-Time Resolution Engine is a separate subsystem | §0 |
| Five-stage resolution pipeline: unknown → estimate → range → chart uncertainty → recommendation | §1 |
| Four outcome states: Proceed / Proceed with caution / Recommend narrowing / Pause | §1 |
| Planetary line overlays stable without exact time; houses/angles require it | §1 table |
| Coaching tone: birth-time uncertainty is common; never discourage exploration | §1 coaching tone |
| Intake observations: 9 required; gathered conversationally, not as rigid script | §2 |
| Optimization and tradeoff reasoning are distinct operations | §3 |
| Tradeoff Engine reasons at narrative level, not placement level | §3 |
| Neutrality principle: no "good/bad/lucky/unlucky" — use supportive/demanding/activating | §4 |
| Universal relocation principle: every move produces easier, more demanding, and unchanged | §5 |
| Neutral conditions: never "irrelevant" — "outside current priorities" | §6 |
| Dignity language: accurately reflect symbolic distinctions without flattening or exaggerating | §7 |
| Dignity: distinguish symbolic strength / suitability for intentions / overall chart balance | §7 |
| AI never implies dignity alone determines whether a location is good or bad | §7 |
| Constitutional addition: AI optimizes understanding, not outcomes | §8 |

---

## Open questions

1. **Intake confidence threshold:** At what point does the AI have "sufficient confidence" in each observation to begin meaningful translation? Is there a minimum required set (e.g., birth confidence + primary intention + constraint geography) before search begins?

2. **Birth-time coaching depth:** How proactive should the AI be about recommending rectification? Should it offer resources (rectification astrologers, common birth record sources by country)? Or is this out of scope for the consultation layer?

3. **Tradeoff Engine narrative framing library:** The Tradeoff Engine needs a library of narrative-level contrasts ("visibility vs. structure," "expression vs. discipline," etc.) mapped to underlying archetype clusters. Who authors this? Is it part of Layer 2 ontology or hardcoded?

4. **Neutral condition tracking:** How are "neutral today" conditions surfaced if they become relevant later? Does the Consultation Canon store them, or are they recalculated on demand?

5. **Dignity language enforcement:** The Guardian needs a specific checklist to catch forbidden dignity language ("good," "bad," "lucky," "unlucky"). Is this a static word list, or a semantic judgment?

---

## Proposed constitutional additions (two)

From §8:
> **The AI should optimize understanding rather than outcomes. Its purpose is to help users choose consciously, not to choose for them.**

From AI-1D §12 (carried forward):
> **The AI should never use astrology to demonstrate its own expertise. It should use astrology to illuminate the user's experience and support better decisions.**

Both are recommended for promotion into `docs/constitutional/FOUNDATIONAL_CONSTITUTION.md`.

---

## Next recommended slice

**AI-3 — Search Specification Schema**  
The interface contract between Translation Engine output and Search Engine input. Blocked on this before pipeline implementation can begin.

**AI-5 — Navigator AI Voice Spec**  
The Communication Doctrine and Tradeoff Engine both depend on a concrete Navigator AI voice specification (tone, persona, pacing, escalation rules, hand-off protocol to Engine).

---

*AI-2 complete. Documentation only. No code changes. No database migrations.*
