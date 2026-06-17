# Document Comprehensiveness and Omission Report

## Scope

- Active code dump parsed: `ACTIVE_CODEBASE_DUMP.txt`
- Code files found: 10
- Generated manuals present and searched: 10
  - `BACKEND_ENGINE_ARCHITECTURE.md` (223.0 KB)
  - `SYSTEM_BOUNDARIES_AND_CANONS.md` (217.3 KB)
  - `ARCHITECTURE_AND_BACKEND_CANON.md` (1691.0 KB)
  - `MASTER_PROJECT_PROFILE.md` (88.0 KB)
  - `FOUNDATIONAL_CONSTITUTION.md` (202.1 KB)
  - `CORE_CONCEPTS_AND_LAYERS.md` (206.2 KB)
  - `INTERFACE_AND_DESIGN_CANON.md` (111.0 KB)
  - `GOVERNANCE_AND_PROTOCOL_CANON.md` (187.3 KB)
  - `AI_SYSTEMS_AND_PROMPT_PROTOCOLS.md` (186.5 KB)
  - `FUTURE_FEATURES_ROADMAP.md` (253.8 KB)
- Extracted active-code symbols/contracts: 1137
- AST parse warnings: 1

## Coverage Summary

- missing: 618
- documented_exact: 361
- weak_field_only: 78
- weak_variant: 75
- documented_contextual: 5

## Coverage by Symbol Type

| Kind | Exact | Contextual | Weak | Missing | Total |
|---|---:|---:|---:|---:|---:|
| class | 4 | 0 | 0 | 22 | 26 |
| code_contract_term | 15 | 0 | 10 | 39 | 64 |
| constant | 9 | 0 | 3 | 38 | 50 |
| endpoint | 11 | 0 | 16 | 18 | 45 |
| function | 22 | 0 | 8 | 138 | 168 |
| json_key | 300 | 0 | 31 | 273 | 604 |
| model_field | 0 | 5 | 85 | 90 | 180 |

## Verdict

The generated manuals are **not 100% comprehensive by exact active-code name**. They document the major architecture, but the active code contains exact endpoint fields, JSON keys, constants, and debug/cache/refinement contracts that are either missing or only weakly represented by name.

## High-Priority Missing Items to Add

### `./add_endpoint.py`
- **endpoint** `/relocation-chart` — POST

