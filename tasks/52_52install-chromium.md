# TASK: 52_install-chromium

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto | Sonnet | Opus  
**Status:** Proposed (awaiting human commit)

## Objective

Install the Chromium browser binary required for Playwright tests.

## Scope

- Playwright testing environment
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- `requirements.txt`

## Files expected to change

- NONE — read-only inventory

## Required behavior

1. Verify that the Chromium browser is installed for Playwright by running the command: `playwright install chromium`.
2. Document the installation process and outcome in the results.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Check that the Chromium browser is available for Playwright by running a sample Playwright script that opens a browser instance.

## Rollback plan

- N/A — This task does not modify any files.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
