/*
  Phase 2.17 dev-only viewport-scoped hydration sandbox.

  This sandbox binds isolated hydration overlays to sanitized viewport metadata.
  It does not own production rendering or viewport state, mutate production
  overlay registries, persist state, start workers, fetch, or expose raw payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const SANDBOX_MODE = "dev_viewport_hydration_sandbox_only";
  const OVERLAY_CLASS = "phase2-17-viewport-hydration-sandbox-overlay";
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

  function copyHydrationMetadata(source) {
    const output = {};
    HYDRATION_FIELDS.forEach(field => {
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

  function sanitizeHydrationEnvelope(envelope) {
    assertObject(envelope, "viewport hydration sandbox envelope");
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
      metadata: copyHydrationMetadata(metadata),
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

  function createViewportHydrationSandbox(options) {
    const documentRef = options?.document || global.document;
    const root = options?.root || documentRef?.createElement("div");
    if (!documentRef || !root) throw new TypeError("document and root are required");
    const initialScope = sanitizeViewportScope(options?.viewport_scope || options?.viewportScope || { id: "initial" });
    if (!initialScope.accepted) throw new TypeError(initialScope.reason);
    const overlays = new Map();
    let activeViewport = initialScope.scope;
    let sequence = 0;

    function renderOverlay(record) {
      const node = record.node || documentRef.createElement("div");
      node.className = OVERLAY_CLASS;
      node.setAttribute("data-phase", "2.17");
      node.setAttribute("data-dev-only", "true");
      node.setAttribute("data-renderer-substrate", RENDERER_SUBSTRATE);
      node.setAttribute("data-overlay-namespace", record.namespace);
      node.setAttribute("data-cache-key", record.cache_key);
      node.setAttribute("data-viewport-id", record.viewport.id);
      node.setAttribute("data-order", String(record.order));
      node.setAttribute("role", "presentation");
      node.textContent = `Phase 2.17 ${record.namespace}@${record.viewport.id}: ${record.metadata.summary?.feature_count ?? 0}`;
      return node;
    }

    function reorderDom() {
      Array.from(overlays.values())
        .sort((a, b) => a.viewport_order - b.viewport_order || a.order - b.order || a.namespace.localeCompare(b.namespace))
        .forEach(record => {
          root.appendChild(record.node);
        });
    }

    function snapshotRecords() {
      return Object.freeze(Array.from(overlays.values())
        .sort((a, b) => a.viewport_order - b.viewport_order || a.order - b.order || a.namespace.localeCompare(b.namespace))
        .map(record => Object.freeze({
          namespace: record.namespace,
          cache_key: record.cache_key,
          order: record.order,
          viewport_order: record.viewport_order,
          viewport_id: record.viewport.id,
          status: record.metadata.status,
          feature_count: Number(record.metadata.summary?.feature_count || 0),
        })));
    }

    function removeRecord(namespace) {
      const record = overlays.get(namespace);
      if (!record) return false;
      if (record.node.parentNode) record.node.parentNode.removeChild(record.node);
      overlays.delete(namespace);
      return true;
    }

    function hydrateOverlay(envelope, optionsForOverlay) {
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
          viewport_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
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
          viewport_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
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
          viewport_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
        });
      }
      const namespace = overlayNamespace(optionsForOverlay, sanitized);
      const prior = overlays.get(namespace);
      const order = prior ? prior.order : ++sequence;
      const record = {
        namespace,
        cache_key: sanitized.cache_key,
        metadata: sanitized.metadata,
        observer: sanitized.observer,
        order,
        viewport_order: sequence,
        viewport: requestedScope.scope,
        node: prior?.node || null,
      };
      record.node = renderOverlay(record);
      overlays.set(namespace, record);
      reorderDom();
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        accepted: true,
        action: prior ? "updated" : "created",
        visible: true,
        overlay_kind: "isolated_dev_viewport_overlay_group",
        namespace,
        cache_key: sanitized.cache_key,
        viewport_id: requestedScope.id,
        order,
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        viewport_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
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
          viewport_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
        });
      }
      activeViewport = next.scope;
      const invalidated = [];
      Array.from(overlays.values()).forEach(record => {
        if (record.viewport.id !== activeViewport.id) {
          removeRecord(record.namespace);
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
        viewport_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
      });
    }

    function replaceOverlay(namespace, envelope, optionsForOverlay) {
      removeRecord(String(namespace || ""));
      return hydrateOverlay(envelope, { ...(optionsForOverlay || {}), namespace });
    }

    function invalidateOutOfScope() {
      return setViewportScope(activeViewport);
    }

    function removeOverlay(namespace) {
      const key = String(namespace || "");
      const removed = removeRecord(key);
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        removed,
        namespace: key,
        viewport_id: activeViewport.id,
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        viewport_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
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
        viewport_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
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
        viewport_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
      });
    }

    return Object.freeze({
      hydrateOverlay,
      setViewportScope,
      replaceOverlay,
      invalidateOutOfScope,
      removeOverlay,
      removeAll,
      inspect,
    });
  }

  global.RelocationSamplingCacheViewportHydrationSandbox = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    SANDBOX_MODE,
    OVERLAY_CLASS,
    createViewportHydrationSandbox,
  });
})(window);
