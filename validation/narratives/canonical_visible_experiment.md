# Canonical Visible Experiment Validation

Date: 2026-05-22

## Scope

Phase 1.9 adds the first visible canonical rendering experiment behind an explicit debug flag:

```text
?canonicalVisible=1
```

Default production behavior remains unchanged. Without the flag, `map_CURRENT.html` renders only the legacy `/search-regions` output and makes no visible canonical layer.

## Why This Is Debug-Only

The canonical layer is not a production migration. It is a small visual probe that paints the existing canonical dry-run sample points into a separate Leaflet layer. It does not replace legacy polygons or aspect lines, does not hide legacy output, and does not become the active renderer.

## Difference From Production Migration

Production migration would require a full viewport canonical renderer, visual review thresholds, popup truth integration, interaction validation, and a clear replacement decision. This phase only proves that canonical mask data can be drawn visibly in the production host without contaminating the legacy render path.

## Visual Questions It Begins To Answer

- Can canonical classified points appear in the expected map location?
- Can canonical output coexist with legacy overlays without replacing them?
- Can debug-only canonical paint stay isolated in its own layer?
- Does the production host remain stable while canonical output is visible?

## What Remains Unproven

- Full viewport canonical coverage.
- Pixel-level parity or intentional divergence from legacy polygons.
- Visual readability at production density.
- Popup truth behavior on canonical pixels.
- Cache/scheduler performance.
- Any aura, gradient, animation, or aesthetic treatment.

## Rollback

Rollback removes `ENABLE_CANONICAL_VISIBLE_DEBUG`, `canonicalVisibleDebugLayer`, `renderCanonicalVisibleDebug()`, related smoke-state fields, smoke assertions for `?canonicalVisible=1`, and this narrative. The legacy renderer, dry-run comparison path, and `/search-regions` route remain intact.
