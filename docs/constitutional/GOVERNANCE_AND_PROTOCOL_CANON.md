# GOVERNANCE_AND_PROTOCOL_CANON.md

**Status:** Canonical onboarding and transfer manual for governance, AI discipline, validation gates, operational protocols, anti-drift rules, and future-agent conduct.  
**Source archive:** `ALL_PROJECT_DOCUMENTS.txt`  
**Generation method:** deeper three-pass local Python extraction and consolidation.  
**Total archive file blocks parsed:** 196  
**Governance/protocol source blocks matched:** 183  
**Audit hash:** `f660637dc820725a`

---

## 0. Constitutional Boundary

**Reveal structure. Preserve judgment.**

This is the governing sentence for the product, the codebase, the validation system, and every AI collaborator that touches the project. The platform exists to reveal geographical chart structure and preserve human judgment. It is not an oracle, not a hidden recommendation system, not a confidence theater, not a dashboard that pretends to know what a user should do, and not an AI-driven symbolic authority. The software reveals where chart conditions hold. The user interprets what those conditions mean.

This boundary applies to governance as much as interface. A future LLM must not “help” by inventing an interpretation layer when the task is geometry. It must not “help” by smoothing a visual defect when the problem is a truth-field or sampling defect. It must not “help” by changing backend architecture when the observed issue is stale browser state, a cached response, a wrong port, or a frontend pane-order bug. It must not inflate a prototype into a production claim, a roadmap idea into a shipped feature, or a partial validation into a pass.

The project’s governance exists because previous AI-assisted development repeatedly exposed a pattern: plausible answers can be expensive, confident, and wrong. This canon is the antidote. It teaches future agents to read the codebase slowly, separate authority layers, prove changes, preserve rollback, and refuse to pretend certainty that has not been earned.

---

## 1. Authority Hierarchy

The project has multiple kinds of knowledge. They are not equal.

### 1.1 Implemented reality

Implemented reality is what the current repository actually does. It includes active backend endpoints, frontend files, validation scripts, reports, screenshots, local HTML sandboxes, migrations, and state models that have been verified against code or current artifacts. Implemented reality outranks chat memory, design wishes, and AI summaries.

Before changing implementation, an AI or developer must ask: What file actually owns this behavior? Is the behavior in production, sandbox, archaeology, doctrine, or roadmap? Has it been validated? Is the server running the same file I think I changed? Is the browser hitting the intended port and endpoint?

### 1.2 Canonical doctrine

Canonical doctrine governs why the system is built this way. It includes architecture principles, rendering truth laws, map-first product doctrine, design canons, validation rules, AI workflow governance, and deferred-excellence tracking. Doctrine can constrain implementation even when implementation is not yet complete. When implementation diverges from doctrine, the team must either fix implementation or explicitly amend doctrine. Silent drift is prohibited.

### 1.3 Validation evidence

Validation evidence includes scripts, JSON reports, markdown narratives, screenshots, smoke outputs, parity checks, fixture manifests, and brute-force comparison artifacts. Evidence outranks confidence. A visual “looks right” only after the relevant truth checks, popup parity, screenshot comparison, or smoke gate has passed. Evidence must be retained because future chats lose context.

### 1.4 Archaeology and history

Archaeology preserves failed paths, superseded ideas, and why decisions changed. It is not automatically current truth. Older contradictory ideas remain valuable because they explain failure modes, but they must not be copied into active doctrine without reconciliation. Superseded docs must be labeled. Future agents must treat raw archaeology as evidence, not law.

### 1.5 Roadmap and speculation

Roadmap features are intentional future directions. Speculative features are valuable ideas that have not earned implementation authority. Neither may be represented as shipped. Future transits, travel mode, advanced AI, Web3-like models, broad ontology ecosystems, or regulatory structures must remain outside active instructions unless explicitly promoted through doctrine and validation.

---

## 2. AI Alignment Strategy

### 2.1 The AI is an assistant, not an authority

AI accelerates reading, drafting, testing, refactoring, and synthesis. It does not own product judgment, symbolic interpretation, merge authority, or proof status. It must remain subordinate to human oversight, repository truth, validation artifacts, and doctrine. Any AI answer that sounds coherent but lacks source contact, code contact, or validation contact is low-trust by default.

### 2.2 Required operating posture for future LLMs

A future LLM working on this project must:

1. Identify the task type: product, renderer, backend, database, validation, governance, documentation, UX, or archaeology.
2. Identify the single instability source under investigation.
3. Read the relevant doctrine before proposing edits.
4. Inspect current implementation before claiming behavior.
5. Separate implemented features from roadmap ideas.
6. Separate frontend rendering from backend math.
7. Separate cache/runtime effects from computation truth.
8. Separate browser/server/path issues from application logic.
9. State uncertainty plainly.
10. Prefer one small reversible change over broad speculative patching.
11. Preserve rollback paths.
12. Produce exact files changed or exact proposed file replacements.
13. Run or define the relevant validation gate.
14. Record what remains unverified.

### 2.3 Anti-Cursor-bullshit rules

The archive repeatedly warns against “vibe coding” failure modes: confident patching, rabbit holes, fake completion, tool-induced overreach, and expensive loops where AI solves the wrong problem. The protocol response is strict.

An AI must not:
- declare success before a smoke test, parity check, screenshot comparison, or explicit human validation;
- rewrite stable architecture because a visual artifact is ugly;
- turn a cosmetic issue into a math panic without evidence;
- confuse a stale uvicorn process or wrong file path with a code defect;
- mix multiple refactors in one change;
- stage broad unrelated files;
- hide uncertainty behind pleasant reassurance;
- invent endpoint schemas, database tables, or UI contracts not present in the source;
- over-generalize a sandbox into production;
- delete archaeology because it is embarrassing or old;
- resurrect superseded paths without a doctrine amendment.

### 2.4 Required answer pattern for technical work

For significant engineering or architecture tasks, the AI should structure its output around:

- Known facts.
- Unknowns.
- Relevant doctrine.
- File(s) involved.
- Proposed smallest change.
- Validation gate.
- Rollback path.
- Rejected scope.
- Next step.

This pattern prevents the AI from substituting narrative coherence for actual control.

---

## 3. Operational Discipline

### 3.1 One instability source at a time

The project has repeatedly suffered when backend math, frontend rendering, cache state, browser state, styling, and UX were debugged simultaneously. The governance rule is: isolate one instability source before editing. If the issue is geometry, do not also change palette. If the issue is drawer layout, do not also change endpoint payloads. If the issue is cache invalidation, do not also refactor search UI. If the issue is stale server state, do not touch math.

### 3.2 Measure before theorizing

A theory is not a diagnosis. Before changing code, gather the smallest evidence that distinguishes likely causes. Use raw JSON, endpoint response inspection, popup truth checks, screenshot overlays, validation scripts, logs, or controlled fixtures. Measurements should classify the failure as math, rendering, data, cache, UI interaction, browser state, or process.

### 3.3 Small reversible commits

Every risky change must be reversible. Git checkpoints precede architecture migration, renderer changes, database changes, payload contract changes, and validation harness changes. A single commit should ideally contain one conceptual change. If a change cannot be reverted without breaking unrelated work, it is too broad or poorly isolated.

### 3.4 Exact edits over vague surgery

The user is not a developer and strongly prefers exact copy-paste instructions. Agents should provide complete replacement blocks, whole-file rewrites when appropriate, or precise commands. Vague “change something like this” instructions are prohibited when code is unstable. Python/JS indentation-sensitive edits require extra care. TextEdit-style manual surgery is discouraged for complex files.

### 3.5 Documentation is infrastructure

Governance artifacts are not “paperwork.” They are the project’s externalized memory. Because chat memory is fragile, important decisions must be promoted into durable docs, current-state files, validation narratives, or audit reports. The purpose is not bureaucracy; it is recoverability.

---

## 4. Validation Constitution

### 4.1 Validation artifacts are first-class project assets

Validation outputs, reports, screenshots, and narratives preserve proof. They are not disposable unless explicitly classified as scratch. They allow future AI sessions and human collaborators to continue without re-litigating everything. A validation artifact should answer: what was tested, why it mattered, what passed, what failed, which files were involved, and what next action is justified.

### 4.2 Required validation logic

Every meaningful system change requires:

1. A hypothesis.
2. A controlled test.
3. A pass/fail criterion.
4. An evidence artifact.
5. A rollback route.
6. A decision about whether doctrine or deferred-excellence inventory needs updating.

A change that cannot define its validation gate is not ready for implementation.

### 4.3 Smoke gates

Smoke tests are guardrails against stale-server, wrong-file, and regression errors. They should be small, repeatable, and focused. Where possible, scripts should exit non-zero on regression and produce a report. A Makefile or shell script can be better than an elaborate framework. Simplicity protects repeatability.

### 4.4 Popup truth checks

The point popup is a truth anchor. Any overlay that claims a condition at a location must agree with point truth within the expected precision of the substrate. Popup-overlay disagreement is a trust threat. If the overlay impression and point inspection disagree, the popup and validated engine truth win. Visual tuning must not hide this conflict.

### 4.5 Brute-force wall validation

The brute-force wall is the reference method: sample densely enough to establish what truth should look like, then back off intelligently. The wall is expensive by design. Its purpose is not production performance; its purpose is to prevent clever shortcuts from lying. Adaptive methods, cache strategies, progressive reveal systems, and canonical renderers must be compared against wall-style truth where appropriate.

### 4.6 Regression classification

Failures must be classified before repair. Categories include:
- blocker: prevents trust or continuation;
- trust risk: user may believe false structure;
- deferred excellence: important but not blocking;
- rejected scope: tempting but intentionally out of bounds;
- archaeology: retained history, not active path.

Classification prevents urgent-sounding but low-value work from derailing the roadmap.

### 4.7 UI validation

UI changes require validation too. Drawer collapse must preserve condition state. Mute/solo must not alter search truth. Overlaps must remain readable. City labels must remain visible. Debug surfaces must remain hidden in commercial mode. Screenshot fixtures should catch regressions where possible.

### 4.8 Cache validation

Cache behavior must be tested independently from computation. A cached correct answer is not proof of current computation. A stale cache can make correct code appear wrong or wrong code appear right. Cache keys must include chart identity, bounds, zoom, block size or resolution, conditions, substrate, lat-cap policy, settings snapshot, and any other parameter that changes output. Cache invalidation on chart change, substrate change, and condition change is mandatory.

---

## 5. Architecture Enforcement

### 5.1 Canonical truth versus display adaptation

Canonical backend truth and frontend display geometry are separate. Frontend wrapping, clipping, smoothing, pane ordering, or visual material language must not change logical astrology semantics. Display adaptation may help Leaflet or Canvas show the truth. It may not redefine the truth.

### 5.2 Rendering truth over cosmetics

The map is an instrument for discovering where symbolic conditions hold, not a poster that must look seamless at every zoom and latitude. Color, opacity, blur, and stroke tweaks do not fix geometry defects. Cosmetic smoothing that moves boundaries, fills, or perceived membership without truth support is prohibited.

### 5.3 Layer purity

Layer 1 membership comes from chart computation and geography. Layer 2 settings can configure vocabulary, defaults, or helper views, but must not secretly alter Layer 1 truth. Layer controls affect display unless they represent explicit semantic conditions. Saved snapshots preserve replay honesty.

### 5.4 Snapshot immutability

Rendered search payloads must be immutable. Save Search, Pin, history, replay, and share functions attach to the rendered snapshot, not the mutable live editor. Re-render creates a new snapshot. Silent mutation destroys trust and produces irreproducible sessions.

### 5.5 Legacy and canonical substrate rules

Migration from legacy to canonical renderers must be gated, reversible, and explicit. No hidden auto-fallback. No mid-session substrate mixing. No silent promotion of debug-only canonical paths to production. No using legacy polygons inside canonical screen-space paths if the doctrine says the substrate is a paradigm swap. If a branch remains for archaeology, mark it clearly.

### 5.6 Database and persistence enforcement

Local JSON, sandbox Supabase schemas, future migrations, saved investigation JSON, settings snapshots, and chart records must not drift into permanent product storage accidentally. Persistence must be designed with ownership, replay honesty, and migration strategy. Birth chart data, chart records, saved locations, saved searches, comparisons, and notes belong to clear objects. Renderer internals do not belong in semantic saved investigations unless explicitly stored as debug metadata.

---

## 6. Governance Closeout Protocol

Every significant task should end with a closeout. The closeout is the project’s internal conscience.

A complete closeout includes:

- Files changed or artifact generated.
- Validation performed or explicitly not performed.
- Evidence location.
- Rollback scope.
- Deferred Excellence Registry update or no-op reason.
- Rendering doctrine update or no-op reason.
- Validation narrative decision.
- Blocker/trust/deferred/rejected classification.
- Rejected scope.
- Next-step recommendation.

If no code changed, say so. If a document was generated without full zero-omission proof, say so. If validation was not run, do not imply it passed.

---

## 7. Memory and Continuity Protocol

### 7.1 Project memory beats chat memory

Chat context is fragile and expensive. Durable project memory lives in docs, ai_context, validation reports, consolidated notes, and transfer briefs. Future AI sessions must not assume the last chat is authoritative. They must read current doctrine and implementation state.

### 7.2 Archaeology pipeline

