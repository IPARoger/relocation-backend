# AI Context Reviewer

This folder is a local project-memory and review handoff area. It is not connected to production app behavior.

## Files

- `product_brief.md`: durable product and UX philosophy for the relocation astrology app.
- `current_state.md`: current milestone, known working behavior, and immediate caveats.
- `decisions.md`: architectural and product decisions that future reviewers should preserve.
- `open_questions.md`: unresolved questions and areas needing human judgment.
- `cursor_latest_report.md`: latest structured report written by Cursor after a task.
- `review_latest.md`: latest OpenAI reviewer output.
- `next_cursor_prompt.md`: suggested next prompt for Cursor, generated from the review.

Private notes, secrets, and scratch material should go in `ai_context/private/` or `*.local.md` files. Those are ignored by git.

## Workflow

1. Cursor writes `cursor_latest_report.md` after a task.
2. The reviewer script gathers repo context, including git status and diff stats.
3. The OpenAI API generates `review_latest.md` and `next_cursor_prompt.md`.
4. The user reads and approves the result before continuing.

## Usage

```bash
export OPENAI_API_KEY="..."
python scripts/ai_review_cursor_report.py
```

Optional model override:

```bash
OPENAI_MODEL="gpt-5.5" python scripts/ai_review_cursor_report.py
```

Never commit API keys. Keep sensitive or private notes in `ai_context/private/`. The user remains the final approver for any generated review, plan, or next Cursor prompt.
