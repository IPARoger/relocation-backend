# C4-5: refreshProfile() in supabase_store_bridge.js

## 1. refreshProfile() Implementation

Added `async function refreshProfile(profileId)` to `supabase_store_bridge.js` inside
the IIFE, after `buildSupabaseStore`. Exposes as `window.refreshProfile = refreshProfile`.

The function:
- Awaits `window.CurrentUserReady` + `window.SupabaseReady` for identity/client
- Fetches one row from `profiles` (id, display_name, profile_type) filtered by profileId + accountId
- Fetches newest `birth_records` row (id, profile_id, birth_date, birth_time_mode, birth_time_start, birth_place_id, timezone_id) filtered by profile_id + account_id, ordered by created_at DESC, limit 1
- Fetches `places` row (id, display_name, latitude, longitude) if birth_place_id is set and not already in store
- Merges place → `window.SupabaseStore.places` (idempotent)
- Merges birth_profile → `window.SupabaseStore.birth_profiles` using same field mapping as init (trimTime, toConfidenceTier)
- Merges client → `window.SupabaseStore.clients` using same field mapping as init (toRecordType)
- All merges are no-ops on duplicate ids; init flow is untouched; SupabaseStore shape/keys unchanged

Location: `supabase_store_bridge.js` lines ~541–640 (between buildSupabaseStore and the init block).

## 2. A2 Before / After

### Before (app_shell.html, appendCreatedProfileToStore):

```javascript
async function appendCreatedProfileToStore(newProfileId) {
  if (!newProfileId) throw new Error("newProfileId is required.");
  const client = await window.SupabaseReady;
  const user = window.CurrentUser;
  if (!client || !user || !user.accountId) throw new Error("Session unavailable.");
  if (!storeRaw) throw new Error("Store not loaded.");
  const accountId = user.accountId;

  const prof = await client
    .from("profiles")
    .select("id, display_name, profile_type")
    .eq("id", newProfileId)
    .eq("account_id", accountId)
    .single();
  if (prof.error) throw prof.error;

  const brRes = await client
    .from("birth_records")
    .select("id, profile_id, birth_date, birth_time_mode, birth_time_start, birth_place_id, timezone_id")
    .eq("profile_id", newProfileId)
    .eq("account_id", accountId)
    .order("created_at", { ascending: false })
    .limit(1);
  if (brRes.error) throw brRes.error;
  const br = brRes.data && brRes.data[0];
  if (!br) throw new Error("New profile has no birth record.");

  storeRaw.places = storeRaw.places || [];
  if (br.birth_place_id && !storeRaw.places.some((p) => p.id === br.birth_place_id)) {
    const plRes = await client
      .from("places")
      .select("id, display_name, latitude, longitude")
      .eq("id", br.birth_place_id)
      .single();
    if (!plRes.error && plRes.data) {
      storeRaw.places.push({ id: plRes.data.id, display_name: plRes.data.display_name,
        lat: parseFloat(plRes.data.latitude), lon: parseFloat(plRes.data.longitude), schema_version: 1 });
    }
  }

  // Field mappings mirrored from supabase_store_bridge.js.
  const trimTime = (t) => (t ? String(t).slice(0, 5) : null);
  const toConfidenceTier = (mode) =>
    mode === "exact" ? "T0" : (mode === "approximate" ? "T2" : "T3");
  const toRecordType = (pt) =>
    pt === "research" ? "research" : (pt === "human" ? "self" : "client");

  storeRaw.birth_profiles = storeRaw.birth_profiles || [];
  if (!storeRaw.birth_profiles.some((b) => b.id === br.id)) {
    storeRaw.birth_profiles.push({ id: br.id, birth_date: br.birth_date,
      birth_time: br.birth_time_mode === "exact" ? trimTime(br.birth_time_start) : null,
      birth_place_id: br.birth_place_id || null, timezone_id: br.timezone_id || null,
      confidence_tier: toConfidenceTier(br.birth_time_mode), confidence_metadata: {},
      representative_time: null, schema_version: 1, updated_at: null });
  }

  storeRaw.clients = storeRaw.clients || [];
  if (!storeRaw.clients.some((c) => c.id === newProfileId)) {
    storeRaw.clients.push({ id: prof.data.id, display_name: prof.data.display_name,
      birth_profile_id: br.id, record_type: toRecordType(prof.data.profile_type),
      current_location_place_id: null, notes: "", tags: [], schema_version: 1, updated_at: null });
  }
  // ... view model rebuild
}
```

### After (app_shell.html, appendCreatedProfileToStore):

```javascript
async function appendCreatedProfileToStore(newProfileId) {
  if (!newProfileId) throw new Error("newProfileId is required.");
  if (!storeRaw) throw new Error("Store not loaded.");
  await window.refreshProfile(newProfileId);

  // Rebuild the view model from the updated store, preserving the layered
  // selection fields. (unchanged)
  const prevSelected = viewModel ? viewModel.selectedChartRecordId : null;
  ...
}
```

Removed: inline profiles/birth_records/places SELECTs, duplicate field mapping helpers,
and manual storeRaw.places/birth_profiles/clients merge blocks (53 lines → 2 lines).

## 3. Smoke Result

```
venv/bin/python scripts/smoke_map_current.py
{"overall_pass": true, "report": "validation/reports/map_current_smoke.json", ...}
exit 0
```

## 4. VERIFIED
