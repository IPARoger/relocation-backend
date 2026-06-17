# TASK: 65

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright for CI testing.

## Scope

- CI tooling for smoke tests
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 62_install-playwright-ci.md

## Files expected to change

- 62_install-playwright-ci.md

## Required behavior

1. Validate that Playwright is installed correctly in the CI environment.
2. Ensure that relevant smoke tests can execute successfully once Playwright is installed.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Verify the installation by running a basic Playwright test that confirms the functionality works (e.g., launching a browser instance).

## Rollback plan

- Revert any changes by removing Playwright configuration or installation instructions from the CI setup.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
