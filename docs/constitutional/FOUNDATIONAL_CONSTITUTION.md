# FOUNDATIONAL_CONSTITUTION.md

**Status:** Foundational constitution for the Astrological Geography platform.  
**Source archive:** `ALL_PROJECT_DOCUMENTS.txt`  
**Generation method:** deeper three-pass local Python extraction and consolidation.  
**Total archive file blocks parsed:** 196  
**Constitutional/foundational source blocks matched:** 196  
**Audit hash:** `90e1ae96336fd53e`

---

## 0. Constitutional chain

The project’s identity rests on three linked layers. Each layer answers a different question. Together they form a chain that scales as more contributors and AI agents join the project.

```
Constitution          →  First Law
Design philosophy     →  Design Spirit
Engineering checklist →  Operational Test
```

If someone unfamiliar with the project asks what it is really trying to do, the shortest faithful answer is:

> **We build instruments that reveal structure while preserving human judgment.** Every subsystem — from the renderer to the AI — exists to illuminate reality rather than replace the person’s own discernment.

---

### 0.1 First Law

**Reveal structure. Preserve judgment.**

This sentence is the constitution. Everything else in the project is subordinate to it.

The system exists to reveal chart structure in geography. It computes, displays, stores, compares, and validates where chart conditions hold in space. It helps the human user see structure that would otherwise require tedious one-city-at-a-time checking. It makes the structure visible, searchable, inspectable, and replayable.

The system must preserve judgment. The final act of meaning belongs to the human agent: the professional astrologer, the client, the exploratory user, or the person making a life decision. The software must not seize that role. It must not call itself the authority on where someone should live. It must not automate astrological conclusions behind the user’s back. It must not hide a ranking engine under a beautiful map. It must not turn symbolic tradeoffs into a single machine verdict.

This constitution protects the human user from three failures: false certainty, hidden authority, and symbolic flattening. The app may reveal “where Sun is in the 1st house.” It may reveal “where Venus in the 7th overlaps with Sun in the 1st.” It may reveal “where the selected condition is excluded.” It may reveal a point’s relocated chart facts. It may not say, as product truth, “therefore this city is best.”

---

### 0.2 Design Spirit

**Reveal, don’t impose.**

The First Law is the legal formulation. The Design Spirit is how it feels in practice — the ethic that holds every product decision together from Web2 through the most ambitious future vision. Because it is simple, it scales.

These are not separate doctrines. They are manifestations of one constitutional idea across subsystems:

| Subsystem | Reveal | Don’t impose |
|-----------|--------|--------------|
| Rendering | Reveal geometry. | Don’t fake topology. |
| Backend | Reveal data. | Don’t invent architecture. |
| UI | Reveal controls. | Don’t hide complexity behind “magic.” |
| AI | Reveal reasoning. | Don’t perform expertise. |
| Astrology | Reveal symbolism. | Don’t dictate destiny. |
| Map and overlays | Reveal the map. | Don’t decorate it. |
| Consultation | Reveal tradeoffs. | Don’t choose for the user. |
| The instrument | Reveal the instrument. | Don’t hide it behind AI. |

The principle is fundamental, not merely elegant. Every subsystem converges on the same pattern because the product is one instrument, not a collection of features.

---

### 0.3 Operational Test

Whenever adding a feature, ask:

1. **What truth is being revealed?**
2. **What judgment still belongs to the user?**
3. **Is anything being imposed that should instead remain visible?**

If the third question cannot be answered clearly, the feature is not ready.

This test applies to rendering, backend contracts, UI flows, AI outputs, settings, exports, onboarding, and every future subsystem. It is the engineering checklist derived from the Design Spirit, which is derived from the First Law.

---

## 1. Constitutional Source Scope

The deeper pass scanned and consolidated source blocks containing constitutional language, foundational tenets, epistemic integrity rules, symbolic humility doctrine, system boundaries, human judgment protections, AI authority limits, validation governance, moral limits of data use, and future policy placeholders.

The matched constitutional categories were:

| Constitutional Category | Matched Blocks |
|---|---:|
| ai_authority_limits | 193 |
| architecture_boundaries | 183 |
| constitutional_anchor | 135 |
| epistemic_integrity | 191 |
| future_policy_domains | 168 |
| human_agency_and_judgment | 107 |
| moral_data_use_limits | 196 |
| symbolic_humility_and_interpretation | 142 |
| validation_governance | 140 |

The source set shows that the constitution is not merely philosophical. It directly governs architecture, rendering, AI, UX, validation, persistence, shared views, professional workflows, and future interpretation systems.

---

## 2. Human Agency Is the Protected Good

### 2.1 The system serves interpretation but does not perform it

The product exists because relocation astrology involves symbolic judgment. A chart condition is not universally good or bad. It becomes meaningful in relation to intention, context, timing, client temperament, lived constraints, professional judgment, and personal agency. Therefore the software cannot be the final interpreter without corrupting the nature of the work.

The constitutional boundary is precise: the system may make conditions visible and searchable; the user evaluates them.

### 2.2 Professional sovereignty

Professional astrologers must remain in charge of symbolic reasoning. The app can accelerate their work, reveal alternatives, preserve searches, compare locations, and prepare client-facing views. It cannot override their judgment or quietly replace their interpretive process. Professional mode must not become an AI oracle wearing a professional UI.

### 2.3 Lay-user agency

Lay users may need more education and guidance, but they still deserve agency. Future AI can help them learn, clarify intentions, and understand options. It cannot manipulate, frighten, flatter, or manufacture a destiny narrative. The user brings biography, values, culture, imagination, and choice.

### 2.4 No hidden paternalism

The app must not decide that it knows better than the user. It must not suppress complex tradeoffs because they are difficult. It must not over-rank “benefic” configurations or over-warn about difficult ones outside explicit user criteria. Human intention matters.

---

## 3. Epistemic Integrity

### 3.1 Truth hierarchy

The constitution establishes a truth hierarchy:

1. **Point truth / popup inspection** is the local authority for a coordinate.
2. **Overlays** are exploratory where-fields.
3. **Chart and account pages** carry denser factual records.
4. **Interpretation** is downstream and human-governed.
5. **AI assistance** is optional and subordinate.

A map overlay that appears to contradict point truth must be corrected, not excused by aesthetics. A popup fact outranks an overlay impression. A validation artifact outranks model confidence. Repository truth outranks chat memory.

### 3.2 Evidence before certainty

The project must prefer evidence over confidence. Validation reports, smoke tests, brute-force walls, popup comparisons, screenshot baselines, raw endpoint responses, and audit metadata are not administrative clutter. They are constitutional instruments. They prevent plausible stories from becoming false law.

### 3.3 Beauty cannot substitute for truth

A beautiful visual that lies is unconstitutional. Blur cannot hide sampling gaps. Glow cannot redefine membership. Smoothness cannot replace correct geometry. Palette cannot fix math. The interface may become beautiful only in ways that remain accountable to the truth substrate.

### 3.4 Unknowns must remain visible

The system and its maintainers must not pretend to know what they have not validated. If a feature is a draft, call it a draft. If a source pass matched 186 of 196 files, say so. If a renderer is beta-stabilized but not final aesthetic approval, say so. If a future AI mode is speculative, mark it future.

This is not pessimism. It is epistemic hygiene.

---

## 4. Symbolic Humility

### 4.1 Astrology is symbolic, not deterministic command

The platform works with astrological symbolism, but it must not become fatalistic. A chart condition can suggest emphasis, structure, tension, opportunity, or difficulty. It does not authorize the software to dictate a life path.

### 4.2 Archetypes hold shape

Symbolic humility does not mean flattening everything into pleasant ambiguity. Saturn remains Saturn. Hard aspects remain hard. Difficult houses remain meaningful. Tradeoffs must remain visible. The system should not comfort-spin every configuration into equal positivity.

### 4.3 No forced destiny language

The product must reject cosmic guarantee language, clickbait mysticism, prophecy voice, and manipulative certainty. Language should preserve openness: “may,” “can suggest,” “one possible expression,” “often relates to,” “under this intention,” and similar framing. Vivid interpretation can exist later when grounded in symbolism, but the shell remains calm and non-coercive.

### 4.4 Recognition over surprise theater

A strong interpretation often produces recognition. It does not need to invent biographical detail. The system must not fabricate personal history, future events, psychology, relationships, career claims, or fate narratives from chart structures.

### 4.5 Tradeoffs are constitutional

Relocation astrology is valuable because it helps users navigate tradeoffs. The system must not erase tension. A location may improve public visibility while increasing private pressure. Another may support relationships while reducing career emphasis. The app must hold this complexity rather than collapse it into winner/loser language.

---

## 5. Moral Limits of Data Use

### 5.1 User data exists to serve user inquiry

Birth data, chart records, saved locations, notes, comparisons, saved searches, shared views, settings snapshots, and future AI context exist to support the user’s exploration. They must not be repurposed into hidden manipulation, unreviewed scoring, or unexplained product conclusions.

### 5.2 Sensitive interpretive material requires restraint

Astrological interpretation can touch life decisions, relationships, career, family, belonging, illness anxiety, spiritual identity, and vulnerability. Future generated interpretation must be treated as sensitive. It needs humility, labeling, and human review pathways for client-facing content.

### 5.3 Shared views require bounded authority

A shared client view is curated. It should expose selected overlays and perhaps limited inspection controls. It must not allow a client to unknowingly mutate the professional’s selected conditions unless that permission is explicit. It must not present debug internals as client-facing truth.

### 5.4 Saved objects require replay honesty

Saved searches and investigations must preserve semantic conditions and settings snapshots. The user should be able to understand what was searched, when, under what settings, and for which chart. Silent mutation of saved meaning is a moral and technical failure.

### 5.5 AI-generated text must be distinguishable

Future AI summaries, notes, client reports, or comparison narratives must be distinguished from factual chart data and from human-authored notes. The user must know what came from the machine and what it is based on.

---

## 6. System Boundary Constitution

### 6.1 Layer separation

The system must preserve layer boundaries:

- Geometry computes factual chart/geography truth.
- Ontology defines available condition language and settings.
- Intent frames the human question.
- Interpretation remains downstream and human-governed.
- Experience makes the system usable and emotionally safe.

No lower layer may be overwritten by a higher layer’s desire. Styling cannot change geometry. AI cannot invent facts. User intention cannot make a condition true. Vocabulary cannot silently mutate saved truth.

### 6.2 Cities are secondary

Cities are human markers inside geography. They are not the computational source. This prevents the product from collapsing into city recommendation and preserves the condition-first search model.

### 6.3 Map-first but not map-only

The map is the instrument face. It reveals geography. But chart records, saved searches, comparisons, favorites, notes, and shared views are also necessary for coherent human work. The constitution rejects “everything on one screen” collapse.

### 6.4 Debug is not product

Developer diagnostics are allowed and important. They must remain separated from commercial UX surfaces. Debug strings, validation overlays, sampling internals, and status metrics should not leak into normal use.

### 6.5 Future is not active law

Future features should be inventoried, not smuggled into active instructions. Rain/Virga, Web3 models, AI interpretation, certification ecosystems, consumer intake, advanced ontology packs, and future regulatory systems require explicit promotion before becoming product law.

---

## 7. AI Constitutional Limits

### 7.1 AI is not the judge

AI can assist, explain, organize, summarize, and suggest. It cannot be the final authority. It must not declare optimal places, override professionals, create hidden rankings, fabricate certainty, or speak as an oracle.

### 7.2 AI must preserve fact/interpretation labels

AI outputs must separate factual chart conditions from interpretive commentary, user intention, and uncertainty. If AI says “Venus is in the 7th here,” that must be grounded in facts. If it says “this may emphasize relationship themes,” that is interpretation and must be labeled as such.

### 7.3 AI must not hallucinate architecture

Development AI must not invent endpoints, database schemas, renderer behavior, or validation status. It must read current files, state unknowns, preserve rollback, and avoid fake confidence.

### 7.4 AI must resist flattery

AI must not bend symbolism to please. It must not turn every hard placement into a hidden blessing or every user desire into confirmation. Respectful truthfulness is more important than comforting language.

### 7.5 AI must be optional where judgment matters

The non-AI professional core must remain usable. A professional should not be forced to ask an AI to operate the instrument. AI is an enhancement, not the product’s constitutional center.

### 7.6 Astrology provides structure. The AI reveals patterns. The user discovers meaning.

These roles must never be confused. The AI must not complete the user’s story, close interpretive space prematurely, or deliver meaning the user should discover for themselves. Recognition is more valuable than explanation. The AI illuminates architecture; the user supplies lived experience.

### 7.7 The AI should never use astrology to demonstrate its own expertise.

