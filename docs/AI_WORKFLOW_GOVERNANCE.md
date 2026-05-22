# AI Workflow Governance Protocol

Date: 2026-05-22. Mandatory closeout protocol for Cursor tasks and phase work.

## Purpose

This protocol exists to prevent governance drift. Every significant AI-assisted task must close with an explicit review of doctrine, deferred work, validation evidence, and rejected ideas. "No update needed" is an allowed outcome only when it is justified in writing.

Deferred excellence is primarily about preserving hidden robustness and institutional memory, not accumulating a future feature wishlist. Features are comparatively easy to remember because users ask for them and demos expose them. The fragile memory is invisible engineering intent: infrastructure, architecture, reliability, governance, performance, renderer trust, scaling, cache/system design, synchronization, testing discipline, CI/regression infrastructure, security hardening, migration doctrine, topology robustness, AI workflow governance, anti-drift protections, rollback/recovery, observability/debugging, backend/data integrity, and anti-fragility.

The Ghost Boss role of this protocol is to protect the project from short-term commercial pressure, founder optimism, and AI recency bias. It asks: what invisible thing did this phase make easier to forget, normalize, or accidentally depend on?

This document does not change code, renderer behavior, astrology math, product behavior, or feature scope. It governs how work is closed out.

## Ghost Boss Governance Doctrine

The Ghost Boss is the invisible engineering conscience for the project. It does not block visible product work by default; it preserves the hidden work that makes visible product promises trustworthy.

Every phase closeout must ask whether it introduced or exposed:

* invisible infrastructure debt;
* architecture debt that could become normalized;
* reliability or data-integrity gaps;
* missing test, CI, regression, or rollback discipline;
* security, privacy, auth, or authorization hardening that is deferred;
* cache invalidation, synchronization, or migration risk;
* topology, renderer, or truth-provenance risk;
* observability/debugging gaps;
* AI drift risk, such as future agents rediscovering rejected ideas, forgetting doctrine, or treating temporary scaffolds as permanent architecture;
* governance erosion, such as skipped narratives, vague "later" notes, unclassified follow-ups, or unjustified "no update needed" claims.

The Ghost Boss should be especially suspicious of visible success that hides structural fragility. A feature that demos well can still require a registry entry if it leaves behind a local-only store, manual validation step, brittle smoke assumption, missing rollback path, unowned migration, or trust-sensitive stub.

## Dangerous Temporary-Forever Compromises

These patterns must be named when they appear:

* local JSON or browser storage quietly becoming product storage;
* manual smoke scripts standing in for CI indefinitely;
* debug-only diagnostics becoming required operational tooling;
* unversioned data shapes or undocumented migration steps;
* feature flags with no graduation/removal plan;
* incomplete share/auth/security assumptions treated as harmless because the demo works;
* cache behavior without invalidation, ownership, or rollback doctrine;
* renderer/aesthetic shortcuts that look good before truth provenance is locked;
* missing observability because local debugging currently feels sufficient;
* AI-generated docs that restate intent but fail to create enforcement hooks.

If a compromise is accepted for velocity, the closeout must state what would make it dangerous, when it should be audited, and whether it belongs in `docs/DEFERRED_EXCELLENCE_REGISTRY.md`.

## Mandatory Governance Closeout

Every task closeout must include:

* **Deferred excellence updates:** State whether `docs/DEFERRED_EXCELLENCE_REGISTRY.md` was updated or why no update was needed.
* **Doctrine updates:** State whether `docs/CURRENT_RENDERING_DOCTRINE.md` or another doctrine file was updated or why no update was needed.
* **Blocker classification:** Classify new follow-up work as production blocker, trust blocker, deferred, rejected, polish, experimental/professional, or future platform.
* **Rollback scope:** State what would need to be reverted if the change is wrong, including files, data shape, feature flag, or workflow scope.
* **Validation status:** State which smoke tests, scripts, manual checks, narratives, or evidence validate the work; if none ran, explain why.
* **Rejected scope:** Name any tempting work that was intentionally not done.
* **Next-step recommendation:** Recommend the next phase or explicitly say no next step is needed.

