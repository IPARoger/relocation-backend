#!/usr/bin/env python3
"""Sandbox relay supervisor — one Python process, no bash stack."""
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
TARGET_OK = int(os.environ.get("RELAY_SANDBOX_TARGET", "5"))
CYCLE_TIMEOUT = int(os.environ.get("RELAY_CYCLE_TIMEOUT", "3600"))
SLEEP_OK = int(os.environ.get("RELAY_SANDBOX_SLEEP_OK", "10"))


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
    env.update({
        "RELAY_HOME": str(SANDBOX),
        "RELAY_TASKS_DIR": str(SANDBOX / "tasks"),
        "RELAY_RESULTS_DIR": str(SANDBOX / "results"),
        "RELAY_HANDOFFS_DIR": str(SANDBOX / "handoffs"),
        "RELAY_GOVERNANCE_DIR": str(SANDBOX / "governance"),
        "RELAY_ROADMAP_QUEUE": str(SANDBOX / "ROADMAP_QUEUE.md"),
        "RELAY_RUNTIME": "local",
        "RELAY_PUSH": "0",
            "RELAY_SANDBOX_MOCK": "1",
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


def write_status(ok_streak: int, last_code: int, note: str) -> None:
    STATUS.write_text(json.dumps({
        "ok_streak": ok_streak, "target": TARGET_OK, "last_code": last_code,
        "note": note, "updated": datetime.now(timezone.utc).isoformat(),
    }, indent=2) + "\n", encoding="utf-8")


def sandbox_has_pending() -> bool:
    """Any numbered sandbox task missing a results closeout."""
    import re
    tasks = SANDBOX / "tasks"
    results = SANDBOX / "results"
    def nums(d):
        out = set()
        for f in d.glob('[0-9][0-9]_*.md'):
            m = re.match(r'(\d+)_', f.name)
            if m:
                out.add(int(m.group(1)))
        return out
    return bool(nums(tasks) - nums(results))


def has_pending() -> bool:
    env = sandbox_env()
    p = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "relay_executor.py"), "--dry-run"],
        cwd=REPO, env=env, capture_output=True, text=True,
    )
    return "would launch" in (p.stdout or "").lower()


def cycle_succeeded() -> bool:
    if not LOG.is_file():
        return False
    tail = LOG.read_text(encoding="utf-8", errors="replace").splitlines()[-30:]
    block = "\n".join(tail)
    if "NO_PENDING_TASK" in block or "Planner API call failed" in block:
        return False
    return any(x in block for x in ("EXECUTED_LOCAL", "PLANNED ", "CLOSEOUT_FOR_BRAIN"))


def run_cycle(env: dict[str, str]) -> int:
    touch("cycle_start")
    log(f"--- cycle start {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ---")
    mode = "exec" if sandbox_has_pending() else "both"  # sandbox: pre-seeded tasks, never plan when pending
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


def main() -> int:
    load_dotenv()
    PIDFILE.write_text(str(os.getpid()), encoding="utf-8")
    env = sandbox_env()
    log(f"=== sandbox supervisor v2 pid={os.getpid()} target={TARGET_OK} ===")
    ok_streak = load_streak()
    while True:
        code = run_cycle(env)
        if code == 0 and cycle_succeeded():
            ok_streak += 1
            write_status(ok_streak, code, "ok")
            log(f"OK_STREAK {ok_streak}/{TARGET_OK}")
            if ok_streak >= TARGET_OK:
                log("=== SANDBOX PASSED: 5 consecutive cycles — ready for main workflow ===")
                touch("passed")
                return 0
            time.sleep(SLEEP_OK)
        else:
            ok_streak = load_streak()
            write_status(ok_streak, code, "reset")
            log(f"OK_STREAK reset (exit {code})")
            time.sleep(30)


if __name__ == "__main__":
    raise SystemExit(main())
