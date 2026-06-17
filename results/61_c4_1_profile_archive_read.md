# RESULT: 61_c4_1_profile_archive_read

**Roadmap ID:** C4-1
**Author:** Cursor (manual copy-paste track)
**Date:** 2026-06-17 UTC

## Lines changed

**None.** No code change made.

## Store availability confirmation

**NOT CONFIRMED safe to use.** Investigation:

- `window.SupabaseStore` key for profiles is **`clients`** (not `profiles`) — `store.clients[]` has `id` + `display_name` for active non-archived profiles.
- However, `planProfileArchive` is called from an event handler that awaits only `window.SupabaseReady`, not `window.SupabaseStoreReady`. At the time of the archive action, `window.SupabaseStore` may not yet be populated (bridge load is asynchronous and can fail independently).
- The inline SELECT is also a **safety check** — it reads the freshest state at the moment of archive to avoid a race where a profile was archived from another tab. Using a stale cache here risks silently allowing an invalid archive.

## Recommendation

C4-1 as specified (drop the query, use cached `profiles`) is **not safe without also awaiting `SupabaseStoreReady`** at the call site. Two safe options:

1. **Minimal fix:** At call site (~line 2857), `await window.SupabaseStoreReady` before calling `planProfileArchive`, then use `window.SupabaseStore.clients`. Requires modifying the call site in addition to the function.
2. **Keep current behavior:** Live query is correct here — archive planning is a destructive pre-check; freshness matters. Skip C4-1 and move to C4-2 (no-brainer backend route substitutions with zero risk).

## Smoke result

Not run — no code change made.

## Status

**NOT VERIFIED** — Hard stop triggered: store availability at call site not confirmed without additional call-site change not in task scope.

Recommended action: skip C4-1 or expand scope to include call-site `SupabaseStoreReady` await. Proceed to **C4-2**.
