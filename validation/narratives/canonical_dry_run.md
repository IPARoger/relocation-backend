# Canonical Dry-Run Validation

Date: 2026-05-22

## Scope

Phase 1.7 allows `map_CURRENT.html` to issue a canonical `/screen-pixel-truth` request in shadow mode only. The visible production renderer remains locked to:

```text
legacy_search_regions
```

The dry-run gate is disabled by default:

```text
ENABLE_CANONICAL_DRY_RUN = false
```

It is enabled only with `?canonicalDryRun=1`.

## What Shadow Mode Means

Shadow mode means the canonical request may execute and its response shape may be inspected, but the canonical response is not returned to the visible renderer. The dispatch path always returns the legacy `/search-regions` response for production drawing.

The dry-run records only a small summary in smoke/debug state: status, HTTP status, point count, condition count, mask count, response point count, and `rendered: false`.

## Why Canonical Output Is Invisible

This phase is a validation/comparison step, not a migration. Painting canonical output would mix two instability sources: request-path validation and visible rendering semantics. Keeping canonical output invisible lets the project prove that `/screen-pixel-truth` can be reached from the production host without changing overlays, colors, layer ordering, popup truth, cache state, or user-facing behavior.

## Why This Phase Exists

The dry-run path measures whether the production host can construct a minimal canonical request from the same birth and condition context used by legacy rendering. It also confirms that canonical execution can be observed without substrate switching, hidden fallback behavior, or state contamination.

## Risks Being Measured

- Request-shape compatibility with `/screen-pixel-truth`.
- Response-shape validity (`masks` count matches requested points).
- Accidental visible rendering of canonical data.
- Accidental production substrate switching.
- Accidental scheduler/cache coupling.
- Console/runtime errors from the shadow path.

## Intentionally Isolated

- Visible rendering remains `/search-regions` only.
- Canonical data is not painted.
- Canonical data is not cached.
- Scheduler and Phase-2 cache remain sandbox-only.
- Overlay colors, geometry semantics, popup behavior, aura, reveal, animation, and astrology math are unchanged.

## Rollback

Rollback removes the `ENABLE_CANONICAL_DRY_RUN` gate, `runCanonicalDryRun()`, the dry-run summary state, the smoke assertions for `?canonicalDryRun=1`, and this narrative. The active legacy renderer and dispatch substrate remain intact.
