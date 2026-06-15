# TWO-AGENT RELAY GOVERNANCE

**Status:** Binding governance for the ChatGPT <-> Cursor file relay
**Type:** Governance / protocol
**Date:** 2026-06-15
**Phase:** Web2 Workflow QA — relay trial

---

## Purpose

This document is the binding law for a minimal, file-based relay that reduces
copy/paste between ChatGPT and Cursor without giving either agent unsafe
autonomous control. It exists to capture 80–90% of the relay benefit while
preserving the human gate that has kept the project safe.

Architectural reality: **ChatGPT and Cursor are both MCP clients.** Neither
hosts the other. This relay therefore uses shared files in the repo (synced via
Git/GitHub), not agent-to-agent control.

---

## Lanes and ownership (single-writer rule)

- **ChatGPT authors `tasks/`.** Cursor only reads `tasks/`.
- **Cursor authors `results/`.** ChatGPT only reads `results/`.
- **`audits/`** holds read-only inventory outputs; either agent may write an
  audit only when explicitly assigned.
- **`doctrine/`** (and existing `docs/.../*CANON*`, constitutional docs) are
  not edited by any agent without explicit human authorization.
- Neither agent edits the other's lane. No exceptions.

---

## Task discipline

- **No self-selecting the next task.** Observations, recommendations, and audit
  findings are NOT authorization. A task begins only when a human commits it to
  `tasks/`.
- **One objective per task.** No bundling.
- **Scope lock.** Every task must declare: files to read, and files expected to
  change. Work stays inside that declared scope. No "while I'm here" changes.

---

## Hard stops (stop and ask — never proceed)

An executing agent must STOP and report instead of proceeding if a task appears
to require any of:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

Encountering a hard stop is a successful, honest outcome — not a failure.

---

## Data rule (critical)

- The relay branch / sandbox is **read-only / diagnosis-only unless explicitly
  authorized** in the specific task.
- **Sandbox code does not mean sandbox data.** Duplicating the folder or working
  on a branch isolates code, not data.
- **Backup code is not backup data.** A full code backup of the repository does
  NOT make the database safe. The relay may not assume database safety because a
  code backup exists.
- `.env.staging` still points to the **shared staging Supabase database**. Any
  write (favorites, comparison sets, archives, current location, birth records,
  settings, etc.) hits live shared data.
- Therefore: no database writes in the relay unless a task explicitly authorizes
  them and names the exact rows/tables. Default is read-only.

---

## Task escalation rule

If execution reveals a future task or opportunity:

- **Record the observation** (in the result's "Remaining unknowns" or an audit).
- **Do not create a new task.**
- **Do not self-author tasks.**
- Only a **human** or **ChatGPT (into `tasks/`)** may create tasks.

Observations and findings are never authorization. They are inputs the human may
later choose to turn into a task.

---

## Read-only trial rule (Phase 1)

Phase 1 relay operation is **READ ONLY**.

Allowed in Phase 1:

- audits
- doctrine reviews
- ownership inventories
- UX reviews
- navigation reviews
- architecture reviews
- placeholder audits

Not allowed in Phase 1:

- database writes
- inserts
- updates
- deletes
- archive actions
- schema work
- migrations
- backend changes
- renderer changes

Phase 1 ends only when a human explicitly authorizes a different phase.

---

## Human approval gate

Any task involving any of the following must **stop and request human approval**
before proceeding:

- database writes
- Supabase mutations
- schema changes
- backend routes
- credentials
- migrations

Stopping at this gate is the correct, successful behavior — not a failure.

---

## Merge gate

- Agents may write only to the relay branch / sandbox lane.
- **Only a human merges to the main/core branch.** No autonomous commits to
  main. No force-push. No autonomous push to remote without human action.
- The human gate is part of the architecture, not an inefficiency.

---

## Closeout contract

Every executed task must produce a `results/` entry containing:

- files changed
- validation evidence (concrete proof, not assertions)
- rollback command
- rejected scope
- **VERIFIED** or **NOT VERIFIED** (based only on evidence; never inferred)

Every audit must end with `VERIFIED (read-only; no files changed)` or
`NOT VERIFIED`.

---

## Stop conditions for the relay itself

Pause the relay and escalate to the human if:

- an agent edits another agent's lane,
- a task lacks a declared scope or objective,
- a hard-stop condition is hit,
- an audit begins recommending itself into implementation,
- repeated failures or context bloat appear (the rain/virga failure mode:
  agents talking to agents, giant context, autonomous rabbit holes).

---

## Telegram notifications

Cursor may send Telegram notifications through `scripts/relay_notify.py` only.
Setup and configuration are documented in
`docs/architecture/RELAY_TELEGRAM_NOTIFICATIONS.md`.

Notifications are **status pings only**. The only permitted events are:

- `started`
- `complete`
- `approval`
- `verified`
- `not-verified`
- `low-balance` (a fixed-label warning that an account needs topping up before a
  run proceeds; carries no task content)

Strict rules:

- **No arbitrary text.** Only the five fixed event labels above may be sent.
- **No task contents.** Task titles, descriptions, IDs, and instructions are
  never transmitted.
- **No code.** No source, diffs, snippets, or stack traces.
- **No paths** unless that path already exists in `results/` and is being
  referenced as an existing closeout artifact.
- **No repeated notifications for the same state.** Send each state transition at
  most once per task (e.g. one `started`, one `verified`/`not-verified`). Do not
  re-fire the same event on retries or re-runs.
- Notifications are advisory: never block work on delivery, and never treat a
  delivery failure as task failure.
- Notifications do not replace the `results/` closeout or the human approval
  gate. The operator still opens the repo to read actual content.

This rule governs notification behavior only. It authorizes no other outbound
communication channel.

---

## Scope / Constraints

- This document governs process only. It authorizes no code, backend, schema, or
  data changes by itself.
- The relay is a trial; this governance may be tightened by the human at any
  time.

## Acceptance / Next Step

- Relay operates under these rules. Changes to this document require explicit
  human authorization.

---

## Automation phase (assisted relay)

This phase replaces the human as the message *courier* between the two agents
while keeping the human as the *merge gate*. It is opt-in and runs only from a
manually triggered GitHub Action.

Components:

- `scripts/relay_planner.py` — calls a small OpenAI model to author the next
  single task into `tasks/` (the ChatGPT lane), or to PAUSE for the human.
- `scripts/relay_executor.py` — launches a Cursor cloud agent to execute the
  newest task with no `results/` closeout. The agent writes `results/` and opens
  a Pull Request. It never merges.
- `.github/workflows/relay.yml` — orchestrates plan -> execute -> notify. It is
  manual-trigger only and defaults to dry-run (no paid calls, no changes).

Binding rules for the automation phase:

- **The human merge gate is unchanged.** Agents open PRs only. Only a human
  merges to the working branch / main. No auto-merge. No force-push.
- **Single-writer lanes still hold.** The planner only writes `tasks/`; the
  executor (via the cloud agent) only writes `results/` and the PR diff.
- **All hard stops still apply.** The planner is instructed never to request a
  schema/backend/database/secret/migration/renderer change; if such a step is
  needed it must PAUSE for the human.
- **Secrets live only in GitHub Actions secrets**, never in the repo:
  `OPENAI_API_KEY`, `CURSOR_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
  (and optional `OPENAI_MODEL`, `CURSOR_MODEL`).
- **Telegram stays notification-only.** The automation may send the existing
  `approval` ping when a PR is opened or the planner pauses — signalling that a
  human is needed. No task content is ever transmitted.
- **Cost control.** The workflow is dry-run by default and has no schedule
  enabled. Enabling the schedule or live runs is an explicit human action.

Kill switch: disable the `two-agent-relay` workflow in the GitHub Actions tab,
or remove the secrets. Either stops all automated activity immediately.

---

## Cost-reduction practices (binding for the automation phase)

- **Cheap model by default.** The planner uses a small OpenAI model
  (`OPENAI_MODEL`, default a "mini" tier). Do not switch to a large model
  without a stated reason.
- **Lean context.** The planner sends only the latest `results/` file plus a
  short rules digest — never the whole repo. This keeps per-run cost in the
  cents range.
- **Preflight before spend.** A cheap OpenAI probe (`relay_preflight.py`,
  `max_tokens=1`) runs before the expensive Cursor execution. If balance is
  exhausted the run stops and a `low-balance` Telegram warning is sent — so work
  is never half-done and re-charged.
- **Idempotent execution.** The executor skips any task that already has a
  `results/` closeout, so re-running after a top-up never repeats (or re-bills)
  completed work.
- **No schedule by default.** Runs are manual until a human enables the cron.
