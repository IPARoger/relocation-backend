/*
  Phase-2 cache scheduler shell.

  Extracted from map_SANDBOX_phase2_cache.html without changing sandbox
  behavior. This module owns queue state, cancellation, budget checks,
  cache commits, and status transitions. The host still owns viewport
  point construction, background job registration, and rendering.
*/
(function(global) {
  "use strict";

  function createPhase2CacheScheduler(options) {
    const {
      budget,
      idleGraceMs,
      defaultBlock,
      buildPointsForJob,
      fetchClassification,
      renderQueue,
      renderStatus,
    } = options;

    if (typeof buildPointsForJob !== "function") {
      throw new Error("buildPointsForJob is required");
    }
    if (typeof fetchClassification !== "function") {
      throw new Error("fetchClassification is required");
    }

    const PHASE2 = {
      status: "idle",
      events: [],
      cache: new Map(),           // key -> {result, samples, completedAt}
      jobs: [],                   // every job ever queued, in order
      budgetUsed: 0,              // running total of cached samples
      active: null,               // currently-running job or null
      pausedForUser: false,       // true between pause() and resume()
      cachePaused: false,         // true after map interaction until next requestUser
      metrics: {
        serverCalls: 0,
        cacheHits: 0,
        abortsObserved: 0,
        deferredForBudget: 0,
        immediateCompleted: 0,
        backgroundCompleted: 0,
      },
      // Set by the host after init()
      birth: null,
      birthKey: "",
      conditions: [],
      baseView: null,
      budget,
    };

    function now() { return new Date().toISOString().slice(11, 23); }

    function emit(type, payload) {
      const ev = { ts: now(), type, payload: payload || {} };
      PHASE2.events.push(ev);
      if (PHASE2.events.length > 500) PHASE2.events.shift();
    }

    function updateQueue() {
      if (typeof renderQueue === "function") renderQueue();
    }

    function setStatus(s) {
      if (PHASE2.status !== s) {
        PHASE2.status = s;
        emit("status", { status: s });
      }
      if (typeof renderStatus === "function") renderStatus();
    }

    function cacheKey(parts) {
      // Stable canonical key for the cache. Order-sensitive on viewport
      // bounds and zoom; order-insensitive on conditions (we sort by id).
      const cs = (parts.conditions || []).map(c => JSON.stringify(c)).sort();
      return JSON.stringify({
        chart: PHASE2.birthKey,
        bounds: parts.bounds,
        zoom: parts.zoom,
        block: parts.block,
        conditions: cs,
        lat_cap: parts.applyLatCap || false,
      });
    }

    function runJob(job) {
      // Returns a promise. On success: populates cache, marks job done.
      // On abort or error: leaves cache untouched.
      const controller = new AbortController();
      job.controller = controller;
      job.status = "active";
      job.startedAt = now();
      PHASE2.active = job;
      emit("job_start", { priority: job.priority, label: job.label });
      updateQueue();

      const grid = buildPointsForJob(job);
      const key = cacheKey({
        bounds: grid.bounds,
        zoom: grid.zoom,
        block: job.block || defaultBlock,
        conditions: job.conditions,
        applyLatCap: job.applyLatCap,
      });
      job.cacheKey = key;
      job.samplesRequested = grid.points.length;

      if (PHASE2.cache.has(key)) {
        PHASE2.metrics.cacheHits += 1;
        job.status = "done";
        job.samples = 0;          // no new samples; served from cache
        job.servedFromCache = true;
        if (job.isUser) PHASE2.metrics.immediateCompleted += 1;
        else PHASE2.metrics.backgroundCompleted += 1;
        emit("job_cache_hit", { priority: job.priority, label: job.label });
        PHASE2.active = null;
        updateQueue();
        if (job.onResult) job.onResult(PHASE2.cache.get(key).result, { cached: true });
        return Promise.resolve({ cached: true });
      }

      // Budget check (only for background jobs; the user request always wins).
      if (!job.isUser) {
        const projected = PHASE2.budgetUsed + job.samplesRequested;
        if (projected > PHASE2.budget) {
          job.status = "deferred";
          job.samples = 0;
          job.deferredReason =
            `would exceed budget (` +
            `${PHASE2.budgetUsed} + ${job.samplesRequested} > ${PHASE2.budget})`;
          PHASE2.metrics.deferredForBudget += 1;
          PHASE2.active = null;
          emit("job_deferred_budget", {
            priority: job.priority,
            projected,
            budget: PHASE2.budget,
          });
          updateQueue();
          return Promise.resolve({ deferred: true });
        }
      }

      PHASE2.metrics.serverCalls += 1;
      return fetchClassification(
        PHASE2.birth,
        grid.points,
        job.conditions,
        job.applyLatCap,
        controller.signal,
      ).then((resp) => {
        // Defensive: if pause() ran between fetch start and resolve, refuse
        // to commit the cache entry. This keeps "no half-cached entries"
        // honest even if AbortController fires fractionally late.
        if (job.cancelled) {
          emit("job_dropped_after_abort", { priority: job.priority });
          return { cancelled: true };
        }
        const blocks = [];
        const masks = resp.masks;
        for (let i = 0; i < masks.length; i++) {
          if (masks[i]) blocks.push({ index: i, mask: masks[i] });
        }
        const samples = grid.points.length;
        PHASE2.cache.set(key, {
          result: { masks, blocks, properties: resp.properties, grid },
          samples,
          completedAt: now(),
          priority: job.priority,
        });
        if (!job.isUser) PHASE2.budgetUsed += samples;
        job.status = "done";
        job.samples = samples;
        job.finishedAt = now();
        if (job.isUser) PHASE2.metrics.immediateCompleted += 1;
        else PHASE2.metrics.backgroundCompleted += 1;
        emit("job_done", {
          priority: job.priority,
          samples,
          cached: false,
          cache_size: PHASE2.cache.size,
        });
        if (job.onResult) job.onResult(PHASE2.cache.get(key).result, { cached: false });
        PHASE2.active = null;
        updateQueue();
        return { ok: true };
      }).catch((err) => {
        if (err.name === "AbortError" || job.cancelled) {
          PHASE2.metrics.abortsObserved += 1;
          job.status = "cancelled";
          emit("job_aborted", { priority: job.priority });
        } else {
          job.status = "error";
          job.error = err.message;
          emit("job_error", { priority: job.priority, error: err.message });
        }
        PHASE2.active = null;
        updateQueue();
        return { aborted: true };
      });
    }

    const scheduler = {
      // The single FIFO pending queue, ordered by priority enum.
      pending: [],
      enqueue(job) {
        job.status = "pending";
        PHASE2.jobs.push(job);
        this.pending.push(job);
        emit("job_enqueue", { priority: job.priority, label: job.label });
        updateQueue();
      },
      // Called when the user makes a fresh request. Aborts in-flight bg
      // job, clears the pending queue, and runs the user request now.
      async serveUser(userJob) {
        PHASE2.pausedForUser = true;
        setStatus("user_serving");
        this._cancelAll();
        await runJob(userJob);
        PHASE2.pausedForUser = false;
        setStatus("idle");
        // Tail of the protocol: resume only after immediate render done.
        setTimeout(() => this._maybeStartNext(), idleGraceMs);
      },
      _cancelAll() {
        if (PHASE2.active && !PHASE2.active.isUser) {
          PHASE2.active.cancelled = true;
          try { PHASE2.active.controller.abort(); } catch {}
          PHASE2.active.status = "cancelled";
          emit("active_cancelled", { priority: PHASE2.active.priority });
          PHASE2.active = null;
        }
        // Drop everything still pending so we are *not* committed to old
        // background work; the new immediate render gets a clean field.
        for (const j of this.pending) {
          if (j.status === "pending") {
            j.status = "cancelled";
            emit("pending_cancelled", { priority: j.priority });
          }
        }
        this.pending = [];
        updateQueue();
      },
      _maybeStartNext() {
        if (PHASE2.active || PHASE2.pausedForUser || PHASE2.cachePaused) return;
        const next = this.pending.shift();
        if (!next) {
          setStatus("idle");
          return;
        }
        setStatus("idle_caching");
        runJob(next).finally(() => this._maybeStartNext());
      },
    };

    return {
      state: PHASE2,
      scheduler,
      emit,
      setStatus,
      cacheKey,
      runJob,
    };
  }

  global.createPhase2CacheScheduler = createPhase2CacheScheduler;
})(window);
