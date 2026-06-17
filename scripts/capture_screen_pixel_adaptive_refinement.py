"""Adaptive screen-space refinement proof.

This is the corrected optimisation target:

    NOT: choose one global block size instead of 1px.
    YES: start sparse, stop in stable empty/filled regions, and refine only
         where occupancy or boundaries require it.

The script compares:
  A. full 1px screen-space truth
  B. adaptive refinement toward that same 1px truth

It uses the same `/screen-pixel-truth` endpoint and the same astrology math.
Only the sampling strategy changes.
"""

from __future__ import annotations

import json
import math
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageChops, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright


BASE = "http://127.0.0.1:8000"
PROFILE = "baseline_validated"
VIEWPORT_SIZE = (960, 600)
OUT_DIR = Path("validation/screenshots/screen_pixel_adaptive_refinement")

CHUNK_SIZE = 400_000
PHASE_SIZES = [16, 8, 4, 2, 1]

MASK_PALETTE: dict[int, tuple[int, int, int, int]] = {
    1: (252, 211, 77, 140),
    2: (56, 189, 248, 140),
    4: (244, 114, 182, 140),
    3: (34, 197, 94, 153),
    5: (249, 115, 22, 153),
    6: (167, 139, 250, 153),
    7: (15, 23, 42, 140),
}


@dataclass(frozen=True)
class Tile:
    x: int
    y: int
    size: int


@dataclass(frozen=True)
class Case:
    id: str
    label: str
    conditions: list[dict[str, Any]]
    view: dict[str, str]


CASES = [
    Case(
        id="sun_1st_world",
        label="Sun in 1st, world",
        conditions=[{"type": "planet_in_house", "id": "A", "planet": "sun", "house": 1}],
        view={"viewport": "world"},
    ),
    Case(
        id="sun_1st_americas_overlap_scale",
        label="Sun in 1st, Americas/regional",
        conditions=[{"type": "planet_in_house", "id": "A", "planet": "sun", "house": 1}],
        view={"fitBounds": "-55,-160,70,-30"},
    ),
    Case(
        id="saturn_mc_0p5_pacific",
        label="Saturn conjunct MC, orb 0.5, Pacific",
        conditions=[{
            "type": "aspect_to_angle", "id": "A", "planet": "saturn",
            "angle": "mc", "aspect": "conjunction", "orb": 0.5,
        }],
        view={"fitBounds": "-65,150,65,180"},
    ),
    Case(
        id="saturn_mc_1_pacific",
        label="Saturn conjunct MC, orb 1, Pacific",
        conditions=[{
            "type": "aspect_to_angle", "id": "A", "planet": "saturn",
            "angle": "mc", "aspect": "conjunction", "orb": 1.0,
        }],
        view={"fitBounds": "-65,150,65,180"},
    ),
    Case(
        id="saturn_asc_1_world",
        label="Saturn conjunct ASC, orb 1, world",
        conditions=[{
            "type": "aspect_to_angle", "id": "A", "planet": "saturn",
            "angle": "asc", "aspect": "conjunction", "orb": 1.0,
        }],
        view={"viewport": "world"},
    ),
    Case(
        id="triple_overlap_americas",
        label="Sun 1st + ASC Capricorn + MC Libra, Americas",
        conditions=[
            {"type": "planet_in_house", "id": "A", "planet": "sun", "house": 1},
            {"type": "angle_in_sign", "id": "B", "angle": "asc", "sign": "capricorn"},
            {"type": "angle_in_sign", "id": "C", "angle": "mc", "sign": "libra"},
        ],
        view={"fitBounds": "-55,-160,70,-30"},
    ),
]


def get_profile_birth() -> dict[str, Any]:
    profiles = json.load(urllib.request.urlopen(f"{BASE}/chart-profiles", timeout=10))
    profile = next((p for p in profiles if p["id"] == PROFILE), profiles[0])
    year, month, day = [int(x) for x in profile["date"].split("-")]
    hour, minute = [int(x) for x in (profile.get("time") or "12:00").split(":")]
    return {
        "birth_year": year,
        "birth_month": month,
        "birth_day": day,
        "birth_hour_utc": hour + minute / 60,
    }


def view_url(case: Case) -> str:
    parts = [f"profile={PROFILE}", "block=16"]
    parts.extend(f"{k}={v}" for k, v in case.view.items())
    # A harmless condition param is enough to let the sandbox initialize.
    parts.append("A=pih:sun:1")
    return f"{BASE}/map_SANDBOX_screen_pixel_truth.html?{'&'.join(parts)}"


