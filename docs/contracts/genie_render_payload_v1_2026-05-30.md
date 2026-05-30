# Genie Render Payload Contract v1

## Status

**CANONICAL** for the payload emitted when the Genie user presses **Search Map** (render / search submit).

**Date:** 2026-05-30  
**Scope:** Documentation / contract only. Defines shape, semantics, legacy adapter rules, and examples. Not implementation.

**Reads with:**

- `genie_SANDBOX_variable_builder.html` — current sandbox prototype and hooks
- `scripts/smoke_genie_sandbox.py` — behavioral smoke for sandbox payload hooks
- `map_CURRENT.html` — `collectSavedInvestigationConditions()` legacy map collector
- `docs/architecture/client_chart_data_model_v1_2026-05-29.md` — Chart Record ownership, saved exploration semantics

**Filename convention:** Dated contract docs put the date at the **end** of the filename.

---

# Purpose

Define the **canonical, immutable snapshot** produced at Genie render time. This payload is the **search truth** handed to the map workspace, history, pin, and (later) save flows.

The Genie editor may hold **live, mutable card state**. Render freezes that state once. Downstream systems must treat the rendered payload as authoritative for “what was searched,” not the live card DOM.

---

# Architectural doctrine

| Rule | Meaning |
|------|---------|
| **Canonical payload uses `variables[]`** | All complete search intent lives in a flat, typed variable list. No A/B/C slots in the canonical model. |
| **Legacy map compatibility is adapter-only** | Production map’s A/B/C + single aspect overlay is a **projection**, not the source of truth. |
| **Do not force Genie into old slots** | The editor is not limited to three planet-house rows. Canonical payload may exceed legacy capacity. |
| **Unlimited variables in canonical payload** | Schema has no hard cap. Current Genie editor UI may cap cards (sandbox: **12**). |
| **NOT = polarity** | Exclusion is `polarity: "exclude"` on a variable. There is **no** standalone exclusion variable type. |
| **Mute / Solo = display controls** | Layer visibility for map replay. **Not** Layer 1 search truth and **not** engine NOT semantics unless explicitly mapped. |
| **Settings owns vocabulary** | Available bodies, aspects, angles, signs, houses, date presets come from the **object registry** owned by Settings. |
| **Genie consumes registry** | Genie dropdowns and validation read registry enablement; Genie does not hardcode planet lists. |
| **Render creates immutable snapshot** | Each Search Map press produces a new payload object. Mutating cards afterward does not retroactively change prior renders. |
| **Pin and Save reference rendered payloads** | Future pin/save attach to a **render id + payload snapshot**, not live card state. (Out of scope to implement here.) |

---

# Language stability doctrine

Genie variable **types**, **category labels**, and **stored `label` strings** participate in long-lived product records (render snapshots, history, Saved Explorations). Terminology choices therefore outlive any single UI pass.

### Principles

- **Category labels should change rarely.** Variable type names, field group headings, and polarity wording are part of the product’s durable vocabulary.
- **Dropdown contents may expand through Settings.** Users may gain new bodies, aspects, or angles without a Genie redesign.
- **Registry vocabulary may expand.** New registry ids may appear; existing ids should remain stable once shipped.
- **User-created searches should remain understandable years later.** A saved “Sun in 1st house” must still read clearly after UI refreshes.
- **Saved Explorations should not become confusing because a category was renamed.** Prefer stable **type ids** (`planet_in_house`, `aspect_to_angle`) and honest **snapshot labels** at render time over live re-labeling on replay.

### Therefore

- **Prefer boring labels over clever labels.** Plain astrological language beats branded coinages in Genie and saved search copy.
- **Prefer clarity over branding.** If a label needs explanation, it is probably wrong for a category name.
- **Branding may occur through visual design, not terminology.** Color, typography, and layout carry brand; type names and field labels stay literal.

**Payload implication:** `variables[].type` and registry ids are **stable keys**. `variables[].label` is a **render-time snapshot** for human replay; do not rewrite historical labels when marketing copy changes.

---

# Top-level payload

Emitted once per successful Genie render (Search Map).

```typescript
{
  schema_version: 1,
  kind: "genie_render",
  createdAt: string,           // ISO-8601 UTC
  chartRecordId: string,       // active Chart Record at render time
  variables: Variable[],
  layerControls: {
    mutedVariableIds: string[],
    soloVariableId: string | null,
    excludeVariableIds: string[]   // ids of variables with polarity "exclude"
  },
  settingsSnapshot: {
    transitModeEnabled: boolean,
    registry: RegistrySnapshot
  },
  legacyCompatibility: LegacyCompatibilityBundle
}
```

