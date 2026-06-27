# AI-1B — Intent Translation Engine Closeout

**Date:** 2026-06-27  
**Task:** AI-1B — Intent Translation Engine Architecture  
**Mode:** Documentation only — no code, no migrations, no UI changes  
**Status:** Complete

---

## Files created / updated

| File | Action |
|------|--------|
| `docs/canon/INTENT_TRANSLATION_ENGINE.md` | **Created** — ~1,900 word full specification |
| `docs/canon/AI_CONSULTATION_ARCHITECTURE.md` | **Updated** — §25 added introducing Intent Translation Engine as distinct subsystem |
| `docs/BETA_MASTER_CHECKLIST.md` | **Updated** — canon table row added; §11 AI note updated |
| `results/AI_1B_INTENT_TRANSLATION_ENGINE_CLOSEOUT.md` | **Created** — this file |

---

## Core decisions captured

| Decision | Location |
|----------|----------|
| Three-subsystem split: Consultation Engine / Translation Engine / Search Engine | §0 |
| Translation is continuous, not one-shot | §1 |
| Three-stage pipeline: natural language → archetypes → search spec | §2 |
| Target is archetype combinations, not isolated placements | §2 Stage 2 |
| Competing hypotheses maintained simultaneously; questions chosen to distinguish, not confirm | §4 |
| Question library organized by domain; smallest number of questions to resolve competition | §5 |
| Compositional search specifications (combinations, not isolated placements) | §6 |
| Optimization is conditional on user priorities; never silent | §7 |
| Cookbook relationship: same underlying recipes, different path to selection | §8 |
| Translation Engine uses Layer 2 ontology but never rewrites it | §9 |
| Five explicit constraints: no fabrication, no silent completion, no hidden ranking, no goal substitution, transparency on request | §10 |

---

## Open questions

1. **Hypothesis confidence model:** What algorithm governs confidence accumulation? Simple count of evidence events? Weighted by event type? Bayesian update? This needs design before implementation.

2. **Question library authorship:** Is the question library authored by product, by professionals (Layer 2), or both? Can professionals add domain-specific questions?

3. **Specification serialization:** What is the canonical JSON/structured format for a search specification handed from the Translation Engine to the Search Engine? This is the critical interface contract between the two subsystems.

4. **Cookbook schema:** The Cookbook cross-reference logic depends on a formalized Cookbook schema. The Cookbook must be fully specified before the Translation Engine can reference it reliably.

5. **Refinement loop feedback path:** How does a search result (a city, an overlay, a point truth) feed back into the Translation Engine as a refinement signal? What is the data contract for that feedback?

---

## Next recommended slice

**AI-2 — Consultation Canon Data Model**

Remains the highest-priority next step. The Translation Engine's progressive refinement, competing hypotheses, and evidence recording all depend on the Consultation Canon DB schema being defined. Without AI-2, the Translation Engine has nowhere to write.

After AI-2: **AI-3 — Search Specification Schema** — the interface contract between Translation Engine output and Search Engine input.

---

*AI-1B complete. Documentation only. No code changes. No database migrations.*