Raw extractions live in pending imports. Themed synthesis helps onboarding but does not outrank raw text when details matter. Institutional synthesis should label claims as implemented, roadmap, speculative, or workflow infrastructure. Later threads generally supersede earlier doctrine on current UX/architecture, but only when reconciliation is explicit.

### 7.3 Transfer documents

Transfer docs bootstrap new sessions. They should be honest about solved items, deferred items, current renderer status, governance status, immediate recommended phases, strategic warnings, and startup procedure. A transfer doc is not a substitute for reading doctrine when making code changes.

### 7.4 Weak source metadata

Placeholder files, incomplete extracts, or combined prompt/audit files must be marked as weak inputs. A missing extraction does not prove missing knowledge if the same substance exists elsewhere. Conversely, a recent upload of an old doc does not make its content current.

---

## 8. Prompt Protocols for Future AI Agents

### 8.1 Startup procedure

A future AI session should begin by identifying the task type, then reading the relevant continuity index, governance doc, deferred excellence registry, current rendering doctrine, validation narratives, and active implementation files. It should check current git status before editing. It should state the one instability source.

### 8.2 When asked to implement

The agent should:
1. Restate the target narrowly.
2. Identify the active file(s).
3. Confirm current behavior from source where possible.
4. Propose the smallest edit.
5. Provide exact changes.
6. Run or request the correct smoke gate.
7. Report honestly.

### 8.3 When asked to diagnose

The agent should:
1. Avoid patching first.
2. Separate likely classes of failure.
3. Ask which evidence distinguishes them, or use available files/logs.
4. Produce a minimal diagnostic test.
5. Recommend only one next change.

### 8.4 When asked to produce documents

The agent must distinguish extraction, synthesis, and verified canon. It may create a draft from matched material, but it must not claim “100% extraction” unless it has actually parsed all relevant blocks and audited the draft back to source. If it cannot verify zero omissions, it must say so.

### 8.5 When asked to evaluate another AI

The agent should be direct, not flattering. It should identify what the other AI got right, what it overstated, what it omitted, what evidence is missing, what risk it introduced, and whether its recommendation is safe to follow. “Looks plausible” is not enough.

---

## 9. Hallucination and Rabbit-Hole Prevention

### 9.1 Common rabbit holes

- Reopening astrology math panic because of a display artifact.
- Replacing the map library before proving the blocker is library-specific.
- Rebuilding the renderer because the palette is ugly.
- Treating AI interpretation as required for non-AI professional workflows.
- Turning local cache experiments into product architecture.
- Building dashboards, telemetry, or abstraction frameworks before there is a reader or use case.
- Creating giant docs that mix law, history, speculation, and implementation without labels.
- Treating visual polish as validation.

### 9.2 Stop conditions

An agent should stop and re-ground when:
- the same patch class fails twice;
- validation output contradicts the theory;
- it is about to change more than one subsystem;
- it cannot name the file that owns the behavior;
- it cannot state rollback;
- it is using “probably” to justify a code edit;
- the user is paying for repeated speculative attempts without progress.

### 9.3 Cost discipline

Rigor can be divided into micro-steps. The project should use one-page or one-file passes when possible, generate indexes before full canons, and separate extraction from synthesis. AI should do more mechanical work via scripts rather than forcing the user into manual repetition. However, speed must not become fake certainty.

---

## 10. Compliance Checklist

Before merging, shipping, or accepting a major document, answer:

1. Does it preserve “Reveal structure. Preserve judgment”?
2. Does it preserve human interpretation authority?
3. Does it distinguish implemented reality from roadmap/speculation?
4. Does it preserve canonical truth versus display adaptation?
5. Does it avoid hidden astrology semantics changes?
6. Does it preserve popup truth and inspectability?
7. Does it have validation evidence or explicitly state validation is pending?
8. Does it include rollback scope?
9. Does it avoid broad unrelated changes?
10. Does it respect snapshot immutability?
11. Does it avoid silently changing chart context?
12. Does it keep debug surfaces out of production UX?
13. Does it preserve project memory and archaeology labels?
14. Does it avoid AI flattery and fake confidence?
15. Does it state unknowns clearly?
16. Does it classify deferred excellence versus blocker?
17. Does it avoid resurrecting superseded paths?
18. Does it protect user trust over visual confidence?
19. Does it document files changed?
20. Does it recommend the next smallest safe step?

---

## 11. Active Non-Goals

The active governance system does not include long-term regulatory frameworks, formal legal compliance programs, telemetry dashboards, enterprise AI governance suites, multi-agent orchestration platforms, speculative Web3 governance, model-training pipelines, certification ecosystems, or production safety boards. These may become relevant later, but they are not active instructions unless explicitly promoted.

---

## Future Operational Excellence Inventory

This inventory tracks future procedural improvements without making them active obligations.

### Validation automation

- Fixture manifest and “run these five” script.
- Expanded latitude and polar stress suite.
- Brute-force/truth export hygiene.
- Golden screenshot regression fixtures.
- Popup-overlay parity sampling harness.
- Cache storm, chart-change, drainage, and substrate-flip smokes.
- CI integration after fixtures stabilize.

### AI workflow governance

- Local AI reviewer prompt templates.
- Structured AI drift audit reports.
- Proposed-updates queue with human approval.
- Better separation of implementation review and doctrine review.
- Red-team prompts for AI overconfidence, flattery, and hallucinated architecture.

### Documentation operations

- Canon generation scripts with source-block hashes.
- Doctrine index maintenance automation.
- Superseded-doc banner enforcement.
- Current-state freshness checks.
- Transfer-document templates per task type.
- Weak-source metadata flags.

### Risk and rollback operations

- Standard rollback checklist per subsystem.
- Migration playbook template based on Phase-C substrate plan.
- Cache-key invariant checker.
- Debug/production surface leakage audit.
- Git pre-commit reminders for broad staging.

### Governance review maturity

- Formal “blocker / trust risk / deferred excellence / rejected scope” tagging in task reports.
- Periodic Deferred Excellence Registry review.
- Human-readable dashboard for validation artifact status, only when someone will actually read it.
- Integration of governance closeout into every major implementation branch.

### Future AI and interpretation controls

- Optional future AI constitution for consumer interpretation.
- Evaluation rubrics for symbolic humility and archetypal honesty.
- Bias tests against comfort-spinning difficult placements.
- Clear labeling of generated interpretation versus factual chart conditions.
- Human override and professional sovereignty controls.



---

## Appendix A — Governance Source Index

### A.1 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/AI_WORKFLOW_GOVERNANCE.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 14272; SHA-12: `570f3cca823a`; score: 256
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Requirement signals:
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in w…
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisi…
  - ## Ghost Boss Governance Doctrine
  - Every phase closeout must ask whether it introduced or exposed:
  - * missing test, CI, regression, or rollback discipline;

### A.2 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/CURRENT_RENDERING_DOCTRINE.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 7576; SHA-12: `0b4a58929157`; score: 75
- Key headings: Current Rendering Doctrine — Summary; The stack (top to bottom); Non-negotiables; Legacy `/search-regions` Truth Grid; Phase-2 cache (product substrate); Evidence bundle (read in this order); Documents marked SUPERSEDED (archaeology preserved); Warnings against backsliding; Remaining gaps (structural, not aesthetic); Recommendation
- Requirement signals:
  - # Current Rendering Doctrine — Summary
  - > **Authority:** `docs/relocation_map_architecture.md` wins on conflict.
  - | **Brute force** | Validation wall. Every optimisation must match it cell-for-cell (or pixel-for-pixel on screen). | Canonical control specimen |
  - | **Targeted escalation** | Extra halo / probes / lat-cap boundary rules **only** at known instability classes. | In use — not global |
  - | **Aura / raindrops / palette** | Visual language on top of truthful occupancy. | Exploration: `map_SANDBOX_raindrop_aesthetic.html` (see `validation/narratives/raindrop_aesthetic_exploration.md`) |

### A.3 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DEFERRED_EXCELLENCE_REGISTRY.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 30563; SHA-12: `8fdc70fc996d`; score: 381
- Key headings: Deferred Excellence Registry; Purpose; Cross-Cutting Doctrine; Status Legend; 1. Renderer / Topology Improvements; 1.1 Stable component IDs across zoom/pan; 1.2 Graph / global path solver; 1.3 Canonical-default migration; 1.4 Continuous topology extraction refinement; 1.5 Subpixel/edge extraction refinement for narrow-orb ASC; 1.6 Seam-aware topology continuity; 1.7 Signed-distance-field experiments
- Requirement signals:
  - The primary purpose is preserving hidden robustness and institutional memory: invisible infrastructure improvements, architecture refinements, reliability upgrades, governance ideas, performance optimizations, renderer trust improvements, scaling concerns, cac…
  - These are the things founders and AI systems tend to forget because users do not directly see them, they do not demo well, short-term success can mask their absence, and commercial pressure naturally favors visible product work. The registry exists to preserve…
  - Short rule: when choosing what to capture here, prefer invisible engineering and infrastructure concerns over visible feature wishes. Feature wishes may be listed when they carry trust, platform, or operational consequences, but the registry's center of gravit…
  - ## Cross-Cutting Doctrine
  - 1. **Anti-death-spiral doctrine (from Phase 1.19):** Do not continue math/rendering work unless it removes a named production blocker or protects future product trust. Items in this registry are evidence of restraint, not a to-do list.

### A.4 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DOCTRINE_INDEX.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 289
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Requirement signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.…

### A.5 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/EXECUTIVE_TRANSFER_BRIEF_NEXT_CHAT.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9792; SHA-12: `d91200d72161`; score: 144
- Key headings: Executive Transfer Brief For Next Chat; 1. Current Project State; 2. What Is Considered Solved; 3. What Is Intentionally Deferred; 4. Current Renderer Status; 4.1 Renderer handoff state; 5. Governance Status; 6. Productization Status; 7. Immediate Next Recommended Phases; 8. Strategic Warnings; 9. Key Philosophical Doctrines; 10. How Future AI Should Behave
- Requirement signals:
  - - Brute-force wall validation exists as the reference method.
  - - Renderer readiness gate explicitly unblocked product scaffolding.
  - - Canonical renderer: debug-only, gated, measurable, reversible.
  - - Transported-material renderer: beta-stabilized for validation-track work, not final aesthetic approval.
  - Do not silently switch renderers. Do not auto-promote canonical. Do not treat visual mismatch as math failure without evidence.

### A.6 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_1_2_EXTRACTION_AUDIT.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 31222; SHA-12: `99e7cbcf42db`; score: 322
- Key headings: Phase 1.2 Extraction Audit; Concise Findings; Files Inspected; Production and backend; Sandboxes; Validation / capture scripts; Doctrine used as constraints; Current Rendering Entry Points; Production renderer; Backend endpoints; Sandbox renderers; Validation harnesses and capture scripts
- Requirement signals:
  - # Phase 1.2 Extraction Audit
  - > **Status:** Preparation audit only. No implementation is authorized by
  - > **Authority:** Follows `docs/PHASE_C_IMPLEMENTATION_PROTOCOL.md`,
  - > **Non-goals:** No production renderer mutation. No cache rewrite. No
  - This audit maps the current rendering entry points, dependency shape,

