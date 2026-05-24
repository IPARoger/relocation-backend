# Doctrine index

**Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.

**How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.

**Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using this broader index for deeper reference.

**Older doctrine and archaeology:** Older docs listed below remain valuable context, evidence, and active companions where not superseded. Treat them as secondary to `docs/constitutional/` on layer sovereignty, forbidden crossings, epistemic humility, runtime/renderer sovereignty, and implementation governance unless a later explicit decision says otherwise.

**Pacing reminder:** **Philosophy and epistemology evolve slowly** (explicit revision). **Implementation details evolve quickly** (iterate with evidence), but **must not contradict** slow doctrine without updating the doctrine file.

---

## Philosophy, intentionality, and institutional synthesis

These files govern **meaning, agency, fate, tradeoffs, tone, and long-form institutional character**. They are **foundational**. Typical change rate: **rare**; edits should be deliberate, often after architect or governance review.

| Document | Governs | Stability |
|----------|---------|-----------|
| `docs/intentionality_and_symbolic_constraints.md` | Fate and agency, relocation as repositioning within structure, tradeoff intelligence, dynamic participation, AI implications at the **meaning** layer. | **Very slow** |
| `docs/brand_and_experience_foundations.md` | Emotionally non-interfering design, interpretive language, archetypal restraint, instrument-not-dashboard, contemplative goals. | **Very slow** |
| `docs/institutional_philosophical_synthesis.md` | Training-oriented weave of philosophy, AI stance, UX, and tensions; synthesizes the above and archaeology themes. | **Slow** |
| `docs/institutional_memory_synthesis.md` | Bridge from archaeology to repo: Implemented, roadmap, speculative labels; UX and visual doctrine summaries; AI strategy summary; unresolved tensions. | **Medium** |

**Foundational product truths (compact, repo-native):**

| Document | Governs | Stability |
|----------|---------|-----------|
| `ai_context/core_product_truths.md` | Astrology truth standard, inspectability, map UX morals, product experience, interpretive integrity pointers, development discipline. | **Slow** |
| `ai_context/product_brief.md` | Short product identity, overlay truth standard, architecture direction bullets, validation corpus stance. | **Medium** |

---

## AI governance and interpretive systems

Governs **how models may speak**, **reviewer layers**, **anti-patterns**, and **drift risks**—operational constraints, not generic “AI ethics” branding.

| Document | Governs | Stability |
|----------|---------|-----------|
| `docs/ai_constitution_and_review_architecture.md` | Three-layer model (generate, review, doctrine), anti-pattern inventory, reviewer questions, symbolic restraint, professional audience. | **Slow**; tactical notes inside may rev faster |
| `docs/review_contracts_and_governance.md` | Lightweight **implementation review**: guardrails without bureaucracy; question lists for UX, AI, integrity, contemplative space. | **Medium** |

*(Process-layer companions: `docs/process/doctrine_review_cycle.md`, `docs/process/ai_drift_audit_framework.md` — see Meta-governance section.)*

**Process memory:**

| Document | Governs | Stability |
|----------|---------|-----------|
| `ai_context/memory_workflow.md` | Promotion from chat and reports to durable docs; anti–vibe-chaos; types of memory. | **Medium** |

---

## Meta-governance / institutional maintenance

**How** doctrine, uncertainty, archaeology, and AI behavior stay coherent over **years**—without process theater. These are **operational philosophy** docs: rhythms, frameworks, and audit checklists. Change when workflow or team scope shifts; not on every sprint.

| Document | Governs | Stability |
|----------|---------|-----------|
| `docs/process/doctrine_review_cycle.md` | Periodic doctrine, UX, AI, and archaeology review **cadence**; slow vs fast docs; tension preservation; post-pivot requirements; good/bad drift examples. | **Medium** |
| `docs/process/decision_and_uncertainty_framework.md` | Uncertainty tiers, heuristic vs exact truth, exploratory vs deterministic posture, reversible decisions, aura as case study, popup/line authority hierarchy. | **Medium** |
| `docs/process/archaeology_and_synthesis_workflow.md` | Raw capture → synthesis → canonicalization → review bundle → model rehydration; anti-flattening rules. | **Medium** |
| `docs/process/ai_drift_audit_framework.md` | Reusable AI behavior audit: drift modes, severity, sample questions, healthy posture examples. | **Medium** |
| `docs/review_contracts_and_governance.md` | Lightweight **per-change** review prompts (implementation, UX, AI, integrity); improvisation vs drift. | **Medium** |
| `docs/review_bundle/` | **Snapshot** package for external philosophical audit (`README.md` + copied doctrine + `open_questions_and_tensions.md`). | **Regenerate** per audit |

