# C5-3 — Remove Dead Bridge Helpers
**Roadmap ID:** C5-3  
**Date:** 2026-06-18  
**Result:** NOT VERIFIED — all three helpers SKIPPED (live callers found)

---

## 1. Caller Check Output

```
grep -rn "toConfidenceTier\|toRecordType\|trimTime" --include="*.js" --include="*.html" --exclude-dir=node_modules --exclude-dir=.git .
```

All matches are internal to `supabase_store_bridge.js` only — no external HTML/JS callers:

```
./supabase_store_bridge.js:29:  function toConfidenceTier(mode) {
./supabase_store_bridge.js:36:  function toRecordType(profile_type) {
./supabase_store_bridge.js:43:  function trimTime(pgTime) {
./supabase_store_bridge.js:395:        birth_time:          br.birth_time_mode === "exact" ? trimTime(br.birth_time_start) : null,
./supabase_store_bridge.js:398:        confidence_tier:     toConfidenceTier(br.birth_time_mode),
./supabase_store_bridge.js:413:        record_type:               toRecordType(profile.profile_type),
./supabase_store_bridge.js:615:        birth_time:          br.birth_time_mode === "exact" ? trimTime(br.birth_time_start) : null,
./supabase_store_bridge.js:618:        confidence_tier:     toConfidenceTier(br.birth_time_mode),
./supabase_store_bridge.js:633:        record_type:               toRecordType(profile.profile_type),
```

---

## 2. Internal Usage Analysis — HARD STOP

All three helpers are called inside **two live exported functions**:

### `buildSupabaseStore()` (lines 163–542)
- Populates `window.SupabaseStore` and `window.SupabaseStoreReady` — the primary public API of this module.
- Calls `trimTime` at line 395, `toConfidenceTier` at line 398, `toRecordType` at line 413.

### `refreshProfile()` (lines 557–644), exported as `window.refreshProfile`
- Explicitly documented: "Exposed as window.refreshProfile for use by app_shell.html after profile creation."
- Calls `trimTime` at line 615, `toConfidenceTier` at line 618, `toRecordType` at line 633.

**Per task hard-stop rule:** "If any helper is called by a live exported function → PAUSE, report, skip that helper."

All three helpers are called by live exported functions. **All three are SKIPPED.**

---

## 3. Functions Deleted or Skipped

| Helper             | Action  | Reason                                                                                    |
|--------------------|---------|-------------------------------------------------------------------------------------------|
| `toConfidenceTier` | SKIPPED | Called by `buildSupabaseStore` (→ `window.SupabaseStore`) and `window.refreshProfile`    |
| `toRecordType`     | SKIPPED | Called by `buildSupabaseStore` (→ `window.SupabaseStore`) and `window.refreshProfile`    |
| `trimTime`         | SKIPPED | Called by `buildSupabaseStore` (→ `window.SupabaseStore`) and `window.refreshProfile`    |

**No changes were made to `supabase_store_bridge.js`.**

---

## 4. Smoke Result

Not run — no changes were made.

---

## 5. Verdict

**NOT VERIFIED**

These helpers are not dead — they are actively used by the module's core exported functionality.
The premise of C5-3 ("dead private bridge helpers") is incorrect per current code state.

**Recommended remediation:**
1. Verify whether `buildSupabaseStore` and `refreshProfile` are exercised at runtime, or if they are unreachable via a different dead-code path.
2. If the parent functions are themselves dead, remove them first (separate task). That would make these helpers dead in a subsequent pass of C5-3.
3. Re-open C5-3 only after confirming the caller functions are gone or the call sites are unreachable.
