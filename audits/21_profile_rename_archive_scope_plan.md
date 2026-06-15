# PLAN: 21_PROFILE_RENAME_ARCHIVE_SCOPE_PLAN

Task: `21_PROFILE_RENAME_ARCHIVE_SCOPE_PLAN`
Mode: read-only planning; documentation output only
Result: **VERIFIED**

## Files inspected

Allowed files only:

- `app_shell.html`
- `account_drawer.js`
- `supabase_store_bridge.js`
- `first_profile_intake.js`
- `main_centerline_FIXER.py`
- `repositories/profiles_repository.py`
- `results/18_profile_add_rename_archive_audit.md`
- `results/19_first_profile_intake_audit.md`
- `results/20_first_profile_intake_copy_fix.md`

No production files were modified.

## Executive summary

Basic backend/repository support already exists for profile rename and archive:

- Rename: `PATCH /profiles/{profile_id}` -> `update_profile(...)` -> updates `profiles.display_name` and/or `profile_type`.
- Archive: `POST /profiles/{profile_id}/archive` -> `archive_profile(...)` -> sets `profiles.archived_at` and `updated_at`.

However, the current app shell does **not** expose Profile / Chart Record rename or archive controls. The shell currently manages profiles mostly through Supabase-client reads/writes and helper overlays, not through the backend profile routes. Rename/archive should be implemented cautiously as a small UI + data write pass, with archive gated by default-profile handling and minimum-profile guardrails.

## 1. Current backend/repository support for profile rename

### Repository

`repositories/profiles_repository.py` has:

```python
def update_profile(profile_id: str, display_name: str = None, profile_type: str = None):
    payload = {"updated_at": _utc_now_iso()}
    if display_name is not None:
        payload["display_name"] = display_name
    if profile_type is not None:
        payload["profile_type"] = profile_type
    result = client.table("profiles").update(payload).eq("id", profile_id).execute()
    return result.data[0] if result.data else None
```

### Backend route

`main_centerline_FIXER.py` has:

```python
@app.patch("/profiles/{profile_id}")
def api_update_profile(profile_id: str, body: ProfileUpdate):
    ...
    return update_profile(profile_id, display_name=body.display_name, profile_type=body.profile_type)
```

So backend/repository rename support exists for `display_name`.

### Caveats

- `get_profile()` / `update_profile()` use service-role repository access, not the RLS-scoped JWT path.
- The route does not inspect the caller's Authorization header or account ownership.
- The route verifies existence only, not account ownership.
- The frontend shell currently does not call this route for profile rename.

For MVP, prefer a frontend Supabase RLS-scoped direct update (`profiles.update({display_name}).eq('id', profileId).eq('account_id', accountId)`) unless/until backend ownership checks are tightened.

## 2. Current backend/repository support for profile archive

### Repository

`repositories/profiles_repository.py` has:

```python
def archive_profile(profile_id: str):
    payload = {
        "archived_at": _utc_now_iso(),
        "updated_at": _utc_now_iso(),
    }
    result = client.table("profiles").update(payload).eq("id", profile_id).execute()
    return result.data[0] if result.data else None
```

### Backend route

`main_centerline_FIXER.py` has:

```python
@app.post("/profiles/{profile_id}/archive")
def api_archive_profile(profile_id: str):
    ...
    return archive_profile(profile_id)
```

So backend/repository archive support exists as a soft archive (`archived_at`).

### Existing read behavior

`supabase_store_bridge.js` already filters profiles:

```js
.from("profiles")
.select("id, display_name, profile_type")
.eq("account_id", accountId)
.is("archived_at", null)
```

Archived profiles are therefore hidden from shell store loading.

### Caveats

- Same backend ownership/auth caveat as rename.
- Archiving the only active profile makes `profiles.length === 0`, which triggers the first-profile intake overlay path.
- Archiving a profile that is the stored default requires clearing/replacing account-level `default_chart_record_id`.

## 3. Frontend surfaces that should expose rename/archive

Recommended MVP surfaces:

1. **Profile Management cards (`screenProfileList`)**
   - Primary place for both Rename and Archive.
   - It already lists each profile/chart record, favorites count, comparison count, default star, and actions (`Open`, `Set Current Location`).
   - Add small secondary buttons: `Rename` and `Archive`.

2. **Account Drawer profile rows**
   - Optional for MVP.
   - Good for setting default and maybe later quick rename, but crowded for archive.
   - Do not put destructive/archive action here in MVP unless there is a clear confirmation UI.

