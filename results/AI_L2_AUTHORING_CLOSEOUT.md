# AI-L2-1 — Layer 2 Authoring Platform Architecture Closeout

**Date:** 2026-06-27
**Task:** AI-L2-1 — Layer 2 Authoring Platform Architecture
**Mode:** Architecture and product design only — no interpretive content, no migrations, no production code
**Model:** Claude Opus
**Status:** Complete

---

## Files created / updated

| File | Action |
|------|--------|
| `docs/canon/LAYER_2_AUTHORING_ARCHITECTURE.md` | **Created** — 15-section platform architecture (~4,100 words) |
| `docs/canon/AI_CONSULTATION_ARCHITECTURE.md` | **Updated** — §14 Ontology Wizard cross-references the authoring architecture |
| `docs/BETA_MASTER_CHECKLIST.md` | **Updated** — canon table row added |
| `results/AI_L2_AUTHORING_CLOSEOUT.md` | **Created** — this file |

---

## Central architectural decision

**Every Layer 2 entry is an addressable, identity-bearing object — not a paragraph inside a file.**

The entry, not the model and not the file, is the atomic unit of authorship, review, versioning, inheritance, and reuse. Every other design decision in the document follows from this commitment. This is what converts Layer 2 from a content store into a knowledge platform on the model of WordPress (addressable objects + revisions + lifecycle), Notion (typed structured properties), and Obsidian (a graph of linked entries).

The stable canonical ID (`L2-PIH-SUN-10`) is content- and version-independent. It is what lets an astrologer say "revisit Saturn in the 12th" and land on one object rather than a scroll position, and what lets a second author fork only the Venus entries while everything else inherits.

---

## Decisions captured (by design question)

| # | Question | Decision |
|---|----------|----------|
| 1 | Representation | Entries as objects with a typed content payload + metadata envelope; closed, versioned entry-type registry |
| 2 | Inheritance | Default → sparse Professional Override; per-entry copy-on-write resolution; multi-level chain permitted |
| 3 | Versioning | Two planes: append-only entry version log + immutable published model manifest |
| 4 | Approval states | Draft / AI Suggested / Needs Review / Approved / Deprecated / Archived; explicit audited state machine; human-only Approved |
| 5 | Reading upload | Pre-population pipeline → AI Suggested entries with provenance, confidence, conflict flags; never auto-approve |
| 6 | Fallback | Entry- and field-level fallback to a guaranteed-complete Default Model |
| 7 | Consultation pinning | Consultation stores model_id + manifest_version + resolved digest; reproducible years later |
| 8 | Consumption | Read-only resolved manifest; Engine reads structured fields, Navigator reads prose, Guardian audits provenance |
| 9 | Wizard | Workflow = addressing (query over entries) + work queues + durable review sessions; never raw markdown |
| 10 | Review/export | Export is a projection; DB of entries is source of truth; ID-reconciled round-trip |
| 11 | Modularity | Sparse override models; override one entry without duplicating the rest |
| 12 | AI assistance | AI may draft; humans approve; AI never silently edits approved content; proposes new versions into review |

---

## Constitutional alignment

- **Reveal, don't impose (§0.2):** the platform reveals an astrologer's own method back as inspectable structure; never imposes a method, never silently rewrites one.
- **§7.6–7.9:** the AI-draft / human-approve boundary (doc §12) is the Layer 2 expression of "the AI reveals a candidate; the human keeps judgment."
- **Guardian (consumption §8.2):** enforces that only Approved-and-published content reaches user surfaces; no fabricated ontology.

---

## Deferred implementation

All nine phases (L2-P0 through L2-P8) are deferred. The Beta ships exactly one default model and builds none of this platform. Each phase requires its own implementation document, migration plan, validation gate, and rollback path before becoming active work.

Smallest safe first step: **L2-P0 — Default Model formalization** (represent the single Beta default model as addressable, typed entries with stable IDs, internal only). Its precondition is freezing the entry-type registry (§1.2).

---

## Open questions

1. **Entry-type registry scope:** The illustrative registry (§1.2) lists eleven types. The final closed set — and per-type field schemas — is a downstream schema task. Which types are required for L2-P0 vs. added later?

2. **ID scheme for compound subjects:** `L2-ASP-SUN-MC-TRINE` works for two-body aspects. Do multi-factor archetype clusters (`CLU`) and recipes (`REC`) need a richer ID grammar, or is a slug sufficient?

3. **Manifest publish cadence:** Who/what triggers a new manifest publish — explicit author action only, or also a scheduled compile? Affects how quickly approved edits reach consumers.

4. **Default Model governance:** The Default Model is platform-owned. What is its own authorship/version/review process? Does it use this same platform internally (dogfooding) from L2-P0?

5. **Cross-model entry references:** Can a `related`/`dependency` link point across models (e.g., an override entry depending on a default entry), and how does that interact with manifest pinning?

6. **Style profile model:** Style is extracted separately (§5.4) but its own object model (versioning, approval, inheritance) is only sketched. Does it deserve a parallel mini-architecture?

---

## Next recommended slice

**AI-3 — Search Specification Schema** remains the highest-priority technical interface (Translation Engine ↔ Engine), independent of Layer 2.

For Layer 2 specifically: **AI-L2-2 — Entry Type Registry and Field Schemas** — freeze the closed entry-type set and define the typed field set per type. This is the precondition for L2-P0 and the natural continuation of this architecture.

---

*AI-L2-1 complete. Architecture and product design only. No interpretive content. No migrations. No production code.*
