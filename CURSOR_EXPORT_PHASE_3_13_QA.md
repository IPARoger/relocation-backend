# Phase 3.13 — Gap Closure / Membrane Pressure (QA Export)

Scope honored:
- Edited only `validation/sandboxes/phase3_01_rain_reveal_sandbox.html` for behavior.
- No production/backend/cache/map_CURRENT/docs/commit changes.

## What changed in Phase 3.13

The 3.12 frontier model was kept and extended with local pressure equalization:

- Added **gap pressure constants** and tighter locality windows:
  - `GAP_PRESSURE_WINDOW_T`
  - `WAKE_PROPAGATION_MAX_EXTRA`
  - tuned `FRONTIER_LOCAL_WINDOW_T`, `LOCAL_SPAWN_DISTANCE_PX`
- Added **neighbor wake propagation** in `_onSettle()` for selected inside-boundary grains:
  - each settled grain computes local unresolved-gap demand
  - demand/proximity increases local spawn budget
  - extra pressure spawns increment `wakePropagationCount`
  - solved regions auto-quiet (closure gating)
- Added local gap diagnostics helpers:
  - `_gapStatsAt(front, tParam, window)`
  - `_unresolvedGapCount(contourIndex)`
  - `_closureConfidence(contourIndex)`
  - `_averageGapDistance(contourIndex)`
- Kept ghost one-sided behavior but made abort timing explicit with
  `GHOST_ABORT_START_CONFIDENCE` so ghost closure attempts imply topology and then withdraw.
- Updated HUD/status text to report unresolved gaps + closure progression.

## Debug API updates (requested)

Added to `window.__truthSubstrateSandbox`:
- `getGapPressureActive()`
- `getUnresolvedGapCount()`
- `getClosureConfidence()`
- `getAverageGapDistance()`
- `getWakePropagationCount()`
- `getLocalMotionRatio()`

And in `getState()`:
- `gapPressureActive`
- `unresolvedGapCount`
- `closureConfidence`
- `averageGapDistance`
- `wakePropagationCount`
- `localMotionRatio`

## Smoke results (headless)

Validated with inline Playwright smoke and deterministic restarts:

- `local spawn ratio stays high`: **PASS**
  - late `localSpawnRatio`: **0.84**
  - late `longRangeSpawnRatio`: **0.15**
- `unresolved gap count decreases`: **PASS**
  - `95 -> 79 -> 17 -> 0`
- `closure confidence rises`: **PASS**
  - `0.01 -> 0.18 -> 0.82 -> 1.00`
- `no monolithic gear shift`: **PASS**
  - counts evolve organically (`live 42 -> 145 -> 112`, `spawned 0 -> 103 -> 111`)
- `no long-distance decorative travel`: **PASS**
  - `localMotionRatio` remains high (>= 0.82 while active, 1.0 in settled late state)
- Console/runtime errors: **none**

## Evidence captures

Saved 6 frames under:
- `validation/screenshots/phase3_13_gap_pressure/`
  - `01_t0_initial.png`
  - `02_seed_phase.png`
  - `03_gap_pressure_closure.png`
  - `04_membrane_locking.png`
  - `05_late_state.png`
  - `06_late_state_guides.png`
  - `manifest.json`

## Honest verdict

This now reads much more like a **membrane closing around hidden topology** than “dots near lines”.

Why:
- unresolved gaps now actively attract local spawning pressure
- neighbor wake propagation closes adjacent holes as tension builds
- solved zones calm down rather than continuing decorative movement
- closure reaches full contour coverage in smoke runs while preserving locality-first motion

Residual caveat:
- closure can happen quickly in high-pressure moments (by design in this narrow pass). A future micro-pass could slightly damp late-stage wake bursts for an even more gradual final lock-in.

## Focused git status

```
 M validation/sandboxes/phase3_01_rain_reveal_sandbox.html
?? validation/screenshots/phase3_13_gap_pressure/
?? CURSOR_EXPORT_PHASE_3_13_QA.md
```

