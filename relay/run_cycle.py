#!/usr/bin/env python3
"""One relay cycle with timeout, fresh .env reload, heartbeat, auto model."""
from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HEARTBEAT = REPO / "relay" / "handoffs" / "heartbeat"
LOG = REPO / "relay" / "handoffs" / "session.log"
QUEUE = REPO / "relay" / "ROADMAP_QUEUE.md"
DEFAULT_TIMEOUT = int(os.environ.get("RELAY_CYCLE_TIMEOUT", "2700"))
HAIKU = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-4-6"


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
            key = key.strip()
            if key:
                os.environ[key] = val


def done_ids() -> set[str]:
    ids: set[str] = set()
    for f in (REPO / "results").glob("*.md"):
        text = f.read_text(encoding="utf-8", errors="replace")
        ids.update(re.findall(r"C[2-5]-[0-9]+", text))
        ids.update(re.findall(r"T[0-3]-[0-9]+", text))
        ids.update(re.findall(r"T0-[0-9]+", text))
    return ids


def next_queue_size() -> str | None:
    if not QUEUE.is_file():
        return None
    done = done_ids()
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| C") and not line.startswith("| T"):
            continue
        if "DEFER" in line:
            continue
        m = re.search(r"\|\s*(C[2-5]-[0-9]+|T[0-3]-[0-9]+)\s*\|\s*([SML])\s*\|", line)
        if not m:
            continue
        rid, size = m.group(1), m.group(2)
        if rid not in done:
            return size
    return None


def pick_model() -> str:
    if os.environ.get("RELAY_AUTO_MODEL", "1").strip() in ("0", "false", "no"):
        return os.environ.get("ANTHROPIC_MODEL", "").strip() or SONNET
    size = next_queue_size()
    if size == "S":
        return HAIKU
    if size in ("M", "L"):
        return SONNET
    return os.environ.get("ANTHROPIC_MODEL", "").strip() or SONNET


def touch_heartbeat(note: str = "") -> None:
    HEARTBEAT.parent.mkdir(parents=True, exist_ok=True)
    HEARTBEAT.write_text(f"{time.time():.0f}\n{note}\n", encoding="utf-8")


def log(msg: str) -> None:
    line = f"{msg}\n"
    sys.stdout.write(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line)


def main() -> int:
    load_dotenv()
    model = pick_model()
    os.environ["ANTHROPIC_MODEL"] = model
    touch_heartbeat("cycle_start")
    log(f"--- cycle start {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} model={model} ---")
    try:
        proc = subprocess.run(
            [sys.executable, "-u", str(REPO / "scripts" / "relay_robot.py"), "--once"],
            cwd=REPO,
            env=os.environ.copy(),
            timeout=DEFAULT_TIMEOUT,
        )
        code = proc.returncode
    except subprocess.TimeoutExpired:
        log(f"CYCLE_TIMEOUT after {DEFAULT_TIMEOUT}s — will auto-resume next cycle")
        touch_heartbeat("timeout")
        return 124
    except Exception as exc:
        log(f"CYCLE_ERROR {exc}")
        touch_heartbeat(f"error:{exc}")
        return 1
    log(f"--- cycle exit {code} {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} ---")
    touch_heartbeat(f"exit_{code}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