### A.7 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 58355; SHA-12: `c6ef18d0c316`; score: 350
- Key headings: Phase-2 Cache Integration — Architecture & Implementation Planning; 0. Where this fits; 1. Grounding — what is true today, measured; 1.1 Sandbox state (measured, not asserted); 1.2 What this means; 1.3 Hard architectural finding — substrate mismatch; 2. Production Scheduler Architecture; 2.1 Single-active-job model; 2.2 Foreground vs background queues; 2.3 Cancellation / interruption behaviour; 2.4 Priority escalation rules; 2.5 Viewport ownership
- Requirement signals:
  - > **Status:** Architecture and planning doctrine. Design only. No code
  - > **Authority:** `docs/relocation_map_architecture.md` (§ "Phase 2 cache
  - > **Companion:** `validation/narratives/phase2_cache_implementation.md`
  - > **Stability:** Slow. Implementation details may rev; design rules here
  - > **Non-goals:** No aura styling. No aesthetic rendering changes. No

### A.8 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_IMPLEMENTATION_PROTOCOL.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 54962; SHA-12: `c32fcebbd584`; score: 669
- Key headings: Phase-C Implementation Protocol; Operational constitution for landing the validated architecture without future chaos; 0. Where this fits; 1. Implementation Phase Breakdown; Phase 1.1 — Documentation alignment (no code); Phase 1.2 — Archaeology fencing (low-risk cleanup); Phase 1.3 — Scheduler extraction (no behaviour change); Phase 1.4 — Substrate adapter scaffold (legacy-only); Phase 1.5 — Canonical substrate wiring (flag-gated); Phase 1.6 — Scheduler/cache wiring on canonical (flag-gated); Phase 1.7 — Parity validation harnesses; Phase 1.8 — Default flip + stabilisation
- Requirement signals:
  - > **Status:** Operational doctrine. Implementation planning only.
  - > **Authority on conflict:** `docs/relocation_map_architecture.md`,
  - > meta-governance cycle. Does not override slow doctrine.
  - > **Non-goals:** Aura aesthetics. Animation. Renderer rewrite. New
  - with — never duplicates — the existing meta-governance docs. Where

### A.9 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_PRODUCTION_MIGRATION_PLAN.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 64644; SHA-12: `af96b1d10c2e`; score: 636
- Key headings: Phase-C Production Migration Plan; Legacy overlay pipeline → canonical screen-space adaptive substrate; 0. Where this fits; 1. Legacy vs Canonical Substrate Audit; 1.1 The legacy overlay pipeline (what is in production today); 1.2 The canonical screen-space substrate (validated, sandbox-proven); 1.3 Semantic differences; 1.4 Rendering differences (visible); 1.5 Cache compatibility implications; 1.6 Validation differences; 1.7 Hidden assumptions; 1.8 Likely regression risks (ranked)
- Requirement signals:
  - > **Status:** Migration architecture and planning doctrine. Design
  - > **Authority on conflict:** `docs/relocation_map_architecture.md`,
  - > **Non-goals:** No aura styling. No aesthetic rendering changes. No
  - has a smoke gate. Every step is independently testable. Every step
  - | Current rendering doctrine | `docs/CURRENT_RENDERING_DOCTRINE.md` | Status board of the stack |

### A.10 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_RENDERING_ARCHITECTURE.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, architecture_enforcement
- Characters: 47288; SHA-12: `3744bf667647`; score: 333
- Key headings: Phase C — Rendering Substrate Architecture (Governing Laws); 0. Where this document sits; 1. Canonical Rendering Truths; 1.1 The four absolute statements; 1.2 Screen-space truth doctrine; 1.3 Adaptive refinement as production substrate; 1.4 Why visible output is canonical; 1.5 Globe truth vs screen truth; 2. Convergence Strategy; 2.1 Convergence is the contract; sample count is not; 2.2 Targeted escalation, never global slowdown; 2.3 Refinement economy — *truth where unstable*
- Requirement signals:
  - > **Authority:** `docs/relocation_map_architecture.md` wins on direct conflict.
  - > **Adopted draft:** 2026-05-21 (same-day as the rendering doctrine reset).
  - > **Stability:** Slow. Implementation details around this doctrine may rev;
  - | Orientation | `docs/CURRENT_RENDERING_DOCTRINE.md` | One-page “where we are now” |
  - | Experience tone | `docs/ux_principles_and_emotional_tone.md`, `docs/brand_and_experience_foundations.md` | How the product *feels* |

### A.11 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PROJECT_CONTINUITY_INDEX.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 2667; SHA-12: `303dae8aa89c`; score: 86
- Key headings: Project Continuity Index; Canonical Governance Docs; Canonical Archaeology Docs; Canonical Renderer Doctrine Docs; Deferred Excellence; Validation Narratives; Continuity Volume Convention; Recommended Future-AI Ingestion Order
- Requirement signals:
  - Purpose: short entry point for future AI/human rehydration. This file points to canonical governance, archaeology, renderer, deferred-excellence, and validation memory without replacing those sources.
  - - `validation/narratives/renderer_readiness_decision_gate.md` — Phase 1.19 blocker taxonomy and anti-death-spiral doctrine.
  - - `memory_archaeology_raw/README.md` — raw intake rules.
  - ## Canonical Renderer Doctrine Docs
  - - `docs/CURRENT_RENDERING_DOCTRINE.md` — fast orientation page.

### A.12 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 187
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Requirement signals:
  - # AI Interpretation Truthfulness Doctrine v1
  - **Scope:** Documentation only. Defines interpretive discipline, forbidden patterns, and a future review architecture. **No AI implementation in dumb Web 2.0 v1.**
  - - `docs/ai_constitution_and_review_architecture.md` — layered governance, anti-patterns, reviewer duties
  - - `docs/constitutional/professional_trust_and_ai_behavior_doctrine.md` — propose vs declare, layer sovereignty
  - **Filename convention:** Dated doctrine docs put the date at the **end** of the filename.

### A.13 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai_constitution_and_review_architecture.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 13119; SHA-12: `d6ae8f16c65e`; score: 174
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Requirement signals:
  - **Doctrine stack (read before changing AI behavior):**
  - - **`docs/DOCTRINE_INDEX.md`** — canonical map of doctrine docs, stability, and reading order.
  - | **Preserve symbolic integrity** | Outputs must stay **accountable** to chart structure—not **rewritten** for likability. |
  - | **Align with project doctrine** | **Epistemic honesty**, **intentionality**, **symbolic constraints**, **non-interfering** UI, **mature** astrology—all **binding** on interpretive layers. |
  - **Non-goal:** Declaring the project “responsible AI” for external stakeholders. This file is **internal** architecture doctrine.

### A.14 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/client_chart_data_model_v1_2026-05-29.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 35789; SHA-12: `795365723409`; score: 147
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Requirement signals:
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`,…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`. Record management is **supporting infrastructure**, not the center of gravity.
  - │  · BehavioralEventLog (post-v1 optional — not required)       │

### A.15 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 20953; SHA-12: `db53e1e91227`; score: 100
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Requirement signals:
  - **ARCHITECTURE REVIEW — aligned with Map-First Product Doctrine (2026-05-31)**
  - **Date:** 2026-05-29 (original); **doctrine alignment:** 2026-05-31
  - **Governing doctrine:** `docs/constitutional/map_first_product_doctrine_v1.md` — supersedes dashboard-centric recommendations in v1.0–v1.1 of this review.
  - - `docs/architecture/client_chart_data_model_v1_2026-05-29.md` (data ownership authority)
  - - `docs/ux/2026-05-29_application_journey_architecture_v1.md` (screen/journey authority)

### A.16 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/brand_and_experience_foundations.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 94
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Requirement signals:
  - **Important:** The emotional and atmospheric goals below are **experiential design constraints**—they govern how future UX and rendering choices should **feel** and **function**. They are **not** marketing fluff; they are institutional memory for product judgm…
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).
  - The interface should **get out of the user’s way** emotionally: it **creates conditions for imagination** rather than **competing** with it.
  - - **Warm, safe containment:** The environment should feel like a **warm blanket** or **safe, contemplative room**—**breathable, calm, trustworthy, spacious, emotionally safe**—so users can **inhabit** it comfortably for **hours**.
  - - **Long sessions without fatigue:** Typography, color restraint, spacing, and low noise support **sustained** exploratory use; the product should feel like a **home** for serious play, not a sprint through a flashy demo.

### A.17 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/cartographic_language_and_city_rendering.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 18608; SHA-12: `33b4db97eb55`; score: 83
- Key headings: Cartographic language and city rendering; 0. Basemap or tile strategy change ⇒ full visual identity re-test; 1. Map label language vs app language; 2. Provider evaluation (map + search); 2.1 Dimensions to score (required for any serious comparison); 2.2 Qualitative stack comparison (high level); 2.3 “Extra hour” vs “multi-day / multi-week”; 2.4 Effort bands for “whole solution” slices; 2.5 GeoNames bridge first vs “long-term now”; 3. City visibility under overlays (hard constraint); 4. City density and ranking (rendering); 5. Clickability: city vs blank map
- Requirement signals:
  - **Out of scope:** Aspect-to-angle **glow/aura** (not implemented; do not conflate with city-layer work).
  - **Institutional rule:** If the team changes **map provider**, **tile format** (raster → vector, host swap, style swap), or **label policy**, we must **re-validate the whole visual system**—not assume the current look “carries over.”
  - **Re-test checklist (non-exhaustive):**
  - | **Light / dark theme** | **Do not** assume one overlay palette works; plan **paired tokens** when dark mode is real. |
  - **Doctrine:** **Do not assume the current palette survives a map-provider change.** Promote tuned values only after **documented** QA pass (screenshots, overlap cases, polar/dateline, international sample).

### A.18 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/README.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 61
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - # Doctrine Categories
  - These documents are binding. They should not receive tentative status headers.
  - - `layer_sovereignty_and_forbidden_crossings.md`

### A.19 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ai_conversational_modes.md`
- Categories: authority_doctrine, ai_alignment, rollback_risk, architecture_enforcement
- Characters: 2887; SHA-12: `b796e2065486`; score: 34
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Requirement signals:
  - - canonical architectural principles,
  - This document should be periodically reviewed and updated as:
  - # Core Principle
  - The AI should adapt conversational style without violating constitutional doctrine.
  - The AI should remain:

### A.20 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/constitutional_ingestion_checklist.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 65
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Requirement signals:
  - # Constitutional Ingestion Checklist
  - - track doctrine ingestion,
  - Update this document whenever:
  - - doctrine evolves,
  - This project contains multiple categories of doctrine:

### A.21 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/conversational_discovery_and_intentionality.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 4218; SHA-12: `c7b5d8b9fc8e`; score: 19
- Key headings: Conversational Discovery And Intentionality; Status; Purpose; Core Principle; User intentionality is sovereign.; Intentionality Discovery; Examples; Archetypal Exploration; Example Exploratory Style; Intentionality Strength; Examples; Layer Relationship
- Requirement signals:
  - The principles of:
  - This document defines how the platform should:
  - The system should feel:
  - # Core Principle
  - The system must:

### A.22 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/epistemic_integrity_and_symbolic_humility.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk
- Characters: 3739; SHA-12: `242cc62cfae5`; score: 28
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior; Good Behavior; Collaborative Discovery
- Requirement signals:
  - - and anti-bullshit doctrine.
  - All AI and interpretive systems must follow these principles.
  - This document establishes the philosophical and operational rules governing:
  - The system must prefer:
  - # Core Principle

### A.23 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/future_excellence_vs_future_feature_excellence.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 45
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Requirement signals:
  - - canonical architectural principles,
  - This document should be periodically reviewed for:
  - # Core Principle
  - ## Infrastructure excellence and feature excellence must remain distinct.
  - - rollback safety,

### A.24 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/implementation_governance_and_ai_workflow_protocol.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3988; SHA-12: `b127e5c52050`; score: 66
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Requirement signals:
  - - rollback protocol,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - - rollback-safe,
  - # Core Principle

### A.25 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer4_optimization_and_exploration_doctrine.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 4341; SHA-12: `289b4552320f`; score: 30
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Requirement signals:
  - # Layer 4 Optimization And Exploration Doctrine
  - - canonical Layer 4 principles,
  - This document should be periodically reviewed for:
  - Layer 4 systems require especially careful constitutional auditing.
  - # Core Principle

### A.26 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer_sovereignty_and_forbidden_crossings.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 45
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Requirement signals:
  - # Layer Sovereignty And Forbidden Crossings
  - These rules are mandatory architectural constraints.
  - - forbidden crossings,
  - - contamination risks,
  - - and trust failure.

### A.27 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layered_symbolic_intelligence_architecture.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4801; SHA-12: `5242de0598f3`; score: 26
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Requirement signals:
  - All future systems must respect:
  - - forbidden crossings,
  - # Core Principle
  - ## Higher layers may NEVER rewrite lower layers.
  - Interpretation never flows downward.

### A.28 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/map_first_product_doctrine_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 73
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Requirement signals:
  - # Map-First Product Doctrine v1
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - Both are **primary surfaces**. The Chart Page must not become an afterthought.
  - # Map doctrine

### A.29 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/mvp_beta_and_future_feature_roadmap.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4767; SHA-12: `c904d8af5d1e`; score: 41
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes; Stage 2 — Professional Beta; Goal
- Requirement signals:
  - not immutable constitutional doctrine.
  - This roadmap should be periodically reviewed for:
  - # Core Principle
  - The MVP should prioritize:
  - The early product should primarily support:

### A.30 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: authority_doctrine, ai_alignment, rollback_risk, architecture_enforcement
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 35
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Requirement signals:
  - - canonical architectural principles,
  - This document should be periodically reviewed and updated as:
  - # Core Principle
  - Truth computation must remain independent from symbolic interpretation systems.
  - - aspect doctrines,

### A.31 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_mode_vs_lay_mode_strategy.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3492; SHA-12: `c166907d611f`; score: 35
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Requirement signals:
  - Core principles are canonical.
  - This document should be periodically reviewed for:
  - Interaction models should evolve carefully.
  - # Core Principle
  - ## The platform should remain professionally trustworthy while still accessible to non-professionals.

### A.32 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_trust_and_ai_behavior_doctrine.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 74
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Requirement signals:
  - # Professional Trust And AI Behavior Doctrine
  - This document defines how AI systems inside the platform must behave.
  - The AI must never behave like:
  - # Core Principle
  - This principle is absolute.

### A.33 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/purification_audit_framework.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 3639; SHA-12: `a43528565790`; score: 49
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Requirement signals:
  - # Purification Audit Framework
  - - purification audits,
  - - and rollback discipline.
  - Purification audits are mandatory maintenance mechanisms.
  - - or violate constitutional doctrine.

### A.34 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/relocation_strategy_framework.md`
- Categories: authority_doctrine, ai_alignment, rollback_risk, architecture_enforcement
- Characters: 2978; SHA-12: `5542c6b3c8b9`; score: 17
- Key headings: Relocation Strategy Framework; Status; Purpose; Core Principle; Subtractive relocation comes before additive optimization.; Subtractive Relocation; Additive Relocation; Strong Relocations Often Do Both; Tradeoff Reality; Archetypes Are Contextual; Optimization Delusion; Layer 4 Behavior
- Requirement signals:
  - - canonical architectural principles,
  - This document should be periodically reviewed and updated as:
  - # Core Principle
  - Optimization should remain:
  - The platform should avoid:

### A.35 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_and_renderer_sovereignty.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3826; SHA-12: `edda50b52a22`; score: 29
- Key headings: Runtime And Renderer Sovereignty; Purpose; Core Principle; Rendering must never alter truth.; Runtime Sovereignty; Renderer Sovereignty; Hydration Boundaries; Sandbox Boundaries; Observer Limitations; Renderer Substrate Integrity; Progressive Refinement; Ambiguity And Implication
- Requirement signals:
  - - rollbackability,
  - # Core Principle
  - ## Rendering must never alter truth.
  - They do not compute symbolic reality.
  - They do not own:

