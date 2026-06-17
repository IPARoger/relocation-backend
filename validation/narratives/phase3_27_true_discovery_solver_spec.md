# Phase 3.27 True Discovery Solver Spec

This is a pre-implementation specification only.

The controlling premise is the Phase 3.26 accountability failure audit: Phase 3.26 failed, overclaimed, and must not be used as the base for patching. Phase 3.27 must be designed so the implementation cannot repeat the same failure mode.

No animation work may begin until this specification is accepted and converted into executable acceptance tests.

## 1. Visible Particle Provenance

Every visible star must be an active solver particle.

No decorative background star field is allowed.

No renderer may draw passive sky dots, passive noise, passive sampling texture, or non-solver decoration that can be mistaken for active solver population.

Required particle state:

```text
Particle {
  id: stable deterministic id
  birthStep: solver step when created
  origin: "initial_full_field" | "frontier_spawn"
  x: current x position
  y: current y position
  x0: initial x position
  y0: initial y position
  vx: current x velocity
  vy: current y velocity
  sampleCount: number of truth samples taken by this particle
  lastSampleStep: most recent solver step sampled
  lastTruth: "inside" | "outside" | "unknown"
  currentCellId: current grid cell
  targetCellId: current solver-selected grid destination, if any
  targetReason: "frontier_pressure" | "uncertainty_gradient" | "local_resample" | "none"
  abandoned: boolean
  abandonedStep: solver step when abandoned, or null
  visible: boolean
}
```

Visible particle proof requirements:

- The renderer must draw particles only by iterating the solver particle list.
- Each rendered particle must expose its `id`, `origin`, current position, initial position, current cell, target cell, and target reason through debug instrumentation.
- A test must compare rendered particle count against active visible solver particle count.
- Any draw call that produces a star-like mark outside the solver particle renderer is a failure.
- Migration proof must use particle histories: for each visible particle, compare `(x0, y0)` to `(x, y)` and compare movement direction to solver frontier zones.

## 2. Full-Field Migration Test

The implementation must include an automated test proving full-field migration.

Pass/fail requirements:

- At `t = 0`, initial particles must be broadly distributed across the full field.
- Broad distribution must be measured by occupied grid coverage, not visual impression.
- Required `t = 0` coverage: at least 70% of macro cells occupied by one or more initial visible particles.
- By mid-animation, at least 40% of initial particles must have moved at least a configured significant distance.
- Significant distance must be defined before implementation as a minimum of `3 * cellSize` or an equivalent explicit pixel threshold.
- Mid-animation movement must be statistically biased toward solver-discovered frontier zones.
- The test must compare particle movement vectors against nearest high-frontier cells discovered by the solver.
- The test must prove particles are not moving toward precomputed polygon boundary targets.

Required test outputs:

```text
initialParticleCount
initialMacroCellCoverage
midParticleCount
percentInitialParticlesMovedSignificantDistance
meanDistanceMoved
medianDistanceMoved
frontierAttractionAlignmentScore
boundaryTargetAlignmentScore
hasPrecomputedBoundaryTargets
pass
```

Failure conditions:

- If particles are broadly visible but not active solver particles: fail.
- If particles remain mostly static by mid-animation: fail.
- If movement direction correlates more strongly with polygon boundary samples than with discovered frontier cells: fail.
- If the test cannot identify particle provenance: fail.

## 3. No Hidden Target Knowledge

The implementation must not encode hidden polygon answers as particle destinations.

Forbidden code concepts:

- `seamTarget`
- `boundaryTarget`
- `settlementTarget`
- `finalTarget`
- `targetPolygon`
- `boundarySamples`
- `seamSamples`
- direct visible particle destinations derived from polygon vertices
- direct visible particle destinations derived from polygon edges
- lerp/interpolation from particle position to polygon-derived coordinate

Required grep checks:

