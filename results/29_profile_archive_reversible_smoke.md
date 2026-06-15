# RESULT: 29_PROFILE_ARCHIVE_REVERSIBLE_SMOKE

Task: `29_PROFILE_ARCHIVE_REVERSIBLE_SMOKE`
Mode: live staging validation (reversible, explicitly approved)
Production code: inspected only (`app_shell.html`, `supabase_store_bridge.js`); not modified
Result: **VERIFIED**

## Environment

- Used `.env.staging` only — project `rnwlrdtqhfjhpllryxiz` (per `docs/architecture/ENV_STAGING_CANON.md`).
- Did NOT use `.env`.
- Owner-authenticated, RLS-respecting client (magiclink -> session), same pattern as Task 23.
- Authenticated as `davidleongoodman@gmail.com` (uid `78980129-...`), owner of account `46b0e3f1-...`.

## Target selection

Inventory of staging:

- Only one account had >=3 active profiles: `0154e6e0-...` (4 "Eng" fixtures). It has **no `account_memberships` row**, so no auth user owns it and an RLS-respecting write is impossible there. Excluded (cannot satisfy rule 4).
- All accounts that have a real owner membership have at most 2 active profiles.

Chosen target: account `46b0e3f1-...`, profile **DG1** (`0a409b44-...`), a clearly disposable test fixture with children (favorites, saved searches, comparison set + places, birth record). Replacement: **lisa** (`307d7b44-...`).

Deviation note (honest): the "at least 3 active profiles" item in the task is a *Prefer* (soft) preference. No owner-accessible account has >=3 active profiles, and fabricating throwaway profiles would be more invasive than the reversible archive itself. A genuinely safe, fully reversible target exists (DG1), and rule 7 was honored: archiving DG1 left **lisa** active, so the last active profile was never archived. Therefore the smoke was RUN (rule 10 "no safe target" did not apply).

## Snapshots (before)

- Active profiles: `["DG1", "lisa"]`.
- `user_settings` for account: **none** (no stored `default_chart_record_id`). Effective/runtime default = first active by created_at = **DG1** -> target was the (effective) default.
- DG1 child counts: birth_records=1, favorite_places=2, saved_searches=3, comparison_sets=1, comparison_set_places=2.

## Archive (exact app query)

```
profiles.update({ archived_at: now, updated_at: now })
        .eq("id", TARGET)
        .eq("account_id", accountId)
        .is("archived_at", null)
```

- Rows affected: 1 (RLS-scoped to the owner's account).

## Verification (after archive)

- Target gone from active profiles: **true** (active = `["lisa"]`).
- Replacement computed = `lisa` (first remaining), matches expected: **true**.
- Child counts unchanged: birth_records=1, favorite_places=2, saved_searches=3, comparison_sets=1, comparison_set_places=2 — **preserved**.
- Default repaired (target was default): wrote account-level `user_settings.settings_json.default_chart_record_id = lisa`; read back = lisa — **true**.

## Restore (finally block)

- `profiles.archived_at` set back to `null` for DG1 (in `finally`).
- Default restored to original state: the smoke had created the `user_settings` row (none existed before), so restore **deleted** that row, returning the account to its original no-stored-default state.

## Post-restore verification

- Active profiles: `["DG1", "lisa"]` — target reappeared: **true**.
- DG1 child counts unchanged vs. baseline: **true** (preserved across archive AND restore).
- `user_settings`: empty again — **settings_restored: true**.
- Independent service-role re-read confirmed: DG1 `archived_at = null`, both profiles active, `user_settings` empty.

## Smoke-sequence checklist

1. Snapshot active profiles — done.
2. Snapshot default — done (none stored; effective default = DG1).
3. Snapshot target child counts (birth_records, favorite_places, saved_searches, comparison_sets, comparison_set_places) — done.
4. Archive via exact app query — done (1 row).
5. Default replacement applied (target was default) — done (-> lisa).
6. Target disappeared from active — verified.
7. Child counts unchanged — verified.
8. Default repaired — verified.
9. Restore `archived_at = null` in `finally` — done.
10. Restore default — done (removed the created settings row, original state).
11. Profile reappears — verified.

## Conclusion

The Phase B archive logic behaves correctly on live staging under RLS: soft-archives the parent only, preserves all child rows, blocks nothing incorrectly, selects the correct replacement, repairs the (effective) default, and is fully reversible. All mutations were restored; independent re-read confirms the account is back to its exact original state.

VERIFIED
