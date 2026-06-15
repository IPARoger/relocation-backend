/*
  Phase 2.13 dev/smoke-only execution runtime.

  This runtime simulates one controlled semantic request lifecycle. It writes
  sanitized metadata into the in-memory store and never fetches, renders, starts
  workers, persists, mutates map state, or hydrates renderer output.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";

  function requireContract(name) {
    if (!global[name]) throw new Error(`${name} is required`);
    return global[name];
  }

  function createExecutionRuntimeDev(options) {
    const cache = requireContract("RelocationSamplingCacheContract");
    const storeContract = requireContract("RelocationSamplingCacheStoreContract");
    const orchestration = requireContract("RelocationSamplingCacheOrchestrationContract");
    const execution = requireContract("RelocationSamplingCacheExecutionBridgeContract");
    const observer = requireContract("RelocationSamplingCacheObserverContract");
    const policy = requireContract("RelocationSamplingCacheExecutionPolicyContract");
    const store = options?.store || storeContract.createMemoryCacheStore(options?.store_options || options?.storeOptions || {});
    let active = false;

    function semanticInput(input) {
      const source = input || {};
      return Object.freeze({
        chart_key: String(source.chart_key || source.chartKey || source.chart_id || ""),
        investigation: Object.freeze({
          house_conditions: source.house_conditions || source.houseConditions || [],
          angle_sign_conditions: source.angle_sign_conditions || source.angleSignConditions || [],
          aspect_overlay: source.aspect_overlay || source.aspectOverlay || null,
        }),
        viewport: source.viewport || {},
        sampling: source.sampling || {},
        intent_group: String(source.intent_group || source.intentGroup || source.chart_key || source.chartKey || source.chart_id || ""),
        scope_role: String(source.scope_role || source.scopeRole || "current_viewport"),
        generation: Number(source.generation || 1),
      });
    }

    function createRequest(input) {
      const semantic = semanticInput(input);
      const key = cache.createSemanticCacheKey(semantic);
      const request = orchestration.createOrchestrationRequest({
        ...key.payload,
        cache_key: key.key,
        intent_group: semantic.intent_group || key.key,
        scope_role: semantic.scope_role,
        generation: semantic.generation,
      });
      const job = orchestration.createJobEnvelope({ request, tier: 0 });
      return Object.freeze({ semantic, key, request, job });
    }

    function hydrationFor(entry, request) {
      return orchestration.createHydrationEnvelope({
        key: entry.key,
        status: entry.value.status,
        summary: entry.value.summary,
        metrics: entry.value.metrics,
        created_at_ms: entry.created_at_ms,
        updated_at_ms: entry.updated_at_ms,
        expires_at_ms: entry.expires_at_ms,
      }, request);
    }

    function executeOnce(input) {
      if (active) {
        return Object.freeze({
          schema_version: VERSION,
          mode: "dev_single_request_only",
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: false,
          reason: "active_request_in_progress",
        });
      }
      active = true;
      try {
        const request = createRequest(input);
        const policyEnvelope = policy.applyExecutionPolicy({
          context: { budgets: { foreground: 1, same_request: 0, boundary: 0, alternate: 0, total: 1 } },
          work: [request.job],
        });
        const allowed = policyEnvelope.decisions[0]?.decision === "run";
        if (!allowed) {
          return Object.freeze({
            schema_version: VERSION,
            mode: "dev_single_request_only",
            rendererSubstrate: RENDERER_SUBSTRATE,
            accepted: false,
            reason: "policy_denied",
            policy: policyEnvelope,
          });
        }
        const queued = execution.createExecutionEnvelope({ job: request.job });
        const running = execution.transitionExecution(queued, execution.STATES.RUNNING);
        const completed = execution.transitionExecution(running, execution.STATES.COMPLETED);
        const stored = store.set({
          key: request.key.key,
          payload: request.key.payload,
          value: {
            status: "ready",
            summary: { lifecycle: "queued_running_completed" },
            metrics: { simulated_pass_count: 1 },
          },
        });
        const hydration = hydrationFor(stored, request.request);
        const hydratedExecution = execution.createExecutionEnvelope({
          job: {
            ...completed.job,
            hydration_eligible: hydration.compatible,
          },
        });
        const observerEnvelope = observer.createObserverEnvelope(hydratedExecution);
        return Object.freeze({
          schema_version: VERSION,
          mode: "dev_single_request_only",
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: true,
          semantic_key: request.key.key,
          lifecycle: Object.freeze([queued.state, running.state, completed.state]),
          policy: policyEnvelope,
          execution: hydratedExecution,
          hydration,
          observer: observerEnvelope,
          store: store.inspect(),
        });
      } finally {
        active = false;
      }
    }

    return Object.freeze({
      executeOnce,
      inspect() {
        return Object.freeze({
          schema_version: VERSION,
          rendererSubstrate: RENDERER_SUBSTRATE,
          active,
          store: store.inspect(),
        });
      },
    });
  }

  global.RelocationSamplingCacheExecutionRuntimeDev = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    createExecutionRuntimeDev,
  });
})(window);
