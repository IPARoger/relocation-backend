# Product Screen and Transition Architecture

## Status

**CANONICAL** for Phase 3 strategic product architecture.

Defines **screen hierarchy**, **navigation**, and **transition rules** for the professional non-AI MVP. Not a visual mockup. Not implementation.

**Reads with:** `docs/product_workflows/professional_non_ai_workflow_v1.md`, `docs/data_model/local_first_data_objects_v1.md`, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`.

---

## Purpose

Ensure every screen **supports the map** and **gets out of the way**. Prevent dashboard creep, orphaned admin flows, and transitions that orphan validation habits.

---

## Information architecture (top level)

```text
                    ┌─────────────────┐
                    │  Account shell   │
                    │  (auth, billing  │
                    │   future)        │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Client list    Settings /      Help / docs
                         orbs (L2)
              │
              ▼
        Client dashboard (home for one client)
              │
     ┌────────┼────────┬─────────────┐
     ▼        ▼        ▼             ▼
   Map     Favorites  Comparisons  Chart record
 explore              workspace    (full natal +
                                      relocated)
```

**Sacred object:** Map exploration screen. All other screens are **supporting cast**.

---

## Screen catalog

### S0 — Account overview (future hardening)

- client list,
- recent investigations across clients,
- account-level settings entry.

**Tone:** calm professional library, not SaaS dashboard grid.

### S1 — Client dashboard (client home)

**Primary job:** resume work on one client.

Contains:

- client identity + birth data summary,
- birth-time confidence indicator (when applicable),
- **Open map** primary action,
- recent investigations,
- favorite cities strip,
- comparison drafts,
- export/share history (future).

**Does not contain:** condition editor as primary surface (that lives on map).

### S2 — Map exploration (primary)

**Layout doctrine:**

- map = maximum viewport,
- controls collapse / drawer / genie (see UI doctrine),
- location search on **map chrome**, not competing sidebar block,
- condition stack accessible but recessive,
- layer mute/solo/NOT in compact control strip or drawer.

**Entry paths:**

- from client dashboard,
- from saved investigation,
- from share/deep link (semantic replay required).

**Exit paths:**

- save investigation,
- add favorite from popup or search,
- open full chart (S4),
- open comparison (S3).

### S3 — Comparison workspace

**Off-map dense surface.**

Supports:

- N cities × 1 chart (MVP),
- future N charts × M cities,
- side-by-side relocated tables,
- explicit tradeoff rows — tension preserved.

**Transition rule:** comparison selections originate from map favorites or explicit city pick — not hidden auto-ranking.

### S4 — Full chart / relocated record

**Authoritative dense truth** for one location + one natal profile.

- aspect tables,
- house breakdown,
- angle lines,
- metadata (timezone, place ID, computation assumptions).

Popup (S2) is **shorthand** of S4, not a competing dialect.

### S5 — Settings / ontology (Layer 2)

- house system,
- tropical/sidereal (Layer 1 display choice — must recompute, not fudge),
- orb defaults,
- visible minor aspects,
- helper layer toggles,
- ontology pack selection (future plugins).

**Rule:** changing settings may invalidate open investigations; UI must say so clearly.

### S6 — Birth data intake / edit

Beautiful, trustworthy forms:

- date, time, place,
- timezone/DST integrity (P3 product-critical),
- confidence tier selection,
- explicit warnings for uncertain time.

Intake may happen **before** first map visit; pre-map idle may warm cache **without** assuming immutable chart state.

### S7 — Export / share modal

Scoped outputs:

- viewport PNG,
- investigation link (semantic),
- client packet (future PDF).

Never export renderer debug artifacts as product truth.

---

## Transition matrix

| From | To | Trigger | State carried |
|------|-----|---------|---------------|
| S1 | S2 | Open map | `clientId`, optional `investigationId` |
| S2 | S1 | Back / done | auto-save investigation draft rules TBD |
| S2 | S4 | Full chart from popup | `clientId`, `placeId` or lat/lon |
| S2 | S3 | Compare favorites | selected place IDs |
| S2 | S7 | Export | viewport + investigation semantics |
| S1 | S6 | Edit birth data | `clientId` |
| S6 | S2 | Save & explore | refreshed chart domain |
| Any | S2 | Deep link | must hydrate conditions + viewport + chart |

**Forbidden transitions:**

- silent chart switch without confirmation,
- deep link that restores pixels but not conditions,
- settings change without invalidation notice.

---

## Mobile / tablet posture

**Honest positioning:** desktop-first professional instrument for MVP.

| Breakpoint | Rule |
|------------|------|
| **Tablet** | map-first; bottom sheet or compact drawer for conditions |
| **Phone** | map-first; progressive disclosure; long-press for point truth (planned) |

Do not claim mobile parity until inspect gesture exists.

---

## Collapse and progressive disclosure

**Genie-into-corner doctrine (target, not MVP-day-one):**

- full condition stack collapses to corner affordance,
- restore control always visible,
- map never loses geographic context during collapse animation,
- no mystery-meat icon-only controls for essential search.

**Deferral criteria (current):** drawer/genie redesign waits until design system + flexible condition rows + map search placement are proven (`docs/ux_principles_and_emotional_tone.md` §6).

Until then: **compress sidebar**, do not animated-shell rewrite.

---

## Renderer and map screen boundary

The map screen **does not own**:

- astrology math changes,
- renderer substrate promotion,
- cache architecture experiments.

Production map remains `legacy_search_regions` unless explicit gated promotion with rollback (`docs/EXECUTIVE_TRANSFER_BRIEF_NEXT_CHAT.md` §4).

**Frozen renderer architecture** — do not reopen for aesthetics:

- transported-material doctrine,
- side-local proportional scaling,
- orthogonal slice doctrine,
- embedded ridge doctrine.

Reopen only on map-context validation proving **structural failure** (centerline drift, broken side-local scaling, label collapse, pane-order impossibility).

---

## UI clutter risks

| Risk | Guard |
|------|-------|
| Sidebar becomes permanent Photoshop panel | Drawer with quick actions only |
| Legend consumes map | Controls echo colors; legend shrinks or dies |
| Status/debug copy in production | `?debugGeometry` gating only |
| Multiple competing search fields | One map-native location search |
| Account chrome bleeds onto map | Separate shells; map route is clean |

---

## Missing abstractions (to implement later)

1. **Navigation state machine** — explicit `AppRoute` + investigation hydration contract
2. **Investigation dirty flag** — unsaved condition changes vs saved replay
3. **Invalidation banner** — Layer 2 settings changed; re-run search
4. **Deep link schema** — versioned URL params for semantic replay
5. **Client ACL model** — who may view/export (future)

---

## First implementation note

Screen architecture should land as **routes + empty shells + state contracts** before visual polish. No screen gets premium animation before map truth regression suite exists.

---

## Source consolidation

| Topic | Prior art |
|-------|-----------|
| Screen priority | `docs/relocation_app_product_roadmap.md` §6, §8 |
| Sidebar → map search | `docs/current_sidebar_ux_audit.md` §10 |
| Drawer deferral | `ai_context/decisions.md`, `docs/ux_principles_and_emotional_tone.md` |
| Chart-centric product | `docs/EXECUTIVE_TRANSFER_BRIEF_NEXT_CHAT.md` §6 |
| Truth hierarchy per surface | `docs/visual_semantic_style_guide.md` §1 |
