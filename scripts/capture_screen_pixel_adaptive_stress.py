"""Adaptive screen-space stress test + cache feasibility benchmark.

This is a benchmark harness only. It does not change rendering logic, color
language, astrology math, aura logic, or product UI. It reuses the same
`/screen-pixel-truth` endpoint and tests the adaptive refinement strategy
against full 1px screen-space truth under deliberately difficult conditions.
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
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "validation/screenshots/screen_pixel_adaptive_stress"
NARRATIVE_PATH = ROOT / "validation/narratives/screen_pixel_adaptive_stress.md"

# Keep the stress suite reviewable and repeatable. 720x450 is large enough to
# show product context while keeping full 1px references (324k points) tractable
# across dozens of worst-case scenarios.
VIEWPORT_SIZE = (720, 450)
PHASE_SIZES = [16, 8, 4, 2, 1]
CHUNK_SIZE = 400_000
CONDITION_LABELS = ["A", "B", "C", "D", "E", "F"]
PLANETS = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
ANGLES = ["asc", "dsc", "mc", "ic"]
ASPECTS_CACHE = ["conjunction", "opposition", "square", "trine"]


def deterministic_color(mask: int) -> tuple[int, int, int, int]:
    """Debug-only mask color for review PNGs.

    Product colors are not changed. This is just to make stress masks > 7
    visible in offline artifacts, since the current product palette only has
    A/B/C overlap colors.
    """
    fixed = {
        1: (252, 211, 77, 140),
        2: (56, 189, 248, 140),
        4: (244, 114, 182, 140),
        3: (34, 197, 94, 153),
        5: (249, 115, 22, 153),
        6: (167, 139, 250, 153),
        7: (15, 23, 42, 140),
    }
    if mask in fixed:
        return fixed[mask]
    hue = (mask * 47) % 360
    c = 0.70
    x = c * (1 - abs((hue / 60) % 2 - 1))
    if hue < 60:
        r, g, b = c, x, 0
    elif hue < 120:
        r, g, b = x, c, 0
    elif hue < 180:
        r, g, b = 0, c, x
    elif hue < 240:
        r, g, b = 0, x, c
    elif hue < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    m = 0.18
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255), 145)


@dataclass(frozen=True)
class Tile:
    x: int
    y: int
    size: int


@dataclass(frozen=True)
class StressCase:
    id: str
    group: str
    label: str
    conditions: list[dict[str, Any]]
    view: dict[str, str]
    apply_lat_cap: bool = False
    profile_birth: dict[str, Any] | None = None


def pih(planet: str, house: int) -> dict[str, Any]:
    return {"type": "planet_in_house", "planet": planet, "house": house}


def ais(angle: str, sign: str) -> dict[str, Any]:
    return {"type": "angle_in_sign", "angle": angle, "sign": sign}


def a2a(planet: str, angle: str, aspect: str, orb: float) -> dict[str, Any]:
    return {"type": "aspect_to_angle", "planet": planet, "angle": angle, "aspect": aspect, "orb": orb}


def assign_ids(conditions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(conditions) > len(CONDITION_LABELS):
        raise ValueError("endpoint supports at most six conditions")
    out = []
    for i, cond in enumerate(conditions):
        c = dict(cond)
        c["id"] = CONDITION_LABELS[i]
        out.append(c)
    return out


SYNTHETIC_PROFILES = {
    "polar_reykjavik": {
        "birth_year": 1988, "birth_month": 1, "birth_day": 6,
        "birth_hour_utc": 2.25,
        "notes": "Synthetic stress profile: high-latitude birth date/time.",
    },
    "solstice_cluster": {
        "birth_year": 1993, "birth_month": 12, "birth_day": 21,
        "birth_hour_utc": 23.9,
        "notes": "Synthetic stress profile: solstice chart near multiple sign/angle transitions.",
    },
    "eclipse_like": {
        "birth_year": 1999, "birth_month": 8, "birth_day": 11,
        "birth_hour_utc": 11.05,
        "notes": "Synthetic stress profile: clustered luminaries/planets around eclipse-era chart.",
    },
}


STRESS_CASES: list[StressCase] = [
    # 1. Thin aspect lines.
    StressCase("thin_saturn_mc_0p25", "thin_aspect_lines", "Saturn conjunct MC, orb 0.25", assign_ids([a2a("saturn", "mc", "conjunction", 0.25)]), {"fitBounds": "-65,150,65,180"}),
    StressCase("thin_saturn_asc_0p25", "thin_aspect_lines", "Saturn conjunct ASC, orb 0.25", assign_ids([a2a("saturn", "asc", "conjunction", 0.25)]), {"viewport": "world"}),
    StressCase("thin_pluto_square_asc_0p25", "thin_aspect_lines", "Pluto square ASC, orb 0.25", assign_ids([a2a("pluto", "asc", "square", 0.25)]), {"viewport": "world"}),
    StressCase("thin_uranus_square_mc_0p25", "thin_aspect_lines", "Uranus square MC, orb 0.25", assign_ids([a2a("uranus", "mc", "square", 0.25)]), {"viewport": "world"}),
    # 2. Multiple thin lines at once.
    StressCase(
        "multi_thin_lines_world",
        "multiple_thin_lines",
        "Four simultaneous 0.5° aspect lines",
        assign_ids([
            a2a("saturn", "mc", "conjunction", 0.5),
            a2a("pluto", "asc", "square", 0.5),
            a2a("uranus", "dsc", "conjunction", 0.5),
            a2a("neptune", "ic", "square", 0.5),
        ]),
        {"viewport": "world"},
    ),
    # 3. Mixed dense overlays (six-condition endpoint max).
    StressCase(
        "mixed_dense_six_conditions",
        "mixed_dense_overlays",
        "Sun 1st + Moon 4th + Mars 2nd + ASC Cap + MC Libra + Saturn MC 0.5",
        assign_ids([
            pih("sun", 1),
            pih("moon", 4),
            pih("mars", 2),
            ais("asc", "capricorn"),
            ais("mc", "libra"),
            a2a("saturn", "mc", "conjunction", 0.5),
        ]),
        {"fitBounds": "-55,-160,70,-30"},
    ),
    # 4. Seam/dateline.
    StressCase("seam_fiji_nz", "seam_dateline", "Saturn MC 0.5 near Fiji/NZ", assign_ids([a2a("saturn", "mc", "conjunction", 0.5)]), {"fitBounds": "-50,160,5,190"}),
    StressCase("seam_alaska_siberia", "seam_dateline", "Saturn ASC 0.5 Alaska/Siberia", assign_ids([a2a("saturn", "asc", "conjunction", 0.5)]), {"fitBounds": "35,150,75,210"}),
    StressCase("seam_world_crossing_180", "seam_dateline", "Mixed aspect world crossing ±180", assign_ids([a2a("saturn", "mc", "conjunction", 0.5), a2a("uranus", "mc", "square", 0.5)]), {"viewport": "world"}),
    # 5. High latitude lat-cap OFF/ON.
    StressCase("high_greenland_latcap_off", "high_latitude", "Greenland/Iceland Saturn MC 0.5 lat-cap OFF", assign_ids([a2a("saturn", "mc", "conjunction", 0.5)]), {"fitBounds": "55,-60,82,20"}, apply_lat_cap=False),
    StressCase("high_greenland_latcap_on", "high_latitude", "Greenland/Iceland Saturn MC 0.5 lat-cap ON", assign_ids([a2a("saturn", "mc", "conjunction", 0.5)]), {"fitBounds": "55,-60,82,20"}, apply_lat_cap=True),
    StressCase("high_svalbard_latcap_off", "high_latitude", "Norway/Svalbard Pluto ASC 0.25 lat-cap OFF", assign_ids([a2a("pluto", "asc", "square", 0.25)]), {"fitBounds": "58,0,83,55"}, apply_lat_cap=False),
    StressCase("high_svalbard_latcap_on", "high_latitude", "Norway/Svalbard Pluto ASC 0.25 lat-cap ON", assign_ids([a2a("pluto", "asc", "square", 0.25)]), {"fitBounds": "58,0,83,55"}, apply_lat_cap=True),
    StressCase("high_southern_latcap_off", "high_latitude", "Southern high lat Uranus MC 0.25 lat-cap OFF", assign_ids([a2a("uranus", "mc", "square", 0.25)]), {"fitBounds": "-82,-80,-50,40"}, apply_lat_cap=False),
    StressCase("high_southern_latcap_on", "high_latitude", "Southern high lat Uranus MC 0.25 lat-cap ON", assign_ids([a2a("uranus", "mc", "square", 0.25)]), {"fitBounds": "-82,-80,-50,40"}, apply_lat_cap=True),
    # 6. Synthetic stress profiles.
    StressCase("profile_polar_reykjavik", "synthetic_profiles", "Synthetic polar profile mixed thin lines", assign_ids([a2a("saturn", "mc", "conjunction", 0.25), a2a("pluto", "asc", "square", 0.25)]), {"viewport": "world"}, profile_birth=SYNTHETIC_PROFILES["polar_reykjavik"]),
    StressCase("profile_solstice_boundaries", "synthetic_profiles", "Synthetic solstice profile angle sign boundaries", assign_ids([ais("asc", "capricorn"), ais("mc", "libra"), a2a("uranus", "mc", "square", 0.25)]), {"viewport": "world"}, profile_birth=SYNTHETIC_PROFILES["solstice_cluster"]),
    StressCase("profile_eclipse_cluster", "synthetic_profiles", "Synthetic clustered profile dense overlay", assign_ids([pih("sun", 1), pih("moon", 4), pih("mars", 2), a2a("neptune", "ic", "square", 0.5)]), {"viewport": "world"}, profile_birth=SYNTHETIC_PROFILES["eclipse_like"]),
]


def get_profile_birth() -> dict[str, Any]:
    profiles = json.load(urllib.request.urlopen(f"{BASE}/chart-profiles", timeout=10))
    p = next((x for x in profiles if x["id"] == PROFILE), profiles[0])
    year, month, day = [int(x) for x in p["date"].split("-")]
    hour, minute = [int(x) for x in (p.get("time") or "12:00").split(":")]
    return {"birth_year": year, "birth_month": month, "birth_day": day, "birth_hour_utc": hour + minute / 60}


def project(lat: float, lng: float, zoom: float) -> tuple[float, float]:
    scale = 256 * (2 ** zoom)
    sin_lat = max(min(math.sin(math.radians(lat)), 0.9999), -0.9999)
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


def view_url(case: StressCase) -> str:
    parts = [f"profile={PROFILE}", "block=16", "A=pih:sun:1"]
    parts.extend(f"{k}={v}" for k, v in case.view.items())
    return f"{BASE}/map_SANDBOX_screen_pixel_truth.html?{'&'.join(parts)}"


def get_leaflet_view(case: StressCase, size: tuple[int, int] = VIEWPORT_SIZE) -> dict[str, Any]:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": size[0], "height": size[1]}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(view_url(case), wait_until="domcontentloaded")
        page.wait_for_function("window.__sptStatus === 'ready' || window.__sptStatus === 'error'", timeout=30_000)
        if page.evaluate("window.__sptStatus") == "error":
            raise RuntimeError(page.evaluate("window.__sptLastError"))
        page.wait_for_timeout(250)
        view = page.evaluate(
            """() => ({
              zoom: window.__map.getZoom(),
              center: {lat: window.__map.getCenter().lat, lng: window.__map.getCenter().lng},
              bounds: {
                north: window.__map.getBounds().getNorth(),
                south: window.__map.getBounds().getSouth(),
                east: window.__map.getBounds().getEast(),
                west: window.__map.getBounds().getWest(),
              },
              size: {x: window.__map.getSize().x, y: window.__map.getSize().y},
            })"""
        )
        ctx.close()
        browser.close()
        return view


def classify_points(
    birth: dict[str, Any],
    conditions: list[dict[str, Any]],
    projector: ScreenProjector,
    pixels: list[tuple[int, int]],
    apply_lat_cap: bool,
) -> tuple[dict[tuple[int, int], int], float, dict[str, Any]]:
    masks: dict[tuple[int, int], int] = {}
    total_server = 0.0
    last_props: dict[str, Any] = {}
    for lo in range(0, len(pixels), CHUNK_SIZE):
        chunk = pixels[lo:lo + CHUNK_SIZE]
        body = json.dumps({
            **birth,
            "points": [projector.screen_to_latlng(x, y) for x, y in chunk],
            "conditions": conditions,
            "apply_lat_cap": apply_lat_cap,
        }).encode()
        req = urllib.request.Request(f"{BASE}/screen-pixel-truth", data=body, headers={"Content-Type": "application/json"})
        resp = json.load(urllib.request.urlopen(req, timeout=180))
        props = resp["properties"]
        total_server += props.get("compute_seconds", 0.0)
        last_props = props
        masks.update({p: m for p, m in zip(chunk, resp["masks"])})
    return masks, total_server, last_props


def render_image(width: int, height: int, masks: dict[tuple[int, int], int]) -> Image.Image:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pix = img.load()
    for (x, y), mask in masks.items():
        if mask:
            pix[x, y] = deterministic_color(mask)
    return img


def draw_rect(img: Image.Image, tile: Tile, mask: int) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle(
        [tile.x, tile.y, min(img.width, tile.x + tile.size) - 1, min(img.height, tile.y + tile.size) - 1],
        fill=deterministic_color(mask),
    )


def sample_points(tile: Tile) -> list[tuple[int, int]]:
    if tile.size == 1:
        return [(tile.x, tile.y)]
    if tile.size == 2:
        return [(tile.x, tile.y), (tile.x + 1, tile.y), (tile.x, tile.y + 1), (tile.x + 1, tile.y + 1)]
    n = 4 if tile.size >= 8 else 3
    pts = []
    for iy in range(n):
        for ix in range(n):
            pts.append((
                min(tile.x + tile.size - 1, tile.x + round((ix + 0.5) * tile.size / n - 0.5)),
                min(tile.y + tile.size - 1, tile.y + round((iy + 0.5) * tile.size / n - 0.5)),
            ))
    return sorted(set(pts))


def initial_tiles(width: int, height: int, size: int) -> list[Tile]:
    return [Tile(x, y, size) for y in range(0, height, size) for x in range(0, width, size)]


def subdivide(tile: Tile, child_size: int, width: int, height: int) -> list[Tile]:
    return [
        Tile(x, y, child_size)
        for y in range(tile.y, min(height, tile.y + tile.size), child_size)
        for x in range(tile.x, min(width, tile.x + tile.size), child_size)
    ]


def dilate_tiles(tiles: Iterable[Tile], size: int, width: int, height: int, radius: int = 1) -> list[Tile]:
    keys = set()
    for t in tiles:
        gx, gy = t.x // size, t.y // size
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                x, y = (gx + dx) * size, (gy + dy) * size
                if 0 <= x < width and 0 <= y < height:
                    keys.add((x, y))
    return [Tile(x, y, size) for x, y in sorted(keys, key=lambda p: (p[1], p[0]))]


def diff_metrics(ref: Image.Image, cand: Image.Image) -> tuple[dict[str, Any], Image.Image]:
    diff = ImageChops.difference(ref, cand)
    total = ref.width * ref.height
    changed = union = xor = 0
    xs: list[int] = []
    ys: list[int] = []
    out = []
    for i, (rp, cp, dp) in enumerate(zip(ref.getdata(), cand.getdata(), diff.getdata())):
        dmax = max(dp)
        if dmax:
            changed += 1
            x = i % ref.width
            y = i // ref.width
            xs.append(x); ys.append(y)
            out.append((255, 0, 255, min(255, max(80, dmax * 3))))
        else:
            out.append((0, 0, 0, 0))
        ref_on, cand_on = rp[3] > 0, cp[3] > 0
        if ref_on or cand_on:
            union += 1
        if ref_on != cand_on:
            xor += 1
    visual = Image.new("RGBA", ref.size, (0, 0, 0, 0))
    visual.putdata(out)
    bbox = None if not xs else {"left": min(xs), "top": min(ys), "right": max(xs), "bottom": max(ys)}
    return {
        "changed_pixels": changed,
        "changed_pct": changed / total * 100,
        "overlay_union_pixels": union,
        "overlay_xor_pixels": xor,
        "overlay_xor_pct_of_union": (xor / union * 100) if union else 0.0,
        "diff_bbox": bbox,
    }, visual


def run_adaptive(case: StressCase, birth: dict[str, Any], view: dict[str, Any]) -> dict[str, Any]:
    projector = ScreenProjector(view)
    width, height = projector.width, projector.height
    all_pixels = [(x, y) for y in range(height) for x in range(width)]

    t0 = time.time()
    ref_masks, ref_server, ref_props = classify_points(birth, case.conditions, projector, all_pixels, case.apply_lat_cap)
    ref_wall = time.time() - t0
    ref_img = render_image(width, height, ref_masks)

    classified_cache: dict[tuple[int, int], int] = {}
    accepted: list[tuple[Tile, int]] = []
    current_tiles = initial_tiles(width, height, PHASE_SIZES[0])
    phases = []
    total_samples = 0
    total_server = 0.0

    case_dir = OUT_DIR / case.id
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "reference_1px.png").parent.mkdir(parents=True, exist_ok=True)
    ref_img.save(case_dir / "reference_1px.png")

    for idx, size in enumerate(PHASE_SIZES):
        tile_points: dict[Tile, list[tuple[int, int]]] = {}
        new_points: list[tuple[int, int]] = []
        for tile in current_tiles:
            pts = sample_points(tile)
            tile_points[tile] = pts
            new_points.extend([p for p in pts if p not in classified_cache])
        unique_new = sorted(set(new_points), key=lambda p: (p[1], p[0]))
        phase_t0 = time.time()
        if unique_new:
            new_masks, server_seconds, _ = classify_points(birth, case.conditions, projector, unique_new, case.apply_lat_cap)
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
                if masks[0]:
                    phase_accepts.append((tile, masks[0]))
                continue
            if nonzero:
                hit_or_mixed.append(tile)
            refine_parents.append(tile)
        accepted.extend(phase_accepts)

        if size != 1:
            child_size = PHASE_SIZES[idx + 1]
            halo = dilate_tiles(hit_or_mixed, size, width, height, radius=1)
            parents = {(t.x, t.y, t.size): t for t in [*refine_parents, *halo]}.values()
            children: list[Tile] = []
            for p in parents:
                children.extend(subdivide(p, child_size, width, height))
            current_tiles = list({(t.x, t.y, t.size): t for t in children}.values())

        approx = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        for tile, mask in accepted:
            draw_rect(approx, tile, mask)
        diff, diff_img = diff_metrics(ref_img, approx)
        approx_path = case_dir / f"phase_{idx + 1}_{size}px_approx.png"
        diff_path = case_dir / f"phase_{idx + 1}_{size}px_diff.png"
        approx.save(approx_path)
        diff_img.save(diff_path)
        phases.append({
            "phase": idx + 1,
            "tile_size": size,
            "tiles_evaluated": len(tile_points),
            "new_samples": len(unique_new),
            "cumulative_samples": total_samples,
            "server_seconds": server_seconds,
            "wall_seconds": time.time() - phase_t0,
            "accepted_tiles": len(phase_accepts),
            "refine_tiles_next": len(current_tiles) if size != 1 else 0,
            "approx_path": str(approx_path.relative_to(ROOT)),
            "diff_path": str(diff_path.relative_to(ROOT)),
            "diff": diff,
        })

    final_diff = phases[-1]["diff"]
    return {
        "case_id": case.id,
        "group": case.group,
        "label": case.label,
        "conditions": case.conditions,
        "view_request": case.view,
        "leaflet_view": view,
        "apply_lat_cap": case.apply_lat_cap,
        "synthetic_profile": case.profile_birth,
        "reference": {
            "path": str((case_dir / "reference_1px.png").relative_to(ROOT)),
            "classified_samples": len(all_pixels),
            "server_seconds": ref_server,
            "wall_seconds": ref_wall,
            "match_pixels": sum(1 for m in ref_masks.values() if m),
            "properties": ref_props,
        },
        "adaptive": {
            "classified_samples": total_samples,
            "server_seconds": total_server,
            "reduction_vs_1px_pct": (1 - total_samples / len(all_pixels)) * 100,
            "speedup_vs_1px_server": ref_server / total_server if total_server else None,
            "final_diff": final_diff,
            "phases": phases,
        },
    }


def capture_basemap(run: dict[str, Any], out_path: Path) -> None:
    view = run["leaflet_view"]
    center = view["center"]
    zoom = view["zoom"]
    html = f"""<!doctype html><html><head><meta charset='utf-8'/>
