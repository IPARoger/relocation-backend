#!/usr/bin/env python3
"""One H4 relay cycle for GitHub Actions (Mac can sleep)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def run(cmd: list[str], **kw) -> int:
    return subprocess.run(cmd, cwd=REPO, check=False, **kw).returncode


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        run(["gh", "auth", "setup-git"], env={**os.environ, "GH_TOKEN": token})
        run(["git", "config", "user.email", "relay@users.noreply.github.com"])
        run(["git", "config", "user.name", "relay-github-actions"])

    run([sys.executable, str(SCRIPTS / "relay_recover_h4.py")])

    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "relay_executor.py"), "--dry-run"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if "NO_PENDING" in out:
        print("NO_PENDING — H4 queue empty, exiting")
        return 0

    print(out.strip())
    code = run([sys.executable, str(SCRIPTS / "relay_executor.py")])
    run(["git", "push", "origin", "HEAD:main"])
    return code


if __name__ == "__main__":
    raise SystemExit(main())
