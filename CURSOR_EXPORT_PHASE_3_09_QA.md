# Phase 3.09 QA Export — Probe Reproduction Sandbox

Validation-only QA snapshot. No production files were touched. No commits were made.

Scope of file changes for this export:

- `validation/sandboxes/phase3_01_rain_reveal_sandbox.html` (existing Phase 3.09 sandbox; **unchanged this turn**).
- `scripts/capture_phase3_09_rain_reproduction.py` (new; capture harness only).
- `validation/screenshots/phase3_09_rain_reproduction/` (new; 6 PNG frames + manifest.json).
- `CURSOR_EXPORT_PHASE_3_09_QA.md` (this report).

## What Changed in Phase 3.09

The sandbox replaced the old broad "all probes everywhere" model with a staged scout → reproduction → fade pipeline. Highlights pulled from
`validation/sandboxes/phase3_01_rain_reveal_sandbox.html`:

- Three probe populations: `SCOUT_PROBE_COUNT = 620`, `REPRODUCTION_PROBE_COUNT = 2600`, `GHOST_PROBE_COUNT = 520` (total 3740 probes, confirmed live via `__truthSubstrateSandbox.getProbeCount()`).
- One **selected hidden region** (proto-contour A). Boundary candidates are split into right-side and left-side validation colors; a third "wrong-side" color marks samples that should die back once confidence rises.
- Two **ghost candidate regions** (proto-contours B and C). Ghost samples reproduce on a single side of their boundary then fade ("almost born → disappears") via `ghostAbortT`.
- Time-keyed status pill drives narrative:
  - `latent probes initializing`
  - `scouts searching hidden regions`
  - `local reproduction near boundary candidates`
  - `boundary confidence culling wrong-side samples`
  - `ghost candidate samples fading`
- Guide layer now draws the selected corridor, both boundary candidate sides, the wrong-side bands, and the ghost one-sided zones.

Timing schedule (after `MOTION_DELAY_MS = 360`):

| Phase                      | Onset (ms) | Duration window | Trigger variable    |
|---------------------------|-----------:|-----------------|--------------------|
| Motion ramp                | 0          | 1100            | `motionT`           |
| Reproduction               | 1050       | 2600            | `reproductionT`     |
| Boundary confidence        | 3300       | 1800            | `confidenceT`       |
| Ghost abort                | 4300       | 1800            | `ghostAbortT`       |
| Interior fill              | 3900       | 2700            | `interiorFillT`     |

## Captured Frame Sequence

Frames live in `validation/screenshots/phase3_09_rain_reproduction/` and were captured headlessly in Playwright by driving the sandbox's public `restart` / `setSpeed` / `setGuides` API at speed 4×. Observed status text at each frame matched the expected phase label.

| File                              | Sim elapsed (ms) | Guides | Observed status                                  |
|-----------------------------------|-----------------:|--------|--------------------------------------------------|
| `01_t0_initial.png`               | 0                | off    | `latent probes initializing`                     |
| `02_scout_phase.png`              | 900              | off    | `scouts searching hidden regions`                |
| `03_reproduction_phase.png`       | 2700             | off    | `local reproduction near boundary candidates`    |
| `04_ghost_fade_phase.png`         | 5500             | off    | `ghost candidate samples fading`                 |
| `05_late_state.png`               | 9000             | off    | `ghost candidate samples fading`                 |
| `06_late_state_guides.png`        | 9000             | on     | `ghost candidate samples fading`                 |

A machine-readable summary is at `validation/screenshots/phase3_09_rain_reproduction/manifest.json`.

## QA Findings (honest)

**Shape birth visible? — Partially.**
Between frame 02 (sparse scout dots) and frame 03 (reproduction) the central diagonal corridor accumulates noticeably more probes than the rest of the map. By frame 05 there is a clear left-to-right orange band in the northern hemisphere and a parallel blue band south of it. With guides off the viewer can sense that "something curved is forming," but the structure does not yet read as a single closed region. The eye sees a coherent corridor, not yet a recognizable shape.

**Local reproduction visible? — Yes.**
Frame 02 vs frame 03 is the strongest evidence: dot density in the boundary corridor visibly thickens while the background scatter does not. The pacing is also legible because the status pill confirms the transition.

