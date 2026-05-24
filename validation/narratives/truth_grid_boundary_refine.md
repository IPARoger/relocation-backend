# Truth Grid Boundary Refinement Validation

## Status

Validation pass created for the uncommitted `truth_grid_engine.py` boundary-refinement change.

Classification: accepted production truth-grid improvement.

This is validation evidence only. It does not touch Phase 2.25, production UI, `map_CURRENT.html`, scheduler/cache systems, aura systems, account/auth/persistence, or backend endpoint behavior.

---

## Purpose

`truth_grid_engine.py` now supports boundary refinement for `/search-regions` truth-grid output when `truth_grid_boundary_refine=true`.

The validation goal is to determine whether the default refined path improves polygon truth without contradicting point truth, destabilizing metadata, or introducing an obvious performance danger.

---

## Validation Artifacts

- Script: `scripts/validate_truth_grid_boundary_refine.py`
- Report: `validation/reports/truth_grid_boundary_refine_validation.json`
- Existing smoke evidence: `scripts/validate_sprint_dc_ic.py`

---

## Cases Covered

The validation compares `/search-regions` with `truth_grid_boundary_refine=false` and `truth_grid_boundary_refine=true` for:

- planet-in-house truth-grid output,
- angle-sign truth-grid output,
- baseline world controls,
- Greenland/Iceland high-latitude-adjacent probes,
- seam/dateline-adjacent controls,
- DC angle-sign spot checks,
- IC angle-sign spot checks.

Probe points are checked against `/relocated-chart` point truth.

---

## Results Summary

Overall validation passed.

The refined output preserved point-truth consistency across all selected probes. The high-north Sun-in-1st case includes a meaningful improvement: an unrefined polygon included the Greenland/Iceland gap probe even though point truth classified the Sun in house 2. The refined polygon excluded that probe, matching point truth.

No refined feature set reported `validation_contradictions`.

Existing DC/IC backend smoke passed after this validation pass.

---

## Metadata Behavior

Metadata was present and intelligible for refined and unrefined requests:

- `boundary_refine` reflected the request flag.
- `merge_step` changed from `0.75` to `0.375` on refined output.
- `refine_samples` was `0` for unrefined requests and nonzero for refined requests.
- `coarse_resolution` was present on polygon feature properties.
- `boundary_refined` was set on refined polygon feature properties.

The report records feature counts, polygon counts, request time, sample counts, merge timing, and contradiction counts per case.

---

## Performance Notes

The final run did not show an obvious performance danger.

Observed refined requests were slower and generally produced more polygon features, which is expected because boundary cells are resampled and merged at a finer step. The final validation run showed roughly:

- baseline Sun house: 142 to 277 features, about 1.18x elapsed time,
- high-north Sun house: 137 to 280 features, about 2.07x elapsed time,
- baseline DC Cancer: 143 to 288 features, about 2.67x elapsed time,
- high-north IC Cancer: 1 to 1 feature, about 2.64x elapsed time.

This is acceptable for the tested cases, but larger multi-condition production payloads should continue to be monitored.

---

## Production Smoke Implications

This change affects default `/search-regions` truth-grid output when callers use `truth_grid_boundary_refine=true`, including the current default request model.

The lightweight production-adjacent smoke `scripts/validate_sprint_dc_ic.py` passed. The map browser smoke was inspected as a catastrophic renderer gate; it delegates backend parity to `validate_sprint_dc_ic.py` and does not appear to assert fixed truth-grid geometry counts.

No production UI behavior was edited during this pass.

---

## Recommendation

Accept and commit `truth_grid_engine.py` as a production truth-grid improvement, together with this dedicated validation script, report, and narrative.

This should remain separate from Phase 2.25.

---

## Exact Commit Plan If Accepted

Stage only:

- `truth_grid_engine.py`
- `scripts/validate_truth_grid_boundary_refine.py`
- `validation/reports/truth_grid_boundary_refine_validation.json`
- `validation/narratives/truth_grid_boundary_refine.md`
- optionally `validation/reports/sprint_dc_ic_validation.json` if preserving the rerun smoke report is desired

Recommended commit message:

`Validate truth grid boundary refinement`

Do not stage:

- `map_CURRENT.html`
- Phase 2.25 files,
- Phase 2 sandbox files,
- Phase 2.24 contract files,
- scheduler/cache files,
- aura files,
- production UI files,
- unrelated generated screenshots or archaeology files.

---

## Rollback Or Quarantine Plan If Not Accepted

If later evidence rejects the change, revert or quarantine only the uncommitted boundary-refinement changes in `truth_grid_engine.py` with explicit approval.

Keep the validation artifacts useful as evidence by either:

- retaining them as a failed validation record with classification changed to the observed failure, or
- moving them into a quarantine/archive path in a separate cleanup pass.

Do not silently restore the previous truth-grid behavior without recording why, because the refined path fixed at least one observed high-north polygon/point-truth mismatch.

---

## Documentation Recommendations

`CURRENT_RENDERING_DOCTRINE.md` should be updated if this change is accepted, because the default `/search-regions` truth-grid production path now uses boundary refinement as part of truth-preserving polygon generation.

`DEFERRED_EXCELLENCE_REGISTRY.md` does not need an update for acceptance. This is not deferred excellence; it is a validated production truth-grid improvement. A future performance guard or broader multi-condition benchmark may be tracked separately if needed.

A product roadmap note is optional. If added, it should be a small production-truth validation note, not a Phase 2.25 integration note.

This validation narrative was created because the change affects default production truth-grid output and needs durable evidence before commit.
