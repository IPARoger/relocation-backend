# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright CI tooling to support automated browser testing.

## Scope

- CI tooling setup for Playwright
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 51_install-playwright.md (duplicate check)

## Files expected to change

- 62_install-playwright-ci.md

## Required behavior

1. Install Playwright as part of the CI process.
2. Ensure that all necessary configurations are added to the CI pipeline.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Verify that the Playwright installation is successful by running a sample CI job that incorporates Playwright tests.

## Rollback plan

- Remove the Playwright installation from the CI configuration if any issues arise.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
