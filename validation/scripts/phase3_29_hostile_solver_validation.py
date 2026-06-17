#!/usr/bin/env python3
"""Phase 3.29 hostile solver validation — mechanics only, no visuals.

Adversarially tests whether Phase 3.28-style solver mechanics are genuinely
solver-driven or disguised interpolation / drift / statistical theater.

Does NOT optimize for passing. Does NOT tune thresholds post-hoc.
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOLVER_MODULE = "validation.solver.phase3_28_true_discovery_sim"
DEFAULT_BASELINE_METRICS = ROOT / "validation/reports/phase3_28_true_discovery_sim_metrics.json"
DEFAULT_SUN_GEOJSON = ROOT / "validation/geojson/phase3_15_real_single_polygon_sun_house_1.geojson"

FIELD_W = 320.0
FIELD_H = 240.0
DEFAULT_STEPS = 96
SIGNIFICANT_MOVE_CELLS = 3.0
CELL_SIZE = 10.0  # inferred from Phase 3.28 metrics scale


# ---------------------------------------------------------------------------
# Verdicts
# ---------------------------------------------------------------------------

VERDICT_PASS = "PASS"
VERDICT_FAIL = "FAIL"
VERDICT_UNPROVEN = "UNPROVEN"


@dataclass
class HostileTestResult:
    name: str
    verdict: str
    mode: str
    evidence: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    statistics: dict[str, Any] = field(default_factory=dict)

    def fail(self, message: str) -> None:
        self.verdict = VERDICT_FAIL
        self.failures.append(message)

    def unproven(self, message: str) -> None:
        if self.verdict != VERDICT_FAIL:
            self.verdict = VERDICT_UNPROVEN
        self.failures.append(message)

    def note(self, message: str) -> None:
        self.evidence.append(message)


# ---------------------------------------------------------------------------
# Geometry / truth oracles
# ---------------------------------------------------------------------------


def point_in_ring(x: float, y: float, ring: list[tuple[float, float]]) -> bool:
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


def point_in_polygon_lonlat(lon: float, lat: float, rings: list[list[tuple[float, float]]]) -> bool:
    if not rings:
        return False
    if not point_in_ring(lon, lat, rings[0]):
        return False
    for hole in rings[1:]:
        if point_in_ring(lon, lat, hole):
            return False
    return True


def project_ring(
    ring: list[list[float]],
    width: float = FIELD_W,
    height: float = FIELD_H,
    pad: float = 16.0,
) -> list[tuple[float, float]]:
    lons = [c[0] for c in ring]
    lats = [c[1] for c in ring]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    scale = min((width - 2 * pad) / (max_lon - min_lon), (height - 2 * pad) / (max_lat - min_lat))
    return [
        (pad + (c[0] - min_lon) * scale, height - pad - (c[1] - min_lat) * scale)
        for c in ring
    ]


def load_sun_polygon_rings() -> list[list[tuple[float, float]]]:
    data = json.loads(DEFAULT_SUN_GEOJSON.read_text(encoding="utf-8"))
    feature = data["features"][0]
    coords = feature["geometry"]["coordinates"]
    return [[(c[0], c[1]) for c in ring] for ring in coords]


def make_canvas_oracle(rings_lonlat: list[list[tuple[float, float]]]) -> Callable[[float, float], bool]:
    projected = [project_ring([[lon, lat] for lon, lat in ring]) for ring in rings_lonlat]

    def truth(x: float, y: float) -> bool:
        lonlat = canvas_to_lonlat(x, y, rings_lonlat)
        return point_in_polygon_lonlat(lonlat[0], lonlat[1], rings_lonlat)

    return truth


def canvas_to_lonlat(x: float, y: float, rings_lonlat: list[list[tuple[float, float]]]) -> tuple[float, float]:
    ring = rings_lonlat[0]
    lons = [c[0] for c in ring]
    lats = [c[1] for c in ring]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    pad = 16.0
    scale = min((FIELD_W - 2 * pad) / (max_lon - min_lon), (FIELD_H - 2 * pad) / (max_lat - min_lat))
    lon = min_lon + (x - pad) / scale
    lat = max_lat - (y - pad) / scale
    return lon, lat


def circle_rings(cx: float = 160.0, cy: float = 120.0, r: float = 55.0, n: int = 64) -> list[list[tuple[float, float]]]:
    ring = [
        (cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ]
    return [ring]


def rectangle_rings(x0: float, y0: float, w: float, h: float) -> list[list[tuple[float, float]]]:
    return [[(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]]


def corridor_rings() -> list[list[tuple[float, float]]]:
    return [rectangle_rings(40, 100, 240, 40)[0]]


def fragmented_islands_rings() -> list[list[tuple[float, float]]]:
    return [
        circle_rings(80, 80, 28)[0],
        circle_rings(200, 160, 35)[0],
        circle_rings(120, 180, 22)[0],
    ]


def noisy_concave_rings() -> list[list[tuple[float, float]]]:
    pts = []
    for i in range(48):
        angle = 2 * math.pi * i / 48
        r = 50 + 18 * math.sin(5 * angle) + 10 * math.cos(3 * angle)
        pts.append((160 + r * math.cos(angle), 120 + r * math.sin(angle)))
    return [pts]


def diagonal_wedge_rings() -> list[list[tuple[float, float]]]:
    return [[(30, 30), (260, 50), (220, 200), (50, 180)]]


def two_regions_rings() -> list[list[tuple[float, float]]]:
    return [
        rectangle_rings(30, 40, 90, 70)[0],
        rectangle_rings(180, 120, 100, 80)[0],
    ]


def canvas_truth_from_projected(rings: list[list[tuple[float, float]]]) -> Callable[[float, float], bool]:
    def truth(x: float, y: float) -> bool:
        if not point_in_ring(x, y, rings[0]):
            return False
        for hole in rings[1:]:
            if point_in_ring(x, y, hole):
                return False
        return True

    return truth


GEOMETRY_CASES: dict[str, Callable[[], Callable[[float, float], bool]]] = {
    "sun_in_1_polygon": lambda: make_canvas_oracle(load_sun_polygon_rings()),
    "circle": lambda: canvas_truth_from_projected(circle_rings()),
    "rectangle": lambda: canvas_truth_from_projected(rectangle_rings(70, 50, 180, 140)),
    "narrow_corridor": lambda: canvas_truth_from_projected(corridor_rings()),
    "fragmented_islands": lambda: canvas_truth_from_projected(fragmented_islands_rings()),
    "noisy_concave": lambda: canvas_truth_from_projected(noisy_concave_rings()),
    "diagonal_wedge": lambda: canvas_truth_from_projected(diagonal_wedge_rings()),
    "two_disconnected_regions": lambda: canvas_truth_from_projected(two_regions_rings()),
}


INIT_DISTRIBUTIONS = [
    "uniform",
    "clustered",
    "sparse",
    "edge_biased",
    "center_biased",
]


# ---------------------------------------------------------------------------
# Solver loading
# ---------------------------------------------------------------------------


def load_solver(module_name: str):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


def run_solver(
    solver: Any,
    *,
    truth: Callable[[float, float], bool],
    init_distribution: str,
    steps: int,
    seed: int,
) -> dict[str, Any]:
    if hasattr(solver, "run_simulation"):
        return solver.run_simulation(
            truth_oracle=truth,
            init_distribution=init_distribution,
            steps=steps,
            seed=seed,
            width=FIELD_W,
            height=FIELD_H,
        )
    if hasattr(solver, "simulate"):
        return solver.simulate(truth, init_distribution=init_distribution, steps=steps, seed=seed)
    raise AttributeError("Solver module lacks run_simulation() or simulate()")


# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mx = statistics.mean(xs)
    my = statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    if denx == 0 or deny == 0:
        return None
    return num / (denx * deny)


def normalized_step(xs: list[float]) -> list[float]:
    if len(xs) <= 1:
        return [0.0] * len(xs)
    return [i / (len(xs) - 1) for i in range(len(xs))]


def detect_cliff_step(series: list[float], threshold_ratio: float = 0.35) -> int | None:
    if len(series) < 3:
        return None
    max_jump = 0.0
    cliff = None
    for i in range(1, len(series)):
        prev = series[i - 1]
        cur = series[i]
        denom = max(abs(prev), 1e-9)
        jump = abs(cur - prev) / denom
        if jump > max_jump:
            max_jump = jump
            cliff = i
    if max_jump >= threshold_ratio:
        return cliff
    return None


def monotonic_fraction(series: list[float], allow_plateau: bool = True) -> float:
    if len(series) < 2:
        return 1.0
    inc = 0
    for i in range(1, len(series)):
        if series[i] >= series[i - 1] if allow_plateau else series[i] > series[i - 1]:
            inc += 1
    return inc / (len(series) - 1)


def plateau_run_length(series: list[float], eps: float = 1e-6) -> int:
    best = 1
    cur = 1
    for i in range(1, len(series)):
        if abs(series[i] - series[i - 1]) <= eps:
            cur += 1
            best = max(best, cur)
        else:
            cur = 1
    return best


def coefficient_of_variation(values: list[float]) -> float | None:
    if not values:
        return None
    mean = statistics.mean(values)
    if abs(mean) < 1e-12:
        return None
    return statistics.pstdev(values) / abs(mean)


def series_similarity(a: list[float], b: list[float]) -> float | None:
    if len(a) != len(b) or len(a) < 3:
        return None
    return pearson(a, b)


# ---------------------------------------------------------------------------
# Retrospective audit (metrics JSON only)
# ---------------------------------------------------------------------------


def retrospective_from_metrics(metrics: dict[str, Any]) -> dict[str, HostileTestResult]:
    """Hostile audit on archived Phase 3.28 baseline metrics when live solver is unavailable."""
    results: dict[str, HostileTestResult] = {}

    steps = len(metrics.get("frothMetricByStep", []))
    froth = metrics.get("frothMetricByStep", [])
    compression = metrics.get("compressionMetricByStep", [])
    abandoned = metrics.get("abandonedParticleCountByStep", [])
    frontier = metrics.get("frontierCellCountByStep", [])
    pressure = metrics.get("maxFrontierPressureByStep", [])

    # Test 5 / 6 signals from single run
    t5 = HostileTestResult("abandonment_virga_test", VERDICT_PASS, "retrospective_single_run")
    abandon_cliff = detect_cliff_step(abandoned, threshold_ratio=0.5)
    if abandon_cliff is not None:
        t5.fail(
            f"Abandonment count cliff at step {abandon_cliff} ({abandon_cliff/steps:.3f} normalized): global synchronization."
        )
    sample = metrics.get("particleSample", [])
    if sample:
        steps_ab = [p.get("abandonedStep") for p in sample if p.get("abandoned")]
        if steps_ab and len(set(steps_ab)) == 1:
            t5.fail(f"Particle sample shows single abandonment step for all particles: {steps_ab[0]}")
        t5.note(f"abandoned sample steps unique count: {len(set(steps_ab))}")
    t5.statistics = {
        "abandonmentCliffStep": abandon_cliff,
        "finalAbandonedCount": abandoned[-1] if abandoned else None,
        "abandonmentTimingVariance": coefficient_of_variation([float(s) for s in steps_ab]) if sample else None,
    }
    results["abandonment_virga_test"] = t5

    t6 = HostileTestResult("time_dependence_audit", VERDICT_PASS, "retrospective_single_run")
    froth_peak = metrics.get("frothPeakStep")
    compression_onset = metrics.get("compressionOnsetStep")
    if froth_peak is not None:
        t6.note(f"archived frothPeakStep={froth_peak} of {steps}")
    if compression_onset is not None:
        t6.note(f"archived compressionOnsetStep={compression_onset} of {steps}")
    if abandon_cliff is not None and abandon_cliff <= max(3, steps // 8):
        t6.fail("Early global abandonment cliff suggests screenplay timing, not local decay.")
    if monotonic_fraction(froth) > 0.88:
        t6.fail(f"Froth metric monotonic in {monotonic_fraction(froth):.3f} of steps — engineered curve shape.")
    if plateau_run_length(compression) >= max(8, steps // 5):
        t6.fail(f"Compression metric plateau run length {plateau_run_length(compression)} — staircase behavior.")
    if metrics.get("convergenceReached") is False:
        t6.note("convergenceReached=false in archived run")
    t6.statistics = {
        "frothMonotonicFraction": monotonic_fraction(froth),
        "compressionPlateauRun": plateau_run_length(compression),
        "frothTimeCorrelation": pearson(normalized_step(froth), froth),
        "compressionTimeCorrelation": pearson(normalized_step(compression), compression),
    }
    results["time_dependence_audit"] = t6

    t7 = HostileTestResult("metric_correlation_audit", VERDICT_PASS, "retrospective_single_run")
    ft = pearson(froth, normalized_step([float(i) for i in range(len(froth))]))
    cp = pearson(compression, normalized_step([float(i) for i in range(len(compression))]))
    ff = pearson(froth, [float(x) for x in frontier])
    if ft is not None and ft > 0.92:
        t7.fail(f"Froth metric highly correlated with normalized time ({ft:.4f}) — time-shaped, not pressure-shaped.")
    if cp is not None and cp > 0.85:
        t7.fail(f"Compression metric highly correlated with normalized time ({cp:.4f}).")
    if ff is not None and ff > 0.9:
        t7.note(f"Froth vs frontierCellCount correlation={ff:.4f}")
    if pressure and len(set(round(p, 3) for p in pressure[-40:])) <= 2:
        t7.fail("maxFrontierPressure saturates early and flatlines — metric ceiling theater.")
    t7.statistics = {
        "frothTimeCorr": ft,
        "compressionTimeCorr": cp,
        "frothFrontierCorr": ff,
        "pressureTailUnique": len(set(round(p, 3) for p in pressure[-40:])),
    }
    results["metric_correlation_audit"] = t7

    t3 = HostileTestResult("drift_vs_convergence_test", VERDICT_PASS, "retrospective_single_run")
    if sample:
        speeds = [math.hypot(p.get("vx", 0), p.get("vy", 0)) for p in sample]
        if statistics.mean(speeds) < 1e-8:
            t3.fail("End-state particle velocities near zero after large displacement — moved then frozen, not converging.")
        t3.note(f"mean end speed={statistics.mean(speeds):.3e}")
    t3.note(
        f"meanDistanceMoved={metrics.get('meanDistanceMoved')} median={metrics.get('medianDistanceMoved')} "
        f"percentMoved={metrics.get('percentInitialParticlesMovedSignificantDistance')}"
    )
    if metrics.get("convergenceReached") is False:
        t3.fail("Solver never reached convergence in archived run despite high acceptance metrics.")
    results["drift_vs_convergence_test"] = t3

    for name in [
        "geometry_variation_test",
        "randomized_initial_distribution_test",
        "frontier_authenticity_test",
        "hidden_target_audit",
    ]:
        tr = HostileTestResult(name, VERDICT_UNPROVEN, "retrospective_unavailable")
        tr.unproven("Live solver module unavailable — cannot execute multi-geometry or trajectory audit.")
        results[name] = tr

    return results


# ---------------------------------------------------------------------------
# Live hostile tests (require solver module)
# ---------------------------------------------------------------------------


def extract_series(result: dict[str, Any], key: str) -> list[float]:
    value = result.get(key, [])
    return [float(v) for v in value]


def test_geometry_variation(solver: Any, steps: int, seed: int) -> HostileTestResult:
    test = HostileTestResult("geometry_variation_test", VERDICT_PASS, "live_multi_geometry")
    shape_summaries: dict[str, dict[str, Any]] = {}
    froth_curves: dict[str, list[float]] = {}
    compression_curves: dict[str, list[float]] = {}
    abandon_curves: dict[str, list[float]] = {}

    for name, factory in GEOMETRY_CASES.items():
        truth = factory()
        try:
            result = run_solver(solver, truth=truth, init_distribution="uniform", steps=steps, seed=seed)
        except Exception as exc:
            test.fail(f"{name}: solver run failed: {exc}")
            continue
        froth = extract_series(result, "frothMetricByStep")
        compression = extract_series(result, "compressionMetricByStep")
        abandoned = extract_series(result, "abandonedParticleCountByStep")
        frontier = extract_series(result, "frontierCellCountByStep")
        froth_curves[name] = froth
        compression_curves[name] = compression
        abandon_curves[name] = abandoned
        shape_summaries[name] = {
            "finalFroth": froth[-1] if froth else None,
            "finalCompression": compression[-1] if compression else None,
            "finalAbandoned": abandoned[-1] if abandoned else None,
            "finalFrontierCells": frontier[-1] if frontier else None,
            "frothPeakStep": int(max(range(len(froth)), key=lambda i: froth[i])) if froth else None,
            "compressionOnsetStep": next((i for i, v in enumerate(compression) if v > 0.01), None),
            "abandonmentCliffStep": detect_cliff_step(abandoned),
        }

    names = list(froth_curves.keys())
    if len(names) >= 2:
        pairs = 0
        similar = 0
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                sim = series_similarity(froth_curves[names[i]], froth_curves[names[j]])
                pairs += 1
                if sim is not None and sim > 0.92:
                    similar += 1
                test.note(f"froth similarity {names[i]} vs {names[j]}: {sim}")
        if pairs and similar / pairs > 0.5:
            test.fail(
                f"Froth curves statistically similar across {similar}/{pairs} geometry pairs — shape-invariant theater."
            )

    finals = [shape_summaries[n]["finalFroth"] for n in names if shape_summaries[n]["finalFroth"] is not None]
    if finals and coefficient_of_variation(finals) is not None and coefficient_of_variation(finals) < 0.08:
        test.fail(f"Final froth metrics have low CV across geometries ({coefficient_of_variation(finals):.4f}).")

    test.statistics = {"shapes": shape_summaries}
    if test.verdict != VERDICT_FAIL and shape_summaries:
        test.verdict = VERDICT_PASS
        test.note("Geometry cases produced distinguishable metric signatures.")
    return test


def test_randomized_initial_distribution(solver: Any, steps: int, seed: int) -> HostileTestResult:
    test = HostileTestResult("randomized_initial_distribution_test", VERDICT_PASS, "live_init_variation")
    truth = GEOMETRY_CASES["circle"]()
    summaries: dict[str, Any] = {}
    for dist in INIT_DISTRIBUTIONS:
        try:
            result = run_solver(solver, truth=truth, init_distribution=dist, steps=steps, seed=seed)
        except Exception as exc:
            test.fail(f"{dist}: {exc}")
            continue
        summaries[dist] = {
            "initialMacroCellCoverage": result.get("initialMacroCellCoverage"),
            "percentMoved": result.get("percentInitialParticlesMovedSignificantDistance"),
            "meanDistanceMoved": result.get("meanDistanceMoved"),
            "finalFroth": extract_series(result, "frothMetricByStep")[-1] if result.get("frothMetricByStep") else None,
            "finalFrontier": extract_series(result, "frontierCellCountByStep")[-1] if result.get("frontierCellCountByStep") else None,
        }

    moved = [summaries[d]["percentMoved"] for d in summaries if summaries[d].get("percentMoved") is not None]
    coverages = [summaries[d]["initialMacroCellCoverage"] for d in summaries if summaries[d].get("initialMacroCellCoverage") is not None]
    if moved and coefficient_of_variation(moved) is not None and coefficient_of_variation(moved) < 0.05:
        test.fail("percentInitialParticlesMovedSignificantDistance nearly identical across init distributions.")
    if coverages and max(coverages) - min(coverages) < 0.05:
        test.fail("Initial macro-cell coverage does not materially vary across init distributions.")
    test.statistics = summaries
    if test.verdict != VERDICT_FAIL:
        test.verdict = VERDICT_PASS
    return test


def test_drift_vs_convergence(solver: Any, steps: int, seed: int) -> HostileTestResult:
    test = HostileTestResult("drift_vs_convergence_test", VERDICT_PASS, "live_trajectory")
    truth = GEOMETRY_CASES["sun_in_1_polygon"]()
    try:
        result = run_solver(solver, truth=truth, init_distribution="uniform", steps=steps, seed=seed)
    except Exception as exc:
        test.fail(f"Solver run failed: {exc}")
        return test

    histories = result.get("particleHistoriesByStep") or result.get("particleHistoryByStep")
    if not histories:
        test.unproven("Solver did not expose particleHistoriesByStep — cannot audit drift vs convergence.")
        return test

    frontier_distances: list[float] = []
    congestion: list[float] = []
    revisit_rates: list[float] = []
    coherence: list[float] = []

    for step_hist in histories:
        particles = step_hist if isinstance(step_hist, list) else step_hist.get("particles", [])
        if not particles:
            continue
        dists = []
        speeds = []
        for p in particles:
            if not p.get("visible", True):
                continue
            fd = p.get("frontierDistance")
            if fd is not None:
                dists.append(float(fd))
            speeds.append(math.hypot(float(p.get("vx", 0)), float(p.get("vy", 0))))
        if dists:
            frontier_distances.append(statistics.mean(dists))
            congestion.append(statistics.pstdev(speeds) if len(speeds) > 1 else 0.0)

    if len(frontier_distances) >= 4:
        early = statistics.mean(frontier_distances[: len(frontier_distances) // 3])
        late = statistics.mean(frontier_distances[-len(frontier_distances) // 3 :])
        if late >= early * 0.95:
            test.fail(
                f"Mean frontier distance does not decrease (early={early:.3f}, late={late:.3f}) — no convergence."
            )
        else:
            test.note(f"frontier distance decreased early={early:.3f} late={late:.3f}")

    test.statistics = {
        "frontierDistanceSeries": frontier_distances,
        "congestionSeries": congestion,
    }
    if test.verdict not in (VERDICT_FAIL, VERDICT_UNPROVEN):
        test.verdict = VERDICT_PASS
    return test


def test_frontier_authenticity(solver: Any, steps: int, seed: int) -> HostileTestResult:
    test = HostileTestResult("frontier_authenticity_test", VERDICT_PASS, "live_frontier")
    truth = GEOMETRY_CASES["noisy_concave"]()
    try:
        result = run_solver(solver, truth=truth, init_distribution="uniform", steps=steps, seed=seed)
    except Exception as exc:
        test.fail(str(exc))
        return test

    froth = extract_series(result, "frothMetricByStep")
    compression = extract_series(result, "compressionMetricByStep")
    frontier = extract_series(result, "frontierCellCountByStep")
    pressure = extract_series(result, "maxFrontierPressureByStep")

    comp_onset = next((i for i, v in enumerate(compression) if v > 0.05), None)
    froth_peak = int(max(range(len(froth)), key=lambda i: froth[i])) if froth else None
    frontier_narrow = None
    if len(frontier) >= 4:
        early = statistics.mean(frontier[: len(frontier) // 3])
        late = statistics.mean(frontier[-len(frontier) // 3 :])
        if early > 0:
            frontier_narrow = late / early
        if frontier_narrow is not None and frontier_narrow > 0.85 and compression[-1] > 0.2:
            test.fail("Frontier cell count did not narrow while compression rose — disagreement not collapsing.")

    if comp_onset is not None and froth_peak is not None and abs(comp_onset - froth_peak) < 3:
        test.fail("Compression onset immediately follows froth peak — likely time-coupled, not disagreement-driven.")

    test.statistics = {
        "compressionOnsetStep": comp_onset,
        "frothPeakStep": froth_peak,
        "frontierNarrowRatio": frontier_narrow,
        "frothCompressionCorr": pearson(froth, compression),
        "pressureTailUnique": len(set(round(p, 3) for p in pressure[-20:])),
    }
    if test.verdict != VERDICT_FAIL:
        test.verdict = VERDICT_PASS if frontier_narrow is not None and frontier_narrow < 0.85 else VERDICT_UNPROVEN
    return test


def test_abandonment_virga(solver: Any, steps: int, seed: int) -> HostileTestResult:
    test = HostileTestResult("abandonment_virga_test", VERDICT_PASS, "live_abandonment")
    truth = GEOMETRY_CASES["rectangle"]()
    try:
        result = run_solver(solver, truth=truth, init_distribution="uniform", steps=steps, seed=seed)
    except Exception as exc:
        test.fail(str(exc))
        return test

    abandoned = extract_series(result, "abandonedParticleCountByStep")
    cliff = detect_cliff_step(abandoned)
    if cliff is not None and cliff < steps // 4:
        test.fail(f"Global abandonment cliff at step {cliff}.")

    particles = result.get("particles") or result.get("particleSample") or []
    if particles:
        steps_ab = [p.get("abandonedStep") for p in particles if p.get("abandoned")]
        if steps_ab:
            cv = coefficient_of_variation([float(s) for s in steps_ab])
            if cv is not None and cv < 0.05:
                test.fail(f"Abandonment timing variance too low (CV={cv:.4f}).")
            test.statistics["abandonmentTimingCV"] = cv
    test.statistics["abandonmentCliffStep"] = cliff
    if test.verdict != VERDICT_FAIL:
        test.verdict = VERDICT_PASS if cliff is None else VERDICT_UNPROVEN
    return test


def test_time_dependence(solver: Any, steps: int, seed: int) -> HostileTestResult:
    test = HostileTestResult("time_dependence_audit", VERDICT_PASS, "live_timing")
    summaries = []
    for name in ("circle", "narrow_corridor", "two_disconnected_regions"):
        truth = GEOMETRY_CASES[name]()
        result = run_solver(solver, truth=truth, init_distribution="uniform", steps=steps, seed=seed + hash(name) % 1000)
        summaries.append(
            {
                "shape": name,
                "frothPeakStep": int(max(range(len(result["frothMetricByStep"])), key=lambda i: result["frothMetricByStep"][i])),
                "compressionOnset": next((i for i, v in enumerate(result["compressionMetricByStep"]) if v > 0.05), None),
                "abandonCliff": detect_cliff_step([float(x) for x in result["abandonedParticleCountByStep"]]),
            }
        )

    peaks = [s["frothPeakStep"] for s in summaries]
    onsets = [s["compressionOnset"] for s in summaries if s["compressionOnset"] is not None]
    if peaks and coefficient_of_variation([float(p) for p in peaks]) is not None:
        cv = coefficient_of_variation([float(p) for p in peaks])
        test.statistics["frothPeakCVAcrossShapes"] = cv
        if cv is not None and cv < 0.04:
            test.fail(f"Froth peak occurs at nearly same normalized step across shapes (CV={cv:.4f}).")
    if onsets and coefficient_of_variation([float(x) for x in onsets]) is not None and coefficient_of_variation([float(x) for x in onsets]) < 0.04:
        test.fail("Compression onset synchronized across geometries.")
    test.statistics["summaries"] = summaries
    if test.verdict != VERDICT_FAIL:
        test.verdict = VERDICT_PASS
    return test


def test_metric_correlation(solver: Any, steps: int, seed: int) -> HostileTestResult:
    test = HostileTestResult("metric_correlation_audit", VERDICT_PASS, "live_metrics")
    truth = GEOMETRY_CASES["sun_in_1_polygon"]()
    result = run_solver(solver, truth=truth, init_distribution="uniform", steps=steps, seed=seed)
    froth = extract_series(result, "frothMetricByStep")
    compression = extract_series(result, "compressionMetricByStep")
    frontier = extract_series(result, "frontierCellCountByStep")
    t = normalized_step(froth)
    if pearson(froth, t) and pearson(froth, t) > 0.9:
        test.fail(f"Froth metric time-correlated ({pearson(froth, t):.4f})")
    if pearson(compression, t) and pearson(compression, t) > 0.85:
        test.fail(f"Compression metric time-correlated ({pearson(compression, t):.4f})")
    if monotonic_fraction(froth) > 0.85:
        test.fail("Froth metric mostly monotonic — engineered curve.")
    test.statistics = {
        "frothTimeCorr": pearson(froth, t),
        "compressionTimeCorr": pearson(compression, t),
        "frothFrontierCorr": pearson(froth, frontier),
        "frothMonotonicFraction": monotonic_fraction(froth),
    }
    if test.verdict != VERDICT_FAIL:
        test.verdict = VERDICT_PASS
    return test


def test_hidden_target(solver: Any, steps: int, seed: int) -> HostileTestResult:
    test = HostileTestResult("hidden_target_audit", VERDICT_PASS, "live_movement")
    truth = GEOMETRY_CASES["sun_in_1_polygon"]()
    result = run_solver(solver, truth=truth, init_distribution="uniform", steps=steps, seed=seed)
    histories = result.get("particleHistoriesByStep")
    if not histories:
        test.unproven("No particleHistoriesByStep — cannot measure oracle-distance correlation.")
        return test

    # Early-stage alignment to oracle boundary vs frontier cells
    early_steps = histories[: max(3, len(histories) // 5)]
    oracle_alignments: list[float] = []
    frontier_alignments: list[float] = []
    ring = project_ring([[c[0], c[1]] for c in load_sun_polygon_rings()[0]])

    def dist_to_ring(x: float, y: float) -> float:
        best = float("inf")
        for i in range(len(ring)):
            x1, y1 = ring[i]
            x2, y2 = ring[(i + 1) % len(ring)]
            best = min(best, _point_segment_dist(x, y, x1, y1, x2, y2))
        return best

    for step_hist in early_steps:
        particles = step_hist if isinstance(step_hist, list) else step_hist.get("particles", [])
        for p in particles:
            vx = float(p.get("vx", 0))
            vy = float(p.get("vy", 0))
            speed = math.hypot(vx, vy)
            if speed < 1e-9:
                continue
            dx = vx / speed
            dy = vy / speed
            ox = float(p.get("x", 0))
            oy = float(p.get("y", 0))
            oracle_alignments.append(abs(dx * _normalize(-(ox - 160)) + dy * _normalize(-(oy - 120))))
            if p.get("targetReason") == "frontier_pressure":
                frontier_alignments.append(1.0)

    if oracle_alignments and statistics.mean(oracle_alignments) > 0.75:
        test.fail("Early movement correlates with oracle geometry vector — hidden target field.")
    test.statistics = {
        "earlyOracleAlignmentMean": statistics.mean(oracle_alignments) if oracle_alignments else None,
        "frontierTargetFraction": len(frontier_alignments) / max(1, len(oracle_alignments)),
    }
    if test.verdict not in (VERDICT_FAIL, VERDICT_UNPROVEN):
        test.verdict = VERDICT_PASS
    return test


def _point_segment_dist(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
    vx = x2 - x1
    vy = y2 - y1
    wx = px - x1
    wy = py - y1
    c1 = vx * wx + vy * wy
    c2 = vx * vx + vy * vy
    t = max(0.0, min(1.0, c1 / (c2 + 1e-15)))
    projx = x1 + t * vx
    projy = y1 + t * vy
    return math.hypot(px - projx, py - projy)


def _normalize(v: float) -> float:
    return max(-1.0, min(1.0, v / 100.0))


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------


def overall_verdict(tests: list[HostileTestResult]) -> str:
    if any(t.verdict == VERDICT_FAIL for t in tests):
        return VERDICT_FAIL
    if any(t.verdict == VERDICT_UNPROVEN for t in tests):
        return VERDICT_UNPROVEN
    return VERDICT_PASS


def build_report_payload(
    *,
    solver_module: str | None,
    solver_available: bool,
    baseline_metrics_path: Path | None,
    tests: list[HostileTestResult],
) -> dict[str, Any]:
    fails = [t for t in tests if t.verdict == VERDICT_FAIL]
    unproven = [t for t in tests if t.verdict == VERDICT_UNPROVEN]

    against_emergence = []
    for t in tests:
        against_emergence.extend(t.failures)
    for t in tests:
        if "monotonic" in " ".join(t.failures).lower():
            against_emergence.append(f"{t.name}: monotonic/time-shaped metrics")
        if "cliff" in " ".join(t.failures).lower():
            against_emergence.append(f"{t.name}: synchronized cliff transitions")

    for_emergence = [t.note for t in tests if t.verdict == VERDICT_PASS]

    return {
        "phase": "3.29_hostile_solver_validation",
        "target": "Phase 3.28 mechanics (metrics-only prototype)",
        "solverModule": solver_module,
        "solverAvailable": solver_available,
        "baselineMetricsPath": str(baseline_metrics_path) if baseline_metrics_path else None,
        "overallVerdict": overall_verdict(tests),
        "emergentClaimSupported": False,
        "tests": [
            {
                "name": t.name,
                "verdict": t.verdict,
                "mode": t.mode,
                "evidence": t.evidence,
                "failures": t.failures,
                "statistics": t.statistics,
            }
            for t in tests
        ],
        "strongestEvidenceAgainstEmergence": against_emergence[:20],
        "strongestEvidenceForEmergence": for_emergence[:20],
        "suspiciousBehaviors": [
            "Archived baseline shows global abandonment cliff at step 11",
            "Froth metric monotonic growth with late plateau in archived run",
            "Compression metric staircase plateaus in archived run",
            "maxFrontierPressure saturates to 1.0 early in archived run",
            "convergenceReached=false in archived acceptance run",
            "End-state particle velocities near zero after large displacement (sample)",
        ],
        "likelyFakeEmergenceMechanisms": [
            "Time-shaped metric curves independent of geometry (if reproduced across shapes)",
            "Global abandonment synchronization",
            "Metric saturation ceilings (frontier pressure -> 1.0)",
            "Acceptance-pass despite non-convergence",
            "Movement then freeze pattern (high displacement, ~0 terminal velocity)",
        ],
        "summary": {
            "failCount": len(fails),
            "unprovenCount": len(unproven),
            "passCount": sum(1 for t in tests if t.verdict == VERDICT_PASS),
            "liveSolverRequiredForFullAudit": not solver_available,
        },
    }


def write_markdown_report(payload: dict[str, Any], path: Path) -> None:
    lines = [
        "# Phase 3.29 Hostile Solver Validation",
        "",
        f"Overall verdict: **{payload['overallVerdict']}**",
        f"Emergent claim supported: **{payload['emergentClaimSupported']}**",
        "",
        f"Solver module: `{payload.get('solverModule')}`",
        f"Solver available: `{payload.get('solverAvailable')}`",
        "",
        "## Test Verdicts",
        "",
        "| Test | Verdict | Mode |",
        "|---|---|---|",
    ]
    for t in payload["tests"]:
        lines.append(f"| {t['name']} | {t['verdict']} | {t['mode']} |")
    lines.extend(
        [
            "",
            "## Strongest Evidence Against Emergence",
            "",
        ]
    )
    for item in payload.get("strongestEvidenceAgainstEmergence", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Strongest Evidence For Emergence", ""])
    for item in payload.get("strongestEvidenceForEmergence", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Suspicious Behaviors", ""])
    for item in payload.get("suspiciousBehaviors", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Likely Fake-Emergence Mechanisms", ""])
    for item in payload.get("likelyFakeEmergenceMechanisms", []):
        lines.append(f"- {item}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Phase 3.29 hostile solver validation")
    parser.add_argument("--solver-module", default=DEFAULT_SOLVER_MODULE)
    parser.add_argument("--baseline-metrics", default=str(DEFAULT_BASELINE_METRICS))
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--seed", type=int, default=328)
    parser.add_argument("--json-out", default=str(ROOT / "validation/reports/phase3_29_hostile_solver_validation.json"))
    parser.add_argument("--md-out", default=str(ROOT / "CURSOR_EXPORT_PHASE_3_29_HOSTILE_VALIDATION.md"))
    args = parser.parse_args(argv)

    solver = load_solver(args.solver_module)
    solver_available = solver is not None

    baseline_path = Path(args.baseline_metrics)
    baseline_metrics = None
    if baseline_path.exists():
        baseline_metrics = json.loads(baseline_path.read_text(encoding="utf-8"))

    tests: list[HostileTestResult] = []

    if solver_available:
        tests.extend(
            [
                test_geometry_variation(solver, args.steps, args.seed),
                test_randomized_initial_distribution(solver, args.steps, args.seed),
                test_drift_vs_convergence(solver, args.steps, args.seed),
                test_frontier_authenticity(solver, args.steps, args.seed),
                test_abandonment_virga(solver, args.steps, args.seed),
                test_time_dependence(solver, args.steps, args.seed),
                test_metric_correlation(solver, args.steps, args.seed),
                test_hidden_target(solver, args.steps, args.seed),
            ]
        )
    elif baseline_metrics:
        retro = retrospective_from_metrics(baseline_metrics)
        tests = list(retro.values())
        blocker = HostileTestResult("solver_availability", VERDICT_FAIL, "blocker")
        blocker.fail(
            f"Phase 3.28 solver module `{args.solver_module}` not importable. "
            "Live multi-geometry hostile tests could not run."
        )
        tests.insert(0, blocker)
    else:
        blocker = HostileTestResult("solver_availability", VERDICT_FAIL, "blocker")
        blocker.fail("No solver module and no baseline metrics JSON found.")
        tests = [blocker]

    payload = build_report_payload(
        solver_module=args.solver_module,
        solver_available=solver_available,
        baseline_metrics_path=baseline_path if baseline_path.exists() else None,
        tests=tests,
    )

    json_out = Path(args.json_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    write_markdown_report(payload, Path(args.md_out))

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["overallVerdict"] == VERDICT_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
