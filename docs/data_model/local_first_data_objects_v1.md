# Local-First Data Objects v1

## Status

**CANONICAL** for Phase 3 strategic product architecture.

Defines **product-layer entities**, **persistence boundaries**, and **local-first scaffold rules**. Not a database schema. Not implementation.

**Reads with:** `docs/relocation_app_product_roadmap.md` §8 (Saved Object Taxonomy, Phase 2.x), `docs/geocoder_and_city_identity_strategy.md`, `docs/constitutional/runtime_and_renderer_sovereignty.md`, `docs/product_workflows/professional_non_ai_workflow_v1.md`.

---

## Purpose

Prevent:

- renderer output becoming durable truth,
- local JSON accidentally becoming product storage,
- ambiguous “saved view” meaning,
- cache keys tied to graphics instead of semantics,
- Layer 2 settings silently rewriting Layer 1 records.

---

## Architectural boundary

```text
┌─────────────────────────────────────────────────────────┐
│  PRODUCT RECORDS (local-first → future sync)            │
│  BirthProfile, Client, Investigation, Favorite, Place   │
└───────────────────────────┬─────────────────────────────┘
                            │ references
┌───────────────────────────▼─────────────────────────────┐
│  SEMANTIC CACHE (ephemeral / scaffold)                  │
│  investigation intent + viewport scope → sampled truth    │
└───────────────────────────┬─────────────────────────────┘
                            │ hydrates (dev sandboxes only)
┌───────────────────────────▼─────────────────────────────┐
│  RENDERER / DISPLAY (never persisted as truth)            │
│  GeoJSON fragments, canvas, aura flags, debug substrate   │
└─────────────────────────────────────────────────────────┘
```

---

## Entity glossary

### ProfessionalAccount

| Field (conceptual) | Notes |
|--------------------|-------|
| `accountId` | Stable owner |
| `displayName` | Professional identity |
| `settingsRef` | Layer 2 defaults (orbs, house system, ontology pack) |
| `createdAt`, `updatedAt` | Audit |

**Future:** billing, team seats, client ACL.

### Client

| Field | Notes |
|-------|-------|
| `clientId` | Scoped to account |
| `displayName` | Professional's label |
| `birthProfileRef` | **One natal chart per client** (MVP) |
| `notes` | Professional-only |
| `tags` | Optional organization |

### BirthProfile

Natal identity record — **Layer 1 input domain**.

| Field | Notes |
|-------|-------|
| `birthProfileId` | |
| `birthDate`, `birthTime`, `birthPlace` | |
| `timezoneId`, `utcOffsetAtBirth` | P3-critical correctness |
| `confidenceTier` | See birth-time doctrine |
| `confidenceMetadata` | range, source, rectification state |
| `layer1SnapshotHash` | Optional — detect when recompute required |

**Must not store:** rendered houses, popup strings, GeoJSON.

### RelocatedChart (future durable object)

`BirthProfile` + `Place` → computed relocated state at a location.

| Field | Notes |
|-------|-------|
| `relocatedChartId` | |
| `birthProfileRef`, `placeRef` | |
| `computedAt` | |
| `pointTruthCache` | Optional memoization of API responses — not map tiles |

Phase 2.3 scope uses investigations, not standalone relocated chart records.

### Place

| Field | Notes |
|-------|-------|
| `placeId` | Stable geoname/WOF-style ID when available |
| `displayName`, `admin1`, `country` | Human disambiguation |
| `lat`, `lon` | Required |
| `source` | geocoder, manual, map pick |

**Rule:** favorites and comparisons reference `placeId`, not raw search strings.

### FavoriteCity

| Field | Notes |
|-------|-------|
| `favoriteId` | |
| `clientRef` | |
| `placeRef` | |
| `notes` | |
| `createdFromInvestigationRef` | Optional lineage |

### OverlayCondition

Semantic search atom — **Layer 1 request**.

| Field | Notes |
|-------|-------|
| `conditionId` | |
| `type` | `planet_in_house`, `angle_in_sign`, `aspect_to_angle`, `not_*` |
| `parameters` | planet, house, sign, aspect, angle target |
| `polarity` | positive search vs exclusion |
| `displayColorKey` | UI legend echo — not renderer truth |

### SavedInvestigation

**Phase 2.3 primary durable inquiry object.**

