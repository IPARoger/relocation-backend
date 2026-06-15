#!/usr/bin/env python3
"""relay_preflight.py — cheap "can we afford this run?" check.

Runs BEFORE the expensive Cursor cloud execution. It makes one minimal OpenAI
probe (max_tokens=1, a fraction of a cent) to detect an empty/again-billable
balance. If funds are exhausted it reports LOW so the workflow can send a
Telegram low-balance warning and STOP — avoiding a wasted, hard-to-resume run
and a possible double charge.

Why only OpenAI is probed: OpenAI returns a clear `insufficient_quota` signal.
Cursor has no public balance endpoint, so the executor instead catches Cursor
billing/auth failures at launch (before the agent does real work) and the
workflow warns then too.

Environment:
  OPENAI_API_KEY   Required for a live check.
  OPENAI_MODEL     Optional; defaults to a small/cheap model.

Usage:
  python scripts/relay_preflight.py --dry-run   # no API call
  python scripts/relay_preflight.py             # live: one tiny probe

Exit codes / stdout:
  0  prints "OK"   — balance looks fine, safe to proceed
  5  prints "LOW"  — insufficient quota; warn human and stop
  3  missing OPENAI_API_KEY
  4  other error (network/auth) — does not necessarily mean low balance
"""

import json
import os
import sys
import urllib.error
import urllib.request

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-5-mini"
TIMEOUT_SECONDS = 30


def probe(api_key, model):
    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 1,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        OPENAI_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS).read()


def main(argv):
    args = argv[1:]
    if "--dry-run" in args:
        sys.stdout.write("OK (dry-run: no probe made)\n")
        return 0

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        sys.stderr.write("Missing OPENAI_API_KEY in environment.\n")
        return 3

    model = os.environ.get("OPENAI_MODEL", "").strip() or DEFAULT_MODEL
    try:
        probe(api_key, model)
        sys.stdout.write("OK\n")
        return 0
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        # 429 + insufficient_quota is OpenAI's "out of credit" signal.
        if e.code == 429 and "insufficient_quota" in body:
            sys.stdout.write("LOW\n")
            return 5
        sys.stderr.write(f"OpenAI probe HTTP {e.code}: {body[:200]}\n")
        return 4
    except Exception as e:
        sys.stderr.write("OpenAI probe failed: " + str(e) + "\n")
        return 4


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
