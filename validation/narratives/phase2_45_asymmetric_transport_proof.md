# Phase 2.46B - Mid-Body Rebalancing

This validation-only pass updates the existing Phase 2.45 asymmetric transport proof outputs. Phase 2.46A surface coherence is accepted; this revision changes only the one-dimensional material tonal distribution.

## Tonal Changes

The release into pale edges was occurring too early, leaving too much near-white territory and not enough material mass in the outer mids. This pass delays the final pale range and expands restrained blue residency across the outer body while preserving the narrow ridge hierarchy and faster compression near the ridge.

This is not a return to the earlier diffuse versions. The goal remains compressed enamel behavior, not atmospheric softness.

## Frozen Invariants

- Local `(s,u)` texture-coordinate transport
- Independent side normalization
- Asymmetry handling
- Orthogonal cross-section identity
- Strip width logic
- Straight and curved geometry cases
- Sample-cut QA logic
- RGB-only rendering model

## QA Inspection

- Ridge width: preserved; no deliberate ridge widening introduced.
- Premature whitening: reduced by making the final pale range thinner and later.
- Lingering haze: not intentionally increased; the outer body carries more subdued blue rather than pale fog.
- Broken material continuity: no broken cross-section continuity observed.
- Asymmetry correctness: Case A fixed asymmetry and Case B dynamic asymmetry still pass with independent side-local normalization.

## Status

The material reads denser and more present than Phase 2.46A while remaining restrained. No transport redesign, geometry changes, effects, post-processing, map integration, production changes, staging, or commit work was performed.
