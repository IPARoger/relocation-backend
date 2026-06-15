/*
  Phase 2.15 dev-only renderer hydration sandbox.

  This sandbox proves sanitized runtime metadata can create one isolated visual
  overlay representation. It does not own production rendering, mutate map
  overlays, persist state, start workers, fetch, or expose raw backend payloads.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const SANDBOX_MODE = "dev_renderer_hydration_sandbox_only";
  const OVERLAY_CLASS = "phase2-15-renderer-hydration-sandbox-overlay";
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

  function sanitizeHydrationEnvelope(envelope) {
    assertObject(envelope, "hydration sandbox envelope");
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

  function createRendererHydrationSandbox(options) {
    const documentRef = options?.document || global.document;
    const root = options?.root || documentRef?.createElement("div");
    if (!documentRef || !root) throw new TypeError("document and root are required");
    let overlay = null;
    let lastHydration = null;

    function removeOverlay() {
      if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
      overlay = null;
      lastHydration = null;
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        removed: true,
        visible: false,
        overlay_count: root.querySelectorAll(`.${OVERLAY_CLASS}`).length,
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
      });
    }

    function hydrateOnce(envelope) {
      removeOverlay();
      const sanitized = sanitizeHydrationEnvelope(envelope);
      if (!sanitized.accepted) {
        return Object.freeze({
          schema_version: VERSION,
          mode: SANDBOX_MODE,
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: false,
          reason: sanitized.reason,
          visible: false,
          renderer_ownership_claimed: false,
          production_registry_mutated: false,
          persisted: false,
        });
      }
      const node = documentRef.createElement("div");
      node.className = OVERLAY_CLASS;
      node.setAttribute("data-phase", "2.15");
      node.setAttribute("data-dev-only", "true");
      node.setAttribute("data-renderer-substrate", RENDERER_SUBSTRATE);
      node.setAttribute("data-cache-key", sanitized.cache_key);
      node.setAttribute("role", "presentation");
      node.textContent = `Phase 2.15 hydrated metadata: ${sanitized.metadata.summary?.feature_count ?? 0}`;
      root.appendChild(node);
      overlay = node;
      lastHydration = sanitized;
      return Object.freeze({
        schema_version: VERSION,
        mode: SANDBOX_MODE,
        rendererSubstrate: RENDERER_SUBSTRATE,
        accepted: true,
        visible: true,
        overlay_kind: "isolated_dev_dom_overlay",
        overlay_count: root.querySelectorAll(`.${OVERLAY_CLASS}`).length,
        cache_key: sanitized.cache_key,
        metadata: sanitized.metadata,
        observer: sanitized.observer,
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
        visible: Boolean(overlay && overlay.parentNode),
        overlay_count: root.querySelectorAll(`.${OVERLAY_CLASS}`).length,
        cache_key: lastHydration?.cache_key || null,
        renderer_ownership_claimed: false,
        production_registry_mutated: false,
        persisted: false,
      });
    }

    return Object.freeze({
      hydrateOnce,
      removeOverlay,
      inspect,
    });
  }

  global.RelocationSamplingCacheRendererHydrationSandbox = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    SANDBOX_MODE,
    OVERLAY_CLASS,
    createRendererHydrationSandbox,
  });
})(window);
