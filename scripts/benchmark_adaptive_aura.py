#!/usr/bin/env python3
"""Compare uniform vs adaptive aura truth sampling (Sun conjunct ASC PoC)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import swisseph as swe

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aura_field_engine import (
    CONVERGENCE_DELTA_THRESHOLD,
    DEFAULT_ADAPTIVE_MAX_DEPTH,
    REFERENCE_TRUTH_ROLE,
    compute_convergence_vs_reference,
    generate_aura_adaptive_raster,
    generate_aura_convergence_raster,
    generate_aura_raster,
)

REPORT_PATH = ROOT / "validation" / "reports" / "adaptive_aura_benchmark.json"

# Baseline validated chart (UTC noon)
JD = swe.julday(1990, 6, 21, 12.0)
OVERLAY = {"planet": "sun", "aspect": "conjunction", "angle": "ASC"}

VIEWPORTS = [
    {"name": "mid_lat_wide", "north": 45, "south": 15, "west": -30, "east": 30},
    {"name": "high_north", "north": 70, "south": 50, "west": -20, "east": 40},
    {"name": "greenland_iceland", "north": 72, "south": 58, "west": -45, "east": -10},
    {"name": "southern", "north": -10, "south": -40, "west": 10, "east": 50},
    {"name": "asc_band", "north": 10, "south": -10, "west": -100, "east": -80},
]

PAINT = (96, 72)
DEPTH_SWEEP = (2, 4, 6, 8)


def _metrics_from_adaptive(adaptive: dict, uniform: dict) -> dict:
    ap = adaptive["properties"]
    conv = ap.get("convergence_vs_reference") or compute_convergence_vs_reference(
        adaptive["strengths"], uniform["strengths"]
    )
    return {
        "sample_count": ap["truth_sample_count"],
        "cell_count": ap["cell_count"],
        "max_depth": ap["max_depth_reached"],
        "mean_delta_vs_reference": conv["mean_delta_vs_reference"],
        "max_delta_vs_reference": conv["max_delta_vs_reference"],
        "pixels_above_threshold_pct": conv["pixels_above_threshold_pct"],
        "stop_reason": ap["stop_reason"],
        "converged": conv["converged"],
        "leaf_budget_hit": ap["leaf_budget_hit"],
        "sample_budget_hit": ap["sample_budget_hit"],
    }


def convergence_at_depth(
    north: float, south: float, west: float, east: float, pw: int, ph: int, max_depth: int
) -> dict:
    uniform = generate_aura_raster(
        JD, OVERLAY, north, south, west, east, pw, ph, max_orb=6.0, apply_lat_cap=True
    )
    adaptive = generate_aura_adaptive_raster(
        JD,
        OVERLAY,
        north,
        south,
        west,
        east,
        pw,
        ph,
        max_orb=6.0,
        apply_lat_cap=True,
        initial_divisions=6,
        max_depth=max_depth,
        gradient_tolerance=0.06,
        include_debug_cells=False,
        include_convergence_metrics=True,
    )
    row = _metrics_from_adaptive(adaptive, uniform)
    row["max_depth_limit"] = max_depth
    return row


def minimum_convergent_depth(sweep: list[dict]) -> dict | None:
    converged = [s for s in sweep if s.get("converged")]
    if not converged:
        return None
    best = min(converged, key=lambda s: (s["max_depth"], s["sample_count"]))
    return {
        "max_depth": best["max_depth_limit"],
        "sample_count": best["sample_count"],
        "pixels_above_threshold_pct": best["pixels_above_threshold_pct"],
    }


def depth_regression_analysis(sweep: list[dict]) -> dict:
    """Explain non-monotonic depth (e.g. depth 8 worse than depth 6)."""
    by_depth = {s["max_depth_limit"]: s for s in sweep}
    d6 = by_depth.get(6)
    d8 = by_depth.get(8)
    out: dict = {"reference_truth_role": REFERENCE_TRUTH_ROLE}
    if not d6 or not d8:
        return out
    worsened = (
        d8["pixels_above_threshold_pct"] > d6["pixels_above_threshold_pct"]
        or d8["max_delta_vs_reference"] > d6["max_delta_vs_reference"]
    )
    out["depth_8_regresses_vs_depth_6"] = worsened
    if worsened:
        out["likely_cause"] = (
            "leaf_budget_hit truncates subdivision: heterogeneous leaf depths assign "
            "flat center strength while reference samples each pixel center."
        )
        out["depth_8_leaf_budget_hit"] = d8.get("leaf_budget_hit")
        out["depth_8_stop_reason"] = d8.get("stop_reason")
    return out


def _metrics_from_convergence(conv_result: dict, uniform: dict) -> dict:
    cp = conv_result["properties"]
    cv = cp["convergence_vs_reference"]
    return {
        "sample_count": cp["truth_sample_count"],
        "cell_count": cp["cell_count"],
        "max_depth": cp["max_depth_reached"],
        "mean_delta_vs_reference": cv["mean_delta_vs_reference"],
        "max_delta_vs_reference": cv["max_delta_vs_reference"],
        "pixels_above_threshold_pct": cv["pixels_above_threshold_pct"],
        "stop_reason": cp["stop_reason"],
        "converged": cv["converged"],
        "overshoot_detected": cp["overshoot_detected"],
        "passes_executed": cp["passes_executed"],
        "pixel_attribution_complete": cp["pixel_attribution_complete"],
    }


def run_convergence(
    north: float,
    south: float,
    west: float,
    east: float,
    pw: int,
    ph: int,
    *,
    initial_divisions: int = 4,
    per_pass_sample_budget: int = 2000,
    max_passes: int = 64,
) -> dict:
    return generate_aura_convergence_raster(
        JD,
        OVERLAY,
        north,
        south,
        west,
        east,
        pw,
        ph,
        max_orb=6.0,
        apply_lat_cap=True,
        initial_divisions=initial_divisions,
        per_pass_sample_budget=per_pass_sample_budget,
        max_passes=max_passes,
        max_samples=120000,
        max_leaves=12000,
        include_debug_cells=False,
        include_pass_history=True,
    )


def convergence_pass_sweep(
    north: float, south: float, west: float, east: float, pw: int, ph: int
) -> list[dict]:
    """Sweep per-pass budget to show convergence scales with truth samples, not depth."""
    out: list[dict] = []
    for budget in (500, 1000, 2000, 4000):
        r = run_convergence(
            north, south, west, east, pw, ph, per_pass_sample_budget=budget
        )
        cp = r["properties"]
        cv = cp["convergence_vs_reference"]
        out.append(
            {
                "per_pass_sample_budget": budget,
                "truth_sample_count": cp["truth_sample_count"],
                "passes_executed": cp["passes_executed"],
                "pixels_above_threshold_pct": cv["pixels_above_threshold_pct"],
                "max_delta_vs_reference": cv["max_delta_vs_reference"],
                "stop_reason": cp["stop_reason"],
                "converged": cv["converged"],
                "overshoot_detected": cp["overshoot_detected"],
            }
        )
    return out


def run_viewport(vp: dict) -> dict:
    north, south, west, east = vp["north"], vp["south"], vp["west"], vp["east"]
    pw, ph = PAINT

    uniform = generate_aura_raster(
        JD, OVERLAY, north, south, west, east, pw, ph, max_orb=6.0, apply_lat_cap=True
    )
    adaptive = generate_aura_adaptive_raster(
        JD,
        OVERLAY,
        north,
        south,
        west,
        east,
        pw,
        ph,
        max_orb=6.0,
        apply_lat_cap=True,
        initial_divisions=6,
        max_depth=DEFAULT_ADAPTIVE_MAX_DEPTH,
        gradient_tolerance=0.06,
        include_debug_cells=False,
        include_convergence_metrics=True,
    )
    convergence = run_convergence(north, south, west, east, pw, ph)

    metrics_depth = _metrics_from_adaptive(adaptive, uniform)
    metrics_convergence = _metrics_from_convergence(convergence, uniform)

    ap = adaptive["properties"]
    cp = convergence["properties"]

    sample_delta = ap["truth_sample_count"] - cp["truth_sample_count"]
    sample_reduction_pct = (
        round(100.0 * sample_delta / ap["truth_sample_count"], 1)
        if ap["truth_sample_count"]
        else 0.0
    )

    convergence_sweep = [
        convergence_at_depth(north, south, west, east, pw, ph, d) for d in DEPTH_SWEEP
    ]

    pass_history = convergence.get("pass_history") or []
    overshoot_passes = [h for h in pass_history if h.get("overshoot_in_pass")]
    return {
        "viewport": vp["name"],
        "paint_grid": f"{pw}x{ph}",
        "reference_truth_role": REFERENCE_TRUTH_ROLE,
        "reference_sample_count": uniform["properties"]["sample_count"],
        "uniform_compute_s": uniform["properties"]["compute_seconds"],
        "depth_driven": {
            "compute_s": ap["compute_seconds"],
            "sample_reduction_pct_vs_uniform": ap["sample_reduction_pct"],
            "refine_triggers": ap["refine_trigger_counts"],
            "depth_histogram": ap["depth_histogram"],
            "convergence_metrics": metrics_depth,
            "depth_regression_diagnostics": ap.get("depth_regression_diagnostics"),
            "convergence_depth_sweep": convergence_sweep,
            "minimum_convergent_depth": minimum_convergent_depth(convergence_sweep),
            "depth_regression_analysis": depth_regression_analysis(convergence_sweep),
        },
        "convergence_driven": {
            "compute_s": cp["compute_seconds"],
            "reference_compute_s": cp["reference_compute_seconds"],
            "passes_executed": cp["passes_executed"],
            "sample_reduction_pct_vs_uniform": cp["sample_reduction_pct"],
            "depth_histogram": cp["depth_histogram"],
            "stop_reason": cp["stop_reason"],
            "overshoot_passes_count": len(overshoot_passes),
            "overshoot_passes": overshoot_passes,
            "pass_history": pass_history,
            "convergence_metrics": metrics_convergence,
            "per_pass_budget_sweep": convergence_pass_sweep(north, south, west, east, pw, ph),
        },
        "depth_vs_convergence": {
            "depth_driven_samples": ap["truth_sample_count"],
            "convergence_driven_samples": cp["truth_sample_count"],
            "convergence_driven_samples_saved": sample_delta,
            "convergence_driven_reduction_vs_depth_pct": sample_reduction_pct,
            "depth_driven_converged": metrics_depth["converged"],
            "convergence_driven_converged": metrics_convergence["converged"],
        },
    }


def _depth_8_regression_summary(results: list[dict]) -> dict:
    """Did convergence-driven prevent the depth-8 regression seen in depth-driven?"""
    summary: dict = {
        "depth_driven_depth_8_regressions": [],
        "convergence_driven_overshoots": [],
    }
    for r in results:
        analysis = r["depth_driven"].get("depth_regression_analysis", {}) or {}
        if analysis.get("depth_8_regresses_vs_depth_6"):
            summary["depth_driven_depth_8_regressions"].append(
                {
                    "viewport": r["viewport"],
                    "likely_cause": analysis.get("likely_cause"),
                    "depth_8_leaf_budget_hit": analysis.get("depth_8_leaf_budget_hit"),
                }
            )
        if r["convergence_driven"].get("overshoot_passes_count", 0) > 0:
            summary["convergence_driven_overshoots"].append(
                {
                    "viewport": r["viewport"],
                    "overshoot_passes_count": r["convergence_driven"]["overshoot_passes_count"],
                    "overshoot_passes": r["convergence_driven"]["overshoot_passes"],
                }
            )
    summary["depth_8_regression_prevented_by_convergence_engine"] = (
        len(summary["depth_driven_depth_8_regressions"]) > 0
        and len(summary["convergence_driven_overshoots"]) == 0
    )
    return summary


def main() -> int:
    results = [run_viewport(vp) for vp in VIEWPORTS]
    depth_8_summary = _depth_8_regression_summary(results)
    report = {
        "description": "Adaptive vs uniform aura benchmark (Sun conjunct ASC truth spine)",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "overlay": OVERLAY,
        "reference_truth_role": REFERENCE_TRUTH_ROLE,
        "convergence_delta_threshold": CONVERGENCE_DELTA_THRESHOLD,
        "default_adaptive_max_depth": DEFAULT_ADAPTIVE_MAX_DEPTH,
        "viewports": results,
        "phase_c_summary": depth_8_summary,
        "notes": [
            "Reference = uniform raster: one swe.houses sample per paint pixel (no blur/interpolation).",
            "Adaptive converged when pixels_above_threshold_pct == 0 at delta 0.05 vs reference.",
            "Depth-driven (legacy): depth 8 regression on asc_band caused by leaf_budget truncation.",
            "Convergence-driven (Phase C): pixel attribution + per-leaf debt + priority queue + "
            "per-pass overshoot guard. No max_depth; spending halts on convergence or guard.",
            "Visual smoothness must come from sample density only; no cosmetic post-process in engine.",
        ],
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(REPORT_PATH), "viewports": len(results)}, indent=2))
    for r in results:
        dd = r["depth_driven"]["convergence_metrics"]
        cd = r["convergence_driven"]["convergence_metrics"]
        savings = r["depth_vs_convergence"]["convergence_driven_reduction_vs_depth_pct"]
        print(
            f"  {r['viewport']}:"
            f" depth-driven samples={dd['sample_count']} converged={dd['converged']} maxΔ={dd['max_delta_vs_reference']};"
            f" convergence-driven samples={cd['sample_count']} passes={cd['passes_executed']} "
            f"converged={cd['converged']} maxΔ={cd['max_delta_vs_reference']} overshoot={cd['overshoot_detected']};"
            f" saved {savings}% samples vs depth-driven"
        )
    print(json.dumps(depth_8_summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
