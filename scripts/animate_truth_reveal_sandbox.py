"""Stitch animated GIFs of the truth-field sandbox reveal modes.

Drives Playwright through ``?stopAtStage=N`` URLs for each animation case,
captures a still per stage from the live sandbox (no rendering changes),
and combines the frames into a GIF using Pillow. A small caption strip is
overlaid with the real engine metrics at that stage.

Outputs (alongside the still PNG bundle):

    validation/screenshots/truth_field_sandbox/
        mode_a_silent_asc_band.gif
        mode_b_pointillist_asc_band.gif
        mode_c_frontier_asc_band.gif
        latcap_ab_greenland.gif

Usage:
    ./venv/bin/python3 scripts/animate_truth_reveal_sandbox.py

All frame PNGs used to build a GIF are also written to disk
(``<case>_frame_<idx>.png``) so QA can scrub frame-by-frame.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "truth_field_sandbox"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_URL = "http://127.0.0.1:8000/map_SANDBOX_truth_reveal.html"
PROFILE_ID = "baseline_validated"

# Per-stage animation: same viewport, increasing stopAtStage.
STAGE_INDICES = [0, 1, 2, 3]
STAGE_FRAME_MS = 1200  # frame duration in the assembled GIF
LATCAP_FRAME_MS = 1800  # slower for the A/B compare

CASES: list[dict[str, Any]] = [
    {
        "gif_id": "mode_a_silent_asc_band",
        "kind": "stage_progression",
        "mode": "silent",
        "viewport": "asc",
        "lat_cap": "on",
        "label": "Mode A — Silent Convergence",
    },
    {
        "gif_id": "mode_b_pointillist_asc_band",
        "kind": "stage_progression",
        "mode": "pointillist",
        "viewport": "asc",
        "lat_cap": "on",
        "label": "Mode B — Pointillist Discovery",
    },
    {
        "gif_id": "mode_c_frontier_asc_band",
        "kind": "stage_progression",
        "mode": "frontier",
        "viewport": "asc",
        "lat_cap": "on",
        "label": "Mode C — Frontier Visualization",
    },
    {
        "gif_id": "latcap_ab_greenland",
        "kind": "latcap_ab",
        "mode": "silent",
        "viewport": "greenland",
        "label": "Lat-cap A/B — Greenland",
    },
]


def build_url(*, mode: str, viewport: str, stop_at_stage: int | None = None,
              lat_cap: str | bool | None = None) -> str:
    params: dict[str, str] = {
        "mode": mode,
        "viewport": viewport,
        "profile": PROFILE_ID,
        "auto": "1",
    }
    if stop_at_stage is not None:
        params["stopAtStage"] = str(stop_at_stage)
    if lat_cap is not None:
        if lat_cap is True or lat_cap == "on" or lat_cap == 1:
            params["latCap"] = "1"
        else:
            params["latCap"] = "0"
    return f"{SANDBOX_URL}?{urlencode(params)}"


def wait_and_capture(page, url: str, frame_path: Path) -> dict[str, Any]:
    """Load `url`, wait for the sandbox to mark itself complete, screenshot
    the map pane only, and return the engine's per-stage result for the
    LAST stage that ran during this load."""
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_function(
        "() => window.__sandboxStatus === 'complete' || window.__sandboxStatus === 'error'",
        timeout=90_000,
    )
    status = page.evaluate("() => window.__sandboxStatus")
    if status != "complete":
        err = page.evaluate("() => window.__sandboxLastError")
        raise RuntimeError(f"sandbox status={status}, error={err}")
    stage_results = page.evaluate(
        "() => JSON.parse(JSON.stringify(window.__sandboxStageResults))"
    )
    last = stage_results[-1] if stage_results else {}
    page.wait_for_timeout(350)  # let final paint transition settle
    map_box = page.evaluate(
        "() => { const el = document.getElementById('map'); "
        "const r = el.getBoundingClientRect(); "
        "return {x: r.x, y: r.y, width: r.width, height: r.height}; }"
    )
    page.screenshot(path=str(frame_path), clip=map_box)
    return last


def annotate_frame(src_path: Path, caption_lines: list[str]) -> "Image.Image":
    """Open a PNG, draw a small bottom-left caption strip with engine state,
    return the PIL image."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(src_path).convert("RGB")
    draw = ImageDraw.Draw(im, "RGBA")
    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/SFNSMono.ttf", 14)
    except Exception:
        try:
            font = ImageFont.truetype(
                "/System/Library/Fonts/Supplemental/Menlo.ttc", 14)
        except Exception:
            font = ImageFont.load_default()
    # Caption strip background
    line_h = 18
    pad = 8
    strip_h = pad + line_h * len(caption_lines) + pad
    strip_w = max(
        draw.textlength(ln, font=font) for ln in caption_lines
    ) + 2 * pad
    x0, y0 = 12, im.height - strip_h - 12
    draw.rectangle(
        [(x0, y0), (x0 + strip_w, y0 + strip_h)],
        fill=(8, 8, 10, 220),
        outline=(60, 60, 70, 255),
        width=1,
    )
    for i, ln in enumerate(caption_lines):
        draw.text((x0 + pad, y0 + pad + i * line_h), ln,
                  fill=(228, 228, 231, 255), font=font)
    return im


