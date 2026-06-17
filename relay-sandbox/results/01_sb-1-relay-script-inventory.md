# RESULT: 01_sb-1-relay-script-inventory

**Roadmap ID:** SB-1
**Author:** Cursor (execution half)
**Date:** 2026-06-17

## Objective

List every `scripts/relay_*.py` with one-line purpose (headers only; read-only).

## Inventory

| Script | One-line purpose |
|--------|------------------|
| `scripts/relay_auto_merge.py` | Wait for a relay cloud-agent PR and squash-merge it to main (optional automation). |
| `scripts/relay_clipboard.py` | Dead-simple relay helper — automates the GPT paste step only (read closeout, plan task, copy prompt to clipboard). |
| `scripts/relay_context.py` | Assemble discipline + closeout context for relay planning (the Claude brain step). |
| `scripts/relay_digest.py` | Build a layman-terms summary of recent relay task closeouts. |
| `scripts/relay_executor.py` | Run the Cursor (execution) half of the relay — find the newest unclosed task and launch a Cursor cloud agent. |
| `scripts/relay_local_loop.py` | Fast sequential relay on your Mac (plan → local Cursor SDK execute → commit, repeat). |
| `scripts/relay_notify.py` | Minimal Telegram relay notifications (fixed event labels only). |
| `scripts/relay_notify_email.py` | Relay pings via Gmail SMTP (stdlib only). |
| `scripts/relay_paths.py` | Relay path resolution — supports sandbox via `RELAY_HOME` env. |
| `scripts/relay_planner.py` | The "GPT brain" of the two-agent relay — author the next task or PAUSE from latest closeout + rules. |
| `scripts/relay_preflight.py` | Cheap "can we afford this run?" check before expensive Cursor cloud execution. |
| `scripts/relay_progress.py` | Track relay task completions and trigger periodic layman digests. |
| `scripts/relay_robot.py` | Robot in the middle — automate closeout → chat brain → task → Cursor executes with logged handoffs. |

**Count:** 13 scripts under `scripts/relay_*.py`.

## Files changed

- `relay-sandbox/results/01_sb-1-relay-script-inventory.md` (this closeout only)
- No changes to `scripts/relay_*.py` or any other source files.

## Validation evidence

```text
$ ls scripts/relay_*.py | wc -l
      13

$ ls scripts/relay_*.py
scripts/relay_auto_merge.py
scripts/relay_clipboard.py
scripts/relay_context.py
scripts/relay_digest.py
scripts/relay_executor.py
scripts/relay_local_loop.py
scripts/relay_notify.py
scripts/relay_notify_email.py
scripts/relay_paths.py
scripts/relay_planner.py
scripts/relay_preflight.py
scripts/relay_progress.py
scripts/relay_robot.py
```

Each file's module docstring (first 1–3 lines after the shebang) was read via `head -n 35` on 2026-06-17. No script bodies were modified or executed.

## Rollback command

```bash
rm relay-sandbox/results/01_sb-1-relay-script-inventory.md
```

## Rejected scope

- Editing any `scripts/relay_*.py` file (task scope: headers only, no edits).
- Schema, backend, database, secrets, migration, or renderer/math/overlay changes (not required; not attempted).
- Running relay scripts or opening a PR (not requested).

## VERIFIED

Read-only inventory complete: 13 `scripts/relay_*.py` files listed with one-line purposes from module docstrings.
