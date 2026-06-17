# Phase 3.26 Field Solver Emergence Export

## Scope

Created a new sandbox only:

- `validation/sandboxes/phase3_26_field_solver_emergence.html`

The Phase 3.22 animation file was not modified.

## Implementation Summary

Phase 3.26 replaces the previous polygon-renderer mental model with a coarse field solver:

- The backend Sun-in-1 polygon is fetched once and projected into sandbox canvas space.
- The polygon is used as a `truth(point)` oracle for inside/outside sampling.
- Broad deterministic probes begin across the full field, not on the polygon boundary.
- A coarse confidence grid accumulates `insideVotes`, `outsideVotes`, activity, confidence, and frontier scores.
- Frontier cells emerge from neighboring inside/outside disagreement.
- Probe movement is driven by nearby unresolved frontier/grid state.
- Additional probes spawn locally near high-frontier/high-uncertainty cells.
- Yellow/blue identity is derived from accumulated vote confidence.
- Outside activity cools into virga as frontier pressure collapses.
- Final silence is drawn from resolved inside grid cells after confidence stabilization, not from traced boundary rails.

The sandbox exposes `window.__phase326State` with:

- `currentPhase`
- `elapsed`
- `t`
- `activeProbeCount`
- `totalSampleCount`
- `frontierCellCount`
- `resolvedInsideCellCount`
- `resolvedOutsideCellCount`
- `averageConfidence`
- `maxFrontierScore`
- `hasDirectBoundaryTargets: false`
- `usesTruthOracleOnly: true`

## Acceptance Answers

**Does any visible probe start on a polygon boundary target?**  
No. Initial probes are generated from a deterministic broad lattice over the canvas. They are not seeded from polygon vertices, edges, rings, or boundary samples.

**Does any visible probe have a precomputed seam target?**  
No. Probes carry position, velocity, seed, birth time, energy, and last sampled truth. There is no precomputed seam destination per probe.

**Is motion driven by local grid/frontier state?**  
Yes. Probe movement uses nearby confidence-grid frontier scores, unresolved confidence, and activity pressure. The attraction point is the center of a local grid cell selected from frontier state, not a polygon boundary coordinate.

**Is the real polygon used only for `truth(point)`?**  
Yes for the solver behavior and visual emergence path. The projected polygon ring is used by `sampleTruth(point)` / point-in-polygon checks to classify probe samples. The final visible body is rendered from resolved inside grid cells after stabilization.

**What still feels fake or provisional?**  
The MVP still recomputes deterministically from zero for each scrubbed frame rather than preserving a live solver state. Confidence is cell-local and can look too clean because each cell quickly becomes pure inside or outside once sampled. Frontier congestion is real grid disagreement, but its visual compression is still tuned heuristically. The final body is a rasterized confidence result rather than a production contour extraction from the stabilized field.

## Proof Screenshots

Captured to `validation/screenshots/phase3_26_field_solver_emergence/`:

- `01_uncertainty.png`
- `02_sampling.png`
- `03_frontier_emergence.png`
- `04_peak_froth.png`
- `05_compression.png`
- `06_cooling_virga.png`
- `07_final_silence.png`

Capture output:

```text
01_uncertainty.png: t=0.030 phase=uncertainty probes=1219 samples=7314 frontier=8
02_sampling.png: t=0.200 phase=sampling probes=1219 samples=47541 frontier=28
03_frontier_emergence.png: t=0.380 phase=frontier emergence probes=1256 samples=89158 frontier=167
04_peak_froth.png: t=0.560 phase=peak froth probes=1477 samples=135315 frontier=275
05_compression.png: t=0.700 phase=compression probes=1728 samples=178894 frontier=191
06_cooling_virga.png: t=0.880 phase=cooling / virga probes=1803 samples=239774 frontier=102
07_final_silence.png: t=1.000 phase=final silence probes=1803 samples=281243 frontier=54
```

## Required Check

Command:

```bash
grep -n "Math.random\\|seamTarget\\|boundaryTarget\\|lerp(.*target\\|buildBoundarySamples\\|drawBoundaryLayer" validation/sandboxes/phase3_26_field_solver_emergence.html || true
```

Output:

```text

```

No prohibited matches were found.

## Additional Verification

Direct deterministic render/debug check:

```text
t=0.030 phase=uncertainty probes=1219 samples=7314 frontier=8 inside=141 outside=1104 avg=0.999 maxFrontier=0.646 noTargets=False truthOnly=True feature=house-0-sun-1-0
t=0.200 phase=sampling probes=1219 samples=47541 frontier=28 inside=190 outside=1478 avg=0.999 maxFrontier=1.000 noTargets=False truthOnly=True feature=house-0-sun-1-0
t=0.380 phase=frontier emergence probes=1256 samples=89158 frontier=167 inside=355 outside=2106 avg=0.994 maxFrontier=1.000 noTargets=False truthOnly=True feature=house-0-sun-1-0
t=0.560 phase=peak froth probes=1477 samples=135315 frontier=275 inside=504 outside=3039 avg=0.985 maxFrontier=0.916 noTargets=False truthOnly=True feature=house-0-sun-1-0
t=0.700 phase=compression probes=1728 samples=178894 frontier=191 inside=506 outside=3225 avg=0.985 maxFrontier=1.000 noTargets=False truthOnly=True feature=house-0-sun-1-0
t=0.880 phase=cooling / virga probes=1803 samples=239774 frontier=102 inside=505 outside=3268 avg=0.985 maxFrontier=0.997 noTargets=False truthOnly=True feature=house-0-sun-1-0
t=1.000 phase=final silence probes=1803 samples=281243 frontier=54 inside=506 outside=3293 avg=0.985 maxFrontier=0.997 noTargets=False truthOnly=True feature=house-0-sun-1-0
```

Note: Python prints JavaScript `false` as `False` in this diagnostic output.