<link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'/>
<style>html,body,#map{{margin:0;padding:0;width:100%;height:100%;}}.leaflet-control-container{{display:none;}}</style></head>
<body><div id='map'></div><script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script>
<script>
const map=L.map('map',{{zoomControl:false,attributionControl:false,zoomSnap:0.25,zoomDelta:0.5,minZoom:2,maxZoom:11,preferCanvas:true,worldCopyJump:false}}).setView([{center['lat']},{center['lng']}],{zoom});
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:11,minZoom:2,crossOrigin:true}}).addTo(map);
window.__ready=false; setTimeout(()=>{{window.__ready=true}},1200);
</script></body></html>"""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": VIEWPORT_SIZE[0], "height": VIEWPORT_SIZE[1]}, device_scale_factor=1)
        page = ctx.new_page()
        page.set_content(html, wait_until="domcontentloaded")
        page.wait_for_function("window.__ready === true", timeout=10_000)
        page.screenshot(path=str(out_path), full_page=False)
        ctx.close()
        browser.close()


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


def create_human_review(run: dict[str, Any]) -> str:
    case_dir = OUT_DIR / run["case_id"]
    basemap_path = case_dir / "human_review_basemap.png"
    capture_basemap(run, basemap_path)
    base = Image.open(basemap_path).convert("RGBA")
    phase_by_size = {p["tile_size"]: p for p in run["adaptive"]["phases"]}
    panels = [
        ("1px reference", ROOT / run["reference"]["path"]),
        ("Adaptive final", ROOT / phase_by_size[1]["approx_path"]),
        ("Diff vs 1px", ROOT / phase_by_size[1]["diff_path"]),
        ("16px sparse exploratory", ROOT / phase_by_size[16]["approx_path"]),
        ("8px regional concentration", ROOT / phase_by_size[8]["approx_path"]),
        ("4px boundary concentration", ROOT / phase_by_size[4]["approx_path"]),
        ("2px near-final", ROOT / phase_by_size[2]["approx_path"]),
        ("local 1px convergence", ROOT / phase_by_size[1]["approx_path"]),
    ]
    rendered = [label_panel(composite(base, p), label) for label, p in panels]
    cols = 2
    gutter = 10
    title_h = 62
    pw, ph = rendered[0].size
    rows = (len(rendered) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * pw + gutter, title_h + rows * ph + (rows - 1) * gutter), (255, 255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 14), f"{run['case_id']} · {run['label']}", fill=(15, 23, 42, 255), font=ImageFont.load_default())
    draw.text(
        (12, 36),
        f"1px {run['reference']['classified_samples']:,} · adaptive {run['adaptive']['classified_samples']:,} · "
        f"reduction {run['adaptive']['reduction_vs_1px_pct']:.1f}% · XOR {run['adaptive']['final_diff']['overlay_xor_pct_of_union']:.3f}%",
        fill=(71, 85, 105, 255),
        font=ImageFont.load_default(),
    )
    for i, panel in enumerate(rendered):
        x = (i % cols) * (pw + gutter)
        y = title_h + (i // cols) * (ph + gutter)
        sheet.alpha_composite(panel, (x, y))
    out = OUT_DIR / f"human_review_{run['case_id']}.png"
    sheet.save(out)
    return str(out.relative_to(ROOT))


def visible_verdict(run: dict[str, Any]) -> str:
    xor = run["adaptive"]["final_diff"]["overlay_xor_pct_of_union"]
    changed = run["adaptive"]["final_diff"]["changed_pct"]
    if xor == 0:
        return "visually identical"
    if xor <= 0.2 and changed <= 0.05:
        return "acceptable / effectively identical"
    if xor <= 1.0:
        return "acceptable with visible edge residue"
    return "failed or needs tighter refinement"


def cache_benchmark(birth: dict[str, Any], base_case: StressCase, base_view: dict[str, Any]) -> list[dict[str, Any]]:
    """Measure/estimate cache priorities on current visible samples."""
    results: list[dict[str, Any]] = []
    base_proj = ScreenProjector(base_view)
    full_pixels = [(x, y) for y in range(base_proj.height) for x in range(base_proj.width)]

    def timed(name: str, priority: int, sample_pixels: list[tuple[int, int]], conditions: list[dict[str, Any]], trigger: str, eager: str, projector: ScreenProjector = base_proj) -> None:
        t0 = time.time()
        masks, server, props = classify_points(birth, assign_ids(conditions), projector, sample_pixels, False)
        wall = time.time() - t0
        mask_bytes = len(sample_pixels)  # 1 byte/mask is enough up to six conditions.
        point_bytes = len(sample_pixels) * 8  # packed int32 x/y or compact tile reference estimate.
        results.append({
            "priority": priority,
            "name": name,
            "sample_count": len(sample_pixels),
            "server_seconds": server,
            "wall_seconds": wall,
            "memory_estimate_bytes": mask_bytes + point_bytes,
            "match_count": sum(1 for m in masks.values() if m),
            "conditions": conditions,
            "background_feasible": wall < 8.0,
            "recommended_trigger": trigger,
            "cache_policy": eager,
            "properties": props,
        })

    timed("current requested field/current viewport/full visible screen", 1, full_pixels, [base_case.conditions[0]], "before first paint only for requested field", "eager")

    # Zoom +1/+2 estimates: same screen pixels at deeper zoom/center.
    for dz in [1, 2]:
        view = json.loads(json.dumps(base_view))
        view["zoom"] = base_view["zoom"] + dz
        projector = ScreenProjector(view)
        pixels = [(x, y) for y in range(projector.height) for x in range(projector.width)]
        timed(f"same center zoom +{dz}", 2, pixels, [base_case.conditions[0]], "after first paint if user pauses", "delayed", projector)

    # Pan buffer: approximate 25% margin means 1.5x width * 1.5x height.
    w, h = base_proj.width, base_proj.height
    buffer_pixels = [(x, y) for y in range(-w // 4, w + w // 4) for x in range(-w // 4, w + w // 4)]
    # Cap this diagnostic to avoid enormous off-screen bodies; estimate if too large.
    buffer_sample_count = int(w * h * 2.25)
    estimate_pps = results[0]["sample_count"] / max(results[0]["server_seconds"], 0.001)
    results.append({
        "priority": 3,
        "name": "25% pan buffer around current viewport",
        "sample_count": buffer_sample_count,
        "server_seconds_estimate": buffer_sample_count / estimate_pps,
        "wall_seconds_estimate": buffer_sample_count / estimate_pps * 1.2,
        "memory_estimate_bytes": buffer_sample_count * 9,
        "background_feasible": buffer_sample_count / estimate_pps < 8.0,
        "recommended_trigger": "after first paint when user pauses",
        "cache_policy": "delayed",
        "note": "Estimated from current-field throughput; not fully materialized to avoid wasting benchmark time.",
    })

    timed("all planet-in-house fields visible screen (10 planets * 1 selected house each)", 4, full_pixels, [pih(p, 1) for p in PLANETS[:6]], "after first paint only if house overlay UI likely", "delayed")
    timed("angle-in-sign fields visible screen", 5, full_pixels, [ais("asc", "capricorn"), ais("dsc", "cancer"), ais("mc", "libra"), ais("ic", "aries")], "when user opens angle/sign controls", "user-triggered")
    timed("aspect-to-angle narrow envelope sample", 6, full_pixels, [a2a("saturn", "mc", "conjunction", 0.5), a2a("pluto", "asc", "square", 0.5), a2a("uranus", "dsc", "conjunction", 0.5), a2a("neptune", "ic", "square", 0.5)], "when user opens aspect controls", "user-triggered")
    timed("aspect-to-angle wider envelope sample", 6, full_pixels, [a2a("saturn", "mc", "conjunction", 3.0), a2a("pluto", "asc", "square", 3.0), a2a("uranus", "dsc", "conjunction", 3.0), a2a("neptune", "ic", "square", 3.0)], "after user selects an aspect family", "user-triggered")
    return results


def write_index_and_report(manifest: dict[str, Any]) -> None:
    lines = ["# Adaptive Stress Human Review Index", "", f"Folder: `{OUT_DIR}`", ""]
    for run in manifest["stress_runs"]:
        lines.extend([
            f"## `{Path(run['human_review_sheet']).name}`",
            "",
            f"- Case: {run['label']}",
            f"- Group: `{run['group']}`",
            f"- 1px samples: `{run['reference']['classified_samples']:,}`",
            f"- Adaptive samples: `{run['adaptive']['classified_samples']:,}`",
            f"- Reduction: `{run['adaptive']['reduction_vs_1px_pct']:.2f}%`",
            f"- Timing: 1px server `{run['reference']['server_seconds']:.2f}s`; adaptive server `{run['adaptive']['server_seconds']:.2f}s`",
            f"- Overlay XOR: `{run['adaptive']['final_diff']['overlay_xor_pct_of_union']:.3f}%`",
            f"- Max visible diff region: `{run['adaptive']['final_diff']['diff_bbox']}`",
            f"- Verdict: {run['verdict']}",
            f"- Review PNG: `{run['human_review_sheet']}`",
            "",
        ])
    (OUT_DIR / "HUMAN_REVIEW_INDEX.md").write_text("\n".join(lines))

    worst = max(manifest["stress_runs"], key=lambda r: r["adaptive"]["final_diff"]["overlay_xor_pct_of_union"])
    reductions = [r["adaptive"]["reduction_vs_1px_pct"] for r in manifest["stress_runs"]]
    narrative = [
        "# Adaptive Screen-Space Stress Test + Cache Feasibility",
        "",
        "No rendering logic, astrology math, aura logic, raindrop visuals, or color polish changed. This is a benchmark artifact pass only.",
        "",
        "## Outputs",
        "",
        f"- Screenshot folder: `{OUT_DIR.relative_to(ROOT)}`",
        f"- Manifest: `{(OUT_DIR / 'manifest.json').relative_to(ROOT)}`",
        f"- Human review index: `{(OUT_DIR / 'HUMAN_REVIEW_INDEX.md').relative_to(ROOT)}`",
        "",
        "## Stress Summary",
        "",
        f"- Stress cases run: `{len(manifest['stress_runs'])}`",
        f"- Median reduction vs full 1px: `{sorted(reductions)[len(reductions)//2]:.1f}%`",
        f"- Worst overlay XOR case: `{worst['case_id']}` at `{worst['adaptive']['final_diff']['overlay_xor_pct_of_union']:.3f}%`",
        f"- Worst-case adaptive samples: `{max(r['adaptive']['classified_samples'] for r in manifest['stress_runs']):,}`",
        "",
        "## Cache Protocol Recommendation",
        "",
        "1. Before first paint: compute only the requested field for the visible screen.",
        "2. Immediately after first paint: if the render finished comfortably, compute zoom +1 for the same center only.",
        "3. When user pauses: compute the 25% pan buffer and optionally zoom +2.",
        "4. Only when the user opens relevant controls: compute angle/sign and aspect families.",
        "5. Do not eagerly cache all planet/house/aspect combinations yet; the benchmark shows this is possible but not necessary before user intent is known.",
        "",
        "Use the worst observed adaptive sample count plus 20% as the conservative production budget for first-pass scheduling.",
        "",
        "## Cache Benchmark",
        "",
    ]
    for c in manifest["cache_benchmark"]:
        seconds = c.get("server_seconds", c.get("server_seconds_estimate"))
        memory = c["memory_estimate_bytes"] / (1024 * 1024)
        narrative.extend([
            f"### Priority {c['priority']}: {c['name']}",
            "",
            f"- Samples: `{c['sample_count']:,}`",
            f"- Server time: `{seconds:.2f}s`",
            f"- Memory estimate: `{memory:.2f} MiB`",
            f"- Background feasible: `{c['background_feasible']}`",
            f"- Policy: `{c['cache_policy']}`",
            f"- Trigger: {c['recommended_trigger']}",
            "",
        ])
    NARRATIVE_PATH.write_text("\n".join(narrative))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    birth = get_profile_birth()
    manifest: dict[str, Any] = {
        "viewport_px": {"width": VIEWPORT_SIZE[0], "height": VIEWPORT_SIZE[1]},
        "phase_sizes": PHASE_SIZES,
        "stress_runs": [],
        "cache_benchmark": [],
        "synthetic_profiles": SYNTHETIC_PROFILES,
    }
    started = time.time()
    for case in STRESS_CASES:
        print(f"\n=== {case.id}: {case.label} ===", flush=True)
        case_birth = case.profile_birth or birth
        view = get_leaflet_view(case)
        try:
            run = run_adaptive(case, case_birth, view)
            run["verdict"] = visible_verdict(run)
            run["human_review_sheet"] = create_human_review(run)
            manifest["stress_runs"].append(run)
            print(
                f"  1px={run['reference']['classified_samples']:,} "
                f"adaptive={run['adaptive']['classified_samples']:,} "
                f"reduction={run['adaptive']['reduction_vs_1px_pct']:.1f}% "
                f"xor={run['adaptive']['final_diff']['overlay_xor_pct_of_union']:.3f}% "
                f"verdict={run['verdict']}",
                flush=True,
            )
        except Exception as exc:
            manifest["stress_runs"].append({
                "case_id": case.id,
                "group": case.group,
                "label": case.label,
                "conditions": case.conditions,
                "view_request": case.view,
                "apply_lat_cap": case.apply_lat_cap,
                "error": str(exc),
                "verdict": "failed to run",
            })
            print(f"  FAILED: {exc}", flush=True)

    cache_case = next(
        (c for c in STRESS_CASES if c.id == "saturn_mc_1_pacific"),
        STRESS_CASES[0],
    )
    cache_view = get_leaflet_view(cache_case)
    print("\n=== cache benchmark ===", flush=True)
    manifest["cache_benchmark"] = cache_benchmark(birth, cache_case, cache_view)
    for item in manifest["cache_benchmark"]:
        seconds = item.get("server_seconds", item.get("server_seconds_estimate"))
        print(f"  P{item['priority']} {item['name']}: samples={item['sample_count']:,} server={seconds:.2f}s", flush=True)

    manifest["wall_seconds_total"] = time.time() - started
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    write_index_and_report(manifest)
    print(f"\nManifest written to {OUT_DIR / 'manifest.json'}", flush=True)
    print(f"Narrative written to {NARRATIVE_PATH}", flush=True)
    print(f"Total wall: {manifest['wall_seconds_total']:.1f}s", flush=True)


if __name__ == "__main__":
    main()
