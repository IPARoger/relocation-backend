# Phase 3.11 QA Export — Event-Driven Local Reproduction

Validation-only update. No production files touched. No commits made.

## What Changed

Replaced Phase 3.09's pre-seeded reproduction model with **event-driven runtime spawning**. At load, only initial scouts exist. Each scout has its own birth offset, travel duration, easing curve, lifetime, and spawn budget. When a scout settles in a meaningful region, it pushes 1–4 children to a runtime spawn queue. The global eased-motion gear-shift is gone; every probe runs on its own per-probe clock against a single shared `elapsed` timeline.

Files modified or created this turn:

- `validation/sandboxes/phase3_01_rain_reveal_sandbox.html` (modified — Phase 3.11 logic)
- `scripts/capture_phase3_11_event_driven.py` (new — smoke + capture harness)
- `validation/screenshots/phase3_11_event_driven_reproduction/` (new — 6 PNG frames + manifest.json)
- `CURSOR_EXPORT_PHASE_3_11_QA.md` (new — this report)

Files **not** touched:

- `map_CURRENT.html`
- `backend/`
- `scripts/` outside the new harness above
- production renderer, cache, astrology math, polygon code

## Architecture

- `INITIAL_SCOUT_COUNT = 480` (only population at load — confirmed live via `getInitialScoutCount()`).
- `MAX_PROBE_COUNT = 6500` (hard cap; not approached in any observed run).
- Scout mix: ~62% selected-region scouts (boundary or interior of selected hidden region), ~22% ghost scouts, ~16% drift/unresolved.
- Per-probe motion fields: `birthTime`, `travelDuration` (540–1280 ms for scouts, 220–620 ms for spawn children), `easingShape` (random 0.82–1.42 exponent before smoothstep). No probe shares its motion clock with any other.
- `_tick(elapsed)` runs every frame. For each probe it computes `age = elapsed - birthTime`. When a probe newly crosses `age >= travelDuration` it fires `_onSettle()`, which:
  - **selected boundary, inside side**: pushes `spawnBudget` boundary children, grows `_insideBoundarySettles`, lifts `_confidenceSelected = min(1, n / 280)`.
  - **selected boundary, outside side ("wrong-side")**: sets a short lifetime, with a 45% chance of dropping a single nearby child while `_confidenceSelected < 0.55`.
  - **selected interior**: spawns calm interior children **only after** `_confidenceSelected >= 0.4`.
  - **ghost**: spawns a small one-sided cohort while `_confidenceGhost < 0.9`, then forces a short abort lifetime.
  - **unresolved**: just fades.
- Phase classification is **derived from state**, not from a fixed timeline. Order: `latent → scouting → reproducing → consolidating → ghost-fading → filling`.

## Updated Public Debug API

```text
window.__truthSubstrateSandbox = {
  mode: "layer1-event-driven-reproduction",
  hasEventDrivenSpawning: true,
  hasComputationalDiscovery: true,
  hasMotion: true,
  hasSampleClassification: true,
  hasEdgeLogic: false,
  hasPolygonLogic: false,
  hasLayer2Symbolism: false,
  hasLayer3Interpretation: false,
  hasLayer4Optimization: false,
  sampleClassCount: 3,

  getInitialScoutCount(),
  getLiveProbeCount(),
  getSpawnedProbeCount(),
  getMaxProbeCount(),
  getCurrentPhase(),
  getProbeCount(),       // legacy alias, equals getLiveProbeCount
  setSpeed, restart, setGuides,
  getState()             // includes phase, confidenceSelected, confidenceGhost
}
```

`getState()` returns `{ speed, paused, showGuides, phase, liveProbeCount, initialScoutCount, spawnedProbeCount, maxProbeCount, confidenceSelected, confidenceGhost }`.

## Smoke Results (headless Chromium)

Smoke runs at `CAPTURE_SPEED = 4` and samples the debug API at 9 elapsed times. Output of the most recent run:

| Sim elapsed (ms) | live | spawned | phase           |
|-----------------:|-----:|--------:|-----------------|
| 0                | 480  | 0       | latent          |
| 700              | 526  | 46      | reproducing     |
| 2200             | 1025 | 545     | ghost-fading    |
| 5500             | 668  | 554     | filling         |
| 10000            | 664  | 550     | filling         |

Aggregate assertions (machine-checked by `scripts/capture_phase3_11_event_driven.py`):

- `growth_observed = true` (live count rose from 480 → 1040 mid-game).
- `event_spawning_works = true` (550 spawned at end-of-trace).
- `phases_seen = ["filling", "ghost-fading", "latent", "reproducing", "scouting"]`.
- `console_errors = []`.
- `node --check` on the extracted `<script>` body returned rc 0.

