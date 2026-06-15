# AUDIT: 18_PROFILE_ADD_RENAME_ARCHIVE_AUDIT

Task: `18_PROFILE_ADD_RENAME_ARCHIVE_AUDIT`
Mode: read-only audit; documentation output only
Result: **VERIFIED**

## Files inspected

Allowed files only:

- `app_shell.html`
- `account_drawer.js`
- `supabase_store_bridge.js`
- `audits/05_frontend_placeholder_honesty_audit.md`

No production files were modified.

## Summary

Profile / Chart Record management is partly wired:

- Opening profiles and setting current location are visible and wired to existing shell/editor handlers.
- Adding a profile is visible in multiple places and wired only as a trigger to `window.__showFirstProfileIntake()`.
- The actual add-profile persistence cannot be verified from the allowed files because the implementation lives outside this audit scope (`first_profile_intake.js`).
- No rename profile / rename Chart Record UI was found.
- No archive/delete profile / archive/delete Chart Record UI was found.
- The bridge is read-only for profiles: it selects active, unarchived `profiles` and maps them into shell `clients` / Chart Records; it does not insert/update/archive/delete profiles.

## 1. Where can users add a profile/chart record?

Three visible entry points were found:

1. Dashboard / chart-record library panel:
   - `+ Add Profile`
   - `data-action="add-chart-record"`

2. Settings → Profile Management:
   - `+ Add Profile`
   - `data-action="pm-add-profile"`

3. Account drawer:
   - `+ Add Profile`
   - `data-action="ad-add-profile"`

Additionally, bootstrap shows the intake overlay automatically when `SupabaseStoreReady` throws `INTAKE_REQUIRED`, which happens when the Supabase bridge finds no profiles/birth records.

## 2. Is add profile actually wired?

Partly, based on allowed files.

The shell and drawer buttons are wired to show the first-profile intake overlay:

- `add-chart-record` calls `window.__showFirstProfileIntake()` if available.
- `pm-add-profile` calls `window.__showFirstProfileIntake()` if available.
- `ad-add-profile` closes the drawer, then calls `window.__showFirstProfileIntake()` if available.
- Bootstrap also calls `window.__showFirstProfileIntake()` when `INTAKE_REQUIRED` is thrown.

What is **not verified** in the allowed files:

- Whether the intake overlay actually creates a `profiles` row.
- Whether it creates the required `birth_records` row.
- Whether it refreshes the shell correctly after creation.

Those behaviors likely live in `first_profile_intake.js`, which was not in the allowed file list. So the UI trigger is wired; end-to-end add persistence is outside this audit's evidence.

## 3. Where can users rename a profile/chart record?

No profile / Chart Record rename control was found in the allowed files.

Rename controls exist only for saved explorations:

- `rename-exploration`

No `rename-profile`, `rename-chart-record`, or equivalent visible action was found.

## 4. Is rename actually wired?

No profile / Chart Record rename wiring was found in the allowed files.

The only rename wiring is saved-investigation / saved-exploration rename, not profile rename.

## 5. Where can users archive/delete a profile/chart record?

No profile / Chart Record archive/delete control was found in the allowed files.

Archive controls exist for other entities:

- Favorites (`archive-favorite`)
- Saved explorations (`archive-exploration`)
- Comparison sets (archive action inside the comparison sets module)

The Profile Management page explicitly says:

```text
Must not appear: edit form, archive, delete, notes count, saved searches count.
```

So profile archive/delete is intentionally absent from that screen.

## 6. Is archive/delete actually wired?

No profile / Chart Record archive/delete wiring was found in the allowed files.

`supabase_store_bridge.js` filters profiles with `archived_at IS NULL`, which means archived profiles can be hidden from the shell, but this bridge does not perform archive/delete writes.

## 7. Are labels consistent: Profile vs Chart Record vs Client?

Not fully.

Current visible label pattern:

- User-facing account/settings surfaces mostly say **Profile** (`Profile Management`, `+ Add Profile`, `Active profile`, `Default profile`).
- Chart surfaces say **Chart Record** (`Chart Record page`, `One Chart Record per person`, `Open Chart Record page`).
- Some educational / professional copy says **client profile**.
- Internal data/model code still uses **client** (`store.clients`, `client_id`, `clientId`, `record_type: client`).

This is understandable architecturally, but user-facing language is mixed. The highest-risk label is the Dashboard button `+ Add Profile` using action `add-chart-record`; users see Profile while the route/model says Chart Record. It is not false, but the terminology is not yet clean.

## 8. What is misleading, if anything?

Potentially misleading:

1. `+ Add Profile` appears active and implies profile creation is available. The allowed files prove only that it opens the intake overlay; they do not prove persistence. If the intake is working, the label is honest. If not, it would be misleading.
2. Mixed terminology (`Profile`, `Chart Record`, `client profile`, internal `client`) can confuse users about whether they are managing one object or several.
3. `Profile Management` has no rename/archive/delete controls. This is not misleading because the screen explicitly says edit/archive/delete must not appear; however, users may expect management to include editing later.

Not misleading:

- No visible rename/archive/delete profile buttons promise unavailable behavior.
- Archive/delete profile behavior is not falsely exposed.
- `supabase_store_bridge.js` read path honestly filters active profiles and does not pretend to write them.

## 9. Smallest safe fix or next implementation task

Smallest safe honesty fix (copy-only, if desired):

- Add a short note near `+ Add Profile`: `Opens profile intake` or `Add Profile (opens intake)`.
- Standardize user-facing terminology in one pass, probably:
  - **Profile** for the person/user-facing object.
  - **Chart Record** only where explaining that one profile has one chart record.
  - Avoid **Client** in user-facing UI unless in explicitly professional/pro copy.

Smallest next implementation audit/task:

- Audit `first_profile_intake.js` end-to-end to verify profile add persistence: `profiles` insert, `birth_records` insert, current-location behavior, reload/refresh, and error states.

Do **not** implement rename/archive/delete until product decisions are made:

- Rename affects profile display name and possibly report/client naming.
- Archive/delete affects favorites, saved investigations, comparison sets, default profile, current profile, and RLS/data ownership. It should be a separate design task, not a copy cleanup.

## Verification status

VERIFIED: within the allowed files, add-profile triggers are present and delegate to the intake overlay; rename/archive/delete profile controls are absent; profile persistence writes are not in the bridge; terminology is mixed but mostly understandable. End-to-end add persistence remains outside this audit because the intake implementation file was not allowed.

VERIFIED
