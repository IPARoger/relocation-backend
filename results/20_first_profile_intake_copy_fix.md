# RESULT: 20_FIRST_PROFILE_INTAKE_COPY_FIX

Task: `20_FIRST_PROFILE_INTAKE_COPY_FIX`
Mode: copy honesty only (implementation)
Result: **VERIFIED**

## Telegram notifications

- Sent `started` exactly once (`sent: started`).
- Closeout: exactly one `verified`.
- No task content, code, or paths transmitted.

## Source evidence

- `audits/19_first_profile_intake_audit.md`
- `results/19_first_profile_intake_audit.md`

## Changes made (only `first_profile_intake.js`, overlay copy)

- Title: `Set up your first chart` -> `Create profile and chart record`.
- Subtitle: `Enter your birth details to begin exploring your relocation astrology.` -> `Enter birth details to create a profile and its chart record. Current location is set separately, later.`
- Added a short helper under the birth-city field: `Select a birth city from the available list.`

## Required changes mapped

1. **Do not change persistence behavior** — Honored. No submit/insert logic touched.
2. **Do not change Supabase writes** — Honored. `profiles` insert, `birth_records` insert, and compensating `profiles` delete are unchanged.
3. **Do not add current-location logic** — Honored. Only a copy note that current location is set separately.
4. **Retitle from first-chart language** — Done -> `Create profile and chart record`.
5. **Clarify birth city must be selected from available places** — Done via the helper line.
6. **Clarify current location is set separately later** — Done in the subtitle.
7. **Keep copy short** — Done.

## Validation evidence

- **`first chart` no longer user-visible:** search for `first chart` in `first_profile_intake.js` returns nothing.
- **Profile + birth_records insert logic unchanged:** `client.from("profiles").insert(...)`, `client.from("birth_records").insert(...)`, `account_id`/`profile_id` fields, and the compensating `client.from("profiles").delete()` are all intact.
- **No Supabase/table/write logic changed:** isolated diff (pre-edit backup vs current) shows only three copy lines changed/added in the overlay `innerHTML`.
- **Only `first_profile_intake.js` changed by this task:** `git diff --stat` for `app_shell.html`, `account_drawer.js`, and `supabase_store_bridge.js` is empty (those carry only pre-existing/no changes from this task).

## Rejected scope

- No persistence/write/logic change.
- No current-location implementation.
- No edits beyond `first_profile_intake.js` and this results file.

## Rollback

```
git checkout -- first_profile_intake.js results/20_first_profile_intake_copy_fix.md
```

VERIFIED
