# Phase 2.36b — Aspect Band Boundary Continuity

## Purpose

Phase 2.36b creates a standalone static visual target for the corrected fixed-spine side-width continuity proof.

The prior 2.36b attempt is not approved because it still read as general ribbon/range morphing rather than independent side-width measurement from a fixed centerline.

The corrected goal is to prove independent left/right boundary distances measured perpendicularly from a fixed dashed exactness spine.

Two separate cases are required:

- **Case A:** the left/9th-house side shrinks from `10 -> 6 -> 3 -> 2.5` while the right/10th-house side remains `10`.
- **Case B:** the right/10th-house side shrinks from `10 -> 6 -> 3 -> 2.5` while the left/9th-house side remains `10`.

This is a continuity proof, not production truth rendering.

## Artifacts

- `validation/visual_targets/phase2_36b_aspect_band_continuity.html`
- `validation/visual_targets/phase2_36b_aspect_band_continuity_caseA.png`
- `validation/visual_targets/phase2_36b_aspect_band_continuity_caseB.png`
- `validation/reports/phase2_36b_aspect_band_continuity.json`

## Scope

This artifact is boundary/mask-only.

It uses:

- flat neutral fill,
- smooth continuous outer boundaries,
- a fixed dashed centerline in both cases,
- perpendicular measurement ticks from the centerline to each boundary,
- direct width callouts at four positions,
- independently changing side widths measured from the centerline,
- visible lopsided geometry around the centerline,
- separate Case A and Case B panels,
- map-like labels/background for scale.

It does not use:

- gradient fill,
- rain,
- virga,
- dots,
- particles,
- blur,
- feathering,
- aura color,
- animation,
- production truth claim,
- production code,
- renderer integration,
- `map_CURRENT.html` changes.

## Relationship to Phase 2.36 Boundary Masks

The existing Phase 2.36 boundary-mask artifacts are suitable as approved proportional boundary proofs only.

They are schematic placeholders.

They are not numerically derived from intended truth/map geometry.

They are not validated geographic truth extents.

The first colored Phase 2.36 aspect-band targets remain rejected/not approved.

## Truth Status

The Phase 2.36b continuity artifact is schematic proportional geometry only.

It is not truth-derived.

It is not truth-derived geographic extent.

It is not production truth rendering.

It is not a claim about real ASC/aspect-band geographic extents.

Its only purpose is to prove independent left/right boundary distances from the fixed centerline.

## Governance Rule

Boundary continuity and mask geometry must be approved before color-gradient work continues.

Future gradient work should fill the approved mask rather than trying to create geometry by blurring a centerline.

After the mask and continuity behavior are approved, a separate gradient pass should test:

- centerline width,
- centerline opacity,
- falloff curve,
- middle-gradient behavior,
- outer-edge translucency.

## Result

The report records mechanical checks as passing:

- boundary/mask-only,
- continuous outer boundaries,
- Case A present,
- Case B present,
- Case A labels `left 10 / right 10`, `left 6 / right 10`, `left 3 / right 10`, and `left 2.5 / right 10`,
- Case B labels `left 10 / right 10`, `left 10 / right 6`, `left 10 / right 3`, and `left 10 / right 2.5`,
- fixed dashed centerline in both cases,
- measurement ticks/callouts visible in both cases,
- smooth outer boundaries in both cases,
- no symmetric whole-corridor narrowing,
- no visual recentering of the centerline,
- no disallowed particle elements,
- neutral flat fill,
- not production truth rendering,
- proportional boundary proof only.

Human review is still required before this becomes an approved geometry target for later gradient work.

## Rollback Scope

Rollback is limited to deleting:

- the continuity HTML artifact,
- the Case A PNG,
- the Case B PNG,
- the continuity JSON report,
- this narrative.

No production code, backend behavior, renderer behavior, `truth_grid_engine.py`, scheduler/cache execution, aura implementation, smoke file, roadmap file, sandbox/prototype file, unrelated file, validation report outside the allowed output, or `map_CURRENT.html` behavior was changed.
