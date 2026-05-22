# Phase-2 Cache Integration — Architecture & Implementation Planning

> **Status:** Architecture and planning doctrine. Design only. No code
> changes authorised by this document.
> **Authority:** `docs/relocation_map_architecture.md` (§ "Phase 2 cache
> priority protocol") and `docs/PHASE_C_RENDERING_ARCHITECTURE.md`
> (substrate laws). This document **operationalises** §10 step 1 of the
> Phase C charter.
> **Companion:** `validation/narratives/phase2_cache_implementation.md`
> (current sandbox implementation notes).
> **Adopted draft:** 2026-05-21.
> **Stability:** Slow. Implementation details may rev; design rules here
> change only by explicit edit naming the prior stance.
> **Non-goals:** No aura styling. No aesthetic rendering changes. No
> astrology math changes. No validated-adaptive-refinement behaviour
> changes. No revival of any superseded path.

This document does one thing: define how the validated adaptive
screen-space refinement substrate is wrapped in a production-grade
cache orchestrator that preserves correctness, user responsiveness,
and the cancellation contract, without introducing speculation
disguised as requirement.

---

## 0. Where this fits

| Layer | Doc | Role |
|------|-----|------|
| Foundational architecture | `docs/relocation_map_architecture.md` | Phase-2 cache priority protocol (canonical) |
| Substrate governing laws | `docs/PHASE_C_RENDERING_ARCHITECTURE.md` | Substrate-level cache doctrine (§5) |
| Operational planning (this doc) | `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` | Production integration architecture, validated against the sandbox |
| Implementation notes | `validation/narratives/phase2_cache_implementation.md` | What the sandbox actually does today |
| Smoke evidence | `validation/reports/phase2_cache_smoke.json` | What the sandbox actually proves |

When this document and the foundational architecture disagree, the
foundational architecture wins. When this document and the substrate
charter disagree, the substrate charter wins. When this document and
the sandbox implementation disagree, the sandbox is treated as
**evidence of one path**, not a binding contract; this document may
override the sandbox.

---

## 1. Grounding — what is true today, measured

This section is the audit trail behind every design rule below. Numbers
are from `validation/reports/phase2_cache_smoke.json` and
`validation/narratives/screen_pixel_adaptive_targeted.md`.

### 1.1 Sandbox state (measured, not asserted)

| Property | Value | Source |
|----------|-------|--------|
| Smoke test outcome | `all_pass: true` (7 tests, ~3 s wall) | `phase2_cache_smoke.json` |
| First-paint USER job samples | 5 130 | smoke test, viewport 720×450 |
| Cache entries after smoke | 1 | smoke test (the USER job itself) |
| Background jobs completed in smoke | 0 | smoke deliberately interrupts before any background completes |
| Cancelled jobs after smoke interrupt | 44 | smoke test |
| Aborts observed (in-flight) | 1 | smoke test |
| H-priority status | `deferred_inactive` | matches doctrine: date-mode-gated |
| Budget constant | 233 118 samples | matches `screen_pixel_adaptive_targeted.md` |
| Sandbox renderer | `/screen-pixel-truth` with fixed `block=8` | `map_SANDBOX_phase2_cache.html` URL_BLOCK |

### 1.2 What this means

| Claim | Status |
|------|--------|
| Cancellation contract works | **Measured** (44 cancellations, 1 abort, no half-cached entries) |
| Priority order registers correctly | **Measured** (A_zoom_plus_1, B_zoom_plus_2, C_pan_buffer in order) |
| Budget constant matches doctrine | **Measured** (233 118) |
| H is deferred until date-mode active | **Measured** (`deferred_inactive`) |
| Idle warm-up converges within budget | **NOT measured** — smoke test interrupts before any background job completes |
| Cache hits actually serve future renders | **NOT measured** — only one cache entry exists at the end of the smoke run |
| Multi-user-action storms degrade gracefully | **NOT measured** — smoke runs one cycle (request → interrupt → request) |
| Cache survives across chart change | **NOT applicable today** — sandbox is single-profile-per-page |

The validation strategy in §7 closes these measured / not-measured gaps
without inventing new performance claims.

### 1.3 Hard architectural finding — substrate mismatch

The Phase-2 cache sandbox uses `/screen-pixel-truth` (the
screen-space substrate). The production map `map_CURRENT.html` still
uses `/search-regions` (the legacy lat/lon-grid path) for the polygon
overlay.

**Consequence:** "Wire the Phase-2 scheduler into `map_CURRENT.html`"
is incomplete. The scheduler can only meaningfully cache the substrate
that the production renderer asks for. If the production renderer
issues lat/lon-grid requests, the cache must wrap that endpoint or be
useless to it.

**Two paths exist, both legitimate:**

| Path | Description | Cost |
|------|-------------|------|
| **Migrate first** | Move `map_CURRENT.html` to `/screen-pixel-truth` for the visible-overlay path, then wire the scheduler over it | Two changes; substrate migration first |
| **Wrap legacy** | Build the scheduler as endpoint-agnostic; cache `/search-regions` responses keyed on payload hash until the migration happens | Faster cache delivery; legacy path's bugs (dashed centerlines, world-copy mismatch, fitBounds aspect) persist until migration |

This document **does not** pick a path; that is the integration
decision for the implementation phase. It does require that the
decision be made explicit and recorded before code is written. §10
proposes a recommended order.

---

## 2. Production Scheduler Architecture

### 2.1 Single-active-job model

The scheduler runs **one active job at a time**, by design.

| Reason | Why single-active is correct |
|--------|------------------------------|
| Endpoint serialisation | `swe.houses` is CPU-bound on the backend; multiple concurrent classifies do not net more work per second |
| Cancellation simplicity | `AbortController` per fetch composes cleanly when the model is "one in flight, abort it" |
| Determinism | No interleaving means no race conditions on cache state |
| Budget honesty | Budget is enforced per-job at enqueue time; concurrent jobs would require speculative budget reservation |

This is **not** a future optimisation hook. Concurrent background jobs
require a different cancellation contract and would re-open the
"half-cached entries" hazard. They are explicitly forbidden by this
doctrine.

### 2.2 Foreground vs background queues

Two roles, one queue:

| Role | What it does | Priority |
|------|--------------|----------|
| **Foreground (USER)** | The user's current request: visible overlay for the current viewport at the current zoom | Always wins; pre-empts any background job |
| **Background (A → H)** | Opportunistic warm-up per `relocation_map_architecture.md` § "Priority order while idle" | Runs only when USER has finished AND idle grace has elapsed AND no `cachePaused` flag |

The queue is **single-FIFO ordered by priority enum**. The scheduler
does not maintain separate foreground and background queues because
they are mutually exclusive: a foreground request *cancels* every
pending and active background job, then runs alone. After it
completes, the background queue is the only active queue.

### 2.3 Cancellation / interruption behaviour

The cancellation contract is contractual, not heuristic. The sandbox
implements it; production must preserve every clause:

| Clause | Implementation requirement |
|--------|----------------------------|
| `pause()` aborts the in-flight job | `AbortController.abort()` per fetch |
| Aborted job's partial response discarded | Defensive `j.cancelled` flag; cache is **only** set on full success |
| Pending queue cleared on pause | Every pending job marked `cancelled` |
| H-priority survives a single pause | H is `deferred_inactive` until date mode active; pause does not "lose" H |
| Active USER request not cancellable by another USER request | A second USER request waits behind the first OR replaces it explicitly; never silent overlap |

**Forbidden:** swallowing an in-flight result after `abort()` and
writing it to the cache "since we already have it." This is the
"half-cached entries" hazard. The cache reflects committed work, not
opportunistic flotsam.

### 2.4 Priority escalation rules

The priority order is **static** by current doctrine. The scheduler
does **not**:

- promote a background job to foreground urgency,
- demote a foreground job to background queue,
- re-order pending jobs based on observed user behaviour,
- skip ahead in the priority list because a later job has a smaller
  payload,
- escalate a deferred-for-budget job above another within the same
  priority tier.

The scheduler **does**:

- mark a job `deferred_budget` if the projected total would exceed the
  budget at enqueue time,
- re-enqueue cancelled jobs (with a fresh AbortController) only after
  the next USER request lands and idle grace expires,
- check the cache before issuing any fetch (cache hits do not consume
  budget).

Any rule beyond this list is a future optimisation gated on telemetry
evidence (§9 and `relocation_map_architecture.md` § 5.5 of Phase C
charter).

### 2.5 Viewport ownership

A USER job owns:

- the **visible** viewport bounds and zoom at the moment of request,
- the current condition set,
- the current `apply_lat_cap` value.

Background jobs of priority A–C own **synthesised** viewports anchored
on the visible center. They do not mutate the visible map. The
sandbox demonstrates this with `pointsFromCenter(zoom, panOffsetPx)`
that calls Leaflet `project` / `unproject` at the synthetic zoom
without calling `map.setView()`. Production integration must preserve
this: cache warm-up is invisible to the user.

A background job that would require mutating the visible map is, by
definition, not a background job. It is a foreground action waiting
for a user gesture.

### 2.6 Concurrency doctrine

| Concurrency surface | Rule |
|---------------------|------|
| Browser → backend | One in-flight request per scheduler |
| Backend → engine | Single-threaded per request (the FastAPI handler) |
| Cache reads | Synchronous, single-threaded (JS event loop) |
| Cache writes | Only on full successful fetch resolve |
| Map event handlers | Each fires `onUserAction(reason)` which is idempotent (it pauses; pausing an already-paused scheduler is a no-op) |

A second in-flight request would not double the throughput because the
backend is the bottleneck. A future server-side cache or sharded
worker pool would change this calculus; until then, single-active is
correct and simpler.

### 2.7 Deterministic replay / coherence

The cache key (sandbox shape, normative for production):

```text
{
  "chart": <profile_id>:<YYYY-MM-DDTHH:MM>,
  "bounds": {n, s, e, w},
  "zoom": <number>,
  "block": <px>,
  "conditions": <sorted JSON array>,
  "lat_cap": <bool>
}
```

| Property | Why this shape |
|----------|----------------|
| Chart identity | Includes profile id and birth instant so two charts cannot collide |
| Bounds | Per-world-copy correctness; bounds are post-Leaflet-projection viewport corners |
| Zoom | Different zoom = different cell area = different classification surface |
| Block | Fixed-block raw classification; an entry at block=8 cannot be served to a request at block=2 |
| Conditions sorted | Order-insensitive on conditions (same set → same key) |
| `lat_cap` | Different cap policy = different `apply_lat_cap` answers at polar tiles |

Two requests with the **same key** must produce the **same** result.
The cache assumes this. If a future schema field affects classification
(e.g. an orb override, a transit moment), it **must** enter the cache
key or the cache is silently wrong. The doctrine rule: **any input
that can change a single mask byte must appear in the key.**

The cache does **not** include:

- Wall-clock time (no time-varying inputs in production today).
- Map style / palette (presentation, not classification).
- Debug flags (presentation).
- User identity (per-chart cache, not per-user).

---

## 3. Zoom Doctrine

### 3.1 The zoom contract

Per `relocation_map_architecture.md` § "Zoom Strategy":

> Zoom must not trigger naive full recomputation.

The contract distinguishes:

| Object | What changes on zoom |
|--------|----------------------|
| **Interior occupancy** | Does **not** change: cells whose classification was correct at the prior zoom remain correct |
| **Edge refinement** | Does change: cells along uncertainty bands need finer sampling at higher zoom |

In the current substrate, this contract is **not yet implemented**:
the sandbox re-solves the full viewport on every pan/zoom
(`map_SANDBOX_phase2_cache.html` and `map_CURRENT.html` both
re-classify entirely). This is the largest unmet substrate gap behind
cache wiring (`docs/CURRENT_RENDERING_DOCTRINE.md` § "Remaining gaps").

### 3.2 Immediate viewport

| Step | Rule |
|------|------|
| User action arrives | `onUserAction()` pauses the scheduler, cancels in-flight, clears pending |
| Cache check | Compute the cache key for the new visible viewport; if hit, paint immediately and skip the network round-trip |
| Cache miss | Issue a USER job; first-paint priority order applies (speed, truth, trust, clarity) |
| First paint | Paint as soon as the USER response resolves |
| Idle grace | After paint, wait `IDLE_GRACE_MS` for further user action; if none, start background queue |

**`IDLE_GRACE_MS` clarification.** The sandbox uses 200 ms. This is a
**post-completion grace**, not a "timer from first paint" (which the
doctrine forbids). It exists because rapid user actions (zoom-tap +
pan-drag) often arrive sub-second; starting background work for 200 ms
that is then immediately cancelled wastes a fetch round-trip. 200 ms
is small enough to feel free, large enough to absorb common gesture
flurries. Future tuning is a measured-evidence question, not a
preference.

### 3.3 +1 / +2 zoom priorities (A, B)

A and B are **synthesised** point grids at the user's current center
at `baseZoom + 1` and `baseZoom + 2`, not at the user's actual map
zoom. They populate cache entries that the user **may** request next.

| Behaviour | Rule |
|-----------|------|
| Synthesised grid bounds | Computed via Leaflet `project`/`unproject` at the synthetic zoom; the map is not moved |
| Cache key | The synthesised bounds and zoom enter the cache key; user gesture that matches gets a cache hit |
| Cancellation | Standard scheduler cancellation; partial A is dropped, not stored |
| Priority order | A runs before B; both run before C; all three run before D |

### 3.4 Reuse versus reclassification (future, gated)

The substrate could in principle reuse interior occupancy from a prior
zoom and refine only the edges at the new zoom. The current cache
does **not** implement this. It treats each `(bounds, zoom, block)`
tuple as a fresh classification.

The reuse pattern, when implemented, requires:

| Requirement | Why |
|------------|-----|
| Per-cell provenance | The renderer must know which cells came from which prior pass |
| Edge detection across zooms | An "edge" at zoom Z is not necessarily an edge at zoom Z+1 |
| Validation that reused interior matches re-classified interior | Must agree cell-for-cell; otherwise reuse is wrong |
| Negative-space guarantees | Reuse must not paint stale cells; the cache key must invalidate when birth or condition changes |

Until those four are demonstrated on a fixture suite, the cache stays
on the "fresh classification per `(bounds, zoom, block)`" rule. This
is conservative on compute, correct by construction, and easy to
reason about.

### 3.5 Edge refinement reuse (future, gated)

Same gate as §3.4. The substrate's adaptive refinement narrative
(`screen_pixel_adaptive_refinement.md`) demonstrates that 1px local
convergence on a band typically classifies under 10% of the viewport.
Reusing the 2px-converged band classification across small zoom
changes is the highest-leverage future cache optimisation, but it is
**deferred** until interior-occupancy reuse is proven first; the two
share architectural prerequisites.

### 3.6 Cache invalidation rules (zoom-related)

| Event | Effect on cache |
|-------|-----------------|
| Zoom in / out (no chart change) | A/B priorities re-target around the new zoom; existing entries retained where bounds match |
| Pan within buffer (~25%) | C priority advances; no invalidation |
| Pan beyond buffer | Treated as a fresh USER request; existing entries remain valid for their original bounds |
| Condition family change | Entries for that family invalidated; others retained |
| Chart change | Entire cache invalidated (per-chart contract) |
| `apply_lat_cap` flip | Affected entries invalidated (different cap = different polar tile answers) |

Invalidation is **coarse and confident**, never clever. "Clever"
invalidation (e.g. "only invalidate the polar tiles when the cap
flips") is correctness risk for negligible cache-retention gain.

### 3.7 Pan/zoom continuity

| Sequence | Behaviour |
|----------|-----------|
| Pan-then-stop | `movestart` pauses; `moveend` (debounced) triggers USER job for new bounds |
| Zoom-then-stop | `zoomstart` pauses; `zoomend` triggers USER job for new zoom |
| Pan during zoom | Single pause; single USER job for the final state |
| Drag-flick | Pan during inertia is a sequence of `moveend` events; debounce (~400 ms in `map_CURRENT.html` today) is correct |
| Idle for `IDLE_GRACE_MS` after USER complete | Background queue starts |

The contract is: **every user gesture pauses the background instantly;
every gesture's final state triggers at most one USER job; background
resumes only after that USER job has painted and the grace has
elapsed.** The user must never feel the cache "lag" behind their
gestures.

---

## 4. Classification Reuse

### 4.1 Already-classified samples

The fundamental reuse question: when can a previously-classified
sample's result be used to satisfy a new request?

Conservative rule (this doctrine, **measured-safe**):

> A sample's classification can be reused if and only if its cache key
> matches exactly: same chart, same bounds, same zoom, same block,
> same sorted conditions, same `lat_cap`.

This is exact-match reuse. It is the easiest invariant to prove and
the easiest to audit. It is also weak — it does not capture
geographically-overlapping requests at different zooms, different
blocks, or different condition subsets.

### 4.2 Reuse between adjacent zooms (future, gated)

Geographic overlap is real: a viewport at zoom Z and a viewport at
zoom Z+1 both contain (lat, lon) coordinates that should yield the
same `swe.houses` answer. The cache could in principle index by
(lat, lon, block) and answer cross-zoom queries.

**Why this is deferred:**

| Reason | Detail |
|--------|--------|
| Per-pixel block alignment differs across zooms | A pixel at zoom Z is a different geographic area than at zoom Z+1; reuse requires recomputing pixel-area equivalence |
| Substrate adaptive refinement is per-zoom | The convergence at zoom Z does not transfer to zoom Z+1 without re-running the refinement loop |
| Validation surface grows | Cross-zoom reuse must be cell-for-cell validated against full re-classification |
| Memory cost rises | A geographic-coordinate cache index is heavier than per-viewport cache entries |

This is the most valuable future optimisation; it remains deferred
until the substrate's adaptive refinement is in production and
interior-occupancy reuse is operational.

### 4.3 Reuse between neighbouring tiles

Within a single viewport at a single zoom, the substrate's adaptive
refinement already reuses **probe samples** from coarser phases to
inform finer phases. This is intra-pass reuse and is owned by the
substrate, not the cache.

The cache does not currently slice viewport responses into
sub-viewport tiles. It stores the whole viewport's classification as
one entry. Sub-viewport tile-level caching is a future shape (the
"tile-space precomputed map tiles" Option C in
`screen_pixel_truth_diagnosis.md`); it is **deferred** until the
substrate is stable and viewport-level caching is in production.

### 4.4 Reuse between conditions

A natural question: if `{Sun in 1st}` is cached and the user requests
`{Sun in 1st, ASC in Capricorn}`, can the Sun-in-1st classification
be reused?

**Answer (conservative, current doctrine):** No. The combined-condition
request issues a single backend call that returns per-point masks for
the full condition set in one pass. Splitting the request, fetching
the missing condition, and AND'ing client-side is **possible** but
introduces a different correctness contract (the combined call returns
a mask; the split-and-combine returns a derived mask that must be
validated against the combined call).

This is the foundational tension behind the sandbox's priority D job:
D pre-caches `{planet_in_house}` for every (planet, house) pair across
the visible samples, in batches of ≤ 6 conditions per call. D's
*usefulness* depends on whether the user's next condition switch can
be answered by a cached subset rather than a fresh fetch. Today the
answer is "only if the user's next request exactly matches a cached
subset," because no client-side condition-mask-recombination logic
exists.

**Rule:** Condition recombination is a future optimisation. It
requires:

1. Backend semantics published: "the mask for `{X, Y}` is the
   bitwise AND of the per-condition masks for `{X}` and `{Y}`,"
   verified by validation on fixtures.
2. A client-side combiner that handles cache-miss-for-superset
   gracefully (issue the fresh fetch, don't try to be clever).
3. Tests proving combined-from-cache equals combined-from-fresh,
   cell for cell, across the dense matrix.

Until those three exist, the cache key is the full sorted condition
set, exact match only.

### 4.5 Negative-space inheritance

`relocation_map_architecture.md` § "House Negative-Space
Optimisation — Future Only" explicitly defers any inference of one
house's region from neighbours' negative space. The cache must not
re-introduce this by accident.

**Rule:** A cache entry for `{Jupiter in 10th}` does **not** imply
anything about `{Jupiter in 9th}` or `{Jupiter in 11th}`. They are
separate cache keys. The renderer never computes the absence of a
match for one condition by observing the presence of a match for
another. This is the same doctrine, applied to the cache: no
implication, only direct classification.

### 4.6 The "6-house doctrine" — D-job splitting

The sandbox splits priority D ("all planet-in-house at visible
samples") into per-planet sub-jobs, each carrying houses 1–6 or 7–12,
because `_MAX_CONDITIONS = 6`. This produces 10 planets × 2 halves =
20 D sub-jobs.

**Implications:**

| Property | Consequence |
|----------|-------------|
| D is interruptible mid-execution | A user action cancels remaining D sub-jobs cleanly |
| D is "done" only when all 20 sub-jobs cache successfully | A partially-completed D is not a usable D; "Sun in houses 1–6 cached, Sun in houses 7–12 not" cannot answer "Sun in house 8" |
| The user benefits from D *incrementally* | The first switch to a cached condition is free, even if D is only 60% done |
| Budget accounting for D | Each sub-job carries its own samples cost; budget consumed incrementally |

The 6-house doctrine is **not** a substrate rule about astrology; it
is an endpoint-cap artifact. If `_MAX_CONDITIONS` rises (future
aesthetics-pass requirement for 7–8 condition stacks per
`screen_pixel_dense_residue.md`), D's sub-job count shrinks
proportionally. This document does not require raising the cap; it
only requires that D's split shape track the cap.

### 4.7 Production correction to sandbox

The sandbox's priority E uses a **placeholder sign** (`signs[0]`,
"aries") for angle-in-sign caching. The implementation note in
`map_SANDBOX_phase2_cache.html` is explicit:

> sign is a placeholder; the real implementation would read the
> relocated chart's actual angle sign and cache that.

Production integration **must** read the chart's actual relocated ASC,
DSC, MC, IC signs and cache those four entries — **not** all 48 (4
angles × 12 signs). Caching all 48 would be wasteful (each cell has
exactly one sign per angle; the other 11 are vacuously false).

This is a documented sandbox shortcut, not a contract violation. The
production integration's E-priority specification is:

> Cache `angle_in_sign` for each of `{ASC, DSC, MC, IC}` at the
> current relocated chart's actual sign for that angle.

---

## 5. Cache Lifecycle

### 5.1 Memory vs disk

| Surface | Current sandbox | Production rule (this doctrine) |
|--------|-----------------|--------------------------------|
| Browser memory | `Map` keyed by canonical JSON | Authoritative for the active session |
| `localStorage` / `IndexedDB` | Not used | **Deferred** — adds correctness/invalidation complexity; not required for MVP |
| Server-side cache | Not implemented | **Deferred** — cross-session sharing requires authentication / privacy / per-user invalidation |

**Rule for the production integration:** memory-only, per-session,
per-tab. Cache dies on page reload (matches sandbox behaviour). This
is the simplest correct shape and the only one currently validated.

A future server-side cache is mentioned in
`relocation_map_architecture.md` § "Phase 2 cache priority protocol"
as an optional addition keyed by
`(profile_id, bounds_hash, zoom, condition_set_hash)`. The hash inputs
must match the cache-key inputs in §2.7 of this document. Until that
infrastructure exists, no cross-session reuse.

### 5.2 Eviction philosophy

A bounded budget (`233 118` samples) is the cache's only ceiling.
There is no LRU, no LFU, no TTL.

| Rule | Why |
|------|-----|
| Cache entries are not evicted during a session | A cached entry is, by definition, work already paid for; evicting it forces a re-fetch |
| Budget refers to background-job samples, not foreground | USER requests always serve; their samples don't count against the budget |
| `deferred_budget` jobs are not silently truncated | They wait; the next idle window may still run them; chart change invalidates the slot |
| Memory pressure | Browser memory is not a constraint at the validated budget (233k samples × small per-sample state) |

If the cache ever needs eviction, it is because:

- the budget rose without measurement (do not),
- the per-sample state grew (a substrate change that requires
  budget recalibration),
- or the architecture moved to multi-chart (a future change that
  requires its own doctrine pass).

Until one of those is true, **eviction is not implemented**.

### 5.3 Warm vs cold states

| State | Definition | Behaviour |
|------|------------|-----------|
| **Cold** | No cache entries for current chart | First USER request runs fresh; background queue starts after idle grace |
| **Warming** | A → H jobs running | Each completing job adds an entry; UI shows no spinner; user actions interrupt |
| **Warm (partial)** | Some priorities done, some pending | New USER requests hit cached entries where keys match; misses fall through to fresh fetches |
| **Warm (complete)** | All A → G priorities done; H deferred unless date mode | Subsequent USER requests are largely cache hits within the warmed condition / viewport set |
| **Invalidated** | Chart change, condition family change, lat_cap flip | Affected entries dropped; warming resumes from cold for those |

A warm state is opportunistic, never promised. The product never
shows a "cache is warm" indicator to the user. The user perceives
faster subsequent requests; the mechanism is invisible.

### 5.4 Session persistence

Deferred. No `localStorage`, no `IndexedDB`, no server-side persistence
in scope for the initial production integration.

**Reason:** Persisted caches require:

| Concern | Why deferred |
|---------|--------------|
| Invalidation on substrate change | If the engine version, condition semantics, or astrology math changes, persisted entries become silently wrong |
| Cross-tab consistency | Two tabs editing the same chart concurrently with separate caches is unsolved |
| Storage budget | `localStorage` has small per-origin quotas; the budget shape changes |
| Privacy / per-user identity | Persisted caches across sessions imply user identity; the product doesn't have authentication today |

These are all solvable, none are urgent. Session persistence enters
this doctrine when there is a measured user benefit and a designed
invalidation contract.

### 5.5 Probabilistic future caching

Per `docs/PHASE_C_RENDERING_ARCHITECTURE.md` §5.5: telemetry-derived
priority reordering is deferred. Until telemetry exists and
demonstrates a measured win against the static A → H order, the
static order is the contract.

**Specifically forbidden today:**

| Pattern | Why |
|---------|-----|
| Mouse-prediction caching | No telemetry; speculative |
| Dwell-zone pre-fetch | No telemetry; speculative |
| Multi-chart pre-warming | Cache is per-current-chart by contract |
| Transit blanket caching | Date-dependent; only valid when date mode is active |
| "Smart" priority re-order based on observed sequences | Asserted optimisation, not measured |

### 5.6 Deferred predictive doctrine

When (if) predictive caching arrives, it must satisfy:

1. **User-first interruption remains absolute.** No predicted job
   delays a real user request, ever.
2. **Measured win.** The new order must demonstrably outperform A → H
   on a defined fixture set, not on intuition.
3. **Invisible to the user.** No new spinner, no pre-fetch animation,
   no "we think you'll want this next" UX.
4. **Reversible.** A telemetry-derived priority can be reverted to A →
   H without code change (config flag); regressions are recoverable.

Anything not satisfying all four is rejected at design review.

---

## 6. Stress Behaviour

### 6.1 Worst-case overlap

The validated worst-case from
`validation/narratives/screen_pixel_dense_residue.md`:

| Case | Samples | XOR vs 1 px | Verdict |
|------|--------:|------------:|---------|
| `dense_5_americas` | 186 853 | 0.386% | acceptable with visible edge residue |
| `dense_6_americas` | 194 265 | 0.334% | acceptable with visible edge residue |

The budget `233 118` (`= 194 265 + 20%`) covers this with margin. The
cache must respect this ceiling; a dense-overlap USER request consumes
near-budget on its own, leaving little budget for background warm-up
on that viewport.

**Behavioural consequence:** for dense-overlap viewports, the
background queue will likely defer many jobs to `deferred_budget`.
This is correct doctrine, not a bug. The user got their answer;
warming priority A (zoom +1) for a six-condition overlap probably
**will** exceed budget; defer it.

### 6.2 High-latitude escalation

The substrate already handles the polar / high-latitude class via the
targeted policy (`edge2_thin2_highlat2_probes`). The cache's only
concern: when `apply_lat_cap` flips, polar tiles' classification
changes, so cache entries with mismatched `lat_cap` cannot be reused.

The cache key includes `lat_cap`. This is sufficient. No additional
high-latitude cache logic is required.

### 6.3 Seam behaviour

The screen-space substrate handles dateline / world-copy correctly by
construction (each visible world copy generates its own screen pixels
and is classified independently). The cache stores the per-viewport
result; if the visible viewport crosses the dateline, the cache
stores the result for that crossing-viewport. No special-case logic
needed.

If a future zoom edge-refinement system shares classifications across
viewports that themselves cross the dateline, it will need a
seam-aware geographic index. **Deferred.**

### 6.4 Interruption storms

The hardest stress class is rapid user actions: zoom-tap → pan-drag →
zoom-tap → condition-change, sub-second between gestures.

**Validated sandbox behaviour:** every gesture fires `onUserAction`
which is idempotent. The scheduler pauses, cancels in-flight, clears
pending. The next idle grace starts on the next gesture's USER
completion.

**Risk:** rapid storms can cause many fetches to start and immediately
abort (network round-trip cost). Mitigations:

| Mitigation | Status |
|------------|--------|
| Debounce USER job issuance | Already present in `map_CURRENT.html` (400 ms) |
| Abort fast enough that the server stops work | `AbortController` aborts the *fetch*; the server may still be processing the request CPU-bound side. This is acceptable but visible in server logs |
| Track an `interruption_storm` flag | **Not required**; existing protocol handles arbitrary storm depth correctly |

The cache survives an interruption storm correctly by being correct
on each step. It does not need a "storm mode."

### 6.5 Rapid zoom spam

A user spamming zoom-in repeatedly issues a sequence of USER jobs at
increasing zoom levels. Each new gesture cancels the prior. The cache
gets at most one entry per gesture's final state. Background warming
for zoom Z is cancelled when the user reaches zoom Z+1. This is
correct.

**Optimisation note (deferred):** A future tile-space cache could
serve sub-second zoom changes from pre-warmed tiles. Today, each
zoom-stop is a fresh USER fetch. This is acceptable: the validated
USER fetch at 720×450 completes in ~0.5 s end-to-end for a single
condition (`screen_pixel_truth_diagnosis.md`), which is well below the
"feels-instant" perception threshold for users intentionally exploring
zoom.

### 6.6 Condition spam

A user toggling condition selectors rapidly issues a sequence of USER
jobs with changing condition sets. Each cancels the prior. Cache
entries from prior selections remain valid for their original keys;
new selections that happen to match cached entries are served as cache
hits.

**Productivity test (future validation):** after a 10-toggle sequence
across the validated condition matrix, the cache should contain
entries for the union of distinct selections, with no duplicates.
This is testable today (see §7) and recommended for the integration
smoke.

### 6.7 Recovery guarantees

The cache and scheduler must recover gracefully from:

| Failure | Behaviour |
|--------|-----------|
| Server unavailable | USER job's fetch rejects; UI shows error state; cache untouched; retry on next user action |
| Server returns 5xx | Same as above |
| Server returns malformed JSON | Fetch error; cache untouched |
| Backend takes longer than the user expects | The user may interrupt; the in-flight job aborts; the cache stays uncommitted |
| Browser tab backgrounded mid-fetch | The browser may throttle; on resume, the next user action restarts the cycle |
| `apply_lat_cap` flipped mid-warm | Affected entries invalidated; warm-up restarts those |
| Chart change mid-warm | Entire cache invalidated; warm-up restarts from cold for the new chart |

**Forbidden recovery patterns:**

- Showing a stale cache entry from a different chart "while we
  reload."
- Painting half-cached data with a "partial" indicator.
- Auto-retrying aborted background jobs without a fresh user action
  (would re-introduce work the user explicitly interrupted).

---

## 7. Validation Strategy

### 7.1 Measurable success criteria

The current `scripts/smoke_phase2_cache.py` covers:

| Test | Status |
|------|--------|
| First paint completes | Pass |
| User action pauses background | Pass |
| Priority order registered correctly | Pass |
| Immediate render after interrupt | Pass |
| No half-cached entries (aggregate check) | Pass |
| Budget constant matches doctrine | Pass |
| Cache entries after protocol | Pass (count ≥ 1) |

The current smoke is **insufficient** to prove the cache is
production-ready. It exercises one pause cycle and counts that one
USER job cached its result. It does not exercise:

- Idle warm-up completing without interruption
- A → H priority drainage within budget
- Cache hits actually serving subsequent USER requests
- Interruption storms
- Condition spam productivity
- Chart-change invalidation

### 7.2 Cache correctness proofs

| Proof | Test design |
|-------|------------|
| **Cache hit returns identical result to fresh fetch** | Run USER job twice with same key; assert second response matches first byte-for-byte |
| **Cache miss does not contaminate cache** | Issue a malformed request; assert cache size unchanged |
| **Order-insensitivity on conditions** | Issue two requests with the same condition set in different orders; assert one cache entry, second is a hit |
| **Chart-change invalidates entire cache** | Issue requests for chart A, switch to chart B, assert cache cleared |
| **`apply_lat_cap` flip invalidates polar-touching entries** | Issue with cap on, flip cap off, assert affected entries dropped |
| **Bounds change beyond buffer issues fresh fetch** | Pan far, assert no spurious cache hit from prior viewport |

These are all client-side state checks; no backend changes required.

### 7.3 Interruption correctness

| Proof | Test design |
|-------|------------|
| **Aborted job leaves no cache entry** | Start background job, abort before resolve, assert cache size unchanged |
| **Server-late response after abort is dropped** | Inject a delayed response; abort during the delay; assert cache unchanged after the delayed response arrives |
| **Interruption storm: 10 rapid pauses produce 0 stuck states** | Fire 10 `onUserAction` events 50 ms apart; assert final `status` is `paused` or `idle`, never `idle_caching` mid-storm |
| **USER job during background does not double-paint** | USER request mid-A-job; assert canvas paints once (USER result), background result discarded |

### 7.4 Stale-cache detection

| Concern | Detection |
|---------|-----------|
| Stale entry served after chart change | Per-chart cache key prevents; test by switching profiles and asserting no cross-contamination |
| Stale entry served after backend semantic change | Versioned cache key (future): include backend schema version in the key when backend evolves |
| Stale entry from a different `lat_cap` | Key includes `lat_cap`; assert by flipping cap and observing miss |

### 7.5 Zoom coherence validation

| Proof | Test design |
|-------|------------|
| **A/B synthesised zooms match user-actual zooms** | Cache an A (zoom+1) entry; then user zooms to that zoom; assert cache hit |
| **Synthesised zoom does not mutate the visible map** | Capture map state before and after A/B job; assert center, zoom, bounds unchanged |
| **C pan buffer covers a small actual pan** | Cache C entry; user pans by < buffer; assert cache hit |
| **Cross-zoom reuse explicitly does not happen (current doctrine)** | Cache zoom Z entry; assert zoom Z+1 request is a cache miss (until reuse is implemented and validated) |

### 7.6 Regression harnesses

| Harness | Role |
|---------|------|
| `scripts/smoke_phase2_cache.py` | Current minimal smoke (passing). Extend per §7.1 gaps. |
| `validation/reports/phase2_cache_smoke.json` | Snapshot output; treat changes as signal |
| New: `scripts/smoke_phase2_cache_drainage.py` (proposed) | Run a full A → H drainage cycle without interruption; assert cache populated, budget respected, no `deferred_budget` for typical viewport |
| New: `scripts/smoke_phase2_cache_storm.py` (proposed) | Interruption-storm cycle (10 rapid actions); assert recovery to idle |
| New: `scripts/smoke_phase2_cache_chart_change.py` (proposed) | Two-chart cycle; assert invalidation |
| Substrate parity: `scripts/smoke_map_current.py` | Must still pass post-integration (no regression of existing overlay behaviour) |

A regression in any of these blocks the integration merge. This is
the *same* discipline as the substrate adaptive validation, applied
to the cache.

### 7.7 What validation cannot prove

| Limitation | Mitigation |
|------------|------------|
| Real-world user behaviour patterns | Telemetry (deferred); until then, the validated A → H order is the contract |
| Long-session memory growth | Manual long-session profiling on first product integration |
| Multi-chart cache contention | Currently single-chart; revisit when chart-switching becomes common |
| Server-side cache correctness | Deferred until server-side cache is built |

The validation strategy is honest about its scope. The smoke tests
prove what they prove; they do not prove the system is correct under
unobserved conditions. The discipline is: when a new condition is
exercised in production, write the smoke for it, then ship.

---

## 8. UX Implications

### 8.1 User perception of responsiveness

The cache is invisible. The user perceives:

| State | What the user feels |
|-------|---------------------|
| First request to a chart | Same as today: USER fetch latency, ~0.5 s for typical 720×450 viewport / single condition |
| Repeated request matching cache | Instant paint (no spinner, no network round-trip) |
| Zoom +1 / +2 after first request | Likely instant (if A/B warmed) or fresh USER (if interrupted) |
| Condition switch within cached set | Free if D/E/F warmed for that condition; fresh USER otherwise |
| Pan within buffer | Free if C warmed; fresh USER otherwise |
| Pan beyond buffer | Fresh USER, same as today |

The product never tells the user "cache is warm." There is no cache
indicator, no warm-up progress, no celebratory paint. The user
notices subsequent actions feeling faster; that is the contract.

### 8.2 Progressive reveal pacing

The substrate's adaptive refinement has a visible refinement
character (`docs/PHASE_C_RENDERING_ARCHITECTURE.md` §9). The cache
does **not** introduce a *new* reveal pacing. A cached USER request
paints once, fully. A cache-miss USER request paints once, fully
(the substrate's adaptive refinement may visibly stage *within* that
single USER request; that staging is owned by the substrate, not the
cache).

**Forbidden:** introducing a reveal animation specifically to mask
cache-miss latency. The substrate's honest pacing is the only
permitted reveal source.

### 8.3 When to defer

| Situation | Defer because |
|-----------|---------------|
| Background job would exceed budget | `deferred_budget`; preserves the budget contract |
| Date mode inactive | H is `deferred_inactive`; transit caches need a date signal |
| `cachePaused` flag set after user interaction | `_maybeStartNext` is a no-op; background must not run during user gesture sequence |
| Server returning errors | Stop background warm-up; resume on next successful USER fetch |

### 8.4 When to interrupt background work

| Trigger | Behaviour |
|---------|-----------|
| `movestart` / `zoomstart` on the map | Immediate `pause()`; abort in-flight; clear pending |
| Condition change | Same as map interaction |
| Chart change | Same + invalidate entire cache |
| Tab backgrounded | Browser-controlled; on resume, next user action restarts cycle |
| Explicit "refresh" action | Same as map interaction; cache survives unless explicitly cleared |

The trigger set is **closed**. The doctrine does **not** support
"interrupt background work if the user is hovering over X" or other
predictive interrupts; those are telemetry-deferred.

### 8.5 Avoiding perceptual mush

The aesthetics doctrine forbids visual mush
(`docs/PHASE_C_RENDERING_ARCHITECTURE.md` §7.5). The cache must not
contribute to mush:

| Forbidden cache-driven UX | Why |
|--------------------------|-----|
| Paint cached "stale" overlay while new fetch resolves | Could show old chart's regions briefly; correctness hazard |
| Animate the transition between cache hit and cache miss | Decorative animation divorced from refinement |
| Show ghost outlines of cached but uncovered regions | Implies coverage that isn't there |

The cache contributes nothing visible to the user except latency
reduction. Period.

### 8.6 Preserving contemplative tone

The product temperament is "quiet analytical instrument"
(`docs/visual_semantic_style_guide.md` § 8). The cache fits this:

- No spinner during warm-up (it's invisible).
- No notification when warm-up completes.
- No "cache statistics" sidebar in default UI.
- Debug panels exist (`?debugCache=1` could be added) but stay
  debug-only.

The user is contemplating the map. The cache makes their next
contemplation faster. They never think about it.

---

## 9. Explicit Anti-Overengineering

This section names every temptation that arises during cache work
and rejects each with a reason. New temptations should be appended
here as they arise; doctrine drift toward "clever caches" is the
primary failure mode of this layer.

### 9.1 What not to build yet

| Tempting feature | Why deferred |
|------------------|--------------|
| Server-side shared cache | Adds auth / privacy / invalidation surface; client cache hasn't proven its scope yet |
| Persistent (`localStorage`) cache | Cross-session invalidation contract is unsolved; correctness risk |
| Sub-viewport tile cache | Substrate-level cache reuse not yet a measured need |
| Cross-zoom geographic index | Requires interior-occupancy reuse first |
| Condition-mask recombination | Backend semantics not formally validated; fixture matrix not in place |
| Aspect cache invalidation by orb change | Aspect orb changes are rare; full re-fetch is simpler |
| `localStorage` quota management | Not used; no quota to manage |
| Cache compression | Memory not a constraint at validated budget |
| Cache statistics UI | Debug-only at best; not a product surface |
| Background job priority pre-emption | Single-active model; pre-emption complicates correctness |
| `Worker` thread for cache management | Browser main thread handles current load |
| Telemetry collection | No telemetry infrastructure; cannot inform any design today |
| Mouse trajectory prediction | Speculative |
| Dwell-zone pre-fetch | Speculative |
| Pre-warming charts before request | Cross-chart cache forbidden |
| "Smart" pause heuristics | Pause-on-interaction is the rule; no smart |
| Re-issuing aborted background jobs without user action | Re-introduces work the user interrupted |

### 9.2 Telemetry-dependent future ideas

These all become legitimate only when:

1. Telemetry infrastructure exists.
2. It captures the relevant signal (cursor trajectory, dwell, etc.).
3. The new behaviour is demonstrated to outperform the static A → H
   order on a defined fixture set.

| Idea | Telemetry needed |
|------|------------------|
| Reorder A → H by historical user follow-up patterns | Sequence of user actions per session |
| Pre-warm condition combinations common for the user | Per-user condition history |
| Prioritise zoom +1 over +2 based on dwell at current zoom | Dwell timing |
| Cache eviction of unused entries | Cache-hit telemetry per entry |
| Predictive pan-direction warm-up | Cursor trajectory / pan vector telemetry |

Without telemetry, every one of these is speculation. The doctrine
forbids speculation disguised as requirement.

### 9.3 Predictive behaviours that remain deferred

Beyond telemetry-dependence, these have additional structural
constraints:

| Behaviour | Additional constraint |
|-----------|----------------------|
| Cross-chart pre-warming | Cache is per-chart by contract; would require per-user identity |
| Speculative transit pre-warming | Transits are date-dependent; speculative warming is invalid |
| Pre-warming for "likely next chart" | Cache is per-current-chart; multi-chart is a separate doctrine pass |
| Server pushing cache entries to the client | Push-based cache needs WebSocket or SSE; not in scope |

### 9.4 Unnecessary complexity risks

Each of these risks would land as a "small improvement" that
silently violates a doctrine clause:

| Pattern | Doctrine clause it violates |
|---------|----------------------------|
| "We can serve the prior cache entry while the new fetch resolves to feel faster" | `relocation_map_architecture.md` § "No half-cached entries"; serves wrong data |
| "Let's parallelise background jobs for throughput" | Single-active-job model; introduces race conditions |
| "Cache entries should expire after N seconds" | TTL eviction; no astrology input varies with wall-clock time today |
| "Let's predict cache hits with a Bloom filter" | Cache is small; full Map lookups are O(1); no optimisation pressure |
| "Server-side cache will simplify everything" | Adds distributed-state correctness surface; client cache hasn't proven its scope yet |
| "The user usually pans east, so let's bias C eastward" | Telemetry-dependent; speculation today |
| "Let's add a 'pre-fetch on hover' to the dropdown" | Mouse-prediction; speculation today |

The pattern: each one sounds small, each one introduces a correctness
surface or a new dependency. The cache is correct *because* it is
small. Growth is gated on measured evidence.

---

## 10. Recommended Implementation Order

The integration is a sequence of small, reversible, separately-validated
steps. Each step has a smoke gate; failing the gate blocks the next.

### Step 0 — Substrate path decision (prerequisite)

Per §1.3, the production map's overlay path differs from the cache
sandbox's. Pick a path **before** writing code:

| Decision | Cost | Recommendation |
|----------|------|----------------|
| (a) Migrate `map_CURRENT.html` overlay path to `/screen-pixel-truth` first | Larger change; substrate fix lands with the cache | **Preferred** if the substrate's adaptive refinement is the long-term overlay; aligns one substrate, then wraps it in the cache |
| (b) Wrap the legacy `/search-regions` path with a cache layer | Smaller change; cache lands first | Acceptable as a transitional step; legacy bugs persist until (a) lands later |

This document recommends (a) but does not mandate. The choice
should be recorded in `ai_context/decisions.md` as part of step 0.

### Step 1 — Extract the scheduler

Move the cache scheduler logic out of `map_SANDBOX_phase2_cache.html`
into a standalone module: e.g. `static/phase2_cache_scheduler.js` or
equivalent.

| Sub-step | Validation |
|----------|------------|
| Extract scheduler verbatim, keep sandbox unchanged | `scripts/smoke_phase2_cache.py` still passes against the sandbox |
| Document the public API (window-side `__phase2` surface) | Inline JSDoc; mirrors current sandbox |
| Confirm scheduler is endpoint-agnostic | Same scheduler can drive `/screen-pixel-truth` or `/search-regions` based on a configured fetch function |

### Step 2 — Wire `map_CURRENT.html` user actions

| Sub-step | Validation |
|----------|------------|
| Import the extracted scheduler | Smoke against `map_CURRENT.html` start-up |
| Wire `map.on("movestart zoomstart")` → `onUserAction` | Manual: map gesture pauses background; verify in console |
| Wire `findRegions()` (or its equivalent) → `serveUser()` | Manual: USER request flows through scheduler |
| Confirm existing `currentRenderToken` cancellation still works | Existing `scripts/smoke_map_current.py` still passes |

### Step 3 — Replace the USER fetch with the scheduler's fetch

| Sub-step | Validation |
|----------|------------|
| Route the production map's USER fetch through `SCHEDULER.serveUser()` | Cache populates with USER entry on first paint |
| Verify cache hit on repeated identical request | Add to smoke: issue identical request twice; assert second is a cache hit |
| Verify chart-change invalidation | Add to smoke: switch profile; assert prior cache entries gone |

### Step 4 — Register the background queue after first paint

| Sub-step | Validation |
|----------|------------|
| Call `registerBackgroundJobs()` after first USER completes | Background queue populates per A → H |
| Wait full drainage on idle viewport (no user actions) | New smoke (`smoke_phase2_cache_drainage.py`) asserts A → G complete, H deferred-inactive, all within budget |
| Verify cache hit serves the next user request | Pre-warmed zoom +1 request returns from cache; assert in smoke |

### Step 5 — Smoke storm and chart-change cases

Per §7.6. Two new smokes:

- `scripts/smoke_phase2_cache_storm.py` (interruption-storm recovery)
- `scripts/smoke_phase2_cache_chart_change.py` (per-chart invalidation)

Both must pass before the integration is considered complete.

### Step 6 — Document the integration

Land a new narrative:

- `validation/narratives/phase2_cache_product_integration.md`

Following the supersession + cross-reference conventions of
`docs/PHASE_C_RENDERING_ARCHITECTURE.md` §8. The sandbox narrative
`validation/narratives/phase2_cache_implementation.md` remains as
implementation-of-protocol; the new narrative documents the
product-integration shape.

### Step 7 — Production correction: E-priority signs

Per §4.7, the sandbox's E-priority uses placeholder signs. The
production integration **must** read the relocated chart's actual
ASC/DSC/MC/IC signs. Add to the integration step explicitly so the
production E job caches the four meaningful entries, not all 48 or
the four placeholder ones.

### Step 8 — Aesthetic pass (downstream, separate scope)

After Steps 0–7 land and pass, the aesthetics pass per
`docs/PHASE_C_RENDERING_ARCHITECTURE.md` §10 step 3 becomes
unblocked. The cache must be in place because aura intensity is
opacity composition over the substrate's discrete bands, and those
bands warm into the cache.

---

## 11. Discoveries While Grounding This Document

Audit trail of tensions surfaced while reading the sandbox, the
smoke, and `map_CURRENT.html` to write this charter. Each is named
so future work can decide it; this document does not solve them.

### 11.1 The substrate-path mismatch (§1.3) is the dominant gap

`map_CURRENT.html`'s production overlay still uses `/search-regions`.
The Phase-2 cache sandbox uses `/screen-pixel-truth`. Integration
without addressing this mismatch produces a cache that caches a
different substrate than the production renderer asks. **Step 0**
of §10 names the decision; the doctrine recommends migrating first.

### 11.2 The smoke proves cancellation, not warm-up

`validation/reports/phase2_cache_smoke.json` shows
`background_completed: 0` and `cache_keys_count: 1`. The smoke
deliberately interrupts before any background job completes. **§7
proposes** new smoke tests (`smoke_phase2_cache_drainage.py`,
`smoke_phase2_cache_storm.py`,
`smoke_phase2_cache_chart_change.py`) to close that proof gap.
These are required before the cache integration is considered
production-ready.

### 11.3 The sandbox's fixed-block (block=8) vs the substrate's adaptive

The sandbox sends a fixed `block=8` uniform point grid to
`/screen-pixel-truth`. The substrate doctrine targets adaptive
refinement converging toward 1 px locally. The cache stores
whatever block size the request used. **Open decision:** does the
cache warm at the substrate's near-final block (2 px) or at a
coarser block (8 px)?

- 2 px → larger payload (~36 k points at 720×450); accurate near-final
- 8 px → smaller payload (~5 k points); near-final adaptive still
  needed on serve

Recommended (this document): warm at the substrate's near-final
block (2 px) so that cache hits serve the visible-overlay-ready
output directly. The adaptive 1 px local refinement on top of cache
hit is then narrow. Decide explicitly in step 0.

### 11.4 The sandbox's E-priority placeholder sign

§4.7. The production integration must read actual relocated signs.
Step 7 of §10 names it explicitly.

### 11.5 `IDLE_GRACE_MS = 200`

Defensible as a post-completion grace, not a "timer from first
paint." The doctrine clause forbidding timer-based behaviour
explicitly targets the latter. 200 ms is small and absorbs gesture
flurries; future tuning is measured-evidence-only.

### 11.6 D-job aggregate "done" semantics

The 20 D sub-jobs collectively constitute "priority D." Done-ness
is per-sub-job, not aggregate. A user benefits incrementally as
each Sun-houses-1-6, Moon-houses-1-6, etc. completes. There is no
single "D is done" event today, and the doctrine does not require
one. If a future product surface needs an "all-house lookups are
free" indicator, that's a small UI affordance, not a substrate
change.

### 11.7 Cache eviction is not implemented

§5.2. Browser memory is not a constraint at the validated budget.
If a future budget rises or per-sample state grows, eviction
becomes a doctrine pass of its own. Until then, no eviction.

### 11.8 Cross-chart cache contamination is impossible by key shape

The cache key includes `chart` (profile id + birth instant). Two
charts cannot collide. Chart change invalidates the whole cache
(coarse invalidation, §3.6). No cross-chart logic to validate;
the absence is the validation.

---

## 12. Recommended Next Implementation Step

**Step 0 — substrate path decision.** Before any code lands, record
the path choice in `ai_context/decisions.md`:

> The production-visible overlay path for `map_CURRENT.html` will be
> migrated to `/screen-pixel-truth` (Path (a)). Phase-2 cache
> integration begins after this migration. OR The Phase-2 cache will
> wrap the existing `/search-regions` path as a transitional step
> (Path (b)); substrate migration follows.

After Step 0, Step 1 (extract scheduler) is the smallest reversible
piece of work; it ships with no behavioural change to the sandbox or
to the production map. Each subsequent step composes onto it with
its own smoke gate.

The integration is **structural hardening**, not a feature. It does
not change what the user sees today; it changes how fast the user
sees what they ask for tomorrow. That is the contract.

---

## 13. Document Provenance

| Field | Value |
|------|------|
| Author surface | Architecture draft, this conversation |
| Reviewed against | `map_SANDBOX_phase2_cache.html`, `scripts/smoke_phase2_cache.py`, `validation/reports/phase2_cache_smoke.json`, `main_centerline_FIXER.py` (endpoints), `map_CURRENT.html` (current overlay path) |
| Authority on conflict | `docs/relocation_map_architecture.md` (§ "Phase 2 cache priority protocol") then `docs/PHASE_C_RENDERING_ARCHITECTURE.md` |
| Supersedes | Nothing |
| Operationalises | `docs/PHASE_C_RENDERING_ARCHITECTURE.md` §10 step 1 |
| Status | Design only; no code authorised |

When this document and any other doc disagree, this document yields
to the foundational architecture and to the Phase C charter, and
otherwise wins until explicitly amended in writing.
