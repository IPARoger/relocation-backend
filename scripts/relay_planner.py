#!/usr/bin/env python3
"""relay_planner.py — the "GPT brain" of the two-agent relay.

Reads the most recent results/ closeout and the relay rules, then asks an
OpenAI model to do ONE of two things:

  1. Author the next single-objective task into tasks/<NN>_<slug>.md, or
  2. PAUSE and hand control to the human (when judgement / approval is needed).

Design constraints (kept deliberately small and cheap):
  - Standard library only (urllib); no pip install required in CI.
  - Lean context: only the latest results file + a short rules digest are sent,
    which is what keeps the per-run cost in the cents range.
  - The model is told to obey tasks/TEMPLATE.md and the relay hard-stops.
  - It can never merge, push to main, or touch secrets/schema/backend — it only
    proposes a task file for a human-gated PR.

Environment:
  OPENAI_API_KEY   Required for a live run.
  OPENAI_MODEL     Optional; defaults to a small/cheap model. Set to whatever
                   cheap model your account has access to.

Usage:
  python scripts/relay_planner.py --dry-run     # prints intended action, no API
  python scripts/relay_planner.py               # live: calls OpenAI, writes file

Exit codes:
  0  planned a task (path printed) OR paused (reason printed) OR nothing to do
  2  invalid usage
  3  missing OPENAI_API_KEY on a live run
  4  OpenAI call / parse failure
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TASKS_DIR = REPO / "tasks"
RESULTS_DIR = REPO / "results"
GOVERNANCE = REPO / "docs" / "architecture" / "TWO_AGENT_RELAY_GOVERNANCE.md"
TEMPLATE = TASKS_DIR / "TEMPLATE.md"

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-5-mini"
TIMEOUT_SECONDS = 60

SYSTEM_PROMPT = """You are the planning half ("ChatGPT lane") of a governed two-agent
relay for a relocation-astrology research tool. Your ONLY job is to propose the
next single task for the executing agent (Cursor), OR to pause for the human.

Hard rules you must obey:
- Exactly ONE objective per task. Never bundle.
- The task must declare: objective, scope, files to read, files expected to
  change, required behavior, hard stops, validation plan, rollback plan, and the
  closeout contract. Follow the provided TEMPLATE structure.
- The relay default is read-only/diagnosis unless a task explicitly authorizes a
  change, and even then it is small and reversible.
- These are HARD STOPS you must never request: schema change, backend change,
  database write, credentials/secrets, migration, renderer/math/overlay changes.
  If the next sensible step needs any of these, PAUSE for the human instead.
- You never merge, never push to main, never touch secrets. A human merges.

Output format (STRICT):
- If a safe next task exists, output ONLY:
    SLUG: <kebab-case-short-slug>
    ---
    <full task markdown following the template>
- If the right move is to stop and let the human decide/approve/QA, output ONLY:
    PAUSE: <one short sentence on why a human is needed>
No other text, no code fences."""


def read_text(p, limit=20000):
    try:
        return p.read_text(encoding="utf-8")[:limit]
    except Exception:
        return ""


def latest_numbered(d):
    """Return (max_NN, latest_file_text) for NN_*.md files in a folder."""
    best_n, best_file = 0, None
    for f in sorted(d.glob("[0-9][0-9]_*.md")):
        m = re.match(r"(\d+)_", f.name)
        if not m:
            continue
        n = int(m.group(1))
        if n >= best_n:
            best_n, best_file = n, f
    return best_n, (read_text(best_file) if best_file else "")


def build_user_prompt():
    last_results_n, last_results = latest_numbered(RESULTS_DIR)
    last_tasks_n, _ = latest_numbered(TASKS_DIR)
    next_n = max(last_results_n, last_tasks_n) + 1
    existing = sorted(
        [f.name for f in TASKS_DIR.glob("[0-9][0-9]_*.md")]
        + [f.name for f in RESULTS_DIR.glob("[0-9][0-9]_*.md")]
    )
    parts = [
        f"Next task number to use: {next_n:02d}",
        "",
        "=== RELAY GOVERNANCE (digest) ===",
        read_text(GOVERNANCE, limit=8000),
        "",
        "=== TASK TEMPLATE (follow this structure) ===",
        read_text(TEMPLATE, limit=4000),
        "",
        "=== MOST RECENT RESULT (what just finished) ===",
        last_results or "(no results yet)",
        "",
        "=== EXISTING TASK/RESULT FILES ===",
        "\n".join(existing) or "(none)",
        "",
        "Propose the next single safe task, or PAUSE for the human.",
    ]
    return next_n, "\n".join(parts)


def call_openai(api_key, model, system, user):
    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
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
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        parsed = json.loads(resp.read().decode("utf-8", "replace"))
    return parsed["choices"][0]["message"]["content"].strip()


def write_task(next_n, slug, body):
    slug = re.sub(r"[^a-z0-9-]", "", slug.lower().replace(" ", "-")) or "task"
    path = TASKS_DIR / f"{next_n:02d}_{slug}.md"
    path.write_text(body.rstrip() + "\n", encoding="utf-8")
    return path


def main(argv):
    args = argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    if args:
        sys.stderr.write("Usage: relay_planner.py [--dry-run]\n")
        return 2

    next_n, user_prompt = build_user_prompt()
    model = os.environ.get("OPENAI_MODEL", "").strip() or DEFAULT_MODEL

    if dry_run:
        sys.stdout.write(
            f"DRY-RUN: would ask {model} to plan task {next_n:02d} "
            f"({len(user_prompt)} chars of context, no API call made).\n"
        )
        return 0

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        sys.stderr.write("Missing OPENAI_API_KEY in environment.\n")
        return 3

    try:
        out = call_openai(api_key, model, SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        sys.stderr.write("OpenAI call failed: " + str(e) + "\n")
        return 4

    if out.startswith("PAUSE:"):
        sys.stdout.write(out.strip() + "\n")
        return 0

    if out.startswith("SLUG:"):
        first, _, rest = out.partition("\n")
        slug = first[len("SLUG:"):].strip()
        body = rest.split("---", 1)[1].strip() if "---" in rest else rest.strip()
        path = write_task(next_n, slug, body)
        sys.stdout.write("PLANNED " + str(path.relative_to(REPO)) + "\n")
        return 0

    sys.stderr.write("Unexpected planner output; not writing a task.\n")
    return 4


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
