# AUDIT: 19_FIRST_PROFILE_INTAKE_AUDIT

Task: `19_FIRST_PROFILE_INTAKE_AUDIT`
Mode: read-only audit; documentation output only
Result: **VERIFIED**

## Files inspected

Allowed files only:

- `first_profile_intake.js`
- `app_shell.html`
- `account_drawer.js`
- `supabase_store_bridge.js`
- `results/18_profile_add_rename_archive_audit.md`

No production files were modified.

## 1. What does `first_profile_intake.js` render?

It renders a modal/overlay with id `rm-first-profile-intake` and a card titled:

```text
Set up your first chart
```

Subtitle:

```text
Enter your birth details to begin exploring your relocation astrology.
```

It exposes `window.__showFirstProfileIntake = showOverlay`, which is called by:

- app shell Dashboard `+ Add Profile` (`add-chart-record`)
- app shell Profile Management `+ Add Profile` (`pm-add-profile`)
- Account Drawer `+ Add Profile` (`ad-add-profile`)
- app shell bootstrap when `INTAKE_REQUIRED`
- the intake script itself when `SupabaseStoreReady` rejects with `Intake overlay required`

## 2. What fields does it collect?

Collected fields:

- Display name (`rm-intake-name`)
- Birth date (`rm-intake-date`)
- Birth time mode: `Exact` or `Unknown`
- Birth time (`rm-intake-time`) only when mode is exact
- Birth city, selected from existing `places` table search results

The birth city search queries Supabase `places` and selects:

- `id`
- `display_name`
- `timezone_id`
- `admin1`
- `country_code`

Selected place is stored client-side as `state.selectedPlace`.

## 3. Does it write to Supabase?

Yes.

On submit, it waits for `window.SupabaseReady`, then performs Supabase writes.

## 4. Which tables does it insert/update?

It inserts into:

1. `profiles`
2. `birth_records`

It can delete from:

- `profiles`, as best-effort compensation if the `birth_records` insert fails after the profile was created.

No update/upsert was found. No write to `current_locations`, `favorite_places`, `comparison_sets`, `user_settings`, or `places` was found.

## 5. Does it create profile, birth record, place/current location rows?

- **Profile row:** Yes. Inserts into `profiles`.
- **Birth record row:** Yes. Inserts into `birth_records`.
- **Place row:** No. It searches/selects an existing `places` row; it does not create a place.
- **Current location row:** No. It does not create or set current location. The bridge later maps `current_location_place_id` from separate current-location data when present, but intake does not set it.

This is honest for first chart setup, but it means Add Profile does not fully create a current-location-ready profile.

## 6. Does it set `account_id` correctly?

Yes, based on allowed-file evidence.

It reads:

```text
var currentUser = window.CurrentUser;
var accountId = currentUser.accountId;
var userId = currentUser.userId;
```

Then writes:

- `profiles.account_id = accountId`
- `profiles.account_user_id = userId` (commented as legacy / schema-required)
- `birth_records.account_id = accountId`
- `birth_records.profile_id = profileId`

It also validates that `currentUser.accountId` exists before writing.

Risk: it does not explicitly verify `currentUser.userId` before writing `account_user_id`; the file comment says this is currently NOT NULL and legacy. If `userId` is missing while `accountId` exists, profile insert may fail. That is surfaced as an error.

## 7. Does it reload/refresh `app_shell` state after save?

Not directly.

On success, it redirects to:

```text
/map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=...&chartRecordId=<profileId>
```

So it does not refresh/re-render app shell in place. It sends the user to the production map with the new profile id in the handoff URL. That is a valid post-create transition, but not an app-shell state refresh.

If the user later returns to the shell, the Supabase bridge should reload profiles from the database.

## 8. Is the Add Profile label honest?

Mostly yes.

The label is honest because the flow creates:

- a `profiles` row
- a `birth_records` row

Those are exactly what the shell adapts into a Profile / Chart Record.

Caveat: the overlay itself says `Set up your first chart`, even when called from `+ Add Profile` after profiles may already exist. The same overlay/function is reused for first profile and additional profile creation. This is somewhat stale/first-only wording, but the underlying add action is real.

## 9. What is missing or risky?

Missing / risky items:

1. **No current location setup.** Intake creates birth profile data but does not create/set current location. Users must use Set Current Location later.
2. **No new place creation.** Birth city must already exist in `places`; if missing, no custom city creation path is present here.
3. **Not transactional.** Profile insert and birth record insert are two separate writes. There is a best-effort compensating delete of the profile if birth record insert fails, but it is not atomic.
4. **Potential orphan profile.** If birth record insert fails and compensating profile delete also fails, the user is shown an orphan profile id for manual cleanup.
5. **Overlay copy says first chart.** Reusing first-profile wording for later add-profile actions may confuse users.
6. **No app-shell in-place refresh.** Success redirects to map rather than refreshing the Profile Management list.
7. **No rename/archive/delete coverage.** As found in task 18, add exists but profile management lifecycle remains incomplete.

## 10. Smallest safe fix if needed?

Smallest copy-only fix:

- Change overlay title from `Set up your first chart` to `Add a profile / chart` or `Create profile and chart record`.
- Adjust subtitle to mention it creates a profile and birth record, not current location.
- Optionally add helper text near birth city: `Birth city must be selected from available places.`

Smallest implementation hardening task (separate):

- Add clearer success behavior for returning to app shell/Profile Management, or add a post-create note that current location is set separately.

Do not broaden into rename/archive/delete here; those remain separate product/data-lifecycle tasks.

## Verification status

VERIFIED: `first_profile_intake.js` renders a real intake overlay, collects display name/birth data/birth city, writes `profiles` and `birth_records` with `account_id`, redirects to the production map after save, and does not create current-location rows or place rows. Add Profile is functionally real, with minor copy risk from "first chart" wording.

VERIFIED
