# Comparison V5 Route Dependency Graph (V5-4A)

## Root cause (Profile regression)

`const RM_COMPARE_V5_CANONICAL` lived in a **separate** `<script>` block from the main app.
`const`/`let` do not leak across script tags, so `render()` called `renderComparisonV5Nav()` on
every route and threw `ReferenceError: RM_COMPARE_V5_CANONICAL is not defined` on Profile.

## Plugin boundary

```
comparison_v5_adapter.js
  └── window.ComparisonV5Adapter

comparison_v5_route.js  [depends on ComparisonV5Adapter]
  ├── RM_COMPARE_V5_CANONICAL (private)
  ├── SHELL_FRAGMENT
  └── window.ComparisonV5Route
        ├── shouldRenderCanonicalShell / renderShellHtml
        ├── syncRouteChrome
        ├── hydrateCanonical / hydrateShadow

app_shell.html (main script) — compare-only
  ├── screenCompare() → ComparisonV5Route
  ├── mountComparisonV5Route() → ComparisonV5Route.syncRouteChrome
  ├── buildComparisonV5HydrationContext()
  ├── hydrateComparisonColumns() → hydrateCanonical | hydrateShadow
  ├── initComparisonWorkspace() → hydrateCanonical (DOM branch)
  └── wireComparisonPlaceToggleButtons() → hydrateCanonical (DOM branch)

Profile / Relocated / Map / Settings / renderNav → no V5 symbols
```

## Delete-safety

Removing the two plugin script tags leaves all non-compare routes bootable.
