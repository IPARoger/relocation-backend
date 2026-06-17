# Web2 Onboarding and Guided Discovery — V2

**Date:** 2026-06-13  
**Supersedes:** WEB2_ONBOARDING_AND_GUIDED_DISCOVERY.md  
**Status:** Planning only. No implementation. No code.  
**Core principle:** Get the user to their first map as fast as possible, then teach the product in context.

---

## What Changed from V1

V1 designed onboarding as a sequence of form screens that gated the map. The user could not see the product until they had answered six questions across three pages.

V2 inverts this. The map loads immediately after signup. All personal intake is collected in a single overlay while the map is already visible and rendering behind it. As soon as minimum required data is entered, the chart starts calculating — the user may see their first line appear before they have even finished the optional fields. Guided discovery then happens on the live map, not in a simulated walkthrough.

The intake overlay is not a form page. It is a floating panel, collapsible, positioned so the map is always visible. The user can skip any optional field and interact with the map at any time.

---

## 1. First Account Creation Flow

### Philosophy

Signup is the shortest possible path to an authenticated state. No personal data is collected at signup. All profile data is collected in the intake overlay on the map. This separates two concerns that V1 conflated: creating a secure account (email + password) and describing yourself astrologically (birth data).

### Entry points

- Landing page primary CTA: one button, no friction preamble.
- Direct link to a shared chart: user is shown the public chart, then prompted to sign up to save their own.
- Returning visitor: session is detected and the map opens directly. Signup screen is never shown to an authenticated user.

### Signup options

**Email / password**
- Two fields: email address and password (minimum 8 characters, show/hide toggle).
- No password confirmation field.
- Submit calls `signUp()` via the publishable key. The `handle_new_user()` trigger fires server-side, creating the account and owner membership invisibly. The user never sees this step.

**Google OAuth**
- Single "Continue with Google" button.
- On success: Supabase creates the `auth.users` row, the trigger fires, and the session is valid. The Google session may supply locale and timezone signals — these are used to pre-fill the language selector and, with lower confidence, the current location field in the intake overlay. All pre-fills are editable.
- Google does not supply birth data. The intake overlay is always required regardless of OAuth provider.

**Email confirmation (production)**
- After email/password signup: "Check your email" holding screen. The map is not yet accessible.
- The holding screen contains: the email address used, a resend link (active after 60 seconds), and a note that the confirmation link expires after 24 hours.
- On confirmation: the user is redirected into the app with an active session. The map loads immediately and the intake overlay appears.
- Google OAuth: no email confirmation step. Session is issued immediately.

### Sign-in (returning user)

Single screen: email + password, or "Continue with Google." "Forgot password?" link triggers Supabase's built-in reset flow. No new backend logic.

On sign-in: if the user has an existing profile with birth data, the map opens at their last-used viewport. If no profile exists, the intake overlay appears over an empty map.

### Error handling

| Condition | Message |
|---|---|
| Email already registered | "An account with this email exists. Sign in instead." |
| Password too short | "Password must be at least 8 characters." |
| Network error | "Check your connection and try again." |
| OAuth cancelled | Return to signup screen silently. |
| Rate limited | "Too many attempts. Try again in a few minutes." |

---

## 2. Intake Overlay

### Design principle

The intake overlay appears over the live map immediately after first login. The map is rendering behind it. The overlay is a floating panel — not a full-screen modal, not a separate page. The user can tap outside the panel on the map at any time. If they do, the overlay collapses to a minimal tab ("Finish setting up your chart →") that re-expands on tap.

The chart begins calculating as soon as birth date and birth location are entered, even before the user submits the full overlay. The user may see their first line appear on the map while still filling in optional fields.

### Language selector

Positioned at the very top of the intake overlay, above all other fields. A dropdown or flag-icon selector. Defaults to the browser's detected locale. If Google OAuth supplied a locale, that is used as the default instead.

Changing the language immediately re-renders all overlay text, all field labels, and all UI strings. It also sets the preferred language stored in `user_settings`. This affects city search results (which `display_name` is shown), date format (day/month/year vs. month/day/year), and time format (12h vs. 24h).

The language selector is always accessible, not buried in settings. For a multilingual product used globally, language choice must not require navigating away from the first screen.

### Intake fields

All fields appear in a single scrollable panel. Required fields are marked. Optional fields are clearly labeled as optional — not with an asterisk system, but with an explicit "(optional)" label in the lighter text style.

---

**Name**

