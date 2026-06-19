# DIGNITIES-0: Dignities + Diffs Display Doctrine v1

**Status:** Authoritative product doctrine (capture only)  
**Date:** 2026-06-16  
**Amended:** 2026-06-16 — house-cell color-only styling (DIGNITIES-1A feedback)  
**Type:** Display / ontology doctrine — no implementation authorized by this document  
**Ticket:** DIGNITIES-0 (capture)

---

## Purpose

Define how **Dignities** and **Diffs** appear in the product: scope, labels, defaults, mutual reception, and separation from interpretive hints. No `app_shell.html` or backend changes are authorized by this capture.

---

## 1. Dignities Are Layer-2 Ontology Metadata

Dignities are **not chart truth**. They are **data-driven relationships**:

| Field | Meaning |
|-------|---------|
| planet | Celestial body |
| sign | Zodiac sign |
| relationship_type | Kind of dignity relationship |

### relationship_type values

- `rulership`
- `detriment`
- `exaltation`
- `fall`

### Engineering rule

**Do not hard-code dignity logic throughout the app.**

Dignity relationships should be sourced from data (settings presets, ontology tables, or equivalent Layer-2 configuration) — not scattered `if planet === X && sign === Y` branches across surfaces.

---

## 2. Dignities Scope

### Dignities apply only to

- PIH tables (Planet-in-House)
- PIH comparison tables
- Exports that include PIH

### Dignities do NOT appear on

- Map popup
- Map search
- Favorites
- Saved investigations
- Location search
- A2A / angle discovery
- General map overlays

### Map → chart handoff

If users want dignity context from the map, they **click through to the relocated chart** (PIH context). The map stays uncluttered.

---

## 3. Dignities UI Label and Placement

| Rule | Value |
|------|-------|
| Label | **Dignities** (not “Show Dignities”) |
| Placement | Small **footer toggle** on **PIH sections only** |
| Default | **OFF** |

---

## 4. Dignities Display Doctrine

### Default display (v1)

Group into two **families**, not four unrelated colors:

| Family | relationship_types |
|--------|------------------|
| Supportive | rulership + exaltation |
| Challenging | detriment + fall |

Do **not** use four unrelated colors by default.

### Styling target (authoritative)

- Dignity styling applies to **PIH house-result cells** (the cells showing where a planet falls in the house grid) — **not** planet name labels.
- Supportive vs challenging is conveyed through **color only**.
- **No `+` / `−` indicators**, badges, or dignity-type glyphs in the UI.
- Planet label column remains neutral typography when Dignities are ON.

### Advanced Settings (future)

Settings may later allow **separate colors/shades** for rulership, exaltation, detriment, and fall individually (per `results/114_settings_doctrine_capture_v1.md` dignities presets).

---

## 5. Mutual Reception

### Do not add

- A separate table/page toggle for mutual reception

### Future control (Settings)

If mutual reception is supported:

**Settings → “Show Mutual Reception with Dignities”**

### Display when enabled

Only when **both** mutual-reception setting **and** Dignities toggle are **ON**:

- Mutual reception may add a **minimal neutral marker** (e.g. parentheses) on or beside the relevant **house-result cell** — separate from dignity color
- Dignity state itself remains **color-driven**; MR is additive, not a second color system
- Tooltip may elaborate; **no extra clutter** on the table page

---

## 6. Diffs

### Label and placement

| Rule | Value |
|------|-------|
| Label | **Diffs** (not “Show Differences”) |
| Placement | Footer of the **first comparison table shown** (likely **AIS**) |
| Scope | Diffs affect **all comparison tables**, not only AIS |
| Default | **OFF** |

### When Diffs are ON

- **Identical** fields visually recede / very light grey
- **Differing** fields remain readable
- **No** scoring
- **No** ranking
- **No** “strength” shading in v1

Diffs are a **readability helper** for scanning comparisons — not an analytic judgment layer.

---

## 7. Dignities and Diffs Are Separate

| Feature | Role | Primary surface |
|---------|------|-----------------|
| **Diffs** | Comparison readability helper | Comparison workspace (footer on first table; applies globally) |
| **Dignities** | PIH ontology layer | PIH sections only |

**Do not colocate** Diffs next to Dignities if Dignities live in PIH footers and Diffs govern all comparison tables.

---

## 8. Interpretive Hints (Separate Future Feature)

**Do not conflate** Interpretive Hints with Dignities.

| Concept | Nature | Default |
|---------|--------|---------|
| Dignities | Traditional ontology metadata (Layer-2) | Display OFF; PIH-only |
| Interpretive Hints | Subjective guidance for decision-making | OFF (per Settings doctrine) |

Interpretive Hints copy (when enabled elsewhere):

> These are subjective interpretations intended to help decision-making and are not objective astrological facts.

---

## 9. Acceptance Criteria

Doctrine-aligned implementation means:

1. **Dignities are PIH-only** — never on map popup, search, favorites, investigations, A2A, or overlays.
2. **Diffs are global comparison-table readability** — toggled from first table footer; applies to all comparison tables.
3. **Both default OFF.**
4. **Labels are concise:** “Dignities” and “Diffs” — not “Show Dignities” / “Show Differences.”
5. **Map popup remains uncluttered** — dignity context via relocated chart / PIH only.
6. **Mutual reception is settings-gated**, not a page-level toggle; quiet inline display when enabled.
7. **Dignity logic is data-driven**, not hard-coded across surfaces.
8. **Default dignity colors** use supportive vs challenging families on **house-result cells** — not four unrelated colors; no +/- UI indicators.
9. **Interpretive Hints remain separate** from Dignities.

---

## Traceability

| Related doc | Relationship |
|-------------|--------------|
| `results/114_settings_doctrine_capture_v1.md` | Dignities presets, Interpretive Hints default OFF |
| Map / popup doctrine | Map stays canonical point truth without dignity overlay |
| Comparison workspace | AIS likely first table; Diffs footer placement |

---

## Out of Scope (This Capture)

- Implementation in UI or renderer
- Backend dignity tables or API design
- Scoring, ranking, or strength shading for Diffs v1
- Map overlay dignity experiments
