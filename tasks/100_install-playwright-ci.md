# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright CI tooling to enable smoke tests.

## Scope

- CI setup for Playwright 
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 51_install-playwright-ci.md

## Files expected to change

- 51_install-playwright-ci.md 

## Required behavior

1. Review the installation instructions in the provided files.
2. Execute the installation steps outlined to set up Playwright for CI testing.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Check that Playwright is correctly installed and configured for CI.
- Confirm that smoke tests can be executed using the new setup.

## Rollback plan

- Remove the Playwright installation or revert any configuration changes made during the install process.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
