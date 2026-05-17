#!/usr/bin/env python3
"""Generate a local AI review from Cursor's latest project report."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AI_CONTEXT_DIR = REPO_ROOT / "ai_context"
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.5")


def read_context_file(name: str) -> str:
    path = AI_CONTEXT_DIR / name
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"# {name}\n\nMissing file: {path}\n"


def run_git(args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except OSError as exc:
        return f"Unable to run git {' '.join(args)}: {exc}"

    output = result.stdout.strip()
    return output or "(no output)"


def build_prompt() -> str:
    context_files = {
        "product_brief.md": read_context_file("product_brief.md"),
        "current_state.md": read_context_file("current_state.md"),
        "decisions.md": read_context_file("decisions.md"),
        "open_questions.md": read_context_file("open_questions.md"),
        "cursor_latest_report.md": read_context_file("cursor_latest_report.md"),
    }

    git_context = {
        "git status --short": run_git(["status", "--short"]),
        "git diff --stat": run_git(["diff", "--stat"]),
        "git diff --summary": run_git(["diff", "--summary"]),
    }

    sections = [
        "# Local Project Context",
        "You are reviewing a Cursor task report for a relocation astrology mapping app.",
        "Use the product brief, current state, decisions, open questions, and git context.",
        "Avoid inventing facts not supported by the provided context.",
        "Focus on review quality, risks, QA instructions, and the next Cursor prompt.",
        "",
        "Return ONLY valid JSON with exactly these keys:",
        "- review_latest_markdown",
        "- next_cursor_prompt_markdown",
        "",
        "The review markdown must include:",
        "1. Executive summary",
        "2. What changed",
        "3. What matters",
        "4. Risks/regressions",
        "5. What the human should manually QA",
        "6. Whether the result matches product philosophy",
        "7. Recommended next Cursor prompt",
        "",
    ]

    for name, content in context_files.items():
        sections.extend([f"## {name}", content.strip(), ""])

    sections.append("## Git Context")
    for command, output in git_context.items():
        sections.extend([f"### {command}", "```", output, "```", ""])

    return "\n".join(sections)


def extract_response_text(response: object) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text

    # Conservative fallback for SDK/object shape changes.
    try:
        return response.output[0].content[0].text  # type: ignore[attr-defined]
    except Exception:
        return str(response)


def parse_review_payload(text: str) -> tuple[str, str]:
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").removesuffix("```").strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```").removesuffix("```").strip()

    try:
        data = json.loads(cleaned)
        review = data["review_latest_markdown"].strip()
        next_prompt = data["next_cursor_prompt_markdown"].strip()
        return review, next_prompt
    except Exception:
        fallback_review = (
            "# Review Latest\n\n"
            "The reviewer response was not valid JSON, so the raw response is preserved below.\n\n"
            "```text\n"
            f"{text.strip()}\n"
            "```\n"
        )
        fallback_prompt = (
            "# Next Cursor Prompt\n\n"
            "The reviewer did not return a parseable next prompt. Read `review_latest.md` and draft the next Cursor prompt manually.\n"
        )
        return fallback_review, fallback_prompt


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "OPENAI_API_KEY is not set.\n\n"
            "To run the local AI reviewer, set it first:\n\n"
            '  export OPENAI_API_KEY="your_api_key_here"\n'
            "  python scripts/ai_review_cursor_report.py\n\n"
            "No files were changed by this run."
        )
        return 2

    try:
        from openai import OpenAI
    except ImportError:
        print(
            "The OpenAI Python SDK is not installed.\n\n"
            "Install it with:\n\n"
            "  pip install -r requirements-ai-reviewer.txt\n"
        )
        return 2

    client = OpenAI()
    prompt = build_prompt()

    try:
        response = client.responses.create(
            model=MODEL,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful senior product-engineering reviewer. "
                        "Return concise, practical markdown inside the requested JSON fields."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
    except Exception as exc:
        print(
            f"OpenAI review failed while using model {MODEL!r}.\n\n"
            f"{exc}\n\n"
            "If this model is unavailable for your account, set OPENAI_MODEL to an available model and retry."
        )
        return 1

    review_markdown, next_prompt_markdown = parse_review_payload(extract_response_text(response))

    (AI_CONTEXT_DIR / "review_latest.md").write_text(review_markdown + "\n", encoding="utf-8")
    (AI_CONTEXT_DIR / "next_cursor_prompt.md").write_text(next_prompt_markdown + "\n", encoding="utf-8")

    print("Wrote ai_context/review_latest.md")
    print("Wrote ai_context/next_cursor_prompt.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
