# Web2 Onboarding and Guided Discovery

**Date:** 2026-06-13  
**Sources:** PHASE_6_CLOSEOUT.md, PROJECT_STATE_AND_NEXT_PHASE.md  
**Status:** Planning only. No implementation. No code.  
**Scope:** First-run experience from landing page through first live map.

---

## Context and Constraints

The backend is fully validated through Phase 6. The onboarding flow must route through the live Supabase schema. Every write described in this document corresponds to an existing, RLS-secured table. No new tables are required for onboarding.

**What exists and is ready:**
- `handle_new_user()` fires on signup and creates one `accounts` row and one `owner` membership automatically. The user emerges from signup already in a valid authorization state.
- `profiles` accepts one row per person per account. `display_name` is the only required user-supplied field at insert time.
- `birth_records` table exists and is linked to profiles.
- `intention_profiles` table exists and is linked to profiles.
- `current_location_history` table exists and is linked to profiles.
- `places` reference data exists (21 rows in production; GeoNames import pending before full launch).
- `favorite_places` and `comparison_sets` are write-ready under the user's session.
- `notes` and `user_settings` tables exist but have no frontend; they are available for onboarding state storage if needed.

**What does not yet exist:**
- Any frontend screen.
- Any map rendering.
- Any SMTP configuration (required for production email confirmation).
- Any city search backed by production reference data at scale.

**Onboarding must not assume:**
- The user knows what astrocartography is.
- The user has their birth time memorized to the minute.
- The user is on a desktop device.
- The user will complete the flow in one sitting.

---

## 1. First Account Creation Flow

### Entry points

Three entry points lead to the same signup form:
1. Landing page primary CTA ("Start your map").
2. Direct link shared by another user (deferred: share links are not yet wired).
3. Returning visitor who bookmarked the app before signing up.

### Signup form

Single screen. Two fields only at this stage:

- **Email address.** Standard email input. Validated client-side for format. Server-side returns a clear error if the address is already registered ("An account with this email already exists — sign in instead").
- **Password.** Minimum 8 characters. No complexity rules at v1. Show/hide toggle. No password confirmation field — confirmation adds friction and is not a meaningful security gain for this use case.

**No name field at signup.** Display name is collected in the profile creation step, where it is contextually meaningful ("What should we call this profile?"). Asking for a name on the signup form conflates the account identity with the first profile identity, which is architecturally wrong — an account can hold multiple profiles.

**Submit behavior:**
- Calls `signUp()` with email and password via the publishable key.
- On success: the `handle_new_user()` trigger fires server-side (transparent to the user). The user's session is immediately valid. No additional API call is needed to create the account.
- On production: the user receives a confirmation email before their session is issued. The screen transitions to a "Check your email" holding state with a resend link.
- On staging (for testing): email confirmation is bypassed via admin API; the session is issued immediately.

### "Check your email" holding state

Shown only when email confirmation is required (production).

- Message: "We sent a confirmation link to [email]. Click it to activate your account."
- Resend link available after 60 seconds. One resend attempt per session before showing a "contact support" path.
- The link in the email contains a Supabase magic token. Clicking it completes confirmation and redirects the user back into the app with an active session.
- On redirect: the app detects an active session and checks whether the user has any profiles. If zero profiles, it routes to the profile creation flow. If one or more profiles exist, it routes to the map.

### Sign-in (returning user)

Separate screen from signup. Fields: email and password. Link to "Forgot password?" which triggers Supabase's built-in password reset flow (requires SMTP). No new backend logic needed.

On successful sign-in: check profile count. Zero profiles → profile creation flow. One or more profiles → map.

### Error handling

| Error | Display |
|---|---|
| Email already registered | "An account with this email already exists." + "Sign in instead" link |
| Weak password | "Password must be at least 8 characters." |
| Network error | "Something went wrong. Check your connection and try again." |
| Rate limited | "Too many attempts. Try again in a few minutes." |

---

## 2. Birth Data Intake Flow

### Why birth data comes before display name

Birth data is the irreducible core of the product. Without a birth date, latitude, and time, no chart can be calculated and the map has nothing to show. Presenting birth data intake before the profile name communicates what the product fundamentally is — this is not a social profile, it is a chart.

### Step 2a — Birth date

**Single input: date picker.**
- Format: calendar or three-field input (day / month / year). Month-first (U.S.) vs. day-first (international) must adapt to locale.
- Range: 1900 to today minus 18 years (soft minimum; no hard age gate in v1).
- No validation beyond "is this a real date." Do not prompt users to reconsider their age.
- Stored as a date field (not datetime) in `birth_records`. The time is collected separately.

