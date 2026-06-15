# PROJECT_BOOTSTRAP_CANON_v1_2026-06-02

**Status:** compact operating canon for onboarding a new AI, human product manager, UX designer, or implementation agent into the Relocation Astrology / Astrological Geography platform.

**Purpose:** provide one manageable source document that explains what the product is, what it is not, how the main surfaces work, how truth is protected, how AI must behave, and what the next build path should be.

**Use this first.** The larger canon documents remain source references. This file is the practical bootstrap.

---

## 0. The First Law

**Reveal structure. Preserve judgment.**

This is the governing sentence for the whole project.

The platform exists to reveal geographical chart structure. It shows where astrological chart conditions hold across the Earth, lets the user inspect specific coordinates and cities, lets them save meaningful places and searches, and lets them compare selected locations using relocated chart facts.

The platform does **not** decide what a user should do. It does not rank cities by default. It does not declare a best place. It does not hide an optimization engine under the interface. It does not turn symbolic complexity into a single score. It does not become an AI oracle.

The software reveals structure. The human preserves judgment.

That human may be a professional astrologer, a serious self-guided user, a client exploring with an astrologer, or a lay user later supported by education and optional AI. In every case, the final act of interpretation remains human.

---

## 1. What We Are Building

We are building a serious relocation astrology geography instrument.

A person begins with a birth chart and a question about place. They may be considering a move, a long stay, a retreat, a nomadic season, a career relocation, a relationship move, or a professional consultation for a client. They are not merely asking, “What is my relocated chart in Lisbon?” They may be asking a deeper geographic question:

> Where on Earth does this chart condition happen?

The product makes that question searchable.

Instead of checking one famous city at a time, the user can select astrological conditions and see where those conditions exist on a map. They can inspect cities and arbitrary points inside those regions. They can save places worth remembering. They can save searches worth revisiting. They can compare a small set of selected places using relocated chart wheels, tables, and notes.

The core object is not the account. It is not a dashboard. It is not a ranked city list. It is not a tourist database.

The core object is a person’s chart evaluated through geography.

---

## 2. What Relocation Astrology Means Here

Relocation astrology starts with one fixed birth moment.

The planets remain where they are astronomically for that birth moment. The person is not given a new natal chart because they move. What changes by location is the local frame: the horizon, meridian, houses, angles, and relationships between planets and angles.

This means a planet may fall into a different house in a new location. A planet may become closer to an angle. The Ascendant and Midheaven signs may change. A condition that is absent in one city may be present somewhere else.

The product focuses on the relocation-specific facts that change with place:

- planets in houses;
- signs on angles;
- planets near or aspecting angles;
- exactness or proximity to angle relationships;
- inclusion or exclusion of selected conditions;
- overlaps between selected conditions.

The product should avoid cluttering relocation-specific surfaces with facts that do not change by relocation unless the user explicitly asks for broader chart context. For example, natal planet-to-planet aspects generally do not change from city to city in the same way houses and angles do. They may matter in interpretation, but they are not the primary geographic search object.

---

## 3. Natal, Current Location, and Candidate Location

Relocation work usually involves three different chart contexts.

### 3.1 Natal Chart

The natal chart is cast for the birth moment at the birth place.

It matters because it is the root chart. Relocation does not create a different person. Every relocated chart remains the same birth moment read from a different place. The natal chart anchors the person’s original symbolic structure.

### 3.2 Current Location Chart

The current location chart is the same birth moment cast for where the person lives now.

This matters because most relocation decisions are not made from the birth hospital. They are made from the life the person is already living. The current location chart shows the relocated chart structure the person is currently experiencing in their present place.

This is not generic metadata. It is a first-class chart context.

If a person is considering moving from Austin to Lisbon, the product should help them understand:

- the natal chart;
- the Austin/current-location chart;
- the Lisbon/candidate chart.

The current location chart is the “life as lived now” reference. It helps users and astrologers see what a candidate place changes, preserves, intensifies, or releases relative to the current place.

### 3.3 Candidate Location Chart

