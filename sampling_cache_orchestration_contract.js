/*
  Phase 2.7 runtime orchestration contract scaffold.

  This file defines sanitized orchestration envelopes and state transitions.
  It does not render, fetch, spawn workers, persist, or wire into map runtime.
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
  const REQUEST_FIELDS = Object.freeze([
    "schema_version",
    "chart_key",
    "investigation",
    "viewport",
    "sampling",
    "cache_key",
    "intent_group",
    "scope_role",
    "generation",
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

  function copyAllowed(source, fields) {
    const output = {};
    fields.forEach(field => {
      if (source[field] !== undefined) output[field] = cloneJson(source[field]);
    });
    return Object.freeze(output);
  }

  function hashString(value) {
    let hash = 2166136261;
    for (let i = 0; i < value.length; i++) {
      hash ^= value.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function stableStringify(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
    return `{${Object.keys(value).sort().map(key => (
      `${JSON.stringify(key)}:${stableStringify(value[key])}`
    )).join(",")}}`;
  }

  function createOrchestrationRequest(input) {
    assertObject(input, "orchestration request");
    const sanitized = copyAllowed(input, REQUEST_FIELDS);
    if (!sanitized.cache_key) throw new TypeError("cache_key is required");
    return Object.freeze({
      ...sanitized,
      schema_version: VERSION,
      intent_group: String(sanitized.intent_group || sanitized.cache_key),
      scope_role: String(sanitized.scope_role || "current_viewport"),
      generation: Number(sanitized.generation || 1),
    });
  }

  function createJobEnvelope(input) {
    assertObject(input, "job envelope");
    const request = createOrchestrationRequest(input.request || input);
    const tier = Number(input.tier == null ? TIERS.FOREGROUND_USER_REQUEST : input.tier);
    if (!Number.isInteger(tier) || tier < 0 || tier > 3) {
      throw new TypeError("tier must be 0, 1, 2, or 3");
    }
    const seed = {
      cache_key: request.cache_key,
      tier,
      scope_role: request.scope_role,
      generation: request.generation,
    };
    return Object.freeze({
      schema_version: VERSION,
      id: `orch:v${VERSION}:${hashString(stableStringify(seed))}`,
      tier,
      cache_key: request.cache_key,
      intent_group: request.intent_group,
      scope_role: request.scope_role,
      generation: request.generation,
      state: input.state || "queued",
      stale: Boolean(input.stale),
      cancelled: Boolean(input.cancelled),
      request,
      observer_progress: Object.freeze({
        status: input.observer_progress?.status || input.observerProgress?.status || "queued",
        completed: Number(input.observer_progress?.completed || input.observerProgress?.completed || 0),
        total: Number(input.observer_progress?.total || input.observerProgress?.total || 0),
        read_only: true,
      }),
    });
  }

  function classifyJobCompatibility(job, activeRequest) {
    assertObject(job, "job");
    const active = createOrchestrationRequest(activeRequest);
    const sameKey = job.cache_key === active.cache_key;
    const sameIntent = job.intent_group === active.intent_group;
    const sameGeneration = Number(job.generation) === Number(active.generation);
    return Object.freeze({
      compatible: sameKey && sameIntent && sameGeneration,
      same_cache_key: sameKey,
      same_intent_group: sameIntent,
      same_generation: sameGeneration,
      reason: sameKey && sameIntent && sameGeneration ? "compatible" : "stale_or_superseded",
    });
  }

  function applyRuntimePreemption(jobs, newRequest) {
    const active = createOrchestrationRequest(newRequest);
    const foreground = createJobEnvelope({
      request: active,
      tier: TIERS.FOREGROUND_USER_REQUEST,
      state: "queued",
    });
    const rewritten = (Array.isArray(jobs) ? jobs : []).map(job => {
      const envelope = createJobEnvelope(job);
      const compatibility = classifyJobCompatibility(envelope, active);
      const lowerTier = envelope.tier > TIERS.FOREGROUND_USER_REQUEST;
      return Object.freeze({
        ...envelope,
        state: compatibility.compatible ? envelope.state : "stale",
        stale: !compatibility.compatible,
        cancelled: lowerTier && !compatibility.compatible,
      });
    });
    return Object.freeze({
      foreground,
      jobs: Object.freeze([foreground, ...rewritten]),
    });
  }

  function markStaleJobs(jobs, activeRequest) {
    const active = createOrchestrationRequest(activeRequest);
    return Object.freeze((Array.isArray(jobs) ? jobs : []).map(job => {
      const envelope = createJobEnvelope(job);
      const compatibility = classifyJobCompatibility(envelope, active);
      return Object.freeze({
        ...envelope,
        state: compatibility.compatible ? envelope.state : "stale",
        stale: !compatibility.compatible,
      });
    }));
  }

  function createHydrationEnvelope(cacheEntry, activeRequest) {
    assertObject(cacheEntry, "cache entry");
    const active = createOrchestrationRequest(activeRequest);
    const sanitized = copyAllowed(cacheEntry, HYDRATION_FIELDS);
    const compatible = cacheEntry.key === active.cache_key;
    return Object.freeze({
      schema_version: VERSION,
      cache_key: String(cacheEntry.key || ""),
      compatible,
      hydrated: compatible,
      execution_required: false,
      hydration: Object.freeze(sanitized),
    });
  }

  global.RelocationSamplingCacheOrchestrationContract = Object.freeze({
    VERSION,
    TIERS,
    REQUEST_FIELDS,
    HYDRATION_FIELDS,
    createOrchestrationRequest,
    createJobEnvelope,
    classifyJobCompatibility,
    applyRuntimePreemption,
    markStaleJobs,
    createHydrationEnvelope,
  });
})(window);