### Step 2b — Birth time

**Two states: known and unknown.**

This is the most consequential UX decision in the onboarding flow. Birth time affects house calculations. Many users do not know their exact birth time. Forcing a time entry for users who do not know it produces junk data that silently corrupts the chart.

**Known path:**
- Time input: hour and minute fields, with AM/PM or 24-hour format adapted to locale.
- Optional: a precision toggle — "Approximate (within an hour)" vs. "Exact." This is stored as metadata, not a separate column, and informs how the app presents the house cusps (with uncertainty indicators rather than precise degrees).

**Unknown path:**
- Radio option: "I don't know my birth time."
- Selecting this stores a null birth time and sets a `time_unknown` flag in `birth_records` (or the equivalent column if it exists).
- The app proceeds with a solar chart — full planetary positions, no house cusps, honest about what cannot be calculated without time.
- A persistent nudge appears on the map: "Add your birth time to see your full chart." This links back to profile edit.

**Why this matters for the product:** silently defaulting to noon or sunrise is an industry anti-pattern that produces authoritative-looking but fabricated house positions. The product must not do this.

### Step 2c — Birth location

**City search input.**
- Backed by the `places` table via an authenticated GET with `ilike` filtering on `display_name`.
- The user types a city name. Results appear as a list after 2+ characters.
- Selecting a city stores: `place_id` (FK to `places`) in `birth_records`, and the latitude/longitude from the `places` row is used for chart calculation.
- If the user's birth city is not in the database: a manual fallback — latitude and longitude entry fields with a helper map pin (no routing, just coordinate display). This stores `place_id = null` and raw `latitude`/`longitude` in the birth record.
- The fallback is not the default path. It is reached via "My city isn't listed."

**This is where the Places data gap matters most.** Until the GeoNames import runs, city search will return few or zero results for most users. The manual fallback must be available from day one.

### Saving birth data

All three fields (date, time/unknown flag, place) are committed as a single `birth_records` INSERT when the user taps "Continue." There is no partial save at this step.

The `birth_records` row is linked to the profile that is created in the next step. Architectural sequence: the profile row must be created before the birth record INSERT, because `birth_records` carries a composite FK to `profiles(id, account_id)`.

**Practical implementation order:**
1. Collect all birth data on screen.
2. When user submits the birth data screen: INSERT `profiles` first (with display name from step 3, or a placeholder), then INSERT `birth_records` referencing the profile.
3. Alternatively: collect birth data on screen, collect display name on the next screen, and commit both as a single backend sequence.

The simpler UX path is to collect display name after birth data but commit everything together.

---

## 3. First Profile Creation Flow

### What a profile is

A profile is one person's astrological data set within an account. The default is the account owner themselves, but a single account can hold profiles for family members, partners, or any person the user wants to chart. Onboarding creates the first profile, which is implicitly "me" unless the user states otherwise.

### Step 3a — Who is this profile for?

Two options presented immediately after birth data:

- **"This is me"** — default, selected by default. The display name defaults to the part of the email address before the `@` symbol, which the user can edit.
- **"This is someone else"** — the user enters a name for the person. No other behavior change in v1; both paths produce the same profile type (`profile_type = 'human'`).

This framing matters. It tells users the product is designed for charting multiple people from a single account — which is a differentiator and sets up the eventual multiple-profile feature without burying it.

### Step 3b — Display name

- Text input, free-form.
- Pre-filled with the email prefix if "This is me" was selected.
- Required. Minimum 1 character. Maximum 60 characters.
- This becomes the label shown on the map and in profile lists.
- Not a username. Not publicly visible in v1. It is personal data, not social identity.

### Step 3c — Current location (optional at onboarding)

- Same city search UI as birth location.
- Question: "Where do you currently live?" or "Where are you based?"
- Stores to `current_location_history` as a new row.
- Optional in onboarding. If skipped, the map opens centered on the birth location.
- A "skip for now" link is visible without scrolling.

**Why collect this:** the map's default viewport should be contextually meaningful — either the user's current location or their birth location, in that priority order. Collecting this also enables future features (commute radius, relocation delta calculations, local event overlays).

### Profile INSERT sequence

