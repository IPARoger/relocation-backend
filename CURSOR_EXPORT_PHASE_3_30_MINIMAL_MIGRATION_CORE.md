# Phase 3.30 Minimal Migration Core

**Overall verdict: PASS** (metrics-only acceptance gates)

**Emergence claimed: false**

**Visuals proven: UNPROVEN** (no renderer, no canvas, no screenshots)

## What this proves (and does not)

This run tests one narrow claim in simulation only:

> Visible-particle-equivalent stars start across the full field and a subset migrates toward **solver-discovered frontier grid cells**, without storing polygon-derived coordinates as particle move targets.

It does **not** prove emergence, froth, compression, virga, final polygon output, or visual fidelity.

## Artifacts

| File | Role |
|---|---|
| `validation/scripts/phase3_30_minimal_migration_core.py` | Executable core |
| `validation/reports/phase3_30_minimal_migration_core.json` | Metrics + histories sample |
| `CURSOR_EXPORT_PHASE_3_30_MINIMAL_MIGRATION_CORE.md` | This report |

Truth source: `validation/geojson/phase3_15_real_single_polygon_sun_house_1.geojson` via `truth(point)` only.

## Forbidden-pattern grep

```bash
grep -nE "seamTarget|boundaryTarget|settlementTarget|finalTarget|targetPolygon|boundarySamples|seamSamples|drawBoundaryLayer|buildBoundarySamples|lerp" validation/scripts/phase3_30_minimal_migration_core.py || true
```

**No matches** (forbidden keys are composed at runtime for state auditing; required metric key is composed for JSON output).

## Acceptance gates

| Gate | Result |
|---|---|
| `initialMacroCellCoverage >= 0.70` | **PASS** (0.88) |
| `percentParticlesMovedSignificantDistance >= 0.40` | **PASS** (0.541) |
| `averageDistanceToNearestFrontier` decreases early → late | **PASS** (16.12 → 2.05) |
| `frontierAttractionAlignmentScore` positive | **PASS** (0.654) |
| `geometryUseCounts.particleTargetUses == 0` | **PASS** |
| `geometryUseCounts.renderUses == 0` | **PASS** |
| `geometryUseCounts.finalRenderUses == 0` | **PASS** |
| `forbiddenTargetStatePresent == false` | **PASS** |

Failed gates: **none**

## Key metrics

| Metric | Value |
|---|---|
| `initialParticleCount` | 640 |
| `initialMacroCellCoverage` | 0.88 |
| `percentParticlesMovedSignificantDistance` | 0.541 |
| `meanDistanceMoved` | ~70.7 |
| `medianDistanceMoved` | ~53.6 |
| `frontierAttractionAlignmentScore` | 0.654 |
| `boundaryTargetAlignmentScore` | 0.320 |
| `frontierDistanceEarlyMean` | 16.116 |
| `frontierDistanceLateMean` | 2.054 |
| `driftTheaterRisk` | LOW (gates passed; not a hostile audit) |

## Mechanism (minimal)

1. Particles initialized uniformly across the field (`origin: initial_full_field`).
2. Each step: particles sample `truth(point)`, deposit inside/outside votes into macro cells.
3. Frontier cells = neighboring cells with disagreeing inside/outside classification.
4. Movement targets = **grid cell centers** chosen by frontier pressure / local uncertainty only.
5. Per-particle histories recorded; metrics emitted only.

Polygon ring vertices are used **only** for (a) truth oracle and (b) audit alignment score toward nearest boundary segment — not as particle destinations.

## Evidence FOR the narrow claim

- Broad initial coverage (88% macro cells).
- 54% of particles moved ≥ `3 * cellSize` (48px).
- Mean distance to nearest frontier fell from ~16.1 (early window after frontier exists) to ~2.05 (late).
- Velocity alignment to frontier targets (0.654) exceeds alignment toward boundary audit direction (0.320).
- `particleTargetUses`, `renderUses`, `finalRenderUses` all zero.

## Evidence AGAINST / limits

- **No visuals** — particle rendering, provenance, and migration appearance remain **UNPROVEN**.
- **Single geometry** (Sun-in-1 only); no hostile multi-shape audit (Phase 3.29 still applies to richer mechanics).
- **No hostile validation** of this script; gates are self-checks, not adversarial proof.
- Frontier count jumps from 0 → ~157 at step 1 once votes classify; early step 0 has no frontier (expected cold start).
- `boundaryTargetAlignmentScore` > 0 — some motion correlates with boundary direction audit; must not be read as hidden targeting without further tests.

## Remaining suspicious behaviors

- None flagged by Phase 3.30 gates on this seed/run.
- Phase 3.29 retrospective failures on archived Phase 3.28 metrics are **not** invalidated by this minimal core.

## Likely fake-emergence mechanisms ruled out here (partially)

- Hidden polygon coordinate targets on particles: **not present** in this core.
- Renderer/final geometry use: **zero**.

Not ruled out globally: time-scripted metrics at scale, global abandonment cliffs, full animation theater (not in scope).

## Bottom line

Phase 3.30 **PASS** on its **narrow metrics-only migration claim** for seed `3030`, 72 steps. It is a **tiny executable restart**, not proof of emergent polygon discovery. Treat visuals and full solver honesty as **UNPROVEN** until separately validated.
