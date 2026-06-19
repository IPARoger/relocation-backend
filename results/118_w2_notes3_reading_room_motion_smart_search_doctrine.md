# W2-NOTES-3: Reading Room / Observatory Room UX Doctrine

**Status:** Authoritative product doctrine (capture only)  
**Date:** 2026-06-16  
**Type:** UX doctrine extension — no implementation authorized by this document  
**Builds on:**

- `results/115_w2_notes_library_doctrine_v1.md` (W2-NOTES-0)
- `results/116_w2_notes1_notes_library_v1.md` (W2-NOTES-1 implementation baseline)
- `results/117_w2_notes2_notes_library_ux_refinement_doctrine.md` (W2-NOTES-2)

---

## Purpose

Extend the Notes Library doctrine with the refined **Reading Room / Observatory Room** UX direction: mental model, main navigation, elastic proportions and motion, visual tone, and future smart-search boundaries.

This document does **not** authorize UI implementation, `app_shell.html` changes, or backend work.

---

## 1. Mental Model Refinement

### What Notes is not

- Not a clerical file cabinet
- Not document management
- Not an administrative records surface

### What Notes is

The Notes Library is the app's **Reading Room** / **Observatory Room**.

It is where user **imagination, reflection, research, and decision creativity** combine.

| Surface family | Character |
|----------------|-----------|
| Comparison / tables pages | Analytic, structured, evaluative |
| Notes Library | Reflective, generative, contemplative |

The Notes page should feel **more contemplative and creative** than comparison and table workspaces — while maintaining **continuity with the product** through a **subtle mood shift**, not a different app.

### Relationship to W2-NOTES-2

W2-NOTES-2 framed Notes as a **research library**. W2-NOTES-3 refines that frame:

- **Research library** → what the user is doing (gathering knowledge)
- **Reading Room / Observatory** → how it should feel (reflective space for sense-making)

Both frames are compatible. This document adds emotional and spatial character without changing authoring or scoping rules.

---

## 2. Main Navigation

### Doctrine

Notes Library should eventually have its **own top-level Chrome / main-menu entry**.

It must **not** live only as a link buried inside Chart Record or Profile.

### Rationale

- Notes span profile work across locations, comparisons, investigations, and map exploration
- Users return to Notes for reflection across sessions — entry should match that habit
- Profile remains the **scope**; navigation should not imply Notes is a sub-panel of Profile management

### Implementation note (future)

Top-level nav coexists with contextual authoring surfaces. Workflow surfaces create notes; the Reading Room manages them.

---

## 3. Dynamic Proportions and Motion

### Elastic three-column layout

Explore **elastic** three-column layouts within **Fibonacci-ish / harmonic** proportion ranges.

Columns breathe — they do not snap like rigid panels.

### Motion principles

| Principle | Requirement |
|-----------|---------------|
| Pace | Slow grow/shrink; human-scale, weighted, calm |
| Avoid | Fast, disorienting shifts; instant “flying file cabinet” changes |
| Clarity | Lots of information moving quickly is bad UX |
| Readability | User must be able to read and understand what changed during a transition |

### Suggested focus states

| State | Collections | Browser | Editor | Use |
|-------|-------------|---------|--------|-----|
| **Library / Browse focus** | Visible | Prominent | Present | Search and discovery |
| **Selected-note focus** | Visible | Narrows | Grows | Note selected; reading begins |
| **Writing focus** | Slim | Slim contextual list | Dominant | Active composition/editing |

W2-NOTES-2 suggested ~20/35/45 (library) and ~15/15/70 (writing). W2-NOTES-3 treats those as **anchors within a harmonic range**, not fixed pixels. Implementation may interpolate between states.

### Workflow invariant

Proportion changes are **layout and emphasis only**. No change to:

- Where notes are authored
- Save semantics
- Profile scoping
- Collection-as-filter behavior

---

## 4. Visual Tone

### Desired character

**Slightly goofy professorial work environment:**

- Comfortable
- Warm
- Contemplative
- Lightly creative

