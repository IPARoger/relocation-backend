# MATERIAL_SYSTEM_CANON.md

**Status:** Canonical material and visual-language reference.  
**Version:** D1 (2026-06-26)  
**Type:** Material audit — not a color audit, not an implementation spec.  
**Authority:** Subordinate to `FOUNDATIONAL_CONSTITUTION.md`, `INTERFACE_AND_DESIGN_CANON.md`, and `UI_STANDARDIZATION_CANON_v1_2026-06-12.md`.  
**Companion:** `results/263_material_system_delta.md`  
**Revision policy:** Hex values and CSS tokens belong in future D2 — not here.

**Screens reviewed:** `profile_standard.html`, `relocated_standard.html`, `comparison_v5_beta.html`, `comparison_notes_slot.html`, `material_texture_study.html`, `motion_lab.html`, `map_SANDBOX_genie_v6.html`; production Profile/Relocated/Comparison V5/Settings/Notes in `app_shell.html`; `CITY_INTELLIGENCE_CANON.md`; `tband_foundation.css`, `relocation_themes.css`, `notes_canonical.css`.

---

## 0. Enduring Guidance

> **The interface should disappear into thought.**

Writing, reading, annotating, editing, and reviewing should feel like one continuous activity. The user should never feel they have entered a different "mode." Every page differs in **purpose**, not **visual language**. Materials — not arbitrary colors — carry identity.

---

## 1. Design Philosophy

### 1.1 Instrument, not software

The product is a **beautifully made instrument**: precise, calm, inspectable, worthy of long sessions. Users interact with **information**, not interface. Chrome is furniture.

### 1.2 One reading continuum

Notes, tables, popups, City Intelligence, and Settings are all **reading surfaces**. There is no "editor mode" and no "dashboard mode" — only depth of attention on the same material system.

### 1.3 Quiet vitality

Warmth and depth support decision-making. Treatment is functional infrastructure. Target feel: **premium publishing** + **contemplative instrument** — never office software, GIS theater, or spiritual retail.

### 1.4 Truth hierarchy governs material

| Surface | Posture |
|---------|---------|
| Point inspection | Dense, diagnostic, calm |
| Map overlays | Restrained; encode membership/proximity only |
| Chart tables | Structural; lines + subtle glow |
| Notes | Immersive; typography leads |
| City Intelligence | Neutral reference prose |
| Settings / Help | Administrative; same card families |
| Debug / scaffold | Quarantined; utilitarian |

Constitutional law unchanged: **Reveal structure. Preserve judgment.**

---

## 2. Material Families

Materials are **roles**, not hex values.

### 2.1 Stone — Ground

**Purpose:** Permanence — page atmosphere, authority foundations.  
**Feeling:** Warm mineral, settled — gallery wall, not concrete UI.  
**Lighting:** Soft top-light; no specular highlights.  
**Texture:** Ultra-faint grain at page-ground only.  
**Interaction:** Static; holds everything else.  
**Use:** Chart page ground, comparison workspace, Settings backdrop. **Not:** map geography, table cells.

### 2.2 Paper — Working surface

**Purpose:** Readable cards, tables, notes fields, CI prose.  
**Feeling:** Warm matte sheet.  
**Lighting:** Even; slight lift from Stone.  
**Texture:** Optional linen/cotton weave at row scale for separation only.  
**Interaction:** Soft inset or border on focus — not color flash.  
**Rejected:** Legal pad, ruled lines, leather journal, deckled edges.

### 2.3 Glass — Transient separation

**Purpose:** Dropdowns, popovers, modals, map explore chrome, Notes pop-out.  
**Feeling:** Frosted, lifted window between layers.  
**Lighting:** Soft shadow beneath; interior slightly brighter than ground.  
**Interaction:** Human-paced appear/dismiss; no bounce.  
**Rule:** Persistent content lives on Paper; Glass is temporary.

### 2.4 Ink — Typography and lines

**Purpose:** Everything read or traced.  
**Roles:** Authority (serif names/titles) · Working (values) · Whisper (metadata) · Structural (hairlines, carets).  
**Interaction:** Links may shift weight; body text does not animate.  
**Core Ink** persists across seasonal themes — identity over atmosphere.

### 2.5 Texture — Separation only

**Purpose:** Orientation without decoration. Barely consciously visible.  
**Approved:** Comparison column hatch (~1.4% diagonal, alternating direction); inset hairlines; CI species divider; optional linen row weave (luminance only); map field differentiation at subconscious intensity.  
**Rejected:** GIS striping, zebra fills, hatch spam, emotional shading, decorative grain on wheels.  
**Comparison hatch (locked):** `comparison_v5_beta.html` — differentiates columns without value judgment; do not intensify.  
**Transported material (map):** Exact centerline is spine; aura/strip communicates proximity — subordinate to truth; beta-stabilized, not final aesthetic sign-off.

### 2.6 Shadow — Weight

**Purpose:** Depth and focus.  
**Tiers:** Wheel (highest) · G3 card double-line + ~4% interior glow · Glass overlay soft shadow · Buttons minimal.  
**Rejected:** Neon halos, decorative row shadows, TRON edges.

### 2.7 Accent — Action

**Purpose:** Affordance and orientation — not emotional valence.  
**Use:** Primary actions, selection tint, Share, applying/separating orb ink.  
**Not:** Default table fills, CI prose, dignity semantics, motion color adds.

