# Client / Chart Data Model v1

## Status

**CANONICAL** for non-AI Web 2.0 product data architecture.

**Date:** 2026-05-29  
**Scope:** Entity model, persistence boundaries, saved exploration shape, active context, and optional post-v1 behavioral capture — **documentation only**. Not SQL. Not implementation.

**Filename convention:** New dated docs put the date at the **end** of the filename (e.g. `client_chart_data_model_v1_2026-05-29.md`). Older files are not renamed by this document.

**Reads with:** `docs/ux/2026-05-29_application_journey_architecture_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/local_product_store_v2.md`, `docs/data_model/supabase_schema_sandbox_plan_v1.md`.

---

# Purpose

Define the **non-AI Web 2.0 product data model** for the relocation app, aligned with the current UX journey doctrine.

This document answers:

- what durable records exist,
- what belongs on each record,
- what must never be persisted as product truth,
- how active chart context flows through screens,
- how behavioral facts may be captured **without interpretation**,
- what is explicitly **out of scope** for the current product generation.

The model supports **exploration, refinement, evaluation, and decision-making** — not administration theater, not oracle closure, not AI-derived meaning.

---

# Core architectural boundary

```text
┌─────────────────────────────────────────────────────────────┐
│  PRODUCT RECORDS (Web 2.0 — local-first → future sync)       │
│  Account · Chart Record · Place · Favorite · SavedExploration│
│  · ComparisonSet · inline notes · History (per Chart Record) │
│  · BehavioralEventLog (post-v1 optional — not required)       │
└───────────────────────────┬─────────────────────────────────┘
                            │ references (never embeds)
┌───────────────────────────▼─────────────────────────────────┐
│  LAYER 1 COMPUTED TRUTH (API / engine — recomputable)        │
│  point truth · membership · relocated chart tables           │
└───────────────────────────┬─────────────────────────────────┘
                            │ must not persist as authority
┌───────────────────────────▼─────────────────────────────────┐
│  RENDERER / DISPLAY (ephemeral)                              │
│  GeoJSON fragments · canvas · aura · debug substrate         │
└─────────────────────────────────────────────────────────────┘
```

**Rule:** Product storage holds **intent, context, and references**. Layer 1 truth is **recomputed** on demand. Renderer output is **never** promoted to durable product truth.

---

# Terminology

| Term | Meaning in Web 2.0 |
|------|-------------------|
| **Chart Record** | Preferred neutral name for the primary user-owned natal identity + professional label. One natal chart per record. |
| **Client** | UI/product language for a Chart Record when the professional workflow treats the subject as a client. **Synonym in current scope**, not a separate entity with multiple charts. |
| **Birth profile** | Natal input domain (date, time, place, timezone). **1:1 with Chart Record** in current scope. |
| **Place** | Stable geographic identity (geoname / WOF-style ID when available + lat/lon). |
| **Saved exploration** | Durable saved search / investigation session (conditions + map context + interaction facts). |
| **Comparison Set** | 2–5 **saved places / locations** compared under **one** Chart Record — not multi-chart comparison. |
| **Active chart context** | Exactly one Chart Record selected as the map’s owner at a time. |

Long-term, **Chart Record** may supersede **Client** in schema naming where the record is not literally a paying client (research chart, self-chart). Current UI may still say “client.”

## Terminology crosswalk (storage vs product language)

| This document | Older / internal storage (v2 scaffold, SQL sandbox) |
|---------------|-----------------------------------------------------|
| **Chart Record** | User-facing **client / chart / research** record — one active natal identity per row |
| `chartRecordId` | Often `client.id` in JSON/SQL |
| Birth profile fields on Chart Record | Separate `birth_profiles` row linked by `birth_profile_id` |
| Inline `notes` on record / favorite / exploration | Canonical Web 2.0 — not a separate `notes` table yet |

**Rule:** Product language may say “client.” Data architecture treats each row as **one Chart Record** with exactly one birth profile in Web 2.0. Internal schemas may split `clients` + `birth_profiles` for normalization; do not infer multiple charts per client from that split.

---

# 1. Chart Record / client model

## Current scope (hard decision)

**One Chart Record = one natal chart = one active client/research identity.** No multiple charts inside one record in the current Web 2.0 product.

