# AUDIT: 15_IN_SHELL_MAP_ROUTE_CLEANUP_AUDIT

Task: `15_IN_SHELL_MAP_ROUTE_CLEANUP_AUDIT`
Mode: read-only audit; documentation output only
Result: **VERIFIED**

## Files inspected

Allowed files only:

- `app_shell.html`
- `audits/05_frontend_placeholder_honesty_audit.md`
- `results/14_screen4_action_honesty_fix.md`

No production files were modified.

## 1. Where can the in-shell map route still be reached?

The in-shell `map` route renders `screenMap()` (registered as `map: screenMap`).
It is **not** reached by the primary top-nav "Map" button: that handler calls
`openMap(...)` and goes to the real production map (`map_CURRENT.html`) with
source `primary nav -> production map` (`app_shell.html` ~1054-1062).

It is still reachable via:

- Screen 4 `Back to shell map` buttons, both states (`data-nav="map"`, lines 1365 and 1397).
- A direct hash/URL targeting `route=map` (the route id `map` is registered at line 264 and rendered via `SCREEN_RENDERERS`).
- Internally, `mountGenieDrawer()` only mounts when `navContext.route === "map"` (line 1937), i.e. it is tied to this route.

So normal discovery is via the Screen 4 `Back to shell map` buttons or a direct route hash; primary nav no longer lands here.

## 2. What does screenMap() currently display?

- Breadcrumb `… · Map discovery` and heading `Screen 2 — Map Discovery`.
- Purpose line `Primary instrument · activeChartRecordId required.`
- Optional `switchNotice`, time-uncertainty warning, and `RESUME_CONTEXT_STUB` when an `explorationId` is present.
- `Module: production-map`: text `Production map opens in the main map tool.`, optional context place, and a primary button `Open production map` (`data-action="open-map-record"`, which calls the real `openMap(...)` handoff).
- A Genie drawer placeholder (expand/collapse; mounts the Genie variable builder when expanded).
- `Module: map-actions`: `Full chart (Screen 4)`, `Compare places (Screen 5)`, `Export / share status`, a disabled `Save exploration (auto-save stub)`, and `Back to Chart Record page`.
- A `stateDebugBlock()` and a `must-not` note.

Note: `screenMap()` computes a local `conditions` variable with draft strings
(`Sun in 10th (draft)`, `ASC in Gemini (draft)`) but does not render it. It is
dead/unused code and is not user-visible.

## 3. Does any user-facing control still imply it is the real production map?

Partially, in copy (not in behavior):

- The heading `Screen 2 — Map Discovery` and the purpose `Primary instrument` imply this page is the primary map. It is not; the real map is `map_CURRENT.html`.
- However, no fake map is rendered. The `production-map` module is honest: it says the production map opens in the main tool and provides an `Open production map` handoff button.
- `Save exploration (auto-save stub)` is disabled and labeled a stub (honest).

So the misleading element is the `Screen 2 — Map Discovery / Primary instrument`
framing, which oversells this page as the main map instrument. The actionable
controls themselves are honest (real handoff button, disabled stub).

## 4. Is "Back to shell map" now honest enough?

Yes, reasonably. After task 14 the two Screen 4 buttons say `Back to shell map`,
which explicitly signals the in-shell shell route rather than the production map.
It is honest. A marginally clearer wording would be `Back to map launcher` or
`Back to map context`, but `Back to shell map` is acceptable and not misleading.

## 5. Should the in-shell map route remain, be renamed, or be removed later?

Recommendation: **rename/reframe it now as a context/launcher page, and consider
removal later.**

- It already behaves as a launcher/context page (its real action is `Open production map`).
- The only dishonest part is the `Screen 2 — Map Discovery / Primary instrument` framing.
- Full removal is a larger change: it would require redirecting the two Screen 4 `Back to shell map` buttons (e.g. to production-map handoff or to the Chart Record page) and handling any direct `route=map` hash. That is more than a copy fix.

## 6. Smallest safe fix if needed

Copy-only, in `app_shell.html`, no behavior change:

- Reframe the heading/purpose so it does not claim to be the primary map, e.g.
  heading `Map launcher / context` and purpose `Opens the production map; this
  page is a context launcher, not the map itself.`
- Optionally relabel the Screen 4 `Back to shell map` buttons to `Back to map launcher` for extra clarity.
- Optionally (code hygiene, not user-facing) remove the unused `conditions` draft
  variable so stale draft strings do not linger in source.

No backend, schema, database, renderer, or `map_CURRENT.html` changes are needed
for the honesty fix.

## Verification status

VERIFIED: the in-shell map route is reachable only via Screen 4 `Back to shell
map` and direct hash; `screenMap()` renders an honest production-map handoff but
is over-framed as `Primary instrument`; `Back to shell map` is honest enough; the
smallest fix is copy-only reframing of the heading/purpose.

VERIFIED