It should use astrology to illuminate the user’s experience and support better decisions. The AI’s intelligence should appear through clarity, not complexity. An output that impresses is less valuable than an output that clarifies.

### 7.8 The AI should interpret the chart honestly, then interpret it in the context of the user’s stated intentions.

Neither the chart nor the intentions should be allowed to erase the other. A technically challenging chart condition should not be dismissed because the user wants reassurance. A user’s stated intention should not override what the chart actually shows.

### 7.9 The AI succeeds when users become progressively more capable of using the instrument without assistance.

Dependence is not the goal. Competence is the goal. An AI feature that makes users more capable over time is constitutional. An AI feature that creates dependence without building capability is not.

---

## 8. Governance and Validation Constitution

### 8.1 One instability source at a time

The project must not debug math, renderer, browser state, cache, UI style, and backend endpoints simultaneously. One change. One hypothesis. One validation gate. One rollback path.

### 8.2 Rollback is a constitutional requirement

Risky changes must be reversible. Git checkpoints, flags, adapters, and smoke gates are not bureaucracy. They preserve project trust.

### 8.3 Validation artifacts are memory

The project’s validation records are institutional memory. They prevent future AI sessions from reopening panic loops or misremembering resolved issues. They should be retained, indexed, and labeled.

### 8.4 Archaeology must remain labeled

Failed paths and superseded documents should not be erased. They should be preserved with clear status banners. This protects future contributors from repeating expensive mistakes.

### 8.5 Closeout discipline

Significant work should end by stating files changed, validation run, rollback scope, deferred-excellence updates, rejected scope, uncertainty, and next smallest safe step. A task that ends with only “done” is too opaque for this project.

---

## 9. Active Constitutional Non-Goals

The active constitution does not authorize:

- automatic city ranking;
- deterministic life advice;
- hidden symbolic scoring;
- AI oracle behavior;
- unreviewed client-facing generated interpretation;
- cosmetic smoothing that changes truth;
- debug clutter in production UX;
- broad speculative rewrites;
- feature-flag infrastructure beyond demonstrated need;
- social/engagement manipulation;
- Web3 ownership systems;
- future regulatory frameworks;
- model-training pipelines;
- rain/virga product animation;
- certification ecosystems.

These may be tracked for later. They are not active law.

---

## 10. Constitutional Review Checklist

Before accepting a feature, document, AI output, or code change, ask:

1. Does it reveal structure?
2. Does it preserve judgment?
3. Does it protect human agency?
4. Does it separate fact from interpretation?
5. Does it preserve symbolic humility?
6. Does it avoid forced certainty?
7. Does it avoid hidden ranking?
8. Does it preserve popup truth?
9. Does it avoid beauty that lies?
10. Does it respect layer boundaries?
11. Does it keep cities secondary to geographic truth?
12. Does it treat data as serving user inquiry?
13. Does it label AI-generated interpretation?
14. Does it avoid flattery distortion?
15. Does it include validation or admit validation is pending?
16. Does it include rollback if risky?
17. Does it avoid resurrecting superseded archaeology?
18. Does it keep future ideas out of active instructions?
19. Does it preserve professional sovereignty?
20. Does it tell the truth about uncertainty?

---

## Future Constitutional Excellence Inventory

This inventory tracks future policy and boundary work without making it active law.

### Interpretation policy

- Formal fact/interpretation labeling standard.
- Sensitive-output review protocol.
- Policy for “positive only” user requests.
- Archetypal integrity rubric.
- Client-facing AI report review gates.

### AI constitution maturity

- Model prompt constitution for consumer AI.
- Professional-assist AI constitution.
- AI flattery and overcertainty evaluation sets.
- Hallucinated-architecture detection.
- Human approval gates for generated client materials.

### Data ethics and privacy

- Chart data retention policy.
- Shared-view permission framework.
- Client/professional data separation.
- Export provenance rules.
- AI-generated note provenance.

### Governance and validation

- Canon drift audits.
- Constitutional review checklist automation.
- Superseded-doc banner enforcement.
- Evidence artifact registry.
- Validation dashboard only if someone will actually read it.

### Future product-policy domains

- Web3 or portable ontology ownership review.
- Certification ecosystem boundaries.
- Consumer guidance limits.
- Regulatory review for advice-like outputs.
- International privacy and data-use rules.

### Experience and emotional safety

- Emotional-noise QA method.
- Long-session comfort review.
- Anti-manipulation interaction audit.
- Calm-shell / vivid-content boundary tests.
- Accessibility and reduced-motion policies for future reveal systems.



---

## Appendix A — Constitutional Source Index

### A.1 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/AI_WORKFLOW_GOVERNANCE.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 14272; SHA-12: `570f3cca823a`; score: 112
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Constitutional signals:
  - # AI Workflow Governance Protocol
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in writing.
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisible engineering inte…
  - The Ghost Boss role of this protocol is to protect the project from short-term commercial pressure, founder optimism, and AI recency bias. It asks: what invisible thing did this phase make easier to forget, normalize, or accidentally depend on?
  - ## Ghost Boss Governance Doctrine

### A.2 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/CURRENT_RENDERING_DOCTRINE.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 7576; SHA-12: `0b4a58929157`; score: 56
- Key headings: Current Rendering Doctrine — Summary; The stack (top to bottom); Non-negotiables; Legacy `/search-regions` Truth Grid; Phase-2 cache (product substrate); Evidence bundle (read in this order); Documents marked SUPERSEDED (archaeology preserved); Warnings against backsliding; Remaining gaps (structural, not aesthetic); Recommendation
- Constitutional signals:
  - # Current Rendering Doctrine — Summary
  - > **Authority:** `docs/relocation_map_architecture.md` wins on conflict.
  - | **Brute force** | Validation wall. Every optimisation must match it cell-for-cell (or pixel-for-pixel on screen). | Canonical control specimen |
  - | **Screen-space truth** | Production sampling axis for **visible overlays**. Classify what the user actually sees. | Canonical for rendering |
  - | **Targeted escalation** | Extra halo / probes / lat-cap boundary rules **only** at known instability classes. | In use — not global |

### A.3 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DEFERRED_EXCELLENCE_REGISTRY.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 30563; SHA-12: `8fdc70fc996d`; score: 140
- Key headings: Deferred Excellence Registry; Purpose; Cross-Cutting Doctrine; Status Legend; 1. Renderer / Topology Improvements; 1.1 Stable component IDs across zoom/pan; 1.2 Graph / global path solver; 1.3 Canonical-default migration; 1.4 Continuous topology extraction refinement; 1.5 Subpixel/edge extraction refinement for narrow-orb ASC; 1.6 Seam-aware topology continuity; 1.7 Signed-distance-field experiments
- Constitutional signals:
  - # Deferred Excellence Registry
  - This registry captures everything we know we *could* improve in the renderer, architecture, UX, product, and reliability stack — and have intentionally deferred to protect MVP velocity. Its primary purpose is **not** to accumulate shiny feature ideas. Features are comparatively e…
  - The primary purpose is preserving hidden robustness and institutional memory: invisible infrastructure improvements, architecture refinements, reliability upgrades, governance ideas, performance optimizations, renderer trust improvements, scaling concerns, cache/system improvemen…
  - These are the things founders and AI systems tend to forget because users do not directly see them, they do not demo well, short-term success can mask their absence, and commercial pressure naturally favors visible product work. The registry exists to preserve long-term engineeri…
  - Short rule: when choosing what to capture here, prefer invisible engineering and infrastructure concerns over visible feature wishes. Feature wishes may be listed when they carry trust, platform, or operational consequences, but the registry's center of gravity is hidden robustne…

### A.4 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DOCTRINE_INDEX.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 157
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Constitutional signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…

### A.5 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/EXECUTIVE_TRANSFER_BRIEF_NEXT_CHAT.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9792; SHA-12: `d91200d72161`; score: 79
- Key headings: Executive Transfer Brief For Next Chat; 1. Current Project State; 2. What Is Considered Solved; 3. What Is Intentionally Deferred; 4. Current Renderer Status; 4.1 Renderer handoff state; 5. Governance Status; 6. Productization Status; 7. Immediate Next Recommended Phases; 8. Strategic Warnings; 9. Key Philosophical Doctrines; 10. How Future AI Should Behave
- Constitutional signals:
  - Purpose: human/operator bootstrap for the next major AI session. This is not archaeology, not raw continuity, and not a replacement for `ai_context/archaeology/RAW_CONTINUITY_VOLUME_7.md`. It is the short strategic operating brief.
  - The project has moved from renderer research into product platform construction. The relocation map now has enough validated rendering confidence to support Phase 2 product work: chart library, saved views, handoff links, deep links, onboarding, future accounts, and professional …
  - - Screen-space truth and adaptive refinement have proven the future truth substrate.
  - - Brute-force wall validation exists as the reference method.
  - - Governance artifacts, continuity volumes, and deferred-excellence tracking are now project infrastructure.

### A.6 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_1_2_EXTRACTION_AUDIT.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 31222; SHA-12: `99e7cbcf42db`; score: 188
- Key headings: Phase 1.2 Extraction Audit; Concise Findings; Files Inspected; Production and backend; Sandboxes; Validation / capture scripts; Doctrine used as constraints; Current Rendering Entry Points; Production renderer; Backend endpoints; Sandbox renderers; Validation harnesses and capture scripts
- Constitutional signals:
  - > **Authority:** Follows `docs/PHASE_C_IMPLEMENTATION_PROTOCOL.md`,
  - must not change behavior and must not mix the legacy production overlay
  - - `/screen-pixel-truth` is validated and used by sandboxes and capture
  - - `map_SANDBOX_phase2_cache.html` contains the Phase-2 scheduler and a
  - canvas painter; it is the main safe source for scheduler extraction.

