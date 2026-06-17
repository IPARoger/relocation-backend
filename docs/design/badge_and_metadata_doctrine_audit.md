# Badge & Metadata Doctrine Audit

Status: provisional audit + doctrine extraction (Phase 2.8D)
Type: archaeology / doctrine only — no code, CSS, API, or component changes
Scope: badges, metadata, ownership, hierarchy, placement, authority

Out of scope (deferred to later phases): colors, typography, animation,
shadows, glow, spacing.

Files audited:
`map_CURRENT.html`, `prototype_profile_workspace_v11.html`,
`prototype_relocated_location_v1.html`, `comparison_v2.html`,
`comparison_v3.html`, `comparison_v4.html`, `comparison_v5.html`,
`city_profile_v1.html`, `city_profile_v2.html`, `city_profile_v3.html`,
`city_profile_v4.html`, `app_shell.html`.

---

## 1. Badge Inventory

Each badge: name, page(s), purpose, data source, placement, role
(Identity / Context / Status / Authority / Action / Warning), and survival
recommendation (YES / NO / MAYBE).

### Natal
- **Pages:** profile v11 (`view-pills .chip[data-view=natal]`), profile favorites list ("Natal (Birth Chart)").
- **Purpose:** select/label the birth-chart view.
- **Data source:** static view state.
- **Placement:** view pills (below header); favorites row text.
- **Role:** Context.
- **Survive:** YES.

### Current Location
- **Pages:** profile v11 (`chip[data-view=current]`, `.reloc-block .reloc`), comparison v3–v5 (`.pcurr-label`, `.city-tag` on Austin).
- **Purpose:** mark the relocated/current-location view or the city that is the user's current location.
- **Data source:** view state; comparison city `tag` field.
- **Placement:** view pills; plate reloc block; sticky city column tag.
- **Role:** Context (view) / Status (city tag).
- **Survive:** YES (but unify wording vs "Relocated").

### Relocated (context language only — not a required visible badge)
- **Pages:** relocated v1 (`#sysMeta` "Relocated" heading, `.ps-label` "Relocated chart", page title), map popup policy text.
- **Purpose:** internal doctrine language for the relocated chart context.
- **Data source:** static section headings.
- **Placement:** side/sys metadata; page top.
- **Role:** Context.
- **Survive:** As **internal doctrine language only.** Do NOT promote
  "Relocated Location" to a primary user-facing badge. User-facing badges
  should likely remain limited to **Natal** and **Current Location**. A
  saved/relocated place should usually be identified by its **place name**,
  **favorite state**, and **chart context** — not a heavy "Relocated Location"
  badge. (Kept open in Section 7.)

### Favorite / Favorited
- **Pages:** map popup (`.popup-action-favorite` "Favorite" → "Favorited ✓"), relocated v1 (`.fav-btn` "Favorited"/"Add to Favorites"), profile v11 (`.fav .star.on`, `.fav-new` highlight).
- **Purpose:** show/toggle favorite state of a place.
- **Data source:** favorite-places API (map/profile); local toggle (relocated prototype).
- **Placement:** popup actions; page header action; favorites list star.
- **Role:** Action + Status (mixed in one control).
- **Survive:** YES (separate Action vs Status concerns later).

### Shared
- **Pages:** none rendered. Appears only in comments (`city_profile_v1/v2`) and was referenced in plans.
- **Purpose:** intended "shared view" marker.
- **Data source:** none yet.
- **Placement:** N/A.
- **Role:** Status (intended).
- **Survive:** MAYBE (no component exists; future need).

### Archived
- **Pages:** map_CURRENT, profile v11 — logic only (`archived_at` filter); no visible badge.
- **Purpose:** hide archived favorites/profiles.
- **Data source:** API `archived_at`.
- **Placement:** none (behavior, not UI).
- **Role:** Status (latent).
- **Survive:** MAYBE (needs a real badge if archived items ever surface).

### Draft
- **Pages:** app_shell (exploration/auto-save copy: "draft").
- **Purpose:** indicate unsaved/auto-save state.
- **Data source:** scaffold state.
- **Placement:** scaffold text.
- **Role:** Status.
- **Survive:** MAYBE (scaffold-only today).

### Active (Chart Record / Active place)
- **Pages:** app_shell (`context-chip` "Active Chart Record", "Active place").
- **Purpose:** show which record/place is in context.
- **Data source:** nav context (scaffold).
- **Placement:** context chip.
- **Role:** Authority/Context.
- **Survive:** MAYBE (scaffold; concept maps to profile authority).