### Avoid

- Silly, cartoonish, or childish
- Corporate or bureaucratic
- Literal filing cabinets, folders, carousels
- Paper textures, fake notebooks, bookshelf graphics
- Evernote-style clutter (from W2-NOTES-2)

### Acceptable influence (diluted)

A subtle **reading room / observatory / studio desk** feeling — atmospheric, not skeuomorphic.

### Product continuity

Notes should be **distinct in mood** from Settings, My Data, and analytic tables — yet **clearly the same product** (typography family, spacing logic, calm information density).

---

## 5. Smart Search Doctrine (Future)

### Intent

Future search should support **semantic / geographic grouping** beyond literal string match.

**Example:**

> Searching **"Asia"** surfaces notes related to Bali, Tokyo, Mumbai, etc., even when individual notes are not tagged "Asia."

### Boundaries

| Rule | Detail |
|------|--------|
| Scope | **Profile-scoped only** — smart search never crosses profiles |
| Isolation | No notes, favorites, or custom locations from one user/profile bleeding into another |
| Timing | Future capability — **not W2-NOTES-3 implementation** unless trivially additive |
| AI role | Retrieval/grouping over user content — not interpretation (see §6) |

### Relationship to W2-NOTES-1 search

W2-NOTES-1 implements client-side filter on title, body, related names, and type. Smart search is a **later layer** on the same profile boundary.

---

## 6. Future AI (Reaffirmed)

Future AI may **synthesize user-authored notes only**.

**Example:**

> "Summarize career-related observations for Southeast Asia."

| Allowed | Not allowed |
|---------|-------------|
| Summarize/search user note content and metadata | Astrological interpretations |
| User-memory synthesis | External analysis injected into note bodies |
| Profile-scoped retrieval | Cross-profile inference |

Notes remain **user-authored knowledge**.

---

## Acceptance Criteria (Future Mockup / Implementation)

A Reading Room implementation pass is doctrine-aligned when:

1. **All Notes** remains the default collection.
2. **Collections remain filters** (not isolated silos), with counts where applicable.
3. **Center column** remains the active browser/search surface.
4. **Editor becomes dominant** in writing focus (browser reduces to slim contextual list).
5. **Motion is calm and human-scale** — transitions slow enough to read; no disorienting panel flight.
6. **Mood is distinct** from Settings/Data and analytic tables, but product-continuous.
7. **Search remains profile-scoped**; no cross-profile leakage.
8. **No scratchpad** — every note tied to a parent object.
9. **No AI interpretation** in Notes UX unless explicitly invoked elsewhere; future synthesis is note-content-only.
10. **Top-level navigation** entry for Notes Library is planned or present (not Chart Record–only burial).
11. **Smart search** (if shipped) respects geographic/semantic grouping within profile scope only.

---

## Traceability Matrix

| Topic | W2-NOTES-0 | W2-NOTES-1 | W2-NOTES-2 | W2-NOTES-3 (this doc) |
|-------|------------|------------|------------|------------------------|
| Contextual authoring | ✓ authoritative | implemented | preserved | preserved |
| Profile master scope | ✓ | implemented | preserved | preserved |
| No scratchpad | ✓ | implemented | preserved | preserved |
| Three-column desktop | — | implemented | refined | elastic + motion |
| All Notes default | — | Profile default | All Notes default | reaffirmed |
| Research library metaphor | — | — | ✓ | → Reading Room / Observatory |
| Focus modes | — | — | Library / Writing % | + Selected-note; harmonic motion |
| Main nav entry | — | Chart Record link | — | top-level Chrome |
| Smart search | — | string filter | global + filter | future semantic/geo |
| Visual tone | avoid cabinets | restrained | research-oriented | professorial, contemplative |

---

## Out of Scope (This Capture)

- `app_shell.html` or any UI implementation
- Backend / search index / embedding infrastructure
- Smoke tests
- Archive/delete flows
- Cross-profile features
- Astrology math or interpretation in Notes AI
