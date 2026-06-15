# Phase 2.10 — Observer / Progress Semantics Contract

## Purpose

Phase 2.10 defines what future observers and visual layers may safely know about semantic discovery and execution progress.

It does not implement visuals, animation, runtime execution, workers, fetches, renderer output, persistence, DOM/map/UI integration, or scheduler control.

## Contract Shape

`sampling_cache_observer_contract.js` exposes `window.RelocationSamplingCacheObserverContract` with:

- `createObserverEnvelope`
- `createObserverBatch`
- observer states
- discovery states
- color states

Observer envelopes are read-only and sanitized. They may describe queued, running, partially discovered, hydration-eligible, completed, stale, cancelled, and error states.

## Discovery Semantics

The contract distinguishes:

- implied nearby structure,
- confirmed discovered structure,
- unresolved ambiguity.

Partial discovery is not completed truth. Implied nearby structure is not confirmed structure. Hydration eligibility is visible only as metadata, not as renderer output.

The neutral-to-colored language is semantic only. Future raindrop/virga/aura layers may observe these states, but they must not fabricate progress, control scheduler priority, force execution, or imply truth before validation.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_10_observer_contract.py
```

The smoke verifies:

- observer envelopes are sanitized,
- stale/cancelled/error states degrade correctly,
- partial discovery is not completed truth,
- implied nearby structure is not confirmed structure,
- unresolved ambiguity remains distinct,
- hydration eligibility visibility works,
- observer state is strictly read-only,
- renderer/debug/aura/fetch/worker fields are stripped,
- no renderer/map/persistence coupling exists.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_observer_contract.js`
- `scripts/smoke_phase2_10_observer_contract.py`
- this narrative
- the tiny Phase 2.10 roadmap note

No renderer runtime, backend, UI, account/auth, cache persistence, scheduler runtime, `phase2_cache_scheduler.js`, aura engine, truth-grid engine, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** visual observers cannot lie about progress, certainty, or truth completion.
- **Deferred excellence:** actual raindrop/virga/aura visualization, real progress telemetry, runtime execution, workers, fetches, persistence, and UI integration remain future work.
- **Rejected scope:** fake progress, scheduler control from observers, renderer output exposure, animation, map/UI coupling, and account/auth work.
- **Next recommendation:** commit as a narrow Phase 2.10 observer semantics checkpoint if the smoke passes and no unrelated files are staged.
