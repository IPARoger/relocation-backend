# RESULT: 12_sb-12-validation-reports

**Roadmap ID:** SB-12
**Author:** Cursor (execution half)
**Date:** 2026-06-18

## Objective

List filenames under `validation/reports/*.json`. Read-only.

## Summary

| Metric | Value |
|--------|------:|
| JSON report files | 55 |

**Finding:** `validation/reports/` exists and contains **55** `.json` files.

## Inventory

1. `angle_sign_api_validation.json`
2. `angle_sign_frontend_validation.json`
3. `async_overlay_decoupling_check.json`
4. `house_789_async_overlay_check.json`
5. `map_current_aura_debug_smoke.json`
6. `map_current_smoke.json`
7. `phase2_34_visible_qa.json`
8. `phase2_36_aspect_band_bounds.json`
9. `phase2_36_aspect_band_targets.json`
10. `phase2_36b_aspect_band_continuity.json`
11. `phase2_36c_truth_aspect_band_bounds.json`
12. `phase2_36d_truth_dynamic_side_caps.json`
13. `phase2_36e_truth_dynamic_band_caps.json`
14. `phase2_36f_truth_dynamic_polygon_renderer.json`
15. `phase2_37_aspect_band_gradient_study.json`
16. `phase2_38_boundary_parametric_pressure.json`
17. `phase2_39_structural_pressure_topology.json`
18. `phase2_39b_structural_pressure_refined.json`
19. `phase2_39c_unified_pressure_topology.json`
20. `phase2_39d_compressed_pressure_topology.json`
21. `phase2_39e_continuous_pressure_membrane.json`
22. `phase2_39f_unified_pressure_body.json`
23. `phase2_40_reference_pressure_render.json`
24. `phase2_41_transfer_function_study.json`
25. `phase2_41b_density_retention_transfer_study.json`
26. `phase2_41d_locked_transfer_reference.json`
27. `phase2_42_locked_transfer_geometry.json`
28. `phase2_43_orthogonal_transport.json`
29. `phase2_44_locked_material_strip_transport.json`
30. `phase2_45_asymmetric_transport_proof.json`
31. `phase2_46_multicolor_validation_board.json`
32. `phase2_48_extreme_asymmetry_stress.json`
33. `phase2_52_map_overlap_sandbox.json`
34. `phase2_cache_smoke.json`
35. `phase3_27_probe_against_phase3_26.json`
36. `phase3_27_probe_against_phase3_26_dynamic.json`
37. `phase3_27_probe_against_phase3_26_v2.json`
38. `phase3_28_true_discovery_sim_metrics.json`
39. `phase3_29_hostile_solver_validation.json`
40. `phase3_30_minimal_migration_core.json`
41. `phase3_30_self_audit.json`
42. `phase3_32_geometry_diversification_audit.json`
43. `phase3_33_alignment_metric_deconstruction.json`
44. `phase3_35_black_box_acceptance_against_current.json`
45. `relocated_truth_field_benchmark.json`
46. `served_truth_grid_debug_url_check.json`
47. `sprint_dc_ic_validation.json`
48. `staged_asc_overlay_browser_check.json`
49. `staged_asc_shared_grid_equivalence.json`
50. `task53_smoke_run.json`
51. `truth_grid_boundary_refine_validation.json`
52. `truth_grid_frontend_integration_check.json`
53. `truth_grid_house_overlay_payload_reduction.json`
54. `truth_grid_integration_summary.json`
55. `truth_grid_integration_validation.json`

## Files changed

- `relay-sandbox/results/12_sb-12-validation-reports.md` (this closeout only)
- No changes to `validation/reports/` or any other source files.

## Validation evidence

```text
$ test -d validation/reports && echo 'validation/reports exists' || echo 'validation/reports MISSING'
validation/reports exists

$ ls -1 validation/reports/*.json | wc -l
      55

$ ls -1 validation/reports/*.json | xargs -n1 basename | sort
angle_sign_api_validation.json
angle_sign_frontend_validation.json
async_overlay_decoupling_check.json
house_789_async_overlay_check.json
map_current_aura_debug_smoke.json
map_current_smoke.json
phase2_34_visible_qa.json
phase2_36_aspect_band_bounds.json
phase2_36_aspect_band_targets.json
phase2_36b_aspect_band_continuity.json
phase2_36c_truth_aspect_band_bounds.json
phase2_36d_truth_dynamic_side_caps.json
phase2_36e_truth_dynamic_band_caps.json
phase2_36f_truth_dynamic_polygon_renderer.json
phase2_37_aspect_band_gradient_study.json
phase2_38_boundary_parametric_pressure.json
phase2_39_structural_pressure_topology.json
phase2_39b_structural_pressure_refined.json
phase2_39c_unified_pressure_topology.json
phase2_39d_compressed_pressure_topology.json
phase2_39e_continuous_pressure_membrane.json
phase2_39f_unified_pressure_body.json
phase2_40_reference_pressure_render.json
phase2_41_transfer_function_study.json
phase2_41b_density_retention_transfer_study.json
phase2_41d_locked_transfer_reference.json
phase2_42_locked_transfer_geometry.json
phase2_43_orthogonal_transport.json
phase2_44_locked_material_strip_transport.json
phase2_45_asymmetric_transport_proof.json
phase2_46_multicolor_validation_board.json
phase2_48_extreme_asymmetry_stress.json
phase2_52_map_overlap_sandbox.json
phase2_cache_smoke.json
phase3_27_probe_against_phase3_26.json
phase3_27_probe_against_phase3_26_dynamic.json
phase3_27_probe_against_phase3_26_v2.json
phase3_28_true_discovery_sim_metrics.json
phase3_29_hostile_solver_validation.json
phase3_30_minimal_migration_core.json
phase3_30_self_audit.json
phase3_32_geometry_diversification_audit.json
phase3_33_alignment_metric_deconstruction.json
phase3_35_black_box_acceptance_against_current.json
relocated_truth_field_benchmark.json
served_truth_grid_debug_url_check.json
sprint_dc_ic_validation.json
staged_asc_overlay_browser_check.json
staged_asc_shared_grid_equivalence.json
task53_smoke_run.json
truth_grid_boundary_refine_validation.json
truth_grid_frontend_integration_check.json
truth_grid_house_overlay_payload_reduction.json
truth_grid_integration_summary.json
truth_grid_integration_validation.json
```

## Rollback command

```bash
rm relay-sandbox/results/12_sb-12-validation-reports.md
```

## Rejected scope

- Modifying, adding, or deleting files under `validation/reports/` (task scope: read-only inventory).
- Schema, backend, database, secrets, migration, or renderer/math/overlay changes (not required; not attempted).
- Opening a PR (not requested).

## VERIFIED

Read-only validation-reports audit complete: **55** `.json` filenames listed under `validation/reports/`; no other artifacts modified.
