# Phase 2.4 — Sampling / Cache Contract Scaffold

## Purpose

Phase 2.4 defines a pure sampling/cache contract scaffold. It does not wire caching into `map_CURRENT.html`, does not change renderer behavior, and does not introduce permanent storage.

The contract exists so future truth-grid, screen-space adaptive, aura, raindrop, virga, and saved-investigation flows can agree on what makes two sampling requests semantically equivalent.

This checkpoint canonizes only the narrow `sampling_cache_contract.js` helper and its dedicated smoke. Broader substrate files such as `substrate_adapter.js` and `scripts/smoke_substrate_adapter.py` remain uncommitted archaeology/prototype scaffold unless promoted by a separate review.

## Contract Shape

The semantic cache payload is versioned and contains:

- `schema_version`
- `chart_key`
- normalized semantic investigation intent
- viewport bounds and zoom
- screen sampling scope

The adapter exposes:

- `normalizeInvestigationIntent`
- `createSamplingScope`
- `createCacheKeyPayload`
- `createSemanticCacheKey`

The helpers are exposed under `window.RelocationSamplingCacheContract`.

## Included Fields

The cache key includes only fields that affect the sampled truth request:

- chart key,
- planet-in-house conditions,
- angle-in-sign conditions,
- aspect-to-angle intent,
- viewport `north`, `south`, `east`, `west`, and `zoom`,
- sampling `width`, `height`, `block_px`, and `lat_cap`.

Condition labels and casing are normalized. Angles normalize descendant labels to `DC`. Object key order does not affect the stable JSON representation or derived cache key.

## Explicitly Excluded Fields

The contract intentionally excludes:

- `generation_mode`,
- renderer substrate,
- debug flags,
- temporary aura/raster/adaptive flags,
- rendered graphics,
- GeoJSON,
- canvas pixels,
- cache hit/miss counters,
- request IDs,
- saved-view IDs.

Saved views and saved investigations may point to what a user meant, but they do not define renderer internals.

## Scaffold Status

This is local/in-memory scaffold infrastructure only. It does not create a database, account storage, cross-session cache, or production cache invalidation policy.

## Renderer Behavior

No production renderer behavior changes. The current runtime remains `legacy_search_regions`, and the current transitional overlay output remains the existing truth-grid/search-regions path.

Point-level relocated chart calculation remains the truth source. Pixel/subpixel sampling is a rendering/sampling strategy over that truth. Future aura, raindrop, and virga outputs must derive from sampled truth or orb distance, not visual blur or fudge.

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_phase2_4_cache_contract.py
```

The smoke verifies:

- equivalent semantic requests produce the same key,
- different chart changes the key,
- different condition changes the key,
- different viewport changes the key,
- different screen sampling changes the key,
- different lat-cap policy changes the key,
- renderer/debug/aura/transient fields do not affect the key.

## Rollback Scope

Rollback is limited to:

- `sampling_cache_contract.js`,
- `scripts/smoke_phase2_4_cache_contract.py`,
- this narrative.

No map rendering, backend astrology math, account/library backend, visual UI, aura engine, truth-grid engine, or cache scheduler file is involved.

## Governance Closeout

- **Trust risk addressed:** cache semantics are anchored to user intent and sampling scope instead of renderer artifacts.
- **Deferred excellence:** persistent cache storage, invalidation, account-scoped cache ownership, and production scheduler wiring remain future work.
- **Rejected scope:** keying off saved graphics, debug flags, renderer internals, or visual effect flags.
- **Next recommendation:** keep cache scheduler wiring separate until a named performance/trust blocker requires it.
