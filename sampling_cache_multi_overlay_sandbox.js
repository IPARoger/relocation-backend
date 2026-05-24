/*
  Phase 2.16 dev-only multi-overlay coexistence sandbox.

  This sandbox manages multiple isolated hydration overlay representations.
  It does not own production rendering, mutate production overlay registries,
  persist state, start workers, fetch, or expose raw backend payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const SANDBOX_MODE = "dev_multi_overlay_coexistence_sandbox_only";
  const OVERLAY_CLASS = "phase2-16-multi-overlay-sandbox-overlay";
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

  function overlayNamespace(options, sanitized) {
    return String(
      options?.namespace ||
      options?.overlay_namespace ||
      options?.overlayNamespace ||
      sanitized.cache_key ||
      "dev-overlay"
    );
  }

  function sanitizeHydrationEnvelope(envelope) {
    assertObject(envelope, "multi-overlay sandbox envelope");
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

  function createMultiOverlaySandbox(options) {
    const documentRef = options?.document || global.document;
    const root = options?.root || documentRef?.createElement("div");
    if (!documentRef || !root) throw new TypeError("document and root are required");
    const overlays = new Map();
    let sequence = 0;

    function renderOverlay(record) {
      const existing = record.node;
      const node = existing || documentRef.createElement("div");
      node.className = OVERLAY_CLASS;
      node.setAttribute("data-phase", "2.16");
      node.setAttribute("data-dev-only", "true");
      node.setAttribute("data-renderer-substrate", RENDERER_SUBSTRATE);
      node.setAttribute("data-overlay-namespace", record.namespace);
      node.setAttribute("data-cache-key", record.cache_key);
      node.setAttribute("data-order", String(record.order));
      node.setAttribute("role", "presentation");
      node.textContent = `Phase 2.16 ${record.namespace}: ${record.metadata.summary?.feature_count ?? 0}`;
      return node;
    }

    function reorderDom() {
      Array.from(overlays.values())
        .sort((a, b) => a.order - b.order || a.namespace.localeCompare(b.namespace))
        .forEach(record => {
          if (record.node.parentNode !== root) root.appendChild(record.node);
          else root.appendChild(record.node);
        });
    }

    function snapshotRecords() {
      return Object.freeze(Array.from(overlays.values())
        .sort((a, b) => a.order - b.order || a.namespace.localeCompare(b.namespace))
        .map(record => Object.freeze({
          namespace: record.namespace,
          cache_key: record.cache_key,
          order: record.order,
          status: record.metadata.status,
          feature_count: Number(record.metadata.summary?.feature_count || 0),
        })));
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
          renderer_ownership_claimed: false,
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
        overlay_kind: "isolated_dev_dom_overlay_group",
        namespace,
        cache_key: sanitized.cache_key,
        order,
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
      });
    }

    function replaceOverlay(namespace, envelope) {
      const key = String(namespace || "");
      if (overlays.has(key)) removeOverlay(key);
      return hydrateOverlay(envelope, { namespace: key });
    }

    function invalidateOverlay(namespace, reason) {
      const key = String(namespace || "");
      const record = overlays.get(key);
      if (!record) {
        return Object.freeze({
          schema_version: VERSION,
          mode: SANDBOX_MODE,
          rendererSubstrate: RENDERER_SUBSTRATE,
          invalidated: false,
          reason: "overlay_not_found",
          namespace: key,
          overlay_count: overlays.size,
          renderer_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
        });
      }
      if (record.node.parentNode) record.node.parentNode.removeChild(record.node);
      overlays.delete(key);
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        invalidated: true,
        reason: String(reason || "stale"),
        namespace: key,
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
      });
    }

    function removeOverlay(namespace) {
      const key = String(namespace || "");
      const record = overlays.get(key);
      if (!record) {
        return Object.freeze({
          schema_version: VERSION,
          mode: SANDBOX_MODE,
          rendererSubstrate: RENDERER_SUBSTRATE,
          removed: false,
          namespace: key,
          overlay_count: overlays.size,
          renderer_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
        });
      }
      if (record.node.parentNode) record.node.parentNode.removeChild(record.node);
      overlays.delete(key);
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        removed: true,
        namespace: key,
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
      });
    }

    function removeAll() {
      Array.from(overlays.keys()).forEach(removeOverlay);
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        removed: true,
        overlay_count: overlays.size,
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
      });
    }

    function inspect() {
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        overlay_count: overlays.size,
        overlays: snapshotRecords(),
        dom_overlay_count: root.querySelectorAll(`.${OVERLAY_CLASS}`).length,
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
      });
    }

    return Object.freeze({
      hydrateOverlay,
      replaceOverlay,
      invalidateOverlay,
      removeOverlay,
      removeAll,
      inspect,
    });
  }

  global.RelocationSamplingCacheMultiOverlaySandbox = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    SANDBOX_MODE,
    OVERLAY_CLASS,
    createMultiOverlaySandbox,
  });
})(window);