On "Create my profile" tap:
1. `profiles` INSERT: `account_id`, `account_user_id` (= `auth.uid()`), `display_name`, `profile_type = 'human'`.
2. `birth_records` INSERT referencing the profile id and account id.
3. `current_location_history` INSERT if a current location was selected (optional).

All three writes use the user's publishable-key session. No service-role involvement.

On any INSERT failure: surface a recoverable error. Do not silently discard data. If only the current location write fails, do not fail the whole onboarding — profile and birth record are the minimum viable state.

---

## 4. First Map Launch Flow

### Transition

After profile and birth data are saved, a single "View my map" CTA replaces the form. No auto-redirect. The user taps to proceed. This gives them a moment of anticipation and avoids the disorienting effect of being auto-forwarded while writes are still in flight.

The button is disabled until all required writes have confirmed (profile + birth record). A loading indicator appears on the button during write flight.

### Map initialization

The map opens with:
1. **Viewport:** centered on the user's current location if provided; otherwise centered on birth location.
2. **Initial zoom:** city level (approximately zoom 8–10), wide enough to see regional geography.
3. **First visible layer:** the astrological line layer for the user's birth chart. Which lines are shown first is a product decision that is not resolved in this document — it requires a separate chart rendering doctrine. The map must load with at least one visible, labeled line.

### Loading state

Chart calculation may take 1–3 seconds. During this time:
- The map background (basemap tiles) loads and renders immediately.
- A non-blocking indicator shows that the chart layer is computing ("Calculating your lines…").
- The user can pan and zoom while waiting.
- Lines render progressively as they become available, not as a single atomic reveal.

### First-run state detection

The app must distinguish a first-run map launch from a returning-user map launch. The simplest reliable signal: check whether the user has favorited any places or saved any comparison sets. If both counts are zero and the profile was created within the last 5 minutes, treat the session as first-run and activate the educational overlay sequence.

This avoids showing tutorial overlays to users who return after a gap, which is more annoying than helpful.

---

## 5. Educational Overlay System

### Principles

1. **Show, then explain.** The map renders first. Overlays appear after the chart lines are visible — explaining what the user is already looking at, not pre-empting it.
2. **One thing at a time.** Each overlay covers exactly one concept. No bullet lists of features.
3. **Dismissible at any point.** Every overlay has an "×" close control that dismisses the entire overlay sequence. Users who already know the product or who learn by exploration must not be trapped.
4. **Progress is saved.** If the user dismisses mid-sequence and returns, the sequence does not restart. State is stored in `user_settings`.
5. **No quiz, no blocking modal.** The overlay is a tooltip or a side panel, not a full-screen interstitial that prevents interaction. The map is always live beneath it.

### Overlay sequence

**Overlay 1 — What are these lines?**
- Trigger: first map render, after chart lines appear.
- Content: one sentence identifying what the lines represent. Example: "These lines show how the sky at your birth moment projects onto the Earth. Each line marks a place where a specific planet was rising, setting, overhead, or at its lowest point when you were born."
- Interactive: none. Tap "Next" or "×."
- Target: no specific map element; top-left panel or bottom sheet introduction.

**Overlay 2 — How to read the colors (or labels)**
- Trigger: after Overlay 1 is acknowledged.
- Content: brief legend. Each line type (e.g., Ascendant, Midheaven, Descendant, IC) has a distinct visual treatment. Explain the two or three most commonly recognized ones. Do not explain all ten planets in the first session.
- Interactive: tapping a line on the map highlights the relevant legend entry.
- Target: the legend element or a specific line on the map (highlight the Sun line if one is visible in the viewport).

**Overlay 3 — What the map is for**
- Trigger: after Overlay 2 is acknowledged.
- Content: one sentence framing the product's purpose. Example: "Use this map to explore which locations on Earth activate different areas of your life — career, relationships, health, creativity."
- Interactive: none.
- Target: general map area.

**Overlay 4 — Favorite a place**
- Trigger: after Overlay 3 is acknowledged.
- Content: "Tap any city to save it to your favorites and start building a comparison."
- Interactive: none — the tap action itself is the interaction; the overlay just directs attention.
- Target: highlight the nearest `places` result to the user's current map center (requires knowing the viewport).
- Completion: dismiss automatically when the user taps a place and the favorite write succeeds.

**Overlay 5 — Come back anytime**
- Trigger: after Overlay 4 completes (or is dismissed).
- Content: "Your chart is saved. Come back whenever you want to explore more locations."
- Interactive: single "Got it" button. Completes the overlay sequence.
- Target: no specific element; bottom sheet or centered card.

