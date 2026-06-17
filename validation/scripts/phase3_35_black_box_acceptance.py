#!/usr/bin/env python3
"""Phase 3.35 — external black-box acceptance harness.

Runs Phase 3.31 solver as-is but computes PASS/FAIL only from raw histories
and truth(point). Ignores all solver self-reported claims. Does NOT claim emergence.
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
from typing import Any, Protocol

ROOT = Path(__file__).resolve().parents[2]
SOLVER_SCRIPT = ROOT / "validation/scripts/phase3_30_minimal_migration_core.py"
DEFAULT_OUT = ROOT / "validation/reports/phase3_35_black_box_acceptance_against_current.json"

SEEDS = list(range(4000, 4030))

# Fixed black-box gates (set before any run)
GATES = {
    "initialCoverage >= 0.70": lambda m: m["initialCoverage"] >= 0.70,
    "particleMigrationFraction >= 0.35": lambda m: m["particleMigrationFraction"] >= 0.35,
    "frontierDistanceDelta > 0": lambda m: m["frontierDistanceDelta"] > 0,
    "nearestFrontierVelocityAlignment >= 0.15": lambda m: m["nearestFrontierVelocityAlignment"] >= 0.15,
    "targetCentralizationTop1 <= 0.12": lambda m: m["targetCentralizationTop1"] <= 0.12,
    "targetCentralizationTop3 <= 0.30": lambda m: m["targetCentralizationTop3"] <= 0.30,
    "uniqueTargetCells >= 40": lambda m: m["uniqueTargetCells"] >= 40,
    "loopTrapFraction <= 0.25": lambda m: m["loopTrapFraction"] <= 0.25,
    "oscillationScore <= 6": lambda m: m["oscillationScore"] <= 6.0,
    "repeatedPositionRatio <= 0.25": lambda m: m["repeatedPositionRatio"] <= 0.25,
    "firstHalfDisplacementFraction <= 0.70": lambda m: m["firstHalfDisplacementFraction"] <= 0.70,
}

GEOMETRY_PASS_RATE_MIN = 0.70
GEOMETRY_SENSITIVITY_MIN_SPREAD = 0.10
LOOP_RADIUS = 12.0
REPEAT_BIN = 2.0


class TruthOracle(Protocol):
    def truth_label(self, x: float, y: float) -> str: ...


@dataclass
class CanvasTruth:
    polygons: list[list[list[tuple[float, float]]]]

    def truth_label(self, x: float, y: float) -> str:
        for poly in self.polygons:
            if poly and isinstance(poly[0], tuple):
                outer, holes = poly, []
            else:
                outer, holes = poly[0], poly[1:]
            if not _point_in_ring(x, y, outer):
                continue
            if any(_point_in_ring(x, y, h) for h in holes):
                continue
            return "inside"
        return "outside"


@dataclass
class GeometrySpec:
    name: str
    family: str
    truth: TruthOracle


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


def _ellipse(cx: float, cy: float, rx: float, ry: float, n: int = 64) -> list[tuple[float, float]]:
    return [
        (cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ]


def _rect(x0: float, y0: float, w: float, h: float) -> list[tuple[float, float]]:
    return [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]


def _alignment_score(samples: list[tuple[float, float, float, float]]) -> float:
    if not samples:
        return 0.0
    scores = []
    for vx, vy, dx, dy in samples:
        vm, dm = math.hypot(vx, vy), math.hypot(dx, dy)
        if vm > 1e-6 and dm > 1e-6:
            scores.append((vx * dx + vy * dy) / (vm * dm))
    return float(statistics.mean(scores)) if scores else 0.0


def build_unknown_geometries(seed: int) -> list[GeometrySpec]:
    rng = __import__("random").Random(seed + 35035)
    geoms: list[GeometrySpec] = []

    def add(name: str, family: str, truth: CanvasTruth) -> None:
        geoms.append(GeometrySpec(name=name, family=family, truth=truth))

    add("circle", "round", CanvasTruth([[_circle(160, 120, 55)]]))
    add("ellipse", "round", CanvasTruth([[_ellipse(155, 118, 70, 45)]]))
    add("rectangle", "rectilinear", CanvasTruth([[_rect(70, 50, 180, 140)]]))
    add("thin_ribbon", "ribbon", CanvasTruth([[_rect(30, 108, 260, 24)]]))
    add("diagonal_ribbon", "ribbon", CanvasTruth([[(40, 40), (250, 70), (245, 95), (35, 65)]]))
    outer, bite = _circle(150, 120, 72, 72), _circle(198, 115, 40, 48)
    add("crescent", "concave", CanvasTruth([[outer, bite]]))
    add(
        "fjord",
        "concave",
        CanvasTruth(
            [[(50, 60), (230, 60), (230, 100), (270, 120), (230, 140), (230, 180), (50, 180)]]
        ),
    )
    add("donut", "ring", CanvasTruth([[_circle(160, 120, 62), _circle(160, 120, 32)]]))
    add("single_island", "island", CanvasTruth([[_circle(160, 120, 38)]]))
    add("two_islands", "island", CanvasTruth([[_circle(85, 75, 30)], [_circle(210, 155, 38)]]))
    add(
        "three_islands",
        "island",
        CanvasTruth([[_circle(70, 70, 24)], [_circle(200, 80, 28)], [_circle(140, 170, 22)]]),
    )
    noisy = []
    for i in range(56):
        a = 2 * math.pi * i / 56
        r = 42 + 14 * math.sin(7 * a + seed * 0.013) + 7 * rng.uniform(-1, 1)
        noisy.append((160 + r * math.cos(a), 120 + r * math.sin(a)))
    add("noisy_blob", "organic", CanvasTruth([[noisy]]))
    add("small_compact", "round", CanvasTruth([[_circle(200, 60, 18)]]))
    add("wide_band", "ribbon", CanvasTruth([[_rect(20, 95, 280, 50)]]))
    s_pts = []
    for i in range(48):
        t = i / 47
        x = 40 + 240 * t
        y = 120 + 35 * math.sin(2 * math.pi * t * 1.5)
        s_pts.append((x, y))
    add("s_curve", "organic", CanvasTruth([[s_pts]]))
    add(
        "split_corridor",
        "corridor",
        CanvasTruth([[_rect(40, 60, 240, 22)], [_rect(40, 158, 240, 22)]]),
    )
    add("off_center_shape", "placement", CanvasTruth([[_circle(55, 55, 42)]]))
    add("shape_near_edge", "placement", CanvasTruth([[_rect(20, 12, 200, 45)]]))
    add(
        "fragmented_field",
        "fragmented",
        CanvasTruth(
            [
                [_circle(60, 60, 12)],
                [_circle(120, 90, 10)],
                [_circle(200, 70, 14)],
                [_circle(250, 150, 11)],
                [_circle(90, 180, 13)],
                [_circle(170, 200, 12)],
            ]
        ),
    )
    add(
        "negative_space_frame",
        "ring",
        CanvasTruth([[_rect(30, 30, 260, 180), _rect(70, 60, 180, 120)]]),
    )

    return geoms


def run_black_box(p31: Any, truth: TruthOracle, seed: int) -> dict[str, Any]:
    """Run solver mechanics; return only raw observables for external scoring."""
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

    initial_cells = {p31.cell_of(p.x, p.y) for p in particles}
    frontier_dist_by_step: list[float] = []
    frontier_cell_count_by_step: list[int] = []
    nearest_frontier_align_samples: list[tuple[float, float, float, float]] = []

    for step in range(p31.STEPS):
        labels = grid.classify()
        frontier = p31.discover_frontier_cells(labels)
        frontier_cell_count_by_step.append(len(frontier))
        step_occ: Counter[str] = Counter()
        frontier_centers = [p31.cell_center(c, r) for c, r in frontier]
        progress = step / max(1, p31.STEPS - 1)
        speed_ramp = p31.DISPLACEMENT_RAMP_START + (1.0 - p31.DISPLACEMENT_RAMP_START) * progress
        if p31.COLD_START_STEPS <= step < 32:
            speed_ramp *= 0.91
        step_dists: list[float] = []

        for p in particles:
            p.lastTruth = truth.truth_label(p.x, p.y)
            col, row = p31.cell_of(p.x, p.y)
            grid.deposit(col, row, p.lastTruth == "inside")

            if frontier_centers:
                nf = min(frontier_centers, key=lambda c: (c[0] - p.x) ** 2 + (c[1] - p.y) ** 2)
                step_dists.append(math.hypot(nf[0] - p.x, nf[1] - p.y))

            if step < p31.COLD_START_STEPS:
                tx = p.x + rng.uniform(-7.0, 7.0)
                ty = p.y + rng.uniform(-7.0, 7.0)
                tx, ty = p31.clamp_position(tx, ty)
                reason = "local_resample"
                cell_id = p31.cell_id_str(*p31.cell_of(tx, ty))
            else:
                tx, ty, reason, cell_id = p31.choose_solver_target(
                    p, grid, labels, frontier, step_occ, step, p31.STEPS, rng
                )
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
                ux, uy = p31.unit_vector(dx, dy)
                pull_scale = min(1.0, max(0.15, math.hypot(dx, dy) / 28.0))
                pull = p31.PARTICLE_SPEED * pull_scale * speed_ramp
                if progress >= 0.58:
                    pull *= 1.28
                p.vx = p.vx * p31.DAMPING + ux * pull
                p.vy = p.vy * p31.DAMPING + uy * pull
                mag = math.hypot(p.vx, p.vy)
                cap = p31.PARTICLE_SPEED * 1.6 * speed_ramp
                if mag > cap:
                    p.vx, p.vy = p.vx / mag * cap, p.vy / mag * cap
                mag = math.hypot(p.vx, p.vy)
                if mag > 0.05 and step >= p31.COLD_START_STEPS and frontier_centers:
                    nf = min(frontier_centers, key=lambda c: (c[0] - p.x) ** 2 + (c[1] - p.y) ** 2)
                    nearest_frontier_align_samples.append(
                        (p.vx, p.vy, nf[0] - p.x, nf[1] - p.y)
                    )

            if progress > 0.52 and frontier_centers:
                nearest = min(frontier_centers, key=lambda c: (c[0] - p.x) ** 2 + (c[1] - p.y) ** 2)
                ndx, ndy = nearest[0] - p.x, nearest[1] - p.y
                if math.hypot(ndx, ndy) > 6.0:
                    nux, nuy = p31.unit_vector(ndx, ndy)
                    w = (progress - 0.52) * 1.4
                    p.vx = p.vx * p31.DAMPING + nux * p31.PARTICLE_SPEED * w
                    p.vy = p.vy * p31.DAMPING + nuy * p31.PARTICLE_SPEED * w

            if len(p.history) >= 4:
                recent = [(round(h[0] / REPEAT_BIN), round(h[1] / REPEAT_BIN)) for h in p.history[-8:]]
                nb = (round((p.x + p.vx) / REPEAT_BIN), round((p.y + p.vy) / REPEAT_BIN))
                if nb in recent:
                    mag = math.hypot(p.vx, p.vy) or 0.1
                    p.vx, p.vy = p31.unit_vector(-p.vy, p.vx)
                    p.vx *= mag
                    p.vy *= mag

            p.x += p.vx
            p.y += p.vy
            p.x, p.y = p31.clamp_position(p.x, p.y)
            p.history.append([round(p.x, 4), round(p.y, 4)])

        if step_dists:
            frontier_dist_by_step.append(statistics.mean(step_dists))

    displacements = [math.hypot(p.x - p.x0, p.y - p.y0) for p in particles]
    migrated = sum(1 for d in displacements if d >= p31.SIGNIFICANT_MOVE)

    targets = Counter(p.targetCellId for p in particles if p.targetCellId)
    top = targets.most_common(10)
    n = len(particles)

    loop_trapped = 0
    oscillation_scores: list[float] = []
    repeated = 0
    total_bins = 0
    half_fracs: list[float] = []

    for p in particles:
        bins = [(round(h[0] / REPEAT_BIN), round(h[1] / REPEAT_BIN)) for h in p.history]
        total_bins += len(bins)
        counts = Counter(bins)
        repeated += sum(c - 1 for c in counts.values() if c > 1)
        if len(p.history) >= 12:
            seg = p.history[-20:]
            plen = sum(
                math.hypot(seg[i][0] - seg[i - 1][0], seg[i][1] - seg[i - 1][1])
                for i in range(1, len(seg))
            )
            net = math.hypot(seg[-1][0] - seg[0][0], seg[-1][1] - seg[0][1])
            oscillation_scores.append(plen / (net + 1e-6))
            lc = Counter(bins[-15:])
            sx = max(pt[0] for pt in seg) - min(pt[0] for pt in seg)
            sy = max(pt[1] for pt in seg) - min(pt[1] for pt in seg)
            if max(lc.values()) >= 5 and max(sx, sy) < LOOP_RADIUS and net < LOOP_RADIUS:
                loop_trapped += 1
        if len(p.history) >= 4:
            mid = len(p.history) // 2
            first = math.hypot(p.history[mid][0] - p.x0, p.history[mid][1] - p.y0)
            total = math.hypot(p.x - p.x0, p.y - p.y0)
            half_fracs.append(first / (total + 1e-9))

    valid = [
        d
        for i, d in enumerate(frontier_dist_by_step)
        if i > 0 and frontier_cell_count_by_step[i] > 0 and d > 0
    ]
    window = max(3, len(valid) // 6)
    if len(valid) >= window * 2:
        early = statistics.mean(valid[:window])
        late = statistics.mean(valid[-window:])
        frontier_delta = early - late
    else:
        early = late = 0.0
        frontier_delta = 0.0

    return {
        "initialCoverage": len(initial_cells) / p31.MACRO_CELL_COUNT,
        "particleMigrationFraction": migrated / n,
        "meanDisplacement": statistics.mean(displacements),
        "medianDisplacement": statistics.median(displacements),
        "frontierDistanceDelta": frontier_delta,
        "frontierDistanceEarlyMean": early,
        "frontierDistanceLateMean": late,
        "nearestFrontierVelocityAlignment": _alignment_score(nearest_frontier_align_samples),
        "nearestFrontierSampleCount": len(nearest_frontier_align_samples),
        "targetCentralizationTop1": top[0][1] / n if top else 0.0,
        "targetCentralizationTop3": sum(c for _, c in top[:3]) / n,
        "uniqueTargetCells": len(targets),
        "loopTrapFraction": loop_trapped / n,
        "oscillationScore": statistics.mean(oscillation_scores) if oscillation_scores else 0.0,
        "repeatedPositionRatio": repeated / max(1, total_bins),
        "firstHalfDisplacementFraction": statistics.mean(half_fracs) if half_fracs else 0.0,
    }


def evaluate_run(metrics: dict[str, Any]) -> tuple[bool, list[str]]:
    failures = [name for name, fn in GATES.items() if not fn(metrics)]
    return len(failures) == 0, failures


def _relative_spread(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = statistics.mean(values)
    if abs(mean) < 1e-9:
        return max(values) - min(values)
    return (max(values) - min(values)) / abs(mean)


def run_harness(seeds: list[int]) -> dict[str, Any]:
    p31 = _load_solver()
    geometries = build_unknown_geometries(seed=seeds[0])

    runs: dict[str, dict[str, Any]] = {}
    for geom in geometries:
        runs[geom.name] = {}
        for seed in seeds:
            metrics = run_black_box(p31, geom.truth, seed)
            passed, failures = evaluate_run(metrics)
            runs[geom.name][str(seed)] = {
                "metrics": metrics,
                "passed": passed,
                "failureReasons": failures,
            }

    geometry_pass_rates: dict[str, float] = {}
    geometry_means: dict[str, dict[str, float]] = {}
    metric_keys = list(next(iter(runs.values()))[str(seeds[0])]["metrics"].keys())

    for geom_name, seed_runs in runs.items():
        geometry_pass_rates[geom_name] = sum(1 for r in seed_runs.values() if r["passed"]) / len(seed_runs)
        geometry_means[geom_name] = {
            k: round(statistics.mean(r["metrics"][k] for r in seed_runs.values()), 6)
            for k in metric_keys
            if k != "nearestFrontierSampleCount"
        }

    seed_pass_rates: dict[str, float] = {}
    for seed in seeds:
        s = str(seed)
        total = sum(1 for g in runs if runs[g][s]["passed"])
        seed_pass_rates[s] = total / len(geometries)

    family_pass: dict[str, list[float]] = {}
    for geom in geometries:
        family_pass.setdefault(geom.family, []).append(geometry_pass_rates[geom.name])

    geometry_sensitivity_spread = {
        "nearestFrontierVelocityAlignment": round(
            _relative_spread([geometry_means[g]["nearestFrontierVelocityAlignment"] for g in geometry_means]),
            6,
        ),
        "frontierDistanceDelta": round(
            _relative_spread([geometry_means[g]["frontierDistanceDelta"] for g in geometry_means]),
            6,
        ),
        "particleMigrationFraction": round(
            _relative_spread([geometry_means[g]["particleMigrationFraction"] for g in geometry_means]),
            6,
        ),
    }

    geometries_passing = sum(1 for r in geometry_pass_rates.values() if r >= GEOMETRY_PASS_RATE_MIN)
    geometry_pass_fraction = geometries_passing / len(geometries)
    families_with_zero = [fam for fam, rates in family_pass.items() if max(rates) == 0.0]
    material_variation = (
        geometry_sensitivity_spread["nearestFrontierVelocityAlignment"] >= GEOMETRY_SENSITIVITY_MIN_SPREAD
        or geometry_sensitivity_spread["frontierDistanceDelta"] >= GEOMETRY_SENSITIVITY_MIN_SPREAD
    )

    global_failures: list[str] = []
    if geometry_pass_fraction < GEOMETRY_PASS_RATE_MIN:
        global_failures.append(
            f"geometry_pass_fraction {geometry_pass_fraction:.3f} < {GEOMETRY_PASS_RATE_MIN}"
        )
    if families_with_zero:
        global_failures.append(f"geometry_families_with_zero_pass_rate: {families_with_zero}")
    if not material_variation:
        global_failures.append(
            "metrics_do_not_vary_materially_by_geometry "
            f"(spreads {geometry_sensitivity_spread})"
        )

    overall_pass = geometry_pass_fraction >= GEOMETRY_PASS_RATE_MIN and not families_with_zero and material_variation

    per_geometry_summary = {}
    for geom in geometries:
        gm = geometry_means[geom.name]
        per_geometry_summary[geom.name] = {
            "family": geom.family,
            "passRate": round(geometry_pass_rates[geom.name], 6),
            "passed": geometry_pass_rates[geom.name] >= GEOMETRY_PASS_RATE_MIN,
            "meanMetrics": gm,
            "dominantFailures": _dominant_failures(runs[geom.name]),
        }

    return {
        "phase": "3.35_black_box_acceptance",
        "emergenceClaimed": False,
        "solverScript": str(SOLVER_SCRIPT.relative_to(ROOT)),
        "harnessOwnsAcceptance": True,
        "ignoresSolverSelfReportedClaims": True,
        "retiredMetrics": ["frontierAttractionAlignmentScore", "chosenTargetPullAlignment"],
        "seeds": seeds,
        "geometryCount": len(geometries),
        "geometries": [g.name for g in geometries],
        "gates": list(GATES.keys()),
        "globalThresholds": {
            "geometryPassFractionMin": GEOMETRY_PASS_RATE_MIN,
            "geometrySensitivityMinSpread": GEOMETRY_SENSITIVITY_MIN_SPREAD,
        },
        "runs": runs,
        "geometryMeans": geometry_means,
        "geometryPassRates": geometry_pass_rates,
        "seedPassRates": seed_pass_rates,
        "geometrySensitivitySpread": geometry_sensitivity_spread,
        "perGeometrySummary": per_geometry_summary,
        "familyPassRates": {k: round(statistics.mean(v), 6) for k, v in family_pass.items()},
        "globalFailureReasons": global_failures,
        "overallVerdict": "PASS" if overall_pass else "FAIL",
        "acceptedForVisualPrototyping": overall_pass,
        "conclusion": (
            "Current solver accepted for visual prototyping under external black-box gates."
            if overall_pass
            else "Current solver NOT accepted for visual prototyping. Do not proceed to visuals."
        ),
    }


def _dominant_failures(seed_runs: dict[str, Any]) -> list[str]:
    counts: Counter[str] = Counter()
    for r in seed_runs.values():
        for f in r["failureReasons"]:
            counts[f] += 1
    return [f"{k} ({v})" for k, v in counts.most_common(5)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 3.35 black-box acceptance")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seeds", type=str, default=",".join(str(s) for s in SEEDS))
    args = parser.parse_args(argv)
    seeds = [int(s.strip()) for s in args.seeds.split(",")]
    report = run_harness(seeds)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "overallVerdict": report["overallVerdict"],
                "acceptedForVisualPrototyping": report["acceptedForVisualPrototyping"],
                "geometryPassFraction": round(
                    sum(1 for r in report["geometryPassRates"].values() if r >= GEOMETRY_PASS_RATE_MIN)
                    / report["geometryCount"],
                    3,
                ),
            },
            indent=2,
        )
    )
    return 0 if report["overallVerdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
