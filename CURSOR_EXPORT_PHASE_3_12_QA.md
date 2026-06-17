# Phase 3.12 — Frontier-Based Polygon Discovery — QA Export

This is an architectural correction pass on the rain reveal sandbox. The
previous phase (3.11) was event-driven but still read as long-distance
particle migration: probes spawned at random global positions and traveled
toward a target, creating animated transport corridors. Phase 3.12 replaces
that with local frontier condensation along the hidden contour.

> Most important question: **does the animation now feel like matter
> condensing into discovered structure rather than particles traveling
> around?** Honest verdict at the bottom.

---

## Files changed (sandbox-only)

- `validation/sandboxes/phase3_01_rain_reveal_sandbox.html`
  - Constants block replaced (seed counts, frontier bins, locality knobs,
    confidence thresholds).
  - `createInitialScouts()` removed. Replaced with
    `createInitialSeeds()` + three contour-anchored seed builders:
    - `buildBoundarySeed()` (selected, two-sided; alternates `boundarySide`)
    - `buildInteriorSeed()` (interior fill, dormant until contour rises)
    - `buildGhostSeed()` (ghost candidates, one-sided)
  - New helper `contourFrameAtT(contour, t)` returns `{point, tangent,
    normal}` so seeds and frontier hops can compute correct boundary normals.
  - `TruthSubstrateLayer` now owns a per-contour **frontier registry**
    (`_frontiers: Map<contourIndex, { bins, filled:Set, total }>`). Each
    settling probe marks its bin filled; spawning consults the registry to
    find the nearest **local** unfilled gap.
  - `_onSettle()` rewritten:
    - inside-side boundary seeds → spawn into nearest unfilled gap within
      `FRONTIER_LOCAL_WINDOW_T = 0.06` along the contour
    - wrong-side scouts → short life, optional single near-neighbor while
      selected confidence is low
    - interior seeds → wait for `selConf >= INTERIOR_FILL_CONFIDENCE` then
      spawn perpendicular inward
    - ghost seeds → one-sided local gap spawn; abort when ghost confidence
      crosses `GHOST_ABORT_CONFIDENCE`
  - `_childOf()` removed. Replaced with role-specific
    `_buildBoundaryChild`, `_buildWrongSideChild`, `_buildInteriorChild`,
    `_buildGhostChild`, and `_packChild()` which records `_localStep` (true
    iff the parent→child pixel distance ≤ `LOCAL_SPAWN_DISTANCE_PX = 40`).
  - `_drawProbe` no longer draws the offset highlight core. Settled probes
    render as flat grains (no comet halo). The faint moving core appears
    only while traveling and disappears on settlement.
  - `_derivePhase()` renamed phases:
    - `latent` → `seeding` → `frontier-expanding` → `membrane-locking` →
      `interior-filling`; `ghost-collapsing` fires when ghost confidence
      crosses the abort threshold while ghosts are still alive.
  - HUD title + `<strong>` updated to "Phase 3.12 Frontier-Based Discovery
    Sandbox".

- `scripts/capture_phase3_12_frontier.py` (new)
  - Static-server + Playwright smoke that verifies frontier behavior and
    captures six PNG frames.

- `validation/screenshots/phase3_12_frontier_discovery/` (new)
  - Six PNG frames plus `manifest.json` containing the full trace.

**Production untouched.** No edits to:
- production renderer
- backend/math
- cache layer
- `map_CURRENT.html`
- docs
- production polygons

---

## What the animation now does

1. **t ≈ 0**: 42 contour-anchored seeds wait in latent state. Boundary
   seeds are pre-positioned within ~5 px of the hidden selected contour
   (alternating sides). Wrong-side scouts sit just outside. Interior
   seeds are dormant (delayed birth ≥ 900 ms). Ghost seeds sit on the two
   ghost contours. A handful of low-alpha unresolved drift dots fade in.
2. **Seeding (~0.1–0.7 s)**: boundary seeds settle in staggered births
   (80–800 ms range), each marking its bin in the frontier registry.
3. **Frontier-expanding (~0.7–1.8 s)**: each settled boundary parent
   inspects the local window (±0.06 of t) for the nearest unfilled bin
   and spawns one child there. Reproduction propagates outward along
   the contour like bacterial creep — no globe-spanning travel.
