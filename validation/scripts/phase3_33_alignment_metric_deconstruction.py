#!/usr/bin/env python3
"""Phase 3.33 — frontierAttractionAlignmentScore hostile deconstruction.

Measurement accountability only. Does NOT patch the solver. Does NOT claim emergence.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SOLVER_SCRIPT = ROOT / "validation/scripts/phase3_30_minimal_migration_core.py"
P32_SCRIPT = ROOT / "validation/scripts/phase3_32_geometry_diversification_audit.py"
P32_REPORT = ROOT / "validation/reports/phase3_32_geometry_diversification_audit.json"
DEFAULT_OUT = ROOT / "validation/reports/phase3_33_alignment_metric_deconstruction.json"

SEEDS = list(range(3030, 3040))
GEOMETRIES = [
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

FIELD_CENTER = (160.0, 120.0)

# Fixed hostile thresholds (before runs)
GEOMETRY_SENSITIVE_MIN_SPREAD = 0.10
REPORTED_VS_RANDOM_MIN_GAP = 0.12
REPORTED_VS_CENTER_MAX_CORR = 0.98
REDUNDANCY_CORR_THRESHOLD = 0.97
NEAREST_FRONTIER_MIN_MEAN_ALIGNMENT = 0.15
TAUTOLOGY_CORR_MAX = 1.0 - 1e-6

VERDICT_PASS = "PASS"
VERDICT_FAIL = "FAIL"
VERDICT_UNPROVEN = "UNPROVEN"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _nearest_on_segment(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
    dx = x2 - x1
    dy = y2 - y1
    len2 = dx * dx + dy * dy
    if len2 < 1e-12:
        return x1, y1
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / len2))
    return x1 + t * dx, y1 + t * dy


def audit_boundary_vector(p31: Any, oracle: Any, x: float, y: float) -> tuple[float, float]:
    """Audit-only boundary direction; not used for particle targets."""
    if hasattr(oracle, "audit_nearest_boundary_point"):
        bx, by = oracle.audit_nearest_boundary_point(x, y)
        return bx - x, by - y
    if hasattr(oracle, "polygons"):
        ring = oracle.polygons[0]
        if ring and isinstance(ring[0], tuple):
            outer = ring
        else:
            outer = ring[0]
        best = outer[0]
        best_d2 = math.inf
        n = len(outer)
        for i in range(n):
            x1, y1 = outer[i]
            x2, y2 = outer[(i + 1) % n]
            px, py = _nearest_on_segment(x, y, x1, y1, x2, y2)
            d2 = (px - x) ** 2 + (py - y) ** 2
            if d2 < best_d2:
                best_d2 = d2
                best = (px, py)
        return best[0] - x, best[1] - y
    return 0.0, 0.0


def run_deconstruction(p31: Any, p32: Any, oracle: Any, seed: int) -> dict[str, Any]:
    rng = __import__("random").Random(seed)
    rng_random = __import__("random").Random(seed + 33033)
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

    sample_buckets: dict[str, list[tuple[float, float, float, float]]] = {
        "frontierAttractionAlignmentScore_reported": [],
        "chosen_target_pull": [],
        "nearest_frontier_direction": [],
        "random_steering_baseline": [],
        "displacement_from_initial": [],
        "center_pull_baseline": [],
        "boundary_normal_audit": [],
        "final_target_cell_direction": [],
    }

    for step in range(p31.STEPS):
        labels = grid.classify()
        frontier = p31.discover_frontier_cells(labels)
        step_occupancy: Counter[str] = Counter()
        frontier_centers = [p31.cell_center(c, r) for c, r in frontier]
        progress = step / max(1, p31.STEPS - 1)
        speed_ramp = p31.DISPLACEMENT_RAMP_START + (1.0 - p31.DISPLACEMENT_RAMP_START) * progress
        if p31.COLD_START_STEPS <= step < 32:
            speed_ramp *= 0.91

        for p in particles:
            if not p.visible:
                continue
            p.lastTruth = oracle.truth_label(p.x, p.y)
            col, row = p31.cell_of(p.x, p.y)
            grid.deposit(col, row, p.lastTruth == "inside")

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

                mag = math.hypot(p.vx, p.vy)
                if mag > 0.05 and step >= p31.COLD_START_STEPS and reason != "none":
                    target_dx, target_dy = tx - p.x, ty - p.y
                    sample_buckets["frontierAttractionAlignmentScore_reported"].append(
                        (p.vx, p.vy, target_dx, target_dy)
                    )
                    sample_buckets["chosen_target_pull"].append((p.vx, p.vy, target_dx, target_dy))
                    if frontier_centers:
                        nf = min(
                            frontier_centers,
                            key=lambda c: (c[0] - p.x) ** 2 + (c[1] - p.y) ** 2,
                        )
                        sample_buckets["nearest_frontier_direction"].append(
                            (p.vx, p.vy, nf[0] - p.x, nf[1] - p.y)
                        )
                    rdx = rng_random.uniform(-1.0, 1.0)
                    rdy = rng_random.uniform(-1.0, 1.0)
                    sample_buckets["random_steering_baseline"].append((p.vx, p.vy, rdx, rdy))
                    sample_buckets["displacement_from_initial"].append(
                        (p.vx, p.vy, p.x - p.x0, p.y - p.y0)
                    )
                    sample_buckets["center_pull_baseline"].append(
                        (p.vx, p.vy, FIELD_CENTER[0] - p.x, FIELD_CENTER[1] - p.y)
                    )
                    bdx, bdy = audit_boundary_vector(p31, oracle, p.x, p.y)
                    sample_buckets["boundary_normal_audit"].append((p.vx, p.vy, bdx, bdy))

            if progress > 0.52 and frontier_centers:
                nearest = min(
                    frontier_centers,
                    key=lambda c: (c[0] - p.x) ** 2 + (c[1] - p.y) ** 2,
                )
                ndx, ndy = nearest[0] - p.x, nearest[1] - p.y
                if math.hypot(ndx, ndy) > 6.0:
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

            p.x += p.vx
            p.y += p.vy
            p.x, p.y = p31.clamp_position(p.x, p.y)
            p.history.append([round(p.x, 4), round(p.y, 4)])

    for p in particles:
        if not p.targetCellId:
            continue
        cc, cr = (int(x) for x in p.targetCellId.split(","))
        tcx, tcy = p31.cell_center(cc, cr)
        mag = math.hypot(p.vx, p.vy)
        if mag > 0.05:
            sample_buckets["final_target_cell_direction"].append(
                (p.vx, p.vy, tcx - p.x, tcy - p.y)
            )

    scores = {k: p31.alignment_score(v) for k, v in sample_buckets.items()}
    scores["sampleCounts"] = {k: len(v) for k, v in sample_buckets.items()}
    return scores


def _relative_spread(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = statistics.mean(values)
    if abs(mean) < 1e-9:
        return max(values) - min(values)
    return (max(values) - min(values)) / abs(mean)


def _pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return float("nan")
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    if denx < 1e-12 or deny < 1e-12:
        return float("nan")
    return num / (denx * deny)


def compute_frontier_migration_evidence(
    *,
    redundant_with_target_pull: bool,
    geometry_insensitive: bool,
    nearest_frontier_mean: float,
    reported_spread: float,
    nearest_spread: float,
) -> dict[str, Any]:
    """Phase 3.34 rule: all three conditions required for true."""
    not_tautological = not redundant_with_target_pull
    geometry_sensitive = not geometry_insensitive
    nearest_materially_positive = nearest_frontier_mean >= NEAREST_FRONTIER_MIN_MEAN_ALIGNMENT

    supported = not_tautological and geometry_sensitive and nearest_materially_positive
    return {
        "evidenceSupportsFrontierResponsiveMigration": supported,
        "conditions": {
            "notTautologicalWithChosenTargetPull": not_tautological,
            "reportedMetricGeometrySensitive": geometry_sensitive,
            "nearestFrontierMateriallyPositive": nearest_materially_positive,
        },
        "values": {
            "nearestFrontierMeanAlignment": round(nearest_frontier_mean, 6),
            "nearestFrontierMinRequired": NEAREST_FRONTIER_MIN_MEAN_ALIGNMENT,
            "reportedRelativeSpread": reported_spread,
            "nearestFrontierRelativeSpread": nearest_spread,
        },
    }


def build_conclusions(
    geometry_means: dict[str, dict[str, float]],
    spreads: dict[str, float],
    cross_metric_corr: dict[str, float],
    p32_reported_spread: float | None,
) -> dict[str, Any]:
    reported = "frontierAttractionAlignmentScore_reported"
    chosen = "chosen_target_pull"
    nearest = "nearest_frontier_direction"
    random_m = "random_steering_baseline"
    center_m = "center_pull_baseline"
    geom_names = GEOMETRIES

    reported_spread = spreads[reported]
    nearest_spread = spreads[nearest]
    random_mean = statistics.mean(geometry_means[g][random_m] for g in geom_names)
    reported_mean = statistics.mean(geometry_means[g][reported] for g in geom_names)
    nearest_mean = statistics.mean(geometry_means[g][nearest] for g in geom_names)
    gap_vs_random = reported_mean - random_mean

    corr_reported_chosen = cross_metric_corr.get(f"{reported}__{chosen}", 1.0)
    corr_reported_center = _pearson(
        [geometry_means[g][reported] for g in geom_names],
        [geometry_means[g][center_m] for g in geom_names],
    )

    redundant_with_target_pull = abs(corr_reported_chosen - 1.0) < TAUTOLOGY_CORR_MAX
    geometry_insensitive = reported_spread < GEOMETRY_SENSITIVE_MIN_SPREAD
    nearest_more_sensitive = nearest_spread > reported_spread * 1.5

    if redundant_with_target_pull and geometry_insensitive:
        metric_verdict = VERDICT_FAIL
        recommendation = "RETIRE_or_RENAME"
        rationale = (
            "frontierAttractionAlignmentScore is tautologically identical to chosen-target "
            "pull alignment and shows negligible cross-geometry spread (~3-4%). "
            "It measures generic solver steering toward selected grid cells, not frontier geometry."
        )
    elif geometry_insensitive:
        metric_verdict = VERDICT_FAIL
        recommendation = "RENAME_and_SPLIT"
        rationale = "Metric is positive but geometry-insensitive; retain nearest-frontier metric separately."
    else:
        metric_verdict = VERDICT_UNPROVEN
        recommendation = "RETAIN_with_rename"
        rationale = "Insufficient evidence for PASS; needs further hostile instrumentation."

    migration_evidence = compute_frontier_migration_evidence(
        redundant_with_target_pull=redundant_with_target_pull,
        geometry_insensitive=geometry_insensitive,
        nearest_frontier_mean=nearest_mean,
        reported_spread=reported_spread,
        nearest_spread=nearest_spread,
    )

    return {
        "frontierAttractionAlignmentScoreVerdict": metric_verdict,
        "metricRecommendation": recommendation,
        "rationale": rationale,
        "isMetricTheater": geometry_insensitive and redundant_with_target_pull,
        "tracksGenericTargetPull": redundant_with_target_pull,
        "distinguishesGeometryBetterThanRandom": gap_vs_random >= REPORTED_VS_RANDOM_MIN_GAP,
        "distinguishesGeometryBetterThanCenter": abs(corr_reported_center) < REPORTED_VS_CENTER_MAX_CORR,
        **migration_evidence,
        "comparisons": {
            "reportedMeanAcrossGeometries": round(reported_mean, 6),
            "randomBaselineMeanAcrossGeometries": round(random_mean, 6),
            "reportedMinusRandomMean": round(gap_vs_random, 6),
            "reportedRelativeSpread": reported_spread,
            "nearestFrontierRelativeSpread": nearest_spread,
            "phase32ReportedRelativeSpread": p32_reported_spread,
            "corrReportedVsChosenTargetPull": corr_reported_chosen,
            "corrReportedVsNearestFrontier": round(
                _pearson(
                    [geometry_means[g][reported] for g in geom_names],
                    [geometry_means[g][nearest] for g in geom_names],
                ),
                6,
            ),
            "corrReportedVsCenterPull": round(corr_reported_center, 6),
            "redundantWithChosenTargetPull": redundant_with_target_pull,
            "geometryInsensitive": geometry_insensitive,
            "nearestFrontierMoreGeometrySensitive": nearest_more_sensitive,
        },
        "tests": {
            "tautology_check": {
                "verdict": VERDICT_FAIL if redundant_with_target_pull else VERDICT_PASS,
                "corrReportedChosen": corr_reported_chosen,
            },
            "geometry_sensitivity_check": {
                "verdict": VERDICT_FAIL if geometry_insensitive else VERDICT_PASS,
                "reportedSpread": reported_spread,
                "threshold": GEOMETRY_SENSITIVE_MIN_SPREAD,
            },
            "random_baseline_check": {
                "verdict": VERDICT_PASS if gap_vs_random >= REPORTED_VS_RANDOM_MIN_GAP else VERDICT_FAIL,
                "gap": round(gap_vs_random, 6),
            },
            "center_pull_redundancy_check": {
                "verdict": VERDICT_FAIL
                if abs(corr_reported_center) > REPORTED_VS_CENTER_MAX_CORR
                else VERDICT_PASS,
                "correlation": round(corr_reported_center, 6),
            },
            "frontier_migration_evidence_check": {
                "verdict": VERDICT_PASS if migration_evidence["evidenceSupportsFrontierResponsiveMigration"] else VERDICT_FAIL,
                "conditions": migration_evidence["conditions"],
                "values": migration_evidence["values"],
            },
        },
    }


def contradiction_audit_prior_bug() -> dict[str, Any]:
    return {
        "phase": "3.34_report_integrity_correction",
        "priorFieldWrong": True,
        "priorValue": True,
        "correctedValue": False,
        "whyPriorWasWrong": (
            "evidenceSupportsFrontierResponsiveMigration was set to "
            "(nearestFrontierRelativeSpread >= GEOMETRY_SENSITIVE_MIN_SPREAD). "
            "High relative spread around a near-zero mean (~0.03) was mistaken for "
            "positive frontier-directional migration evidence."
        ),
        "controllingRule": (
            "Field is true only when ALL hold: (1) reported metric not tautological with "
            "chosen target pull, (2) reported metric geometry-sensitive (relative spread >= "
            f"{GEOMETRY_SENSITIVE_MIN_SPREAD}), (3) nearest-frontier mean alignment >= "
            f"{NEAREST_FRONTIER_MIN_MEAN_ALIGNMENT}."
        ),
    }


def run_audit(seeds: list[int]) -> dict[str, Any]:
    p31 = _load_module(SOLVER_SCRIPT, "p31")
    p32 = _load_module(P32_SCRIPT, "p32")

    per_run: dict[str, dict[str, dict[str, Any]]] = {}
    for geom in GEOMETRIES:
        per_run[geom] = {}
        for seed in seeds:
            geoms = p32.build_geometries(p31, seed=seed)
            oracle = geoms[geom]
            per_run[geom][str(seed)] = run_deconstruction(p31, p32, oracle, seed)

    geometry_means: dict[str, dict[str, float]] = {}
    for geom in GEOMETRIES:
        keys = [
            "frontierAttractionAlignmentScore_reported",
            "chosen_target_pull",
            "nearest_frontier_direction",
            "random_steering_baseline",
            "displacement_from_initial",
            "center_pull_baseline",
            "boundary_normal_audit",
            "final_target_cell_direction",
        ]
        geometry_means[geom] = {
            k: round(
                statistics.mean(per_run[geom][str(s)][k] for s in seeds),
                6,
            )
            for k in keys
        }

    metric_keys = list(next(iter(geometry_means.values())).keys())
    spreads = {m: round(_relative_spread([geometry_means[g][m] for g in GEOMETRIES]), 6) for m in metric_keys}

    geom_names = GEOMETRIES
    cross_metric_corr: dict[str, float] = {}
    for i, a in enumerate(metric_keys):
        for b in metric_keys[i + 1 :]:
            xs = [geometry_means[g][a] for g in geom_names]
            ys = [geometry_means[g][b] for g in geom_names]
            cross_metric_corr[f"{a}__{b}"] = round(_pearson(xs, ys), 6)

    p32_reported_spread = None
    if P32_REPORT.exists():
        p32_data = json.loads(P32_REPORT.read_text(encoding="utf-8"))
        p32_spreads = p32_data.get("tests", {}).get("geometry_fingerprint_audit", {}).get(
            "metricRelativeSpread", {}
        )
        p32_reported_spread = p32_spreads.get("frontierAttractionAlignmentScore")

    built = build_conclusions(geometry_means, spreads, cross_metric_corr, p32_reported_spread)
    comparisons = built.pop("comparisons")
    tests = built.pop("tests")

    return {
        "phase": "3.33_alignment_metric_deconstruction",
        "emergenceClaimed": False,
        "solverScript": str(SOLVER_SCRIPT.relative_to(ROOT)),
        "phase32ReportReference": str(P32_REPORT.relative_to(ROOT)),
        "seeds": seeds,
        "geometries": GEOMETRIES,
        "perRunScores": per_run,
        "geometryMeans": geometry_means,
        "metricRelativeSpread": spreads,
        "crossGeometryMetricCorrelation": cross_metric_corr,
        "comparisons": comparisons,
        "tests": tests,
        "conclusions": {k: v for k, v in built.items() if k not in ("conditions", "values")},
        "frontierMigrationEvidence": {
            "conditions": built.get("conditions", {}),
            "values": built.get("values", {}),
        },
        "contradictionAudit": contradiction_audit_prior_bug(),
    }


def recompute_report_integrity(report: dict[str, Any]) -> dict[str, Any]:
    """Phase 3.34: fix conclusions from existing per-run data without re-simulating."""
    geometry_means = report["geometryMeans"]
    spreads = report["metricRelativeSpread"]
    cross_metric_corr = report["crossGeometryMetricCorrelation"]
    p32_spread = report.get("comparisons", {}).get("phase32ReportedRelativeSpread")
    built = build_conclusions(geometry_means, spreads, cross_metric_corr, p32_spread)
    comparisons = built.pop("comparisons")
    tests = built.pop("tests")
    report["comparisons"] = comparisons
    report["tests"] = tests
    report["conclusions"] = {k: v for k, v in built.items() if k not in ("conditions", "values")}
    report["frontierMigrationEvidence"] = {
        "conditions": built.get("conditions", {}),
        "values": built.get("values", {}),
    }
    report["contradictionAudit"] = contradiction_audit_prior_bug()
    report["reportIntegrityCorrection"] = "3.34"
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 3.33 alignment deconstruction")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seeds", type=str, default=",".join(str(s) for s in SEEDS))
    parser.add_argument(
        "--recompute-integrity-only",
        type=Path,
        default=None,
        help="Phase 3.34: patch conclusions from existing JSON (no re-simulation)",
    )
    args = parser.parse_args(argv)
    if args.recompute_integrity_only:
        report = recompute_report_integrity(
            json.loads(args.recompute_integrity_only.read_text(encoding="utf-8"))
        )
    else:
        seeds = [int(s.strip()) for s in args.seeds.split(",")]
        report = run_audit(seeds)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verdict": report["conclusions"]["frontierAttractionAlignmentScoreVerdict"],
                "recommendation": report["conclusions"]["metricRecommendation"],
                "evidenceSupportsFrontierResponsiveMigration": report["conclusions"][
                    "evidenceSupportsFrontierResponsiveMigration"
                ],
            },
            indent=2,
        )
    )
    return 0 if report["conclusions"]["frontierAttractionAlignmentScoreVerdict"] == VERDICT_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
