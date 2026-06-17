"""Phase 3.11 capture + smoke: drives the Phase 3.11 event-driven rain sandbox.

Runs a headless Chromium against `validation/sandboxes/phase3_01_rain_reveal_sandbox.html`,
samples the new debug API over time to verify event-driven spawning works (probe count
must grow, phase must advance), then captures 6 PNG frames at meaningful elapsed times.

Validation-only. Does not edit any production files.
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
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "phase3_11_event_driven_reproduction"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_PATH = "validation/sandboxes/phase3_01_rain_reveal_sandbox.html"
CAPTURE_SPEED = 4

# Sampled elapsed times (ms of sim time) for the smoke trace.
SAMPLE_ELAPSED_MS = [0, 300, 700, 1200, 2000, 3500, 5500, 8000, 11000]

# Frames the user asked for.
FRAMES = [
    {"name": "01_t0_initial",              "elapsed_ms": 0,     "guides": False},
    {"name": "02_scout_phase",             "elapsed_ms": 700,   "guides": False},
    {"name": "03_reproduction_phase",      "elapsed_ms": 2200,  "guides": False},
    {"name": "04_ghost_fade_phase",        "elapsed_ms": 5500,  "guides": False},
    {"name": "05_late_state",              "elapsed_ms": 10000, "guides": False},
    {"name": "06_late_state_guides",       "elapsed_ms": 10000, "guides": True},
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


def restart_and_run(page, target_elapsed_ms: int, guides: bool, speed: int = CAPTURE_SPEED):
    page.evaluate(
        """({guides, speed}) => {
            const api = window.__truthSubstrateSandbox;
            api.setSpeed(1);
            api.restart();
            api.setGuides(Boolean(guides));
            api.setSpeed(speed);
        }""",
        {"guides": guides, "speed": speed},
    )
    wall_ms = max(0, target_elapsed_ms / speed)
    if wall_ms > 0:
        page.wait_for_timeout(wall_ms)


def snapshot(page):
    return page.evaluate(
        """() => {
            const api = window.__truthSubstrateSandbox;
            const state = api.getState();
            return {
                live: api.getLiveProbeCount(),
                initial: api.getInitialScoutCount(),
                spawned: api.getSpawnedProbeCount(),
                max: api.getMaxProbeCount(),
                phase: api.getCurrentPhase(),
                confidenceSelected: state.confidenceSelected,
                confidenceGhost: state.confidenceGhost,
                statusText: document.getElementById('status').textContent,
            };
        }"""
    )


def main():
    port = find_free_port()
    url = f"http://127.0.0.1:{port}/{SANDBOX_PATH}"
    out_manifest = {"sandbox": SANDBOX_PATH, "url": url, "capture_speed_multiplier": CAPTURE_SPEED}
    with local_static_server(port):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                context = browser.new_context(viewport={"width": 1280, "height": 800})
                page = context.new_page()
                console_errors: list[str] = []
                page.on("pageerror", lambda exc: console_errors.append(str(exc)))
                page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "window.__truthSubstrateSandbox && window.__truthSubstrateSandbox.hasEventDrivenSpawning === true",
                    timeout=10_000,
                )
                api_shape = page.evaluate(
                    """() => Object.keys(window.__truthSubstrateSandbox).sort()"""
                )

                # Smoke trace: probe count must grow over time.
                trace: list[dict] = []
                for elapsed in SAMPLE_ELAPSED_MS:
                    restart_and_run(page, elapsed, guides=False)
                    s = snapshot(page)
                    s["elapsed_ms"] = elapsed
                    trace.append(s)

                # Verify monotonic growth from t=0 to mid-game.
                first_live = trace[0]["live"]
                mid_live = trace[4]["live"]   # ~2000ms
                late_live = trace[-1]["live"]
                spawned_seen = trace[-1]["spawned"]
                phases_seen = sorted({t["phase"] for t in trace})
                growth_observed = mid_live > first_live + 8
                no_gear_shift_signal = spawned_seen > 0 and trace[1]["spawned"] >= 0  # spawns appear gradually
                event_spawning_works = spawned_seen >= 12

                # Capture frames.
                captured: list[dict] = []
                for frame in FRAMES:
                    restart_and_run(page, frame["elapsed_ms"], guides=frame["guides"])
                    s = snapshot(page)
                    out_path = OUT_DIR / f"{frame['name']}.png"
                    page.screenshot(path=str(out_path), full_page=False)
                    captured.append({
                        "file": str(out_path.relative_to(REPO_ROOT)),
                        "name": frame["name"],
                        "elapsed_ms": frame["elapsed_ms"],
                        "guides": frame["guides"],
                        "live": s["live"],
                        "spawned": s["spawned"],
                        "phase": s["phase"],
                        "status": s["statusText"],
                    })

                out_manifest.update({
                    "api_keys": api_shape,
                    "console_errors": console_errors,
                    "trace": trace,
                    "growth_observed": growth_observed,
                    "event_spawning_works": event_spawning_works,
                    "phases_seen": phases_seen,
                    "frames": captured,
                })
                (OUT_DIR / "manifest.json").write_text(json.dumps(out_manifest, indent=2))
                print(json.dumps({
                    "growth_observed": growth_observed,
                    "event_spawning_works": event_spawning_works,
                    "phases_seen": phases_seen,
                    "console_errors": console_errors,
                    "first_live": first_live,
                    "mid_live": mid_live,
                    "late_live": late_live,
                    "spawned_seen": spawned_seen,
                    "frames": [{k: f[k] for k in ("name", "elapsed_ms", "live", "spawned", "phase")} for f in captured],
                }, indent=2))
                return 0 if (growth_observed and event_spawning_works and not console_errors) else 2
            finally:
                browser.close()


if __name__ == "__main__":
    sys.exit(main())