```bash
grep -n "seamTarget\|boundaryTarget\|settlementTarget\|finalTarget\|targetPolygon\|boundarySamples\|seamSamples" validation/sandboxes/phase3_27_true_discovery_solver.html || true
grep -n "lerp(.*target\|interpolate.*target\|target.*polygon\|polygon.*target" validation/sandboxes/phase3_27_true_discovery_solver.html || true
grep -n "buildBoundarySamples\|drawBoundaryLayer\|sampleBoundary\|traceBoundary" validation/sandboxes/phase3_27_true_discovery_solver.html || true
```

Required structural proof:

- Polygon geometry may be passed only to `truth(point)` or an equivalent oracle function.
- Visible particles may target only solver grid cells.
- Solver grid cells may become attractive only through accumulated sampling, uncertainty, activity, and frontier pressure.
- If any particle stores a polygon-derived coordinate as a target, the implementation fails.
- If final settlement uses polygon vertices, polygon edges, or boundary samples as destinations, the implementation fails.

## 4. Solver-Caused Froth

“Froth” must be a measured solver condition, not jitter and not a time label.

Numerical definition:

Froth exists in a cell or local region when all of the following are true:

- local particle density is above baseline field density by a configured multiplier
- particle velocity variance indicates congestion or competition
- sample count in the local region has increased repeatedly over recent solver steps
- frontier pressure remains unresolved
- inside/outside neighbor disagreement persists

Required froth metrics:

```text
localParticleDensity
baselineParticleDensity
densityMultiplier
localVelocityVariance
recentSampleRate
frontierPressure
neighborDisagreement
unresolvedDuration
```

Failure conditions:

- If froth is triggered by phase name or timestamp: fail.
- If froth is merely random jitter: fail.
- If froth appears without increased particle density: fail.
- If froth appears without repeated sampling: fail.
- If froth appears where frontier pressure is low: fail.

## 5. Solver-Caused Compression

Compression must mean measured frontier narrowing.

Compression is not allowed to be `smoothstep(time)`, `progress`, or a named animation phase.

Numerical definition:

Compression occurs when:

- total unresolved frontier area decreases over a window of solver steps
- frontier band width decreases over the same window
- particle density along remaining frontier increases
- outside and inside confidence fields become sharper around the remaining boundary
- unresolved corridors collapse into fewer, narrower zones

Required compression metrics:

```text
frontierCellCountNow
frontierCellCountPreviousWindow
frontierBandWidthNow
frontierBandWidthPreviousWindow
frontierParticleDensityNow
frontierParticleDensityPreviousWindow
confidenceGradientNow
confidenceGradientPreviousWindow
compressionRatio
```

Failure conditions:

- If compression starts at a fixed progress value: fail.
- If compression changes damping or search radius based on time: fail.
- If compression is visible but the frontier metrics do not narrow: fail.

## 6. Solver-Caused Virga

Virga must be caused by explicit abandonment state.

No progress-based fake lift is allowed.

Required abandonment state:

```text
Particle.abandoned = true
Particle.abandonedStep = step
Particle.abandonmentReason =
  "outside_resolved" |
  "frontier_moved_away" |
  "low_information_value" |
  "superseded_by_higher_confidence_region"
```

Virga eligibility:

- particle was previously active
- particle sampled or contributed to an outside-leaning region
- particle is no longer useful to unresolved frontier pressure
- particle has an explicit abandonment reason
- particle enters a cooling/decay behavior derived from abandonment age, not global progress

Failure conditions:

- If virga lift begins at a fixed time: fail.
- If virga particles lack abandonment reasons: fail.
- If all outside particles lift regardless of solver usefulness: fail.
- If virga is only a visual fade effect with no solver state transition: fail.

## 7. Final Resolution Gate

The final polygon cannot appear based on time.

Forbidden:

- `finalAlpha = smoothstep(progress)`
- final render enabled by `t > threshold`
- final render enabled by phase label
- final render enabled by elapsed milliseconds

Required convergence metrics:

```text
samplingCoverage
resolvedInsideCellCount
resolvedOutsideCellCount
unresolvedCellCount
frontierCellCount
frontierCellCountDeltaWindow
maxFrontierPressure
averageConfidenceIncludingUnsampledCells
confidenceStabilityWindow
minimumConsecutiveStableSteps
```