### A.7 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 58355; SHA-12: `c6ef18d0c316`; score: 298
- Key headings: Phase-2 Cache Integration — Architecture & Implementation Planning; 0. Where this fits; 1. Grounding — what is true today, measured; 1.1 Sandbox state (measured, not asserted); 1.2 What this means; 1.3 Hard architectural finding — substrate mismatch; 2. Production Scheduler Architecture; 2.1 Single-active-job model; 2.2 Foreground vs background queues; 2.3 Cancellation / interruption behaviour; 2.4 Priority escalation rules; 2.5 Viewport ownership
- Constitutional signals:
  - > **Status:** Architecture and planning doctrine. Design only. No code
  - > **Authority:** `docs/relocation_map_architecture.md` (§ "Phase 2 cache
  - > **Companion:** `validation/narratives/phase2_cache_implementation.md`
  - > **Stability:** Slow. Implementation details may rev; design rules here
  - | Foundational architecture | `docs/relocation_map_architecture.md` | Phase-2 cache priority protocol (canonical) |

### A.8 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_IMPLEMENTATION_PROTOCOL.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 54962; SHA-12: `c32fcebbd584`; score: 315
- Key headings: Phase-C Implementation Protocol; Operational constitution for landing the validated architecture without future chaos; 0. Where this fits; 1. Implementation Phase Breakdown; Phase 1.1 — Documentation alignment (no code); Phase 1.2 — Archaeology fencing (low-risk cleanup); Phase 1.3 — Scheduler extraction (no behaviour change); Phase 1.4 — Substrate adapter scaffold (legacy-only); Phase 1.5 — Canonical substrate wiring (flag-gated); Phase 1.6 — Scheduler/cache wiring on canonical (flag-gated); Phase 1.7 — Parity validation harnesses; Phase 1.8 — Default flip + stabilisation
- Constitutional signals:
  - ## Operational constitution for landing the validated architecture without future chaos
  - > **Status:** Operational doctrine. Implementation planning only.
  - > **Authority on conflict:** `docs/relocation_map_architecture.md`,
  - > `docs/process/*` and `ai_context/memory_workflow.md`.
  - > meta-governance cycle. Does not override slow doctrine.

### A.9 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_PRODUCTION_MIGRATION_PLAN.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 64644; SHA-12: `af96b1d10c2e`; score: 378
- Key headings: Phase-C Production Migration Plan; Legacy overlay pipeline → canonical screen-space adaptive substrate; 0. Where this fits; 1. Legacy vs Canonical Substrate Audit; 1.1 The legacy overlay pipeline (what is in production today); 1.2 The canonical screen-space substrate (validated, sandbox-proven); 1.3 Semantic differences; 1.4 Rendering differences (visible); 1.5 Cache compatibility implications; 1.6 Validation differences; 1.7 Hidden assumptions; 1.8 Likely regression risks (ranked)
- Constitutional signals:
  - > **Status:** Migration architecture and planning doctrine. Design
  - > **Authority on conflict:** `docs/relocation_map_architecture.md`,
  - validated screen-space adaptive substrate (`/screen-pixel-truth`).
  - | Foundational architecture | `docs/relocation_map_architecture.md` | Architecture canon |
  - | Current rendering doctrine | `docs/CURRENT_RENDERING_DOCTRINE.md` | Status board of the stack |

### A.10 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_RENDERING_ARCHITECTURE.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 47288; SHA-12: `3744bf667647`; score: 258
- Key headings: Phase C — Rendering Substrate Architecture (Governing Laws); 0. Where this document sits; 1. Canonical Rendering Truths; 1.1 The four absolute statements; 1.2 Screen-space truth doctrine; 1.3 Adaptive refinement as production substrate; 1.4 Why visible output is canonical; 1.5 Globe truth vs screen truth; 2. Convergence Strategy; 2.1 Convergence is the contract; sample count is not; 2.2 Targeted escalation, never global slowdown; 2.3 Refinement economy — *truth where unstable*
- Constitutional signals:
  - > **Status:** Foundational. Constitutional charter for the rendering substrate
  - > **Authority:** `docs/relocation_map_architecture.md` wins on direct conflict.
  - > **Adopted draft:** 2026-05-21 (same-day as the rendering doctrine reset).
  - > **Stability:** Slow. Implementation details around this doctrine may rev;
  - > future agents, contributors, and reviewers cannot quietly regress toward

### A.11 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PROJECT_CONTINUITY_INDEX.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 2667; SHA-12: `303dae8aa89c`; score: 23
- Key headings: Project Continuity Index; Canonical Governance Docs; Canonical Archaeology Docs; Canonical Renderer Doctrine Docs; Deferred Excellence; Validation Narratives; Continuity Volume Convention; Recommended Future-AI Ingestion Order
- Constitutional signals:
  - Purpose: short entry point for future AI/human rehydration. This file points to canonical governance, archaeology, renderer, deferred-excellence, and validation memory without replacing those sources.
  - - `docs/AI_WORKFLOW_GOVERNANCE.md` — mandatory closeout, Ghost Boss governance, continuity volume protocol, hidden robustness review.
  - - `validation/narratives/renderer_readiness_decision_gate.md` — Phase 1.19 blocker taxonomy and anti-death-spiral doctrine.
  - - `ai_context/archaeology/RAW_CONTINUITY_VOLUME_7.md` — canonical continuity volume container for this phase.
  - - `memory_archaeology_raw/README.md` — raw intake rules.

### A.12 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 206
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Constitutional signals:
  - # AI Interpretation Truthfulness Doctrine v1
  - **CANONICAL** for **future** AI-assisted interpretation layers — not current product scope.
  - **Scope:** Documentation only. Defines interpretive discipline, forbidden patterns, and a future review architecture. **No AI implementation in dumb Web 2.0 v1.**
  - - `docs/ai_constitution_and_review_architecture.md` — layered governance, anti-patterns, reviewer duties
  - - `docs/constitutional/epistemic_integrity_and_symbolic_humility.md` — honest uncertainty, symbolic restraint

### A.13 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai_constitution_and_review_architecture.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 13119; SHA-12: `d6ae8f16c65e`; score: 142
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Constitutional signals:
  - # AI constitution and review architecture
  - **Status:** Internal **governance architecture** for future AI-assisted interpretation—not a shipping spec, not marketing, not ethics theater.
  - **Doctrine stack (read before changing AI behavior):**
  - - **`docs/intentionality_and_symbolic_constraints.md`** — fate/agency, tradeoffs, intentionality, AI governance implications.
  - - **`docs/brand_and_experience_foundations.md`** — **Interpretive language and emotional transparency**; **Interpretive integrity and archetypal honesty**; emotionally **non-interfering** design.

### A.14 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/client_chart_data_model_v1_2026-05-29.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 35789; SHA-12: `795365723409`; score: 176
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Constitutional signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - - how behavioral facts may be captured **without interpretation**,

### A.15 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 20953; SHA-12: `db53e1e91227`; score: 87
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Constitutional signals:
  - **ARCHITECTURE REVIEW — aligned with Map-First Product Doctrine (2026-05-31)**
  - **Date:** 2026-05-29 (original); **doctrine alignment:** 2026-05-31
  - **Governing doctrine:** `docs/constitutional/map_first_product_doctrine_v1.md` — supersedes dashboard-centric recommendations in v1.0–v1.1 of this review.
  - - `docs/architecture/client_chart_data_model_v1_2026-05-29.md` (data ownership authority)
  - - `docs/ux/2026-05-29_application_journey_architecture_v1.md` (screen/journey authority)

### A.16 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/aspect_aura_defaults.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, future_policy_domains
- Characters: 1291; SHA-12: `2e467a76fee6`; score: 1
- Key headings: Aspect aura defaults (approximate display); Authority; Default screen weights (Leaflet `weight`, approximate); NOT done here
- Constitutional signals:
  - ## Authority
  - - No latitude-aware geographic σ for aura width (future refinement).

### A.17 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/brand_and_experience_foundations.md`
- Categories: epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 114
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Constitutional signals:
  - **What this is not:** A brand book, logo spec, marketing narrative, campaign, or visual identity system. **No** speculative public branding.
  - **Important:** The emotional and atmospheric goals below are **experiential design constraints**—they govern how future UX and rendering choices should **feel** and **function**. They are **not** marketing fluff; they are institutional memory for product judgment.
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).
  - - **Warm, safe containment:** The environment should feel like a **warm blanket** or **safe, contemplative room**—**breathable, calm, trustworthy, spacious, emotionally safe**—so users can **inhabit** it comfortably for **hours**.
  - - **Long sessions without fatigue:** Typography, color restraint, spacing, and low noise support **sustained** exploratory use; the product should feel like a **home** for serious play, not a sprint through a flashy demo.

### A.18 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/cartographic_language_and_city_rendering.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 18608; SHA-12: `33b4db97eb55`; score: 44
- Key headings: Cartographic language and city rendering; 0. Basemap or tile strategy change ⇒ full visual identity re-test; 1. Map label language vs app language; 2. Provider evaluation (map + search); 2.1 Dimensions to score (required for any serious comparison); 2.2 Qualitative stack comparison (high level); 2.3 “Extra hour” vs “multi-day / multi-week”; 2.4 Effort bands for “whole solution” slices; 2.5 GeoNames bridge first vs “long-term now”; 3. City visibility under overlays (hard constraint); 4. City density and ranking (rendering); 5. Clickability: city vs blank map
- Constitutional signals:
  - **Status:** Planning and constraints for **basemap language**, **city visibility**, and **interaction clarity**. Complements `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, and `docs/map_and_overlay_design_research.md`.
  - **Out of scope:** Aspect-to-angle **glow/aura** (not implemented; do not conflate with city-layer work).
  - **Institutional rule:** If the team changes **map provider**, **tile format** (raster → vector, host swap, style swap), or **label policy**, we must **re-validate the whole visual system**—not assume the current look “carries over.”
  - | **City readability** | Label collision, halo, and density differ; custom markers may need new stroke/fill against new tiles. |
  - | **Light / dark theme** | **Do not** assume one overlay palette works; plan **paired tokens** when dark mode is real. |

### A.19 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/README.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 65
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Constitutional signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - layer sovereignty,
  - - truth integrity,
  - - symbolic humility,

### A.20 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ai_conversational_modes.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 2887; SHA-12: `b796e2065486`; score: 37
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Constitutional signals:
  - # AI Conversational Modes
  - This document contains a mixture of:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - and deferred implementation ideas.

### A.21 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/constitutional_ingestion_checklist.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 57
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Constitutional signals:
  - # Constitutional Ingestion Checklist
  - - track doctrine ingestion,
  - Update this document whenever:
  - - new constitutional docs are added,
  - - doctrine evolves,

### A.22 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/conversational_discovery_and_intentionality.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 4218; SHA-12: `c7b5d8b9fc8e`; score: 30
- Key headings: Conversational Discovery And Intentionality; Status; Purpose; Core Principle; User intentionality is sovereign.; Intentionality Discovery; Examples; Archetypal Exploration; Example Exploratory Style; Intentionality Strength; Examples; Layer Relationship
- Constitutional signals:
  - The principles of:
  - remain exploratory and subject to iteration.
  - # Core Principle
  - The system must:
  - - "I can't raise capital."

### A.23 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/epistemic_integrity_and_symbolic_humility.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 3739; SHA-12: `242cc62cfae5`; score: 53
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior; Good Behavior; Collaborative Discovery
- Constitutional signals:
  - # Epistemic Integrity And Symbolic Humility
  - - epistemic behavior,
  - - uncertainty handling,
  - - symbolic humility,
  - - and anti-bullshit doctrine.

### A.24 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/future_excellence_vs_future_feature_excellence.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 34
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Constitutional signals:
  - # Future Excellence vs Future Feature Excellence
  - This document contains:
  - - canonical architectural principles,
  - - future-oriented planning,
  - # Maintenance Notes

### A.25 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/implementation_governance_and_ai_workflow_protocol.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3988; SHA-12: `b127e5c52050`; score: 42
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Constitutional signals:
  - # Implementation Governance And AI Workflow Protocol
  - - AI workflow behavior,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - - constitutionally governed development.

### A.26 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer4_optimization_and_exploration_doctrine.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 4341; SHA-12: `289b4552320f`; score: 36
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Constitutional signals:
  - # Layer 4 Optimization And Exploration Doctrine
  - This document contains:
  - - canonical Layer 4 principles,
  - - and future-facing interaction concepts.
  - Advanced optimization behaviors remain exploratory and subject to refinement.

### A.27 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer_sovereignty_and_forbidden_crossings.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 72
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Constitutional signals:
  - # Layer Sovereignty And Forbidden Crossings
  - It defines hard constitutional boundaries between layers.
  - These rules are mandatory architectural constraints.
  - - layer sovereignty,
  - - forbidden crossings,

### A.28 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layered_symbolic_intelligence_architecture.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 4801; SHA-12: `5242de0598f3`; score: 59
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Constitutional signals:
  - It defines the constitutional layer architecture of the platform.
  - All future systems must respect:
  - - layer sovereignty,
  - - forbidden crossings,
  - - and truth integrity.

### A.29 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/map_first_product_doctrine_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 47
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Constitutional signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.

### A.30 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/mvp_beta_and_future_feature_roadmap.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 4767; SHA-12: `c904d8af5d1e`; score: 51
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes; Stage 2 — Professional Beta; Goal
- Constitutional signals:
  - # MVP, Beta, And Future Feature Roadmap
  - This document contains:
  - - and future feature concepts.
  - not immutable constitutional doctrine.
  - # Maintenance Notes

### A.31 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 51
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Constitutional signals:
  - This document contains a mixture of:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - and deferred implementation ideas.
  - - prevent future contradictions,

### A.32 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_mode_vs_lay_mode_strategy.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 3492; SHA-12: `c166907d611f`; score: 60
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Constitutional signals:
  - This document contains:
  - - and future product direction.
  - Core principles are canonical.
  - Specific implementations remain exploratory.
  - # Maintenance Notes

### A.33 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_trust_and_ai_behavior_doctrine.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 89
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Constitutional signals:
  - # Professional Trust And AI Behavior Doctrine
  - This document defines how AI systems inside the platform must behave.
  - - epistemic integrity,
  - - symbolic restraint,
  - The AI must never behave like:

### A.34 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/purification_audit_framework.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3639; SHA-12: `a43528565790`; score: 69
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Constitutional signals:
  - - architectural integrity checks,
  - Purification audits are mandatory maintenance mechanisms.
  - - or violate constitutional doctrine.
  - - preserve architectural integrity,
  - # Core Principle

### A.35 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/relocation_strategy_framework.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 2978; SHA-12: `5542c6b3c8b9`; score: 15
- Key headings: Relocation Strategy Framework; Status; Purpose; Core Principle; Subtractive relocation comes before additive optimization.; Subtractive Relocation; Additive Relocation; Strong Relocations Often Do Both; Tradeoff Reality; Archetypes Are Contextual; Optimization Delusion; Layer 4 Behavior
- Constitutional signals:
  - This document contains a mixture of:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - and deferred implementation ideas.
  - - prevent future contradictions,

### A.36 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_and_renderer_sovereignty.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance
- Characters: 3826; SHA-12: `edda50b52a22`; score: 67
- Key headings: Runtime And Renderer Sovereignty; Purpose; Core Principle; Rendering must never alter truth.; Runtime Sovereignty; Renderer Sovereignty; Hydration Boundaries; Sandbox Boundaries; Observer Limitations; Renderer Substrate Integrity; Progressive Refinement; Ambiguity And Implication
- Constitutional signals:
  - # Runtime And Renderer Sovereignty
  - - runtime sovereignty,
  - - renderer sovereignty,
  - # Core Principle
  - ## Rendering must never alter truth.

### A.37 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_build_sequence_and_timeline.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 4934; SHA-12: `12aea4343437`; score: 47
- Key headings: Runtime Build Sequence And Timeline; Status; Maintenance Notes; Purpose; Core Principle; Build irreversible foundations first.; Phase Family 1 — Truth And Runtime Foundation; Goal; Includes; Status; Phase Family 2 — Renderer Reintegration; Goal
- Constitutional signals:
  - This document contains:
  - not immutable doctrine.
  - # Maintenance Notes
  - - AI layering,
  - - and future expansion.

### A.38 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/symbolic_language_style_guide.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits
- Characters: 1703; SHA-12: `11e6dd9bdb1a`; score: 21
- Key headings: Symbolic Language Style Guide; Purpose; Core Principle; Preferred Style; Avoid; Good Examples; Bad Examples; Archetypal Precision; Symbolic Humility; Constitutional Goal
- Constitutional signals:
  - # Core Principle
  - - or fake-certain.
  - - manipulative certainty,
  - - and fake spiritual authority.
  - The AI should discuss:

### A.39 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 3360; SHA-12: `554add110fa4`; score: 51
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Constitutional signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - - epistemic collapse,
  - - false certainty,
  - Truth belongs primarily to Layer 1.

### A.40 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_app_shell_handoff_audit_v1_2026-05-30.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 16528; SHA-12: `a7754235e25c`; score: 33
- Key headings: Genie → App Shell Handoff Audit v1; Status; Executive summary; A. Current Genie contract; Emitter; Trigger; Payload shape (as implemented); Variable semantics (canonical); Output destinations today; Not emitted / not connected; B. Current app shell contract; Navigation context (in-app)
- Constitutional signals:
  - **Partially superseded:** commit `9e448e0` added hook-only map execution (`__rmExecuteGenieRender`). Sections on **app shell handoff** and **Genie → shell transport** remain accurate. Sections claiming map has **no** Genie path are updated below.
  - **Three distinct states (do not conflate):**
  - There is **zero wired handoff** between Genie and app shell, or between shell navigation and automatic Genie search on map load. `legacyCompatibility` is emitted for diagnostics; map engine adapter **must not** use it as execution input.
  - | Search truth | `complete` and `experimental` variables with `enabled: true` |
  - ### Search / render truth (default user path)

### A.41 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_render_payload_v1_2026-05-30.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 27674; SHA-12: `7e997018eed9`; score: 74
- Key headings: Genie Render Payload Contract v1; Status; Purpose; Architectural doctrine; Language stability doctrine; Principles; Therefore; Top-level payload; Field notes; Render immutability; Future references (not defined here); Variable object
- Constitutional signals:
  - **Scope:** Documentation / contract only. Defines shape, semantics, legacy adapter rules, and examples. Not implementation.
  - Define the **canonical, immutable snapshot** produced at Genie render time. This payload is the **search truth** handed to the map workspace, history, pin, and (later) save flows.
  - The Genie editor may hold **live, mutable card state**. Render freezes that state once. Downstream systems must treat the rendered payload as authoritative for “what was searched,” not the live card DOM.
  - # Architectural doctrine
  - | Rule | Meaning |

### A.42 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/variable_card_language_v1_2026-05-30.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 15184; SHA-12: `bde701502163`; score: 53
- Key headings: Variable Card Language Contract v1; Status; Purpose; Core doctrine; Canonical internal type IDs; Language registry concept; Composition rule; Registry ownership; Snapshot rule (Saved Explorations); Beta display label candidates; `planet_in_house`; `angle_in_sign`
- Constitutional signals:
  - - `docs/contracts/genie_render_payload_v1_2026-05-30.md` — stable type ids, `variables[].label` snapshots, language stability doctrine
  - - Saved Explorations remain readable when category labels change
  - # Core doctrine
  - | Principle | Meaning |
  - | **Stable IDs are canonical** | `planet_in_house`, registry ids (`sun`, `ASC`, `trine`), and payload fields are the source of truth — never derived from display strings. |

### A.43 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/current_sidebar_ux_audit.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 4992; SHA-12: `c07666b5828f`; score: 8
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces; 9. Condition model — **next structural UX step (documented)**; 10. Location search placement (documented)
- Constitutional signals:
  - - Earlier passes used extra `<br>` / `hr` slack; **paired selects** and **compact first section** reduced scroll.
  - - Three **planet-in-house** blocks remain **hardcoded A/B/C** (see §Condition model—next structural step).
  - - Section titles + tinted cards improve scan; **design system** still deferred.
  - **Engineering note:** needs coordinated **API/payload** and validation work later—**do not** half-migrate UI alone.
  - ## 11. First-use onboarding (implemented + future)

### A.44 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/local_first_data_objects_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 8758; SHA-12: `90256838acac`; score: 59
- Key headings: Local-First Data Objects v1; Status; Purpose; Architectural boundary; Entity glossary; ProfessionalAccount; Client; BirthProfile; RelocatedChart (future durable object); Place; FavoriteCity; OverlayCondition
- Constitutional signals:
  - Defines **product-layer entities**, **persistence boundaries**, and **local-first scaffold rules**. Not a database schema. Not implementation.
  - **Reads with:** `docs/relocation_app_product_roadmap.md` §8 (Saved Object Taxonomy, Phase 2.x), `docs/geocoder_and_city_identity_strategy.md`, `docs/constitutional/runtime_and_renderer_sovereignty.md`, `docs/product_workflows/professional_non_ai_workflow_v1.md`.
  - - renderer output becoming durable truth,
  - ## Architectural boundary
  - │  PRODUCT RECORDS (local-first → future sync)            │

### A.45 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/local_product_store_v2.md`
- Categories: epistemic_integrity, moral_data_use_limits, validation_governance, future_policy_domains
- Characters: 2604; SHA-12: `0fee91b48aed`; score: 10
- Key headings: Local Product Store v2; Status; Purpose; File location; Python module; Validation rules; Scripts; Explicit non-goals (Phase 3.0a); Rollback; Revision
- Constitutional signals:
  - Runtime smokes write to **temp paths** only. Do not promote this file to product storage without explicit migration approval.
  - | `validate_store(state)` | Structural + forbidden-key checks |
  - ## Validation rules
  - - `_storage` must be `TEMPORARY_LOCAL_SCAFFOLD`
  - - `storage_schema_version` must be `2`

