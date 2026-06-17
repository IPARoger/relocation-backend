"""Phase 3.10 QA export: screenshot the Phase 3.09 sandbox at key elapsed times.

Drives `validation/sandboxes/phase3_01_rain_reveal_sandbox.html` through
representative milestones in its scout -> reproduction -> ghost-fade timeline.
Validation-only. Reads from the existing `window.__truthSubstrateSandbox`
debug surface; does not alter Phase 3.09 behavior.
"""

from __future__ import annotations

import contextlib
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "phase3_09_rain_reproduction"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_PATH = "validation/sandboxes/phase3_01_rain_reveal_sandbox.html"
CAPTURE_SPEED = 4  # sandbox's own speed multiplier (also surfaced via "Speed: 4x")

# Elapsed simulation times (ms) chosen from the sandbox timing model:
# MOTION_DELAY_MS=360, reproduction onset at delay+1050ms (~1410ms),
# confidence at delay+3300ms (~3660ms), ghost abort at delay+4300ms (~4660ms).
FRAMES = [
    {"name": "01_t0_initial",         "elapsed_ms": 0,    "guides": False, "status": "latent probes initializing"},
    {"name": "02_scout_phase",        "elapsed_ms": 900,  "guides": False, "status": "scouts searching hidden regions"},
    {"name": "03_reproduction_phase", "elapsed_ms": 2700, "guides": False, "status": "local reproduction near boundary candidates"},
    {"name": "04_ghost_fade_phase",   "elapsed_ms": 5500, "guides": False, "status": "ghost candidate samples fading"},
    {"name": "05_late_state",         "elapsed_ms": 9000, "guides": False, "status": "ghost candidate samples fading"},
    {"name": "06_late_state_guides",  "elapsed_ms": 9000, "guides": True,  "status": "ghost candidate samples fading"},
]


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@contextlib.contextmanager
def local_static_server(port: int):
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=str(REPO_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 5.0
        while time.time() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.05)
        yield
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def capture() -> dict:
    port = find_free_port()
    url = f"http://127.0.0.1:{port}/{SANDBOX_PATH}"
    captured: list[dict] = []
    with local_static_server(port):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                context = browser.new_context(viewport={"width": 1280, "height": 800})
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "window.__truthSubstrateSandbox && window.__truthSubstrateSandbox.getProbeCount() > 0",
                    timeout=10_000,
                )
                probe_count = page.evaluate(
                    "window.__truthSubstrateSandbox.getProbeCount()"
                )

                for frame in FRAMES:
                    # restart + set high speed + wait the right wall-clock window so
                    # the layer's own animator advances exactly `elapsed_ms` of sim time.
                    wall_ms = max(0, frame["elapsed_ms"] / CAPTURE_SPEED)
                    page.evaluate(
                        """({guides, speed}) => {
                            const api = window.__truthSubstrateSandbox;
                            api.setGuides(Boolean(guides));
                            api.setSpeed(1);
                            api.restart();
                            api.setSpeed(speed);
                        }""",
                        {"guides": frame["guides"], "speed": CAPTURE_SPEED},
                    )
                    if wall_ms > 0:
                        page.wait_for_timeout(wall_ms)
                    # Pause so the screenshot is a stable single frame.
                    paused_state = page.evaluate(
                        """() => {
                            const api = window.__truthSubstrateSandbox;
                            const map = document.querySelector('#map');
                            // Toggle pause via the existing UI button so we go through
                            // the public surface only.
                            const btn = document.getElementById('playPause');
                            if (btn.textContent === 'Pause') btn.click();
                            const status = document.getElementById('status').textContent;
                            return { status, probeCount: api.getProbeCount(), state: api.getState() };
                        }"""
                    )
                    out_path = OUT_DIR / f"{frame['name']}.png"
                    page.screenshot(path=str(out_path), full_page=False)
                    captured.append({
                        "name": frame["name"],
                        "file": str(out_path.relative_to(REPO_ROOT)),
                        "elapsed_ms": frame["elapsed_ms"],
                        "wall_ms": wall_ms,
                        "guides": frame["guides"],
                        "observed_status": paused_state["status"],
                        "expected_status_hint": frame["status"],
                        "probe_count": paused_state["probeCount"],
                    })

                manifest = {
                    "sandbox": SANDBOX_PATH,
                    "url": url,
                    "capture_speed_multiplier": CAPTURE_SPEED,
                    "probe_count_at_load": probe_count,
                    "frames": captured,
                }
                (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
                return manifest
            finally:
                browser.close()


if __name__ == "__main__":
    summary = capture()
    print(json.dumps(summary, indent=2))
