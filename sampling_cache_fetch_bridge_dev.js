/*
  Phase 2.14 isolated dev fetch bridge.

  This bridge executes one controlled backend fetch and stores sanitized metadata
  only. It does not render, create layers, persist, start workers, mutate map
  state, or replace production runtime behavior.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const RENDERER_SUBSTRATE = "legacy_search_regions";
  const DEFAULT_ENDPOINT = "http://127.0.0.1:8000/search-regions";

  function requireContract(name) {
    if (!global[name]) throw new Error(`${name} is required`);
    return global[name];
  }

  function firstHouseCondition(input) {
    const list = input.house_conditions || input.houseConditions || [];
    const first = list[0] || {};
    return {
      type: "planet_in_house",
      planet: String(first.planet || "sun").toLowerCase(),
      house: Number(first.house || 1),
    };
  }

  function buildSearchPayload(input) {
    const source = input || {};
    return Object.freeze({
      birth_year: Number(source.birth_year || source.birthYear || 1990),
      birth_month: Number(source.birth_month || source.birthMonth || 1),
      birth_day: Number(source.birth_day || source.birthDay || 1),
      birth_hour_utc: Number(source.birth_hour_utc || source.birthHourUTC || 12),
      house_conditions: [firstHouseCondition(source)],
      angle_sign_conditions: [],
      resolution: Number(source.resolution || 30),
      generation_mode: "contour",
    });
  }

  function semanticInput(input) {
    const source = input || {};
    return Object.freeze({
      chart_key: String(source.chart_key || source.chartKey || source.chart_id || "dev-chart"),
      investigation: Object.freeze({
        house_conditions: source.house_conditions || source.houseConditions || [firstHouseCondition(source)],
        angle_sign_conditions: [],
        aspect_overlay: null,
      }),
      viewport: source.viewport || { north: 60, south: -60, east: 180, west: -180, zoom: 1 },
      sampling: source.sampling || { width: 360, height: 180, block_px: 30, lat_cap: true },
      intent_group: String(source.intent_group || source.intentGroup || source.chart_key || source.chartKey || source.chart_id || "dev-chart"),
      scope_role: "dev_fetch_bridge",
      generation: Number(source.generation || 1),
    });
  }

  function sanitizeBackendMetadata(data, responseStatus) {
    const features = Array.isArray(data?.features) ? data.features : [];
    return Object.freeze({
      status: responseStatus >= 200 && responseStatus < 300 ? "ready" : "error",
      summary: Object.freeze({
        feature_count: features.length,
        response_type: String(data?.type || "unknown"),
      }),
      metrics: Object.freeze({
        backend_status: responseStatus,
      }),
    });
  }

  function createFetchBridgeDev(options) {
    const cache = requireContract("RelocationSamplingCacheContract");
    const storeContract = requireContract("RelocationSamplingCacheStoreContract");
    const orchestration = requireContract("RelocationSamplingCacheOrchestrationContract");
    const execution = requireContract("RelocationSamplingCacheExecutionBridgeContract");
    const observer = requireContract("RelocationSamplingCacheObserverContract");
    const policy = requireContract("RelocationSamplingCacheExecutionPolicyContract");
    const store = options?.store || storeContract.createMemoryCacheStore(options?.store_options || options?.storeOptions || {});
    const endpoint = options?.endpoint || DEFAULT_ENDPOINT;
    let active = false;

    async function executeOnce(input) {
      if (active) {
        return Object.freeze({
          schema_version: VERSION,
          mode: "dev_single_fetch_only",
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: false,
          reason: "active_request_in_progress",
        });
      }
      active = true;
      try {
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
        const policyEnvelope = policy.applyExecutionPolicy({
          context: { budgets: { foreground: 1, same_request: 0, boundary: 0, alternate: 0, total: 1 } },
          work: [job],
        });
        const queued = execution.createExecutionEnvelope({ job });
        const running = execution.transitionExecution(queued, execution.STATES.RUNNING);
        const response = await global.fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(buildSearchPayload(input)),
        });
        const data = await response.json();
        const metadata = sanitizeBackendMetadata(data, response.status);
        const completed = execution.transitionExecution(running, execution.STATES.COMPLETED);
        const stored = store.set({
          key: key.key,
          payload: key.payload,
          value: metadata,
        });
        const hydration = orchestration.createHydrationEnvelope({
          key: stored.key,
          status: stored.value.status,
          summary: stored.value.summary,
          metrics: stored.value.metrics,
          created_at_ms: stored.created_at_ms,
          updated_at_ms: stored.updated_at_ms,
          expires_at_ms: stored.expires_at_ms,
        }, request);
        const hydratedExecution = execution.createExecutionEnvelope({
          job: {
            ...completed.job,
            hydration_eligible: hydration.compatible,
          },
        });
        const observerEnvelope = observer.createObserverEnvelope(hydratedExecution);
        return Object.freeze({
          schema_version: VERSION,
          mode: "dev_single_fetch_only",
          rendererSubstrate: RENDERER_SUBSTRATE,
          accepted: true,
          semantic_key: key.key,
          lifecycle: Object.freeze([queued.state, running.state, completed.state]),
          policy: policyEnvelope,
          execution: hydratedExecution,
          hydration,
          observer: observerEnvelope,
          store: store.inspect(),
          backend: Object.freeze({
            endpoint,
            status: response.status,
            metadata,
          }),
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
          endpoint,
          store: store.inspect(),
        });
      },
    });
  }

  global.RelocationSamplingCacheFetchBridgeDev = Object.freeze({
    VERSION,
    RENDERER_SUBSTRATE,
    DEFAULT_ENDPOINT,
    createFetchBridgeDev,
  });
})(window);
