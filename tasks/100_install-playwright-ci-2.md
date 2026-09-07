# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)  

## Objective

Install Playwright CI tooling to support end-to-end testing in the project.

## Scope

- Tools setup for end-to-end testing
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- `51_install-playwright.md`
- `62_install-playwright-ci.md`

## Files expected to change

- `51_install-playwright.md`  
- `62_install-playwright-ci.md`

## Required behavior

1. Verify the current setup instructions for Playwright in the specified files.
2. Implement necessary adjustments to ensure CI integration for Playwright.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Validate integration by running a sample Playwright test in the CI pipeline and confirming successful completion.

## Rollback plan

- Revert changes in `51_install-playwright.md` and `62_install-playwright-ci.md` to their previous state prior to modifications.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