### Confidence (tier)
- **Pages:** app_shell (`confidenceTier`, birth-time uncertainty warn-box).
- **Purpose:** communicate birth-time confidence.
- **Data source:** birth profile `confidence_tier`.
- **Placement:** context chip; warning box.
- **Role:** Status / Warning.
- **Survive:** MAYBE (post-v1 concept; keep as warning, not decorative badge).

### Record Type (self / research / client)
- **Pages:** app_shell (`recordType`, `formatRecordType`).
- **Purpose:** classify chart record ownership.
- **Data source:** store `record_type`.
- **Placement:** context chip, record lists.
- **Role:** Identity/Context.
- **Survive:** MAYBE (scaffold vocabulary, not current product language).

### Tropical
- **Pages:** profile v11, relocated v1 (`#sysMeta` Zodiac), comparison v3–v5 (`.profile-line.system`).
- **Purpose:** declare zodiac system.
- **Data source:** static profile/system fields.
- **Placement:** plate sub-line; sys metadata; profile band.
- **Role:** Context (system).
- **Survive:** MAYBE as a badge — likely **metadata**, not a badge (see Part 3).

### Placidus
- **Pages:** profile v11, relocated v1 (Houses), comparison v3–v5 (`.profile-line.system`), app_shell (house-system select), map popup (policy note re Placidus ±65°).
- **Purpose:** declare house system.
- **Data source:** static; map policy text.
- **Placement:** plate sub-line; sys metadata; popup policy note.
- **Role:** Context (system) / Warning (map policy).
- **Survive:** MAYBE as a badge — likely **metadata** (see Part 3).

### Sidereal / Koch
- **Pages:** none. Not present in any audited surface.
- **Purpose:** alternative zodiac/house systems (future).
- **Data source:** none.
- **Placement:** N/A.
- **Role:** Context (future).
- **Survive:** MAYBE (only if multi-system support arrives).

### Current Profile
- **Pages:** profile v11 (`.profile-select` name + caret), relocated v1 (`#profileSelect`), map (`#chartProfile` select), comparison (`.profile-name`/`.nav-account` static).
- **Purpose:** show/switch the governing profile.
- **Data source:** chart-profiles / profiles API (map, profile); static (comparison/city).
- **Placement:** header / in-plate selector.
- **Role:** Authority.
- **Survive:** YES (highest-authority control; unify presentation later).

### Current City / Current Comparison / Current Search
- **Pages:** profile v11 lower lists (Favorites, Saved Comparisons, Saved Searches); relocated v1 location plate; not rendered as discrete "current X" badges.
- **Purpose:** indicate active/selected saved entity.
- **Data source:** favorites/comparisons/searches state.
- **Placement:** lower saved panels; plate.
- **Role:** Context/Status.
- **Survive:** MAYBE (currently implicit via selection, not explicit badges).

### Lat Cap ON/OFF (debug)
- **Pages:** map_CURRENT (debug/self-check overlays).
- **Purpose:** developer diagnostic.
- **Data source:** runtime flag.
- **Placement:** debug overlay.
- **Role:** Status (internal).
- **Survive:** NO (debug-only; never product canon).

---

## 2. Metadata Inventory

Each field: name, pages, purpose, importance tier (1 must-see → 4 advanced),
recommended ownership.

**Birth Time is Tier 1 identity/chart data.** It is NOT ordinary metadata and
must never be grouped visually with Lat/Lon, UTC, or source/provenance.

### Tier 1 identity / chart block (one cohesive group)

These four belong together as identity/chart data, not low-priority metadata:

| Field | Pages | Purpose | Tier | Ownership |
|---|---|---|---|---|
| Profile Name | profile, relocated, comparison, map select | Identify the lens/person | 1 | Profile |
| Birth Date | profile, relocated, comparison, app_shell | Identity / chart data | 1 | Profile |
| Birth Time | profile, relocated, comparison, app_shell | Identity / chart data | 1 | Profile |
| Birth Place | profile, relocated, comparison | Identity / chart data | 1 | Profile |

### Supporting technical metadata

Distinct from the identity block above; technical inputs and system settings.
Do not group Birth Time with any of these:

| Field | Pages | Purpose | Tier | Ownership |
|---|---|---|---|---|
| Birth Lat/Lon | profile (sub), relocated (sys) | Chart geometry input | 3 | Profile |
| UTC Offset | profile, relocated, comparison | Time normalization | 2 | Profile / Location |
| Time Zone (named, e.g. JST) | relocated (`+09:00 (JST)`), city orientation | Human-readable TZ | 3 | Location |
| Zodiac System (Tropical) | profile, relocated, comparison | Interpretive system | 2 | System |
| House System (Placidus) | profile, relocated, comparison, app_shell, map policy | Interpretive system | 2 | System |
| Source / provenance | relocated (`city_dataset`), map (`popup-dataset-note`), city profiles | Provenance | 4 | System / Shared View |

