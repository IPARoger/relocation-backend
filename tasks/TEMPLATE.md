# TASK: <TASK-ID>

**Author:** ChatGPT (tasks/ lane)
**Model (suggested):** Auto | Sonnet | Opus
**Status:** Proposed (awaiting human commit)

## Objective

<One sentence. One objective only.>

## Scope

- <surface / module in scope>
- Relay data rule applies: read-only / diagnosis-only unless explicitly
  authorized in this task.

## Files to read

- <path>
- <path>

## Files expected to change

- <path>  (or: NONE — read-only inventory)

## Required behavior

1. <...>
2. <...>

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears
to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- <how success is proven — live evidence, before/after, etc.>

## Rollback plan

- <exact command or steps>

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
