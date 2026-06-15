/*
  Relocation substrate adapter scaffold.

  Phase 1.3 boundary only: this file defines contracts between the
  production renderer host, future screen-space classification substrate,
  scheduler/cache layer, and future perceptual renderer. It does not fetch,
  render, cache, migrate /search-regions, or change production behavior.
*/
(function(global) {
  "use strict";

  const VERSION = 1;

  const HOST_OWNS = Object.freeze([
    "leaflet_map",
    "visible_layers",
    "sidebar_inputs",
    "popup_truth",
    "render_status",
    "debug_panels",
  ]);

  const SUBSTRATE_OWNS = Object.freeze([
    "classification_requests",
    "point_order",
    "mask_order",
    "refinement_metrics",
    "cancellation_signal",
  ]);

  const CACHE_OWNS = Object.freeze([
    "cache_key_shape",
    "foreground_background_priority",
    "abort_without_commit",
    "budget_accounting",
  ]);

  function assertObject(value, label) {
    if (!value || typeof value !== "object") {
      throw new TypeError(`${label} must be an object`);
    }
  }

  function assertFiniteNumber(value, label) {
    if (!Number.isFinite(Number(value))) {
      throw new TypeError(`${label} must be finite`);
    }
  }

  function normalizeConditionSet(conditions) {
    if (!Array.isArray(conditions)) return [];
    return conditions.map(condition => ({ ...condition }));
  }

  function normalizeAngleLabel(value) {
    const v = String(value || "").trim().toUpperCase();
    if (v === "DSC" || v === "DESC" || v === "DES" || v === "DCS") return "DC";
    return v;
  }

  function roundNumber(value, places) {
    assertFiniteNumber(value, "numeric value");
    const factor = Math.pow(10, places);
    return Math.round(Number(value) * factor) / factor;
  }

  function stableStringify(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) {
      return `[${value.map(stableStringify).join(",")}]`;
    }
    return `{${Object.keys(value).sort().map(key => (
      `${JSON.stringify(key)}:${stableStringify(value[key])}`
    )).join(",")}}`;
  }

  function normalizePlanetInHouse(condition) {
    return Object.freeze({
      type: "planet_in_house",
      slot: condition.slot == null ? null : String(condition.slot).trim().toUpperCase(),
      planet: String(condition.planet || "").trim().toLowerCase(),
      house: Number(condition.house),
    });
  }

  function normalizeAngleSign(condition) {
    return Object.freeze({
      type: "angle_in_sign",
      angle: normalizeAngleLabel(condition.angle),
      sign: String(condition.sign || "").trim().toLowerCase(),
    });
  }

  function normalizeAspectOverlay(condition) {
    if (!condition) return null;
    return Object.freeze({
      type: "aspect_to_angle",
      planet: String(condition.planet || "").trim().toLowerCase(),
      aspect: String(condition.aspect || "").trim().toLowerCase(),
      angle: normalizeAngleLabel(condition.angle),
    });
  }

  function normalizeInvestigationIntent(input) {
    const source = input || {};
    const houseConditions = (source.house_conditions || source.houseConditions || [])
      .map(normalizePlanetInHouse)
      .sort((a, b) => stableStringify(a).localeCompare(stableStringify(b)));
    const angleSignConditions = (source.angle_sign_conditions || source.angleSignConditions || [])
      .map(normalizeAngleSign)
      .sort((a, b) => stableStringify(a).localeCompare(stableStringify(b)));
    return Object.freeze({
      schema_version: 1,
      house_conditions: Object.freeze(houseConditions),
      angle_sign_conditions: Object.freeze(angleSignConditions),
      aspect_overlay: normalizeAspectOverlay(source.aspect_overlay || source.aspectOverlay),
    });
  }

  function createSamplingScope(input) {
    assertObject(input, "sampling scope");
    assertObject(input.viewport, "sampling scope viewport");
    assertObject(input.sampling, "sampling scope sampling");
    const viewport = input.viewport;
    const sampling = input.sampling;
    return Object.freeze({
      viewport: Object.freeze({
        north: roundNumber(viewport.north, 6),
        south: roundNumber(viewport.south, 6),
        east: roundNumber(viewport.east, 6),
        west: roundNumber(viewport.west, 6),
        zoom: roundNumber(viewport.zoom, 3),
      }),
      sampling: Object.freeze({
        width: Math.round(Number(sampling.width)),
        height: Math.round(Number(sampling.height)),
        block_px: Math.round(Number(sampling.block_px ?? sampling.blockPx)),
        lat_cap: Boolean(sampling.lat_cap ?? sampling.latCap),
      }),
    });
  }

  function createCacheKeyPayload(input) {
    assertObject(input, "cache key payload");
    const scope = createSamplingScope(input);
    return Object.freeze({
      schema_version: 1,
      chart_key: String(input.chart_key ?? input.chartKey ?? ""),
      investigation: normalizeInvestigationIntent(
        input.investigation || input.intent || input.conditions || {}
      ),
      viewport: scope.viewport,
      sampling: scope.sampling,
    });
  }

  function hashString(value) {
    let hash = 2166136261;
    for (let i = 0; i < value.length; i++) {
      hash ^= value.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function createSemanticCacheKey(input) {
    const payload = createCacheKeyPayload(input);
    const stable = stableStringify(payload);
    return Object.freeze({
      key: `rm:v1:${hashString(stable)}`,
      payload,
      stable_json: stable,
    });
  }

  function createViewportRequest(input) {
    assertObject(input, "viewport request");
    const { bounds, zoom, size, blockPx, applyLatCap } = input;
    assertObject(bounds, "viewport bounds");
    assertObject(size, "viewport size");
    for (const key of ["north", "south", "east", "west"]) {
      assertFiniteNumber(bounds[key], `bounds.${key}`);
    }
    assertFiniteNumber(zoom, "zoom");
    assertFiniteNumber(size.width, "size.width");
    assertFiniteNumber(size.height, "size.height");
    assertFiniteNumber(blockPx, "blockPx");
    return Object.freeze({
      bounds: Object.freeze({ ...bounds }),
      zoom: Number(zoom),
      size: Object.freeze({
        width: Number(size.width),
        height: Number(size.height),
      }),
      blockPx: Number(blockPx),
      applyLatCap: Boolean(applyLatCap),
    });
  }

  function createClassificationRequest(input) {
    assertObject(input, "classification request");
    const { birth, viewport, conditions, requestId } = input;
    assertObject(birth, "birth");
    assertObject(viewport, "viewport");
    return Object.freeze({
      requestId: requestId == null ? null : String(requestId),
      birth: Object.freeze({ ...birth }),
      viewport,
      conditions: Object.freeze(normalizeConditionSet(conditions)),
    });
  }

  function createCancellationScope(reason) {
    const controller = new AbortController();
    return Object.freeze({
      reason: reason || "unspecified",
      signal: controller.signal,
      abort() {
        controller.abort();
      },
    });
  }

  function createCacheBoundary(input) {
    assertObject(input, "cache boundary");
    const { chartKey, viewport, conditions, substrate } = input;
    assertObject(viewport, "viewport");
    return Object.freeze({
      chartKey: String(chartKey || ""),
      substrate: String(substrate || "unbound"),
      bounds: viewport.bounds,
      zoom: viewport.zoom,
      blockPx: viewport.blockPx,
      applyLatCap: viewport.applyLatCap,
      conditions: Object.freeze(normalizeConditionSet(conditions)),
    });
  }

  function createRefinementStatus(input) {
    const status = input || {};
    return Object.freeze({
      stage: status.stage || "unstarted",
      sampleCount: Number(status.sampleCount || 0),
      cellCount: Number(status.cellCount || 0),
      stopReason: status.stopReason || null,
      converged: status.converged == null ? null : Boolean(status.converged),
    });
  }

  function createRendererHostBoundary(input) {
    const host = input || {};
    return Object.freeze({
      hostId: String(host.hostId || "map_CURRENT"),
      owns: HOST_OWNS,
      substrateOwns: SUBSTRATE_OWNS,
      cacheOwns: CACHE_OWNS,
      mayRender: Boolean(host.mayRender),
    });
  }

  global.RelocationSubstrateAdapter = Object.freeze({
    VERSION,
    HOST_OWNS,
    SUBSTRATE_OWNS,
    CACHE_OWNS,
    createViewportRequest,
    createClassificationRequest,
    createCancellationScope,
    createCacheBoundary,
    normalizeInvestigationIntent,
    createSamplingScope,
    createCacheKeyPayload,
    createSemanticCacheKey,
    createRefinementStatus,
    createRendererHostBoundary,
  });
})(window);
