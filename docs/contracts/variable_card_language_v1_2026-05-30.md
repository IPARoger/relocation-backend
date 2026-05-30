# Variable Card Language Contract v1

## Status

**CANONICAL** for Genie variable-card **user-facing language** — labels, shorthand, dropdown copy, and presentation tokens.

**Date:** 2026-05-30  
**Scope:** Documentation / contract only. Defines a modular language layer. **Not final branding.**

**Reads with:**

- `docs/contracts/genie_render_payload_v1_2026-05-30.md` — stable type ids, `variables[].label` snapshots, language stability doctrine
- `genie_SANDBOX_variable_builder.html` — current sandbox labels (prototype; not authoritative for copy)
- `docs/architecture/client_chart_data_model_v1_2026-05-29.md` — Saved Exploration replay honesty

**Filename convention:** Dated contract docs put the date at the **end** of the filename.

---

# Purpose

Define the **user-facing language system** for Genie variable cards so that:

- Copy can evolve without breaking **payload type ids**, **registry ids**, or **renderer logic**
- Saved Explorations remain readable when category labels change
- Beta can ship with **boring, obvious** wording while leaving room for visual polish later

This document governs **presentation language only**. It does **not** define search semantics, engine contracts, or persistence schema (see Genie Render Payload Contract v1).

---

# Core doctrine

| Principle | Meaning |
|-----------|---------|
| **Stable IDs are canonical** | `planet_in_house`, registry ids (`sun`, `ASC`, `trine`), and payload fields are the source of truth — never derived from display strings. |
| **Labels are presentation** | Category names, separators, and shorthand are swappable skin over stable ids. |
| **User-facing labels must be modular / configurable** | UI reads from a language registry (or equivalent config), not string literals scattered in renderers. |
| **Do not hardcode final naming into payload semantics** | Payload stores `type` + ids + optional snapshot `label`; it does not store “Planet → House” as a semantic key. |
| **Dropdowns teach the meaning** | Field selectors carry explanatory copy (e.g. “Ascendant (ASC)”). Category labels only need to be **clear enough for beta**. |
| **Prefer boring and obvious over invented vocabulary** | “Planet in House” beats neologisms. Aligns with Language Stability Doctrine in render payload contract. |
| **Avoid marriage to any one separator today** | Slash, dash, dot, star, and arrow are **style tokens**, not architectural commitments. |

---

# Canonical internal type IDs

These ids are **fixed** for payload, storage, and renderer routing. Display labels must not replace them.

| Type id | Layer | Notes |
|---------|-------|-------|
| `planet_in_house` | natal / relocation | Web 2.0 core |
| `angle_in_sign` | natal / relocation | Web 2.0 core |
| `aspect_to_angle` | natal / relocation | Web 2.0 core |
| `transit_through_house` | transit | Experimental; gated by Settings |
| `transit_aspect_to_angle` | transit | Experimental; gated by Settings |

**Sandbox note:** prototype may still expose `transiting_aspect_to_angle`; canonical id is `transit_aspect_to_angle` per render payload contract.

---

# Language registry concept

Genie UI (and future theme packs) consume a **card language registry** — a small config object separate from object vocabulary registry (bodies, signs, aspects).

```typescript
type SeparatorToken = "/" | "-" | "·" | "✦" | "→";

interface CardLanguageRegistry {
  /** Style token applied when composing compound category labels */
  separatorToken: SeparatorToken;

  /** Category labels in type picker and card headers (Configuration Mode) */
  labels: {
    planet_in_house: string;
    angle_in_sign: string;
    aspect_to_angle: string;
    transit_through_house: string;
    transit_aspect_to_angle: string;
    /** Group heading for transit types in type menu */
    transit_group: string;
  };

  /** Primary action button (Genie footer) */
  primaryAction: string;

  /** Polarity / layer control copy (may be icon-only in compact UI) */
  polarity?: {
    include: string;
    exclude: string;   // UI may show "NOT" as shorthand
  };

  /** Exploration Mode shorthand formatter hooks — implementation-defined */
  shorthand?: ShorthandRules;
}
```

### Composition rule

Compound labels may be built from a template, e.g.:

```text
{leftLabel} {separatorToken} {rightLabel}
```

Examples with `separatorToken: "·"`:

- `Planet · House`
- `Angle · Sign`
- `Aspect · Angle`

Templates are **presentation**. Payload continues to store `type: "planet_in_house"` regardless of whether the card header reads “House Placement” or “Planet / House”.

### Registry ownership

| Registry | Owner | Contents |
|----------|-------|----------|
| **Object registry** | Settings | Bodies, angles, signs, aspects, houses, date presets — ids + enablement |
| **Card language registry** | Product / theme layer | Category labels, separator token, button copy, shorthand rules |

Genie **consumes both**. Neither registry belongs in renderer GeoJSON or backend classify payloads.

### Snapshot rule (Saved Explorations)

