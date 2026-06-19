# W2-NOTES-0: Notes Library Doctrine v1

**Status:** Authoritative product doctrine (capture only)  
**Date:** 2026-06-16  
**Type:** Doctrine / requirements capture — no implementation authorized by this document  
**Ticket:** W2-NOTES-0 (capture) → W2-NOTES-1 (future implementation)

---

## Purpose

Define how notes work in the relocation product: where they are authored, how they are scoped, how the Notes Library is structured, and what v1 must not become. This document does not authorize code changes.

---

## 1. Contextual authoring (not free-floating notes)

Notes are **authored in context**, not as general scratchpad entries.

### Authoring surfaces

| Surface | Context |
|---------|---------|
| Chart Record / Profile | Profile-scoped record notes |
| Relocated Location | Notes tied to a relocated chart / place view |
| Saved Location | Notes on a favorited or saved place |
| Comparison | Notes on a comparison set or workspace |
| Saved Investigation / Saved Search | Notes on an investigation or search artifact |
| City Intelligence | Notes on city-intel surfaces |
| Map exploration | Notes from map exploration workflow |

**Rule:** Every note originates from a workflow object. There is no standalone “new note” that exists without a parent entity.

---

## 2. Notes Library is management, not a notebook

The Notes Library is a **management and search surface**, not a general writing app or personal notebook.

### Master scope: selected profile

- **Selected profile is the master scope.**
- A user sees notes **only for the selected profile**.
- The library answers: *“What notes exist for this profile’s work?”*

### Do not build

- Cross-profile aggregations (e.g. “all Boston notes” across every profile).
- Global note feeds unrelated to profile selection.

### Correct model

```
Profile (selected)
  └── all notes connected to that profile's work
        ├── profile notes
        ├── saved location notes
        ├── relocated chart notes
        ├── comparison notes
        ├── investigation notes
        ├── city intelligence notes
        └── map notes
```

---

## 3. No general scratchpad (Web2)

- **No general scratchpad for Web2.**
- Every note must belong to an object:
  - profile
  - location
  - comparison
  - investigation
  - city intel
  - map search / exploration
- **Avoid** creating a free-form notebook or writing app inside the relocation app.

---

## 4. Notes Library structure (preferred v1 layout)

Three-column layout:

| Column | Role |
|--------|------|
| **Left** | File cabinets / note categories |
| **Middle** | Searchable note list |
| **Right** | Large editor for selected note |

### Middle column list items

Each row shows:

- Title
- Object type (category)
- Related object (e.g. place name, comparison title)
- First-line preview
- Updated time

### File cabinets (categories)

1. Profile
2. Saved Locations
3. Relocated Charts
4. Comparisons
5. Saved Searches / Investigations
6. City Intelligence
7. Map Notes

Selecting a cabinet filters the middle column to that note type (within the selected profile scope).

---

## 5. Search and filtering

### Searchable fields

- Title
- Body
- Related place name
- Comparison name
- Note type

### Sort options (v1)

- Recently updated
- Name
- Note type

### Deferred

- **Location distance** sort — later only; not required for v1.

---

## 6. Actions

Per note:

| Action | v1 |
|--------|-----|
| Open | Yes |
| Edit | Yes |
| Save | Yes |
| Rename / title | Yes |
| Archive | Yes (preferred over hard delete) |
| Delete | Later; **archive preferred** |

---

## 7. Design doctrine

### Avoid

- “File cabinet” visual ugliness (literal skeuomorphic cabinets, cheesy metaphors).
- Corny carousel patterns unless separately prototyped and approved.
- Cheesy rotating library gimmicks for Web2.

### v1 posture

- **Simple and restrained.**
- Clear categories, readable list, focused editor.

### Future visual idea (not v1)

One active cabinet may **expand** while inactive cabinets **collapse** — explore only after v1 ships and only if a separate prototype validates the pattern.

---

## 8. AI future (out of scope for v1)

Later, AI may **summarize or search user notes only**.

**Example query:**

> “Summarize my Southeast Asia notes about career and education.”

### AI boundaries

| Allowed | Not allowed |
|---------|-------------|
| User-memory synthesis | Astrological interpretation |
| Search/summarize over user’s own notes | Implicit chart judgment from notes AI |

Astrological interpretation belongs elsewhere and only when **explicitly invoked** — not from Notes Library AI.

---

## 9. Relationship to Settings

- **Notes do NOT belong in Settings.**
- **Notes do NOT belong in My Data** (per Settings doctrine v1).
- Settings may list **data controls** (export, archive policies, etc.) but **not** note authoring or editing.
- Note authoring/editing belongs to:
  - Workflow surfaces (contextual), and
  - **Notes Library** (management).

---

## 10. Acceptance criteria for W2-NOTES-1

A v1 Notes Library implementation is **acceptable** when:

1. **Selected profile scopes all notes** — no cross-profile leakage in the library UI.
2. **Note categories are visible** — file-cabinet column (or equivalent restrained filter) matches doctrine categories.
3. **Note list is searchable** — title, body, related names, type per §5.
4. **Selecting a note opens an editor** — right column (or equivalent focused edit surface).
5. **Existing note saves are preserved** — no regression to current persistence paths for contextual notes.
6. **No free-floating general notebook** — every note remains tied to a parent object; no scratchpad mode.

---

## General notes

| Topic | Doctrine |
|-------|----------|
| W2-NOTES-0 | This capture document only |
| W2-NOTES-1 | First implementation slice against §10 |
| Web2 scope | Contextual notes + library management; not a writing product |
| Delete vs archive | Prefer archive; hard delete deferred |
| Cross-profile search | Explicitly out of scope |
| Settings / My Data | Notes excluded from both as authoring homes |

---

## Traceability

| Related doc | Relationship |
|-------------|--------------|
| `results/114_settings_doctrine_capture_v1.md` | My Data excludes notes; Settings excludes notes |
| W2-SETTINGS-1 nav framework | Unaffected by this capture |
