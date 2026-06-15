# tasks/ — ChatGPT lane (task specs)

**Owner (single writer):** ChatGPT.
**Cursor must not author files here.** Cursor only *reads* tasks from this folder.

## Purpose

This folder is the inbound mailbox for the two-agent file relay. ChatGPT writes
one task spec per file; a human commits it; Cursor reads it and executes inside
the task's declared scope. This removes the copy/paste of task text into Cursor
while keeping a human merge gate.

See `docs/architecture/TWO_AGENT_RELAY_GOVERNANCE.md` for the binding rules.

## Contract

- One objective per task file. No bundled objectives.
- File naming: `tasks/<NN>_<short-slug>.md` (e.g. `tasks/01_chart-record-empty-states.md`).
- Every task must declare: objective, scope, files to read, files expected to
  change, validation plan, rollback plan.
- A task must list explicit hard-stop conditions (see governance) and instruct
  the executing agent to stop rather than proceed if any are hit.
- Use `tasks/TEMPLATE.md` as the starting point.

## Lane rules (summary)

- ChatGPT authors `tasks/`. Cursor authors `results/`.
- Neither agent edits the other's lane.
- No agent edits `doctrine/` without explicit human authorization.
- No self-selecting the next task — a task begins only when explicitly assigned
  and committed by the human.