**Ghost fade visible? — Yes (subtle but real).**
Between frame 03 and frame 05 the purple ghost cluster in the lower-right thins and the lower-left purple swath collapses to a faint residue. Frame 06 with guides shows the ghost one-sided zones aligned exactly where the fading purple lived. The effect is more legible at speed 1× in-browser than in a still — the fade is most readable as motion.

**Low-interest regions thin? — Partially.**
The unresolved samples class fades correctly (its `unresolvedPresence` is gated on `reproductionT`). However, frames 03–05 still show a noticeable background population because reproduction probes were *pre-seeded at startup* (`createReproductionProbes` is called inside the initial `createProbes`). The growth is therefore a fade-in of pre-allocated probes, not true on-the-fly cell division.

**Guides explain the hidden structure? — Yes.**
Frame 06 cleanly labels: `selected hidden region`, `right-side boundary candidates`, `left-side boundary candidates`, `wrong-side samples`, `ghost candidate region`, `ghost one-sided boundary zone`. The diagonal selected corridor visibly carries the dense reproduction.

## Weaknesses

1. **Probe count is fixed at load (3740).** Reproduction is simulated by holding spawn probes invisible until their `delay` elapses, then easing them in via `birthPresence = easedLocal`. Functionally this looks like growth, but it is not an emergent multiplication process — there is no spawning loop driven by local confidence. If the next pass wants the "germs locally divide when they discover truth" feel, the architecture should let probes call a `spawnNeighbor()` when their boundary score crosses a threshold.
2. **Coverage is global, not concentrated enough yet.** Even at frame 05 there is a thin haze of probes far from the selected corridor (mostly wrong-side and unresolved samples still mid-fade). The "low interest regions empty out" goal is only ~70% achieved visually.
3. **Frame 02 (scout phase) reads sparse and a bit chaotic.** Without guides, the scout layer alone does not yet hint at where the structure will form. The visual story starts at frame 03.
4. **Ghost regions abort before becoming visually compelling.** Their density peak is brief and modest; in still frames they read more like noise than as "almost born regions." The intended "almost there → dies" narrative arc is more legible in motion than in stills.
5. **Color encoding is dense.** Six classes (positive, negative, wrong, interior, ghost, unresolved) overlap geographically, which makes guides-off interpretation harder than the underlying logic deserves.

## Next Recommended Narrow Pass

Single-instability proposal for Phase 3.11 (do not start without explicit go-ahead):

> Replace pre-seeded reproduction probes with **event-driven local spawning**. A scout that lands within the boundary corridor calls `spawnNeighbor()` up to N times within a small radius, with a cooldown. Wrong-side scouts get a lower spawn cap; ghost scouts get a sharp cap and a hard abort time. This converts the current fade-in trick into actual locally driven density growth without changing astrology math, the polygon renderer, or production code.

Optional companion: reduce the visible color palette to **three** classes during guides-off display (selected boundary, selected interior, ghost) and keep the six-class palette only when guides are on. This protects the "shape being born" signal from being washed out by class noise.

## Files Changed This Turn

```
?? CURSOR_EXPORT_PHASE_3_09_QA.md
?? scripts/capture_phase3_09_rain_reproduction.py
?? validation/screenshots/phase3_09_rain_reproduction/01_t0_initial.png
?? validation/screenshots/phase3_09_rain_reproduction/02_scout_phase.png
?? validation/screenshots/phase3_09_rain_reproduction/03_reproduction_phase.png
?? validation/screenshots/phase3_09_rain_reproduction/04_ghost_fade_phase.png
?? validation/screenshots/phase3_09_rain_reproduction/05_late_state.png
?? validation/screenshots/phase3_09_rain_reproduction/06_late_state_guides.png
?? validation/screenshots/phase3_09_rain_reproduction/manifest.json
```

Phase 3.09 behavior was **not** modified. `map_CURRENT.html`, backend, math, cache, and final polygon renderer were **not** touched.

## Git Status Summary (relevant to this export)

```
 M validation/reports/map_current_smoke.json     (from previous smoke run, unchanged this turn)
?? scripts/capture_phase3_09_rain_reproduction.py (new, this turn)
?? validation/reports/phase2_cache_smoke.json    (from previous smoke run, unchanged this turn)
?? validation/screenshots/phase3_09_rain_reproduction/  (new, this turn)
?? CURSOR_EXPORT_PHASE_3_09_QA.md                (this report)
```

The broader repo has many other pre-existing modified/untracked entries from earlier work; none were created or altered by this export.
