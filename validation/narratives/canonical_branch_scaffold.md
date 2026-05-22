# Canonical Branch Scaffold Validation

Date: 2026-05-22

## Scope

Phase 1.6 extends the renderer dispatch scaffold so the future canonical substrate has a named branch:

```text
canonical_screen_space
```

The active production substrate remains:

```text
legacy_search_regions
```

## Why The Branch Exists

The production migration needs an explicit place where canonical screen-space rendering will eventually be wired. Naming the branch now makes the future switch visible and reviewable instead of allowing hidden route selection or automatic fallback behavior to appear later.

## Why It Is Blocked

The canonical branch intentionally throws before any network request. It does not call `/screen-pixel-truth`, does not classify points, does not render masks, and does not alter the current legacy overlay flow.

This preserves the rule that production migration has not begun. The branch is detectable for validation, but inactive for behavior.

## Why Explicitness Matters

The dispatch layer now recognizes two possible substrates:

- `legacy_search_regions`: active, production route, delegates to `/search-regions`.
- `canonical_screen_space`: known future route, hard-blocked until an explicit migration phase activates it.

There is no hidden switching, no fallback from canonical to legacy, and no automatic use of `/screen-pixel-truth`.

## Future Activation Step

The first true migration phase should replace the hard-blocked canonical branch with a separately validated adapter call that prepares a canonical screen-space request. That phase must remain its own instability source and should not add cache, scheduler integration, aura styling, reveal animation, or unrelated renderer cleanup.

## Rollback Simplicity

Rollback is limited to removing the `canonical_screen_space` identifier, the blocked branch in `dispatchOverlayRequest()`, the smoke assertion that probes the branch, and this narrative. The active legacy route remains unchanged, so rollback does not touch astrology math, visual rendering, cache behavior, or backend schemas.