| Field | Persist? |
|-------|----------|
| `investigationId` | yes |
| `clientRef` / `birthProfileRef` | yes |
| `conditions[]` | yes — full semantic intent |
| `viewport` (center, zoom, bounds) | yes — display context |
| `layer2SettingsSnapshot` | yes — orbs/system at time of search |
| `mutedLayers`, `soloLayer` | optional — UI state |
| `title`, `notes` | yes |
| `createdAt`, `updatedAt` | yes |
| GeoJSON, canvas, renderer payload | **NO** |
| aura / virga / rain flags | **NO** |
| debug substrate, resolution knobs | **NO** |

### ComparisonSession

| Field | Notes |
|-------|-------|
| `comparisonId` | |
| `clientRef` | |
| `placeRefs[]` | Ordered shortlist |
| `investigationRef` | Optional parent context |
| `snapshotNotes` | Professional annotations |

---

## Cache object (scaffold — not product DB)

### SemanticCacheEntry

**Key composition:**

```text
hash(
  birthProfileLayer1Domain,
  conditionsCanonicalJson,
  layer2SettingsAffectingTruth,
  viewportSamplingScope
)
```

**Must NOT key on:**

- saved rendered graphics,
- aura/virga/rain output,
- debug flags,
- renderer substrate name alone.

**Value:** sanitized truth samples / hydration metadata — not production overlay registries.

Phase 2.6–2.14 scaffolds remain **dev/smoke only** until Phase 2.24 readiness contract passes.

---

## Canonical vs display geometry

| Concern | Owner | Persisted? |
|---------|-------|------------|
| House membership, angle sign, aspect exactness | Layer 1 engine / API | via point truth + grid samples |
| World wrap, seam copies, Leaflet fragments | Display adapter | **never** as canonical |
| Cusp softness, aura bands | Display heuristic | **never** as membership |
| Popup values at point | Layer 1 API | cacheable, not authoritative storage substitute |

**Forbidden:** seam surgery on canonical topology to fix cosmetics.

---

## Local-first persistence rules

### Scaffold (current)

- browser `localStorage` / local JSON files = **scaffold only**
- must be labeled in code and docs as non-product storage
- no silent promotion to account sync

### MVP target

- local-first with explicit export/import
- optional sync layer later with versioned schema migrations — **no hidden migrations**

### Migration doctrine

Every schema change requires:

1. version bump,
2. migration script or explicit wipe policy,
3. rollback instructions,
4. validation fixture update.

---

## Layer 1 vs Layer 2 in data

| Data | Layer |
|------|-------|
| Birth datetime, place, ephemeris placements | L1 |
| House system, zodiac mode | L1 compute parameter |
| Orb defaults, minor aspect visibility | L2 |
| Helper dignity layers | L2 |
| Ontology packs / plugins | L2 |
| User intention text | L3 (future) |
| Optimization scores | L4 (future) |

**Storage rule:** Layer 2 settings are snapshotted on investigations so replay is honest. Changing account defaults does not retroactively rewrite saved investigations without user action.

---

## Birth time uncertainty in data

When `confidenceTier != exact`:

- store range bounds and source,
- do **not** store fake exact times without flag,
- future: `candidateChartDomains[]` for multi-domain cache — **schema reserved, not MVP-rendered**.

See `docs/future/birth_time_uncertainty_and_confidence_doctrine.md`.

---

## Missing abstractions

1. **Schema version field** on all persisted objects
2. **Investigation replay validator** — semantic diff vs live engine
3. **Place resolution audit log** — which geocoder candidate was chosen
4. **Export bundle format** — client packet JSON schema
5. **Sync conflict policy** — local vs account authority (future)

---

## Complexity traps

| Trap | Consequence |
|------|-------------|
| Persisting GeoJSON as truth | Seam fixes corrupt astrology |
| Cache keyed on renderer | Invalidation nightmare |
| Investigation without conditions | Fake professional replay |
| Favorites without stable place IDs | Broken comparisons |
| Layer 2 settings global mutable | Silent truth drift |

---

## Validation method

Data model slices prove:

- round-trip serialize/deserialize of `SavedInvestigation`,
- replay hydrates conditions identically,
- persisted object contains **no** renderer fields (lint/ schema test),
- cache key stable across cosmetic renderer changes.

---

## Source consolidation

| Topic | Prior art |
|-------|-----------|
| Saved taxonomy | `docs/relocation_app_product_roadmap.md` §8 |
| Phase 2.3–2.24 contracts | same, §Phase 2.x |
| Place identity | `docs/geocoder_and_city_identity_strategy.md` |
| Runtime sovereignty | `docs/constitutional/runtime_and_renderer_sovereignty.md` |
| Rejected persistence | `memory_archaeology_raw/consolidated_notes/rejected_or_obsolete_approaches.md` |