### Overlay state storage

Each overlay's completion state is stored as a row in `user_settings` at the account level (`profile_id IS NULL`):
- Key: `onboarding_overlay_sequence`
- Value (JSON): `{"last_completed": 3, "dismissed_at": null, "total_steps": 5}`

This allows the sequence to resume across devices and sessions without querying any frontend local storage.

---

## 6. Completion Criteria

Onboarding is considered complete when all of the following are true:

| # | Criterion | Backing table |
|---|---|---|
| C1 | User has a confirmed auth session | `auth.users` (email confirmed) |
| C2 | User's account and owner membership exist | `accounts`, `account_memberships` |
| C3 | At least one `profiles` row exists with `display_name` set | `profiles` |
| C4 | At least one `birth_records` row linked to the profile exists | `birth_records` |
| C5 | The map has rendered at least one astrological line layer | (client-side event; logged to `user_settings` or equivalent) |
| C6 | The overlay sequence has been started (Overlay 1 seen) | `user_settings` |

C6 requires only that the sequence was triggered, not completed. A user who dismisses all overlays immediately still counts as having completed onboarding — they saw the map, they understood enough to dismiss the guidance, and they are in a valid product state.

C4 (birth record) is the minimum for the map to show anything meaningful. If a user somehow reaches the map without C4, the map must show an empty state with a direct link back to profile editing to add birth data, not an error screen.

### Re-entry after incomplete onboarding

If a user signs up, creates a profile without birth data, and then closes the browser:

- On next sign-in: the app detects a profile exists but no birth record. It routes to the birth data entry screen with the existing profile pre-loaded — not back to step 1.
- The user does not re-enter the account creation flow. Their account and profile already exist.
- The only missing data is the birth record. Route directly to step 2b (birth date).

If a user signs up and closes the browser before creating a profile:

- On next sign-in: the app detects zero profiles. It routes to the beginning of the profile creation flow (step 2a, birth date).
- Account creation is already complete (the trigger fired at signup). Do not show the signup screen again.

---

## 7. Data Persistence Requirements

### What is written per onboarding

| Data | Table | Write timing | Required | Notes |
|---|---|---|---|---|
| Account | `accounts` | Automatic at signup (trigger) | Yes | No user action needed; never shown to user |
| Owner membership | `account_memberships` | Automatic at signup (trigger) | Yes | No user action needed |
| Profile | `profiles` | On "Create my profile" submit | Yes | `display_name`, `account_id`, `account_user_id`, `profile_type='human'` |
| Birth record | `birth_records` | On "Create my profile" submit | Yes | Date, time (nullable), place_id or lat/lng, time_unknown flag |
| Current location | `current_location_history` | On "Create my profile" submit | No (optional) | Only if user supplied a current city |
| Overlay state | `user_settings` | On each overlay acknowledgement | No (but affects UX) | Account-level row, `profile_id IS NULL` |
| First favorite | `favorite_places` | When user taps a place during or after overlay 4 | No (but is Overlay 4 completion trigger) | `profile_id`, `place_id`, `account_id` |

### What is never written during onboarding

- `notes` — no notes interface in the onboarding flow.
- `comparison_sets` or `comparison_set_places` — comparison is a post-onboarding feature.
- `share_links` — no sharing during onboarding.
- `visited_places`, `saved_searches`, `intention_profiles` — post-onboarding features.

### Durability requirements

- **Profile + birth record:** committed atomically on submit. If either fails, neither is saved. The form remains open with an error. Retry must be available without re-entering data.
- **Overlay state:** best-effort write. A failure to write overlay progress does not block the user or show an error. The sequence simply restarts from Overlay 1 on next session if state was lost.
- **Current location:** best-effort write. If it fails, onboarding continues. The map opens centered on the birth location as a fallback.
- **Favorites written during overlay 4:** these use the standard `favorite_places` write path. A write failure surfaces a toast ("Could not save that city — try again") but does not interrupt the overlay sequence.

### Resume-state detection logic (client-side)

On every app load after sign-in, the client performs two reads using the user's session JWT:

1. `GET /rest/v1/profiles?select=id,display_name&limit=1` — to determine if a profile exists.
2. `GET /rest/v1/birth_records?select=id&profile_id=eq.{profile_id}&limit=1` — to determine if birth data exists.

These two reads determine routing:
- No profile → route to profile creation (step 2a).
- Profile, no birth record → route to birth data entry (step 2b), profile pre-loaded.
- Profile + birth record → route to map.

