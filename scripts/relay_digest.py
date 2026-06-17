#!/usr/bin/env python3
"""Build a layman-terms summary of recent relay task closeouts."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"


def numbered_results(since_task: int, through_task: int) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for f in sorted(RESULTS.glob("[0-9][0-9]_*.md")):
        m = re.match(r"(\d+)_", f.name)
        if not m:
            continue
        n = int(m.group(1))
        if since_task < n <= through_task:
            rows.append((n, f.read_text(encoding="utf-8")[:2500]))
    return rows


def fallback_summary(rows: list[tuple[int, str]], count: int) -> str:
    lines = [
        f"Relay check-in ({count} tasks since last summary)",
        "",
        "Plain English:",
    ]
    for n, body in rows[-8:]:
        title = body.split("\n", 1)[0].strip("# ").strip()
        verified = "VERIFIED" in body.upper()
        lines.append(f"  • Task {n}: {title[:60]} — {'done' if verified else 'partial/needs follow-up'}")
    lines.extend(
        [
            "",
            "The loop keeps running automatically.",
            "Reply OK here (or run Actions → two-agent-relay → Continue after digest) if you want to acknowledge.",
        ]
    )
    return "\n".join(lines)


def build_layman_digest(since_task: int, through_task: int, count: int) -> str:
    rows = numbered_results(since_task, through_task)
    if not rows:
        return (
            f"Relay check-in ({count} tasks completed).\n\n"
            "No new closeout files found to summarize yet. Loop is still running."
        )

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return fallback_summary(rows, count)

    blob = "\n\n---\n\n".join(f"TASK {n}:\n{text}" for n, text in rows)
    prompt = (
        f"Summarize these {len(rows)} software relay task closeouts for a non-technical product owner. "
        "Use 6-10 short sentences, plain English, no jargon. Say what changed in the app/product, "
        "what is working, what is still shaky, and whether they need to do anything (usually no). "
        "End with one line: 'Reply OK to acknowledge; relay continues automatically unless you pause it.'\n\n"
        + blob[:12000]
    )
    payload = json.dumps(
        {
            "model": os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
            "messages": [
                {"role": "system", "content": "You write clear, brief status updates."},
                {"role": "user", "content": prompt},
            ],
        }
    ).encode()
    req = urllib.request.Request(
        OPENAI_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            parsed = json.loads(resp.read().decode())
        text = parsed["choices"][0]["message"]["content"].strip()
        return f"Relay check-in ({count} tasks)\n\n{text}"
    except (urllib.error.URLError, KeyError, json.JSONDecodeError):
        return fallback_summary(rows, count)
