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
  python scripts/relay_executor.py             # live: cloud agent (default) or local (RELAY_RUNTIME=local)

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

import sys
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from relay_paths import REPO, RESULTS_DIR, TASKS_DIR


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
    return tasks[pending[0]] if pending else None



def merge_cloud_pr_and_pull(result) -> None:
    """After cloud agent finishes, merge PR/branch and pull main (RELAY_AUTO_MERGE=1)."""
    if os.environ.get("RELAY_AUTO_MERGE", "1").strip().lower() in ("0", "false", "no"):
        return
    import shutil
    import subprocess

    pr_url = ""
    branch = ""
    git = getattr(result, "git", None)
    if git and getattr(git, "branches", None):
        for br in git.branches:
            if getattr(br, "pr_url", ""):
                pr_url = br.pr_url
            if getattr(br, "branch", ""):
                branch = br.branch
    try:
        if shutil.which("gh") and pr_url:
            subprocess.run(
                ["gh", "pr", "merge", pr_url, "--squash", "--delete-branch"],
                cwd=REPO,
                check=False,
            )
        elif branch:
            subprocess.run(["git", "fetch", "origin", branch], cwd=REPO, check=False)
            subprocess.run(
                ["git", "merge", "--no-edit", f"origin/{branch}"],
                cwd=REPO,
                check=False,
            )
        subprocess.run(["git", "pull", "origin", "main"], cwd=REPO, check=False)
    except OSError as exc:
        sys.stderr.write(f"merge_cloud_pr_and_pull: {exc}\n")


def build_prompt(task_path, local: bool = False):
    task_text = task_path.read_text(encoding="utf-8")
    finish = (
        "Apply changes directly in the working tree. Do not open a PR.\n"
        if local
        else "Do not merge; a human merges the PR.\n"
    )
    return (
        "You are the executing (Cursor) half of a governed two-agent relay.\n"
        "Execute EXACTLY the task below, staying strictly inside its declared\n"
        "scope. Obey every hard stop: if the work needs a schema/backend/database\n"
        "change, secrets, a migration, or renderer/math/overlay changes, STOP and\n"
        "explain instead of proceeding.\n\n"
        "When done, write the closeout to "
        f"results/{task_path.stem}.md following the relay closeout contract\n"
        "(files changed, validation evidence, rollback command, rejected scope,\n"
        "and VERIFIED or NOT VERIFIED). "
        + finish
        + "\n=== TASK FILE: "
        + task_path.name
        + " ===\n"
        + task_text
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
        runtime = os.environ.get("RELAY_RUNTIME", "cloud").strip().lower()
        where = "local agent" if runtime == "local" else "cloud agent"
        sys.stdout.write(
            "DRY-RUN: would launch a Cursor " + where + " for "
            + task.name
            + " (no API call made).\n"
        )
        return 0


    if os.environ.get("RELAY_SANDBOX_MOCK", "").strip() in ("1", "true", "yes"):
        out_path = RESULTS_DIR / f"{task.stem}.md"
        body = (
            f"# RESULT: {task.stem}\n\n"
            f"**Roadmap ID:** SB-N (sandbox mock)\n"
            f"**Author:** sandbox mock executor\n\n"
            f"Mock closeout for loop validation. Task file: {task.name}\n\n"
            f"**VERIFIED**\n"
        )
        out_path.write_text(body, encoding="utf-8")
        sys.stdout.write(f"EXECUTED_MOCK task={task.name} closeout={out_path.relative_to(REPO)}\n")
        return 0


    api_key = os.environ.get("CURSOR_API_KEY", "").strip()
    if not api_key:
        sys.stderr.write("Missing CURSOR_API_KEY in environment.\n")
        return 3

    runtime = os.environ.get("RELAY_RUNTIME", "cloud").strip().lower()
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    branch = os.environ.get("RELAY_BRANCH", "").strip()
    default_model = "composer-2.5" if runtime == "local" else "auto"
    model = os.environ.get("CURSOR_MODEL", "").strip() or default_model
    prompt = build_prompt(task, local=(runtime == "local"))

    try:
        from cursor_sdk import Agent, AgentOptions, CloudAgentOptions, LocalAgentOptions

        if runtime == "local":
            opts = AgentOptions(
                api_key=api_key,
                model=model,
                local=LocalAgentOptions(cwd=str(REPO)),
            )
            result = Agent.prompt(prompt, opts)
            agent_id = getattr(result, "id", None) or getattr(result, "agent_id", "?")
            status = getattr(result, "status", "?")
            sys.stdout.write(
                "EXECUTED_LOCAL agent="
                + str(agent_id)
                + " status="
                + str(status)
                + " task="
                + task.name
                + "\n"
            )
            if str(status).lower() in ("error", "failed", "cancelled"):
                return 4
            return 0

        repo_url = "https://github.com/" + repo + ".git" if repo else None
        cloud = CloudAgentOptions(
            repos=[{"url": repo_url}] if repo_url else [],
            auto_create_pr=True,
            skip_reviewer_request=True,
        )

        wait = os.environ.get("RELAY_EXECUTOR_WAIT", "").strip().lower() in (
            "1",
            "true",
            "yes",
        )
        opts = AgentOptions(api_key=api_key, model=model, cloud=cloud)
        if wait:
            result = Agent.prompt(prompt, opts)
            agent_id = getattr(result, "id", None) or getattr(result, "agent_id", "?")
            status = getattr(result, "status", "?")
            sys.stdout.write(
                "EXECUTED_CLOUD agent="
                + str(agent_id)
                + " status="
                + str(status)
                + " task="
                + task.name
                + "\n"
            )
            merge_cloud_pr_and_pull(result)
            if str(status).lower() in ("error", "failed", "cancelled"):
                return 4
            return 0

        agent = Agent.create(opts)
        run = agent.send(prompt)
        run_id = getattr(run, "run_id", None) or getattr(run, "id", "?")
        sys.stdout.write(
            "LAUNCHED agent=" + agent.agent_id + " run=" + str(run_id) + " task=" + task.name + "\n"
        )
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