### A.46 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/supabase_schema_sandbox_plan_v1.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 16155; SHA-12: `8fac31540a5b`; score: 58
- Key headings: Supabase Schema Sandbox Plan v1; Status; Explicit non-goals (current phase); Architectural boundary; 1. Proposed table list; 2. Columns per table; `professional_accounts`; `clients`; `birth_profiles`; `places`; `saved_charts`; `saved_investigations`
- Constitutional signals:
  - **Reads with:** `docs/data_model/local_first_data_objects_v1.md`, `docs/future/birth_time_uncertainty_and_confidence_doctrine.md`, `validation/narratives/phase2_3_saved_investigation_replay.md`, `library/library.json` (legacy scaffold).
  - Supabase is a **schema mirror / future sync target** only.
  - ## Architectural boundary
  - │  PRODUCT RECORDS (local-first → future Supabase sync)   │
  - │  RENDERER / DISPLAY (never persisted as truth)          │

### A.47 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/design/brand_visual_language_and_design_doctrine.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 52
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Constitutional signals:
  - # Brand, Visual Language, and Design Doctrine
  - Consolidates **brand foundations**, **visual epistemology**, and **restrained premium language** for the professional non-AI MVP. Not a logo guide. Not marketing.
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - - calm, restrained, inspectable, premium, trustworthy, professional.
  - - mystical rainbow dashboard,

