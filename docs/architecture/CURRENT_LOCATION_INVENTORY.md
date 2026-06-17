# Current Location Inventory
**Step CL-1 — Audit Only**
Date: 2026-06-13

---

## Q1 — Exact Schema: `current_location_history`

### Columns

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| `id` | uuid | NOT NULL | `gen_random_uuid()` | PK |
| `profile_id` | uuid | NOT NULL | — | FK → `profiles(id)` (see phase4 composite FK below) |
| `account_id` | uuid | NOT NULL | — | FK → `accounts(id)` ON DELETE CASCADE; added phase2, NOT NULL locked phase4 |
| `place_id` | uuid | NULL | — | FK → `places(id)` |
| `selected_at` | timestamptz | NOT NULL | `now()` | |
| `is_current` | boolean | NOT NULL | `false` | True for the active current location |
| `source` | text | NOT NULL | `'manual'` | `'manual'` \| future: `'gps'` |
| `notes` | text | NULL | — | |
| `created_at` | timestamptz | NOT NULL | `now()` | |

### Constraints

| Name | Definition |
|------|-----------|
| `current_location_history_profile_account_fkey` | `(profile_id, account_id)` → `profiles(id, account_id)` ON UPDATE CASCADE ON DELETE CASCADE |

Phase 4 also created trigger `trg_current_location_history_set_account` (BEFORE INSERT/UPDATE on `profile_id`) to enforce account consistency.

### Indexes

| Index | Columns |
|-------|---------|
| `idx_current_location_profile_id` | `(profile_id)` |
| `idx_current_location_history_acct` | `(account_id)` |

### RLS Policies (Phase 5)

| Operation | Policy |
|-----------|--------|
| SELECT | `account_id IN (SELECT app_account_ids())` |
| INSERT | `app_has_account_role(account_id, ['owner','admin','member','assistant'])` |
| UPDATE | same |
| DELETE | same |

---

## Q2 — Staging Row Count

**Zero rows.** `Content-Range: */0` confirmed via REST API against staging.

---

## Q3 — Is `current_location_history` Currently Read?

**Not directly.** No code queries the table.

Indirectly: `app_shell.html` reads `client.current_location_place_id` from the
view model (line 535). `local_product_store.py` reads it from the mock JSON
fixture (line 210). Neither reads from `current_location_history`.

---

## Q4 — Is `current_location_history` Currently Written?

**No.** Zero INSERT or UPDATE references to this table in any app source file
(`.js`, `.html`, `.py`). The table is fully provisioned but completely dormant.

---

## Q5 — Does Any UI Ask for Current Location?

**No.** `first_profile_intake.js` has no current location field. No form, modal,
or UI element in any file prompts the user for their current city.

---

## Q6 — Does Any UI Display Current Location?

**Yes — with placeholder data.**

`app_shell.html` displays `currentCity` in every profile card:
- Line 888: `Current city: ${r.currentCity}` (drawer compact view)
- Line 1041: same in library card

`adaptStoreToView()` derives `currentCity` from `client.current_location_place_id`:
- If a matching place is found → shows `place.display_name`
- If `current_location_place_id === null` and `record_type === "client"` → shows `"Not set"`

All real Supabase profiles currently show **"Not set"** because
`supabase_store_bridge.js` hardcodes `current_location_place_id: null` (line 213).

---

## Q7 — Does Any Code Access Browser GPS?

**No.** Zero references to `navigator.geolocation`, `getCurrentPosition`, or
`watchPosition` anywhere in the application source files.

---

## Q8 — Local Product Store Current Location Fields

The mock scaffold (`scaffold/local_product/TEMPORARY_product_store.json`) does
include `current_location_place_id` on each client record:

| Mock Client | current_location_place_id |
|-------------|--------------------------|
| `cr-anna-rivera` | `place_portland` |
| `cr-jordan-lee` | `null` |
| `cr-research-event` | `null` |

The `user_settings` object has no current location field.

---

## Q9 — How Does `app_shell.html` Represent Current City/Location?

