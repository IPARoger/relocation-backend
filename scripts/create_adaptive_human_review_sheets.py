"""Create human-readable QA sheets for adaptive refinement outputs.

This script does not classify, sample, or alter rendering logic. It only:
  1. reads the existing adaptive-refinement manifest and overlay PNGs,
  2. captures a matching Leaflet basemap for each case viewport,
  3. composites the already-generated transparent overlays/diffs over that
     basemap, and
  4. writes large contact sheets and a markdown index for human review.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "validation/screenshots/screen_pixel_adaptive_refinement"
MANIFEST_PATH = OUT_DIR / "manifest.json"

REQUESTED_CASES = [
    "saturn_mc_0p5_pacific",
    "saturn_mc_1_pacific",
    "saturn_asc_1_world",
    "sun_1st_world",
    "triple_overlap_americas",
]

PANEL_W = 960
PANEL_H = 600
LABEL_H = 44
GUTTER = 14
COLS = 2


def rel(path: str) -> Path:
    return ROOT / path


def capture_basemap(run: dict[str, Any], out_path: Path) -> None:
    """Capture a clean Leaflet basemap matching the manifest view."""
    view = run["leaflet_view"]
    center = view["center"]
    zoom = view["zoom"]
    html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    html, body, #map {{ margin:0; padding:0; width:100%; height:100%; }}
    .leaflet-control-container {{ display:none; }}
  </style>
</head>
<body>
<div id="map"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const map = L.map('map', {{
  zoomControl: false,
  attributionControl: false,
  zoomSnap: 0.25,
  zoomDelta: 0.5,
  minZoom: 2,
  maxZoom: 11,
  preferCanvas: true,
  worldCopyJump: false,
}}).setView([{center['lat']}, {center['lng']}], {zoom});
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
  maxZoom: 11,
  minZoom: 2,
  crossOrigin: true,
}}).addTo(map);
window.__ready = false;
setTimeout(() => {{ window.__ready = true; }}, 1200);
</script>
</body>
</html>
"""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": PANEL_W, "height": PANEL_H},
            device_scale_factor=1,
        )
        page = ctx.new_page()
        page.set_content(html, wait_until="domcontentloaded")
        page.wait_for_function("window.__ready === true", timeout=10_000)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(out_path), full_page=False)
        ctx.close()
        browser.close()


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def composite_on_basemap(basemap: Image.Image, overlay_path: Path) -> Image.Image:
    base = basemap.copy().convert("RGBA")
    overlay = load_rgba(overlay_path)
    if overlay.size != base.size:
        overlay = overlay.resize(base.size, Image.Resampling.NEAREST)
    base.alpha_composite(overlay)
    return base


def label_panel(img: Image.Image, label: str) -> Image.Image:
    panel = Image.new("RGBA", (PANEL_W, PANEL_H + LABEL_H), (255, 255, 255, 255))
    panel.alpha_composite(img.convert("RGBA"), (0, LABEL_H))
    draw = ImageDraw.Draw(panel)
    font = ImageFont.load_default()
    draw.rectangle([0, 0, PANEL_W, LABEL_H], fill=(248, 250, 252, 255))
    draw.text((12, 15), label, fill=(15, 23, 42, 255), font=font)
    return panel


