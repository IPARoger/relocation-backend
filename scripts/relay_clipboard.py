#!/usr/bin/env python3
"""Dead-simple relay helper — automates the GPT paste step only.

What you did by hand:
  1. Read latest results/ closeout
  2. Ask GPT/Claude for next task
  3. Paste prompt into Cursor

This script does 1+2 and copies the new task to your clipboard.
You stay in Cursor (no CURSOR_API_KEY, no cloud agents, no GitHub Actions).

Usage:
  export OPENAI_API_KEY=...   # or ANTHROPIC_API_KEY
  python scripts/relay_clipboard.py          # plan + copy to clipboard
  python scripts/relay_clipboard.py --open   # also opens the task file

Then in Cursor: Cmd+I (or your agent shortcut), paste, Enter.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def copy_to_clipboard(text: str) -> bool:
  try:
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
    return True
  except Exception:
    return False


def main(argv: list[str]) -> int:
  parser = argparse.ArgumentParser(description="Plan next relay task and copy to clipboard")
  parser.add_argument("--open", action="store_true", help="Open task file in default editor")
  args = parser.parse_args(argv)

  proc = subprocess.run(
    [sys.executable, str(REPO / "scripts" / "relay_planner.py")],
    cwd=REPO,
    capture_output=True,
    text=True,
  )
  out = (proc.stdout or "") + (proc.stderr or "")
  print(out.strip())

  if proc.returncode != 0:
    return proc.returncode
  if out.strip().startswith("PAUSE:"):
    return 0

  # Find newest task file (planner just wrote it)
  tasks = sorted((REPO / "tasks").glob("[0-9][0-9]_*.md"), key=lambda p: p.stat().st_mtime)
  if not tasks:
    sys.stderr.write("No task file found after planning.\n")
    return 4
  task = tasks[-1]
  body = task.read_text(encoding="utf-8")

  prompt = (
    "Execute this relay task exactly. Stay in scope. Write closeout to "
    f"results/{task.stem}.md when done.\n\n"
    + body
  )

  if copy_to_clipboard(prompt):
    print(f"\n✓ Copied to clipboard ({task.name}) — paste into Cursor agent (Cmd+I).")
  else:
    print(f"\n--- paste into Cursor ---\n{prompt}\n---")

  if args.open:
    subprocess.run(["open", str(task)], check=False)

  return 0


if __name__ == "__main__":
  raise SystemExit(main(sys.argv[1:]))