def caption_for_stage(case_label: str, stage_idx: int, stage: dict[str, Any]) -> list[str]:
    props = stage.get("properties", {})
    cv = props.get("convergence_vs_reference") or {}
    stop = props.get("stop_reason", "—")
    if props.get("converged"):
        stop_line = f"stop  converged ({stop})"
    elif props.get("overshoot_detected"):
        stop_line = f"stop  overshoot ({stop})"
    else:
        stop_line = f"stop  {stop}"
    return [
        f"{case_label}   stage {stage_idx}  ({stage.get('stage_id', '—')})",
        f"samples {props.get('truth_sample_count', '—'):,}   "
        f"leaves {stage.get('leaf_count', '—')}   "
        f"frontier {stage.get('frontier_count', '—')}   "
        f"residual {stage.get('residual_count', '—')}",
        f"maxΔ {cv.get('max_delta_vs_reference', 0):.4f}   "
        f"meanΔ {cv.get('mean_delta_vs_reference', 0):.4f}   "
        f"px>Δ {cv.get('pixels_above_threshold_pct', 0):.1f}%",
        stop_line,
    ]


def caption_for_latcap(label: str, capped: bool, stage: dict[str, Any]) -> list[str]:
    props = stage.get("properties", {})
    cv = props.get("convergence_vs_reference") or {}
    return [
        f"{label}   lat-cap {'ON' if capped else 'OFF'}",
        f"samples {props.get('truth_sample_count', '—'):,}   "
        f"leaves {stage.get('leaf_count', '—')}   "
        f"frontier {stage.get('frontier_count', '—')}",
        f"maxΔ vs uniform reference  {cv.get('max_delta_vs_reference', 0):.4f}",
        f"stop  {props.get('stop_reason', '—')}",
    ]


def write_gif(frames: list["Image.Image"], out_path: Path, duration_ms: int) -> None:
    if not frames:
        raise RuntimeError("no frames")
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=False,
        disposal=2,
    )


def run_stage_progression(page, case: dict[str, Any]) -> dict[str, Any]:
    print(f"\n=== {case['gif_id']} ({case['kind']}) ===")
    frames_pil = []
    frame_records = []
    for idx in STAGE_INDICES:
        url = build_url(
            mode=case["mode"],
            viewport=case["viewport"],
            stop_at_stage=idx,
            lat_cap=case.get("lat_cap"),
        )
        frame_path = OUT_DIR / f"{case['gif_id']}_frame_{idx}.png"
        print(f"  stage {idx}: {url}")
        last = wait_and_capture(page, url, frame_path)
        caption = caption_for_stage(case["label"], idx, last)
        img = annotate_frame(frame_path, caption)
        frames_pil.append(img)
        frame_records.append({
            "stage_idx": idx,
            "stage_id": last.get("stage_id"),
            "url": url,
            "frame_image": frame_path.name,
            "truth_sample_count": (last.get("properties") or {}).get("truth_sample_count"),
            "leaf_count": last.get("leaf_count"),
            "frontier_count": last.get("frontier_count"),
            "residual_count": last.get("residual_count"),
            "max_delta_vs_reference": ((last.get("properties") or {}).get("convergence_vs_reference") or {}).get("max_delta_vs_reference"),
            "mean_delta_vs_reference": ((last.get("properties") or {}).get("convergence_vs_reference") or {}).get("mean_delta_vs_reference"),
            "stop_reason": (last.get("properties") or {}).get("stop_reason"),
            "converged": (last.get("properties") or {}).get("converged"),
        })
    gif_path = OUT_DIR / f"{case['gif_id']}.gif"
    write_gif(frames_pil, gif_path, STAGE_FRAME_MS)
    print(f"  -> {gif_path.name}  ({len(frames_pil)} frames, {STAGE_FRAME_MS}ms each)")
    return {
        "gif": gif_path.name,
        "frame_count": len(frames_pil),
        "frame_duration_ms": STAGE_FRAME_MS,
        "frames": frame_records,
    }