- Label: "What should we call this profile?"
- Free-form text input. Pre-filled with the email prefix for email/password users, or the Google display name for OAuth users. Both are editable.
- Required. Minimum 1 character. Maximum 60 characters.
- Helper text beneath: "This is a private label. It's not your username and it won't be shown to others."

---

**Birth date**

- Label: "Birth date"
- Three-field input: day, month, year. Order adapts to locale (DMY or MDY). Native `<input type="date">` on mobile.
- Required.
- Range: 1900 to the current date.
- No age gate. No validation beyond confirming the date is real.

---

**Birth time**

- Label: "Birth time"
- Three states selectable via radio or segmented control:
  - **Exact** — hour and minute fields, AM/PM or 24h adapted to locale. Unlocks house cusp calculation and angle lines.
  - **Approximate (within an hour)** — same fields, but the app displays house cusps with an uncertainty indicator. The position uncertainty range is stored as metadata. Angular lines are shown with a shaded band rather than a sharp line.
  - **Unknown** — stores null birth time and a `time_unknown` flag. The map renders a solar chart: full planetary positions, no house cusps, no angle lines. A persistent but unobtrusive nudge appears on the map: "Add your birth time to unlock your full chart →" linking to profile edit.
- Required (one of the three states must be selected, but "Unknown" is always valid).
- Do not default to noon, sunrise, or any fabricated time. The product does not produce authoritative-looking fabricated data.

---

**Birth location**

- Label: "Where were you born?"
- City search input backed by the `places` table via `ilike` filtering on `display_name`.
- Results appear after 2+ characters, debounced at 250ms.
- Each result shows: city name on one line, region and country in a lighter style on a second line.
- On selection: the map pans to the selected city's coordinates. This gives the user their first spatial orientation before the chart is even drawn.
- Fallback: "My city isn't listed →" opens manual coordinate entry (latitude + longitude fields, with a draggable pin on the map). Stores `place_id = null` with raw coordinates. This path should be rare once the GeoNames import is complete.
- Required.

---

**Gender** *(optional)*

- Label: "Gender (optional)"
- A small selector with options: Woman, Man, Non-binary / other, Prefer not to say.
- Purpose: the product may use this to contextualize astrological interpretations in future (e.g., Venus placement context varies by relationship structure). It is not used for chart calculation in v1. It is stored in `profiles` or an extension field.
- "Prefer not to say" and leaving the field entirely are both equivalent to no selection. Neither is treated as a data gap in any part of the product.

---

**Current location** *(optional)*

- Label: "Where do you currently live? (optional)"
- Same city search UI as birth location.
- If Google OAuth supplied a timezone or location signal with high confidence, the nearest city is pre-selected. User can clear and re-search.
- Stores to `current_location_history`.
- If provided: the initial map viewport centers on the current location rather than the birth location.
- If skipped: map centers on the birth location.

---

**Citizenship checkbox**

- Label: "I am a citizen of my birth country"
- Default: checked, because this is true for most users born in their country of citizenship.
- This is functionally a convenience flag, not a legal question. It affects the initial assumption in the relocation use case — a user who is a citizen of their birth country has different mobility options than a user who was born in one country but has citizenship elsewhere (a common scenario for international families, diaspora communities, and dual nationals).
- Opt-out: unchecking reveals a secondary optional field: "Which countries are you a citizen of?" — a multi-select city/country search. This is low priority at v1 and may be deferred to profile edit.
- Skip support: the checkbox section can be collapsed or skipped without error. The default checked state covers the majority of users without requiring any action.

---

### Submission behavior

The "Generate my map" button is enabled as soon as birth date and birth location are entered. Birth time must be in one of the three states (Exact, Approximate, or Unknown). Name is required. Gender, current location, and citizenship are optional.

On submit:
1. `profiles` INSERT with `display_name`, `account_id`, `account_user_id`, `profile_type = 'human'`, gender if provided.
2. `birth_records` INSERT with date, time (or null), time precision state, birth place id, birth coordinates.
3. `current_location_history` INSERT if a current location was provided (best-effort; failure does not block).
4. `user_settings` INSERT for language preference and citizenship flag (best-effort).
5. The intake overlay closes. The chart calculation request fires (or confirms, if it already started when birth date + location were entered). The map comes fully into view.

All required writes (profile + birth record) are committed atomically. If either fails, the overlay remains open with a recoverable error. The form data is not cleared on failure.

### Re-entry behavior

If a user closes the browser before submitting the intake overlay:

- No profile exists yet. On next sign-in, the map loads and the intake overlay reappears with no pre-filled data (since nothing was saved).
- The account exists (the trigger fired at signup). The overlay must not re-run signup. It re-presents the intake panel only.

