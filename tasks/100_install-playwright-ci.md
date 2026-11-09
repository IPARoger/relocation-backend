# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright for CI to enable smoke tests.

## Scope

- CI environment setup
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 62_install-playwright-ci.md

## Files expected to change

- 62_install-playwright-ci.md

## Required behavior

1. Review the installation requirement for Playwright in the CI context.
2. Write the steps to install Playwright for CI usage clearly in the designated file.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Verify that the installation steps are documented correctly and can be followed to set up Playwright in CI.

## Rollback plan

- Remove the added installation instructions if they are incorrect or unnecessary.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