### A.36 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_build_sequence_and_timeline.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4934; SHA-12: `12aea4343437`; score: 43
- Key headings: Runtime Build Sequence And Timeline; Status; Maintenance Notes; Purpose; Core Principle; Build irreversible foundations first.; Phase Family 1 — Truth And Runtime Foundation; Goal; Includes; Status; Phase Family 2 — Renderer Reintegration; Goal
- Requirement signals:
  - not immutable doctrine.
  - This document should be periodically reviewed for:
  - # Core Principle
  - The system should:
  - - and rollback safety.

### A.37 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/symbolic_language_style_guide.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 1703; SHA-12: `11e6dd9bdb1a`; score: 12
- Key headings: Symbolic Language Style Guide; Purpose; Core Principle; Preferred Style; Avoid; Good Examples; Bad Examples; Archetypal Precision; Symbolic Humility; Constitutional Goal
- Requirement signals:
  - This document defines how symbolic language should be expressed by the platform.
  - # Core Principle
  - The system should sound:
  - It should not sound:
  - - and fake spiritual authority.

### A.38 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3360; SHA-12: `554add110fa4`; score: 30
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Requirement signals:
  - - orb doctrines,
  - # Important Principle
  - ## Truth must remain sovereign.
  - but may never rewrite truth.
  - # Another Important Principle

### A.39 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_app_shell_handoff_audit_v1_2026-05-30.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 16528; SHA-12: `a7754235e25c`; score: 77
- Key headings: Genie → App Shell Handoff Audit v1; Status; Executive summary; A. Current Genie contract; Emitter; Trigger; Payload shape (as implemented); Variable semantics (canonical); Output destinations today; Not emitted / not connected; B. Current app shell contract; Navigation context (in-app)
- Requirement signals:
  - # Genie → App Shell Handoff Audit v1
  - **AUDIT ONLY** — read-only gap analysis. No redesign, no implementation.
  - **Scope:** What Genie emits today, what app shell and map expect today, and what adapter/transport is required to connect them.
  - **Three distinct states (do not conflate):**
  - There is **zero wired handoff** between Genie and app shell, or between shell navigation and automatic Genie search on map load. `legacyCompatibility` is emitted for diagnostics; map engine adapter **must not** use it as execution input.

### A.40 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_render_payload_v1_2026-05-30.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, architecture_enforcement
- Characters: 27674; SHA-12: `7e997018eed9`; score: 106
- Key headings: Genie Render Payload Contract v1; Status; Purpose; Architectural doctrine; Language stability doctrine; Principles; Therefore; Top-level payload; Field notes; Render immutability; Future references (not defined here); Variable object
- Requirement signals:
  - **Scope:** Documentation / contract only. Defines shape, semantics, legacy adapter rules, and examples. Not implementation.
  - The Genie editor may hold **live, mutable card state**. Render freezes that state once. Downstream systems must treat the rendered payload as authoritative for “what was searched,” not the live card DOM.
  - # Architectural doctrine
  - | Rule | Meaning |
  - | **Do not force Genie into old slots** | The editor is not limited to three planet-house rows. Canonical payload may exceed legacy capacity. |

### A.41 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/variable_card_language_v1_2026-05-30.md`
- Categories: authority_doctrine, ai_alignment, architecture_enforcement
- Characters: 15184; SHA-12: `bde701502163`; score: 62
- Key headings: Variable Card Language Contract v1; Status; Purpose; Core doctrine; Canonical internal type IDs; Language registry concept; Composition rule; Registry ownership; Snapshot rule (Saved Explorations); Beta display label candidates; `planet_in_house`; `angle_in_sign`
- Requirement signals:
  - - `docs/contracts/genie_render_payload_v1_2026-05-30.md` — stable type ids, `variables[].label` snapshots, language stability doctrine
  - # Core doctrine
  - | Principle | Meaning |
  - | **Stable IDs are canonical** | `planet_in_house`, registry ids (`sun`, `ASC`, `trine`), and payload fields are the source of truth — never derived from display strings. |
  - | **User-facing labels must be modular / configurable** | UI reads from a language registry (or equivalent config), not string literals scattered in renderers. |

### A.42 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/current_sidebar_ux_audit.md`
- Categories: ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 4992; SHA-12: `c07666b5828f`; score: 8
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces; 9. Condition model — **next structural UX step (documented)**; 10. Location search placement (documented)
- Requirement signals:
  - # Current Sidebar / Map UX Audit
  - - Fixed panel still trades width vs map; **reset control** mitigates **lost world** after heavy panning.
  - - **`#renderStatus` / `#debugStatus`:** gated on `?debugGeometry` — unchanged.
  - **Behavior goal:** first row may default to planet-in-house, but users should eventually run **only** angle-in-sign or **only** aspect-to-angle without dummy planet rows.
  - **Engineering note:** needs coordinated **API/payload** and validation work later—**do not** half-migrate UI alone.

### A.43 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/local_first_data_objects_v1.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 8758; SHA-12: `90256838acac`; score: 61
- Key headings: Local-First Data Objects v1; Status; Purpose; Architectural boundary; Entity glossary; ProfessionalAccount; Client; BirthProfile; RelocatedChart (future durable object); Place; FavoriteCity; OverlayCondition
- Requirement signals:
  - Defines **product-layer entities**, **persistence boundaries**, and **local-first scaffold rules**. Not a database schema. Not implementation.
  - │  RENDERER / DISPLAY (never persisted as truth)            │
  - | `createdAt`, `updatedAt` | Audit |
  - | `confidenceTier` | See birth-time doctrine |
  - | `layer1SnapshotHash` | Optional — detect when recompute required |

### A.44 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/supabase_schema_sandbox_plan_v1.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 16155; SHA-12: `8fac31540a5b`; score: 31
- Key headings: Supabase Schema Sandbox Plan v1; Status; Explicit non-goals (current phase); Architectural boundary; 1. Proposed table list; 2. Columns per table; `professional_accounts`; `clients`; `birth_profiles`; `places`; `saved_charts`; `saved_investigations`
- Requirement signals:
  - **Reads with:** `docs/data_model/local_first_data_objects_v1.md`, `docs/future/birth_time_uncertainty_and_confidence_doctrine.md`, `validation/narratives/phase2_3_saved_investigation_replay.md`, `library/library.json` (legacy scaffold).
  - ## Explicit non-goals (current phase)
  - │  RENDERER / DISPLAY (never persisted as truth)          │
  - | `utc_offset_at_birth_minutes` | `integer` NULL | audit / DST edge cases |
  - | `confidence_tier` | `text` NOT NULL | `T0`–`T4`; see birth-time doctrine |

### A.45 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/design/brand_visual_language_and_design_doctrine.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 55
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Requirement signals:
  - # Brand, Visual Language, and Design Doctrine
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - | **Fantasy** | Allowed in user meaning-making; forbidden in fake certainty |
  - | **Export** | Must declare tier (exploration vs authoritative) |
  - ### Principles

### A.46 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 69
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Requirement signals:
  - # Birth Time Uncertainty and Confidence Doctrine
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `v…
  - - AI intake may help later — **MVP must handle tiers without AI**.
  - ## Core principle
  - The system must:

### A.47 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/layer5_experiential_education_through_travel_v1.md`
- Categories: authority_doctrine, ai_alignment, architecture_enforcement
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 42
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Requirement signals:
  - **Reads with (boundary context only):** `docs/ux/2026-05-29_application_journey_architecture_v1.md` §Future Rooms, `docs/constitutional/layer_sovereignty_and_forbidden_crossings.md`.
  - **Must not be read as:** screen spec, sprint backlog, course marketplace brief, or Layer 1–3 implementation requirement.
  - | Notice what changed when you relocated or slowed down | Memorize rules without location context |
  - Reading may support the journey — glossaries, brief context, safety notes — but **reading is never the main pedagogical engine**. The main engine is **lived geographic comparison** grounded in the same factual substrate the professional instrument provides.
  - Curricula should **eventually** be personalized from:

### A.48 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_and_city_identity_strategy.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 42
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Requirement signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - **Related:** `memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `docs/geocoder_dataset_feasibility.md`, `docs/cartographic_language_and_city_rendering.md` (basemap change ⇒ **§0** full visual re-test), `docs/relocation_app_product_roadm…
  - ## 1. Doctrine: city search is core systems engineering
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`…
  - Current prototype list search (`cities.js`) is a **stand-in** only: **name, lat/lng, population (and minimal fields)**—**no reliable country/admin**, **no alternate names**, **no stable place IDs**, and **no** trustworthy global ranking (e.g. Paris, France vs …

### A.49 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_dataset_feasibility.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 16429; SHA-12: `6ba544bcfafd`; score: 40
- Key headings: Geocoder dataset feasibility (planning pass); 1. Summary recommendation; 2. Option-by-option evaluation; 2.1 GeoNames — `cities500` / `cities1000` / `allCountries`; 2.2 Natural Earth — populated places (`ne_10m_populated_places`); 2.3 Who’s On First (WOF); 2.4 Pelias / Geocode Earth (open-data stack vs hosted); 2.5 Mapbox / Google (hosted geocoding & Places); 3. Licensing notes (high level — verify before ship); 4. Rough import plan (GeoNames-first); 5. Data fields needed (canonical `Place` record); 6. Proposed ranking formula (v1 — heuristic, explainable)
- Requirement signals:
  - **Non-goals here:** Astrology/math/overlay changes; shipping a full geocoder integration; vendor contracts.
  - **Companion docs:** `docs/cartographic_language_and_city_rendering.md`, `docs/next_implementation_sequence.md` (Priority band 4), `validation/narratives/city_data_and_search_notes.md`.
  - **London vs Londonderry / Paris / Atlanta / Albany:** GeoNames gives **distinct rows** with different IDs and **country/admin**; failures are usually **search/ranking bugs**, not missing rows. Substring bugs are fixed in **application ranking + tokenization**,…
  - - **Concordances** let you keep **geonameid** for astro validation while storing **wof:id** as canonical app ID.
  - **Pelias (self-hosted):** Open-source (**MIT** per project documentation); aggregates **OpenStreetMap (ODbL)**, **GeoNames (CC-BY)**, **Who’s On First**, **OpenAddresses** (per-jurisdiction licenses), **US TIGER**, etc. **Attribution and share-alike** obligati…

### A.50 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/governance/anti_cursor_bullshit_governance_rules.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 144
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Requirement signals:
  - # Anti-Cursor Bullshit Governance Rules
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountabilit…
  - 3. **rollback path** — how to revert,
  - | Rule | Rationale |

### A.51 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_memory_synthesis.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 16257; SHA-12: `04f378dc370d`; score: 184
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Requirement signals:
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.
  - **Orientation index (all doctrine files, pacing, reading order):** `docs/DOCTRINE_INDEX.md`
  - **Institutional maintenance (cadence, uncertainty, archaeology pipeline, AI drift audit):** `docs/process/`
  - **Implementation review guardrails (questions, exceptions):** `docs/review_contracts_and_governance.md`

### A.52 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_philosophical_synthesis.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 241
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Requirement signals:
  - **Status:** Foundational doctrine for **future training**, **reviewer systems**, **UX design**, **product strategy**, **conversational architecture**, and **interpretive governance**.
  - **Authority:** Synthesizes durable texts in `ai_context/`, `docs/`, and `memory_archaeology_raw/consolidated_notes/`. It **does not** supersede those sources on technical implementation; it **weaves** them into one training-readable whole.
  - Underneath lies a technical moral that keeps philosophy honest: **inspectable precision**. If the map shows a region or line, it must mean something **precise** in the relocated model. “Plausible-looking geometry” is not validation. **False membership** is rej…
  - **Practical implication:** Institutional decisions should always ask two questions: (1) Does this preserve **symbolic and mathematical integrity** at the point of contact with the user? (2) Does this preserve **room for the user’s intention, biography, and cul…
  - Popups are **dense shorthand**, not spreadsheet-on-map; they settle local truth **without** pretending to be the entire counseling session. Aura, gradients, and planned cusp softness are **display semantics** with strict contracts: they must **not** contradict…

### A.53 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/intentionality_and_symbolic_constraints.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 8365; SHA-12: `d1c233003983`; score: 81
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Requirement signals:
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite m…
  - **Companion doctrine (read together):**
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account): symbolic exploration on the map must stay **accountable** to structure.
  - - **`ai_context/memory_workflow.md`** — how proposals are reviewed and promoted so chat drift does not override this doctrine.

### A.54 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/map_and_overlay_design_research.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 5149; SHA-12: `f3943cdf7cf9`; score: 37
- Key headings: Map and Overlay Design Research; 1. Leaflet vs MapLibre vs Google Maps (philosophical comparison); 2. Current Leaflet strengths (for this codebase); 3. Actual blockers to watch for (hypothesis list—not confirmed); 4. Overlay transparency strategy (research directions); 5. Semantic overlap colors; 6. Aura rendering directions (non-commitments); 7. Map-edge and world-wrap ideas; 8. Dark / light mode implications; 9. Multilingual city rendering; 10. Decision rule (when to reopen migration); Related docs
- Requirement signals:
  - - Predefine **known pairings** (child colors) for 2-way overlaps; plan extension rules for 3+ without mud.
  - - **Future:** WebGL only if profiling proves need—**do not start** there for MVP experiments.
  - - **Display adapter** direction: fragments, world copies, stable feature IDs—research continues in `validation/narratives/leaflet_edge_and_wrap_notes.md`.
  - - Psychology: users should see **continuous cognitive space** even when implementation uses duplicates.
  - - Exclusion / NOT treatments must stay legible in both.

### A.55 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/next_implementation_sequence.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 10690; SHA-12: `ced0e563c90b`; score: 111
- Key headings: Next Implementation Sequence; Priority band 1 — UX polish (minimal architecture risk); Chunk 1.1 — Sidebar density and “debug vs ship” clarity; Chunk 1.2 — Popup and typography refinement; Chunk 1.3 — Native select stability + legend clutter reduction; Priority band 2 — Validator / stress tooling; Chunk 2.1 — Fixture manifest + “run these five” script; Chunk 2.2 — Latitude / polar stress suite expansion; Chunk 2.3 — Brute-force / truth export hygiene; Priority band 3 — Account + birth-data workflows; Chunk 3.1 — Birth data model (local-only MVP); Chunk 3.2 — Chart list + “open on map”
- Requirement signals:
  - Small, **low-risk**, **testable**, **isolated** chunks—ordered by current product priorities. This is **sequencing and planning only**, not a commitment to build everything listed.
  - ## Priority band 1 — UX polish (minimal architecture risk)
  - - **Validation:** Visual pass; confirm map remains primary; no regression on popup/dropdown behavior.
  - - **UX risks:** Hiding too much—power users lose discoverability. Mitigation: progressive disclosure, keep debug behind explicit mode.
  - - **Architecture risks:** Low if changes stay presentational.

### A.56 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 181
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Requirement signals:
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_an…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - Users should feel they are **exploring places and possibilities**, not managing software. Every screen earns its place by advancing that journey or by getting out of the way.
  - **Product identity (2026-05-31):** See `docs/constitutional/map_first_product_doctrine_v1.md`. The app is a **relocation discovery instrument** — not a CRM, SaaS dashboard, or record-management platform with a map attached. **Center of gravity:** Map → Analysi…

### A.57 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 289
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Requirement signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.…

### A.58 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/README.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 61
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - # Doctrine Categories
  - These documents are binding. They should not receive tentative status headers.
  - - `layer_sovereignty_and_forbidden_crossings.md`

### A.59 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 145
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Requirement signals:
  - - the authority when UX behavior is ambiguous
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - **Reads with (secondary):** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` (indexed catalog), `docs/constitutional/map_first_product_doctrine_v1.md`, journey and workflow architecture docs.
  - ### Principle

