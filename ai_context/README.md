# AI Context Reviewer

This folder is a local project-memory and review handoff area. It is not connected to production app behavior.

## Files

- `product_brief.md`: durable product and UX philosophy for the relocation astrology app.
- `core_product_truths.md`: stable principles that should survive individual tasks and experiments.
- `current_state.md`: current milestone, known working behavior, and immediate caveats.
- `decisions.md`: architectural and product decisions that future reviewers should preserve.
- `open_questions.md`: unresolved questions and areas needing human judgment.
- `memory_workflow.md`: how raw archaeology is mined into durable project memory.
- `cursor_latest_report.md`: latest structured report written by Cursor after a task.
- `review_latest.md`: latest OpenAI reviewer output.
- `next_cursor_prompt.md`: suggested next prompt for Cursor, generated from the review.
- `proposed_updates/`: reviewer-generated suggested replacements for durable memory files. Review manually before copying anything into durable memory.

Private notes, secrets, and scratch material should go in `ai_context/private/` or `*.local.md` files. Those are ignored by git.

Raw archaeology extracts live under `memory_archaeology_raw/pending_imports/`. Cross-chat synthesis notes live under `memory_archaeology_raw/consolidated_notes/`. A bridge summary with explicit status labels is in `docs/institutional_memory_synthesis.md`.

Stabilization and sequencing (onboarding after a break): `docs/project_continuity_workflow.md`, `docs/next_implementation_sequence.md`, `docs/workspace_hygiene_and_cleanup.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/map_and_overlay_design_research.md`, `docs/visual_semantic_style_guide.md`, `docs/brand_and_experience_foundations.md`.

## Workflow

1. Cursor writes `cursor_latest_report.md` after a task.
2. The reviewer script gathers repo context, including git status and diff stats.
3. The OpenAI API generates `review_latest.md`, `next_cursor_prompt.md`, and proposed memory updates under `proposed_updates/`.
4. The user reads and approves the result before continuing.
5. Durable memory files are updated only after human review.

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
