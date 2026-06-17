# TASK: 64

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright to enable running CI tests in the relay environment.

## Scope

- CI testing framework integration.
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- `51_install-playwright.md`
- `62_install-playwright-ci.md`

## Files expected to change

- `requirements.txt` (or: NONE — read-only inventory)

## Required behavior

1. Review the contents of `51_install-playwright.md` for any specific dependencies or configurations needed for Playwright.
2. Apply necessary installation commands to ensure Playwright can run for CI testing.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Confirm that Playwright is successfully installed by checking the `requirements.txt` or any corresponding installation logs.
- Run a preliminary test to verify the proper setup of Playwright in the CI environment.

## Rollback plan

- Remove the Playwright lines from `requirements.txt` or revert any changes made in the installation process.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