### A.48 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 66
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Constitutional signals:
  - # Birth Time Uncertainty and Confidence Doctrine
  - Defines **epistemic tiers**, **user-facing honesty**, **data recording**, and **engine behavior boundaries** for uncertain birth times. Not implementation. Not rectification software spec.
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `validation/narratives…
  - Birth time uncertainty is **product-critical** for relocation work:
  - - AI intake may help later — **MVP must handle tiers without AI**.

### A.49 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/layer5_experiential_education_through_travel_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 50
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Constitutional signals:
  - **FUTURE ONLY — QUARANTINED**
  - **Not MVP. Not beta. Not current roadmap. Not AI intake. Not dashboard design. Not map UX. Not implementation planning.**
  - This document preserves a **post-AI product vision** for experiential education. It exists so the idea is not lost and is not accidentally folded into near-term scope.
  - **Dependency:** Requires mature AI guidance, relocation exploration substrate, and user observation capture — **after** standalone Web 2.0 facts-first product is proven.
  - **Reads with (boundary context only):** `docs/ux/2026-05-29_application_journey_architecture_v1.md` §Future Rooms, `docs/constitutional/layer_sovereignty_and_forbidden_crossings.md`.

### A.50 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_and_city_identity_strategy.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 28
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Constitutional signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - **Related:** `memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `docs/geocoder_dataset_feasibility.md`, `docs/cartographic_language_and_city_rendering.md` (basemap change ⇒ **§0** full visual re-test), `docs/relocation_app_product_roadmap.md` §7–8, `docs/m…
  - ## 1. Doctrine: city search is core systems engineering
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`). The map binds **h…
  - Current prototype list search (`cities.js`) is a **stand-in** only: **name, lat/lng, population (and minimal fields)**—**no reliable country/admin**, **no alternate names**, **no stable place IDs**, and **no** trustworthy global ranking (e.g. Paris, France vs Paris, Texas; London…

### A.51 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_dataset_feasibility.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance
- Characters: 16429; SHA-12: `6ba544bcfafd`; score: 27
- Key headings: Geocoder dataset feasibility (planning pass); 1. Summary recommendation; 2. Option-by-option evaluation; 2.1 GeoNames — `cities500` / `cities1000` / `allCountries`; 2.2 Natural Earth — populated places (`ne_10m_populated_places`); 2.3 Who’s On First (WOF); 2.4 Pelias / Geocode Earth (open-data stack vs hosted); 2.5 Mapbox / Google (hosted geocoding & Places); 3. Licensing notes (high level — verify before ship); 4. Rough import plan (GeoNames-first); 5. Data fields needed (canonical `Place` record); 6. Proposed ranking formula (v1 — heuristic, explainable)
- Constitutional signals:
  - **Companion docs:** `docs/cartographic_language_and_city_rendering.md`, `docs/next_implementation_sequence.md` (Priority band 4), `validation/narratives/city_data_and_search_notes.md`.
  - | **allCountries** | Full gazetteer | **All feature classes** (terrain, streams, …)—**not** a drop-in “city list”; use only if you explicitly need non-PPL features or will **filter heavily** by `feature class` / `feature code`. |
  - - **`asciiname` + `alternatenames`** on the main row; **full i18n / historic / preferred flags** in **`alternateNamesV2.zip`** (`isHistoric`, `isPreferredName`, `isolanguage`, etc.).
  - - **Daily delta files** (`modifications-*.txt`, etc.) support **incremental refresh** for offline caches.
  - **London vs Londonderry / Paris / Atlanta / Albany:** GeoNames gives **distinct rows** with different IDs and **country/admin**; failures are usually **search/ranking bugs**, not missing rows. Substring bugs are fixed in **application ranking + tokenization**, not by swapping dat…

### A.52 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/governance/anti_cursor_bullshit_governance_rules.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 75
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Constitutional signals:
  - # Anti-Cursor Bullshit Governance Rules
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountability_failure_audit.md` …
  - Cursor and other AI agents are **accelerators**, not authorities.
  - This project assumes **low trust in AI outputs until proven**.

### A.53 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_memory_synthesis.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 16257; SHA-12: `04f378dc370d`; score: 137
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Constitutional signals:
  - This document bridges **raw multi-chat archaeology** into **project-maintained memory**. It uses explicit status labels:
  - - **Implemented (repo):** verified or strongly evidenced in the current codebase / current milestone docs in this repository.
  - - **Roadmap:** intentional next-direction supported by archaeology and/or roadmap docs, not claimed shipped.
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.

### A.54 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_philosophical_synthesis.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 219
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Constitutional signals:
  - **Status:** Foundational doctrine for **future training**, **reviewer systems**, **UX design**, **product strategy**, **conversational architecture**, and **interpretive governance**.
  - **Authority:** Synthesizes durable texts in `ai_context/`, `docs/`, and `memory_archaeology_raw/consolidated_notes/`. It **does not** supersede those sources on technical implementation; it **weaves** them into one training-readable whole.
  - The relocation astrology platform is built on a paradox that mature users already live inside: **structure is real, and agency is real**. The chart is treated as **structurally real** for product purposes—not as an infinitely rewriteable “vibe,” not as a story generator that owes…
  - This posture has a deliberate audience: **astrology for grownups**—intellectually serious, skepticism-friendly, **sober without cynicism**. Warmth is expressed through **restraint**, not through neon spiritual retail. Excitement is expected to arise from **exploration and judgmen…
  - Underneath lies a technical moral that keeps philosophy honest: **inspectable precision**. If the map shows a region or line, it must mean something **precise** in the relocated model. “Plausible-looking geometry” is not validation. **False membership** is rejected even when cosm…

### A.55 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/intentionality_and_symbolic_constraints.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 8365; SHA-12: `d1c233003983`; score: 76
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Constitutional signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**
  - - **`docs/brand_and_experience_foundations.md`** — especially **“Interpretive integrity and archetypal honesty”** and **“Interpretive language and emotional transparency.”**

### A.56 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/local_archive_policy.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 1554; SHA-12: `5f3f7178bbfa`; score: 7
- Key headings: Local Archive Policy; Archive/Junk Drawer Candidates; Do Not Commit; Rule Of Thumb
- Constitutional signals:
  - Use archive folders for materials that explain product or technical decisions:
  - - Failed experiments that may teach something later.
  - - Temporary validation outputs worth keeping for proof-of-work.
  - - Notes explaining abandoned approaches.
  - - `archive_failed_approaches/`

### A.57 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/map_and_overlay_design_research.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 5149; SHA-12: `f3943cdf7cf9`; score: 15
- Key headings: Map and Overlay Design Research; 1. Leaflet vs MapLibre vs Google Maps (philosophical comparison); 2. Current Leaflet strengths (for this codebase); 3. Actual blockers to watch for (hypothesis list—not confirmed); 4. Overlay transparency strategy (research directions); 5. Semantic overlap colors; 6. Aura rendering directions (non-commitments); 7. Map-edge and world-wrap ideas; 8. Dark / light mode implications; 9. Multilingual city rendering; 10. Decision rule (when to reopen migration); Related docs
- Constitutional signals:
  - **Planning and research only.** No map migration is prescribed here. The project **stays on Leaflet for MVP** unless concrete blockers emerge (`ai_context/decisions.md`, `current_state.md`).
  - | **Fit for this product** | Strong when overlays are **GeoJSON + careful projection/wrap discipline** and the team values **direct control** over truth vs display separation. | Strong if **vector basemaps**, **pitch**, **client-side style**, or **dense label collision** become c…
  - | **Non-technical cost** | You maintain more glue (wrap, performance quirks). | Investment in style JSON, shader-era debugging. | Billing, keys, usage caps, compliance narrative. |
  - - **Lower migration tax** while overlay **truth** and **overlap readability** are still evolving—**avoid rewriting two crises at once**.
  - Treat as **migration triggers only when evidenced**:

### A.58 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/next_implementation_sequence.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 10690; SHA-12: `ced0e563c90b`; score: 69
- Key headings: Next Implementation Sequence; Priority band 1 — UX polish (minimal architecture risk); Chunk 1.1 — Sidebar density and “debug vs ship” clarity; Chunk 1.2 — Popup and typography refinement; Chunk 1.3 — Native select stability + legend clutter reduction; Priority band 2 — Validator / stress tooling; Chunk 2.1 — Fixture manifest + “run these five” script; Chunk 2.2 — Latitude / polar stress suite expansion; Chunk 2.3 — Brute-force / truth export hygiene; Priority band 3 — Account + birth-data workflows; Chunk 3.1 — Birth data model (local-only MVP); Chunk 3.2 — Chart list + “open on map”
- Constitutional signals:
  - **Reference:** `ai_context/current_state.md`, `docs/relocation_app_product_roadmap.md`, `ai_context/open_questions.md`.
  - - **Validation:** Visual pass; confirm map remains primary; no regression on popup/dropdown behavior.
  - - **Do not overengineer:** No new framework, no drawer rewrite here—**incremental compression** only.
  - - **Why:** Popup is diagnostic truth; typography should match premium, calm instrument tone.
  - - **Validation:** Side-by-side screenshots; high-north / southern fixtures; dateline popups unchanged logically.

### A.59 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/00_OPERATOR_START_HERE.md`
- Categories: symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance
- Characters: 697; SHA-12: `a0e79ddfcf29`; score: 4
- Key headings: AI Onboarding Entry Point
- Constitutional signals:
  - # AI Onboarding Entry Point
  - 1. 01_ai_product_core
  - Primary historical failure modes:
  - - oracle behavior
  - - repeating doctrine without understanding doctrine

### A.60 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 185
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Constitutional signals:
  - **CANONICAL** for non-AI application UX architecture (Web 2.0 standalone product).
  - **Scope:** User journey, screen responsibilities, mood states, and control architecture for the **dumb version** — facts-first exploration without AI dependency.
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doct…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.

### A.61 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 157
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Constitutional signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…

### A.62 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/README.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 65
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Constitutional signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - layer sovereignty,
  - - truth integrity,
  - - symbolic humility,

### A.63 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 121
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Constitutional signals:
  - # UX Constitution
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - - the authority when UX behavior is ambiguous
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.

### A.64 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 252
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Constitutional signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.65 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 35789; SHA-12: `795365723409`; score: 176
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Constitutional signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - - how behavioral facts may be captured **without interpretation**,

### A.66 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 8365; SHA-12: `d1c233003983`; score: 76
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Constitutional signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**
  - - **`docs/brand_and_experience_foundations.md`** — especially **“Interpretive integrity and archetypal honesty”** and **“Interpretive language and emotional transparency.”**

### A.67 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 47
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Constitutional signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.

### A.68 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 50
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Constitutional signals:
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.
  - **Must not contain:** activity feeds, recents, owner hero cards, favorites, charts, map as primary surface, widgets, metrics.

### A.69 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9566; SHA-12: `3de8663545ba`; score: 79
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Constitutional signals:
  - # Professional Non-AI Workflow v1
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - AI is **absent or explicitly off**,

### A.70 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 3360; SHA-12: `554add110fa4`; score: 51
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Constitutional signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - - epistemic collapse,
  - - false certainty,
  - Truth belongs primarily to Layer 1.

### A.71 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/DOCTRINE_INDEX.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 157
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Constitutional signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…

### A.72 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/README.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 65
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Constitutional signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - layer sovereignty,
  - - truth integrity,
  - - symbolic humility,

### A.73 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_CONSTITUTION.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 121
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Constitutional signals:
  - # UX Constitution
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - - the authority when UX behavior is ambiguous
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.

### A.74 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_DOCTRINE_MASTER.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 252
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Constitutional signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.75 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/constitutional_summary.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance
- Characters: 4609; SHA-12: `8238f401edb1`; score: 83
- Key headings: Constitutional Summary; Purpose; Layer Architecture; Layer 1 - Truth; Layer 2 - Symbolic Ontology; Layer 3 - Intentional Interpretation; Layer 4 - Exploratory Optimization; Forbidden Crossings; Epistemic Doctrine; Runtime And Renderer Sovereignty; Purification Principle; Professional Trust And AI Behavior
- Constitutional signals:
  - # Constitutional Summary
  - Read this first in new AI sessions. It is a compact bootstrap summary, not a replacement for the full constitutional documents in `docs/constitutional/`.
  - The Relocation App is a layered symbolic intelligence platform. It is not a monolithic astrology chatbot, hidden recommendation engine, or mystical certainty machine.
  - ## Layer 1 - Truth
  - Layer 1 owns astronomical and geometric truth:

### A.76 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/epistemic_integrity_and_symbolic_humility.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 3739; SHA-12: `242cc62cfae5`; score: 53
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior; Good Behavior; Collaborative Discovery
- Constitutional signals:
  - # Epistemic Integrity And Symbolic Humility
  - - epistemic behavior,
  - - uncertainty handling,
  - - symbolic humility,
  - - and anti-bullshit doctrine.

### A.77 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/intentionality_and_symbolic_constraints.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 8365; SHA-12: `d1c233003983`; score: 76
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Constitutional signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**
  - - **`docs/brand_and_experience_foundations.md`** — especially **“Interpretive integrity and archetypal honesty”** and **“Interpretive language and emotional transparency.”**

### A.78 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layer_sovereignty_and_forbidden_crossings.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 72
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Constitutional signals:
  - # Layer Sovereignty And Forbidden Crossings
  - It defines hard constitutional boundaries between layers.
  - These rules are mandatory architectural constraints.
  - - layer sovereignty,
  - - forbidden crossings,

### A.79 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layered_symbolic_intelligence_architecture.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 4801; SHA-12: `5242de0598f3`; score: 59
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Constitutional signals:
  - It defines the constitutional layer architecture of the platform.
  - All future systems must respect:
  - - layer sovereignty,
  - - forbidden crossings,
  - - and truth integrity.

### A.80 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/map_first_product_doctrine_v1.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 47
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Constitutional signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.

### A.81 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 3360; SHA-12: `554add110fa4`; score: 51
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Constitutional signals:
  - # Truth vs Astrological Fact vs Interpretation
  - - Interpretation
  - - epistemic collapse,
  - - false certainty,
  - Truth belongs primarily to Layer 1.

### A.82 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/2026-05-29_application_journey_architecture_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 185
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Constitutional signals:
  - **CANONICAL** for non-AI application UX architecture (Web 2.0 standalone product).
  - **Scope:** User journey, screen responsibilities, mood states, and control architecture for the **dumb version** — facts-first exploration without AI dependency.
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doct…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.

### A.83 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/PLAIN_LANGUAGE_PRODUCT_EXPLANATION_v1_2026-06-01.md`
- Categories: constitutional_anchor, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, validation_governance
- Characters: 6093; SHA-12: `0c7a9042f0a5`; score: 23
- Key headings: Plain Language Product Explanation; What Problem Does The Product Solve?; Why Relocation Astrology Is Geographic; Why The Map Is The Primary Discovery Instrument; What Overlays Represent; Why Cities Are Not The Primary Object Of Analysis; Natal Chart; Current Location Chart; Candidate Location Chart; Favorites; Saved Searches; Comparison
- Constitutional signals:
  - # Plain Language Product Explanation
  - This document explains the relocation astrology platform in ordinary language.
  - Rankings create false certainty.
  - ## Objective Fact Versus Interpretation
  - Interpretation begins after those facts.

### A.84 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_constitution_and_review_architecture.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 13121; SHA-12: `96b9567947d8`; score: 142
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Constitutional signals:
  - # AI constitution and review architecture
  - **Status:** Internal **governance architecture** for future AI-assisted interpretation—not a shipping spec, not marketing, not ethics theater.
  - **Doctrine stack (read before changing AI behavior):**
  - - **`docs/intentionality_and_symbolic_constraints.md`** — fate/agency, tradeoffs, intentionality, AI governance implications.
  - - **`docs/brand_and_experience_foundations.md`** — **Interpretive language and emotional transparency**; **Interpretive integrity and archetypal honesty**; emotionally **non-interfering** design.

### A.85 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 206
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Constitutional signals:
  - # AI Interpretation Truthfulness Doctrine v1
  - **CANONICAL** for **future** AI-assisted interpretation layers — not current product scope.
  - **Scope:** Documentation only. Defines interpretive discipline, forbidden patterns, and a future review architecture. **No AI implementation in dumb Web 2.0 v1.**
  - - `docs/ai_constitution_and_review_architecture.md` — layered governance, anti-patterns, reviewer duties
  - - `docs/constitutional/epistemic_integrity_and_symbolic_humility.md` — honest uncertainty, symbolic restraint

### A.86 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 66
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Constitutional signals:
  - # Birth Time Uncertainty and Confidence Doctrine
  - Defines **epistemic tiers**, **user-facing honesty**, **data recording**, and **engine behavior boundaries** for uncertain birth times. Not implementation. Not rectification software spec.
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `validation/narratives…
  - Birth time uncertainty is **product-critical** for relocation work:
  - - AI intake may help later — **MVP must handle tiers without AI**.

### A.87 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_and_experience_foundations.md`
- Categories: epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 114
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Constitutional signals:
  - **What this is not:** A brand book, logo spec, marketing narrative, campaign, or visual identity system. **No** speculative public branding.
  - **Important:** The emotional and atmospheric goals below are **experiential design constraints**—they govern how future UX and rendering choices should **feel** and **function**. They are **not** marketing fluff; they are institutional memory for product judgment.
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).
  - - **Warm, safe containment:** The environment should feel like a **warm blanket** or **safe, contemplative room**—**breathable, calm, trustworthy, spacious, emotionally safe**—so users can **inhabit** it comfortably for **hours**.
  - - **Long sessions without fatigue:** Typography, color restraint, spacing, and low noise support **sustained** exploratory use; the product should feel like a **home** for serious play, not a sprint through a flashy demo.

