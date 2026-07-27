# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Verify the installation of Playwright.

## Scope

- Check the integration of Playwright with the current setup.
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 51_install-playwright.md

## Files expected to change

- NONE — read-only inventory

## Required behavior

1. Confirm that Playwright is installed correctly.
2. Execute a test script to ensure Playwright functions as expected in the current environment.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Document the results of the Playwright installation check and any test script results as evidence.

## Rollback plan

- N/A since this is a verification task with no changes made.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
