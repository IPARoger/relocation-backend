# AI-1C — Overlap Search Strategy Closeout

**Date:** 2026-06-27  
**Task:** AI-1C — Overlap Search Strategy / Viability Probing  
**Mode:** Documentation only — no code, no migrations, no UI changes  
**Status:** Complete

---

## Files created / updated

| File | Action |
|------|--------|
| `docs/canon/INTENT_TRANSLATION_ENGINE.md` | **Updated** — §12 Overlap Search Strategy and viability probing; §13 Search specification serialization (future dependency); §11 deferred items renumbered to §14 |
| `docs/canon/AI_CONSULTATION_ARCHITECTURE.md` | **Updated** — §25 note expanded to mention viability probing |
| `results/AI_1C_OVERLAP_SEARCH_STRATEGY_CLOSEOUT.md` | **Created** — this file |

---

## Core decisions captured

| Decision | Location |
|----------|----------|
| Overlap Search Strategy is search preparation, not recommendation | §12 definition |
| AI may pre-search variants but must disclose all results | §12 core principle |
| Required transparency: what was tried, worked, substituted, tradeoff introduced, why | §12 required transparency |
| User may open the underlying spec in Genie at any point | §12 required transparency |
| Viable alternative paths must not be collapsed — preserve as strategy options | §12 exploration preservation rule |
| Partial match is not failure; must be characterized honestly | §12 partial-match honesty |
| Forbidden phrasing: "basically the same," "just as good," "the best result" | §12 partial-match honesty |
| Viability probing precedes optimization; they are sequential, not simultaneous | §12 relationship to optimization |
| Cookbook recipe tree and AI variant testing use the same recipe tree | §12 relationship to Cookbook |
| Search spec serialization format flagged as AI-3 dependency | §13 |
| Seven required fields for search spec format | §13 |

---

## Open questions

1. **Variant limit:** How many variants should the AI test before reporting? Is there a budget (3 variants? 5?)? Unconstrained probing has cost implications.

2. **Transparency surface:** Where exactly does the transparency summary appear in the UI? A collapsible panel? An inspector drawer? The Genie panel? Needs product design decision.

3. **Cookbook recipe tree authorship:** Who authors the branch structure — product, professionals, or both? Can the AI propose new branches based on observed user patterns?

4. **Viability threshold:** What constitutes a "viable" result? Minimum number of matching metro areas globally? Minimum A2A orb tightness? This needs a product decision before implementation.

5. **Partial match scoring:** Is there a formalized scoring of "how partial" a match is, or is this always a qualitative narrative judgment by the AI?

---

## Recommended next slice

**AI-3 — Search Specification Schema**

The serialization format for search specifications (§13) is now the critical shared interface between the Translation Engine and the Search Engine. It is a dependency for both the full pipeline and the Overlap Search Strategy. AI-3 should define the canonical JSON schema.

After AI-3: **AI-2 — Consultation Canon Data Model** (enables evidence persistence and Working Hypothesis storage).

---

*AI-1C complete. Documentation only. No code changes. No database migrations.*
