#!/usr/bin/env python3
"""relay_notify.py — minimal Telegram relay notifications.

Notifications ONLY. By design this script cannot transmit task content, code,
repository data, file paths, diffs, or any free-form text. It can send exactly
one of five fixed event labels:

    started      -> "Task started"
    complete     -> "Task complete"
    approval     -> "Human approval required"
    verified     -> "VERIFIED"
    not-verified -> "NOT VERIFIED"

There is intentionally no argument for a custom message. The only input accepted
is the event key, which is validated against the allow-list below.

Configuration (read from the environment; never hard-coded, never logged):

    TELEGRAM_BOT_TOKEN   Bot token from BotFather.
    TELEGRAM_CHAT_ID     Destination chat id.

Usage:
    python scripts/relay_notify.py started
    python scripts/relay_notify.py verified
    python scripts/relay_notify.py approval --dry-run

Exit codes:
    0  notification sent (or printed in --dry-run)
    2  invalid usage / unknown event
    3  missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID
    4  delivery failure
"""

import json
import os
import sys
import urllib.error
import urllib.request

# Fixed allow-list. The VALUE is the entire message body that can ever be sent.
# Keep this dict the single source of truth: nothing else is transmittable.
ALLOWED_EVENTS = {
    "started": "Task started",
    "complete": "Task complete",
    "approval": "Human approval required",
    "verified": "VERIFIED",
    "not-verified": "NOT VERIFIED",
    "low-balance": "Low balance \u2014 top up before this task runs",
}

# Optional, purely decorative prefixes. They contain no task data.
EVENT_PREFIX = {
    "started": "\u25B6\uFE0F",
    "complete": "\u2705",
    "approval": "\u26A0\uFE0F",
    "verified": "\u2705",
    "not-verified": "\u274C",
    "low-balance": "\U0001F4B3",
}

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
TIMEOUT_SECONDS = 10


def usage(stream=sys.stderr):
    keys = " | ".join(ALLOWED_EVENTS.keys())
    stream.write(
        "Usage: relay_notify.py <event> [--dry-run]\n"
        f"  event: {keys}\n"
    )


def build_message(event_key):
    """Return the exact, fixed text for an allowed event. No other text exists."""
    prefix = EVENT_PREFIX.get(event_key, "")
    body = ALLOWED_EVENTS[event_key]
    return (prefix + " " + body).strip()


def send(token, chat_id, text):
    payload = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        TELEGRAM_API.format(token=token),
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        raw = resp.read().decode("utf-8", "replace")
    parsed = json.loads(raw)
    if not parsed.get("ok"):
        raise RuntimeError("telegram_api_not_ok:" + str(parsed.get("error_code", "unknown")))


def main(argv):
    args = [a for a in argv[1:]]
    dry_run = False
    if "--dry-run" in args:
        dry_run = True
        args.remove("--dry-run")

    if len(args) != 1:
        usage()
        return 2

    event_key = args[0].strip().lower()
    if event_key not in ALLOWED_EVENTS:
        sys.stderr.write(f"Unknown event: {event_key!r}\n")
        usage()
        return 2

    text = build_message(event_key)

    if dry_run:
        sys.stdout.write(text + "\n")
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        sys.stderr.write(
            "Missing TELEGRAM_BOT_TOKEN and/or TELEGRAM_CHAT_ID in environment.\n"
        )
        return 3

    try:
        send(token, chat_id, text)
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, ValueError) as exc:
        sys.stderr.write("Notification delivery failed: " + str(exc) + "\n")
        return 4

    sys.stdout.write("sent: " + event_key + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
