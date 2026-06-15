"""
ARCHAEOLOGY / DEBUG POC — not the canonical production rendering substrate.

Scalar aspect aura field — truth-sampled orb distance grid (PoC: Sun
conjunct ASC). Retained for Phase A/B validation history, regression
comparison, and debug-only inspection. The Phase-C production path is the
adaptive screen-space truth substrate documented in
docs/PHASE_C_RENDERING_ARCHITECTURE.md and migrated via
docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md.

No cosmetic smoothing: strength = max(0, 1 - orb_deg / max_orb) from
relocated-chart angle evaluation at each geographic sample.
"""

from __future__ import annotations

import heapq
import time
from typing import Any

import numpy as np
import swisseph as swe

from truth_grid_engine import normalize_angle_sign_code

PRODUCT_LAT_CAP = 65.0

ASPECT_OFFSETS = {
    "conjunction": [0],
    "opposition": [180],
    "square": [90, 270],
    "trine": [120, 240],
    "sextile": [60, 300],
    "hard": [0, 90, 180, 270],
    "soft": [60, 120, 240, 300],
    "any": [0, 60, 90, 120, 180, 240, 270, 300],
}

PLANET_IDS = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO,
    "chiron": swe.CHIRON,
}

# PoC scope gate — do not generalize until doctrine validation passes.
AURA_POC_OVERLAY = {
    "planet": "sun",
    "aspect": "conjunction",
    "angle": "ASC",
}

# Phase A truth spine: uniform raster at paint resolution = reference truth.
# One swe.houses evaluation per displayed pixel; no interpolation between cells.
REFERENCE_TRUTH_ROLE = "uniform_one_sample_per_paint_pixel"
CONVERGENCE_DELTA_THRESHOLD = 0.05
# Depth 8 can regress when leaf budget truncates mid-subdivision (see convergence notes).
DEFAULT_ADAPTIVE_MAX_DEPTH = 6

# Phase B: refinement reveal stages — derived from real quadtree budgets, not timers.
REFINEMENT_REVEAL_STAGES: list[dict[str, Any]] = [
    {
        "stage_id": "coarse_world",
        "label": "Coarse world",
        "ordinal": 0,
        "initial_divisions": 4,
        "max_depth": 2,
        "max_samples": 8000,
        "provisional": True,
    },
    {
        "stage_id": "regional_refine",
        "label": "Regional refine",
        "ordinal": 1,
        "initial_divisions": 5,
        "max_depth": 4,
        "max_samples": 24000,
        "provisional": True,
    },
    {
        "stage_id": "boundary_refine",
        "label": "Boundary refine",
        "ordinal": 2,
        "initial_divisions": 6,
        "max_depth": 5,
        "max_samples": 60000,
        "provisional": True,
    },
    {
        "stage_id": "contour_stabilization",
        "label": "Contour stabilization",
        "ordinal": 3,
        "initial_divisions": 6,
        "max_depth": DEFAULT_ADAPTIVE_MAX_DEPTH,
        "max_samples": 120000,
        "provisional": False,
    },
]

REVEAL_TRANSPORT_VERSION = 1
REVEAL_MAX_TRUTH_SAMPLES = 4000
PENDING_REFINE_STOP_REASONS = frozenset(
    {"max_depth", "leaf_budget", "min_cell", "sample_budget"}
)


def signed_angle_diff(a: float, b: float) -> float:
    return ((a - b + 180) % 360) - 180


def is_aura_poc_overlay(aspect_overlay: dict | None) -> bool:
    if not aspect_overlay:
        return False
    planet = str(aspect_overlay.get("planet", "")).lower()
    aspect = str(aspect_overlay.get("aspect", "")).lower()
    angle = normalize_angle_sign_code(str(aspect_overlay.get("angle", "")))
    return (
        planet == AURA_POC_OVERLAY["planet"]
        and aspect == AURA_POC_OVERLAY["aspect"]
        and angle == AURA_POC_OVERLAY["angle"]
    )


def _angle_longitude_at_point(jd: float, lat: float, lon: float, angle: str) -> float | None:
    try:
        _, ascmc = swe.houses(jd, lat, lon, b"P")
        if angle == "ASC":
            return float(ascmc[0] % 360)
        if angle == "DC":
            return float((ascmc[0] + 180.0) % 360)
        if angle == "IC":
            return float((ascmc[1] + 180.0) % 360)
        if angle == "MC":
            return float(ascmc[1] % 360)
    except Exception:
        return None
    return None


def _poc_context(jd: float, aspect_overlay: dict) -> tuple[float, list[float], str, str, str]:
    if not is_aura_poc_overlay(aspect_overlay):
        raise ValueError(
            "Aura PoC supports only Sun conjunct ASC "
            f"(got {aspect_overlay})."
        )
    selected_planet = str(aspect_overlay["planet"]).lower()
    selected_angle = normalize_angle_sign_code(str(aspect_overlay["angle"]))
    selected_aspect = str(aspect_overlay["aspect"]).lower()
    planet_id = PLANET_IDS.get(selected_planet)
    if planet_id is None:
        raise ValueError(f"Unknown planet: {selected_planet}")
    planet_lon = float(swe.calc_ut(jd, planet_id)[0][0] % 360)
    offsets = ASPECT_OFFSETS.get(selected_aspect, [0])
    return planet_lon, offsets, selected_angle, selected_aspect, selected_planet


def orb_strength_at_point(
    jd: float,
    lat: float,
    lon: float,
    planet_lon: float,
    offsets: list[float],
    selected_angle: str,
    max_orb: float,
) -> tuple[float, float]:
    ang = _angle_longitude_at_point(jd, lat, lon, selected_angle)
    if ang is None:
        return 180.0, 0.0
    best_orb = 180.0
    for offset in offsets:
        target = (planet_lon + offset) % 360
        orb = abs(signed_angle_diff(ang, target))
        if orb < best_orb:
            best_orb = orb
    strength = max(0.0, 1.0 - best_orb / max_orb)
    return best_orb, strength


def _cell_ring(
    lon: float,
    lat: float,
    half_res: float,
    cap: float | None = PRODUCT_LAT_CAP,
) -> list[list[float]]:
    """Axis-aligned cell; optionally clipped to ±cap."""
    lon0 = lon - half_res
    lon1 = lon + half_res
    lat0 = lat - half_res
    lat1 = lat + half_res
    if cap is not None:
        lat0 = max(-cap, lat0)
        lat1 = min(cap, lat1)
    if lat0 >= lat1:
        return []
    return [
        [lon0, lat0],
        [lon1, lat0],
        [lon1, lat1],
        [lon0, lat1],
        [lon0, lat0],
    ]


