# TASK: 55

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install the `supabase-py` package in the environment.

## Scope

- Python environment setup
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- `results/53_53verify-smoke-scripts.md`
- `tasks/54_install-supabase-py.md`

## Files expected to change

- NONE — read-only inventory

## Required behavior

1. Check the current Python environment for the presence of `supabase-py`.
2. If `supabase-py` is not installed, install it using pip.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Confirm successful installation of `supabase-py` by running the command `python3 -m pip show supabase` to check package version and location.

## Rollback plan

```bash
# Uninstall supabase-py if necessary.
pip uninstall -y supabase
```

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
