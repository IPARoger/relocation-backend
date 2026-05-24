/*
  Phase 2.24 dev-only production-readiness boundary contract.

  This contract classifies sandbox/runtime scaffold readiness for future
  production promotion. It does not integrate with production rendering, mutate
  overlay registries, start workers, fetch, persist state, or expose raw backend
  payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const CONTRACT_MODE = "dev_production_readiness_contract_only";
  const READINESS_STATUSES = Object.freeze([
    "not_ready",
    "sandbox_only",
    "transitional_candidate",
    "production_candidate",
  ]);
  const FORBIDDEN_RUNTIME_TERMS = Object.freeze([
    "symbolic_score",
    "recommendation",
    "best_location",
    "bestLocation",
    "unified_meaning",
    "unified_astrology_meaning",
    "truth_final",
    "interpretation_authority",
    "predictive_authority",
    "hidden_ontology",
  ]);
  const RAW_OR_FORBIDDEN_FIELDS = Object.freeze([
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
  const HARD_GATES = Object.freeze([
    "layer_sovereignty",
    "runtime_sovereignty",
    "truth_integrity",
    "observer_safety",
    "cache_scheduler_safety",
    "terminology_safety",
    "validation_requirements",
    "production_path_unchanged",
  ]);

  function cloneJson(value) {
    if (value == null) return value;
    return JSON.parse(JSON.stringify(value));
  }

  function assertObject(value, label) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new TypeError(`${label} must be an object`);
    }
  }

  function valueContainsForbiddenField(value, fields) {
    if (!value || typeof value !== "object") return false;
    if (Array.isArray(value)) return value.some(item => valueContainsForbiddenField(item, fields));
    return Object.keys(value).some(key => fields.includes(key) || valueContainsForbiddenField(value[key], fields));
  }

  function textContainsRuntimeForbiddenTerm(value) {
    const text = JSON.stringify(value || {});
    return FORBIDDEN_RUNTIME_TERMS.some(term => text.includes(term));
  }

  function bool(value) {
    return value === true;
  }

  function pass(name) {
    return Object.freeze({ gate: name, passed: true, reasons: Object.freeze([]) });
  }

  function fail(name, reasons) {
    return Object.freeze({ gate: name, passed: false, reasons: Object.freeze(reasons) });
  }

  function checkLayerSovereignty(profile) {
    const layer = profile.layer_sovereignty || {};
    const reasons = [];
    if (!bool(layer.no_interpretation_in_runtime_metadata)) reasons.push("runtime_metadata_must_not_contain_interpretation");
    if (!bool(layer.no_symbolic_scoring)) reasons.push("symbolic_scoring_forbidden");
    if (!bool(layer.no_recommendation_authority)) reasons.push("recommendation_authority_forbidden");
    if (!bool(layer.no_best_location_logic)) reasons.push("best_location_logic_forbidden");
    if (!bool(layer.no_hidden_ontology)) reasons.push("hidden_ontology_forbidden");
    return reasons.length ? fail("layer_sovereignty", reasons) : pass("layer_sovereignty");
  }

  function checkRuntimeSovereignty(profile) {
    const runtime = profile.runtime_sovereignty || {};
    const reasons = [];
    if (!bool(runtime.renderer_ownership_claimed === false)) reasons.push("renderer_ownership_must_not_be_claimed");
    if (!bool(runtime.production_registry_mutated === false)) reasons.push("production_registry_must_not_be_mutated");
    if (!bool(runtime.dom_mutation_outside_approved_root === false)) reasons.push("dom_mutation_outside_approved_root_forbidden");
    if (!bool(runtime.raw_backend_payload_exposed === false)) reasons.push("raw_backend_payload_exposure_forbidden");
    if (!bool(runtime.unsafe_hydration === false)) reasons.push("unsafe_hydration_forbidden");
    return reasons.length ? fail("runtime_sovereignty", reasons) : pass("runtime_sovereignty");
  }

  function checkTruthIntegrity(profile) {
    const truth = profile.truth_integrity || {};
    const reasons = [];
    if (!bool(truth.final_truth_claimed === false)) reasons.push("final_truth_claims_forbidden");
    if (!bool(truth.candidates_confirmed_as_truth === false)) reasons.push("candidate_outputs_must_not_be_confirmed_truth");
    if (!bool(truth.runtime_priority_implies_symbolic_importance === false)) reasons.push("runtime_priority_must_not_imply_symbolic_importance");
    return reasons.length ? fail("truth_integrity", reasons) : pass("truth_integrity");
  }

  function checkObserverSafety(profile) {
    const observer = profile.observer_safety || {};
    const reasons = [];
    if (!bool(observer.read_only)) reasons.push("observers_must_be_read_only");
    if (!bool(observer.can_control_lifecycle === false)) reasons.push("observer_lifecycle_control_forbidden");
    if (!bool(observer.can_control_scheduler === false)) reasons.push("observer_scheduler_control_forbidden");
    if (!bool(observer.can_control_hydration === false)) reasons.push("observer_hydration_control_forbidden");
    if (!bool(observer.can_control_cache === false)) reasons.push("observer_cache_control_forbidden");
    if (!bool(observer.metadata_sanitized)) reasons.push("observer_metadata_must_be_sanitized");
    return reasons.length ? fail("observer_safety", reasons) : pass("observer_safety");
  }

  function checkCacheSchedulerSafety(profile) {
    const cache = profile.cache_scheduler_safety || {};
    const reasons = [];
    if (!bool(cache.semantic_cache_keys_renderer_independent)) reasons.push("cache_keys_must_be_renderer_independent");
    if (!bool(cache.semantic_cache_keys_debug_independent)) reasons.push("cache_keys_must_be_debug_independent");
    if (!bool(cache.semantic_cache_keys_aura_independent)) reasons.push("cache_keys_must_be_aura_independent");
    if (!bool(cache.foreground_user_request_protected)) reasons.push("foreground_user_request_must_be_protected");
    if (!bool(cache.background_work_cannot_block_current_intent)) reasons.push("background_work_must_not_block_current_intent");
    if (!bool(cache.stale_or_cancelled_work_cannot_hydrate_visibly)) reasons.push("stale_or_cancelled_work_must_not_hydrate_visibly");
    return reasons.length ? fail("cache_scheduler_safety", reasons) : pass("cache_scheduler_safety");
  }

  function checkTerminologySafety(profile) {
    const terminology = profile.terminology_safety || {};
    const runtimeEnvelope = terminology.runtime_envelope || {};
    const quarantinedCandidateVocabulary = terminology.quarantined_candidate_vocabulary || {};
    const reasons = [];
    if (!bool(terminology.neutral_runtime_metadata)) reasons.push("runtime_metadata_must_use_neutral_terms");
    if (valueContainsForbiddenField(runtimeEnvelope, RAW_OR_FORBIDDEN_FIELDS)) reasons.push("runtime_envelope_contains_raw_or_forbidden_field");
    if (textContainsRuntimeForbiddenTerm(runtimeEnvelope)) reasons.push("runtime_envelope_contains_forbidden_vocabulary");
    if (textContainsRuntimeForbiddenTerm(quarantinedCandidateVocabulary) && !bool(terminology.candidate_vocabulary_quarantined)) {
      reasons.push("candidate_vocabulary_must_be_quarantined_when_layer4_terms_are_present");
    }
    return reasons.length ? fail("terminology_safety", reasons) : pass("terminology_safety");
  }

  function checkValidationRequirements(profile) {
    const validation = profile.validation_requirements || {};
    const reasons = [];
    if (!bool(validation.dedicated_smoke_exists)) reasons.push("dedicated_smoke_required");
    if (!bool(validation.narrative_exists)) reasons.push("validation_narrative_required");
    if (!bool(validation.rollback_scope_clear)) reasons.push("rollback_scope_required");
    return reasons.length ? fail("validation_requirements", reasons) : pass("validation_requirements");
  }

  function checkProductionPath(profile) {
    const production = profile.production_path || {};
    const reasons = [];
    if (String(production.renderer_substrate || "") !== RENDERER_SUBSTRATE) reasons.push("production_renderer_substrate_must_remain_legacy_search_regions");
    if (!bool(production.fetch_coupled === false)) reasons.push("fetch_coupling_forbidden");
    if (!bool(production.worker_coupled === false)) reasons.push("worker_coupling_forbidden");
    if (!bool(production.dom_or_map_coupled === false)) reasons.push("dom_or_map_coupling_forbidden");
    if (!bool(production.renderer_coupled === false)) reasons.push("renderer_coupling_forbidden");
    if (!bool(production.persistence_coupled === false)) reasons.push("persistence_coupling_forbidden");
    if (!bool(production.backend_coupled === false)) reasons.push("backend_coupling_forbidden");
    return reasons.length ? fail("production_path_unchanged", reasons) : pass("production_path_unchanged");
  }

  function classifyReadiness(profile) {
    assertObject(profile, "production readiness profile");
    if (valueContainsForbiddenField(profile, RAW_OR_FORBIDDEN_FIELDS)) {
      return Object.freeze({
        schema_version: VERSION,
        mode: CONTRACT_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        accepted: false,
        readiness_status: "not_ready",
        hard_gates_passed: false,
        failed_gates: Object.freeze(["raw_or_forbidden_field_present"]),
        gate_results: Object.freeze([fail("runtime_sovereignty", ["raw_or_forbidden_field_present"])]),
        production_path_unchanged: true,
        contract_only: true,
      });
    }

    const gateResults = Object.freeze([
      checkLayerSovereignty(profile),
      checkRuntimeSovereignty(profile),
      checkTruthIntegrity(profile),
      checkObserverSafety(profile),
      checkCacheSchedulerSafety(profile),
      checkTerminologySafety(profile),
      checkValidationRequirements(profile),
      checkProductionPath(profile),
    ]);
    const failed = gateResults.filter(result => !result.passed).map(result => result.gate);
    const allHardGatesPassed = failed.length === 0;
    const requestedStatus = String(profile.requested_readiness_status || "sandbox_only");
    const knownStatus = READINESS_STATUSES.includes(requestedStatus) ? requestedStatus : "not_ready";
    let readinessStatus = allHardGatesPassed ? knownStatus : "not_ready";
    if (allHardGatesPassed && (readinessStatus === "not_ready" || readinessStatus === "sandbox_only")) {
      readinessStatus = "transitional_candidate";
    }

    return Object.freeze({
      schema_version: VERSION,
      mode: CONTRACT_MODE,
      rendererSubstrate: RENDERER_SUBSTRATE,
      accepted: allHardGatesPassed,
      requested_readiness_status: knownStatus,
      readiness_status: readinessStatus,
      hard_gates: HARD_GATES,
      hard_gates_passed: allHardGatesPassed,
      failed_gates: Object.freeze(failed),
      gate_results: gateResults,
      production_candidate_allowed: readinessStatus === "production_candidate" && allHardGatesPassed,
      transitional_candidate_allowed: (
        (readinessStatus === "transitional_candidate" || readinessStatus === "production_candidate") &&
        allHardGatesPassed
      ),
      production_path_unchanged: true,
      renderer_ownership_claimed: false,
      production_registry_mutated: false,
      persisted: false,
      fetch_used: false,
      worker_started: false,
      dom_or_map_mutated: false,
      backend_coupled: false,
      contract_only: true,
      sanitized_profile: Object.freeze(cloneJson(profile)),
    });
  }

  function inspectContract() {
    return Object.freeze({
      schema_version: VERSION,
      mode: CONTRACT_MODE,
      rendererSubstrate: RENDERER_SUBSTRATE,
      readiness_statuses: READINESS_STATUSES,
      hard_gates: HARD_GATES,
      production_path_unchanged: true,
      contract_only: true,
      fetch_used: false,
      worker_started: false,
      dom_or_map_mutated: false,
      backend_coupled: false,
    });
  }

  global.RelocationSamplingCacheProductionReadinessContract = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    CONTRACT_MODE,
    READINESS_STATUSES,
    HARD_GATES,
    classifyReadiness,
    inspectContract,
  });
})(window);
