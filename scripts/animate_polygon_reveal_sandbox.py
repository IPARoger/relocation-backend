"""Stitch animated GIFs of the polygon-reveal sandbox.

For each pacing variant (calm, bloom, eager), drive Playwright through
``?stopAtPhase=N`` URLs and assemble a per-phase GIF. Also build a
cache-swap GIF that captures the same probe field colored first as
Sun-in-1st, then as Moon-in-4th from cache (the engine call count
should not change between the two frames).

Every frame is annotated with real engine metrics (probe count, match
count, classify-endpoint calls). No decorative captioning.

Outputs in ``validation/screenshots/polygon_reveal_sandbox/``:

    calm_progression.gif        5 frames (phase 0 .. 4)
    bloom_progression.gif       4 frames
    eager_progression.gif       4 frames
    cache_swap_moon4.gif        2 frames

Usage:
    ./venv/bin/python3 scripts/animate_polygon_reveal_sandbox.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "polygon_reveal_sandbox"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_URL = "http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html"
PROFILE_ID = "baseline_validated"
SEED = 42
FRAME_MS = 1400
CACHE_SWAP_FRAME_MS = 2000

# Pacing variant → number of phases (initial scatter + refinement passes).
PACING_PHASES = {
    "calm":  5,  # scatter + 4 refines
    "bloom": 4,  # scatter + 3 refines
    "eager": 4,
}

CASES: list[dict[str, Any]] = [
    {
        "gif_id": "calm_progression",
        "kind": "progression",
        "pacing": "calm",
        "viewport": "world",
        "label": "Calm scatter — phase progression",
    },
    {
        "gif_id": "bloom_progression",
        "kind": "progression",
        "pacing": "bloom",
        "viewport": "world",
        "label": "Cosmic bloom — phase progression",
    },
    {
        "gif_id": "eager_progression",
        "kind": "progression",
        "pacing": "eager",
        "viewport": "world",
        "label": "Eager reveal — phase progression",
    },
    {
        "gif_id": "cache_swap_moon4",
        "kind": "cache_swap",
        "pacing": "calm",
        "viewport": "world",
        "swap_to": "moon:4",
        "label": "Cache swap — Sun-in-1st → Moon-in-4th",
    },
]


def build_url(*, pacing: str, viewport: str,
              stop_at_phase: int | None = None,
              swap_to: str | None = None,
              planet: str = "sun", house: int = 1) -> str:
    params: dict[str, str] = {
        "pacing": pacing,
        "viewport": viewport,
        "planet": planet,
        "house": str(house),
        "profile": PROFILE_ID,
        "seed": str(SEED),
        "auto": "1",
    }
    if stop_at_phase is not None:
        params["stopAtPhase"] = str(stop_at_phase)
    if swap_to is not None:
        params["swapTo"] = swap_to
    return f"{SANDBOX_URL}?{urlencode(params)}"


def wait_and_capture(page, url: str, frame_path: Path) -> dict[str, Any]:
    """Load ``url``, wait until the sandbox marks itself complete,
    screenshot the map pane only, and return the last snapshot + the
    cumulative classify-endpoint call count."""
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_function(
        "() => window.__sandboxStatus === 'complete' || window.__sandboxStatus === 'error'",
        timeout=90_000,
    )
    status = page.evaluate("() => window.__sandboxStatus")
    if status != "complete":
        err = page.evaluate("() => window.__sandboxLastError")
        raise RuntimeError(f"sandbox status={status}, error={err}")
    snapshots = page.evaluate(
        "() => JSON.parse(JSON.stringify(window.__sandboxSnapshots))"
    )
    classify_calls = page.evaluate("() => window.__classifyCallCount || 0")
    last = snapshots[-1] if snapshots else {}
    page.wait_for_timeout(900)  # let any per-probe CSS fades settle
    map_box = page.evaluate(
        "() => { const el = document.getElementById('map'); "
        "const r = el.getBoundingClientRect(); "
        "return {x: r.x, y: r.y, width: r.width, height: r.height}; }"
    )
    page.screenshot(path=str(frame_path), clip=map_box)
    last["__classify_calls"] = classify_calls
    return last


def annotate_frame(src_path: Path, caption_lines: list[str]) -> "Image.Image":
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(src_path).convert("RGB")
    draw = ImageDraw.Draw(im, "RGBA")
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 14)
    except Exception:
        try:
            font = ImageFont.truetype(
                "/System/Library/Fonts/Supplemental/Menlo.ttc", 14)
        except Exception:
            font = ImageFont.load_default()
    line_h = 18
    pad = 8
    strip_h = pad + line_h * len(caption_lines) + pad
    strip_w = max(draw.textlength(ln, font=font) for ln in caption_lines) + 2 * pad
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


def caption_for_phase(case_label: str, phase_idx: int, snap: dict[str, Any]) -> list[str]:
    return [
        f"{case_label}",
        f"phase {phase_idx}   ({snap.get('phase_id', '—')})",
        f"probes {snap.get('probe_count', 0):,}   "
        f"match {snap.get('matches', 0):,}   "
        f"non-match {snap.get('non_matches', 0):,}   "
        f"above cap {snap.get('capped', 0)}",
        f"target  {snap.get('planet', '—')} in {snap.get('house', '—')}   "
        f"classify calls {snap.get('__classify_calls', 0)}",
    ]


def caption_for_swap(case_label: str, snap: dict[str, Any], frame_label: str) -> list[str]:
    return [
        f"{case_label}",
        f"frame: {frame_label}",
        f"probes {snap.get('probe_count', 0):,}   "
        f"match {snap.get('matches', 0):,}   "
        f"non-match {snap.get('non_matches', 0):,}",
        f"target  {snap.get('planet', '—')} in {snap.get('house', '—')}   "
        f"classify calls {snap.get('__classify_calls', 0)}",
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


def run_progression(page, case: dict[str, Any]) -> dict[str, Any]:
    print(f"\n=== {case['gif_id']} (progression) ===")
    n_phases = PACING_PHASES[case["pacing"]]
    frames_pil = []
    frame_records = []
    for idx in range(n_phases):
        url = build_url(pacing=case["pacing"], viewport=case["viewport"],
                        stop_at_phase=idx)
        frame_path = OUT_DIR / f"{case['gif_id']}_frame_{idx}.png"
        print(f"  phase {idx}: {url}")
        last = wait_and_capture(page, url, frame_path)
        caption = caption_for_phase(case["label"], idx, last)
        img = annotate_frame(frame_path, caption)
        frames_pil.append(img)
        frame_records.append({
            "phase_idx": idx,
            "phase_id": last.get("phase_id"),
            "url": url,
            "frame_image": frame_path.name,
            "probe_count": last.get("probe_count"),
            "matches": last.get("matches"),
            "non_matches": last.get("non_matches"),
            "capped": last.get("capped"),
            "classify_calls": last.get("__classify_calls"),
        })
    gif_path = OUT_DIR / f"{case['gif_id']}.gif"
    write_gif(frames_pil, gif_path, FRAME_MS)
    print(f"  -> {gif_path.name}  ({len(frames_pil)} frames, {FRAME_MS} ms each)")
    return {
        "gif": gif_path.name,
        "frame_count": len(frames_pil),
        "frame_duration_ms": FRAME_MS,
        "frames": frame_records,
    }


def run_cache_swap(page, case: dict[str, Any]) -> dict[str, Any]:
    """Frame 0: full reveal with target Sun-in-1st (5 classify calls).
       Frame 1: same probe field re-colored as Moon-in-4th from cache
                (classify call count UNCHANGED — that is the point)."""
    print(f"\n=== {case['gif_id']} (cache swap) ===")
    frames_pil = []
    frame_records = []
    # Frame 0: original reveal (no swap)
    url0 = build_url(pacing=case["pacing"], viewport=case["viewport"])
    fp0 = OUT_DIR / f"{case['gif_id']}_frame_0_sun1.png"
    print(f"  frame 0 (sun-1): {url0}")
    snap0 = wait_and_capture(page, url0, fp0)
    cap0 = caption_for_swap(case["label"], snap0, "before swap (sun in 1st)")
    frames_pil.append(annotate_frame(fp0, cap0))
    frame_records.append({
        "url": url0, "frame_image": fp0.name,
        "probe_count": snap0.get("probe_count"),
        "matches": snap0.get("matches"),
        "non_matches": snap0.get("non_matches"),
        "classify_calls": snap0.get("__classify_calls"),
        "target": "sun-1",
    })
    # Frame 1: same run with swapTo set; the swap happens after completion,
    # uses only the in-page cache, no new classify-points calls.
    url1 = build_url(pacing=case["pacing"], viewport=case["viewport"],
                     swap_to=case["swap_to"])
    fp1 = OUT_DIR / f"{case['gif_id']}_frame_1_moon4.png"
    print(f"  frame 1 (moon-4 from cache): {url1}")
    snap1 = wait_and_capture(page, url1, fp1)
    cap1 = caption_for_swap(case["label"], snap1, "after swap (moon in 4th, from cache)")
    frames_pil.append(annotate_frame(fp1, cap1))
    frame_records.append({
        "url": url1, "frame_image": fp1.name,
        "probe_count": snap1.get("probe_count"),
        "matches": snap1.get("matches"),
        "non_matches": snap1.get("non_matches"),
        "classify_calls": snap1.get("__classify_calls"),
        "target": "moon-4",
    })
    gif_path = OUT_DIR / f"{case['gif_id']}.gif"
    write_gif(frames_pil, gif_path, CACHE_SWAP_FRAME_MS)
    classify_unchanged = (snap0.get("__classify_calls")
                          == snap1.get("__classify_calls"))
    print(f"  -> {gif_path.name}  ({len(frames_pil)} frames, "
          f"{CACHE_SWAP_FRAME_MS} ms each)  "
          f"classify_unchanged={classify_unchanged}")
    return {
        "gif": gif_path.name,
        "frame_count": len(frames_pil),
        "frame_duration_ms": CACHE_SWAP_FRAME_MS,
        "frames": frame_records,
        "classify_calls_unchanged_across_swap": classify_unchanged,
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
        "schema": "polygon_reveal_sandbox_animations@1",
        "sandbox_url": SANDBOX_URL,
        "profile_id": PROFILE_ID,
        "seed": SEED,
        "output_dir": str(OUT_DIR.relative_to(REPO_ROOT)),
        "animations": [],
    }
    page_errors: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1480, "height": 900},
                                   device_scale_factor=2)
        page = ctx.new_page()
        page.on("pageerror", lambda exc: page_errors.append(f"pageerror: {exc}"))
        for case in CASES:
            try:
                if case["kind"] == "progression":
                    summary["animations"].append({
                        "gif_id": case["gif_id"],
                        "kind": case["kind"],
                        **run_progression(page, case),
                    })
                elif case["kind"] == "cache_swap":
                    summary["animations"].append({
                        "gif_id": case["gif_id"],
                        "kind": case["kind"],
                        **run_cache_swap(page, case),
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