### A.88 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_visual_language_and_design_doctrine.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 52
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Constitutional signals:
  - # Brand, Visual Language, and Design Doctrine
  - Consolidates **brand foundations**, **visual epistemology**, and **restrained premium language** for the professional non-AI MVP. Not a logo guide. Not marketing.
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - - calm, restrained, inspectable, premium, trustworthy, professional.
  - - mystical rainbow dashboard,

### A.89 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/client_chart_data_model_v1_2026-05-29.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 35789; SHA-12: `795365723409`; score: 176
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Constitutional signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - - how behavioral facts may be captured **without interpretation**,

### A.90 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/conversational_discovery_and_intentionality.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 4218; SHA-12: `c7b5d8b9fc8e`; score: 30
- Key headings: Conversational Discovery And Intentionality; Status; Purpose; Core Principle; User intentionality is sovereign.; Intentionality Discovery; Examples; Archetypal Exploration; Example Exploratory Style; Intentionality Strength; Examples; Layer Relationship
- Constitutional signals:
  - The principles of:
  - remain exploratory and subject to iteration.
  - # Core Principle
  - The system must:
  - - "I can't raise capital."

### A.91 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/core_product_truths.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9535; SHA-12: `9d9048f7cab4`; score: 97
- Key headings: Core Product Truths; Astrology Truth; Inspectability; Map and Overlay UX; Product Experience; Visual / Semantic Product Identity; Emotionally non-interfering design (experiential constraints); Interpretive language and emotional transparency (doctrine); Interpretive integrity and archetypal honesty (doctrine); Development Discipline; Where the nuanced history lives
- Constitutional signals:
  - # Core Product Truths
  - These are durable principles that should survive individual implementation chunks, UI experiments, and future chat transitions.
  - ## Astrology Truth
  - - Map overlays must agree with point-and-click astrology truth.
  - - Popup point-truth validation is authoritative for local membership checks.

### A.92 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/geocoder_and_city_identity_strategy.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 28
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Constitutional signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - **Related:** `memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `docs/geocoder_dataset_feasibility.md`, `docs/cartographic_language_and_city_rendering.md` (basemap change ⇒ **§0** full visual re-test), `docs/relocation_app_product_roadmap.md` §7–8, `docs/m…
  - ## 1. Doctrine: city search is core systems engineering
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`). The map binds **h…
  - Current prototype list search (`cities.js`) is a **stand-in** only: **name, lat/lng, population (and minimal fields)**—**no reliable country/admin**, **no alternate names**, **no stable place IDs**, and **no** trustworthy global ranking (e.g. Paris, France vs Paris, Texas; London…

### A.93 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/map_drawer_and_layer_control_doctrine.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 7226; SHA-12: `181a6ad8f6bd`; score: 40
- Key headings: Map Drawer and Layer Control Doctrine; Status; Purpose; Control hierarchy (map screen); Drawer architecture (target); Zones; Genie-into-corner collapse; Deferral (current phase); Condition editor doctrine; Target model; Card visual language; Search action
- Constitutional signals:
  - # Map Drawer and Layer Control Doctrine
  - **Reads with:** `docs/overlay_and_aura_visual_strategy.md` §H, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/visual_semantic_style_guide.md` §9, `docs/product_workflows/product_screen_and_transition_architecture.md`.
  - Keep the **map sacred**. Controls must:
  - Priority order — highest wins when space is constrained:
  - | 1 | **Map viewport** | full available area |

### A.94 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/product_screen_and_transition_architecture.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 50
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Constitutional signals:
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.
  - **Must not contain:** activity feeds, recents, owner hero cards, favorites, charts, map as primary surface, widgets, metrics.

### A.95 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_mode_vs_lay_mode_strategy.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 3492; SHA-12: `c166907d611f`; score: 60
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Constitutional signals:
  - This document contains:
  - - and future product direction.
  - Core principles are canonical.
  - Specific implementations remain exploratory.
  - # Maintenance Notes

### A.96 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_non_ai_workflow_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9566; SHA-12: `3de8663545ba`; score: 79
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Constitutional signals:
  - # Professional Non-AI Workflow v1
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - AI is **absent or explicitly off**,

### A.97 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_trust_and_ai_behavior_doctrine.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 89
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Constitutional signals:
  - # Professional Trust And AI Behavior Doctrine
  - This document defines how AI systems inside the platform must behave.
  - - epistemic integrity,
  - - symbolic restraint,
  - The AI must never behave like:

### A.98 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_workflow_and_explanatory_language.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 11541; SHA-12: `1814ff883a7c`; score: 75
- Key headings: Professional Workflow And Explanatory Language; Status; Purpose; Professional Map Workflow; Desired Placement Search; Exclude / NOT Variables; Solo And Mute Controls; Inspection Workflow; Helper Layers; Intention Remains Primary; Astro Assist Substitution Guidance; Additive And Subtractive Relocation
- Constitutional signals:
  - This is a living product-training and explanatory-language document.
  - It contains:
  - - future help text,
  - - and training/video outline candidates.
  - This is NOT constitutional doctrine.

### A.99 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/symbolic_language_style_guide.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits
- Characters: 1703; SHA-12: `11e6dd9bdb1a`; score: 21
- Key headings: Symbolic Language Style Guide; Purpose; Core Principle; Preferred Style; Avoid; Good Examples; Bad Examples; Archetypal Precision; Symbolic Humility; Constitutional Goal
- Constitutional signals:
  - # Core Principle
  - - or fake-certain.
  - - manipulative certainty,
  - - and fake spiritual authority.
  - The AI should discuss:

### A.100 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ux_principles_and_emotional_tone.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 4906; SHA-12: `3924025d2ba8`; score: 30
- Key headings: UX Principles and Emotional Tone; 1. Core temperament; 2. Map-first atmosphere; 3. Delight without spectacle; 4. Overlap readability philosophy; 5. Typography and color tone; 6. Layout cautions: drawer / genie / chrome; 7. Mobile and tablet; 8. When to stop designing; 9. Where philosophy is already strong in the repo; 10. Where philosophy could still drift; Related docs
- Constitutional signals:
  - # UX Principles and Emotional Tone
  - | Principle | Meaning |
  - | **Restraint** | Premium is **quiet**; confidence without shouting. No astrology hype aesthetic. |
  - | **Anti-overdesign** | No speculative chrome before map truth and readability are solid. |
  - - **Professional trustworthiness:** numbers, regions, and overlaps must **mean** something inspectable; visual polish never substitutes for false certainty.

### A.101 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/visual_semantic_style_guide.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9451; SHA-12: `93105f1b5ba9`; score: 49
- Key headings: Visual & Semantic Style Guide (Relocation Map System); 1. Visual epistemology (truth hierarchy); 2. House field semantics (categorical + cusp softness); 3. Aspect-to-angle aura semantics (intensity, not category); 4. Overlay texture semantics (almost subconscious); 5. NOT / exclusion overlays; 6. Color philosophy; 7. Popup visual language; 8. Interface tone; 9. Map and control relationship; 10. Account / chart page relationship; 11. Implementation discipline
- Constitutional signals:
  - **Status:** Planning and doctrine. This document defines **what visuals mean** and **how they should behave**. It does **not** mandate implementation order or ship dates.
  - **Companion docs:** `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/map_and_overlay_design_research.md`, `docs/brand_and_experience_foundations.md`, `docs/intentionality_and_symbolic_constraints.md` (fate/agency/tradeoffs), `docs/ai_c…
  - **Discipline:** Future rendering work should follow this guide so the product does not drift toward **debuggy/generic** UIs or **beautiful-but-unusable** spectacle.
  - ## 1. Visual epistemology (truth hierarchy)
  - | **Right-click / point popup** | **Canonical point truth** for the queried location | Authoritative for “what is true *here*” at that click (degrees, houses, etc.). |

### A.102 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ai_conversational_modes.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 2887; SHA-12: `b796e2065486`; score: 37
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Constitutional signals:
  - # AI Conversational Modes
  - This document contains a mixture of:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - and deferred implementation ideas.

### A.103 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/archaeology_and_synthesis_workflow.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9005; SHA-12: `d3add7674811`; score: 73
- Key headings: Archaeology and synthesis workflow; 1. Pipeline overview; 2. When to create an archaeology pass; 3. When to create or update synthesis docs; 4. Durable truths vs transient implementation; 5. How to avoid flattening nuance during synthesis; 6. Preserving contradictory but valuable tensions; 7. Doctrine canonicalization; 8. Open tension preservation; 9. Institutional memory updating (rhythm); 10. Governance refresh; 11. Review bundle generation
- Constitutional signals:
  - **Purpose:** Capture chat and session intelligence **without** flattening nuance, **without** treating the latest thread as law, and **without** losing rejected paths that explain pivots.
  - **Reads with:** `ai_context/memory_workflow.md`, `docs/institutional_memory_synthesis.md`, `docs/project_memory_taxonomy.md`, `docs/process/doctrine_review_cycle.md`.
  - Human merge remains authoritative. This workflow is **not** an autonomous agent pipeline.
  - Raw capture → themed synthesis → doctrine canonicalization → open tension preservation
  - → institutional memory update → governance refresh → review bundle → future rehydration

### A.104 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/decision_and_uncertainty_framework.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9068; SHA-12: `4b8f251dada4`; score: 75
- Key headings: Decision and uncertainty framework; 1. Bounded uncertainty; 2. Heuristic vs exact truth; 3. Symbolic plausibility vs fake precision; 4. Exploratory guidance vs deterministic recommendation; 5. Preserving ambiguity intentionally; 6. Reversible decisions; 7. Experimentation doctrine; 8. User-facing confidence vs backend uncertainty; 9. “Good enough for exploration” vs “authoritative truth”; 10. Case study: aura philosophy; 11. Visual approximation doctrine
- Constitutional signals:
  - # Decision and uncertainty framework
  - **Status:** Meta-governance — how the institution handles **uncertainty**, **ambiguity**, **heuristics**, and **judgment** without premature closure.
  - **Purpose:** Prevent fake precision, oracle UX, and tension-erasure while still allowing **fast exploration** and **reversible experiments**.
  - **Reads with:** `docs/visual_semantic_style_guide.md` §1, `docs/overlay_and_aura_visual_strategy.md` (aura doctrine), `docs/intentionality_and_symbolic_constraints.md`, `docs/process/doctrine_review_cycle.md`.
  - ## 1. Bounded uncertainty

### A.105 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/doctrine_review_cycle.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9902; SHA-12: `00598386986c`; score: 70
- Key headings: Doctrine review cycle; 1. What this cycle protects; 2. Slow docs policy; 3. Implementation vs philosophy separation; 4. Tension-preservation doctrine; 5. Rationale preservation rules (“why”, not just “what”); 6. Review cadences (suggested, not ceremonial); 6.1 Doctrine coherence review; 6.2 AI drift audit; 6.3 UX coherence review; 6.4 Archaeology / synthesis refresh; 6.5 Review bundle / external audit
- Constitutional signals:
  - # Doctrine review cycle
  - **Status:** Meta-governance — **institutional maintenance**, not product behavior.
  - **Purpose:** Periodic coherence maintenance so the project does not **silently drift**, **forget reasoning**, **flatten tensions**, or **confuse fast implementation with slow philosophy**.
  - **Reads with:** `docs/DOCTRINE_INDEX.md`, `docs/review_contracts_and_governance.md`, `docs/process/decision_and_uncertainty_framework.md`, `ai_context/memory_workflow.md`.
  - This is **not** bureaucracy. It is a **lightweight rhythm** for a long-lived symbolic instrument: enough structure that future contributors inherit **why**, not only **what**.

### A.106 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/future_excellence_vs_future_feature_excellence.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 34
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Constitutional signals:
  - # Future Excellence vs Future Feature Excellence
  - This document contains:
  - - canonical architectural principles,
  - - future-oriented planning,
  - # Maintenance Notes

### A.107 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer4_optimization_and_exploration_doctrine.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 4341; SHA-12: `289b4552320f`; score: 36
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Constitutional signals:
  - # Layer 4 Optimization And Exploration Doctrine
  - This document contains:
  - - canonical Layer 4 principles,
  - - and future-facing interaction concepts.
  - Advanced optimization behaviors remain exploratory and subject to refinement.

### A.108 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer5_experiential_education_through_travel_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 50
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Constitutional signals:
  - **FUTURE ONLY — QUARANTINED**
  - **Not MVP. Not beta. Not current roadmap. Not AI intake. Not dashboard design. Not map UX. Not implementation planning.**
  - This document preserves a **post-AI product vision** for experiential education. It exists so the idea is not lost and is not accidentally folded into near-term scope.
  - **Dependency:** Requires mature AI guidance, relocation exploration substrate, and user observation capture — **after** standalone Web 2.0 facts-first product is proven.
  - **Reads with (boundary context only):** `docs/ux/2026-05-29_application_journey_architecture_v1.md` §Future Rooms, `docs/constitutional/layer_sovereignty_and_forbidden_crossings.md`.

### A.109 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/local_archive_policy.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 1554; SHA-12: `5f3f7178bbfa`; score: 7
- Key headings: Local Archive Policy; Archive/Junk Drawer Candidates; Do Not Commit; Rule Of Thumb
- Constitutional signals:
  - Use archive folders for materials that explain product or technical decisions:
  - - Failed experiments that may teach something later.
  - - Temporary validation outputs worth keeping for proof-of-work.
  - - Notes explaining abandoned approaches.
  - - `archive_failed_approaches/`

### A.110 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/memory_workflow.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 6877; SHA-12: `0a90f034aa1f`; score: 29
- Key headings: Memory Maintenance Workflow; Purpose; Sources; Mining Old Chats; Processing Extraction Docs; Consolidating Raw Archaeology (optional phase); Updating Durable Memory; Memory Types; Raw Extraction; Durable Memory; Roadmap; Current Implementation State
- Constitutional signals:
  - # Memory Maintenance Workflow
  - This document explains how project memory should be maintained without turning old chats, reports, and speculative ideas into an unstructured pile.
  - The goal is durable continuity. Cursor and external reviewers should be able to understand the product direction, current state, and important constraints without rereading every past chat.
  - This workflow is not an autonomous agent system. The user remains the final editor and approver.
  - **Institutional map (broader pipeline):** `docs/process/archaeology_and_synthesis_workflow.md` — raw → synthesis → doctrine → review bundle → rehydration. **Cadence:** `docs/process/doctrine_review_cycle.md`.

### A.111 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/mvp_beta_and_future_feature_roadmap.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 4767; SHA-12: `c904d8af5d1e`; score: 51
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes; Stage 2 — Professional Beta; Goal
- Constitutional signals:
  - # MVP, Beta, And Future Feature Roadmap
  - This document contains:
  - - and future feature concepts.
  - not immutable constitutional doctrine.
  - # Maintenance Notes

### A.112 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 51
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Constitutional signals:
  - This document contains a mixture of:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - and deferred implementation ideas.
  - - prevent future contradictions,

### A.113 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_continuity_workflow.md`
- Categories: epistemic_integrity, human_agency_and_judgment, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 5184; SHA-12: `8a80bdfb8e6e`; score: 21
- Key headings: Project Continuity Workflow; 1. Goals; 2. Memory lanes (what goes where); 3. Archaeology intake workflow; 4. Consolidation workflow (when to run); 5. Reviewer workflow; 6. Proposed updates workflow; 7. Raw archaeology vs durable truths; 8. How future chats should initialize; 9. How to continue safely after context loss; 10. Related docs
- Constitutional signals:
  - How to keep **coherence** across sessions, models, and months—without turning the repo into chaos. Complements `ai_context/memory_workflow.md` (detailed file rhythm) and `docs/institutional_memory_synthesis.md` (archaeology → durable truth).
  - - **Clear separation:** raw archaeology vs curated principles vs implementation state.
  - | **Themed synthesis** | `memory_archaeology_raw/consolidated_notes/` | Onboarding-friendly themes; still subordinate to **human-reviewed** `ai_context/` for “current doctrine.” |
  - | **Durable truths** | `ai_context/core_product_truths.md`, `decisions.md`, `product_brief.md` | Stable principles and decisions. |
  - | **Current implementation** | `ai_context/current_state.md` | What the repo **does now**; update when behavior shifts. |