**Web 2.0 ownership rule:** Favorites, inline notes, saved explorations, map/search history, and comparison sets belong to **exactly one Chart Record**. There is no shared favorite pool, note namespace, or history bucket across records except at account settings (e.g. global defaults, clear-all-history as lower priority).

| Allowed | Not allowed (current) |
|---------|------------------------|
| One birth profile per Chart Record | Nested chart list on one client |
| Separate Chart Records for distinct natal identities | Composite chart as child of client |
| Professional display name + inline notes on the record | Rectified alternate time as sibling chart under same client |
| User-declared `confidenceTier` + optional metadata | AI-inferred birth time stored as exact time |

## Alternate charts and special cases

If the user needs a **distinct natal identity** — **research chart**, **composite chart** (future), **solar chart policy record** (future), etc. — each is created as a **separate Chart Record** (client-like row), not as a nested chart collection.

**Relocated event charts are not a Web 2.0 MVP use case.** Edge cases belong under **`record_type: research`** without event-chart product UX or storage typing. Dedicated event-chart support remains a future box only (see §11 exclusions).

**Not separate Chart Records:** birth-time uncertainty variants, rectification candidates, or bounded-range hypotheses. Those belong to **one user-facing Chart Record** as internal metadata / future internal calculation domains — see birth-time sections below. **Rectification workflow is out of scope** for Web 2.0.

**Rationale:** Keeps active context, favorites, saved explorations, and map ownership unambiguous. Avoids selector complexity and hidden chart switching in MVP.

## Chart Record fields (conceptual)

| Field | Required | Notes |
|-------|----------|-------|
| `chartRecordId` | yes | Stable ID |
| `accountId` | yes | Owning professional account |
| `displayName` | yes | Professional label (“Anna Rivera”, “Research — Solstice reference”) |
| `recordType` | yes | Web 2.0: **`self`**, **`client`**, **`research`** only — not `event` |
| `birthDate` | yes | |
| `birthTime` | yes / nullable | Nullable only with honest unknown-time or bounded-range policy — see below |
| `birthPlace` | yes | Place ref or embedded place fields |
| `timezoneId` | yes | P3-critical |
| `confidenceTier` | yes | User-declared epistemic tier (T0–T4) — **stored metadata**, not computed |
| `confidenceMetadata` | optional | Source, bounded range, notes — e.g. certificate, oral history, rectification-in-progress flag |
| `currentLocationPlaceRef` | optional | “Where I live now” for psychological comparison on chart screen |
| `notes` | optional | Record-level **inline** note (see Notes section) |
| `tags` | optional | Organization only |
| `createdAt`, `updatedAt` | yes | |

### Optional demographic / profile metadata (future only)

Optional fields such as **gender** or similar demographic profile metadata may later support **AI interpretation layers** (post–Web 2.0). They are **not required** for Dumb Web 2.0 and **must not affect Layer 1 geometry** or relocation truth computation. Do not model, require, or surface in MVP UI unless explicitly approved in a future slice.

### Birth time confidence — in scope vs excluded (Web 2.0)

| In scope (storage) | Excluded (Web 2.0) |
|--------------------|---------------------|
| User-declared `confidenceTier` | Confidence **computation** engine |
| Optional `confidenceMetadata` (range, source) | Rectification workflow automation |
| Honest display of tier on client, map, popup, comparison, export | AI birth-time **inference** stored as fact |
| Warnings when precision is assumed | Silent promotion of guess to exact time |

Aligns with `docs/future/birth_time_uncertainty_and_confidence_doctrine.md` for **recording and surfacing** tier; does not implement rectification or AI intake.

### Unknown birth time (Web 2.0)

**Unknown birth time means relocation chart cannot be run honestly.** Houses and angles are time-sensitive; the app must **not fake precision**.

When `birthTime` is unknown (e.g. tier T3):

- Do **not** present relocation overlays or point truth as authoritative without explicit solar-chart or documented policy watermark.
- Route the user to **guidance**: find birth records, ask family, obtain bounded approximate range — not to silent defaults masquerading as exact.
- Nullable `birthTime` is allowed **only** with visible tier/policy — never an invisible noon chart.
- **Very broad uncertainty** should route the user toward finding better birth-time records — not toward pretending a single exact time.

