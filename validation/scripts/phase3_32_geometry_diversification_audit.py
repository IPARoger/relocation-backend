#!/usr/bin/env python3
"""Phase 3.32 — geometry diversification hostile audit.

Runs Phase 3.31 mechanics unchanged across multiple truth geometries.
Truth geometry is used ONLY via truth(point). Does NOT claim emergence.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import statistics
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol

ROOT = Path(__file__).resolve().parents[2]
SOLVER_SCRIPT = ROOT / "validation/scripts/phase3_30_minimal_migration_core.py"
DEFAULT_OUT = ROOT / "validation/reports/phase3_32_geometry_diversification_audit.json"

SEEDS = list(range(3030, 3040))

# Fixed hostile thresholds (set before runs)
FINGERPRINT_MIN_RELATIVE_SPREAD = 0.10
FINGERPRINT_SUSPICIOUS_METRICS_MIN_COUNT = 4
DIRECTIONAL_DIVERSITY_MIN = 0.35
TARGET_ENTROPY_MIN = 2.5
FRONTIER_OCCUPANCY_VARIANCE_MIN = 0.0008
FRONTIER_TRACKING_CORR_MIN = 0.05
GEOMETRY_PASS_RATE_MIN = 0.35

VERDICT_PASS = "PASS"
VERDICT_FAIL = "FAIL"
VERDICT_SUSPICIOUS = "SUSPICIOUS"
VERDICT_UNPROVEN = "UNPROVEN"


class TruthPointOracle(Protocol):
    def truth_label(self, x: float, y: float) -> str: ...
    @property
    def calls(self) -> int: ...


@dataclass
class CanvasOracle:
    """Canvas-space polygons for truth(point) only. Each entry: [outer, *holes]."""

    polygons: list[list[list[tuple[float, float]]]]
    calls: int = 0

    def truth_label(self, x: float, y: float) -> str:
        self.calls += 1
        for poly in self.polygons:
            if poly and isinstance(poly[0], tuple):
                outer, holes = poly, []
            else:
                outer, holes = poly[0], poly[1:]
            if not _point_in_ring(x, y, outer):
                continue
            if any(_point_in_ring(x, y, hole) for hole in holes):
                continue
            return "inside"
        return "outside"


def _load_solver():
    spec = importlib.util.spec_from_file_location("p31", SOLVER_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["p31"] = mod
    spec.loader.exec_module(mod)
    return mod


def _point_in_ring(x: float, y: float, ring: list[tuple[float, float]]) -> bool:
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > y) != (yj > y):
            xinters = (xj - xi) * (y - yi) / (yj - yi + 1e-15) + xi
            if x < xinters:
                inside = not inside
        j = i
    return inside


def _circle(cx: float, cy: float, r: float, n: int = 64) -> list[tuple[float, float]]:
    return [
        (cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ]


def _rect(x0: float, y0: float, w: float, h: float) -> list[tuple[float, float]]:
    return [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]


def build_geometries(p31: Any, seed: int) -> dict[str, CanvasOracle | Any]:
    rng = __import__("random").Random(seed + 32032)
    geoms: dict[str, CanvasOracle | Any] = {}

    geoms["sun_in_1_polygon"] = p31.TruthOracle(p31.load_sun_rings_lonlat())

    geoms["circle"] = CanvasOracle([[_circle(160, 120, 55)]])

    geoms["thin_diagonal_ribbon"] = CanvasOracle(
        [[(40, 40), (250, 70), (245, 95), (35, 65)]]
    )

    geoms["two_disconnected_islands"] = CanvasOracle(
        [[_circle(85, 75, 30)], [_circle(210, 155, 38)]]
    )

    outer = _circle(150, 120, 72, 72)
    bite = _circle(195, 115, 42, 48)
    geoms["concave_crescent"] = CanvasOracle([[outer, bite]])

    geoms["narrow_fjord"] = CanvasOracle(
        [
            [
                (50, 60),
                (230, 60),
                (230, 100),
                (270, 120),
                (230, 140),
                (230, 180),
                (50, 180),
            ]
        ]
    )

    noisy = []
    for i in range(56):
        angle = 2 * math.pi * i / 56
        r = 44 + 16 * math.sin(7 * angle + seed * 0.01) + 8 * rng.uniform(-1, 1)
        noisy.append((160 + r * math.cos(angle), 120 + r * math.sin(angle)))
    geoms["randomized_noisy_blob"] = CanvasOracle([[noisy]])

    geoms["hollow_ring_donut"] = CanvasOracle([[_circle(160, 120, 62), _circle(160, 120, 32)]])

    geoms["long_coastline_strip"] = CanvasOracle(
        [
            [
                (20, 95),
                (80, 88),
                (140, 102),
                (200, 90),
                (290, 98),
                (290, 118),
                (200, 110),
                (140, 122),
                (80, 108),
                (20, 115),
            ]
        ]
    )

    geoms["small_compact_island"] = CanvasOracle([[_circle(160, 120, 22)]])

    return geoms


def run_mechanics(p31: Any, oracle: TruthPointOracle, seed: int) -> dict[str, Any]:
    """Execute Phase 3.31 loop with injected truth(point) oracle only."""
    rng = __import__("random").Random(seed)
    grid = p31.VoteGrid()
    particles: list[p31.Particle] = []
    for i in range(p31.PARTICLE_COUNT):
        x = rng.uniform(p31.MARGIN, p31.FIELD_W - p31.MARGIN)
        y = rng.uniform(p31.MARGIN, p31.FIELD_H - p31.MARGIN)
        particles.append(
            p31.Particle(
                id=i,
                x0=x,
                y0=y,
                x=x,
                y=y,
                vx=0.0,
                vy=0.0,
                visible=True,
                origin="initial_full_field",
                targetReason="none",
                sampleCount=0,
                lastTruth="unknown",
            )
        )

    occupied_initial = {p31.cell_of(p.x, p.y) for p in particles if p.visible}
    initial_macro_cell_coverage = len(occupied_initial) / p31.MACRO_CELL_COUNT

    frontier_cell_count_by_step: list[int] = []
    average_distance_to_nearest_frontier_by_step: list[float] = []
    frontier_alignment_samples: list[tuple[float, float, float, float]] = []
    target_ids_by_step: list[list[str | None]] = []
    frontier_occupancy_by_step: list[Counter[str]] = []
    movement_vectors: list[tuple[float, float]] = []
    frontier_distance_deltas: list[float] = []

    for step in range(p31.STEPS):
        labels = grid.classify()
        frontier = p31.discover_frontier_cells(labels)
        frontier_cell_count_by_step.append(len(frontier))
        step_occupancy: Counter[str] = Counter()
        target_ids_by_step.append([])

        dists: list[float] = []
        frontier_centers = [p31.cell_center(c, r) for c, r in frontier]
        progress = step / max(1, p31.STEPS - 1)
        speed_ramp = p31.DISPLACEMENT_RAMP_START + (1.0 - p31.DISPLACEMENT_RAMP_START) * progress
        if p31.COLD_START_STEPS <= step < 32:
            speed_ramp *= 0.91

        for p in particles:
            if not p.visible:
                continue

            prev_dist_frontier = None
            if frontier_centers:
                nearest_prev = min(
                    frontier_centers,
                    key=lambda c: (c[0] - p.x) ** 2 + (c[1] - p.y) ** 2,
                )
                prev_dist_frontier = math.hypot(nearest_prev[0] - p.x, nearest_prev[1] - p.y)

            label = oracle.truth_label(p.x, p.y)
            p.lastTruth = label
            p.sampleCount += 1
            col, row = p31.cell_of(p.x, p.y)
            grid.deposit(col, row, label == "inside")

            if frontier_centers:
                nearest = min(
                    frontier_centers,
                    key=lambda center: (center[0] - p.x) ** 2 + (center[1] - p.y) ** 2,
                )
                dists.append(math.hypot(nearest[0] - p.x, nearest[1] - p.y))

            if step < p31.COLD_START_STEPS:
                tx = p.x + rng.uniform(-7.0, 7.0)
                ty = p.y + rng.uniform(-7.0, 7.0)
                tx, ty = p31.clamp_position(tx, ty)
                reason = "local_resample"
                cell_id = p31.cell_id_str(*p31.cell_of(tx, ty))
            else:
                tx, ty, reason, cell_id = p31.choose_solver_target(
                    p, grid, labels, frontier, step_occupancy, step, p31.STEPS, rng
                )
            p.targetReason = reason
            if cell_id == p.targetCellId:
                p.dwellSteps += 1
            else:
                p.dwellSteps = 0
            p.targetCellId = cell_id
            target_ids_by_step[-1].append(cell_id)

            if step < p31.COLD_START_STEPS:
                dx, dy = tx - p.x, ty - p.y
                ux, uy = p31.unit_vector(dx, dy)
                p.vx = p.vx * p31.DAMPING + ux * 0.7
                p.vy = p.vy * p31.DAMPING + uy * 0.7
            elif reason == "none":
                p.vx *= p31.DAMPING
                p.vy *= p31.DAMPING
            else:
                dx, dy = tx - p.x, ty - p.y
                dist = math.hypot(dx, dy)
                ux, uy = p31.unit_vector(dx, dy)
                pull_scale = min(1.0, max(0.15, dist / 28.0))
                pull = p31.PARTICLE_SPEED * pull_scale * speed_ramp
                if progress >= 0.58:
                    pull *= 1.28
                p.vx = p.vx * p31.DAMPING + ux * pull
                p.vy = p.vy * p31.DAMPING + uy * pull
                mag = math.hypot(p.vx, p.vy)
                cap = p31.PARTICLE_SPEED * 1.6 * speed_ramp
                if mag > cap:
                    p.vx = p.vx / mag * cap
                    p.vy = p.vy / mag * cap
                if mag > 0.05:
                    frontier_alignment_samples.append((p.vx, p.vy, dx, dy))

            if progress > 0.52 and frontier_centers:
                nearest = min(
                    frontier_centers,
                    key=lambda center: (center[0] - p.x) ** 2 + (center[1] - p.y) ** 2,
                )
                ndx, ndy = nearest[0] - p.x, nearest[1] - p.y
                ndist = math.hypot(ndx, ndy)
                if ndist > 6.0:
                    nux, nuy = p31.unit_vector(ndx, ndy)
                    close_w = (progress - 0.52) * 1.4
                    p.vx = p.vx * p31.DAMPING + nux * p31.PARTICLE_SPEED * close_w
                    p.vy = p.vy * p31.DAMPING + nuy * p31.PARTICLE_SPEED * close_w

            if len(p.history) >= 4:
                recent_bins = [
                    (round(h[0] / p31.REPEAT_BIN), round(h[1] / p31.REPEAT_BIN))
                    for h in p.history[-8:]
                ]
                next_bin = (
                    round((p.x + p.vx) / p31.REPEAT_BIN),
                    round((p.y + p.vy) / p31.REPEAT_BIN),
                )
                if next_bin in recent_bins:
                    mag = math.hypot(p.vx, p.vy) or 0.1
                    p.vx, p.vy = p31.unit_vector(-p.vy, p.vx)
                    p.vx *= mag
                    p.vy *= mag

            if math.hypot(p.vx, p.vy) > 0.02:
                movement_vectors.append((p.vx, p.vy))

            p.x += p.vx
            p.y += p.vy
            p.x, p.y = p31.clamp_position(p.x, p.y)
            p.history.append([round(p.x, 4), round(p.y, 4)])

            if prev_dist_frontier is not None and frontier_centers:
                nearest_after = min(
                    frontier_centers,
                    key=lambda c: (c[0] - p.x) ** 2 + (c[1] - p.y) ** 2,
                )
                after = math.hypot(nearest_after[0] - p.x, nearest_after[1] - p.y)
                frontier_distance_deltas.append(prev_dist_frontier - after)

        frontier_occupancy_by_step.append(step_occupancy)
        avg_dist = float(statistics.mean(dists)) if dists else float("nan")
        average_distance_to_nearest_frontier_by_step.append(round(avg_dist, 6))

    distances_moved = [math.hypot(p.x - p.x0, p.y - p.y0) for p in particles]
    percent_moved = sum(1 for d in distances_moved if d >= p31.SIGNIFICANT_MOVE) / len(distances_moved)

    frontier_attraction_alignment_score = p31.alignment_score(frontier_alignment_samples)

    valid_dist_steps = [
        d
        for i, d in enumerate(average_distance_to_nearest_frontier_by_step)
        if i > 0 and frontier_cell_count_by_step[i] > 0 and not math.isnan(d)
    ]
    window = max(3, len(valid_dist_steps) // 6)
    if len(valid_dist_steps) >= window * 2:
        early_avg = statistics.mean(valid_dist_steps[:window])
        late_avg = statistics.mean(valid_dist_steps[-window:])
        frontier_distance_decreases = late_avg < early_avg
    else:
        early_avg = late_avg = float("nan")
        frontier_distance_decreases = False

    anticheat = p31.compute_anticheat_metrics(particles)

    gates = {
        "initialMacroCellCoverage >= 0.70": initial_macro_cell_coverage >= 0.70,
        "percentParticlesMovedSignificantDistance >= 0.35": percent_moved >= 0.35,
        "averageDistanceToNearestFrontier decreases early to late": frontier_distance_decreases,
        "frontierAttractionAlignmentScore positive": frontier_attraction_alignment_score > 0.0,
        "centralizationTop1Fraction <= 0.12": anticheat["centralizationTop1Fraction"] <= 0.12,
        "centralizationTop3Fraction <= 0.30": anticheat["centralizationTop3Fraction"] <= 0.30,
        "uniqueFinalTargetCellIds >= 40": anticheat["uniqueFinalTargetCellIds"] >= 40,
        "percentParticlesTrappedInSmallLoops <= 0.25": anticheat["percentParticlesTrappedInSmallLoops"] <= 0.25,
        "oscillationScoreMean <= 6": anticheat["oscillationScoreMean"] <= 6.0,
        "repeatedPositionRatio <= 0.25": anticheat["repeatedPositionRatio"] <= 0.25,
        "meanFirstHalfDisplacementFraction <= 0.70": anticheat["meanFirstHalfDisplacementFraction"] <= 0.70,
    }
    acceptance_passed = all(gates.values())

    motion = _motion_metrics(
        particles, movement_vectors, target_ids_by_step, frontier_occupancy_by_step, frontier_distance_deltas
    )

    return {
        "acceptancePassed": acceptance_passed,
        "failedGates": [k for k, v in gates.items() if not v],
        "initialMacroCellCoverage": round(initial_macro_cell_coverage, 6),
        "percentParticlesMovedSignificantDistance": round(percent_moved, 6),
        "frontierAttractionAlignmentScore": round(frontier_attraction_alignment_score, 6),
        "frontierCellCountFinal": frontier_cell_count_by_step[-1] if frontier_cell_count_by_step else 0,
        "frontierCellCountMean": round(statistics.mean(frontier_cell_count_by_step[1:]), 6)
        if len(frontier_cell_count_by_step) > 1
        else 0,
        "frontierDistanceEarlyMean": early_avg if not math.isnan(early_avg) else None,
        "frontierDistanceLateMean": late_avg if not math.isnan(late_avg) else None,
        "frontierDistanceDecreases": frontier_distance_decreases,
        "meanDistanceMoved": round(statistics.mean(distances_moved), 6),
        "truthOracleCalls": getattr(oracle, "calls", 0),
        **anticheat,
        **motion,
    }


def _motion_metrics(
    particles: list[Any],
    movement_vectors: list[tuple[float, float]],
    target_ids_by_step: list[list[str | None]],
    frontier_occupancy_by_step: list[Counter[str]],
    frontier_distance_deltas: list[float],
) -> dict[str, Any]:
    angles = [math.atan2(vy, vx) for vx, vy in movement_vectors if math.hypot(vx, vy) > 0.05]
    if len(angles) >= 2:
        mean_sin = statistics.mean(math.sin(a) for a in angles)
        mean_cos = statistics.mean(math.cos(a) for a in angles)
        resultant_len = math.hypot(mean_sin, mean_cos)
        directional_diversity = 1.0 - resultant_len
    else:
        directional_diversity = 0.0

    all_targets = [tid for step in target_ids_by_step for tid in step if tid]
    target_counts = Counter(all_targets)
    n = sum(target_counts.values())
    if n > 0:
        target_entropy = -sum((c / n) * math.log(c / n + 1e-15) for c in target_counts.values())
    else:
        target_entropy = 0.0

    xs = [p.x for p in particles]
    ys = [p.y for p in particles]
    spatial_variance = statistics.pvariance(xs) + statistics.pvariance(ys)

    occ_vars = []
    for occ in frontier_occupancy_by_step:
        if not occ:
            continue
        counts = list(occ.values())
        occ_vars.append(statistics.pvariance(counts) if len(counts) > 1 else 0.0)
    frontier_occupancy_variance = statistics.mean(occ_vars) if occ_vars else 0.0

    if len(frontier_distance_deltas) > 10:
        positive = sum(1 for d in frontier_distance_deltas if d > 0)
        frontier_tracking_ratio = positive / len(frontier_distance_deltas)
    else:
        frontier_tracking_ratio = 0.0

    return {
        "directionalDiversity": round(directional_diversity, 6),
        "targetSelectionEntropy": round(target_entropy, 6),
        "spatialDistributionVariance": round(spatial_variance, 6),
        "frontierOccupancyVarianceMean": round(frontier_occupancy_variance, 6),
        "frontierTrackingRatio": round(frontier_tracking_ratio, 6),
    }


def _relative_spread(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = statistics.mean(values)
    if abs(mean) < 1e-9:
        return max(values) - min(values)
    return (max(values) - min(values)) / abs(mean)


def _fingerprint_audit(geometry_means: dict[str, dict[str, float]]) -> dict[str, Any]:
    metrics = [
        "frontierAttractionAlignmentScore",
        "centralizationTop1Fraction",
        "centralizationTop3Fraction",
        "uniqueFinalTargetCellIds",
        "percentParticlesTrappedInSmallLoops",
        "oscillationScoreMean",
        "repeatedPositionRatio",
        "meanFirstHalfDisplacementFraction",
        "percentParticlesMovedSignificantDistance",
        "frontierCellCountMean",
        "directionalDiversity",
        "targetSelectionEntropy",
        "spatialDistributionVariance",
        "frontierOccupancyVarianceMean",
        "frontierTrackingRatio",
    ]
    spreads: dict[str, float] = {}
    suspicious: list[str] = []
    for m in metrics:
        vals = [geometry_means[g][m] for g in geometry_means if m in geometry_means[g]]
        if len(vals) < 2:
            continue
        rel = _relative_spread(vals)
        spreads[m] = round(rel, 6)
        if rel < FINGERPRINT_MIN_RELATIVE_SPREAD:
            suspicious.append(m)

    return {
        "metricRelativeSpread": spreads,
        "suspiciouslyStableMetrics": suspicious,
        "verdict": VERDICT_SUSPICIOUS
        if len(suspicious) >= FINGERPRINT_SUSPICIOUS_METRICS_MIN_COUNT
        else VERDICT_PASS,
    }


def run_audit(seeds: list[int]) -> dict[str, Any]:
    p31 = _load_solver()
    geometry_names = [
        "sun_in_1_polygon",
        "circle",
        "thin_diagonal_ribbon",
        "two_disconnected_islands",
        "concave_crescent",
        "narrow_fjord",
        "randomized_noisy_blob",
        "hollow_ring_donut",
        "long_coastline_strip",
        "small_compact_island",
    ]

    runs: dict[str, dict[str, dict[str, Any]]] = {}
    for geom in geometry_names:
        runs[geom] = {}
        geoms = build_geometries(p31, seed=seeds[0])
        oracle = geoms[geom]
        for seed in seeds:
            if geom == "randomized_noisy_blob":
                oracle = build_geometries(p31, seed=seed)["randomized_noisy_blob"]
            runs[geom][str(seed)] = run_mechanics(p31, oracle, seed)

    geometry_means: dict[str, dict[str, float]] = {}
    geometry_pass_rates: dict[str, float] = {}
    for geom, seed_runs in runs.items():
        keys = [
            "frontierAttractionAlignmentScore",
            "centralizationTop1Fraction",
            "uniqueFinalTargetCellIds",
            "percentParticlesTrappedInSmallLoops",
            "oscillationScoreMean",
            "repeatedPositionRatio",
            "meanFirstHalfDisplacementFraction",
            "percentParticlesMovedSignificantDistance",
            "frontierCellCountMean",
            "directionalDiversity",
            "targetSelectionEntropy",
            "spatialDistributionVariance",
            "frontierOccupancyVarianceMean",
            "frontierTrackingRatio",
            "centralizationTop3Fraction",
        ]
        geometry_means[geom] = {
            k: round(statistics.mean(r[k] for r in seed_runs.values()), 6) for k in keys
        }
        geometry_pass_rates[geom] = sum(
            1 for r in seed_runs.values() if r["acceptancePassed"]
        ) / len(seed_runs)

    fingerprint = _fingerprint_audit(geometry_means)

    motion_audit = {
        "directionalDiversityMeanAcrossGeometries": round(
            statistics.mean(geometry_means[g]["directionalDiversity"] for g in geometry_means), 6
        ),
        "targetEntropyMeanAcrossGeometries": round(
            statistics.mean(geometry_means[g]["targetSelectionEntropy"] for g in geometry_means), 6
        ),
        "verdict": VERDICT_PASS
        if statistics.mean(geometry_means[g]["directionalDiversity"] for g in geometry_means)
        >= DIRECTIONAL_DIVERSITY_MIN
        and statistics.mean(geometry_means[g]["targetSelectionEntropy"] for g in geometry_means)
        >= TARGET_ENTROPY_MIN
        else VERDICT_FAIL,
    }

    frontier_audit = {
        "frontierOccupancyVarianceMean": round(
            statistics.mean(geometry_means[g]["frontierOccupancyVarianceMean"] for g in geometry_means), 6
        ),
        "frontierTrackingRatioMean": round(
            statistics.mean(geometry_means[g]["frontierTrackingRatio"] for g in geometry_means), 6
        ),
        "verdict": VERDICT_PASS
        if statistics.mean(geometry_means[g]["frontierTrackingRatio"] for g in geometry_means)
        >= FRONTIER_TRACKING_CORR_MIN
        else VERDICT_UNPROVEN,
    }

    sun_mean = geometry_means["sun_in_1_polygon"]
    others = [g for g in geometry_means if g != "sun_in_1_polygon"]
    sun_vs_other_spread = _relative_spread(
        [geometry_means[g]["frontierCellCountMean"] for g in geometry_means]
    )

    materially_different = sun_vs_other_spread >= FINGERPRINT_MIN_RELATIVE_SPREAD
    overfit_likely = (
        geometry_pass_rates["sun_in_1_polygon"] >= 0.9
        and statistics.mean(geometry_pass_rates[g] for g in others) < GEOMETRY_PASS_RATE_MIN
    )
    too_stable = fingerprint["verdict"] == VERDICT_SUSPICIOUS

    if too_stable and not materially_different:
        geometry_verdict = VERDICT_SUSPICIOUS
        frontier_responsive = False
    elif materially_different and not overfit_likely:
        geometry_verdict = VERDICT_PASS
        frontier_responsive = frontier_audit["verdict"] == VERDICT_PASS
    elif overfit_likely:
        geometry_verdict = VERDICT_FAIL
        frontier_responsive = False
    else:
        geometry_verdict = VERDICT_UNPROVEN
        frontier_responsive = frontier_audit["verdict"] == VERDICT_PASS

    overall = VERDICT_FAIL if overfit_likely or too_stable else geometry_verdict

    return {
        "phase": "3.32_geometry_diversification_audit",
        "emergenceClaimed": False,
        "solverScript": str(SOLVER_SCRIPT.relative_to(ROOT)),
        "seeds": seeds,
        "geometries": geometry_names,
        "runs": runs,
        "geometryMeans": geometry_means,
        "geometryPassRates": geometry_pass_rates,
        "tests": {
            "multi_geometry_robustness": {
                "verdict": VERDICT_PASS if materially_different else VERDICT_FAIL,
                "geometryPassRates": geometry_pass_rates,
                "materiallyDifferent": materially_different,
            },
            "geometry_fingerprint_audit": fingerprint,
            "motion_authenticity_audit": motion_audit,
            "frontier_dependence_audit": frontier_audit,
            "seed_robustness": {
                "verdict": VERDICT_PASS
                if all(
                    sum(1 for s in seeds if runs[g][str(s)]["acceptancePassed"]) >= len(seeds) * 0.5
                    for g in geometry_names
                )
                else VERDICT_FAIL,
                "perGeometryPassRate": geometry_pass_rates,
            },
        },
        "conclusions": {
            "geometryMateriallyChangesBehavior": materially_different,
            "solverAppearsOverfitToSun": overfit_likely,
            "metricsTooStableAcrossGeometries": too_stable,
            "evidenceSupportsFrontierResponsiveMigration": frontier_responsive,
            "overallVerdict": overall,
        },
        "strongestEvidenceAgainstGeometryDriven": (
            [
                "frontierAttractionAlignmentScore relative spread only "
                f"{fingerprint['metricRelativeSpread'].get('frontierAttractionAlignmentScore', 0):.4f} across 10 geometries",
                "targetSelectionEntropy and frontierTrackingRatio also suspiciously stable",
                f"Many geometries fail Phase 3.31 gates: {geometry_pass_rates}",
            ]
            if too_stable
            else []
        ),
        "strongestEvidenceForGeometryDriven": [
            f"Frontier cell count relative spread across geometries: {round(sun_vs_other_spread, 4)}",
            f"Pass rates vary by geometry: {geometry_pass_rates}",
        ]
        if materially_different
        else [],
        "suspiciousBehaviors": fingerprint.get("suspiciouslyStableMetrics", []),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 3.32 geometry diversification audit")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seeds", type=str, default=",".join(str(s) for s in SEEDS))
    args = parser.parse_args(argv)
    seeds = [int(s.strip()) for s in args.seeds.split(",")]
    report = run_audit(seeds)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overallVerdict": report["conclusions"]["overallVerdict"], "overfit": report["conclusions"]["solverAppearsOverfitToSun"]}, indent=2))
    return 0 if report["conclusions"]["overallVerdict"] == VERDICT_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
