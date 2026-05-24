/*
  Phase 2.22 dev-only aggregate_candidate-field sandbox.

  This sandbox accumulates sanitized adjacent_candidate fields into exploratory
  aggregate_candidate aggregate continuity. It does not own production rendering, mutate production
  overlay registries, persist state, start workers, fetch, or expose raw backend
  payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const SANDBOX_MODE = "dev_aggregate_candidate_field_sandbox_only";
  const OVERLAY_CLASS = "phase2-22-aggregate_candidate-field-sandbox-overlay";
  const FORBIDDEN_FIELDS = Object.freeze([
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
  const HYDRATION_FIELDS = Object.freeze([
    "schema_version",
    "key",
    "status",
    "summary",
    "metrics",
    "created_at_ms",
    "updated_at_ms",
    "expires_at_ms",
  ]);
  const VIEWPORT_FIELDS = Object.freeze([
    "id",
    "zoom",
    "north",
    "south",
    "east",
    "west",
    "semantic_id",
  ]);
  const ADAPTIVE_FIELDS = Object.freeze([
    "refinement_density",
    "refinement_load",
    "boundary_priority",
    "interior_stability",
    "refinement_budget",
    "adaptive_generation",
  ]);
  const AMBIGUITY_FIELDS = Object.freeze([
    "ambiguity_continuity_group_id",
    "ambiguity_confidence",
    "ambiguity_overlap",
    "candidate_refinement_ids",
    "uncertainty_generation",
    "ambiguity_status",
  ]);
  const ADJACENT_CANDIDATE_FIELDS = Object.freeze([
    "adjacent_candidate_field_id",
    "adjacent_candidate_direction",
    "adjacency_weight",
    "adjacent_candidate_source_candidate_group",
    "adjacent_candidate_generation",
    "adjacent_candidate_status",
  ]);
  const AGGREGATE_CANDIDATE_FIELDS = Object.freeze([
    "aggregate_candidate_field_id",
    "aggregate_candidate_generation",
    "aggregate_weight",
    "aggregate_candidate_contributors",
    "aggregate_candidate_status",
    "aggregate_candidate_lineage",
    "aggregate_candidate_scope",
  ]);

  function assertObject(value, label) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new TypeError(`${label} must be an object`);
    }
  }

  function cloneJson(value) {
    if (value == null) return value;
    return JSON.parse(JSON.stringify(value));
  }

  function includesForbiddenField(value) {
    if (!value || typeof value !== "object") return false;
    if (Array.isArray(value)) return value.some(includesForbiddenField);
    return Object.keys(value).some(key => (
      FORBIDDEN_FIELDS.includes(key) || includesForbiddenField(value[key])
    ));
  }

  function copyFields(source, fields) {
    const output = {};
    fields.forEach(field => {
      if (source[field] !== undefined) output[field] = cloneJson(source[field]);
    });
    return Object.freeze(output);
  }

  function stableStringify(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
    return `{${Object.keys(value).sort().map(key => (
      `${JSON.stringify(key)}:${stableStringify(value[key])}`
    )).join(",")}}`;
  }

  function numberOrZero(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : 0;
  }

  function clamp01(value) {
    return Math.max(0, Math.min(1, numberOrZero(value)));
  }

  function stateIsBlocked(envelope) {
    const observerState = String(envelope.observer?.observer_state || "");
    const executionState = String(envelope.execution?.state || envelope.execution?.job?.state || "");
    return Boolean(
      observerState === "stale" ||
      observerState === "cancelled" ||
      executionState === "stale" ||
      executionState === "cancelled" ||
      envelope.execution?.job?.stale ||
      envelope.execution?.job?.cancelled
    );
  }

  function sanitizeViewportScope(scope) {
    assertObject(scope, "viewport scope");
    if (includesForbiddenField(scope)) {
      return Object.freeze({ accepted: false, reason: "raw_or_forbidden_viewport_field" });
    }
    const output = {};
    VIEWPORT_FIELDS.forEach(field => {
      if (scope[field] !== undefined) output[field] = cloneJson(scope[field]);
    });
    if (!output.id && output.semantic_id) output.id = output.semantic_id;
    if (!output.id) output.id = stableStringify(output);
    output.id = String(output.id);
    output.zoom = Number(output.zoom || 0);
    return Object.freeze({ accepted: true, scope: Object.freeze(output), id: output.id });
  }

  function sanitizeAdaptiveMetadata(metadata) {
    const source = metadata || {};
    if (includesForbiddenField(source)) return Object.freeze({ accepted: false, reason: "raw_or_forbidden_adaptive_field" });
    const output = copyFields(source, ADAPTIVE_FIELDS);
    return Object.freeze({
      accepted: true,
      metadata: Object.freeze({
        refinement_density: String(output.refinement_density || "medium"),
        refinement_load: clamp01(output.refinement_load),
        boundary_priority: clamp01(output.boundary_priority),
        interior_stability: clamp01(output.interior_stability),
        refinement_budget: Math.max(0, Math.floor(numberOrZero(output.refinement_budget || 1))),
        adaptive_generation: Math.max(1, Math.floor(numberOrZero(output.adaptive_generation || 1))),
        density_affects_activity_not_truth: true,
      }),
    });
  }

  function sanitizeAmbiguityMetadata(metadata) {
    const source = metadata || {};
    if (includesForbiddenField(source)) return Object.freeze({ accepted: false, reason: "raw_or_forbidden_ambiguity_field" });
    const output = copyFields(source, AMBIGUITY_FIELDS);
    const candidates = Array.isArray(output.candidate_refinement_ids)
      ? output.candidate_refinement_ids.map(item => String(item))
      : [];
    return Object.freeze({
      accepted: true,
      metadata: Object.freeze({
        ambiguity_continuity_group_id: String(output.ambiguity_continuity_group_id || "ambiguity-candidate-group"),
        ambiguity_confidence: clamp01(output.ambiguity_confidence),
        ambiguity_overlap: clamp01(output.ambiguity_overlap),
        candidate_refinement_ids: Object.freeze(candidates),
        uncertainty_generation: Math.max(1, Math.floor(numberOrZero(output.uncertainty_generation || 1))),
        ambiguity_status: String(output.ambiguity_status || "unresolved"),
        ambiguity_is_error: false,
        overlapping_candidates_confirmed_truth: false,
        unresolved_structure_invalid: false,
      }),
    });
  }

  function sanitizeAdjacentCandidateMetadata(metadata) {
    const source = metadata || {};
    if (includesForbiddenField(source)) return Object.freeze({ accepted: false, reason: "raw_or_forbidden_adjacent_candidate_field" });
    const output = copyFields(source, ADJACENT_CANDIDATE_FIELDS);
    return Object.freeze({
      accepted: true,
      metadata: Object.freeze({
        adjacent_candidate_field_id: String(output.adjacent_candidate_field_id || "adjacent_candidate-field"),
        adjacent_candidate_direction: String(output.adjacent_candidate_direction || "nearby"),
        adjacency_weight: clamp01(output.adjacency_weight),
        adjacent_candidate_source_candidate_group: String(output.adjacent_candidate_source_candidate_group || ""),
        adjacent_candidate_generation: Math.max(1, Math.floor(numberOrZero(output.adjacent_candidate_generation || 1))),
        adjacent_candidate_status: String(output.adjacent_candidate_status || "unresolved"),
        adjacent_candidate_confirmed_truth_claimed: false,
        directional_continuity_claimed: false,
        ontology_boundary_preserved: true,
      }),
    });
  }

  function sanitizeAggregateCandidateMetadata(metadata) {
    const source = metadata || {};
    if (includesForbiddenField(source)) return Object.freeze({ accepted: false, reason: "raw_or_forbidden_aggregate_candidate_field" });
    const output = copyFields(source, AGGREGATE_CANDIDATE_FIELDS);
    const contributors = Array.isArray(output.aggregate_candidate_contributors)
      ? output.aggregate_candidate_contributors.map(item => String(item))
      : [];
    const lineage = Array.isArray(output.aggregate_candidate_lineage)
      ? output.aggregate_candidate_lineage.map(item => String(item))
      : [];
    return Object.freeze({
      accepted: true,
      metadata: Object.freeze({
        aggregate_candidate_field_id: String(output.aggregate_candidate_field_id || "aggregate_candidate-field"),
        aggregate_candidate_generation: Math.max(1, Math.floor(numberOrZero(output.aggregate_candidate_generation || 1))),
        aggregate_weight: clamp01(output.aggregate_weight),
        aggregate_candidate_contributors: Object.freeze(contributors),
        aggregate_candidate_status: String(output.aggregate_candidate_status || "exploratory"),
        aggregate_candidate_lineage: Object.freeze(lineage),
        aggregate_candidate_scope: String(output.aggregate_candidate_scope || "current_viewport"),
        aggregate_candidate_confirmed_truth_claimed: false,
        interpretation_boundary_preserved: true,
        recommendation_boundary_preserved: true,
        predictive_authority_boundary_preserved: true,
        aggregate_continuity_claimed: false,
        no_visual_theater_surface: true,
      }),
    });
  }

  function sanitizeHydrationEnvelope(envelope) {
    assertObject(envelope, "aggregate_candidate field sandbox envelope");
    if (includesForbiddenField(envelope)) return Object.freeze({ accepted: false, reason: "raw_or_forbidden_field_present" });
    const hydrationEnvelope = envelope.hydration || envelope;
    assertObject(hydrationEnvelope, "hydration envelope");
    const metadata = hydrationEnvelope.hydration;
    assertObject(metadata, "hydration metadata");
    const compatible = hydrationEnvelope.compatible === true;
    const hydrated = hydrationEnvelope.hydrated === true;
    const visible = envelope.observer?.hydration_visible !== false;
    const readOnly = envelope.observer ? envelope.observer.read_only === true : true;
    if (!compatible || !hydrated || !visible || !readOnly || stateIsBlocked(envelope)) {
      return Object.freeze({ accepted: false, reason: "not_hydration_visible" });
    }
    if (String(metadata.status || "") !== "ready") {
      return Object.freeze({ accepted: false, reason: "metadata_not_ready" });
    }
    return Object.freeze({
      accepted: true,
      cache_key: String(hydrationEnvelope.cache_key || metadata.key || ""),
      metadata: copyFields(metadata, HYDRATION_FIELDS),
      observer: Object.freeze({
        observer_state: String(envelope.observer?.observer_state || "hydration_eligible"),
        discovery_state: String(envelope.observer?.discovery_state || "nearby_structure_available"),
        display_state: String(envelope.observer?.display_state || "transitioning"),
        read_only: true,
      }),
    });
  }

  function overlayNamespace(options, sanitized) {
    return String(options?.namespace || options?.overlay_namespace || options?.overlayNamespace || sanitized.cache_key || "dev-overlay");
  }

  function createAggregateCandidateFieldSandbox(options) {
    const documentRef = options?.document || global.document;
    const root = options?.root || documentRef?.createElement("div");
    if (!documentRef || !root) throw new TypeError("document and root are required");
    const initialScope = sanitizeViewportScope(options?.viewport_scope || options?.viewportScope || { id: "initial" });
    if (!initialScope.accepted) throw new TypeError(initialScope.reason);
    const overlays = new Map();
    const aggregateCandidateLineage = new Map();
    let activeViewport = initialScope.scope;
    let sequence = 0;

    function overlayKey(namespace, viewportId, aggregate_candidateId) {
      return `${String(viewportId)}::${String(namespace)}::${String(aggregate_candidateId)}`;
    }

    function reject(reason) {
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        accepted: false,
        reason,
        visible: false,
        overlay_count: overlays.size,
        viewport_id: activeViewport.id,
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        aggregate_candidate_confirmed_truth_claimed: false,
        interpretation_boundary_preserved: true,
        recommendation_boundary_preserved: true,
        predictive_authority_boundary_preserved: true,
        aggregate_continuity_claimed: false,
        no_visual_theater_surface: true,
      });
    }

    function renderOverlay(record) {
      const node = documentRef.createElement("div");
      node.className = OVERLAY_CLASS;
      node.setAttribute("data-phase", "2.22");
      node.setAttribute("data-dev-only", "true");
      node.setAttribute("data-renderer-substrate", RENDERER_SUBSTRATE);
      node.setAttribute("data-overlay-namespace", record.namespace);
      node.setAttribute("data-aggregate_candidate-field-id", record.aggregate_candidate.aggregate_candidate_field_id);
      node.setAttribute("data-aggregate_candidate-status", record.aggregate_candidate.aggregate_candidate_status);
      node.setAttribute("data-aggregate_candidate-generation", String(record.aggregate_candidate.aggregate_candidate_generation));
      node.setAttribute("data-cache-key", record.cache_key);
      node.setAttribute("data-viewport-id", record.viewport.id);
      node.setAttribute("role", "presentation");
      node.textContent = `Phase 2.22 ${record.namespace}: ${record.aggregate_candidate.aggregate_candidate_status}`;
      return node;
    }

    function removeRecord(key) {
      const record = overlays.get(key);
      if (!record) return false;
      if (record.node.parentNode) record.node.parentNode.removeChild(record.node);
      overlays.delete(key);
      return true;
    }

    function snapshotRecords() {
      return Object.freeze(Array.from(overlays.values())
        .sort((a, b) => a.order - b.order || a.namespace.localeCompare(b.namespace))
        .map(record => Object.freeze({
          overlay_id: record.overlay_id,
          namespace: record.namespace,
          cache_key: record.cache_key,
          order: record.order,
          viewport_id: record.viewport.id,
          adjacent_candidate_field_id: record.adjacent_candidate.adjacent_candidate_field_id,
          ambiguity_continuity_group_id: record.ambiguity.ambiguity_continuity_group_id,
          aggregate_candidate_field_id: record.aggregate_candidate.aggregate_candidate_field_id,
          aggregate_candidate_generation: record.aggregate_candidate.aggregate_candidate_generation,
          aggregate_weight: record.aggregate_candidate.aggregate_weight,
          aggregate_candidate_contributors: record.aggregate_candidate.aggregate_candidate_contributors,
          aggregate_candidate_status: record.aggregate_candidate.aggregate_candidate_status,
          aggregate_candidate_scope: record.aggregate_candidate.aggregate_candidate_scope,
          aggregate_candidate_confirmed_truth_claimed: false,
          interpretation_boundary_preserved: true,
          recommendation_boundary_preserved: true,
          predictive_authority_boundary_preserved: true,
          aggregate_continuity_claimed: false,
          no_visual_theater_surface: true,
          density_affects_activity_not_truth: true,
          adjacent_candidate_confirmed_truth_claimed: false,
          final_truth_claimed: false,
        })));
    }

    function lineageFor(aggregate_candidateId) {
      return Object.freeze((aggregateCandidateLineage.get(aggregate_candidateId) || []).map(item => Object.freeze({ ...item })));
    }

    function hydrateAggregateCandidate(envelope, optionsForOverlay) {
      const sanitized = sanitizeHydrationEnvelope(envelope);
      if (!sanitized.accepted) return reject(sanitized.reason);
      const requestedScope = sanitizeViewportScope(optionsForOverlay?.viewport_scope || optionsForOverlay?.viewportScope || activeViewport);
      if (!requestedScope.accepted) return reject(requestedScope.reason);
      if (requestedScope.id !== activeViewport.id) return reject("viewport_scope_mismatch");
      const adaptive = sanitizeAdaptiveMetadata(optionsForOverlay?.adaptive || optionsForOverlay?.adaptive_metadata || optionsForOverlay?.adaptiveMetadata || {});
      if (!adaptive.accepted) return reject(adaptive.reason);
      const ambiguity = sanitizeAmbiguityMetadata(optionsForOverlay?.ambiguity || optionsForOverlay?.ambiguity_metadata || optionsForOverlay?.ambiguityMetadata || {});
      if (!ambiguity.accepted) return reject(ambiguity.reason);
      const adjacent_candidate = sanitizeAdjacentCandidateMetadata(optionsForOverlay?.adjacent_candidate || optionsForOverlay?.adjacent_candidate_metadata || optionsForOverlay?.adjacent_candidateMetadata || {});
      if (!adjacent_candidate.accepted) return reject(adjacent_candidate.reason);
      const aggregate_candidate = sanitizeAggregateCandidateMetadata(optionsForOverlay?.aggregate_candidate || optionsForOverlay?.aggregate_candidate_metadata || optionsForOverlay?.aggregate_candidateMetadata || {});
      if (!aggregate_candidate.accepted) return reject(aggregate_candidate.reason);
      const namespace = overlayNamespace(optionsForOverlay, sanitized);
      const aggregate_candidateId = aggregate_candidate.metadata.aggregate_candidate_field_id;
      const key = overlayKey(namespace, requestedScope.id, aggregate_candidateId);
      const prior = overlays.get(key);
      if (prior && aggregate_candidate.metadata.aggregate_candidate_generation < prior.aggregate_candidate.aggregate_candidate_generation) {
        return reject("older_aggregate_candidate_generation");
      }
      if (prior) removeRecord(key);
      const order = prior ? prior.order + 1 : ++sequence;
      const overlayId = `${key}::aggregate_candidate-${aggregate_candidate.metadata.aggregate_candidate_generation}`;
      const lineageEntry = Object.freeze({
        overlay_id: overlayId,
        superseded_overlay_id: prior?.overlay_id || null,
        cache_key: sanitized.cache_key,
        aggregate_candidate_generation: aggregate_candidate.metadata.aggregate_candidate_generation,
        aggregate_candidate_status: aggregate_candidate.metadata.aggregate_candidate_status,
        aggregate_candidate_contributors: aggregate_candidate.metadata.aggregate_candidate_contributors,
        adjacent_candidate_field_id: adjacent_candidate.metadata.adjacent_candidate_field_id,
      });
      aggregateCandidateLineage.set(aggregate_candidateId, Object.freeze([...(aggregateCandidateLineage.get(aggregate_candidateId) || []), lineageEntry]));
      const record = {
        overlay_id: overlayId,
        namespace,
        cache_key: sanitized.cache_key,
        hydration: sanitized.metadata,
        observer: sanitized.observer,
        adaptive: adaptive.metadata,
        ambiguity: ambiguity.metadata,
        adjacent_candidate: adjacent_candidate.metadata,
        aggregate_candidate: aggregate_candidate.metadata,
        viewport: requestedScope.scope,
        order,
      };
      record.node = renderOverlay(record);
      overlays.set(key, record);
      root.appendChild(record.node);
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        accepted: true,
        action: prior ? "aggregate_candidate_superseded" : "created",
        visible: true,
        overlay_kind: "isolated_dev_aggregate_candidate_field_overlay",
        overlay_id: overlayId,
        superseded_overlay_id: prior?.overlay_id || null,
        namespace,
        cache_key: sanitized.cache_key,
        viewport_id: requestedScope.id,
        adaptive: adaptive.metadata,
        ambiguity: ambiguity.metadata,
        adjacent_candidate: adjacent_candidate.metadata,
        aggregate_candidate: aggregate_candidate.metadata,
        lineage: lineageFor(aggregate_candidateId),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        aggregate_candidate_confirmed_truth_claimed: false,
        interpretation_boundary_preserved: true,
        recommendation_boundary_preserved: true,
        predictive_authority_boundary_preserved: true,
        aggregate_continuity_claimed: false,
        no_visual_theater_surface: true,
        density_affects_activity_not_truth: true,
        adjacent_candidate_confirmed_truth_claimed: false,
        final_truth_claimed: false,
      });
    }

    function invalidateAggregateCandidate(aggregate_candidateId, reason) {
      const removed = [];
      Array.from(overlays.entries()).forEach(([key, record]) => {
        if (record.aggregate_candidate.aggregate_candidate_field_id === String(aggregate_candidateId)) {
          removeRecord(key);
          removed.push(record.namespace);
        }
      });
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        invalidated: removed.length > 0,
        reason: String(reason || "aggregate_candidate_invalidated"),
        aggregate_candidate_field_id: String(aggregate_candidateId || ""),
        removed: Object.freeze(removed),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        aggregate_candidate_confirmed_truth_claimed: false,
        interpretation_boundary_preserved: true,
        recommendation_boundary_preserved: true,
        predictive_authority_boundary_preserved: true,
        aggregate_continuity_claimed: false,
        no_visual_theater_surface: true,
      });
    }

    function setViewportScope(scope) {
      const next = sanitizeViewportScope(scope);
      if (!next.accepted) return reject(next.reason);
      activeViewport = next.scope;
      const invalidated = [];
      Array.from(overlays.entries()).forEach(([key, record]) => {
        if (record.viewport.id !== activeViewport.id) {
          removeRecord(key);
          invalidated.push(record.namespace);
        }
      });
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        accepted: true,
        viewport_id: activeViewport.id,
        invalidated: Object.freeze(invalidated),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        aggregate_candidate_confirmed_truth_claimed: false,
        interpretation_boundary_preserved: true,
        recommendation_boundary_preserved: true,
        predictive_authority_boundary_preserved: true,
        aggregate_continuity_claimed: false,
        no_visual_theater_surface: true,
      });
    }

    function removeAll() {
      Array.from(overlays.keys()).forEach(removeRecord);
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        removed: true,
        viewport_id: activeViewport.id,
        overlay_count: overlays.size,
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        aggregate_candidate_confirmed_truth_claimed: false,
        interpretation_boundary_preserved: true,
        recommendation_boundary_preserved: true,
        predictive_authority_boundary_preserved: true,
        aggregate_continuity_claimed: false,
        no_visual_theater_surface: true,
      });
    }

    function inspect() {
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        viewport_id: activeViewport.id,
        viewport_scope: cloneJson(activeViewport),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        dom_overlay_count: root.querySelectorAll(`.${OVERLAY_CLASS}`).length,
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        aggregate_candidate_confirmed_truth_claimed: false,
        interpretation_boundary_preserved: true,
        recommendation_boundary_preserved: true,
        predictive_authority_boundary_preserved: true,
        aggregate_continuity_claimed: false,
        no_visual_theater_surface: true,
      });
    }

    return Object.freeze({
      hydrateAggregateCandidate,
      invalidateAggregateCandidate,
      setViewportScope,
      removeAll,
      inspect,
    });
  }

  global.RelocationSamplingCacheAggregateCandidateFieldSandbox = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    SANDBOX_MODE,
    OVERLAY_CLASS,
    createAggregateCandidateFieldSandbox,
  });
})(window);
