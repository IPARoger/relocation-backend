# CURRENT LOCATION & NATAL LOCATION — SAVED PLACES DOCTRINE

**Status:** Captured for future — documentation/planning only (no code authorized)
**Type:** Product doctrine / data-ownership note
**Date:** 2026-06-15
**Phase:** Web2 Workflow QA

---

## Purpose

This note records how **Current Location** and **Natal Location** should appear
within the Saved Places / Favorites and comparison workflows.

Both are special, system-owned locations tied to a profile. They are not
ordinary favorites. The intent is that they become reachable from the same
location surfaces a user already uses (Saved Places, Comparison, Map, Screen 4)
while remaining clearly distinct from user-saved investigation places.

This is a doctrine note only. No implementation, schema, or UI change is
authorized by this entry.

---

## Data ownership

1. **Current Location** is special profile metadata backed by
   `current_location_history` (most recent `is_current=true` row per profile,
   resolved to a `places` row via `place_id`).
2. **Natal Location** is special birth/profile metadata backed by
   `birth_records.birth_place_id` (resolved to a `places` row).
3. **Favorite places** remain user-saved investigation places backed by
   `favorite_places`.

Current Location and Natal Location must **not** be written into
`favorite_places` automatically. They are derived/system rows, surfaced into
the Saved Places UI at render time — not persisted as favorites.

---

## UI doctrine

1. In the Saved Places UI for the **active Chart Record/profile**, show
   Natal Location and Current Location as **pinned/system rows** above the
   user's favorites.
2. Pinned/system row ordering is fixed:
   1. **Natal Location** [System]
   2. **Current Location** [System]
   ----------------------------------
   3. User Favorites...
   4. User Favorites...
   5. User Favorites...

   Natal Location is first (the chart's origin), Current Location is second
   (where the profile is now), then user favorites follow. Current Location
   must not be listed first.
3. Visual badges should distinguish the three kinds of rows:
   - **Natal Location**
   - **Current Location**
   - **Favorite**
3. The pinned system rows are scoped to the active profile only. They must
   never leak across profiles (DG1's current/natal must not appear for Lisa).
4. Leave Current Location in the Saved Places / Favorites zone for now. Do not
   promote it into a separate relocated-chart-style block, to avoid confusing
   it with relocated chart pages.

---

## System location visibility (Settings)

11. Saved Places ordering (restated authoritative form):
    a. **Natal Location** [System]
    b. **Current Location** [System]
    c. **User Favorites**
12. Natal Location and Current Location are pinned into Saved Places **by
    default** for the active Chart Record/profile.
13. Users may **hide or re-enable** these system locations through **Settings**.
14. Hiding a system location removes it from the **Saved Places UI only**. It is
    a presentation/preference toggle, not a data operation.
15. Hiding does **not** delete the underlying data:
    - `birth_records.birth_place_id`
    - `current_location_history`
16. Re-enabling restores the system row to Saved Places.
17. System locations must remain **visually distinguished** from user favorites
    (system badges per the UI doctrine), whether pinned by default or restored
    after being hidden.

This visibility preference is profile/account-scoped user settings (the
existing `user_settings` surface is the natural home), not a mutation of the
natal or current-location source records.

---

## Comparison doctrine

1. Current Location and Natal Location should be **selectable** as comparison
   targets alongside saved favorite places.
2. They participate in comparison as place inputs only; they are not converted
   into `favorite_places` when selected.
3. Existing comparison doctrine is preserved: comparison edits are
   non-destructive, and building a changed comparison creates a new saved
   version rather than mutating an old one.
4. Do **not** add a dedicated natal/current two-chart comparison directly onto
   the Chart Record page. Comparison remains on the Comparison surface.

---

## Map doctrine

1. Current Location and Natal Location should be selectable for **map
   centering** for the active profile, reusing the existing saved-place
   center/open behavior.
2. Selecting them centers the map only. It must not change Genie/search
   variables or overlays, and must not persist viewport.
3. They should be scoped to the active profile, like Saved Places.

---

## Screen 4 doctrine

1. Current Location and Natal Location should be selectable as destinations for
   the **Screen 4 relocated chart view**, using the same
   `chartRecordId + placeId` contract already used for favorites.
2. No new chart-wheel or renderer work is implied; Screen 4 continues to show
   the existing relocated-facts table for the chosen place.

---

## Explicit rejected approaches

- **Do not** store Current Location or Natal Location as normal
  `favorite_places` rows automatically.
- **Do not** add a natal/current two-chart comparison block directly onto the
  Chart Record page.
- **Do not** create a prominent current-location chart block on the profile
  page yet.
- **Do not** move Current Location out of the Saved Places / Favorites zone yet
  (avoid implying it is its own relocated chart page).
- **Do not** couple Current Location and Favorites (no automatic
  "save current as favorite" or "set favorite as current" without an explicit
  future user action).

---

## Future implementation sequence

(Indicative ordering only — each step is a separate, explicitly authorized
task. Nothing here is authorized now.)

1. Surface Natal Location and Current Location as pinned/system rows in the
   Saved Places UI for the active profile, with distinguishing badges
   (read-only display first).
2. Make those pinned rows openable on the Map (center-only), reusing existing
   saved-place center behavior.
3. Make those pinned rows selectable for the Screen 4 relocated chart view via
   the existing `chartRecordId + placeId` contract.
4. Allow those pinned rows to be selected as comparison targets on the
   Comparison page, preserving non-destructive versioning.
5. Only later, and only if explicitly requested, consider explicit user actions
   to convert between Current Location / Natal Location and Favorites.

---

## Scope / Constraints

- This note records doctrine and sequence only.
- No code changes authorized by this entry.
- No schema changes authorized by this entry.
- Not part of any active implementation task.

## Acceptance / Next Step

- Awaiting explicit operator direction before any Saved Places / pinned-location
  implementation work.
