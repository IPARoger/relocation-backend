#!/usr/bin/env python3
"""Track relay task completions and trigger periodic layman digests."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROGRESS = REPO / "relay" / "progress.json"
DEFAULT_INTERVAL = 15


def load_progress() -> dict:
    if PROGRESS.is_file():
        return json.loads(PROGRESS.read_text(encoding="utf-8"))
    return {
        "completed_since_digest": 0,
        "last_digest_through_task": 0,
        "digest_interval": DEFAULT_INTERVAL,
    }


def save_progress(data: dict) -> None:
    PROGRESS.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def latest_result_number() -> int:
    best = 0
    for f in (REPO / "results").glob("[0-9][0-9]_*.md"):
        m = re.match(r"(\d+)_", f.name)
        if m:
            best = max(best, int(m.group(1)))
    return best


def interval() -> int:
    env = os.environ.get("RELAY_DIGEST_INTERVAL", "").strip()
    if env.isdigit():
        return int(env)
    return int(load_progress().get("digest_interval") or DEFAULT_INTERVAL)


def record_closeout() -> int:
    data = load_progress()
    data["completed_since_digest"] = int(data.get("completed_since_digest", 0)) + 1
    data["last_completed_task"] = latest_result_number()
    save_progress(data)
    count = data["completed_since_digest"]
    print(f"RECORDED completed_since_digest={count}")
    return count


def send_digest_if_due() -> int:
    data = load_progress()
    n = int(data.get("completed_since_digest", 0))
    every = interval()
    if n < every:
        print(f"DIGEST_SKIP ({n}/{every})")
        return 0

    sys.path.insert(0, str(REPO / "scripts"))
    from relay_digest import build_layman_digest

    through = latest_result_number()
    since = int(data.get("last_digest_through_task", 0))
    text = build_layman_digest(since_task=since, through_task=through, count=n)

    notified = False
    try:
        from relay_notify import env_credentials, send_with_retries

        token, chat_id = env_credentials()
        if token and chat_id is not None:
            send_with_retries(token, chat_id, text[:4000])
            print("DIGEST_SENT telegram")
            notified = True
    except Exception as exc:
        print(f"telegram digest failed: {exc}", file=sys.stderr)

    try:
        from relay_notify_email import credentials, send_email

        creds = credentials()
        if creds:
            send_email(
                "[Relay] 15-task summary",
                text,
                creds[2],
                creds[0],
                creds[1],
            )
            print("DIGEST_SENT email")
            notified = True
    except Exception as exc:
        print(f"email digest failed: {exc}", file=sys.stderr)

    if not notified:
        print(text)
        print("DIGEST_PRINTED (no notify credentials)", file=sys.stderr)
        return 4

    data["completed_since_digest"] = 0
    data["last_digest_through_task"] = through
    data["awaiting_digest_ack"] = True
    save_progress(data)
    print(f"DIGEST_DONE through_task={through}")
    return 0


def clear_digest_ack() -> None:
    data = load_progress()
    data["awaiting_digest_ack"] = False
    save_progress(data)
    print("DIGEST_ACK_CLEARED")


def is_awaiting_ack() -> bool:
    return bool(load_progress().get("awaiting_digest_ack"))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        sys.stderr.write(
            "Usage: relay_progress.py record-closeout|send-digest-if-due|clear-ack|status\n"
        )
        return 2
    cmd = argv[1]
    if cmd == "record-closeout":
        record_closeout()
        return 0
    if cmd == "send-digest-if-due":
        return send_digest_if_due()
    if cmd == "clear-ack":
        clear_digest_ack()
        return 0
    if cmd == "status":
        print(json.dumps(load_progress(), indent=2))
        return 0
    sys.stderr.write(f"Unknown command: {cmd}\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
