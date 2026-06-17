# Phase 3.27 True Discovery Acceptance Tests

These tests are an executable gate for any future true-discovery solver work.

They are designed to fail the Phase 3.26 sandbox because Phase 3.26 used passive visual marks, scripted timing, hardcoded proof booleans, and insufficient particle provenance.

Default probe target:

```bash
python validation/scripts/phase3_27_acceptance_probe.py \
  --sandbox validation/sandboxes/phase3_26_field_solver_emergence.html \
  --report CURSOR_EXPORT_PHASE_3_26_FIELD_SOLVER_EMERGENCE.md
```

Dynamic browser checks are mandatory for any future candidate acceptance. A run without `--url` must fail the dynamic migration gate and mark migration as dynamically unproven:

```bash
python validation/scripts/phase3_27_acceptance_probe.py \
  --sandbox validation/sandboxes/phase3_26_field_solver_emergence.html \
  --report CURSOR_EXPORT_PHASE_3_26_FIELD_SOLVER_EMERGENCE.md \
  --url http://127.0.0.1:8722/validation/sandboxes/phase3_26_field_solver_emergence.html
```

The probe exits non-zero if any required acceptance test fails. A future implementation cannot be accepted without dynamic migration proof.

## 1. Passive Sky Detection

Purpose: prove every visible star-like mark is an active solver particle.

Pass criteria:

- Star-like draw calls occur only inside a dedicated active particle renderer.
- Background rendering may draw grid lines, labels, panels, and non-particle scaffolding only.
- Background rendering must not call particle/star drawing helpers.
- Background rendering must not draw tiny dot-like marks that can be mistaken for active solver particles.

Fail criteria:

- Any `drawBackground` or equivalent passive renderer calls `drawCell`, `arc`, or another star-like primitive for field dots.
- Tiny `fillRect` calls inside passive render loops fail.
- Full-canvas background paint such as `ctx.fillRect(0, 0, W, H)` does not count as a star-like draw call.
- Any star-like mark lacks particle provenance.
- Rendered particle count cannot be matched to active solver particle count.

Concrete Phase 3.26 failure target:

- `drawBackground()` calls `drawCell(...)` for passive field dots.

## 2. Full-Field Migration Test

Purpose: prove visible particles actually migrate from full-field positions toward solver-discovered frontier zones.

Required data:

- Initial particle list at `t = 0`.
- Mid-animation particle list.
- Stable particle ids.
- Each particle’s required fields: `id`, `x0`, `y0`, `x`, `y`, `visible`, `origin`, `targetReason`.
- Solver cell width.
- Solver frontier cells at mid-animation.
- Proof that target cells are solver-discovered frontier or uncertainty cells.

Pass criteria:

- At `t = 0`, initial visible particles occupy at least 70% of configured macro cells.
- At mid-animation, at least 40% of initial particles moved more than `3 * cellWidth`.
- Movement vectors align more strongly with discovered high-frontier cells than with polygon boundary samples.
- No movement destination is a polygon-derived boundary target.
- Probe output must include `initialMacroCellCoverage`, `percentInitialParticlesMovedSignificantDistance`, `meanDistanceMoved`, `medianDistanceMoved`, `frontierAttractionAlignmentScore`, and `boundaryTargetAlignmentScore` when boundary samples exist.

Fail criteria:

- Any required particle provenance field is absent.
- Fewer than 40% of initial particles move more than `3 * cellWidth`.
- Movement direction cannot be compared to frontier state.
- Boundary-derived target data exists.
- Dynamic browser proof is not run.

Concrete Phase 3.26 failure target:

- Phase 3.26 particle state does not expose stable ids or initial positions as `(x0, y0)` for migration proof.

## 3. Boundary-Target Audit

Purpose: prove no hidden answer geometry is used as particle destination data.

Forbidden fields, names, and concepts:

- `seamTarget`
- `boundaryTarget`
- `settlementTarget`
- `finalTarget`
- `targetPolygon`
- `boundarySamples`
- `seamSamples`
- `polygonTarget`
- `targetFromPolygon`
- `buildBoundarySamples`
- `drawBoundaryLayer`
- `sampleBoundary`
- `traceBoundary`
- particle destinations derived from polygon vertices
- particle destinations derived from polygon edges
- final settlement destinations derived from polygon geometry

Pass criteria:

- No forbidden fields or equivalent target concepts appear in code.
- Particle target state contains only solver grid cell ids or solver field coordinates derived from sampled grid state.
- Polygon geometry is passed only to a truth oracle function.

Fail criteria:

- Any particle stores a polygon-derived destination.
- Any visible particle target is built from polygon vertices or edges.
- Any final settlement target is built from polygon vertices or edges.
- The implementation asserts target absence through a hardcoded debug boolean instead of instrumentation.

Concrete Phase 3.26 failure target:

- `hasDirectBoundaryTargets: false` is a hardcoded assertion, not proof.

## 3b. Geometry-Use Audit

Purpose: prove polygon geometry is used only by the truth oracle.

Required candidate instrumentation:

```text
polygonGeometryUseCounts = {
  truthOracleCalls,
  particleTargetUses,
  renderUses,
  finalRenderUses
}
```

Pass criteria:

- `polygonGeometryUseCounts` exists in the candidate sandbox or debug API.
- `truthOracleCalls` may be greater than zero.
- `particleTargetUses` must equal zero.
- `renderUses` must equal zero.
- `finalRenderUses` must equal zero.

Fail criteria:

- The instrumentation is missing.
- Any forbidden geometry-use counter is nonzero.
- The report relies on grep instead of geometry-use counters.

## 4. Time-Script Audit

Purpose: reject scripted timing described as solver behavior.

Forbidden patterns:

- final reveal driven by `progress`, `t`, elapsed milliseconds, or phase threshold
- compression driven by `progress`, `t`, elapsed milliseconds, or phase threshold
- virga driven by `progress`, `t`, elapsed milliseconds, or phase threshold
- color identity driven by `progress`, `t`, elapsed milliseconds, or phase threshold
- phase transitions presented as solver states but defined by static time thresholds

Pass criteria:

- Final reveal is gated by convergence metrics.
- Compression is gated by measured frontier narrowing.
- Virga is gated by explicit abandonment state.
- Color identity is gated by confidence/vote state only.
- Phase labels, if present, are derived from solver metrics.

Fail criteria:

- `finalAlpha = smoothstep(progress...)` or equivalent exists.
- `compression = smoothstep(progress...)` or equivalent exists.
- `cooling = smoothstep(progress...)` or equivalent controls virga.
- Color changes require `progress > ...`.
- `PHASES` or equivalent maps labels to fixed `t` values.

Concrete Phase 3.26 failure targets:

- `final: smoothstep((progress - 0.93) / 0.07)`
- `compression = smoothstep((progress - 0.56) / 0.20)`
- `cooling = smoothstep((state.progress - 0.76) / 0.16)`
- `state.progress > 0.42` and `state.progress > 0.44` color gates
- static `PHASES` array with `t` thresholds

## 5. Froth Causality Test

Purpose: prove froth is caused by solver pressure rather than jitter or labels.

Required metrics:

- local particle density
- baseline particle density
- local congestion or velocity variance
- recent repeated sampling rate
- unresolved frontier pressure
- neighbor disagreement
- unresolved duration

Pass criteria:

- Froth regions exceed density threshold relative to baseline.
- Froth regions show congestion or velocity variance.
- Froth regions show repeated recent sampling.
- Froth regions coincide with unresolved frontier pressure.
- Froth is not enabled by phase name or timestamp.

Fail criteria:

- No froth metrics exist.
- Froth is represented only by larger dots, jitter, alpha, or color.
- Froth activation depends on `progress`, `t`, or static phase labels.
- Froth appears where unresolved frontier pressure is low or unmeasured.

Concrete Phase 3.26 failure target:

- dot size changes with `state.progress > 0.55`, while no explicit froth causality metric is exposed.

