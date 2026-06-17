#!/usr/bin/env python3
"""Wait for a relay cloud-agent PR and squash-merge it to main (optional automation)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

TIMEOUT = int(os.environ.get("RELAY_AUTO_MERGE_TIMEOUT", "600"))  # 90 min
POLL = int(os.environ.get("RELAY_AUTO_MERGE_POLL", "30"))


def disabled() -> bool:
    return os.environ.get("RELAY_AUTO_MERGE", "1").strip().lower() in ("0", "false", "no")


def api(token: str, method: str, path: str, body: dict | None = None):
    url = "https://api.github.com" + path
    data = json.dumps(body).encode() if body is not None else None
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if data:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as err:
        raw = err.read().decode()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"message": raw}
        return {"_error": True, "_status": err.code, **payload}


def list_open_prs(token: str, repo: str) -> list[dict]:
    out = api(token, "GET", f"/repos/{repo}/pulls?state=open&per_page=20&sort=created&direction=desc")
    return out if isinstance(out, list) else []


def pick_pr(prs: list[dict], task: int | None) -> dict | None:
    relay = [p for p in prs if (p.get("head") or {}).get("ref", "").startswith("cursor/")]
    if not relay:
        return None
    if task is not None:
        needle = str(task)
        for p in relay:
            title = (p.get("title") or "").lower()
            body = (p.get("body") or "").lower()
            if needle in title or f"task {needle}" in title or f"task {needle}:" in title:
                return p
    return relay[0]


def mark_ready(token: str, repo: str, number: int) -> bool:
    r = api(token, "POST", f"/repos/{repo}/pulls/{number}/ready_for_review")
    if r.get("_error"):
        return False
    return True


def squash_merge(token: str, repo: str, number: int) -> tuple[bool, str]:
    r = api(
        token,
        "PUT",
        f"/repos/{repo}/pulls/{number}/merge",
        {"merge_method": "squash"},
    )
    if r.get("_error"):
        return False, f"HTTP {r.get('_status')}: {r.get('message', r)}"
    if r.get("merged"):
        return True, r.get("sha", "")
    return False, str(r)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=int, default=None)
    parser.add_argument("--once", action="store_true", help="Single poll attempt (for cron)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv[1:])

    if disabled():
        print("SKIP: RELAY_AUTO_MERGE disabled")
        return 0

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if not token or not repo:
        sys.stderr.write("Need GITHUB_TOKEN and GITHUB_REPOSITORY\n")
        return 3

    deadline = time.time() + (POLL if args.once else TIMEOUT)
    seen: int | None = None

    while time.time() < deadline:
        prs = list_open_prs(token, repo)
        pr = pick_pr(prs, args.task)
        if pr is None:
            print(f"waiting for relay PR (task={args.task})...")
            time.sleep(POLL)
            continue

        number = pr["number"]
        if seen != number:
            print(f"found PR #{number}: {pr.get('title', '')[:70]}")
            seen = number

        if pr.get("draft"):
            if args.dry_run:
                print(f"DRY-RUN: would mark PR #{number} ready")
            else:
                mark_ready(token, repo, number)
                print(f"marked PR #{number} ready for review")
            time.sleep(15)
            continue

        mergeable = pr.get("mergeable")
        state = pr.get("mergeable_state")
        if mergeable is False and state == "dirty":
            sys.stderr.write(f"PR #{number} has conflicts; cannot auto-merge\n")
            return 4
        if mergeable is None:
            time.sleep(POLL)
            continue
        if mergeable is False:
            print(f"PR #{number} not mergeable yet ({state}); waiting...")
            time.sleep(POLL)
            continue

        if args.dry_run:
            print(f"DRY-RUN: would squash-merge PR #{number}")
            return 0

        ok, detail = squash_merge(token, repo, number)
        if ok:
            print(f"MERGED PR #{number} squash -> {detail[:12]}")
            return 0
        print(f"merge attempt failed: {detail}; retrying...")
        time.sleep(POLL)

    sys.stderr.write(f"Timed out after {TIMEOUT}s waiting to merge relay PR\n")
    return 4


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