def get_leaflet_view(case: Case) -> dict[str, Any]:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": VIEWPORT_SIZE[0], "height": VIEWPORT_SIZE[1]},
            device_scale_factor=1,
        )
        page = ctx.new_page()
        page.goto(view_url(case), wait_until="domcontentloaded")
        page.wait_for_function("window.__sptStatus === 'ready' || window.__sptStatus === 'error'")
        status = page.evaluate("window.__sptStatus")
        if status == "error":
            raise RuntimeError(page.evaluate("window.__sptLastError"))
        page.wait_for_timeout(250)
        data = page.evaluate(
            """
            () => ({
              zoom: window.__map.getZoom(),
              center: {
                lat: window.__map.getCenter().lat,
                lng: window.__map.getCenter().lng,
              },
              bounds: {
                north: window.__map.getBounds().getNorth(),
                south: window.__map.getBounds().getSouth(),
                east: window.__map.getBounds().getEast(),
                west: window.__map.getBounds().getWest(),
              },
              size: {
                x: window.__map.getSize().x,
                y: window.__map.getSize().y,
              },
            })
            """
        )
        ctx.close()
        browser.close()
        return data


def project(lat: float, lng: float, zoom: float) -> tuple[float, float]:
    scale = 256 * (2 ** zoom)
    sin_lat = math.sin(math.radians(lat))
    sin_lat = min(max(sin_lat, -0.9999), 0.9999)
    x = (lng + 180.0) / 360.0 * scale
    y = (0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)) * scale
    return x, y


def unproject(x: float, y: float, zoom: float) -> tuple[float, float]:
    scale = 256 * (2 ** zoom)
    lng = x / scale * 360.0 - 180.0
    n = math.pi - 2 * math.pi * y / scale
    lat = math.degrees(math.atan(math.sinh(n)))
    return lat, lng


class ScreenProjector:
    def __init__(self, view: dict[str, Any]):
        self.width = int(view["size"]["x"])
        self.height = int(view["size"]["y"])
        self.zoom = float(view["zoom"])
        cx, cy = project(view["center"]["lat"], view["center"]["lng"], self.zoom)
        self.origin_x = cx - self.width / 2
        self.origin_y = cy - self.height / 2

    def screen_to_latlng(self, px: int, py: int) -> tuple[float, float]:
        return unproject(self.origin_x + px + 0.5, self.origin_y + py + 0.5, self.zoom)


def classify_points(
    birth: dict[str, Any],
    conditions: list[dict[str, Any]],
    projector: ScreenProjector,
    pixels: list[tuple[int, int]],
) -> dict[tuple[int, int], int]:
    out: dict[tuple[int, int], int] = {}
    for lo in range(0, len(pixels), CHUNK_SIZE):
        chunk = pixels[lo:lo + CHUNK_SIZE]
        points = [projector.screen_to_latlng(x, y) for x, y in chunk]
        body = json.dumps({
            **birth,
            "points": points,
            "conditions": conditions,
            "apply_lat_cap": False,
        }).encode()
        req = urllib.request.Request(
            f"{BASE}/screen-pixel-truth",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        resp = json.load(urllib.request.urlopen(req, timeout=120))
        out.update({pix: mask for pix, mask in zip(chunk, resp["masks"])})
    return out


def color_for_mask(mask: int) -> tuple[int, int, int, int]:
    return MASK_PALETTE.get(mask, (255, 0, 255, 160))


def alpha_composite_rect(img: Image.Image, tile: Tile, mask: int) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle(
        [tile.x, tile.y, min(img.width, tile.x + tile.size) - 1, min(img.height, tile.y + tile.size) - 1],
        fill=color_for_mask(mask),
    )


def render_reference(width: int, height: int, masks: dict[tuple[int, int], int]) -> Image.Image:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pix = img.load()
    for (x, y), mask in masks.items():
        if mask:
            pix[x, y] = color_for_mask(mask)
    return img


def sample_points(tile: Tile) -> list[tuple[int, int]]:
    # Dense enough to catch narrow features in the first exploratory pass,
    # still much cheaper than full 1px truth. Larger tiles use a 4x4 probe
    # lattice; small tiles use their actual pixels.
    if tile.size == 1:
        return [(tile.x, tile.y)]
    if tile.size == 2:
        return [
            (tile.x, tile.y),
            (tile.x + 1, tile.y),
            (tile.x, tile.y + 1),
            (tile.x + 1, tile.y + 1),
        ]
    n = 4 if tile.size >= 8 else 3
    pts = []
    for iy in range(n):
        for ix in range(n):
            px = min(tile.x + tile.size - 1, tile.x + round((ix + 0.5) * tile.size / n - 0.5))
            py = min(tile.y + tile.size - 1, tile.y + round((iy + 0.5) * tile.size / n - 0.5))
            pts.append((px, py))
    return sorted(set(pts))


def initial_tiles(width: int, height: int, size: int) -> list[Tile]:
    return [Tile(x, y, size) for y in range(0, height, size) for x in range(0, width, size)]


def subdivide(tile: Tile, child_size: int, width: int, height: int) -> list[Tile]:
    children = []
    for y in range(tile.y, min(height, tile.y + tile.size), child_size):
        for x in range(tile.x, min(width, tile.x + tile.size), child_size):
            children.append(Tile(x, y, child_size))
    return children


def dilate_tiles(tiles: Iterable[Tile], size: int, width: int, height: int, radius: int = 1) -> list[Tile]:
    keys = set()
    for t in tiles:
        gx = t.x // size
        gy = t.y // size
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                x = (gx + dx) * size
                y = (gy + dy) * size
                if 0 <= x < width and 0 <= y < height:
                    keys.add((x, y))
    return [Tile(x, y, size) for x, y in sorted(keys, key=lambda p: (p[1], p[0]))]


def diff_metrics(ref: Image.Image, cand: Image.Image) -> tuple[dict[str, Any], Image.Image]:
    diff = ImageChops.difference(ref, cand)
    total = ref.width * ref.height
    changed = 0
    union = 0
    xor = 0
    sq = 0
    visual = Image.new("RGBA", ref.size, (0, 0, 0, 0))
    out = []
    for rp, cp, dp in zip(ref.getdata(), cand.getdata(), diff.getdata()):
        dmax = max(dp)
        if dmax:
            changed += 1
            out.append((255, 0, 255, min(255, max(80, dmax * 3))))
        else:
            out.append((0, 0, 0, 0))
        ref_on = rp[3] > 0
        cand_on = cp[3] > 0
        if ref_on or cand_on:
            union += 1
        if ref_on != cand_on:
            xor += 1
        sq += sum(c * c for c in dp)
    visual.putdata(out)
    return {
        "changed_pixels": changed,
        "changed_pct": changed / total * 100,
        "overlay_union_pixels": union,
        "overlay_xor_pixels": xor,
        "overlay_xor_pct_of_union": (xor / union * 100) if union else 0,
        "rmse_rgba": math.sqrt(sq / (total * 4)),
    }, visual


def annotate(img: Image.Image, title: str) -> Image.Image:
    out = Image.new("RGBA", img.size, (255, 255, 255, 255))
    out.alpha_composite(img.convert("RGBA"))
    draw = ImageDraw.Draw(out)
    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), title, font=font)
    draw.rectangle([0, 0, bbox[2] + 16, bbox[3] + 16], fill=(255, 255, 255, 235))
    draw.text((8, 8), title, fill=(15, 23, 42, 255), font=font)
    return out


