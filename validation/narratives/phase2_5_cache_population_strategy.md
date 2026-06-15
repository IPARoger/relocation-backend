# Phase 2.5 — Sampling / Cache Population Strategy

## Purpose

Phase 2.5 formalizes cache-population scheduling doctrine and adds a narrow renderer-neutral scheduler contract scaffold. It does not render, fetch, persist cache state, spawn workers, or wire into `map_CURRENT.html`.

## Doctrine

User-requested conditions render first. User input always preempts background cache work.

The point-level relocated chart engine remains the truth source. Pixel/subpixel sampling discovers truth; it does not invent truth or substitute visual effects for calculation.

Cache population should adaptively cluster around meaningful structure: boundaries, cusps, overlaps, seams, and condition transitions. Broad homogeneous spaces need fewer samples. Borders, overlaps, ambiguity domains, and transition regions need more.

Raindrop and virga remain future visualizations of discovery/cache population. They may be aesthetically paced, but they must not become fake loading animations or scheduler correctness mechanisms.

## Scheduler Priority Model

- **Tier 0:** foreground user request.
- **Tier 1:** same-request likely next zooms and pan-adjacent scopes.
- **Tier 2:** boundary-focused adaptive refinement.
- **Tier 3:** alternate semantic investigations.

If the user selects a new variable, lower-tier work is cancelled or deprioritized conceptually and the new user request becomes Tier 0.

## Scaffold Added

`sampling_cache_scheduler_contract.js` exposes:

- `TIERS`
- `TIER_NAMES`
- `createWorkDescriptor`
- `sortWorkDescriptors`
- `applyUserPreemption`
- `descriptorPublicShape`

Descriptors are semantic/scope-oriented only. They carry cache keys, payload shape, tier, scope role, reason, preemption group, and cancellation/deprioritization flags. They do not execute work.

## Deferred Optimizations

The roadmap and Deferred Excellence Registry preserve, but do not implement:

- ambiguity-domain rendering,
- overlap-confidence wheel language,
- telemetry-driven scheduler tuning,
- intake-time/pre-map cache precomputation,
- six-house boundary derivation,
- ASC/DC and MC/IC opposition reuse after seam/cusp/high-latitude validation.

Aspect-to-angle semantics are not collapsed. For example, `planet opposite ASC` must not be treated as identical to `planet conjunct DC` unless future doctrine explicitly permits it.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_5_scheduler_contract.py
```

The smoke verifies:

- Tier 0 through Tier 3 ordering,
- work descriptor generation,
- user-input preemption semantics,
- semantic/scope-oriented descriptor fields,
- absence of renderer/debug/aura/fetch/worker pollution.

The first smoke run caught polluted cache-payload passthrough; the contract was tightened so descriptor payloads retain only semantic cache fields.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_scheduler_contract.js`,
- `scripts/smoke_phase2_5_scheduler_contract.py`,
- this narrative,
- the concise Phase 2.5 doctrine additions in roadmap/deferred docs.

No renderer runtime, UI, backend, account/auth, cache persistence, `phase2_cache_scheduler.js`, aura engine, truth-grid engine, or `map_CURRENT.html` file is involved.

## Governance Closeout

- **Trust risk addressed:** background cache exploration is explicitly subordinate to user intent.
- **Deferred excellence:** telemetry tuning, ambiguity-domain rendering, overlap-confidence language, and pre-map precomputation remain future work.
- **Rejected scope:** rendering, fetching, persistence, workers, aura/raindrop/virga implementation, and semantic-equivalence shortcuts.
- **Next recommendation:** commit this as a narrow Phase 2.5 doctrine and scheduler-contract checkpoint if the smoke passes and no unrelated files are staged.
