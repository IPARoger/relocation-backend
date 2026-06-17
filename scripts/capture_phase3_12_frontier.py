"""Phase 3.12 capture + smoke: drives the frontier-based discovery sandbox.

Runs a headless Chromium against `validation/sandboxes/phase3_01_rain_reveal_sandbox.html`,
samples the new debug API over time to verify:
  - probe count grows organically (event-driven, no global gear shift)
  - frontier nodes are consumed as discovery proceeds
  - most spawns are local (localSpawnRatio dominates longRangeSpawnRatio)
  - contour confidence rises legibly
Then captures 6 PNG frames at meaningful elapsed times.

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
OUT_DIR = REPO_ROOT / "validation" / "screenshots" / "phase3_12_frontier_discovery"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SANDBOX_PATH = "validation/sandboxes/phase3_01_rain_reveal_sandbox.html"
CAPTURE_SPEED = 4

SAMPLE_ELAPSED_MS = [0, 300, 700, 1200, 2000, 3500, 5500, 8000, 11000]

FRAMES = [
    {"name": "01_t0_initial",                "elapsed_ms": 0,     "guides": False},
    {"name": "02_seed_phase",                "elapsed_ms": 700,   "guides": False},
    {"name": "03_frontier_expansion",        "elapsed_ms": 2200,  "guides": False},
    {"name": "04_membrane_locking",          "elapsed_ms": 4200,  "guides": False},
    {"name": "05_late_state",                "elapsed_ms": 10000, "guides": False},
    {"name": "06_late_state_guides",         "elapsed_ms": 10000, "guides": True},
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
                frontierTotal: state.frontierNodeCount,
                frontierActive: state.activeFrontierCount,
                localSpawnRatio: state.localSpawnRatio,
                longRangeSpawnRatio: state.longRangeSpawnRatio,
                contourConfidence: state.contourConfidence,
                membraneFormationConfidence: state.membraneFormationConfidence,
                ghostConfidence: state.ghostConfidence,
                localSpawns: state.localSpawns,
                longRangeSpawns: state.longRangeSpawns,
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
                    "window.__truthSubstrateSandbox && window.__truthSubstrateSandbox.hasFrontierBasedDiscovery === true",
                    timeout=10_000,
                )
                api_shape = page.evaluate(
                    """() => Object.keys(window.__truthSubstrateSandbox).sort()"""
                )

                trace: list[dict] = []
                for elapsed in SAMPLE_ELAPSED_MS:
                    restart_and_run(page, elapsed, guides=False)
                    s = snapshot(page)
                    s["elapsed_ms"] = elapsed
                    trace.append(s)

                first_live = trace[0]["live"]
                mid_live = trace[4]["live"]
                late_live = trace[-1]["live"]
                spawned_seen = trace[-1]["spawned"]
                phases_seen = sorted({t["phase"] for t in trace})
                growth_observed = mid_live > first_live + 8
                event_spawning_works = spawned_seen >= 10
                late_local_ratio = trace[-1]["localSpawnRatio"]
                locality_dominant = late_local_ratio >= 0.70
                contour_confidence_rises = trace[-1]["contourConfidence"] > trace[1]["contourConfidence"]
                frontier_consumed = trace[-1]["frontierActive"] < trace[0]["frontierActive"]

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
                        "localSpawnRatio": s["localSpawnRatio"],
                        "contourConfidence": s["contourConfidence"],
                        "status": s["statusText"],
                    })

                out_manifest.update({
                    "api_keys": api_shape,
                    "console_errors": console_errors,
                    "trace": trace,
                    "growth_observed": growth_observed,
                    "event_spawning_works": event_spawning_works,
                    "locality_dominant": locality_dominant,
                    "late_local_spawn_ratio": late_local_ratio,
                    "contour_confidence_rises": contour_confidence_rises,
                    "frontier_consumed": frontier_consumed,
                    "phases_seen": phases_seen,
                    "frames": captured,
                })
                (OUT_DIR / "manifest.json").write_text(json.dumps(out_manifest, indent=2))
                print(json.dumps({
                    "growth_observed": growth_observed,
                    "event_spawning_works": event_spawning_works,
                    "locality_dominant": locality_dominant,
                    "late_local_spawn_ratio": late_local_ratio,
                    "contour_confidence_rises": contour_confidence_rises,
                    "frontier_consumed": frontier_consumed,
                    "phases_seen": phases_seen,
                    "console_errors": console_errors,
                    "first_live": first_live,
                    "mid_live": mid_live,
                    "late_live": late_live,
                    "spawned_seen": spawned_seen,
                    "frames": [{k: f[k] for k in ("name", "elapsed_ms", "live", "spawned", "phase", "localSpawnRatio", "contourConfidence")} for f in captured],
                }, indent=2))
                return 0 if (
                    growth_observed and event_spawning_works and locality_dominant
                    and contour_confidence_rises and not console_errors
                ) else 2
            finally:
                browser.close()


if __name__ == "__main__":
    sys.exit(main())