## 6. Virga Causality Test

Purpose: prove virga is caused by abandonment state.

Required particle state:

```text
abandoned: boolean
abandonedStep: integer or null
abandonmentReason: string or null
```

Allowed abandonment reasons:

- `outside_resolved`
- `frontier_moved_away`
- `low_information_value`
- `superseded_by_higher_confidence_region`

Pass criteria:

- Every virga particle has `abandoned = true`.
- Every virga particle has `abandonedStep`.
- Every virga particle has an allowed `abandonmentReason`.
- Virga motion is derived from abandonment age and local state, not global progress.

Fail criteria:

- Virga lift/fade begins at fixed progress or elapsed time.
- Virga particles lack abandonment state.
- Outside particles become virga solely because they are outside.
- Virga is a visual effect without solver state transition.

Concrete Phase 3.26 failure target:

- virga uses `cooling = smoothstep((state.progress - 0.76) / 0.16)` and no explicit abandonment reason.

## 7. Final Renderer Test

Purpose: reject raw grid bricks and time-gated final reveal.

Pass criteria:

- Final render is enabled only after convergence metrics pass.
- Final output is not raw grid-cell rectangles.
- Canvas `fillRect` is allowed for background paint and particle-sized marks.
- Final renderer mode must be declared as `debugGrid` or `resolvedContour`.
- Acceptance final mode must be `resolvedContour` or an equivalent non-brick renderer.
- Debug grid may be visible only in debug mode.
- Non-debug final output must be generated from the resolved field through a renderer that does not expose raw yellow raster bricks.

Fail criteria:

- Final output uses grid-cell-sized `fillRect` calls per resolved cell as the visible body.
- Final renderer mode is missing.
- Final renderer mode is `debugGrid` for acceptance output.
- Final visibility is multiplied by a time-derived alpha.
- Final polygon can appear while frontier pressure remains unresolved.
- Final render is enabled by progress, elapsed time, or fixed phase label.

Concrete Phase 3.26 failure targets:

- `drawFinal(finalAlpha, sim)` draws `ctx.fillRect(...)` for cells.
- `finalAlpha` is derived from `progress`.

## 8. Report Truthfulness Test

Purpose: prevent reports from claiming compliance without proof.

Pass criteria:

- Every success claim cites exact code evidence and passing test output.
- Every claim using “emergent,” “truth-oracle only,” “no direct boundary targets,” “virga,” “compression,” or “final” must cite a named passing test and the associated output.
- Screenshots are treated as visual evidence only, not mechanism proof.
- Grep checks are treated as necessary but insufficient.
- Debug booleans are treated as assertions unless backed by instrumentation.
- Unproven causal claims are labeled `UNPROVEN`.
- Time-driven behavior is labeled `SCRIPTED`.
- Literal debug assertions are labeled `HARDCODED`.

Fail criteria:

- Report claims success based on screenshots alone.
- Report claims success based on grep alone.
- Report claims success based on hardcoded booleans.
- Report uses “emergent,” “solver-caused,” or equivalent without causal evidence.
- Report uses required claim language without naming the passing test that proves it.

Concrete Phase 3.26 failure targets:

- `usesTruthOracleOnly: true` is hardcoded in debug state.
- `hasDirectBoundaryTargets: false` is hardcoded in debug state.
- The Phase 3.26 report claimed compliance while final reveal, compression, virga, and phase labels were scripted.

## Required Output Format

The acceptance probe must produce JSON with this shape:

```json
{
  "sandbox": "path",
  "report": "path or null",
  "passed": false,
  "tests": [
    {
      "name": "passive_sky_detection",
      "mode": "static",
      "passed": false,
      "evidence": ["..."],
      "failures": ["..."]
    }
  ]
}
```

The process must exit with:

- `0` only if all tests pass
- `1` if any test fails
- `2` if the probe itself cannot run due to missing inputs

The output must identify static-only failures separately from dynamically unproven failures through each test’s `mode` field.
