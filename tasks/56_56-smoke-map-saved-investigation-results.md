# Task 56 — Review and Record Results of Map/Saved-Investigation Smoke Tests

**Roadmap ID:** T56_1  
**Task type:** Read-only diagnosis / closeout documentation  
**Authorized changes:** One new markdown result file only

---

## Objective

Read the result file from Task 55 (`relay/55_55smoke-map-saved-investigation.md`) and produce a closeout record that accurately captures pass/fail status, any failures or blockers found, and the recommended next action. No code changes.

---

## Scope

- Read Task 55 result only.  
- Produce one new file: `relay/56_smoke-map-saved-investigation-results.md`.  
- Do **not** touch any source files, test scripts, or CI config.

---

## Files to Read

| File | Purpose |
|---|---|
| `relay/55_55smoke-map-saved-investigation.md` | Task 55 result — playwright smoke of map and saved-investigation routes |
| `relay/54_54run-quarantine-smoke-tests.md` | Prior quarantine smoke context (reference only) |
| `relay/50_smoke_quarantine_routes.md` | Quarantine route list (reference only) |

---

## Files Expected to Change

| File | Change |
|---|---|
| `relay/56_smoke-map-saved-investigation-results.md` | **NEW** — closeout record (created by Cursor) |

No other files may be modified.

---

## Required Behavior

Cursor must:

1. Open and read `relay/55_55smoke-map-saved-investigation.md` in full.
2. Extract:
   - Which routes/pages were tested.
   - Pass / fail / skip status for each test.
   - Any error messages, timeouts, or assertion failures verbatim.
   - Whether Playwright and Chromium executed successfully or threw setup errors.
3. Write `relay/56_smoke-map-saved-investigation-results.md` containing:
   - **Summary verdict**: PASSED / PARTIALLY VERIFIED / NOT VERIFIED / BLOCKED (pick one).
   - **Test matrix**: route → status → evidence quote.
   - **Failures section**: exact error text for anything that did not pass.
   - **Root cause classification** for each failure (setup error, server not running, missing route, assertion mismatch, Playwright config, other).
   - **Recommended next action**: the single smallest unblock step, or "no action needed" if all passed.

---

## Hard Stops

- Do **not** re-run any smoke tests.  
- Do **not** edit any `.js`, `.py`, `.html`, or `.ts` files.  
- Do **not** modify CI config or Playwright config.  
- Do **not** touch schema, backend, database, migrations, or renderer files.  
- If Task 55 result file is absent or empty, write that finding in the closeout file and stop — do not attempt to re-execute the task.

---

## Validation Plan

The closeout file is valid if:
- It exists at `relay/56_smoke-map-saved-investigation-results.md`.
- It contains a single top-level verdict word (PASSED / PARTIALLY VERIFIED / NOT VERIFIED / BLOCKED).
- It lists every route tested in Task 55 with a per-route status.
- Any failure includes a verbatim error quote (not a paraphrase).
- It ends with a concrete "Recommended next action" section.

---

## Rollback Plan

The only artifact produced is a new markdown file. Rollback = `git rm relay/56_smoke-map-saved-investigation-results.md`. No code was changed so no code rollback is needed.

---

## Closeout Contract

Task 56 is complete when:
- [ ] `relay/56_smoke-map-saved-investigation-results.md` exists and is non-empty.
- [ ] Verdict is one of the four allowed values.
- [ ] Per-route test matrix is present.
- [ ] Failures (if any) include verbatim error text.
- [ ] "Recommended next action" section is present and actionable.
- [ ] No source files were modified.
