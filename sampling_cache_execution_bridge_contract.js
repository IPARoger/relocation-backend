/*
  Phase 2.9 mock execution bridge contract.

  This file defines deterministic lifecycle state transitions for orchestration
  jobs. It does not execute work, fetch, render, spawn workers, persist, or wire
  into map/UI runtime.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const STATES = Object.freeze({
    QUEUED: "queued",
    RUNNING: "running",
    COMPLETED: "completed",
    CANCELLED: "cancelled",
    STALE: "stale",
    ERROR: "error",
  });
  const TERMINAL_STATES = Object.freeze([
    STATES.COMPLETED,
    STATES.CANCELLED,
    STATES.STALE,
    STATES.ERROR,
  ]);
  const ALLOWED_TRANSITIONS = Object.freeze({
    queued: Object.freeze(["running", "cancelled", "stale", "error"]),
    running: Object.freeze(["completed", "cancelled", "stale", "error"]),
    completed: Object.freeze([]),
    cancelled: Object.freeze([]),
    stale: Object.freeze([]),
    error: Object.freeze([]),
  });
  const JOB_FIELDS = Object.freeze([
    "schema_version",
    "id",
    "tier",
    "cache_key",
    "intent_group",
    "scope_role",
    "generation",
    "state",
    "stale",
    "cancelled",
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

  function sanitizeJob(job) {
    assertObject(job, "execution job");
    const sanitized = {};
    JOB_FIELDS.forEach(field => {
      if (job[field] !== undefined) sanitized[field] = cloneJson(job[field]);
    });
    sanitized.schema_version = VERSION;
    sanitized.id = String(sanitized.id || "");
    sanitized.cache_key = String(sanitized.cache_key || "");
    sanitized.intent_group = String(sanitized.intent_group || sanitized.cache_key);
    sanitized.scope_role = String(sanitized.scope_role || "current_viewport");
    sanitized.generation = Number(sanitized.generation || 1);
    sanitized.tier = Number(sanitized.tier || 0);
    sanitized.state = String(sanitized.state || STATES.QUEUED);
    sanitized.stale = Boolean(sanitized.stale);
    sanitized.cancelled = Boolean(sanitized.cancelled);
    return Object.freeze(sanitized);
  }

  function canTransition(fromState, toState) {
    const from = String(fromState || STATES.QUEUED);
    const to = String(toState || "");
    return Boolean((ALLOWED_TRANSITIONS[from] || []).includes(to));
  }

  function observerProgressFor(job, message) {
    const state = String(job.state || STATES.QUEUED);
    const completed = state === STATES.COMPLETED ? 1 : 0;
    const total = TERMINAL_STATES.includes(state) ? 1 : 1;
    return Object.freeze({
      status: state,
      completed,
      total,
      message: String(message || state),
      read_only: true,
    });
  }

  function createExecutionEnvelope(input) {
    assertObject(input, "execution envelope");
    const job = sanitizeJob(input.job || input);
    return Object.freeze({
      schema_version: VERSION,
      job,
      state: job.state,
      foreground_owned: job.tier === 0,
      terminal: TERMINAL_STATES.includes(job.state),
      hydration_eligible: job.state === STATES.COMPLETED && !job.stale && !job.cancelled,
      observer_progress: observerProgressFor(job, input.message),
    });
  }

  function transitionExecution(envelopeOrJob, toState, options) {
    const current = createExecutionEnvelope(envelopeOrJob.job ? envelopeOrJob : { job: envelopeOrJob });
    const target = String(toState || "");
    if (!canTransition(current.state, target)) {
      return Object.freeze({
        ...current,
        rejected: true,
        rejection_reason: `invalid_transition:${current.state}->${target}`,
      });
    }
    const nextJob = sanitizeJob({
      ...current.job,
      state: target,
      stale: target === STATES.STALE || current.job.stale,
      cancelled: target === STATES.CANCELLED || current.job.cancelled,
    });
    return createExecutionEnvelope({ job: nextJob, message: options?.message || target });
  }

  function applyLogicalPreemption(jobs, foregroundJob) {
    const foreground = sanitizeJob({
      ...foregroundJob,
      tier: 0,
      state: foregroundJob?.state || STATES.QUEUED,
    });
    const rewritten = (Array.isArray(jobs) ? jobs : []).map(job => {
      const sanitized = sanitizeJob(job);
      const incompatible = sanitized.cache_key !== foreground.cache_key ||
        sanitized.intent_group !== foreground.intent_group ||
        Number(sanitized.generation) !== Number(foreground.generation);
      const lowerTier = sanitized.tier > 0;
      const state = incompatible ? STATES.STALE : sanitized.state;
      return createExecutionEnvelope({
        job: {
          ...sanitized,
          state,
          stale: incompatible,
          cancelled: lowerTier && incompatible,
        },
        message: incompatible ? "preempted" : sanitized.state,
      });
    });
    return Object.freeze({
      foreground: createExecutionEnvelope({ job: foreground }),
      jobs: Object.freeze(rewritten),
    });
  }

  function propagateStale(jobs, activeJob) {
    const active = sanitizeJob(activeJob);
    return Object.freeze((Array.isArray(jobs) ? jobs : []).map(job => {
      const sanitized = sanitizeJob(job);
      const stale = sanitized.cache_key !== active.cache_key ||
        sanitized.intent_group !== active.intent_group ||
        Number(sanitized.generation) !== Number(active.generation);
      return createExecutionEnvelope({
        job: {
          ...sanitized,
          state: stale ? STATES.STALE : sanitized.state,
          stale,
        },
        message: stale ? "stale" : sanitized.state,
      });
    }));
  }

  function canHydrate(envelopeOrJob) {
    const envelope = createExecutionEnvelope(envelopeOrJob.job ? envelopeOrJob : { job: envelopeOrJob });
    return envelope.hydration_eligible;
  }

  global.RelocationSamplingCacheExecutionBridgeContract = Object.freeze({
    VERSION,
    STATES,
    TERMINAL_STATES,
    ALLOWED_TRANSITIONS,
    createExecutionEnvelope,
    transitionExecution,
    canTransition,
    applyLogicalPreemption,
    propagateStale,
    canHydrate,
  });
})(window);
