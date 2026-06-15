/*
  Phase 2.11 execution policy semantics contract.

  This file defines foreground guarantees, conceptual budgets, hydration gates,
  readiness distinctions, observer cadence, and speculative limits. It does not
  execute, fetch, render, persist, interpret astrology, or implement AI/intake.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const DEFAULT_BUDGETS = Object.freeze({
    foreground: 1,
    same_request: 2,
    boundary: 1,
    alternate: 1,
    total: 4,
  });
  const READINESS = Object.freeze({
    NOT_READY: "not_ready",
    TRUTH_READY: "truth_ready",
    HYDRATION_READY: "hydration_ready",
    DISPLAY_READY: "display_ready",
  });
  const POLICY_FIELDS = Object.freeze([
    "tier",
    "cache_key",
    "intent_group",
    "scope_role",
    "generation",
    "state",
    "stale",
    "cancelled",
    "hydration_eligible",
    "observer_state",
  ]);
  const HINT_FIELDS = Object.freeze([
    "source",
    "mode",
    "priority",
    "confidence",
    "reason",
  ]);

  function assertObject(value, label) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new TypeError(`${label} must be an object`);
    }
  }

  function numberOrDefault(value, fallback) {
    const n = Number(value);
    return Number.isFinite(n) ? n : fallback;
  }

  function tierBucket(tier) {
    const value = Number(tier || 0);
    if (value === 0) return "foreground";
    if (value === 1) return "same_request";
    if (value === 2) return "boundary";
    return "alternate";
  }

  function sanitizeWork(input) {
    assertObject(input, "policy work item");
    const source = input.job || input;
    const out = {};
    POLICY_FIELDS.forEach(field => {
      if (source[field] !== undefined) out[field] = source[field];
    });
    out.tier = Number(out.tier || 0);
    out.cache_key = String(out.cache_key || "");
    out.intent_group = String(out.intent_group || out.cache_key);
    out.scope_role = String(out.scope_role || "current_viewport");
    out.generation = Number(out.generation || 1);
    out.state = String(out.state || "queued");
    out.stale = Boolean(out.stale);
    out.cancelled = Boolean(out.cancelled);
    out.hydration_eligible = Boolean(out.hydration_eligible);
    return Object.freeze(out);
  }

  function sanitizePriorityHint(input) {
    const source = input || {};
    const out = {};
    HINT_FIELDS.forEach(field => {
      if (source[field] !== undefined) out[field] = source[field];
    });
    return Object.freeze({
      source: String(out.source || "unspecified"),
      mode: String(out.mode || "neutral"),
      priority: String(out.priority || "normal"),
      confidence: Math.max(0, Math.min(1, numberOrDefault(out.confidence, 0))),
      reason: String(out.reason || ""),
      astrology_meaning_encoded: false,
    });
  }

  function createPolicyContext(input) {
    const source = input || {};
    const budgets = { ...DEFAULT_BUDGETS, ...(source.budgets || {}) };
    return Object.freeze({
      schema_version: VERSION,
      budgets: Object.freeze({
        foreground: Math.max(1, Math.floor(numberOrDefault(budgets.foreground, DEFAULT_BUDGETS.foreground))),
        same_request: Math.max(0, Math.floor(numberOrDefault(budgets.same_request, DEFAULT_BUDGETS.same_request))),
        boundary: Math.max(0, Math.floor(numberOrDefault(budgets.boundary, DEFAULT_BUDGETS.boundary))),
        alternate: Math.max(0, Math.floor(numberOrDefault(budgets.alternate, DEFAULT_BUDGETS.alternate))),
        total: Math.max(1, Math.floor(numberOrDefault(budgets.total, DEFAULT_BUDGETS.total))),
      }),
      observer_cadence_ms: Math.max(0, Math.floor(numberOrDefault(source.observer_cadence_ms ?? source.observerCadenceMs, 250))),
      speculative_limit: Math.max(0, Math.floor(numberOrDefault(source.speculative_limit ?? source.speculativeLimit, 1))),
      priority_hint: sanitizePriorityHint(source.priority_hint || source.priorityHint),
    });
  }

  function readinessFor(work) {
    const item = sanitizeWork(work);
    if (item.stale || item.cancelled || item.state === "stale" || item.state === "cancelled" || item.state === "error") {
      return READINESS.NOT_READY;
    }
    if (item.hydration_eligible && item.state === "completed") {
      return READINESS.HYDRATION_READY;
    }
    if (item.state === "completed") {
      return READINESS.TRUTH_READY;
    }
    return READINESS.NOT_READY;
  }

  function canHydrateUnderPolicy(work) {
    return readinessFor(work) === READINESS.HYDRATION_READY;
  }

  function sortByPolicyPriority(items) {
    return items.slice().sort((a, b) => {
      const tierDelta = a.tier - b.tier;
      if (tierDelta !== 0) return tierDelta;
      const aReady = a.state === "completed" ? 1 : 0;
      const bReady = b.state === "completed" ? 1 : 0;
      if (aReady !== bReady) return aReady - bReady;
      return String(a.cache_key).localeCompare(String(b.cache_key));
    });
  }

  function applyExecutionPolicy(input) {
    assertObject(input, "execution policy input");
    const context = createPolicyContext(input.context || {});
    const items = sortByPolicyPriority((input.work || []).map(sanitizeWork));
    const used = { foreground: 0, same_request: 0, boundary: 0, alternate: 0, total: 0 };
    const decisions = items.map(item => {
      const bucket = tierBucket(item.tier);
      const terminalOrInvalid = item.stale || item.cancelled || ["stale", "cancelled", "error"].includes(item.state);
      let decision = "defer";
      if (terminalOrInvalid) {
        decision = "drop";
      } else if (item.tier === 0 && used.foreground < context.budgets.foreground && used.total < context.budgets.total) {
        decision = "run";
      } else if (item.tier > 0 && used[bucket] < context.budgets[bucket] && used.total < context.budgets.total) {
        decision = "run";
      } else if (item.tier >= 3) {
        decision = "throttle";
      }
      if (decision === "run") {
        used[bucket]++;
        used.total++;
      }
      return Object.freeze({
        schema_version: VERSION,
        cache_key: item.cache_key,
        tier: item.tier,
        bucket,
        decision,
        readiness: readinessFor(item),
        hydration_allowed: canHydrateUnderPolicy(item),
        observer_update_allowed: decision === "run" || item.state === "completed",
        observer_cadence_ms: context.observer_cadence_ms,
        reason: terminalOrInvalid ? "stale_cancelled_or_error" : decision,
      });
    });
    return Object.freeze({
      schema_version: VERSION,
      context,
      decisions: Object.freeze(decisions),
      foreground_blocked: !decisions.some(d => d.tier === 0 && d.decision === "run"),
      used_budget: Object.freeze(used),
    });
  }

  global.RelocationSamplingCacheExecutionPolicyContract = Object.freeze({
    VERSION,
    DEFAULT_BUDGETS,
    READINESS,
    createPolicyContext,
    sanitizePriorityHint,
    readinessFor,
    canHydrateUnderPolicy,
    applyExecutionPolicy,
  });
})(window);