### Field notes

| Field | Required | Notes |
|-------|----------|-------|
| `schema_version` | yes | Always `1` for this contract. |
| `kind` | yes | Always `"genie_render"`. Distinguishes from `saved_investigation`, sandbox debug kinds, etc. |
| `createdAt` | yes | Immutable render timestamp. |
| `chartRecordId` | yes | Aligns with Chart Record / client ownership in client data model. Legacy map may still emit `chart_id` inside adapter bundle only. |
| `variables` | yes | Ordered list. Includes **incomplete** cards only when the editor chooses to snapshot draft state; **default render omits incomplete cards from search truth** (see Variable status). |
| `layerControls` | yes | Display + exclude id lists. Mute/solo ids reference `variables[].id`. |
| `settingsSnapshot` | yes | Registry + transit toggle at render time — same honesty rule as saved exploration `settingsSnapshot`. |
| `legacyCompatibility` | yes | Adapter projection for legacy map / library handoff. **Must not** be treated as canonical. |

### Render immutability

- The Genie UI may keep editing after render.
- `lastRenderedPayload` (implementation detail) or history entries store a **copy** of this object.
- Re-render produces a **new** `createdAt` and may replace “active search” pointer; it does not mutate prior snapshots.

### Future references (not defined here)

- **History:** append-only log of render payload refs + map viewport facts.
- **Pin:** user-owned bookmark pointing at one render snapshot + viewport.
- **Save:** durable saved exploration embedding this payload (or a stable hash + full copy) under `chartRecordId`.

No persistence, AI, or handoff transport logic belongs in this contract.

---

# Variable object

Each card in the Genie editor maps to one variable object in `variables[]`.

```typescript
interface Variable {
  id: string;
  type: VariableType;
  polarity: "include" | "exclude";
  enabled: boolean;
  status: "incomplete" | "complete" | "disabled" | "experimental";
  label: string;
  fields: VariableFields;
}
```

### Common fields

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Stable within editor session; must be stable in rendered snapshot for layer controls and legacy cross-refs. |
| `type` | yes | One of supported types below. Empty type ⇒ `status: "incomplete"`. |
| `polarity` | yes | `"include"` (default) or `"exclude"`. Replaces separate NOT variable type and replaces `layer.not` boolean in sandbox. |
| `enabled` | yes | When `false`, variable is ignored for search truth (e.g. transit types while transit mode off). |
| `status` | yes | See status table below. |
| `label` | yes | Human-readable summary for UI/history (e.g. `"Sun in 1st house"`). May be empty for incomplete cards. |
| `fields` | yes | Type-specific payload; keys use camelCase in canonical contract. |

### Variable status

| Status | Meaning |
|--------|---------|
| `incomplete` | Type and/or required fields missing. **Excluded from Layer 1 search** on render. |
| `complete` | All required fields valid per registry. **Included in search truth** when `enabled` and polarity resolved. |
| `disabled` | Type known but gated off (e.g. transit variable while `transitModeEnabled === false`). |
| `experimental` | Complete transit variable while transit mode on; engine may no-op until transit contract exists. |

**Default render rule:** only `complete` and `experimental` variables participate in search truth. Incomplete cards may remain in `variables[]` for editor continuity but must not be silently promoted to conditions.

### Polarity (NOT)

- **NOT is not a type.** Toggling NOT on a card sets `polarity: "exclude"`.
- Exclude variables remain in `variables[]` with full `fields`.
- `layerControls.excludeVariableIds` duplicates exclude ids for fast replay (must match `polarity === "exclude"`).
- Legacy adapter may additionally project exclude variables into `notExclusions[]` (see Legacy compatibility).

### Mute and Solo (display only)

- Mute / Solo are **not** fields on the variable.
- They appear only in `layerControls.mutedVariableIds` and `layerControls.soloVariableId`.
- They affect **map layer visibility / emphasis** on replay, not whether a condition was searched.
- Aligns with client data model optional `mutedLayers`, `soloLayerId` on saved exploration — **replay UI**, not Layer 1 membership truth.

---

# Supported variable types

| Type | Transit | Web 2.0 search |
|------|---------|----------------|
| `planet_in_house` | no | yes |
| `angle_in_sign` | no | yes |
| `aspect_to_angle` | no | yes |
| `transit_through_house` | yes | experimental only |
| `transit_aspect_to_angle` | yes | experimental only |

