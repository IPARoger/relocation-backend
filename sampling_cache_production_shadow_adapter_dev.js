/*
  Phase 2.25 dev-only production shadow adapter.

  This adapter evaluates production-adjacent candidate metadata through the
  Phase 2.24 production-readiness contract. It does not fetch, render, mutate
  DOM/map state, register production ownership, hydrate production layers,
  alter legacy_search_regions, persist state, or expose raw backend payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const MODE = "dev_production_shadow_adapter_only";
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const ADAPTER_NAMESPACE = "RelocationSamplingCacheProductionShadowAdapterDev";
  const RAW_OR_FORBIDDEN_RUNTIME_FIELDS = Object.freeze([
    "features",
    "geometry",
    "coordinates",
    "geojson",
    "raw_payload",
    "rawPayload",
    "renderer_output",
    "canvas_pixels",
    "leaflet_layers",
    "production_layer_id",
    "debug",
    "aura_mode",
    "virga_mode",
    "worker_id",
    "fetch_url",
    "generation_mode",
  ]);

  function readinessContract() {
    const contract = global.RelocationSamplingCacheProductionReadinessContract;
    if (!contract || typeof contract.classifyReadiness !== "function") {
      throw new Error("Phase 2.24 production-readiness contract is required");
    }
    return contract;
  }

  function cloneJson(value) {
    if (value == null) return value;
    return JSON.parse(JSON.stringify(value));
  }

  function assertObject(value, label) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new TypeError(`${label} must be an object`);
    }
  }

  function hasOwn(value, key) {
    return Object.prototype.hasOwnProperty.call(value || {}, key);
  }

  function deepHasField(value, fields) {
    if (!value || typeof value !== "object") return false;
    if (Array.isArray(value)) return value.some(item => deepHasField(item, fields));
    return Object.keys(value).some(key => fields.includes(key) || deepHasField(value[key], fields));
  }

  function deepOmitFields(value, fields) {
    if (!value || typeof value !== "object") return value;
    if (Array.isArray(value)) return value.map(item => deepOmitFields(item, fields));
    const out = {};
    Object.keys(value).forEach(key => {
      if (!fields.includes(key)) out[key] = deepOmitFields(value[key], fields);
    });
    return out;
  }

  function bool(value, fallback) {
    return typeof value === "boolean" ? value : fallback;
  }

  function stringValue(value, fallback) {
    return typeof value === "string" && value ? value : fallback;
  }

  function createShadowProfile(candidate) {
    assertObject(candidate, "production shadow candidate");
    const runtimeMetadata = candidate.runtime_metadata || {};
    const production = candidate.production_path || {};
    const flags = candidate.boundary_flags || {};
    const observer = candidate.observer || {};
    const cache = candidate.cache || {};
    const validation = candidate.validation || {};
    const sanitizedRuntimeEnvelope = deepOmitFields(runtimeMetadata, RAW_OR_FORBIDDEN_RUNTIME_FIELDS);
    const symbolicScoringPresent = deepHasField(runtimeMetadata, ["symbolic_score"]);
    const recommendationLogicPresent = deepHasField(runtimeMetadata, ["recommendation_logic", "recommendation"]);
    const bestLocationLogicPresent = deepHasField(runtimeMetadata, ["best_location_logic", "best_location", "bestLocation"]);
    const hiddenOntologyPresent = deepHasField(runtimeMetadata, ["hidden_ontology"]);
    const rawPayloadPresent = deepHasField(runtimeMetadata, RAW_OR_FORBIDDEN_RUNTIME_FIELDS);

    return {
      requested_readiness_status: stringValue(candidate.requested_readiness_status, "transitional_candidate"),
      layer_sovereignty: {
        no_interpretation_in_runtime_metadata: bool(flags.no_interpretation_in_runtime_metadata, true),
        no_symbolic_scoring: bool(flags.no_symbolic_scoring, true) && !symbolicScoringPresent,
        no_recommendation_authority: bool(flags.no_recommendation_authority, true) && !recommendationLogicPresent,
        no_best_location_logic: bool(flags.no_best_location_logic, true) && !bestLocationLogicPresent,
        no_hidden_ontology: bool(flags.no_hidden_ontology, true) && !hiddenOntologyPresent,
      },
      runtime_sovereignty: {
        renderer_ownership_claimed: bool(flags.renderer_ownership_claimed, false),
        production_registry_mutated: bool(flags.production_registry_mutated, false),
        dom_mutation_outside_approved_root: bool(flags.dom_mutation_outside_approved_root, false),
        raw_backend_payload_exposed: bool(
          flags.raw_backend_payload_exposed,
          false
        ) || rawPayloadPresent,
        unsafe_hydration: bool(flags.unsafe_hydration, false),
      },
      truth_integrity: {
        final_truth_claimed: bool(flags.final_truth_claimed, false),
        candidates_confirmed_as_truth: bool(flags.candidates_confirmed_as_truth, false),
        runtime_priority_implies_symbolic_importance: bool(flags.runtime_priority_implies_symbolic_importance, false),
      },
      observer_safety: {
        read_only: bool(observer.read_only, true),
        can_control_lifecycle: bool(observer.can_control_lifecycle, false),
        can_control_scheduler: bool(observer.can_control_scheduler, false),
        can_control_hydration: bool(observer.can_control_hydration, false),
        can_control_cache: bool(observer.can_control_cache, false),
        metadata_sanitized: true,
      },
      cache_scheduler_safety: {
        semantic_cache_keys_renderer_independent: bool(cache.semantic_cache_keys_renderer_independent, true),
        semantic_cache_keys_debug_independent: bool(cache.semantic_cache_keys_debug_independent, true),
        semantic_cache_keys_aura_independent: bool(cache.semantic_cache_keys_aura_independent, true),
        foreground_user_request_protected: bool(cache.foreground_user_request_protected, true),
        background_work_cannot_block_current_intent: bool(cache.background_work_cannot_block_current_intent, true),
        stale_or_cancelled_work_cannot_hydrate_visibly: bool(
          cache.stale_or_cancelled_work_cannot_hydrate_visibly,
          bool(flags.stale_or_cancelled_work_cannot_hydrate_visibly, true)
        ),
      },
      terminology_safety: {
        neutral_runtime_metadata: bool(flags.neutral_runtime_metadata, true),
        candidate_vocabulary_quarantined: bool(flags.candidate_vocabulary_quarantined, true),
        runtime_envelope: sanitizedRuntimeEnvelope,
        quarantined_candidate_vocabulary: cloneJson(candidate.quarantined_candidate_vocabulary || {}),
      },
      validation_requirements: {
        dedicated_smoke_exists: bool(validation.dedicated_smoke_exists, true),
        narrative_exists: bool(validation.narrative_exists, true),
        rollback_scope_clear: bool(validation.rollback_scope_clear, true),
      },
      production_path: {
        renderer_substrate: stringValue(production.renderer_substrate, RENDERER_SUBSTRATE),
        fetch_coupled: bool(production.fetch_coupled, false),
        worker_coupled: bool(production.worker_coupled, false),
        dom_or_map_coupled: bool(production.dom_or_map_coupled, false),
        renderer_coupled: bool(production.renderer_coupled, false),
        persistence_coupled: bool(production.persistence_coupled, false),
        backend_coupled: bool(production.backend_coupled, false),
      },
    };
  }

  function evaluateShadowCandidate(candidate) {
    const contract = readinessContract();
    const shadowProfile = createShadowProfile(candidate);
    const classification = contract.classifyReadiness(shadowProfile);
    return Object.freeze({
      schema_version: VERSION,
      mode: MODE,
      adapter_namespace: ADAPTER_NAMESPACE,
      debug_only: true,
      production_shadow_only: true,
      metadata_only: true,
      rendererSubstrate: RENDERER_SUBSTRATE,
      active_production_substrate: RENDERER_SUBSTRATE,
      legacy_search_regions_active: true,
      fetch_used: false,
      render_started: false,
      dom_or_map_mutated: false,
      production_registry_mutated: false,
      renderer_ownership_claimed: false,
      production_layers_hydrated: false,
      raw_backend_payload_exposed: false,
      final_truth_claimed: false,
      recommendation_surface_created: false,
      scoring_surface_created: false,
      interpretation_surface_created: false,
      accepted: classification.accepted,
      readiness_status: classification.readiness_status,
      failed_gates: classification.failed_gates,
      gate_results: classification.gate_results,
      classification,
      sanitized_profile: classification.sanitized_profile,
    });
  }

  function inspectAdapter() {
    const contract = readinessContract().inspectContract();
    return Object.freeze({
      schema_version: VERSION,
      mode: MODE,
      adapter_namespace: ADAPTER_NAMESPACE,
      debug_only: true,
      standalone: true,
      metadata_only: true,
      rendererSubstrate: RENDERER_SUBSTRATE,
      active_production_substrate: RENDERER_SUBSTRATE,
      legacy_search_regions_active: true,
      contract_mode: contract.mode,
      contract_renderer_substrate: contract.rendererSubstrate,
      fetch_used: false,
      render_started: false,
      worker_started: false,
      dom_or_map_mutated: false,
      production_registry_mutated: false,
      renderer_ownership_claimed: false,
      production_layers_hydrated: false,
      persisted: false,
      backend_coupled: false,
      raw_backend_payload_exposed: false,
      final_truth_claimed: false,
      recommendation_surface_created: false,
      scoring_surface_created: false,
      interpretation_surface_created: false,
    });
  }

  global[ADAPTER_NAMESPACE] = Object.freeze({
    VERSION,
    MODE,
    RENDERER_SUBSTRATE,
    createShadowProfile,
    evaluateShadowCandidate,
    inspectAdapter,
  });
})(window);
