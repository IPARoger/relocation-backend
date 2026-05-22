# Phase C — Rendering Substrate Architecture (Governing Laws)

> **Status:** Foundational. Constitutional charter for the rendering substrate
> as it stands at the close of substrate engineering and the opening of the
> aesthetics pass.
> **Authority:** `docs/relocation_map_architecture.md` wins on direct conflict.
> This document **consolidates and extends** that architecture; it does not
> override it.
> **Adopted draft:** 2026-05-21 (same-day as the rendering doctrine reset).
> **Stability:** Slow. Implementation details around this doctrine may rev;
> this file does not, except by explicit edit naming the prior stance and
> the reason for the change.
> **Purpose:** Define the governing laws of the *rendering civilization* so
> future agents, contributors, and reviewers cannot quietly regress toward
> fixed global grids, naive polygon assumptions, premature optimisation,
> renderer-wide slowdown for local instability, visual mush, geometry-first
> thinking, cache-over-user-responsiveness, or erasure of archaeology.

---

## 0. Where this document sits

| Layer | Document | Role |
|------|----------|------|
| Orientation | `docs/CURRENT_RENDERING_DOCTRINE.md` | One-page “where we are now” |
| Foundational architecture | `docs/relocation_map_architecture.md` | Immediate-truth + opportunistic-expansion |
| **Substrate laws (this file)** | `docs/PHASE_C_RENDERING_ARCHITECTURE.md` | Governing laws of the substrate at the close of substrate engineering |
| Visual semantics | `docs/visual_semantic_style_guide.md`, `docs/overlay_and_aura_visual_strategy.md` | What visuals *mean* |
| Experience tone | `docs/ux_principles_and_emotional_tone.md`, `docs/brand_and_experience_foundations.md` | How the product *feels* |

This is **substrate doctrine**, not aesthetic doctrine. It governs how the
renderer computes, classifies, refines, caches, and exposes truth. It does
not specify palette, opacity curves, or copy.

---

## 1. Canonical Rendering Truths

### 1.1 The four absolute statements

These are inherited from `relocation_map_architecture.md` and made explicit
here as **non-negotiable**:

1. **Every point on Earth already has a real relocation state.** The
   renderer never invents geometry. It classifies reality, reveals the
   requested condition, and progressively caches surrounding reality.
2. **Brute force is the canonical truth layer.** Every optimisation must
   answer "is this cell in the requested condition?" with the same result
   as the brute-force endpoint, on every cell tested, or the optimisation
   is rejected.
3. **Screen-space is the canonical *sampling axis* for visible overlays.**
   The geographic lat/lon grid lives on as validation tooling; it is not
   the production renderer.
4. **Truth comes first, optimisation comes later.** Step 10
   (refinement acceleration) cannot begin until steps 3–9 in the
   architecture doc are visually and semantically stable.

### 1.2 Screen-space truth doctrine

The production renderer samples the **visible map**, not the **globe**.

| Property | Why it is canonical |
|---------|---------------------|
| Sampling axis = screen pixels (in tiles of `16 → 8 → 4 → 2 → 1`) | The geography the engine evaluates is identical to the geography the eye will look at. No grid spacing can ever fall coarser than the dot size. |
| Primitive painted = the tile that was sampled | Bug class #2 (drawing-primitive mismatch) cannot occur. |
| Per-world-copy sampling | Bug class #3 (world-copy mismatch) cannot occur. Each visible world copy generates its own screen pixels. |
| Re-sample on `zoomend` / debounced `moveend` | Bug class #4 (stale geographic grid reused across zoom) cannot occur. |
| Reference = full 1 px screen-space classification | Adaptive convergence is measured against this, **not** against a lat/lon grid. |

The lat/lon-grid `/brute-force-grid` endpoint remains in production source
as the **control specimen** and validation wall (`relocation_map_architecture.md`
§ "Brute Force as Control Specimen"). It must not be re-elevated to
production rendering. Any pull request proposing to do so must amend this
section.

> **Forbidden regression pattern:** "Sample a lat/lon grid and paint dots."
> This produces gaps at zoom, dashed centerlines, and one-world-copy
> overlay mismatch. Diagnosis: `validation/narratives/screen_pixel_truth_diagnosis.md`.

### 1.3 Adaptive refinement as production substrate

The adaptive screen-space refinement validated in
`validation/narratives/screen_pixel_adaptive_refinement.md` and hardened in
`validation/narratives/screen_pixel_adaptive_targeted.md` is the **production
substrate**. Its measured behaviour is:

| Case | Full 1 px samples | Adaptive samples | Reduction | Overlay XOR vs 1 px |
|------|------------------:|-----------------:|----------:|--------------------:|
| Sun in 1st, world | 576 000 | 70 329 | 87.8% | 0.140% |
| Saturn ☌ MC, orb 0.5, Pacific | 576 000 | 50 580 | 91.2% | 0.000% |
| Saturn ☌ ASC, orb 1, world | 576 000 | 56 168 | 90.2% | 0.000% |
| Triple overlap, Americas | 576 000 | 109 423 | 81.0% | 0.018% |

Adaptive refinement is **not** a cheaper alternative to brute force. It is a
*learned compression* of brute force, accepted only when it produces
brute-force-identical answers on the cells tested. The compression is
governed by **convergence against the screen-pixel reference**, not by a
fixed sample budget.

### 1.4 Why visible output is canonical

The product's truth contract is at the **point**, not at the cell, not at
the polygon, not at the abstract field. The popup is the canonical authority
for "what is true *here*" (`docs/visual_semantic_style_guide.md` § 1). The
visible overlay is canonical when it **agrees with the popup** at every
sampled cell.