On render (Search Map), copy the **resolved display strings** into `variables[].label` (and any card-level category label if stored). If `CARD_LANGUAGE_REGISTRY` changes later:

- **Ids remain valid** for engine replay
- **Snapshot labels** preserve what the user saw at save time
- Optional: re-derive labels from ids for live UI only — never overwrite stored snapshots silently

---

# Beta display label candidates

Category labels are **not finalized**. Below are **candidates for user testing**, not commitments.

### `planet_in_house`

| Candidate | Notes |
|-----------|-------|
| Planet / House | Clear; slash reads as “two fields” |
| Planet - House | Neutral |
| Planet · House | Soft separator; good beta default |
| Planet ✦ House | Decorative; brand-forward |
| Planet → House | Directional; may feel aggressive for daily use |
| House Placement | Semantic paraphrase; hides “planet” in category name |

### `angle_in_sign`

| Candidate | Notes |
|-----------|-------|
| Angle / Sign | Clear |
| Angle - Sign | Neutral |
| Angle · Sign | Soft |
| Angle ✦ Sign | Decorative |
| Angle → Sign | Directional |
| Angle Sign | Minimal; relies on dropdowns for teaching |

### `aspect_to_angle`

| Candidate | Notes |
|-----------|-------|
| Aspect / Angle | Clear |
| Aspect - Angle | Neutral |
| Aspect · Angle | Soft |
| Aspect ✦ Angle | Decorative |
| Aspect → Angle | Directional |
| Planetary Aspect | Emphasizes body; angle field in dropdown |
| Angle Aspect | Emphasizes angle target |

### Transit group (type menu heading)

| Candidate | Notes |
|-----------|-------|
| Relocated Transits (Experimental) | **Preferred beta** — honest, scoped |

Individual transit type labels may reuse separator pattern, e.g. `Transit · House`, `Transit · Aspect · Angle`, or stay fully spelled out in beta.

---

# Separator direction (current preference)

| Preference | Rationale |
|------------|-----------|
| **Prefer** `/`, `-`, `·`, or `✦` over `→` for beta | Arrows imply direction, sequence, or causality the product does not assert |
| **Do not decide final separator now** | Treat as `separatorToken` in language registry |
| **Arrow remains available** | Visual testing may prove it works in compact Exploration rows — not ruled out, just not default |

**Recommended beta token:** `·` (middle dot) — readable, calm, non-directional, works in long and short labels.

**Alternate beta token:** `/` — maximally obvious “two-part field” semantics for Configuration Mode.

---

# Dropdown label doctrine

Dropdowns carry **teaching weight**. Category labels can stay short because options are explicit.

### Angles (preferred beta pattern)

| Display label | Internal value |
|---------------|----------------|
| Ascendant (ASC) | `ASC` |
| Descendant (DSC) | `DSC` |
| Midheaven (MC) | `MC` |
| Imum Coeli (IC) | `IC` |

### General rules

- **Display:** fuller names where helpful for lay and professional users
- **Storage / payload:** stable uppercase angle tokens (`ASC`, `DSC`, `MC`, `IC`)
- **Bodies, signs, aspects:** follow object registry `label` fields; may add parentheticals when ambiguous (e.g. “North Node (☊)” — optional, not required for beta)
- **Houses:** numeric 1–12 with optional ordinal copy in tooltip (“1st house”) — internal value remains integer

Never persist dropdown display strings as semantic keys. Persist registry ids only.

---

# Configuration Mode vs Exploration Mode

| Mode | Language role |
|------|-----------------|
| **Configuration Mode** | Full category labels, field labels, dropdown teaching copy, date controls for transit |
| **Exploration Mode** | Compact shorthand on cards and overlay-control rows; Genie may collapse or dock |

### Exploration shorthand (examples)

Long-form labels in Configuration; collapsed Exploration uses **compact symbolic shorthand**:

| Variable | Shorthand example |
|----------|-------------------|
| Sun in 1st house | `☉ 1H` |
| ASC in Aries | `ASC ♈` |
| Venus trine MC | `♀ △ MC` |
| NOT Moon in 4th | `NOT ☽ 4H` |

Shorthand rules are **presentation** — implement via `shorthand` formatters keyed by `type` + registry ids. Glyph availability may fall back to text (`Sun 1H`) when fonts or accessibility settings require.

**NOT prefix:** indicates `polarity: "exclude"` in shorthand; not a separate variable type.

---

# Overlay and map surface doctrine

The map is a **symbolic field**, not a label canvas.

### Do

- Keep regions visually clean — color, opacity, and boundary carry meaning
- Put readable detail in **Genie**, **collapsed overlay controls**, **popups**, **chart pages**, **Saved Explorations**, and **exports**
- Use **small color swatches** tied to variable type or user-assigned track color

### Do not

- Stamp variable labels directly onto map regions at zoom levels where clutter accumulates
- Use full-card rainbow backgrounds as the primary type indicator — color belongs in **swatches** and restrained accents