### A.114 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_memory_taxonomy.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 5641; SHA-12: `e630f6401456`; score: 55
- Key headings: Project Memory Taxonomy; Architecture; UX Philosophy; Visual doctrine vs rendering experiments vs temporary UX; Implementation State; Future Features; Rejected Approaches; Validation Methodology; Edge Cases; Unresolved Questions; AI Strategy; Product Philosophy
- Constitutional signals:
  - This taxonomy keeps project memory organized as the app grows across chats, validation passes, experiments, and external reviews.
  - - Canonical backend truth versus frontend display geometry.
  - - Truth-grid generation strategy.
  - - Leaflet versus future map-library evaluation.
  - Stable experience principles and design constraints.

### A.115 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/relocation_strategy_framework.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 2978; SHA-12: `5542c6b3c8b9`; score: 15
- Key headings: Relocation Strategy Framework; Status; Purpose; Core Principle; Subtractive relocation comes before additive optimization.; Subtractive Relocation; Additive Relocation; Strong Relocations Often Do Both; Tradeoff Reality; Archetypes Are Contextual; Optimization Delusion; Layer 4 Behavior
- Constitutional signals:
  - This document contains a mixture of:
  - - canonical architectural principles,
  - - tentative future architecture,
  - - and deferred implementation ideas.
  - - prevent future contradictions,

### A.116 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ai_and_professional_workflow_strategy.md`
- Categories: human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 4077; SHA-12: `093c412a15e4`; score: 17
- Key headings: AI and Professional Workflow Strategy (From Archaeology); Institutional memory vs chat memory (anti–vibe-chaos); AI reviewer infrastructure (evolution); Non-negotiable product stance; AI collaboration failures as institutional risk; Second-opinion models; Practitioner assist vision (future); Consumer / intake AI (later); Strategic business hypotheses (treat as archaeology, not commitments); Tension to preserve
- Constitutional signals:
  - # AI and Professional Workflow Strategy (From Archaeology)
  - - **Project memory** (`ai_context/`, `docs/`, themed consolidated notes) is **slow, deliberate, and reconciled to the codebase**—the antidote to treating the latest model reply as law.
  - **Anti–vibe-chaos principles** (from repeated archaeology):
  - - Reconcile claims against **git and running modules** before refactoring (“which `main` is live?”).
  - - **Human visual QA** remains authoritative for map topology even when screenshots or agents say “looks fine.”

### A.117 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/current_sidebar_ux_audit.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 4992; SHA-12: `c07666b5828f`; score: 8
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces; 9. Condition model — **next structural UX step (documented)**; 10. Location search placement (documented)
- Constitutional signals:
  - - Earlier passes used extra `<br>` / `hr` slack; **paired selects** and **compact first section** reduced scroll.
  - - Three **planet-in-house** blocks remain **hardcoded A/B/C** (see §Condition model—next structural step).
  - - Section titles + tinted cards improve scan; **design system** still deferred.
  - **Engineering note:** needs coordinated **API/payload** and validation work later—**do not** half-migrate UI alone.
  - ## 11. First-use onboarding (implemented + future)

### A.118 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/foundational_product_truths.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance
- Characters: 4380; SHA-12: `9c5286269c09`; score: 32
- Key headings: Foundational Product Truths (From Archaeology); Trust and truth; Overlap and decision-making; Precision vs cosmetics (non-negotiable vs acceptable); Separation of concerns (recurring architectural moral); Human + AI collaboration stance; Emotional tone and moat; Repetition as signal
- Constitutional signals:
  - # Foundational Product Truths (From Archaeology)
  - **Status labels:** *Durable principle* = should guide decisions for years. *Product stance* = strategic positioning. *Process principle* = how the team builds.
  - ## Trust and truth
  - - **Durable principle — Inspectable precision:** If the map shows a region, line, or overlap, it must mean something **precise** in the relocated chart model. “Plausible geometry” is not validation. Trust is built through reproducible checks, not visual confidence.
  - - **Durable principle — The map is the primary model (not an illustration):** Users explore **geography as astrology**. The map is not decoration around a chart calculator; it is the main instrument.

### A.119 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/geocoder_and_city_strategy.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance
- Characters: 1799; SHA-12: `098e8b02e313`; score: 7
- Key headings: Geocoder and City Strategy (From Archaeology); Why cities are core (not decoration); Readability and density; Search and disambiguation; Internationalization; Provider strategy tension (open); Dataset anecdotes (process lessons); UX details that affect trust
- Constitutional signals:
  - Relocation decisions happen at **named places**; the map must connect semantically rich astrology overlays to **human geography**.
  - - First-match jumps fail for duplicate names (Springfield, Portland, etc.).
  - - Non-Latin labels and mixed scripts complicated manual validation.
  - - Need transliteration, alternate spellings, historical names (Bombay/Mumbai), and “Astro.com naming alignment” for repeatable validation sessions.
  - **Archaeology consensus:** do not migrate prematurely; separate canonical geometry from display; reassess after display adapter maturity.

### A.120 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_memory_synthesis.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 16257; SHA-12: `04f378dc370d`; score: 137
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Constitutional signals:
  - This document bridges **raw multi-chat archaeology** into **project-maintained memory**. It uses explicit status labels:
  - - **Implemented (repo):** verified or strongly evidenced in the current codebase / current milestone docs in this repository.
  - - **Roadmap:** intentional next-direction supported by archaeology and/or roadmap docs, not claimed shipped.
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.

### A.121 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_philosophical_synthesis.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 219
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Constitutional signals:
  - **Status:** Foundational doctrine for **future training**, **reviewer systems**, **UX design**, **product strategy**, **conversational architecture**, and **interpretive governance**.
  - **Authority:** Synthesizes durable texts in `ai_context/`, `docs/`, and `memory_archaeology_raw/consolidated_notes/`. It **does not** supersede those sources on technical implementation; it **weaves** them into one training-readable whole.
  - The relocation astrology platform is built on a paradox that mature users already live inside: **structure is real, and agency is real**. The chart is treated as **structurally real** for product purposes—not as an infinitely rewriteable “vibe,” not as a story generator that owes…
  - This posture has a deliberate audience: **astrology for grownups**—intellectually serious, skepticism-friendly, **sober without cynicism**. Warmth is expressed through **restraint**, not through neon spiritual retail. Excitement is expected to arise from **exploration and judgmen…
  - Underneath lies a technical moral that keeps philosophy honest: **inspectable precision**. If the map shows a region or line, it must mean something **precise** in the relocated model. “Plausible-looking geometry” is not validation. **False membership** is rejected even when cosm…

### A.122 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/map_workspace_behavior_audit_v1_2026-05-30.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 15325; SHA-12: `7567f30ce7ff`; score: 52
- Key headings: Map Workspace Behavior Audit v1; Status; Purpose; Language and ID doctrine (applies to all sections); 1. Behavior already decided; Genie modes; Reasons to reopen Genie (decided intents); Search and render; Variable model; Legacy adapter (handoff to production map path); Map surface and overlay doctrine; Clear Map
- Constitutional signals:
  - - `docs/ui/map_drawer_and_layer_control_doctrine.md` — map-primary hierarchy (strategic)
  - This document does **not** add features, layouts, or architecture. It consolidates decisions already present in contracts and related doctrine.
  - # Language and ID doctrine (applies to all sections)
  - | Rule | Status |
  - | **Do not hardcode final wording into payload semantics** | Decided — snapshot `variables[].label` at render; do not derive engine truth from display strings |

### A.123 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/open_questions_and_unresolved_areas.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3871; SHA-12: `c86a26458dc6`; score: 26
- Key headings: Open Questions and Unresolved Areas (From Archaeology); Geometry and calculation semantics; Rendering architecture; Validation systems; UX systems; Data + search; Product scope and ethics; Renderer beta stabilization questions (Chat 08); Operational workflow; Weak archaeology coverage (second pass, 2026-05); Human review gate
- Constitutional signals:
  - These are **not** a bug list. They are **institutional uncertainties** that multiple chats circled without final product canon.
  - - Formal spec for **MC** presentation: relocated ecliptic MC vs culmination/RA line products—must be explicit in user-facing language and internal tests.
  - ## Validation systems
  - - Automating regression: what becomes CI vs quarterly manual QA vs “validation dossier only.”
  - - Replace fixed panel with **drawer / collapsible rail** without losing obvious restore affordances.

### A.124 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/product_brief.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3080; SHA-12: `ba708a2f1745`; score: 26
- Key headings: Product Brief; Product; Current Core Capabilities; Product Philosophy; Overlay Truth Standard; Current Architecture Direction; Validation Corpus; Institutional memory (archaeology)
- Constitutional signals:
  - - `truth_grid` house overlays for Planet-in-House searches.
  - - Point-and-click popup truth checks for local chart details.
  - - Keep the experience professional-grade, calm, inviting, premium, restrained, and trustworthy.
  - - AI should support the professional core later, not replace it.
  - ## Overlay Truth Standard

