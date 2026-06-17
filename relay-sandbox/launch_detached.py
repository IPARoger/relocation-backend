#!/usr/bin/env python3
"""Spawn supervisor/monitor fully detached from parent shell."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SANDBOX = REPO / "relay-sandbox"
HANDOFFS = SANDBOX / "handoffs"


def env_with_defaults() -> dict[str, str]:
    env = os.environ.copy()
    defaults = {
        "RELAY_SANDBOX_TARGET": "10",
        "RELAY_SANDBOX_MIN_ELAPSED_SEC": "3600",
        "RELAY_SANDBOX_MOCK": "0",
        "RELAY_SANDBOX_FRESH": "1",
        "RELAY_SANDBOX_PROGRESS_SEC": "600",
        "RELAY_SANDBOX_MONITOR_SEC": "600",
    }
    for k, v in defaults.items():
        env.setdefault(k, v)
    return env


def pid_alive(pidfile: Path) -> int | None:
    if not pidfile.is_file():
        return None
    try:
        pid = int(pidfile.read_text().strip())
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError):
        return None


def spawn(cmd: list[str], log_path: Path, pidfile: Path | None) -> int:
    logf = open(log_path, "a", encoding="utf-8")
    proc = subprocess.Popen(
        cmd,
        cwd=REPO,
        env=env_with_defaults(),
        stdin=subprocess.DEVNULL,
        stdout=logf,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    if pidfile:
        pidfile.write_text(str(proc.pid), encoding="utf-8")
    print(f"started pid={proc.pid} cmd={' '.join(cmd)}")
    return proc.pid


def main() -> int:
    role = sys.argv[1] if len(sys.argv) > 1 else "supervisor"
    if role == "supervisor":
        pf = HANDOFFS / "supervisor.pid"
        alive = pid_alive(pf)
        if alive:
            print(f"supervisor already running pid={alive}")
            return 0
        spawn(
            [sys.executable, "-u", str(SANDBOX / "supervisor.py")],
            HANDOFFS / "supervisor.nohup.log",
            pf,
        )
    elif role == "monitor":
        pf = HANDOFFS / "monitor.pid"
        alive = pid_alive(pf)
        if alive:
            print(f"monitor already running pid={alive}")
            return 0
        spawn(
            [str(SANDBOX / "monitor.sh")],
            HANDOFFS / "monitor.log",
            pf,
        )
    else:
        print(f"unknown role: {role}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