The candidate location chart is the same birth moment cast for a place the user is considering.

The candidate may be a city, a small town, a region, a coordinate from a map click, or a point inside an overlay. It is a chart instance at a location. The city name is a human label; the actual engine object is coordinate truth.

Candidate charts are studied in popups, full chart views, favorites, and comparison.

---

## 4. Why the Map Exists

The map exists because the question is geographical.

Relocation astrology conditions are not naturally a list of cities. They form fields, bands, corridors, pockets, seams, overlaps, holes, exclusions, and regions across the Earth. A city-by-city workflow requires the user to already know which cities to test. That is backwards for discovery.

The map lets the user begin with conditions instead of city guesses.

A traditional workflow might be:

1. choose Lisbon;
2. generate relocated chart;
3. choose Austin;
4. generate relocated chart;
5. choose Tokyo;
6. generate relocated chart;
7. repeat until exhausted.

This product’s workflow is:

1. choose chart conditions;
2. search the map;
3. see where those conditions hold;
4. inspect cities or coordinates inside the revealed geography;
5. save the places and searches that matter;
6. compare selected locations.

The map is not decoration. It is the instrument face.

---

## 5. What Map Overlays Mean

Map overlays show where selected chart conditions hold.

They are not fuzzy suggestions. They are not mood graphics. They are not city recommendations. They represent computed chart/geography membership or proximity under the product’s rules and settings.

Examples:

### Jupiter in 10th

A Jupiter-in-10th overlay means:

> At coordinates inside this region, this person’s relocated chart places Jupiter in the 10th house.

It does not mean “career success guaranteed.” It does not mean “good city.” It means the condition holds there.

### Venus trine Midheaven

A Venus-trine-MC band means:

> At coordinates along or inside this displayed band, Venus forms the selected trine relationship to the relocated Midheaven within the product’s aspect/orb rule.

The band expresses proximity or membership depending on the renderer and settings. Exact centerline and point inspection remain truth anchors.

### NOT Mars in 12th

A NOT Mars-in-12th condition means:

> The user has chosen to avoid or deprioritize coordinates where Mars falls in the 12th house for this inquiry.

It is not a moral judgment. It is not an alarm. It should render as calm exclusion or deprioritization, not danger theater.

### Overlap

Overlap means multiple selected conditions are true in the same geography. Overlap is often the answer, not just clutter. If Jupiter in 10th and Venus trine MC overlap outside the Mars-in-12th exclusion, that geography satisfies the positive conditions while avoiding the user’s explicit exclusion.

The app should preserve overlap as meaningful structure without implying the overlap is objectively best.

---

## 6. Point Truth, Field Truth, and Replay Truth

The system protects trust through three major truth families.

### 6.1 Point Truth

Point truth is what is true at one coordinate.

A point may be selected by clicking a city, searching for a place, clicking the wilderness, clicking the ocean, or opening a favorite. The point truth response should compute the relocated chart facts for that coordinate.

Point truth is the local authority. If an overlay appears to disagree with point truth, the overlay or renderer must be investigated. The popup or full point chart is not overridden by pretty graphics.

### 6.2 Field Truth

Field truth is where a selected condition holds across geography.

Field truth is shown as overlays: regions, bands, masks, material strips, exclusions, and overlaps. Field truth is exploratory because it represents many points across space. It must remain accountable to point truth and validation.

### 6.3 Replay Truth

Replay truth is the ability to return honestly to a saved inquiry.

A saved search must preserve the chart context, semantic variables, settings snapshot, viewport, created time, and render metadata needed to restore the inquiry. Replay truth does not mean freezing arbitrary renderer internals as product truth. It means the user can know what they searched, under which settings, for which chart, and where the map was focused.

---

## 7. The Five Layer Model

The project’s conceptual architecture has five layers. These are not academic decoration; they prevent the product from collapsing into dashboard, oracle, or visual theater.

### Layer 1 — Geometry and Factual Computation

Layer 1 owns chart/geography truth.

