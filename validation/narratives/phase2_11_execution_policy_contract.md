# Phase 2.11 — Execution Policy Semantics Contract

## Purpose

Phase 2.11 defines execution policy semantics before real runtime execution exists.

It specifies foreground guarantees, conceptual concurrency budgets, background throttling, starvation prevention, cancellation propagation, hydration gates, readiness distinctions, observer cadence, speculative work limits, and neutral policy inputs/outputs.

## Boundaries

There is no intake system yet. There is no AI interpretation layer yet. There is no astrology meaning framework yet.

The current system remains "just the facts": semantic conditions, cache, scheduling, lifecycle, and observer state. Future AI/intake may provide opaque priority hints, but this policy must not encode interpretive astrology or location meaning.

## Contract Shape

`sampling_cache_execution_policy_contract.js` exposes `window.RelocationSamplingCacheExecutionPolicyContract` with:

- `createPolicyContext`
- `sanitizePriorityHint`
- `readinessFor`
- `canHydrateUnderPolicy`
- `applyExecutionPolicy`

## Policy Semantics

Tier 0 foreground work must not be blocked by lower tiers. Background work is budgeted and throttled. Same-request work outranks alternate investigations. Speculative work is bounded and disposable.

Stale or cancelled jobs cannot hydrate. Completed compatible jobs may become truth-ready. Hydration-ready and display-ready are distinct policy meanings, and display readiness does not imply interpretive completion.

Observer updates are cadence-limited and read-only so they cannot create fake responsiveness or control execution.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_11_execution_policy_contract.py
```

The smoke verifies:

- Tier 0 foreground is never blocked,
- background budget is capped,
- same-request work outranks alternate investigations,
- speculative work is throttled,
- stale/cancelled jobs cannot hydrate,
- completed compatible jobs can become truth-ready,
- truth-ready, hydration-ready, and display-ready remain distinct,
- observer updates are cadence-limited,
- renderer/debug/aura/fetch/worker fields are stripped,
- future priority hints are accepted as opaque scheduling hints without astrology meaning.

The first smoke run caught two boundary issues: completed readiness bookkeeping could consume same-request budget before pending same-request work, and priority-hint validation needed to preserve opaque hints while stripping interpretive astrology meaning.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_execution_policy_contract.js`
- `scripts/smoke_phase2_11_execution_policy_contract.py`
- this narrative
- the tiny Phase 2.11 roadmap note

No renderer runtime, backend, UI, account/auth, cache persistence, scheduler runtime, `phase2_cache_scheduler.js`, aura engine, truth-grid engine, AI/intake implementation, astrology interpretation layer, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** runtime execution cannot begin without foreground, budget, hydration, observer, and speculative-work policy semantics.
- **Deferred excellence:** real execution, workers, fetches, telemetry, persistence, AI/intake, astrology interpretation, UI integration, and visual progress systems remain future work.
- **Rejected scope:** interpretive astrology ranking, location meaning, renderer output, fake responsiveness, worker orchestration, backend storage, and account/auth work.
- **Next recommendation:** commit as a narrow Phase 2.11 execution policy checkpoint if the smoke passes and no unrelated files are staged.
