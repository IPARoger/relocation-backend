# AI-RT-3 — Intent Compilation Engine Closeout

**Date:** 2026-06-27
**Task:** AI-RT-3 — Intent Compilation Engine

---

## Deliverables

| Artifact | Path | Status |
|----------|------|--------|
| Intent Compilation Engine canon | `docs/canon/INTENT_COMPILATION_ENGINE.md` | Created |
| Closeout report | `results/AI_RT_3_INTENT_COMPILATION_ENGINE_CLOSEOUT.md` | This file |

---

## What was defined

`INTENT_COMPILATION_ENGINE.md` establishes the deterministic compiler layer between Navigator conversation and immutable SearchSpec output.

### Sections

| § | Content |
|---|---------|
| §0 | Design axiom: the ICE is a compiler, not a conversationalist |
| §1 | Position in architecture (flow diagram: User → Navigator → ICE → SearchSpec → Engine → Overlays → Map) |
| §2 | Evidence accumulation: 7 evidence types with distinct lifecycle rules |
| §3 | Intention strength: Hard / Strong / Exploratory / Emerging / Unknown — inferred from conversation, not questionnaires |
| §4 | 7 compiler invariants (no invented intentions, no hidden substitutions, no silent optimization, no forgotten evidence, no erased branches, no mutating confirmed specs, no city lists by default) |
| §5 | 6 compilation passes: evidence classification → ambiguity resolution → symbolic grammar mapping → SearchSpec candidate generation → condition merging → branch separation |
| §6 | Branch formation: rules for when competing life strategies must stay separate |
| §7 | Branch retirement: 7 lifecycle states (active, proposed, confirmed, paused, archived, superseded, merged_into) with explicit transition rules |
| §8 | Contradiction handling: 4 contradiction types; compiler preserves both sides until user resolves |
| §9 | Confidence: belongs to compiler interpretation, not user goals; 3 confidence levels for compiled conditions |
| §10 | Recompilation: 7 trigger types; prior confirmed specs always immutable |
| §11 | Transparency: 5 user-inspectable views; internal fields hidden |
| §12 | Guardian hooks: 7 preconditions every compiled spec must satisfy |
| §13 | Layer 2 relationship: select-only, no authoring |
| §14 | Overlay-first doctrine enforced at compiler output boundary |
| §15 | Cross-references to all related canons |
| §16 | Open questions deferred to implementation |

---

## Acceptance

| Criterion | Met |
|-----------|-----|
| Compiler distinct from Navigator and Engine | Yes — §0, §1 |
| Evidence types have distinct lifecycle rules | Yes — §2 |
| Intention strength inferred from conversation | Yes — §3 |
| Translation runs as sequential passes | Yes — §5 |
| Competing life strategies preserved as branches | Yes — §6 |
| Branch retirement never silently discards | Yes — §7 |
| Contradictions preserved until user resolves | Yes — §8 |
| Confidence belongs to compiler, not user | Yes — §9 |
| Recompilation never mutates confirmed specs | Yes — §10 |
| User can inspect current state | Yes — §11 |
| Guardian hooks cover all compiler invariants | Yes — §12 |
| Layer 2 is read-only | Yes — §13 |
| Overlay-first enforced at output boundary | Yes — §14 |

---

## Optional follow-up

- Correct `INTENT_TRANSLATION_ENGINE.md` §0 table: "candidate cities" → "overlay branches" (separate pass)
- Update `AI_RUNTIME_ARCHITECTURE.md` to reference ICE as the named component between Navigator and SearchSpec
