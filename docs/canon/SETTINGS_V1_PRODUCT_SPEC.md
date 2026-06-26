# SETTINGS_V1_PRODUCT_SPEC.md

**Status:** Canonical V1 Settings product specification.  
**Version:** V1 (2026-06-27)  
**Type:** Product spec — not an implementation spec, not a visual redesign brief.  
**Authority:** Subordinate to `FOUNDATIONAL_CONSTITUTION.md`, `INTERFACE_AND_DESIGN_CANON.md`, `UI_STANDARDIZATION_CANON_v1_2026-06-12.md`, and `MATERIAL_SYSTEM_CANON.md`.  
**Companion audits:** `results/262_settings_harmonization_audit.md`, `results/273_product_owner_comparison_settings_notes_audit.md`  
**Revision policy:** Binding product decisions live here. Implementation tickets wire to this doc; do not re-litigate settled V1 choices in slice audits.

**Purpose:** Stop repeated rediscovery of Settings decisions. This document is the authoritative V1 Settings product spec for Beta and the first public release wave.

---

## 0. Enduring guidance

> **Every visible control must tell the truth.**

Settings is an administrative reading surface in the same instrument family as Profile, Comparison, and Notes. V1 preserves the **current excellent Settings visual language** — stone/paper cards, calm density, serif section authority. **Do not redesign** Settings chrome while wiring controls.

**Control truth law (binding):** No decorative switches. Every visible setting must either:

- affect **calculation**,
- affect **rendering**,
- affect **saved-object behavior**,
- affect **export**, or
- be **honestly marked SOON / disabled**.

Do not ship beautiful fake controls.

---

## 1. Scope — what Settings V1 is

| In scope | Out of scope (V1) |
|----------|-------------------|
| Astrology calculation & display preferences with real backend keys | Speculative house-system menus beyond engine support |
| Planet & body visibility (simple model) | Subjective orb presets (Strict / Normal / Generous) |
| Aspect visibility & orbs (planet-list model) | Triplicity, terms, face, dignity scoring / weighting |
| Late-house planet alert (single control) | Three-category late-house breakdown |
| Dignities presets + custom editor (four types only) | Glyph library implementation before asset catalog |
| Visual palette defaults (overlay, aspect, dignity, A/S, glow) | Export wizard / templates as primary Settings UI |
| Saved-object management surfaces | AI sorting, weighted ranking, “best match” |
| Composite chart creation (low prominence) | Map circle styling as final visual language |

---

## 2. Sort options (binding)

**Sort options are ONLY:**

1. **A–Z**
2. **Recently Added**
3. **Recently Viewed**
4. **Distance**

**Explicitly excluded from V1:**

- Weighting, ranking, or “best match”
- AI sorting or relevance scoring
- Extra sort dimensions or compound sort UI

Any list in Settings or saved-object management that offers sorting must use this closed set (plus honest “not sortable” when N/A).

---

## 3. Orbs (binding)

### 3.1 Presentation model

- **List aspects like planets** — one row per aspect.
- Each row: **show checkbox** + **numeric orb box**.
- **Defaults are visible and editable** — no hidden resolver-only values without UI.

### 3.2 Defaults & gating

| Group | V1 behavior |
|-------|-------------|
| **Major aspects** | Visible by default; editable orbs |
| **Minor aspects** | Gated under **“Minor Aspects (Advanced)”** collapsed section |
| **Custom orbs** | Gated under **“Custom Orbs (Advanced)”** collapsed section |

### 3.3 Excluded

- **No subjective presets** — Strict, Normal, Generous, or equivalent mood-based orb bundles are **not** V1 product.

---

## 4. Late-house planets (binding)

- **One setting only:** **Late-house planet alert**
- **Default orb:** **2°**
- **Retrograde case is implied** in the alert behavior — no separate retrograde toggle in V1
- **No three-category breakdown** (e.g. early / exact / late buckets as separate user-facing controls)

---

## 5. Aspects (binding)

| Setting | V1 default | Notes |
|---------|------------|-------|
| **Include aspects to asteroids** | User toggle | Calculation/rendering when wired |
| **Include out-of-sign aspects** | **OFF** | User may enable |
| **Include aspects to angles in chart wheel** | **ON** | Wheel rendering |
| **Applying / separating** | Appearance / color only | **Not** a calculation checkbox — color encodes motion where engine already classifies |

---

## 6. Dignities (binding)

### 6.1 Section

Dignities receive a **dedicated Settings section** — not buried in Appearance stubs.

### 6.2 Presets

| Preset | Example (Pisces) |
|--------|------------------|
| **Ancient** | Jupiter rules Pisces |
| **Modern** | Neptune rules Pisces |
| **Hybrid** | Jupiter + Neptune rule Pisces |
| **Custom** | Opens dignity editor |

Show **examples** inline so users understand preset semantics before selecting.

### 6.3 Custom editor

- Editor shows **12 signs** and **planets as needed**
- **“Add dignity”** affordance for custom rows
- **Supported dignity types only:**
  - Ruler
  - Detriment
  - Exaltation
  - Fall

**Excluded:** triplicity, terms, face, weighting, scoring, or any UI that encourages dignity weights.

### 6.4 Colors

