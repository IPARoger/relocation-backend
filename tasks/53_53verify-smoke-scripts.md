# TASK: 53

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Verify the execution of all smoke scripts to ensure that the end-to-end functionality is intact.

## Scope

- Smoke testing of the Playwright scripts in the `scripts/` directory.
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- `scripts/smoke_*.py`

## Files expected to change

- NONE — read-only inventory

## Required behavior

1. Execute each smoke script found in the `scripts/` directory.
2. Document execution results and any errors encountered.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Gather output logs for each smoke script execution showing pass/fail status.
- Evidence will be collected before and after running the scripts.

## Rollback plan

- No rollback required as no files will be changed.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