### Ambiguous / bounded birth time (future box only)

```text
┌──────────────────────────────────────────────┐
│  FUTURE: Birth-time uncertainty gradient      │
│  Post–Web 2.0 AI may support user-indicated   │
│  bounded ranges, likely centers, and internal │
│  uncertainty-gradient rendering on ONE Chart  │
│  Record — NOT v1.                           │
│                                               │
│  May involve multiple INTERNAL chart          │
│  calculations for range endpoints — must NOT  │
│  surface as multiple user-facing charts.      │
│                                               │
│  Very broad ranges → guidance to improve      │
│  birth-time records, not fake precision.      │
│  Do not design range engine or UI here.       │
└──────────────────────────────────────────────┘
```

**Explicitly omitted from Web 2.0 implementation:** confidence computation engine, rectification workflow state machine, composite chart parameters, AI birth-time inference pipeline.

## Future expansion boxes (not current features)

```text
┌──────────────────────────────────────────────┐
│  FUTURE: Multi-chart grouping (optional)      │
│  A "Case" or "Person" entity could group      │
│  multiple Chart Records (natal, research)│
│  without breaking 1:1 map ownership.           │
│  NOT in Web 2.0 UI or schema requirements.    │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  FUTURE: Internal birth-time candidates       │
│  Reserved on one user-facing Chart Record:    │
│  candidateChartDomains[] or equivalent for      │
│  bounded-range / uncertainty-gradient work.     │
│  Multiple internal calculations allowed;        │
│  ONE user-facing chart identity only.           │
│  NOT Web 2.0 — do not normalize or implement.   │
└──────────────────────────────────────────────┘
```

---

# 2. House system and Layer 2 settings

## House system (hard decision)

**House system is a global/account setting**, not per-Chart Record in current scope.

| Setting | Scope (current) | Notes |
|---------|-----------------|-------|
| `houseSystem` | Account / user settings | e.g. Placidus — one default for the professional |
| `defaultOrbs`, visible minors, helper layers | Account settings | Layer 2 |
| Per-chart house system override | **Future only** | Possible later; do not model in MVP UI or migrations as required |

**Saved explorations** snapshot Layer 2 settings at save time (`settingsSnapshot`) so replay is honest — changing account defaults does not silently rewrite past explorations.

Most astrologers use one house system consistently; global default matches that workflow.

---

# 3. Favorites

## Ownership (hard decision)

**Favorites belong to exactly one Chart Record.** There is no separate favorite list per nested chart (because nested charts do not exist in current scope).

| Field | Notes |
|-------|-------|
| `favoriteId` | |
| `chartRecordId` | Owner — required |
| `placeId` | Stable place reference |
| `displayName` | Optional user label |
| `notes` | Optional place-scoped note |
| `savedExplorationId` | Optional lineage — favorited during which exploration |
| `createdAt` | |

**Future (not implemented):** import or copy favorites from one Chart Record to another (duplicate place refs + notes). Document as possible migration/utility only.

## Favorite → map / chart (Web 2.0)

| Rule | Detail |
|------|--------|
| Ownership | Favorite belongs to its **owning Chart Record** |
| User-facing identity | In Web 2.0, that owner **is** the same user-facing client/chart record |
| Open on map | Hydrates **that Chart Record** as `activeChartRecordId` **plus** the favorite’s saved place (center / popup context) |
| Open chart view | Same owning Chart Record + place-scoped full relocated chart |
| Never | Silent switch to a different Chart Record |

---

# 4. Notes

## Simplicity rule (hard decision)

**Inline notes are canonical for Web 2.0.** Store notes on the Chart Record, favorite, saved exploration, or comparison set as **plain text fields** on those objects.

A standalone **`Note` entity / polymorphic notes table** is **deferred normalization** — do not require it for MVP persistence or UI.

Notes attach to:

1. **Chart Record** — `notes` field (general annotation), and/or  
2. **Place within a Chart Record** — inline `notes` on favorite, saved exploration, comparison column, or inspected city context.

**No separate “client note vs chart note”** hierarchy — one Chart Record, one namespace; optional place scope via which object carries the inline field.