| Mode | Rule |
|------|------|
| **Default** | One color family for **Ruler + Exaltation**; one color family for **Detriment + Fall** |
| **Advanced** | May split all four dignity types into separate colors |

Link dignity colors to the broader visual palette (§8).

---

## 7. Planet visibility (binding)

- **Keep simple.**
- **Chart** vs **overlays/tables** may be separated **only if already useful** in production — do not invent new independent matrices for V1.
- Do not overcomplicate into many independent visibility grids.

---

## 8. Visual palette (binding)

Related color families should govern:

- Overlay colors
- Aspect colors
- Dignity colors
- Applying / separating colors
- Chart inner glow
- **Search Map / pinwheel** language

**Pinwheel direction (product):** optimistic, primary, exploratory — **not** muted, autumnal, or “art-student.”

**Map circles:** existing map circle treatments are **placeholders**, not final visual language. Settings palette work must not cement placeholder map styling as canon.

---

## 9. Glyphs (binding)

- **Do not use emoji** for astrological glyphs in Settings or anywhere in the instrument.
- Use **actual glyph assets / SVGs**.

**Future glyph audit** may ingest uploaded ZIPs and classify reasonable alternatives. Known alternatives to catalog (not implement until assets are indexed):

| Body / sign | Alternatives |
|-------------|--------------|
| Mars | Alternate = upside-down Venus |
| Uranus | Multiple historical glyph forms |
| Pluto | PL monogram vs glyph forms |
| Capricorn | Variant goat/fish-tail forms |

**Do not implement** a glyph picker library until assets are cataloged.

---

## 10. Saved object management (binding)

Settings **must** provide management surfaces for:

| Object type | Management |
|-------------|------------|
| Saved Searches | Rename · Archive · Tag/Folder (where applicable) · Delete · Bulk Delete |
| Saved Comparisons | Same |
| Favorites | Same + **folders/labels** |
| Notes | Same |
| Birth Profiles | Same |

### Actions (all applicable types)

- **Rename**
- **Archive**
- **Tag / Folder** (where applicable)
- **Delete**
- **Bulk Delete** — with **irreversible warning**

### Favorites & Profile

- Favorites support **folders/labels**.
- **Profile page** should surface folders/labels **without cluttering** the page — management depth lives in Settings; Profile shows summary affordances only.

### Sorting in management lists

Use only the four sort options from §2.

---

## 11. Composite charts (binding)

- **Available but not prominent** in V1.
- **“Create Composite”** may live in **Settings** and/or **Profile management** — not primary nav hero.
- User selects **two or more existing birth profiles**.
- Result creates a **NEW profile / chart record** — **do not** clog or mutate existing profiles in place.

---

## 12. Export (binding)

- **Export templates / wizard do NOT belong primarily in Settings.**
- Export is a **workflow at export time** (contextual to the object being exported).
- Settings may eventually hold **export defaults only** — not the wizard UI.

---

## 13. Implementation sequence (after canon)

1. **Add ready settings first** — wire controls that already have resolver keys and consumers ([262](results/262_settings_harmonization_audit.md) parity table).
2. **Preserve** current Settings visual language — no redesign pass.
3. **Do not add** speculative complexity beyond this spec.
4. **Mark SOON** or **disable** anything not yet wired — per Control truth law (§0).
5. **Remove or gate** decorative controls identified in PO audit ([273](results/273_product_owner_comparison_settings_notes_audit.md)).

Suggested wiring order (product, not sprint mandate):

| Phase | Focus |
|-------|-------|
| **S1** | Orb & aspect rows (§3, §5) — replace stub panels |
| **S2** | Late-house alert (§4) |
| **S3** | Dignities section (§6) |
| **S4** | Saved-object management (§10) |
| **S5** | Planet visibility simplification (§7) |
| **S6** | Palette defaults (§8) — coordinate with map placeholder replacement |
| **S7** | Composite creation entry (§11) |
| **S8** | Glyph catalog + picker (§9) — **after** asset audit |

---

## 14. Relationship to existing audits

| Document | Relationship |
|----------|--------------|
| `prototype_settings_v2.html` | Visual/IA reference where not superseded |
| `results/262_settings_harmonization_audit.md` | Engineering inventory — **subordinate** to this spec for product decisions |
| `results/114_settings_doctrine_capture_v1.md` | Nav IA — align; stub rows must converge to §0 truth law |
| `results/273_product_owner_comparison_settings_notes_audit.md` | PO findings — Settings stubs violate §0 until wired or marked SOON |

When 262 or prototype conflicts with this spec, **this spec wins** for V1 product behavior.

---

## 15. Acceptance — V1 Settings “done”

Settings V1 is **product-complete** when:

- [ ] Every visible control satisfies §0 (truth law)
- [ ] Orb/aspect UI matches §3–§5 (no Strict/Normal/Generous)
- [ ] Sort surfaces use only §2 options
- [ ] Dignities section matches §6
- [ ] Saved-object management surfaces exist for §10 types
- [ ] Composite creation follows §11 without profile mutation
- [ ] Export remains contextual per §12
- [ ] No emoji glyphs; glyph library deferred per §9
- [ ] Visual language unchanged from current instrument Settings chrome

---

*End of Settings V1 Product Spec.*
