# Phase 2.44b - Texture Compression Refinement

The accepted texture-coordinate transport architecture is frozen. This revision changes only the one-dimensional transported material texture.

## Frozen Invariants

- Texture-coordinate transport is unchanged.
- Local `(s,u)` sampling is unchanged.
- Orthogonal strip transport is unchanged.
- Strip topology and width logic are unchanged.
- Curved geometry is unchanged.
- Sample-cut QA overlays are unchanged.
- RGB-only rendering remains the model.

## Texture-Only Correction

The prior strip preserved cross-sectional identity but still had too much soft residency around the ridge. This pass narrows the darkest tonal residency near `u=0.5`, increases local compression immediately adjacent to the ridge, reduces lingering mid-blue residency, and accelerates early release while preserving the pale edge timing.

No blur, glow, gaussian smoothing, alpha-distance falloff, spline-distance opacity, feathering, post-processing, separate ridge stroke, geometry redesign, or transport redesign was introduced.

## Outputs

- `validation/visual_targets/phase2_44_locked_material_strip_transport.png`
- `validation/visual_targets/phase2_44_tightened_material_texture_control.png`
- `validation/reports/phase2_44_locked_material_strip_transport.json`
- `validation/narratives/phase2_44_locked_material_strip_transport.md`

## QA Invariant

At every orthogonal cut, the curved strip should preserve the same compressed material identity as the straight strip. The target read is a compressed enamel material strip bent through space, not a soft blue glow around a curve.