`adaptStoreToView()` maps each store client through a view model object.
The relevant section:

```
client.current_location_place_id
  → look up in placesById (keyed by place.id)
  → if found: currentCity = place.display_name
  → if null and record_type === "client": currentCity = "Not set"
  → if null and other record_type: currentCity = "—"
```

The `currentCity` string is then rendered in the profile card. The view model
does not carry a separate `currentPlaceId` — only `currentCity` (display string)
is surfaced to the render layer. The raw `client.current_location_place_id` is
consumed and discarded during adaptation.

---

## Q10 — How Does `supabase_store_bridge.js` Handle `current_location_place_id`?

**Hard-coded `null` for every profile.** Line 213:

```javascript
current_location_place_id: null,
```

No query to `current_location_history` is made. The bridge assembles store
client objects from `profiles` + `birth_records` only. Current location is
a known gap in the bridge — acknowledged at build time by the explicit `null`.

---

## Q11 — Smallest Safe v1 Implementation

The schema is fully ready. No migrations are needed.

### Read side (bridge)

In `supabase_store_bridge.js`, after fetching `profiles`:

```
For each profile:
  SELECT place_id FROM current_location_history
  WHERE profile_id = $1 AND is_current = true
  ORDER BY selected_at DESC
  LIMIT 1
```

Use the returned `place_id` as `current_location_place_id` in the store client.
If no row exists, remain `null`.

This can be done as a single query for all profiles (batch by account_id) then
mapped by `profile_id`. Requires one additional Supabase query in the bridge.

### Write side (new UI)

A minimal "Set Current Location" overlay — can reuse the place-search component
already built in `first_profile_intake.js`:

1. User searches existing `places` table by `display_name`
2. User selects a place
3. Frontend inserts a row into `current_location_history`:
   ```
   { profile_id, account_id, place_id, is_current: true, source: "manual" }
   ```
4. Frontend updates previous `is_current = true` row to `is_current = false`
   (or a `SECURITY DEFINER` function handles the flip atomically)
5. Page reloads or `SupabaseStore` rebuilds

The simplest acceptable v1 skips the "previous row flip" and just inserts a new
`is_current = true` row. The bridge query (`ORDER BY selected_at DESC LIMIT 1`)
naturally picks the most recent regardless of other rows.

### Entry point

Add a "Set current location" button or link in the profile card (drawer, library
screen) that opens the overlay. This is one `data-action` binding in `app_shell.html`
and one new overlay file (similar to `first_profile_intake.js`).

---

## Q12 — What Should NOT Be Built Yet

| Feature | Why deferred |
|---------|-------------|
| GPS (`navigator.geolocation`) | Requires permission UI, coordinate-to-place resolution, error handling. Out of scope for v1 search-based flow. |
| Road Trip Mode | Continuous location updates via `location_events` table. Separate product feature entirely. |
| `location_events` write path | No product need yet; table exists for future use only. |
| Automatic location detection | Requires either GPS or IP geolocation; both deferred. |
| Multiple simultaneous current locations | `is_current` boolean model supports one active row per profile. Multiple current locations is a future enhancement. |
| Current location for comparison profiles | Comparison profiles not yet built. |
| Geocoder / free-text lat/lon entry | Same deferral as in first_profile_intake; `places` table search only for v1. |
| Current location for unauthenticated users | Not applicable; current location is profile-bound and RLS-protected. |

---

## Implementation Readiness Summary

| Component | Status |
|-----------|--------|
| `current_location_history` table | ✅ Exists, correct schema, RLS live |
| `places` table for search | ✅ Exists, used in first_profile_intake already |
| `supabase_store_bridge.js` gap | Identified — one query needed |
| UI write path | Does not exist — new overlay required |
| Read-to-display path in `app_shell.html` | ✅ Already wired — just needs non-null `current_location_place_id` |
| GPS | ❌ Explicitly deferred |
| `location_events` | ❌ Explicitly deferred |

**The schema does the right thing already. Only the write UI and bridge query are missing.**
