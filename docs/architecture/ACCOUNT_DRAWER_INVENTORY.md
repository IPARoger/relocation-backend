# Account Drawer Inventory
**Step: AD-1**
**Date: 2026-06-13**
**Status: Inventory only — no implementation**

---

## 1. Recommended Launch Point

**Header right-rail button in `app_shell.html`.**

The current app header is:
```html
<header class="app-header">
  <h1>Relocation App</h1>
  <span class="tag">Chart Record doctrine · placeholders only</span>
  <nav class="primary-nav" id="primaryNav"></nav>
  <span class="screen-meta" id="screenMeta">Screen 0</span>
</header>
```

The `screen-meta` span sits at `margin-left: auto`, which pushes it to the far right of the header flex row. The cleanest insertion point is **a new account button placed between `#primaryNav` and `#screenMeta`** — or replacing/supplementing `#screenMeta`. This is the universal SaaS pattern: persistent, top-right, one tap from anywhere in the app.

The button should show `CurrentUser.accountName` (or initials fallback) and dispatch a `data-action="open-account-drawer"` event. The account drawer IIFE (new file) opens a slide-in or modal panel.

**Why not a nav route?**
`settings` already exists as a `data-nav` route (Screen S5). The account drawer is a _persistent overlay_ — not a screen. It should not break the current nav-context model. It is dismissible without navigation.

**Why not a footer link?**
The footer already hosts "Future rooms — quarantined." Logout/account at the footer is poor UX and easily missed.

---

## 2. What Drawer Systems Already Exist

### 2a. Modal backdrop (app_shell.html)
A reusable `<div class="modal-backdrop" id="popupModal">` already exists:
- CSS: `display:none; position:fixed; inset:0; background:rgba(0,0,0,.35); z-index:100; align-items:center; justify-content:center`
- Toggle: `.open` class → `display:flex`
- Pattern: `openPopup()` / `closePopup()` via `data-action`
- Backdrop click dismisses
- Used for Screen 3 map popup today

This is the **reusable pattern** for the account drawer. A second `<div class="modal-backdrop" id="accountDrawer">` can be added alongside the existing one, using the identical CSS class and open/close mechanism.

### 2b. Genie drawer placeholder (app_shell.html — Screen 2)
A `.drawer-placeholder` div hosts the Genie variable builder on the Map screen. This is a content slot, not a structural drawer. The Genie panel mounts into `#genieDrawerMount` via `RelocationGenieVariableBuilder.mount()`.

**Not reusable** for the account drawer — it's Genie-specific and map-scoped.

### 2c. Map onboarding card (map_CURRENT.html)
A floating `<div id="mapOnboarding" class="map-onboarding">` card appears on first map load. Dismissed via sessionStorage. Has a `[data-dismiss-onboarding]` button.

**Not a general drawer.** But the sessionStorage dismiss pattern is worth reusing for tutorial progress.

---

## 3. Can an Existing Drawer Framework Be Reused?

**Yes, partially.** The `modal-backdrop` + `.modal` pattern in `app_shell.html` is directly reusable:

```css
/* Already in app_shell.html — no CSS changes needed */
.modal-backdrop { display:none; position:fixed; inset:0; background:rgba(0,0,0,.35); z-index:100; ... }
.modal-backdrop.open { display:flex; }
.modal { background:var(--panel); border-radius:8px; max-width:420px; width:100%; padding:16px; ... }
```

For a slide-in drawer (preferred over a centered modal for account management):
- Add one new CSS block to `account_drawer.js` styles injection (same IIFE pattern as `current_location_editor.js`)
- Override `.modal` to be `max-width:340px; position:fixed; top:0; right:0; height:100vh; border-radius:0; overflow-y:auto`
- Keep the `.modal-backdrop` for the scrim

This avoids touching any existing CSS and keeps the drawer self-contained in the new file.

**Pattern to follow**: `current_location_editor.js` IIFE style — self-contained, injects its own styles, exposes `window.__showAccountDrawer()`.

---

## 4. CurrentUser Fields Available Today

From `user_profile.js`, `window.CurrentUser` is:

