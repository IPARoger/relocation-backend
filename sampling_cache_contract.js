/*
  Phase 2.4 sampling/cache contract scaffold.

  This file defines only semantic cache-key helpers. It does not fetch,
  render, schedule, persist, or wire itself into runtime map behavior.
*/
(function(global) {
  "use strict";

  const SCHEMA_VERSION = 1;

  function assertObject(value, label) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new TypeError(`${label} must be an object`);
    }
  }

  function assertFiniteNumber(value, label) {
    if (!Number.isFinite(Number(value))) {
      throw new TypeError(`${label} must be finite`);
    }
  }

  function normalizeText(value) {
    return String(value || "").trim().toLowerCase();
  }

  function normalizeAngleLabel(value) {
    const angle = String(value || "").trim().toUpperCase();
    if (["DESC", "DES", "DSC", "DCS"].includes(angle)) return "DC";
    return angle;
  }

  function roundNumber(value, places) {
    assertFiniteNumber(value, "numeric value");
    const factor = Math.pow(10, places);
    return Math.round(Number(value) * factor) / factor;
  }

  function stableStringify(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
    return `{${Object.keys(value).sort().map(key => (
      `${JSON.stringify(key)}:${stableStringify(value[key])}`
    )).join(",")}}`;
  }

  function hashString(value) {
    let hash = 2166136261;
    for (let i = 0; i < value.length; i++) {
      hash ^= value.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function normalizePlanetInHouse(condition) {
    return Object.freeze({
      type: "planet_in_house",
      slot: condition.slot == null ? null : String(condition.slot).trim().toUpperCase(),
      planet: normalizeText(condition.planet),
      house: Number(condition.house),
    });
  }

  function normalizeAngleSign(condition) {
    return Object.freeze({
      type: "angle_in_sign",
      angle: normalizeAngleLabel(condition.angle),
      sign: normalizeText(condition.sign),
    });
  }

  function normalizeAspectOverlay(condition) {
    if (!condition) return null;
    return Object.freeze({
      type: "aspect_to_angle",
      planet: normalizeText(condition.planet),
      aspect: normalizeText(condition.aspect),
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
      schema_version: SCHEMA_VERSION,
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
      schema_version: SCHEMA_VERSION,
      chart_key: String(input.chart_key ?? input.chartKey ?? ""),
      investigation: normalizeInvestigationIntent(
        input.investigation || input.intent || input.conditions || {}
      ),
      viewport: scope.viewport,
      sampling: scope.sampling,
    });
  }

  function createSemanticCacheKey(input) {
    const payload = createCacheKeyPayload(input);
    const stableJson = stableStringify(payload);
    return Object.freeze({
      key: `rm:v${SCHEMA_VERSION}:${hashString(stableJson)}`,
      payload,
      stable_json: stableJson,
    });
  }

  global.RelocationSamplingCacheContract = Object.freeze({
    normalizeInvestigationIntent,
    createSamplingScope,
    createCacheKeyPayload,
    createSemanticCacheKey,
  });
})(window);
