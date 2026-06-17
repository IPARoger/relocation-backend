#!/usr/bin/env python3
"""relay_notify.py — minimal Telegram relay notifications."""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

ALLOWED_EVENTS = {
    "started": "Task started",
    "complete": "Task complete",
    "approval": "Human approval required",
    "verified": "VERIFIED",
    "not-verified": "NOT VERIFIED",
    "low-balance": "Low balance \u2014 top up before this task runs",
}

EVENT_PREFIX = {
    "started": "\u25B6\uFE0F",
    "complete": "\u2705",
    "approval": "\u26A0\uFE0F",
    "verified": "\u2705",
    "not-verified": "\u274C",
    "low-balance": "\U0001F4B3",
}

TIMEOUT_SECONDS = 30
MAX_RETRIES = 3


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="relay_notify.py")
    parser.add_argument("event", choices=ALLOWED_EVENTS.keys(), nargs="?")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--task", default=None)
    parser.add_argument("--message", default=None)
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Validate token + chat_id via getMe/getChat; send a test ping.",
    )
    return parser.parse_args(argv[1:])


def env_credentials():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip().strip('"').strip("'")
    chat_raw = os.environ.get("TELEGRAM_CHAT_ID", "").strip().strip('"').strip("'")
    if not token or not chat_raw:
        return None, None
    if chat_raw.lstrip("-").isdigit():
        chat_id = int(chat_raw)
    else:
        chat_id = chat_raw
    return token, chat_id


def build_message(event_key, task=None, extra_message=None):
    prefix = EVENT_PREFIX.get(event_key, "")
    body = ALLOWED_EVENTS[event_key]
    text = (prefix + " " + body).strip()
    if task:
        text += f"\nTask: {task}"
    if extra_message:
        text += f"\n{extra_message}"
    return text


def telegram_request(token, method, payload=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            raise RuntimeError(f"telegram_http_{exc.code}: {raw[:200]}") from exc
        desc = parsed.get("description", raw[:200])
        raise RuntimeError(
            f"telegram_http_{exc.code}: {desc} (error_code={parsed.get('error_code')})"
        ) from exc
    parsed = json.loads(raw)
    if not parsed.get("ok"):
        desc = parsed.get("description", "unknown")
        raise RuntimeError(
            f"telegram_api_not_ok: {desc} (error_code={parsed.get('error_code')})"
        )
    return parsed


def send_with_retries(token, chat_id, text):
    payload = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            telegram_request(token, "sendMessage", payload)
            return
        except (urllib.error.URLError, RuntimeError, ValueError) as exc:
            last_err = exc
            msg = str(exc).lower()
            retryable = any(
                k in msg
                for k in ("timeout", "timed out", "connection reset", "temporarily")
            )
            if attempt < MAX_RETRIES and retryable:
                time.sleep(2 * attempt)
                continue
            raise last_err from exc


def verify_credentials(token, chat_id):
    me = telegram_request(token, "getMe")
    username = me.get("result", {}).get("username", "?")
    sys.stdout.write(f"getMe ok: @{username}\n")
    try:
        chat = telegram_request(token, "getChat", {"chat_id": chat_id})
        title = chat.get("result", {}).get("title") or chat.get("result", {}).get(
            "first_name", "?"
        )
        sys.stdout.write(f"getChat ok: {title}\n")
    except RuntimeError as exc:
        sys.stderr.write("getChat warning: " + str(exc) + "\n")
    send_with_retries(token, chat_id, "\u2705 Relay Telegram test ping")


def main(argv):
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)

    if args.verify:
        token, chat_id = env_credentials()
        if not token or chat_id is None:
            sys.stderr.write("Missing TELEGRAM_BOT_TOKEN and/or TELEGRAM_CHAT_ID.\n")
            return 3
        try:
            verify_credentials(token, chat_id)
        except (urllib.error.URLError, RuntimeError, ValueError) as exc:
            sys.stderr.write("Telegram verify failed: " + str(exc) + "\n")
            return 4
        sys.stdout.write("verify: ok\n")
        return 0

    if not args.event:
        sys.stderr.write("Usage: relay_notify.py <event> | --verify\n")
        return 2

    text = build_message(args.event, args.task, args.message)
    if args.dry_run:
        sys.stdout.write(text + "\n")
        return 0

    token, chat_id = env_credentials()
    if not token or chat_id is None:
        sys.stderr.write("Missing TELEGRAM_BOT_TOKEN and/or TELEGRAM_CHAT_ID.\n")
        return 3

    try:
        send_with_retries(token, chat_id, text)
    except (urllib.error.URLError, RuntimeError, ValueError) as exc:
        sys.stderr.write("Notification delivery failed: " + str(exc) + "\n")
        return 4

    sys.stdout.write("sent: " + args.event + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
