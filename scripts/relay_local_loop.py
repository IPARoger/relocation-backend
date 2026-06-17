#!/usr/bin/env python3
"""relay_local_loop.py — fast sequential relay on your Mac (copy-paste speed).

Replaces GitHub Actions + cloud agents for the hot path:
  1. Plan next task (cheap OpenAI API, ~seconds)
  2. Execute with LOCAL Cursor SDK (~minutes, same machine as IDE)
  3. Git commit (+ optional push for backup)
  4. Repeat

Cost profile (typical):
  - Planner: gpt-4o-mini, fractions of a cent per task (not Opus).
  - Executor: Cursor subscription / Composer models via SDK — NOT Claude Opus API.

Environment (required for live runs):
  OPENAI_API_KEY, CURSOR_API_KEY

Optional:
  OPENAI_MODEL          default gpt-4o-mini
  CURSOR_MODEL          default composer-2.5 (avoid opus — expensive)
  RELAY_LOCAL_PUSH=1    git push after each task
  RELAY_LOCAL_PULL=1    git pull --rebase before each cycle
  RELAY_LOCAL_MAX_TASKS N  stop after N tasks (default: unlimited)
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID  optional pings

Usage:
  pip install cursor-sdk
  export OPENAI_API_KEY=... CURSOR_API_KEY=...
  python scripts/relay_local_loop.py --dry-run
  python scripts/relay_local_loop.py --once      # one plan+execute cycle
  python scripts/relay_local_loop.py             # loop until PAUSE or Ctrl+C
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def run_script(name: str, *extra: str, env: dict | None = None) -> tuple[int, str]:
    merged = {**os.environ, **(env or {})}
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / name), *extra],
        cwd=REPO,
        env=merged,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def notify(event: str, task: str | None = None, message: str | None = None) -> None:
    args = [event]
    if task:
        args += ["--task", task]
    if message:
        args += ["--message", message]
    run_script("relay_notify.py", *args)


def git(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def pending_task_name() -> str | None:
    code, out = run_script("relay_executor.py", "--dry-run", env={"RELAY_RUNTIME": "local"})
    if "would launch" in out:
        m = re.search(r"for (\d+_[^\s)]+)", out)
        return m.group(1) if m else None
    return None


def commit_all(message: str) -> None:
    git("add", "-A")
    code, _ = git("diff", "--staged", "--quiet")
    if code == 0:
        print("(nothing to commit)")
        return
    code, out = git("commit", "-m", message)
    print(out or f"commit exit {code}")
    if os.environ.get("RELAY_LOCAL_PUSH", "").strip().lower() in ("1", "true", "yes"):
        code, out = git("push")
        print(out or f"push exit {code}")


def maybe_pull() -> None:
    if os.environ.get("RELAY_LOCAL_PULL", "").strip().lower() not in ("1", "true", "yes"):
        return
    code, out = git("pull", "--rebase")
    print(out)
    if code != 0:
        sys.stderr.write("git pull failed; fix conflicts and re-run.\n")
        raise SystemExit(1)


def check_digest_pause(force: bool) -> None:
    if force:
        return
    code, out = run_script("relay_progress.py", "status")
    if '"awaiting_digest_ack": true' in out.replace(" ", "").lower():
        sys.stderr.write(
            "PAUSE: digest acknowledgment pending. Read Telegram summary, then:\n"
            "  python scripts/relay_progress.py clear-ack\n"
            "Or re-run with --force\n"
        )
        raise SystemExit(0)


def one_cycle(dry_run: bool) -> str:
    """Returns: done | pause | noop"""
    maybe_pull()
    task = pending_task_name()

    if task is None:
        print("No pending task — planning next…")
        if dry_run:
            code, out = run_script("relay_planner.py", "--dry-run")
            print(out)
            return "noop"
        code, out = run_script("relay_planner.py")
        print(out)
        if code != 0:
            sys.stderr.write(f"planner failed ({code})\n")
            raise SystemExit(code)
        if out.strip().startswith("PAUSE:"):
            notify("approval", message=out.strip())
            return "pause"
        if "PLANNED" not in out:
            return "noop"
        commit_all(f"relay: {out.splitlines()[0]}")
        task = pending_task_name()
        if task is None:
            sys.stderr.write("Planner wrote a task but executor sees none pending.\n")
            return "noop"

    print(f"Executing task {task} (local Cursor SDK)…")
    if dry_run:
        code, out = run_script(
            "relay_executor.py",
            "--dry-run",
            env={"RELAY_RUNTIME": "local"},
        )
        print(out)
        return "done"

    notify("started", task=task)
    code, out = run_script(
        "relay_executor.py",
        env={"RELAY_RUNTIME": "local"},
    )
    print(out)
    if code == 5:
        notify("low-balance", task=task)
        raise SystemExit(5)
    if code != 0:
        notify("not-verified", task=task, message=out[:500])
        raise SystemExit(code)

    commit_all(f"relay: complete {task}")
    run_script("relay_progress.py", "record-closeout")
    run_script("relay_progress.py", "send-digest-if-due")
    commit_all("relay: progress counter")
    notify("complete", task=task)
    return "done"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Local fast relay loop")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--once", action="store_true", help="Run one plan+execute cycle")
    parser.add_argument("--force", action="store_true", help="Ignore digest pause gate")
    args = parser.parse_args(argv)

    if not args.dry_run:
        if not os.environ.get("CURSOR_API_KEY", "").strip():
            sys.stderr.write("Missing CURSOR_API_KEY (Cursor → Settings → Integrations)\n")
            return 3
        has_planner = bool(
            os.environ.get("OPENAI_API_KEY", "").strip()
            or os.environ.get("ANTHROPIC_API_KEY", "").strip() or os.environ.get("API_ROBOT", "").strip()
        )
        if not has_planner and pending_task_name() is None:
            sys.stderr.write(
                "Missing OPENAI_API_KEY or ANTHROPIC_API_KEY for planning.\n"
                "(Not needed when a task is already waiting in tasks/.)\n"
            )
            return 3

    check_digest_pause(args.force)

    if not args.dry_run and os.environ.get("OPENAI_API_KEY", "").strip():
        code, out = run_script("relay_preflight.py")
        print(out)
        if code == 5:
            notify("low-balance")
            return 5

    max_tasks = os.environ.get("RELAY_LOCAL_MAX_TASKS", "").strip()
    limit = int(max_tasks) if max_tasks.isdigit() else None
    done = 0

    while True:
        result = one_cycle(args.dry_run)
        if result == "pause":
            return 0
        if result == "done":
            done += 1
            if args.once or (limit is not None and done >= limit):
                return 0
        if result == "noop" and args.once:
            return 0
        if args.dry_run:
            return 0
        time.sleep(2)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