```javascript
{
  userId:      string   // auth.users.id
  accountId:   string   // accounts.id
  accountName: string   // accounts.name
  accountType: string   // 'personal' | 'professional' | 'family' | 'organization'
  role:        string   // 'owner' | 'admin' | 'member' | 'assistant' | 'viewer'
}
```

All five fields are populated on every authenticated load. No additional queries required to display Section A (Account).

---

## 5. What user_settings Fields Currently Exist

**Database schema** (`2026_06_08_schema_v1.sql` + `2026_06_13_phase2_account_id_columns.sql`):

```sql
user_settings (
  id               uuid PRIMARY KEY,
  account_user_id  uuid NOT NULL,           -- legacy auth.users FK
  account_id       uuid → accounts(id),     -- added in phase2
  profile_id       uuid → profiles(id),     -- null = account-level row
  settings_json    jsonb NOT NULL DEFAULT {},
  created_at       timestamptz,
  updated_at       timestamptz
)
```

RLS: full CRUD for all authenticated roles (owner/admin/member/assistant).

**What `supabase_store_bridge.js` reads from `settings_json`** (the `rawSettings` object):

| Key | Default | Purpose |
|---|---|---|
| `default_chart_record_id` | `storeClients[0].id` | Which profile opens by default |
| `settings_version` | `1` | Schema version guard |
| `house_system` | `"placidus"` | Astrological house system |
| `zodiac_mode` | `"tropical"` | Sidereal vs tropical |
| `orb_defaults` | `{conjunction:8,square:6,...}` | Aspect orb widths |
| `visible_minor_aspects` | `false` | Minor aspect display toggle |
| `helper_layers` | `{}` | Map layer visibility |
| `ontology_pack_id` | `null` | Condition ontology pack |

These are the **fields the bridge already reads**. None are currently writable from the UI.

---

## 6. What Settings Are Already Implemented

| Setting | Status |
|---|---|
| `default_chart_record_id` | **Read-only display** in `screenSettings()` — select disabled |
| `house_system` | **Read-only display** in `screenSettings()` — select disabled |
| Profile switching via localStorage | **Working** — `switchChartRecord()` + `_savePersistedChartRecord()` |
| Map onboarding dismiss | **Working** — sessionStorage key `rm_map_onboarding_dismissed` |
| Current location | **Working** — CL-2/CL-3 complete |

Nothing in `user_settings` is currently writable from the frontend.

---

## 7. What Settings Are Scaffolded but Not Wired

| Setting | Where Scaffolded | Status |
|---|---|---|
| `default_chart_record_id` | `screenSettings()` — disabled `<select>` | Needs write path to `user_settings` |
| `house_system` | `screenSettings()` — disabled `<select>` | Needs write path |
| `history clear` | `screenSettings()` — disabled buttons | Placeholder only; table not defined |
| `zodiac_mode` | bridge reads it | No UI exists |
| `orb_defaults` | bridge reads it | No UI exists |
| `visible_minor_aspects` | bridge reads it | No UI exists |
| Birth data edit | `screenBirthData()` — inputs present | All inputs unconnected; no save path |

**Smallest writable setting for v1 account drawer**: `default_chart_record_id` — the select can be unlocked and the `user_settings` upsert is a single JSON field write.

---

## 8. What Help / Tutorial Infrastructure Already Exists

| Feature | File | Implementation |
|---|---|---|
| Map onboarding card | `map_CURRENT.html` | CSS + sessionStorage dismiss. One-time "right-click to open relocated chart" tip |
| `skipOnboarding` URL param | `map_CURRENT.html` | Suppresses map onboarding card when debug params are present |
| `skipOnboarding` param emission | `app_shell.html` line 767 | `buildMapHandoffUrl()` sets `params.set("skipOnboarding", "1")` |
| "Future rooms" page | `app_shell.html` | Quarantined screen — not real help content |

**Nothing else.** No help page, no tutorial system, no about page, no feedback mechanism exists. The "Learn", "Tutorials", "About Relocation Astrology", and "Feedback" sections of the proposed drawer are **all net-new**.

---

## 9. What Account-Management Features Already Exist