Operational consequence: if a renderer is internally elegant but disagrees
with the popup on any cell, the renderer is wrong, not the popup.

### 1.5 Globe truth vs screen truth

| Layer | Granularity | Authoritative for |
|-------|-------------|-------------------|
| Engine (`swe.houses` per `(lat, lon)`) | Continuous geography | Per-point membership / orb / sign |
| Brute-force lat/lon grid | Fixed geographic spacing | "Does the field exist where we think it does" verification |
| Screen-pixel adaptive | Adaptive geographic spacing, fixed *visible* spacing | Per-pixel painted overlay |
| Popup | Single point | Final arbiter at a click |

The renderer's job is to **bridge** globe truth to screen truth without
changing membership semantics. The brute-force layer guards globe truth.
The popup guards point truth. The adaptive layer compresses globe truth
into a screen-pixel-faithful overlay. None substitutes for the others.

---

## 2. Convergence Strategy

### 2.1 Convergence is the contract; sample count is not

The substrate is judged by **agreement with screen-pixel reference**, not
by samples spent. The acceptance band is established as:

| Band | Overlay XOR vs full 1 px | Verdict |
|------|--------------------------|---------|
| `effectively identical` | ≤ 0.20% | Ship |
| `acceptable with visible edge residue` | 0.20%–0.40% | Ship, accepted residue (multi-overlap seams) |
| `failed / needs tighter refinement` | > 0.40% | Reject; tighten policy or escalate |

These bands are measured, not asserted
(`validation/narratives/screen_pixel_dense_residue.md`). Worst observed
under the active policy across the validated dense matrix is **0.386%**,
on the 5-condition Americas case. That is the *current accepted ceiling*.

### 2.2 Targeted escalation, never global slowdown

Extra refinement is deployed **only** at structural instability triggers,
listed below from `validation/narratives/screen_pixel_adaptive_targeted.md`
and `relocation_map_architecture.md` § "Refinement Hardening":

| Trigger | Extra halo | Condition |
|--------|------------|-----------|
| Tile within `2` tiles of **viewport edge** | `+2` halo | Always |
| Tile straddles **±65°** | `+2` halo | Case contains aspect-to-angle condition |
| **Thin-line aspect** (orb ≤ 0.5°) | `+2` halo + extra probes at ≥ 8 px tiles | Per occupied/mixed tile, every phase |
| Tile within `4°` of lat-cap (when `apply_lat_cap=true`) | Force-refine; no coarse early-accept-empty | Always when lat-cap on |

**Cases without an aspect-to-angle condition do not trigger high-latitude
or thin-line escalation.** Mid-latitude interior tiles in aspect-to-angle
cases keep the baseline halo. Anything in this paragraph that drifts toward
"always escalate, just in case" is a doctrine violation.

### 2.3 Refinement economy — *truth where unstable*

The economy of the substrate is:

1. **Stable empty regions** stop sampling almost immediately.
   Verified: empty-viewport adaptive passes converge at sparse depths
   with ≤ 1% of full-1 px samples.
2. **Stable filled interiors** accept as filled and stop subdividing.
   The interior of `Sun in 1st` polygons stabilises within two adaptive
   phases.
3. **Frontier regions** (transitions, centerlines, overlap seams) receive
   more samples, locally, down toward 1 px.

The thing that wins more samples is **uncertainty**, not radius from the
viewport center, not radius from a frontier, not a global "make everything
better" knob. Anything that escalates uniformly across the viewport is, by
definition, the wrong tool.

### 2.4 Local vs global refinement

| Decision | Made how |
|----------|----------|
| When to start refining | Per-tile probe lattice; mixed/occupied/halo-of-occupied tiles subdivide |
| When to stop refining (a single tile) | Probe agreement at the current tile size, or final phase reached |
| When to stop the **whole pass** | Convergence vs reference at the screen-pixel level, or sample-budget deferral |
| When to escalate the whole pass | Never globally; only the *triggers* in §2.2 can raise per-tile halos |

The convergence test runs against the **screen-pixel reference**. The
budget gate (currently `233 118` samples at +20% over worst observed for
720×450) is the **deferral signal**, not a silent truncation signal: a job
that cannot complete inside budget is *deferred* into the cache, never
served as a half-completed render
(`relocation_map_architecture.md` § "Phase 2 cache priority protocol",
"Budget enforcement").

### 2.5 Refinement hierarchy

The hierarchy is fixed; do not invent intermediate phases:

| Phase | Tile size | Role |
|-------|----------:|------|
| Exploratory | 16 px | Discover where occupancy exists |
| Regional | 8 px | Concentrate around occupancy + 1-tile halo |
| Boundary | 4 px | Concentrate at occupancy and transition seams |
| Near-final | 2 px | Default visual surface for most production cases |
| Local fine | 1 px | Only inside remaining uncertainty; never global |

The `1 px` phase is **local** and intrinsic to corridors where the field
is narrow (thin-line aspect-to-angle, sharp sign-angle edges, polar
compressed corridors). It is not a global pass and must never be one.

---

## 3. Frontier Prioritization

### 3.1 What a frontier is

A **frontier** is any tile whose probe lattice disagrees with itself
(some probes match, some do not) **or** whose neighbour is occupied while
the tile itself probes empty (the one-tile halo). Frontiers are where the
geometry of the answer changes within the spatial budget of the tile.
Frontiers are the only thing in the substrate that earns deeper sampling.

### 3.2 Why active geometry deserves the resources

Three reasons (architectural, not aesthetic):

1. **The signal lives at the seam.** Stable interiors and stable empties
   contain no new information per added sample. Seam tiles contain *all*
   the geometry the next phase will paint.
