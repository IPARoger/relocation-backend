# RELAY OPERATING GUIDE

**Status:** Operating guide for the Claude ↔ Cursor file relay (**Phase 2**)
**Type:** Process guide
**Date:** 2026-06-17 (Phase 2); 2026-06-15 (Phase 1)

Binding rules live in `TWO_AGENT_RELAY_GOVERNANCE.md`. This guide is the concise
how-to. If the two ever conflict, governance wins — except where Phase 2 is
explicitly authorized below and in governance.

---

## Purpose

Run the relay **without the human as message courier**. Claude plans and commits
tasks to GitHub; Cursor executes and commits results; routine git (commit/push)
happens inside authorized tasks. The human is pulled in only for product, risk,
and judgment calls — ideally via Telegram, then laptop when needed.

**Modular-by-default:** prefer flags, env vars, relative URLs, and extension
points over hardcoding. Leave room for future features; do not paint into corners.

---

## Phase 2 workflow (current)

1. **Claude** reads latest `results/` from **GitHub** (not pasted by human).
2. **Claude** authors the next task → `tasks/<NN>_<slug>.md` and commits/pushes
   to the repo. Human does **not** ferry task text.
3. **Cursor** picks up the task (human may say “execute task N” in Cursor, or
   Cursor reads `tasks/` directly). Executes inside declared scope.
4. **Cursor** writes closeout → `results/<NN>_<slug>.md`.
5. If the task authorizes it: **Cursor** commits and pushes source changes.
   Otherwise: stop after closeout for human review.
6. **Claude** reads the new `results/` from GitHub and drafts the next task.
   Loop continues.

**No copy/paste relay.** GitHub is the bus. Telegram is the escalation channel.

---

## Lane ownership

- **Claude** authors `tasks/`. Cursor only reads `tasks/`.
- **Cursor** authors `results/`. Claude only reads `results/`.
- Either agent may author `audits/` only when explicitly assigned.
- No agent edits the other's lane.
- No agent edits `doctrine/` or constitutional docs without explicit human
  authorization.

---

## Human checkpoints (Phase 2)

| Gate | Who | When |
|------|-----|------|
| **Product / CEO** | Human | UX, flows, feature retire/keep, user-facing promises, scope tradeoffs |
| **CFO / risk** | Human | Prod cutover, billing, schema/RLS, irreversible deletes, new paid APIs |
| **Routine execution** | Cursor | Audits, scoped fixes, smoke alignment, docs — when task says so |
| **Routine git** | Cursor | Commit + push when task explicitly authorizes (e.g. `41b_*` commit tasks) |

**Default when unsure:** ask the human (Telegram first). Do not guess on product
or risk.

Phase 1 required human commit of every task and human push of every result.
Phase 2 relaxes that for **authorized, scoped tasks** only. Tasks that touch
hard stops still stop and wait.

---

## Telegram contact (async human gate)

The relay Telegram group is already set up. Use it so the human can step away
from the laptop and respond on phone.

### Fixed pings (`scripts/relay_notify.py`)

Lifecycle only — no task content in the message body:

| Event | Use |
|-------|-----|
| `started` | Cursor picked up a task |
| `verified` / `not-verified` | Closeout ready |
| `approval` | Human attention needed — see `results/` |
| `complete` | Push/merge done for this task cycle |

### Question conventions (human-readable)

When agents need a decision, ping `approval` **and** record the full question
in `results/` (or task PAUSE note). In the group, use these **labels** so the
human knows what to open:

| Label | Emoji | Meaning |
|-------|-------|---------|
| **Check Cursor** | 🔵 | Implementation / repo question — open `tasks/` or `results/` on laptop |
| **Check App** | 🟠 | Product / UX / “what should users see?” decision |
| **Check Risk** | 🔴 | Schema, prod, credentials, or irreversible action |

Agents: **when unsure, default to Check Cursor + `approval` ping** and stop work
until answered. Never block on Telegram delivery failure — the `results/` file
is the source of truth.

Full setup: `docs/architecture/RELAY_TELEGRAM_NOTIFICATIONS.md`.

---

## What runs without human ferrying

- Read-only audits and inventories
- Port/env/smoke normalization inside scope
- Frontend constants → relative URLs / shared `API_BASE`
- Commits and pushes when the task authorizes them and validation passes
- Sequential task drafting by Claude after reading `results/` on GitHub

## What still stops for human

- Schema, migrations, RLS, production Supabase cutover
- Backend route changes (unless task explicitly authorizes)
- Database writes outside named test scope
- Retiring user-visible features (library, legacy paths, dual services)
- Renderer / math / overlay logic changes
- Credentials and secrets in repo
- Anything the task marks as product or CFO gate

---

## Escalation procedure

- If execution reveals future work: record in `results/` (“Remaining unknowns”).
  **Claude** may draft the follow-up task into `tasks/` after reading GitHub —
  no need for human to paste observations.
- If a task hits a hard stop: stop, write `NOT VERIFIED` or partial closeout,
  send `approval` + **Check Cursor** / **Check App** / **Check Risk** as
  appropriate, and wait.
- Observations in an audit are not authorization to implement — the next task
  must still declare scope.

---

## Hard stops

Stop and ask — never proceed — if a task appears to require:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

Encountering a hard stop is a successful, honest outcome.

---

## Modular build principles (binding for Phase 2)

- **Same-origin APIs:** empty `API_BASE`, relative fetch paths — no port lock-in.
- **Feature flags:** off by default (`RM_PHASE2_LIBRARY=0`); opt-in smokes.
- **Backend owns writes:** JWT routes; legacy paths return 410, not silent drift.
- **Extension before deletion:** audit → flag → migrate → retire.
- **Env over hardcode:** `PORT`, `BASE_URL` in `.env.example` / smokes, not
  scattered literals.

---

## VERIFIED / NOT VERIFIED expectations

- Every result ends with `VERIFIED` or `NOT VERIFIED`, based only on evidence.
- Every audit ends with `VERIFIED (read-only; no files changed)` or
  `NOT VERIFIED`.
- Never infer success. Prove it with concrete evidence (grep, smoke exit code,
  diff stat).

---

## Phase 1 (superseded except audits)

Phase 1 was read-only trial + human on every commit/push. Archived for reference:

- Human committed every inbound task and pushed every outbound result.
- No autonomous merges.

Phase 2 began **2026-06-17** with explicit human authorization (port
normalization checkpoint `e6a1948` and relay mode change). Phase 1 rules apply
only when a task explicitly says “Phase 1 read-only.”