### A.60 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 302
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Requirement signals:
  - # UX Doctrine Master
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.
  - - `docs/constitutional/map_first_product_doctrine_v1.md`

### A.61 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 35789; SHA-12: `795365723409`; score: 147
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Requirement signals:
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`,…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`. Record management is **supporting infrastructure**, not the center of gravity.
  - │  · BehavioralEventLog (post-v1 optional — not required)       │

### A.62 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 8365; SHA-12: `d1c233003983`; score: 81
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Requirement signals:
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite m…
  - **Companion doctrine (read together):**
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account): symbolic exploration on the map must stay **accountable** to structure.
  - - **`ai_context/memory_workflow.md`** — how proposals are reviewed and promoted so chat drift does not override this doctrine.

### A.63 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 73
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Requirement signals:
  - # Map-First Product Doctrine v1
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - Both are **primary surfaces**. The Chart Page must not become an afterthought.
  - # Map doctrine

### A.64 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 60
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Requirement signals:
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.
  - **Must not contain:** activity feeds, recents, owner hero cards, favorites, charts, map as primary surface, widgets, metrics.

### A.65 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9566; SHA-12: `3de8663545ba`; score: 92
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Requirement signals:
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_l…
  - The workflow must remain **fully usable** without Astro Assist, scoring engines, or conversational intake.
  - ## Core workflow principle

### A.66 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3360; SHA-12: `554add110fa4`; score: 30
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Requirement signals:
  - - orb doctrines,
  - # Important Principle
  - ## Truth must remain sovereign.
  - but may never rewrite truth.
  - # Another Important Principle

### A.67 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/DOCTRINE_INDEX.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 289
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Requirement signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.…

### A.68 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/README.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 61
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - # Doctrine Categories
  - These documents are binding. They should not receive tentative status headers.
  - - `layer_sovereignty_and_forbidden_crossings.md`

### A.69 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_CONSTITUTION.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 145
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Requirement signals:
  - - the authority when UX behavior is ambiguous
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - **Reads with (secondary):** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` (indexed catalog), `docs/constitutional/map_first_product_doctrine_v1.md`, journey and workflow architecture docs.
  - ### Principle

### A.70 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_DOCTRINE_MASTER.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 302
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Requirement signals:
  - # UX Doctrine Master
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.
  - - `docs/constitutional/map_first_product_doctrine_v1.md`

### A.71 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/constitutional_summary.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4609; SHA-12: `8238f401edb1`; score: 53
- Key headings: Constitutional Summary; Purpose; Layer Architecture; Layer 1 - Truth; Layer 2 - Symbolic Ontology; Layer 3 - Intentional Interpretation; Layer 4 - Exploratory Optimization; Forbidden Crossings; Epistemic Doctrine; Runtime And Renderer Sovereignty; Purification Principle; Professional Trust And AI Behavior
- Requirement signals:
  - Layer 1 is deterministic, inspectable, objective, and independently verifiable. It must not interpret, optimize, moralize, psychologically frame, or alter truth to satisfy user desire.
  - - orb doctrines,
  - Layer 2 may interpret truth through a declared symbolic framework, but it may never rewrite geometry. Symbolic systems may disagree; no ontology is permanently privileged as universal truth.
  - Layer 3 is collaborative, conversational, probabilistic, and user-intent driven. It may clarify and compare, but it must not fabricate certainty, manipulate the user, or alter Layer 1 truth or Layer 2 definitions.
  - Layer 4 is invitation-sensitive and subordinate to Layer 3 intentionality. It may suggest and compare, but must not hijack, pressure, impose symbolic agendas, or turn optimization into destiny theater.

### A.72 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/epistemic_integrity_and_symbolic_humility.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk
- Characters: 3739; SHA-12: `242cc62cfae5`; score: 28
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior; Good Behavior; Collaborative Discovery
- Requirement signals:
  - - and anti-bullshit doctrine.
  - All AI and interpretive systems must follow these principles.
  - This document establishes the philosophical and operational rules governing:
  - The system must prefer:
  - # Core Principle

### A.73 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/intentionality_and_symbolic_constraints.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 8365; SHA-12: `d1c233003983`; score: 81
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Requirement signals:
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite m…
  - **Companion doctrine (read together):**
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account): symbolic exploration on the map must stay **accountable** to structure.
  - - **`ai_context/memory_workflow.md`** — how proposals are reviewed and promoted so chat drift does not override this doctrine.

### A.74 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layer_sovereignty_and_forbidden_crossings.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3715; SHA-12: `76af8fdb4707`; score: 45
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.; Forbidden Crossing #2; Layer 3 may NOT fabricate symbolic meaning.
- Requirement signals:
  - # Layer Sovereignty And Forbidden Crossings
  - These rules are mandatory architectural constraints.
  - - forbidden crossings,
  - - contamination risks,
  - - and trust failure.

### A.75 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layered_symbolic_intelligence_architecture.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4801; SHA-12: `5242de0598f3`; score: 26
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.; Layer 1 Characteristics; Examples
- Requirement signals:
  - All future systems must respect:
  - - forbidden crossings,
  - # Core Principle
  - ## Higher layers may NEVER rewrite lower layers.
  - Interpretation never flows downward.

### A.76 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/map_first_product_doctrine_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 73
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Requirement signals:
  - # Map-First Product Doctrine v1
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - Both are **primary surfaces**. The Chart Page must not become an afterthought.
  - # Map doctrine

### A.77 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3360; SHA-12: `554add110fa4`; score: 30
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Requirement signals:
  - - orb doctrines,
  - # Important Principle
  - ## Truth must remain sovereign.
  - but may never rewrite truth.
  - # Another Important Principle

### A.78 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/2026-05-29_application_journey_architecture_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 181
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Requirement signals:
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_an…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - Users should feel they are **exploring places and possibilities**, not managing software. Every screen earns its place by advancing that journey or by getting out of the way.
  - **Product identity (2026-05-31):** See `docs/constitutional/map_first_product_doctrine_v1.md`. The app is a **relocation discovery instrument** — not a CRM, SaaS dashboard, or record-management platform with a map attached. **Center of gravity:** Map → Analysi…

### A.79 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/PLAIN_LANGUAGE_PRODUCT_EXPLANATION_v1_2026-06-01.md`
- Categories: ai_alignment, workflow_process
- Characters: 6093; SHA-12: `0c7a9042f0a5`; score: 8
- Key headings: Plain Language Product Explanation; What Problem Does The Product Solve?; Why Relocation Astrology Is Geographic; Why The Map Is The Primary Discovery Instrument; What Overlays Represent; Why Cities Are Not The Primary Object Of Analysis; Natal Chart; Current Location Chart; Candidate Location Chart; Favorites; Saved Searches; Comparison
- Requirement signals:
  - - investigate cities
  - The software should help users discover meaningful astrological geography.
  - It should not pretend to know what choices they should make.

### A.80 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_constitution_and_review_architecture.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 13121; SHA-12: `96b9567947d8`; score: 174
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal); 10. Relationship to future professional workflows; Review contract (summary)
- Requirement signals:
  - **Doctrine stack (read before changing AI behavior):**
  - - **`docs/DOCTRINE_INDEX.md`** — canonical map of doctrine docs, stability, and reading order.
  - | **Preserve symbolic integrity** | Outputs must stay **accountable** to chart structure—not **rewritten** for likability. |
  - | **Align with project doctrine** | **Epistemic honesty**, **intentionality**, **symbolic constraints**, **non-interfering** UI, **mature** astrology—all **binding** on interpretive layers. |
  - **Non-goal:** Declaring the project “responsible AI” for external stakeholders. This file is **internal** architecture doctrine.

### A.81 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 22169; SHA-12: `b7b7a39122bb`; score: 187
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit; Not allowed — prediction or guarantee; Required distinction: pattern language vs outcome language
- Requirement signals:
  - # AI Interpretation Truthfulness Doctrine v1
  - **Scope:** Documentation only. Defines interpretive discipline, forbidden patterns, and a future review architecture. **No AI implementation in dumb Web 2.0 v1.**
  - - `docs/ai_constitution_and_review_architecture.md` — layered governance, anti-patterns, reviewer duties
  - - `docs/constitutional/professional_trust_and_ai_behavior_doctrine.md` — propose vs declare, layer sovereignty
  - **Filename convention:** Dated doctrine docs put the date at the **end** of the filename.

