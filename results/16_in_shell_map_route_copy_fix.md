# RESULT: 16_IN_SHELL_MAP_ROUTE_COPY_FIX

Task: `16_IN_SHELL_MAP_ROUTE_COPY_FIX`
Mode: copy cleanup only (implementation)
Result: **VERIFIED**

## Telegram notifications

- Sent `started` exactly once (`sent: started`).
- Closeout: exactly one `verified`.
- No task content, code, or paths transmitted.

## Source evidence

- `audits/15_in_shell_map_route_cleanup_audit.md`
- `results/15_in_shell_map_route_cleanup_audit.md`

## Changes made (only `app_shell.html`)

1. Heading reframed in both visible places (route meta + on-screen H2):
   - `Screen 2 — Map Discovery` -> `Screen 2 — Map Launcher` (registry line 264 and `screenMap()` H2).
2. Purpose reframed:
   - `Primary instrument · activeChartRecordId required.` -> `Use the production map for exploration. This shell page preserves context and handoff controls.`
3. Removed the provably-unused draft variables inside `screenMap()`:
   - `const exp = activeExploration();`
   - `const conditions = exp ? exp.conditions : [...draft...];`
   These were computed but never rendered. The shared `activeExploration()` function is retained (still used by `activeContextChip()` at line 958).

## Required changes mapped

1. **Keep the route** — Done. `map: screenMap` and route id `map` unchanged.
2. **Keep Open production map handoff** — Done. Button present (line 1314).
3. **Do not change navigation behavior** — Done. No `data-nav`/`data-action`/`openMap` logic changed.
4. **Do not touch `map_CURRENT.html`** — Honored.
5. **Change heading/purpose so it does not imply primary map** — Done.
6. **Suggested wording** — Applied verbatim.
7. **Optional dead-variable removal** — Done; provably unused, minimal 2-line removal.

## Validation evidence

- **`Primary instrument` wording gone:** search returns nothing.
- **`Open production map` still exists:** present at line 1314.
- **`data-action="open-map-record"` still exists:** present at lines 1166 and 1314 (the map-launcher handoff button is line 1314).
- **Only `app_shell.html` changed by this task:** isolated diff (pre-edit backup vs current) shows only the heading/purpose lines and the two removed dead lines.
- **No backend/schema/map/renderer changes:** `git diff --stat -- map_CURRENT.html` empty; all edits are copy/text plus dead-code removal in one function.

## Rejected scope

- No navigation/behavior change.
- No route removal.
- No `map_CURRENT.html`, backend, schema, or renderer change.
- No edits beyond `app_shell.html` and this results file.

## Rollback

```
git checkout -- app_shell.html results/16_in_shell_map_route_copy_fix.md
```

VERIFIED
