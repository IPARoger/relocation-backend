# AUDIT: 13_SCREEN4_ACTION_HONESTY_AUDIT

Task: `13_SCREEN4_ACTION_HONESTY_AUDIT`
Mode: read-only audit; documentation output only
Result: **VERIFIED**

## Files inspected

Allowed files only:

- `app_shell.html`
- `results/11_export_share_honesty_fix.md`
- `results/12_export_button_label_honesty_fix.md`
- `audits/05_frontend_placeholder_honesty_audit.md`

No production files were modified.

## Screen 4 action surface

`screenChart()` renders Screen 4 (`Screen 4 — View Chart`). It has two states.

### Blocked state

When `chartRecordId` or `placeId` is missing, Screen 4 renders:

- `Back to map` (`data-nav="map"`)

This is a navigation button only.

### Normal state

When both `chartRecordId` and `placeId` exist, Screen 4 renders:

- Inline note textarea: `Optional inline note (placeholder — not saved)`
- `Favorite this place` (`disabled`)
- `Back to map` (`data-nav="map"`)
- `Add to comparison` (`data-nav="compare"`)
- `Export / share status` (`data-nav="export"`)

## Behavior evidence

Generic `data-nav` handling:

- Reads `data-nav`, optional `data-chart-record`, optional `data-place-id`, optional `data-place`.
- Builds a patch only from explicit data attributes.
- For `route === "compare"`, calls `navigate(route, patch, { pushReturn: true })`.
- For other routes, calls `navigate(route, patch)`.

Because the Screen 4 action buttons do not provide explicit `data-place-id`, the current `navContext` is preserved by `navigate(...)`, but no comparison-set mutation occurs.

## Answers

### 1. What action buttons/links exist on Screen 4?

Normal state:

- `Favorite this place` (disabled)
- `Back to map`
- `Add to comparison`
- `Export / share status`

Blocked state:

- `Back to map`

Screen 4 also includes an inline note textarea marked `placeholder — not saved`, but it is not an action button/link.

### 2. Which are real?

- `Export / share status` is real as navigation to the honest status screen created by tasks 11/12. It does not promise export generation anymore.
- `Back to map` is real as navigation to the shell `map` route, but not necessarily to the production `map_CURRENT.html` handoff.
- `Add to comparison` is real only as navigation to the Compare screen; it is not real as an “add current place to comparison set” action.

### 3. Which are disabled placeholders?

- `Favorite this place` is disabled.
- Inline note textarea is an honest placeholder (`placeholder — not saved`) but is not disabled.

### 4. Which imply behavior that does not happen?

- `Add to comparison` implies the current place will be added to a comparison set. Current behavior only navigates to the Compare screen and records return context; no place is added.
- `Back to map` can imply return to the production map, but it uses `data-nav="map"`, which routes to the in-shell map route. Prior audit 05 classified this as an orphaned navigation path.

`Export / share status` no longer implies export/share generation after tasks 11/12.

### 5. Is “Add to comparison” honest?

No. It is misleading as an action label.

Current behavior:

- Navigates to route `compare`.
- Uses `{ pushReturn: true }`, so the return snapshot preserves context.
- Does not add the current place to a comparison set.
- Does not mutate comparison data.

So the smallest honest label would be something like `Open comparison workspace` or `Comparison status`, unless a later implementation actually wires place insertion.

### 6. Is “Favorite this place” honest, disabled, or misleading?

It is honest enough because it is disabled. It appears in a panel with a note textarea that explicitly says `placeholder — not saved`, and prior audit 05 classified Screen 4 notes/favorite as an acceptable honest placeholder.

A future micro-copy improvement could label it `Favorite this place (not available yet)`, but it is not currently a high-priority misleading active control because it cannot be clicked.

### 7. Is “Back to map” honest and correctly contextual?

Partially.

It is honest that it navigates to a map route and preserves current `navContext`, but it is not fully contextual if the user expects the production map (`map_CURRENT.html`). The button uses `data-nav="map"`, not `openMap(...)`, so it returns to the in-shell map route. Audit 05 already classified this as an orphaned navigation path.

Smallest honesty wording would be `Back to shell map` or `Back to map status`. A behavior fix would be to wire this to production map handoff, but that is outside a read-only audit and may be broader than a copy-only honesty fix.

### 8. Smallest fix if needed

Smallest copy-only honesty fix in `app_shell.html`:

- `Add to comparison` -> `Open comparison workspace` or `Comparison status`.
- `Back to map` -> `Back to shell map` / `Back to map status`, unless the product decision is to wire production-map handoff.
- Optionally `Favorite this place` -> `Favorite this place (not available yet)` while keeping it disabled.

No backend, schema, database, renderer, or `map_CURRENT.html` work is required for the honesty fix.

## Verification status

VERIFIED: Screen 4 action buttons were inventoried from `app_shell.html`; prior audit evidence was checked; `Add to comparison` and `Back to map` remain the honesty gaps; `Favorite this place` is disabled/honest; `Export / share status` is honest after tasks 11/12.

VERIFIED