3. **Chart Record page**
   - Optional later.
   - A `Rename profile` action here is natural because the page is the profile's detail surface.
   - Archive from here is more dangerous; keep in Profile Management first.

Recommended first implementation: Profile Management only.

## 4. What must happen if the default profile is archived?

Required behavior:

1. **Do not leave `default_chart_record_id` pointing at an archived profile.**
2. Pick a replacement default from the remaining active profiles.
3. Update account-level `user_settings.settings_json.default_chart_record_id` to the replacement.
4. Update local persisted chart selection (`rm_active_chart_record_<userId>`) if it points to the archived profile.
5. If the archived profile is the current `navContext.chartRecordId`, navigate to the replacement profile's Chart Record page or Dashboard after reload.
6. If no other active profiles remain, block archive for MVP and tell the user to create another profile first.

Existing bridge fallback:

- If saved default is invalid/archived, `supabase_store_bridge.js` chooses `storeClients[0].id` as `defaultChartRecordId`.

But fallback alone is not enough. It prevents crashing but leaves stored settings stale. Archive implementation should proactively patch settings.

## 5. Child objects that must remain preserved

Profile archive should be a **soft hide of the parent profile**, not a cascade delete.

Preserve all child/history objects:

- `birth_records`
- `favorite_places`
- `saved_searches` / saved investigations
- `comparison_sets`
- `comparison_set_places`
- `current_location_history`
- `visited_places`
- `notes`
- `share_links`
- profile-scoped `user_settings` rows if any
- any future profile-linked artifacts

Why preserve:

- Archive is reversible in data terms even if unarchive UI is not built yet.
- Favorites/saved searches/comparisons are user work product.
- The bridge already hides child objects indirectly because archived profiles are not in active `storeClients`, but the data should remain for possible restore/admin recovery.

## 6. Explicitly reject for MVP

Reject for MVP:

- Hard delete profile.
- Cascade delete child objects.
- Unarchive/restore UI.
- Bulk archive/delete.
- Archive from Account Drawer.
- Archive the last active profile.
- Rename birth-record facts as part of profile rename.
- Edit birth date/time/place in this task.
- Multi-profile merge/split.
- Profile type mutation unless there is a product reason.
- Backend route exposure without ownership/auth hardening.

## 7. Smallest safe implementation sequence

### Phase A — Rename only (lowest risk)

1. Add `Rename` button to Profile Management cards only.
2. On click, prompt for a trimmed display name.
3. Validate non-empty and changed.
4. Use existing Supabase client in `app_shell.html` to update:
   - table: `profiles`
   - fields: `{ display_name: nextName, updated_at: new Date().toISOString() }`
   - filters: `.eq('id', profileId).eq('account_id', accountId)`
5. Reload app shell after success.
6. Write result with proof that favorites/saved investigations/comparisons are untouched.

Rationale: copy/display name only, no default-profile consequences.

### Phase B — Archive with guardrails

1. Add `Archive` button to Profile Management cards only.
2. Disable/hide Archive if there is only one active profile, or show a confirmation explaining another profile is required first.
3. Confirm with explicit wording: archive hides the profile but preserves saved places, saved investigations, comparisons, and history.
4. Compute remaining active profiles before update.
5. If archiving current/default profile, choose replacement default from remaining active profiles (prefer first remaining active profile in current order).
6. Update `profiles.archived_at` and `updated_at` for the target profile via Supabase RLS-scoped client with both `id` and `account_id` filters.
7. If needed, patch account-level settings with replacement `default_chart_record_id` using existing `saveAccountSettingsPatch(...)`.
8. If local persisted active profile points to archived profile, update it to replacement via existing `savePersistedChartRecord(...)`.
9. Reload app shell after success.
10. Verify bridge hides archived profile and children remain in DB.

### Phase C — Backend hardening later

If the backend profile routes are used instead of direct Supabase client writes, first add/authenticate ownership checks:

- Require Bearer token or session identity.
- Ensure `profile.account_id` belongs to the caller.
- Avoid service-role updates for arbitrary profile ids without authorization.

## Verification status

VERIFIED: backend/repository support for profile rename/archive exists; frontend exposure does not yet exist; bridge already hides archived profiles and falls back on invalid default, but implementation must explicitly replace stale defaults and preserve child objects.

VERIFIED
