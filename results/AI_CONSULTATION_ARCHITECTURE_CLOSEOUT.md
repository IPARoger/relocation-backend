# AI-1 — AI Consultation Architecture Closeout

**Date:** 2026-06-27  
**Task:** AI-1 — AI Consultation Architecture Canon  
**Mode:** Documentation only — no code, no migrations, no UI changes  
**Status:** Complete

---

## Files read

| File | Purpose |
|------|---------|
| `docs/governance/AI_WORK_PROTOCOL.md` | Context discipline, workflow discipline, commit discipline |
| `docs/ai/AI_SYSTEMS_AND_PROMPT_PROTOCOLS.md` | Core AI product role, guardrails, prompt protocols, anti-oracle doctrine |
| `docs/constitutional/FOUNDATIONAL_CONSTITUTION.md` | "Reveal structure. Preserve judgment." — governing rule |
| `docs/product/FUTURE_FEATURES_ROADMAP.md` | Roadmap separation doctrine, AI-and-interpretive-future context |
| `docs/product/WEB2_ONBOARDING_AND_GUIDED_DISCOVERY_V2.md` | First-experience intake flow, profile data collection pattern |
| `docs/MICRO_INTERACTIONS_AND_EMOTIONAL_MOVEMENT_DOCTRINE.md` | Emotional movement, instrument vs. casino, user emotional arc |
| `docs/product_decisions/MICRO_DECISIONS_LOG.md` | Capture-first doctrine, append-only memory pattern |
| `docs/BETA_MASTER_CHECKLIST.md` | Project status, existing section structure |

---

## Files created / updated

| File | Action |
|------|--------|
| `docs/canon/AI_CONSULTATION_ARCHITECTURE.md` | **Created** — 3,000+ word canon document |
| `docs/BETA_MASTER_CHECKLIST.md` | **Updated** — added §11 AI Consultation Architecture + canon table row |
| `results/AI_CONSULTATION_ARCHITECTURE_CLOSEOUT.md` | **Created** — this file |

---

## Decisions captured in the canon

| Decision | Location in canon |
|----------|-------------------|
| AI never edits Layer 1 (Truth) | §1 Layer model |
| Five-layer model (Truth / Ontology / Intention / Search / City Intelligence) | §1 |
| Five AI roles with separate scope | §2 |
| Reviewer / Ghost Boss AI is mandatory infrastructure | §2 |
| Consultation Canon is product infrastructure, not chat memory | §3 |
| Evidence events are append-only; contradictions preserved | §4 |
| Intention certainty inferred from context, not asked as 1–10 | §6 |
| Search/refinement loop is flexible and reversible | §7 |
| All "better/worse" language must be conditional | §8 |
| Substitutions described as related strategies, not equivalents | §9 |
| Relationship mode: examine risks before optimization | §11 |
| No fear language, no deterministic breakup language | §11 |
| Rare Alignment / Unusual Congruence — never "Magic City" | §12 |
| Birth-time uncertainty: no fabricated fixed time, no noon default | §13 |
| Ontology Wizard: inferred/approved/active/conflict states | §14 |
| Style extraction separate from ontology | §14 |
| Experiential travel module: teach observation, not prediction | §15 |
| Model routing by task complexity, not one frontier model for all | §16 |
| Web2 instrument remains sovereign; AI is additive | §18 |

---

## Deferred implementation items

All of the following are documented but explicitly **not active** in Web2 Beta.

| Item | Why deferred |
|------|-------------|
| Consultation Canon DB schema | Requires architecture decision and migration plan |
| Navigator AI prompt design | Requires product iteration, safety review, and budget spec |
| Reviewer AI prompt design | Requires structured tool-call specification |
| Ontology Wizard UI | Requires Settings architecture extension planning |
| Reading upload pipeline | Requires security and anonymization specification |
| Birth-time uncertainty overlay rendering | Requires renderer extension planning |
| Relationship / family mode | Requires multi-profile chart pipeline |
| Experiential travel module | Requires GPS integration and mobile specification |
| Product package / pricing | Future commercial planning |

---

## Open questions

1. **Consultation Canon persistence:** Supabase JSONB column per profile row, or separate `consultation_events` table with materialized current state? The append-only evidence log favors a separate events table.

2. **Reviewer AI model tier:** What model class is acceptable for the Reviewer? It needs to reliably catch oracle language and hidden ranking but runs on every AI output — cost matters.

3. **Ontology Wizard promotion timing:** Is Ontology Wizard part of the initial AI release, or a separate professional tier promoted later? The professional onboarding path likely needs to be stable first.

4. **Multi-profile chart pipeline:** Relationship mode requires storing and rendering Person A, Person B, and Composite in one session. Does the current chart pipeline support this, or does it require a new investigation object type?

5. **Reading upload security:** What is the anonymization contract? Does the system need to verify anonymization, or does it rely on user attestation? Legal review needed before ship.

6. **Travel module GPS permission model:** Passive GPS logging vs. point-in-time queries vs. opt-in route recording — privacy and battery implications differ significantly.

---

## Next recommended slice

**AI-2 — Consultation Canon Data Model**

Define the database schema for the Consultation Canon: evidence event table, current-state materialized view, user ownership rules, correction mechanism. This is the pre-requisite for all AI feature work. It does not require any AI model; it is pure data architecture.

After AI-2 is stable, **AI-3 — Navigator AI Prompt Specification** becomes the first AI model work.

---

*AI-1 complete. No code changes. No database changes. No UI changes.*
---

## AI-1A Addendum — Consultation Architecture Refinement

**Date:** 2026-06-27

### Additional sections added (AI-1A)

| Section | Title | Key decisions |
|---------|-------|---------------|
| §18 | AI Initiative Levels | Three levels: Passive / Suggestive / Reflective. Suggestive teaches methodology by demonstrating it. Reflective always invites correction — never declares. |
| §19 | Consultation Profiles | Multiple independent profiles per user. Profiles never bleed into one another. Merging requires explicit user action. |
| §20 | Working Hypotheses | Separate from evidence. Evolve as evidence accumulates. Evidence never disappears. Fields include primary goal, confidence, secondary goals, active city hypotheses, rejected hypotheses, open tensions. |
| §21 | Consultation Checkpoints | Milestone summaries at meaningful consultation stages. Provide resume points and token-efficient context reconstruction. Append-only. Never replace the Consultation Canon. |
| §22 | Cost Principle | Structured persistent state is both a continuity and an economic tool. Prefer structured state over replaying full conversation histories to language models. |

### Section renumbering

Sections 18 and 19 (Web2 sovereignty and deferred items) moved to §23 and §24 to accommodate the five new sections.

### Open questions added by AI-1A

- **Profile switching UX:** How does the user navigate between active Consultation Profiles? Should the map surface reflect the active profile, or are profiles always in a separate panel?
- **Checkpoint trigger logic:** What defines a "meaningful stage" programmatically vs. narratively? Should the AI always suggest, or sometimes create silently with a notification?
- **Working Hypothesis display:** Is the Working Hypothesis always visible to the user, or surfaced on request? Should corrections to a hypothesis also generate an evidence event?
- **Token budget for Checkpoint context reconstruction:** What is the maximum token budget for reconstructing a session from a Checkpoint? This determines Checkpoint verbosity spec.

*AI-1A complete. Documentation only. No code changes. No database migrations.*