### Explicitly excluded (not in v1 Genie)

| Excluded | Reason |
|----------|--------|
| `planet_aspect_to_planet` | Not in Web 2.0 Layer 1 search surface. |
| Masculine / feminine sign presets | Registry vocabulary only; not a variable type. |
| Element / mode sign presets | Same. |
| Standalone exclusion variable type | Use `polarity: "exclude"` on any supported type. |

---

# Field contracts

All ids are **lowercase** for bodies, signs, aspects unless angle tokens (`ASC`, `MC`, …). Houses are integers **1–12**. Dates are ISO **YYYY-MM-DD** when present.

### `planet_in_house`

```typescript
fields: {
  body: string;   // registry bodies id, e.g. "sun"
  house: number;  // 1–12
}
```

### `angle_in_sign`

```typescript
fields: {
  angle: string;  // registry angles id, e.g. "ASC"
  sign: string;   // registry signs id, e.g. "libra"
}
```

### `aspect_to_angle`

```typescript
fields: {
  body: string;    // registry bodies id
  aspect: string;  // registry aspects id, e.g. "trine"
  angle: string;   // registry angles id
}
```

### `transit_through_house`

```typescript
fields: {
  transitBody: string;
  house: number;
  datePreset: string;   // registry date_presets id
  startDate: string | null;  // required when datePreset === "custom"
  endDate: string | null;
  experimental: true;   // always true for transit types in v1
}
```

### `transit_aspect_to_angle`

```typescript
fields: {
  transitBody: string;
  aspect: string;
  angle: string;
  datePreset: string;
  startDate: string | null;
  endDate: string | null;
  experimental: true;
}
```

**Registry rule:** every `body`, `transitBody`, `aspect`, `angle`, `sign`, `house`, and `datePreset` value must exist in `settingsSnapshot.registry` with that category **enabled** at render time. Disabled registry entries invalidate completeness.

---

# Settings snapshot

```typescript
interface SettingsSnapshot {
  transitModeEnabled: boolean;
  registry: RegistrySnapshot;
}

/** Shape mirrors sandbox objectRegistry.snapshot(): category → id → enabled */
type RegistrySnapshot = Record<string, Record<string, boolean>>;
```

- **Settings** is the authority for which objects exist and default enablement.
- **Genie** reads registry at render and copies into `settingsSnapshot` so replay stays honest if account settings change later.
- Transit variables require `transitModeEnabled: true` to reach `status: "experimental"`. When false, transit cards are `disabled` and omitted from search truth.

---

# Legacy compatibility (adapter-only)

`legacyCompatibility` projects canonical `variables[]` onto the **legacy map investigation shape** used by `map_CURRENT.html` `collectSavedInvestigationConditions()` and library save handoff.

**Critical rule:** The adapter **must not** silently pretend all canonical variables were rendered by the legacy map. When canonical payload exceeds legacy capacity, the bundle must carry explicit **degradation metadata**.

### Legacy bundle shape

```typescript
interface LegacyCompatibilityBundle {
  schema_version: 1;
  kind: "saved_investigation";
  chart_id: string;                    // same value as chartRecordId (legacy key name)
  house_conditions: LegacyHouseCondition[];
  angle_sign_conditions: LegacyAngleSignCondition[];
  aspect_overlay: LegacyAspectOverlay | null;
  notExclusions: LegacyNotExclusion[];
  degradation: LegacyDegradation;
}

interface LegacyDegradation {
  canonicalVariableCount: number;
  legacyMappedCount: number;
  unmappedVariableIds: string[];
  warnings: string[];   // human-readable, e.g. "4th planet_in_house not mapped to A/B/C"
}
```

### Mapping rules (include polarity only)

Apply to variables where `status` is `complete` or `experimental`, `enabled === true`, and **`polarity === "include"`**, in **`variables[]` order**:

| Canonical | Legacy target | Limit |
|-----------|---------------|-------|
| First 3 `planet_in_house` | `house_conditions[]` slots **A**, **B**, **C** | 3 |
| First `angle_in_sign` | `angle_sign_conditions[0]` | 1 |
| First `aspect_to_angle` | `aspect_overlay` (single object) | 1 |
| `polarity === "exclude"` (any type) | `notExclusions[]` | no fixed cap in adapter contract |

