/*
  Phase 2.20 dev-only ambiguity-candidate-group sandbox.

  This sandbox represents unresolved or overlapping ambiguity candidate_groups from
  sanitized metadata. It does not own production rendering, mutate production
  overlay registries, persist state, start workers, fetch, or expose raw
  backend payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const SANDBOX_MODE = "dev_ambiguity_candidate_group_sandbox_only";
  const OVERLAY_CLASS = "phase2-20-ambiguity-candidate-group-sandbox-overlay";
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
    if (includesForbiddenField(source)) {
      return Object.freeze({ accepted: false, reason: "raw_or_forbidden_adaptive_field" });
    }
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
    if (includesForbiddenField(source)) {
      return Object.freeze({ accepted: false, reason: "raw_or_forbidden_ambiguity_field" });
    }
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

  function sanitizeHydrationEnvelope(envelope) {
    assertObject(envelope, "ambiguity candidate_group sandbox envelope");
    if (includesForbiddenField(envelope)) {
      return Object.freeze({ accepted: false, reason: "raw_or_forbidden_field_present" });
    }
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
        discovery_state: String(envelope.observer?.discovery_state || "unresolved_ambiguity"),
        display_state: String(envelope.observer?.display_state || "transitioning"),
        read_only: true,
      }),
    });
  }

  function overlayNamespace(options, sanitized) {
    return String(
      options?.namespace ||
      options?.overlay_namespace ||
      options?.overlayNamespace ||
      sanitized.cache_key ||
      "dev-overlay"
    );
  }

  function createAmbiguityCandidateGroupSandbox(options) {
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
        ambiguity_is_error: false,
        overlapping_candidates_confirmed_truth: false,
        unresolved_structure_invalid: false,
      });
    }

    function renderOverlay(record) {
      const node = documentRef.createElement("div");
      node.className = OVERLAY_CLASS;
      node.setAttribute("data-phase", "2.20");
      node.setAttribute("data-dev-only", "true");
      node.setAttribute("data-renderer-substrate", RENDERER_SUBSTRATE);
      node.setAttribute("data-overlay-namespace", record.namespace);
      node.setAttribute("data-ambiguity-candidate-group-id", record.ambiguity.ambiguity_continuity_group_id);
      node.setAttribute("data-ambiguity-status", record.ambiguity.ambiguity_status);
      node.setAttribute("data-uncertainty-generation", String(record.ambiguity.uncertainty_generation));
      node.setAttribute("data-cache-key", record.cache_key);
      node.setAttribute("data-viewport-id", record.viewport.id);
      node.setAttribute("role", "presentation");
      node.textContent = `Phase 2.20 ${record.namespace}: ${record.ambiguity.ambiguity_status}`;
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
          ambiguity_continuity_group_id: record.ambiguity.ambiguity_continuity_group_id,
          ambiguity_confidence: record.ambiguity.ambiguity_confidence,
          ambiguity_overlap: record.ambiguity.ambiguity_overlap,
          candidate_refinement_ids: record.ambiguity.candidate_refinement_ids,
          uncertainty_generation: record.ambiguity.uncertainty_generation,
          ambiguity_status: record.ambiguity.ambiguity_status,
          ambiguity_is_error: false,
          overlapping_candidates_confirmed_truth: false,
          unresolved_structure_invalid: false,
          density_affects_activity_not_truth: true,
          final_truth_claimed: false,
        })));
    }

    function lineageFor(candidateGroupId) {
      return Object.freeze((candidateGroupLineage.get(candidateGroupId) || []).map(item => Object.freeze({ ...item })));
    }

    function hydrateAmbiguity(envelope, optionsForOverlay) {
      const sanitized = sanitizeHydrationEnvelope(envelope);
      if (!sanitized.accepted) return reject(sanitized.reason);
      const requestedScope = sanitizeViewportScope(
        optionsForOverlay?.viewport_scope ||
        optionsForOverlay?.viewportScope ||
        activeViewport
      );
      if (!requestedScope.accepted) return reject(requestedScope.reason);
      if (requestedScope.id !== activeViewport.id) return reject("viewport_scope_mismatch");
      const adaptive = sanitizeAdaptiveMetadata(
        optionsForOverlay?.adaptive ||
        optionsForOverlay?.adaptive_metadata ||
        optionsForOverlay?.adaptiveMetadata ||
        {}
      );
      if (!adaptive.accepted) return reject(adaptive.reason);
      const ambiguity = sanitizeAmbiguityMetadata(
        optionsForOverlay?.ambiguity ||
        optionsForOverlay?.ambiguity_metadata ||
        optionsForOverlay?.ambiguityMetadata ||
        {}
      );
      if (!ambiguity.accepted) return reject(ambiguity.reason);
      const namespace = overlayNamespace(optionsForOverlay, sanitized);
      const candidateGroupId = ambiguity.metadata.ambiguity_continuity_group_id;
      const key = overlayKey(namespace, requestedScope.id, candidateGroupId);
      const prior = overlays.get(key);
      if (prior && ambiguity.metadata.uncertainty_generation < prior.ambiguity.uncertainty_generation) {
        return reject("older_uncertainty_generation");
      }
      if (prior) removeRecord(key);
      const order = prior ? prior.order + 1 : ++sequence;
      const overlayId = `${key}::uncertainty-${ambiguity.metadata.uncertainty_generation}`;
      const lineageEntry = Object.freeze({
        overlay_id: overlayId,
        superseded_overlay_id: prior?.overlay_id || null,
        cache_key: sanitized.cache_key,
        uncertainty_generation: ambiguity.metadata.uncertainty_generation,
        ambiguity_status: ambiguity.metadata.ambiguity_status,
        candidate_refinement_ids: ambiguity.metadata.candidate_refinement_ids,
      });
      candidateGroupLineage.set(candidateGroupId, Object.freeze([...(candidateGroupLineage.get(candidateGroupId) || []), lineageEntry]));
      const record = {
        overlay_id: overlayId,
        namespace,
        cache_key: sanitized.cache_key,
        hydration: sanitized.metadata,
        observer: sanitized.observer,
        adaptive: adaptive.metadata,
        ambiguity: ambiguity.metadata,
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
        action: prior ? "ambiguity_superseded" : "created",
        visible: true,
        overlay_kind: "isolated_dev_ambiguity_candidate_group_overlay",
        overlay_id: overlayId,
        superseded_overlay_id: prior?.overlay_id || null,
        namespace,
        cache_key: sanitized.cache_key,
        viewport_id: requestedScope.id,
        adaptive: adaptive.metadata,
        ambiguity: ambiguity.metadata,
        lineage: lineageFor(candidateGroupId),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        ambiguity_is_error: false,
        overlapping_candidates_confirmed_truth: false,
        unresolved_structure_invalid: false,
        density_affects_activity_not_truth: true,
        final_truth_claimed: false,
      });
    }

    function invalidateAmbiguity(candidateGroupId, reason) {
      const removed = [];
      Array.from(overlays.entries()).forEach(([key, record]) => {
        if (record.ambiguity.ambiguity_continuity_group_id === String(candidateGroupId)) {
          removeRecord(key);
          removed.push(record.namespace);
        }
      });
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        invalidated: removed.length > 0,
        reason: String(reason || "ambiguity_invalidated"),
        ambiguity_continuity_group_id: String(candidateGroupId || ""),
        removed: Object.freeze(removed),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        ambiguity_is_error: false,
        overlapping_candidates_confirmed_truth: false,
        unresolved_structure_invalid: false,
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
        ambiguity_is_error: false,
        overlapping_candidates_confirmed_truth: false,
        unresolved_structure_invalid: false,
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
        ambiguity_is_error: false,
        overlapping_candidates_confirmed_truth: false,
        unresolved_structure_invalid: false,
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
        ambiguity_is_error: false,
        overlapping_candidates_confirmed_truth: false,
        unresolved_structure_invalid: false,
      });
    }

    return Object.freeze({
      hydrateAmbiguity,
      invalidateAmbiguity,
      setViewportScope,
      removeAll,
      inspect,
    });
  }

  global.RelocationSamplingCacheAmbiguityCandidateGroupSandbox = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    SANDBOX_MODE,
    OVERLAY_CLASS,
    createAmbiguityCandidateGroupSandbox,
  });
})(window);
