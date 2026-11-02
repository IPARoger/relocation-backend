# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright for CI in the project.

## Scope

- CI tooling setup for testing
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 51_install-playwright.md

## Files expected to change

- 62_install-playwright-ci.md

## Required behavior

1. Review the current installation instructions for Playwright.
2. Implement the installation steps as specified in the CI context.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Confirm successful installation by running `npx playwright install` and verifying that all browsers are installed for the CI environment.

## Rollback plan

- Remove the Playwright installations from CI settings if any issues arise during installation.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
