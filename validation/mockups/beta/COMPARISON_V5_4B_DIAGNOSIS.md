# V5-4B Compare Route State — Diagnosis

## Branching (`screenCompare`)

| URL state | Branch | DOM |
|-----------|--------|-----|
| `#/compare` (no `comparisonSetId`) | `renderComparisonPickerShell()` | picker only — no `#rm-cmp-v5-root`, no legacy Module panels |
| `#/compare?comparisonSetId=VALID` + cs in store | `ComparisonV5Route.renderShellHtml()` | `#rm-cmp-v5-root` + hidden `#rm-screen5-columns` bridge |
| `#/compare?comparisonSetId=…` but cs missing / flag off | legacy fallback | `rm-comparison-beta-root` (rollback) |

## `shouldRenderCanonicalShell`

True only when: flag on, `cs` exists, `comparisonSetId` set, `ws` exists, and `cs.placeIds.length >= 2`.

## `renderShellHtml`

Emits `#rm-cmp-v5-root` and hydration bridge with `#rm-screen5-columns` (`data-chart-record`, `data-place-ids`).

## Hydration sequence

1. `render()` → `mountComparisonV5Route(#main)` (compare only)
2. `hydrateComparisonColumns` fetches relocated cols → `_comparisonColsCache = cols`
3. When `#rm-cmp-v5-root` present and `cols.length > 0` → `ComparisonV5Route.hydrateCanonical(v5ctx)`

## Root cause: empty V5 tables / city bar

`bindScreenActions()` and `mountComparisonV5Route()` both called `hydrateComparisonColumns()`.
Each call increments `_screen5Token`; the first async fetch was discarded when the second started,
so `hydrateCanonical` never ran with populated `cols`.

## Root cause: partial V5 chrome

`syncRouteChrome` keyed only on `comparisonSetId` in the URL, not on resolved `cs` or canonical DOM.
Stale/invalid ids showed V5 nav/body class while legacy picker/modules rendered.

## Fixes (V5-4B)

- Compare hydration owned by `mountComparisonV5Route` only (`bindScreenActions` skips compare).
- `syncRouteChrome` uses `canonicalActive` (cs + ws + `#rm-cmp-v5-root` + `shouldRenderCanonicalShell`).
- Picker-only path when no `comparisonSetId`.
- Canonical hydrate gated on non-empty `cols` array.
