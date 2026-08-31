# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Install Playwright for CI environment.

## Scope

- CI integration for testing with Playwright
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 51_install-playwright.md
- 61_install-playwright.md

## Files expected to change

- 61_install-playwright.md (for CI related updates)

## Required behavior

1. Review existing installation steps for Playwright in the CI context.
2. Document and implement any necessary adjustments to facilitate CI integration.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- Confirm CI environment can successfully run Playwright tests post-installation.

## Rollback plan

- Revert changes made in 61_install-playwright.md if issues arise.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