2. **The eye reads the boundary first.** Map readability under translucency
   depends on edge fidelity, not interior fidelity
   (`docs/overlay_and_aura_visual_strategy.md` § E "Map Readability Is
   Sacred"). The renderer should spend its budget where the eye spends its
   attention.
3. **Overlap correctness lives on the boundary.** Multi-condition overlap
   is the product's primary decision object
   (`ai_context/core_product_truths.md`). Overlap regions are bounded by
   the intersection of frontiers; their correctness is the integral of
   per-frontier correctness.

### 3.3 Frontier clustering — observed shape

Across the validated cases (`screen_pixel_adaptive_refinement.md`),
frontiers cluster in three observable ways:

| Cluster | Geometry | Treatment |
|--------|----------|-----------|
| Polygon edges | One-cell-thick chains | Baseline halo, default phases |
| Thin-line centerlines (low-orb aspect-to-angle) | Sub-pixel corridors | Thin-line halo `+2`, extra probes; local 1 px convergence along the corridor |
| Multi-overlap seams | Polygons of 2+ overlapping conditions | Same baseline halo; residue accepted to `≤ 0.40%` XOR per §2.1 |

The substrate does not adopt a "bacterial growth" or stochastic frontier
expansion metaphor as policy. The validated metaphor is **deterministic
halo refinement** at structural triggers. Stochastic expansion is reserved
for the *aesthetic* layer (§9) where its truthfulness contract is the
sampled occupancy, not the visible bloom.

### 3.4 Why empty settled regions stop early

Three operational reasons:

1. **No information.** Settled empty has zero probe disagreement at the
   current tile size; further subdivision is by definition wasteful.
2. **Budget discipline.** The 233 118-sample budget is sized at +20% over
   the worst observed structural case. Refining settled empties consumes
   that budget for cases that have nothing useful to refine.
3. **User responsiveness.** Phase-1 wall-clock latency is a contractual
   obligation (`relocation_map_architecture.md` § "Phase 1 — Immediate
   Response"). Settled-empty refinement directly trades latency for no
   information gain. Forbidden.

---

## 4. Stopping Doctrine

### 4.1 When refinement stops

A tile stops refining when one of the following is true, in order of
specificity:

| Condition | Meaning |
|-----------|---------|
| **Probe stable empty** | All probes agree the tile is empty |
| **Probe stable filled** | All probes agree the tile is filled for the same condition mask |
| **At leaf size** (1 px) | Tile is at terminal resolution; no further subdivision possible |
| **Reference parity** | The reconstructed overlay agrees with the screen-pixel reference at this region |

A pass stops when:

| Condition | Meaning |
|-----------|---------|
| **All tiles stable** | No frontier remains |
| **Convergence vs reference** | Overlay XOR ≤ §2.1 acceptance band |
| **Budget deferral** | The pass would exceed the per-viewport sample budget; deferred to cache, never partially served |

### 4.2 Acceptable residue

Residue is acceptable **only** at multi-overlap transition seams, and
**only** below 0.40% XOR
(`validation/narratives/screen_pixel_dense_residue.md`).

| Residue location | Acceptable? |
|------------------|-------------|
| Stable single-condition interior | No |
| Stable empty region | No |
| Polygon edge of any single condition | No (must converge under §2.2 escalation) |
| Multi-overlap transition seam, ≤ 0.40% XOR | **Yes** — accepted; further reduction would cost samples without changing the human verdict on map-context review sheets |
| Centerline of the thin-line aspect itself | No (must reach 0.000% XOR; structural target) |

### 4.3 Exactness doctrine

Exactness is required where the product **promises** exactness:

| Element | Exactness target |
|---------|------------------|
| Aspect-to-angle centerline | 0.000% XOR vs 1 px reference |
| House polygon boundary (single condition) | ≤ 0.20% XOR |
| Angle-in-sign polygon boundary | ≤ 0.20% XOR |
| Multi-overlap seam | ≤ 0.40% XOR |
| Lat-cap edge (when on) | Forced refinement within 4° of cap |

Exactness is **not** required where the product is honest about its
limits: above the ±65° polar cap (when on), the product does not promise
truthful answers and must not render them
(`relocation_map_architecture.md` § "Polar Placidus error rendering",
unresolved UX call documented in `ai_context/open_questions.md`).

### 4.4 Deterministic ties

If two refinement decisions produce the same outcome at the same point —
e.g. tile probes split 2/2 — the deterministic resolution is:

| Tie | Resolution |
|-----|------------|
| Probe split at a tile | Subdivide; do not flip a coin |
| Stable-filled vs stable-empty disagreement between adjacent tiles | Subdivide both at the shared edge |
| Convergence band boundary (Δ at the exact threshold) | Round toward more refinement, never less |

There is no stochastic decision permitted inside the substrate's
classification path. The astrology call (`swe.houses`) is deterministic;
the renderer must remain deterministic on the same inputs.

### 4.5 Diminishing returns

A refinement step that reduces overlay XOR by less than the noise floor
of the underlying engine call (in practice, well under 0.01% for a single
additional refinement phase on a converged case) is **not** an
improvement; it is sample consumption.

Operationalisation: the policy sweep in `screen_pixel_adaptive_targeted.md`
records the sample cost of each escalation step. The chosen policy
(`edge2_thin2_highlat2_probes`) sits at the inflection point where the
next escalation `edge3_thin3_hl3_latcap3_nocoarse2` costs ~22% more
samples to convert zero additional failing cases.

**Doctrine rule:** the next refinement escalation must demonstrate that
it reduces the failing-case set, not merely that it reduces XOR on cases
already in the accepted band. Otherwise it is a cost without information.

---

## 5. Cache Doctrine

### 5.1 User-first interruption

The cache is a user-first opportunistic substrate, not a render
accelerator that may delay the user. The full protocol lives in
`relocation_map_architecture.md` § "Phase 2 cache priority protocol" and
the implementation sandbox in `validation/narratives/phase2_cache_implementation.md`.

**Hard rules (restated, normative):**

1. First paint = user-requested conditions only.
2. Any `zoom` / `pan` / condition change pauses the cache, aborts in-flight
   background requests, serves the user, then resumes.
3. No half-cached entries: a slot is fully populated and marked ready, or
   discarded.
4. Background work runs only during idle (no user events for a grace
   window; idle is event-derived, not timer-derived from first paint).
5. Each background task is cancellable mid-flight without leaving partial
   state.

### 5.2 Immediate-render priority

Phase-1 priority is unconditional:

1. **speed**
2. **truth**
3. **trust**
4. **clarity**

Speed is at the top **only because** truth is already guaranteed by the
substrate (every served render is brute-force-equivalent on the cells
tested). If speed ever conflicts with truth, truth wins; this is enforced
by the rule that adaptive refinement is accepted only when it converges
against the screen-pixel reference.

### 5.3 Resumable background work

Background priority order is A → H
(`relocation_map_architecture.md` § "Priority order while idle"):

| Priority | What |
|----------|------|
| A | Same condition, zoom +1, same center |
| B | Same condition, zoom +2, same center |
| C | Same condition, pan buffer (~25% margin) |
| D | All planet-in-house at visible samples |
| E | Angle-in-sign at visible samples |
| F | Aspect-to-angle for major planets × angles × aspects at default orb |
| G | Wider-orb / aura envelopes for F |
| H | Transits, only when date-mode signals are active |

Each priority is cancellable at any point. The cache holds only ready
entries. The budget gate (233 118 samples per viewport) defers, never
truncates.

### 5.4 Cache invalidation philosophy

Invalidation is **coarse and confident**, never clever:

| Trigger | Effect |
|--------|--------|
| Chart change (birth data) | Entire cache invalidated |
| Condition family change | Entries for that family invalidated |
| `apply_lat_cap` flip | Affected tiles invalidated |
| Zoom change | A/B/C priorities re-targeted; existing entries retained where bounds match |
| Pan within buffer | C priority advances; no invalidation |
| Pan beyond buffer | Treated as fresh user request |

The cache is **per-chart**. It does not cache other charts. Switching
the natal chart is an invalidation, not a multi-chart cache miss.

### 5.5 Future probabilistic prioritization (deferred)

A later iteration may reorder the A → H priority list using telemetry:
cursor trajectory, dwell on a control, statistical likelihood of follow-up
conditions for similar users. Any such addition must:

1. Preserve the user-first interruption rule.
2. Be documented as a measured win against the static order, not asserted.
3. Stay invisible to the user (no spinner, no flicker, no pre-fetch
   animation).

Until that evidence exists, the static priority order is the contract.

**Forbidden today:** mouse-prediction caching, dwell-zone pre-fetching,
multi-chart pre-warming, transit blanket caching outside date-mode signals.

### 5.6 Forbidden regression patterns (cache)

| Pattern | Why it fails |
|---------|--------------|
| Pre-warm everything eagerly | Blocks user; wastes compute; date-dependent transit pollution |
| "Smart" prediction without telemetry evidence | Asserted optimisation, not measured |
| Half-cached entries served as if complete | Correctness hazard and debugging trap |
| Server-side shared cache before client substrate is stable | Premature distributed-state complexity |
| Caching that survives chart change | Cross-chart contamination |

---

## 6. Stress Doctrine

The substrate is hardened against a fixed set of known stress classes.
Each class has a measured policy response. New stress classes that arise
must follow the same shape: name, fixture, validation pass, doctrine note.

### 6.1 Stress class inventory

| Class | Trigger | Policy response | Closed? |
|-------|--------|-----------------|---------|
| **Seam / dateline** | Viewport crosses ±180° | Per-world-copy sampling (screen-space substrate handles natively) | Yes |
| **Polar / high-latitude with aspect-to-angle** | Tile straddles ±65° + case has aspect-to-angle | `+2` highlat halo + lat-cap boundary forced refinement | Yes (`high_svalbard_latcap_off` 5.615% → 0.000%) |
| **Cusp ambiguity** | House membership flips across cusp at sub-pixel scale | Baseline refinement to 1 px in local corridor; cusp display softness is a *visual* layer on top (see §7) | Substrate yes; visual policy deferred to aesthetics pass |
| **Overlap density (5–6 conditions)** | Multi-condition seams | Targeted policy; residue ≤ 0.386% XOR accepted | Substrate yes; condition cap is at 6 (`_MAX_CONDITIONS`); 7–8 deferred |
| **Narrow aspect corridor (orb ≤ 0.5°)** | Sub-pixel-thin centerline | Thin-line `+2` halo + extra probes at ≥ 8 px tiles | Yes (`thin_pluto_square_asc_0p25` 0.415% → 0.000%) |
| **Viewport edge** | Narrow lines exiting the screen | `+2` edge halo | Yes |

### 6.2 Acceptable localized escalation

The substrate **may** spend more samples locally on a stress class than
on a baseline tile, **as long as**:

1. The escalation is triggered only by the structural condition (§2.2).
2. The escalation does not slow tiles that do not trigger it.
3. The escalation reduces a failing-case set, not merely a passing one.
4. The total per-viewport cost stays within the +20% safety budget.

These are not soft preferences. They are the gate for any future
escalation rule.

### 6.3 Where the substrate refuses to compensate

| Failure mode | Substrate response |
|--------------|--------------------|
| Placidus undefined above ±65° (cap off) | Substrate **does not invent membership**. Visual policy must label, not render. |
| Sub-grid-level sub-pixel orb at extreme zoom | The substrate goes to 1 px; below 1 px is `Option C` precomputed tile space, deferred (`screen_pixel_truth_diagnosis.md` § Option C) |
| Engine call fails at a single point | Treated as a missing sample; the tile does not paint; not painted as empty, not painted as filled |
| Multi-overlap seam below 0.40% XOR | Accepted residue; refusal to spend more samples for no human-verdict change |

The substrate's refusal to compensate is itself a doctrine: any future
work that adds cosmetic compensation for these (blur, feather, neighbour
inference, dead-reckoning fill) is a rejection of canonical truth.

---

## 7. Rendering Philosophy

This section is **substrate-adjacent** (it constrains how the substrate's
output may be styled) rather than substrate proper. The substrate produces
honest tile-level occupancy; the renderer chooses how to express it.

### 7.1 Readability over saturation

`docs/overlay_and_aura_visual_strategy.md` § E and
`docs/visual_semantic_style_guide.md` § 6 are the authority. Restated:

- Map readability is sacred. The Earth layer must remain visible under
  every overlay state.
- Translucency is the legitimate knob. Saturation is the legitimate knob.
  Dot density is the legitimate knob (§D.0 of the overlay strategy doc).
- Blur, feather filters, gaussian widening of lines, and post-process
  glow are **not** legitimate knobs.

### 7.2 Overlap as meaning

Overlap is the product's primary decision object
(`ai_context/core_product_truths.md`). The renderer treats overlap as a
**semantic** object, not an opacity-stacking artefact:

- Future palette work uses **deliberate child colors** for known overlap
  pairs (`docs/overlay_and_aura_visual_strategy.md` § B).
- Naive alpha mud is a regression. The substrate's per-tile mask carries
  enough information to drive deterministic overlap colors at paint
  time.
- Overlap regions must remain city-readable.

### 7.3 Translucency doctrine

Per `relocation_map_architecture.md` § "Aura Rendering Principles" and
the overlay strategy doc:

- Aura is **occupancy widening**, not blur. Each band is "cells within
  `|abs_sep − target| ≤ band_orb`", queried against the substrate at a
  sequence of widening orbs.
- The intensity curve from band edge to centerline is **non-linear and
  concave toward the line**: logarithmic, exponential, power-law, or
  sigmoid. Linear ramps are forbidden by doctrine.
- The intensity profile **compresses proportionally** with the corridor:
  a narrow sextile corridor reads with the same character as a wide
  conjunction corridor, at different absolute widths.
- The centerline is the strongest visual point. The mid-orb is **not**
  the loudest place.

### 7.4 Aura restraint

Aura is **a non-certifying field**. It does not define membership, orbs,
or legal "inside / outside" semantics. Authority remains on the exact
angular centerline and on point truth in the popup
(`docs/overlay_and_aura_visual_strategy.md` § "Doctrine: non-certifying
field"). The renderer must reflect this in its visual hierarchy:

- Centerline reads strongest.
- The first near-exact band reads materially visible.
- Outer bands read restrained.
- City labels remain legible at the relevant zoom.

If a candidate aura curve cannot satisfy both "centerline reads as
strongest" **and** "labels remain legible behind it", the candidate is
wrong and must be retuned. This is a hard constraint.

### 7.5 Anti-mush doctrine

Forbidden visual states, even when the underlying occupancy is truthful:

| Forbidden | Why |
|-----------|-----|
| Giant opaque washes | Buries the basemap |
| Muddy alpha stacking | Overlap reads as one synthetic region instead of multiple truths |
| Over-dense middle bands ("soft speed bump") | Mid-orb dominates; centerline is no longer strongest |
| Decorative GIS striping / hatch spam | Misreads as uncertainty bands; pollutes semantics |
| Atmospheric soup at dense city zoom | City labels become illegible |
| Cosmetic boundary smoothing (blur, antialias widening) | Visually moves the membership boundary |

### 7.6 Map-first philosophy

The map is the instrument. Controls, chrome, sidebar, debug panels,
onboarding affordances, and aesthetic flourishes **support** exploration
and then **recede**
(`docs/ux_principles_and_emotional_tone.md` § 2, § 9).

Operational consequences:

- Debug panels are debug-mode only (`debugGeometry`, `traceConditions`,
  `debugAdaptive`, etc.) and not present in default UI.
- Status text is restrained; user-facing status clutter stays hidden
  unless deliberately redesigned (`ai_context/current_state.md`).
- New visual layers earn their pixels against the map-first standard
  before shipping.

### 7.7 Elegance versus gimmick

The temperament is **quiet analytical instrument**, not performative
showcase
(`docs/brand_and_experience_foundations.md`,
`ai_context/core_product_truths.md` § "Emotionally non-interfering design"):

| Elegance (allowed) | Gimmick (forbidden) |
|--------------------|---------------------|
| Subtle staging tied to real refinement | Theatrical reveal divorced from computation |
| Calm typography that supports inspection | Marketing-banner typography |
| Honest translucency at restrained opacity | Neon, high-chroma accent soup |
| Restrained palette with child-color overlap semantics | Rainbow debug palette shipped as final |
| Aura that respects the centerline | Aura that glows like a notification |
| Cusp transition at categorical boundaries | Aura ramp reused for house cusps (semantic collision) |

The substrate is permitted to have a **visible refinement character** (§9)
only when that character is the visible surface of real computation. If
the same effect could be produced by a timer, a particle system, or a
shader without consulting the engine, it is gimmick and must be rejected.

---

## 8. Archaeology Doctrine

### 8.1 Preserve failed paths

The repository preserves:

- Superseded technical philosophy
  (`docs/technical_philosophy/progressive_field_reveal.md`,
  `docs/technical_philosophy/truth_field_rendering_path.md`).
- Superseded validation narratives
  (`polygon_reveal_sandbox_visual_qa.md`,
  `polygon_reveal_topology_target_v1.md`,
  `progressive_reveal_phase_b.md`,
  `screen_pixel_block_sweep.md`,
  `sun_conjunct_asc_truth_field_spine_phase_a.md` — see §11 for the
  last entry's reclassification).
- Diagnostic sandboxes not in production
  (`map_SANDBOX_brute_force.html`,
  `map_SANDBOX_screen_pixel_truth.html`,
  `map_SANDBOX_polygon_reveal.html`,
  `map_SANDBOX_truth_reveal.html`).

These are not deletions waiting to happen. They are evidence.

### 8.2 Mark superseded, do not erase

The convention is set:

- Add a `> **STATUS: SUPERSEDED** (date) — preserved as archaeology.`
  block at the top of the document.
- Name the **current replacement** and the **reason for supersession**.
- Add a warning against re-implementing from the superseded document.
- **Do not** delete content. The path the project did not take is part
  of the record of why the current path was chosen.

This convention is in active use across the rendering-philosophy folder
and the validation narratives. Future supersessions must follow the
same shape.

### 8.3 Preserve why, not only what

A superseded document without a **why** turns into a future temptation.
The reasons are the institutional immune system. The required content
for a supersession header is:

1. What the document was.
2. Why it was superseded (the architectural mistake or wrong target).
3. The current canonical document.
4. An explicit warning against re-implementing without doctrine review.

### 8.4 Anti-backsliding principles

The repository's anti-backsliding immune system has three layers:

| Layer | Mechanism |
|-------|-----------|
| Document-level | Supersession headers (§8.2) |
| Index-level | `docs/CURRENT_RENDERING_DOCTRINE.md` lists every superseded doc with reason |
| Code-level | Validation suites (`scripts/smoke_*.py`, `validate_sprint_dc_ic.py`, benchmarks) refuse merges that regress the substrate |

A doctrine drift not visible at all three layers is the kind of drift the
repository is designed to catch. Future PRs that propose to revive a
superseded approach must amend the supersession headers in writing — not
just write new code under the old shape.

### 8.5 What may not be deleted

- Validation narratives.
- Validation reports (`validation/reports/*.json`).
- Validation screenshots, where they document a fixture or regression.
- Superseded doctrine docs.
- Sandboxes (`map_SANDBOX_*.html`) that produced doctrine evidence.

Workspace cleanup is governed by
`docs/workspace_hygiene_and_cleanup.md`; that document does not authorise
deletion of archaeology. The boundary is: scratch artefacts, browser temp
folders, local secrets, partial benchmark scratch directories — yes;
narratives, reports, supersession headers — no.

---

## 9. Reveal / Aesthetic Implications

This is the **bridge to the aesthetics pass**, not the aesthetics pass
itself. It documents what the substrate makes possible without committing
to a specific visual.

### 9.1 Refinement as visible process

The substrate already has a visible refinement character: tile sizes
shrink in well-defined phases (16 → 8 → 4 → 2 → 1) and the regions that
refine are exactly the regions where the field is geometrically
interesting.

This is **the legitimate raw material** for a future "computation as
identity" visual language. The relevant property: the visible motion is
the visible surface of real refinement, not a render-time animation
layer.

### 9.2 The raindrop / virga model

Earlier exploration of stochastic refinement as an animation metaphor
(the "raindrop model" in
`validation/narratives/screen_pixel_adaptive_refinement.md` §
"Architectural conclusion") is reframed:

- The raindrop model is **computational first**: it is the visible form
  of adaptive truth discovery.
- It may later be expressed visually as a layered staging metaphor —
  sparse exploratory probes, occupied regions gaining density, empty
  regions remaining quiet, boundaries converging to local 1 px truth.
- It is not, and must not become, a particle system divorced from the
  refinement pipeline. There are no random raindrops. Every visible
  element is a real tile or a real sample.

### 9.3 Pacing philosophy

Pacing is governed by **real refinement timing**, not by aesthetic
preference for a duration:

- Each phase paints when its work completes.
- If the work completes in 200 ms, the user sees 200 ms.
- If it completes in 2 s, the user sees 2 s, and that 2 s is honest.
- A target wall-clock budget exists (Phase-1 first-paint contract) but
  it is enforced by the **substrate's** refinement economy, not by a
  client-side timer that "smooths" the pacing.

### 9.4 Convergence aesthetics

The substrate's convergence has a measurable visual signature:

| Phase | Visual character |
|-------|------------------|
| 16 px | Sparse, coarse, low-fidelity overlay; clearly provisional |
| 8 px | Regional shape emerging |
| 4 px | Boundary structure visible |
| 2 px | Near-final; default visual surface |
| 1 px local | Centerline / overlap seam crispness |

The aesthetics pass may *use* this signature (e.g. provisional tiles
read with lighter weight or dashed indication in a future advanced
mode). The aesthetics pass may *not* invent a signature uncoupled from
the phases.

### 9.5 Magic versus noise

The line is drawn empirically and operationally:

| Magic (allowed) | Noise (forbidden) |
|-----------------|-------------------|
| The user perceives the map *clarifying* | The user perceives the map *flickering* |
| Provisional reads as provisional | Provisional reads as final and then changes |
| Final stage is visually quiet and sharp | Final stage flashes a celebratory bloom |
| Refinement runs once per user request | Refinement runs on a timer |
| Stages replace, not stack | Ghost layers accumulate |

A useful test: take a screenshot at phase N and a screenshot at phase
N+1. The XOR of the two screenshots must equal exactly the set of
pixels that legitimately changed classification. Anything else is noise
the renderer added.

### 9.6 Delight budget

Delight is **scarce and earned**:

- Delight from exploration, not from UI theatrics
  (`ai_context/core_product_truths.md` § "Emotionally non-interfering").
- Subtle delight: smooth staging, thoughtful typography, readable
  defaults
  (`docs/ux_principles_and_emotional_tone.md` § 3).
- Excitement from the *answer*, not from the *animation*.

The substrate's delight budget for visible refinement is: **one
honest reveal per user request**, **gated by debug or settings**, never
default-on without a measured user-study win. This is the position
inherited from
`docs/technical_philosophy/progressive_field_reveal.md` (superseded) and
ratified by the current doctrine.

---

## 10. Future Implementation Order

The order is normative. Steps may not be skipped without a doctrine
amendment naming the new stance.

### Step 1 — Phase-2 cache integration (substrate, **next**)

| What | Status |
|------|--------|
| Extract scheduler from `map_SANDBOX_phase2_cache.html` into a shared module | Open |
| Wire `map_CURRENT.html` map events to `onUserAction` | Open |
| Connect date-mode UI to `setDateModeActive` | Open (transit UI not yet built) |
| Confirm cache cancellation under repeated zoom/pan | Smoke covered by `scripts/smoke_phase2_cache.py` |

**Why first:** The cache is the only substrate gap between the validated
sandbox and the production product surface. Aesthetics work without the
cache is structurally premature: aura intensity is opacity composition
over the substrate's discrete bands, and the bands are produced by the
same engine the cache warms.

### Step 2 — Adaptive renderer production integration

| What | Status |
|------|--------|
| Migrate `map_CURRENT.html` overlay path to the screen-space adaptive substrate | Partial; product UI still on legacy paths |
| Verify popup parity at sampled cells | Existing validation; extend on integration |
| Confirm dense-residue acceptance band holds in product | Re-run `screen_pixel_dense_residue.md` matrix |

**Why second:** The substrate is validated in the sandboxes; the
product surface still uses pre-substrate paths in places. Closing this
gap unblocks the aesthetics pass to operate on a single canonical
overlay pipeline.

### Step 3 — Aesthetic sandboxing

| What | Notes |
|------|------|
| One throwaway sandbox per aesthetic question | Centerline-only aura, overlap palette, NOT exclusion, cusp transition |
| Feature flags, branches, or off-main prototypes | `docs/visual_semantic_style_guide.md` § 11 |
| One change at a time | `relocation_map_architecture.md` § "Critical Engineering Rule" |

**Why third:** Aesthetic work that touches the production map without
prior sandbox validation has a long history of regression. The
discipline is to land aesthetics on top of a fixed substrate, one
question at a time, with a fixture for each.

### Step 4 — Aura experimentation

The aura system per
`docs/overlay_and_aura_visual_strategy.md` § D and
`relocation_map_architecture.md` § "Aura Rendering Principles". Required
properties before any production use:

| Property | Constraint |
|----------|------------|
| Built from occupancy bands | `|abs_sep − target| ≤ band_orb` for a sequence of band orbs |
| Non-linear, concave-to-line intensity curve | Logarithmic / exponential / power-law / sigmoid; linear forbidden |
| Centerline is strongest | Hard constraint |
| Map readability under aura | Hard constraint |
| Proportional compression | The curve shape is invariant under corridor scaling |

The aura layer is permitted to ship under feature flag once a single
aspect family passes the substrate-parity and city-readability gates on
the validated fixture set.

### Step 5 — Overlap semantics (child colors)

The deliberate child-color system per
`docs/overlay_and_aura_visual_strategy.md` § B. Sequence:

1. Define parent colors for each condition family.
2. Define child colors for known 2-way overlaps.
3. Define behaviour for 3-way overlaps (calm, not noisier than 2-way).
4. Test against the validated dense-residue matrix; ensure overlap
   readability survives `dense_5_americas` (worst seam residue).

### Step 6 — Probabilistic refinement (deferred)

Reserved for after the substrate is stable in production and a
measurable failing-case set exists that targeted escalation cannot
close. The gate per §2.5 still applies: a new refinement rule must
reduce the failing-case set, not merely XOR on already-accepted cases.

If `truth_grid` becomes the default (per `ai_context/open_questions.md`)
the relationship between truth-grid sampling and screen-space adaptive
sampling becomes part of this step.

### Step 7 — Predictive caching (deferred)

Per §5.5. Requires telemetry, measurable win, invisible UX. Until
those exist the static A → H priority order is the contract.

### Step 8 — Transit overlays

Per `relocation_map_architecture.md` § "Transit Philosophy". The
substrate is already capable; the UI shape is frozen. This step is
about **wiring** the existing substrate to the transit UI surface,
not about new substrate work.

### Step 9 — House negative-space inference (future-only, gated)

Per `relocation_map_architecture.md` § "House Negative-Space
Optimisation — Future Only". Admissible only on the same validation
gate the rest of the substrate must pass. Until then, direct per-cell
classification remains canonical.

---

## 11. Discoveries from Grounding This Document

This section is the **audit trail** of contradictions and tensions
surfaced by re-reading the repo to write this charter. They are not
solved here; they are named so subsequent work can decide them.

### 11.1 Phase A / Phase B substrate vs current doctrine

The work landed earlier in this conversation thread —
`aura_field_engine.py` (Phase A reference truth, convergence metrics)
and the progressive-reveal transport (Phase B) — was produced before
the current doctrine reset to screen-space adaptive refinement.

The narratives are now marked SUPERSEDED:

- `validation/narratives/progressive_reveal_phase_b.md` — superseded.
- `docs/technical_philosophy/progressive_field_reveal.md` — superseded.
- `docs/technical_philosophy/truth_field_rendering_path.md` — superseded.

The Phase A narrative
`validation/narratives/sun_conjunct_asc_truth_field_spine_phase_a.md`
should be **reclassified as superseded** with a header pointing at
`docs/CURRENT_RENDERING_DOCTRINE.md` and
`validation/narratives/screen_pixel_adaptive_refinement.md`. This
charter is the right document to authorise that reclassification.

**Code implication:** `aura_field_engine.py` and its endpoints
(`/aura-raster`, `/aura-raster-adaptive`,
`/aura-refinement-reveal-stages`) are **archaeology**, not the
substrate the next aura pass will build on. Future aura work composes
opacity / saturation / dot density over the **screen-space adaptive
substrate**, not over the lat/lon scalar grid. The `aura_field_engine.py`
module may remain on disk as preserved exploration; it must not be
re-elevated to production rendering.

### 11.2 `truth_grid` vs screen-space adaptive

`ai_context/decisions.md` § "Architecture" still describes `truth_grid`
as "the canonical architecture direction for house overlays and other
binary region searches." The doctrine reset moves the canonical
**visible-overlay** path to screen-space adaptive. The relationship
must be made explicit:

- `truth_grid` remains the canonical **off-screen verification** tool
  for binary region truth.
- Screen-space adaptive is the canonical **production-visible** path.
- They are not in conflict if `truth_grid` is reframed as
  validation / verification tooling; they are in conflict if both
  claim the production overlay surface.

**Recommended resolution:** add a sentence to `ai_context/decisions.md`
clarifying that the production *visible-overlay* path is screen-space
adaptive, while `truth_grid` remains the binary-region truth-source for
verification. Out of scope for this document to do; named here.

### 11.3 Zoom edge-refinement gap

`docs/CURRENT_RENDERING_DOCTRINE.md` § "Remaining gaps" and
`docs/relocation_map_architecture.md` § "Zoom Strategy" both call out
that interior occupancy reuse on zoom is **not implemented**. The
sandbox re-solves the full viewport on pan/zoom. This is the most
substantive substrate gap behind the cache wiring.

### 11.4 Polar / Placidus policy

`ai_context/open_questions.md` § "Validation" notes the ±65° lat-cap
policy is not yet a decided product treatment ("hide", "stripe", "label
as unavailable"). The substrate's behaviour at the cap is correct
(force-refine within 4°; do not invent membership above). The product
treatment of points above is not.

### 11.5 Condition cap (6) vs dense matrix

`validation/narratives/screen_pixel_dense_residue.md` § "Endpoint cap
note" documents that 7–8 simultaneous conditions are out of scope until
`_MAX_CONDITIONS`, `_CONDITION_LABELS`, and the palette work are
raised. Not blocking today; named for the aesthetics pass.

### 11.6 Centerline reads stronger / labels remain readable

`docs/overlay_and_aura_visual_strategy.md` § E + `relocation_map_architecture.md`
§ "Aura Rendering Principles" both require "centerline is strongest"
AND "labels remain readable" simultaneously. No validated aura curve
exists yet that holds both at all zooms with all condition stacks.
This is **the** open visual question for the aesthetics pass.

---

## 12. Recommended Next Implementation Step

**Phase-2 cache integration into `map_CURRENT.html`** (§10 step 1).

This is the highest-leverage substrate work because:

- It is the only structural gap between the validated sandbox and the
  product surface (`CURRENT_RENDERING_DOCTRINE.md` § "Remaining gaps").
- It unblocks the aesthetics pass: aura intensity is opacity composition
  over the substrate's discrete bands; the bands warm into the cache; the
  cache must exist before the aura layer can paint without first-render
  delay.
- It is fully validated in sandbox (`scripts/smoke_phase2_cache.py`
  passes; protocol is implemented and measured).
- It does not touch astrology math, does not touch visual semantics, and
  preserves user-first interruption by construction.

**Order of work inside the step:**

1. Extract the sandbox scheduler into a shared module
   (`static/phase2_cache_scheduler.js` or equivalent).
2. Wire `map_CURRENT.html` map events to `onUserAction`.
3. Re-run the Phase-2 smoke against the product map.
4. Document the integration in a fresh
   `validation/narratives/phase2_cache_product_integration.md`,
   following the supersession + cross-reference conventions of §8.

After that lands, the aesthetics pass (`§10` step 3 onwards) becomes
the legitimate next surface of work.

---

## 13. Document Provenance

| Field | Value |
|------|------|
| Author surface | Charter draft, this conversation |
| Reviewed against | Repo state as of 2026-05-21 doctrine reset + 2026-05-20 Phase A/B archaeology |
| Authority on conflict | `docs/relocation_map_architecture.md` |
| Companion orientation | `docs/CURRENT_RENDERING_DOCTRINE.md` |
| Supersedes | Nothing (consolidates and extends) |
| Reclassifies as superseded | `validation/narratives/sun_conjunct_asc_truth_field_spine_phase_a.md` (recommendation, §11.1) |

When this document and any other doc disagree, this document yields to
`docs/relocation_map_architecture.md` and otherwise wins until
explicitly amended in writing.