| Feature | Implementation |
|---|---|
| Signup / login | `auth.html` — email/password with Supabase |
| Session guard | `auth_guard.js` — redirect to `/auth.html` if no session |
| Logout | `window.logout()` in `auth_guard.js` — signOut + redirect |
| CurrentUser load | `user_profile.js` — reads accounts + memberships |
| Add Profile | `window.__showFirstProfileIntake()` — works, launched from `data-action="add-chart-record"` |
| Set Current Location | `window.__showCurrentLocationEditor(profileId)` — CL-3 complete |
| Profile selector | `chartRecordSelectHtml()` — `<select>` present on multiple screens |
| Profile persistence | localStorage key `rm_selected_chart_${userId}` |

**Not yet built:**
- Profile editing (name, birth data)
- Profile deletion
- Account name editing
- Password change (forgot-password exists in auth.html)
- Notification settings
- Data export
- Account deletion

---

## 10. Smallest Useful v1 Account Drawer

A **slide-in panel from the right**, launched by an account button in the header, implemented as a new `account_drawer.js` IIFE file.

### Minimum viable content:

**Section A — Account** (all data from `window.CurrentUser`, zero queries):
- Account name
- Account type badge
- Role badge

**Section B — Profiles** (data from `window.SupabaseStoreReady` / current view model):
- Profile list from `vm.chartRecords` (display name + current city)
- Active profile indicator
- "Add Profile" button → calls existing `window.__showFirstProfileIntake()`
- "Set Current Location" → calls existing `window.__showCurrentLocationEditor(profileId)`

**Section C — Settings** (link only):
- "Settings →" button navigates to existing `data-nav="settings"` screen (S5)
- No new settings UI in v1 drawer

**Section D — Help** (static text + external links):
- Three static text lines: what relocation astrology is, how the system works, how to read the map
- No tutorial engine required for v1
- Feedback: `mailto:` link or external form link (static)

**Section E — Logout:**
- Single button calling `window.logout()`

---

## Implementation Sequence

### AD-2: account_drawer.js

New IIFE file. Follows the `current_location_editor.js` pattern exactly.

- `window.__showAccountDrawer()` — opens the drawer
- Self-contained CSS injected at first open
- Reads `window.CurrentUser` (zero queries for Section A)
- Reads `window.SupabaseStoreReady` for profile list in Section B (already resolved by the time any user clicks the button)
- Calls existing `window.__showFirstProfileIntake()` and `window.__showCurrentLocationEditor()`
- Calls existing `window.logout()`
- Links to `data-nav="settings"` for Section C (via `window.__rmAppShell.navigate` or a `data-nav` button inside the drawer)

### AD-3: Header button injection in app_shell.html

- Add account button to header: `<button id="accountDrawerBtn" data-action="open-account-drawer">` between `#primaryNav` and `#screenMeta`
- Add `data-action="open-account-drawer"` handler calling `window.__showAccountDrawer()`
- Add `<script src="/account_drawer.js"></script>` alongside existing auth script tags

### AD-4: FastAPI route

- Add `GET /account_drawer.js` to `main_centerline_FIXER.py`

---

## Reuse Opportunities

| What | Reuse from |
|---|---|
| IIFE + style injection pattern | `current_location_editor.js` |
| Overlay/modal CSS class names | `app_shell.html` modal-backdrop |
| `data-action` dispatch | existing `attachEventListeners()` |
| Add Profile launch | `window.__showFirstProfileIntake()` |
| Set Location launch | `window.__showCurrentLocationEditor()` |
| Logout | `window.logout()` (auth_guard.js) |
| Profile list data | `window.__rmAppShell.viewModel()` |

---

## Missing Pieces for v1 Drawer

| Gap | Needed for | Difficulty |
|---|---|---|
| Account button in header HTML | Launch point | Trivial |
| `window.__showAccountDrawer()` export | Drawer open | New file |
| Profile list rendering in drawer | Section B | Simple (data already in viewModel) |
| Static help copy | Section D | Content only |
| `window.__rmAppShell.navigate()` callable from drawer | Settings link | Already exposed in `window.__rmAppShell` |

---

## Explicit Non-Goals for AD-2 through AD-4

- Profile editing
- Password change from the drawer
- Account name editing
- Multi-user account management (invitations, member list)
- Tutorial engine / step-by-step onboarding
- Settings write path (that is a separate step)
- Notes
- Export
- Account deletion