**Extra canonical variables** (4th+ planet-in-house, 2nd+ angle-in-sign, 2nd+ aspect-to-angle, all transit variables) **remain only in `variables[]`**. Their ids must appear in `degradation.unmappedVariableIds`.

### Legacy record shapes (match map_CURRENT)

**House condition:**

```json
{
  "slot": "A",
  "type": "planet_in_house",
  "planet": "sun",
  "house": 1,
  "variableId": "var-1"
}
```

Adapter maps canonical `fields.body` → legacy `planet`. Optional `variableId` cross-ref recommended.

**Angle sign condition:**

```json
{
  "type": "angle_in_sign",
  "angle": "ASC",
  "sign": "libra",
  "variableId": "var-2"
}
```

**Aspect overlay:**

```json
{
  "type": "aspect_to_angle",
  "planet": "venus",
  "aspect": "trine",
  "angle": "MC",
  "variableId": "var-3"
}
```

**NOT exclusion (explicit array):**

```json
{
  "type": "planet_in_house",
  "planet": "moon",
  "house": 4,
  "variableId": "var-4",
  "polarity": "exclude"
}
```

Aligns with client data model **`notExclusions[]`** — explicit polarity, not merged into positive conditions.

### Adapter must not

- Drop unmapped variables without listing them in `degradation`.
- Collapse multiple aspect-to-angle variables into one without a warning.
- Map exclude variables into positive A/B/C or aspect_overlay slots.
- Rewrite canonical `variables[]` to fit legacy slots.

---

# Examples

## Example 1 — Sun in 1st + ASC Libra + Venus trine MC

Three include variables, no layer controls, transit off.

```json
{
  "schema_version": 1,
  "kind": "genie_render",
  "createdAt": "2026-05-30T14:22:01.000Z",
  "chartRecordId": "cr_anna_rivera",
  "variables": [
    {
      "id": "var-1",
      "type": "planet_in_house",
      "polarity": "include",
      "enabled": true,
      "status": "complete",
      "label": "Sun in 1st house",
      "fields": { "body": "sun", "house": 1 }
    },
    {
      "id": "var-2",
      "type": "angle_in_sign",
      "polarity": "include",
      "enabled": true,
      "status": "complete",
      "label": "ASC in Libra",
      "fields": { "angle": "ASC", "sign": "libra" }
    },
    {
      "id": "var-3",
      "type": "aspect_to_angle",
      "polarity": "include",
      "enabled": true,
      "status": "complete",
      "label": "Venus trine MC",
      "fields": { "body": "venus", "aspect": "trine", "angle": "MC" }
    }
  ],
  "layerControls": {
    "mutedVariableIds": [],
    "soloVariableId": null,
    "excludeVariableIds": []
  },
  "settingsSnapshot": {
    "transitModeEnabled": false,
    "registry": {
      "bodies": { "sun": true, "moon": true, "venus": true },
      "angles": { "ASC": true, "MC": true },
      "signs": { "libra": true },
      "aspects": { "trine": true },
      "houses": { "1": true }
    }
  },
  "legacyCompatibility": {
    "schema_version": 1,
    "kind": "saved_investigation",
    "chart_id": "cr_anna_rivera",
    "house_conditions": [
      { "slot": "A", "type": "planet_in_house", "planet": "sun", "house": 1, "variableId": "var-1" }
    ],
    "angle_sign_conditions": [
      { "type": "angle_in_sign", "angle": "ASC", "sign": "libra", "variableId": "var-2" }
    ],
    "aspect_overlay": {
      "type": "aspect_to_angle",
      "planet": "venus",
      "aspect": "trine",
      "angle": "MC",
      "variableId": "var-3"
    },
    "notExclusions": [],
    "degradation": {
      "canonicalVariableCount": 3,
      "legacyMappedCount": 3,
      "unmappedVariableIds": [],
      "warnings": []
    }
  }
}
```

---

## Example 2 — NOT Moon in 4th + muted Mars square ASC + solo Sun in 1st

Demonstrates polarity, mute, and solo. Search truth still includes all three complete variables; mute/solo affect replay display only.