### Other fields (location & city intelligence)

| Field | Pages | Purpose | Tier | Ownership |
|---|---|---|---|---|
| Relocated Place | relocated, profile current view, map popup | Page subject location | 1 | Location |
| Relocated Lat/Lon | relocated (plate + sys), map popup | Location geometry | 2 | Location |
| Relocated UTC | relocated, profile current | Location time | 2 | Location |
| Country | relocated, city profiles | Place context | 2 | Location / City Intelligence |
| State / Province / Region | relocated ("Kansai"), comparison ("Texas, USA") | Place context | 3 | Location / City Intelligence |
| Population | relocated intel, city profiles | City scale | 3 | City Intelligence |
| Cost of Living / Monthly Cost | relocated intel, city profiles | Affordability | 3 | City Intelligence |
| Safety | city profiles, comparison CI | Livability | 3 | City Intelligence |
| Stability | city profiles | Livability | 3 | City Intelligence |
| Infrastructure | city profiles | Livability | 3 | City Intelligence |
| Climate | relocated intel, comparison CI, city profiles | Environment | 3 | City Intelligence |
| Expat Community | city profiles | Livability | 4 | City Intelligence |
| Nearest Airport / Distance | relocated (remote-only) | Remote access | 4 | Location / City Intelligence |
| Nearest Settlement / Distance | relocated (remote-only) | Remote access | 4 | Location / City Intelligence |
| Confidence Tier | app_shell | Birth-time trust | 4 (post-v1) | Profile / System |
| Chart angles (ASC/MC/IC/DSC positions) | profile, relocated, comparison, map popup | Chart facts | 1 (on chart pages) | Location (via Profile authority) |

---

## 3. Badge vs Metadata Classification

Many artifacts currently live in the wrong layer. Target layer per item:
**Badge**, **Metadata**, **Plate Content**, **Table Content**, **Tooltip Only**.

| Item | Current treatment | Target layer | Note |
|---|---|---|---|
| Natal / Current Location / Comparison (views) | Pills (profile) | **Badge** | Context badges / view switch |
| Relocated (label) | Heading text | **Context language / Plate Content** | Not a required visible badge; identify saved places by place name + favorite state + chart context. User-facing badges likely limited to Natal / Current Location. |
| Favorite state | Button + star + row highlight | **Badge** (status) + Action control | Split status badge from the toggle action |
| Shared | — | **Badge** | When/if shared views exist |
| Archived | Logic only | **Badge** | Only if archived items become visible |
| Draft | Scaffold text | **Badge** | Status badge if drafts surface |
| Active (record/place) | Context chip | **Plate Content** | Authority belongs in the plate, not a chip |
| Confidence tier | Chip + warning | **Badge** (warning) | Keep as warning, not decoration |
| Profile name | Selector / plate | **Plate Content** | Highest authority; lives in plate |
| Tropical | System sub-line / sys row | **Metadata** | Not a badge; system metadata |
| Placidus | System sub-line / sys row | **Metadata** | Same; map policy note is separate Warning |
| Sidereal / Koch | — | **Metadata** | Future system metadata |
| Birth Date / Birth Time / Birth Place | Plate sub-lines | **Plate Content** (Tier 1 identity/chart data) | Identity/chart data, NOT low-priority metadata; UTC offset is separate supporting metadata |
| Lat/Lon (birth) | Plate sub / sys | **Metadata** | Tier 3; can be tucked |
| Lat/Lon (relocated) | Plate / sys / popup | **Metadata** | Tier 2 on location pages |
| UTC offset | Plate / sys / popup | **Metadata** | Normalize format |
| Time zone name (JST) | Inline w/ UTC | **Metadata** / **Tooltip Only** | Optional enrichment |
| Country / Region | Meta block / city hero | **Metadata** | Location-owned |
| Population, Cost, Safety, Stability, Infrastructure, Climate, Expat | Snapshot cells / intel list / comparison rows | **Table Content** | City Intelligence facts |
| Nearest Airport/Settlement | Intel list (remote) | **Table Content** | Conditional metadata |
| Source / dataset note | Sys row / popup note | **Tooltip Only** | Provenance, not primary |
| Lat cap ON/OFF | Debug overlay | **Tooltip Only** (or removed) | Internal diagnostic |

