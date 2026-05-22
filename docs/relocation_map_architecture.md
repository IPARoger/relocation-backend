# Relocation Map Architecture — Immediate Truth + Opportunistic Expansion

> **Status:** Foundational architecture doctrine.
> **Adopted:** 2026-05-21.
> **Stability:** Slow. Implementation details rev; this file does not, except
> by explicit edit referencing the reason and the prior state.
>
> This document supersedes the implicit "reveal drives the solve"
> assumption that lived in
> `docs/technical_philosophy/progressive_field_reveal.md` and
> `docs/technical_philosophy/truth_field_rendering_path.md`. Brute-force
> classification is now the canonical truth layer; reveal/animation is
> a stylistic choice layered on top, never a substitute for truth.

## Core Principle

Every point on Earth already has a real relocation state.

The renderer does **not** invent geometry. It only:

1. **classifies reality** (per-point real `swe.houses` etc.)
2. **reveals requested reality** (renders the cells matching the
   current request, immediately)
3. **progressively caches surrounding reality** (uses the user's
   attention time as background compute time)

**Brute-force classification is the canonical truth layer.** All
future optimisation must preserve exact classification integrity:
the optimised path must answer "is this cell in the requested
condition?" with the same result as the brute-force endpoint, for
every cell, or the optimisation is rejected.

## Brute Force as Control Specimen

The brute-force renderer is **intentionally inelegant**. That is
the point. It is the control specimen. It guarantees correctness
by refusing every shortcut and asking the engine about every cell.
Everything else in the system is measured against it.

The discipline this creates:

- Brute force proves the **geometry** — the actual shape of every
  planet-in-house, angle-in-sign, aspect-to-angle, and transit
  occupancy polygon at the engine's true resolution.
- Brute force proves the **topology** — which polygons touch,
  which contain others, which are disjoint, where boundaries lie.
- Brute force proves the **overlap semantics** — what it means
  for a cell to satisfy two or three simultaneous conditions, and
  what the renderer should paint when that happens.
- Brute force proves the **transit occupancy** — every transit
  overlay must produce the same polygons brute force produces for
  the same `(transit moment, condition)` pair.
- Brute force proves the **centerlines** — every centerline must
  trace through the brute-force polygon, not through an
  approximation of it.

Only after each of those is proven does the question become:

> How **little** computation can produce the **same** truthful
> result?

That question is the real role of every "smart" technique we may
later layer on top:

- stochastic probes
- refinement passes
- adaptive density
- opportunistic caching
- zoom edge-refinement
- background expansion

These are *not alternatives to* brute force. They are *learned
compressions of* brute force, and they are accepted only when the
compression produces brute-force-identical answers on the cells we
test.

Stated philosophically: **we are no longer inventing geometry.
We are learning how to reveal already-proven geometry
efficiently.** That is the stronger architecture. Any future
proposal that conflicts with it must either be rejected or be
accompanied by a doctrine edit explaining the new stance.

## Aura Rendering Principles

Aura is the visual layer that sits on top of an exact aspect-to-angle
centerline. Its sole job is to convey *strength near exactness*. It
is not a separate astrology, not a separate geometry, and not blur.
The principles below are normative governance; the detailed
implementation prose lives in `docs/overlay_and_aura_visual_strategy.md`
and `docs/technical_philosophy/rendering_truth_over_cosmetics.md`.

### 1. Aura is deterministic occupancy widening, never blur