def run_latcap_ab(page, case: dict[str, Any]) -> dict[str, Any]:
    print(f"\n=== {case['gif_id']} ({case['kind']}) ===")
    frames_pil = []
    frame_records = []
    for capped in (True, False):
        url = build_url(
            mode=case["mode"],
            viewport=case["viewport"],
            lat_cap="on" if capped else "off",
        )
        frame_path = OUT_DIR / f"{case['gif_id']}_frame_{'capped' if capped else 'uncapped'}.png"
        print(f"  capped={capped}: {url}")
        last = wait_and_capture(page, url, frame_path)
        caption = caption_for_latcap(case["label"], capped, last)
        img = annotate_frame(frame_path, caption)
        frames_pil.append(img)
        frame_records.append({
            "capped": capped,
            "url": url,
            "frame_image": frame_path.name,
            "truth_sample_count": (last.get("properties") or {}).get("truth_sample_count"),
            "leaf_count": last.get("leaf_count"),
            "frontier_count": last.get("frontier_count"),
            "max_delta_vs_reference": ((last.get("properties") or {}).get("convergence_vs_reference") or {}).get("max_delta_vs_reference"),
            "stop_reason": (last.get("properties") or {}).get("stop_reason"),
        })
    gif_path = OUT_DIR / f"{case['gif_id']}.gif"
    write_gif(frames_pil, gif_path, LATCAP_FRAME_MS)
    print(f"  -> {gif_path.name}  ({len(frames_pil)} frames, {LATCAP_FRAME_MS}ms each)")
    return {
        "gif": gif_path.name,
        "frame_count": len(frames_pil),
        "frame_duration_ms": LATCAP_FRAME_MS,
        "frames": frame_records,
    }


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed; install via `./venv/bin/pip install playwright`")
        return 2
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("Pillow not installed; install via `./venv/bin/pip install Pillow`")
        return 2

    summary: dict[str, Any] = {
        "schema": "truth_field_sandbox_animations@1",
        "sandbox_url": SANDBOX_URL,
        "output_dir": str(OUT_DIR.relative_to(REPO_ROOT)),
        "animations": [],
    }
    page_errors: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 800},
                                   device_scale_factor=2)
        page = ctx.new_page()
        page.on("pageerror", lambda exc: page_errors.append(f"pageerror: {exc}"))
        for case in CASES:
            try:
                if case["kind"] == "stage_progression":
                    summary["animations"].append({
                        "gif_id": case["gif_id"],
                        "kind": case["kind"],
                        **run_stage_progression(page, case),
                    })
                elif case["kind"] == "latcap_ab":
                    summary["animations"].append({
                        "gif_id": case["gif_id"],
                        "kind": case["kind"],
                        **run_latcap_ab(page, case),
                    })
            except Exception as exc:
                print(f"  FAIL {case['gif_id']}: {exc}")
                summary["animations"].append({
                    "gif_id": case["gif_id"],
                    "kind": case["kind"],
                    "error": str(exc),
                })
        browser.close()
    summary["page_errors"] = page_errors
    out_manifest = OUT_DIR / "animations_manifest.json"
    out_manifest.write_text(json.dumps(summary, indent=2))
    print(f"\nanimations manifest: {out_manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
