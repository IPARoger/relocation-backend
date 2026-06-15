/*
  Phase 2.5 sampling/cache scheduler contract scaffold.

  This file defines renderer-neutral work descriptors and priority semantics.
  It does not render, fetch, schedule workers, persist cache state, or wire
  into map runtime behavior.
*/
(function(global) {
  "use strict";

  const VERSION = 1;

  const TIERS = Object.freeze({
    FOREGROUND_USER_REQUEST: 0,
    SAME_REQUEST_NEXT_SCOPE: 1,
    BOUNDARY_REFINEMENT: 2,
    ALTERNATE_INVESTIGATION: 3,
  });

  const TIER_NAMES = Object.freeze({
    0: "foreground_user_request",
    1: "same_request_next_scope",
    2: "boundary_refinement",
    3: "alternate_investigation",
  });

  const ALLOWED_DESCRIPTOR_FIELDS = Object.freeze([
    "schema_version",
    "id",
    "tier",
    "tier_name",
    "cache_key",
    "cache_payload",
    "scope_role",
    "reason",
    "preempt_group",
    "cancelled",
    "deprioritized",
  ]);

  function assertObject(value, label) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new TypeError(`${label} must be an object`);
    }
  }

  function normalizeTier(value) {
    const tier = Number(value);
    if (!Number.isInteger(tier) || tier < 0 || tier > 3) {
      throw new TypeError("tier must be 0, 1, 2, or 3");
    }
    return tier;
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

  function cloneCachePayload(payload) {
    if (payload == null) return null;
    assertObject(payload, "cache payload");
    const allowed = {};
    ["schema_version", "chart_key", "investigation", "viewport", "sampling"].forEach(key => {
      if (payload[key] !== undefined) allowed[key] = payload[key];
    });
    return JSON.parse(JSON.stringify(allowed));
  }

  function createWorkDescriptor(input) {
    assertObject(input, "work descriptor");
    const tier = normalizeTier(input.tier);
    const cacheKey = String(input.cache_key ?? input.cacheKey ?? "");
    if (!cacheKey) throw new TypeError("cache_key is required");
    const descriptorSeed = {
      tier,
      cache_key: cacheKey,
      scope_role: String(input.scope_role ?? input.scopeRole ?? TIER_NAMES[tier]),
      reason: String(input.reason || TIER_NAMES[tier]),
      preempt_group: String(input.preempt_group ?? input.preemptGroup ?? cacheKey),
    };
    return Object.freeze({
      schema_version: VERSION,
      id: `scw:v${VERSION}:${hashString(stableStringify(descriptorSeed))}`,
      tier,
      tier_name: TIER_NAMES[tier],
      cache_key: cacheKey,
      cache_payload: cloneCachePayload(input.cache_payload ?? input.cachePayload),
      scope_role: descriptorSeed.scope_role,
      reason: descriptorSeed.reason,
      preempt_group: descriptorSeed.preempt_group,
      cancelled: false,
      deprioritized: false,
    });
  }

  function sortWorkDescriptors(descriptors) {
    if (!Array.isArray(descriptors)) return [];
    return descriptors.slice().sort((a, b) => {
      const tierDelta = normalizeTier(a.tier) - normalizeTier(b.tier);
      if (tierDelta !== 0) return tierDelta;
      return String(a.id || "").localeCompare(String(b.id || ""));
    });
  }

  function applyUserPreemption(descriptors, foregroundDescriptor) {
    const foreground = createWorkDescriptor({
      ...foregroundDescriptor,
      tier: TIERS.FOREGROUND_USER_REQUEST,
      reason: foregroundDescriptor?.reason || "user_input_preempted_queue",
    });
    const foregroundGroup = foreground.preempt_group;
    const carried = Array.isArray(descriptors) ? descriptors : [];
    const rewritten = carried.map(item => {
      const descriptor = createWorkDescriptor(item);
      const sameGroup = descriptor.preempt_group === foregroundGroup;
      const lowerTier = descriptor.tier > TIERS.FOREGROUND_USER_REQUEST;
      return Object.freeze({
        ...descriptor,
        cancelled: lowerTier && !sameGroup,
        deprioritized: lowerTier,
      });
    });
    return Object.freeze({
      foreground,
      queue: Object.freeze(sortWorkDescriptors([foreground, ...rewritten])),
    });
  }

  function descriptorPublicShape(descriptor) {
    assertObject(descriptor, "descriptor");
    const shape = {};
    ALLOWED_DESCRIPTOR_FIELDS.forEach(key => {
      shape[key] = descriptor[key];
    });
    return Object.freeze(shape);
  }

  global.RelocationSamplingCacheSchedulerContract = Object.freeze({
    VERSION,
    TIERS,
    TIER_NAMES,
    ALLOWED_DESCRIPTOR_FIELDS,
    createWorkDescriptor,
    sortWorkDescriptors,
    applyUserPreemption,
    descriptorPublicShape,
  });
})(window);
