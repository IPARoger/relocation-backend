# results/ — Cursor lane (closeout reports)

**Owner (single writer):** Cursor.
**ChatGPT must not author files here.** ChatGPT only *reads* results from this
folder (e.g. via the GitHub connector) to plan the next task.

## Purpose

This folder is the outbound mailbox. After Cursor executes a task from `tasks/`,
it writes one closeout report per task here. A human reviews and pushes; ChatGPT
then reads the result from GitHub without anyone pasting it back. This removes
the copy/paste of Cursor output into ChatGPT.

See `docs/architecture/TWO_AGENT_RELAY_GOVERNANCE.md` for the binding rules.

## Contract

- One result file per task, named to match its task:
  `results/<NN>_<short-slug>.md` (same id/slug as the originating task).
- Every result must end with `VERIFIED` or `NOT VERIFIED`, based only on
  evidence. Never infer success.
- Use `results/TEMPLATE.md` as the starting point.

## Lane rules (summary)

- Cursor authors `results/`. ChatGPT authors `tasks/`.
- Neither agent edits the other's lane.
- No agent edits `doctrine/` without explicit human authorization.
- Only a human merges to the main/core branch.