| Web 2.0 (canonical) | Deferred |
|---------------------|----------|
| `ChartRecord.notes` | Standalone `Note[]` table |
| `Favorite.notes` | Cross-record note linking |
| `SavedExploration.notes` | Rich note types / threading |
| `ComparisonSet.notes` | |

**Future (not current):** voice capture → transcription stored in inline `notes` or `body` with `source: voice_transcript`. No separate note type system required now.

---

# 5. Saved explorations

**Primary durable inquiry object** for map discovery (Screen 2). Product language may say “saved search” or “saved exploration”; storage may use `saved_investigation` in SQL sandbox — same concept.

## Purpose

Store enough data to **reopen**, **audit**, and **understand** a search session without persisting renderer artifacts or interpretive claims.

## Required ownership

| Field | Required | Notes |
|-------|----------|-------|
| `savedExplorationId` | yes | |
| `chartRecordId` | yes | Owning chart/client |
| `createdAt`, `updatedAt` | yes | |

## Optional descriptive fields

| Field | Notes |
|-------|-------|
| `name` | Optional — auto-save may use generated title |
| `intention` / `purpose` | Optional free text — user-stated, not inferred |
| `notes` | Optional session note |
| `pinned` | Optional boolean — pin in recent list |

## Search semantics (must persist)

| Field | Notes |
|-------|-------|
| `conditions[]` | Layer 1 intent — **Web 2.0 only** (see condition naming below) |
| `notExclusions[]` | NOT / exclusion conditions — **explicit polarity**, not merged silently into positive conditions |
| `settingsSnapshot` | Layer 2 at time of search (orbs, house system, visible minors) — from **account** settings snapshot |
| `mutedLayers`, `soloLayerId` | Optional UI replay state |

### Web 2.0 search conditions (Layer 1)

| Technical condition type | Meaning |
|--------------------------|---------|
| **planet-in-house** | Planet membership in relocated house |
| **angle-in-sign** | Angle (ASC/MC/etc.) in zodiac sign |
| **aspect-to-angle** | Aspect relationship to an angle |

These names are **technically accurate** for storage and engine contracts. **User-facing labels may change later** — do not rename condition types in schema or docs until product copy is decided.

### Transit conditions — post-v1 / future box only

**Transits are not Web 2.0.** Current product conditions are planet-in-house, angle-in-sign, and aspect-to-angle only.

```text
┌──────────────────────────────────────────────┐
│  FUTURE: Transit placement / search           │
│  Post-v1. Requires date range + reference     │
│  time (+ ephemeris anchor). Persist only when │
│  engine contract exists. Not in v1 UI or      │
│  saved exploration schema requirements.       │
└──────────────────────────────────────────────┘
```

## Map context (must persist)

| Field | Notes |
|-------|-------|
| `mapCenter` | lat/lon |
| `mapZoom` | |
| `mapBounds` | optional north/south/east/west |
| `renderedRegions` | optional — semantic region ids/handles only — **never raw GeoJSON blobs** |
| `selectedRegions` | optional — user-selected subset if distinct from rendered |

## Interaction facts (should persist when unambiguous)

| Field | Notes |
|-------|-------|
| `clickedCities[]` | Place refs user explicitly inspected or clicked |
| `clickedRandomLocations[]` | Map picks without stable city ID — lat/lon + optional user label |
| `selectedCities[]` | Cities added to session context without click, when unambiguous (e.g. search bar pick) |

Store **behavioral facts** only. Example: user ran “Sun in 1st house” five times this month → store five exploration records with same condition hash — **do not** label user as “Sun-in-1st oriented” in Web 2.0.

## Explicit persistence prohibitions

**Must NOT persist** on saved exploration:

- GeoJSON fragments, canvas snapshots as canonical truth
- aura / virga / rain flags, debug substrate, renderer resolution knobs
- AI summaries, dignity scores, optimization rankings
- interpretive labels derived from repeated motifs

## Auto-save

Draft explorations may auto-save with partial fields. Auto-save **must not block** navigation (user sovereignty). `updatedAt` tracks drafts; `name` remains optional.

---

# 6. Active context doctrine

**Exactly one active Chart Record** at a time for map-attached work. Every action (search, favorite, inspect, compare, export) must resolve **which Chart Record owns it** before mutating data.

