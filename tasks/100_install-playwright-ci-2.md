# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright for CI to enable automated testing.

## Scope

- CI testing environment
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 51_install-playwright-ci.md

## Files expected to change

- 51_install-playwright-ci.md

## Required behavior

1. Check for existing Playwright installation in CI.
2. Update the CI configuration to use Playwright for testing.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Verify that Playwright is successfully installed by running a basic test script in the CI environment.

## Rollback plan

- Revert changes made to `51_install-playwright-ci.md` if the installation fails.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