def generate_aura_raster(
    jd: float,
    aspect_overlay: dict,
    north: float,
    south: float,
    west: float,
    east: float,
    width: int,
    height: int,
    max_orb: float = 6.0,
    apply_lat_cap: bool = True,
) -> dict[str, Any]:
    """Viewport raster: one truth sample per pixel cell (continuous strength, no banding)."""
    if width < 1 or height < 1:
        raise ValueError("width and height must be positive")
    if max_orb <= 0:
        raise ValueError("max_orb must be positive")

    planet_lon, offsets, selected_angle, selected_aspect, selected_planet = _poc_context(
        jd, aspect_overlay
    )
    started = time.perf_counter()
    cap = PRODUCT_LAT_CAP if apply_lat_cap else None
    strengths: list[float] = []
    orbs: list[float] = []
    sample_count = 0
    lat_span = north - south
    lon_span = east - west
    if lon_span <= 0:
        lon_span += 360.0

    for j in range(height):
        lat = north - (j + 0.5) * lat_span / height
        if cap is not None and abs(lat) > cap:
            strengths.extend([0.0] * width)
            continue
        for i in range(width):
            lon = west + (i + 0.5) * lon_span / width
            if lon > 180:
                lon -= 360
            if lon <= -180:
                lon += 360
            sample_count += 1
            best_orb, strength = orb_strength_at_point(
                jd, lat, lon, planet_lon, offsets, selected_angle, max_orb
            )
            if strength > 0:
                orbs.append(best_orb)
            strengths.append(round(strength, 5))

    elapsed = round(time.perf_counter() - started, 4)
    deg_per_px_lat = lat_span / height if height else None
    deg_per_px_lon = lon_span / width if width else None
    return {
        "width": width,
        "height": height,
        "bounds": {"north": north, "south": south, "west": west, "east": east},
        "strengths": strengths,
        "properties": {
            "aura_poc": True,
            "truth_spine_overlay": "sun_conjunct_asc",
            "reference_truth_role": REFERENCE_TRUTH_ROLE,
            "render_mode": "raster",
            "aspect_overlay": {
                "planet": selected_planet,
                "aspect": selected_aspect,
                "angle": selected_angle,
            },
            "max_orb": max_orb,
            "apply_lat_cap": apply_lat_cap,
            "lat_cap": PRODUCT_LAT_CAP if apply_lat_cap else None,
            "sample_count": sample_count,
            "nonzero_count": sum(1 for s in strengths if s > 0),
            "compute_seconds": elapsed,
            "deg_per_pixel_lat": round(deg_per_px_lat, 5) if deg_per_px_lat is not None else None,
            "deg_per_pixel_lon": round(deg_per_px_lon, 5) if deg_per_px_lon is not None else None,
            "strength_formula": "max(0, 1 - orb_deg / max_orb)",
            "strength_min": round(min(orbs), 4) if orbs else 0,
            "strength_max": round(max(0.0, 1.0 - min(orbs) / max_orb), 4) if orbs else 0,
        },
    }


# Adaptive refinement thresholds — coarse bands only (finer bands refine excessively).
AURA_ADAPTIVE_THRESHOLDS = (0.04, 0.4)


def _normalize_lon(lon: float) -> float:
    while lon > 180:
        lon -= 360
    while lon <= -180:
        lon += 360
    return lon


def _cell_fully_outside_lat_cap(south: float, north: float, cap: float) -> bool:
    return south > cap or north < -cap


def _lon_span_west_east(west: float, east: float) -> float:
    span = east - west
    return span + 360.0 if span <= 0 else span


def compute_convergence_vs_reference(
    adaptive_strengths: list[float],
    reference_strengths: list[float],
    delta_threshold: float = CONVERGENCE_DELTA_THRESHOLD,
) -> dict[str, Any]:
    """
    Compare adaptive paint raster to uniform reference at identical width×height.
    Mismatch above threshold remains visible — never smoothed away.
    """
    if len(adaptive_strengths) != len(reference_strengths):
        raise ValueError(
            f"strength length mismatch: adaptive={len(adaptive_strengths)} "
            f"reference={len(reference_strengths)}"
        )
    diffs = [abs(a - r) for a, r in zip(adaptive_strengths, reference_strengths)]
    n = len(diffs)
    over = sum(1 for d in diffs if d > delta_threshold)
    return {
        "reference_truth_role": REFERENCE_TRUTH_ROLE,
        "delta_threshold": delta_threshold,
        "paint_pixel_count": n,
        "mean_delta_vs_reference": round(sum(diffs) / n, 6) if n else 0.0,
        "max_delta_vs_reference": round(max(diffs), 6) if diffs else 0.0,
        "pixels_above_threshold": over,
        "pixels_above_threshold_pct": round(100.0 * over / n, 2) if n else 0.0,
        "converged": over == 0,
    }


def _aggregate_stop_reason(
    leaves: list[dict[str, Any]],
    *,
    sample_budget_hit: bool,
    leaf_budget_hit: bool,
    max_depth_reached: int,
    max_depth: int,
) -> str:
    """Top-level stop reason for the adaptive pass (inspectable, not cosmetic)."""
    if sample_budget_hit:
        return "sample_budget"
    if leaf_budget_hit:
        return "leaf_budget"
    if max_depth_reached >= max_depth:
        forced = sum(
            1
            for leaf in leaves
            if leaf.get("stop_reason") == "max_depth" and not leaf.get("stable")
        )
        if forced > 0:
            return "max_depth_with_pending_refinement"
    return "field_converged"


def get_refinement_reveal_stage(stage_id: str) -> dict[str, Any]:
    for stage in REFINEMENT_REVEAL_STAGES:
        if stage["stage_id"] == stage_id:
            return dict(stage)
    raise ValueError(
        f"Unknown refinement stage {stage_id!r}; "
        f"expected one of {[s['stage_id'] for s in REFINEMENT_REVEAL_STAGES]}"
    )


def classify_observed_refinement_stage(
    *,
    max_depth_reached: int,
    convergence: dict[str, Any] | None,
    leaves: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Infer which reveal stage the engine state most closely matches (post-pass).
    Uses depth, frontier pressure, and convergence — not wall-clock timing.
    """
    pending = sum(
        1
        for leaf in leaves
        if not leaf.get("stable")
        and leaf.get("stop_reason") in PENDING_REFINE_STOP_REASONS
    )
    converged = bool(convergence and convergence.get("converged"))
    if converged:
        stage_id = "contour_stabilization"
        derivation = "convergence_vs_reference.converged"
    elif max_depth_reached <= 0 and pending == 0:
        stage_id = "coarse_world"
        derivation = "max_depth_reached=0; stable coarse partition"
    elif max_depth_reached <= 2:
        stage_id = "regional_refine"
        derivation = f"max_depth_reached={max_depth_reached}; frontier={pending}"
    elif max_depth_reached <= 4:
        stage_id = "boundary_refine"
        derivation = f"max_depth_reached={max_depth_reached}; frontier={pending}"
    else:
        stage_id = "contour_stabilization"
        derivation = (
            f"max_depth_reached={max_depth_reached}; frontier={pending}; not yet converged"
        )
    cfg = get_refinement_reveal_stage(stage_id)
    return {
        "stage_id": stage_id,
        "label": cfg["label"],
        "ordinal": cfg["ordinal"],
        "provisional": not converged and cfg["provisional"],
        "derivation": derivation,
        "active_frontier_leaf_count": pending,
    }


def build_reveal_transport(
    *,
    leaves: list[dict[str, Any]],
    properties: dict[str, Any],
    requested_stage_id: str | None,
    convergence: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Inspectable stage snapshot for progressive reveal (no streaming theater).
    replace_prior_snapshot=True — client must replace, not stack, prior geometry.
    """
    observed = classify_observed_refinement_stage(
        max_depth_reached=int(properties.get("max_depth_reached", 0)),
        convergence=convergence,
        leaves=leaves,
    )
    requested: dict[str, Any] | None = None
    if requested_stage_id:
        cfg = get_refinement_reveal_stage(requested_stage_id)
        requested = {
            "stage_id": cfg["stage_id"],
            "label": cfg["label"],
            "ordinal": cfg["ordinal"],
            "provisional": cfg["provisional"],
            "max_depth_limit": cfg["max_depth"],
            "initial_divisions": cfg["initial_divisions"],
        }

    truth_samples: list[dict[str, Any]] = []
    for leaf in leaves:
        depth = int(leaf.get("depth", 0))
        for pt in leaf.get("truth_samples") or []:
            truth_samples.append({**pt, "leaf_depth": depth})
            if len(truth_samples) >= REVEAL_MAX_TRUTH_SAMPLES:
                break
        if len(truth_samples) >= REVEAL_MAX_TRUTH_SAMPLES:
            break

    frontier_features: list[dict[str, Any]] = []
    for leaf in leaves:
        if leaf.get("stable"):
            continue
        if leaf.get("stop_reason") not in PENDING_REFINE_STOP_REASONS:
            continue
        lw, ls, le, ln = leaf["west"], leaf["south"], leaf["east"], leaf["north"]
        frontier_features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[lw, ls], [le, ls], [le, ln], [lw, ln], [lw, ls]]],
                },
                "properties": {
                    "layer": "refinement_frontier",
                    "depth": leaf["depth"],
                    "stop_reason": leaf.get("stop_reason"),
                    "estimated_error": leaf.get("estimated_error", 0),
                },
            }
        )

    return {
        "transport_version": REVEAL_TRANSPORT_VERSION,
        "replace_prior_snapshot": True,
        "overlay_scope": "sun_conjunct_asc_poc_only",
        "requested_stage": requested,
        "observed_stage": observed,
        "engine_state": {
            "truth_sample_count": properties.get("truth_sample_count"),
            "cell_count": properties.get("cell_count"),
            "max_depth_reached": properties.get("max_depth_reached"),
            "max_depth_limit": properties.get("max_depth"),
            "stop_reason": properties.get("stop_reason"),
            "refine_trigger_counts": properties.get("refine_trigger_counts"),
            "depth_histogram": properties.get("depth_histogram"),
            "convergence_vs_reference": convergence,
            "sample_budget_hit": properties.get("sample_budget_hit"),
            "leaf_budget_hit": properties.get("leaf_budget_hit"),
        },
        "truth_samples": truth_samples,
        "truth_sample_count_reported": len(truth_samples),
        "truth_sample_truncated": sum(len(leaf.get("truth_samples") or []) for leaf in leaves)
        > REVEAL_MAX_TRUTH_SAMPLES,
        "frontier_cells": {
            "type": "FeatureCollection",
            "features": frontier_features,
        },
        "active_frontier_leaf_count": observed["active_frontier_leaf_count"],
    }


