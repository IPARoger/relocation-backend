# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto  
**Status:** Proposed (awaiting human commit)

## Objective

Audit the settings to confirm the truthfulness of the current settings consumption.

## Scope

- settings consumption
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 02_settings_consumption_audit.md
- 03_settings_truth_audit.md

## Files expected to change

- NONE — read-only inventory

## Required behavior

1. Review the `settings consumption` audit document to extract current settings.
2. Verify these settings against the truth audit for discrepancies or inaccuracies.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change
- backend change
- database write
- credentials / secrets
- migration
- renderer / math / overlay changes

## Validation plan

- The audit will validate by cross-referencing discrepancies between the settings consumption and the truth audit, ensuring all are accounted for and truthful.

## Rollback plan

- No changes will be made; therefore, no rollback is required.

## Closeout required (Cursor writes this into results/)

- files changed
- validation evidence
- rollback command
- rejected scope
- VERIFIED or NOT VERIFIED