### `./main_centerline_FIXER.py`
- **endpoint** `/aspect-orb-at-point` — GET
- **endpoint** `/aura-field` — POST
- **endpoint** `/aura-raster-adaptive` — POST
- **endpoint** `/aura-raster-convergence` — POST
- **endpoint** `/aura-refinement-reveal-stages` — GET
- **endpoint** `/chart-profiles` — GET
- **endpoint** `/chart-records` — GET
- **endpoint** `/chart-records/{chart_record_id}` — GET
- **endpoint** `/chart-records/{chart_record_id}/engine-birth` — GET
- **endpoint** `/library/active` — POST
- **endpoint** `/library/charts` — POST
- **endpoint** `/library/charts/{chart_id}` — DELETE
- **endpoint** `/library/charts/{chart_id}/favorite` — POST
- **endpoint** `/library/settings` — PUT
- **endpoint** `/library/state` — GET
- **endpoint** `/library/views` — POST
- **endpoint** `/library/views/{view_id}` — DELETE
- **model_field** `AuraAdaptiveRasterRequest.birth_day` — int default=
- **model_field** `AuraAdaptiveRasterRequest.birth_hour_utc` — float default=
- **model_field** `AuraAdaptiveRasterRequest.birth_month` — int default=
- **model_field** `AuraAdaptiveRasterRequest.birth_year` — int default=
- **model_field** `AuraAdaptiveRasterRequest.gradient_tolerance` — float default=0.06
- **model_field** `AuraAdaptiveRasterRequest.include_convergence_metrics` — bool default=True
- **model_field** `AuraAdaptiveRasterRequest.include_debug_cells` — bool default=True
- **model_field** `AuraAdaptiveRasterRequest.include_reveal_transport` — bool default=False
- **model_field** `AuraAdaptiveRasterRequest.initial_divisions` — int default=6
- **model_field** `AuraAdaptiveRasterRequest.max_depth` — int default=6
- **model_field** `AuraAdaptiveRasterRequest.max_leaves` — int default=12000
- **model_field** `AuraAdaptiveRasterRequest.max_orb` — float default=6.0
- **model_field** `AuraAdaptiveRasterRequest.max_samples` — int default=120000
- **model_field** `AuraAdaptiveRasterRequest.min_cell_deg` — float default=0.035
- **model_field** `AuraAdaptiveRasterRequest.paint_height` — int default=
- **model_field** `AuraAdaptiveRasterRequest.paint_width` — int default=
- **model_field** `AuraAdaptiveRasterRequest.refinement_stage_id` — str | None default=None
- **model_field** `AuraConvergenceRasterRequest.birth_day` — int default=
- **model_field** `AuraConvergenceRasterRequest.birth_hour_utc` — float default=
- **model_field** `AuraConvergenceRasterRequest.birth_month` — int default=
- **model_field** `AuraConvergenceRasterRequest.birth_year` — int default=
- **model_field** `AuraConvergenceRasterRequest.convergence_delta_threshold` — float default=CONVERGENCE_DELTA_THRESHOLD
- **model_field** `AuraConvergenceRasterRequest.include_debug_cells` — bool default=True
- **model_field** `AuraConvergenceRasterRequest.include_pass_history` — bool default=True
- **model_field** `AuraConvergenceRasterRequest.include_pixel_attribution_sample` — bool default=False
- **model_field** `AuraConvergenceRasterRequest.initial_divisions` — int default=4
- **model_field** `AuraConvergenceRasterRequest.max_leaves` — int default=12000
- **model_field** `AuraConvergenceRasterRequest.max_orb` — float default=6.0
- **model_field** `AuraConvergenceRasterRequest.max_passes` — int default=64
- **model_field** `AuraConvergenceRasterRequest.max_samples` — int default=120000
- **model_field** `AuraConvergenceRasterRequest.min_cell_deg` — float default=0.035
- **model_field** `AuraConvergenceRasterRequest.overshoot_guard` — bool default=True
- **model_field** `AuraConvergenceRasterRequest.paint_height` — int default=
- **model_field** `AuraConvergenceRasterRequest.paint_width` — int default=
- **model_field** `AuraConvergenceRasterRequest.per_pass_sample_budget` — int default=2000
- **model_field** `AuraConvergenceRasterRequest.pixel_attribution_sample_cap` — int default=4000
- **model_field** `AuraConvergenceRasterRequest.target_pixels_above_threshold_pct` — float default=0.0
- **model_field** `AuraFieldRequest.birth_day` — int default=
- **model_field** `AuraFieldRequest.birth_hour_utc` — float default=
- **model_field** `AuraFieldRequest.birth_month` — int default=
- **model_field** `AuraFieldRequest.birth_year` — int default=
- **model_field** `AuraFieldRequest.include_debug_points` — bool default=False
- **model_field** `AuraFieldRequest.max_orb` — float default=6.0
- **model_field** `AuraFieldRequest.min_strength` — float default=0.04
- **model_field** `AuraRasterRequest.birth_day` — int default=
- **model_field** `AuraRasterRequest.birth_hour_utc` — float default=
- **model_field** `AuraRasterRequest.birth_month` — int default=
- **model_field** `AuraRasterRequest.birth_year` — int default=
- **model_field** `AuraRasterRequest.max_orb` — float default=6.0
- **model_field** `BruteForceGridRequest.birth_day` — int default=
- **model_field** `BruteForceGridRequest.birth_hour_utc` — float default=
- **model_field** `BruteForceGridRequest.birth_month` — int default=
- **model_field** `BruteForceGridRequest.birth_year` — int default=
- **model_field** `BruteForceGridRequest.grid_deg` — float default=
- **model_field** `BruteForceGridRequest.include_non_matches` — bool default=False
- **model_field** `BruteForceGridRequest.target_house` — int | None default=None
- **model_field** `BruteForceGridRequest.target_planet` — str | None default=None
- **model_field** `ClassifyPointsRequest.birth_day` — int default=
- **model_field** `ClassifyPointsRequest.birth_hour_utc` — float default=
- **model_field** `ClassifyPointsRequest.birth_month` — int default=
- **model_field** `ClassifyPointsRequest.birth_year` — int default=
- **model_field** `ScreenPixelTruthRequest.birth_day` — int default=
- **model_field** `ScreenPixelTruthRequest.birth_hour_utc` — float default=
- **model_field** `ScreenPixelTruthRequest.birth_month` — int default=
- **model_field** `ScreenPixelTruthRequest.birth_year` — int default=
- **model_field** `SearchRequest.aspect_resolution` — float default=0.5
- **model_field** `SearchRequest.birth_day` — int default=
- **model_field** `SearchRequest.birth_hour_utc` — float default=
- **model_field** `SearchRequest.birth_month` — int default=
- **model_field** `SearchRequest.birth_year` — int default=
- **model_field** `SearchRequest.overlay_stage` — str | None default=None
- **model_field** `SearchRequest.return_all_houses` — bool default=False