### Collapsed overlay-control row (Exploration Mode)

Each active variable may appear as a compact row:

| Element | Purpose |
|---------|---------|
| Small color swatch | Layer identity without map clutter |
| Shorthand label | e.g. `☉ 1H`, `NOT ☽ 4H` |
| Mute toggle / icon | Display control — not search truth |
| Solo toggle / icon | Display control — not search truth |
| NOT / exclude toggle / icon | Sets `polarity: "exclude"` on the variable |

Aligns with render payload: mute/solo in `layerControls`; exclude via polarity + `excludeVariableIds`.

---

# Button language

### Adopted for beta

| Control | Label |
|---------|-------|
| Primary Genie action | **Search Map** |

Invoked on press: emit Genie Render Payload v1 snapshot and hand off to map search/render pipeline.

### Deferred alternatives (not beta)

| Label | Why deferred |
|-------|--------------|
| Create Map | Poetic; may imply the map does not already exist |
| Find Regions | Accurate but wordy; “regions” is internal |
| Show Regions | Passive; understates search intent |
| Draw | Tool-like; suggests manual geometry |
| Go | Too vague |
| Render | Too technical for lay users |

### Rationale summary

- **Search Map** is generic, honest, and safe for beta — describes user intent without exposing implementation
- **Render** belongs in dev panels and logs, not primary CTA copy
- Final marketing pass may revisit copy **without** changing payload `kind` or button hook ids if hooks are named neutrally (e.g. `searchMap`, not `renderBtn`)

---

# Transit language

| Rule | Detail |
|------|--------|
| Group label | **Relocated Transits (Experimental)** |
| Default | **Disabled** — transit variable types unavailable until user opts in |
| Explanation | **?** control opens modal; do not hide experimental status |
| Vocabulary | Transit bodies, aspects, date presets from **Settings object registry** when enabled |
| Policy | **Do not decide transit-node policy here** (e.g. mean vs true node) — Settings / engine contracts |

Transit card labels should include experimental signaling in Configuration Mode; shorthand rows may use muted styling consistent with sandbox transit card treatment.

---

# AI assist (future only)

Not in beta scope. Documented to constrain future layers.

| Rule | Detail |
|------|--------|
| Role | AI may **generate or pre-populate** variable cards — suggestions only |
| Sovereignty | AI does **not** replace the Genie; user edits every card |
| Inspectability | Suggestions must be **inspectable, editable, acceptable, and rejectable** |
| Epistemic frame | **AI may propose; the map reveals** — no premature verdicts |
| Output shape | Proposals must compile to normal variable objects (stable type ids + registry ids), never opaque “search intent” blobs |

AI-generated labels follow the same snapshot rules: once accepted and rendered, labels freeze in the payload.

---

# Relationship to render payload

```text
┌─────────────────────────────┐
│  CARD_LANGUAGE_REGISTRY     │  presentation (this contract)
│  labels · separator · CTA   │
└──────────────┬──────────────┘
               │ composes UI copy
┌──────────────▼──────────────┐
│  Genie variable cards       │  live editor state
└──────────────┬──────────────┘
               │ Search Map
┌──────────────▼──────────────┐
│  genie_render payload       │  stable type ids + registry ids
│  variables[].label snapshot │  + optional display snapshot
└─────────────────────────────┘
```

---

# Explicit non-goals

- Final brand voice, marketing taglines, or logo-adjacent coinages
- Map renderer label stamping or GeoJSON property naming
- Object registry catalog contents (bodies list) — Settings domain
- Backend or Store v3 schema
- Smoke test assertions on copy strings
- Transit engine semantics or date-range computation
- AI prompt design or model selection

---

# Open questions

| # | Question |
|---|----------|
| 1 | Single global `separatorToken` vs per-type override (e.g. `House Placement` without separator)? |
| 2 | Should `variables[].label` store full sentence (“Sun in 1st house”) or composed category + fields separately for i18n? |
| 3 | Shorthand glyph set: standard astro Unicode vs text fallback policy for accessibility? |
| 4 | Should “NOT” appear as word, strikethrough, or red badge in Exploration rows? |
| 5 | Is `Planetary Aspect` or `Aspect · Angle` clearer for `aspect_to_angle` in professional mode? |
| 6 | Transit type labels: prefix “Transit” on each card vs group-only heading? |
| 7 | Button hook id: rename sandbox `renderBtn` → `searchMapBtn` during implementation slice? |
| 8 | Language registry versioning: store `languageRegistryVersion` in render payload for replay debugging? |

---

# Cross-reference summary

| Document | Relationship |
|----------|--------------|
| `genie_render_payload_v1_2026-05-30.md` | Stable ids, `label` snapshots, language stability doctrine |
| `client_chart_data_model_v1_2026-05-29.md` | Saved Exploration durability and settings snapshots |
| `genie_SANDBOX_variable_builder.html` | Prototype uses “Render”, `transiting_aspect_to_angle`, hardcoded type labels — pre-contract |