```json
{
  "schema_version": 1,
  "kind": "genie_render",
  "createdAt": "2026-05-30T14:30:00.000Z",
  "chartRecordId": "cr_research_solstice",
  "variables": [
    {
      "id": "var-1",
      "type": "planet_in_house",
      "polarity": "include",
      "enabled": true,
      "status": "complete",
      "label": "Sun in 1st house",
      "fields": { "body": "sun", "house": 1 }
    },
    {
      "id": "var-2",
      "type": "aspect_to_angle",
      "polarity": "include",
      "enabled": true,
      "status": "complete",
      "label": "Mars square ASC",
      "fields": { "body": "mars", "aspect": "square", "angle": "ASC" }
    },
    {
      "id": "var-3",
      "type": "planet_in_house",
      "polarity": "exclude",
      "enabled": true,
      "status": "complete",
      "label": "NOT Moon in 4th house",
      "fields": { "body": "moon", "house": 4 }
    }
  ],
  "layerControls": {
    "mutedVariableIds": ["var-2"],
    "soloVariableId": "var-1",
    "excludeVariableIds": ["var-3"]
  },
  "settingsSnapshot": {
    "transitModeEnabled": false,
    "registry": { "bodies": { "sun": true, "mars": true, "moon": true } }
  },
  "legacyCompatibility": {
    "schema_version": 1,
    "kind": "saved_investigation",
    "chart_id": "cr_research_solstice",
    "house_conditions": [
      { "slot": "A", "type": "planet_in_house", "planet": "sun", "house": 1, "variableId": "var-1" }
    ],
    "angle_sign_conditions": [],
    "aspect_overlay": {
      "type": "aspect_to_angle",
      "planet": "mars",
      "aspect": "square",
      "angle": "ASC",
      "variableId": "var-2"
    },
    "notExclusions": [
      {
        "type": "planet_in_house",
        "planet": "moon",
        "house": 4,
        "variableId": "var-3",
        "polarity": "exclude"
      }
    ],
    "degradation": {
      "canonicalVariableCount": 3,
      "legacyMappedCount": 2,
      "unmappedVariableIds": [],
      "warnings": []
    }
  }
}
```

**Note:** `legacyMappedCount` counts positive legacy slots filled (1 house + 1 aspect). Exclude is tracked separately in `notExclusions`. Mute/solo do not appear in legacy investigation conditions.

---

## Example 3 — Legacy degradation (4 planet-house + 2 aspect-angle)

Canonical payload exceeds legacy map capacity. Adapter maps first 3 houses and first 1 aspect only; remainder stays canonical-only with explicit warnings.

```json
{
  "schema_version": 1,
  "kind": "genie_render",
  "createdAt": "2026-05-30T15:00:00.000Z",
  "chartRecordId": "cr_demo_degrade",
  "variables": [
    { "id": "v1", "type": "planet_in_house", "polarity": "include", "enabled": true, "status": "complete", "label": "Sun in 1", "fields": { "body": "sun", "house": 1 } },
    { "id": "v2", "type": "planet_in_house", "polarity": "include", "enabled": true, "status": "complete", "label": "Moon in 2", "fields": { "body": "moon", "house": 2 } },
    { "id": "v3", "type": "planet_in_house", "polarity": "include", "enabled": true, "status": "complete", "label": "Mercury in 3", "fields": { "body": "mercury", "house": 3 } },
    { "id": "v4", "type": "planet_in_house", "polarity": "include", "enabled": true, "status": "complete", "label": "Venus in 4", "fields": { "body": "venus", "house": 4 } },
    { "id": "v5", "type": "aspect_to_angle", "polarity": "include", "enabled": true, "status": "complete", "label": "Mars square ASC", "fields": { "body": "mars", "aspect": "square", "angle": "ASC" } },
    { "id": "v6", "type": "aspect_to_angle", "polarity": "include", "enabled": true, "status": "complete", "label": "Jupiter trine MC", "fields": { "body": "jupiter", "aspect": "trine", "angle": "MC" } }
  ],
  "layerControls": {
    "mutedVariableIds": [],
    "soloVariableId": null,
    "excludeVariableIds": []
  },
  "settingsSnapshot": {
    "transitModeEnabled": false,
    "registry": {}
  },
  "legacyCompatibility": {
    "schema_version": 1,
    "kind": "saved_investigation",
    "chart_id": "cr_demo_degrade",
    "house_conditions": [
      { "slot": "A", "type": "planet_in_house", "planet": "sun", "house": 1, "variableId": "v1" },
      { "slot": "B", "type": "planet_in_house", "planet": "moon", "house": 2, "variableId": "v2" },
      { "slot": "C", "type": "planet_in_house", "planet": "mercury", "house": 3, "variableId": "v3" }
    ],
    "angle_sign_conditions": [],
    "aspect_overlay": {
      "type": "aspect_to_angle",
      "planet": "mars",
      "aspect": "square",
      "angle": "ASC",
      "variableId": "v5"
    },
    "notExclusions": [],
    "degradation": {
      "canonicalVariableCount": 6,
      "legacyMappedCount": 4,
      "unmappedVariableIds": ["v4", "v6"],
      "warnings": [
        "planet_in_house v4 (Venus in 4) exceeds legacy A/B/C capacity",
        "aspect_to_angle v6 (Jupiter trine MC) exceeds legacy single aspect_overlay slot"
      ]
    }
  }
}
```