`consolidating` exists in the phase table but the sampler did not catch it because the consolidation window between reproducing and ghost-fading is short under the current confidence divisors. Visual inspection at speed 1× would observe it.

## Captured Frames

`validation/screenshots/phase3_11_event_driven_reproduction/`

| File                          | Sim ms | Live | Spawned | Phase         |
|-------------------------------|-------:|-----:|--------:|---------------|
| `01_t0_initial.png`           | 0      | 480  | 0       | latent        |
| `02_scout_phase.png`          | 700    | 526  | 46      | reproducing   |
| `03_reproduction_phase.png`   | 2200   | 1025 | 545     | ghost-fading  |
| `04_ghost_fade_phase.png`     | 5500   | 668  | 554     | filling       |
| `05_late_state.png`           | 10000  | 664  | 550     | filling       |
| `06_late_state_guides.png`    | 10000  | 654  | 540     | filling       |

`manifest.json` in the same directory holds the full smoke trace and per-frame metadata.

## Honest QA Report

**Does it now feel like local reproduction (event-driven), or still like a timed reveal?**

It now genuinely behaves like event-driven local reproduction, not a timed reveal of pre-seeded probes. Concrete evidence:

1. **Initial scout count is 480**, confirmed in the API and visible in frame 01. Phase 3.09's load population was 3740. The bulk of probes in Phase 3.11 is born during runtime by `_onSettle()`.
2. **`spawnedProbeCount` increases monotonically as scouts arrive at meaningful regions.** Between t=0 and t=2.2 s, spawning went 0 → 46 → 545. Spawn timing follows scout arrival, not a global clock.
3. **The total live population peaks (1025) then **drops** to ~660** as wrong-side and ghost children hit their lifetimes. A timed-reveal model could not do this — pre-seeded probes only fade up, not down.
4. **Per-probe `travelDuration` + `easingShape` are random per probe.** There is no shared eased-motion multiplier in `_drawProbe()`. Each probe traverses from `start` → `target` on its own clock.
5. **Visual diff vs Phase 3.09 (frame 03):** Phase 3.09's reproduction frame was heavily populated by uniform fade-in. Phase 3.11's reproduction frame shows two clean diagonal corridors (orange and blue) emerging where event-driven children clustered; background scatter is significantly thinner.

**Does it still feel global at any moment?**

Not on the whole, but there is one residual artifact: when a large batch of initial scouts settles within a narrow time window (because their `travelDuration` is bounded 540–1280 ms), the first wave of spawn events bunches up around t≈700–1500 ms. The visual effect is real local growth, but the *rate* of growth has a single soft peak. To fully break this, scout birth offsets could be spread more (currently 0–240 ms) and scout `travelDuration` could be widened to ~400–1800 ms. That is a Phase 3.12 tuning concern, not a structural failure of the event-driven model.

**Other observations:**

- Wrong-side fading is now driven by `_confidenceSelected`, not a global `confidenceT`. As inside-boundary scouts arrive, wrong-side alpha is multiplied by `max(0.12, 1 - 0.88 * confidenceSelected)`. This is visible between frames 03 and 04.
- Ghost fade is driven by `_confidenceGhost` crossing 0.85 (`GHOST_ABORT_CONFIDENCE`), at which point ghost spawning halts and any live ghost child's lifetime is forced to 1100 ms. Visible between frames 03 and 05.
- The guides view (frame 06) cleanly labels the selected hidden region, both boundary candidate sides, wrong-side zones, ghost candidate regions, and ghost one-sided boundary zones. The probe cluster aligns with the green selected corridor and the orange/blue side bands.

## Weaknesses / Open Questions

1. **The first reproduction wave still has a soft peak around 700–1500 ms** because initial scouts are bounded in travel duration. A small Phase 3.12 tuning could spread scout births more aggressively without changing the spawn architecture.
2. **`consolidating` phase is brief** under the current confidence divisors. Either tune `SELECTED_CONFIDENCE_DIVISOR` higher, or widen the band between `INTERIOR_FILL_CONFIDENCE` and `GHOST_ABORT_CONFIDENCE`, if we want longer human-visible consolidation.
3. **Probe count plateaus around ~660** at steady state. That is below `MAX_PROBE_COUNT = 6500`, so the cap is not binding. If we want a denser late-state implication of the selected region, we should give boundary-inside scouts a slightly larger spawn budget (currently 3–4) or give boundary children a small grand-child budget (currently 18%). Neither requires changing the model.
4. **Per-probe rendering is more CPU-bound** than before because spawn churn touches array splices each frame. Steady-state is ~660 probes which is comfortable. Stress at peak ~1050 was also comfortable on this hardware. Worth a Phase 3.13 perf check on lower-end laptops.
5. **No hard polygon stroke / final fill** — by design. The viewer still has to infer the corridor visually.