It includes birth data, coordinate evaluation, house system, zodiac mode, ephemeris calculations, angles, houses, truth grids, screen-space masks, exact centerlines, aspect-to-angle distances, and condition membership.

Layer 1 answers:

- What is true at this coordinate?
- Where does this condition hold?
- Is this point inside or outside this condition?
- How close is this point to exactness?

Layer 1 does not interpret. It does not decide if the condition is good.

### Layer 2 — Ontology, Vocabulary, and Settings

Layer 2 defines the structured questions users can ask.

It includes condition types, variable cards, stable IDs, labels, aspect families, orb defaults, house system options, zodiac modes, future professional dictionaries, and settings snapshots.

Layer 2 can name and configure questions. It cannot make a coordinate true or false by rhetoric. Stable IDs and structured fields outrank display copy.

### Layer 3 — Intent and Workflow Framing

Layer 3 is the human inquiry.

It includes what the user wants to move toward or away from, why a professional chose a condition set, saved search names, notes, constraints, known cities, and comparison context.

Intent matters because chart conditions are not universally good or bad. A user seeking public visibility may evaluate an angular Sun differently from a user seeking retreat. A user seeking stability may handle Saturn differently from a user seeking disruption. The product preserves this context without pretending to own the answer.

### Layer 4 — Interpretation and AI Assistance

Layer 4 is optional explanation, interpretation, educational support, AI assistance, professional assist, and future consumer intake.

Layer 4 must always be downstream of Layers 1–3. AI may explain facts, suggest alternative searches, translate human intent into proposed conditions, or summarize comparison differences. It cannot invent Layer 1 facts. It cannot decide the user’s life. It cannot quietly rank cities as product truth.

Layer 4 must label fact, interpretation, uncertainty, and user intent.

### Layer 5 — Experience and Visual Atmosphere

Layer 5 is the product’s felt surface: typography, spacing, tone, motion, palette, interaction style, map calm, drawer behavior, and visual hierarchy.

It should feel premium, restrained, contemplative, calm, and durable for long sessions. It should not feel like a SaaS dashboard, CRM, toy, neon mystical app, or analytics console.

Layer 5 must never override Layer 1. Beauty that lies is worse than rough honesty.

---

## 8. Core Product Surfaces

The product is map-first but not map-only.

### 8.1 Map

The Map finds possibilities.

It is for geographic discovery: building and running searches, seeing overlays, reading overlap, panning and zooming, inspecting points, saving cities or coordinates, and reopening Genie to modify the search.

The Map is not profile management, billing, account settings, CRM, full chart study, or city ranking.

The Map’s loop is:

1. Build Search.
2. Search Map.
3. Explore Results.
4. Optionally Modify Search.
5. Explore Results again.

After Search Map, the map should lead. Controls should quiet down. The user should feel that the product got out of the way so they can read geography.

### 8.2 Genie

Genie builds and modifies searches.

It holds variable selection, condition rows or chips, Add Variable, Search Map, Clear Map, and optionally Save Search while the Genie is open.

Genie is not profile editing. It is not client management. It is not account settings. It is not a CRM drawer.

Before search, Genie may be fuller because the user is building the inquiry. After search, Genie retracts or compresses because the map and overlays become primary. When the user reopens Genie, existing variables are visible and editable again.

### 8.3 Profile Page

The Profile Page orients the person and their charts.

It should show:

- profile/chart subject name;
- birth date;
- birth time;
- birth city;
- optional subdued technical metadata such as UTC, lat/lon, Tropical, Placidus;
- current location as a first-class city/place;
- natal chart wheel;
- current-location chart wheel;
- relevant astrology tables;
- favorites;
- saved searches;
- notes where appropriate;
- edit/add profile actions nearby but not dominant.

The Profile Page is not a dashboard, not account admin, not city evaluation, not CRM, not the main map discovery surface.

It is the study base for one chart/person.

The Profile Page is also likely to set the visual style system for the application: typography, spacing, chart rendering, premium restraint, hierarchy, and emotional tone. The map is a special-purpose instrument; the Profile Page is where the product’s designed identity becomes most visible.

