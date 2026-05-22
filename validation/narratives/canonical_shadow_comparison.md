# Canonical Shadow Comparison Validation

Date: 2026-05-22

## Scope

Phase 1.8 extends canonical dry-run mode so `map_CURRENT.html` can collect comparison metrics between the visible legacy `/search-regions` response and an invisible `/screen-pixel-truth` shadow response. The user still sees only the legacy renderer.

## Visual Identity Is Not The Goal

The legacy path returns GeoJSON features: polygons and linework shaped by the historical overlay renderer. The canonical path returns point masks from explicit truth classification. These are different substrates, so visual identity with legacy is not the standard for this phase.

The goal is truth continuity and artifact reduction: prove the production host can ask the canonical substrate the same chart/condition question, receive a valid response, and keep it isolated until a later visible rendering experiment maps masks into screen output.

## Metrics Collected

The dry-run summary records:

- Legacy success/schema status.
- Legacy feature count.
- Legacy generation mode.
- Legacy request elapsed time.
- Canonical HTTP/status result.
- Canonical point count.
- Canonical condition count.
- Canonical mask count.
- Canonical matched/occupied count.
- Canonical response point count.
- Canonical request elapsed time.
- Schema mismatch flags for both paths.
- Visible renderer substrate.
- `canonicalRendered: false`.

## What Remains Unproven

- Pixel-level parity between legacy polygons and canonical masks.
- User-facing readability of canonical output.
- Canonical layer composition and color semantics.
- Popup truth integration against visible canonical pixels.
- Cache/scheduler behavior for canonical production requests.
- Performance at full viewport density.

## Future Visible Migration Must Prove

The first visible canonical experiment must prove that canonical masks can be painted without changing astrology math, without hiding uncertainty, and without regressing popup truth or map interaction. It must also define explicit visual review artifacts and acceptance thresholds before replacing legacy rendering.

## Isolation Guarantees

- Legacy `/search-regions` remains the only visible renderer.
- Canonical output is not painted to the map.
- Canonical output is not cached.
- Scheduler integration remains absent.
- No aura, animation, gradients, or aesthetic comparison is introduced.
- No hidden fallback or automatic substrate switching exists.

## Rollback

Rollback removes the comparison summaries from `runCanonicalDryRun()`, the smoke assertions for comparison metrics, and this narrative. The dry-run gate and legacy renderer can remain independently intact.
