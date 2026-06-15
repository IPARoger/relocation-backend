/*
  Phase 2.19 dev-only adaptive refinement density sandbox.

  This sandbox prioritizes progressive refinement density from sanitized
  runtime load metadata. It does not own production rendering, mutate
  production overlay registries, persist state, start workers, fetch, or expose
  raw backend payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const SANDBOX_MODE = "dev_adaptive_density_sandbox_only";
  const OVERLAY_CLASS = "phase2-19-adaptive-density-sandbox-overlay";
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
    const density = String(output.refinement_density || "medium");
    const pressure = clamp01(output.refinement_load);
    const boundary = clamp01(output.boundary_priority);
    const stability = clamp01(output.interior_stability);
    const budget = Math.max(0, Math.floor(numberOrZero(output.refinement_budget || 1)));
    const generation = Math.max(1, Math.floor(numberOrZero(output.adaptive_generation || 1)));
    const score = boundary * 0.5 + pressure * 0.35 + (1 - stability) * 0.15;
    return Object.freeze({
      accepted: true,
      metadata: Object.freeze({
        refinement_density: density,
        refinement_load: pressure,
        boundary_priority: boundary,
        interior_stability: stability,
        refinement_budget: budget,
        adaptive_generation: generation,
        refinement_order_score: Number(score.toFixed(6)),
        density_affects_activity_not_truth: true,
      }),
    });
  }

  function sanitizeHydrationEnvelope(envelope) {
    assertObject(envelope, "adaptive density sandbox envelope");
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
        discovery_state: String(envelope.observer?.discovery_state || "runtime_structure_available"),
        display_state: String(envelope.observer?.display_state || "active"),
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

  function createAdaptiveDensitySandbox(options) {
    const documentRef = options?.document || global.document;
    const root = options?.root || documentRef?.createElement("div");
    if (!documentRef || !root) throw new TypeError("document and root are required");
    const initialScope = sanitizeViewportScope(options?.viewport_scope || options?.viewportScope || { id: "initial" });
    if (!initialScope.accepted) throw new TypeError(initialScope.reason);
    let activeViewport = initialScope.scope;
    let sequence = 0;
    const overlays = new Map();
    const pending = [];

    function overlayKey(namespace, viewportId) {
      return `${String(viewportId)}::${String(namespace)}`;
    }

    function renderOverlay(record) {
      const node = documentRef.createElement("div");
      node.className = OVERLAY_CLASS;
      node.setAttribute("data-phase", "2.19");
      node.setAttribute("data-dev-only", "true");
      node.setAttribute("data-renderer-substrate", RENDERER_SUBSTRATE);
      node.setAttribute("data-overlay-namespace", record.namespace);
      node.setAttribute("data-cache-key", record.cache_key);
      node.setAttribute("data-viewport-id", record.viewport.id);
      node.setAttribute("data-refinement-density", record.adaptive.refinement_density);
      node.setAttribute("data-adaptive-generation", String(record.adaptive.adaptive_generation));
      node.setAttribute("data-priority-score", String(record.adaptive.refinement_order_score));
      node.setAttribute("role", "presentation");
      node.textContent = `Phase 2.19 ${record.namespace}: ${record.adaptive.refinement_density}`;
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
          refinement_density: record.adaptive.refinement_density,
          refinement_load: record.adaptive.refinement_load,
          boundary_priority: record.adaptive.boundary_priority,
          interior_stability: record.adaptive.interior_stability,
          refinement_budget: record.adaptive.refinement_budget,
          adaptive_generation: record.adaptive.adaptive_generation,
          refinement_order_score: record.adaptive.refinement_order_score,
          final_truth_claimed: false,
          density_affects_activity_not_truth: true,
        })));
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
        final_truth_claimed: false,
        density_affects_activity_not_truth: true,
      });
    }

    function createCandidate(envelope, optionsForOverlay) {
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
      const namespace = overlayNamespace(optionsForOverlay, sanitized);
      return Object.freeze({
        accepted: true,
        namespace,
        cache_key: sanitized.cache_key,
        hydration: sanitized.metadata,
        observer: sanitized.observer,
        viewport: requestedScope.scope,
        adaptive: adaptive.metadata,
      });
    }

    function applyCandidate(candidate) {
      const key = overlayKey(candidate.namespace, candidate.viewport.id);
      const prior = overlays.get(key);
      if (prior && candidate.adaptive.adaptive_generation < prior.adaptive.adaptive_generation) {
        return reject("older_adaptive_generation");
      }
      if (prior) removeRecord(key);
      const order = prior ? prior.order + 1 : ++sequence;
      const overlayId = `${key}::adaptive-${candidate.adaptive.adaptive_generation}`;
      const record = {
        overlay_id: overlayId,
        namespace: candidate.namespace,
        cache_key: candidate.cache_key,
        hydration: candidate.hydration,
        observer: candidate.observer,
        viewport: candidate.viewport,
        adaptive: candidate.adaptive,
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
        action: prior ? "adaptively_refined" : "created",
        visible: true,
        overlay_kind: "isolated_dev_adaptive_density_overlay",
        overlay_id: overlayId,
        superseded_overlay_id: prior?.overlay_id || null,
        namespace: candidate.namespace,
        cache_key: candidate.cache_key,
        viewport_id: candidate.viewport.id,
        adaptive: candidate.adaptive,
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        final_truth_claimed: false,
        sparse_interiors_truth_complete: candidate.adaptive.interior_stability >= 0.8,
        density_affects_activity_not_truth: true,
      });
    }

    function hydrateAdaptive(envelope, optionsForOverlay) {
      const candidate = createCandidate(envelope, optionsForOverlay || {});
      if (!candidate.accepted) return candidate;
      return applyCandidate(candidate);
    }

    function planAdaptiveBatch(items, optionsForBatch) {
      const budget = Math.max(0, Math.floor(numberOrZero(optionsForBatch?.refinement_budget ?? items?.length ?? 0)));
      const candidates = (Array.isArray(items) ? items : []).map(item => {
        const candidate = createCandidate(item.envelope, item.options || {});
        return candidate.accepted ? candidate : Object.freeze({ ...candidate, rejected_candidate: true });
      });
      const acceptedCandidates = candidates
        .filter(candidate => candidate.accepted)
        .sort((a, b) => (
          b.adaptive.refinement_order_score - a.adaptive.refinement_order_score ||
          b.adaptive.boundary_priority - a.adaptive.boundary_priority ||
          b.adaptive.adaptive_generation - a.adaptive.adaptive_generation ||
          a.namespace.localeCompare(b.namespace)
        ));
      const selected = acceptedCandidates.slice(0, budget);
      const deferred = acceptedCandidates.slice(budget);
      pending.splice(0, pending.length, ...deferred);
      const applied = selected.map(applyCandidate);
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        accepted: true,
        budget,
        applied: Object.freeze(applied),
        deferred: Object.freeze(deferred.map(candidate => Object.freeze({
          namespace: candidate.namespace,
          cache_key: candidate.cache_key,
          refinement_order_score: candidate.adaptive.refinement_order_score,
          boundary_priority: candidate.adaptive.boundary_priority,
          interior_stability: candidate.adaptive.interior_stability,
          stable_sparse_interior: candidate.adaptive.interior_stability >= 0.8,
        }))),
        rejected_count: candidates.filter(candidate => candidate.rejected_candidate).length,
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        final_truth_claimed: false,
        density_affects_activity_not_truth: true,
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
        final_truth_claimed: false,
        density_affects_activity_not_truth: true,
      });
    }

    function removeAll() {
      Array.from(overlays.keys()).forEach(removeRecord);
      pending.splice(0, pending.length);
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
        final_truth_claimed: false,
        density_affects_activity_not_truth: true,
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
        pending_count: pending.length,
        dom_overlay_count: root.querySelectorAll(`.${OVERLAY_CLASS}`).length,
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        final_truth_claimed: false,
        density_affects_activity_not_truth: true,
      });
    }

    return Object.freeze({
      hydrateAdaptive,
      planAdaptiveBatch,
      setViewportScope,
      removeAll,
      inspect,
    });
  }

  global.RelocationSamplingCacheAdaptiveDensitySandbox = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    SANDBOX_MODE,
    OVERLAY_CLASS,
    createAdaptiveDensitySandbox,
  });
})(window);
