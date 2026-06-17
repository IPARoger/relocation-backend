# TASK: 54

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto | Sonnet | Opus  
**Status:** Proposed (awaiting human commit)

## Objective

Install the `supabase-py` package to enable backend access for smoke tests.

## Scope

- Environment setup and dependencies for executing smoke tests. 
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- `.env.staging`
- `requirements.txt`

## Files expected to change

- `requirements.txt` (or: NONE — read-only inventory)

## Required behavior

1. Install the `supabase-py` package within the existing Python virtual environment.
2. Ensure that the installation does not affect other dependencies or the environment settings.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Verify that `supabase-py` is included in `requirements.txt` post-installation.
- Confirm installation success by checking the package version using the command: `python3 -m pip show supabase`.

## Rollback plan

```bash
# This command will uninstall the package if needed.
pip uninstall -y supabase
```

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
