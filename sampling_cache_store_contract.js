/*
  Phase 2.6 in-memory sampling/cache store contract scaffold.

  This file defines a local memory store for sanitized semantic cache entries.
  It does not render, fetch, persist, spawn workers, or wire into runtime map
  behavior.
*/
(function(global) {
  "use strict";

  const VERSION = 1;
  const DEFAULT_TTL_MS = 5 * 60 * 1000;
  const PAYLOAD_FIELDS = Object.freeze([
    "schema_version",
    "chart_key",
    "investigation",
    "viewport",
    "sampling",
  ]);
  const VALUE_FIELDS = Object.freeze(["status", "summary", "metrics", "error"]);

  function assertObject(value, label) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new TypeError(`${label} must be an object`);
    }
  }

  function nowMs(clock) {
    return Number(clock ? clock() : Date.now());
  }

  function cloneJson(value) {
    if (value == null) return value;
    return JSON.parse(JSON.stringify(value));
  }

  function sanitizePayload(payload) {
    assertObject(payload, "cache payload");
    const sanitized = {};
    PAYLOAD_FIELDS.forEach(field => {
      if (payload[field] !== undefined) sanitized[field] = cloneJson(payload[field]);
    });
    return Object.freeze(sanitized);
  }

  function sanitizeValue(value) {
    const source = value || {};
    assertObject(source, "cache value");
    const sanitized = {};
    VALUE_FIELDS.forEach(field => {
      if (source[field] === undefined) return;
      if (field === "error" && typeof source[field] !== "string") return;
      sanitized[field] = cloneJson(source[field]);
    });
    return Object.freeze(sanitized);
  }

  function cloneEntry(entry) {
    if (!entry) return null;
    return Object.freeze({
      schema_version: entry.schema_version,
      key: entry.key,
      payload: Object.freeze(cloneJson(entry.payload)),
      value: Object.freeze(cloneJson(entry.value)),
      created_at_ms: entry.created_at_ms,
      updated_at_ms: entry.updated_at_ms,
      expires_at_ms: entry.expires_at_ms,
    });
  }

  function createMemoryCacheStore(options) {
    const opts = options || {};
    const ttlMs = Number(opts.ttl_ms ?? opts.ttlMs ?? DEFAULT_TTL_MS);
    if (!Number.isFinite(ttlMs) || ttlMs <= 0) {
      throw new TypeError("ttl_ms must be a positive finite number");
    }
    const clock = typeof opts.now === "function" ? opts.now : null;
    const entries = new Map();

    function isExpired(entry, atMs) {
      return Number(entry.expires_at_ms) <= atMs;
    }

    function get(key) {
      const stringKey = String(key || "");
      const entry = entries.get(stringKey);
      if (!entry) return null;
      if (isExpired(entry, nowMs(clock))) {
        entries.delete(stringKey);
        return null;
      }
      return cloneEntry(entry);
    }

    function has(key) {
      return get(key) !== null;
    }

    function set(entry) {
      assertObject(entry, "cache entry");
      const key = String(entry.key || entry.cache_key || entry.cacheKey || "");
      if (!key) throw new TypeError("cache entry key is required");
      const atMs = nowMs(clock);
      const existing = entries.get(key);
      const createdAt = existing ? existing.created_at_ms : atMs;
      const stored = Object.freeze({
        schema_version: VERSION,
        key,
        payload: sanitizePayload(entry.payload || entry.cache_payload || entry.cachePayload),
        value: sanitizeValue(entry.value || {}),
        created_at_ms: createdAt,
        updated_at_ms: atMs,
        expires_at_ms: atMs + ttlMs,
      });
      entries.set(key, stored);
      return cloneEntry(stored);
    }

    function invalidate(keyOrPredicate) {
      if (typeof keyOrPredicate === "function") {
        let removed = 0;
        Array.from(entries.entries()).forEach(([key, entry]) => {
          if (keyOrPredicate(cloneEntry(entry))) {
            entries.delete(key);
            removed++;
          }
        });
        return removed;
      }
      const key = String(keyOrPredicate || "");
      return entries.delete(key) ? 1 : 0;
    }

    function clear() {
      const count = entries.size;
      entries.clear();
      return count;
    }

    function inspect() {
      const atMs = nowMs(clock);
      const summaries = [];
      Array.from(entries.entries()).forEach(([key, entry]) => {
        if (isExpired(entry, atMs)) {
          entries.delete(key);
          return;
        }
        summaries.push(Object.freeze({
          key,
          status: entry.value.status || null,
          created_at_ms: entry.created_at_ms,
          updated_at_ms: entry.updated_at_ms,
          expires_at_ms: entry.expires_at_ms,
          payload_fields: Object.freeze(Object.keys(entry.payload).sort()),
          value_fields: Object.freeze(Object.keys(entry.value).sort()),
        }));
      });
      return Object.freeze({
        schema_version: VERSION,
        count: summaries.length,
        ttl_ms: ttlMs,
        entries: Object.freeze(summaries),
      });
    }

    return Object.freeze({ get, set, has, invalidate, inspect, clear });
  }

  global.RelocationSamplingCacheStoreContract = Object.freeze({
    VERSION,
    DEFAULT_TTL_MS,
    PAYLOAD_FIELDS,
    VALUE_FIELDS,
    createMemoryCacheStore,
  });
})(window);