The aura is built from the same brute-force occupancy substrate as
every other layer. Each band is "cells within `|abs_sep − target| ≤
band_orb`" for a sequence of band orbs (e.g. `≤ 0.5°`, `≤ 1°`, `≤ 2°`,
`≤ 4°`). Each band is *truthful geometric distance from exactness*.
Rendering intensity emerges from **weighted opacity, saturation, and
density across the discrete bands** — never from gaussian blur,
feather filters, or glow effects.

### 2. Intensity must be non-linear from edge to centerline

A linear ramp is rejected. Intensity must follow a *non-linear*
curve — logarithmic, exponential, power-law, sigmoid, or another
deliberately concave-toward-the-line shape — so that:

- **Most of the aura remains restrained**: translucent, breathable,
  map-readable.
- **The strongest visual intensity is reserved for the centerline**
  (the exact-aspect band) and, optionally, the immediately
  neighboring near-exact band.

A linear edge-to-line ramp produces an opaque middle corridor that
fogs out the map; that outcome is forbidden by this doctrine even
when the underlying occupancy is truthful.

### 3. Map readability is sacred

The Earth layer — cities, coastlines, labels, political geography —
must remain readable beneath every overlay state. The aura system
is permitted to:

- Carry a strong (even near-opaque) **exact centerline**.
- Carry one materially-visible near-exact band immediately adjacent
  to that centerline.

The aura system is **not** permitted to:

- Produce giant opaque washes.
- Produce muddy overlap or atmospheric soup.
- Produce over-dense middle bands.
- Make labels illegible at the relevant zoom.

If a candidate aura curve cannot satisfy both "centerline reads as
strongest" and "labels remain legible behind it", the curve is wrong
and must be retuned. This is a hard constraint, not a polish-pass
preference.

### 4. The intensity profile must compress proportionally

When the corridor's total spatial width shrinks — at sextiles, in
compressed high-latitude houses, at user-tightened orbs, in narrow
angular corridors — the *same intensity curve must compress with it*.
The visual energy profile is what is preserved; the spatial width is
what changes. A tight sextile band, a polar-compressed corridor, and
a default conjunction band must all read with the same character
(restrained outer, sharp centerline) at different absolute widths.

### 5. The current palette is proof-of-concept only

The colors currently used in the brute-force sandbox (yellow / blue /
rose / green / orange / violet / deep slate) validate **overlap
semantics, occupancy logic, and blending mechanics** — they prove the
*math* is composable and reportable. They do not represent the
product's final visual language.

A dedicated graphics/design specialist pass is reserved for, later:

- base color system and child colors for overlaps,
- translucency hierarchy,
- accessibility,
- dark-map and light-map behaviour,
- emotional tone and perceptual harmony,
- label readability under every overlay state,
- contemplative-UX coherence.

Order is fixed: **truthful geometry first, beautiful restrained
visual language second.** No palette decision shipping today is
treated as final, and no future palette decision is allowed to alter
the underlying occupancy.

## Immediate UX Strategy

When the user requests a condition — for example *Sun in 1st house*,
*Jupiter in 10th house*, *ASC in Scorpio*, *Mars square MC* — the
engine must:

### Phase 1 — Immediate Response

Allocate **all** compute budget to the requested condition only.
Return the first truthful render as fast as possible.

The renderer must **not**, during Phase 1:

- precompute unrelated fields,
- block on a global cache to warm,
- render decorative animation, or
- smooth geometry artificially to mask incomplete work.

The priority order during Phase 1 is, in order:

1. speed
2. truth
3. trust
4. clarity

### Phase 2 — Background Opportunistic Expansion

Immediately after the first render appears, the engine begins
background caching of:

- all planets at every classified cell
- all houses at every classified cell
- all angle signs at every classified cell
- all angular distances at every classified cell
- (eventually) aspect-to-angle relationships

This happens invisibly while the user studies the map, pans, zooms,
or changes conditions. The user's attention time becomes compute
time. The first switch to a related condition should feel free
because the cache is already populated for the cells already on
screen.

### Phase 2 cache priority protocol

The background cache is **user-first**, never speculative-first.
The user's *next* request always interrupts the background cache;
the cache never delays a user response.

**Hard rules.**

1. **First paint.** Compute *only* the user's requested conditions
   for the current viewport at the current zoom. Background cache
   has not started yet.
2. **Interrupt on user action.** Any zoom, pan, or condition change
   immediately *pauses* the background cache. The new user request
   is served first. Background cache resumes only after the new
   immediate render completes.
3. **Resume on idle.** If the user is idle (no zoom / pan / edit
   for a small grace window), the engine begins the priority order
   below. Idle is detected by the absence of user events, not by a
   timer started on first paint.
4. **Date-dependent caches are conditional.** Transit caches are
   computed *only* when a date or date range is currently requested
   or strongly likely (a date picker is open, a date control is
   focused, or transits are toggled on). Transit cache is never
   eagerly populated.
5. **No mouse-prediction.** Cursor-direction and dwell-zone
   pre-fetching are explicitly **future telemetry-based
   optimisation**, not part of the protocol today. The current
   protocol must work without any predictive signal.

**Priority order while idle, after first paint.**

| Priority | What | Why |
|---|---|---|
| A | Same condition(s), **zoom +1** for same center | Next-most-likely user action is "look closer." |
| B | Same condition(s), **zoom +2** for same center | Two-step zoom-in convergence path. |
| C | Same condition(s), **pan buffer** around the current viewport (≈25% margin) | Anticipates small pan toward neighboring regions. |
| D | Same visible samples, **all planet-in-house** classifications (Sun → Pluto × houses 1–12) | Lets future planet/house switches feel free without re-solving. |
| E | Same visible samples, **angle-in-sign** for ASC / DSC / MC / IC | Common follow-up overlay; cheap because angles are already computed per cell. |
| F | Same visible samples, **aspect-to-angle** for major planets × ASC/DSC/MC/IC × major aspects, at default narrow orb | Most expensive natal layer; enables instant aspect-to-angle toggles. |
| G | **Wider orb / aura envelopes** for F | Aura bands are deterministic widenings of F, so the truth substrate must be ready before the aura layer can paint without delay. |
| H | **Transits**, only if date-mode signals are active | Conditional. Date dependence makes blanket transit caching invalid; we cache transits for the *current* moment / date / range only. |

**What is not in the priority order.**

- *Other charts.* The cache is per-current-chart. Switching the
  natal chart invalidates the entire cache.
- *Other viewports far from the current center.* Far pan beyond
  the buffer is treated as a fresh user request, not as something
  to pre-warm.
- *Speculative condition combinations the user has not signalled.*
  Six-condition stacks are not eagerly populated just because the
  endpoint allows them.

**Cancellation semantics.** Each background task must be
*cancellable mid-flight* without leaving a partial cache that
could be served as if complete. Either the cache entry is fully
populated and marked ready, or it is discarded. Half-cached
entries are not allowed; they are a correctness hazard and a
debugging trap.

**Budget enforcement.** Background cache stays within the
measured worst-case budget recorded in
`validation/narratives/screen_pixel_adaptive_targeted.md`
(currently `233,118` adaptive samples for a 720×450 viewport at
+20% over the worst observed case). If a priority would exceed
that budget for the current viewport, it is *deferred*, not
silently truncated; the doctrine prefers an empty cache slot over
a partial one.

**Future optimisation (deferred, not part of this protocol).** A
later iteration may use *telemetry-derived* signals — cursor
trajectory, dwell on a control, statistical likelihood of
follow-up conditions for similar users — to reorder this priority
list. Any such addition must:

1. Preserve the user-first interruption rule.
2. Be documented as a measured win against the static order above,
   not asserted.
3. Stay invisible to the user (no spinner, no flicker, no
   pre-fetch animation).

Until that evidence exists, the static priority order is the
contract.

## Zoom Strategy

Zoom must not trigger naive full recomputation. Instead the engine
must distinguish between:

- **interior occupancy** — cells whose classification we already
  know from a prior solve. These remain valid until the chart or
  the requested condition changes.
- **edge refinement** — cells along uncertainty bands (transitions
  between match and non-match) where the prior solve's spacing was
  coarser than the new zoom level can show.

When the user zooms in, only the edge refinement requires
additional density. The interior occupancy is reused.

A coarse world solve, a medium regional refinement, and a fine
local refinement all share the same underlying occupancy graph.
We are **refining uncertainty bands**, never **recomputing known
occupancy**.

## Refinement Hardening — Targeted Policy, Not Global Slowdown

The adaptive screen-space refinement does **not** apply a global
halo enlargement. The renderer keeps its measured baseline cost
on the cases where the baseline is already correct, and spends
extra samples *only* where structural triggers fire.

The targeted policy is normative and is documented end-to-end in:

- `validation/narratives/screen_pixel_adaptive_targeted.md` —
  measured policy sweep, before/after on the Svalbard failure,
  measured safety buffer (`+20%` = `233,118` adaptive samples for
  720×450), and the lat-cap recommendation.
- `validation/narratives/screen_pixel_dense_residue.md` —
  focused 5- and 6-condition matrix confirming the dense-overlay
  residue stays inside the `acceptable / effectively identical`
  to `acceptable with visible edge residue` band (worst `0.386%`
  XOR) under the targeted policy alone, with no new refinement
  rule required.

**Where extra resources are deployed.** Only when one of the
following structural triggers fires on a tile:

1. The tile is within a small tile-count margin of the **viewport
   edge** (narrow aspect lines that exit the screen).
2. The case contains an **aspect-to-angle** condition *and* the
   tile sits at **high latitude** (default ±65°, with a viewport
   high-latitude assist at ±55°).
3. The case contains an **aspect-to-angle** condition with
   **orb ≤ 0.5°** (thin-line refinement).
4. `apply_lat_cap=true` and the tile **hugs the lat-cap boundary**
   (within `4°` of ±65°). These tiles cannot early-accept as
   empty at coarse sizes; they must subdivide.

**Where extra resources are explicitly not deployed.**

- Cases without aspect-to-angle conditions never trigger
  high-latitude or thin-line escalation.
- Wide-orb (>0.5°) aspect-to-angle conditions do not trigger
  thin-line escalation.
- Mid-latitude interior tiles in aspect-to-angle cases keep the
  baseline halo.
- House polygons (planet-in-house, angle-in-sign) below the polar
  threshold are unaffected by high-latitude escalation.

The Svalbard high-latitude thin-line failure observed in the
original stress run is **closed** by this policy. The dense
multi-overlap residue class is **accepted** at its current
magnitude; further reduction would cost samples without changing
the human verdict on map-context review sheets.

## House Negative-Space Optimisation — Future Only

> **Status:** future optimisation. Not implemented. Not relied on
> for correctness. Recorded here so a later refinement does not
> reinvent the idea without doctrine review.

If house topology is complete and contiguous on a given chart,
the discovery of enough neighboring house boundaries may imply
intervening houses by **negative space**: if the 1st and 3rd
regions are known, the 2nd may be derivable as the space between
them, modulo the polar regions where Placidus is undefined.

This is *only* admissible if and when it satisfies the same gate
the rest of the architecture must satisfy:

- The implied region must match brute-force classification cell
  for cell across the validation matrix.
- The implication must respect the polar / lat-cap exclusion
  zone, where the engine has no truthful answer to imply from.
- It must compose cleanly with overlap semantics (overlap of an
  *implied* region and an explicit region must produce the same
  mask as overlap of two explicit regions).
- It must be cancellable like every other Phase-2 cache task; a
  half-implied region is not a valid cache slot.

Until those properties are proven on a validation bundle, the
canonical truth source remains direct per-cell classification.
Negative-space inference is **not** a substitute for brute force,
and any future PR proposing it must reference this section and
provide the validation evidence.

## Transit Philosophy

### Status of transit overlays in the product

Natal relocation is the foundational layer. Transit overlays are
**temporary energetic weather systems applied onto the underlying
relocation geography** — they are additive, not a replacement
worldview.

Many astrologers (including the product creator) primarily hold
that transits act on the **natal** chart, not the relocated
houses. Relocated-transit overlays are therefore:

- **off by default,**
- clearly labelled as **exploratory**, and
- accompanied by an explicit disclaimer that this interpretive
  stance is not universally accepted.

The renderer remains neutral. It classifies the requested
condition; any interpretive framing lives in an AI / explanation
layer that may or may not ship later.

> The feature is still potentially extremely valuable and
> visually compelling for exploratory users. It must feel
> **optional, advanced, discoverable, intriguing** — never
> doctrinal, mandatory, or "the app's main theory."

### What is and is not mapped

Traditional **planet-to-planet** transits do not map well
geographically. They belong in charts, timelines, comparison
views, and interpretation layers — never on the relocation map.

What **does** map is "locations where a transit condition is
true." Examples:

- Transit Jupiter in relocated 10th house
- Transit Pluto in relocated 4th house
- Transit Saturn conjunct relocated MC
- Transit Uranus square relocated ASC

These are answered by the same brute-force pattern as natal
conditions: at each location, compute the relocated chart and the
current transit relationships to that chart's houses and angles,
then classify yes/no (with optional orb distance and exactness
once aspect-to-angle ships).

This produces:

- truthful transit polygons (yes / no / partial)
- truthful transit centerlines
- (eventually) truthful transit aura bands

A transit overlay must work identically to a natal overlay. There
is no separate "transit rendering pipeline"; both go through the
same classify-every-cell architecture.

### Product distinction

> The map is **not** "show all transits everywhere."
> The map **is** "find places where a meaningful transit condition
> is occurring."

That distinction keeps the UX coherent. The map is a *finder*, not
a *broadcaster*. The user arrives with a question; the map answers
exactly that question.

There is a deeper, genuinely-new distinction underneath this one:

| Traditional astrology software                | This system                                              |
|-----------------------------------------------|----------------------------------------------------------|
| Shows transits **TO YOU**.                    | Shows **WHERE** a transit becomes active.                |
| Output is text, charts, dates.                | Output is geography — polygons and centerlines on a map. |
| "What is Pluto doing in your 10th house?"     | "Where on Earth would Pluto currently transit a 10th house?" |
| Time-axis tool.                               | Space-axis tool.                                         |

That inversion — from time-axis to space-axis — is what makes the
transit overlay a meaningful addition to the relocation map rather
than a duplicate of every existing transit tool. The renderer must
not slip back into the time-axis framing; if a feature only makes
sense as "transits to you", it belongs in the chart layer, not on
the map.

### Initial transit UI (governs step 7 when it lands)

The transit overlay enters the UI through a single off-by-default
toggle. When enabled, a small expandable drawer appears containing
exactly three controls:

1. **Transit Planet** — a single dropdown
   (Jupiter, Saturn, Uranus, Neptune, Pluto, …).
2. **Target Type** — a single dropdown with two options:
   - *Relocated House* — ships first.
   - *Relocated Angle Aspect* — anticipated but **not built yet**
     (see "Aspect-to-angle transits", below).
3. **Date Mode** — a single dropdown:
   - *Today* — no further input.
   - *Fixed Date* — reveals one calendar input.
   - *Date Range* — reveals start-date + end-date inputs.

If Target Type is *Relocated House*, a fourth control appears: a
1–12 house dropdown. This is the only combination that ships in
the first transit cut.

That is the full UI surface. Nothing else appears in the default
interface. In particular, **orb customisation is not exposed**
in the main UI; the renderer uses sensible defaults and any
advanced controls live behind an explicit settings panel.

### Aspect-to-angle transits (anticipated, not built)

The architecture must anticipate transit conditions of the form
"Transit Saturn conjunct relocated MC", "Transit Uranus square
relocated ASC", "Transit Neptune opposite relocated DSC", etc.

These will use **default orbs** baked into the engine; optional
per-aspect orb customisation goes into a settings panel, not the
main drawer. The data model for transit conditions should be
designed so the *Relocated Angle Aspect* target type can be
turned on later without re-shaping the request schema.

### Outer-planet focus

Initial transit overlays must focus on **slow outer planets and
meaningful long-duration occupancies**:

- Pluto in relocated 10th
- Saturn in relocated 12th
- Jupiter in relocated 1st
- Uranus conjunct relocated MC

Daily transits and Moon overlays are explicitly out of scope for
the first version. The product must remain contemplative,
spatial, meaningful, readable — not a noisy daily-transit clutter
field, not a hyperactive animation system.

The dropdown may technically list inner planets, but the default
selection, the example library, and any "Try this" affordances
must point to outer planets.

### AI interpretation layer (future, not on the map)

When (and only when) the rest of the product is unassailable, an
optional AI layer may provide:

- cautious interpretation of a current transit overlay,
- contextual suggestions (other meaningful transits this user
  could explore),
- warnings about consensus disagreement (e.g. "many astrologers
  consider transits to act on the natal chart, not the relocated
  one"),
- duration and orb explanations.

This layer does **not** alter the map. The map keeps classifying
conditions; the AI layer reads the same engine output the user
sees and explains it in language. If a future AI shipping
decision conflicts with this separation, this doctrine wins.

## Current Development Order

| #  | Step                                                           | Status                          |
|----|----------------------------------------------------------------|----------------------------------|
| 1  | Single planet-in-house brute force                            | **DONE** — `validation/narratives/brute_force_polygon_proof.md` |
| 2  | Multiple simultaneous planet-in-house conditions              | **DONE** — `validation/narratives/brute_force_multi_condition_proof.md` |
| 3  | Overlap rendering semantics (real `swe.houses` per cell, mask)| **DONE** — same narrative as step 2 |
| 4  | Angle-in-sign overlays (ASC/MC/IC/DSC in zodiac sign)         | **DONE** — `validation/narratives/brute_force_angle_in_sign_proof.md` |
| 5  | Combined condition queries (mixed condition *types*)          | **DONE** — exercised by the angle-in-sign proof's mixed-type cases (09–12) |
| 6  | Aspect-to-angle centerlines                                   | **DONE** — `validation/narratives/brute_force_aspect_to_angle_proof.md` |
| 7  | Transit-to-relocated-house overlays                           | pending — first transit cut. UI shape fixed (see "Initial transit UI"). Outer planets only by default. Off-by-default toggle + disclaimer required. |
| 8  | Transit aspect-to-relocated-angle overlays                    | pending — schema must be anticipated in step 7; **renderer not built until step 7 stabilises**. Default orbs only; advanced orb customisation lives in settings, never the main drawer. |
| 9  | Aura / gradient rendering                                     | pending                          |
| 10 | Refinement acceleration (the optimisation phase)              | pending — *gated on stability*   |

The numbering is normative. Steps may not be skipped without an
explicit doctrine update. In particular, **step 10 cannot begin
until steps 3–9 are visually and semantically stable**, because the
optimisation must preserve the behaviour those steps establish.

## Critical Engineering Rule

> Do **not** optimise prematurely.
>
> For now:
> * maximal brute force
> * maximal truth
> * maximal inspectability
>
> Only optimise *after*:
> * overlap semantics stabilise
> * edge behaviour stabilises
> * centerlines stabilise
> * transit geometry stabilises
>
> Optimisation comes later. Truth comes first.

Any pull request whose primary justification is "this is faster"
or "this reduces compute" must be rejected before steps 3–9 are
stable. Speed improvements that are *also* simpler or *also*
clearer are acceptable; speed improvements that introduce
caching, approximation, contour fitting, or smoothing are not.

## Current Compliance Audit

This section records how the live system matches the doctrine *as
of adoption*. It will be updated as new doctrine steps land. Items
marked GAP are not bugs — they are the explicit next-work surface.

| Concern                                                    | Status                                                                                                                                                                          |
|------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Brute-force endpoint                                       | ✓ `POST /brute-force-grid` ships and is canonical.                                                                                                                              |
| Single planet-in-house                                     | ✓ proven.                                                                                                                                                                       |
| Multi-condition planet-in-house with real overlap          | ✓ proven (1, 2, 3 conditions, mask-based response).                                                                                                                             |
| No smoothing / blur / polygon fill / cosmetic geometry     | ✓ enforced in `map_SANDBOX_brute_force.html` via constant-radius pixel-occupancy painting.                                                                                       |
| Phase-1 immediate response (request-only compute)          | ✓ inherently — endpoint never precomputes anything beyond the requested conditions.                                                                                              |
| Phase-2 background opportunistic expansion                 | **PROTOTYPE** — `map_SANDBOX_phase2_cache.html` implements the documented priority protocol (A→H, interrupt, budget, no half-entries). Smoke: `scripts/smoke_phase2_cache.py`. Not yet wired into `map_CURRENT.html`. See `validation/narratives/phase2_cache_implementation.md`. |
| Zoom = edge refinement, not re-solve                       | **GAP** — sandbox re-solves the full viewport on pan/zoom (auto-rerun checkbox). The "interior preserved, edges refined" pipeline does not yet exist.                            |
| Angle-in-sign overlays                                     | ✓ step 4 done — discriminated `angle_in_sign` slot in `/brute-force-grid`, mask-aware rendering in sandbox, identity checks against IC/MC and ASC/DSC pass to the cell. Legacy `map_CURRENT.html` still uses the old smoothing path; product migration is a separate step. |
| Combined condition queries (mixed types)                   | ✓ step 5 done — discriminated union schema lets a single request mix `planet_in_house` and `angle_in_sign` slots; overlap is real (single `swe.houses` per cell tests all slots). Future condition types (transit, aspect-to-angle) extend the same union. |
| Aspect-to-angle centerlines                                | ✓ step 6 done — `aspect_to_angle` slot in `/brute-force-grid` with `(planet, angle, aspect, orb)`; centerlines emerge as truthful occupancy bands. MC aspects produce meridians, ASC aspects produce curves, both from the same per-cell test. IC/MC and ASC/DSC identities verified to the cell. Legacy `map_CURRENT.html` aspect path still untouched. |
| Transit overlays (Phase 2 condition family)                | **GAP** — steps 7–8. Endpoint will need a "transit moment" parameter; the schema must support a single instant (*Today* / *Fixed Date*) and a date-range integration (*Date Range*). UI shape and constraints are now frozen (off by default, exploratory disclaimer, outer-planet focus, single-drawer surface, no main-UI orb customisation). |
| Aura / gradient rendering                                  | **GAP** — step 9. Truthful aura design is documented in `docs/overlay_and_aura_visual_strategy.md` but has not been implemented under the new architecture.                     |
| Refinement acceleration                                    | **PARTIAL** — adaptive screen-space refinement with targeted-policy hardening is in place (see `validation/narratives/screen_pixel_adaptive_targeted.md`, `validation/narratives/screen_pixel_dense_residue.md`). Full step-10 work (aspect-aware caching, transit caching, telemetry-driven refinement) remains gated on Phase-2 cache landing in product. |
| Polar Placidus error rendering                             | known, surfaced in proofs. Treatment ("hide", "lat-cap", "stripe", "label as unavailable") is an unresolved UX call.                                                            |

The architecture also implicitly retires several earlier
exploration tracks. These are kept as evidence, not as guidance:

- `validation/narratives/polygon_reveal_sandbox_visual_qa.md`
- `validation/narratives/polygon_reveal_topology_target_v1.md`
- `map_SANDBOX_polygon_reveal.html`

These describe stochastic-sampling reveal pacing — a working
exploration that the brute-force proof rendered obsolete as a
*performance* path. Reveal/animation may return as a *stylistic*
layer over the brute-force solve once steps 4–9 settle; the
sandboxes and narratives remain on disk as historical record and
must not be cited as current architecture.

## Where to look first when changing the relocation map

1. This file — does the change respect the four phase priorities,
   the brute-force-is-canonical rule, and the "no optimisation
   yet" gate?
2. `docs/visual_semantic_style_guide.md` §truth hierarchy — does
   the visual encoding still distinguish truth tiers correctly?
3. `validation/narratives/brute_force_polygon_proof.md`,
   `validation/narratives/brute_force_multi_condition_proof.md`,
   `validation/narratives/brute_force_angle_in_sign_proof.md`, and
   `validation/narratives/brute_force_aspect_to_angle_proof.md`
   — are the new behaviours backed by an evidence bundle?
4. `docs/next_implementation_sequence.md` — the UX-band
   sequencing is still valid for shipping the *product surface*;
   this doctrine governs the *rendering substrate* underneath.

When this doctrine and any other doc disagree, this doctrine
wins until it is explicitly amended in writing.