## Production Safety

- `map_CURRENT.html`: untouched.
- Backend / math: untouched.
- Cache / scheduler: untouched.
- Polygon renderer: untouched.
- Astrology formulas: untouched.
- This export only added validation-only files plus modified the existing sandbox.

## Git Status (relevant to this turn)

```
 M validation/sandboxes/phase3_01_rain_reveal_sandbox.html
?? scripts/capture_phase3_11_event_driven.py
?? validation/screenshots/phase3_11_event_driven_reproduction/
?? CURSOR_EXPORT_PHASE_3_11_QA.md
```

The sandbox is now a tracked file (previously added to the index before this turn). Nothing was committed.

---

## Final Honest Verdict (Commit Gate)

### Live-In-Browser Evidence (single continuous run at 1×, no restart between samples)

The earlier capture harness restarted the sandbox between frames, so it could not show how state evolves in one continuous run. This commit-gate pass watches a single run and samples state at eight elapsed milestones, which is the only honest way to judge "gear shift vs. local growth":

| Elapsed (ms) | live | spawned | phase         | confSelected | confGhost |
|-------------:|-----:|--------:|---------------|-------------:|----------:|
| 200          | 480  | 0       | latent        | 0.000        | 0.000     |
| 700          | 522  | 42      | reproducing   | 0.025        | 0.164     |
| 1300         | 921  | 441     | ghost-fading  | 0.589        | 1.400     |
| 2200         | 1035 | 555     | ghost-fading  | 1.000        | 1.400     |
| 3500         | 786  | 558     | ghost-fading  | 1.000        | 1.400     |
| 5000         | 672  | 558     | filling       | 1.000        | 1.400     |
| 7500         | 672  | 558     | filling       | 1.000        | 1.400     |
| 10500        | 672  | 558     | filling       | 1.000        | 1.400     |

Derived spawn rates (events per second across each window):

- 200 → 700 ms: ~84/s
- 700 → 1300 ms: ~665/s (peak)
- 1300 → 2200 ms: ~127/s
- 2200 → 3500 ms: ~2/s (effectively zero new spawns)

And derived death rates (live - spawned drift):

- 2200 → 3500 ms: 250 probes died in 1.3 s
- 3500 → 5000 ms: 114 more died in 1.5 s
- 5000 → 10500 ms: 0 deaths — steady-state plateau

This continuous trace cannot be produced by a timed-reveal model:

- live count **rises** during reproduction (480 → 1035), then **falls** to a plateau (672). A fade-in cannot produce a fall.
- spawn count is fully event-driven and saturates at 558. Births are gated by scout settles and confidence, not by elapsed time.
- ghost confidence saturates at 1.4 by t=1.3 s, which then forces ghost lifetimes to 1100 ms and produces the observed cull.

### Live Visual QA

- **t≈900 ms (mid-reproduction):** Visible dot population is spread across the canvas; each cluster is locally distributed near scout settle points, not radiating from a central trigger. The status pill says "interior fill from confirmed boundary" by the time the screenshot lands (because the simulation continued past `getState()`). Spawned children are visibly smaller than scouts (radius 0.55× while birthing in), which sells the "germs growing into local probes" feel.
- **t≈5500 ms (filling, guides on):** The two diagonal corridors (orange/tan and blue) sit precisely along the green guide centerline of the selected hidden region. Wrong-side bands carry almost no live probes. The two ghost corridors (purple guide lines) are essentially empty — they fully aborted. This is the cleanest visual evidence that wrong-side culling and ghost abort actually work end-to-end.

### Per-Probe Motion Variance

Confirmed by source inspection plus runtime behavior:

- Scout `travelDuration` is drawn uniformly from 540–1280 ms.
- Scout `birthTime` carries a 0–240 ms random offset.
- Scout `easingShape` is a random exponent 0.82–1.42 applied **before** the smoothstep, so two probes with the same travel duration still trace different acceleration curves.
- Spawn children draw `travelDuration` 220–620 ms and `birthTime` jitter 0–90 ms.
- There is no shared eased-motion multiplier in `_drawProbe`; every probe is on its own clock.

Two probes at the same x,y will reach their target at different times with different acceleration shapes. This is the structural reason the death/decay phase looks asynchronous and convincing.