If the user submits the overlay but closes the browser before the map loads:

- Profile and birth record exist. On next sign-in, the app detects the complete profile and routes directly to the map. The intake overlay does not reappear.

---

## 3. Map Launch

### Loading sequence

Immediately after intake is submitted (or when a returning user signs in):

1. Map base tiles load and render at full viewport. This is fast — it requires no user data.
2. Chart calculation begins. A non-blocking indicator ("Calculating your chart…") appears in a corner of the map, not obscuring any content.
3. Astrological lines render progressively as they become available. The first visible line may appear within 1–3 seconds. The user can pan and zoom during calculation.
4. When calculation is complete, the indicator disappears.
5. If this is a first-run session: the guided discovery overlay sequence activates after the first line is visible.

### Initial viewport

Priority order:
1. Current location, if provided in intake.
2. Birth location.
3. Geographic center based on the browser's detected locale (fallback only, used when neither of the above is available — unlikely after intake).

Initial zoom: regional level (approximately zoom 5–7), wide enough to show nearby countries and significant geography. This gives the user a meaningful first spatial context without overwhelming them with the entire world.

### First-run detection

A session is treated as first-run if the account's `user_settings` contains no `onboarding_overlay_sequence` key. This key is written on the first overlay acknowledgement. Until it exists, every map load for this account activates the discovery sequence.