### 8.4 Comparison

Comparison evaluates selected places.

The user has already found or chosen places. Comparison holds them side by side or in a structured layout so the user can study what changes by location.

Each place should show:

- city/place name;
- country/state;
- latitude/longitude;
- relocated chart wheel;
- planet-in-house table;
- aspect-to-angle table;
- angle-in-sign table;
- notes;
- optional small city information icon, clearly secondary.

Comparison must not contain default scores, ranks, “best city,” benefits panels, opportunities panels, climate scoring, AI verdicts, or tourism content as primary material.

Comparison is not a city details page. It is a relocated-chart comparison surface.

For desktop, the current preference is horizontal comparison with an option in settings/preferences to switch to vertical layout. The initial range should support roughly 2–5 cities, with design probably best around 2–3 and usable expansion up to 5.

### 8.5 Favorites

Favorites preserve places.

A favorite is a city or arbitrary coordinate the user cares about in the context of one chart/person. Favorites should include natal place and current location as anchors, then user-marked candidates.

Favorites are not a history feed. They are not every place ever clicked. They are not rankings. They are a working list of places that matter and can feed Comparison.

### 8.6 Saved Searches

Saved Searches preserve questions.

A saved search is a named inquiry: selected conditions, chart context, settings snapshot, viewport/context, and replay metadata. It lets the user return to “the question I was asking,” not merely a place.

Favorites save places. Saved Searches save inquiries.

This distinction is critical.

### 8.7 Settings

Settings administers preferences and configuration.

It may include account, billing, house system, zodiac mode, orb defaults, display preferences, professional options, history/archive management, and future AI behavior preferences.

Settings is not the product home.

### 8.8 Help / Education

Help teaches the product.

It may explain relocation astrology, map overlays, houses, angles, aspects, point truth, saved searches, favorites, comparison, current location, and professional workflow.

Help is support and education, not a daily work surface.

---

## 9. Account vs Chart Subject

The logged-in user and the chart subject are different concepts.

Example: Dave Goodman may be the logged-in account holder. Anna Rivera may be the chart/person currently being studied.

The UI must not collapse these roles.

The logged-in user belongs in the app corner or Settings context. Do not print “Account Owner” beside the name in normal UI. That is internal role language.

The chart subject belongs on the Profile Page, Map identity plate, and Comparison context.

Do not put Anna in the global chrome as if every page is her account. Do not put Dave front and center on every chart page unless Dave is the chart subject. Do not create three competing identity systems.

User-facing language should use names, places, and chart facts. Avoid internal phrases such as:

- Account Owner;
- Working Context;
- preset;
- current location preset;
- birth location preset;
- Who You Are;
- Where You Are.

Planning phrases can guide design. They should not appear as UI copy.

---

## 10. Current Location Doctrine

Current Location is not a trivial metadata field.

It is the city or coordinate where the person currently lives. The current-location chart is the relocated chart for the life they are living now.

Relocation is usually not birth place → candidate city. It is often:

1. natal origin;
2. current life;
3. possible future place.

The user may be trying to change what their current location emphasizes. They may also want to preserve something their current location supports. The current-location chart gives them a lived baseline for comparison.

On screen, Current Location should appear as a city/place name. It should not appear as “preset.” It should not be buried as technical metadata. It is a first-class analytical fact.

---

## 11. What the Product Is Not

The product is not a dashboard.

A dashboard implies widgets, feeds, metrics, recents, summaries, and account-management gravity. This product’s center is geographic discovery and chart study, not administrative telemetry.

The product is not a CRM.

Professional users may manage multiple clients eventually, but the product is not about pipeline management, client sales status, contact records, or business activity feeds. It is an astrology geography instrument with client/chart records attached, not client management with a map sticker.

The product is not a city-ranking app.

It does not score places by default. It does not say Lisbon is 92/100. It does not declare a winner. It does not rank city quality, opportunity, climate, walkability, or destiny.

The product is not a travel app.

Lifestyle, cost, politics, climate, visa, airport access, and neighborhood facts may matter later as optional city intelligence, but they are not the astrological search condition.