A legacy-only map renderer loading **only** `legacyCompatibility` will search 3 houses and 1 aspect. A Genie-aware renderer must read **`variables[]`** for full truth.

---

# Implementation notes

1. **Sandbox alignment slice (future):** `genie_SANDBOX_variable_builder.html` currently emits `kind: "genie_sandbox_render"`, `generatedAt`, `planet` field names, `layer.not`, type id `transiting_aspect_to_angle`, and nests adapter output under `normalized.legacy_compatible` without `degradation`. Implement contract v1 in sandbox as a focused migration; update `smoke_genie_sandbox.py` accordingly.

2. **Adapter function:** Implement `buildLegacyCompatibility(variables, chartRecordId)` as a pure function from canonical payload → legacy bundle. Map `body` → legacy `planet`, `transitBody` → legacy `planet` in transit records when transit engine exists.

3. **Render gate:** Search Map should be disabled while any card is `incomplete`, matching sandbox gating (Add blocked until all complete). Payload may still expose `normalizePayload()` for debug.

4. **Editor cap vs schema:** Keep `MAX_VARIABLES = 12` as UI constant; do not encode in `schema_version`.

5. **Saved exploration embedding:** When save is implemented, persist full `genie_render` payload (or `variables[]` + `settingsSnapshot` + `layerControls`) on saved exploration; store `legacyCompatibility` only as optional cache for old map paths.

6. **Smoke coverage:** Extend smoke to assert `kind`, `polarity`, `body`/`transitBody`, `degradation` when sandbox adopts v1.

7. **Handoff:** Map shell transport (URL params, postMessage) should carry a **render payload id** or compressed canonical JSON — not legacy slots alone. Out of scope for this doc.

---

# Open questions

| # | Question |
|---|----------|
| 1 | Should incomplete cards appear in `variables[]` on render at all, or only complete/experimental? Sandbox currently clones all cards; contract allows both with default omit-from-search rule. |
| 2 | When solo is active, does replay hide non-solo layers entirely, or dim them? Display semantics only — not search truth. |
| 3 | Should `label` be user-editable or always derived from fields + polarity? |
| 4 | Exact `notExclusions[]` engine semantics on legacy map — does NOT exclude regions from union, or filter after compute? Engine contract TBD. |
| 5 | Transit variables in canonical payload when backend has no transit engine: strip at render, or emit `experimental` and no-op with UI watermark? |
| 6 | Stable `renderId` (uuid) in addition to `createdAt` for pin/save deduplication? |
| 7 | Registry snapshot: full catalog vs enabled-only map — sandbox uses enabled-only; confirm Settings export shape. |
| 8 | Rename path: `transiting_aspect_to_angle` → `transit_aspect_to_angle` in UI type menu and payload for consistency. |

---

# Explicit non-goals

- Defining map renderer GeoJSON, aura, or backend classify request bodies
- Store v3 / Supabase schema migration
- App shell or map handoff URL contract
- History list UI, pin chip behavior, or save-to-library workflow
- AI interpretation of variables or natural-language card entry
- Planet-aspect-to-planet, sign presets, or rectification domains
- Committing or modifying production files (`map_CURRENT.html`, backend, Store v3)
- Requiring legacy map to consume unlimited variables without a Genie-aware code path

---

# Cross-reference summary

| Source | Relationship |
|--------|--------------|
| `client_chart_data_model_v1` | `chartRecordId`, `settingsSnapshot`, `notExclusions[]`, saved exploration ownership |
| `map_CURRENT` `collectSavedInvestigationConditions` | Legacy adapter target (3 house slots, 1 angle sign, 1 aspect overlay) |
| `genie_SANDBOX_variable_builder.html` | Prototype; precedes this contract in several field names |
| `smoke_genie_sandbox.py` | Validates sandbox hooks; will need revision when sandbox adopts v1 |