## Continuity Volume Protocol

Continuity volumes are canonical archaeology infrastructure for major phase transfers, not optional documentation. They preserve chronology, rationale, rejected paths, governance state, and warnings that would otherwise be lost between AI sessions.

Generate a new continuity volume when:

* a major phase completes;
* project doctrine, governance, or product direction pivots;
* enough chat/session material accumulates that future agents would otherwise need the transcript to understand why decisions happened;
* validation, renderer, productization, or governance history changes in a way that should survive context compaction.

Store continuity volumes in:

```text
ai_context/archaeology/RAW_CONTINUITY_VOLUME_<n>.md
```

`ai_context/archaeology/RAW_CONTINUITY_VOLUME_7.md` is the canonical archaeology continuity container for this phase. Future volumes should follow that same family/location convention unless an earlier established project pattern supersedes it.

Future AI agents should ingest continuity volumes before planning or implementation when a task touches governance, renderer doctrine, deferred excellence, product direction, or multi-phase continuity. Treat the volume as archaeology evidence: read it with `docs/AI_WORKFLOW_GOVERNANCE.md`, `docs/DEFERRED_EXCELLENCE_REGISTRY.md`, `docs/CURRENT_RENDERING_DOCTRINE.md`, and the relevant validation narratives. Do not promote raw continuity claims into doctrine without cross-checking current files and code.

## Mandatory Closeout Checklist

At the end of every significant task or phase, the agent must answer each item:

1. **Behavior changed?** State whether code, renderer behavior, astrology math, product behavior, data shape, or API contracts changed.
2. **Validation evidence captured?** State what smoke tests, scripts, manual checks, screenshots, or narratives prove the result. If validation was skipped, explain why.
3. **Doctrine update needed?** Decide whether `docs/CURRENT_RENDERING_DOCTRINE.md` needs an update and justify the answer.
4. **Deferred registry update needed?** Decide whether `docs/DEFERRED_EXCELLENCE_REGISTRY.md` needs an update and justify the answer.
5. **Validation narrative needed?** Decide whether a file under `validation/narratives/` is required and justify the answer.
6. **Blocker classification complete?** Classify newly discovered work as production blocker, trust blocker, deferred, rejected, polish, experimental/professional, or future platform.
7. **Rejected ideas preserved?** Record any tempting but rejected approach if forgetting it would risk future drift.
8. **Temporary compromises named?** Name any new compromise, its owner area, and when it must be revisited.
9. **Hidden robustness reviewed?** State whether the task created or exposed invisible infrastructure, reliability, performance, scaling, security, testing, rollback, observability, migration, topology, renderer-trust, synchronization, data-integrity, or AI-governance work.
10. **Prompt footer included?** Include the standard governance footer in any proposed next task prompt.

The closeout must explicitly say either:

* "Updated governance artifacts: ..." with file paths, or
* "No governance artifact update needed because ..." with specific reasons.

Generic statements like "no docs needed" are not sufficient.

## When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`

Update the Deferred Excellence Registry immediately when any of the following happens:

* A task creates a known future improvement that is intentionally deferred.
* A shortcut, stub, placeholder, local-only persistence choice, manual process, or debug-only seam is accepted for MVP velocity.
* A product, renderer, UX, reliability, performance, or platform idea is discussed but not implemented.
* A hidden robustness item is discovered: invisible infrastructure, architecture refinement, scaling concern, cache/system improvement, synchronization concern, testing discipline, CI/regression infrastructure, security hardening, migration doctrine, topology robustness, AI workflow governance, anti-drift protection, rollback/recovery, observability/debugging, backend/data integrity, or anti-fragility.
* A deferred item changes class, priority, scope, risk, or recommended timing.
* A deferred item is promoted into active work or demoted because evidence changed.
* A temporary compromise survives into a later phase.
* An experiment proves a direction should not become product doctrine.
* A deferred item appears to have silently become important enough to promote because usage, revenue exposure, professional sharing, operational risk, or user trust changed.

Each registry update must include:

