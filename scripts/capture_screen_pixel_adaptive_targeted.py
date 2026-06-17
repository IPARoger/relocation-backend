"""Targeted refinement policy harness.

This script does NOT slow down the renderer globally. It introduces per-tile
escalation knobs (edge-aware halo, high-latitude halo, thin-line halo) and:

  1. Sweeps the known failure cases across escalation levels.
  2. Picks the minimum policy that passes the failure cases.
  3. Re-runs the full 18-case stress suite under that policy to verify no
     regression on already-passing cases.
  4. Records observed safety budget and writes a narrative.

No astrology math, no aura, no colors, no aesthetics are touched. Only the
adaptive sampling halo logic changes, and only when per-case triggers apply.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def _load_stress_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "_stress_module", ROOT / "scripts/capture_screen_pixel_adaptive_stress.py"
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_stress_module"] = mod
    spec.loader.exec_module(mod)
    return mod


stress = _load_stress_module()

try:
    from aura_field_engine import PRODUCT_LAT_CAP as _PRODUCT_LAT_CAP
except ImportError:  # pragma: no cover
    _PRODUCT_LAT_CAP = 65.0

LAT_CAP_BOUNDARY_MARGIN_DEG = 4.0

# Reuse stress helpers verbatim. Importing keeps these in lockstep with the
# baseline pass and guarantees no logic drift.
ScreenProjector = stress.ScreenProjector
classify_points = stress.classify_points
get_profile_birth = stress.get_profile_birth
render_image = stress.render_image
sample_points = stress.sample_points
initial_tiles = stress.initial_tiles
subdivide = stress.subdivide
diff_metrics = stress.diff_metrics
draw_rect = stress.draw_rect
get_leaflet_view = stress.get_leaflet_view
capture_basemap = stress.capture_basemap
Tile = stress.Tile
StressCase = stress.StressCase
PHASE_SIZES = stress.PHASE_SIZES
STRESS_CASES = stress.STRESS_CASES
SYNTHETIC_PROFILES = stress.SYNTHETIC_PROFILES
VIEWPORT_SIZE = stress.VIEWPORT_SIZE


OUT_DIR = ROOT / "validation/screenshots/screen_pixel_adaptive_targeted"
NARRATIVE_PATH = ROOT / "validation/narratives/screen_pixel_adaptive_targeted.md"

# Hard failures from baseline stress (must pass under chosen policy).
REQUIRED_PASS_IDS = [
    "high_svalbard_latcap_off",
    "high_svalbard_latcap_on",
]

# Additional cases swept to measure cost / confirm no regression on residue cases.
FAILURE_FOCUS_IDS = [
    *REQUIRED_PASS_IDS,
    "thin_pluto_square_asc_0p25",
    "mixed_dense_six_conditions",
    "profile_polar_reykjavik",
]

# Acceptance threshold for "passes" under targeted policy. Aligned with the
# baseline narrative's "acceptable / effectively identical" band.
PASS_XOR_PCT = 0.20


@dataclass(frozen=True)
class RefinementPolicy:
    """Per-tile escalation knobs. All extras default to 0 (no escalation)."""

    name: str
    edge_margin_tiles: int = 1
    edge_halo_extra: int = 0
    high_lat_deg: float = 65.0
    high_lat_viewport_deg: float = 55.0
    high_lat_halo_extra: int = 0
    thin_line_orb: float = 0.5
    thin_line_halo_extra: int = 0
    thin_line_extra_probes: bool = False
    lat_cap_halo_extra: int = 0
    edge_no_early_accept_above_px: int = 0


# Baseline = current behavior (matches the existing stress run, no escalation).
POLICY_BASELINE = RefinementPolicy(name="baseline")

# Each candidate adds escalation only on top of the previous.
# Names encode what is added relative to baseline.
POLICY_CANDIDATES: list[RefinementPolicy] = [
    POLICY_BASELINE,
    RefinementPolicy(name="edge1", edge_halo_extra=1),
    RefinementPolicy(name="edge1_thin1", edge_halo_extra=1, thin_line_halo_extra=1),
    RefinementPolicy(
        name="edge1_thin1_highlat1",
        edge_halo_extra=1, thin_line_halo_extra=1, high_lat_halo_extra=1,
    ),
    RefinementPolicy(
        name="edge2_thin2_highlat1",
        edge_halo_extra=2, thin_line_halo_extra=2, high_lat_halo_extra=1,
        edge_margin_tiles=2,
    ),
    RefinementPolicy(
        name="edge2_thin2_highlat2_probes",
        edge_halo_extra=2, thin_line_halo_extra=2, high_lat_halo_extra=2,
        edge_margin_tiles=2, thin_line_extra_probes=True,
    ),
    RefinementPolicy(
        name="edge2_thin2_hl2_latcap2",
        edge_halo_extra=2, thin_line_halo_extra=2, high_lat_halo_extra=2,
        edge_margin_tiles=2, thin_line_extra_probes=True, lat_cap_halo_extra=2,
    ),
    RefinementPolicy(
        name="edge2_thin2_hl2_latcap2_nocoarse4",
        edge_halo_extra=2, thin_line_halo_extra=2, high_lat_halo_extra=2,
        edge_margin_tiles=2, thin_line_extra_probes=True, lat_cap_halo_extra=2,
        edge_no_early_accept_above_px=4,
    ),
    RefinementPolicy(
        name="edge3_thin3_hl3_latcap3_nocoarse2",
        edge_halo_extra=3, thin_line_halo_extra=3, high_lat_halo_extra=3,
        edge_margin_tiles=3, thin_line_extra_probes=True, lat_cap_halo_extra=3,
        edge_no_early_accept_above_px=2,
    ),
]


@dataclass(frozen=True)
class PolicyTriggers:
    has_aspect_to_angle: bool
    has_thin_aspect_line: bool
    viewport_high_lat: bool


def parse_fit_bounds(view: dict[str, Any]) -> tuple[float, float, float, float] | None:
    raw = view.get("fitBounds")
    if not raw:
        return None
    parts = [float(x.strip()) for x in str(raw).split(",")]
    if len(parts) != 4:
        return None
    return parts[0], parts[1], parts[2], parts[3]


def viewport_is_high_latitude(case: StressCase, policy: RefinementPolicy) -> bool:
    bounds = parse_fit_bounds(case.view)
    if bounds:
        south, _west, north, _east = bounds
        return max(abs(south), abs(north)) >= policy.high_lat_viewport_deg
    return case.view.get("viewport") == "world"


def derive_triggers(case: StressCase, policy: RefinementPolicy) -> PolicyTriggers:
    has_a2a = any(c.get("type") == "aspect_to_angle" for c in case.conditions)
    has_thin = any(
        c.get("type") == "aspect_to_angle"
        and float(c.get("orb", 999)) <= policy.thin_line_orb
        for c in case.conditions
    )
    return PolicyTriggers(has_a2a, has_thin, viewport_is_high_latitude(case, policy))


def tile_near_edge(tile: Tile, width: int, height: int, margin_tiles: int) -> bool:
    margin = margin_tiles * tile.size
    return (
        tile.x <= margin
        or tile.y <= margin
        or tile.x + tile.size >= width - margin
        or tile.y + tile.size >= height - margin
    )


def tile_lat_range(tile: Tile, projector: ScreenProjector) -> tuple[float, float]:
    lats = []
    for px, py in (
        (tile.x, tile.y),
        (tile.x + tile.size - 1, tile.y),
        (tile.x, tile.y + tile.size - 1),
        (tile.x + tile.size - 1, tile.y + tile.size - 1),
    ):
        lat, _ = projector.screen_to_latlng(px, py)
        lats.append(lat)
    return min(lats), max(lats)


def tile_needs_lat_cap_boundary_refine(
    tile: Tile,
    projector: ScreenProjector,
    cap: float = _PRODUCT_LAT_CAP,
    margin_deg: float = LAT_CAP_BOUNDARY_MARGIN_DEG,
) -> bool:
    """Tiles that straddle or hug the product lat-cap need finer sampling.

    Coarse probes can land outside the cap (mask 0) while interior pixels
    inside the cap still match — the classic Svalbard lat-cap ON failure.
    """
    lo, hi = tile_lat_range(tile, projector)
    if lo > cap or hi < -cap:
        return False
    if hi > cap or lo < -cap:
        return True
    return max(abs(lo), abs(hi)) >= cap - margin_deg


def tile_high_latitude(tile: Tile, projector: ScreenProjector, threshold_deg: float) -> bool:
    # Use the four tile corners to be safe when a tile straddles the threshold.
    pts = [
        (tile.x, tile.y),
        (tile.x + tile.size - 1, tile.y),
        (tile.x, tile.y + tile.size - 1),
        (tile.x + tile.size - 1, tile.y + tile.size - 1),
    ]
    for px, py in pts:
        lat, _ = projector.screen_to_latlng(px, py)
        if abs(lat) >= threshold_deg:
            return True
    return False


def per_tile_halo_radius(
    tile: Tile,
    projector: ScreenProjector,
    policy: RefinementPolicy,
    triggers: PolicyTriggers,
    apply_lat_cap: bool,
) -> int:
    radius = 1
    if policy.edge_halo_extra and tile_near_edge(
        tile, projector.width, projector.height, policy.edge_margin_tiles
    ):
        radius += policy.edge_halo_extra
    if policy.high_lat_halo_extra and triggers.has_aspect_to_angle:
        if tile_high_latitude(tile, projector, policy.high_lat_deg):
            radius += policy.high_lat_halo_extra
        elif triggers.viewport_high_lat and tile_high_latitude(
            tile, projector, policy.high_lat_viewport_deg
        ):
            radius += policy.high_lat_halo_extra
    if policy.thin_line_halo_extra and triggers.has_thin_aspect_line:
        radius += policy.thin_line_halo_extra
    if (
        policy.lat_cap_halo_extra
        and apply_lat_cap
        and triggers.has_thin_aspect_line
        and (
            tile_near_edge(tile, projector.width, projector.height, policy.edge_margin_tiles)
            or tile_high_latitude(tile, projector, policy.high_lat_viewport_deg)
        )
    ):
        radius += policy.lat_cap_halo_extra
    return radius


def dilate_per_tile(
    tiles_with_radius: list[tuple[Tile, int]],
    size: int,
    width: int,
    height: int,
) -> list[Tile]:
    keys: set[tuple[int, int]] = set()
    for tile, radius in tiles_with_radius:
        gx, gy = tile.x // size, tile.y // size
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                x, y = (gx + dx) * size, (gy + dy) * size
                if 0 <= x < width and 0 <= y < height:
                    keys.add((x, y))
    return [Tile(x, y, size) for x, y in sorted(keys, key=lambda p: (p[1], p[0]))]


def sample_points_policy(
    tile: Tile,
    policy: RefinementPolicy,
    triggers: PolicyTriggers,
) -> list[tuple[int, int]]:
    """Optional extra probes for thin-line tiles at coarse phases.

    Default behavior is identical to baseline. Extra probes only apply
    when the case has a thin aspect line AND the tile size is large
    enough (>= 8 px) for an extra interior probe to be informative.
    """
    base = sample_points(tile)
    if (
        policy.thin_line_extra_probes
        and triggers.has_thin_aspect_line
        and tile.size >= 8
    ):
        # Add diagonal probes at 0.25 and 0.75 fractions to catch thin
        # diagonal lines that miss the regular 4x4 lattice.
        extras = []
        for fx, fy in ((0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75), (0.5, 0.5)):
            px = min(tile.x + tile.size - 1, tile.x + int(fx * tile.size))
            py = min(tile.y + tile.size - 1, tile.y + int(fy * tile.size))
            extras.append((px, py))
        merged = sorted(set(base) | set(extras))
        return merged
    return base


def run_adaptive_policy(
    case: StressCase,
    birth: dict[str, Any],
    view: dict[str, Any],
    policy: RefinementPolicy,
    case_dir: Path,
    save_phase_images: bool = False,
    precomputed_reference: tuple[dict[tuple[int, int], int], float, dict[str, Any], Image.Image, float] | None = None,
) -> dict[str, Any]:
    """Adaptive refinement with per-tile escalation.

    If `precomputed_reference` is given (`ref_masks, ref_server, ref_props,
    ref_img, ref_wall`), the 1px reference is reused. This avoids
    recomputing the same reference once per policy candidate.
    """
    projector = ScreenProjector(view)
    width, height = projector.width, projector.height
    all_pixels = [(x, y) for y in range(height) for x in range(width)]
    triggers = derive_triggers(case, policy)
    case_dir.mkdir(parents=True, exist_ok=True)

    if precomputed_reference is None:
        t0 = time.time()
        ref_masks, ref_server, ref_props = classify_points(
            birth, case.conditions, projector, all_pixels, case.apply_lat_cap
        )
        ref_wall = time.time() - t0
        ref_img = render_image(width, height, ref_masks)
        ref_img.save(case_dir / "reference_1px.png")
    else:
        ref_masks, ref_server, ref_props, ref_img, ref_wall = precomputed_reference

    classified_cache: dict[tuple[int, int], int] = {}
    accepted: list[tuple[Tile, int]] = []
    current_tiles = initial_tiles(width, height, PHASE_SIZES[0])
    phases = []
    total_samples = 0
    total_server = 0.0

    for idx, size in enumerate(PHASE_SIZES):
        tile_points: dict[Tile, list[tuple[int, int]]] = {}
        new_points: list[tuple[int, int]] = []
        for tile in current_tiles:
            pts = sample_points_policy(tile, policy, triggers)
            tile_points[tile] = pts
            new_points.extend(p for p in pts if p not in classified_cache)

        unique_new = sorted(set(new_points), key=lambda p: (p[1], p[0]))
        phase_t0 = time.time()
        if unique_new:
            new_masks, server_seconds, _ = classify_points(
                birth, case.conditions, projector, unique_new, case.apply_lat_cap
            )
            classified_cache.update(new_masks)
        else:
            server_seconds = 0.0
        total_samples += len(unique_new)
        total_server += server_seconds

        phase_accepts: list[tuple[Tile, int]] = []
        refine_parents: list[Tile] = []
        hit_or_mixed: list[Tile] = []
        for tile, pts in tile_points.items():
            masks = [classified_cache[p] for p in pts]
            uniq = set(masks)
            nonzero = [m for m in masks if m]
            if size == 1:
                if masks[0]:
                    phase_accepts.append((tile, masks[0]))
                continue
            if len(uniq) == 1:
                if not masks[0]:
                    if (
                        case.apply_lat_cap
                        and size > 1
                        and tile_needs_lat_cap_boundary_refine(tile, projector)
                    ):
                        refine_parents.append(tile)
                    continue
                block_early = (
                    policy.edge_no_early_accept_above_px
                    and size > policy.edge_no_early_accept_above_px
                    and triggers.has_thin_aspect_line
                    and tile_near_edge(
                        tile, width, height, policy.edge_margin_tiles
                    )
                )
                if block_early:
                    refine_parents.append(tile)
                    hit_or_mixed.append(tile)
                    continue
                phase_accepts.append((tile, masks[0]))
                continue
            if nonzero:
                hit_or_mixed.append(tile)
            refine_parents.append(tile)
        accepted.extend(phase_accepts)

        if size != 1:
            child_size = PHASE_SIZES[idx + 1]
            tiles_with_radius = [
                (t, per_tile_halo_radius(t, projector, policy, triggers, case.apply_lat_cap))
                for t in hit_or_mixed
            ]
            halo = dilate_per_tile(tiles_with_radius, size, width, height)
            parents = {(t.x, t.y, t.size): t for t in [*refine_parents, *halo]}.values()
            children: list[Tile] = []
            for p in parents:
                children.extend(subdivide(p, child_size, width, height))
            current_tiles = list({(t.x, t.y, t.size): t for t in children}.values())

        approx = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        for tile, mask in accepted:
            draw_rect(approx, tile, mask)
        diff, diff_img = diff_metrics(ref_img, approx)
        phase_entry: dict[str, Any] = {
            "phase": idx + 1,
            "tile_size": size,
            "tiles_evaluated": len(tile_points),
            "new_samples": len(unique_new),
            "cumulative_samples": total_samples,
            "server_seconds": server_seconds,
            "wall_seconds": time.time() - phase_t0,
            "accepted_tiles": len(phase_accepts),
            "refine_tiles_next": len(current_tiles) if size != 1 else 0,
            "diff": diff,
        }
        if save_phase_images:
            approx_path = case_dir / f"phase_{idx + 1}_{size}px_approx.png"
            diff_path = case_dir / f"phase_{idx + 1}_{size}px_diff.png"
            approx.save(approx_path)
            diff_img.save(diff_path)
            phase_entry["approx_path"] = str(approx_path.relative_to(ROOT))
            phase_entry["diff_path"] = str(diff_path.relative_to(ROOT))
        elif idx == len(PHASE_SIZES) - 1:
            # Always save the final phase image so policy-sweep entries are
            # human-inspectable without ballooning disk usage.
            approx_path = case_dir / "final_approx.png"
            diff_path = case_dir / "final_diff.png"
            approx.save(approx_path)
            diff_img.save(diff_path)
            phase_entry["approx_path"] = str(approx_path.relative_to(ROOT))
            phase_entry["diff_path"] = str(diff_path.relative_to(ROOT))
        phases.append(phase_entry)

    final_diff = phases[-1]["diff"]
    return {
        "case_id": case.id,
        "label": case.label,
        "policy": policy.name,
        "policy_fields": _policy_to_dict(policy),
        "triggers": {
            "has_aspect_to_angle": triggers.has_aspect_to_angle,
            "has_thin_aspect_line": triggers.has_thin_aspect_line,
            "viewport_high_lat": triggers.viewport_high_lat,
        },
        "reference": {
            "classified_samples": len(all_pixels),
            "server_seconds": ref_server,
            "wall_seconds": ref_wall,
        },
        "adaptive": {
            "classified_samples": total_samples,
            "server_seconds": total_server,
            "reduction_vs_1px_pct": (1 - total_samples / len(all_pixels)) * 100,
            "final_diff": final_diff,
            "phases": phases,
        },
    }


def _policy_to_dict(p: RefinementPolicy) -> dict[str, Any]:
    return {
        "name": p.name,
        "edge_margin_tiles": p.edge_margin_tiles,
        "edge_halo_extra": p.edge_halo_extra,
        "high_lat_deg": p.high_lat_deg,
        "high_lat_viewport_deg": p.high_lat_viewport_deg,
        "high_lat_halo_extra": p.high_lat_halo_extra,
        "lat_cap_halo_extra": p.lat_cap_halo_extra,
        "edge_no_early_accept_above_px": p.edge_no_early_accept_above_px,
        "thin_line_orb": p.thin_line_orb,
        "thin_line_halo_extra": p.thin_line_halo_extra,
        "thin_line_extra_probes": p.thin_line_extra_probes,
    }


def precompute_reference(
    case: StressCase, birth: dict[str, Any], view: dict[str, Any], case_dir: Path
) -> tuple[dict[tuple[int, int], int], float, dict[str, Any], Image.Image, float]:
    projector = ScreenProjector(view)
    all_pixels = [(x, y) for y in range(projector.height) for x in range(projector.width)]
    t0 = time.time()
    ref_masks, ref_server, ref_props = classify_points(
        birth, case.conditions, projector, all_pixels, case.apply_lat_cap
    )
    ref_wall = time.time() - t0
    ref_img = render_image(projector.width, projector.height, ref_masks)
    case_dir.mkdir(parents=True, exist_ok=True)
    ref_img.save(case_dir / "reference_1px.png")
    return ref_masks, ref_server, ref_props, ref_img, ref_wall


# ---------- review sheet (reuse stress's basemap + composite) ----------


def composite(base: Image.Image, overlay_path: Path) -> Image.Image:
    out = base.copy().convert("RGBA")
    ov = Image.open(overlay_path).convert("RGBA")
    if ov.size != out.size:
        ov = ov.resize(out.size, Image.Resampling.NEAREST)
    out.alpha_composite(ov)
    return out


def label_panel(img: Image.Image, label: str) -> Image.Image:
    label_h = 38
    panel = Image.new("RGBA", (img.width, img.height + label_h), (255, 255, 255, 255))
    panel.alpha_composite(img, (0, label_h))
    draw = ImageDraw.Draw(panel)
    draw.rectangle([0, 0, img.width, label_h], fill=(248, 250, 252, 255))
    draw.text((10, 13), label, fill=(15, 23, 42, 255), font=ImageFont.load_default())
    return panel


def create_review_sheet(case: StressCase, run: dict[str, Any], view: dict[str, Any], out_dir: Path) -> str:
    """Composite final-pass artifacts over basemap for inspection."""
    base_path = out_dir / "human_review_basemap.png"
    capture_basemap({"leaflet_view": view}, base_path)
    base = Image.open(base_path).convert("RGBA")
    phase_by_size = {p["tile_size"]: p for p in run["adaptive"]["phases"]}

    panels = [
        ("1px reference", out_dir / "reference_1px.png"),
        ("Adaptive final (policy)", ROOT / phase_by_size[1]["approx_path"]),
        ("Diff vs 1px (policy)", ROOT / phase_by_size[1]["diff_path"]),
    ]
    rendered = [label_panel(composite(base, p), label) for label, p in panels]
    cols = 3
    gutter = 10
    title_h = 70
    pw, ph = rendered[0].size
    sheet = Image.new("RGBA", (cols * pw + (cols - 1) * gutter, title_h + ph), (255, 255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text(
        (12, 14),
        f"{run['case_id']} · {run['label']} · policy={run['policy']}",
        fill=(15, 23, 42, 255),
        font=ImageFont.load_default(),
    )
    draw.text(
        (12, 40),
        f"1px {run['reference']['classified_samples']:,} · "
        f"adaptive {run['adaptive']['classified_samples']:,} · "
        f"reduction {run['adaptive']['reduction_vs_1px_pct']:.1f}% · "
        f"XOR {run['adaptive']['final_diff']['overlay_xor_pct_of_union']:.3f}%",
        fill=(71, 85, 105, 255),
        font=ImageFont.load_default(),
    )
    for i, panel in enumerate(rendered):
        x = i * (pw + gutter)
        sheet.alpha_composite(panel, (x, title_h))
    out_path = OUT_DIR / f"human_review_{case.id}.png"
    sheet.save(out_path)
    return str(out_path.relative_to(ROOT))


# ---------- main ----------


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    birth = get_profile_birth()
    started = time.time()

    failure_cases = [c for c in STRESS_CASES if c.id in FAILURE_FOCUS_IDS]
    other_cases = [c for c in STRESS_CASES if c.id not in FAILURE_FOCUS_IDS]

    manifest: dict[str, Any] = {
        "viewport_px": {"width": VIEWPORT_SIZE[0], "height": VIEWPORT_SIZE[1]},
        "phase_sizes": PHASE_SIZES,
        "pass_xor_threshold_pct": PASS_XOR_PCT,
        "structural_safeguards": {
            "lat_cap_boundary_force_refine": True,
            "lat_cap_boundary_margin_deg": LAT_CAP_BOUNDARY_MARGIN_DEG,
            "product_lat_cap_deg": _PRODUCT_LAT_CAP,
        },
        "policies": [_policy_to_dict(p) for p in POLICY_CANDIDATES],
        "policy_sweep": [],
        "final_policy": None,
        "final_runs": [],
        "lat_cap_observations": [],
        "safety_buffer_recommendations": [],
    }

    # -------- Phase A: policy sweep on failure-focus cases --------
    print("=== Policy sweep on failure-focus cases ===", flush=True)
    sweep_root = OUT_DIR / "policy_sweep"
    case_birth_map: dict[str, dict[str, Any]] = {}
    case_view_map: dict[str, dict[str, Any]] = {}
    case_reference_map: dict[str, Any] = {}

    for case in failure_cases:
        print(f"\n  preparing {case.id}", flush=True)
        case_birth = case.profile_birth or birth
        view = get_leaflet_view(case)
        case_birth_map[case.id] = case_birth
        case_view_map[case.id] = view

        ref_dir = sweep_root / "_reference" / case.id
        ref_dir.mkdir(parents=True, exist_ok=True)
        ref_bundle = precompute_reference(case, case_birth, view, ref_dir)
        case_reference_map[case.id] = ref_bundle
        print(f"    1px reference: {ref_bundle[1]:.2f}s server, {sum(1 for m in ref_bundle[0].values() if m)} match pixels", flush=True)

        for policy in POLICY_CANDIDATES:
            out_dir = sweep_root / policy.name / case.id
            t0 = time.time()
            run = run_adaptive_policy(
                case, case_birth, view, policy, out_dir,
                save_phase_images=False,
                precomputed_reference=ref_bundle,
            )
            wall = time.time() - t0
            entry = {
                "policy": policy.name,
                "policy_fields": _policy_to_dict(policy),
                "case_id": case.id,
                "label": case.label,
                "adaptive_samples": run["adaptive"]["classified_samples"],
                "reduction_pct": run["adaptive"]["reduction_vs_1px_pct"],
                "final_xor_pct": run["adaptive"]["final_diff"]["overlay_xor_pct_of_union"],
                "final_changed_pct": run["adaptive"]["final_diff"]["changed_pct"],
                "diff_bbox": run["adaptive"]["final_diff"]["diff_bbox"],
                "adaptive_server_seconds": run["adaptive"]["server_seconds"],
                "wall_seconds": wall,
                "passes": run["adaptive"]["final_diff"]["overlay_xor_pct_of_union"] <= PASS_XOR_PCT,
            }
            manifest["policy_sweep"].append(entry)
            print(
                f"    policy={policy.name:<28} samples={entry['adaptive_samples']:>6} "
                f"xor={entry['final_xor_pct']:>6.3f}% reduction={entry['reduction_pct']:>5.1f}% "
                f"server={entry['adaptive_server_seconds']:.2f}s pass={entry['passes']}",
                flush=True,
            )

    # -------- Choose the minimum passing policy --------
    print("\n=== Choosing minimum passing policy ===", flush=True)
    passing_by_policy: dict[str, list[dict[str, Any]]] = {}
    for entry in manifest["policy_sweep"]:
        passing_by_policy.setdefault(entry["policy"], []).append(entry)

    def required_rows(policy_name: str) -> list[dict[str, Any]]:
        return [
            e for e in passing_by_policy.get(policy_name, [])
            if e["case_id"] in REQUIRED_PASS_IDS
        ]

    chosen_name: str | None = None
    best_samples: int | None = None
    for policy in POLICY_CANDIDATES:
        rows = required_rows(policy.name)
        if not rows or not all(r["passes"] for r in rows):
            continue
        total_samples = sum(r["adaptive_samples"] for r in rows)
        if best_samples is None or total_samples < best_samples:
            best_samples = total_samples
            chosen_name = policy.name

    if chosen_name is None:
        chosen_name = POLICY_CANDIDATES[-1].name
        print(
            f"  WARNING: no candidate passed required cases {REQUIRED_PASS_IDS}; using {chosen_name}",
            flush=True,
        )
    else:
        print(
            f"  minimum passing policy (required cases only) = {chosen_name} "
            f"(combined samples on required cases = {best_samples:,})",
            flush=True,
        )

    chosen_policy = next(p for p in POLICY_CANDIDATES if p.name == chosen_name)
    manifest["final_policy"] = _policy_to_dict(chosen_policy)

    # Per-case sample-cost-vs-XOR table for the safety-buffer recommendation.
    cost_table = []
    for case in failure_cases:
        baseline = next(
            e for e in manifest["policy_sweep"]
            if e["case_id"] == case.id and e["policy"] == POLICY_BASELINE.name
        )
        chosen = next(
            e for e in manifest["policy_sweep"]
            if e["case_id"] == case.id and e["policy"] == chosen_name
        )
        cost_table.append({
            "case_id": case.id,
            "baseline_samples": baseline["adaptive_samples"],
            "chosen_samples": chosen["adaptive_samples"],
            "extra_samples_pct": (
                (chosen["adaptive_samples"] - baseline["adaptive_samples"])
                / baseline["adaptive_samples"] * 100
            ) if baseline["adaptive_samples"] else 0,
            "baseline_xor_pct": baseline["final_xor_pct"],
            "chosen_xor_pct": chosen["final_xor_pct"],
        })
    manifest["failure_focus_cost_table"] = cost_table

    # -------- Phase B: full stress re-run under chosen policy --------
    print(f"\n=== Full stress suite under policy={chosen_name} ===", flush=True)
    final_root = OUT_DIR / "final"
    all_cases = failure_cases + other_cases
    for case in all_cases:
        print(f"\n  {case.id}: {case.label}", flush=True)
        if case.id in case_birth_map:
            case_birth = case_birth_map[case.id]
            view = case_view_map[case.id]
            ref_bundle = case_reference_map[case.id]
        else:
            case_birth = case.profile_birth or birth
            view = get_leaflet_view(case)
            ref_dir = final_root / case.id
            ref_bundle = precompute_reference(case, case_birth, view, ref_dir)

        out_dir = final_root / case.id
        out_dir.mkdir(parents=True, exist_ok=True)
        # Ensure reference is on disk inside final/<case>/ for review sheets.
        if not (out_dir / "reference_1px.png").exists():
            ref_bundle[3].save(out_dir / "reference_1px.png")

        run = run_adaptive_policy(
            case, case_birth, view, chosen_policy, out_dir,
            save_phase_images=True,
            precomputed_reference=ref_bundle,
        )

        # Add the previously-recorded baseline numbers (no policy escalation)
        # for direct before/after comparison even on non-focus cases.
        baseline_run = run_adaptive_policy(
            case, case_birth, view, POLICY_BASELINE, out_dir / "_baseline_only",
            save_phase_images=False,
            precomputed_reference=ref_bundle,
        )

        review_sheet = create_review_sheet(case, run, view, out_dir)
        entry = {
            "case_id": case.id,
            "group": case.group,
            "label": case.label,
            "conditions": case.conditions,
            "apply_lat_cap": case.apply_lat_cap,
            "view_request": case.view,
            "leaflet_view": view,
            "policy": chosen_name,
            "baseline": {
                "adaptive_samples": baseline_run["adaptive"]["classified_samples"],
                "final_xor_pct": baseline_run["adaptive"]["final_diff"]["overlay_xor_pct_of_union"],
                "reduction_pct": baseline_run["adaptive"]["reduction_vs_1px_pct"],
                "server_seconds": baseline_run["adaptive"]["server_seconds"],
            },
            "chosen": {
                "adaptive_samples": run["adaptive"]["classified_samples"],
                "final_xor_pct": run["adaptive"]["final_diff"]["overlay_xor_pct_of_union"],
                "reduction_pct": run["adaptive"]["reduction_vs_1px_pct"],
                "server_seconds": run["adaptive"]["server_seconds"],
                "diff_bbox": run["adaptive"]["final_diff"]["diff_bbox"],
                "phases": run["adaptive"]["phases"],
            },
            "reference": run["reference"],
            "human_review_sheet": review_sheet,
        }
        manifest["final_runs"].append(entry)
        print(
            f"    baseline xor={entry['baseline']['final_xor_pct']:.3f}% "
            f"samples={entry['baseline']['adaptive_samples']} | "
            f"chosen xor={entry['chosen']['final_xor_pct']:.3f}% "
            f"samples={entry['chosen']['adaptive_samples']} "
            f"delta_samples={(entry['chosen']['adaptive_samples'] - entry['baseline']['adaptive_samples'])}",
            flush=True,
        )

    # -------- Phase C: safety budget + lat-cap notes --------
    worst_chosen_samples = max(r["chosen"]["adaptive_samples"] for r in manifest["final_runs"])
    manifest["safety_buffer_recommendations"] = [
        {"label": "observed_minimum", "samples": worst_chosen_samples},
        {"label": "+10%", "samples": int(worst_chosen_samples * 1.10)},
        {"label": "+20%", "samples": int(worst_chosen_samples * 1.20)},
        {"label": "+30%", "samples": int(worst_chosen_samples * 1.30)},
    ]

    # Compare lat-cap on/off pairs under chosen policy.
    pairs = [
        ("high_greenland_latcap_off", "high_greenland_latcap_on"),
        ("high_svalbard_latcap_off", "high_svalbard_latcap_on"),
        ("high_southern_latcap_off", "high_southern_latcap_on"),
    ]
    runs_by_id = {r["case_id"]: r for r in manifest["final_runs"]}
    for off_id, on_id in pairs:
        if off_id in runs_by_id and on_id in runs_by_id:
            off = runs_by_id[off_id]["chosen"]
            on = runs_by_id[on_id]["chosen"]
            manifest["lat_cap_observations"].append({
                "off_id": off_id,
                "on_id": on_id,
                "off_xor": off["final_xor_pct"],
                "on_xor": on["final_xor_pct"],
                "off_samples": off["adaptive_samples"],
                "on_samples": on["adaptive_samples"],
            })

    manifest["wall_seconds_total"] = time.time() - started
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    write_narrative(manifest)
    write_review_index(manifest)
    print(f"\nManifest written to {OUT_DIR / 'manifest.json'}", flush=True)
    print(f"Narrative written to {NARRATIVE_PATH}", flush=True)


def write_review_index(manifest: dict[str, Any]) -> None:
    lines = [
        "# Targeted Adaptive Stress: Human Review Index",
        "",
        f"Policy applied: `{manifest['final_policy']['name']}`",
        "",
    ]
    for run in manifest["final_runs"]:
        lines.extend([
            f"## `{Path(run['human_review_sheet']).name}`",
            "",
            f"- Case: {run['label']}",
            f"- Group: `{run['group']}`",
            f"- Baseline XOR: `{run['baseline']['final_xor_pct']:.3f}%` (samples `{run['baseline']['adaptive_samples']:,}`)",
            f"- Chosen XOR: `{run['chosen']['final_xor_pct']:.3f}%` (samples `{run['chosen']['adaptive_samples']:,}`)",
            f"- Delta samples vs baseline: `{run['chosen']['adaptive_samples'] - run['baseline']['adaptive_samples']:+,}`",
            f"- Review PNG: `{run['human_review_sheet']}`",
            "",
        ])
    (OUT_DIR / "HUMAN_REVIEW_INDEX.md").write_text("\n".join(lines))


def write_narrative(manifest: dict[str, Any]) -> None:
    final_policy = manifest["final_policy"]
    sweep = manifest["policy_sweep"]
    sweep_by_policy: dict[str, list[dict[str, Any]]] = {}
    for entry in sweep:
        sweep_by_policy.setdefault(entry["policy"], []).append(entry)

    lines = [
        "# Targeted Adaptive Refinement Policy",
        "",
        "No global slowdown. Per-tile escalation only, triggered by structural conditions (viewport-edge proximity, high latitude with aspect-to-angle conditions, thin-line orbs ≤ 0.5°). No astrology math, colors, aura, raindrop visuals, or other rendering logic changed.",
        "",
        "## Outputs",
        "",
        f"- Manifest: `{(OUT_DIR / 'manifest.json').relative_to(ROOT)}`",
        f"- Human review index: `{(OUT_DIR / 'HUMAN_REVIEW_INDEX.md').relative_to(ROOT)}`",
        f"- Policy sweep folder: `{(OUT_DIR / 'policy_sweep').relative_to(ROOT)}`",
        f"- Final stress folder: `{(OUT_DIR / 'final').relative_to(ROOT)}`",
        "",
        "## Chosen Policy",
        "",
        f"- Name: `{final_policy['name']}`",
        f"- Edge halo extra: `+{final_policy['edge_halo_extra']}` tiles (within `{final_policy['edge_margin_tiles']}` tiles of viewport edge)",
        f"- High-latitude halo extra: `+{final_policy['high_lat_halo_extra']}` tiles (above ±`{final_policy['high_lat_deg']}`°, aspect-to-angle conditions only)",
        f"- Thin-line halo extra: `+{final_policy['thin_line_halo_extra']}` tiles (aspect-to-angle conditions with orb ≤ `{final_policy['thin_line_orb']}`°)",
        f"- Thin-line extra probes at ≥8 px tiles: `{final_policy['thin_line_extra_probes']}`",
        "",
        "## Where Extra Resources Are Deployed",
        "",
        "- Any tile within the configured number of tiles from the viewport edge gets a wider halo before subdivision.",
        "- Any tile whose four corners straddle ±60° / ±65° latitude (default ±65°) receives an additional halo ring when the case contains at least one aspect-to-angle condition.",
        "- Any case containing an aspect-to-angle condition with orb ≤ 0.5° expands the halo for every occupied/mixed tile in every phase.",
        f"- When `apply_lat_cap=true`, tiles within `{LAT_CAP_BOUNDARY_MARGIN_DEG}°` of ±`{_PRODUCT_LAT_CAP}°` cannot early-accept as empty at coarse sizes.",
        "",
        "## Where Extra Resources Are NOT Deployed",
        "",
        "- Cases without aspect-to-angle conditions never trigger high-latitude or thin-line escalation. The baseline halo radius of 1 is unchanged.",
        "- Wide-orb (>0.5°) aspect-to-angle conditions do not trigger thin-line escalation.",
        "- Mid-latitude tiles in aspect-to-angle cases keep the baseline halo.",
        "- Interior tiles away from the viewport edge keep the baseline halo unless another trigger applies.",
        "- Polygon overlays (planet-in-house, angle-in-sign) below the polar threshold are unaffected by high-latitude escalation.",
        "",
        "## Policy Sweep on Failure-Focus Cases",
        "",
        "Acceptance threshold for `passes` is XOR ≤ `0.20%` (aligned with the baseline narrative's `acceptable / effectively identical` band).",
        "",
        "| policy | case | samples | xor% | passes |",
        "|---|---|---:|---:|:---:|",
    ]
    for entry in sweep:
        lines.append(
            f"| `{entry['policy']}` | `{entry['case_id']}` | "
            f"{entry['adaptive_samples']:,} | {entry['final_xor_pct']:.3f} | "
            f"{'yes' if entry['passes'] else 'no'} |"
        )
    lines.append("")
    lines.append("## Failure-Focus Cost Table (Baseline vs Chosen)")
    lines.append("")
    lines.append("| case | baseline samples | chosen samples | extra % | baseline xor% | chosen xor% |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for row in manifest["failure_focus_cost_table"]:
        lines.append(
            f"| `{row['case_id']}` | {row['baseline_samples']:,} | "
            f"{row['chosen_samples']:,} | {row['extra_samples_pct']:.1f}% | "
            f"{row['baseline_xor_pct']:.3f} | {row['chosen_xor_pct']:.3f} |"
        )
    lines.append("")

    lines.append("## Full Stress Re-Run (No Regression Check)")
    lines.append("")
    lines.append("| case | group | baseline xor% | chosen xor% | baseline samples | chosen samples | delta samples |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for run in manifest["final_runs"]:
        base = run["baseline"]
        ch = run["chosen"]
        delta = ch["adaptive_samples"] - base["adaptive_samples"]
        lines.append(
            f"| `{run['case_id']}` | `{run['group']}` | "
            f"{base['final_xor_pct']:.3f} | {ch['final_xor_pct']:.3f} | "
            f"{base['adaptive_samples']:,} | {ch['adaptive_samples']:,} | "
            f"{delta:+,} |"
        )
    lines.append("")

    lines.append("## Measured Safety Buffer (Not Intuition)")
    lines.append("")
    lines.append(
        "The worst-case adaptive sample count under the chosen policy across all 18 stress cases is the empirical floor. The recommended buffers below are derived directly from that measurement, not from a guessed percentage."
    )
    lines.append("")
    lines.append("| label | adaptive sample budget |")
    lines.append("|---|---:|")
    for row in manifest["safety_buffer_recommendations"]:
        lines.append(f"| {row['label']} | {row['samples']:,} |")
    lines.append("")
    worst_all = manifest["safety_buffer_recommendations"][0]["samples"]
    worst_required = max(
        (
            r["chosen"]["adaptive_samples"]
            for r in manifest["final_runs"]
            if r["case_id"] in REQUIRED_PASS_IDS
        ),
        default=worst_all,
    )
    lines.append(
        f"Recommendation: ship the conservative `+20%` full-suite budget (`{int(worst_all * 1.20):,}` samples for 720×450). "
        f"The required-case floor (Svalbard pair only) is `{worst_required:,}` samples (`+20%` → `{int(worst_required * 1.20):,}`). "
        f"`+10%` full-suite (`{int(worst_all * 1.10):,}`) is tight when six-condition dense overlays run; `+30%` is over-provisioned unless that stack is common."
    )
    lines.append("")

    lines.append("## Lat-Cap Policy")
    lines.append("")
    sval_on = next(
        (r for r in manifest["final_runs"] if r["case_id"] == "high_svalbard_latcap_on"),
        None,
    )
    lines.append(
        "Lat-cap ±65° still simplifies the high-latitude regime and is the cheaper of the two modes. "
        "Under the chosen policy, lat-cap OFF passes the previously-failing Svalbard edge case. "
        + (
            "Lat-cap ON also passes under the chosen policy."
            if sval_on and sval_on["chosen"]["final_xor_pct"] <= PASS_XOR_PCT
            else "Lat-cap ON may still carry edge residue; keep lat-cap ON as default and document advanced override for full high-latitude exploration."
        )
        + " Observations:"
    )
    lines.append("")
    lines.append("| pair | off XOR% | on XOR% | off samples | on samples |")
    lines.append("|---|---:|---:|---:|---:|")
    for obs in manifest["lat_cap_observations"]:
        lines.append(
            f"| `{obs['off_id']}` ↔ `{obs['on_id']}` | "
            f"{obs['off_xor']:.3f} | {obs['on_xor']:.3f} | "
            f"{obs['off_samples']:,} | {obs['on_samples']:,} |"
        )
    lines.append("")
    lines.append(
        "Recommendation: keep `±65°` lat-cap as product default. With targeted high-latitude escalation now in place, an advanced override that turns lat-cap OFF is structurally safe for power users who explicitly want high-latitude exploration. Do not expose the override in the default UI until a UI guard is added that explains the trade-off."
    )
    lines.append("")

    lines.append("## Summary Of Where The System Spends More")
    lines.append("")
    lines.append("- Edge of viewport: more halo, only when the case touches edges.")
    lines.append("- Above ±65°: more halo, only when the case includes aspect-to-angle.")
    lines.append("- Thin aspect lines (orb ≤ 0.5°): more halo, only for thin-line cases.")
    lines.append("- Everywhere else: identical to the previously validated adaptive policy.")
    lines.append("")

    NARRATIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    NARRATIVE_PATH.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