**Primary ownership unit (Web 2.0):** Chart Record is the primary ownership unit. Favorites, saved explorations, map history, notes, and selected locations belong to **one Chart Record** unless explicitly copied/imported later (future utility — not current scope).

## Entry paths

| Entry path | Active Chart Record | Additional context |
|------------|---------------------|-------------------|
| **Dashboard → map** | Account owner’s **`defaultChartRecordId`** (configured default Chart Record). **Not** “last used chart” unless explicitly decided in a later product pass. | Empty draft or user picks recent exploration |
| **Dashboard → recent exploration → map** | Exploration’s `chartRecordId` | Hydrate saved map state + conditions |
| **Chart Record page → map** | That page’s Chart Record | Resume that record’s most recent search / history / pinned maps when returning to this page |
| **Favorite → map or chart** | Favorite’s **owning Chart Record** (same user-facing client/chart record in Web 2.0) | Hydrate record **plus** favorite’s saved place |
| **Saved exploration → resume** | Exploration’s `chartRecordId` | Full saved exploration semantics + map state |
| **Comparison workspace** | Comparison Set’s **originating Chart Record** — set contains **2–5 places / saved locations**, not multiple Chart Records | Facts only — **no ranking, no interpretation** |
| **Comparison → return to map / chart page** | **Preserve originating Chart Record context** — do not silently switch records on return | Optional restore pre-compare viewport |
| **Map chart selector** | User-selected Chart Record — **explicit override only** | Becomes active map context **until changed again**. **Never silent.** |
| **Deep link** | Must include `chartRecordId` + exploration semantics | Not pixels alone |

**Account settings (conceptual):** `defaultChartRecordId` — account owner’s primary Chart Record for dashboard → map. Do not infer from session “last chart” in Web 2.0 MVP.

**Map rule:** The map always knows `activeChartRecordId`. Switching records clears or forks exploration context per product rules — never orphan favorites/notes onto the wrong record.

**Session state (conceptual):**

```text
activeChartRecordId: uuid
activeSavedExplorationId: uuid | null
activePlaceId: uuid | null   // popup / inspect context
activeComparisonSetId: uuid | null
```

Handoff to production map (`map_CURRENT.html`) remains a **future integration** — when implemented, must pass semantic active context, not shell-only placeholders.

---

# 7. Map and search history

**History is per Chart Record.** Recent map views, search runs, and inspect actions for a record belong to that record only — not a global undifferentiated log.

| Rule | Notes |
|------|-------|
| Scope | `chartRecordId` on every history row or derived from parent exploration |
| Clear UX | **Clear history** belongs in **Settings** (support route), not on the map surface |
| Primary action | **Clear this chart’s history** — scoped to active/default Chart Record |
| Secondary | **Clear all history** — account-wide; separate, lower-priority control |
| No interruption | Clearing history must not block map navigation (user sovereignty) |

History stores **behavioral facts** (viewport, conditions hash, timestamp, place refs clicked) — not interpretive summaries. Same prohibitions as saved explorations for renderer/AI/scoring artifacts.

Optional link: history entries may reference `savedExplorationId` when user explicitly saved; ephemeral history may expire or roll off by policy (implementation detail).

---

# 8. User sovereignty / interruption doctrine (data layer)

User action **always outranks** background work. Data layer implications:

| Background work | Must yield to |
|-----------------|---------------|
| Auto-save draft | Navigation, route change, explicit discard |
| Cache warming / precomputation | Pan, zoom, search, inspect, escape |
| Analytics batch flush | Click, navigation, modal close |
| Export generation | Cancel, navigate away |

**Implementation posture (when built):**

- Writes are async and debounced; never modal-block exploration
- Failed background work degrades gracefully — no silent overwrite of user edits
- `updatedAt` conflicts surface as recoverable drafts, not hard locks

Data exists to **support exploration**, not interrupt it.

---

# 9. Places and comparisons

## Place

Shared entity referenced by favorites, explorations, comparisons, and notes.

**Identity doctrine (Web 2.0):**

