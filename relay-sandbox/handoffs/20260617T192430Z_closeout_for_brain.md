# Closeout ingested for next Claude/GPT plan

This replaces pasting Cursor output back into Claude by hand.
On the next `relay_robot.py` plan step, this file is included in the context pack.

## Source: relay-sandbox/results/11_sb-11-chat-instructions-lines.md

# RESULT: 11_sb-11-chat-instructions-lines

**Roadmap ID:** SB-11
**Author:** Cursor (execution half)
**Date:** 2026-06-18

## Objective

Count lines in `relay/CHAT_INSTRUCTIONS.md`. Read-only.

## Summary

`relay/CHAT_INSTRUCTIONS.md` contains **9** lines (including blank lines and trailing newline).

| Metric | Value |
|--------|------:|
| Line count (`wc -l`) | 9 |
| Byte size | 339 |

## Files changed

- `relay-sandbox/results/11_sb-11-chat-instructions-lines.md` (this closeout only)
- No changes to `relay/CHAT_INSTRUCTIONS.md` or any other source files.

## Validation evidence

```text
$ wc -l relay/CHAT_INSTRUCTIONS.md
       9 relay/CHAT_INSTRUCTIONS.md

$ wc -c relay/CHAT_INSTRUCTIONS.md
     339 relay/CHAT_INSTRUCTIONS.md

$ cat -n relay/CHAT_INSTRUCTIONS.md
     1	# Claude / ChatGPT project instructions (paste here once)
     2	
     3	Paste your Claude Project custom instructions, system prompt, and discipline
     4	rules below this line. The relay robot sends this file on every planning call
     5	so API planning matches your real chat brain.
     6	
     7	---
     8	(Paste your Claude Project instructions here. Replace this placeholder.)
     9	
```

## Rollback command

```bash
rm relay-sandbox/results/11_sb-11-chat-instructions-lines.md
```

## Rejected scope

- Modifying, adding, or deleting `relay/CHAT_INSTRUCTIONS.md` (task scope: read-only line count).
- Schema, backend, database, secrets, migration, or renderer/math/overlay changes (not required; not attempted).
- Opening a PR (not requested).

## VERIFIED

Read-only chat-instructions line audit complete: **9** lines in `relay/CHAT_INSTRUCTIONS.md`; no other artifacts modified.