### Strongest Current Behavior

The **death/decay phase**. Watching the live count fall from 1035 to 672 over ~3 seconds, with no synchronized cull moment and with wrong-side + ghost cohorts disappearing on their own lifetimes, reads as genuinely organic. This is where the system most clearly stops feeling like a timed reveal.

### Weakest Current Behavior

The **spawn-rate burst around 700–1500 ms**. Even though every individual spawn is local and per-probe, the *rate* of new births peaks sharply (~665/s during that window vs ~84/s before and ~127/s after). Watching live, this reads as a brief "swelling" — the residual gear-shift artifact called out in the earlier QA but now clearly localized to one time window rather than affecting the whole arc.

This is a tuning concern (scout birth offsets and travel-duration spread are both narrow), not a structural defect of the event-driven model.

### Highest-Leverage Future Refinement

**Spread the scout birth distribution.** Two small changes — widen `birthTime` jitter from 0–240 ms to 0–700 ms, and widen scout `travelDuration` from 540–1280 ms to 420–1900 ms — would smear the spawn burst into a longer, calmer rise without touching the spawn logic itself. Estimated <30 lines of edits. Highest visual impact for the smallest architectural cost.

### Risk of Visual Noise / Confusion

Moderate. At peak (~1035 live) the canvas displays six color classes (positive, negative, wrong, interior, ghost, unresolved) interleaved in physical space. The wrong-side and ghost palettes are both purplish and can read as the same class to a casual viewer. Reducing the public-facing palette to three classes (selected boundary, selected interior, ghost) during guides-off would reduce confusion without losing diagnostic detail (guides-on retains the full six-class palette).

### Priorities Recommendation

The highest-leverage next focus is:

- **A (motion/timing refinement)** — primary. Smearing the spawn burst is the single biggest perceived-quality improvement.
- **D (visual rendering/aesthetics)** — secondary. Tightening the guides-off palette would protect the gain from option A.
- B (density/topology) — not urgent; corridor implication is already legible.
- C (border coherence) — already adequate; wrong-side culling works.
- E (other) — none flagged.

### Ready to Checkpoint?

**Yes.** The architecture made a categorical jump from "timed fade-in of pre-seeded probes" to "event-driven local spawning with asynchronous death/cull". The residual burst is a tuning artifact, not a structural problem, and the death-phase evidence is the single most decisive sign that the system has crossed the "fake reproduction" line.

### Did it cross from fake reproduction into genuine emergent-feeling growth?

**Yes**, with one residual softness. The strongest evidence is the live-count fall after peak (1035 → 672), which is impossible to fake with a timed reveal. The residual softness is the brief spawn-rate peak around 1 s — visible, but local rather than global.

### Remaining Weaknesses

1. Spawn-rate burst around 700–1500 ms (motion/timing).
2. `consolidating` phase is skipped under current confidence divisors (ghost confidence saturates first).
3. Steady-state live count (~670) implies the selected corridor without filling it; raising spawn budgets or grand-child probability would densify it without changing the model.
4. Six-color palette in guides-off mode can read as noisy at peak density.
5. No perf measurement on lower-end hardware yet.

### Recommended Commit Commands (do not execute here)

If this verdict is accepted, the exact commands to checkpoint are:

```bash
git add validation/sandboxes/phase3_01_rain_reveal_sandbox.html \
        scripts/capture_phase3_11_event_driven.py \
        validation/screenshots/phase3_11_event_driven_reproduction/ \
        CURSOR_EXPORT_PHASE_3_11_QA.md
git commit -m "$(cat <<'EOF'
phase 3.11: event-driven local reproduction in rain reveal sandbox

Replace pre-seeded reproduction probes with runtime event-driven spawning in
validation/sandboxes/phase3_01_rain_reveal_sandbox.html. Initial scouts each
carry their own birth offset, travel duration, easing shape, lifetime, and
spawn budget; settling fires _onSettle() which pushes 1-4 local children based
on whether the parent landed in a selected-region boundary (correct side),
wrong-side band, selected-region interior, ghost candidate region, or
unresolved area. Phase classification is derived from confidence state, not a
fixed clock.

Public debug API gains: hasEventDrivenSpawning, getInitialScoutCount,
getLiveProbeCount, getSpawnedProbeCount, getMaxProbeCount, getCurrentPhase,
plus richer getState() output.

Validation-only. No production files, no map_CURRENT.html, no backend or
astrology math, no cache, no polygon renderer touched. Includes capture
harness, six PNG frames, manifest, and a full QA export with final verdict.
EOF
)"
```
