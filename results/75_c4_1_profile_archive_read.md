# RESULT: 75_c4_1_profile_archive_read

**Roadmap ID:** C4-1
**Date:** 2026-06-18

## Files Changed

| File | Change |
|------|--------|
| `app_shell.html` | `pm-archive-profile`: `await window.SupabaseStoreReady` before plan; `planProfileArchive()` reads `window.SupabaseStore.clients` instead of direct Supabase `profiles` SELECT |

## Caller Audit

| Caller | Location | Notes |
|--------|----------|-------|
| `pm-archive-profile` click handler | ~line 2758 | Sole production caller; now awaits `SupabaseStoreReady` then calls `planProfileArchive(profileId)` |

No other references to `planProfileArchive` in the codebase.

## Before / After Read Path

**Before:**
```javascript
async function planProfileArchive(profileId) {
  const client = await window.SupabaseReady;
  let q = client.from("profiles").select("id, display_name")
    .is("archived_at", null).order("created_at", { ascending: true });
  // ... account_id filter, await q
}
```

**After:**
```javascript
// Call site:
await window.SupabaseStoreReady;
const plan = await planProfileArchive(profileId);

// Function:
async function planProfileArchive(profileId) {
  const store = window.SupabaseStore;
  const active = store.clients.map((c) => ({
    id: c.id,
    display_name: c.display_name,
  }));
  // ... same blocked/remaining/replacement logic unchanged
}
```

**Safety note:** `store.clients` is populated by `supabase_store_bridge.js` from the same `profiles` query (created_at asc, archived_at null, account-scoped). Bridge filters to profiles with birth records — identical to `chartRecords` shown in UI. Archive planning therefore matches visible profile set.

## Validation

| Check | Result |
|-------|--------|
| `smoke_profile_rename_archive.py` | exit **0** — 10/10 PASS (rename, archive, only-profile 422, default repoint, no reload, no console errors) |
| `rg 'from\("profiles"\)' app_shell.html` | **0 matches** |

## Remaining Supabase Reads

| File | Match | Classification |
|------|-------|----------------|
| `app_shell.html` | none | C4-1 path fully retired |

(Other files may still read `profiles` via bridge or backend — out of C4-1 scope.)

## C4-1 Verdict

**VERIFIED**