def save_progression(path: Path, panels: list[tuple[str, Image.Image]]) -> None:
    gutter = 10
    w, h = panels[0][1].size
    sheet = Image.new("RGBA", (w * len(panels) + gutter * (len(panels) - 1), h), (245, 245, 245, 255))
    x = 0
    for title, img in panels:
        sheet.alpha_composite(annotate(img, title), (x, 0))
        x += w + gutter
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def run_adaptive(case: Case, birth: dict[str, Any], view: dict[str, Any]) -> dict[str, Any]:
    projector = ScreenProjector(view)
    width, height = projector.width, projector.height

    # Full 1px truth reference.
    all_pixels = [(x, y) for y in range(height) for x in range(width)]
    t0 = time.time()
    ref_masks = classify_points(birth, case.conditions, projector, all_pixels)
    reference_seconds = time.time() - t0
    ref_img = render_reference(width, height, ref_masks)

    classified_cache: dict[tuple[int, int], int] = {}
    accepted: list[tuple[Tile, int]] = []
    current_tiles = initial_tiles(width, height, PHASE_SIZES[0])
    phases = []

    total_classify_seconds = 0.0
    total_new_samples = 0
    panels: list[tuple[str, Image.Image]] = [("1px reference", ref_img)]

    for phase_idx, size in enumerate(PHASE_SIZES):
        phase_start = time.time()
        probe_points: list[tuple[int, int]] = []
        tile_points: dict[Tile, list[tuple[int, int]]] = {}
        for tile in current_tiles:
            pts = sample_points(tile)
            tile_points[tile] = pts
            probe_points.extend([p for p in pts if p not in classified_cache])

        unique_new = sorted(set(probe_points), key=lambda p: (p[1], p[0]))
        classify_start = time.time()
        if unique_new:
            classified_cache.update(classify_points(birth, case.conditions, projector, unique_new))
        classify_seconds = time.time() - classify_start
        total_classify_seconds += classify_seconds
        total_new_samples += len(unique_new)

        refine_parents: list[Tile] = []
        hit_or_mixed: list[Tile] = []
        phase_accepts: list[tuple[Tile, int]] = []

        for tile, pts in tile_points.items():
            masks = [classified_cache[p] for p in pts]
            unique_masks = set(masks)
            nonzero = [m for m in masks if m]
            if size == 1:
                mask = masks[0]
                if mask:
                    phase_accepts.append((tile, mask))
                continue
            if len(unique_masks) == 1:
                only = masks[0]
                if only:
                    phase_accepts.append((tile, only))
                # Stable empty or stable filled: stop here.
                continue
            if nonzero:
                hit_or_mixed.append(tile)
            refine_parents.append(tile)

        accepted.extend(phase_accepts)

        if size != 1:
            child_size = PHASE_SIZES[phase_idx + 1]
            # Refine mixed tiles and a one-tile halo around any occupied/mixed
            # tile. The halo is the computational version of "boundary
            # concentration": nearby empty tiles get one chance to prove they
            # are truly empty at the next level.
            halo_parents = dilate_tiles(hit_or_mixed, size, width, height, radius=1)
            parents = {t: None for t in [*refine_parents, *halo_parents]}.keys()
            child_tiles = []
            for parent in parents:
                child_tiles.extend(subdivide(parent, child_size, width, height))
            # De-dupe children.
            current_tiles = list({(t.x, t.y, t.size): t for t in child_tiles}.values())

        approx = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        for tile, mask in accepted:
            alpha_composite_rect(approx, tile, mask)
        metrics, diff = diff_metrics(ref_img, approx)
        phase_dir = OUT_DIR / case.id
        approx_path = phase_dir / f"phase_{phase_idx + 1}_{size}px_approx.png"
        diff_path = phase_dir / f"phase_{phase_idx + 1}_{size}px_diff.png"
        approx_path.parent.mkdir(parents=True, exist_ok=True)
        approx.save(approx_path)
        diff.save(diff_path)
        panels.append((f"phase {phase_idx + 1}: {size}px", approx))
        phases.append({
            "phase": phase_idx + 1,
            "tile_size": size,
            "tiles_evaluated": len(tile_points),
            "new_samples": len(unique_new),
            "cumulative_samples": total_new_samples,
            "classify_seconds": classify_seconds,
            "phase_seconds": time.time() - phase_start,
            "accepted_tiles": len(phase_accepts),
            "refine_tiles_next": len(current_tiles) if size != 1 else 0,
            "approx_path": str(approx_path),
            "diff_path": str(diff_path),
            "diff": metrics,
        })

    sheet_path = OUT_DIR / case.id / "progression_sheet.png"
    save_progression(sheet_path, panels)
    ref_path = OUT_DIR / case.id / "reference_1px.png"
    ref_img.save(ref_path)

    final = phases[-1]
    return {
        "case_id": case.id,
        "label": case.label,
        "conditions": case.conditions,
        "view_request": case.view,
        "leaflet_view": view,
        "reference": {
            "path": str(ref_path),
            "pixels": width * height,
            "classified_samples": len(all_pixels),
            "seconds": reference_seconds,
            "match_pixels": sum(1 for m in ref_masks.values() if m),
        },
        "adaptive": {
            "progression_sheet": str(sheet_path),
            "classified_samples": total_new_samples,
            "classify_seconds": total_classify_seconds,
            "reduction_vs_1px_pct": (1 - total_new_samples / len(all_pixels)) * 100,
            "speedup_vs_1px": reference_seconds / total_classify_seconds if total_classify_seconds else None,
            "final_diff": final["diff"],
            "phases": phases,
        },
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    birth = get_profile_birth()
    started = time.time()
    manifest: dict[str, Any] = {
        "profile": PROFILE,
        "viewport_px": {"width": VIEWPORT_SIZE[0], "height": VIEWPORT_SIZE[1]},
        "phase_sizes": PHASE_SIZES,
        "contract": "adaptive screen-space refinement toward 1px truth; not global lower resolution",
        "runs": [],
    }
    for case in CASES:
        print(f"\n=== {case.id}: {case.label} ===", flush=True)
        view = get_leaflet_view(case)
        result = run_adaptive(case, birth, view)
        r = result["reference"]
        a = result["adaptive"]
        d = a["final_diff"]
        print(
            f"  ref: {r['classified_samples']:,} samples, {r['seconds']:.2f}s, "
            f"matches={r['match_pixels']:,}",
            flush=True,
        )
        print(
            f"  adaptive: {a['classified_samples']:,} samples, "
            f"{a['classify_seconds']:.2f}s, reduction={a['reduction_vs_1px_pct']:.1f}%, "
            f"xor={d['overlay_xor_pct_of_union']:.2f}%, changed={d['changed_pct']:.2f}%",
            flush=True,
        )
        manifest["runs"].append(result)

    manifest["wall_seconds_total"] = time.time() - started
    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest written to {manifest_path}", flush=True)
    print(f"Total wall: {manifest['wall_seconds_total']:.1f}s", flush=True)


if __name__ == "__main__":
    main()