def make_sheet(case_id: str, run: dict[str, Any], basemap: Image.Image) -> Path:
    adaptive = run["adaptive"]
    phases = adaptive["phases"]
    phase_by_size = {p["tile_size"]: p for p in phases}

    panels: list[tuple[str, Path]] = [
        ("1px reference over basemap", rel(run["reference"]["path"])),
        ("Adaptive final over basemap", rel(phase_by_size[1]["approx_path"])),
        ("Final diff over basemap", rel(phase_by_size[1]["diff_path"])),
        ("Progression: 16px sparse exploratory", rel(phase_by_size[16]["approx_path"])),
        ("Progression: 8px regional concentration", rel(phase_by_size[8]["approx_path"])),
        ("Progression: 4px boundary concentration", rel(phase_by_size[4]["approx_path"])),
        ("Progression: 2px near-final", rel(phase_by_size[2]["approx_path"])),
        ("Progression: local 1px convergence", rel(phase_by_size[1]["approx_path"])),
    ]

    rendered = [
        label_panel(composite_on_basemap(basemap, path), label)
        for label, path in panels
    ]

    panel_w, panel_h = rendered[0].size
    rows = (len(rendered) + COLS - 1) // COLS
    title_h = 70
    sheet = Image.new(
        "RGBA",
        (
            COLS * panel_w + (COLS - 1) * GUTTER,
            title_h + rows * panel_h + (rows - 1) * GUTTER,
        ),
        (255, 255, 255, 255),
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    title = f"{case_id} · adaptive screen-space refinement human review"
    subtitle = (
        f"1px={run['reference']['classified_samples']:,} samples · "
        f"adaptive={adaptive['classified_samples']:,} samples · "
        f"reduction={adaptive['reduction_vs_1px_pct']:.1f}% · "
        f"XOR={adaptive['final_diff']['overlay_xor_pct_of_union']:.3f}%"
    )
    draw.text((14, 16), title, fill=(15, 23, 42, 255), font=font)
    draw.text((14, 40), subtitle, fill=(71, 85, 105, 255), font=font)

    for idx, panel in enumerate(rendered):
        row = idx // COLS
        col = idx % COLS
        x = col * (panel_w + GUTTER)
        y = title_h + row * (panel_h + GUTTER)
        sheet.alpha_composite(panel, (x, y))

    out_path = OUT_DIR / f"human_review_{case_id}.png"
    sheet.save(out_path)
    return out_path


def verdict_for(run: dict[str, Any]) -> str:
    xor = run["adaptive"]["final_diff"]["overlay_xor_pct_of_union"]
    if xor == 0:
        return "Visually identical; final adaptive overlay matches the 1px reference in this proof."
    if xor < 0.05:
        return "Visually identical for review purposes; only tiny edge-pixel residue remains."
    if xor < 0.2:
        return "Effectively identical; inspect diff panel for tiny boundary residue."
    return "Close but visible diff may require stricter local refinement."


def write_index(runs: dict[str, dict[str, Any]], sheet_paths: dict[str, Path]) -> None:
    lines = [
        "# Human Review Index: Adaptive Screen-Space Refinement",
        "",
        "These PNGs are review sheets only. They composite the already-generated adaptive overlays over a matching Leaflet basemap; no rendering logic, astrology math, colors, aura, or styling were changed.",
        "",
        f"Folder: `{OUT_DIR}`",
        "",
    ]
    for case_id in REQUESTED_CASES:
        run = runs[case_id]
        adaptive = run["adaptive"]
        reference = run["reference"]
        diff = adaptive["final_diff"]
        sheet = sheet_paths[case_id]
        lines.extend([
            f"## `{sheet.name}`",
            "",
            f"- Path: `{sheet}`",
            f"- What it proves: `{run['label']}` adaptive refinement over real map context, compared against full 1px screen-space truth.",
            f"- 1px sample count: `{reference['classified_samples']:,}`",
            f"- Adaptive sample count: `{adaptive['classified_samples']:,}`",
            f"- Reduction: `{adaptive['reduction_vs_1px_pct']:.2f}%`",
            f"- Timing: full 1px `{reference['seconds']:.2f}s`; adaptive classify `{adaptive['classify_seconds']:.2f}s`; speedup `{adaptive['speedup_vs_1px']:.1f}x`",
            f"- Overlay XOR: `{diff['overlay_xor_pct_of_union']:.3f}%`",
            f"- Visual verdict: {verdict_for(run)}",
            "",
        ])
    (OUT_DIR / "HUMAN_REVIEW_INDEX.md").write_text("\n".join(lines))


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    runs = {run["case_id"]: run for run in manifest["runs"]}
    sheet_paths: dict[str, Path] = {}
    for case_id in REQUESTED_CASES:
        run = runs[case_id]
        case_dir = OUT_DIR / case_id
        basemap_path = case_dir / "human_review_basemap.png"
        capture_basemap(run, basemap_path)
        basemap = load_rgba(basemap_path)
        sheet_paths[case_id] = make_sheet(case_id, run, basemap)
        print(f"wrote {sheet_paths[case_id]}")
    write_index(runs, sheet_paths)
    print(f"wrote {OUT_DIR / 'HUMAN_REVIEW_INDEX.md'}")


if __name__ == "__main__":
    main()