### `./aura_field_engine.py`
- **code_contract_term** `PRODUCT_LAT_CAP` — count=12
- **code_contract_term** `max_leaves` — count=11
- **code_contract_term** `max_samples` — count=19
- **code_contract_term** `overshoot_guard` — count=7
- **code_contract_term** `per_pass_sample_budget` — count=6

### `./main_centerline_FIXER.py`
- **code_contract_term** `MAX_CELLS` — count=3
- **code_contract_term** `POINT_CAP` — count=3
- **code_contract_term** `PRODUCT_LAT_CAP` — count=6
- **code_contract_term** `_ANGLE_TO_CUSP_INDEX` — count=5
- **code_contract_term** `_ASPECT_TARGET_DEG` — count=3
- **code_contract_term** `_MAX_CONDITIONS` — count=5
- **code_contract_term** `max_leaves` — count=6
- **code_contract_term** `max_samples` — count=10
- **code_contract_term** `overshoot_guard` — count=3
- **code_contract_term** `per_pass_sample_budget` — count=3
- **class** `AngleInSignCondition` — 
- **class** `AngleSignCondition` — 
- **class** `AspectToAngleCondition` — 
- **class** `AuraAdaptiveRasterRequest` — 
- **class** `AuraConvergenceRasterRequest` — 
- **class** `AuraFieldRequest` — 
- **class** `AuraRasterRequest` — 
- **class** `BruteForceGridRequest` — 
- **class** `ClassifyPointsRequest` — 
- **class** `PlanetInHouseCondition` — 
- **class** `ScreenPixelTruthRequest` — 
- **class** `SearchRequest` — 

### `./main_contours.py`
- **class** `SearchRequest` — 

### `./main_centerline_FIXER.py`
- **model_field** `LibraryActiveSelection.chart_id` — str | None default=
- **model_field** `LibrarySettingsPatch.default_substrate` — str | None default=None
- **model_field** `LibrarySettingsPatch.experimental_mode_enabled` — bool | None default=None
- **model_field** `LibrarySettingsPatch.lat_cap_label_enabled` — bool | None default=None
- **model_field** `LibrarySettingsPatch.phase2_cache_enabled` — bool | None default=None
- **model_field** `LibraryViewSave.center_lat` — float | None default=None
- **model_field** `LibraryViewSave.center_lon` — float | None default=None
- **model_field** `LibraryViewSave.chart_id` — str default=

### `./truth_field_regions.py`
- **model_field** `MergedCell.lat_max` — float default=
- **model_field** `MergedCell.lat_min` — float default=
- **model_field** `MergedCell.lon_max` — float default=
- **model_field** `MergedCell.lon_min` — float default=
- **model_field** `MergedCell.source_cell_count` — int default=

### `./truth_grid_engine.py`
- **model_field** `MergedCell.lat_max` — float default=
- **model_field** `MergedCell.lat_min` — float default=
- **model_field** `MergedCell.lon_max` — float default=
- **model_field** `MergedCell.lon_min` — float default=
- **model_field** `MergedCell.source_cell_count` — int default=

### `./aura_field_engine.py`
- **code_contract_term** `LAT_MAX` — count=2
- **code_contract_term** `LAT_MIN` — count=2
- **code_contract_term** `convergence_delta_threshold` — count=12
- **code_contract_term** `leaf_budget` — count=33
- **code_contract_term** `orb_strength_at_point` — count=5
- **code_contract_term** `signed_angle_diff` — count=3
- **code_contract_term** `target_pixels_above_threshold_pct` — count=4

### `./main_centerline_FIXER.py`
- **code_contract_term** `CLASSIFY_PRODUCT_LAT_CAP` — count=4
- **code_contract_term** `convergence_delta_threshold` — count=5
- **code_contract_term** `signed_angle_diff` — count=5
- **code_contract_term** `target_pixels_above_threshold_pct` — count=3

### `./truth_field_regions.py`
- **code_contract_term** `LAT_MAX` — count=25
- **code_contract_term** `LAT_MIN` — count=27
- **code_contract_term** `LON_MAX` — count=21
- **code_contract_term** `LON_MIN` — count=23
- **code_contract_term** `cacheHits` — count=1
- **code_contract_term** `cacheMisses` — count=1
- **code_contract_term** `cacheSamples` — count=1
- **code_contract_term** `cache_hits` — count=3
- **code_contract_term** `cache_misses` — count=5

