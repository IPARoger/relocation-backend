#!/usr/bin/env python3
"""relay_robot.py — robot in the middle (replaces your paste, keeps discipline).

Exactly your hand workflow, automated:
  closeout in results/  →  chat brain (API + full context pack)  →  task  →  Cursor executes

TRANSPARENT: every step logged to relay/handoffs/<timestamp>_<step>.md
  You can read exactly what the robot sent and received. Nothing invisible.

Setup (one time):
  1. Put governance .md files in relay/governance/ (symlink or move existing docs)
  2. export ANTHROPIC_API_KEY=...  (or OPENAI_API_KEY)
  3. export CURSOR_API_KEY=... from cursor.com/dashboard?tab=cloud-agents
     → My Settings → API keys  (NOT the Integrations page)

Usage:
  python scripts/relay_robot.py --once     # one full cycle
  python scripts/relay_robot.py            # loop until PAUSE / Ctrl+C
  python scripts/relay_robot.py --dry-run  # show what would run, no API
  python scripts/relay_robot.py --step plan   # plan only (logged)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
import sys
sys.path.insert(0, str(SCRIPTS))
from relay_paths import HANDOFFS_DIR as HANDOFFS


def load_dotenv_files() -> None:
    for name in (".env", ".env.local"):
        path = REPO / name
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip(chr(34)).strip(chr(39))
            if key and key not in os.environ:
                os.environ[key] = val




def log_handoff(step: str, content: str) -> Path:
    HANDOFFS.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = HANDOFFS / f"{ts}_{step}.md"
    path.write_text(content, encoding="utf-8")
    print(f"HANDOFF {path.relative_to(REPO)}")
    return path


def run(cmd: list[str], env: dict | None = None) -> tuple[int, str]:
    merged = {**os.environ, **(env or {})}
    p = subprocess.run(cmd, cwd=REPO, env=merged, capture_output=True, text=True)
    out = ((p.stdout or "") + (p.stderr or "")).strip()
    return p.returncode, out


def pending_task() -> str | None:
    code, out = run(
        [sys.executable, str(SCRIPTS / "relay_executor.py"), "--dry-run"],
        env={"RELAY_RUNTIME": "local"},
    )
    m = re.search(r"for (\d+_[^\s)]+)", out)
    return m.group(1) if m else None


def git_commit(msg: str) -> None:
    run(["git", "add", "-A"])
    code, _ = run(["git", "diff", "--staged", "--quiet"])
    if code == 0:
        return
    run(["git", "commit", "-m", msg])
    if os.environ.get("RELAY_PUSH", "").lower() in ("1", "true", "yes"):
        run(["git", "push"])


def step_plan(dry_run: bool) -> str:
    """Returns: planned | pause | noop"""
    run([sys.executable, str(SCRIPTS / "relay_context.py")])
    ctx_path = HANDOFFS / "latest_context.md"
    ctx = ctx_path.read_text(encoding="utf-8") if ctx_path.is_file() else ""

    if dry_run:
        code, out = run(
            [sys.executable, str(SCRIPTS / "relay_planner.py"), "--dry-run", "--full-context"]
        )
        log_handoff("plan_dry_run", f"# Plan (dry run)\n\n```\n{out}\n```\n\n## Context pack\n\n{ctx}")
        print(out)
        return "noop"

    code, out = run(
        [sys.executable, str(SCRIPTS / "relay_planner.py"), "--full-context"]
    )
    log_handoff(
        "plan",
        f"# Plan API response\n\n```\n{out}\n```\n\n## Context pack sent\n\n{ctx}",
    )
    print(out)
    if out.startswith("PAUSE:"):
        return "pause"
    if "PLANNED" in out:
        git_commit(f"relay: robot plan — {out.splitlines()[0]}")
        return "planned"
    return "noop"


def step_execute(dry_run: bool) -> str:
    task = pending_task()
    if not task:
        print("NO_PENDING_TASK")
        return "noop"

    if dry_run:
        code, out = run(
            [sys.executable, str(SCRIPTS / "relay_executor.py"), "--dry-run"],
            env={"RELAY_RUNTIME": "local"},
        )
        log_handoff("exec_dry_run", f"# Execute (dry run)\n\nTask: {task}\n\n```\n{out}\n```")
        print(out)
        return "done"

    if not os.environ.get("CURSOR_API_KEY", "").strip():
        msg = (
            "# Cursor executor blocked — missing CURSOR_API_KEY\n\n"
            "Get key: https://cursor.com/dashboard?tab=cloud-agents\n"
            "→ My Settings → API keys → New API key\n\n"
            f"Task waiting: {task}\n"
        )
        inbox = REPO / "relay" / "inbox" / "NEEDS_CURSOR_API_KEY.md"
        inbox.parent.mkdir(parents=True, exist_ok=True)
        inbox.write_text(msg, encoding="utf-8")
        log_handoff("exec_blocked", msg)
        sys.stderr.write(
            "Missing CURSOR_API_KEY. See relay/inbox/NEEDS_CURSOR_API_KEY.md\n"
            "Dashboard: cursor.com/dashboard?tab=cloud-agents → My Settings → API keys\n"
        )
        return "blocked"

    code, out = run(
        [sys.executable, str(SCRIPTS / "relay_executor.py")],
        env={"RELAY_RUNTIME": "local"},
    )
    log_handoff("exec", f"# Cursor local agent\n\nTask: {task}\n\n```\n{out}\n```")
    print(out)
    if code != 0:
        return "error"
    sys.path.insert(0, str(SCRIPTS))
    from relay_context import write_closeout_handoff
    co = write_closeout_handoff()
    if co:
        print(f"CLOSEOUT_FOR_BRAIN {co.relative_to(REPO)} (next plan reads this — no paste needed)")
    git_commit(f"relay: robot executed {task}")
    run([sys.executable, str(SCRIPTS / "relay_progress.py"), "record-closeout"])
    git_commit("relay: progress")
    return "done"


def one_cycle(dry_run: bool, step: str) -> str:
    if step in ("both", "plan"):
        if pending_task() is None:
            r = step_plan(dry_run)
            if r in ("pause", "noop") and step == "plan":
                return r
        elif step == "plan":
            print(f"Task already pending: {pending_task()}")

    if step in ("both", "exec"):
        return step_execute(dry_run)
    return "done"


def main(argv: list[str]) -> int:
    load_dotenv_files()
    parser = argparse.ArgumentParser(description="Relay robot — chat discipline → Cursor")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--step", choices=["both", "plan", "exec"], default="both")
    args = parser.parse_args(argv)

    if not args.dry_run:
        has_brain = bool(
            os.environ.get("ANTHROPIC_API_KEY", "").strip()
            or os.environ.get("API_ROBOT", "").strip()
            or os.environ.get("OPENAI_API_KEY", "").strip()
        )
        if not has_brain and args.step in ("both", "plan"):
            sys.stderr.write(
                "Set API_ROBOT or ANTHROPIC_API_KEY (Claude brain) or OPENAI_API_KEY for planning.\n"
            )
            return 3

    gov = REPO / "relay" / "governance"
    md = [f for f in gov.glob("*.md") if f.name.upper() != "README.MD"] if gov.is_dir() else []
    if not md:
        sys.stderr.write(
            "WARNING: relay/governance/ has no .md files.\n"
            "Symlink or move your governance docs there (see relay/governance/README.md).\n"
        )

    while True:
        result = one_cycle(args.dry_run, args.step)
        if result in ("pause", "blocked", "error"):
            return 1 if result == "error" else 0
        if args.once or args.dry_run:
            return 0
        if result == "noop" and args.step == "exec":
            return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
