/*
  Phase 2.12 dev/smoke-only runtime bridge scaffold.

  This bridge composes committed semantic/cache/orchestration/lifecycle/observer/
  policy contracts in a browser context. It produces metadata-only envelopes and
  never fetches, renders, starts workers, persists, or mutates DOM/map state.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";

  function requireContract(name) {
    if (!global[name]) throw new Error(`${name} is required`);
    return global[name];
  }

  function createDevRuntimeBridge(options) {
    const cache = requireContract("RelocationSamplingCacheContract");
    const storeContract = requireContract("RelocationSamplingCacheStoreContract");
    const orchestration = requireContract("RelocationSamplingCacheOrchestrationContract");
    const execution = requireContract("RelocationSamplingCacheExecutionBridgeContract");
    const observer = requireContract("RelocationSamplingCacheObserverContract");
    const policy = requireContract("RelocationSamplingCacheExecutionPolicyContract");
    const store = options?.store || storeContract.createMemoryCacheStore(options?.store_options || options?.storeOptions || {});

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

    function requestEnvelope(input) {
      const semantic = semanticInput(input);
      const key = cache.createSemanticCacheKey(semantic);
      const request = orchestration.createOrchestrationRequest({
        ...key.payload,
        cache_key: key.key,
        intent_group: semantic.intent_group || key.key,
        scope_role: semantic.scope_role,
        generation: semantic.generation,
      });
      return Object.freeze({ semantic, key, request });
    }

    function seedCache(input, value) {
      const envelope = requestEnvelope(input);
      return store.set({
        key: envelope.key.key,
        payload: envelope.key.payload,
        value: value || { status: "ready", summary: {}, metrics: {} },
      });
    }

    function evaluate(input) {
      const envelope = requestEnvelope(input);
      const cached = store.get(envelope.key.key);
      if (cached) {
        const hydration = orchestration.createHydrationEnvelope({
          key: cached.key,
          status: cached.value.status,
          summary: cached.value.summary,
          metrics: cached.value.metrics,
          created_at_ms: cached.created_at_ms,
          updated_at_ms: cached.updated_at_ms,
          expires_at_ms: cached.expires_at_ms,
        }, envelope.request);
        const executionEnvelope = execution.createExecutionEnvelope({
          job: {
            tier: 0,
            cache_key: envelope.key.key,
            intent_group: envelope.request.intent_group,
            scope_role: envelope.request.scope_role,
            generation: envelope.request.generation,
            state: "completed",
            hydration_eligible: hydration.compatible,
          },
        });
        const observerEnvelope = observer.createObserverEnvelope(executionEnvelope);
        const policyEnvelope = policy.applyExecutionPolicy({
          context: { budgets: { foreground: 1, same_request: 0, boundary: 0, alternate: 0, total: 1 } },
          work: [executionEnvelope.job],
        });
        return Object.freeze({
          schema_version: VERSION,
          mode: "dev_smoke_only",
          rendererSubstrate: RENDERER_SUBSTRATE,
          outcome: "cache_hit",
          semantic_key: envelope.key.key,
          hydration,
          execution: executionEnvelope,
          observer: observerEnvelope,
          policy: policyEnvelope,
          execution_required: false,
        });
      }

      const job = orchestration.createJobEnvelope({ request: envelope.request, tier: 0 });
      const executionEnvelope = execution.createExecutionEnvelope({ job });
      const observerEnvelope = observer.createObserverEnvelope(executionEnvelope);
      const policyEnvelope = policy.applyExecutionPolicy({
        context: { budgets: { foreground: 1, same_request: 0, boundary: 0, alternate: 0, total: 1 } },
        work: [job],
      });
      return Object.freeze({
        schema_version: VERSION,
        mode: "dev_smoke_only",
        rendererSubstrate: RENDERER_SUBSTRATE,
        outcome: "cache_miss",
        semantic_key: envelope.key.key,
        hydration: null,
        execution: executionEnvelope,
        observer: observerEnvelope,
        policy: policyEnvelope,
        execution_required: false,
      });
    }

    return Object.freeze({
      evaluate,
      seedCache,
      inspect() {
        return Object.freeze({
          schema_version: VERSION,
          rendererSubstrate: RENDERER_SUBSTRATE,
          store: store.inspect(),
        });
      },
    });
  }

  global.RelocationSamplingCacheRuntimeBridgeDev = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    createDevRuntimeBridge,
  });
})(window);
