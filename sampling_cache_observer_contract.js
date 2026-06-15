/*
  Phase 2.10 observer/progress semantics contract.

  This file defines read-only observer envelopes for future visual layers. It
  does not render, animate, execute, fetch, schedule, persist, or wire into map
  runtime behavior.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const OBSERVER_STATES = Object.freeze({
    QUEUED: "queued",
    RUNNING: "running",
    PARTIALLY_DISCOVERED: "partially_discovered",
    HYDRATION_ELIGIBLE: "hydration_eligible",
    COMPLETED: "completed",
    STALE: "stale",
    CANCELLED: "cancelled",
    ERROR: "error",
  });
  const DISCOVERY_STATES = Object.freeze({
    NONE: "none",
    IMPLIED_NEARBY_STRUCTURE: "implied_nearby_structure",
    CONFIRMED_DISCOVERED_STRUCTURE: "confirmed_discovered_structure",
    UNRESOLVED_AMBIGUITY: "unresolved_ambiguity",
  });
  const COLOR_STATES = Object.freeze({
    NEUTRAL: "neutral",
    TRANSITIONING: "transitioning",
    COLORED: "colored",
    MUTED: "muted",
  });

  function assertObject(value, label) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new TypeError(`${label} must be an object`);
    }
  }

  function numberOrZero(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : 0;
  }

  function clamp01(value) {
    return Math.max(0, Math.min(1, numberOrZero(value)));
  }

  function executionStateFrom(input) {
    return String(input.state || input.status || input.job?.state || input.observer_progress?.status || OBSERVER_STATES.QUEUED);
  }

  function observerStateFor(input) {
    const state = executionStateFrom(input);
    if (input.stale || input.job?.stale || state === "stale") return OBSERVER_STATES.STALE;
    if (input.cancelled || input.job?.cancelled || state === "cancelled") return OBSERVER_STATES.CANCELLED;
    if (state === "error") return OBSERVER_STATES.ERROR;
    if (input.hydration_eligible || input.hydrated) return OBSERVER_STATES.HYDRATION_ELIGIBLE;
    if (state === "completed") return OBSERVER_STATES.COMPLETED;
    const completed = numberOrZero(input.observer_progress?.completed ?? input.completed);
    const total = numberOrZero(input.observer_progress?.total ?? input.total);
    if (state === "running" && total > 0 && completed > 0 && completed < total) {
      return OBSERVER_STATES.PARTIALLY_DISCOVERED;
    }
    if (state === "running") return OBSERVER_STATES.RUNNING;
    return OBSERVER_STATES.QUEUED;
  }

  function discoveryStateFor(input, observerState) {
    if ([OBSERVER_STATES.STALE, OBSERVER_STATES.CANCELLED, OBSERVER_STATES.ERROR].includes(observerState)) {
      return input.discovery_state === DISCOVERY_STATES.IMPLIED_NEARBY_STRUCTURE
        ? DISCOVERY_STATES.IMPLIED_NEARBY_STRUCTURE
        : DISCOVERY_STATES.NONE;
    }
    if (input.ambiguity || input.discovery_state === DISCOVERY_STATES.UNRESOLVED_AMBIGUITY) {
      return DISCOVERY_STATES.UNRESOLVED_AMBIGUITY;
    }
    if (input.discovery_state === DISCOVERY_STATES.IMPLIED_NEARBY_STRUCTURE) {
      return DISCOVERY_STATES.IMPLIED_NEARBY_STRUCTURE;
    }
    if (
      observerState === OBSERVER_STATES.COMPLETED ||
      observerState === OBSERVER_STATES.HYDRATION_ELIGIBLE ||
      input.discovery_state === DISCOVERY_STATES.CONFIRMED_DISCOVERED_STRUCTURE
    ) {
      return DISCOVERY_STATES.CONFIRMED_DISCOVERED_STRUCTURE;
    }
    return DISCOVERY_STATES.NONE;
  }

  function colorStateFor(observerState, discoveryState) {
    if ([OBSERVER_STATES.STALE, OBSERVER_STATES.CANCELLED, OBSERVER_STATES.ERROR].includes(observerState)) {
      return COLOR_STATES.MUTED;
    }
    if (discoveryState === DISCOVERY_STATES.CONFIRMED_DISCOVERED_STRUCTURE) {
      return COLOR_STATES.COLORED;
    }
    if (
      observerState === OBSERVER_STATES.PARTIALLY_DISCOVERED ||
      discoveryState === DISCOVERY_STATES.IMPLIED_NEARBY_STRUCTURE ||
      discoveryState === DISCOVERY_STATES.UNRESOLVED_AMBIGUITY
    ) {
      return COLOR_STATES.TRANSITIONING;
    }
    return COLOR_STATES.NEUTRAL;
  }

  function progressFor(input, observerState) {
    const completed = numberOrZero(input.observer_progress?.completed ?? input.completed);
    const total = numberOrZero(input.observer_progress?.total ?? input.total);
    if (observerState === OBSERVER_STATES.COMPLETED || observerState === OBSERVER_STATES.HYDRATION_ELIGIBLE) {
      return 1;
    }
    if (total <= 0) return 0;
    return clamp01(completed / total);
  }

  function createObserverEnvelope(input) {
    assertObject(input, "observer input");
    const observerState = observerStateFor(input);
    const discoveryState = discoveryStateFor(input, observerState);
    return Object.freeze({
      schema_version: VERSION,
      cache_key: String(input.cache_key || input.job?.cache_key || ""),
      intent_group: String(input.intent_group || input.job?.intent_group || ""),
      observer_state: observerState,
      discovery_state: discoveryState,
      color_state: colorStateFor(observerState, discoveryState),
      progress_ratio: progressFor(input, observerState),
      hydration_visible: Boolean(input.hydration_eligible || input.hydrated),
      truth_complete: observerState === OBSERVER_STATES.COMPLETED && discoveryState === DISCOVERY_STATES.CONFIRMED_DISCOVERED_STRUCTURE,
      read_only: true,
      can_control_scheduler: false,
      can_control_execution: false,
    });
  }

  function createObserverBatch(inputs) {
    return Object.freeze((Array.isArray(inputs) ? inputs : []).map(createObserverEnvelope));
  }

  global.RelocationSamplingCacheObserverContract = Object.freeze({
    VERSION,
    OBSERVER_STATES,
    DISCOVERY_STATES,
    COLOR_STATES,
    createObserverEnvelope,
    createObserverBatch,
  });
})(window);