**Distinction:** `review_contracts` = **gate before merge/ship**; `doctrine_review_cycle` = **rhythm over time**; `decision_and_uncertainty_framework` = **epistemic rules** for what may stay fuzzy; `archaeology_and_synthesis_workflow` = **memory pipeline**; `ai_drift_audit_framework` = **interpretive AI** pass/fail patterns.

---

## Rendering substrate architecture

Governs **how the relocation map computes and renders truth**—the
substrate beneath UX and visual semantics. This is law for any
change touching the polygon engine, overlays, or transit math.

| Document | Governs | Stability |
|----------|---------|-----------|
| `docs/CURRENT_RENDERING_DOCTRINE.md` | **Start here** — one-page summary of the current stack (screen-space truth, adaptive refinement, targeted escalation, Phase-2 cache, brute-force wall) plus superseded-doc index and backsliding warnings. | **Medium** |
| `docs/relocation_map_architecture.md` | Immediate-truth + opportunistic-expansion architecture: brute-force as canonical truth, Phase-1 immediate render / Phase-2 background cache (priority protocol), zoom = edge refinement, transit philosophy, targeted refinement hardening, house negative-space (future only), ordered development sequence. | **Slow** |
| `docs/PHASE_C_RENDERING_ARCHITECTURE.md` | Governing architecture/philosophy of the adaptive screen-space refinement substrate. | **Slow** |
| `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` | Phase-2 cache integration architecture and production-oriented orchestration doctrine. | **Slow** |
| `docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md` | Controlled migration plan from legacy `/search-regions` overlays to the canonical screen-space substrate. | **Slow** |
| `docs/PHASE_C_IMPLEMENTATION_PROTOCOL.md` | Operating manual for implementing Phase-C work through reversible commits and validation gates. | **Slow** |

**Superseded (archaeology preserved, do not implement from these):**

| Document | Why |
|----------|-----|
| `docs/technical_philosophy/progressive_field_reveal.md` | Reveal drove the solve |
| `docs/technical_philosophy/truth_field_rendering_path.md` | Scalar-field / raster path |
| `validation/narratives/polygon_reveal_*.md`, `progressive_reveal_phase_b.md` | Reveal pacing R&D |
| `validation/narratives/screen_pixel_block_sweep.md` | Global block-size wrong target |

---

## UX, experience, and product roadmap

Governs **how the product feels and behaves** in interaction—doctrine adjacent to shipping detail.

| Document | Governs | Stability |
|----------|---------|-----------|
| `docs/ux_principles_and_emotional_tone.md` | Temperament, map-first, overlap readability, layout cautions, mobile honesty, when to stop designing. | **Slow** |
| `docs/relocation_app_product_roadmap.md` | Strategic product narrative and capability bands. | **Medium** |
| `docs/current_sidebar_ux_audit.md` | Historical audit snapshot; informs decisions, not necessarily current UI truth. | **Mostly static** |
| `docs/next_implementation_sequence.md` | UX-band sequencing for shipping the **product surface**; lives alongside `docs/relocation_map_architecture.md`, which governs the rendering substrate. | **Fast** relative to philosophy |

---

## Visual semantics, overlays, and cartography

Governs **what visuals mean** (truth hierarchy, layers, encodings) and **planning** for aura, overlap, NOT, color—distinct from incidental pixels in the live HTML.

| Document | Governs | Stability |
|----------|---------|-----------|
| `docs/visual_semantic_style_guide.md` | Truth hierarchy table, house vs aura semantics, texture, NOT, color philosophy, popup language, implementation discipline. | **Slow** for meaning |
| `docs/overlay_and_aura_visual_strategy.md` | Overlap philosophy, aura philosophy, child-color direction, NOT, layer mute model, onboarding veil ideas. | **Slow** for meaning; **medium** for tactics |
| `docs/aspect_aura_defaults.md` | Aspect and aura tuning notes tied to product parameters. | **Medium** |
| `docs/cartographic_language_and_city_rendering.md` | Basemap vs gazetteer separation, tile language, geocoder relationship. | **Medium** |
| `docs/map_and_overlay_design_research.md` | Research and constraints; MVP map-library stance; not an automatic mandate to migrate. | **Medium** |

---

## Place search, identity, data feasibility

Governs **named-place work** and professional trust in geography—not contour math.

| Document | Governs | Stability |
|----------|---------|-----------|
| `docs/geocoder_and_city_identity_strategy.md` | Doctrine and target ranking and disambiguation; honesty about placeholder data. | **Slow** for doctrine; **faster** for vendor specifics |
| `docs/geocoder_dataset_feasibility.md` | Dataset and vendor tradeoffs; feasibility. | **Medium** |

