# RESULT: 04_HOUSE_SYSTEM_HONESTY

Author: Cursor (relay trial)
Task author: ChatGPT
Status: Closeout
Result: **VERIFIED**

## Objective

Remove the user-visible honesty gap around house-system settings by making the
Settings UI clearly state that only Placidus is currently active.

## Files read

- `app_shell.html` (screenSettings + save-settings handler + saveAccountSettingsPatch)
- `audits/02_settings_consumption_audit.md` (prior finding: house_system stored/displayed but never consumed; engine hardcodes Placidus)
- `audits/03_settings_truth_audit.md` (prior classification: Deferred Product Truth with active honesty gap)

## Files changed

- `app_shell.html` (only)

git diff --stat: `app_shell.html | 28 +++++------- (12 insertions, 16 deletions)`

## Exact UI change

1. **House-system control is now honest and disabled.** The `<select id="rm-settings-house">`
   was previously a live dropdown bound to the stored `house_system` value, implying
   Koch / Equal / Whole Sign would change calculations. It is now:
   - `disabled aria-disabled="true"` (non-interactive, greyed out)
   - shows `Placidus (active)` selected
   - other systems labeled `Whole Sign — coming soon`, `Equal — coming soon`,
     `Koch — coming soon` (each `disabled`)
   - accompanied by honest copy: *"Placidus only for now. Other house systems are
     planned but not yet active."*

2. **Save no longer mutates house_system.** The `save-settings` handler previously read
   `houseEl.value` and wrote `house_system` into the patch. It now omits `house_system`
   entirely and only patches `default_chart_record_id`. Because `saveAccountSettingsPatch`
   is merge-based (`Object.assign({}, raw.user_settings || {}, patch)`), any previously
   stored `house_system` value is preserved untouched.

3. **Removed now-unused locals** (`raw`, `us`, `curHouse`, `HOUSE_OPTIONS`) from
   `screenSettings()` and the `houseEl` lookup from the handler. No dangling references
   remain (verified by grep: 0 hits for each identifier).

Future house-system support is **not** removed from data structures: the field still
exists in storage and is preserved on save; only the misleading interactive UI and the
write path were neutralized.

## Validation evidence

Live render of S5 — Settings against the running app on 127.0.0.1:8004 (authenticated
session, real Supabase/RLS path), screenshot at
`validation_screenshots/04_house_system/settings_house_honest.png`:

| Check | Result |
|---|---|
| Default Chart Record selector present | PASS (2 options) |
| House-system select disabled | PASS (`disabled === true`) |
| House-system active label | PASS ("Placidus (active)") |
| Honest copy "Placidus only for now" present | PASS |
| Save button still present | PASS |
| Page errors / console errors | NONE |
| `user_settings` altered by render | NO (before == after) |

Static checks:
- `grep` for `curHouse`, `HOUSE_OPTIONS`, `houseEl`, `house_system` in `app_shell.html`: 0 matches.
- `saveAccountSettingsPatch` confirmed merge-based, preserving omitted keys.
- `git diff --stat`: only `app_shell.html` changed.

Note on validation step 4 ("Save Settings and confirm no error"): a live Save click was
intentionally **not** performed, because it would issue a Supabase write. The save path
was verified statically instead (handler intact; only `default_chart_record_id` patched;
merge preserves `house_system`). This keeps the validation non-mutating, consistent with
the requirement that `user_settings` not be altered.

## Rollback command

```
git checkout -- app_shell.html
```

## Rejected scope

- No backend / engine / schema / migration changes.
- No renderer / math / overlay changes.
- Did not wire house_system into the calculation engine (explicitly out of scope; engine
  remains Placidus-only).
- Did not remove house_system from storage/data structures.
- Did not perform a live mutating Save during validation.
- No adjacent Settings cleanup beyond removing identifiers made dead by this change.

## Remaining unknowns

- The active account currently has no `user_settings` row at `profile_id IS NULL`
  (before/after both empty), so non-mutation of an *existing* stored `house_system` was
  proven by code/merge logic rather than by a populated row. Behavior is correct either way.

VERIFIED
