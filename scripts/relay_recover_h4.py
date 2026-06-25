#!/usr/bin/env python3
"""Recover finished H4 cloud-agent branches and unblock the task queue."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TASKS = REPO / "tasks"
RESULTS = REPO / "results"


def numbered(d: Path) -> dict[int, Path]:
    out: dict[int, Path] = {}
    for f in d.glob("[0-9][0-9]_*.md"):
        m = re.match(r"(\d+)_", f.name)
        if m:
            out[int(m.group(1))] = f
    return out


def run(cmd: list[str]) -> int:
    return subprocess.run(cmd, cwd=REPO, check=False).returncode


def main() -> int:
    run(["git", "fetch", "origin"])
    tasks = numbered(TASKS)
    results = set(numbered(RESULTS))
    pending = sorted(n for n in tasks if n not in results)
    if not pending:
        return 0
    # Merge any origin/cursor branch that contains results for pending task
    proc = subprocess.run(
        ["git", "branch", "-r"], cwd=REPO, capture_output=True, text=True, check=False
    )
    branches = [b.strip() for b in (proc.stdout or "").splitlines() if "origin/cursor/" in b]
    recovered = 0
    for n in pending:
        stem = tasks[n].stem
        result_name = f"{stem}.md"
        for br in branches:
            show = subprocess.run(
                ["git", "show", f"{br}:results/{result_name}"],
                cwd=REPO, capture_output=True, text=False, check=False,
            )
            if show.returncode != 0:
                continue
            local = RESULTS / result_name
            if not local.exists():
                local.write_bytes(show.stdout)
            short = br.replace("origin/", "")
            run(["git", "fetch", "origin", short.split("/", 1)[-1]])
            if run(["git", "merge", "--no-edit", br]) == 0:
                run(["git", "push", "origin", "main"])
                print(f"RECOVERED task {n} from {br}")
                recovered += 1
                results.add(n)
            break
    return 0 if recovered == 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