### A.82 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 7243; SHA-12: `f8208d0d336f`; score: 69
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording; Natural language intake (future AI — not MVP); Timezone and DST (P3 product-critical)
- Requirement signals:
  - # Birth Time Uncertainty and Confidence Doctrine
  - **Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `v…
  - - AI intake may help later — **MVP must handle tiers without AI**.
  - ## Core principle
  - The system must:

### A.83 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_and_experience_foundations.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 12722; SHA-12: `d3afa8b142af`; score: 94
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles; “Instrument not dashboard”; “Beautiful but not performative”
- Requirement signals:
  - **Important:** The emotional and atmospheric goals below are **experiential design constraints**—they govern how future UX and rendering choices should **feel** and **function**. They are **not** marketing fluff; they are institutional memory for product judgm…
  - Companion: **`docs/visual_semantic_style_guide.md`** (visual epistemology and layer semantics), **`docs/ux_principles_and_emotional_tone.md`** (UX principles).
  - The interface should **get out of the user’s way** emotionally: it **creates conditions for imagination** rather than **competing** with it.
  - - **Warm, safe containment:** The environment should feel like a **warm blanket** or **safe, contemplative room**—**breathable, calm, trustworthy, spacious, emotionally safe**—so users can **inhabit** it comfortably for **hours**.
  - - **Long sessions without fatigue:** Typography, color restraint, spacing, and low noise support **sustained** exploratory use; the product should feel like a **home** for serious play, not a sprint through a flashy demo.

### A.84 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_visual_language_and_design_doctrine.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 7092; SHA-12: `cc31d7224c14`; score: 55
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing; Cusp vs aura (do not conflate); NOT / exclusion visual language
- Requirement signals:
  - # Brand, Visual Language, and Design Doctrine
  - **Reads with:** `docs/brand_and_experience_foundations.md`, `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/constitutional/symbolic_language_style_guide.md`.
  - | **Fantasy** | Allowed in user meaning-making; forbidden in fake certainty |
  - | **Export** | Must declare tier (exploration vs authoritative) |
  - ### Principles

### A.85 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/client_chart_data_model_v1_2026-05-29.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 35789; SHA-12: `795365723409`; score: 147
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Requirement signals:
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`,…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`. Record management is **supporting infrastructure**, not the center of gravity.
  - │  · BehavioralEventLog (post-v1 optional — not required)       │

### A.86 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/core_product_truths.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9535; SHA-12: `9d9048f7cab4`; score: 103
- Key headings: Core Product Truths; Astrology Truth; Inspectability; Map and Overlay UX; Product Experience; Visual / Semantic Product Identity; Emotionally non-interfering design (experiential constraints); Interpretive language and emotional transparency (doctrine); Interpretive integrity and archetypal honesty (doctrine); Development Discipline; Where the nuanced history lives
- Requirement signals:
  - These are durable principles that should survive individual implementation chunks, UI experiments, and future chat transitions.
  - - Map overlays must agree with point-and-click astrology truth.
  - - Popup point-truth validation is authoritative for local membership checks.
  - - Canonical backend truth must not be altered to satisfy frontend display constraints.
  - - Frontend wrapping, clipping, or rendering should never change logical astrology membership.

### A.87 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/geocoder_and_city_identity_strategy.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 7774; SHA-12: `1f2f2dd177f3`; score: 42
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data; 9. Current HTML prototype (honest subset); 10. Aspect / aura
- Requirement signals:
  - **Status:** Product doctrine + implementation roadmap. **Not** a commitment to a specific vendor or schema until Chunk 4.x in `docs/next_implementation_sequence.md` is executed.
  - **Related:** `memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `docs/geocoder_dataset_feasibility.md`, `docs/cartographic_language_and_city_rendering.md` (basemap change ⇒ **§0** full visual re-test), `docs/relocation_app_product_roadm…
  - ## 1. Doctrine: city search is core systems engineering
  - **City search and stable place identity are not “secondary polish.”** Relocation work is **named-place** work (`memory_archaeology_raw/consolidated_notes/geocoder_and_city_strategy.md`, `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md`…
  - Current prototype list search (`cities.js`) is a **stand-in** only: **name, lat/lng, population (and minimal fields)**—**no reliable country/admin**, **no alternate names**, **no stable place IDs**, and **no** trustworthy global ranking (e.g. Paris, France vs …

### A.88 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/map_drawer_and_layer_control_doctrine.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 7226; SHA-12: `181a6ad8f6bd`; score: 47
- Key headings: Map Drawer and Layer Control Doctrine; Status; Purpose; Control hierarchy (map screen); Drawer architecture (target); Zones; Genie-into-corner collapse; Deferral (current phase); Condition editor doctrine; Target model; Card visual language; Search action
- Requirement signals:
  - # Map Drawer and Layer Control Doctrine
  - **Reads with:** `docs/overlay_and_aura_visual_strategy.md` §H, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/visual_semantic_style_guide.md` §9, `docs/product_workflows/product_screen_and_transition_architecture.md`.
  - Keep the **map sacred**. Controls must:
  - **Rule:** if a control hides coastlines, labels, or overlap evidence, it fails.
  - **Non-goals:** gimmick animations, physics toys, hidden controls with no restore.

### A.89 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/product_screen_and_transition_architecture.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 60
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Requirement signals:
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.
  - **Must not contain:** activity feeds, recents, owner hero cards, favorites, charts, map as primary surface, widgets, metrics.

### A.90 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_mode_vs_lay_mode_strategy.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3492; SHA-12: `c166907d611f`; score: 35
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role; Lay / Explorer Mode; Purpose
- Requirement signals:
  - Core principles are canonical.
  - This document should be periodically reviewed for:
  - Interaction models should evolve carefully.
  - # Core Principle
  - ## The platform should remain professionally trustworthy while still accessible to non-professionals.

### A.91 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_non_ai_workflow_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9566; SHA-12: `3de8663545ba`; score: 92
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Requirement signals:
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_l…
  - The workflow must remain **fully usable** without Astro Assist, scoring engines, or conversational intake.
  - ## Core workflow principle

### A.92 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_trust_and_ai_behavior_doctrine.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4267; SHA-12: `0c22e1113b72`; score: 74
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience; Professional Posture; AI Must Respect Layer Sovereignty
- Requirement signals:
  - # Professional Trust And AI Behavior Doctrine
  - This document defines how AI systems inside the platform must behave.
  - The AI must never behave like:
  - # Core Principle
  - This principle is absolute.

### A.93 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_workflow_and_explanatory_language.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 11541; SHA-12: `1814ff883a7c`; score: 51
- Key headings: Professional Workflow And Explanatory Language; Status; Purpose; Professional Map Workflow; Desired Placement Search; Exclude / NOT Variables; Solo And Mute Controls; Inspection Workflow; Helper Layers; Intention Remains Primary; Astro Assist Substitution Guidance; Additive And Subtractive Relocation
- Requirement signals:
  - This is NOT constitutional doctrine.
  - Update this document whenever product explanation language, professional workflow guidance, or popup copy concepts are clarified.
  - This document preserves explanatory language and professional workflow doctrine for later use in:
  - Professionals should be able to:
  - The map should make it easy to see where desired conditions overlap.

### A.94 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ux_principles_and_emotional_tone.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4906; SHA-12: `3924025d2ba8`; score: 35
- Key headings: UX Principles and Emotional Tone; 1. Core temperament; 2. Map-first atmosphere; 3. Delight without spectacle; 4. Overlap readability philosophy; 5. Typography and color tone; 6. Layout cautions: drawer / genie / chrome; 7. Mobile and tablet; 8. When to stop designing; 9. Where philosophy is already strong in the repo; 10. Where philosophy could still drift; Related docs
- Requirement signals:
  - # UX Principles and Emotional Tone
  - A concise distillation of how the product should **feel** and **behave**. Complements `docs/relocation_app_product_roadmap.md` (strategy) and `docs/overlay_and_aura_visual_strategy.md` (visual planning).
  - | Principle | Meaning |
  - - **Professional trustworthiness:** numbers, regions, and overlaps must **mean** something inspectable; visual polish never substitutes for false certainty.
  - - **City readability priority:** candidate places must remain discoverable **under** overlays (see roadmap §4).

### A.95 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/visual_semantic_style_guide.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 9451; SHA-12: `93105f1b5ba9`; score: 66
- Key headings: Visual & Semantic Style Guide (Relocation Map System); 1. Visual epistemology (truth hierarchy); 2. House field semantics (categorical + cusp softness); 3. Aspect-to-angle aura semantics (intensity, not category); 4. Overlay texture semantics (almost subconscious); 5. NOT / exclusion overlays; 6. Color philosophy; 7. Popup visual language; 8. Interface tone; 9. Map and control relationship; 10. Account / chart page relationship; 11. Implementation discipline
- Requirement signals:
  - **Status:** Planning and doctrine. This document defines **what visuals mean** and **how they should behave**. It does **not** mandate implementation order or ship dates.
  - **Companion docs:** `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/map_and_overlay_design_research.md`, `docs/brand_and_experience_foundations.md`, `docs/intentionality_and_symbolic_constraints.md` (fate/agency/tr…
  - **Discipline:** Future rendering work should follow this guide so the product does not drift toward **debuggy/generic** UIs or **beautiful-but-unusable** spectacle.
  - **Popups are appetizers, not full chart reports.** They must stay information-dense but **legible**; the heavy tables belong off-map.
  - **Direction:** City popup, right-click popup, favorites, and comparison snippets should **converge** on one typographic and labeling convention (headers, planet weight, house alignment).

### A.96 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ai_conversational_modes.md`
- Categories: authority_doctrine, ai_alignment, rollback_risk, architecture_enforcement
- Characters: 2887; SHA-12: `b796e2065486`; score: 34
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety; Deferred Excellence Notice; Maintenance Notes
- Requirement signals:
  - - canonical architectural principles,
  - This document should be periodically reviewed and updated as:
  - # Core Principle
  - The AI should adapt conversational style without violating constitutional doctrine.
  - The AI should remain:

### A.97 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/archaeology_and_synthesis_workflow.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9005; SHA-12: `d3add7674811`; score: 154
- Key headings: Archaeology and synthesis workflow; 1. Pipeline overview; 2. When to create an archaeology pass; 3. When to create or update synthesis docs; 4. Durable truths vs transient implementation; 5. How to avoid flattening nuance during synthesis; 6. Preserving contradictory but valuable tensions; 7. Doctrine canonicalization; 8. Open tension preservation; 9. Institutional memory updating (rhythm); 10. Governance refresh; 11. Review bundle generation
- Requirement signals:
  - **Reads with:** `ai_context/memory_workflow.md`, `docs/institutional_memory_synthesis.md`, `docs/project_memory_taxonomy.md`, `docs/process/doctrine_review_cycle.md`.
  - Raw capture → themed synthesis → doctrine canonicalization → open tension preservation
  - | **Raw capture** | `memory_archaeology_raw/pending_imports/` | Evidence, chronology, quotes, failure stories |
  - | **Canonical doctrine** | `docs/`, `ai_context/core_product_truths.md` | Slow law |
  - | **External audit package** | `docs/review_bundle/` | Snapshot copies + tensions summary |

### A.98 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/decision_and_uncertainty_framework.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9068; SHA-12: `4b8f251dada4`; score: 90
- Key headings: Decision and uncertainty framework; 1. Bounded uncertainty; 2. Heuristic vs exact truth; 3. Symbolic plausibility vs fake precision; 4. Exploratory guidance vs deterministic recommendation; 5. Preserving ambiguity intentionally; 6. Reversible decisions; 7. Experimentation doctrine; 8. User-facing confidence vs backend uncertainty; 9. “Good enough for exploration” vs “authoritative truth”; 10. Case study: aura philosophy; 11. Visual approximation doctrine
- Requirement signals:
  - **Reads with:** `docs/visual_semantic_style_guide.md` §1, `docs/overlay_and_aura_visual_strategy.md` (aura doctrine), `docs/intentionality_and_symbolic_constraints.md`, `docs/process/doctrine_review_cycle.md`.
  - | **Membership / math** (in house? on line?) | Drive toward **exact**, validated, inspectable answers; popup authority. |
  - | **Symbolic ambiguity** (paradox, multi-valence) | **Preserve intentionally**; do not force single verdict in software. |
  - **Bounded uncertainty** means: be precise where the engine is precise; be honest where the engine is silent; do not **smuggle certainty** through UI fluency or model confidence.
  - Some questions **should remain open** until practitioner feedback or long-session stress testing—not because the team is indecisive, but because **premature certainty** would lie.

### A.99 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/doctrine_review_cycle.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9902; SHA-12: `00598386986c`; score: 138
- Key headings: Doctrine review cycle; 1. What this cycle protects; 2. Slow docs policy; 3. Implementation vs philosophy separation; 4. Tension-preservation doctrine; 5. Rationale preservation rules (“why”, not just “what”); 6. Review cadences (suggested, not ceremonial); 6.1 Doctrine coherence review; 6.2 AI drift audit; 6.3 UX coherence review; 6.4 Archaeology / synthesis refresh; 6.5 Review bundle / external audit
- Requirement signals:
  - # Doctrine review cycle
  - **Reads with:** `docs/DOCTRINE_INDEX.md`, `docs/review_contracts_and_governance.md`, `docs/process/decision_and_uncertainty_framework.md`, `ai_context/memory_workflow.md`.
  - **Fast docs** govern **what is true now** and **how we ship**: `ai_context/current_state.md`, `ai_context/decisions.md`, validation narratives, tactical tuning notes.
  - **Rule:** Fast docs may **not contradict** slow docs without **updating slow docs** or recording a **time-bounded exception** in `ai_context/decisions.md` with rationale.
  - | Layer | May iterate quickly | Must stay accountable to |

### A.100 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/future_excellence_vs_future_feature_excellence.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3941; SHA-12: `46cc032cf2b8`; score: 45
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence; WHAT the system can eventually do.; Examples Of Future Feature Excellence
- Requirement signals:
  - - canonical architectural principles,
  - This document should be periodically reviewed for:
  - # Core Principle
  - ## Infrastructure excellence and feature excellence must remain distinct.
  - - rollback safety,

### A.101 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer4_optimization_and_exploration_doctrine.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 4341; SHA-12: `289b4552320f`; score: 30
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both; Intentionality Strength Matters; Exploration Modes
- Requirement signals:
  - # Layer 4 Optimization And Exploration Doctrine
  - - canonical Layer 4 principles,
  - This document should be periodically reviewed for:
  - Layer 4 systems require especially careful constitutional auditing.
  - # Core Principle

### A.102 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer5_experiential_education_through_travel_v1.md`
- Categories: authority_doctrine, ai_alignment, architecture_enforcement
- Characters: 7769; SHA-12: `9ca3e64754b9`; score: 42
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only); Relationship to Other Layers; Activation Criteria (Future — Not Current)
- Requirement signals:
  - **Reads with (boundary context only):** `docs/ux/2026-05-29_application_journey_architecture_v1.md` §Future Rooms, `docs/constitutional/layer_sovereignty_and_forbidden_crossings.md`.
  - **Must not be read as:** screen spec, sprint backlog, course marketplace brief, or Layer 1–3 implementation requirement.
  - | Notice what changed when you relocated or slowed down | Memorize rules without location context |
  - Reading may support the journey — glossaries, brief context, safety notes — but **reading is never the main pedagogical engine**. The main engine is **lived geographic comparison** grounded in the same factual substrate the professional instrument provides.
  - Curricula should **eventually** be personalized from:

### A.103 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/memory_workflow.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 6877; SHA-12: `0a90f034aa1f`; score: 112
- Key headings: Memory Maintenance Workflow; Purpose; Sources; Mining Old Chats; Processing Extraction Docs; Consolidating Raw Archaeology (optional phase); Updating Durable Memory; Memory Types; Raw Extraction; Durable Memory; Roadmap; Current Implementation State
- Requirement signals:
  - This document explains how project memory should be maintained without turning old chats, reports, and speculative ideas into an unstructured pile.
  - The goal is durable continuity. Cursor and external reviewers should be able to understand the product direction, current state, and important constraints without rereading every past chat.
  - **Institutional map (broader pipeline):** `docs/process/archaeology_and_synthesis_workflow.md` — raw → synthesis → doctrine → review bundle → rehydration. **Cadence:** `docs/process/doctrine_review_cycle.md`.
  - - Validation reports and narratives under `validation/`.
  - - Durable product principles.

### A.104 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/mvp_beta_and_future_feature_roadmap.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4767; SHA-12: `c904d8af5d1e`; score: 41
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes; Stage 2 — Professional Beta; Goal
- Requirement signals:
  - not immutable constitutional doctrine.
  - This roadmap should be periodically reviewed for:
  - # Core Principle
  - The MVP should prioritize:
  - The early product should primarily support:

### A.105 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: authority_doctrine, ai_alignment, rollback_risk, architecture_enforcement
- Characters: 3617; SHA-12: `f6bab89d14d7`; score: 35
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology; Professional Cookbook Systems; Plugin Safety
- Requirement signals:
  - - canonical architectural principles,
  - This document should be periodically reviewed and updated as:
  - # Core Principle
  - Truth computation must remain independent from symbolic interpretation systems.
  - - aspect doctrines,

### A.106 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_continuity_workflow.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 5184; SHA-12: `8a80bdfb8e6e`; score: 80
- Key headings: Project Continuity Workflow; 1. Goals; 2. Memory lanes (what goes where); 3. Archaeology intake workflow; 4. Consolidation workflow (when to run); 5. Reviewer workflow; 6. Proposed updates workflow; 7. Raw archaeology vs durable truths; 8. How future chats should initialize; 9. How to continue safely after context loss; 10. Related docs
- Requirement signals:
  - - **Clear separation:** raw archaeology vs curated principles vs implementation state.
  - | **Themed synthesis** | `memory_archaeology_raw/consolidated_notes/` | Onboarding-friendly themes; still subordinate to **human-reviewed** `ai_context/` for “current doctrine.” |
  - | **Durable truths** | `ai_context/core_product_truths.md`, `decisions.md`, `product_brief.md` | Stable principles and decisions. |
  - **Do not consolidate when:**
  - - Before verifying which backend/frontend entrypoints are actually running (**wrong-module** class of failure).

### A.107 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_memory_taxonomy.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 5641; SHA-12: `e630f6401456`; score: 79
- Key headings: Project Memory Taxonomy; Architecture; UX Philosophy; Visual doctrine vs rendering experiments vs temporary UX; Implementation State; Future Features; Rejected Approaches; Validation Methodology; Edge Cases; Unresolved Questions; AI Strategy; Product Philosophy
- Requirement signals:
  - This taxonomy keeps project memory organized as the app grows across chats, validation passes, experiments, and external reviews.
  - Stable experience principles and design constraints.
  - **Doctrine vs experiments:** Stable UX principles live here and in `ai_context/core_product_truths.md` (“Visual / Semantic Product Identity”). **Durable visual doctrine** (epistemology: what overlays *mean* vs what popups *prove*) is expanded in **`docs/visual…
  - ## Visual doctrine vs rendering experiments vs temporary UX
  - **Durable visual doctrine** — What should remain true across refactors:

### A.108 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ai_and_professional_workflow_strategy.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4077; SHA-12: `093c412a15e4`; score: 49
- Key headings: AI and Professional Workflow Strategy (From Archaeology); Institutional memory vs chat memory (anti–vibe-chaos); AI reviewer infrastructure (evolution); Non-negotiable product stance; AI collaboration failures as institutional risk; Second-opinion models; Practitioner assist vision (future); Consumer / intake AI (later); Strategic business hypotheses (treat as archaeology, not commitments); Tension to preserve
- Requirement signals:
  - **Anti–vibe-chaos principles** (from repeated archaeology):
  - - **Direction in archaeology:** reviewer prompts should carry **exact scripts, expected outputs, and hypotheses**; screenshots alone are fragile.
  - - **Non-AI / “dumb mode” remains sacred:** the app must be fully usable without automated interpretation—professional sovereignty matters ethically and commercially.
  - - **AI is augmentation, not authority:** aids with alternatives, intake translation, summaries—does not replace judgment.
  - ## AI collaboration failures as institutional risk

### A.109 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/current_sidebar_ux_audit.md`
- Categories: ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 4992; SHA-12: `c07666b5828f`; score: 8
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces; 9. Condition model — **next structural UX step (documented)**; 10. Location search placement (documented)
- Requirement signals:
  - # Current Sidebar / Map UX Audit
  - - Fixed panel still trades width vs map; **reset control** mitigates **lost world** after heavy panning.
  - - **`#renderStatus` / `#debugStatus`:** gated on `?debugGeometry` — unchanged.
  - **Behavior goal:** first row may default to planet-in-house, but users should eventually run **only** angle-in-sign or **only** aspect-to-angle without dummy planet rows.
  - **Engineering note:** needs coordinated **API/payload** and validation work later—**do not** half-migrate UI alone.

### A.110 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/foundational_product_truths.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 4380; SHA-12: `9c5286269c09`; score: 37
- Key headings: Foundational Product Truths (From Archaeology); Trust and truth; Overlap and decision-making; Precision vs cosmetics (non-negotiable vs acceptable); Separation of concerns (recurring architectural moral); Human + AI collaboration stance; Emotional tone and moat; Repetition as signal
- Requirement signals:
  - **Status labels:** *Durable principle* = should guide decisions for years. *Product stance* = strategic positioning. *Process principle* = how the team builds.
  - - **Durable principle — Inspectable precision:** If the map shows a region, line, or overlap, it must mean something **precise** in the relocated chart model. “Plausible geometry” is not validation. Trust is built through reproducible checks, not visual confid…
  - - **Durable principle — The map is the primary model (not an illustration):** Users explore **geography as astrology**. The map is not decoration around a chart calculator; it is the main instrument.
  - - **Durable principle — Professional rigor before lay simplification:** Build a **neutral, powerful professional engine first**; simplify for lay users only after the foundation is trustworthy.
  - - **Durable principle — Overlap is often the answer:** The deepest product value is where conditions coincide—house + house, house + angle sign, angle + aspect corridor, multi-condition intersection. Overlap is a **semantic object**, not a rendering accident.

### A.111 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_memory_synthesis.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 16257; SHA-12: `04f378dc370d`; score: 184
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine; 4. UX / design language; Visual-semantic system evolution
- Requirement signals:
  - - **Speculative:** valuable vision, monetization hypotheticals, or far-future modality—must not be mistaken for current product truth.
  - - **Workflow infrastructure:** how humans and AI maintain **persistent institutional memory**—review scripts, `proposed_updates/`, archaeology intake, validation dossiers. This is **process**, not product behavior in the app.
  - **Orientation index (all doctrine files, pacing, reading order):** `docs/DOCTRINE_INDEX.md`
  - **Institutional maintenance (cadence, uncertainty, archaeology pipeline, AI drift audit):** `docs/process/`
  - **Implementation review guardrails (questions, exceptions):** `docs/review_contracts_and_governance.md`

### A.112 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_philosophical_synthesis.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 27007; SHA-12: `d9ca2489a35d`; score: 241
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome; 4.2 Conversational pacing (human and AI); 4.3 Instrument, not dashboard
- Requirement signals:
  - **Status:** Foundational doctrine for **future training**, **reviewer systems**, **UX design**, **product strategy**, **conversational architecture**, and **interpretive governance**.
  - **Authority:** Synthesizes durable texts in `ai_context/`, `docs/`, and `memory_archaeology_raw/consolidated_notes/`. It **does not** supersede those sources on technical implementation; it **weaves** them into one training-readable whole.
  - Underneath lies a technical moral that keeps philosophy honest: **inspectable precision**. If the map shows a region or line, it must mean something **precise** in the relocated model. “Plausible-looking geometry” is not validation. **False membership** is rej…
  - **Practical implication:** Institutional decisions should always ask two questions: (1) Does this preserve **symbolic and mathematical integrity** at the point of contact with the user? (2) Does this preserve **room for the user’s intention, biography, and cul…
  - Popups are **dense shorthand**, not spreadsheet-on-map; they settle local truth **without** pretending to be the entire counseling session. Aura, gradients, and planned cusp softness are **display semantics** with strict contracts: they must **not** contradict…

### A.113 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/map_workspace_behavior_audit_v1_2026-05-30.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 15325; SHA-12: `7567f30ce7ff`; score: 103
- Key headings: Map Workspace Behavior Audit v1; Status; Purpose; Language and ID doctrine (applies to all sections); 1. Behavior already decided; Genie modes; Reasons to reopen Genie (decided intents); Search and render; Variable model; Legacy adapter (handoff to production map path); Map surface and overlay doctrine; Clear Map
- Requirement signals:
  - # Map Workspace Behavior Audit v1
  - **AUDIT** — records what is decided, partially decided, and undecided for the map workspace (Genie + map surface + exploration chrome).
  - - `docs/ui/map_drawer_and_layer_control_doctrine.md` — map-primary hierarchy (strategic)
  - This document does **not** add features, layouts, or architecture. It consolidates decisions already present in contracts and related doctrine.
  - # Language and ID doctrine (applies to all sections)

### A.114 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/open_questions_and_unresolved_areas.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3871; SHA-12: `c86a26458dc6`; score: 33
- Key headings: Open Questions and Unresolved Areas (From Archaeology); Geometry and calculation semantics; Rendering architecture; Validation systems; UX systems; Data + search; Product scope and ethics; Renderer beta stabilization questions (Chat 08); Operational workflow; Weak archaeology coverage (second pass, 2026-05); Human review gate
- Requirement signals:
  - - Formal spec for **MC** presentation: relocated ecliptic MC vs culmination/RA line products—must be explicit in user-facing language and internal tests.
  - ## Validation systems
  - - Automating regression: what becomes CI vs quarterly manual QA vs “validation dossier only.”
  - - Whether overlap hot zones should ever be highlighted by default, or only through explicit user-controlled modes.
  - - How public positioning should read: astrology-forward vs broader decision-intelligence framing.

### A.115 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/product_brief.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3080; SHA-12: `ba708a2f1745`; score: 36
- Key headings: Product Brief; Product; Current Core Capabilities; Product Philosophy; Overlay Truth Standard; Current Architecture Direction; Validation Corpus; Institutional memory (archaeology)
- Requirement signals:
  - The app should become a calm, premium, trustworthy instrument for exploration, not a cluttered dashboard.
  - - Controls should serve exploration, not dominate it.
  - - Users should enjoy spending time in the app.
  - - AI should support the professional core later, not replace it.
  - The app should not casually accept mathematical inaccuracies. Canonical backend geometry must be trustworthy and stable. Frontend wrapping, clipping, and display adaptation must never change logical astrology semantics.

### A.116 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/relocation_app_product_roadmap.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 27057; SHA-12: `24ab9bae5cb8`; score: 197
- Key headings: Relocation App Product Roadmap; 1. Current Stable Milestone; 2. Product Philosophy; 3. Core Search Types; 4. Overlay/Color System Roadmap; 5. Aspect Aura Roadmap; 6. UX/Layout Roadmap; 7. City Search / Geocoder Roadmap; 8. Birth Data / Accounts / Professional Mode Roadmap; Saved Object Taxonomy; Phase 2.4 Sampling / Cache Scaffold; Phase 2.5 Sampling / Cache Population Strategy
- Requirement signals:
  - This document preserves the current product strategy, development sequence, UX philosophy, and validation priorities for future work.
  - - Popup truth generally matches overlays in current validation.
  - - Validation contradictions are `0` in current truth-grid and angle-sign tests.
  - The app should be a map-first experience. The map is the product surface; controls exist to serve exploration, not dominate it.
  - Core principles:

### A.117 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ux_and_design_language.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 3849; SHA-12: `ac5f86eb3a13`; score: 24
- Key headings: UX and Design Language (From Archaeology); Map-first and spatial reading; Trust UX vs explanation UX; Typography and popups (professional validation patterns); Interaction pitfalls called out repeatedly; Emotional tone; Product positioning language (from archaeology); Tensions to preserve (not resolve here); Chat 08 update: style presets and mobile layer control
- Requirement signals:
  - - **Map dominance:** Controls exist to serve exploration; they must not steal the primary visual field during validation or professional use.
  - - **Global map ergonomics:** Users must pan freely near **Pacific/dateline/polar** regions during validation; artificial snap-back is disqualifying for this product class.
  - - **Lay users cannot be expected to reconcile** overlay edges with chart tables; that is a **developer failure mode**, not a user skill issue.
  - - **Professionals still need an oracle:** Right-click / precise coordinate inspection is framed as **truth instrumentation**. It must have onboarding (hint, mode toggle), and mobile needs long-press equivalent.
  - ## Typography and popups (professional validation patterns)