### `./truth_grid_engine.py`
- **code_contract_term** `LAT_MAX` — count=15
- **code_contract_term** `LAT_MIN` — count=17
- **code_contract_term** `LON_MAX` — count=14
- **code_contract_term** `LON_MIN` — count=16

### `./aura_field_engine.py`
- **constant** `ASPECT_OFFSETS` — {
- **constant** `AURA_ADAPTIVE_THRESHOLDS` — (0.04, 0.4)
- **constant** `AURA_POC_OVERLAY` — {
- **constant** `CONVERGENCE_DELTA_THRESHOLD` — 0.05
- **constant** `CONVERGENCE_OVERSHOOT_STALL_PASSES` — 2
- **constant** `CONVERGENCE_RENDER_MODE` — "convergence_raster"
- **constant** `DEFAULT_ADAPTIVE_MAX_DEPTH` — 6
- **constant** `DEFAULT_CONVERGENCE_MAX_PASSES` — 64
- **constant** `DEFAULT_CONVERGENCE_PER_PASS_SAMPLES` — 2000
- **constant** `PENDING_REFINE_STOP_REASONS` — frozenset(
- **constant** `PLANET_IDS` — {
- **constant** `PRODUCT_LAT_CAP` — 65.0
- **constant** `REFERENCE_TRUTH_ROLE` — "uniform_one_sample_per_paint_pixel"
- **constant** `REVEAL_MAX_TRUTH_SAMPLES` — 4000
- **constant** `REVEAL_TRANSPORT_VERSION` — 1

### `./brute_force_validator.py`
- **constant** `ASPECT_COLORS` — {
- **constant** `LAT_STEP` — 0.5
- **constant** `LON_STEP` — 0.5

### `./local_product_store.py`
- **constant** `APP_DIR` — Path(__file__).resolve().parent
- **constant** `DEFAULT_STORE_PATH` — APP_DIR / "scaffold" / "local_product" / "TEMPORARY_product_store.json"
- **constant** `HISTORY_EVENT_TYPES` — frozenset({"map_search", "map_view", "place_inspect"})
- **constant** `RECORD_TYPES` — frozenset({"self", "client", "research"})
- **constant** `STORAGE_MARKER` — "TEMPORARY_LOCAL_SCAFFOLD"
- **constant** `SUPABASE_MIRROR_VERSION` — 1

### `./main_centerline_FIXER.py`
- **constant** `APP_DIR` — Path(__file__).parent
- **constant** `CHARTS_FILE` — Path(__file__).parent / "charts" / "chart_profiles.json"
- **constant** `LIBRARY_DIR` — APP_DIR / "library"
- **constant** `LIBRARY_SCHEMA_VERSION` — 1
- **constant** `LOCAL_PRODUCT_STORE_SCAFFOLD` — (

### `./truth_field_regions.py`
- **constant** `HIGH_NORTHERN_FIXTURE` — {
- **constant** `KNOWN_FALSE_PROBES` — [
- **constant** `LAT_MAX` — 65.0
- **constant** `LAT_MIN` — -65.0
- **constant** `LON_MAX` — 180.0
- **constant** `LON_MIN` — -180.0

### `./truth_grid_engine.py`
- **constant** `LON_MAX` — 180.0
- **constant** `LON_MIN` — -180.0
- **constant** `SIGN_NAMES` — [

### `./aura_field_engine.py`
- **json_key** `convergence_vs_reference` — count=3
- **json_key** `debug_cells` — count=2
- **json_key** `pixel_attribution_complete` — count=1

### `./local_product_store.py`
- **json_key** `chart_record_history` — count=1
- **json_key** `default_reopen_mode` — count=1
- **json_key** `supabase_mirror_version` — count=1

### `./main_centerline_FIXER.py`
- **json_key** `canonicalFeatureId` — count=1
- **json_key** `per_mask_counts` — count=2

### `./truth_field_regions.py`
- **json_key** `cacheHits` — count=1
- **json_key** `cacheMisses` — count=1
- **json_key** `canonicalFeatureId` — count=2
- **json_key** `cellCount` — count=2
- **json_key** `mergedFeatureCount` — count=2
- **json_key** `sourceCellCount` — count=1

### `./truth_grid_engine.py`
- **json_key** `canonicalFeatureId` — count=2

### `./local_product_store.py`
- **class** `ChartRecordBirthResolutionError` — 

### `./main_centerline_FIXER.py`
- **class** `ClassifyPointPayload` — 
- **class** `LibraryActiveSelection` — 
- **class** `LibraryChartUpsert` — 
- **class** `LibraryFavoriteToggle` — 
- **class** `LibrarySettingsPatch` — 
- **class** `LibraryViewSave` — 

### `./truth_field_regions.py`
- **class** `MergedCell` — 

### `./truth_grid_engine.py`
- **class** `MergedCell` — 

### `./aura_field_engine.py`
- **function** `_initial_cell_pixel_groups` — 
- **function** `_partition_pixels_to_children` — 
- **function** `_rasterize_leaves` — 
- **function** `_viewport_pixel_coords` — 
- **function** `classify_observed_refinement_stage` — 
- **function** `generate_aura_convergence_raster` — 
- **function** `generate_aura_field` — 
- **function** `is_aura_poc_overlay` — 

### `./local_product_store.py`
- **function** `append_chart_record_history` — 
- **function** `get_birth_profile_for_chart_record` — 
- **function** `get_chart_record` — 
- **function** `get_default_chart_record_id` — 
- **function** `list_chart_record_summaries` — 
- **function** `set_default_chart_record_id` — 
- **function** `summarize_chart_record` — 

### `./main_centerline_FIXER.py`
- **function** `_ensure_local_product_store_read_enabled` — 
- **function** `_local_product_store_read_enabled` — 
- **function** `_next_chart_id` — 
- **function** `aura_raster_adaptive` — 
- **function** `aura_raster_convergence` — 
- **function** `aura_refinement_reveal_stages` — 
- **function** `create_or_update_library_chart` — 
- **function** `delete_library_chart` — 
- **function** `get_chart_profiles` — 
- **function** `get_chart_record_engine_birth` — 
- **function** `get_chart_record_summary` — 
- **function** `list_chart_records_api` — 
- **function** `load_chart_profiles` — 
- **function** `serve_local_product_store_json` — 
- **function** `serve_map_sandbox_phase2_cache` — 
- **function** `serve_map_sandbox_truth_pixels` — 
- **function** `serve_map_sandbox_truth_reveal` — 
- **function** `serve_phase2_cache_scheduler` — 
- **function** `toggle_library_chart_favorite` — 

### `./truth_field_regions.py`
- **function** `build_center_grid` — 
- **function** `cell_to_feature` — 
- **function** `cells_from_grid` — 
- **function** `cells_to_geojson` — 

...plus 11 more entries in the JSON audit.

## High-Priority Weakly Documented Items

### `./main_centerline_FIXER.py`
- **endpoint** `/app_shell.html` — GET | hits: html:211
- **endpoint** `/cities.js` — GET | hits: js:818, cities.js:24
- **endpoint** `/genie_SANDBOX_variable_builder.html` — GET | hits: html:211, genie_SANDBOX_variable_builder.html:27
- **endpoint** `/genie_map_engine_adapter.js` — GET | hits: genie_map_engine_adapter.js:8, js:818
- **endpoint** `/genie_variable_builder.css` — GET | hits: css:51
- **endpoint** `/genie_variable_builder.js` — GET | hits: js:818
- **endpoint** `/library.html` — GET | hits: library.html:2, html:211, /library:53
- **endpoint** `/local-product-store.json` — GET | hits: json:780
- **endpoint** `/map_CURRENT.html` — GET | hits: html:211, map_CURRENT.html:102
- **endpoint** `/map_SANDBOX_brute_force.html` — GET | hits: map_SANDBOX_brute_force.html:6, html:211
- **endpoint** `/map_SANDBOX_polygon_reveal.html` — GET | hits: html:211
- **endpoint** `/map_SANDBOX_raindrop_aesthetic.html` — GET | hits: html:211, map_SANDBOX_raindrop_aesthetic.html:17
- **endpoint** `/map_SANDBOX_screen_pixel_truth.html` — GET | hits: html:211, map_SANDBOX_screen_pixel_truth.html:12
- **endpoint** `/map_SANDBOX_truth_pixels.html` — GET | hits: html:211
- **endpoint** `/map_SANDBOX_truth_reveal.html` — GET | hits: html:211
- **endpoint** `/substrate_adapter.js` — GET | hits: js:818
- **model_field** `AngleInSignCondition.angle` — Literal['asc', 'mc', 'ic', 'dsc'] default= | hits: angle:488
- **model_field** `AngleInSignCondition.sign` — Literal['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'] default= | hits: sign:2460
- **model_field** `AngleInSignCondition.type` — Literal['angle_in_sign'] default='angle_in_sign' | hits: type:544
- **model_field** `AngleSignCondition.angle` — str default= | hits: angle:488
- **model_field** `AngleSignCondition.sign` — str default= | hits: sign:2460
- **model_field** `AspectToAngleCondition.angle` — Literal['asc', 'mc', 'ic', 'dsc'] default= | hits: angle:488
- **model_field** `AspectToAngleCondition.aspect` — Literal['conjunction', 'sextile', 'square', 'trine', 'opposition'] default= | hits: aspect:716
- **model_field** `AspectToAngleCondition.orb` — float default=Field(default=1.0, gt=0.0, le=15.0) | hits: orb:704
- **model_field** `AspectToAngleCondition.planet` — str default= | hits: planet:286
- **model_field** `AspectToAngleCondition.type` — Literal['aspect_to_angle'] default='aspect_to_angle' | hits: type:544
- **model_field** `AuraAdaptiveRasterRequest.apply_lat_cap` — bool default=True | hits: apply_lat_cap:3
- **model_field** `AuraAdaptiveRasterRequest.aspect_overlay` — dict default= | hits: aspect_overlay:31
- **model_field** `AuraAdaptiveRasterRequest.east` — float default= | hits: east:2
- **model_field** `AuraAdaptiveRasterRequest.north` — float default= | hits: north:22
- **model_field** `AuraAdaptiveRasterRequest.south` — float default= | hits: south:36
- **model_field** `AuraAdaptiveRasterRequest.west` — float default= | hits: west:5
- **model_field** `AuraConvergenceRasterRequest.apply_lat_cap` — bool default=True | hits: apply_lat_cap:3
- **model_field** `AuraConvergenceRasterRequest.aspect_overlay` — dict default= | hits: aspect_overlay:31
- **model_field** `AuraConvergenceRasterRequest.east` — float default= | hits: east:2
- **model_field** `AuraConvergenceRasterRequest.north` — float default= | hits: north:22
- **model_field** `AuraConvergenceRasterRequest.south` — float default= | hits: south:36
- **model_field** `AuraConvergenceRasterRequest.west` — float default= | hits: west:5
- **model_field** `AuraFieldRequest.apply_lat_cap` — bool default=True | hits: apply_lat_cap:3
- **model_field** `AuraFieldRequest.aspect_overlay` — dict default= | hits: aspect_overlay:31
- **model_field** `AuraFieldRequest.resolution` — float default=2.0 | hits: resolution:173
- **model_field** `AuraRasterRequest.apply_lat_cap` — bool default=True | hits: apply_lat_cap:3
- **model_field** `AuraRasterRequest.aspect_overlay` — dict default= | hits: aspect_overlay:31
- **model_field** `AuraRasterRequest.east` — float default= | hits: east:2
- **model_field** `AuraRasterRequest.height` — int default= | hits: height:2
- **model_field** `AuraRasterRequest.north` — float default= | hits: north:22
- **model_field** `AuraRasterRequest.south` — float default= | hits: south:36
- **model_field** `AuraRasterRequest.west` — float default= | hits: west:5
- **model_field** `AuraRasterRequest.width` — int default= | hits: width:54
- **model_field** `BruteForceGridRequest.apply_lat_cap` — bool default=False | hits: apply_lat_cap:3
- **model_field** `BruteForceGridRequest.conditions` — list[Condition] | None default=None | hits: conditions:338
- **model_field** `BruteForceGridRequest.east` — float default= | hits: east:2
- **model_field** `BruteForceGridRequest.north` — float default= | hits: north:22
- **model_field** `BruteForceGridRequest.south` — float default= | hits: south:36
- **model_field** `BruteForceGridRequest.west` — float default= | hits: west:5
- **model_field** `ClassifyPointsRequest.apply_lat_cap` — bool default=True | hits: apply_lat_cap:3
- **model_field** `ClassifyPointsRequest.points` — list[ClassifyPointPayload] default= | hits: points:307
- **model_field** `PlanetInHouseCondition.house` — int default= | hits: house:988
- **model_field** `PlanetInHouseCondition.planet` — str default= | hits: planet:286
- **model_field** `PlanetInHouseCondition.type` — Literal['planet_in_house'] default='planet_in_house' | hits: type:544
- **model_field** `ScreenPixelTruthRequest.apply_lat_cap` — bool default=False | hits: apply_lat_cap:3
- **model_field** `ScreenPixelTruthRequest.conditions` — list[Condition] | None default=None | hits: conditions:338
- **model_field** `ScreenPixelTruthRequest.points` — list[Any] default=Field(..., description='List of [lat, lon] pairs (degrees).') | hits: points:307
- **model_field** `SearchRequest.angle_sign_conditions` — List[AngleSignCondition] default=Field(default_factory=list) | hits: angle_sign_conditions:31
- **model_field** `SearchRequest.aspect_overlay` — dict | None default=None | hits: aspect_overlay:31
- **model_field** `SearchRequest.generation_mode` — str default='contour' | hits: generation_mode:31
- **model_field** `SearchRequest.house_conditions` — List[Condition] default= | hits: house_conditions:31
- **model_field** `SearchRequest.resolution` — float default=1.5 | hits: resolution:173
- **model_field** `SearchRequest.truth_grid_boundary_refine` — bool default=True | hits: truth_grid_boundary_refine:33
- **model_field** `SearchRequest.truth_grid_resolution` — float default=0.75 | hits: truth_grid_resolution:31
- **model_field** `ClassifyPointPayload.lat` — float default= | hits: lat:4465
- **model_field** `ClassifyPointPayload.lon` — float default= | hits: lon:1208
- **model_field** `LibraryChartUpsert.date` — str default= | hits: date:1087
- **model_field** `LibraryChartUpsert.favorite` — bool default=False | hits: favorite:506
- **model_field** `LibraryChartUpsert.id` — str | None default=None | hits: id:8920
- **model_field** `LibraryChartUpsert.lat` — float default=0.0 | hits: lat:4465
- **model_field** `LibraryChartUpsert.lon` — float default=0.0 | hits: lon:1208
- **model_field** `LibraryChartUpsert.name` — str default= | hits: name:702
- **model_field** `LibraryChartUpsert.notes` — str default='' | hits: notes:477
- **model_field** `LibraryChartUpsert.place` — str default='' | hits: place:961
- **model_field** `LibraryChartUpsert.time` — str default= | hits: time:1019
- **model_field** `LibraryChartUpsert.timezone` — str default='UTC' | hits: timezone:32
- **model_field** `LibraryFavoriteToggle.favorite` — bool default= | hits: favorite:506
- **model_field** `LibraryViewSave.conditions` — list[dict[str, Any]] default=Field(default_factory=list) | hits: conditions:338
- **model_field** `LibraryViewSave.east` — float default= | hits: east:2
- **model_field** `LibraryViewSave.label` — str default='Saved view' | hits: label:580
- **model_field** `LibraryViewSave.north` — float default= | hits: north:22
- **model_field** `LibraryViewSave.notes` — str default='' | hits: notes:477
- **model_field** `LibraryViewSave.south` — float default= | hits: south:36
- **model_field** `LibraryViewSave.west` — float default= | hits: west:5
- **model_field** `LibraryViewSave.zoom` — float default= | hits: zoom:226

### `./truth_field_regions.py`
- **model_field** `Cell.center_lat` — float default= | hits: Cell:805
- **model_field** `Cell.center_lon` — float default= | hits: Cell:805
- **model_field** `Cell.is_boundary` — bool default= | hits: Cell:805
- **model_field** `Cell.lat_max` — float default= | hits: Cell:805
- **model_field** `Cell.lat_min` — float default= | hits: Cell:805
- **model_field** `Cell.lon_max` — float default= | hits: Cell:805
- **model_field** `Cell.lon_min` — float default= | hits: Cell:805
- **model_field** `MergedCell.house` — int default= | hits: house:988
- **model_field** `MergedCell.level` — str default= | hits: level:167

### `./truth_grid_engine.py`
- **model_field** `MergedCell.house` — int default= | hits: house:988

### `./add_endpoint.py`
- **code_contract_term** `swe.calc_ut` — count=1 | hits: swe:143

### `./aura_field_engine.py`
- **code_contract_term** `swe.calc_ut` — count=1 | hits: swe:143

### `./brute_force_validator.py`
- **code_contract_term** `swe.calc_ut` — count=1 | hits: swe:143
- **code_contract_term** `swe.julday` — count=1 | hits: swe:143

### `./main_centerline_FIXER.py`
- **code_contract_term** `swe.calc_ut` — count=5 | hits: swe:143
- **code_contract_term** `swe.julday` — count=2 | hits: swe:143
- **code_contract_term** `swe.sidtime` — count=1 | hits: swe:143

### `./main_contours.py`
- **code_contract_term** `swe.calc_ut` — count=3 | hits: swe:143
- **code_contract_term** `swe.julday` — count=1 | hits: swe:143
- **code_contract_term** `swe.sidtime` — count=1 | hits: swe:143

### `./local_product_store.py`
- **constant** `FORBIDDEN_KEY_SUBSTRINGS` — ( | hits: FORBIDDEN KEY SUBSTRINGS:15

### `./main_centerline_FIXER.py`
- **constant** `LIBRARY_FILE` — LIBRARY_DIR / "library.json" | hits: LIBRARY FILE:3

### `./truth_grid_engine.py`
- **constant** `LATITUDE_CAP` — [-65.0, 65.0] | hits: LATITUDE-CAP:3, LATITUDE CAP:24

### `./aura_field_engine.py`
- **json_key** `sample_count` — count=4 | hits: sample count:13

### `./local_product_store.py`
- **json_key** `layer_display_state` — count=2 | hits: layer display state:1
- **json_key** `settings_snapshot_version` — count=1 | hits: settings snapshot version:5

### `./main_centerline_FIXER.py`
- **json_key** `overlap_counts` — count=2 | hits: overlap counts:1

### `./truth_grid_engine.py`
- **json_key** `sample_count` — count=4 | hits: sample count:13

### `./add_endpoint.py`
- **function** `relocation_chart` —  | hits: relocation chart:6

### `./local_product_store.py`
- **function** `chart_record_id` —  | hits: chart record id:1
- **function** `list_chart_records` —  | hits: list chart records:1

### `./main_centerline_FIXER.py`
- **function** `brute_force_grid` —  | hits: brute-force-grid:25, brute force grid:1
- **function** `classify_points` —  | hits: classify-points:25, classify points:1
- **function** `relocated_chart` —  | hits: relocated-chart:7, relocated chart:127

### `./truth_field_regions.py`
- **function** `classify_grid` —  | hits: classify grid:1

## Lower-Priority Missing Summary

- Normal-priority missing symbols: 347
  - `./aura_field_engine.py`: 122; examples: `active_frontier_leaf_count`, `adaptive_strategy`, `cell_count`, `center_orb`, `chiron`, `compute_seconds`, `converged`, `convergence_delta_threshold`, `cumulative_samples`, `default_max_depth_doctrine`
  - `./main_centerline_FIXER.py`: 90; examples: `active_chart_id`, `asc_contour_seconds`, `asc_deg`, `asc_grid_seconds`, `asc_sign`, `aspect_offset`, `aspect_resolution`, `aspect_set`, `center_lat`, `center_lon`
  - `./truth_field_regions.py`: 66; examples: `__main__`, `actual_sun_house`, `allHousesCompressionRatio`, `allMergedSizeBytes`, `allRawSizeBytes`, `allSunHousesAvailableFromSameSamples`, `aspectNotes`, `birthDate`, `birth_day`, `birth_hour_utc`
  - `./local_product_store.py`: 38; examples: `birthCity`, `birthSummary`, `birth_day`, `birth_hour_utc`, `birth_month`, `birth_place_id`, `birth_year`, `client_id`, `currentCity`, `current_location_place_id`
  - `./truth_grid_engine.py`: 22; examples: `classify_seconds`, `condition_index`, `feature_count`, `houses_cached`, `houses_returned`, `merge_step`, `merge_validate_seconds`, `refine_samples`, `sign_index`, `signs_returned`
  - `./main_contours.py`: 9; examples: `chiron`, `condition_index`, `mercury`, `neptune`, `pluto`, `uranus`, `get_houses`, `get_planet_positions`, `julian_day`

## Parse Warnings

- `./main_contours.py`: unindent does not match any outer indentation level (<unknown>, line 222)

## Recommended Documentation Patch Targets

1. Add a generated live-code endpoint/schema appendix covering every Pydantic request field and endpoint route.
2. Add a Store v3 appendix for `local_product_store.py`: exact top-level keys, object keys, forbidden substrings, validation rules, record types, event types, confidence tiers, and comparison constraints.
3. Add an aura/debug archaeology appendix for exact PoC endpoints, request fields, response properties, constants, budgets, convergence metrics, and non-production status.
4. Add exact screen-pixel/brute-force contracts: masks, A–F labels, caps (`POINT_CAP`, `MAX_CELLS`, `_MAX_CONDITIONS`), histograms, overlap counts, and response properties.
5. Add truth-field validation-output documentation for `Cell`, `MergedCell`, GeoJSON feature properties, merge benchmark reports, false probes, and validation record paths.
