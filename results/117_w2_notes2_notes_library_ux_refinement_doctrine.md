# W2-NOTES-2: Notes Library UX Refinement Doctrine

**Status:** Authoritative product doctrine (capture only)  
**Date:** 2026-06-16  
**Type:** UX refinement doctrine — builds on W2-NOTES-0 / W2-NOTES-1; no implementation authorized by this document  
**Supersedes:** Visual and interaction tone in W2-NOTES-1 where this document is more specific; does **not** supersede contextual authoring or profile-scoping rules from `results/115_w2_notes_library_doctrine_v1.md`

---

## Purpose

Refine the Notes Library experience beyond the W2-NOTES-1 structural implementation while preserving the doctrine that notes are **authored in workflow context** and **managed from a centralized library**.

---

## Core Mental Model

The Notes Library is **not** a collection of filing cabinets.

The Notes Library is the user's **research library**.

Users are gathering:

- observations
- relocation ideas
- comparisons
- city intelligence
- long-term decision-making research

The experience should feel like **browsing and editing a personal research collection** rather than managing files.

| Wrong frame | Right frame |
|-------------|-------------|
| Document management | Research collection |
| Filing cabinets | Library browser + desk |
| Administrative records | Curiosity and exploration |

---

## Layout (Desktop)

Desktop layout remains **three-column**.

### Left Column — Collections

**Purpose:** Scope and filter the library.

Collections act as **filters**, not isolated filing systems.

**Default landing state:** **All Notes**

| Collection | Role |
|------------|------|
| All Notes | Default; shows entire profile-scoped library |
| Profile Notes | Filter to profile / chart-record notes |
| Saved Locations | Filter to saved-location notes |
| Relocated Charts | Filter to relocated-chart notes |
| Comparisons | Filter to comparison notes |
| Saved Searches / Investigations | Filter to investigation notes |
| City Intelligence | Filter to city-intel notes |
| Map Notes | Filter to map exploration notes |

**Display note counts** beside each collection label.

Example:

```
All Notes (84)
Profile Notes (3)
Saved Locations (29)
Relocated Charts (12)
Comparisons (18)
Saved Searches (9)
City Intelligence (11)
Map Notes (2)
```

Counts reflect the **selected profile scope** only.

---

### Center Column — Library Browser

**Purpose:** Browse and locate notes.

The center column is **not** a passive preview pane. It is the **active note browser**.

Contains:

- Search field
- Search results
- Sort controls
- Note metadata

**Example entries:**

```
Tokyo Career Research
Saved Location · Tokyo, Japan
Updated Yesterday
```

```
Singapore vs Tokyo
Comparison
Updated 3 Days Ago
```

**Search field** searches globally within the selected profile:

- Note title
- Note body
- Place names
- Comparison names
- Investigation names
- Note type metadata

**Search is global.** Collections **further filter** search results (collection ∩ search).

---

### Right Column — Editor

**Purpose:** Read and edit the selected note.

Contains:

- Title
- Metadata
- Related object reference
- Note editor
- Save controls

This should be the **largest working area**.

| Metaphor | Column |
|----------|--------|
| Bookshelf | Center (browser) |
| Desk | Right (editor) |

---

## Dynamic Focus Modes

The Notes Library should support **lightweight focus shifting**. Layout change only — **no workflow changes**.

### Library Focus

Used when searching and browsing.

Approximate column proportions:

| Collections | Browser | Editor |
|-------------|---------|--------|
| 20% | 35% | 45% |

### Writing Focus

Used when actively editing.

Approximate column proportions:

| Collections | Browser | Editor |
|-------------|---------|--------|
| 15% | 15% | 70% |

Users should move naturally between **discovery** and **writing** without leaving the page.

---

## Visual Personality

The page should **not** feel bureaucratic, corporate, heavy, or administrative.

### Avoid

- Filing cabinet metaphors
- Folder trees
- Bookshelf graphics
- Rotating carousels
- Skeuomorphic office imagery
- Evernote-style clutter

### Desired tone

- Thoughtful
- Exploratory
- Slightly lighter
- Approachable
- Research-oriented

The page should feel like a place for **curiosity and exploration** rather than document management.

A small amount of **warmth, softness, and visual friendliness** is encouraged.

The goal is **subtle emotional lightness** — not humor or novelty.

---

## Mobile Doctrine

Mobile **abandons** the three-column layout.

**Flow:**

```
Collections → Results → Editor
```

Each stage occupies the full screen.

Back navigation returns to the previous stage.

The experience should feel **natural and native** rather than compressed desktop UI.

---

## Future AI Support

Future AI note synthesis may summarize **user-authored notes only**.

**Example:**

> "Summarize career-related observations for Southeast Asia."

### AI boundaries

| Allowed | Not allowed |
|---------|-------------|
| Summarize/search user note content | Astrological interpretations |
| Use note metadata for scoping | External analysis injected into summaries |
| User-memory synthesis | Implicit chart judgment |

Notes remain **user-authored knowledge**. AI is a retrieval/synthesis layer over that knowledge — not an astrology engine.

---

## Relationship to Prior Doctrine

| Document | Relationship |
|----------|--------------|
| `results/115_w2_notes_library_doctrine_v1.md` | Authoritative for contextual authoring, profile scope, no scratchpad, categories |
| `results/116_w2_notes1_notes_library_v1.md` | W2-NOTES-1 structural baseline; UX refinement deferred here |
| This document | Authoritative for mental model, proportions, focus modes, visual tone, mobile flow |

### Preserved from W2-NOTES-0 / W2-NOTES-1

- Notes authored in context (not created as free-floating scratchpad entries)
- Selected profile is master scope
- No cross-profile “all Boston notes”
- Notes do not belong in Settings or My Data
- No general notebook for Web2

### Changed / refined by W2-NOTES-2

- **All Notes** as default collection (W2-NOTES-1 defaulted to Profile)
- Collection labels reframed (e.g. “Profile Notes” vs “Profile”)
- Note counts in left column
- Explicit Library Focus vs Writing Focus proportions
- Stronger research-library mental model and visual personality guidance
- Mobile three-stage flow defined

---

## Acceptance (for future W2-NOTES-2 implementation)

A UX refinement pass is doctrine-aligned when:

1. Default collection is **All Notes** with accurate per-category counts.
2. Center column behaves as an **active browser** (search, sort, rich list metadata) — not a passive preview.
3. Right column is visually dominant in **Writing Focus** (~70% editor).
4. **Library Focus** (~20 / 35 / 45) is available for browse/search sessions.
5. Search is global within profile; collections filter results.
6. Visual design avoids filing-cabinet / corporate / Evernote clutter; tone is research-oriented and lightly warm.
7. Mobile uses Collections → Results → Editor full-screen stages with back navigation.
8. No scratchpad, no workflow change to contextual authoring, no Settings placement.
9. No AI in v2 implementation unless explicitly scoped; future AI respects note-only boundaries.

---

## Out of scope (this capture)

- Implementation in `app_shell.html`
- New note types or backend schema
- Archive/delete flows
- Cross-profile search
- Astrology interpretation in any form
