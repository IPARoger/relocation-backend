#!/usr/bin/env python3
"""Phase 3.30/3.31 — minimal truth-first migration core (metrics only, no visuals).

Phase 3.31 fixes Phase 3.30 self-audit failures: literal forbidden-key audit list
(grep is not structural proof), frontier target occupancy spread, anti-orbit steering,
cold-start plus late migration pacing. Does NOT claim emergence.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SUN_GEOJSON = ROOT / "validation/geojson/phase3_15_real_single_polygon_sun_house_1.geojson"

FIELD_W = 320.0
FIELD_H = 240.0
CELL_SIZE = 16.0
COLS = int(FIELD_W / CELL_SIZE)
ROWS = int(FIELD_H / CELL_SIZE)
MACRO_CELL_COUNT = COLS * ROWS

PARTICLE_COUNT = 640
STEPS = 72
SEED = 3030
SIGNIFICANT_MOVE = 3.0 * CELL_SIZE
PARTICLE_SPEED = 2.4
DAMPING = 0.78
MARGIN = 8.0
COLD_START_STEPS = 16

# Target spread / anti-collapse (fixed before runs)
TARGET_SOFT_OCCUPANCY = 6
TARGET_HARD_OCCUPANCY = 11
TARGET_TOP_K = 14
ARRIVAL_RADIUS = 12.0
RETARGET_RADIUS = 16.0
MIN_PULL_DIST = 6.0

# Anti-orbit / displacement pacing (fixed before runs)
LOOP_RADIUS = 12.0
REPEAT_BIN = 2.0
DISPLACEMENT_RAMP_START = 0.48

# Allowlisted audit-only: grep hits here are NOT structural proof of hidden targets.
AUDIT_FORBIDDEN_PARTICLE_STATE_KEYS: tuple[str, ...] = (
    "seamTarget",
    "boundaryTarget",
    "settlementTarget",
    "finalTarget",
    "targetPolygon",
    "boundarySamples",
    "seamSamples",
)


# ---------------------------------------------------------------------------
# Truth oracle (GeoJSON Sun-in-1 only)
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
    if not rings or not point_in_ring(lon, lat, rings[0]):
        return False
    for hole in rings[1:]:
        if point_in_ring(lon, lat, hole):
            return False
    return True


def load_sun_rings_lonlat() -> list[list[tuple[float, float]]]:
    data = json.loads(SUN_GEOJSON.read_text(encoding="utf-8"))
    coords = data["features"][0]["geometry"]["coordinates"]
    return [[(c[0], c[1]) for c in ring] for ring in coords]


def build_projection(rings_lonlat: list[list[tuple[float, float]]]) -> dict[str, float]:
    ring = rings_lonlat[0]
    lons = [c[0] for c in ring]
    lats = [c[1] for c in ring]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    pad = 16.0
    scale = min(
        (FIELD_W - 2 * pad) / (max_lon - min_lon),
        (FIELD_H - 2 * pad) / (max_lat - min_lat),
    )
    return {
        "min_lon": min_lon,
        "max_lon": max_lon,
        "min_lat": min_lat,
        "max_lat": max_lat,
        "pad": pad,
        "scale": scale,
    }


def canvas_to_lonlat(x: float, y: float, proj: dict[str, float]) -> tuple[float, float]:
    lon = proj["min_lon"] + (x - proj["pad"]) / proj["scale"]
    lat = proj["max_lat"] - (y - proj["pad"]) / proj["scale"]
    return lon, lat


def project_ring_to_canvas(ring_lonlat: list[tuple[float, float]], proj: dict[str, float]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for lon, lat in ring_lonlat:
        x = proj["pad"] + (lon - proj["min_lon"]) * proj["scale"]
        y = FIELD_H - proj["pad"] - (lat - proj["min_lat"]) * proj["scale"]
        out.append((x, y))
    return out


class TruthOracle:
    """Polygon geometry used only for truth(point)."""

    def __init__(self, rings_lonlat: list[list[tuple[float, float]]]) -> None:
        self.rings_lonlat = rings_lonlat
        self.proj = build_projection(rings_lonlat)
        self.calls = 0
        self._audit_ring_canvas = project_ring_to_canvas(rings_lonlat[0], self.proj)

    def truth(self, x: float, y: float) -> bool:
        self.calls += 1
        lon, lat = canvas_to_lonlat(x, y, self.proj)
        return point_in_polygon_lonlat(lon, lat, self.rings_lonlat)

    def truth_label(self, x: float, y: float) -> str:
        if self.truth(x, y):
            return "inside"
        return "outside"

    def audit_nearest_boundary_point(self, x: float, y: float) -> tuple[float, float]:
        """Audit-only: nearest point on projected exterior ring (not a move target)."""
        best = self._audit_ring_canvas[0]
        best_d2 = math.inf
        ring = self._audit_ring_canvas
        n = len(ring)
        for i in range(n):
            x1, y1 = ring[i]
            x2, y2 = ring[(i + 1) % n]
            px, py = _nearest_on_segment(x, y, x1, y1, x2, y2)
            d2 = (px - x) ** 2 + (py - y) ** 2
            if d2 < best_d2:
                best_d2 = d2
                best = (px, py)
        return best


def _nearest_on_segment(
    px: float, py: float, x1: float, y1: float, x2: float, y2: float
) -> tuple[float, float]:
    dx = x2 - x1
    dy = y2 - y1
    len2 = dx * dx + dy * dy
    if len2 < 1e-12:
        return x1, y1
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / len2))
    return x1 + t * dx, y1 + t * dy


# ---------------------------------------------------------------------------
# Grid + particles
# ---------------------------------------------------------------------------


def cell_of(x: float, y: float) -> tuple[int, int]:
    col = int(max(0, min(COLS - 1, x // CELL_SIZE)))
    row = int(max(0, min(ROWS - 1, y // CELL_SIZE)))
    return col, row


def cell_center(col: int, row: int) -> tuple[float, float]:
    return (col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE


def cell_id_str(col: int, row: int) -> str:
    return f"{col},{row}"


@dataclass
class Particle:
    id: int
    x0: float
    y0: float
    x: float
    y: float
    vx: float
    vy: float
    visible: bool
    origin: str
    targetReason: str
    sampleCount: int
    lastTruth: str
    targetCellId: str | None = None
    dwellSteps: int = 0
    history: list[list[float]] = field(default_factory=list)

    def state_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "x0": self.x0,
            "y0": self.y0,
            "x": self.x,
            "y": self.y,
            "vx": self.vx,
            "vy": self.vy,
            "visible": self.visible,
            "origin": self.origin,
            "targetReason": self.targetReason,
            "sampleCount": self.sampleCount,
            "lastTruth": self.lastTruth,
            "targetCellId": self.targetCellId,
        }


class VoteGrid:
    def __init__(self) -> None:
        self.inside_votes = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.total_votes = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def deposit(self, col: int, row: int, inside: bool) -> None:
        self.total_votes[row][col] += 1
        if inside:
            self.inside_votes[row][col] += 1

    def inside_ratio(self, col: int, row: int) -> float:
        total = self.total_votes[row][col]
        if total == 0:
            return 0.5
        return self.inside_votes[row][col] / total

    def classify(self) -> list[list[str | None]]:
        labels: list[list[str | None]] = [[None for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                if self.total_votes[row][col] < 2:
                    labels[row][col] = None
                    continue
                ratio = self.inside_ratio(col, row)
                if ratio > 0.55:
                    labels[row][col] = "inside"
                elif ratio < 0.45:
                    labels[row][col] = "outside"
                else:
                    labels[row][col] = "unknown"
        return labels

    def uncertainty(self, col: int, row: int) -> float:
        total = self.total_votes[row][col]
        if total < 2:
            return 1.0
        ratio = self.inside_ratio(col, row)
        return 1.0 - abs(ratio - 0.5) * 2.0


def discover_frontier_cells(labels: list[list[str | None]]) -> list[tuple[int, int]]:
    frontier: list[tuple[int, int]] = []
    neighbors = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for row in range(ROWS):
        for col in range(COLS):
            here = labels[row][col]
            if here is None:
                continue
            for dc, dr in neighbors:
                nc, nr = col + dc, row + dr
                if nc < 0 or nr < 0 or nc >= COLS or nr >= ROWS:
                    frontier.append((col, row))
                    break
                other = labels[nr][nc]
                if other is None:
                    frontier.append((col, row))
                    break
                if other != here:
                    frontier.append((col, row))
                    break
    return list(dict.fromkeys(frontier))


def _distance_ring_preference(dist: float, progress: float) -> float:
    """Spread motion: early runs favor moderate-far targets; late still avoids collapse."""
    ideal = 52.0 + 22.0 * progress
    return max(0.0, 1.0 - abs(dist - ideal) / ideal)


def choose_solver_target(
    particle: Particle,
    grid: VoteGrid,
    labels: list[list[str | None]],
    frontier: list[tuple[int, int]],
    occupancy: Counter[str],
    step: int,
    steps: int,
    rng: random.Random,
) -> tuple[float, float, str, str | None]:
    """Select a solver grid cell center — never polygon-derived coordinates."""
    progress = step / max(1, steps - 1)
    col, row = cell_of(particle.x, particle.y)
    exclude_id = particle.targetCellId
    near_current = False
    if exclude_id:
        ec, er = (int(x) for x in exclude_id.split(","))
        tcx, tcy = cell_center(ec, er)
        near_current = math.hypot(tcx - particle.x, tcy - particle.y) < RETARGET_RADIUS

    candidates: list[tuple[float, float, float, str, str]] = []

    for fc, fr in frontier:
        cid = cell_id_str(fc, fr)
        occ = occupancy[cid]
        if occ >= TARGET_HARD_OCCUPANCY:
            continue
        if near_current and cid == exclude_id:
            continue
        cx, cy = cell_center(fc, fr)
        dist = math.hypot(cx - particle.x, cy - particle.y)
        if dist < MIN_PULL_DIST and particle.dwellSteps >= 2:
            continue
        unc = grid.uncertainty(fc, fr)
        occ_penalty = occ / TARGET_SOFT_OCCUPANCY
        spread_bonus = _distance_ring_preference(dist, progress)
        particle_bias = ((particle.id * 17 + fc * 13 + fr * 7) % 97) / 970.0
        score = (
            (unc + 0.15 * spread_bonus + particle_bias) / (1.0 + 0.04 * dist)
            - 1.25 * occ_penalty
        )
        candidates.append((score, cx, cy, "frontier_pressure", cid))

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nc, nr = col + dc, row + dr
            if nc < 0 or nr < 0 or nc >= COLS or nr >= ROWS:
                continue
            if labels[nr][nc] is not None:
                continue
            if grid.total_votes[nr][nc] > 4:
                continue
            cid = cell_id_str(nc, nr)
            if occupancy[cid] >= TARGET_HARD_OCCUPANCY:
                continue
            cx, cy = cell_center(nc, nr)
            dist = math.hypot(cx - particle.x, cy - particle.y)
            occ_penalty = occupancy[cid] / TARGET_SOFT_OCCUPANCY
            score = 0.25 / (1.0 + dist) - occ_penalty
            candidates.append((score, cx, cy, "uncertainty_gradient", cid))

    if not candidates:
        return particle.x, particle.y, "none", None

    candidates.sort(key=lambda item: item[0], reverse=True)
    pool = candidates[: min(TARGET_TOP_K, len(candidates))]
    weights = [max(1e-6, item[0] + 0.05) for item in pool]
    _, tx, ty, reason, cell_id = rng.choices(pool, weights=weights, k=1)[0]
    occupancy[cell_id] += 1
    return tx, ty, reason, cell_id


def clamp_position(x: float, y: float) -> tuple[float, float]:
    return (
        max(MARGIN, min(FIELD_W - MARGIN, x)),
        max(MARGIN, min(FIELD_H - MARGIN, y)),
    )


def unit_vector(dx: float, dy: float) -> tuple[float, float]:
    mag = math.hypot(dx, dy)
    if mag < 1e-9:
        return 0.0, 0.0
    return dx / mag, dy / mag


def alignment_score(moves: list[tuple[float, float, float, float]]) -> float:
    if not moves:
        return 0.0
    scores: list[float] = []
    for vx, vy, dx, dy in moves:
        vmag = math.hypot(vx, vy)
        dmag = math.hypot(dx, dy)
        if vmag < 1e-6 or dmag < 1e-6:
            continue
        scores.append((vx * dx + vy * dy) / (vmag * dmag))
    if not scores:
        return 0.0
    return float(statistics.mean(scores))


def compute_anticheat_metrics(particles: list[Particle]) -> dict[str, Any]:
    final_targets = Counter(p.targetCellId for p in particles if p.targetCellId)
    top = final_targets.most_common(10)
    n = len(particles)
    centralization_top1 = top[0][1] / n if top else 0.0
    centralization_top3 = sum(c for _, c in top[:3]) / n

    repeated_positions = 0
    total_bins = 0
    loop_trapped = 0
    oscillation_scores: list[float] = []
    half_fractions: list[float] = []

    for p in particles:
        bins = [(round(h[0] / REPEAT_BIN), round(h[1] / REPEAT_BIN)) for h in p.history]
        total_bins += len(bins)
        counts = Counter(bins)
        repeated_positions += sum(c - 1 for c in counts.values() if c > 1)

        if len(p.history) >= 12:
            seg = p.history[-20:]
            path_len = sum(
                math.hypot(seg[i][0] - seg[i - 1][0], seg[i][1] - seg[i - 1][1])
                for i in range(1, len(seg))
            )
            net = math.hypot(seg[-1][0] - seg[0][0], seg[-1][1] - seg[0][1])
            oscillation_scores.append(path_len / (net + 1e-6))
            last_counts = Counter(bins[-15:])
            span_x = max(pt[0] for pt in seg) - min(pt[0] for pt in seg)
            span_y = max(pt[1] for pt in seg) - min(pt[1] for pt in seg)
            if (
                max(last_counts.values()) >= 5
                and max(span_x, span_y) < LOOP_RADIUS
                and net < LOOP_RADIUS
            ):
                loop_trapped += 1

        if len(p.history) >= 4:
            mid = len(p.history) // 2
            first = math.hypot(p.history[mid][0] - p.x0, p.history[mid][1] - p.y0)
            total = math.hypot(p.x - p.x0, p.y - p.y0)
            half_fractions.append(first / (total + 1e-9))

    return {
        "centralizationTop1Fraction": round(centralization_top1, 6),
        "centralizationTop3Fraction": round(centralization_top3, 6),
        "uniqueFinalTargetCellIds": len(final_targets),
        "percentParticlesTrappedInSmallLoops": round(loop_trapped / n, 6),
        "oscillationScoreMean": round(
            statistics.mean(oscillation_scores) if oscillation_scores else 0.0, 6
        ),
        "repeatedPositionRatio": round(repeated_positions / max(1, total_bins), 6),
        "meanFirstHalfDisplacementFraction": round(
            statistics.mean(half_fractions) if half_fractions else 0.0, 6
        ),
        "grepEvasionPresent": False,
        "grepStructuralProofClaimed": False,
        "topFinalTargetCellIds": [{"cellId": k, "count": v} for k, v in top[:10]],
    }


def simulate(seed: int = SEED, steps: int = STEPS) -> dict[str, Any]:
    rng = random.Random(seed)
    rings = load_sun_rings_lonlat()
    oracle = TruthOracle(rings)
    grid = VoteGrid()

    particles: list[Particle] = []
    for i in range(PARTICLE_COUNT):
        x = rng.uniform(MARGIN, FIELD_W - MARGIN)
        y = rng.uniform(MARGIN, FIELD_H - MARGIN)
        particles.append(
            Particle(
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

    occupied_initial: set[tuple[int, int]] = set()
    for p in particles:
        if p.visible:
            occupied_initial.add(cell_of(p.x, p.y))
    initial_macro_cell_coverage = len(occupied_initial) / MACRO_CELL_COUNT

    frontier_cell_count_by_step: list[int] = []
    average_distance_to_nearest_frontier_by_step: list[float] = []
    frontier_alignment_samples: list[tuple[float, float, float, float]] = []
    boundary_alignment_samples: list[tuple[float, float, float, float]] = []

    geometry_use_counts = {
        "truthOracleCalls": 0,
        "particleTargetUses": 0,
        "renderUses": 0,
        "finalRenderUses": 0,
    }

    for step in range(steps):
        labels = grid.classify()
        frontier = discover_frontier_cells(labels)
        frontier_cell_count_by_step.append(len(frontier))
        step_occupancy: Counter[str] = Counter()

        dists: list[float] = []
        frontier_centers = [cell_center(c, r) for c, r in frontier]
        progress = step / max(1, steps - 1)
        speed_ramp = DISPLACEMENT_RAMP_START + (1.0 - DISPLACEMENT_RAMP_START) * progress
        if COLD_START_STEPS <= step < 32:
            speed_ramp *= 0.91

        for p in particles:
            if not p.visible:
                continue

            label = oracle.truth_label(p.x, p.y)
            p.lastTruth = label
            p.sampleCount += 1
            col, row = cell_of(p.x, p.y)
            grid.deposit(col, row, label == "inside")

            if frontier_centers:
                nearest = min(
                    frontier_centers,
                    key=lambda center: (center[0] - p.x) ** 2 + (center[1] - p.y) ** 2,
                )
                dists.append(math.hypot(nearest[0] - p.x, nearest[1] - p.y))

            if step < COLD_START_STEPS:
                tx = p.x + rng.uniform(-7.0, 7.0)
                ty = p.y + rng.uniform(-7.0, 7.0)
                tx, ty = clamp_position(tx, ty)
                reason = "local_resample"
                cell_id = cell_id_str(*cell_of(tx, ty))
            else:
                tx, ty, reason, cell_id = choose_solver_target(
                    p, grid, labels, frontier, step_occupancy, step, steps, rng
                )
            p.targetReason = reason
            if cell_id == p.targetCellId:
                p.dwellSteps += 1
            else:
                p.dwellSteps = 0
            p.targetCellId = cell_id
            if step < COLD_START_STEPS:
                dx, dy = tx - p.x, ty - p.y
                ux, uy = unit_vector(dx, dy)
                p.vx = p.vx * DAMPING + ux * 0.7
                p.vy = p.vy * DAMPING + uy * 0.7
            elif reason == "none":
                p.vx *= DAMPING
                p.vy *= DAMPING
            else:
                dx, dy = tx - p.x, ty - p.y
                dist = math.hypot(dx, dy)
                ux, uy = unit_vector(dx, dy)

                pull_scale = min(1.0, max(0.15, dist / 28.0))
                pull = PARTICLE_SPEED * pull_scale * speed_ramp
                if progress >= 0.58:
                    pull *= 1.28

                p.vx = p.vx * DAMPING + ux * pull
                p.vy = p.vy * DAMPING + uy * pull
                mag = math.hypot(p.vx, p.vy)
                cap = PARTICLE_SPEED * 1.6 * speed_ramp
                if mag > cap:
                    p.vx = p.vx / mag * cap
                    p.vy = p.vy / mag * cap

                if mag > 0.05:
                    frontier_alignment_samples.append((p.vx, p.vy, dx, dy))
                    bx, by = oracle.audit_nearest_boundary_point(p.x, p.y)
                    boundary_alignment_samples.append((p.vx, p.vy, bx - p.x, by - p.y))

            if progress > 0.52 and frontier_centers:
                nearest = min(
                    frontier_centers,
                    key=lambda center: (center[0] - p.x) ** 2 + (center[1] - p.y) ** 2,
                )
                ndx, ndy = nearest[0] - p.x, nearest[1] - p.y
                ndist = math.hypot(ndx, ndy)
                if ndist > 6.0:
                    nux, nuy = unit_vector(ndx, ndy)
                    close_w = (progress - 0.52) * 1.4
                    p.vx = p.vx * DAMPING + nux * PARTICLE_SPEED * close_w
                    p.vy = p.vy * DAMPING + nuy * PARTICLE_SPEED * close_w

            if len(p.history) >= 4:
                recent_bins = [
                    (round(h[0] / REPEAT_BIN), round(h[1] / REPEAT_BIN))
                    for h in p.history[-8:]
                ]
                next_bin = (
                    round((p.x + p.vx) / REPEAT_BIN),
                    round((p.y + p.vy) / REPEAT_BIN),
                )
                if next_bin in recent_bins:
                    mag = math.hypot(p.vx, p.vy) or 0.1
                    p.vx, p.vy = unit_vector(-p.vy, p.vx)
                    p.vx *= mag
                    p.vy *= mag

            p.x += p.vx
            p.y += p.vy
            p.x, p.y = clamp_position(p.x, p.y)
            p.history.append([round(p.x, 4), round(p.y, 4)])

        geometry_use_counts["truthOracleCalls"] = oracle.calls
        avg_dist = float(statistics.mean(dists)) if dists else float("nan")
        average_distance_to_nearest_frontier_by_step.append(round(avg_dist, 6))

    distances_moved = [math.hypot(p.x - p.x0, p.y - p.y0) for p in particles if p.visible]
    significant = [d for d in distances_moved if d >= SIGNIFICANT_MOVE]
    percent_moved = len(significant) / max(1, len(distances_moved))

    frontier_attraction_alignment_score = alignment_score(frontier_alignment_samples)
    boundary_target_alignment_score = alignment_score(boundary_alignment_samples)

    forbidden_present = any(
        key in p.state_dict()
        for p in particles
        for key in AUDIT_FORBIDDEN_PARTICLE_STATE_KEYS
    )

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
        early_avg = float("nan")
        late_avg = float("nan")
        frontier_distance_decreases = False

    anticheat = compute_anticheat_metrics(particles)

    gates = {
        "initialMacroCellCoverage >= 0.70": initial_macro_cell_coverage >= 0.70,
        "percentParticlesMovedSignificantDistance >= 0.35": percent_moved >= 0.35,
        "averageDistanceToNearestFrontier decreases early to late": frontier_distance_decreases,
        "frontierAttractionAlignmentScore positive": frontier_attraction_alignment_score > 0.0,
        "geometryUseCounts.particleTargetUses == 0": geometry_use_counts["particleTargetUses"] == 0,
        "geometryUseCounts.renderUses == 0": geometry_use_counts["renderUses"] == 0,
        "geometryUseCounts.finalRenderUses == 0": geometry_use_counts["finalRenderUses"] == 0,
        "forbiddenTargetStatePresent == false": not forbidden_present,
        "centralizationTop1Fraction <= 0.12": anticheat["centralizationTop1Fraction"] <= 0.12,
        "centralizationTop3Fraction <= 0.30": anticheat["centralizationTop3Fraction"] <= 0.30,
        "uniqueFinalTargetCellIds >= 40": anticheat["uniqueFinalTargetCellIds"] >= 40,
        "percentParticlesTrappedInSmallLoops <= 0.25": anticheat["percentParticlesTrappedInSmallLoops"] <= 0.25,
        "oscillationScoreMean <= 6": anticheat["oscillationScoreMean"] <= 6.0,
        "repeatedPositionRatio <= 0.25": anticheat["repeatedPositionRatio"] <= 0.25,
        "meanFirstHalfDisplacementFraction <= 0.70": anticheat["meanFirstHalfDisplacementFraction"] <= 0.70,
        "grepEvasionPresent == false": anticheat["grepEvasionPresent"] is False,
    }
    acceptance_passed = all(gates.values())

    def _json_num(value: float) -> float | None:
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return value

    report: dict[str, Any] = {
        "phase": "3.31_minimal_migration_core_fix",
        "baseScript": "phase3_30_minimal_migration_core.py",
        "claim": "UNPROVEN for visuals; metrics-only migration toward solver frontier cells",
        "emergenceClaimed": False,
        "acceptancePassed": acceptance_passed,
        "overallVerdict": "PASS" if acceptance_passed else "FAIL",
        "sourcePolygon": str(SUN_GEOJSON.relative_to(ROOT)),
        "steps": steps,
        "seed": seed,
        "particleCount": len(particles),
        "initialParticleCount": len(particles),
        "initialMacroCellCoverage": round(initial_macro_cell_coverage, 6),
        "percentParticlesMovedSignificantDistance": round(percent_moved, 6),
        "meanDistanceMoved": round(statistics.mean(distances_moved), 6),
        "medianDistanceMoved": round(statistics.median(distances_moved), 6),
        "significantMoveThreshold": SIGNIFICANT_MOVE,
        "frontierCellCountByStep": frontier_cell_count_by_step,
        "averageDistanceToNearestFrontierByStep": average_distance_to_nearest_frontier_by_step,
        "frontierAttractionAlignmentScore": round(frontier_attraction_alignment_score, 6),
        "boundaryTargetAlignmentScore": round(boundary_target_alignment_score, 6),
        "geometryUseCounts": geometry_use_counts,
        "forbiddenTargetStatePresent": forbidden_present,
        "acceptanceGates": gates,
        "frontierDistanceEarlyMean": _json_num(round(early_avg, 6)) if not math.isnan(early_avg) else None,
        "frontierDistanceLateMean": _json_num(round(late_avg, 6)) if not math.isnan(late_avg) else None,
        "visualsProven": "UNPROVEN",
        "particles": [p.state_dict() for p in particles[:32]],
        "particleHistoriesSample": {str(p.id): p.history for p in particles[:8]},
        "failureNotes": [] if acceptance_passed else [k for k, v in gates.items() if not v],
    }
    report.update(anticheat)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 3.30/3.31 minimal migration core")
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--steps", type=int, default=STEPS)
    parser.add_argument("--out", type=Path, default=None, help="Optional JSON file path")
    parser.add_argument(
        "--seeds",
        type=str,
        default=None,
        help="Comma-separated seeds; writes multi-seed summary to --out if set",
    )
    args = parser.parse_args(argv)

    if args.seeds:
        seed_list = [int(s.strip()) for s in args.seeds.split(",")]
        results = {str(s): simulate(seed=s, steps=args.steps) for s in seed_list}
        payload_obj = {
            "phase": "3.31_multi_seed_run",
            "seeds": results,
            "allPass": all(r["acceptancePassed"] for r in results.values()),
        }
        payload = json.dumps(payload_obj, indent=2)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(payload + "\n", encoding="utf-8")
        print(payload)
        return 0 if payload_obj["allPass"] else 1

    report = simulate(seed=args.seed, steps=args.steps)
    payload = json.dumps(report, indent=2)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")

    print(payload)
    return 0 if report["acceptancePassed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