The product is not an AI oracle.

AI may later assist. It may not become the authority.

The product is not traditional astrocartography only.

It may include angular lines or bands, but its broader value includes house regions, angle signs, aspect-to-angle relationships, exclusions, overlap search, point inspection, saved investigations, and comparison.

---

## 12. UX Failure Modes To Avoid

Future designers and AI agents must avoid these repeated failure modes.

### 12.1 Dashboard Thinking

Do not create a home page full of cards, recents, metrics, top cities, AI insights, and engagement widgets. That centers software management instead of astrological geography.

### 12.2 CRM Thinking

Do not turn the Profile Page into a client database record. Professionals need chart sovereignty, not sales software.

### 12.3 City Ranking

Do not add scores, ranks, “best city,” “recommended city,” or “opportunity rating” to Comparison or Map by default.

### 12.4 Decorative Charts

Do not treat chart wheels as thumbnails beside admin widgets. Charts are primary artifacts. If they are too small to read, the layout is lying about what matters.

### 12.5 Internal Language Leaks

Do not show “preset,” “Account Owner,” “Working Context,” “Who You Are,” or “Where You Are” as UI copy.

### 12.6 Genie Scope Creep

Do not put profile editing, birth data management, billing, favorites archives, or client management inside Genie. Genie builds and modifies searches.

### 12.7 Louder Chrome After Search

After Search Map, controls should recede. Back/forward/pin/search/city controls can remain available, but they should quiet down so map and overlays lead.

### 12.8 Map As Blank Road Atlas

The map is not merely a blank geography surface. It is the discovery instrument for computed chart overlays.

### 12.9 Comparison As City Intelligence

Comparison should not become climate, cost, lifestyle, tourism, politics, or opportunity panels. City information may appear later as a secondary layer, not the main body.

### 12.10 Visual Polish Over Conceptual Clarity

Nice spacing cannot rescue wrong hierarchy. First decide what each surface is for. Then design.

---

## 13. Backend / Architecture Snapshot

The backend is the factual engine.

Its job is to compute, expose, validate, and preserve geographical chart-condition truth. It evaluates conditions at coordinates.

The engine begins with chart data and latitude/longitude, not city rankings. A city lookup resolves to coordinates. Arbitrary points must remain inspectable.

The backend must support:

- point truth;
- field truth;
- replay truth;
- validation truth.

Typical active or near-active capabilities include:

- relocated chart / point inspection;
- search regions;
- truth-grid region generation;
- screen-pixel truth / screen-space masks;
- classify points;
- brute-force validation grid;
- saved search objects;
- favorite locations;
- comparison sets;
- settings snapshots;
- cache keys and invalidation metadata.

Backend responses must not include “best city,” “move here,” “ideal,” “favorable verdict,” or hidden interpretation as core truth.

A cache key must include everything that can change truth or visible classification: chart identity, settings, conditions, viewport/bounds or points, substrate, zoom, resolution/block size, latitude cap policy, orb settings, and engine/render mode where relevant.

Cache is not proof. Stale cache can make wrong code look right or right code look wrong.

---

## 14. Validation Discipline

Validation is not paperwork. It is memory and trust.

Every meaningful system change needs:

1. a hypothesis;
2. a controlled test;
3. a pass/fail criterion;
4. an evidence artifact;
5. a rollback route;
6. a statement of what remains unverified.

Point popup truth is the local authority. Overlay systems must be checked against point truth. Brute-force wall validation remains the reference when optimized renderers or adaptive methods need proof.

Do not debug math, cache, frontend rendering, browser state, and UI styling at the same time. One instability source at a time.

Do not claim “complete,” “fixed,” or “validated” unless the relevant validation actually ran.

---

## 15. AI Discipline

AI may help the product and the build process, but only under discipline.

### 15.1 Product AI

Future product AI may:

- explain terminology;
- help lay users learn;
- ask about intention;
- translate human goals into proposed search conditions;
- suggest alternative searches;
- summarize factual differences in Comparison;
- assist professionals with search expansion;
- help generate reviewed client materials.

