# TASK: 63

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright CI tooling for running automated smoke tests.

## Scope

- Integration of Playwright for end-to-end testing in the CI pipeline.
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- `51_install-playwright.md`
- `62_install-playwright-ci.md`

## Files expected to change

- `README.md` (to provide instructions on running Playwright CI)
- `playwright.config.js` (if it needs configuration adjustments)

## Required behavior

1. Review the existing Playwright installation documentation in `51_install-playwright.md`.
2. Follow the steps necessary to ensure Playwright can be executed as part of the CI workflow.
3. Document the process and any necessary configurations in `README.md` and/or `playwright.config.js`.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Run the CI pipeline with Playwright tests to verify successful execution and generate results showing successful smoke tests.

## Rollback plan

- If the installation does not function as expected, revert changes in `README.md` and any modifications made to `playwright.config.js`.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
