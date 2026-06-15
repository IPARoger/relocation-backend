# RESULT: 07_SAVED_INVESTIGATION_REPLAY_HONESTY

Task: `07_SAVED_INVESTIGATION_REPLAY_HONESTY`
Mode: small UI copy fix only
Result: **VERIFIED**

## Telegram notifications

- Sent `started` exactly once at task start (`sent: started`).
- Closeout: exactly one `verified` notification after scope verification.
- No arbitrary text, task content, code, or paths were sent to Telegram.

## Objective

Correct the Saved Investigation replay copy so it accurately reflects current
behavior established in task 06: reopening a saved investigation restores
chart/profile context, saved conditions, and viewport center/zoom, then
auto-runs Find Regions once.

## Question 1 — user-visible replay wording

All replay wording is centralized in a single constant and reused everywhere:

- `app_shell.html:233` — `RESUME_CONTEXT_STUB` (the source string).
- `resumeContextStubHtml()` renders it in:
  - Dashboard "recent-explorations-across-records" list.
  - Chart Record "saved-explorations (this Chart Record)" list.
- Map screen (`screenMap()`) renders it as a stub when `navContext.explorationId`
  is present.

There is exactly one user-visible string; changing the constant updates all
three placements consistently.

## Question 2 — wording updated to match behavior

Before:

> Resume passes context only; saved conditions not replayed on map (v1).

After:

> Resume restores the chart, saved conditions, and map view, then runs Find Regions once.

This now matches the verified task 06 behavior: chart/profile context, saved
conditions, and viewport center/zoom are restored, and Find Regions auto-runs
once.

## Question 3 — honest and consistent

- The old copy falsely claimed conditions are "not replayed"; the new copy is
  truthful.
- A single constant drives all three surfaces, so dashboard, chart-record, and
  map wording stay identical and consistent.
- The new copy does not over-promise: it omits unrestored items
  (settings snapshot, exact prior map artifacts, selected place, UI state),
  which is accurate per task 06.

## Files changed by this task

- `app_shell.html` — one line (`RESUME_CONTEXT_STUB` text only).
- `results/07_saved_investigation_replay_honesty.md` — this output.

## Validation evidence

Isolated task-07 change (backup taken immediately before edit vs current):

```
233c233
< const RESUME_CONTEXT_STUB = "Resume passes context only; saved conditions not replayed on map (v1).";
---
> const RESUME_CONTEXT_STUB = "Resume restores the chart, saved conditions, and map view, then runs Find Regions once.";
```

Confirmed:

- Replay behavior unchanged — only a string constant's text changed; no logic,
  handlers, or data flow touched.
- Only copy changed — exactly one line in `app_shell.html`.
- No routes changed — `data-nav`/`data-action`/handoff URLs untouched.
- No map logic changed — `map_CURRENT.html` not modified.

## Note on working tree

The repository working tree also contains pre-existing uncommitted house-system
honesty edits from an earlier task (04). Those are unrelated to task 07 and were
not introduced here; task 07's sole change is the single copy line above.

## Rejected scope

- No backend, database, schema, or map logic changes.
- No replay behavior changes.
- No edits beyond the single authorized copy string and this results file.

## Rollback

```
git checkout -- app_shell.html results/07_saved_investigation_replay_honesty.md
```

VERIFIED
