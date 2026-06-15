/*
  Genie render → map engine adapter (Web 2.0 slice 1).

  Consumes payload.variables[] ONLY — never legacyCompatibility or DOM slots.
*/
(function (global) {
  "use strict";

  const VERSION = 1;

  const TRANSIT_TYPES = Object.freeze([
    "transit_through_house",
    "transit_aspect_to_angle",
  ]);

  function isTransitType(type) {
    return TRANSIT_TYPES.includes(type);
  }

  /**
   * @param {unknown} payload
   * @returns {{ ok: boolean, errors: string[], payload?: object }}
   */
  function validateGenieRender(payload) {
    const errors = [];
    if (!payload || typeof payload !== "object") {
      return { ok: false, errors: ["payload must be an object"] };
    }
    if (payload.schema_version !== 1) {
      errors.push("schema_version must be 1");
    }
    if (payload.kind !== "genie_render") {
      errors.push('kind must be "genie_render"');
    }
    if (!Array.isArray(payload.variables)) {
      errors.push("variables must be an array");
    }
    return {
      ok: errors.length === 0,
      errors,
      payload: errors.length === 0 ? payload : undefined,
    };
  }

  /**
   * @param {object} payload validated genie_render
   * @param {object} birthContext { birth_year, birth_month, birth_day, birth_hour_utc }
   * @returns {object} EngineExecutionPlan
   */
  function buildEngineExecutionPlan(payload, birthContext) {
    if (!birthContext || typeof birthContext !== "object") {
      throw new TypeError("birthContext must be an object");
    }

    const house_conditions = [];
    const angle_sign_conditions = [];
    /** @type {{ planet: string, aspect: string, angle: string, variableId?: string } | null} */
    let aspectOverlay = null;
    /** @type {{ variableId: string, status: string, reason: string }[]} */
    const degradation = [];

    let aspectIncludeCount = 0;

    for (const v of payload.variables) {
      if (!v || typeof v !== "object" || !v.id) continue;

      if (v.polarity === "exclude") {
        degradation.push({
          variableId: v.id,
          status: "deferred",
          reason: "exclude_not_supported_in_engine_v1",
        });
        continue;
      }

      if (isTransitType(v.type)) {
        degradation.push({
          variableId: v.id,
          status: "deferred",
          reason: "transit_not_supported_in_engine_v1",
        });
        continue;
      }

      if (v.enabled === false || v.status !== "complete") {
        continue;
      }

      const fields = v.fields || {};

      if (v.type === "planet_in_house") {
        house_conditions.push({
          type: "planet_in_house",
          planet: fields.body,
          house: parseInt(fields.house, 10),
          variableId: v.id,
        });
        continue;
      }

      if (v.type === "angle_in_sign") {
        angle_sign_conditions.push({
          type: "angle_in_sign",
          angle: fields.angle,
          sign: fields.sign,
          variableId: v.id,
        });
        continue;
      }

      if (v.type === "aspect_to_angle") {
        if (aspectIncludeCount === 0) {
          aspectOverlay = {
            planet: fields.body,
            aspect: fields.aspect,
            angle: fields.angle,
            variableId: v.id,
          };
          aspectIncludeCount += 1;
        } else {
          degradation.push({
            variableId: v.id,
            status: "deferred",
            reason: "additional_aspect_not_executed_v1",
          });
        }
      }
    }

    return {
      source: "genie_render",
      birth: { ...birthContext },
      house_conditions,
      angle_sign_conditions,
      aspectOverlay,
      degradation,
      canonicalVariableCount: payload.variables.length,
    };
  }

  const RelocationGenieMapEngineAdapter = Object.freeze({
    VERSION,
    validateGenieRender,
    buildEngineExecutionPlan,
    isTransitType,
  });

  global.RelocationGenieMapEngineAdapter = RelocationGenieMapEngineAdapter;
})(typeof globalThis !== "undefined" ? globalThis : window);
