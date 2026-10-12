# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright for CI environment.

## Scope

- CI environment setup
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 63_install-playwright-ci.md

## Files expected to change

- 63_install-playwright-ci.md

## Required behavior

1. Review the current installation documentation for Playwright.
2. Create or update `63_install-playwright-ci.md` with the necessary steps for installing Playwright in the CI environment.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Ensure `63_install-playwright-ci.md` is updated with clear installation steps.
- Check for any errors or omissions in the documentation by running a CI test with Playwright.

## Rollback plan

- Revert changes made to `63_install-playwright-ci.md` to its previous state.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