This is more reliable than a time-based heuristic (V1's "profile created within 5 minutes"). It survives page refreshes, device changes, and network interruptions without false positives.

---

## 4. Map-Based Guided Discovery

### Principles

1. **Map first.** Every overlay appears after the map is rendered and at least one line is visible. The user is looking at real data when they receive the explanation.
2. **One concept per overlay.** No overview screens. No list of features. Each overlay introduces exactly one interaction and stops.
3. **Always skippable.** A global "Skip tour" control is always visible. Pressing it dismisses the entire sequence and marks it complete in `user_settings`. It never reappears.
4. **Sequentially optional.** Each overlay has its own "Skip this" link that advances to the next overlay without completing the interaction it describes. The user can skip individual overlays without skipping the whole sequence.
5. **Map always live.** The user can interact with the map at any point during any overlay. Overlays are non-blocking panels or tooltips, not interstitials.
6. **Progress persisted.** State is stored in `user_settings` at the account level (key: `onboarding_overlay_sequence`, value: JSON recording `last_completed`, `skipped_steps`, `dismissed_at`). The sequence resumes from the correct step across sessions and devices.
7. **Not repeated.** Once the sequence is complete or globally skipped, it does not reappear. A separate "Restart tutorial" option is available in the Help section for users who want to revisit it.

---

### Overlay 1 — Profile selector and Add profile

**Trigger:** First map render, after chart lines appear.  
**Target:** The profile selector control (top of the sidebar or header area).  
**Content:** "This is your first profile — it's your own birth chart. You can add profiles for partners, family, or anyone else you want to chart. Switch between them here."  
**Interaction:** None required. "Next" or "Skip this."  
**Why first:** The profile is the atomic unit of the product. Before teaching features, the user must understand what the active subject of the map is. Multiple profiles are a core differentiator and should be surfaced before any other concept.

---

### Overlay 2 — Genie search (AI Astro Assist)

**Trigger:** After Overlay 1 is acknowledged.  
**Target:** The Genie / AI search entry point (search bar or dedicated button).  
**Content:** "Not sure where to start? Tell Genie what you're looking for — in plain language. 'I want somewhere good for my career' or 'I'm looking for connection and creativity.' Genie translates your intentions into chart variables and shows you where they land on your map."  
**Interaction:** Optional — user can type a query now or tap "Next" to continue.  
**Why second:** Many users arrive not knowing what astrocartography variables mean. Genie is the lowest-friction entry into the product for this majority. Teaching it early removes the anxiety of needing to understand the system before using it.

---

### Overlay 3 — Selecting variables

**Trigger:** After Overlay 2 is acknowledged.  
**Target:** The variable selector panel (layer list, planet/angle toggles).  
**Content:** "You can also build your own search. Each line on the map represents a planet at a specific angle. Turn variables on and off to find where your chosen themes overlap."  
**Interaction:** Encourage the user to tap one toggle to show or hide a layer.  
**Why third:** For users who already know astrocartography, or who want control after seeing what Genie produced, the manual variable layer is the primary interface. It deserves its own overlay, separate from Genie.

---

### Overlay 4 — Mute / Solo / NOT

**Trigger:** After Overlay 3 is acknowledged.  
**Target:** The mute, solo, and NOT controls on any variable row.  
**Content:** "Three ways to focus: Mute hides a line without removing it. Solo shows only that line. NOT excludes a line's influence — useful when a planet is one you want to avoid."  
**Interaction:** Encourage the user to try one of the three controls.  
**Why fourth:** These are the search refinement tools. Once the user understands variables, these controls are the next step in precision. NOT in particular is a unique and important concept — exclusionary search is rare in consumer products and must be taught explicitly.

---

### Overlay 5 — City popup

**Trigger:** After Overlay 4 is acknowledged, or when the user first taps a city on the map (whichever comes first).  
**Target:** A city marker or the popup that appears on city tap.  
**Content:** "Tap any city to see which chart lines pass through it, how far they are, and what they mean for that location."  
**Interaction:** Encouraged — the overlay completes automatically if the user taps a city. Otherwise, "Next."  
**Why fifth:** Understanding the city popup is prerequisite to favoriting, comparing, and saving places. It is the information surface that makes the map meaningful rather than decorative.

---

### Overlay 6 — Right-click / arbitrary point truth

**Trigger:** After Overlay 5 is acknowledged.  
**Target:** Any point on the map that is not a city marker.  
**Content:** "You're not limited to cities. Right-click anywhere on the map (or long-press on mobile) to see the chart truth at that exact point. Useful for rural locations, specific addresses, or anywhere that isn't in the city database."  
**Interaction:** Encouraged — demonstrate by right-clicking or long-pressing. "Next" to advance without interaction.  
**Why sixth:** This is a power-user feature that unlocks the map for uses beyond city comparison. Surfacing it early signals that the product is not limited to an existing city list — a common misconception about astrocartography tools.

---

### Overlay 7 — Save to favorites and name the saved place

**Trigger:** After Overlay 6 is acknowledged.  
**Target:** The favorite/save button in the city popup or the context menu.  
**Content:** "Save any location to your favorites list. Give it a name — 'Berlin for career' or 'Bali short-term' — so you remember why you saved it. You can save as many as you want and return to them any time."  
**Interaction:** Encouraged — saves the current city or any pinned point. The write to `favorite_places` confirms. "Next" to advance without saving.  
**Why seventh:** Saving is the first persistent action the user takes that is meaningful to their personal workflow. It also creates data (favorite count > 0) that enables downstream features like comparison. Teaching it here, in context, is more natural than introducing it in a list.

---

### Overlay 8 — Compare / pin feature

**Trigger:** After Overlay 7 is acknowledged.  
**Target:** The compare or pin control in the favorites list or city popup.  
**Content:** "Pin two or more locations to compare them side by side. The comparison table shows which chart themes each location activates, so you can weigh tradeoffs without losing either option."  
**Interaction:** None required — comparison requires at least two saved locations, which the user may not yet have. "Next" to advance.  
**Note:** If the user has fewer than two saved locations, the overlay shows a preview of what the comparison table looks like. It does not require the user to have saved enough places to demonstrate it live in this step.  
**Why eighth:** Comparison is the core analytical workflow for the relocation decision use case. Users who save places will naturally want to compare them. This overlay bridges that intention to the specific UI control.

---

### Overlay 9 — Slider / ghost tools

**Trigger:** After Overlay 8 is acknowledged.  
**Target:** The time slider or ghost/transit overlay control.  
**Content:** "Use the time slider to move your chart forward or backward — see how your lines shift as you age, or project future transits. Ghost mode overlays a second chart (a partner, a transit, or a relocated chart) so you can see both at once."  
**Interaction:** None required. "Next."  
**Why ninth:** These are advanced tools that require context before they are useful. Placing them late in the sequence ensures the user already understands the basic line structure before being introduced to time variation. Introducing sliders too early causes confusion about which chart they are looking at.

---

### Overlay 10 — Share

**Trigger:** After Overlay 9 is acknowledged.  
**Target:** The share button or share link control.  
**Content:** "Share your map or a specific view with an astrologer, a friend, or your future self. You control whether the link is private, unlisted, or public."  
**Interaction:** None required. "Next."  
**Note:** Share links are wired in the backend (`share_links` table, `get_shared_chart()` RPC, visibility check). The frontend share UI is not yet built but the overlay can be drafted now.

---

### Overlay 11 — Notes entry point

**Trigger:** After Overlay 10 is acknowledged.  
**Target:** The notes icon or notes panel entry point on the map or city popup.  
**Content:** "Add notes to any location, line, or profile. Notes are private, saved to your account, and available on any device. Use them to record insights from an astrologer session, track your research, or remind yourself why a city did or didn't resonate."  
**Interaction:** None required.  
**Completion:** Tapping "Got it" on Overlay 11 marks the discovery sequence complete in `user_settings`. A brief "You're all set" confirmation replaces the overlay for 2 seconds, then disappears. The map is fully live with no overlays.  
**Why last:** Notes are a workflow tool, not a discovery tool. They are most meaningful once the user has done enough exploring to have something worth recording. Introducing them last, after all the active features, gives them the correct context.

---

### Deferred from first-run sequence

**Road Trip Mode** is not included in the first-run onboarding sequence. It is a distinct and complex mode that changes the fundamental interaction model of the map. Introducing it during the tutorial would compete with the core line-based workflow. Road Trip Mode is documented separately and is surfaced via:
- A "Modes" section in the Help / Education panel.
- A tooltip or badge on the mode selector control, visible after the first-run sequence completes.
- A dedicated tutorial sequence that activates only when the user first switches into Road Trip Mode.

---

## 5. Educational Content

The following content is accessible from a persistent "Learn" or "Help" entry point in the app. It is not shown during the first-run sequence. It is structured for self-directed discovery, not reading from start to finish.

---

### 5.1 Start Here: Beginner Guide to Relocation Astrology

**Purpose:** Give users with no prior astrological knowledge enough context to understand what the map is showing.

**Contents:**
- What astrocartography is: the birth chart mapped onto the surface of the Earth.
- What the lines represent: each line marks a place on Earth where one planet was at a specific angle to the horizon (rising, setting, overhead, or at its lowest) at the moment of birth.
- Why location matters astrologically: the same chart produces different angular relationships depending on where you are on Earth, which changes which planetary energies are most activated.
- What the map cannot do: it does not calculate transits (unless the time slider is used), it does not show synastry unless a second profile is loaded, and it does not make prescriptive decisions.
- One concept to hold: the map shows *potential for activation*, not guaranteed outcomes. The same Sun MC line in Berlin might express as career momentum for one person and public visibility stress for another. Context, intention, and timing all matter.

**Format:** Scrollable article. Approximately 400 words. No jargon without definition. Links to the relevant overlay in the discovery sequence where appropriate.

---

### 5.2 How to Use This Product

**Purpose:** A functional orientation for users who skipped or completed the discovery sequence and want a reference.

**Contents:**
- How to start a search: Genie vs. manual variable selection.
- How to read the variable panel: planets, angles, and what each combination means at a basic level.
- How to interpret a city popup: which lines are within orb, what "within orb" means, how to read the planetary theme summary.
- How to save and organize favorites.
- How to build a comparison.
- How to add notes.
- How to share a view.

**Format:** Short-form reference with section headers. Each section is one to three paragraphs. No tutorial sequence — this is a reference, not a walkthrough.

---

### 5.3 Use Cases

A library of short-form use case guides. Each covers: the question the user is trying to answer, which product features to use, and a worked example.

**5.3a Job relocation — three-city choice**
The user has job offers in three cities and wants to understand which best supports their career intentions. Workflow: load MC and Sun lines for career, add Jupiter and Saturn as modifiers, save all three cities, open comparison table, note which city has the most constructive overlap with career variables and the fewest antagonistic ones.

**5.3b Professional relocation**
A senior professional, possibly working with a relocation coach or executive astrologer. Workflow: use AI Astro Assist to translate professional intentions into variables, refine with NOT exclusions for planets associated with difficulty in professional contexts, use Diff mode (future) to compare shortlisted cities in detail, export or share the comparison for an external session.

**5.3c Medical tourism**
The user is seeking treatment and wants to understand which locations might be supportive of healing. Workflow: use the healing and vitality intention context in Genie, focus on 6th house activations and Jupiter/Chiron lines, check what lines pass within orb of specific clinic cities, compare options in the table.

**5.3d College selection**
A student or parent evaluating university cities. Workflow: use Mercury and Jupiter variables for learning environments, add Moon for emotional environment, exclude Saturn for pressure/restriction if desired, save all candidate cities, compare.

**5.3e Personal growth and spiritual development**
The user is not relocating for work but for inner development — retreat, transformation, a new chapter. Workflow: Pluto and Neptune lines for depth and dissolution, Jupiter for expansion, 12th house activations, Chiron. Note that these are high-intensity activations and context (how long the stay, what the intention is) significantly affects interpretation.

**5.3f Digital nomad / van life / slow travel**
The user moves frequently and wants to understand the landscape of their options globally. Workflow: use the slider to layer transit lines over natal lines, identify windows where specific regions are additionally activated, save regions rather than specific cities, use Road Trip Mode for continuous-movement planning (see Road Trip Mode documentation).

**5.3g Open-ended exploration**
The user is curious, not yet asking a specific question. Workflow: start with AI Astro Assist using "I want to explore" as the opening prompt, let Genie suggest an intention context based on the user's current transits or dominant natal themes, explore the suggested variables, save anything that resonates.

---

### 5.4 How AI Astro Assist (Genie) Works

**Purpose:** Set accurate expectations. Genie is a powerful tool but is not an oracle and must not be presented as one.

**What Genie does:**
- Listens to intentions expressed in natural language and translates them into astrological search variables. A statement like "I want somewhere that supports my creative work" becomes a set of relevant planetary variables (Venus, Neptune, 5th house activations, etc.) that are then applied to the map as a layer filter.
- Asks clarifying questions when an intention is vague or could map to multiple themes. "Creative work" in a career context is different from "creative work" as personal expression — the clarification changes which variables are prioritized.
- Translates *desired states* (what the user wants more of) into positive variable selections and *undesired states* (what the user wants less of or wants to avoid) into NOT exclusions.
- Summarizes its reasoning: after generating a variable set, Genie shows which intentions mapped to which variables and why, so the user can validate the translation and adjust manually.

**What Genie does not do:**
- It does not declare one city as universally best. There is no ranking algorithm producing a single answer. The output is always a filtered map showing where certain conditions are present — the user makes the judgment.
- It does not act as an astrologer or make life advice. Its role is to translate stated intentions into the product's search language, not to interpret the chart or prescribe life decisions.
- It does not know facts about cities (cost of living, visa requirements, climate). It operates only on astrological data. These practical dimensions must be researched outside the product.
- It is not infallible. Its variable translation is a starting point. Users should inspect the variable list it produces and adjust any selections that do not match their actual intentions.

---

### 5.5 Product Method

**Purpose:** Teach the systematic workflow that produces reliable results, as opposed to casual browsing.

**Step 1 — Find overlaps for desired features**
Start with two or three variables that represent the most important intentions. Locations where multiple desired lines intersect or are within orb of each other are "hot zones" of cumulative activation. One strong planet is notable; two or three in the same region are significant.

**Step 2 — Use NOT and exclusions for undesired features**
NOT is the complement of selection. A user who wants career activation but has Saturn in a difficult position natal may want to exclude Saturn MC lines rather than risk interpreting them as career help. NOT filters are applied per-variable and do not remove the line from the map — they flag locations where the excluded variable is active, so the user can make an informed choice rather than discovering the conflict later.

**Step 3 — Refine with AI Astro Assist**
After manual exploration, bring findings back to Genie for a second pass. Describe what you've found ("I see a lot of Venus and Jupiter overlap in Southeast Asia") and ask what that pattern suggests for the stated intention. Genie can provide a contextualized interpretation of the overlap pattern without declaring it optimal.

**Step 4 — Compare tradeoffs in tables**
Once two or more candidate locations are saved, the comparison table shows the full variable profile of each location side by side. This is the analytical core of the relocation decision workflow. No location will be perfect on all dimensions. The table makes the tradeoffs explicit so the user can prioritize.

**Step 5 — Use the dignities toggle optionally**
The dignities layer shows where planets are in signs of dignity, detriment, exaltation, or fall at the user's birth location and at any selected map point. This is an advanced interpretive layer — it adds nuance to the basic line activation but it is not a scoring system and does not override line-based analysis. It is off by default. Use it as a modifier after the primary variable analysis is complete.

**Step 6 — Use Diff mode to compare nearby or similar locations**
*(Future feature — see Section 7)* Diff mode shows only the differences between two locations that are geographically close or otherwise similar. Useful when comparing two cities in the same region, or two neighborhood-scale points within one city.

---

### 5.6 Beginner Path

A recommended sequence for users who are new to astrocartography and want to build understanding gradually rather than being overwhelmed by the full feature set.

**Start with AI Astro Assist.** Don't touch any manual controls on the first session. Tell Genie one intention in plain language and explore the map it produces. The goal is to see the lines, get a felt sense of the geography, and save two or three places that feel interesting. No analysis yet.

**Explore ASC/MC sign changes.** On a second or third session, zoom in on a region that interested you. Notice where the Ascendant and Midheaven lines shift you from one sign to another. These are the most commonly discussed lines in relocation astrology and the easiest to get initial context on from general astrological resources.

**Learn one element at a time.** Pick one planet — the Sun is the most intuitive starting point — and explore only its lines for a full session. Understand what the four angles (AS, MC, DS, IC) mean for that planet before layering in a second planet. Depth before breadth.

**Full chart review comes later.** Only after the user has explored individual variables and a few planetary themes should they attempt a complete multi-planet analysis. The comparison table and variable overlap tools are designed for this stage. Jumping to full-chart analysis before understanding individual variables produces confusion, not insight.

---

### 5.7 Professional Path

A recommended workflow for users who have astrological training, are working with a professional astrologer, or are making a high-stakes relocation decision.

**Use the app with an astrologer or AI Astro Assist as a second opinion.** The product is designed as a research and visualization tool, not a replacement for expert interpretation. A professional user will have specific variable hypotheses based on their chart knowledge and can use the product to test those hypotheses against the geographic database.

**Manage tradeoffs explicitly.** Professional-level analysis acknowledges that no location is uniformly positive. The NOT exclusion tool, the comparison table, and the notes system are designed for tradeoff management. A professional workflow might result in a ranked shortlist with explicit reasoning attached to each candidate, not a single answer.

**Save and compare candidates systematically.** Use the favorites system to build a complete candidate list before evaluating any single location in depth. Use comparison tables to surface the full variable profile of each candidate. Add notes with session-specific observations. Share the resulting view with a client, collaborator, or external astrologer for additional input.

---

## 6. Data Persistence Requirements

### Written during onboarding

| Data | Table | Timing | Required |
|---|---|---|---|
| Account | `accounts` | Trigger at signup | Yes |
| Owner membership | `account_memberships` | Trigger at signup | Yes |
| Language preference | `user_settings` (account-level) | On language change in overlay | Best-effort |
| Profile | `profiles` | On intake overlay submit | Yes |
| Birth record | `birth_records` | On intake overlay submit | Yes |
| Current location | `current_location_history` | On intake overlay submit | Optional |
| Gender | `profiles` extension field | On intake overlay submit | Optional |
| Citizenship flag | `user_settings` | On intake overlay submit | Optional |
| First favorite | `favorite_places` | When user saves from Overlay 7 or map | Optional |
| Overlay sequence state | `user_settings` (account-level) | On each overlay acknowledgement | Best-effort |

### Durability rules

- Profile + birth record commit atomically. Neither saves without the other.
- All other fields are best-effort. Failures do not block the user or surface errors that require action.
- Overlay state loss (due to network failure on the `user_settings` write) causes the sequence to restart from Overlay 1, not from the last completed overlay. This is a minor UX regression; it is acceptable because re-watching early overlays is harmless and adding retry logic for optional state adds complexity without user-facing value.

### Resume routing

On every cold load after sign-in:

| Profile exists | Birth record exists | Route to |
|---|---|---|
| No | — | Intake overlay over map |
| Yes | No | Intake overlay (birth data fields only) over map |
| Yes | Yes | Map directly |

The intake overlay does not re-appear once a complete profile + birth record exist. The language selector is always accessible from settings regardless.

---

## 7. Completion Criteria

Onboarding is complete when:

| # | Criterion | Table |
|---|---|---|
| C1 | Active auth session exists | `auth.users` |
| C2 | Account and owner membership exist | `accounts`, `account_memberships` |
| C3 | Profile row with `display_name` exists | `profiles` |
| C4 | Birth record linked to profile exists | `birth_records` |
| C5 | Map has rendered at least one line | Logged to `user_settings` on first render event |
| C6 | Overlay sequence has been started or skipped | `user_settings` key `onboarding_overlay_sequence` exists |

A user who submits the intake overlay, reaches the map, and immediately hits "Skip tour" satisfies all six criteria. They are in a complete and valid product state.

---

## 8. Mobile Considerations

### Intake overlay on mobile

- The overlay renders as a bottom sheet on screens narrower than 768px. It occupies 60% of screen height in its initial state, with a drag handle to expand to 90% or collapse to a tab.
- The map is always visible in the background above the collapsed bottom sheet. Swiping the map (not the overlay) dismisses the overlay to its collapsed tab state.
- Language selector: renders as a full-width dropdown at the top of the bottom sheet. Opening it expands the sheet to full height.
- City search within the overlay: opens a sub-sheet over the current sheet. Keyboard auto-focused. Results visible above keyboard on iPhone SE (375px).
- Date and time inputs: use native `<input type="date">` and `<input type="time">`. Custom pickers are only introduced if native behavior is insufficient.

### Discovery overlays on mobile

- All 11 guided discovery overlays render as bottom sheets on mobile (half-height, collapsible).
- Element highlights (pointing to specific UI controls) use a pulsing ring animation rather than pointer arrows, since the pointer's target element may be offscreen on mobile.
- "Skip tour" and "Next" controls are always visible in the bottom sheet header, above the scroll fold, at full-width touch targets.

### Map interaction on mobile

- Long-press anywhere on the map triggers the right-click / arbitrary point behavior (Overlay 6).
- All map controls (zoom, profile switcher, variable panel toggle) are touch-target sized (minimum 44×44pt).
- The bottom sheet overlay does not obscure the map controls. Map controls are repositioned to the top half of the screen when a bottom sheet is open.

### Interruption and offline behavior

- **App backgrounded mid-intake:** in-memory form state is preserved for the session. No partial writes occur mid-form.
- **Network lost during intake submit:** form data is not cleared. An error message identifies the failure as a network issue. Retry button is visible. No auto-retry.
- **Session expired (over 1 hour idle):** the Supabase client refreshes the token using the refresh token (valid for 1 week by default). If the refresh fails (user explicitly signed out elsewhere), the sign-in screen is shown.

### Performance targets

- Signup form time to interactive: under 2 seconds on 4G.
- Intake overlay render: under 500ms after first authenticated map load.
- Map base tiles visible: under 1 second after authentication.
- First chart line visible: under 4 seconds from intake submit on 4G.
- City search response: under 300ms after 250ms debounce.
- Overlay animations: under 200ms transition. No jank on Snapdragon 662-class devices.

---

## 9. Future Feature Notes

The following features are not part of v1 onboarding or the current product scope but are noted here because they affect how the onboarding is described and how educational content is framed.

### Dignity light-ups

An optional table layer that shows where planets are in signs of dignity (domicile, exaltation), detriment, or fall at any map point. This is not a scoring system — it does not produce a numeric ranking of locations. It is a contextual modifier: a planet in dignity in a given location may express more clearly or constructively, while a planet in detriment may require more conscious integration.

**Implementation note:** This layer is off by default. It must not appear in the initial map render or the first-run discovery sequence. It is introduced in the Professional Path documentation (Section 5.7) as an advanced modifier. Dignity light-ups should never be framed as "this city is better because your Sun is in dignity there" — the relationship between dignity and lived experience is nuanced and depends heavily on natal chart context.

### Diff Mode

A comparison mode that shows only the differences between two locations that are geographically close or contextually similar. When two cities are within 300km of each other, or when the user explicitly enters Diff mode with two saved locations selected, the map hides all lines that are identical or near-identical between the two locations and highlights only what is meaningfully different.

**Use cases:** comparing two neighborhoods in the same metropolitan area, two cities in the same country, or two candidate cities that share most of their planetary activations but differ in one or two significant variables. Diff mode is especially useful for users who have already narrowed to a final shortlist and need to distinguish between near-equivalent options.

**Onboarding reference:** Diff mode is mentioned in Overlay 9 (slider/ghost tools) as a contextual aside only. It is not demonstrated during the first-run sequence. It receives its own tutorial when the user first enters Diff mode.

---

## Open Questions Carried from V1

1. **Chart rendering engine.** Still unresolved. The choice of calculation library and line rendering approach determines map load time, layer format, and what can be shown at first-run. This is the largest single unresolved technical dependency.
2. **Which lines render first.** Initial chart layer selection has astrological significance. A separate rendering doctrine is required.
3. **Birth time uncertainty display.** How house cusps are shown (with uncertainty bands) when the user selects "Approximate" requires a visual design decision.
4. **Line detail content.** What appears when the user taps a line — label only, brief description, or full interpretive panel — requires a separate content and UX specification.
5. **GeoNames import timing.** City search is not viable at scale until the import runs. Onboarding intake (birth location field) must include the manual coordinate fallback from day one.
6. **Gender field schema.** The `profiles` table schema as validated through Phase 6 does not include a gender column. Adding it requires a Phase 7-adjacent schema change or a `user_settings`-based storage approach before the intake overlay can write this field.
7. **Citizenship field schema.** Similarly, the citizenship flag and multi-citizenship list have no current table representation. This field may be stored in `user_settings` as a JSON value or deferred to a future schema addition.
