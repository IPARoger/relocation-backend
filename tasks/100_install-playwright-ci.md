# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)  

## Objective

Install Playwright for CI purposes.

## Scope

- CI environment setup
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 51_install-playwright.md

## Files expected to change

- 51_install-playwright-ci.md

## Required behavior

1. Install Playwright as specified in the CI documentation.
2. Ensure that the installation process does not change any other existing configurations.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Verify that Playwright is correctly installed by running the CI workflow and checking for successful execution.

## Rollback plan

- Reverse the installation by removing any added dependencies and restoring CI configuration to its previous state.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
