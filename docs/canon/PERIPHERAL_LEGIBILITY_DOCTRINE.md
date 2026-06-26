# Peripheral Legibility & Transparent Interface Doctrine

**Status:** Foundational design doctrine (D2)  
**Date:** 2026-06-27  
**Type:** Visual philosophy — not an implementation spec, not a color audit  
**Authority:** Subordinate to [FOUNDATIONAL_CONSTITUTION.md](../constitutional/FOUNDATIONAL_CONSTITUTION.md). Connects [INTERFACE_AND_DESIGN_CANON.md](../product/INTERFACE_AND_DESIGN_CANON.md) and [MATERIAL_SYSTEM_CANON.md](MATERIAL_SYSTEM_CANON.md).  
**Scope:** How the interface should feel when read, ignored, and returned to — across every surface of the product.

---

## 0. What this document is

The constitution says **Reveal structure. Preserve judgment.** The interface canon says how screens, workflows, and semantic layers obey that law. The material canon says what surfaces are made of — stone, paper, glass, glow.

This doctrine sits between them. It answers a different question:

> *How should the interface behave in the user's attention?*

Not: what color is the button?  
Not: which screen owns which control?  
But: when the user is looking at a chart, a comparison, a map, or a note — what should the chrome do?

**Answer:** It should remain transparent to the subject. The beauty comes from symbols, archetypes, relationships, discoveries, and the user's own insight — not from interface ornamentation. The interface should enhance perception. It should never compete for it.

---

## 1. Core principle: transparent to the subject

A relocation instrument is read for hours. The user's attention belongs to the chart, the table, the map band, the sentence they are writing. The interface is the lens, not the landscape.

Transparency does not mean invisibility. An invisible interface is as arrogant as a loud one — it hides affordances, punishes discovery, and forces memorization. Transparency means the interface **defers**. It holds structure steady so meaning can move. It does not insert itself between the user and what they came to see.

When this works, users describe the product as "calm," "serious," "clear," or "beautiful" — and they mean the *astrology* feels beautiful, not the chrome.

---

## 2. Peripheral legibility

**Peripheral legibility** is the discipline of making every element fully readable when sought, and naturally recessive when not actively examined.

The user should be able to:

- notice an element instantly when they need it, and
- effortlessly ignore it when they do not,

without either state feeling forced.

This is **not** low contrast. It is not gray-on-gray. It is not "subtle" in the sense of hidden. Faded illegibility is a failure mode — it trades one kind of noise for another.

Peripheral legibility is achieved through:

| Lever | Role |
|-------|------|
| **Hierarchy** | Primary subject reads first; chrome reads last |
| **Spacing** | Density where data lives; air where structure breathes |
| **Rhythm** | Repeated intervals so the eye learns the grid once |
| **Restrained color** | Color encodes meaning, not mood |
| **Visual weight** | Heavy marks for data; light marks for structure |
| **Proportion** | Type and icons sized to their informational job |
| **Typography** | Reading surfaces use reading type; controls use control type |
| **Breathing room** | Margins that let symbols and numbers exist without crowding |

The test is behavioral: can a user work for forty minutes without feeling nagged — and still find every control in two seconds when they look for it?

---

## 3. No "Look at me"

Reject interface elements that continually request attention.

Avoid:

- decorative animation
- unnecessary glow
- loud gradients
- heavy borders
- oversized icons
- visual gimmicks
- novelty for its own sake

Nothing should say **"Look at me."**

Instead it quietly says **"I'm here when you need me."**

A map overlay encoding an exact aspect line *should* be assertive — it is subject matter, not chrome. A save button should not pulse. **Spectacle belongs to the astrology, not the furniture.** Motion confirms state change at human pace; it does not perform enthusiasm.

---

## 4. Energy comes from within

The emotional energy of the application comes from:

- the astrology
- the discoveries
- the archetypes
- the comparisons
- the user's curiosity

The interface simply reveals them.

Do not manufacture excitement through ornament. A dramatic gradient behind a table does not make the table more true. A glowing border around a settings card does not make settings more important. The product earns feeling when a user sees a condition they did not expect — when two cities diverge, when a dignity pattern repeats, when a note crystallizes a judgment they were circling.

The interface's job is to **stay out of the way of that moment**.

This aligns with the constitution: the system reveals structure; the human supplies meaning. Ornament that manufactures emotion is a soft form of hidden authority — it suggests how the user should feel about what they see.

---

## 5. Application by surface

The following sections describe how peripheral legibility applies across the product. They do not prescribe pixels or tokens — see MATERIAL_SYSTEM_CANON for material roles and INTERFACE_AND_DESIGN_CANON for screen law.

### Glyphs

Glyphs are primary subject matter. They should read crisply at table density and wheel scale. The Relocation Symbol System (see [RELOCATION_SYMBOL_SYSTEM.md](RELOCATION_SYMBOL_SYSTEM.md)) exists so glyphs share stroke weight and proportion — harmony among symbols, not among UI chrome.

Peripheral legibility here means: glyphs are never decorated *around*; they are never animated for delight; variant pickers in Settings show glyphs as specimens, not as marketing tiles.

### Diff tables

Comparison diffs exist to make sameness and difference legible at a glance. The table chrome — headers, dividers, row hover — should recede. The cell content — planet, house, aspect, dignity wash — should lead.

Duplicate fades, late-house markers, and dignity tints are informational ink. They may be stronger than surrounding paper because they *are* the reading. The table frame should not shout louder than the cell that changed.

### Settings

Settings are administrative. They are important when configuring; they should not haunt the user during inspection. Peripheral legibility means: clear section hierarchy, honest Coming Soon labels, no fake switches, no decorative palette theater.