Key correction: **Tropical/Placidus are metadata, not badges.** They are
currently styled like context labels but carry system-setting meaning.

---

## 4. Placement Audit

Natural placement tendencies already visible (observation, not design):

- **Above wheel / page top:** location subject (relocated), view badges (profile pills), comparison profile band. Profile/relocated keep identity above the wheel.
- **Beside wheel:** profile/natal plate, relocated side plate (place, coords, "For {profile}"). Lat/lon and "For profile" naturally sit beside the wheel.
- **Under wheel:** reference tables (PiH/AiS/A2A), relocated `sys-meta` (Birth/Relocated/System), city intelligence + notes. System metadata and intelligence gravitate below the wheel.
- **In header:** profile authority selector; account control.
- **In footer:** none meaningful (app_shell footer is scaffold quarantine).
- **In table:** all City Intelligence facts (population/cost/safety/etc.); comparison fact matrix.
- **In City Intelligence (hero/sections):** KPI snapshot, accordion livability detail.
- **In tooltip:** provenance/source, dataset notes, internal diagnostics, time-zone enrichment.
- **Hidden until expanded:** city profile accordions (`acc-row`), comparison block collapse, notes composers.

Tendency summary: **identity + subject go up/beside the wheel; system + provenance go below or into tooltips; livability facts go into tables/intelligence.**

---

## 5. Authority Hierarchy Audit

Emerging doctrine hierarchy:
1. Profile / Native
2. Chart Wheel
3. Context (Natal / Current / Relocated / Comparison)
4. Metadata

Findings vs hierarchy:

- **Follows:** `prototype_profile_workspace_v11.html` — profile selector at top, wheel central, view pills as context, metadata in plate sub-lines. Clean hierarchy.
- **Follows:** `prototype_relocated_location_v1.html` — place is subject but profile authority persists ("For {profile}", profile switcher); wheel is in the initial viewport; metadata sits below. Honors the rule that profile authority outranks location subject.
- **Partial conflict:** `map_CURRENT.html` — profile authority is a plain `#chartProfile` select buried in a side panel, while the popup leads with the clicked point. Authority is present but visually subordinate to the point; acceptable for a Micro plate but weakens the "profile is highest" cue.
- **Conflict:** comparison v2–v5 — profile band is present, but `recordType`/current-location and city tags compete; v2 `profile-strip` mixes "Who You Are / Intent" bars that imply non-profile authority. v5 is closest to correct (single profile band + city plates).
- **Conflict (vocabulary):** `app_shell.html` — uses "Active Chart Record" as authority instead of "Profile". Concept is parallel but the language diverges from product canon; scaffold-only.
- **Metadata above context:** city profiles legitimately invert (place authority, no profile), which is fine because they are not chart-bearing pages — but they must never imply chart authority.

No chart-bearing page currently lets metadata outrank the wheel or profile,
which is the most important invariant. The main risks are (a) profile authority
being visually weak on the map, and (b) Tropical/Placidus reading as context
badges rather than metadata.

---

## 6. Standardization Candidates

Recommendations only; no final lock.

### Date format
- **Variants:** "14 March 1989" (profile, relocated), "Sep 12 1985" (comparison v5), "Feb 14, 1990" (comparison v2), `<input type=date>` ISO (app_shell).
- **Recommended direction:** one human-readable canonical (e.g. "14 March 1989") for display; ISO only for inputs/storage.

### Time format
- **Variants:** "07:42", "14:15" (24h), "10:30 AM" (12h), "14:32 UTC" (time with TZ glued on).
- **Recommended direction:** pick 24h or 12h consistently for display; never glue "UTC" directly onto a local birth time.

### Lat/Lon format
- **Variants:** 2-decimal hemispheric "38.72° N, 9.14° W"; 4-decimal hemispheric "40.7128° N, 74.0060° W" (with thin space); 4-decimal raw signed in map popup "Lat 35.0116 · Lon 135.7681" (no hemisphere).
- **Recommended direction:** one canonical precision + hemispheric notation for display; keep raw signed decimals for computation/tooltips.

### UTC format
- **Variants:** "+09:00", "+00:00", "-07:00", "UTC+1", "UTC 07:42 · +00:00", "+09:00 (JST)".
- **Recommended direction:** canonical "UTC±HH:MM"; optional named TZ in parentheses; stop emitting bare "UTC+1".

### Country naming
- **Variants:** "Japan", "Portugal" (country), but comparison stores "Texas, USA" in the **country** field (state-as-country).
- **Recommended direction:** separate Country from State/Region fields; never store a state in the country slot.

