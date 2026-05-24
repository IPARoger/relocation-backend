/*
  Phase 2.21 dev-only implication-field sandbox.

  This sandbox represents nearby unresolved implication fields from sanitized
  ambiguity/adaptive metadata. It does not own production rendering, mutate
  production overlay registries, persist state, start workers, fetch, or expose
  raw backend payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const SANDBOX_MODE = "dev_implication_field_sandbox_only";
  const OVERLAY_CLASS = "phase2-21-implication-field-sandbox-overlay";
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
    "refinement_pressure",
    "boundary_priority",
    "interior_stability",
    "refinement_budget",
    "adaptive_generation",
  ]);
  const AMBIGUITY_FIELDS = Object.freeze([
    "ambiguity_domain_id",
    "ambiguity_confidence",
    "ambiguity_overlap",
    "candidate_refinement_ids",
    "uncertainty_generation",
    "ambiguity_status",
  ]);
  const IMPLICATION_FIELDS = Object.freeze([
    "implication_field_id",
    "implication_direction",
    "implication_strength",
    "implication_source_domain",
    "implication_generation",
    "implication_status",
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
        refinement_pressure: clamp01(output.refinement_pressure),
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
        ambiguity_domain_id: String(output.ambiguity_domain_id || "ambiguity-domain"),
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

  function sanitizeImplicationMetadata(metadata) {
    const source = metadata || {};
    if (includesForbiddenField(source)) {
      return Object.freeze({ accepted: false, reason: "raw_or_forbidden_implication_field" });
    }
    const output = copyFields(source, IMPLICATION_FIELDS);
    return Object.freeze({
      accepted: true,
      metadata: Object.freeze({
        implication_field_id: String(output.implication_field_id || "implication-field"),
        implication_direction: String(output.implication_direction || "nearby"),
        implication_strength: clamp01(output.implication_strength),
        implication_source_domain: String(output.implication_source_domain || ""),
        implication_generation: Math.max(1, Math.floor(numberOrZero(output.implication_generation || 1))),
        implication_status: String(output.implication_status || "unresolved"),
        implication_is_confirmed_truth: false,
        directional_attraction_guarantees_outcome: false,
        speculative_astrology_meaning_synthesized: false,
      }),
    });
  }

  function sanitizeHydrationEnvelope(envelope) {
    assertObject(envelope, "implication field sandbox envelope");
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
        discovery_state: String(envelope.observer?.discovery_state || "implied_nearby_structure"),
        color_state: String(envelope.observer?.color_state || "transitioning"),
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

  function createImplicationFieldSandbox(options) {
    const documentRef = options?.document || global.document;
    const root = options?.root || documentRef?.createElement("div");
    if (!documentRef || !root) throw new TypeError("document and root are required");
    const initialScope = sanitizeViewportScope(options?.viewport_scope || options?.viewportScope || { id: "initial" });
    if (!initialScope.accepted) throw new TypeError(initialScope.reason);
    const overlays = new Map();
    const implicationLineage = new Map();
    let activeViewport = initialScope.scope;
    let sequence = 0;

    function overlayKey(namespace, viewportId, implicationId) {
      return `${String(viewportId)}::${String(namespace)}::${String(implicationId)}`;
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
        implication_is_confirmed_truth: false,
        directional_attraction_guarantees_outcome: false,
        speculative_astrology_meaning_synthesized: false,
      });
    }

    function renderOverlay(record) {
      const node = documentRef.createElement("div");
      node.className = OVERLAY_CLASS;
      node.setAttribute("data-phase", "2.21");
      node.setAttribute("data-dev-only", "true");
      node.setAttribute("data-renderer-substrate", RENDERER_SUBSTRATE);
      node.setAttribute("data-overlay-namespace", record.namespace);
      node.setAttribute("data-implication-field-id", record.implication.implication_field_id);
      node.setAttribute("data-implication-direction", record.implication.implication_direction);
      node.setAttribute("data-implication-status", record.implication.implication_status);
      node.setAttribute("data-implication-generation", String(record.implication.implication_generation));
      node.setAttribute("data-cache-key", record.cache_key);
      node.setAttribute("data-viewport-id", record.viewport.id);
      node.setAttribute("role", "presentation");
      node.textContent = `Phase 2.21 ${record.namespace}: ${record.implication.implication_direction}`;
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
          ambiguity_domain_id: record.ambiguity.ambiguity_domain_id,
          implication_field_id: record.implication.implication_field_id,
          implication_direction: record.implication.implication_direction,
          implication_strength: record.implication.implication_strength,
          implication_source_domain: record.implication.implication_source_domain,
          implication_generation: record.implication.implication_generation,
          implication_status: record.implication.implication_status,
          implication_is_confirmed_truth: false,
          directional_attraction_guarantees_outcome: false,
          speculative_astrology_meaning_synthesized: false,
          density_affects_activity_not_truth: true,
          truth_final: false,
        })));
    }

    function lineageFor(implicationId) {
      return Object.freeze((implicationLineage.get(implicationId) || []).map(item => Object.freeze({ ...item })));
    }

    function hydrateImplication(envelope, optionsForOverlay) {
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
      const implication = sanitizeImplicationMetadata(
        optionsForOverlay?.implication ||
        optionsForOverlay?.implication_metadata ||
        optionsForOverlay?.implicationMetadata ||
        {}
      );
      if (!implication.accepted) return reject(implication.reason);
      const namespace = overlayNamespace(optionsForOverlay, sanitized);
      const implicationId = implication.metadata.implication_field_id;
      const key = overlayKey(namespace, requestedScope.id, implicationId);
      const prior = overlays.get(key);
      if (prior && implication.metadata.implication_generation < prior.implication.implication_generation) {
        return reject("older_implication_generation");
      }
      if (prior) removeRecord(key);
      const order = prior ? prior.order + 1 : ++sequence;
      const overlayId = `${key}::implication-${implication.metadata.implication_generation}`;
      const lineageEntry = Object.freeze({
        overlay_id: overlayId,
        superseded_overlay_id: prior?.overlay_id || null,
        cache_key: sanitized.cache_key,
        implication_generation: implication.metadata.implication_generation,
        implication_status: implication.metadata.implication_status,
        implication_source_domain: implication.metadata.implication_source_domain,
        implication_direction: implication.metadata.implication_direction,
      });
      implicationLineage.set(implicationId, Object.freeze([...(implicationLineage.get(implicationId) || []), lineageEntry]));
      const record = {
        overlay_id: overlayId,
        namespace,
        cache_key: sanitized.cache_key,
        hydration: sanitized.metadata,
        observer: sanitized.observer,
        adaptive: adaptive.metadata,
        ambiguity: ambiguity.metadata,
        implication: implication.metadata,
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
        action: prior ? "implication_superseded" : "created",
        visible: true,
        overlay_kind: "isolated_dev_implication_field_overlay",
        overlay_id: overlayId,
        superseded_overlay_id: prior?.overlay_id || null,
        namespace,
        cache_key: sanitized.cache_key,
        viewport_id: requestedScope.id,
        adaptive: adaptive.metadata,
        ambiguity: ambiguity.metadata,
        implication: implication.metadata,
        lineage: lineageFor(implicationId),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        implication_is_confirmed_truth: false,
        directional_attraction_guarantees_outcome: false,
        speculative_astrology_meaning_synthesized: false,
        density_affects_activity_not_truth: true,
        truth_final: false,
      });
    }

    function invalidateImplication(implicationId, reason) {
      const removed = [];
      Array.from(overlays.entries()).forEach(([key, record]) => {
        if (record.implication.implication_field_id === String(implicationId)) {
          removeRecord(key);
          removed.push(record.namespace);
        }
      });
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        invalidated: removed.length > 0,
        reason: String(reason || "implication_invalidated"),
        implication_field_id: String(implicationId || ""),
        removed: Object.freeze(removed),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        implication_is_confirmed_truth: false,
        directional_attraction_guarantees_outcome: false,
        speculative_astrology_meaning_synthesized: false,
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
        implication_is_confirmed_truth: false,
        directional_attraction_guarantees_outcome: false,
        speculative_astrology_meaning_synthesized: false,
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
        implication_is_confirmed_truth: false,
        directional_attraction_guarantees_outcome: false,
        speculative_astrology_meaning_synthesized: false,
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
        implication_is_confirmed_truth: false,
        directional_attraction_guarantees_outcome: false,
        speculative_astrology_meaning_synthesized: false,
      });
    }

    return Object.freeze({
      hydrateImplication,
      invalidateImplication,
      setViewportScope,
      removeAll,
      inspect,
    });
  }

  global.RelocationSamplingCacheImplicationFieldSandbox = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    SANDBOX_MODE,
    OVERLAY_CLASS,
    createImplicationFieldSandbox,
  });
})(window);