### 2.8 Status — Information hue

**Purpose:** State and astrology semantics.  
**Families:** Map overlays (12-family) · Dignities two-color · Badges de-pilled · Warnings restrained · NOT redaction · Coming-soon honest badges.

---

## 3. Typography

Typography is the most present material — structure of attention.

### 3.1 Roles

| Role | Face | Job |
|------|------|-----|
| Serif authority | Iowan / Palatino family | Names, card titles, CI headlines |
| Sans workhorse | System UI | Metadata heads, controls, hints |
| Monospace | Rare | Coordinates/debug only |

### 3.2 Reading depths

| Depth | Context | Type job |
|-------|---------|----------|
| Glance | Map chrome | Instant anchors |
| Burst | Popup, CI inline | One settling read |
| Sustained | Comparison, tables | Scan under load — align, no fatigue |
| Immersion | Notes, long CI | Flow — 1.55+ leading |

### 3.3 Rules

- Flush-left serif card titles; no redundant column headers when title exists.
- Uppercase tracked labels for micro-metadata only — not prose.
- Centered name plate (Zone B); Edit/+ are appendages.
- Table row unit ~21px (Fibonacci); Notes ~14.5px / 1.55 leading.
- AiS: centered sign grid; PiH: ordinal + late-house `?`; A2A: abbrev + orb; empty `—`.
- Notes: toolbar **below** editor (`NotesCanonical`); premium publishing, not text-editor chrome.

---

## 4. Texture Doctrine

> Texture creates **separation**, never **decoration.**

If texture is noticed first, it is too strong. Earn-the-line: prefer whitespace when hierarchy is clear (`UI_STANDARDIZATION_CANON` §3). Real divider before City Intelligence — different species from astrology tables.

---

## 5. Chrome

Chrome **recedes** behind content.

| Control | Doctrine |
|---------|----------|
| Buttons | One primary per context; label the object (Edit, Add, Search) |
| Dropdowns | D2 soft card; checkmark + tint; plain carets |
| Sliders | Dim track; bright on hover (map depth model) |
| Carets | Left of title; right=open, down=collapsed, never up |
| Cards | `tcard` + G3; Settings panels same family |
| Popups | Glass; diagnostic calm density |

Map explore: bar dissolves; Genie → bottle square; debug quarantined.

---

## 6. Reading Comfort Doctrine

Long sessions get **easier**, not harder. Optimize: reading, thinking, annotating, comparison, research.

**Avoid:** editor mode, dashboard mode, notebook gimmicks, zebra fatigue, entertainment motion.

**Notes (H7):** warm neutral field, generous margins, quiet toolbar, restrained contrast (`notes_canonical.css`).

---

## 7. Motion

Human-scale furniture. Objects have weight.

- Functional only — explains what appeared and where it went.
- ~0.75× baseline; Genie teaching-paced, desynchronized beats.
- Ease-out or linear — **no acceleration, overshoot, or bounce**.
- Chart motion subtracts color; does not add it.
- Table collapse → caret square; Notes pop-out → continuous morph from button footprint.
- Rain/virga overlay reveal: intent locked, implementation deferred.

---

## 8. Color Philosophy

**No palette here.** Color communicates **information**:

| Domain | Job |
|--------|-----|
| Maps | Membership, exclusion, proximity |
| Tables | Applying/separating; dignities |
| Status | Badges, warnings, NOT |
| Photos (CI) | Geographic reality |
| Accent | Deliberate actions |

Color does **not** decorate backgrounds, rows, comparison winners, or CI prose. Seasonal themes shift atmosphere; Core Ink persists. Overlays must not change Layer 1 membership.

---

## 9. Shared Product Identity

Six rooms, one house: Map · Profile · Relocated · Comparison · Notes · Settings · CI · Help (future).

**Shared DNA:** identity plate grammar · wheel focal tier · G3 cards · Fibonacci spacing · D2 dropdowns · left caret collapse · Notes canonical · earn-the-line.

**Surface tiers** (`surface_treatment_doctrine.md`): (1) wheel focal · (2) stone ground · (3) grouped cards · (4) structural tables · (5) glass transient · (6) scaffold.

| Surface | Alignment |
|---------|-----------|
| Profile / Relocated | Reference — `tband_foundation.css` |
| Comparison V5 | Largely aligned — hatch, G3, notes rail |
| Notes | H7 canonical |
| Settings | H6 converging |
| Map | **Not harmonized** |
| Help | **Not started** |
| CI production | Doctrine ready; UI pending |

---

## 10. Future Palette Pass (D2)

D2 assigns tokens; D1 assigns materials.

**D2 delivers:** semantic material/color tokens; ink steps; theme surface ramps; texture constants; motion durations; button/link formalization; dignity color overrides when consumer exists.

**D2 does not:** change truth geometry; add decoration-only palette; introduce winner/loser comparison colors.

**Inputs:** `relocation_themes.css`, `VERSION_1_COLOR_DOCTRINE.md`, palette/texture studies, colorist pass.

---

## 11. Anti-Patterns

Dashboard grids · notebook skeuomorphism · neon table glow · GIS hatch spam · isolated map chrome · broken settings controls · toolbar-above Notes editor · color as decoration.

---

## 12. Revision Log

| Date | Note |
|------|------|
| 2026-06-26 | D1 initial material canon |