### State / Region naming
- **Variants:** "Kansai" (region, relocated), "Texas, USA" (comparison), "OR USA" (profile birthplace "Portland, OR USA").
- **Recommended direction:** decide full vs abbreviated state and apply uniformly; keep region distinct from country.

### Zodiac naming
- **Variants:** "Tropical" only (no Sidereal present).
- **Recommended direction:** canonical "Tropical"; reserve "Sidereal" for future; treat as metadata.

### House system naming
- **Variants:** "Placidus" everywhere; app_shell select also "Placidus"; map policy note ties Placidus to ±65° latitude.
- **Recommended direction:** canonical "Placidus"; reserve "Koch"/others for future; treat as metadata; keep latitude policy as a separate Warning, not a system badge.

### City name + country pairing
- **Variants:** "Kyoto, Japan", "Lisbon, Portugal", "Austin, Texas, USA", "Bali, Indonesia".
- **Recommended direction:** canonical "{City}, {Country}" for display; surface admin/region separately when needed.

---

## 6a. Action-Language Standardization (required future doctrine)

Action verbs are currently used loosely across surfaces (e.g. "Edit"/"Add"
profile controls, "Add to Favorites", "Replace", "Restore", "Save", "Open chart",
"View chart"). Action-language standardization is a **required future doctrine**.

Actions needing standardization:

- Add
- Edit
- Change
- Remove
- Archive
- Restore
- Save
- Open
- View

**"Add," "Edit," and "Change" must not be used interchangeably.**

Provisional distinction (plain form):

- Add = create a new object or attach a new item.
- Edit = modify the contents of an existing object.
- Change = switch a selected setting / context / value.

Examples:

- Add Favorite
- Edit Notes
- Change Profile
- Change House System

This section names the need only; final verb mapping is deferred and remains
open (see Section 7).

---

## 7. Open Questions

Documented tensions; not resolved here.

- **State/province: abbreviation vs full name** — "Texas, USA" vs "OR USA" vs "Kansai". No rule yet; affects plates and comparison columns.
- **Country: full vs abbreviated** — currently always full, but state sometimes occupies the country field; do we ever abbreviate?
- **UTC vs local time presentation** — birth time shown both as local ("07:42") and glued to UTC ("14:32 UTC"); which is canonical for the user, and where does the offset live?
- **Time-zone naming** — show named TZ (JST) alongside offset, in tooltip only, or omit?
- **Tropical / Placidus placement** — metadata sub-line (profile), labeled sys rows (relocated), or system band (comparison)? Same data, three placements.
- **Favorite: status vs action** — one control conflates "is favorited" (status) with "toggle favorite" (action); should these separate?
- **"Current Location" vs "Relocated"** — two names for adjacent concepts (view label vs page subject vs city tag); needs one vocabulary.
- **Relocated Location as a visible badge** — kept open: should a saved/relocated place ever carry a "Relocated Location" badge, or is it always identified by place name + favorite state + chart context? Current lean: no heavy badge; user-facing badges limited to Natal / Current Location.
- **Action-verb mapping** — Add vs Edit vs Change (and Remove/Archive/Restore/Save/Open/View) are used loosely; final mapping deferred (see Section 6a).
- **Archived / Shared / Draft** — logic and intent exist without rendered badges; when they surface, what is the canonical badge treatment?
- **Confidence tier** — post-v1; is it a warning only, or also a persistent badge?
- **Lat/Lon precision** — 2 vs 4 decimals; hemispheric vs signed; per-surface or global?
- **Metadata density on mobile** — sys-meta is a 3-column grid; comparison is horizontally scrolled; how much metadata survives small screens?
- **Long-name behavior** — long city/country/region strings in sticky comparison columns and plates; truncate, wrap, or ellipsize?
- **Provenance/source** — "city_dataset", dataset notes, World Bank/Numbeo citations: tooltip-only, footnote, or City Intelligence section?
- **app_shell vocabulary** — "Chart Record" / "record type" vs product "Profile"; reconcile or keep scaffold-only?

---

## Summary of highest-value corrections

1. Reclassify **Tropical/Placidus** as metadata, not badges.
2. Unify **profile authority** presentation across Map / Profile / Relocated / Comparison (and strengthen it on Map).
3. Separate **Favorite status** from the **favorite toggle action**.
4. Normalize **date / time / lat-lon / UTC / country / state** formats.
5. Fix the **state-in-country** field misuse in comparison data.
6. Reconcile **"Current Location" vs "Relocated"** vocabulary.
7. Keep **provenance, diagnostics, and dataset notes** in tooltips/footnotes, never as primary badges.
