# Canonical Viewport-Density Debug Validation

Date: 2026-05-22

## Scope

Phase 1.10 expands the explicit `?canonicalVisible=1` experiment from a tiny five-point probe to a coarse viewport-density screen-space sample. Default production remains unchanged:

- Active substrate: `legacy_search_regions`
- Visible production renderer: `/search-regions`
- Default `/screen-pixel-truth` calls: none

## Debug Block Size

The canonical debug layer samples the visible viewport at a coarse block size:

```text
canonicalBlock=12
```

The query parameter can override this value, clamped to a conservative debug range. Full `1px` rendering is intentionally deferred.

## Why Coarse Blocks

Coarse blocks make the first viewport-scale comparison inspectable without pretending to be production quality. They keep request size bounded, make individual sampled cells visible, and avoid mixing this phase with adaptive refinement, cache integration, or visual polish.

## What This Starts Answering

- Whether canonical screen-space samples cover the visible viewport.
- Whether canonical blocks align spatially with the map container.
- Whether canonical output can coexist with legacy overlays without replacing them.
- Whether basic counts and timing stay observable in smoke/debug state.

## What Remains Unproven

- Full `1px` canonical rendering.
- Adaptive refinement.
- Pixel-level parity or acceptance thresholds.
- Popup truth on canonical pixels.
- Production performance under dense interaction.
- Cache/scheduler integration.
- Any aura, gradient, animation, or aesthetic treatment.

## Isolation Guarantees

The canonical viewport-density layer is drawn only on a separate debug canvas under `?canonicalVisible=1`. It does not alter the legacy polygon/aspect layers, does not hide legacy overlays, does not switch the active renderer, and does not introduce hidden fallback behavior.

## Manual Inspection

Open:

```text
http://127.0.0.1:8000/map_CURRENT.html?skipOnboarding=1&canonicalVisible=1
```

Optional block override:

```text
http://127.0.0.1:8000/map_CURRENT.html?skipOnboarding=1&canonicalVisible=1&canonicalBlock=8
```

Click `Find regions`. The map should show normal legacy overlays plus a coarse translucent canonical debug grid.

## Rollback

Rollback removes viewport grid construction, the canonical debug canvas paint path, `canonicalBlock` handling, smoke assertions for viewport-density metrics, and this narrative. The legacy renderer and dry-run comparison path remain independently reversible.