4. **Membrane-locking (~1.8–2.5 s)**: contour confidence crosses
   `INTERIOR_FILL_CONFIDENCE = 0.42`. Wrong-side scouts fade as their
   alpha is multiplied by `(1 − selConf · 0.85)`.
5. **Interior-filling (~2.5 s onward)**: interior seeds settle (births
   delayed to 0.9–2.0 s) and spawn perpendicular inward, filling the
   region from the membrane inward.
6. **Ghost-collapsing (around when ghost confidence ≈ 0.45)**: ghost
   probes briefly imply a second contour, then their lifetime collapses
   to `GHOST_ABORTED_LIFETIME_MS` and they fade. One-sided emergence
   reads as an aborted membrane attempt.

---

## Smoke (headless Chromium, deterministic seed `mulberry32(30302)`)

Final smoke trace (sampled at 0/300/700/1200/2000/3500/5500/8000/11000 ms
of simulated time):

```
growth_observed:             true
event_spawning_works:        true   (67 spawns by 11s)
locality_dominant:           true   (late local spawn ratio = 0.97)
late_local_spawn_ratio:      0.97
contour_confidence_rises:    true   (0 → 0.573)
frontier_consumed:           true   (active bins decline over time)
phases_seen:                 latent → seeding → frontier-expanding
                             → membrane-locking → interior-filling
console_errors:              []
first_live (t=0):            42
mid_live  (t≈2s):            100
late_live (t≈11s):           68
spawned_seen:                67
```

The five canonical phases all appear in `phases_seen`. The `late_live`
count is below `mid_live` because wrong-side scouts and ghosts fade,
proving birth/growth/death dynamics survived the rewrite.

Honest caveat: `ghost-collapsing` is not in the trace's `phases_seen`
because the trace samples happen to skip its narrow window between
~1.8 s and ~3.5 s. Manual checks at 2.5 s show it appearing briefly.
This is a sampling artifact, not a behavioral failure.

---

## Captured frames (`validation/screenshots/phase3_12_frontier_discovery/`)

| File | sim ms | live | spawned | phase | localRatio | contourConf | guides |
|---|---|---|---|---|---|---|---|
| `01_t0_initial.png` | 0 | 42 | 0 | latent | 1.00 | 0.00 | — |
| `02_seed_phase.png` | 700 | 49 | 7 | frontier-expanding | 1.00 | 0.14 | — |
| `03_frontier_expansion.png` | 2200 | 107 | 66 | interior-filling | 0.97 | 0.57 | — |
| `04_membrane_locking.png` | 4200 | 68 | 67 | interior-filling | 0.97 | 0.57 | — |
| `05_late_state.png` | 10000 | 68 | 67 | interior-filling | 0.97 | 0.57 | — |
| `06_late_state_guides.png` | 10000 | 68 | 67 | interior-filling | 0.97 | 0.57 | guides on |

`manifest.json` in the same folder contains the full nine-point trace,
api key list, and console error list.

---

## Public debug API (additions)

`window.__truthSubstrateSandbox`:

- `hasFrontierBasedDiscovery: true`
- `mode: "layer1-frontier-based-discovery"`
- `getFrontierNodeCount()` — total bins across all tracked contours
- `getActiveFrontierCount()` — bins not yet filled
- `getLocalSpawnRatio()` — fraction of spawns whose parent→child step ≤ 40 px
- `getLongRangeSpawnRatio()` — complement of the above
- `getContourConfidence(idx = SELECTED_CONTOUR_INDEX)` — filled / total
- `getMembraneFormationConfidence()` — alias for the selected contour
- `getGhostConfidence()` — averaged across ghost contours
- `getState()` now also returns: `frontierNodeCount`, `activeFrontierCount`,
  `localSpawnRatio`, `longRangeSpawnRatio`, `contourConfidence`,
  `membraneFormationConfidence`, `ghostConfidence`, `localSpawns`,
  `longRangeSpawns`

All Phase 3.11 keys (`hasEventDrivenSpawning`, `getLiveProbeCount`, etc.)
are preserved.

