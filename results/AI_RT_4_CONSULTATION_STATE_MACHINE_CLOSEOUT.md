# AI-RT-4 — Consultation State Machine Closeout

**Date:** 2026-06-27
**Task:** AI-RT-4 — Consultation State Machine

---

## Deliverables

| Artifact | Path | Status |
|----------|------|--------|
| Consultation State Machine | `docs/canon/CONSULTATION_STATE_MACHINE.md` | Created |
| Closeout report | `results/AI_RT_4_CONSULTATION_STATE_MACHINE_CLOSEOUT.md` | This file |

---

## What was defined

19 lifecycle states covering the full arc of an AI-assisted relocation consultation, from Idle through Archived/Closed.

### States

| # | State | Owner | Key purpose |
|---|-------|-------|-------------|
| 1 | Idle | Web2 instrument | No AI active; instrument fully available |
| 2 | Intake | Navigator / Astro Assist | Collect birth data and first intention |
| 3 | Birth-Time Resolution | Navigator + Flow Engine | Assess certainty; never fabricate birth time |
| 4 | Discovery | Navigator + Memory Agent | Accumulate evidence; no compilation yet |
| 5 | Working Hypothesis | Navigator + Intent Compiler | Pre-compilation staging; user reviews draft |
| 6 | Intent Compilation | Intent Compiler | 6 deterministic passes; produces proposed SearchSpec(s) |
| 7 | SearchSpec Proposed | Navigator | Consent gate; user reviews branches before Engine runs |
| 8 | Overlay Search | Engine | Executes confirmed SearchSpec; returns overlay branches |
| 9 | Overlay Review | Navigator + Map | Review overlay results; decide next step |
| 10 | Tradeoff Discussion | Navigator + Tradeoff Engine | Reason through gains/gives-up per branch |
| 11 | Optimization / Carving | Navigator + Intent Compiler | Refine conditions; explicit; produces new SearchSpec |
| 12 | Branch Confirmation | Navigator | Explicit strategic commitment; others paused not discarded |
| 13 | Map Exploration | Map instrument + Navigator | Primary Web2 product state; user drives exploration |
| 14 | Place Selection | Map + Navigator | First place enters scope; user-initiated only |
| 15 | Comparison | Comparison instrument + Navigator | Per-place astrological comparison; no ranking |
| 16 | City Intelligence | Navigator + CI layer | Practical factors; downstream of place selection |
| 17 | Reflection / Checkpoint | Memory Agent + Navigator | Save state; confirm summary; enable resume |
| 18 | Resume | Memory Agent + Navigator | Return after pause; no forced re-intake |
| 19 | Archived / Closed | Memory Agent | Terminal; all state preserved; resumable |

### Each state includes

- Purpose, owner, required inputs, produced outputs
- Allowed transitions and forbidden transitions
- Persistence behavior (Canon writes)
- Guardian involvement with key audit checks
- User-visible behavior
- Failure / fallback behavior

### Additional sections

- §3: Recompilation trigger table (6 triggers; routing rules)
- §4: Astro Assist abbreviated flow (states skipped, states never skipped)
- §5: Cross-cutting rules table (all states)
- §6: Canon cross-references

---

## Acceptance

| Criterion | Met |
|-----------|-----|
| 19 required states defined | Yes |
| Each state has all required subsections | Yes |
| "Intent Compiler" is preferred name with note re ICE | Yes — State 6 |
| AI is not the product; Web2 sovereign | Yes — §0, §5 |
| Map is primary exploration surface | Yes — State 13, §5 |
| Search produces overlays not city lists | Yes — State 8, §5 |
| Cities enter only after user selection | Yes — State 14, §5 |
| Confirmed SearchSpecs are immutable | Yes — §5 |
| New evidence triggers recompilation not mutation | Yes — §3 |
| Branches never silently discarded | Yes — States 7, 12 |
| Contradictory intentions preserved | Yes — State 5, §3 |
| Guardian reviews all user-facing AI output | Yes — every state Guardian section |
| Navigator / Astro Assist / Wizard framed as surfaces not AIs | Yes — §0, §4 |
| Astro Assist flow defined | Yes — §4 |