### A.125 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/rejected_or_obsolete_approaches.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries
- Characters: 2949; SHA-12: `9bccda948bdc`; score: 11
- Key headings: Rejected or Obsolete Approaches (From Archaeology); Geometry / seam handling; Rendering / signal processing mistakes; Aspect / line extraction misconceptions (historic debugging); Incorrect astronomical short-cuts (explicit catastrophic failures); UX / workflow paths; Institutional / AI process paths; Overlap representation (product iteration); Possibly obsolete but historically explanatory; Not “rejected,” but **dangerous if misunderstood**
- Constitutional signals:
  - This list preserves **why** certain paths were abandoned or flagged dangerous. Do not revive without explicit human re-approval.
  - - **Seam repair by altering canonical polygon topology** (boundary-walking / forced closure along map window edges): caused **house identity leakage**, collapsed distinct houses, Southern Hemisphere artifacts—**rejected as architecture**.
  - - **Hard rectangular overlays presented as real** scaffolding: epistemically dangerous if mistaken for valid Placidus regions.
  - - **Gaussian blur** (or similar) on astronomical fields used for truth extraction: can **shift** solutions and create false loops—rejected for truth; aesthetics belong in frontend-only layers.
  - - **Contour extraction as the final word for centerlines** in some eras: produced double-line artifacts and boundary effects; archaeology pushes toward clearer centerline definitions + separate aura—exact implementation remains product-specific.

### A.126 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/relocation_app_product_roadmap.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 27057; SHA-12: `24ab9bae5cb8`; score: 193
- Key headings: Relocation App Product Roadmap; 1. Current Stable Milestone; 2. Product Philosophy; 3. Core Search Types; 4. Overlay/Color System Roadmap; 5. Aspect Aura Roadmap; 6. UX/Layout Roadmap; 7. City Search / Geocoder Roadmap; 8. Birth Data / Accounts / Professional Mode Roadmap; Saved Object Taxonomy; Phase 2.4 Sampling / Cache Scaffold; Phase 2.5 Sampling / Cache Population Strategy
- Constitutional signals:
  - This document preserves the current product strategy, development sequence, UX philosophy, and validation priorities for future work.
  - - `truth_grid` house overlays are working and remain opt-in.
  - - Popup truth generally matches overlays in current validation.
  - - Validation contradictions are `0` in current truth-grid and angle-sign tests.
  - - `truth_grid` is not yet default.

### A.127 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/travel_and_future_modes.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, validation_governance, future_policy_domains
- Characters: 1279; SHA-12: `c351ba13dcef`; score: 4
- Key headings: Travel and Future Modes (From Archaeology); Road-trip / GPS mode; Offline / airplane scenarios; Transit overlays and relocated houses (debated); Positioning consequence; Dependencies called out
- Constitutional signals:
  - # Travel and Future Modes (From Archaeology)
  - ## Offline / airplane scenarios
  - GPS can work without network; archaeology suggests **pre-downloaded tiles/caches/routes** so travel mode works in constrained connectivity.
  - - User’s personal stance appears: transits against **natal houses** feel truer than transits against relocated houses.
  - Travel mode reframes the app from static comparison to **lived movement**—high engineering and validation complexity; likely **late-phase** feature family.

### A.128 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ux_and_design_language.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3849; SHA-12: `ac5f86eb3a13`; score: 32
- Key headings: UX and Design Language (From Archaeology); Map-first and spatial reading; Trust UX vs explanation UX; Typography and popups (professional validation patterns); Interaction pitfalls called out repeatedly; Emotional tone; Product positioning language (from archaeology); Tensions to preserve (not resolve here); Chat 08 update: style presets and mobile layer control
- Constitutional signals:
  - - **Map dominance:** Controls exist to serve exploration; they must not steal the primary visual field during validation or professional use.
  - - **Panel vs drawer tension:** Fixed panels repeatedly **hid map evidence** (lines behind UI). Future direction: adjacent panel, collapsible drawer, draggable rail—anything that preserves inspectability.
  - - **Global map ergonomics:** Users must pan freely near **Pacific/dateline/polar** regions during validation; artificial snap-back is disqualifying for this product class.
  - - **Lay users cannot be expected to reconcile** overlay edges with chart tables; that is a **developer failure mode**, not a user skill issue.
  - - **Professionals still need an oracle:** Right-click / precise coordinate inspection is framed as **truth instrumentation**. It must have onboarding (hint, mode toggle), and mobile needs long-press equivalent.

### A.129 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 20953; SHA-12: `db53e1e91227`; score: 87
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Constitutional signals:
  - **ARCHITECTURE REVIEW — aligned with Map-First Product Doctrine (2026-05-31)**
  - **Date:** 2026-05-29 (original); **doctrine alignment:** 2026-05-31
  - **Governing doctrine:** `docs/constitutional/map_first_product_doctrine_v1.md` — supersedes dashboard-centric recommendations in v1.0–v1.1 of this review.
  - - `docs/architecture/client_chart_data_model_v1_2026-05-29.md` (data ownership authority)
  - - `docs/ux/2026-05-29_application_journey_architecture_v1.md` (screen/journey authority)

### A.130 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/00_OPERATOR_START_HERE.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance
- Characters: 697; SHA-12: `a0e79ddfcf29`; score: 4
- Key headings: AI Onboarding Entry Point
- Constitutional signals:
  - # AI Onboarding Entry Point
  - 1. 01_ai_product_core
  - Primary historical failure modes:
  - - oracle behavior
  - - repeating doctrine without understanding doctrine

### A.131 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_EVALUATION_LOG.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, validation_governance
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.132 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_WORKFLOW_GOVERNANCE.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 14272; SHA-12: `570f3cca823a`; score: 112
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Constitutional signals:
  - # AI Workflow Governance Protocol
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in writing.
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisible engineering inte…
  - The Ghost Boss role of this protocol is to protect the project from short-term commercial pressure, founder optimism, and AI recency bias. It asks: what invisible thing did this phase make easier to forget, normalize, or accidentally depend on?
  - ## Ghost Boss Governance Doctrine

### A.133 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/KILL_TEST.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, validation_governance
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.134 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/PRODUCT_COMPREHENSION_GATE.md`
- Categories: epistemic_integrity, moral_data_use_limits, ai_authority_limits, validation_governance
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.135 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/ai_drift_audit_framework.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9541; SHA-12: `889f1d9b2f3a`; score: 68
- Key headings: AI drift audit framework; 1. Healthy AI posture (target); 2. Audit dimensions and warning signs; 2.1 Excessive certainty; 2.2 Flattery; 2.3 Manipulative spirituality; 2.4 Optimization obsession; 2.5 Over-helpfulness; 2.6 Premature closure; 2.7 Reducing exploratory play; 2.8 Guru behavior; 2.9 Dependency framing
- Constitutional signals:
  - # AI drift audit framework
  - **Status:** Meta-governance — reusable **audit checklist** for interpretive and assistive AI behavior over time.
  - **Purpose:** Catch **comfort bias**, **oracle creep**, and **flattening** before they ship—not after user dependency forms.
  - **Reads with:** `docs/ai_constitution_and_review_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/brand_and_experience_foundations.md`, `docs/process/doctrine_review_cycle.md`.
  - This is **not** generic “AI ethics.” It is **product-specific** interpretive governance for a relocation astrology instrument.

### A.136 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/anti_cursor_bullshit_governance_rules.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 75
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Constitutional signals:
  - # Anti-Cursor Bullshit Governance Rules
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountability_failure_audit.md` …
  - Cursor and other AI agents are **accelerators**, not authorities.
  - This project assumes **low trust in AI outputs until proven**.

### A.137 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/constitutional_ingestion_checklist.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 57
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Constitutional signals:
  - # Constitutional Ingestion Checklist
  - - track doctrine ingestion,
  - Update this document whenever:
  - - new constitutional docs are added,
  - - doctrine evolves,

### A.138 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/implementation_governance_and_ai_workflow_protocol.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3988; SHA-12: `b127e5c52050`; score: 42
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Constitutional signals:
  - # Implementation Governance And AI Workflow Protocol
  - - AI workflow behavior,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - - constitutionally governed development.

### A.139 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/purification_audit_framework.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 3639; SHA-12: `a43528565790`; score: 69
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Constitutional signals:
  - - architectural integrity checks,
  - Purification audits are mandatory maintenance mechanisms.
  - - or violate constitutional doctrine.
  - - preserve architectural integrity,
  - # Core Principle

### A.140 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/review_contracts_and_governance.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 12252; SHA-12: `18cc9636738c`; score: 97
- Key headings: Review contracts and governance (implementation layer); 1. What a “review contract” is here; 2. Principles reviewers hold in tension; 3. Implementation review questions; 4. UX review questions; 5. AI behavior review questions; 6. Symbolic integrity review questions; 7. Exploratory and play preservation checks; 8. Anti-chaos visual checks; 9. Anti-guru and anti-coercion checks; 10. Does this preserve contemplative space?; 11. Intelligent exceptions (examples)
- Constitutional signals:
  - **Status:** Lightweight operational doctrine—**not** a compliance checklist, **not** a substitute for judgment, **not** corporate policy theater.
  - **Reads with:** `docs/ai_constitution_and_review_architecture.md` (interpretive AI layers and anti-patterns), `docs/DOCTRINE_INDEX.md` (where each doctrine lives), `docs/institutional_philosophical_synthesis.md` (foundational synthesis for training), `docs/process/doctrine_review…
  - **Purpose:** give reviewers and implementers **shared guardrails** so work preserves **symbolic honesty, restraint, readability, agency, intentionality, exploratory freedom, professional seriousness, and emotional tone**—while still allowing **fast iteration** and **intelligent i…
  - A review contract is a **constitutional alignment**: before merge or ship, someone asks whether the change **moves the product in a direction we have already committed to**, or whether it **drifts** toward comfort bias, spectacle, oracle framing, epistemic lying, or UX chaos.
  - Contracts are **guardrails**, not formulas. They do not award points for mechanical compliance. A change can satisfy every literal question below and still be wrong in context—or violate one question deliberately for a **documented, rare, intelligent exception**. The reviewer’s j…

### A.141 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 185
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Constitutional signals:
  - **CANONICAL** for non-AI application UX architecture (Web 2.0 standalone product).
  - **Scope:** User journey, screen responsibilities, mood states, and control architecture for the **dumb version** — facts-first exploration without AI dependency.
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_and_layer_control_doct…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.

### A.142 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 157
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Constitutional signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.md` before using thi…

### A.143 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/README.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 65
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Constitutional signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - - layer sovereignty,
  - - truth integrity,
  - - symbolic humility,

### A.144 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 121
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Constitutional signals:
  - # UX Constitution
  - **CANONICAL** — single source of truth for **product behavior** (UX Truth).
  - - the authority when UX behavior is ambiguous
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.

### A.145 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 252
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Constitutional signals:
  - # UX Doctrine Master
  - **CANONICAL** — primary source of truth for **UX Truth** (workflow, hierarchy, transformation, continuity).
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.

### A.146 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: constitutional_anchor, epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 35789; SHA-12: `795365723409`; score: 176
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Constitutional signals:
  - **CANONICAL** for non-AI Web 2.0 product data architecture.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/su…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - - how behavioral facts may be captured **without interpretation**,

### A.147 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 8365; SHA-12: `d1c233003983`; score: 76
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Constitutional signals:
  - # Intentionality and symbolic constraints
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite malleability.
  - **Companion doctrine (read together):**
  - - **`docs/brand_and_experience_foundations.md`** — especially **“Interpretive integrity and archetypal honesty”** and **“Interpretive language and emotional transparency.”**

### A.148 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: epistemic_integrity, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, future_policy_domains
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 47
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Constitutional signals:
  - # Map-First Product Doctrine v1
  - **CANONICAL** — supersedes prior dashboard-centric interpretations in May 2026 planning documents.
  - **Scope:** Product identity, primary surfaces, Map / Chart Page co-stars, continuity hierarchy, intent reservation, comparison layout canon, related-chart links, AI boundaries.
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/ai/ai_interp…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.

### A.149 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: constitutional_anchor, epistemic_integrity, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 50
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Constitutional signals:
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emot…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.
  - **Must not contain:** activity feeds, recents, owner hero cards, favorites, charts, map as primary surface, widgets, metrics.

### A.150 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: constitutional_anchor, epistemic_integrity, human_agency_and_judgment, symbolic_humility_and_interpretation, moral_data_use_limits, ai_authority_limits, architecture_boundaries, validation_governance, future_policy_domains
- Characters: 9566; SHA-12: `3de8663545ba`; score: 79
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Constitutional signals:
  - # Professional Non-AI Workflow v1
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/r…
  - - AI is **absent or explicitly off**,



---

## Appendix B — Audit Statement

Programmatic pass selected 196 constitutional/foundational source blocks from 196 total archive blocks. The audit JSON stores matched file names, hashes, headings, constitutional signals, category counts, central sources, and source metadata. Final generated word count before this statement: 21317 words.
