/*
  Phase 2.18 dev-only progressive refinement hydration sandbox.

  This sandbox progresses coarse hydration overlays into refined overlays while
  tracking sanitized lineage. It does not own production rendering, mutate
  production overlay registries, persist state, start workers, fetch, or expose
  raw backend payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const SANDBOX_MODE = "dev_progressive_refinement_sandbox_only";
  const OVERLAY_CLASS = "phase2-18-progressive-refinement-sandbox-overlay";
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
  const REFINEMENT_FIELDS = Object.freeze([
    "refinement_level",
    "parent_overlay_id",
    "refinement_generation",
    "refinement_scope",
    "refinement_status",
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

  function sanitizeRefinementMetadata(metadata) {
    const source = metadata || {};
    if (includesForbiddenField(source)) {
      return Object.freeze({ accepted: false, reason: "raw_or_forbidden_refinement_field" });
    }
    const output = copyFields(source, REFINEMENT_FIELDS);
    return Object.freeze({
      accepted: true,
      metadata: Object.freeze({
        refinement_level: String(output.refinement_level || "coarse"),
        parent_overlay_id: output.parent_overlay_id ? String(output.parent_overlay_id) : null,
        refinement_generation: Number(output.refinement_generation || 1),
        refinement_scope: output.refinement_scope || "current_viewport",
        refinement_status: String(output.refinement_status || "provisional"),
      }),
    });
  }

  function sanitizeHydrationEnvelope(envelope) {
    assertObject(envelope, "progressive refinement sandbox envelope");
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
        discovery_state: String(envelope.observer?.discovery_state || "confirmed_discovered_structure"),
        color_state: String(envelope.observer?.color_state || "colored"),
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

  function createProgressiveRefinementSandbox(options) {
    const documentRef = options?.document || global.document;
    const root = options?.root || documentRef?.createElement("div");
    if (!documentRef || !root) throw new TypeError("document and root are required");
    const initialScope = sanitizeViewportScope(options?.viewport_scope || options?.viewportScope || { id: "initial" });
    if (!initialScope.accepted) throw new TypeError(initialScope.reason);
    const overlays = new Map();
    const lineage = new Map();
    let activeViewport = initialScope.scope;
    let sequence = 0;

    function overlayKey(namespace, viewportId) {
      return `${String(viewportId)}::${String(namespace)}`;
    }

    function renderOverlay(record) {
      const node = documentRef.createElement("div");
      node.className = OVERLAY_CLASS;
      node.setAttribute("data-phase", "2.18");
      node.setAttribute("data-dev-only", "true");
      node.setAttribute("data-renderer-substrate", RENDERER_SUBSTRATE);
      node.setAttribute("data-overlay-namespace", record.namespace);
      node.setAttribute("data-cache-key", record.cache_key);
      node.setAttribute("data-viewport-id", record.viewport.id);
      node.setAttribute("data-refinement-level", record.refinement.refinement_level);
      node.setAttribute("data-refinement-generation", String(record.refinement.refinement_generation));
      node.setAttribute("data-order", String(record.order));
      node.setAttribute("role", "presentation");
      node.textContent = `Phase 2.18 ${record.namespace}@${record.viewport.id} ${record.refinement.refinement_level}`;
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
          refinement_level: record.refinement.refinement_level,
          refinement_generation: record.refinement.refinement_generation,
          parent_overlay_id: record.refinement.parent_overlay_id,
          refinement_status: record.refinement.refinement_status,
          truth_final: record.truth_final,
        })));
    }

    function lineageFor(key) {
      return Object.freeze((lineage.get(key) || []).map(item => Object.freeze({ ...item })));
    }

    function hydrateRefinement(envelope, optionsForOverlay) {
      const sanitized = sanitizeHydrationEnvelope(envelope);
      if (!sanitized.accepted) {
        return Object.freeze({
          schema_version: VERSION,
          mode: SANDBOX_MODE,
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: false,
          reason: sanitized.reason,
          visible: false,
          overlay_count: overlays.size,
          viewport_id: activeViewport.id,
          renderer_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
          truth_final: false,
        });
      }
      const requestedScope = sanitizeViewportScope(
        optionsForOverlay?.viewport_scope ||
        optionsForOverlay?.viewportScope ||
        activeViewport
      );
      if (!requestedScope.accepted) {
        return Object.freeze({
          schema_version: VERSION,
          mode: SANDBOX_MODE,
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: false,
          reason: requestedScope.reason,
          visible: false,
          overlay_count: overlays.size,
          viewport_id: activeViewport.id,
          renderer_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
          truth_final: false,
        });
      }
      if (requestedScope.id !== activeViewport.id) {
        return Object.freeze({
          schema_version: VERSION,
          mode: SANDBOX_MODE,
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: false,
          reason: "viewport_scope_mismatch",
          visible: false,
          overlay_count: overlays.size,
          viewport_id: activeViewport.id,
          requested_viewport_id: requestedScope.id,
          renderer_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
          truth_final: false,
        });
      }
      const refinement = sanitizeRefinementMetadata(
        optionsForOverlay?.refinement ||
        optionsForOverlay?.refinement_metadata ||
        optionsForOverlay?.refinementMetadata ||
        {}
      );
      if (!refinement.accepted) {
        return Object.freeze({
          schema_version: VERSION,
          mode: SANDBOX_MODE,
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: false,
          reason: refinement.reason,
          visible: false,
          overlay_count: overlays.size,
          viewport_id: activeViewport.id,
          renderer_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
          truth_final: false,
        });
      }
      const namespace = overlayNamespace(optionsForOverlay, sanitized);
      const key = overlayKey(namespace, requestedScope.id);
      const prior = overlays.get(key);
      if (prior && Number(refinement.metadata.refinement_generation) < Number(prior.refinement.refinement_generation)) {
        return Object.freeze({
          schema_version: VERSION,
          mode: SANDBOX_MODE,
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: false,
          reason: "older_refinement_generation",
          visible: false,
          overlay_count: overlays.size,
          viewport_id: activeViewport.id,
          namespace,
          renderer_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
          truth_final: false,
        });
      }
      const order = prior ? prior.order + 1 : ++sequence;
      const previousOverlayId = prior?.overlay_id || null;
      const overlayId = `${key}::gen-${refinement.metadata.refinement_generation}`;
      if (prior) removeRecord(key);
      const existingLineage = lineage.get(key) || [];
      const lineageEntry = Object.freeze({
        overlay_id: overlayId,
        parent_overlay_id: refinement.metadata.parent_overlay_id || previousOverlayId,
        cache_key: sanitized.cache_key,
        refinement_level: refinement.metadata.refinement_level,
        refinement_generation: refinement.metadata.refinement_generation,
        refinement_status: refinement.metadata.refinement_status,
        superseded_overlay_id: previousOverlayId,
      });
      lineage.set(key, Object.freeze([...existingLineage, lineageEntry]));
      const record = {
        overlay_id: overlayId,
        namespace,
        cache_key: sanitized.cache_key,
        metadata: sanitized.metadata,
        observer: sanitized.observer,
        refinement: refinement.metadata,
        order,
        viewport: requestedScope.scope,
        truth_final: false,
      };
      record.node = renderOverlay(record);
      overlays.set(key, record);
      root.appendChild(record.node);
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        accepted: true,
        action: previousOverlayId ? "refined" : "created",
        visible: true,
        overlay_kind: "isolated_dev_progressive_refinement_overlay",
        overlay_id: overlayId,
        superseded_overlay_id: previousOverlayId,
        namespace,
        cache_key: sanitized.cache_key,
        viewport_id: requestedScope.id,
        refinement: refinement.metadata,
        lineage: lineageFor(key),
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        truth_final: false,
      });
    }

    function invalidateRefinement(namespace, reason) {
      const key = overlayKey(namespace, activeViewport.id);
      const removed = removeRecord(key);
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        invalidated: removed,
        reason: String(reason || "stale_refinement"),
        namespace: String(namespace || ""),
        viewport_id: activeViewport.id,
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
        truth_final: false,
      });
    }

    function setViewportScope(scope) {
      const next = sanitizeViewportScope(scope);
      if (!next.accepted) {
        return Object.freeze({
          schema_version: VERSION,
          mode: SANDBOX_MODE,
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: false,
          reason: next.reason,
          viewport_id: activeViewport.id,
          overlay_count: overlays.size,
          renderer_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
          truth_final: false,
        });
      }
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
        truth_final: false,
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
        truth_final: false,
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
        truth_final: false,
      });
    }

    return Object.freeze({
      hydrateRefinement,
      invalidateRefinement,
      setViewportScope,
      removeAll,
      inspect,
    });
  }

  global.RelocationSamplingCacheProgressiveRefinementSandbox = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    SANDBOX_MODE,
    OVERLAY_CLASS,
    createProgressiveRefinementSandbox,
  });
})(window);
