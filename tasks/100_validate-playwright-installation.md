# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Verify that the Playwright installation is correctly configured.

## Scope

- Validate the Playwright installation across relevant projects.
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 62_install-playwright-ci.md
- 63_install-playwright-ci.md

## Files expected to change

- NONE — read-only inventory

## Required behavior

1. Run the Playwright validation script to check the installation.
2. Ensure that all Playwright dependencies are correctly installed and report any issues found.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Success is confirmed through the output of the Playwright validation script indicating all dependencies are installed correctly.

## Rollback plan

- No rollback is required as the task involves validation only.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