| Rule | Detail |
|------|--------|
| **Canonical key** | `placeId` (storage: `places[].id`) is the stable reference in favorites, saved explorations, comparison sets, and history |
| **Display only** | `displayName` is for UI — **not** a durable identity key; never use display name alone for persistence or deep links |
| **Disambiguation (long-term)** | `country_code`, `admin1`, and related country/admin fields are **required long-term** for proper place disambiguation once a geocoder / place database is chosen |
| **Current scaffold** | Minimal manual places are acceptable until geocoder strategy is decided — doctrine above still applies |
| **Out of scope now** | Do **not** build geocoder integration or a timezone place database in Web 2.0 — preserve fields and references only |

| Field | Notes |
|-------|-------|
| `placeId` | Stable ID when geocoder provides one; canonical FK target |
| `displayName`, `admin1`, `country` | Display + disambiguation — not substitutes for `placeId` |
| `lat`, `lon` | Required |
| `source` | `geocoder`, `manual`, `map_pick` |

## Comparison set (Screen 5)

**Web 2.0 comparison = 2–5 saved places / locations under one active Chart Record.** It does **not** mean multi-chart comparison columns (future professional edge case only).

| Field | Notes |
|-------|-------|
| `comparisonSetId` | |
| `chartRecordId` | **Originating / owning** Chart Record — one natal context for all columns |
| `placeIds[]` | 2–5 ordered places / saved locations — **columns are places, not Chart Records** |
| `savedExplorationId` | Optional parent |
| `notes` | Session notepad |
| `createdAt`, `updatedAt` | |

**Return doctrine:** Leaving comparison and returning to map or Chart Record page **preserves the originating Chart Record context**.

Facts only in comparison columns — **no ranking, no interpretation, no persisted “winner” or score**.

---

# 10. Analytics / behavioral event capture (post-v1 optional)

**Not required Web 2.0 scope.** The following is **future-friendly guidance only** — implement when product explicitly approves analytics storage. Web 2.0 ships without a mandatory behavioral event pipeline.

Web 2.0 stores **no interpretation layer**. If events are captured later, log **append-only facts** for audit or optional analytics — not personality labels, rankings, or AI training claims.

## Event envelope (conceptual — post-v1)

| Field | Notes |
|-------|-------|
| `eventId` | |
| `accountId`, `chartRecordId` | Context |
| `eventType` | Neutral fact name — see catalog |
| `occurredAt` | |
| `payload` | JSON — type-specific facts only |
| `sessionId` | Optional correlation |

## Example event types (facts only — optional catalog)

| `eventType` | Example payload facts |
|-------------|----------------------|
| `map_zoom` | zoom level, center, chartRecordId |
| `map_pan` | bounds, center |
| `map_focus_region` | region id or bounds hash |
| `page_time` | screen id, durationMs |
| `search_abandoned` | conditions partial, dismiss explicit only |
| `conditions_rendered` | condition ids at render time |
| `conditions_active_at_search` | condition ids at search submit |
| `city_clicked` | placeId or lat/lon |
| `favorite_saved` | placeId, chartRecordId |
| `chart_view_opened` | chartRecordId, placeId optional |
| `comparison_opened` | comparisonSetId, placeIds |
| `export_started` / `export_completed` | scope type, format |
| `exploration_pinned` | savedExplorationId |
| `condition_signature_seen` | conditionCanonicalHash, explorationId — **query may repeat; no “motif” label in UI** |

**Do not use interpretive event names** (e.g. “search_motif_repeated”, “user_preference_inferred”). Repeated condition signatures are discoverable by querying exploration records — no Web 2.0 UI or stored label required.

## Pinned map states

Optional `pinned` on saved exploration or user-owned viewport bookmarks — not algorithmic “suggested revisits.”

---

# 11. Explicit exclusions (current Web 2.0 scope)

The following are **not** part of the current product data model implementation:

| Exclusion | Notes |
|-----------|-------|
| AI interpretation | No stored AI narratives as product fields |
| Birth time confidence **computation** / rectification engine | Tier **recording** is in scope; automation is not |
| AI birth-time inference | Must not write inferred time as exact fact |
| Rectification workflow | Out of scope — not a product path in Web 2.0 |
| Bounded range / gradient birth-time rendering | Future internal property on one Chart Record — see §1 |
| Transit condition persistence + engine | Post-v1 future box — Web 2.0 uses planet-in-house, angle-in-sign, aspect-to-angle only |
| Composite chart implementation | Separate record if ever added |
| Relocated event charts as product type | Not Web 2.0 — use `research` for edge cases; no `record_type: event` |
| Marketplace | No commerce entities |
| Experiential travel course (Layer 5) | See `docs/future/layer5_experiential_education_through_travel_v1.md` |
| Multi-chart-per-client UI | No nested chart lists |
| Multi–Chart Record comparison columns | Future only — Web 2.0 compares places under one record |
| Internal birth-time candidates under one record | Future room only — §1; not multiple user-facing charts |
| Mandatory behavioral analytics pipeline | Post-v1 optional — §10 |
| Optimization / dignity scoring | No ranking fields on explorations or comparisons |
| Renderer persistence | GeoJSON, aura, canvas, debug as durable truth |

---

# Entity relationship summary

```text
ProfessionalAccount
  ├── userSettings (houseSystem global, orbs, defaultChartRecordId optional)
  └── ChartRecord[] (1:1 birth profile each)
        ├── Favorite[] (place scoped)
        ├── SavedExploration[] (conditions + map + interaction facts)
        ├── ComparisonSet[] (place shortlists)
        ├── inline notes (on record, favorite, exploration, comparison)
        ├── History[] (per Chart Record — map/search/inspect facts)
        └── BehavioralEvent[] (post-v1 optional)

Place ← referenced by favorites, explorations, comparisons, history
```

---

# Alignment with local product store v2 (Phase 3.0a)

Current scaffold (`local_product_store.py`, schema v2) already encodes:

- one `birth_profile_id` per client,
- **required** `confidence_tier` on birth profile (aligns with user-declared storage in §1),
- `saved_investigation` with `settings_snapshot`,
- client-scoped favorites,
- forbidden renderer keys in investigation JSON.

**Gaps this document adds** for future schema revisions:

- explicit NOT exclusion array on saved exploration,
- clicked/selected city facts on saved exploration,
- optional intention field,
- pinned flag,
- per–Chart Record history + settings-scoped clear,
- post-v1 optional behavioral event log,
- neutral Chart Record naming guidance,
- global house system vs per-record override policy,
- transit persistence deferred with date-range requirement when added.

Bump `storage_schema_version` when implementing — do not silently migrate.

---

# Relationship to existing docs

| Document | Relationship |
|----------|--------------|
| `docs/ux/2026-05-29_application_journey_architecture_v1.md` | **UX authority** — Screens 0–6, active context on map, saved exploration doctrine, user sovereignty. This data model implements those journeys. |
| `docs/data_model/local_first_data_objects_v1.md` | **Entity glossary** — BirthProfile, Client, Investigation, Favorite, Place. This doc tightens Web 2.0 decisions (1:1 chart, global house system, notes simplicity). |
| `docs/data_model/local_product_store_v2.md` | **Current file scaffold** — v2 JSON shape and validation rules. Implementation target for local-first persistence; align on next schema bump. |
| `docs/data_model/supabase_schema_sandbox_plan_v1.md` | **Future SQL mirror** — tables `clients`, `birth_profiles`, `saved_investigations`, `favorite_cities`, etc. Not applied; use as directional check, not live schema. |
| `supabase/migrations/*.sql` | **Not modified by this doc** — sandbox SQL authored separately; reconcile when product schema stabilizes. |

---

# Revision

| Version | Date | Change |
|---------|------|--------|
| v1 | 2026-05-29 | Initial Web 2.0 client/chart data architecture |
| v1.1 | 2026-05-29 | Doctrine corrections: confidence tier storage, unknown/ambiguous birth time, history, active context paths, inline notes, post-v1 analytics, transit deferred, terminology crosswalk |
| v1.2 | 2026-05-29 | Comparison = places under one Chart Record; favorite/map hydration; dashboard default not last-chart; birth-time uncertainty gradient box; Web 2.0 condition naming; transit future box |
| v1.3 | 2026-05-29 | Demote `event` record_type; research-only edge cases; place_id canonical doctrine; optional demographic metadata future box |

Future revisions: append date to filename (`client_chart_data_model_v2_YYYY-MM-DD.md`) or bump version segment per repo doc convention.