No third-party state management library is required for this logic. The routing decision is made from live Supabase reads on every cold load.

---

## 8. Mobile Considerations

### Screen size constraints

Onboarding must be designed mobile-first. The majority of first-time visits will likely arrive on mobile browsers. No native app exists; the experience is a web app.

**Form screens (steps 1–3):**
- Single-column layout at all breakpoints.
- The active input must be visible above the mobile software keyboard. Birth time and date pickers must not be obscured by the keyboard when open. Test: iPhone SE (375px wide) at minimum.
- Date pickers: the native `<input type="date">` and `<input type="time">` render well on iOS and Android and should be used in preference to custom pickers. Custom pickers should only be introduced if the native behavior is demonstrably insufficient for the product's needs.
- "Skip" and "Back" links must be 44×44pt minimum touch targets.
- CTA buttons must span the full width of the content column (not a fixed pixel width).

**City search:**
- On mobile, the city search input opens a full-screen search sheet rather than an inline dropdown. The sheet contains the search input pinned at the top and results listed below.
- Keyboard is auto-focused when the sheet opens.
- Results must be readable at 16px body text — city name on one line, country on a second line in a lighter weight. Do not truncate city names.

**Map screen:**
- The map must render at full viewport size with no horizontal scroll.
- Overlay tooltips on mobile become bottom sheets. Tooltip arrows pointing to specific map elements are replaced by a "highlight pulse" animation on the target element.
- The map controls (zoom, pan) must not be obscured by the overlay bottom sheet. The sheet should be half-height or less in its initial state, collapsible.

### Interruption tolerance

Mobile users are frequently interrupted. The onboarding flow must tolerate:

- **App backgrounding mid-form:** form state is preserved in memory. On foreground return within the same browser session, the form is exactly as the user left it. No validation is re-run until submit.
- **Phone call during the flow:** same as backgrounding.
- **Closing the browser tab:** the user's session persists (Supabase handles token storage in localStorage). On next visit to the app, the session is detected and the routing logic above runs. No re-login is required unless the session has expired (default: 1 hour access token, 1 week refresh).
- **Loss of network during a write:** surface a specific message ("No internet connection — your data was not saved"). Do not lose the form data. Provide a "Try again" button. Do not auto-retry silently.

### Progressive web app behavior

In v1, no PWA manifest or service worker is required. The app functions as a standard web app. If the user installs it to their home screen via the browser's "Add to Home Screen" prompt, it behaves identically. PWA features (offline mode, push notifications) are post-v1.

### Orientation

Onboarding form screens are designed for portrait orientation. The map screen supports both orientations. No orientation lock is applied.

### Performance targets on mobile

- Time to interactive for the signup form: under 2 seconds on a 4G connection.
- Time from "Create my profile" submit to first map render: under 5 seconds on a 4G connection. (This is dominated by chart calculation, not network.)
- City search results latency: under 300ms after the user stops typing (client-side debounce, 250ms).
- Overlay animations: 200ms or less. No overlay should feel sluggish on a mid-range Android device (Snapdragon 662 or equivalent, 2023 era).

---

## Open Questions (not resolved in this document)

The following require a separate decision before implementation begins:

1. **Chart rendering engine.** Which library or service calculates and renders the astrological lines on the map? This is the largest unresolved technical dependency in the entire product. The onboarding flow assumes it exists; the choice of engine affects map load time, layer format, and what can be shown at first-run.

2. **Birth time uncertainty display.** How are house cusps shown (or not shown) when `time_unknown = true`? This requires a separate rendering doctrine.

3. **Which lines are shown first.** The initial map render shows "the chart." Which planets, which line types (AS, MC, DS, IC), in what order, at what visual weight? This is a product decision with astrological significance.

4. **Overlay 2 — Line identification.** Tapping a line shows what? A label, a tooltip, a side panel? What is shown for a Sun MC line vs. a Saturn DS line? This requires a separate line-detail UX spec.

5. **GeoNames import timing.** City search is non-functional for most cities until the import runs. Onboarding should not launch on production until the import is complete.

6. **Minimum age policy.** Is the product intended for users under 18? If yes, no change is needed. If no, a soft or hard age gate must be designed.

7. **Multiple profiles at onboarding.** Should the first-run experience offer "Add a partner's chart" as an optional step after the user's own profile is created? Deferred to a future onboarding iteration, but the backend supports it from day one.