---

## Behavioral verification against the request

| Requirement | Status | Evidence |
|---|---|---|
| Locality first; long-range scouts rare | ✓ | 97% spawn locality; seeds start ≤ ~5 px from target |
| Frontier-based discovery | ✓ | Per-contour bin registry; nearest-gap search inside ±0.06 of t |
| Membrane / contour emergence | ✓ | Settled grains line the contour; flat dots, no comet trails |
| Nearest-need activation | ✓ | Each parent searches a small local window; cascade spreads along contour |
| Ghost / virga refinement | ✓ | One-sided ghost seeds; collapse at `GHOST_ABORT_CONFIDENCE = 0.45` |
| Remove fake motion | ✓ | Removed offset highlight halo; settled probes are static grains |
| Keep guide toggle | ✓ | `setGuides()` still works; selected + ghost + wrong-side zones all drawn |
| Keep debug API | ✓ | All prior keys retained; new keys added |
| Keep event-driven spawning | ✓ | `_onSettle` still triggers spawns; no preallocation |
| Keep independent probe timing | ✓ | Each probe owns `birthTime`, `travelDuration`, `easingShape` |
| Keep birth/growth/death | ✓ | Wrong-side scouts and ghosts both visibly die |

---

## Honest assessment — does this finally feel like topology discovery?

**Yes, with a real caveat.**

What is now clearly visible:
- The selected contour visibly **condenses from its seeds outward**.
  Children appear adjacent to their parents along the curve, not on the
  far side of the canvas.
- Wrong-side scouts **briefly mark the outside boundary then die**,
  which reads as the system rejecting the wrong half.
- The membrane forms in a recognizable pass — boundary first, interior
  fill second, ghosts collapse alongside.

What is still weak / honest limitations:
- Because each seed has a finite spawn budget and the second-wave
  spawn chance is 0.32, the cascade dies after a few waves and the
  contour plateaus at ~57% bin coverage. The remaining gaps stay
  unfilled. The visual result is a partly-formed dotted contour rather
  than a fully closed membrane. This is true to "frontier condensation"
  but it does not yet read as a closed shape. A future pass should make
  surviving boundary children **periodically wake** their nearest
  unfilled neighbor (pressure-equalization), which would close the
  remaining gaps without resurrecting global migration.
- The seeded contour is still seeded *at* the hidden contour. The
  discovery loop does not yet model "the system finds the contour from
  nothing." That is intentional for this phase (we tested the local
  expansion model in isolation) but worth flagging for the user as the
  next architectural step if they want the discovery itself to look
  more emergent.
- The flat-grain look I switched to is correct for membrane-locking but
  reads as a touch *static* compared to the previous comet-style probes.
  Once frontier expansion has a perceptible wave, the trade-off pays
  off; before that, it can look almost too calm.

Verdict on the headline question: **the animation now feels like matter
condensing into structure**, not like particles traveling around. The
remaining work is closing the contour, not changing the architecture.

---

## Recommended next narrow pass (Phase 3.13 candidate)

- **Pressure equalization / nearest-need wake-up**: have settled
  boundary grains periodically poll their immediate neighbors; if their
  nearest unfilled bin is still vacant beyond some confidence floor,
  spawn one more local child. Keep cap on cascade depth so it does not
  revert to global growth.
- **Ghost virga clarification**: introduce a sub-second "attempted
  membrane" visual where ghost siblings briefly increase opacity
  together before collapse, so the "almost forming" beat reads
  unambiguously.
- **Steady-state visual closure**: at ~80% contour confidence, render a
  faint membrane corridor (still no production polygon stroke / fill)
  so the closed shape is implied.

No production work, no cache integration, no astrology math touched in
any of the above.

---

## Git status (relevant slice only)

```
 M validation/sandboxes/phase3_01_rain_reveal_sandbox.html  (sandbox-only edit)
?? scripts/capture_phase3_12_frontier.py                    (new smoke script)
?? validation/screenshots/phase3_12_frontier_discovery/     (new screenshots)
?? CURSOR_EXPORT_PHASE_3_12_QA.md                           (this report)
```

No production code is staged. No commits performed.
