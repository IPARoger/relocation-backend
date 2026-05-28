# Map Drawer and Layer Control Doctrine

## Status

**CANONICAL** for Phase 3 strategic product architecture.

Defines **map-primary control hierarchy**, **drawer/collapse behavior**, and **layer interaction semantics**. Not a component spec. Not implementation.

**Reads with:** `docs/overlay_and_aura_visual_strategy.md` §H, `docs/current_sidebar_ux_audit.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/visual_semantic_style_guide.md` §9, `docs/product_workflows/product_screen_and_transition_architecture.md`.

---

## Purpose

Keep the **map sacred**. Controls must:

- support exploration,
- collapse away,
- restore obviously,
- survive mobile,
- avoid Photoshop panel chaos.

---

## Control hierarchy (map screen)

Priority order — highest wins when space is constrained:

| Priority | Control | Placement target |
|----------|---------|------------------|
| 1 | **Map viewport** | full available area |
| 2 | **Point inspect affordance** | implicit (right-click hint) |
| 3 | **Location search** | map chrome, top-center, translucent |
| 4 | **Primary search action** | visible without scroll on laptop |
| 5 | **Condition list** | drawer / side rail |
| 6 | **Layer mute/solo/NOT** | compact strip or drawer section |
| 7 | **Legend** | deprecate in favor of control color echo |
| 8 | **Debug / status** | `?debugGeometry` only |

**Rule:** if a control hides coastlines, labels, or overlap evidence, it fails.

---

## Drawer architecture (target)

### Zones

```text
┌──────────────────────────────────────────────┐
│  [Location search ────────────────]   [≡]   │  ← map chrome
│                                              │
│                                              │
│              MAP (sacred)                    │
│                                              │
│                                              │
│                                    ┌──────┐  │
│                                    │ genie│  │  ← collapsed affordance
│                                    └──────┘  │
└──────────────────────────────────────────────┘

Expanded drawer (side or bottom sheet):
  - Client/chart context (compact)
  - Add condition
  - Condition cards (color-tinted)
  - Layer mixer (mute/solo/NOT)
  - Find regions / run search
```

### Genie-into-corner collapse

When user collapses controls:

1. drawer animates to **corner chip** (not off-screen death),
2. chip shows **active condition count** + alert dot if dirty,
3. **one tap** restores prior drawer height,
4. map resize is smooth; no layout jump that loses cursor context,
5. no auto-collapse on timer — user owns chrome.

**Non-goals:** gimmick animations, physics toys, hidden controls with no restore.

### Deferral (current phase)

Full drawer/genie is **deferred** until:

- flexible **Add condition** rows exist (API coordinated),
- map-native location search shipped,
- design system tokens for spacing/type/color exist.

**Until then:** compress fixed sidebar per audit; do not rewrite map shell.

---

## Condition editor doctrine

### Target model

Each row = one semantic condition:

- planet in house,
- angle in sign,
- aspect to angle,
- NOT variant.

**No dummy rows** to satisfy legacy A/B/C payload shape.

### Card visual language

- tinted card echoes overlay color (legend by control),
- calm typography,
- delete/edit inline,
- exclusion rows use muted/warning family — not alarm red.

### Search action

- single primary **Find regions** / **Update map**,
- no auto-advance dropdown chains,
- no user-facing debug strings (“Angular overlay ready”).

---

## Layer mixer doctrine

Treat layers as **audio tracks**, not GIS stack tables.

| Action | Semantics | Default UX |
|--------|-----------|------------|
| **Mute** | hide visually; stays in investigation | tap icon |
| **Solo** | isolate temporarily | long-press or menu |
| **Restore all** | undo solo | explicit button |
| **Send to background** | lower visual priority | advanced menu |
| **Send to foreground** | raise for inspection | advanced menu |
| **NOT / exclusion** | deprioritized veil | separate row type |

**Principles:**

- dissect overlap, do not prohibit multi-variable search,
- no astrological ranking implied by foreground,
- NOT uses desaturating veil — not inverse glow (`docs/overlay_and_aura_visual_strategy.md` §C).

### Mobile layer controls

- compact drawer or bottom sheet,
- tap layer → inspect,
- long-press → mute/solo,
- never expose full stack at once,
- goal: **quick focus**, not graphics-stack management.

---

## Map-native affordances

| Affordance | Rule |
|------------|------|
| **Reset map** | top-right map control; restores default center/zoom |
| **Right-click truth** | session onboarding card; optional future veil |
| **Zoom** | native Leaflet; no custom gimmick |
| **Basemap** | calm; labels sacred under overlays |

Location search **leaves sidebar** permanently in target architecture.

---

## Renderer interaction boundary

Layer controls affect **display visibility and stacking only**.

They must **not**:

- change Layer 1 membership,
- trigger silent renderer substrate switch,
- mutate canonical overlay registries in production,
- persist mute state as astrological truth.

**Frozen renderer core** (no reopen for aesthetics):

- transported-material doctrine,
- side-local proportional scaling,
- orthogonal slice doctrine,
- embedded ridge doctrine.

Palette, overlap compositing, child colors, pane order after validation — **flexible**.

---

## UI clutter anti-patterns

| Anti-pattern | Why rejected |
|--------------|--------------|
| Permanent legend panel | wastes map; controls echo colors |
| Full-height fixed sidebar | hides overlap evidence |
| Photoshop layer panel | mobile failure; cognitive load |
| Status badges in production | debug only |
| Custom selects without a11y | audit flagged |
| Tutorial tour/coach marks | onboarding = one map hint |
| Rainbow default palette | proof-of-concept only (§J overlay doc) |

---

## Accessibility notes (planned)

- keyboard path to run search and toggle mute,
- focus trap only inside open drawer — map remains pannable,
- long-press = point truth on touch devices (open question until spec'd),
- color semantics not solely hue-dependent (texture/icon backup for overlap).

---

## Missing abstractions

1. **`LayerDisplayState`** — mute/solo/z-order per condition ID
2. **`DrawerLayoutState`** — expanded/collapsed/height preset
3. **`ConditionDirtyFlag`** — unsaved vs running investigation
4. **Mobile gesture map** — inspect vs pan disambiguation

---

## Validation method

UI slices prove:

- collapse/restore preserves condition state,
- mute/solo does not alter API payload unless explicitly designed,
- overlap readable at 1280×800 with drawer collapsed,
- screenshot regression fixtures unchanged for truth regions.

---

## Source consolidation

| Topic | Prior art |
|-------|-----------|
| Mixer model | `docs/overlay_and_aura_visual_strategy.md` §H |
| Sidebar audit | `docs/current_sidebar_ux_audit.md` |
| Drawer deferral | `docs/ux_principles_and_emotional_tone.md` §6 |
| Review contract risk | `docs/review_contracts_and_governance.md` §4 |
| Renderer freeze | `docs/EXECUTIVE_TRANSFER_BRIEF_NEXT_CHAT.md` §4.1 |