def _depth_regression_diagnostics(
    leaves: list[dict[str, Any]],
    *,
    leaf_budget_hit: bool,
    max_depth_reached: int,
    convergence: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Explain depth-8-style regression: truncated subdivision leaves heterogeneous
    leaf sizes; pixel inherits deepest leaf center strength, not per-pixel truth.
    """
    pending = sum(
        1
        for leaf in leaves
        if leaf.get("stop_reason") in ("max_depth", "sample_budget", "leaf_budget")
        and not leaf.get("stable")
    )
    budget_truncated = sum(1 for leaf in leaves if leaf.get("stop_reason") == "sample_budget")
    diag: dict[str, Any] = {
        "leaf_budget_hit": leaf_budget_hit,
        "max_depth_reached": max_depth_reached,
        "leaves_pending_refinement": pending,
        "leaves_stopped_sample_budget": budget_truncated,
        "regression_mechanism": (
            "leaf_budget_or_sample_budget truncates quadtree mid-band; "
            "sibling leaves at mismatched depths assign flat center strength to pixels "
            "that uniform reference samples at pixel center — increases maxΔ without blur."
        ),
    }
    if convergence and not convergence.get("converged") and leaf_budget_hit:
        diag["regression_likely"] = True
    elif convergence and convergence.get("converged"):
        diag["regression_likely"] = False
    return diag


def _refinement_reasons(
    corner_strengths: list[float],
    center_strength: float,
    gradient_tolerance: float,
    depth: int,
    min_strength: float = 0.04,
) -> list[str]:
    """
    Refine only when the scalar field (strength) is non-uniform or crosses bands.
    Raw orb corner deltas are NOT used — ASC orb changes quickly with position and
    would force global subdivision without improving strength fidelity.
    """
    reasons: list[str] = []
    all_s = corner_strengths + [center_strength]
    s_min = min(all_s)
    s_max = max(all_s)
    if s_max < min_strength:
        return reasons
    effective_tol = gradient_tolerance * (1.0 + depth * 0.18)
    if s_max - s_min > effective_tol:
        reasons.append("gradient")
    if max(abs(center_strength - c) for c in corner_strengths) > effective_tol:
        reasons.append("center_corner")
    if s_min == 0.0 and s_max > 0.0:
        reasons.append("orb_boundary")
    for threshold in AURA_ADAPTIVE_THRESHOLDS:
        below = any(s < threshold for s in all_s)
        above = any(s >= threshold for s in all_s)
        if below and above:
            reasons.append(f"threshold_{threshold}")
            break
    return reasons


def _subdivide_cell(
    west: float, south: float, east: float, north: float
) -> list[tuple[float, float, float, float]]:
    mid_lon = west + _lon_span_west_east(west, east) / 2.0
    if mid_lon > 180:
        mid_lon -= 360
    mid_lat = (south + north) / 2.0
    return [
        (west, south, mid_lon, mid_lat),
        (mid_lon, south, east, mid_lat),
        (mid_lon, mid_lat, east, north),
        (west, mid_lat, mid_lon, north),
    ]


def _point_in_cell(lon: float, lat: float, west: float, south: float, east: float, north: float) -> bool:
    if lat < south or lat > north:
        return False
    lon = _normalize_lon(lon)
    w = _normalize_lon(west)
    e = _normalize_lon(east)
    if w <= e:
        return w <= lon <= e
    return lon >= w or lon <= e


def _rasterize_leaves(
    leaves: list[dict[str, Any]],
    north: float,
    south: float,
    west: float,
    east: float,
    width: int,
    height: int,
) -> list[float]:
    """Map each paint pixel to the smallest leaf containing its center (center truth strength)."""
    lat_span = north - south
    lon_span = _lon_span_west_east(west, east)
    strengths = [0.0] * (width * height)
    for j in range(height):
        lat = north - (j + 0.5) * lat_span / height
        for i in range(width):
            lon = _normalize_lon(west + (i + 0.5) * lon_span / width)
            best: dict[str, Any] | None = None
            best_area = float("inf")
            for leaf in leaves:
                lw, ls, le, ln = leaf["west"], leaf["south"], leaf["east"], leaf["north"]
                if not _point_in_cell(lon, lat, lw, ls, le, ln):
                    continue
                area = _lon_span_west_east(lw, le) * (ln - ls)
                if area < best_area:
                    best_area = area
                    best = leaf
            idx = j * width + i
            strengths[idx] = round(float(best["strength"]) if best else 0.0, 5)
    return strengths


def generate_aura_adaptive_raster(
    jd: float,
    aspect_overlay: dict,
    north: float,
    south: float,
    west: float,
    east: float,
    paint_width: int,
    paint_height: int,
    max_orb: float = 6.0,
    apply_lat_cap: bool = True,
    initial_divisions: int = 6,
    max_depth: int = 8,
    gradient_tolerance: float = 0.06,
    min_cell_deg: float = 0.035,
    max_samples: int = 120000,
    max_leaves: int = 12000,
    include_debug_cells: bool = True,
    include_convergence_metrics: bool = True,
    include_reveal_transport: bool = False,
    refinement_stage_id: str | None = None,
) -> dict[str, Any]:
    """
    Adaptive quadtree refinement for aura scalar field (PoC: Sun conjunct ASC).

    Truth samples at cell corners (+ center for leaf value). Subdivide only when
    gradient, orb boundary, or strength-band crossings indicate uncertainty.
    Interior stable regions stop early — no uniform brute force.
    """
    if paint_width < 1 or paint_height < 1:
        raise ValueError("paint_width and paint_height must be positive")
    if max_orb <= 0:
        raise ValueError("max_orb must be positive")
    if initial_divisions < 2:
        raise ValueError("initial_divisions must be >= 2")

    planet_lon, offsets, selected_angle, selected_aspect, selected_planet = _poc_context(
        jd, aspect_overlay
    )
    started = time.perf_counter()
    cap = PRODUCT_LAT_CAP if apply_lat_cap else None

    def sample(lat: float, lon: float) -> tuple[float, float]:
        return orb_strength_at_point(
            jd, lat, _normalize_lon(lon), planet_lon, offsets, selected_angle, max_orb
        )

    leaves: list[dict[str, Any]] = []
    total_samples = 0
    refine_counts: dict[str, int] = {}
    depth_histogram: dict[int, int] = {}
    leaf_budget_hit = False

    def process_cell(west: float, south: float, east: float, north: float, depth: int) -> None:
        nonlocal total_samples, leaf_budget_hit
        if cap is not None and _cell_fully_outside_lat_cap(south, north, cap):
            leaves.append(
                {
                    "west": west,
                    "south": south,
                    "east": east,
                    "north": north,
                    "strength": 0.0,
                    "depth": depth,
                    "estimated_error": 0.0,
                    "leaf": True,
                    "outside_lat_cap": True,
                    "truth_samples": [],
                }
            )
            depth_histogram[depth] = depth_histogram.get(depth, 0) + 1
            return

        corners = [
            (west, south),
            (east, south),
            (east, north),
            (west, north),
        ]
        corner_strengths: list[float] = []
        corner_orbs: list[float] = []
        truth_samples: list[dict[str, Any]] = []
        for clon, clat in corners:
            total_samples += 1
            orb, strength = sample(clat, clon)
            corner_strengths.append(strength)
            corner_orbs.append(orb)
            truth_samples.append(
                {
                    "lon": round(_normalize_lon(clon), 5),
                    "lat": round(clat, 5),
                    "strength": round(strength, 5),
                    "role": "corner",
                }
            )

        center_lon = west + _lon_span_west_east(west, east) / 2.0
        if center_lon > 180:
            center_lon -= 360
        center_lat = (south + north) / 2.0
        total_samples += 1
        center_orb, center_strength = sample(center_lat, center_lon)
        truth_samples.append(
            {
                "lon": round(_normalize_lon(center_lon), 5),
                "lat": round(center_lat, 5),
                "strength": round(center_strength, 5),
                "role": "center",
            }
        )

        if total_samples >= max_samples:
            leaves.append(
                {
                    "west": west,
                    "south": south,
                    "east": east,
                    "north": north,
                    "strength": round(center_strength, 5),
                    "center_orb": round(center_orb, 4),
                    "depth": depth,
                    "estimated_error": 0.0,
                    "leaf": True,
                    "stop_reason": "sample_budget",
                    "truth_samples": truth_samples,
                }
            )
            depth_histogram[depth] = depth_histogram.get(depth, 0) + 1
            return

        est_error = max(corner_strengths) - min(corner_strengths)
        lon_span = _lon_span_west_east(west, east)
        lat_span = north - south
        reasons = _refinement_reasons(
            corner_strengths, center_strength, gradient_tolerance, depth
        )

        at_leaf_cap = len(leaves) >= max_leaves
        can_split = (
            bool(reasons)
            and depth < max_depth
            and lon_span > min_cell_deg
            and lat_span > min_cell_deg
            and total_samples < max_samples
            and not at_leaf_cap
        )
        if bool(reasons) and at_leaf_cap:
            leaf_budget_hit = True

        if can_split:
            for reason in reasons:
                refine_counts[reason] = refine_counts.get(reason, 0) + 1
            for quad in _subdivide_cell(west, south, east, north):
                process_cell(*quad, depth + 1)
            return

        leaves.append(
            {
                "west": west,
                "south": south,
                "east": east,
                "north": north,
                "strength": round(center_strength, 5),
                "center_orb": round(center_orb, 4),
                "depth": depth,
                "estimated_error": round(est_error, 5),
                "leaf": True,
                "stable": not reasons,
                "stop_reason": (
                    "leaf_budget"
                    if reasons and at_leaf_cap
                    else (
                        "max_depth"
                        if reasons and depth >= max_depth
                        else ("min_cell" if reasons else "stable_interior")
                    )
                ),
                "truth_samples": truth_samples,
            }
        )
        depth_histogram[depth] = depth_histogram.get(depth, 0) + 1

    lat_span = north - south
    lon_span = _lon_span_west_east(west, east)
    n = initial_divisions
    for row in range(n):
        lat0 = north - (row + 1) * lat_span / n
        lat1 = north - row * lat_span / n
        for col in range(n):
            lon0 = west + col * lon_span / n
            lon1 = west + (col + 1) * lon_span / n
            if lon1 > 180:
                lon1 -= 360
            if lon0 > 180:
                lon0 -= 360
            process_cell(lon0, lat0, lon1, lat1, 0)

    uniform_equivalent = paint_width * paint_height
    sample_reduction_pct = round(
        100.0 * (1.0 - total_samples / uniform_equivalent) if uniform_equivalent else 0.0,
        1,
    )
    strengths = _rasterize_leaves(leaves, north, south, west, east, paint_width, paint_height)
    sample_budget_hit = total_samples >= max_samples
    elapsed = round(time.perf_counter() - started, 4)

    convergence: dict[str, Any] | None = None
    reference_meta: dict[str, Any] | None = None
    if include_convergence_metrics:
        reference = generate_aura_raster(
            jd,
            aspect_overlay,
            north,
            south,
            west,
            east,
            paint_width,
            paint_height,
            max_orb=max_orb,
            apply_lat_cap=apply_lat_cap,
        )
        convergence = compute_convergence_vs_reference(strengths, reference["strengths"])
        reference_meta = {
            "reference_truth_role": REFERENCE_TRUTH_ROLE,
            "reference_sample_count": reference["properties"]["sample_count"],
            "reference_compute_seconds": reference["properties"]["compute_seconds"],
        }

    debug_features: list[dict[str, Any]] = []
    if include_debug_cells:
        for leaf in leaves:
            lw, ls, le, ln = leaf["west"], leaf["south"], leaf["east"], leaf["north"]
            ring = [[lw, ls], [le, ls], [le, ln], [lw, ln], [lw, ls]]
            debug_features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [ring]},
                    "properties": {
                        "layer": "adaptive_aura_cell",
                        "depth": leaf["depth"],
                        "strength": leaf["strength"],
                        "estimated_error": leaf.get("estimated_error", 0),
                        "stable": bool(leaf.get("stable")),
                        "stop_reason": leaf.get("stop_reason"),
                        "outside_lat_cap": bool(leaf.get("outside_lat_cap")),
                    },
                }
            )

    max_depth_seen = max((leaf["depth"] for leaf in leaves), default=0)
    stable_leaves = sum(1 for leaf in leaves if leaf.get("stable"))
    refined_leaves = len(leaves) - stable_leaves
    stop_reason = _aggregate_stop_reason(
        leaves,
        sample_budget_hit=sample_budget_hit,
        leaf_budget_hit=leaf_budget_hit,
        max_depth_reached=max_depth_seen,
        max_depth=max_depth,
    )
    regression_diag = _depth_regression_diagnostics(
        leaves,
        leaf_budget_hit=leaf_budget_hit,
        max_depth_reached=max_depth_seen,
        convergence=convergence,
    )

    reveal_transport: dict[str, Any] | None = None
    if include_reveal_transport:
        reveal_transport = build_reveal_transport(
            leaves=leaves,
            properties={
                "truth_sample_count": total_samples,
                "cell_count": len(leaves),
                "max_depth_reached": max_depth_seen,
                "max_depth": max_depth,
                "stop_reason": stop_reason,
                "refine_trigger_counts": refine_counts,
                "depth_histogram": depth_histogram,
                "sample_budget_hit": sample_budget_hit,
                "leaf_budget_hit": leaf_budget_hit,
            },
            requested_stage_id=refinement_stage_id,
            convergence=convergence,
        )

    result: dict[str, Any] = {
        "width": paint_width,
        "height": paint_height,
        "bounds": {"north": north, "south": south, "west": west, "east": east},
        "strengths": strengths,
        "leaves": leaves,
        "debug_cells": {
            "type": "FeatureCollection",
            "features": debug_features,
        },
        "properties": {
            "aura_poc": True,
            "truth_spine_overlay": "sun_conjunct_asc",
            "render_mode": "adaptive_raster",
            "stop_reason": stop_reason,
            "aspect_overlay": {
                "planet": selected_planet,
                "aspect": selected_aspect,
                "angle": selected_angle,
            },
            "max_orb": max_orb,
            "apply_lat_cap": apply_lat_cap,
            "lat_cap": PRODUCT_LAT_CAP if apply_lat_cap else None,
            "adaptive_strategy": "quadtree_corner_sampling",
            "initial_divisions": initial_divisions,
            "max_depth": max_depth,
            "max_depth_reached": max_depth_seen,
            "default_max_depth_doctrine": DEFAULT_ADAPTIVE_MAX_DEPTH,
            "gradient_tolerance": gradient_tolerance,
            "min_cell_deg": min_cell_deg,
            "max_leaves": max_leaves,
            "sample_budget_hit": sample_budget_hit,
            "leaf_budget_hit": leaf_budget_hit,
            "truth_sample_count": total_samples,
            "sample_count": total_samples,
            "leaf_count": len(leaves),
            "cell_count": len(leaves),
            "stable_leaf_count": stable_leaves,
            "refined_leaf_count": refined_leaves,
            "uniform_equivalent_samples": uniform_equivalent,
            "sample_reduction_pct": sample_reduction_pct,
            "refine_trigger_counts": refine_counts,
            "depth_histogram": depth_histogram,
            "compute_seconds": elapsed,
            "strength_formula": "max(0, 1 - orb_deg / max_orb)",
            "leaf_value_policy": "center_truth_sample; pixels inherit deepest containing leaf",
            "interpolation_policy": "none_across_cells; partition of viewport",
            "nonzero_count": sum(1 for s in strengths if s > 0),
            "convergence_vs_reference": convergence,
            "reference_truth": reference_meta,
            "depth_regression_diagnostics": regression_diag,
            "refinement_stage_id": refinement_stage_id,
        },
    }
    if reveal_transport is not None:
        result["reveal_transport"] = reveal_transport
        result["properties"]["refinement_reveal"] = {
            "requested_stage_id": refinement_stage_id,
            "observed_stage_id": reveal_transport["observed_stage"]["stage_id"],
            "provisional": reveal_transport["observed_stage"]["provisional"],
            "replace_prior_snapshot": reveal_transport["replace_prior_snapshot"],
        }
    return result


# ---------------------------------------------------------------------------
# Phase C — Convergence-debt-driven adaptive refinement
# ---------------------------------------------------------------------------
#
# Doctrine: refinement budget is spent where the field disagrees with the
# uniform reference at the pixel scale — not where depth permits. The engine
# carries a real pixel-attribution map (C1), a measurable per-leaf debt (C2),
# a priority-queue loop ordered by debt (C3), and per-pass budgets with an
# overshoot guard (C4). No interpolation, no smoothing, no hidden mismatch.

CONVERGENCE_RENDER_MODE = "convergence_raster"
DEFAULT_CONVERGENCE_PER_PASS_SAMPLES = 2000
DEFAULT_CONVERGENCE_MAX_PASSES = 64
CONVERGENCE_OVERSHOOT_STALL_PASSES = 2


def _viewport_pixel_coords(
    paint_width: int,
    paint_height: int,
    north: float,
    south: float,
    west: float,
    east: float,
) -> list[tuple[float, float]]:
    """Pixel-center (lon, lat) per paint index. Lon wrap handled by _normalize_lon."""
    lat_span = north - south
    lon_span = _lon_span_west_east(west, east)
    coords: list[tuple[float, float]] = [(0.0, 0.0)] * (paint_width * paint_height)
    for j in range(paint_height):
        lat = north - (j + 0.5) * lat_span / paint_height
        for i in range(paint_width):
            lon = _normalize_lon(west + (i + 0.5) * lon_span / paint_width)
            coords[j * paint_width + i] = (lon, lat)
    return coords


def _initial_cell_pixel_groups(
    paint_width: int,
    paint_height: int,
    initial_divisions: int,
    north: float,
    south: float,
    west: float,
    east: float,
) -> list[list[int]]:
    """Partition all paint pixels across an initial_divisions × initial_divisions coarse grid."""
    lat_span = north - south
    lon_span = _lon_span_west_east(west, east)
    cell_lat = lat_span / initial_divisions
    cell_lon = lon_span / initial_divisions
    groups: list[list[int]] = [[] for _ in range(initial_divisions * initial_divisions)]
    for j in range(paint_height):
        lat = north - (j + 0.5) * lat_span / paint_height
        row = int((north - lat) / cell_lat)
        if row < 0:
            row = 0
        elif row >= initial_divisions:
            row = initial_divisions - 1
        for i in range(paint_width):
            lon_off = (i + 0.5) * lon_span / paint_width
            col = int(lon_off / cell_lon)
            if col < 0:
                col = 0
            elif col >= initial_divisions:
                col = initial_divisions - 1
            groups[row * initial_divisions + col].append(j * paint_width + i)
    return groups


def _partition_pixels_to_children(
    pixel_indices: list[int],
    pixel_coords: list[tuple[float, float]],
    west: float,
    east: float,
    mid_lon: float,
    mid_lat: float,
) -> list[list[int]]:
    """Distribute parent pixels across SW/SE/NE/NW children using mid-lon, mid-lat."""
    children: list[list[int]] = [[], [], [], []]
    lon_span_full = _lon_span_west_east(west, east)
    mid_off = ((mid_lon - west) % 360 + 360) % 360
    if mid_off > lon_span_full:
        mid_off = lon_span_full
    for pix in pixel_indices:
        plon, plat = pixel_coords[pix]
        plon_off = ((plon - west) % 360 + 360) % 360
        if plon_off > lon_span_full:
            plon_off -= 360
        is_east = plon_off >= mid_off
        is_north = plat >= mid_lat
        if not is_east and not is_north:
            children[0].append(pix)  # SW
        elif is_east and not is_north:
            children[1].append(pix)  # SE
        elif is_east and is_north:
            children[2].append(pix)  # NE
        else:
            children[3].append(pix)  # NW
    return children


def _cell_center(west: float, south: float, east: float, north: float) -> tuple[float, float]:
    center_lon = _normalize_lon(west + _lon_span_west_east(west, east) / 2.0)
    center_lat = (south + north) / 2.0
    return center_lon, center_lat


def _can_split_convergence_leaf(
    leaf: dict[str, Any],
    *,
    min_cell_deg: float,
    leaf_count: int,
    max_leaves: int,
    total_samples: int,
    max_samples: int,
) -> tuple[bool, str | None]:
    """Reason this leaf cannot be split further (inspectable; no silent stops)."""
    if len(leaf["pixel_indices"]) <= 1:
        return False, "pixel_atomic"
    lon_span = _lon_span_west_east(leaf["west"], leaf["east"])
    lat_span = leaf["north"] - leaf["south"]
    if lon_span <= min_cell_deg or lat_span <= min_cell_deg:
        return False, "min_cell"
    if leaf_count >= max_leaves:
        return False, "leaf_budget"
    if total_samples >= max_samples:
        return False, "sample_budget"
    return True, None


def generate_aura_convergence_raster(
    jd: float,
    aspect_overlay: dict,
    north: float,
    south: float,
    west: float,
    east: float,
    paint_width: int,
    paint_height: int,
    max_orb: float = 6.0,
    apply_lat_cap: bool = True,
    initial_divisions: int = 4,
    convergence_delta_threshold: float = CONVERGENCE_DELTA_THRESHOLD,
    target_pixels_above_threshold_pct: float = 0.0,
    per_pass_sample_budget: int = DEFAULT_CONVERGENCE_PER_PASS_SAMPLES,
    max_passes: int = DEFAULT_CONVERGENCE_MAX_PASSES,
    max_samples: int = 120000,
    max_leaves: int = 12000,
    min_cell_deg: float = 0.035,
    overshoot_guard: bool = True,
    include_debug_cells: bool = True,
    include_pass_history: bool = True,
    include_pixel_attribution_sample: bool = False,
    pixel_attribution_sample_cap: int = 4000,
) -> dict[str, Any]:
    """
    Convergence-debt-driven adaptive raster (PoC: Sun conjunct ASC).

    Pixel attribution (C1) is maintained per leaf. Each leaf carries a debt (C2)
    measured against a uniform reference raster (one truth sample per paint pixel,
    identical bounds + lat cap). A priority queue (C3) drives refinement: highest
    debt first, leaf splits into 4, children inherit parent's pixel partition by
    mid-lon/mid-lat. Per-pass budgets bound work; an overshoot guard (C4) halts
    the engine if a refinement pass *increases* the count of pixels above the
    convergence delta — preventing the depth-8 leaf_budget regression mode.

    No interpolation across leaves, no blur, no smoothing. Each pixel's strength
    is the center truth sample of the leaf that owns it. Mismatch vs reference is
    reported, not hidden.
    """
    if paint_width < 1 or paint_height < 1:
        raise ValueError("paint_width and paint_height must be positive")
    if max_orb <= 0:
        raise ValueError("max_orb must be positive")
    if initial_divisions < 2:
        raise ValueError("initial_divisions must be >= 2")
    if per_pass_sample_budget < 1:
        raise ValueError("per_pass_sample_budget must be >= 1")
    if max_passes < 1:
        raise ValueError("max_passes must be >= 1")
    if convergence_delta_threshold <= 0:
        raise ValueError("convergence_delta_threshold must be positive")

    planet_lon, offsets, selected_angle, selected_aspect, selected_planet = _poc_context(
        jd, aspect_overlay
    )
    started = time.perf_counter()
    cap = PRODUCT_LAT_CAP if apply_lat_cap else None

    reference = generate_aura_raster(
        jd,
        aspect_overlay,
        north,
        south,
        west,
        east,
        paint_width,
        paint_height,
        max_orb=max_orb,
        apply_lat_cap=apply_lat_cap,
    )
    reference_strengths = reference["strengths"]
    pixel_count = len(reference_strengths)
    target_pixels_above = max(
        0, int(round(target_pixels_above_threshold_pct * pixel_count / 100.0))
    )

    pixel_coords = _viewport_pixel_coords(paint_width, paint_height, north, south, west, east)
    initial_groups = _initial_cell_pixel_groups(
        paint_width, paint_height, initial_divisions, north, south, west, east
    )

    pixel_strength: list[float] = list(reference_strengths)
    pixel_leaf_id: list[int] = [-1] * pixel_count
    pixels_above = 0

    leaves: dict[int, dict[str, Any]] = {}
    next_id = 0
    total_samples = 0
    refine_counts: dict[str, int] = {"split": 0}
    depth_histogram: dict[int, int] = {}
    pq: list[tuple[float, int, int]] = []
    heap_seq = 0  # tie-breaker; ensures heap ordering for equal debt

    def _record_depth(depth: int) -> None:
        depth_histogram[depth] = depth_histogram.get(depth, 0) + 1

    def _outside_cap(s: float, n: float) -> bool:
        return cap is not None and _cell_fully_outside_lat_cap(s, n, cap)

    def _create_leaf(
        leaf_west: float,
        leaf_south: float,
        leaf_east: float,
        leaf_north: float,
        depth: int,
        pixel_indices: list[int],
    ) -> int:
        """Sample center, update pixel strengths/above counter, compute debt, push to PQ."""
        nonlocal next_id, total_samples, pixels_above, heap_seq
        leaf_id = next_id
        next_id += 1

        if _outside_cap(leaf_south, leaf_north):
            # Reference is already 0 over the cap; leaf truthfully reports 0 and contributes 0 debt.
            strength = 0.0
            center_orb = 180.0
            settled = True
            stop_reason: str | None = "outside_lat_cap"
        else:
            center_lon, center_lat = _cell_center(leaf_west, leaf_south, leaf_east, leaf_north)
            total_samples += 1
            center_orb, strength = orb_strength_at_point(
                jd, center_lat, center_lon, planet_lon, offsets, selected_angle, max_orb
            )
            settled = False
            stop_reason = None

        debt = 0.0
        for pix in pixel_indices:
            old_s = pixel_strength[pix]
            ref_s = reference_strengths[pix]
            was_above = abs(old_s - ref_s) > convergence_delta_threshold
            is_above = abs(strength - ref_s) > convergence_delta_threshold
            pixel_strength[pix] = strength
            pixel_leaf_id[pix] = leaf_id
            if was_above and not is_above:
                pixels_above -= 1
            elif not was_above and is_above:
                pixels_above += 1
            debt += abs(strength - ref_s)

        leaf: dict[str, Any] = {
            "id": leaf_id,
            "west": leaf_west,
            "south": leaf_south,
            "east": leaf_east,
            "north": leaf_north,
            "strength": round(strength, 5),
            "center_orb": round(center_orb, 4),
            "depth": depth,
            "pixel_indices": pixel_indices,
            "pixel_count": len(pixel_indices),
            "debt": debt,
            "settled": settled,
            "stop_reason": stop_reason,
            "outside_lat_cap": stop_reason == "outside_lat_cap",
        }
        leaves[leaf_id] = leaf
        if not settled:
            if debt <= 0:
                leaf["settled"] = True
                leaf["stop_reason"] = "zero_debt"
            else:
                # heapq is min-heap; push -debt for max-by-debt. seq disambiguates ties.
                heapq.heappush(pq, (-debt, heap_seq, leaf_id))
                heap_seq += 1
        if leaf["settled"]:
            _record_depth(depth)
        return leaf_id

    # Initial coarse partition with full pixel attribution.
    lat_span = north - south
    lon_span = _lon_span_west_east(west, east)
    for row in range(initial_divisions):
        lat0 = north - (row + 1) * lat_span / initial_divisions
        lat1 = north - row * lat_span / initial_divisions
        for col in range(initial_divisions):
            lon0 = west + col * lon_span / initial_divisions
            lon1 = west + (col + 1) * lon_span / initial_divisions
            if lon0 > 180:
                lon0 -= 360
            if lon1 > 180:
                lon1 -= 360
            cell_idx = row * initial_divisions + col
            _create_leaf(lon0, lat0, lon1, lat1, 0, initial_groups[cell_idx])

    pass_history: list[dict[str, Any]] = []
    pass_idx = 0
    final_stop_reason = "max_passes"
    converged = False
    overshoot_detected = False
    stall_counter = 0

    # If the initial coarse partition already matches the reference (e.g. empty
    # viewport), no actionable leaves exist — record that as converged truthfully.
    if pixels_above <= target_pixels_above:
        converged = True
        final_stop_reason = "converged_at_initial_partition"
    elif not pq:
        final_stop_reason = "no_actionable_leaves"

    while pq and total_samples < max_samples and pass_idx < max_passes and not converged:
        pass_idx += 1
        pass_start_samples = total_samples
        pass_start_pixels_above = pixels_above
        pass_start_leaf_count = len(leaves)
        splits_this_pass = 0
        skipped_atomic = 0
        skipped_min_cell = 0
        skipped_leaf_budget = 0
        skipped_sample_budget = 0

        # Pass loop: spend per-pass budget on highest-debt leaves.
        while pq:
            if total_samples - pass_start_samples >= per_pass_sample_budget:
                break
            if total_samples >= max_samples:
                break
            neg_debt, _seq, leaf_id = heapq.heappop(pq)
            leaf = leaves.get(leaf_id)
            if leaf is None or leaf.get("settled") or leaf.get("split"):
                continue  # stale entry; leaf already retired
            current_debt = leaf["debt"]
            if abs(-neg_debt - current_debt) > 1e-9:
                # debt changed since insertion (shouldn't happen but be defensive)
                heapq.heappush(pq, (-current_debt, heap_seq, leaf_id))
                heap_seq += 1
                continue
            if current_debt <= 0:
                leaf["settled"] = True
                leaf["stop_reason"] = "zero_debt"
                _record_depth(leaf["depth"])
                continue
            can_split, why_not = _can_split_convergence_leaf(
                leaf,
                min_cell_deg=min_cell_deg,
                leaf_count=len(leaves),
                max_leaves=max_leaves,
                total_samples=total_samples,
                max_samples=max_samples,
            )
            if not can_split:
                leaf["settled"] = True
                leaf["stop_reason"] = why_not
                _record_depth(leaf["depth"])
                if why_not == "pixel_atomic":
                    skipped_atomic += 1
                elif why_not == "min_cell":
                    skipped_min_cell += 1
                elif why_not == "leaf_budget":
                    skipped_leaf_budget += 1
                elif why_not == "sample_budget":
                    skipped_sample_budget += 1
                continue

            mid_lon, mid_lat = _cell_center(
                leaf["west"], leaf["south"], leaf["east"], leaf["north"]
            )
            partitioned = _partition_pixels_to_children(
                leaf["pixel_indices"],
                pixel_coords,
                leaf["west"],
                leaf["east"],
                mid_lon,
                mid_lat,
            )
            child_bounds = _subdivide_cell(
                leaf["west"], leaf["south"], leaf["east"], leaf["north"]
            )
            leaf["split"] = True
            leaf["pixel_indices"] = []  # ownership transferred to children
            for (cw, cs, ce, cn), child_pix in zip(child_bounds, partitioned):
                if not child_pix:
                    # Child owns no paint pixel — still create a settled leaf for the
                    # debug surface, but no truth sample is taken (it would not affect raster).
                    no_pix_id = next_id
                    next_id += 1
                    leaves[no_pix_id] = {
                        "id": no_pix_id,
                        "west": cw,
                        "south": cs,
                        "east": ce,
                        "north": cn,
                        "strength": 0.0,
                        "center_orb": None,
                        "depth": leaf["depth"] + 1,
                        "pixel_indices": [],
                        "pixel_count": 0,
                        "debt": 0.0,
                        "settled": True,
                        "stop_reason": "no_pixels",
                        "outside_lat_cap": False,
                    }
                    _record_depth(leaf["depth"] + 1)
                    continue
                _create_leaf(cw, cs, ce, cn, leaf["depth"] + 1, child_pix)
            refine_counts["split"] += 1
            splits_this_pass += 1

        pass_end_samples = total_samples
        pass_end_pixels_above = pixels_above
        pass_end_leaf_count = len(leaves)
        pass_samples = pass_end_samples - pass_start_samples

        if pixel_count > 0:
            pixels_above_pct = round(100.0 * pixels_above / pixel_count, 4)
            start_pct = round(100.0 * pass_start_pixels_above / pixel_count, 4)
        else:
            pixels_above_pct = 0.0
            start_pct = 0.0

        overshoot = pixels_above > pass_start_pixels_above
        progressed = pixels_above < pass_start_pixels_above

        pass_history.append(
            {
                "pass_index": pass_idx,
                "samples_used": pass_samples,
                "cumulative_samples": pass_end_samples,
                "leaves_split": splits_this_pass,
                "leaf_count_before": pass_start_leaf_count,
                "leaf_count_after": pass_end_leaf_count,
                "pixels_above_threshold_before_pct": start_pct,
                "pixels_above_threshold_after_pct": pixels_above_pct,
                "pixels_above_threshold_delta": pixels_above - pass_start_pixels_above,
                "overshoot_in_pass": overshoot,
                "progressed": progressed,
                "skipped_pixel_atomic": skipped_atomic,
                "skipped_min_cell": skipped_min_cell,
                "skipped_leaf_budget": skipped_leaf_budget,
                "skipped_sample_budget": skipped_sample_budget,
                "pq_size_after": len(pq),
            }
        )

        if overshoot and overshoot_guard:
            overshoot_detected = True
            final_stop_reason = "overshoot_guard_triggered"
            break

        if pixels_above <= target_pixels_above:
            converged = True
            final_stop_reason = "converged"
            break

        if splits_this_pass == 0:
            final_stop_reason = "no_actionable_leaves"
            break

        if not progressed:
            stall_counter += 1
            if stall_counter >= CONVERGENCE_OVERSHOOT_STALL_PASSES:
                final_stop_reason = "convergence_stalled"
                break
        else:
            stall_counter = 0

    if total_samples >= max_samples and not converged and not overshoot_detected:
        if final_stop_reason == "max_passes":
            final_stop_reason = "sample_budget"

    if not pq and not converged and not overshoot_detected and final_stop_reason == "max_passes":
        final_stop_reason = "no_actionable_leaves"

    # Re-check final convergence flag against pixel-level truth (defensive: any
    # incremental counter drift would surface here, never silently).
    if pixels_above <= target_pixels_above:
        converged = True
        if final_stop_reason in ("max_passes", "no_actionable_leaves"):
            final_stop_reason = "converged"

    # Final per-pixel diffs (also drives the final convergence report).
    diffs = [abs(pixel_strength[i] - reference_strengths[i]) for i in range(pixel_count)]
    pixels_above_final = sum(1 for d in diffs if d > convergence_delta_threshold)
    mean_delta = round(sum(diffs) / pixel_count, 6) if pixel_count else 0.0
    max_delta = round(max(diffs), 6) if diffs else 0.0
    convergence_final = {
        "reference_truth_role": REFERENCE_TRUTH_ROLE,
        "delta_threshold": convergence_delta_threshold,
        "paint_pixel_count": pixel_count,
        "mean_delta_vs_reference": mean_delta,
        "max_delta_vs_reference": max_delta,
        "pixels_above_threshold": pixels_above_final,
        "pixels_above_threshold_pct": round(100.0 * pixels_above_final / pixel_count, 4)
        if pixel_count
        else 0.0,
        "converged": pixels_above_final <= target_pixels_above,
    }

    # Mark any leaves still in the queue as settled (their stop reason is whatever bound stopped us).
    remainder_reason = (
        "sample_budget"
        if final_stop_reason in ("sample_budget",)
        else "max_passes"
        if final_stop_reason in ("max_passes", "convergence_stalled")
        else "overshoot_guard"
        if final_stop_reason == "overshoot_guard_triggered"
        else final_stop_reason
    )
    while pq:
        _neg_debt, _seq, leaf_id = heapq.heappop(pq)
        leaf = leaves.get(leaf_id)
        if leaf is None or leaf.get("settled") or leaf.get("split"):
            continue
        leaf["settled"] = True
        leaf["stop_reason"] = remainder_reason
        _record_depth(leaf["depth"])

    # Rasterize from the pixel attribution map (no per-pixel leaf scan).
    strengths = [round(pixel_strength[i], 5) for i in range(pixel_count)]

    active_leaves = [leaf for leaf in leaves.values() if not leaf.get("split")]
    leaf_pixel_counts = [leaf["pixel_count"] for leaf in active_leaves]
    pixel_owned = sum(leaf_pixel_counts)
    max_depth_seen = max((leaf["depth"] for leaf in active_leaves), default=0)
    stable_leaves = sum(1 for leaf in active_leaves if leaf.get("stop_reason") == "zero_debt")
    refined_leaves = sum(1 for leaf in active_leaves if leaf.get("stop_reason") != "zero_debt")

    elapsed = round(time.perf_counter() - started, 4)
    sample_reduction_pct = (
        round(100.0 * (1.0 - total_samples / pixel_count), 1) if pixel_count else 0.0
    )

    debug_features: list[dict[str, Any]] = []
    if include_debug_cells:
        for leaf in active_leaves:
            lw, ls, le, ln = leaf["west"], leaf["south"], leaf["east"], leaf["north"]
            ring = [[lw, ls], [le, ls], [le, ln], [lw, ln], [lw, ls]]
            debug_features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [ring]},
                    "properties": {
                        "layer": "convergence_aura_cell",
                        "depth": leaf["depth"],
                        "strength": leaf["strength"],
                        "debt": round(leaf["debt"], 5),
                        "pixel_count": leaf["pixel_count"],
                        "stop_reason": leaf.get("stop_reason"),
                        "settled": bool(leaf.get("settled")),
                        "outside_lat_cap": bool(leaf.get("outside_lat_cap")),
                    },
                }
            )

    attribution_sample: list[dict[str, Any]] = []
    if include_pixel_attribution_sample:
        step = max(1, pixel_count // pixel_attribution_sample_cap)
        for pix in range(0, pixel_count, step):
            plon, plat = pixel_coords[pix]
            attribution_sample.append(
                {
                    "pixel_index": pix,
                    "lon": round(plon, 5),
                    "lat": round(plat, 5),
                    "leaf_id": pixel_leaf_id[pix],
                    "strength": round(pixel_strength[pix], 5),
                    "reference_strength": round(reference_strengths[pix], 5),
                    "delta": round(abs(pixel_strength[pix] - reference_strengths[pix]), 5),
                }
            )

    # Drop the heavy `pixel_indices` per-leaf from the response — debug surface
    # already lists per-leaf pixel_count; pixel_attribution_sample carries the
    # inspectable pixel→leaf mapping when explicitly requested.
    leaves_out: list[dict[str, Any]] = []
    for leaf in active_leaves:
        out_leaf = dict(leaf)
        out_leaf.pop("pixel_indices", None)
        leaves_out.append(out_leaf)

    properties: dict[str, Any] = {
        "aura_poc": True,
        "truth_spine_overlay": "sun_conjunct_asc",
        "render_mode": CONVERGENCE_RENDER_MODE,
        "stop_reason": final_stop_reason,
        "converged": converged,
        "overshoot_detected": overshoot_detected,
        "aspect_overlay": {
            "planet": selected_planet,
            "aspect": selected_aspect,
            "angle": selected_angle,
        },
        "max_orb": max_orb,
        "apply_lat_cap": apply_lat_cap,
        "lat_cap": PRODUCT_LAT_CAP if apply_lat_cap else None,
        "adaptive_strategy": "convergence_debt_priority_queue",
        "initial_divisions": initial_divisions,
        "convergence_delta_threshold": convergence_delta_threshold,
        "target_pixels_above_threshold_pct": target_pixels_above_threshold_pct,
        "per_pass_sample_budget": per_pass_sample_budget,
        "max_passes": max_passes,
        "passes_executed": pass_idx,
        "max_samples": max_samples,
        "max_leaves": max_leaves,
        "min_cell_deg": min_cell_deg,
        "overshoot_guard_enabled": overshoot_guard,
        "max_depth_reached": max_depth_seen,
        "truth_sample_count": total_samples,
        "sample_count": total_samples,
        "leaf_count": len(active_leaves),
        "cell_count": len(active_leaves),
        "stable_leaf_count": stable_leaves,
        "refined_leaf_count": refined_leaves,
        "depth_histogram": depth_histogram,
        "refine_trigger_counts": refine_counts,
        "uniform_equivalent_samples": pixel_count,
        "sample_reduction_pct": sample_reduction_pct,
        "compute_seconds": elapsed,
        "reference_compute_seconds": reference["properties"]["compute_seconds"],
        "strength_formula": "max(0, 1 - orb_deg / max_orb)",
        "leaf_value_policy": "center_truth_sample; pixels inherit owning leaf via pixel attribution",
        "interpolation_policy": "none_across_cells; partition of viewport",
        "pixel_attribution_total": pixel_owned,
        "pixel_attribution_complete": pixel_owned == pixel_count,
        "nonzero_count": sum(1 for s in strengths if s > 0),
        "convergence_vs_reference": convergence_final,
        "reference_truth": {
            "reference_truth_role": REFERENCE_TRUTH_ROLE,
            "reference_sample_count": reference["properties"]["sample_count"],
            "reference_compute_seconds": reference["properties"]["compute_seconds"],
        },
        # Doctrine compatibility — convergence engine never relies on max_depth;
        # legacy adaptive callers may still inspect these fields.
        "default_max_depth_doctrine": DEFAULT_ADAPTIVE_MAX_DEPTH,
        "leaf_budget_hit": any(
            leaf.get("stop_reason") == "leaf_budget" for leaf in active_leaves
        ),
        "sample_budget_hit": total_samples >= max_samples,
    }

    result: dict[str, Any] = {
        "width": paint_width,
        "height": paint_height,
        "bounds": {"north": north, "south": south, "west": west, "east": east},
        "strengths": strengths,
        "leaves": leaves_out,
        "debug_cells": {
            "type": "FeatureCollection",
            "features": debug_features,
        },
        "properties": properties,
    }
    if include_pass_history:
        result["pass_history"] = pass_history
    if include_pixel_attribution_sample:
        result["pixel_attribution_sample"] = attribution_sample
    return result


def generate_aura_field(
    jd: float,
    aspect_overlay: dict,
    resolution: float,
    max_orb: float = 6.0,
    min_strength: float = 0.04,
    include_debug_points: bool = False,
    apply_lat_cap: bool = True,
) -> dict[str, Any]:
    """
    Sample geographic grid; orb = min |signed_angle_diff(angle_lon, target_lon + offset)|.
    strength = max(0, 1 - orb / max_orb).
    """
    if resolution <= 0 or max_orb <= 0:
        raise ValueError("resolution and max_orb must be positive")

    planet_lon, offsets, selected_angle, selected_aspect, selected_planet = _poc_context(
        jd, aspect_overlay
    )

    started = time.perf_counter()
    cap = PRODUCT_LAT_CAP if apply_lat_cap else 85.0
    lat_min = -cap if apply_lat_cap else -85.0
    lat_max = cap if apply_lat_cap else 85.0
    lat_vals = np.arange(lat_min, lat_max + 1e-9, resolution)
    lon_vals = np.arange(-180, 180 + 1e-9, resolution)
    half = resolution / 2.0
    ring_cap = PRODUCT_LAT_CAP if apply_lat_cap else None

    features: list[dict] = []
    strengths: list[float] = []
    orbs: list[float] = []
    sample_count = 0

    for lat in lat_vals:
        for lon in lon_vals:
            sample_count += 1
            best_orb, strength = orb_strength_at_point(
                jd,
                float(lat),
                float(lon),
                planet_lon,
                offsets,
                selected_angle,
                max_orb,
            )
            if strength < min_strength:
                continue

            strengths.append(strength)
            orbs.append(best_orb)

            ring = _cell_ring(float(lon), float(lat), half, ring_cap)
            if len(ring) < 4:
                continue

            features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [ring]},
                    "properties": {
                        "layer": "aura_field",
                        "strength": round(strength, 4),
                        "orb_deg": round(best_orb, 4),
                        "lat": round(float(lat), 5),
                        "lon": round(float(lon), 5),
                    },
                }
            )

            if include_debug_points:
                features.append(
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [float(lon), float(lat)]},
                        "properties": {
                            "layer": "aura_debug_sample",
                            "strength": round(strength, 4),
                            "orb_deg": round(best_orb, 4),
                        },
                    }
                )

    elapsed = round(time.perf_counter() - started, 4)
    return {
        "type": "FeatureCollection",
        "features": features,
        "properties": {
            "aura_poc": True,
            "aspect_overlay": {
                "planet": selected_planet,
                "aspect": selected_aspect,
                "angle": selected_angle,
            },
            "resolution": resolution,
            "max_orb": max_orb,
            "min_strength": min_strength,
            "apply_lat_cap": apply_lat_cap,
            "lat_cap": PRODUCT_LAT_CAP if apply_lat_cap else None,
            "grid_shape": [len(lat_vals), len(lon_vals)],
            "sample_count": sample_count,
            "cell_count": len([f for f in features if f["properties"].get("layer") == "aura_field"]),
            "strength_min": round(min(strengths), 4) if strengths else None,
            "strength_max": round(max(strengths), 4) if strengths else None,
            "orb_min": round(min(orbs), 4) if orbs else None,
            "orb_max": round(max(orbs), 4) if orbs else None,
            "compute_seconds": elapsed,
            "strength_formula": "max(0, 1 - orb_deg / max_orb)",
            "clipping_policy": (
                f"sample and cell bounds ±{PRODUCT_LAT_CAP}° lat"
                if apply_lat_cap
                else "no latitude cap (debugNoLatCap)"
            ),
        },
    }
