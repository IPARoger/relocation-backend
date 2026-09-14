# TASK: 100

**Author:** ChatGPT (tasks/ lane)  
**Model (suggested):** Auto | Sonnet | Opus  
**Status:** Proposed (awaiting human commit)  

## Objective

Analyze the existing comparison sets inventory for completeness and correctness.  

## Scope

- Review current comparison sets listed in the project.
- Relay data rule applies: read-only / diagnosis-only unless explicitly authorized in this task.

## Files to read

- 66_c4_6_comparison_sets_bridge.md  
- 98_cux3_unified_saved_location_search.md  

## Files expected to change

- NONE — read-only inventory  

## Required behavior

1. Document any discrepancies or missing data in the comparison sets.
2. Create a summary report of findings for future reference.

## Hard stops (stop and ask — do not proceed)

This task is NOT authorized to perform any of the following. If the work appears to require any of these, STOP and report instead of proceeding:

- schema change  
- backend change  
- database write  
- credentials / secrets  
- migration  
- renderer / math / overlay changes  

## Validation plan

- The analysis will be verified by cross-referencing with the expected structures and any existing comparison set schemas highlighted in the relevant documentation.

## Rollback plan

- No rollback required as this is a read-only analysis.

## Closeout required (Cursor writes this into results/)

- files changed: NONE  
- validation evidence: Summary report of findings will be included.  
- rollback command: N/A  
- rejected scope: N/A  
- VERIFIED or NOT VERIFIED: To be determined upon completion of the analysis.
