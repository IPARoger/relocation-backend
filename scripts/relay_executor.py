#!/usr/bin/env python3
"""relay_executor.py — runs the Cursor (execution) half of the relay.

Finds the newest task in tasks/ that has no matching results/ closeout yet, then
launches a Cursor CLOUD agent to execute it. The cloud agent does the work on a
branch, writes the results/<NN>_*.md closeout, and opens a Pull Request. It does
NOT merge — a human merges. That preserves the relay's human gate.

Why cloud (not local): you do not have to keep a laptop open; it runs on
Cursor's infrastructure straight from GitHub Actions.

Environment:
  CURSOR_API_KEY   Required for a live run (Cursor dashboard -> Integrations).
  GITHUB_REPOSITORY  e.g. "IPARoger/relocation-backend" (set automatically in CI).
  RELAY_BRANCH     Branch the agent should work from (default: current checkout).
  CURSOR_MODEL     Optional model id (default: auto).

Usage:
  python scripts/relay_executor.py --dry-run   # shows which task it would run
  python scripts/relay_executor.py             # live: launches cloud agent + PR

Exit codes:
  0  launched an agent (id printed) OR nothing pending
  2  invalid usage
  3  missing CURSOR_API_KEY on a live run
  4  launch failure
"""

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TASKS_DIR = REPO / "tasks"
RESULTS_DIR = REPO / "results"


def numbered(d):
    out = {}
    for f in d.glob("[0-9][0-9]_*.md"):
        m = re.match(r"(\d+)_", f.name)
        if m:
            out.setdefault(int(m.group(1)), f)
    return out


def next_pending_task():
    """Newest task number with no matching results file. Returns Path or None."""
    tasks = numbered(TASKS_DIR)
    results = set(numbered(RESULTS_DIR).keys())
    pending = sorted(n for n in tasks if n not in results)
    return tasks[pending[-1]] if pending else None


def build_prompt(task_path):
    task_text = task_path.read_text(encoding="utf-8")
    return (
        "You are the executing (Cursor) half of a governed two-agent relay.\n"
        "Execute EXACTLY the task below, staying strictly inside its declared\n"
        "scope. Obey every hard stop: if the work needs a schema/backend/database\n"
        "change, secrets, a migration, or renderer/math/overlay changes, STOP and\n"
        "explain instead of proceeding.\n\n"
        "When done, write the closeout to "
        f"results/{task_path.stem}.md following the relay closeout contract\n"
        "(files changed, validation evidence, rollback command, rejected scope,\n"
        "and VERIFIED or NOT VERIFIED). Do not merge; a human merges the PR.\n\n"
        "=== TASK FILE: " + task_path.name + " ===\n" + task_text
    )


def main(argv):
    args = argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    if args:
        sys.stderr.write("Usage: relay_executor.py [--dry-run]\n")
        return 2

    task = next_pending_task()
    if task is None:
        sys.stdout.write("NO_PENDING (every task has a results closeout)\n")
        return 0

    if dry_run:
        sys.stdout.write(
            "DRY-RUN: would launch a Cursor cloud agent for "
            + task.name
            + " (no API call made).\n"
        )
        return 0

    api_key = os.environ.get("CURSOR_API_KEY", "").strip()
    if not api_key:
        sys.stderr.write("Missing CURSOR_API_KEY in environment.\n")
        return 3

    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    branch = os.environ.get("RELAY_BRANCH", "").strip()
    model = os.environ.get("CURSOR_MODEL", "").strip() or "auto"
    prompt = build_prompt(task)

    try:
        from cursor_sdk import Agent, AgentOptions, CloudAgentOptions

        repo_url = "https://github.com/" + repo + ".git" if repo else None
        cloud = CloudAgentOptions(
            repos=[{"url": repo_url}] if repo_url else [],
            auto_create_pr=True,
            skip_reviewer_request=True,
        )

        result = Agent.prompt(
            prompt,
            AgentOptions(api_key=api_key, model=model, cloud=cloud),
        )
        agent_id = getattr(result, "id", None) or getattr(result, "agent_id", "?")
        sys.stdout.write("EXECUTED agent=" + str(agent_id) + " task=" + task.name + "\n")
        return 0
    except Exception as e:
        msg = str(e).lower()
        # Treat billing/quota/auth launch failures as a fundable problem so the
        # workflow warns the human (low balance) instead of failing silently.
        if any(k in msg for k in ("quota", "billing", "payment", "insufficient", "401", "unauthorized")):
            sys.stderr.write("Cloud agent launch blocked (billing/auth): " + str(e) + "\n")
            sys.stdout.write("LOW\n")
            return 5
        sys.stderr.write("Cloud agent launch failed: " + str(e) + "\n")
        return 4


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
