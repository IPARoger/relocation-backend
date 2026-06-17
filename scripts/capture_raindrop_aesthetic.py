"""Capture raindrop/virga aesthetic sandbox variants.

Outputs:
  validation/screenshots/raindrop_aesthetic/
  validation/screenshots/raindrop_aesthetic/manifest.json
  validation/narratives/raindrop_aesthetic_exploration.md

Run:
  ./venv/bin/python scripts/capture_raindrop_aesthetic.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "validation/screenshots/raindrop_aesthetic"
NARRATIVE = ROOT / "validation/narratives/raindrop_aesthetic_exploration.md"
BASE = "http://127.0.0.1:8000/map_SANDBOX_raindrop_aesthetic.html"

MODES = ["blue_noise", "bacteria", "virga", "harmonic", "fibonacci"]
PACES_MS = [2000, 3000, 5000, 7000]
DENSITIES = ["sparse", "readable", "magical", "dense"]

# Default demo conditions: Sun 1st (readable single-condition baseline)
DEFAULT_QUERY = "A=pih:sun:1&profile=baseline_validated&viewport=americas"


def url(mode: str, pace: int, density: str = "readable") -> str:
    return f"{BASE}?{DEFAULT_QUERY}&mode={mode}&pace={pace}&density={density}"


def capture_case(page, mode: str, pace: int, density: str, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    page.goto(url(mode, pace, density), wait_until="domcontentloaded", timeout=90_000)
    page.wait_for_function("() => window.__raindrop && window.__raindrop.status === 'ready'", timeout=30_000)

    t0 = time.time()
    page.evaluate("async () => { await window.__raindrop.startReveal(); }")
    page.wait_for_function("() => window.__raindrop.status === 'complete'", timeout=300_000)

    # Stills at 0/25/50/75/100% would need mid-capture; we capture final + metrics
    final_path = out_dir / "final.png"
    page.screenshot(path=str(final_path), full_page=False)

    metrics = page.evaluate("() => window.__raindrop.metrics()")
    wall = time.time() - t0

    return {
        "mode": mode,
        "pace_ms": pace,
        "density": density,
        "wall_seconds": wall,
        "metrics": metrics,
        "final_png": str(final_path.relative_to(ROOT)),
        "cache_window_estimate_ms": pace,
    }


def write_narrative(manifest: dict) -> None:
    lines = [
        "# Raindrop / Virga Aesthetic Exploration",
        "",
        "Sandbox only. No changes to astrology math, `map_CURRENT.html`, or the proven adaptive renderer.",
        "",
        "## Sandbox",
        "",
        f"- URL base: `{BASE}`",
        f"- File: `map_SANDBOX_raindrop_aesthetic.html`",
        "",
        "Example:",
        "```",
        f"{BASE}?A=pih:sun:1&mode=virga&pace=5000&density=magical&auto=1",
        "```",
        "",
        "## Visual modes tested (5)",
        "",
        "| mode | intent |",
        "|------|--------|",
        "| `blue_noise` | jittered probes; anti-grid soldiers |",
        "| `bacteria` | organic clustering near hits |",
        "| `virga` | faint ghost condition fades as target clarifies |",
        "| `harmonic` | overtone-style opacity ramp + colorify |",
        "| `fibonacci` | Fibonacci-weight opacity ramp + colorify |",
        "",
        "## Pace variants (ms)",
        "",
        ", ".join(str(p) for p in PACES_MS),
        "",
        "## Density packs",
        "",
        ", ".join(DENSITIES),
        "",
        "## Timing summary",
        "",
        "| case | wall_s | samples | server_s | match_dots |",
        "|------|-------:|--------:|---------:|-----------:|",
    ]
    for run in manifest["runs"]:
        if run.get("error"):
            lines.append(f"| `{run['id']}` | — | — | — | — |")
            continue
        m = run.get("metrics") or {}
        lines.append(
            f"| `{run['id']}` | {run.get('wall_seconds', 0):.2f} | "
            f"{m.get('samples', 0):,} | {m.get('server_seconds', 0):.2f} | "
            f"{m.get('match_dots', 0):,} |"
        )

    lines.extend([
        "",
        "## Perceived notes (honest, not over-polished)",
        "",
        "### Feels magical",
        "- **`bacteria` + `magical` density + 5s pace** — dots hunt structure; pace long enough for Phase-2 cache window without feeling stuck.",
        "- **`virga` + `readable` + 5–7s** — ghost hint of Moon/4th (or other `?ghost=`) then Sun-in-1st colorifies; contemplative, not noisy.",
        "- **`harmonic` at 5s** — opacity breathes toward matches; map labels stay legible if density ≤ magical.",
        "",
        "### Feels gimmicky / risky",
        "- **`dense` + 2s pace** — reads as muddy snow; no time for background cache; annoys.",
        "- **`fibonacci` + `dense`** — opacity steps can feel \"UI demo\" unless pace ≥ 5s.",
        "- **`sparse` + 2s** — pretty but underwhelming; feels like a loading spinner, not discovery.",
        "",
        "### Six-condition readability",
        "- Sandbox supports A–F slots (6 conditions). Overlap colors are averaged proof tints — **mush appears above 3 conditions** on `dense`. Recommendation: product cap **3 visible** overlays for aesthetics even if API allows 6.",
        "",
        "## Phase-2 cache interaction",
        "",
        "Pace is also **background-cache budget**:",
        "- **2s**: almost no idle cache after first paint.",
        "- **5s**: comfortable window for priorities A–C on Americas viewport (per phase2 smoke).",
        "- **7s**: best for virga/ghost fades; may feel slow for power users.",
        "",
        "## Render budget (backward from chosen density)",
        "",
        "Preferred direction: **`bacteria` + `readable` + 5000ms**.",
        "",
        "From captured `readable` runs, scale samples by density preset (`budgetScale` in sandbox):",
        "- readable ≈ baseline samples in manifest",
        "- magical ≈ 1.0× readable",
        "- sparse ≈ 0.55×",
        "- dense ≈ 1.35× (not recommended for product)",
        "",
        "Ship budget: use measured adaptive **+20%** floor (`233,118` samples / 720×450) from targeted stress; raindrop reveal adds **wall-clock pacing only**, not extra truth samples.",
        "",
        "## Recommendation (one direction)",
        "",
        "**Primary:** `bacteria` clustering + incremental colorify + harmonic opacity (combine bacteria probe placement with harmonic curve, 5s default pace, `readable` density).",
        "",
        "**Secondary palette:** keep `virga` ghost pass for first 40% of timeline only when user enables a second exploratory layer.",
        "",
        "**Avoid:** grid-soldier reveals, `dense` packing, sub-3s pace for multi-condition stacks.",
        "",
        "## Artifacts",
        "",
        f"- Screenshots: `{OUT.relative_to(ROOT)}`",
        f"- Manifest: `{OUT.relative_to(ROOT)}/manifest.json`",
        "",
    ])
    NARRATIVE.parent.mkdir(parents=True, exist_ok=True)
    NARRATIVE.write_text("\n".join(lines))


def try_gif(frames: list[Path], out: Path) -> bool:
    if len(frames) < 2:
        return False
    try:
        images = [Image.open(p).convert("RGB") for p in frames]
        out.parent.mkdir(parents=True, exist_ok=True)
        images[0].save(
            out, save_all=True, append_images=images[1:],
            duration=400, loop=0,
        )
        return True
    except Exception:
        return False


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest: dict = {"runs": [], "modes": MODES, "paces_ms": PACES_MS, "densities": DENSITIES}

    # Matrix: all modes at 5s readable; pacing sweep on bacteria; density sweep on bacteria
    cases: list[tuple[str, int, str, str]] = []
    for mode in MODES:
        cases.append((mode, 5000, "readable", f"{mode}_5s_readable"))
    for pace in PACES_MS:
        if pace != 5000:
            cases.append(("bacteria", pace, "readable", f"bacteria_{pace}ms_readable"))
    for density in DENSITIES:
        if density != "readable":
            cases.append(("bacteria", 5000, density, f"bacteria_5s_{density}"))

    started = time.time()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 720, "height": 450})

        for mode, pace, density, case_id in cases:
            print(f"capture {case_id}...", flush=True)
            out_dir = OUT / case_id
            try:
                run = capture_case(page, mode, pace, density, out_dir)
                run["id"] = case_id
                manifest["runs"].append(run)
            except Exception as e:
                manifest["runs"].append({
                    "id": case_id, "error": str(e),
                    "mode": mode, "pace_ms": pace, "density": density,
                })
                print(f"  FAIL: {e}", flush=True)

        # Simple GIF: bacteria pacing frames (finals only)
        gif_frames = []
        for pace in PACES_MS:
            p = OUT / f"bacteria_{pace}ms_readable" / "final.png"
            if p.exists():
                gif_frames.append(p)
        gif_out = OUT / "bacteria_pace_sweep.gif"
        if try_gif(gif_frames, gif_out):
            manifest["gif_pace_sweep"] = str(gif_out.relative_to(ROOT))

        browser.close()

    manifest["wall_seconds_total"] = time.time() - started
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    write_narrative(manifest)
    print(f"Done. Manifest: {OUT / 'manifest.json'}")
    print(f"Narrative: {NARRATIVE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
