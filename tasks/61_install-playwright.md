# TASK: 61

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright for testing functionality.

## Scope

- Installation of Playwright in the project environment.
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- `51_install-playwright.md`

## Files expected to change

- `requirements.txt` (or: NONE — read-only inventory)

## Required behavior

1. Install Playwright and its dependencies.
2. Verify the installation by checking if `playwright` can be imported successfully in the existing test setup.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Success is proven by confirming that Playwright is installed and can be imported without errors.

## Rollback plan

- If the installation fails, use the command to uninstall Playwright: `pip uninstall playwright`.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
