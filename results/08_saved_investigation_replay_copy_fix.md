# RESULT: 08_SAVED_INVESTIGATION_REPLAY_COPY_FIX

Task: `08_SAVED_INVESTIGATION_REPLAY_COPY_FIX`
Mode: small scoped implementation (UI copy only)
Result: **VERIFIED**

## Telegram notifications

- Sent `started` exactly once at task start (`sent: started`).
- Closeout: exactly one `verified`.
- No task content, code, or paths transmitted.

## Context note (important)

The original stale string identified in audit 06 —
`Resume passes context only; saved conditions not replayed on map (v1).` —
was already replaced in task 07. All saved-investigation replay copy is driven
by a single constant, `RESUME_CONTEXT_STUB` (`app_shell.html` line 233), reused
in three render sites:

- Dashboard "recent-explorations-across-records" list (line 1110)
- Chart Record "saved-explorations" list (line 1192)
- Map screen resume stub (line 1310)

Task 08 refines that one constant so the wording also states the conditions/
viewport are restored *when available*, that search runs once, and that it is
*not a frozen snapshot* — matching the four required points.

## Before / after copy

Before (post task 07 state):

> Resume restores the chart, saved conditions, and map view, then runs Find Regions once.

After (task 08):

> Reopens on the map — saved conditions and the map view are restored when available, then the search runs once. Not a frozen snapshot.

This satisfies the required behavior:

1. Saved investigation reopens on the map. ("Reopens on the map")
2. Saved conditions and viewport restored when available. ("saved conditions and
   the map view are restored when available")
3. Map search runs once automatically. ("then the search runs once")
4. Not a frozen rendered snapshot. ("Not a frozen snapshot")

Language is short and non-promotional. No new behavior was added; only the
display string changed.

Note: "map view" is used as the user-facing term for the viewport; the concept
is the same (center/zoom restoration).

## Validation evidence

Isolated task-08 change (pre-edit backup vs current):

```
233c233
< const RESUME_CONTEXT_STUB = "Resume restores the chart, saved conditions, and map view, then runs Find Regions once.";
---
> const RESUME_CONTEXT_STUB = "Reopens on the map \u2014 saved conditions and the map view are restored when available, then the search runs once. Not a frozen snapshot.";
```

(`\u2014` is a JavaScript string escape for an em dash; it renders as "—".)

Confirmed:

- Only `app_shell.html` was changed by this task (exactly one line).
- The constant still flows to all three render sites (lines 1110, 1192, 1310).
- `map_CURRENT.html` unchanged (`git diff --stat` empty).
- No backend route, Supabase/schema/migration, or renderer/math change.
- No new behavior introduced; replay logic untouched.

Local UI check: verified at the code-path level — the updated constant is wired
into the three rendering functions/sites above. A full browser render was not
executed in this session; the change is a pure display string with no logic
impact.

## Working-tree note

The repository working tree also contains pre-existing, unrelated modifications
(`main_centerline_FIXER.py`, `repositories/profiles_repository.py`,
`docs/...`, and earlier app_shell edits). These predate task 08 and were not
introduced by it; task 08's sole change is the single copy line proven above.

## Rejected scope

- No `map_CURRENT.html` change.
- No backend routes, Supabase, schema, or migrations.
- No renderer/math change.
- No edits to tasks/results/audits beyond this results file.

## Rollback

```
git checkout -- app_shell.html results/08_saved_investigation_replay_copy_fix.md
```

VERIFIED