### A.118 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 20953; SHA-12: `db53e1e91227`; score: 100
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning; 3. Active-context doctrine; Session contract
- Requirement signals:
  - **ARCHITECTURE REVIEW — aligned with Map-First Product Doctrine (2026-05-31)**
  - **Date:** 2026-05-29 (original); **doctrine alignment:** 2026-05-31
  - **Governing doctrine:** `docs/constitutional/map_first_product_doctrine_v1.md` — supersedes dashboard-centric recommendations in v1.0–v1.1 of this review.
  - - `docs/architecture/client_chart_data_model_v1_2026-05-29.md` (data ownership authority)
  - - `docs/ux/2026-05-29_application_journey_architecture_v1.md` (screen/journey authority)

### A.119 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/00_OPERATOR_START_HERE.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 697; SHA-12: `a0e79ddfcf29`; score: 8
- Key headings: AI Onboarding Entry Point
- Requirement signals:
  - - Complete Product Comprehension Gate
  - Primary historical failure modes:
  - - repeating doctrine without understanding doctrine
  - Understanding must be demonstrated, not claimed.

### A.120 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_EVALUATION_LOG.md`
- Categories: ai_alignment, validation_gates
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.121 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/AI_WORKFLOW_GOVERNANCE.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 14272; SHA-12: `570f3cca823a`; score: 256
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives; Classification Rules; Mandatory Standard Prompt Footer
- Requirement signals:
  - This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in w…
  - Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisi…
  - ## Ghost Boss Governance Doctrine
  - Every phase closeout must ask whether it introduced or exposed:
  - * missing test, CI, regression, or rollback discipline;

### A.122 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/KILL_TEST.md`
- Categories: ai_alignment, validation_gates
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.123 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/PRODUCT_COMPREHENSION_GATE.md`
- Categories: ai_alignment, validation_gates
- Characters: 2; SHA-12: `75a11da44c80`; score: 0

### A.124 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/ai_drift_audit_framework.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9541; SHA-12: `889f1d9b2f3a`; score: 84
- Key headings: AI drift audit framework; 1. Healthy AI posture (target); 2. Audit dimensions and warning signs; 2.1 Excessive certainty; 2.2 Flattery; 2.3 Manipulative spirituality; 2.4 Optimization obsession; 2.5 Over-helpfulness; 2.6 Premature closure; 2.7 Reducing exploratory play; 2.8 Guru behavior; 2.9 Dependency framing
- Requirement signals:
  - # AI drift audit framework
  - **Status:** Meta-governance — reusable **audit checklist** for interpretive and assistive AI behavior over time.
  - **Reads with:** `docs/ai_constitution_and_review_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`, `docs/brand_and_experience_foundations.md`, `docs/process/doctrine_review_cycle.md`.
  - The model (or assist layer) should behave like:
  - - A **GPS recalculator** under constraints—not a prophet, not a therapist replacement, not a spiritual authority.

### A.125 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/anti_cursor_bullshit_governance_rules.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 8314; SHA-12: `790aab0faf7d`; score: 144
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX; Mandatory closeout (every significant task); Layer sovereignty quick check
- Requirement signals:
  - # Anti-Cursor Bullshit Governance Rules
  - Operational rules for **AI-assisted development** on this repository. Prevents vibe coding, fake certainty, hidden migrations, renderer panic, and documentation theater.
  - **Reads with:** `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/constitutional/implementation_governance_and_ai_workflow_protocol.md`, `docs/process/ai_drift_audit_framework.md`, `docs/review_contracts_and_governance.md`, `validation/narratives/phase3_26_accountabilit…
  - 3. **rollback path** — how to revert,
  - | Rule | Rationale |

### A.126 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/constitutional_ingestion_checklist.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3060; SHA-12: `3ace0cd9a495`; score: 65
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer; UX / Product Strategy Layer; Maintenance Requirements
- Requirement signals:
  - # Constitutional Ingestion Checklist
  - - track doctrine ingestion,
  - Update this document whenever:
  - - doctrine evolves,
  - This project contains multiple categories of doctrine:

### A.127 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/implementation_governance_and_ai_workflow_protocol.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3988; SHA-12: `b127e5c52050`; score: 66
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production; Smoke-First Development; Constitutional Enforcement
- Requirement signals:
  - - rollback protocol,
  - - and architectural governance rules.
  - All implementation systems and AI collaborators must follow these principles.
  - - rollback-safe,
  - # Core Principle

### A.128 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/purification_audit_framework.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, rollback_risk, architecture_enforcement
- Characters: 3639; SHA-12: `a43528565790`; score: 49
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks; Layer 4 Checks; Runtime Purity Checks
- Requirement signals:
  - # Purification Audit Framework
  - - purification audits,
  - - and rollback discipline.
  - Purification audits are mandatory maintenance mechanisms.
  - - or violate constitutional doctrine.

### A.129 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/04_ai_validation/review_contracts_and_governance.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 12252; SHA-12: `18cc9636738c`; score: 140
- Key headings: Review contracts and governance (implementation layer); 1. What a “review contract” is here; 2. Principles reviewers hold in tension; 3. Implementation review questions; 4. UX review questions; 5. AI behavior review questions; 6. Symbolic integrity review questions; 7. Exploratory and play preservation checks; 8. Anti-chaos visual checks; 9. Anti-guru and anti-coercion checks; 10. Does this preserve contemplative space?; 11. Intelligent exceptions (examples)
- Requirement signals:
  - **Status:** Lightweight operational doctrine—**not** a compliance checklist, **not** a substitute for judgment, **not** corporate policy theater.
  - **Reads with:** `docs/ai_constitution_and_review_architecture.md` (interpretive AI layers and anti-patterns), `docs/DOCTRINE_INDEX.md` (where each doctrine lives), `docs/institutional_philosophical_synthesis.md` (foundational synthesis for training), `docs/pro…
  - **Purpose:** give reviewers and implementers **shared guardrails** so work preserves **symbolic honesty, restraint, readability, agency, intentionality, exploratory freedom, professional seriousness, and emotional tone**—while still allowing **fast iteration**…
  - Contracts are **guardrails**, not formulas. They do not award points for mechanical compliance. A change can satisfy every literal question below and still be wrong in context—or violate one question deliberately for a **documented, rare, intelligent exception…
  - **Doctrine** (meaning, tone, truth hierarchy, interpretive ethics) should evolve **slowly** and with **explicit revision**. **Implementation** (controls, performance, map options, geocoder choice, rendering tactics) may iterate **rapidly**—as long as it **does…

### A.130 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 32245; SHA-12: `8ebf2b906395`; score: 181
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision; Discovery; Refinement
- Requirement signals:
  - **This is not implementation.** Routes, components, and visual polish must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/ui/map_drawer_an…
  - **AI boundary:** AI architecture exists elsewhere. This document describes the **standalone Web 2.0 product**. AI features may appear **only as future placeholders** and must **not** affect current screen design.
  - Users should feel they are **exploring places and possibilities**, not managing software. Every screen earns its place by advancing that journey or by getting out of the way.
  - **Product identity (2026-05-31):** See `docs/constitutional/map_first_product_doctrine_v1.md`. The app is a **relocation discovery instrument** — not a CRM, SaaS dashboard, or record-management platform with a map attached. **Center of gravity:** Map → Analysi…

### A.131 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 15975; SHA-12: `ffca0c0f93b1`; score: 289
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene; Implementation state and decisions (fast-moving); Review outputs and proposals (rotating)
- Requirement signals:
  - # Doctrine index
  - **Purpose:** One orientation page for future chats, agents, contributors, and reviewers. It answers: **which file is law for what**, **how fast it should change**, and **whether it is foundational meaning or implementation-facing**.
  - **How to use:** Start here when you are about to change behavior, copy, or visuals. Follow links; do not treat this index as the full text of any doctrine.
  - **Top UX authority:** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` is the consolidated UX Truth source (workflow, hierarchy, transformation). Mockup and UI work must consult it before proposing workflow changes.
  - **Top constitutional authority:** `docs/constitutional/` is now the primary constitutional doctrine namespace. New AI sessions should bootstrap from `ai_context/constitutional_summary.md`, `ai_context/current_project_state.md`, and `docs/constitutional/README.…

### A.132 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/README.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 2857; SHA-12: `1e003b635a0c`; score: 61
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - # Constitutional Doctrine Index
  - This directory contains the constitutional doctrine set for the Relocation App platform.
  - # Doctrine Categories
  - These documents are binding. They should not receive tentative status headers.
  - - `layer_sovereignty_and_forbidden_crossings.md`

### A.133 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 34207; SHA-12: `5e220ad77dad`; score: 145
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists; Required behaviors; Forbidden behaviors
- Requirement signals:
  - - the authority when UX behavior is ambiguous
  - **Parallel authority:** Geometry Truth governs calculations and relocation math. **UX Truth** governs what the product *is* and how it *behaves*. Neither may be violated for convenience.
  - **Supersedes:** When this constitution conflicts with older planning docs, mockup passes, or draft inventories, **this document wins**. Update downstream docs; do not reinterpret constitution to match legacy UI.
  - **Reads with (secondary):** `docs/product_doctrine/UX_DOCTRINE_MASTER.md` (indexed catalog), `docs/constitutional/map_first_product_doctrine_v1.md`, journey and workflow architecture docs.
  - ### Principle

### A.134 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, architecture_enforcement
- Characters: 52041; SHA-12: `85f4ed2fffef`; score: 302
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application; UX-D-008 — Map is primary; Genie is temporary; UX-D-009 — Search construction belongs to Genie; layer inspection belongs to Map
- Requirement signals:
  - # UX Doctrine Master
  - **Scope:** Product UX doctrine extracted from governance documents, journey architecture, map/chart/comparison workflow discussions, Genie discussions, mockup passes, and founder corrections. **Not implementation.**
  - **Parallel:** Geometry Truth governs calculations, validation, and relocation math. **UX Truth** governs workflow, hierarchy, and transformation. Mockups and UI must comply with UX Truth the same way code must comply with Geometry Truth.
  - **Usage:** Future mockup work and workflow proposals **must consult this document first**. Do not invent, optimize, or simplify workflow in mockups or implementation without updating this document.
  - - `docs/constitutional/map_first_product_doctrine_v1.md`

### A.135 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 35789; SHA-12: `795365723409`; score: 147
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases; Chart Record fields (conceptual); Optional demographic / profile metadata (future only)
- Requirement signals:
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`,…
  - Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.
  - - what must never be persisted as product truth,
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`. Record management is **supporting infrastructure**, not the center of gravity.
  - │  · BehavioralEventLog (post-v1 optional — not required)       │

### A.136 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 8365; SHA-12: `d1c233003983`; score: 81
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract
- Requirement signals:
  - **Status:** Durable **institutional philosophy** and **future AI-governance** doctrine.
  - **Purpose:** State clearly how this product thinks about **fate**, **agency**, **relocation**, **tradeoffs**, and **intentionality** so implementation, copy, and interpretive systems do not drift toward manipulative spirituality, false certainty, or infinite m…
  - **Companion doctrine (read together):**
  - - **`docs/visual_semantic_style_guide.md`** — **truth hierarchy** (popup / overlay / account): symbolic exploration on the map must stay **accountable** to structure.
  - - **`ai_context/memory_workflow.md`** — how proposals are reviewed and promoted so chat drift does not override this doctrine.

### A.137 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, architecture_enforcement
- Characters: 9016; SHA-12: `a67e60eba18a`; score: 73
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class; Continuity hierarchy; Discovery → Analysis workflow
- Requirement signals:
  - # Map-First Product Doctrine v1
  - **Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/architecture/client_chart_data_model_v1_2026-05-29.md`, `docs/product_workflows/product_screen_and_transition_architecture.md`, `docs/intentionality_and_symbolic_constraints.md`…
  - **This is doctrine, not implementation.** Routes, components, and shell behavior must trace here before account/chart workflow slices ship.
  - Both are **primary surfaces**. The Chart Page must not become an afterthought.
  - # Map doctrine

### A.138 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: authority_doctrine, ai_alignment, validation_gates, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9275; SHA-12: `8187d0e4980f`; score: 60
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record; S5 — Settings / ontology (Layer 2); S6 — Birth data intake / edit
- Requirement signals:
  - Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md` (**product identity authority**), `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux…
  - Ensure every screen **supports the map and chart analysis loop** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.
  - **Product identity (2026-05-31):** Map → Analysis → Administration. See `docs/constitutional/map_first_product_doctrine_v1.md`.
  - **Must not contain:** activity feeds, recents, owner hero cards, favorites, charts, map as primary surface, widgets, metrics.

### A.139 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 9566; SHA-12: `3de8663545ba`; score: 92
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth; Step 5 — Save favorites and investigations; Step 6 — Compare and decide
- Requirement signals:
  - This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.
  - **This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.
  - **Reads with:** `docs/constitutional/map_first_product_doctrine_v1.md`, `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_l…
  - The workflow must remain **fully usable** without Astro Assist, scoring engines, or conversational intake.
  - ## Core workflow principle

### A.140 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: authority_doctrine, ai_alignment, workflow_process, rollback_risk, architecture_enforcement
- Characters: 3360; SHA-12: `554add110fa4`; score: 30
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact; Interpretation; Examples Of Interpretation
- Requirement signals:
  - - orb doctrines,
  - # Important Principle
  - ## Truth must remain sovereign.
  - but may never rewrite truth.
  - # Another Important Principle



---

## Appendix B — Audit Statement

Programmatic pass selected 183 governance/protocol-related source blocks from 196 total archive blocks. The audit JSON stores matched file names, hashes, headings, requirement signals, category counts, and source metadata. Final generated word count before this statement: 21187 words.