When Settings are open, they earn full attention. When closed, they leave no visual afterimage on chart surfaces. Appearance and glyph controls affect downstream surfaces — they should be curated and calm, not gamified.

### Notes

Notes are immersive reading surfaces. Typography leads; chrome follows. The notes field should feel like paper on stone — not like a comment widget in a social app.

Pop-out notes use glass separation (see Material canon) — transient, not ornamental. The user's words are the subject; the frame exists so they can write without leaving context.

### Chart wheels

Wheels are symbolic diagrams. Aspects, bodies, and angles are the vocabulary. Wheel chrome — ticks, rims, labels — should be precise and quiet. Aspect lines may be visually stronger than the rim because they encode relationship.

Do not animate the wheel to impress. Do not add gratuitous depth or faux-3D. The wheel should feel like an instrument face: legible, stable, trustworthy.

### City Intelligence

City Intelligence is reference prose — neutral, factual, subordinate to chart truth. It should read like a well-set paragraph in a field guide, not like a marketing card.

Peripheral legibility: CI panels sit beside inspection without stealing the column that holds chart facts. Headlines are modest; body copy breathes.

### Map overlays

Overlays are a special case. They **may** be visually stronger than surrounding chrome — because they are geographic encodings of chart structure, not interface decoration.

Pinwheels, aspect bands, exact lines, and exclusion fills carry meaning on the map canvas. They should be clear, distinguishable, and calm — not neon, not pulsing, not gradient-stacked for drama. The map ground stays geographic; overlays are legible ink on top.

The Genie and explore controls remain peripheral: available, readable, recessive until invoked.

### Help

Help explains; it does not perform. Copy is plain. Layout is generous. No mascot energy, no illustration clutter unless it teaches structure.

Help should feel as though it could be printed — timeless, scannable, respectful of the user's intelligence.

### Popups

Popups are glass — transient separation. They appear with purpose, dismiss without ceremony. Content inside a popup follows the same hierarchy as its parent surface: subject first, actions second, chrome last.

Avoid stacked shadows, animated entrances, and decorative headers. A popup is a temporary reading room, not a stage.

### Buttons

Buttons signal affordance, not personality. Primary actions are clear; secondary actions are quieter; destructive actions are honest without theatrics.

A button should not be the most colorful thing on the screen unless the screen is empty. On a chart page, the chart wins.

### Tables

Tables are the backbone of inspection — AIS, PIH, A2A, comparison columns. Row rhythm and column alignment do the work. Zebra striping, if used, is a whisper. Borders are structural, not decorative.

Numbers and glyphs align so the eye can travel down a column without friction. Peripheral legibility in tables is the difference between "spreadsheet" and "instrument readout."

---

## 6. Why overlays may be stronger than chrome

This doctrine rejects spectacle in the interface — but it does **not** demand that everything be equally faint.

**Chrome** (toolbars, section headers, settings cards, navigation) should recede.  
**Subject ink** (glyphs, aspect lines, map fills, diff highlights, dignity washes) may be stronger — because it is what the user came to read.

If an element encodes astrological structure, it may claim more weight; if it encodes software structure, it should not. When overlays feel loud, quiet the chrome — not the ink. Strong overlays on a calm map are correct.

---

## 7. Timelessness

The interface should feel as though it could have existed years ago and still feel appropriate years from now.

Avoid fashionable styling:

- trend gradients
- novelty radii
- decorative glass for its own sake
- "AI product" aesthetics
- excessive roundness or excessive sharpness as a brand pose

Prefer enduring clarity:

- consistent grids
- readable type
- materials that age well (warm paper, settled stone)
- symbols that outlive UI fashion

Timelessness is not nostalgia. It is **restraint in the service of long sessions** — the user who returns daily for years should not feel dated, and should not feel fatigued.

---

## 8. Relationship to existing canon

| Canon | What it owns | What this doctrine adds |
|-------|--------------|-------------------------|
| [FOUNDATIONAL_CONSTITUTION](../constitutional/FOUNDATIONAL_CONSTITUTION.md) | Epistemic law — reveal structure, preserve judgment | *How attention should flow* so judgment stays human |
| [INTERFACE_AND_DESIGN_CANON](../product/INTERFACE_AND_DESIGN_CANON.md) | Screen hierarchy, workflows, semantic layers | *Visual philosophy* for why chrome defers to subject |
| [MATERIAL_SYSTEM_CANON](MATERIAL_SYSTEM_CANON.md) | Stone, paper, glass, glow — material roles | *Legibility posture* — when materials speak loudly vs quietly |

This document does not duplicate their requirements. It connects them:

- The constitution protects meaning.
- The interface canon organizes surfaces.
- The material canon names what surfaces are made of.
- **Peripheral legibility** names how those surfaces behave in attention.

Implementation tokens, hex values, motion curves, and component specs belong in future work — not here.

---

## 9. Review questions

Use these when evaluating any new UI work:

1. Is the subject matter visually louder than the chrome around it?
2. Can every control be found in two seconds when looked for — and ignored when not?
3. Does anything say "Look at me" without encoding structure?
4. Is color doing informational work, or decorative work?
5. Would this still feel appropriate in ten years?
6. Does the design manufacture emotion, or reveal something the user can feel for themselves?

If the answer to (3) or (6) is wrong, revise — regardless of how polished the mockup looks.

---

## 10. One sentence

**The interface should disappear into thought — and reappear instantly on demand.**

That is peripheral legibility. That is transparent to the subject. That is how an astrological geography instrument earns long trust.

---

*D2 — documentation only. No implementation.*