Product AI may not:

- become primary navigation;
- decide where a user should move;
- hide rankings;
- invent chart facts;
- flatten tradeoffs;
- fabricate biography;
- comfort-spin all difficulty into positivity;
- speak as a guru;
- override a professional.

### 15.2 Development AI

Development AI must:

- read the relevant files;
- state unknowns;
- identify the task type;
- isolate one instability source;
- propose the smallest reversible change;
- name exact files;
- provide validation and rollback;
- avoid fake confidence.

Development AI must not:

- invent endpoints;
- invent database schemas;
- silently migrate architecture;
- conflate cache/runtime/browser issues with math;
- create broad unrelated patches;
- claim validation that did not happen.

---

## 16. Source Library Protocol

The project now has a bounded source library. This is intentional.

Do not feed every historical document to Cursor or a new AI by default. Most old documents are archaeology, validation history, implementation detail, or superseded drafts.

Default behavior:

1. Start with this bootstrap document.
2. Add one or two task-specific canon files.
3. Do not load backend docs for pure UX work unless needed.
4. Do not load roadmap docs for active implementation unless deciding scope.
5. Do not load Codebase Dictionary unless doing concrete code work.
6. Do not load historical mockups unless reviewing mockup mistakes.

Recommended task packs:

### Product / UX / Profile Page

- PROJECT_BOOTSTRAP_CANON
- FOUNDATIONAL_CONSTITUTION
- CORE_CONCEPTS_AND_LAYERS
- INTERFACE_AND_DESIGN_CANON

### Backend / API / Persistence

- PROJECT_BOOTSTRAP_CANON
- BACKEND_ENGINE_ARCHITECTURE
- ARCHITECTURE_AND_BACKEND_CANON
- CODEBASE_DICTIONARY when exact schemas or endpoints are needed

### AI / Prompt / Governance

- PROJECT_BOOTSTRAP_CANON
- AI_SYSTEMS_AND_PROMPT_PROTOCOLS
- GOVERNANCE_AND_PROTOCOL_CANON

### Future Planning

- PROJECT_BOOTSTRAP_CANON
- FUTURE_FEATURES_ROADMAP
- SYSTEM_BOUNDARIES_AND_CANONS

### Cursor Rule

If a document is not required for the task, do not load it. Context discipline saves money and reduces contamination.

---

## 17. Current Build Path

The project should now move from doctrine generation back into controlled product execution.

### Milestone 1 — Product Shell / Orientation

Goal: make the application stop looking like a dashboard or CRM.

Surfaces:

- Map;
- Profile;
- Compare;
- Settings;
- Help.

No dashboard home as product center. No AI. No city rankings.

Acceptance check: a new user or AI can explain what each surface is for without inventing admin widgets or rankings.

### Milestone 2 — Profile Page

Goal: establish the person/chart study base and visual design language.

Must include:

- chart subject identity;
- birth facts;
- current location;
- natal chart;
- current-location chart;
- tables;
- favorites;
- saved searches;
- Compare entry;
- restrained edit/add actions.

Must not include:

- account-owner labels;
- CRM panels;
- dashboard feeds;
- scores;
- city ranking;
- map search controls;
- “Who You Are / Where You Are” labels.

Profile Page likely sets the style guide: typography, chart treatment, spacing, premium restraint, table design, and object hierarchy.

### Milestone 3 — Map Search Loop

Goal: implement and design the core loop cleanly.

Loop:

1. Build Search in Genie.
2. Search Map.
3. Overlays appear.
4. Genie and chrome quiet down.
5. Explore Results.
6. Reopen Genie to Modify Search.
7. Search again.

Acceptance check: before search, during search building, after search, and modifying search each have clear hierarchy.

### Milestone 4 — Favorites and Saved Searches

Goal: make discovery durable.

Favorites = places. Saved Searches = inquiries.

Acceptance check: the user can find something, save a place, save a search, return later, and understand the difference.

### Milestone 5 — Comparison

