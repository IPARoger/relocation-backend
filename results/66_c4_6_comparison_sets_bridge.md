# C4-6: comparison_sets Bridge Migration

## 1. Bridge Addition — Before/After

### Before (supabase_store_bridge.js)

**comparison_sets fetch (select):**
```js
var csResult = await client
  .from("comparison_sets")
  .select("id, profile_id")
  .eq("account_id", accountId)
  .is("archived_at", null);
```

**storeCompSets mapping:**
```js
var storeCompSets = compSets.map(function (cs) {
  return {
    id:                    cs.id,
    client_id:             cs.profile_id,
    place_ids:             cspBySetId[cs.id] || [],
    saved_investigation_id: null,
    notes:                 comparisonSetNoteByTargetId[cs.id] || "",
    schema_version:        1,
    updated_at:            null,
  };
});
```

### After (supabase_store_bridge.js)

**comparison_sets fetch (select):**
```js
var csResult = await client
  .from("comparison_sets")
  .select("id, profile_id, title, created_at, updated_at")
  .eq("account_id", accountId)
  .is("archived_at", null);
```

**storeCompSets mapping:**
```js
var storeCompSets = compSets.map(function (cs) {
  return {
    id:                    cs.id,
    client_id:             cs.profile_id,
    profile_id:            cs.profile_id,
    title:                 cs.title || "",
    place_ids:             cspBySetId[cs.id] || [],
    saved_investigation_id: null,
    notes:                 comparisonSetNoteByTargetId[cs.id] || "",
    schema_version:        1,
    created_at:            cs.created_at || null,
    updated_at:            cs.updated_at  || null,
  };
});
```

Notes:
- Added `title`, `created_at`, `updated_at` to select
- Added `profile_id` (alongside existing `client_id`) to store shape for A1 filter
- `client_id` preserved — `adaptStoreToView` reads `cs.client_id` and is unaffected
- Place counts available via `cs.place_ids.length` (bridge already fetches comparison_set_places)

## 2. A1 Before/After

### Before (app_shell.html hydrateChartRecordComparisonSets)

```js
const accountId = window.CurrentUser && window.CurrentUser.accountId;
try {
  const client = await window.SupabaseReady;
  if (!client) throw new Error("Supabase unavailable.");
  let q = client
    .from("comparison_sets")
    .select("id, title, created_at, updated_at")
    .eq("profile_id", chartRecordId)
    .is("archived_at", null)
    .order("updated_at", { ascending: false });
  if (accountId) q = q.eq("account_id", accountId);
  const { data: sets, error } = await q;
  if (error) throw error;
  if (!stillCurrent()) return;
  const rows = Array.isArray(sets) ? sets : [];
  if (rows.length === 0) {
    container.innerHTML = `<p class="meta">No comparison sets yet. Build a comparison from saved places.</p>`;
    return;
  }
  // Place counts (best-effort; non-fatal if it fails)
  const counts = {};
  try {
    const ids = rows.map((r) => r.id);
    const { data: cspRows } = await client
      .from("comparison_set_places")
      .select("comparison_set_id")
      .in("comparison_set_id", ids);
    (cspRows || []).forEach((r) => { counts[r.comparison_set_id] = (counts[r.comparison_set_id] || 0) + 1; });
  } catch (e) { /* counts optional */ }
  if (!stillCurrent()) return;
```

### After (app_shell.html hydrateChartRecordComparisonSets)

```js
try {
  const compSets = (window.SupabaseStore?.comparison_sets ?? []).filter(cs => cs.profile_id === chartRecordId);
  if (!stillCurrent()) return;
  const rows = compSets.slice().sort((a, b) => {
    const ta = a.updated_at || a.created_at || "";
    const tb = b.updated_at || b.created_at || "";
    return tb.localeCompare(ta);
  });
  if (rows.length === 0) {
    container.innerHTML = `<p class="meta">No comparison sets yet. Build a comparison from saved places.</p>`;
    return;
  }
  const counts = {};
  rows.forEach((cs) => { counts[cs.id] = Array.isArray(cs.place_ids) ? cs.place_ids.length : 0; });
  if (!stillCurrent()) return;
```

Notes:
- Removed 2 inline Supabase queries (comparison_sets + comparison_set_places)
- Bridge already filters archived_at at fetch time — no need to re-filter
- Place count derived from `cs.place_ids.length` (bridge has full join already)
- Downstream render (`cs.title`, `cs.updated_at`, `cs.created_at`, `counts[cs.id]`) unchanged

## 3. Decision Gate Outcome

**PASS — no hard stops triggered.**

- `adaptStoreToView` reads `cs.client_id`, `cs.place_ids`, `cs.notes`, `cs.id` — all preserved
- `profile_id` added as extra field (does not rename/remove `client_id`)
- No per-chart-record filtering requiring bridge restructure (flat store filtered by `profile_id` is sufficient)
- Bridge init flow unchanged; `comparison_sets` key shape extended, not replaced

## 4. Smoke Result

```
{"overall_pass": true, "report": "validation/reports/map_current_smoke.json", "url": "http://127.0.0.1:8004/map_CURRENT.html?..."}
```

Exit code: 0 — PASS

## 5. VERIFIED
