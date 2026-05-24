/*
  Phase 2.23 dev-only cross-candidate_group continuity sandbox.

  This sandbox lets analysis exploration candidate_groups coexist and reference one
  another structurally. It does not merge candidate_groups into interpretation, own
  production rendering, mutate production overlay registries, persist state,
  start workers, fetch, or expose raw backend payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const SANDBOX_MODE = "dev_cross_candidate_group_continuity_sandbox_only";
  const OVERLAY_CLASS = "phase2-23-cross-candidate_group-continuity-sandbox-overlay";
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
  const CANDIDATE_GROUP_FIELDS = Object.freeze([
    "continuity_group_id",
    "continuity_group_generation",
    "continuity_group_lineage",
    "contributing_groups",
    "continuity_status",
    "coexistence_scope",
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
    if (includesForbiddenField(scope)) return Object.freeze({ accepted: false, reason: "raw_or_forbidden_viewport_field" });
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
      }),
    });
  }

  function sanitizeCandidateGroupMetadata(metadata) {
    const source = metadata || {};
    if (includesForbiddenField(source)) return Object.freeze({ accepted: false, reason: "raw_or_forbidden_candidate_group_field" });
    const output = copyFields(source, CANDIDATE_GROUP_FIELDS);
    const lineage = Array.isArray(output.continuity_group_lineage) ? output.continuity_group_lineage.map(item => String(item)) : [];
    const contributors = Array.isArray(output.contributing_groups) ? output.contributing_groups.map(item => String(item)) : [];
    return Object.freeze({
      accepted: true,
      metadata: Object.freeze({
        continuity_group_id: String(output.continuity_group_id || "analysis-candidate_group"),
        continuity_group_generation: Math.max(1, Math.floor(numberOrZero(output.continuity_group_generation || 1))),
        continuity_group_lineage: Object.freeze(lineage),
        contributing_groups: Object.freeze(contributors),
        continuity_status: String(output.continuity_status || "coexisting"),
        coexistence_scope: String(output.coexistence_scope || "current_viewport"),
        interpretation_boundary_preserved: true,
        no_unified_meaning_surface: true,
        recommendation_boundary_preserved: true,
        convergence_validates_truth_claimed: false,
        scoring_boundary_preserved: true,
        forbidden_recommendation_surface_absent: true,
      }),
    });
  }

  function sanitizeHydrationEnvelope(envelope) {
    assertObject(envelope, "cross-candidate_group continuity sandbox envelope");
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

  function createCrossCandidateGroupContinuitySandbox(options) {
    const documentRef = options?.document || global.document;
    const root = options?.root || documentRef?.createElement("div");
    if (!documentRef || !root) throw new TypeError("document and root are required");
    const initialScope = sanitizeViewportScope(options?.viewport_scope || options?.viewportScope || { id: "initial" });
    if (!initialScope.accepted) throw new TypeError(initialScope.reason);
    const overlays = new Map();
    const candidateGroupLineage = new Map();
    let activeViewport = initialScope.scope;
    let sequence = 0;

    function overlayKey(namespace, viewportId, candidateGroupId) {
      return `${String(viewportId)}::${String(namespace)}::${String(candidateGroupId)}`;
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
        interpretation_boundary_preserved: true,
        no_unified_meaning_surface: true,
        recommendation_boundary_preserved: true,
        convergence_validates_truth_claimed: false,
      });
    }

    function renderOverlay(record) {
      const node = documentRef.createElement("div");
      node.className = OVERLAY_CLASS;
      node.setAttribute("data-phase", "2.23");
      node.setAttribute("data-dev-only", "true");
      node.setAttribute("data-renderer-substrate", RENDERER_SUBSTRATE);
      node.setAttribute("data-overlay-namespace", record.namespace);
      node.setAttribute("data-candidate_group-id", record.candidate_group.continuity_group_id);
      node.setAttribute("data-continuity-status", record.candidate_group.continuity_status);
      node.setAttribute("data-candidate_group-generation", String(record.candidate_group.continuity_group_generation));
      node.setAttribute("data-cache-key", record.cache_key);
      node.setAttribute("data-viewport-id", record.viewport.id);
      node.setAttribute("role", "presentation");
      node.textContent = `Phase 2.23 ${record.candidate_group.continuity_group_id}: ${record.candidate_group.continuity_status}`;
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
        .sort((a, b) => a.order - b.order || a.candidate_group.continuity_group_id.localeCompare(b.candidate_group.continuity_group_id))
        .map(record => Object.freeze({
          overlay_id: record.overlay_id,
          namespace: record.namespace,
          cache_key: record.cache_key,
          order: record.order,
          viewport_id: record.viewport.id,
          continuity_group_id: record.candidate_group.continuity_group_id,
          continuity_group_generation: record.candidate_group.continuity_group_generation,
          continuity_group_lineage: record.candidate_group.continuity_group_lineage,
          contributing_groups: record.candidate_group.contributing_groups,
          continuity_status: record.candidate_group.continuity_status,
          coexistence_scope: record.candidate_group.coexistence_scope,
          adjacent_candidate_field_id: record.adjacent_candidate.adjacent_candidate_field_id,
          aggregate_candidate_field_id: record.aggregate_candidate.aggregate_candidate_field_id,
          density_affects_activity_not_truth: true,
          interpretation_boundary_preserved: true,
          no_unified_meaning_surface: true,
          recommendation_boundary_preserved: true,
          convergence_validates_truth_claimed: false,
          scoring_boundary_preserved: true,
          forbidden_recommendation_surface_absent: true,
          final_truth_claimed: false,
        })));
    }

    function lineageFor(candidateGroupId) {
      return Object.freeze((candidateGroupLineage.get(candidateGroupId) || []).map(item => Object.freeze({ ...item })));
    }

    function hydrateCandidateGroup(envelope, optionsForOverlay) {
      const sanitized = sanitizeHydrationEnvelope(envelope);
      if (!sanitized.accepted) return reject(sanitized.reason);
      const requestedScope = sanitizeViewportScope(optionsForOverlay?.viewport_scope || optionsForOverlay?.viewportScope || activeViewport);
      if (!requestedScope.accepted) return reject(requestedScope.reason);
      if (requestedScope.id !== activeViewport.id) return reject("viewport_scope_mismatch");
      const adaptive = sanitizeAdaptiveMetadata(optionsForOverlay?.adaptive || optionsForOverlay?.adaptive_metadata || optionsForOverlay?.adaptiveMetadata || {});
      if (!adaptive.accepted) return reject(adaptive.reason);
      const adjacent_candidate = sanitizeAdjacentCandidateMetadata(optionsForOverlay?.adjacent_candidate || optionsForOverlay?.adjacent_candidate_metadata || optionsForOverlay?.adjacent_candidateMetadata || {});
      if (!adjacent_candidate.accepted) return reject(adjacent_candidate.reason);
      const aggregate_candidate = sanitizeAggregateCandidateMetadata(optionsForOverlay?.aggregate_candidate || optionsForOverlay?.aggregate_candidate_metadata || optionsForOverlay?.aggregate_candidateMetadata || {});
      if (!aggregate_candidate.accepted) return reject(aggregate_candidate.reason);
      const candidate_group = sanitizeCandidateGroupMetadata(optionsForOverlay?.candidate_group || optionsForOverlay?.candidate_group_metadata || optionsForOverlay?.candidate_groupMetadata || {});
      if (!candidate_group.accepted) return reject(candidate_group.reason);
      const namespace = overlayNamespace(optionsForOverlay, sanitized);
      const candidateGroupId = candidate_group.metadata.continuity_group_id;
      const key = overlayKey(namespace, requestedScope.id, candidateGroupId);
      const prior = overlays.get(key);
      if (prior && candidate_group.metadata.continuity_group_generation < prior.candidate_group.continuity_group_generation) {
        return reject("older_continuity_group_generation");
      }
      if (prior) removeRecord(key);
      const order = prior ? prior.order + 1 : ++sequence;
      const overlayId = `${key}::candidate_group-${candidate_group.metadata.continuity_group_generation}`;
      const lineageEntry = Object.freeze({
        overlay_id: overlayId,
        superseded_overlay_id: prior?.overlay_id || null,
        cache_key: sanitized.cache_key,
        continuity_group_generation: candidate_group.metadata.continuity_group_generation,
        continuity_status: candidate_group.metadata.continuity_status,
        contributing_groups: candidate_group.metadata.contributing_groups,
      });
      candidateGroupLineage.set(candidateGroupId, Object.freeze([...(candidateGroupLineage.get(candidateGroupId) || []), lineageEntry]));
      const record = {
        overlay_id: overlayId,
        namespace,
        cache_key: sanitized.cache_key,
        hydration: sanitized.metadata,
        observer: sanitized.observer,
        adaptive: adaptive.metadata,
        adjacent_candidate: adjacent_candidate.metadata,
        aggregate_candidate: aggregate_candidate.metadata,
        candidate_group: candidate_group.metadata,
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
        action: prior ? "candidate_group_continuity_superseded" : "created",
        visible: true,
        overlay_kind: "isolated_dev_cross_candidate_group_continuity_overlay",
        overlay_id: overlayId,
        superseded_overlay_id: prior?.overlay_id || null,
        namespace,
        cache_key: sanitized.cache_key,
        viewport_id: requestedScope.id,
        adaptive: adaptive.metadata,
        adjacent_candidate: adjacent_candidate.metadata,
        aggregate_candidate: aggregate_candidate.metadata,
        candidate_group: candidate_group.metadata,
        lineage: lineageFor(candidateGroupId),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        interpretation_boundary_preserved: true,
        no_unified_meaning_surface: true,
        recommendation_boundary_preserved: true,
        convergence_validates_truth_claimed: false,
        scoring_boundary_preserved: true,
        forbidden_recommendation_surface_absent: true,
        density_affects_activity_not_truth: true,
        final_truth_claimed: false,
      });
    }

    function invalidateCandidateGroup(candidateGroupId, reason) {
      const removed = [];
      Array.from(overlays.entries()).forEach(([key, record]) => {
        if (record.candidate_group.continuity_group_id === String(candidateGroupId)) {
          removeRecord(key);
          removed.push(record.namespace);
        }
      });
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        invalidated: removed.length > 0,
        reason: String(reason || "candidate_group_invalidated"),
        continuity_group_id: String(candidateGroupId || ""),
        removed: Object.freeze(removed),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        interpretation_boundary_preserved: true,
        no_unified_meaning_surface: true,
        recommendation_boundary_preserved: true,
        convergence_validates_truth_claimed: false,
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
        interpretation_boundary_preserved: true,
        no_unified_meaning_surface: true,
        recommendation_boundary_preserved: true,
        convergence_validates_truth_claimed: false,
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
        interpretation_boundary_preserved: true,
        no_unified_meaning_surface: true,
        recommendation_boundary_preserved: true,
        convergence_validates_truth_claimed: false,
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
        interpretation_boundary_preserved: true,
        no_unified_meaning_surface: true,
        recommendation_boundary_preserved: true,
        convergence_validates_truth_claimed: false,
      });
    }

    return Object.freeze({
      hydrateCandidateGroup,
      invalidateCandidateGroup,
      setViewportScope,
      removeAll,
      inspect,
    });
  }

  global.RelocationSamplingCacheCrossCandidateGroupContinuitySandbox = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    SANDBOX_MODE,
    OVERLAY_CLASS,
    createCrossCandidateGroupContinuitySandbox,
  });
})(window);