Goal: compare selected places using relocated chart facts and notes.

Initial desktop preference: horizontal layout, with user option to switch to vertical. Support 2–5 cities, with 2–3 as the design sweet spot.

Each city/place includes:

- name;
- country/state;
- coordinates;
- relocated chart wheel;
- planet-in-house table;
- aspect-to-angle table;
- angle-in-sign table;
- notes;
- optional small city info icon.

Must not include scores, ranks, benefits, opportunities, climate panels, or AI verdicts as primary content.

### Milestone 6 — Harmony Pass

Goal: apply the Profile Page style language back to Map and Comparison, then harmonize.

The Profile Page may generate the core style system. The Map remains a special instrument surface. Comparison inherits chart/table language. Settings and Help stay quiet.

---

## 18. Current Open Questions

These are real open questions, not failures.

1. **City intelligence boundary:** how much optional non-astrological city information belongs near candidates later, and where?
2. **Pin vs Saved Search:** Pin appears to preserve a map/investigation moment; Saved Search preserves a named inquiry. The user-facing distinction needs sharper doctrine.
3. **Multi-person relocation:** family/partner relocation may require multiple charts later; v1 likely remains one chart at a time.
4. **Intent visibility in v1:** intent matters philosophically, but its first visible implementation should remain light or deferred.
5. **Comparison entry path:** favorites-first is clean, but direct map-to-comparison may be useful later.
6. **Birth-time uncertainty:** confidence tiers and bounded search need later UX clarity.
7. **Mobile:** no mobile mockups yet; Genie/drawer behavior will need separate design.
8. **City density:** map labels need a serious strategy, possibly purchasable dataset/provider support, label-density logic by screen area, and clickable names rather than tiny bubbles.

Do not resolve these by guessing. Flag them when relevant.

---

## 19. One-Page Summary For A New Contributor

This is a relocation astrology geography platform.

It starts with a person’s birth chart and asks where selected chart conditions hold on Earth. The map is the discovery instrument: users build searches from astrological variables, run the search, see overlays, inspect points and cities, save meaningful places or searches, and compare selected locations.

The product is not a dashboard, CRM, city-ranking app, travel guide, or AI oracle. It does not tell the user where to live. It shows where the chart conditions are true and preserves human judgment.

The main surfaces are:

- **Map:** find possibilities through overlays and point inspection.
- **Genie:** build and modify searches.
- **Profile Page:** study one person/chart, including natal and current-location charts.
- **Favorites:** preserve places.
- **Saved Searches:** preserve inquiries.
- **Comparison:** study selected candidate places with relocated chart facts and notes.
- **Settings:** administer preferences.
- **Help:** teach the product.

The core law is: **Reveal structure. Preserve judgment.**

If a proposed feature, design, AI output, or backend change violates that, it is wrong no matter how polished it looks.

---

## 20. Immediate Instruction For Cursor / AI

Before designing or coding, read this document and the task-specific canon files explicitly referenced in the prompt.

Do not infer from old chat memory.

Do not browse unrelated archaeology.

Do not create new doctrine unless the user explicitly asks.

Do not propose mockups until you can explain the screen purpose, visible objects, hierarchy, and forbidden patterns in plain language.

For the next product-design sprint, focus on one surface at a time, starting with the Profile Page.


---

# Decision Capture System

Before creating new doctrine, review:

- docs/resolutions/MICRO_DECISION_LOG_v1_2026-06-02.md
- docs/resolutions/BIG_PICTURE_DEVELOPMENT_LOG_v1_2026-06-02.md

The project uses a three-layer decision hierarchy:

MICRO
→ BIG PICTURE
→ CANON

MICRO is the capture layer.

BIG PICTURE is the synthesis layer.

CANON is the stable law layer.

Chronology is authoritative.

Newer entries supersede older conflicting entries unless explicitly marked exploratory.

All durable observations should enter MICRO first.

AI systems may suggest MICRO entries automatically when product-relevant insights appear.

Do not create new doctrine when a MICRO entry is sufficient.

