# AUDIT: 09_SAVED_INVESTIGATION_COPY_CENTRALIZATION

Task: verify every user-facing saved-investigation replay **description** originates from `RESUME_CONTEXT_STUB`.
Mode: read-only diagnosis; audit output only.
Result: **VERIFIED**

## Files inspected

- `app_shell.html`

## Search performed

Searched `app_shell.html` for saved-investigation / replay / resume / snapshot wording:

- `saved investigation`
- `saved-investigation`
- `saved exploration`
- `saved-exploration`
- `resume`
- `reopen`
- `replay`
- `conditions.*restore`
- `restore.*conditions`
- `viewport`
- `map view`
- `frozen snapshot`
- `snapshot`
- `search runs`
- `runs once`
- `Find Regions`

Also searched directly for:

- `RESUME_CONTEXT_STUB`
- `resumeContextStubHtml`

## Central replay description

The only user-facing replay behavior description is centralized here:

```text
const RESUME_CONTEXT_STUB = "Reopens on the map \u2014 saved conditions and the map view are restored when available, then the search runs once. Not a frozen snapshot.";
```

It is rendered through these sites:

- `resumeContextStubHtml()` returns the constant inside a `<span class="meta">...`.
- Dashboard recent-explorations list calls `resumeContextStubHtml()`.
- Chart Record saved-explorations list calls `resumeContextStubHtml()`.
- Map screen renders `${RESUME_CONTEXT_STUB}` when `navContext.explorationId` is present.

## Non-description user-visible strings found outside the constant

These user-facing strings mention resume/exploration but do **not** describe replay behavior, restored conditions, viewport restoration, auto-search, or snapshot semantics:

- `Resumed exploration:` — context chip/status label for the active exploration.
- `Resume exploration for this record.` — chart-record page purpose text.
- `No saved explorations yet. Open the map, run a search, and save it to resume later.` — empty-state instruction.
- `Resume → Map` — button label.
- `Resumed exploration: ${exploration.name}` / `Resumed exploration` — navigation notice.

These are labels, statuses, or empty-state instructions; they are not saved-investigation replay behavior descriptions.

## Remaining replay descriptions outside `RESUME_CONTEXT_STUB`

None found.

## Scope verification

- No files modified except this requested audit output.
- No production code changed.
- No backend, schema, database, renderer, or map logic inspected beyond the requested `app_shell.html` search context.

VERIFIED
