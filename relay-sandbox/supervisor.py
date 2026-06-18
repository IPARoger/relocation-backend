#!/usr/bin/env python3
"""Sandbox relay supervisor — extended soak: 10/10 + 1h minimum."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SANDBOX = REPO / "relay-sandbox"
LOG = SANDBOX / "handoffs" / "session.log"
HEARTBEAT = SANDBOX / "handoffs" / "heartbeat"
STATUS = SANDBOX / "handoffs" / "status.json"
PIDFILE = SANDBOX / "handoffs" / "supervisor.pid"
TARGET_OK = int(os.environ.get("RELAY_SANDBOX_TARGET", "10"))
SOAK_MIN_SEC = int(os.environ.get("RELAY_SANDBOX_MIN_ELAPSED_SEC", "3600"))
CYCLE_TIMEOUT = int(os.environ.get("RELAY_CYCLE_TIMEOUT", "3600"))
SLEEP_OK = int(os.environ.get("RELAY_SANDBOX_SLEEP_OK", "10"))
PROGRESS_SEC = int(os.environ.get("RELAY_SANDBOX_PROGRESS_SEC", "600"))


def load_dotenv() -> None:
    for name in (".env", ".env.local"):
        path = REPO / name
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            val = val.split("#", 1)[0].strip().strip('"').strip("'")
            if key.strip():
                os.environ.setdefault(key.strip(), val)


def sandbox_env() -> dict[str, str]:
    env = os.environ.copy()
    mock = os.environ.get("RELAY_SANDBOX_MOCK", "0").strip()
    skip_planner = os.environ.get("RELAY_SANDBOX_SKIP_PLANNER", "1").strip().lower() in (
        "1", "true", "yes"
    )
    env.update({
        "RELAY_HOME": str(SANDBOX),
        "RELAY_TASKS_DIR": str(SANDBOX / "tasks"),
        "RELAY_RESULTS_DIR": str(SANDBOX / "results"),
        "RELAY_HANDOFFS_DIR": str(SANDBOX / "handoffs"),
        "RELAY_GOVERNANCE_DIR": str(SANDBOX / "governance"),
        "RELAY_ROADMAP_QUEUE": str(SANDBOX / "ROADMAP_QUEUE.md"),
        "RELAY_RUNTIME": "local",
        "RELAY_PUSH": "0",
        "RELAY_SANDBOX_MOCK": mock,
        "RELAY_SANDBOX_SKIP_PLANNER": "1" if skip_planner else "0",
        "CURSOR_MODEL": os.environ.get("CURSOR_MODEL", "auto"),
        "RELAY_AUTO_MODEL": os.environ.get("RELAY_AUTO_MODEL", "1"),
    })
    return env


def log(msg: str) -> None:
    line = f"{msg}\n"
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line)
    sys.stdout.write(line)
    sys.stdout.flush()


def touch(note: str) -> None:
    HEARTBEAT.write_text(f"{time.time():.0f}\n{note}\n", encoding="utf-8")


def write_status(
    ok_streak: int,
    last_code: int,
    note: str,
    start_time: float,
    last_error: str = "",
) -> None:
    elapsed_min = round((time.time() - start_time) / 60, 1)
    STATUS.write_text(json.dumps({
        "ok_streak": ok_streak,
        "target": TARGET_OK,
        "min_elapsed_min": SOAK_MIN_SEC / 60,
        "elapsed_min": elapsed_min,
        "last_code": last_code,
        "last_error": last_error or None,
        "mock": os.environ.get("RELAY_SANDBOX_MOCK", "0"),
        "note": note,
        "updated": datetime.now(timezone.utc).isoformat(),
    }, indent=2) + "\n", encoding="utf-8")


def sandbox_has_pending() -> bool:
    import re
    tasks = SANDBOX / "tasks"
    results = SANDBOX / "results"

    def nums(d: Path) -> set[int]:
        out: set[int] = set()
        for f in d.glob("[0-9][0-9]_*.md"):
            m = re.match(r"(\d+)_", f.name)
            if m:
                out.add(int(m.group(1)))
        return out

    return bool(nums(tasks) - nums(results))


def cycle_succeeded() -> bool:
    if not LOG.is_file():
        return False
    lines = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    start = 0
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("--- cycle start "):
            start = i
            break
    block = "\n".join(lines[start:])
    if "NO_PENDING_TASK" in block or "Planner API call failed" in block:
        return False
    return any(x in block for x in ("EXECUTED_LOCAL", "EXECUTED_MOCK", "PLANNED ", "CLOSEOUT_FOR_BRAIN"))


def last_cycle_error() -> str:
    if not LOG.is_file():
        return ""
    lines = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    start = 0
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("--- cycle start "):
            start = i
            break
    block = lines[start:]
    for line in reversed(block):
        if "Planner API call failed" in line:
            return line.strip()
        if line.startswith("CYCLE_TIMEOUT"):
            return line.strip()
        if line.startswith("CYCLE_ERROR"):
            return line.strip()
        if "Missing CURSOR_API_KEY" in line:
            return line.strip()
    if block and block[-1].startswith("--- cycle exit ") and not block[-1].endswith("exit 0 ---"):
        return block[-1].strip()
    return ""


def run_cycle(env: dict[str, str]) -> int:
    touch("cycle_start")
    log(f"--- cycle start {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ---")
    skip_planner = env.get("RELAY_SANDBOX_SKIP_PLANNER", "1").strip() in ("1", "true", "yes")
    mode = "exec" if sandbox_has_pending() or skip_planner else "both"
    cmd = [
        sys.executable, "-u", str(REPO / "scripts" / "relay_robot.py"),
        "--once", "--step", mode,
    ]
    log(f"CMD {' '.join(cmd)}")
    try:
        with LOG.open("a", encoding="utf-8") as logf:
            proc = subprocess.run(
                cmd,
                cwd=REPO,
                env=env,
                timeout=CYCLE_TIMEOUT,
                stdout=logf,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        touch(f"exit_{proc.returncode}")
        log(f"--- cycle exit {proc.returncode} ---")
        return proc.returncode
    except subprocess.TimeoutExpired:
        log(f"CYCLE_TIMEOUT {CYCLE_TIMEOUT}s")
        touch("timeout")
        return 124
    except Exception as exc:
        log(f"CYCLE_ERROR {exc}")
        touch(f"error:{exc}")
        return 1


def load_streak() -> int:
    if not STATUS.is_file():
        return 0
    try:
        return int(json.loads(STATUS.read_text()).get("ok_streak", 0))
    except Exception:
        return 0


def maybe_progress(start_time: float, last_progress: float, ok_streak: int, last_error: str) -> float:
    now = time.time()
    if now - last_progress >= PROGRESS_SEC:
        elapsed_min = round((now - start_time) / 60, 1)
        log(
            f"PROGRESS ok_streak={ok_streak}/{TARGET_OK} "
            f"elapsed_min={elapsed_min} last_error={last_error or 'none'}"
        )
        write_status(ok_streak, 0, "progress", start_time, last_error)
        return now
    return last_progress


def main() -> int:
    load_dotenv()
    PIDFILE.write_text(str(os.getpid()), encoding="utf-8")
    env = sandbox_env()
    start_time = time.time()
    fresh = os.environ.get("RELAY_SANDBOX_FRESH", "1").strip().lower() in ("1", "true", "yes")
    ok_streak = 0 if fresh else load_streak()
    last_error = ""
    last_progress = start_time
    mock_flag = env.get("RELAY_SANDBOX_MOCK", "0")
    skip_flag = env.get("RELAY_SANDBOX_SKIP_PLANNER", "1")
    log(
        f"=== sandbox soak supervisor pid={os.getpid()} "
        f"target={TARGET_OK} min_elapsed_min={SOAK_MIN_SEC / 60:.0f} "
        f"mock={mock_flag} skip_planner={skip_flag} cursor_model={env.get('CURSOR_MODEL', 'auto')} ==="
    )
    write_status(ok_streak, 0, "soak_started", start_time, last_error)
    while True:
        last_progress = maybe_progress(start_time, last_progress, ok_streak, last_error)
        code = run_cycle(env)
        last_error = last_cycle_error() if code != 0 or not cycle_succeeded() else ""
        if code == 0 and cycle_succeeded():
            ok_streak += 1
            write_status(ok_streak, code, "ok", start_time, last_error)
            log(f"OK_STREAK {ok_streak}/{TARGET_OK}")
            elapsed = time.time() - start_time
            if ok_streak >= TARGET_OK and elapsed >= SOAK_MIN_SEC:
                elapsed_min = round(elapsed / 60, 1)
                log(
                    f"=== SANDBOX SOAK PASSED: {TARGET_OK} consecutive cycles "
                    f"and {elapsed_min} min elapsed ==="
                )
                touch("passed")
                write_status(ok_streak, code, "passed", start_time, last_error)
                return 0
            if ok_streak >= TARGET_OK:
                log(
                    f"OK_STREAK {ok_streak}/{TARGET_OK} but only "
                    f"{round(elapsed / 60, 1)} min elapsed — continuing until "
                    f"{SOAK_MIN_SEC / 60:.0f} min"
                )
            time.sleep(SLEEP_OK)
        elif code == 0:
            log("OK_STREAK hold (no pending task, waiting)")
            write_status(ok_streak, code, "waiting", start_time, last_error or "no pending work")
            time.sleep(30)
        else:
            ok_streak = 0
            write_status(ok_streak, code, "reset", start_time, last_error)
            log(f"OK_STREAK reset (exit {code})")
            time.sleep(30)


if __name__ == "__main__":
    raise SystemExit(main())