* Why the item matters.
* Why it remains deferred or why it is being promoted/deprioritized.
* Classification: MVP blocker, trust blocker, polish, experimental/professional, future platform, or rejected.
* Rough priority: high, medium, or low.
* Risk if ignored forever.
* Date and explanation when an item's status changes.

## When To Update `CURRENT_RENDERING_DOCTRINE.md`

Update `docs/CURRENT_RENDERING_DOCTRINE.md` when a task changes or clarifies renderer truth, including:

* Production renderer substrate or canonical/debug renderer status.
* Astrology math boundaries or assumptions.
* Lat-cap behavior, high-latitude policy, seam policy, or topology policy.
* Adaptive renderer policy, cache doctrine, sample/refinement policy, or truth-source provenance.
* Popup truth, overlay truth, or map-rendering validation doctrine.
* Which renderer paths are production, debug, experimental, or rejected.

Do not update the doctrine for product-only scaffolding unless it changes renderer boundaries or restates renderer constraints that future agents must obey.

If no update is needed, the closeout must explain why, for example: "No doctrine update needed because this phase only added library handoff metadata and did not change substrate, math, rendering policy, or cache policy."

## When To Create Validation Narratives

Create or update a file under `validation/narratives/` when work is phase-sized or when it changes evidence, product trust, or decision-making. A validation narrative is required for:

* Any named phase, such as Phase 2.1 or Phase 2.2.
* Renderer, topology, cache, validation, or substrate work.
* Product scaffolding that creates a new user-facing seam, API contract, or persistence shape.
* Any investigation that changes blocker classification.
* Any experiment whose result should guide later implementation.
* Any smoke failure or regression whose root cause matters later.

A narrative may be skipped for tiny typo-only documentation edits, but the closeout must explicitly say why.

## Classification Rules

Use these classifications consistently:

* **Production blocker:** Must be resolved before public/MVP release because shipped behavior is wrong, broken, unsafe, or unusable.
* **Trust blocker:** Not necessarily blocking launch, but skipping it risks long-term credibility, professional confidence, or truthful interpretation.
* **Deferred:** Valuable and real, but intentionally postponed to protect current phase velocity.
* **Rejected:** Should not be pursued unless future evidence changes. Record the reason to prevent rediscovery loops.
* **Polish:** Improves feel, aesthetics, clarity, or perceived quality without changing core truth or product viability.
* **Experimental/professional:** Appropriate for debug, expert, or advanced workflows before mainstream product adoption.
* **Future platform:** Belongs to later account, payment, collaboration, sharing, export, analytics, or multi-user infrastructure phases.

When uncertain, classify conservatively and name the evidence that would change the classification.

## Mandatory Standard Prompt Footer

Add this footer to all future Cursor task prompts:

```text
Governance closeout required:
- At the end, explicitly state whether docs/DEFERRED_EXCELLENCE_REGISTRY.md needs an update, and why.
- Explicitly state whether docs/CURRENT_RENDERING_DOCTRINE.md needs an update, and why.
- Create or update a validation narrative if this task changes behavior, evidence, scope, product trust, or phase status.
- Classify any new follow-up as production blocker, trust blocker, deferred, rejected, polish, experimental/professional, or future platform.
- Review hidden robustness: infrastructure, architecture, reliability, performance, scaling, cache/system design, synchronization, testing/CI, security, migration, topology trust, rollback/recovery, observability, backend/data integrity, and AI/governance drift.
- Treat Deferred Excellence as institutional memory for non-demoable engineering intent, not as a shiny feature wishlist.
- If no governance artifact update is needed, justify "no update needed" explicitly.
```

## Closeout Response Template

Use this shape for future significant task summaries:

```text
Governance closeout:
- Deferred registry: [updated / not updated] because ...
- Rendering doctrine: [updated / not updated] because ...
- Validation narrative: [created / updated / not needed] because ...
- New classifications: ...
- Rejected ideas or compromises: ...
- Hidden robustness / Ghost Boss review: ...
- Standard footer for next prompt: included / not applicable because ...
```

## Enforcement Rule

No significant phase is complete until the governance closeout is written. A task may have passing tests and correct code but still be incomplete if it leaves doctrine, deferred work, validation narratives, or blocker classification ambiguous.