Final render may begin only when all configured convergence criteria pass:

- sampling coverage exceeds threshold
- unresolved cell count is below threshold
- frontier pressure is below threshold or stable within a narrow band
- confidence is stable over a configured window
- no high-pressure frontier cells remain
- minimum consecutive stable solver steps has elapsed

Failure conditions:

- If final render appears before convergence metrics pass: fail.
- If final render appears only because time reached a threshold: fail.
- If final render can appear while frontier pressure remains high: fail.

## 8. Renderer Separation

The solver grid is internal evidence only.

The final visual must not expose yellow raster bricks.

Renderer rules:

- Debug mode may show grid cells.
- Non-debug final mode may not show raw cell rectangles as the final polygon body.
- Final visual must be generated from the resolved field through a rendering layer that smooths or contours the stable field without using polygon boundary samples as visual rails.
- The renderer must distinguish between debug evidence and production visual output.
- Any final image that visibly exposes grid-cell brick structure as the primary shape fails.

Required proof:

- Debug screenshots may include grid evidence.
- Acceptance screenshots must include non-debug final output.
- A visual or pixel-level check must verify that final output is not a raw grid-cell raster.

## 9. Acceptance Tests

Implementation cannot begin until these pass/fail tests are defined as executable checks.

Required tests:

1. Visible particle provenance test
   - Pass if every visible star maps to an active solver particle.
   - Fail if passive decorative stars are drawn.

2. Full-field initial distribution test
   - Pass if initial visible particles cover required macro-cell area.
   - Fail if initial particles are clustered near the answer.

3. Full-field migration test
   - Pass if required percentage of initial particles move significant distance toward discovered frontier zones.
   - Fail if particles remain decorative or static.

4. No hidden target knowledge grep test
   - Pass if forbidden target terms and interpolation patterns are absent.
   - Fail on any hidden target shortcut.

5. Geometry-use audit test
   - Pass if polygon geometry is used only by truth oracle code.
   - Fail if polygon geometry is used to create visible particle targets, final settlement targets, or boundary rails.

6. Frontier causality test
   - Pass if high visible frontier/froth regions correspond to high measured frontier pressure.
   - Fail if frontier visuals are phase-timed or uncorrelated.

7. Froth causality test
   - Pass if froth appears only where density, congestion, repeated sampling, and unresolved frontier pressure exceed thresholds.
   - Fail if froth is jitter or a time label.

8. Compression causality test
   - Pass if compression corresponds to measured frontier narrowing.
   - Fail if compression is caused by progress or elapsed time.

9. Virga abandonment test
   - Pass if virga particles have explicit abandonment state and reasons.
   - Fail if virga lift/fade is globally time-scripted.

10. Final resolution gate test
    - Pass if final render appears only after convergence metrics pass.
    - Fail if final render is progress-gated.

11. Final renderer separation test
    - Pass if final output does not expose raw yellow grid bricks.
    - Fail if final polygon body is raw cell rectangles.

12. Report truthfulness test
    - Pass if every report claim cites passing tests or exact code evidence.
    - Fail if any claim relies on screenshots alone, hardcoded booleans, or intended behavior.

## 10. Forbidden Claims

No report may claim success unless tests pass.

Forbidden report claims unless proven by executable evidence:

- “emergent”
- “solver-caused”
- “field-discovered”
- “truth-oracle only”
- “no direct boundary targets”
- “no hidden rails”
- “full-field migration”
- “compression from uncertainty”
- “virga from abandonment”
- “final after stabilization”
- “visible particles are solver particles”

Required reporting standard:

- Each claim must cite exact code evidence and test output.
- Screenshots may support a claim but may not prove mechanism by themselves.
- Hardcoded debug booleans are not proof.
- Passing grep is necessary but not sufficient.
- If causality is not proven, the report must say UNPROVEN.
- If timing drives the behavior, the report must say SCRIPTED.
- If a literal debug assertion stands in for verification, the report must say HARDCODED.
