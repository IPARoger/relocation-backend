/*
  Phase 2.8 mock runtime harness.

  This file composes the semantic cache key, memory store, and orchestration
  contracts as a semantic flow proof. It does not fetch, render, persist, spawn
  workers, hydrate renderer output, or wire into map/UI runtime.
*/
(function(global) {
  "use strict";

  const VERSION = 1;

  function requireContract(name) {
    if (!global[name]) throw new Error(`${name} is required`);
    return global[name];
  }

  function cloneJson(value) {
    if (value == null) return value;
    return JSON.parse(JSON.stringify(value));
  }

  function sanitizeSavedInvestigation(input) {
    const source = input || {};
    return Object.freeze({
      chart_key: String(source.chart_key ?? source.chartKey ?? source.chart_id ?? ""),
      investigation: Object.freeze({
        house_conditions: cloneJson(source.house_conditions || source.houseConditions || []),
        angle_sign_conditions: cloneJson(source.angle_sign_conditions || source.angleSignConditions || []),
        aspect_overlay: cloneJson(source.aspect_overlay || source.aspectOverlay || null),
      }),
      viewport: cloneJson(source.viewport || {}),
      sampling: cloneJson(source.sampling || {}),
      intent_group: String(source.intent_group ?? source.intentGroup ?? source.chart_key ?? source.chartKey ?? source.chart_id ?? ""),
      scope_role: String(source.scope_role ?? source.scopeRole ?? "current_viewport"),
      generation: Number(source.generation || 1),
    });
  }

  function createMockRuntimeHarness(options) {
    const cacheContract = requireContract("RelocationSamplingCacheContract");
    const storeContract = requireContract("RelocationSamplingCacheStoreContract");
    const orchestrationContract = requireContract("RelocationSamplingCacheOrchestrationContract");
    const store = options?.store || storeContract.createMemoryCacheStore(options?.store_options || options?.storeOptions || {});

    function createSemanticRequest(input) {
      const saved = sanitizeSavedInvestigation(input);
      const semantic = cacheContract.createSemanticCacheKey(saved);
      return Object.freeze({
        schema_version: VERSION,
        saved_investigation: saved,
        semantic,
        orchestration_request: orchestrationContract.createOrchestrationRequest({
          ...semantic.payload,
          cache_key: semantic.key,
          intent_group: saved.intent_group || semantic.key,
          scope_role: saved.scope_role,
          generation: saved.generation,
        }),
      });
    }

    function handleRequest(input) {
      const semanticRequest = createSemanticRequest(input);
      const cached = store.get(semanticRequest.semantic.key);
      if (cached) {
        const hydration = orchestrationContract.createHydrationEnvelope(
          {
            key: cached.key,
            status: cached.value.status,
            summary: cached.value.summary,
            metrics: cached.value.metrics,
            created_at_ms: cached.created_at_ms,
            updated_at_ms: cached.updated_at_ms,
            expires_at_ms: cached.expires_at_ms,
          },
          semanticRequest.orchestration_request
        );
        return Object.freeze({
          schema_version: VERSION,
          outcome: "cache_hit",
          semantic_request: semanticRequest,
          hydration,
          execution_required: false,
          job: null,
        });
      }
      const job = orchestrationContract.createJobEnvelope({
        request: semanticRequest.orchestration_request,
        tier: orchestrationContract.TIERS.FOREGROUND_USER_REQUEST,
      });
      return Object.freeze({
        schema_version: VERSION,
        outcome: "cache_miss",
        semantic_request: semanticRequest,
        hydration: null,
        execution_required: false,
        job,
      });
    }

    function seedCache(input, value) {
      const semanticRequest = createSemanticRequest(input);
      return store.set({
        key: semanticRequest.semantic.key,
        payload: semanticRequest.semantic.payload,
        value: value || { status: "ready" },
      });
    }

    function simulateSameRequestScope(input, scopePatch) {
      const base = createSemanticRequest(input);
      const patched = createSemanticRequest({
        ...input,
        viewport: { ...input.viewport, ...(scopePatch?.viewport || {}) },
        sampling: { ...input.sampling, ...(scopePatch?.sampling || {}) },
        scope_role: scopePatch?.scope_role || scopePatch?.scopeRole || "next_scope",
        intent_group: base.orchestration_request.intent_group,
        generation: base.orchestration_request.generation,
      });
      const job = orchestrationContract.createJobEnvelope({
        request: patched.orchestration_request,
        tier: orchestrationContract.TIERS.SAME_REQUEST_NEXT_SCOPE,
      });
      return Object.freeze({
        base,
        patched,
        job,
        compatibility: orchestrationContract.classifyJobCompatibility(
          job,
          base.orchestration_request
        ),
      });
    }

    function simulatePreemption(existingJobs, nextInput) {
      const next = createSemanticRequest(nextInput);
      return orchestrationContract.applyRuntimePreemption(
        existingJobs || [],
        next.orchestration_request
      );
    }

    function inspect() {
      return Object.freeze({
        schema_version: VERSION,
        store: store.inspect(),
      });
    }

    return Object.freeze({
      createSemanticRequest,
      handleRequest,
      seedCache,
      simulateSameRequestScope,
      simulatePreemption,
      inspect,
      store,
    });
  }

  global.RelocationSamplingCacheMockRuntimeHarness = Object.freeze({
    VERSION,
    createMockRuntimeHarness,
  });
})(window);