---

## Validation, proof, and quality

**How we know the map is right**—evidence, narratives, scripts. Narratives and reports change often; **the habit** of validation is foundational.

| Location | Governs | Stability |
|----------|---------|-----------|
| `validation/` (narratives, reports, screenshots) | Regression stories, QA checklists, structured reports—**evidence**. | **Append-heavy** |
| `memory_archaeology_raw/consolidated_notes/validation_and_proof_strategy.md` | Themed archaeology notes on proof posture. | **Medium** |

---

## Institutional memory, archaeology, hygiene

Raw and consolidated **conversation-derived** material; taxonomy and cleanup.

| Document | Governs | Stability |
|----------|---------|-----------|
| `memory_archaeology_raw/pending_imports/` | Raw extracts—**evidence**, not canonical law. | **Append** |
| `memory_archaeology_raw/consolidated_notes/` | Themed synthesis from archaeology (UX, AI, overlay philosophy, architecture, and so on). | **Medium** |
| `docs/project_memory_taxonomy.md` | Taxonomy of memory types. | **Medium** |
| `docs/project_continuity_workflow.md` | Continuity for humans working the repo. | **Medium** |
| `docs/workspace_hygiene_and_cleanup.md` | Weight, cleanup, archive options. | **Medium** |
| `docs/local_archive_policy.md` | Local archive discipline. | **Slow** |

---

## Implementation state and decisions (fast-moving)

Describes **what is true now** and **what was decided**.

| Document | Governs | Stability |
|----------|---------|-----------|
| `ai_context/current_state.md` | What works, what is caveated, which files matter. | **Fast** |
| `ai_context/decisions.md` | Recorded decisions steering implementation. | **Fast** |
| `ai_context/open_questions.md` | Unresolved questions—inputs to future doctrine and review. | **Fast** |
| `ai_context/README.md` | Onboarding pointer for `ai_context/`. | **Medium** |

---

## Review outputs and proposals (rotating)

| Location | Governs | Stability |
|----------|---------|-----------|
| `ai_context/review_latest.md`, `ai_context/cursor_latest_report.md` | Latest reviewer or agent outputs—**not** law. | **Rotating** |
| `ai_context/proposed_updates/` | Suggested patches to memory—pending human merge. | **Until merged or rejected** |

---

## Live application surface (fastest iteration)

| Artifact | Governs | Stability |
|----------|---------|-----------|
| `map_CURRENT.html`, backend Python modules, `cities.js`, and related | **Behavior as shipped**. Accountable to `docs/visual_semantic_style_guide.md` and `ai_context/core_product_truths.md`. | **Fast** |

Code is **not** indexed exhaustively here; this page names **doctrinal** companions. When code and doctrine diverge, **fix code or update doctrine explicitly**—never silent drift.

---

## Suggested reading order (new contributor or agent)

1. `ai_context/constitutional_summary.md`
2. `ai_context/current_project_state.md`
3. `docs/constitutional/README.md`
4. `docs/DOCTRINE_INDEX.md` (this file) for deeper reference
5. `ai_context/core_product_truths.md`
6. `docs/CURRENT_RENDERING_DOCTRINE.md` then `docs/relocation_map_architecture.md` before any change to the polygon engine, overlay endpoints, or rendering substrate
7. `docs/intentionality_and_symbolic_constraints.md`
8. `docs/visual_semantic_style_guide.md` §1 (truth hierarchy)
9. `docs/brand_and_experience_foundations.md` (interpretive sections)
10. `docs/review_contracts_and_governance.md` before a substantive change review
11. `docs/ai_constitution_and_review_architecture.md` before any interpretive AI ship
12. `docs/process/decision_and_uncertainty_framework.md` when adding heuristics, confidence UI, or fuzzy visual layers
13. `docs/process/doctrine_review_cycle.md` + `docs/process/archaeology_and_synthesis_workflow.md` when maintaining memory or after a major pivot

For breadth without implementation detail: `docs/institutional_philosophical_synthesis.md`.  
For external audit handoff: `docs/review_bundle/README.md`.

---

## Cross-links from other docs

`docs/institutional_memory_synthesis.md` lists this index alongside raw and consolidated archaeology paths so reviewers can jump here quickly.

---

## Revision

Update `docs/DOCTRINE_INDEX.md` when new **durable** docs are added under `docs/`, `docs/process/`, or `ai_context/` that govern behavior, meaning, or review. File moves, renames, or archival changes should be reflected so the index stays trustworthy.
